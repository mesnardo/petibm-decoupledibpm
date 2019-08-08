#include "oscillatingsphere.h"

#include <petibm/io.h>

OscillatingSphereSolver::OscillatingSphereSolver(
    const MPI_Comm &world, const YAML::Node & node)
{
    init(world, node);
}  // OscillatingSphereSolver::OscillatingSphereSolver

OscillatingSphereSolver::~OscillatingSphereSolver()
{
    PetscErrorCode ierr;
    PetscBool finalized;

    PetscFunctionBeginUser;

    ierr = PetscFinalized(&finalized); CHKERRV(ierr);
    if (finalized) return;

    ierr = destroy(); CHKERRV(ierr);
}  // OscillatingSphereSolver::~OscillatingSphereSolver

PetscErrorCode OscillatingSphereSolver::init(const MPI_Comm &world,
                                             const YAML::Node &node)
{
    PetscErrorCode ierr;

    PetscFunctionBeginUser;

    ierr = LietAl2016Solver::init(world, node); CHKERRQ(ierr);

    ierr = PetscLogStagePush(stageInitialize); CHKERRQ(ierr);

    const YAML::Node &config_kin = node["bodies"][0]["kinematics"];
    f = config_kin["f"].as<PetscReal>(0.0);
    Am = config_kin["Am"].as<PetscReal>(0.0);
    Um = 2.0 * PETSC_PI * f * Am;
    Xc0 = config_kin["center"][0].as<PetscReal>(0.0);
    Yc0 = config_kin["center"][1].as<PetscReal>(0.0);
    Zc0 = config_kin["center"][2].as<PetscReal>(0.0);

    ierr = PetscLogStagePop(); CHKERRQ(ierr);

    PetscFunctionReturn(0);
}  // OscillatingSphereSolver::init

PetscErrorCode OscillatingSphereSolver::setCoordinatesBodies(
    const PetscReal &ti)
{
    PetscReal Xd,  // displacement in the x-direction
              Yd,  // displacement in the y-direction
              Zd;  // displacement in the z-direction
    petibm::type::SingleBody &body = bodies->bodies[0];
    petibm::type::RealVec2D &coords = body->coords;
    petibm::type::RealVec2D &coords0 = body->coords0;

    PetscFunctionBeginUser;

    // compute the displacement
    Xd = Am * PetscSinReal(2*PETSC_PI * f * ti);
    Yd = 0.0;
    Zd = 0.0;

    for (PetscInt k = 0; k < body->nPts; k++)
    {
        coords[k][0] = coords0[k][0] + Xd;
        coords[k][1] = coords0[k][1] + Yd;
        coords[k][2] = coords0[k][2] + Zd;
    }

    PetscFunctionReturn(0);
} // OscillatingSphereSolver::setCoordinatesBodies

PetscErrorCode OscillatingSphereSolver::setVelocityBodies(
    const PetscReal &ti)
{
    PetscErrorCode ierr;
    PetscReal Ux;  // translation velocity in x-direction
    PetscReal **UB_arr;
    petibm::type::SingleBody &body = bodies->bodies[0];

    PetscFunctionBeginUser;

    // compute the translational velocity at current time
    Ux = Um * PetscCosReal(2 * PETSC_PI * f * ti);
    // update the boundary velocity array
    ierr = DMDAVecGetArrayDOF(body->da, UB, &UB_arr); CHKERRQ(ierr);
    for (PetscInt k = body->bgPt; k < body->edPt; k++)
    {
        UB_arr[k][0] = Ux;
        UB_arr[k][1] = 0.0;
        UB_arr[k][2] = 0.0;
    }
    ierr = DMDAVecRestoreArrayDOF(body->da, UB, &UB_arr); CHKERRQ(ierr);

    PetscFunctionReturn(0);
} // OscillatingSphereSolver::setVelocityBodies
