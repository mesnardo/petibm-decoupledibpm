"""Plot the history of the drag coefficient for different time-step sizes."""

from matplotlib import pyplot
from mpl_toolkits.axes_grid1.inset_locator import mark_inset, zoomed_inset_axes
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

# Get drag coefficient obtained with dt=0.001.
label = '$0.001 D / U_m$'
filepath = rootdir / 'algo1-dt=0.001' / 'forces-0.txt'
t, cd = get_drag_coefficient(filepath)
simus[label] = dict(t=f * t, cd=cd,
                    kwargs=dict(color='black', zorder=1))

# Get drag coefficient obtained with dt=0.002.
label = '$0.002 D / U_m$'
filepath = rootdir / 'algo1' / 'forces-0.txt'
t, cd = get_drag_coefficient(filepath)
simus[label] = dict(t=f * t, cd=cd,
                    kwargs=dict(color='black', linestyle='--', zorder=2))

# Get drag coefficient obtained with dt=0.002.
label = '$0.005 D / U_m$'
filepath = rootdir / 'algo1-dt=0.005' / 'forces-0.txt'
t, cd = get_drag_coefficient(filepath)
simus[label] = dict(t=f * t, cd=cd,
                    kwargs=dict(color='black', linestyle=':', zorder=3))

# Plot the history of the force coefficients.
pyplot.rc('font', family='serif', size=16)
fig, ax = pyplot.subplots(figsize=(6.0, 4.0))
ax.set_xlabel('$t / T$')
ax.set_ylabel('$C_D$')
for label, simu in simus.items():
    ax.plot(simu['t'], simu['cd'], label=label, **simu['kwargs'])
ax.axis((1.0, 3.0, -4.0, 4.0))
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.legend(ncol=1, prop={'size': 10}, frameon=False)
fig.tight_layout()

# Add zoom.
axins = zoomed_inset_axes(ax, 5, loc=4)
for label, simu in simus.items():
    axins.plot(simu['t'], simu['cd'], label=label, **simu['kwargs'])
view = (2.82, 2.92, 3.0, 3.5)
axins.set_xlim(view[:2])
axins.set_ylim(view[2:])
axins.set_xticks([], [])
axins.set_yticks([], [])
mark_inset(ax, axins, loc1=2, loc2=4, fc='none', ec='0.5')

# Save the figure.
figdir = rootdir / 'figures'
figdir.mkdir(parents=True, exist_ok=True)
filepath = figdir / 'drag_coefficient_dt.png'
fig.savefig(filepath, dpi=300, bbox_inches='tight')

if show_figure:
    pyplot.show()
