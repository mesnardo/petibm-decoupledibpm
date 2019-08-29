"""Fluid properties, geometric and kinematic parameters."""

import numpy


# Parameters.
D = 1.0  # sphere diameter

# Kinematic parameters.
Am = 0.125 * D  # oscillation amplitude
Um = 1.0  # maximum translation velocity

# Fluid properties.
Re = 78.54  # Reynolds number
nu = Um * D / Re  # kinematic viscosity
rho = 1.0  # density

# Temporal parameters.
St = 1.2732  # Strouhal number
f = St * Um / D  # oscillation frequency
T = 1 / f  # time period

# Simulation parameters.
dt = 0.00157 * D / Um  # time-step size
n_periods = 5  # number of periods
tf = n_periods * T  # final time
nt_period = 500  # number of time steps per period
nt = n_periods * nt_period  # number of time steps
dt2 = tf / nt  # time-step size


if __name__ == '__main__':
    print(locals())
