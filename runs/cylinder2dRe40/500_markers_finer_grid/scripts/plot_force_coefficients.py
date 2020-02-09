"""Plot the history of the force coefficients."""

import math
from matplotlib import pyplot
import numpy
import pathlib

import petibmpy

import rodney


args = rodney.parse_command_line()

# Load forces from file.
simudir = pathlib.Path(__file__).absolute().parents[1]
datadir = simudir / 'output'
filepath = datadir / 'forces-0.txt'
t, fx, fy = petibmpy.read_forces(filepath)

# Convert forces to force coefficients.
rho, U_inf, D = 1.0, 1.0, 1.0
coeff = 1 / (0.5 * rho * U_inf**2 * D)
cd, cl = petibmpy.get_force_coefficients(fx, fy, coeff=coeff)

print(f'Final value of the drag coefficient: CD = {cd[-1]:.4f}')
time_limits = (40.0, 50.0)
cd_, = petibmpy.get_time_averaged_values(t, cd, limits=time_limits)
print(f'Time-averaged {time_limits} drag coefficient: <CD> = {cd_:.4f}')

# Plot the history of the force coefficients.
pyplot.rc('font', family='serif', size=14)
fig, ax = pyplot.subplots(figsize=(8.0, 4.0))
ax.set_xlabel('Non-dimensional time')
ax.set_ylabel('Force coefficients')
ax.plot(t, cd, label='$C_D$', color='black', linestyle='-')
ax.plot(t, cl, label='$C_L$', color='black', linestyle='--')
ax.legend(frameon=False)
ax.set_xlim(t[0], t[-1])
ax.set_ylim(-3.0, 3.0)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
fig.tight_layout()

if args.save_figures:
    # Save the figure.
    figdir = simudir / 'figures'
    figdir.mkdir(parents=True, exist_ok=True)
    filepath = figdir / 'force_coefficients.png'
    fig.savefig(filepath, dpi=300, bbox_inches='tight')

if args.show_figures:
    pyplot.show()
