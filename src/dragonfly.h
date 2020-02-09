/**
 * \file dragonfly.h
 * \brief Definition of the class DragonflySolver.
 * \copyright Copyright (c) 2019-2020, Olivier Mesnard. All rights reserved.
 * \license BSD 3-Clause License.
 */

#pragma once

#include "lietal2016.h"

struct BodyParameters
{
    PetscInt nt_cycle;
    std::string folder;
};  // BodyParameters

class DragonflySolver : public LietAl2016Solver
{
public:
    DragonflySolver() = default;
    DragonflySolver(const MPI_Comm &world, const YAML::Node &node);
    ~DragonflySolver();
    using LietAl2016Solver::destroy;
    using LietAl2016Solver::advance;
    using LietAl2016Solver::write;
    using LietAl2016Solver::ioInitialData;
    using LietAl2016Solver::finished;
    PetscErrorCode init(const MPI_Comm &world, const YAML::Node &node);

protected:
    std::vector<BodyParameters> params;
    std::string datadir;
    PetscInt nt_cycle;
    PetscErrorCode setCoordinatesBodies(const PetscReal &ti);
    PetscErrorCode setVelocityBodies(const PetscReal &ti);

};  // DragonflySolver