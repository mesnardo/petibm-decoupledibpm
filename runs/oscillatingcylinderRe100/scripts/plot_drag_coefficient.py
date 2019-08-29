"""Plot the history of the drag coefficient for different algorithms."""

from matplotlib import pyplot
from matplotlib.gridspec import GridSpec
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

# Get drag coefficient obtained with algo 1 and scheme 3.
label = 'Algo. 1'
filepath = rootdir / 'algo1' / 'forces-0.txt'
t, cd = get_drag_coefficient(filepath)
simus[label] = dict(t=f * t, cd=cd,
                    kwargs=dict(color='C0', zorder=4))

# Get drag coefficient obtained with algo 2 and scheme 3.
label = 'Algo. 2'
filepath = rootdir / 'algo2' / 'forces-0.txt'
t, cd = get_drag_coefficient(filepath)
simus[label] = dict(t=f * t, cd=cd,
                    kwargs=dict(color='C1', linestyle='--', zorder=5))

# Get drag coefficient obtained with algo 3 and scheme 3 (dt=0.002).
label = r'Algo. 3 ($\Delta t=0.002D/U_m$)'
filepath = rootdir / 'algo3' / 'forces-0.txt'
t, cd = get_drag_coefficient(filepath)
simus[label] = dict(t=f * t, cd=cd,
                    kwargs=dict(color='black', zorder=1))

# Get drag coefficient obtained with algo 3 and scheme 3 (dt=0.001).
label = r'Algo. 3 ($\Delta t=0.001D/U_m$)'
filepath = rootdir / 'algo3-dt=0.001' / 'forces-0.txt'
t, cd = get_drag_coefficient(filepath)
simus[label] = dict(t=f * t, cd=cd,
                    kwargs=dict(color='black', linestyle='--', zorder=2))

# Get drag coefficient obtained with algo 3 and scheme 3 (dt=0.0005).
label = r'Algo. 3 ($\Delta t=0.0005D/U_m$)'
filepath = rootdir / 'algo3-dt=0.0005' / 'forces-0.txt'
t, cd = get_drag_coefficient(filepath)
simus[label] = dict(t=f * t, cd=cd,
                    kwargs=dict(color='black', linestyle=':', zorder=3))

# Initialize the Matplotlib figure.
pyplot.rc('font', family='serif', size=12)
fig = pyplot.figure(figsize=(8.0, 6.0))
gs = GridSpec(2, 2, figure=fig)

# Plot the history of the force coefficients.
ax1 = fig.add_subplot(gs[0, :])
ax1.set_xlabel('$t / T$')
ax1.set_ylabel('$C_D$')
for label, simu in simus.items():
    ax1.plot(simu['t'], simu['cd'], label=label, **simu['kwargs'])
ax1.legend(ncol=3)
ax1.axis((0.0, 4.0, -6.0, 8.0))
ax1.legend(ncol=3, prop={'size': 10}, frameon=False)
ax1.spines['right'].set_visible(False)
ax1.spines['top'].set_visible(False)

# Plot a zoom at early stage.
ax2 = fig.add_subplot(gs[1, 0])
ax2.set_xlabel('$t / T$')
ax2.set_ylabel('$C_D$')
for label, simu in simus.items():
    ax2.plot(simu['t'], simu['cd'], label=label, **simu['kwargs'])
ax2.axis((0.0, 0.2, -6.0, 6.0))
ax2.spines['right'].set_visible(False)
ax2.spines['top'].set_visible(False)

# Plot a zoom at later stage.
ax3 = fig.add_subplot(gs[1, 1])
ax3.set_xlabel('$t / T$')
ax3.set_ylabel('$C_D$')
for label, simu in simus.items():
    ax3.plot(simu['t'], simu['cd'], label=label, **simu['kwargs'])
ax3.axis((3.75, 4.0, 3.0, 4.0))
ax3.spines['right'].set_visible(False)
ax3.spines['top'].set_visible(False)

fig.tight_layout()

# Save the figure.
figdir = rootdir / 'figures'
figdir.mkdir(parents=True, exist_ok=True)
filepath = figdir / 'drag_coefficient.png'
fig.savefig(filepath, dpi=300, bbox_inches='tight')

if show_figure:
    pyplot.show()
