#include "lietal2016.h"

LietAl2016Solver::LietAl2016Solver(const MPI_Comm &world,
                                   const YAML::Node &node)
{
    init(world, node);
}  // LietAl2016Solver

LietAl2016Solver::~LietAl2016Solver()
{
    PetscErrorCode ierr;
    PetscBool finalized;

    PetscFunctionBeginUser;

    ierr = PetscFinalized(&finalized); CHKERRV(ierr);
    if (finalized) return;

    ierr = destroy(); CHKERRV(ierr);
}  // ~LietAl2016Solver

PetscErrorCode LietAl2016Solver::init(const MPI_Comm &world,
                                      const YAML::Node &node)
{
    PetscErrorCode ierr;

    PetscFunctionBeginUser;

    ierr = RigidKinematicsSolver::init(world, node); CHKERRQ(ierr);

    ierr = PetscLogStagePush(stageInitialize); CHKERRQ(ierr);

    algo = 1;
    scheme = 3;
    if (node["parameters"]["lietal2016"])
    {
        const YAML::Node &decoupling = node["parameters"]["lietal2016"];
        algo = decoupling["algo"].as<PetscInt>(1);
        scheme = decoupling["scheme"].as<PetscInt>(3);
    }

    if (node["bodies"][0]["kinematics"])
        move = PETSC_TRUE;
    
    dV = 1.0;
    petibm::type::SingleBody &body = bodies->bodies[0];
    petibm::type::IntVec1D idx = body->meshIdx[0];
    for (PetscInt d = 0; d < mesh->dim; ++d)
        dV *= mesh->dL[3][d][idx[d]];

    ierr = PetscLogStagePop(); CHKERRQ(ierr);

    PetscFunctionReturn(0);
}  // init

PetscErrorCode LietAl2016Solver::advance()
{
    PetscErrorCode ierr;

    PetscFunctionBeginUser;
    
    t += dt;
    ite++;

    if (move)
    {
        ierr = moveBodies(t); CHKERRQ(ierr);
    }

    switch (scheme)
    {
        case 1:
            ierr = scheme1(); CHKERRQ(ierr);
            break;
        case 2:
            ierr = scheme2(); CHKERRQ(ierr);
            break;
        case 3:
            ierr = scheme3(); CHKERRQ(ierr);
            break;
        case 4:
            ierr = scheme4(); CHKERRQ(ierr);
            break;
        default:
            SETERRQ(comm, PETSC_ERR_ARG_UNKNOWN_TYPE,
                    "Unknown value for the scheme. "
                    "Accepted values are 1, 2, 3, and 4");
    }

    switch (algo)
    {
        case 1:
            ierr = algorithm1(); CHKERRQ(ierr);
            break;
        case 2:
            ierr = algorithm2(); CHKERRQ(ierr);
            break;
        case 3:
            ierr = algorithm3(); CHKERRQ(ierr);
            break;
        default:
            SETERRQ(comm, PETSC_ERR_ARG_UNKNOWN_TYPE,
                    "Unknown value for the algorithm. "
                    "Accepted values are 1, 2, and 3");
    }

    ierr = bc->updateGhostValues(solution); CHKERRQ(ierr);

    PetscFunctionReturn(0);
}  // advance

PetscErrorCode LietAl2016Solver::scheme1()
{
    PetscErrorCode ierr;

    PetscFunctionBeginUser;

    // f = 0
    ierr = VecSet(f, 0.0); CHKERRQ(ierr);

    PetscFunctionReturn(0);
}  // scheme1

PetscErrorCode LietAl2016Solver::scheme2()
{
    PetscFunctionBeginUser;

    // use the forces from the previous time step

    PetscFunctionReturn(0);
}  // scheme2

PetscErrorCode LietAl2016Solver::scheme3()
{
    PetscErrorCode ierr;

    PetscFunctionBeginUser;

    // solve EBNH f = -E u
    ierr = MatMult(E, solution->UGlobal, rhsf); CHKERRQ(ierr);
    ierr = VecScale(rhsf, -1.0); CHKERRQ(ierr);
    ierr = VecAYPX(rhsf, 1.0, UB); CHKERRQ(ierr);
    ierr = fSolver->solve(f, rhsf); CHKERRQ(ierr);

    PetscFunctionReturn(0);
}  // scheme3

PetscErrorCode LietAl2016Solver::scheme4()
{
    PetscErrorCode ierr;

    PetscFunctionBeginUser;

    // solve EBNH f = -E \tilde{u}
    // where \tilde{u} is the solution from an explicit time advancement
    // without momentum forcing
    Vec uTilde;
    ierr = VecDuplicate(solution->UGlobal, &uTilde); CHKERRQ(ierr);
    ierr = MatMult(G, solution->pGlobal, rhs1); CHKERRQ(ierr);
    ierr = VecScale(rhs1, -1.0); CHKERRQ(ierr);
    ierr = VecAXPY(rhs1, convCoeffs->explicitCoeffs[0], conv[0]); CHKERRQ(ierr);
    ierr = VecAXPY(rhs1, diffCoeffs->explicitCoeffs[0], diff[0]); CHKERRQ(ierr);
    ierr = VecWAXPY(uTilde, dt, rhs1, solution->UGlobal); CHKERRQ(ierr);

    ierr = MatMult(E, uTilde, rhsf); CHKERRQ(ierr);
    ierr = VecScale(rhsf, -1.0); CHKERRQ(ierr);
    ierr = VecAYPX(rhsf, 1.0, UB); CHKERRQ(ierr);
    ierr = fSolver->solve(f, rhsf); CHKERRQ(ierr);

    ierr = VecDestroy(&uTilde); CHKERRQ(ierr);

    PetscFunctionReturn(0);
}  // scheme4

PetscErrorCode LietAl2016Solver::algorithm1()
{
    PetscErrorCode ierr;
    
    PetscFunctionBeginUser;

    ierr = assembleRHSVelocity(); CHKERRQ(ierr);
    ierr = solveVelocity(); CHKERRQ(ierr);
    
    ierr = assembleRHSForces(); CHKERRQ(ierr);
    ierr = solveForces(); CHKERRQ(ierr);
    ierr = applyNoSlip(); CHKERRQ(ierr);

    ierr = assembleRHSPoisson(); CHKERRQ(ierr);
    ierr = solvePoisson(); CHKERRQ(ierr);
    ierr = applyDivergenceFreeVelocity(); CHKERRQ(ierr);

    ierr = updatePressure(); CHKERRQ(ierr);
    ierr = updateForces(); CHKERRQ(ierr);

    PetscFunctionReturn(0);
}  // algorithm1


PetscErrorCode LietAl2016Solver::algorithm2()
{
    PetscErrorCode ierr;
    
    PetscFunctionBeginUser;

    ierr = assembleRHSVelocity(); CHKERRQ(ierr);
    ierr = solveVelocity(); CHKERRQ(ierr);
    
    ierr = assembleRHSForces(); CHKERRQ(ierr);
    ierr = solveForces(); CHKERRQ(ierr);

    // enforce no-slip condition by solving another system for the velocity
    ierr = MatMultAdd(H, df, rhs1, rhs1); CHKERRQ(ierr);
    ierr = vSolver->solve(solution->UGlobal, rhs1); CHKERRQ(ierr);

    ierr = assembleRHSPoisson(); CHKERRQ(ierr);
    ierr = solvePoisson(); CHKERRQ(ierr);
    ierr = applyDivergenceFreeVelocity(); CHKERRQ(ierr);

    ierr = updatePressure(); CHKERRQ(ierr);
    ierr = updateForces(); CHKERRQ(ierr);

    PetscFunctionReturn(0);
}  // algorithm2

PetscErrorCode LietAl2016Solver::algorithm3()
{
    PetscErrorCode ierr;
    
    PetscFunctionBeginUser;

    ierr = assembleRHSVelocity(); CHKERRQ(ierr);
    ierr = solveVelocity(); CHKERRQ(ierr);

    ierr = assembleRHSPoisson(); CHKERRQ(ierr);
    ierr = solvePoisson(); CHKERRQ(ierr);
    ierr = applyDivergenceFreeVelocity(); CHKERRQ(ierr);

    ierr = assembleRHSForces(); CHKERRQ(ierr);
    ierr = solveForces(); CHKERRQ(ierr);
    ierr = applyNoSlip(); CHKERRQ(ierr);

    ierr = updatePressure(); CHKERRQ(ierr);
    ierr = updateForces(); CHKERRQ(ierr);

    PetscFunctionReturn(0);
}  // algorithm3

PetscErrorCode LietAl2016Solver::writeForcesASCII()
{
    PetscErrorCode ierr;
    petibm::type::RealVec1D fAvg(3, 0.0);
    Vec fEuler;
    std::vector<Vec> fEulerUnpacked(mesh->dim);

    PetscFunctionBeginUser;

    ierr = PetscLogStagePush(stageIntegrateForces); CHKERRQ(ierr);

    ierr = VecDuplicate(solution->UGlobal, &fEuler); CHKERRQ(ierr);
    ierr = MatMult(H, f, fEuler); CHKERRQ(ierr);

    ierr = DMCompositeGetAccessArray(mesh->UPack, fEuler, mesh->dim, nullptr,
                                     fEulerUnpacked.data()); CHKERRQ(ierr);
    for (PetscInt d = 0; d < mesh->dim; ++d)
    {
        ierr = VecSum(fEulerUnpacked[d], &fAvg[d]); CHKERRQ(ierr);
        fAvg[d] *= -dV;
    }
    ierr = DMCompositeRestoreAccessArray(mesh->UPack, fEuler, mesh->dim, nullptr,
                                         fEulerUnpacked.data()); CHKERRQ(ierr);
    ierr = VecDestroy(&fEuler); CHKERRQ(ierr);

    ierr = PetscLogStagePop(); CHKERRQ(ierr);  // end of stageIntegrateForces

    ierr = PetscLogStagePush(stageWrite); CHKERRQ(ierr);

    // write the time value
    ierr = PetscViewerASCIIPrintf(forcesViewer, "%10.8e\t", t); CHKERRQ(ierr);

    // write forces
    for (PetscInt d = 0; d < mesh->dim; ++d)
    {
        ierr = PetscViewerASCIIPrintf(
            forcesViewer, "%10.8e\t", fAvg[d]); CHKERRQ(ierr);
    }
    ierr = PetscViewerASCIIPrintf(forcesViewer, "\n"); CHKERRQ(ierr);

    ierr = PetscLogStagePop(); CHKERRQ(ierr);  // end of stageWrite

    PetscFunctionReturn(0);
}  // writeForcesASCII
