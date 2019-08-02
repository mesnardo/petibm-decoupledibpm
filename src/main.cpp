#include <petscsys.h>
#include <yaml-cpp/yaml.h>

#include <petibm/parser.h>

#include "lietal2016.h"
#include "oscillatingcylinder.h"
#include "oscillatingsphere.h"
#include "translatingcylinder.h"

typedef std::shared_ptr<LietAl2016Solver> Solver;

PetscErrorCode createSolver(
    const MPI_Comm &comm, const YAML::Node &config, Solver &solver)
{
    PetscErrorCode ierr;
    char s[PETSC_MAX_PATH_LEN];
    PetscBool flag;
    std::string name;

    PetscFunctionBeginUser;

    name = "li_et_al_2016";
    ierr = PetscOptionsGetString(
        nullptr, nullptr, "-solver", s, sizeof(s), &flag); CHKERRQ(ierr);
    if (flag) name = s;

    if (name == "li_et_al_2016")
        solver = std::make_shared<LietAl2016Solver>(comm, config);
    else if (name == "oscillating_cylinder")
        solver = std::make_shared<OscillatingCylinderSolver>(comm, config);
    else if (name == "translating_cylinder")
        solver = std::make_shared<TranslatingCylinderSolver>(comm, config);
    else if (name == "oscillating_sphere")
        solver = std::make_shared<OscillatingSphereSolver>(comm, config);
    else
        SETERRQ(comm, PETSC_ERR_ARG_WRONG,
                "Accepted values for -solver are: "
                "'li_et_al_2016' and 'oscillating_cylinder'.");

    PetscFunctionReturn(0);
}  // createSolver

int main(int argc, char **argv)
{
    PetscErrorCode ierr;
    YAML::Node config;
    Solver solver;

    ierr = PetscInitialize(&argc, &argv, nullptr, nullptr); CHKERRQ(ierr);
    ierr = PetscLogDefaultBegin(); CHKERRQ(ierr);

    // parse configuration files; store info in YAML node
    ierr = petibm::parser::getSettings(config); CHKERRQ(ierr);

    // initialize the solver
    ierr = createSolver(PETSC_COMM_WORLD, config, solver); CHKERRQ(ierr);
    ierr = solver->ioInitialData(); CHKERRQ(ierr);
    ierr = PetscPrintf(PETSC_COMM_WORLD,
                       "Completed initialization stage\n"); CHKERRQ(ierr);

    // integrate the solution in time
    while (!solver->finished())
    {
        // compute the solution at the next time step
        ierr = solver->advance(); CHKERRQ(ierr);
        // output data to files
        ierr = solver->write(); CHKERRQ(ierr);
    }

    // destroy the solver
    ierr = solver->destroy(); CHKERRQ(ierr);

    ierr = PetscFinalize(); CHKERRQ(ierr);

    return 0;
}  // main
