#pragma once

#include "lietal2016.h"

class OscillatingSphereSolver : public LietAl2016Solver
{
public:
    OscillatingSphereSolver() = default;
    OscillatingSphereSolver(const MPI_Comm &world, const YAML::Node &node);
    ~OscillatingSphereSolver();
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
    PetscReal Zc0;
    PetscErrorCode setCoordinatesBodies(const PetscReal &ti);
    PetscErrorCode setVelocityBodies(const PetscReal &ti);

};  // OscillatingSphereSolver