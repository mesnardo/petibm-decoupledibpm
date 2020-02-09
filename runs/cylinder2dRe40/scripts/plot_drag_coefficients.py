"""Plot the history of the force coefficients."""

import math
from matplotlib import pyplot
import numpy
import pathlib

import petibmpy

import rodney


def get_drag_coefficient(simudir):
    """Load forces, compute and return drag coefficient."""
    # Load forces from file.
    datadir = simudir / 'output'
    filepath = datadir / 'forces-0.txt'
    t, fx, _ = petibmpy.read_forces(filepath)
    # Convert forces to force coefficients.
    rho, U_inf, D = 1.0, 1.0, 1.0
    coeff = 1 / (0.5 * rho * U_inf**2 * D)
    cd, = petibmpy.get_force_coefficients(fx, coeff=coeff)
    print(f'Final value of the drag coefficient: CD = {cd[-1]:.4f}')
    time_limits = (40.0, 50.0)
    cd_, = petibmpy.get_time_averaged_values(t, cd, limits=time_limits)
    print(f'Time-averaged {time_limits} drag coefficient: <CD> = {cd_:.4f}')
    return t, cd


args = rodney.parse_command_line()

maindir = pathlib.Path(__file__).absolute().parents[1]

label1 = r'500 markers ($\Delta s \approx 0.38 \Delta x$)'
simudir1 = maindir / '500_markers'
t1, cd1 = get_drag_coefficient(simudir1)

label2 = r'189 markers ($\Delta s \approx \Delta x$)'
simudir2 = maindir / '189_markers'
t2, cd2 = get_drag_coefficient(simudir2)

# Plot the history of the force coefficients.
pyplot.rc('font', family='serif', size=14)
fig, ax = pyplot.subplots(figsize=(8.0, 4.0))
ax.set_xlabel('Non-dimensional time')
ax.set_ylabel('Drag coefficient')
ax.plot(t1, cd1, label=label1, color='C3', linestyle='-')
ax.plot(t2, cd2, label=label2, color='black', linestyle='--')
ax.legend(frameon=False)
ax.set_xlim(0.0, 30.0)
ax.set_ylim(0.0, 3.0)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
fig.tight_layout()

if args.save_figures:
    # Save the figure.
    figdir = maindir / 'figures'
    figdir.mkdir(parents=True, exist_ok=True)
    filepath = figdir / 'drag_coefficients.png'
    fig.savefig(filepath, dpi=300, bbox_inches='tight')

if args.show_figures:
    pyplot.show()
