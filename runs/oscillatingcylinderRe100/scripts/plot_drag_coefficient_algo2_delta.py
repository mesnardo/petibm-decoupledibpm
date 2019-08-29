"""Plot the history of the drag coefficient for different delta functions."""

from matplotlib import pyplot
import numpy
import pathlib

import petibmpy


rootdir = pathlib.Path(__file__).parents[1]
show_figure = True  # if True, display the figure(s).

# Set parameters.
Re = 100.0  # Reynolds number
KC = 5.0  # Keulegan-Carpenter number
D = 1.0  # cylinder diameter
Um = 1.0  # maximum translational velocity
nu = Um * D / Re  # kinematic viscosity
rho = 1.0  # density
f = Um / D / KC  # oscillation frequency
w = 2 * numpy.pi * f  # angular frequency
Am = Um / w  # oscillation amplitude


def get_drag_coefficient(filepath):
    """Load drag from file and return drag coefficient.

    Parameters
    ----------
    filepath : pathlib.Path or str
        Path of the file with the history of the forces.

    Returns
    -------
    t : numpy.ndarray
        Time values as a 1D array of floats.
    cd : numpy.ndarray
        History of the drag coefficient as a 1D array of floats.

    """
    # Load drag force from file.
    t, fx, _ = petibmpy.read_forces(filepath)
    # Convert drag to drag coefficient.
    V = numpy.pi * D**2 / 4  # body volume
    ax = w**2 * Am * numpy.sin(w * t)
    fx += rho * V * ax
    cd = fx / (0.5 * rho * Um**2 * D)
    return t, cd


simus = {}

# Get drag coefficient obtained with 3-point delta function.
label = 'Roma et al. (1999)'
filepath = rootdir / 'algo2' / 'forces-0.txt'
t, cd = get_drag_coefficient(filepath)
simus[label] = dict(t=f * t, cd=cd,
                    kwargs=dict(color='C0', linestyle='-', zorder=1))

# Get drag coefficient obtained with 4-point delta function.
label = 'Peskin (2002)'
filepath = rootdir / 'algo2-peskin' / 'forces-0.txt'
t, cd = get_drag_coefficient(filepath)
simus[label] = dict(t=f * t, cd=cd,
                    kwargs=dict(color='C1', linestyle='--', zorder=2))

# Plot the history of the force coefficients.
pyplot.rc('font', family='serif', size=16)
fig, ax = pyplot.subplots(figsize=(8.0, 4.0))
ax.set_xlabel('$t / T$')
ax.set_ylabel('$C_D$')
for label, simu in simus.items():
    ax.plot(simu['t'], simu['cd'], label=label, **simu['kwargs'])
ax.legend(ncol=3)
ax.axis((0.0, 4.0, -6.0, 6.0))
ax.legend(ncol=2, frameon=False, prop={'size': 12})
fig.tight_layout()
# Save the figure.
figdir = rootdir / 'figures'
figdir.mkdir(parents=True, exist_ok=True)
filepath = figdir / 'drag_coefficient_algo2_delta.png'
fig.savefig(filepath, dpi=300, bbox_inches='tight')

if show_figure:
    pyplot.show()
