/**
 * \file dragonfly.cpp
 * \brief Implementation of the class DragonflySolver.
 * \copyright Copyright (c) 2019-2020, Olivier Mesnard. All rights reserved.
 * \license BSD 3-Clause License.
 */

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

    const YAML::Node &config_bodies = node["bodies"];
    PetscInt nBodies = config_bodies.size();
    params.resize(nBodies);
    std::string simudir = node["directory"].as<std::string>();
    for (std::size_t i = 0; i < nBodies; ++i)
    {
        const YAML::Node &config_body = config_bodies[i]["kinematics"];
        params[i].nt_cycle = config_body["nt_cycle"].as<PetscInt>();
        params[i].folder = simudir + "/" +
                           config_body["folder"].as<std::string>();
    }

    ierr = PetscLogStagePop(); CHKERRQ(ierr);

    PetscFunctionReturn(0);
}  // DragonflySolver::init

PetscErrorCode DragonflySolver::setCoordinatesBodies(const PetscReal &ti)
{
    PetscErrorCode ierr;

    PetscFunctionBeginUser;

    // load body coordinates from file
    for (size_t i = 0; i < bodies->nBodies; ++i)
    {
        PetscInt n = ite % params[i].nt_cycle;
        std::stringstream ss;
        ss << std::setfill('0') << std::setw(7) << n;
        petibm::type::SingleBody &body = bodies->bodies[i];
        std::string filepath;
        filepath = params[i].folder + "/position_" + ss.str() + ".txt";
        PetscInt numPts;
        ierr = petibm::io::readLagrangianPoints(filepath, numPts, body->coords);
    }

    PetscFunctionReturn(0);
} // DragonflySolver::setCoordinatesBodies

PetscErrorCode DragonflySolver::setVelocityBodies(const PetscReal &ti)
{
    PetscErrorCode ierr;
    PetscInt nBodies = bodies->nBodies;
    std::vector<Vec> unPacked(nBodies);
    PetscReal **UB_arr;

    PetscFunctionBeginUser;

    // update the boundary velocity array
    ierr = DMCompositeGetAccessArray(
        bodies->dmPack, UB, nBodies, nullptr, unPacked.data()); CHKERRQ(ierr);

    for (size_t i = 0; i < nBodies; ++i)
    {
        petibm::type::SingleBody &body = bodies->bodies[i];
        // load velocity data from file
        PetscInt n = ite % params[i].nt_cycle;
        std::stringstream ss;
        ss << std::setfill('0') << std::setw(7) << n;
        std::string filepath;
        filepath = params[i].folder + "/velocity_" + ss.str() + ".txt";
        petibm::type::RealVec2D UB_vec;
        PetscInt numPts;
        ierr = petibm::io::readLagrangianPoints(filepath, numPts, UB_vec);
        ierr = DMDAVecGetArrayDOF(
            body->da, unPacked[i], &UB_arr); CHKERRQ(ierr);
        for (PetscInt k = body->bgPt; k < body->edPt; ++k)
        {
            for (PetscInt d = 0; d < body->dim; d++)
                UB_arr[k][d] = UB_vec[k][d];
        }
        ierr = DMDAVecRestoreArrayDOF(
            body->da, unPacked[i], &UB_arr); CHKERRQ(ierr);
    }

    ierr = DMCompositeRestoreAccessArray(
        bodies->dmPack, UB, nBodies, nullptr, unPacked.data()); CHKERRQ(ierr);

    PetscFunctionReturn(0);
} // DragonflySolver::setVelocityBodies
