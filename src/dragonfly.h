#pragma once

#include "lietal2016.h"

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
    std::string datadir;
    PetscInt nt_cycle;
    PetscErrorCode setCoordinatesBodies(const PetscReal &ti);
    PetscErrorCode setVelocityBodies(const PetscReal &ti);

};  // DragonflySolver