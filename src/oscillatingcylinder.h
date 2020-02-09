/**
 * \file oscillatingcylinder.h
 * \brief Definition of the class OscillatingCylinderSolver.
 * \copyright Copyright (c) 2019-2020, Olivier Mesnard. All rights reserved.
 * \license BSD 3-Clause License.
 */

#pragma once

#include "lietal2016.h"

class OscillatingCylinderSolver : public LietAl2016Solver
{
public:
    OscillatingCylinderSolver() = default;
    OscillatingCylinderSolver(const MPI_Comm &world, const YAML::Node &node);
    ~OscillatingCylinderSolver();
    using LietAl2016Solver::destroy;
    using LietAl2016Solver::advance;
    using LietAl2016Solver::write;
    using LietAl2016Solver::ioInitialData;
    using LietAl2016Solver::finished;
    PetscErrorCode init(const MPI_Comm &world, const YAML::Node &node);

protected:
    PetscReal f;
    PetscReal Am;
    PetscReal Um;
    PetscReal Xc0;
    PetscReal Yc0;
    PetscErrorCode setCoordinatesBodies(const PetscReal &ti);
    PetscErrorCode setVelocityBodies(const PetscReal &ti);

};  // OscillatingCylinderSolver