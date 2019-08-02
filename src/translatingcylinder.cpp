#include "translatingcylinder.h"

#include <petibm/io.h>

TranslatingCylinderSolver::TranslatingCylinderSolver(const MPI_Comm &world, const YAML::Node & node)
{
    init(world, node);
}  // TranslatingCylinderSolver::TranslatingCylinderSolver

TranslatingCylinderSolver::~TranslatingCylinderSolver()
{
    PetscErrorCode ierr;
    PetscBool finalized;

    PetscFunctionBeginUser;

    ierr = PetscFinalized(&finalized); CHKERRV(ierr);
    if (finalized) return;

    ierr = destroy(); CHKERRV(ierr);
}  // TranslatingCylinderSolver::~TranslatingCylinderSolver

PetscErrorCode TranslatingCylinderSolver::init(const MPI_Comm &world,
                                               const YAML::Node &node)
{
    PetscErrorCode ierr;

    PetscFunctionBeginUser;

    ierr = LietAl2016Solver::init(world, node); CHKERRQ(ierr);

    ierr = PetscLogStagePush(stageInitialize); CHKERRQ(ierr);

    const YAML::Node &config_kin = node["bodies"][0]["kinematics"];
    U0 = config_kin["U0"].as<PetscReal>(0.0);
    V0 = config_kin["V0"].as<PetscReal>(0.0);

    ierr = PetscLogStagePop(); CHKERRQ(ierr);

    PetscFunctionReturn(0);
}  // TranslatingCylinderSolver::init

PetscErrorCode TranslatingCylinderSolver::setCoordinatesBodies(
    const PetscReal &ti)
{
    petibm::type::SingleBody &body = bodies->bodies[0];
    petibm::type::RealVec2D &coords = body->coords;
    petibm::type::RealVec2D &coords0 = body->coords0;

    PetscFunctionBeginUser;

    for (PetscInt k = 0; k < body->nPts; k++)
    {
        coords[k][0] = coords0[k][0] + U0 * ti;
        coords[k][1] = coords0[k][1] + V0 * ti;
    }

    PetscFunctionReturn(0);
} // TranslatingCylinderSolver::setCoordinatesBodies

PetscErrorCode TranslatingCylinderSolver::setVelocityBodies(
    const PetscReal &ti)
{
    PetscErrorCode ierr;
    PetscReal **UB_arr;
    petibm::type::SingleBody &body = bodies->bodies[0];

    PetscFunctionBeginUser;

    // update the boundary velocity array
    ierr = DMDAVecGetArrayDOF(body->da, UB, &UB_arr); CHKERRQ(ierr);
    for (PetscInt k = body->bgPt; k < body->edPt; k++)
    {
        UB_arr[k][0] = U0;
        UB_arr[k][1] = V0;
    }
    ierr = DMDAVecRestoreArrayDOF(body->da, UB, &UB_arr); CHKERRQ(ierr);

    PetscFunctionReturn(0);
} // TranslatingCylinderSolver::setVelocityBodies
