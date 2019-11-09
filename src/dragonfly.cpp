#include <iomanip>

#include <petibm/io.h>

#include "dragonfly.h"

DragonflySolver::DragonflySolver(
    const MPI_Comm &world, const YAML::Node & node)
{
    init(world, node);
}  // DragonflySolver::DragonflySolver

DragonflySolver::~DragonflySolver()
{
    PetscErrorCode ierr;
    PetscBool finalized;

    PetscFunctionBeginUser;

    ierr = PetscFinalized(&finalized); CHKERRV(ierr);
    if (finalized) return;

    ierr = destroy(); CHKERRV(ierr);
}  // DragonflySolver::~DragonflySolver

PetscErrorCode DragonflySolver::init(const MPI_Comm &world,
                                     const YAML::Node &node)
{
    PetscErrorCode ierr;

    PetscFunctionBeginUser;

    ierr = LietAl2016Solver::init(world, node); CHKERRQ(ierr);

    ierr = PetscLogStagePush(stageInitialize); CHKERRQ(ierr);

    const YAML::Node &config_kin = node["bodies"][0]["kinematics"];
    std::string simudir = node["directory"].as<std::string>();
    datadir = simudir + "/" + config_kin["folder"].as<std::string>();
    nt_cycle = config_kin["nt_cycle"].as<PetscInt>();

    ierr = PetscLogStagePop(); CHKERRQ(ierr);

    PetscFunctionReturn(0);
}  // DragonflySolver::init

PetscErrorCode DragonflySolver::setCoordinatesBodies(const PetscReal &ti)
{
    PetscErrorCode ierr;
    std::string filepath;
    std::stringstream ss;
    PetscInt n = ite % nt_cycle;
    petibm::type::SingleBody &body = bodies->bodies[0];
    PetscInt numPts;

    PetscFunctionBeginUser;

    // load body coordinates from file
    ss << std::setfill('0') << std::setw(7) << n;
    filepath = datadir + "/position_" + ss.str() + ".txt";
    ierr = petibm::io::readLagrangianPoints(filepath, numPts, body->coords);

    PetscFunctionReturn(0);
} // DragonflySolver::setCoordinatesBodies

PetscErrorCode DragonflySolver::setVelocityBodies(const PetscReal &ti)
{
    PetscErrorCode ierr;
    petibm::type::RealVec2D UB_vec;
    PetscReal **UB_arr;
    petibm::type::SingleBody &body = bodies->bodies[0];
    std::string filepath;
    std::stringstream ss;
    PetscInt n = ite % nt_cycle;
    PetscInt numPts;

    PetscFunctionBeginUser;

    // load velocity data from file
    ss << std::setfill('0') << std::setw(7) << n;
    filepath = datadir + "/velocity_" + ss.str() + ".txt";
    ierr = petibm::io::readLagrangianPoints(filepath, numPts, UB_vec);

    // update the boundary velocity array
    ierr = DMDAVecGetArrayDOF(body->da, UB, &UB_arr); CHKERRQ(ierr);
    for (PetscInt k = body->bgPt; k < body->edPt; k++)
    {
        for (PetscInt d = 0; d < body->dim; d++)
            UB_arr[k][d] = UB_vec[k][d];
    }
    ierr = DMDAVecRestoreArrayDOF(body->da, UB, &UB_arr); CHKERRQ(ierr);

    PetscFunctionReturn(0);
} // DragonflySolver::setVelocityBodies
