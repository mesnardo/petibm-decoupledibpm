/**
 * \file oscillatingcylinders.cpp
 * \brief Implementation of the class OscillatingCylindersSolver.
 * \copyright Copyright (c) 2019-2020, Olivier Mesnard. All rights reserved.
 * \license BSD 3-Clause License.
 */

#include "oscillatingcylinders.h"

#include <petibm/io.h>

OscillatingCylindersSolver::OscillatingCylindersSolver(const MPI_Comm &world, const YAML::Node & node)
{
    init(world, node);
}  // OscillatingCylindersSolver::OscillatingCylindersSolver

OscillatingCylindersSolver::~OscillatingCylindersSolver()
{
    PetscErrorCode ierr;
    PetscBool finalized;

    PetscFunctionBeginUser;

    ierr = PetscFinalized(&finalized); CHKERRV(ierr);
    if (finalized) return;

    ierr = destroy(); CHKERRV(ierr);
}  // OscillatingCylinderSolver::~OscillatingCylinderSolver

PetscErrorCode OscillatingCylindersSolver::init(const MPI_Comm &world,
                                                const YAML::Node &node)
{
    PetscErrorCode ierr;

    PetscFunctionBeginUser;

    ierr = LietAl2016Solver::init(world, node); CHKERRQ(ierr);

    ierr = PetscLogStagePush(stageInitialize); CHKERRQ(ierr);

    const YAML::Node &config_bodies = node["bodies"];
    PetscInt nBodies = config_bodies.size();
    params.resize(nBodies);
    for (std::size_t i = 0; i < nBodies; ++i)
    {
        const YAML::Node &config_body = config_bodies[i]["kinematics"];
        params[i].f = config_body["f"].as<PetscReal>(0.0);
        PetscReal Dc = config_body["D"].as<PetscReal>(1.0);
        PetscReal KC = config_body["KC"].as<PetscReal>(0.0);
        params[i].Am = Dc * KC / (2.0 * PETSC_PI);
        params[i].Um = 2.0 * PETSC_PI * params[i].f * params[i].Am;
        params[i].Xc0 = config_body["center"][0].as<PetscReal>(0.0);
        params[i].Yc0 = config_body["center"][1].as<PetscReal>(0.0);
    }

    ierr = PetscLogStagePop(); CHKERRQ(ierr);

    PetscFunctionReturn(0);
}  // OscillatingCylindersSolver::init

PetscErrorCode OscillatingCylindersSolver::setCoordinatesBodies(
    const PetscReal &ti)
{
    PetscReal Xd,  // displacement in the x-direction
              Yd;  // displacement in the y-direction
    petibm::type::SingleBody &body = bodies->bodies[0];
    petibm::type::RealVec2D &coords = body->coords;
    petibm::type::RealVec2D &coords0 = body->coords0;

    PetscFunctionBeginUser;

    for (size_t i = 0; i < bodies->nBodies; ++i)
    {
        Xd = - params[i].Am * PetscSinReal(2 * PETSC_PI * params[i].f * ti);
        Yd = 0.0;

        petibm::type::SingleBody &body = bodies->bodies[i];
        petibm::type::RealVec2D &coords = body->coords;
        petibm::type::RealVec2D &coords0 = body->coords0;

        for (PetscInt k = 0; k < body->nPts; k++)
        {
            coords[k][0] = coords0[k][0] + Xd;
            coords[k][1] = coords0[k][1] + Yd;
        }
    }

    PetscFunctionReturn(0);
} // OscillatingCylindersSolver::setCoordinatesBodies

PetscErrorCode OscillatingCylindersSolver::setVelocityBodies(
    const PetscReal &ti)
{
    PetscErrorCode ierr;
    PetscInt nBodies = bodies->nBodies;
    PetscReal Ux;  // translation velocity in x-direction
    std::vector<Vec> unPacked(nBodies);
    PetscReal **UB_arr;

    PetscFunctionBeginUser;

    ierr = DMCompositeGetAccessArray(
        bodies->dmPack, UB, nBodies, nullptr, unPacked.data()); CHKERRQ(ierr);
    for (size_t i = 0; i < nBodies; ++i)
    {
        petibm::type::SingleBody &body = bodies->bodies[i];
        Ux = - params[i].Um * PetscCosReal(2 * PETSC_PI * params[i].f * ti);
        ierr = DMDAVecGetArrayDOF(
            body->da, unPacked[i], &UB_arr); CHKERRQ(ierr);
        for (PetscInt k = body->bgPt; k < body->edPt; ++k)
        {
            UB_arr[k][0] = Ux;
            UB_arr[k][1] = 0.0;
        }
        ierr = DMDAVecRestoreArrayDOF(
            body->da, unPacked[i], &UB_arr); CHKERRQ(ierr);
    }

    ierr = DMCompositeRestoreAccessArray(
        bodies->dmPack, UB, nBodies, nullptr, unPacked.data()); CHKERRQ(ierr);

    PetscFunctionReturn(0);
} // OscillatingCylindersSolver::setVelocityBodies
