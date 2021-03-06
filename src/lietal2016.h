/**
 * \file lietal2016.h
 * \brief Definition of the class LietAl2016Solver.
 * \copyright Copyright (c) 2019-2020, Olivier Mesnard. All rights reserved.
 * \license BSD 3-Clause License.
 */

#pragma once

#include <petibm/rigidkinematics/rigidkinematics.h>

class LietAl2016Solver : protected RigidKinematicsSolver
{
public:
    LietAl2016Solver() = default;
    LietAl2016Solver(const MPI_Comm &world, const YAML::Node &node);
    ~LietAl2016Solver();
    PetscErrorCode init(const MPI_Comm &world, const YAML::Node &node);
    PetscErrorCode advance();
    using RigidKinematicsSolver::destroy;
    using RigidKinematicsSolver::write;
    using RigidKinematicsSolver::ioInitialData;
    using RigidKinematicsSolver::finished;

protected:
    PetscInt algo;
    PetscInt scheme;
    PetscBool move;
    PetscReal dV;
    PetscErrorCode scheme1();
    PetscErrorCode scheme2();
    PetscErrorCode scheme3();
    PetscErrorCode scheme4();
    PetscErrorCode algorithm1();
    PetscErrorCode algorithm2();
    PetscErrorCode algorithm3();
    PetscErrorCode writeForcesASCII();

};  // LietAl2016Solver