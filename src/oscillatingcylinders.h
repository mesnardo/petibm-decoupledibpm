/**
 * \file oscillatingcylinders.h
 * \brief Definition of the class OscillatingCylindersSolver.
 * \copyright Copyright (c) 2019-2020, Olivier Mesnard. All rights reserved.
 * \license BSD 3-Clause License.
 */

#pragma once

#include "lietal2016.h"

struct OscillatingCylinder
{
    PetscReal f;
    PetscReal Am;
    PetscReal Um;
    PetscReal Xc0;
    PetscReal Yc0;
};  // OscillatingCylinder

class OscillatingCylindersSolver : public LietAl2016Solver
{
public:
    OscillatingCylindersSolver() = default;
    OscillatingCylindersSolver(const MPI_Comm &world, const YAML::Node &node);
    ~OscillatingCylindersSolver();
    using LietAl2016Solver::destroy;
    using LietAl2016Solver::advance;
    using LietAl2016Solver::write;
    using LietAl2016Solver::ioInitialData;
    using LietAl2016Solver::finished;
    PetscErrorCode init(const MPI_Comm &world, const YAML::Node &node);

protected:
    std::vector<OscillatingCylinder> params;
    PetscErrorCode setCoordinatesBodies(const PetscReal &ti);
    PetscErrorCode setVelocityBodies(const PetscReal &ti);

};  // OscillatingCylindersSolver