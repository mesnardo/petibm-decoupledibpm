/**
 * \file translatingcylinder.h
 * \brief Definition of the class TranslatingCylinderSolver.
 * \copyright Copyright (c) 2019-2020, Olivier Mesnard. All rights reserved.
 * \license BSD 3-Clause License.
 */

#pragma once

#include "lietal2016.h"

class TranslatingCylinderSolver : public LietAl2016Solver
{
public:
    TranslatingCylinderSolver() = default;
    TranslatingCylinderSolver(const MPI_Comm &world, const YAML::Node &node);
    ~TranslatingCylinderSolver();
    using LietAl2016Solver::destroy;
    using LietAl2016Solver::advance;
    using LietAl2016Solver::write;
    using LietAl2016Solver::ioInitialData;
    using LietAl2016Solver::finished;
    PetscErrorCode init(const MPI_Comm &world, const YAML::Node &node);

protected:
    PetscReal U0;
    PetscReal V0;
    PetscErrorCode setCoordinatesBodies(const PetscReal &ti);
    PetscErrorCode setVelocityBodies(const PetscReal &ti);

};  // TranslatingCylinderSolver