"""Plot the history of the force coefficients."""

import math
from matplotlib import pyplot
import numpy
import pathlib

import petibmpy


# Load forces from file.
simudir = pathlib.Path(__file__).absolute().parents[1]
filepath = simudir / 'forces-0.txt'
t, fx, fy = petibmpy.read_forces(filepath)

# Convert forces to force coefficients.
rho, U_inf, D = 1.0, 1.0, 1.0
coeff = 1 / (0.5 * rho * U_inf**2 * D)
cd, cl = petibmpy.get_force_coefficients(fx, fy, coeff=coeff)

# Plot the history of the force coefficients.
pyplot.rc('font', family='serif', size=16)
fig, ax = pyplot.subplots(figsize=(8.0, 4.0))
ax.set_xlabel('Non-dimensional time')
ax.set_ylabel('Force coefficients')
ax.grid()
ax.plot(t, cd, label='$C_D$')
ax.plot(t, cl, label='$C_L$')
ax.legend()
ax.set_ylim(-3.0, 3.0)
fig.tight_layout()

# Save the figure.
figdir = simudir / 'figures'
figdir.mkdir(parents=True, exist_ok=True)
filepath = figdir / 'force_coefficients.png'
fig.savefig(filepath, dpi=300)

pyplot.show()
