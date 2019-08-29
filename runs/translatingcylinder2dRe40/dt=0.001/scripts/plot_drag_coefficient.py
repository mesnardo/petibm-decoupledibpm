"""Plot the history of the drag coefficient."""

from matplotlib import pyplot
import pathlib

import petibmpy


# Load forces from file.
simudir = pathlib.Path(__file__).absolute().parents[1]
filepath = simudir / 'forces-0.txt'
t, fx, fy = petibmpy.read_forces(filepath)

# Convert forces to force coefficients.
rho, U0, D = 1.0, 1.0, 1.0
coeff = 1 / (0.5 * rho * U0**2 * D)
cd, cl = petibmpy.get_force_coefficients(fx, fy, coeff=coeff)

# Plot the history of the drag coefficient.
pyplot.rc('font', family='serif', size=16)
fig, ax = pyplot.subplots(figsize=(8.0, 4.0))
ax.set_xlabel('$t$')
ax.set_ylabel('$C_D$')
ax.grid()
ax.plot(t, cd)
ax.set_xlim(0.0, 3.5)
ax.set_ylim(0.0, 5.0)
fig.tight_layout()

# Save the figure.
figdir = simudir / 'figures'
figdir.mkdir(parents=True, exist_ok=True)
filepath = figdir / 'drag_coefficient.png'
fig.savefig(filepath, dpi=300)

pyplot.show()
