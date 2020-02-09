"""Plot the history of the drag coefficient for different time-step sizes."""

from matplotlib import pyplot
import numpy
import pathlib

import petibmpy

import rodney


args = rodney.parse_command_line()
maindir = pathlib.Path(__file__).parents[1]

# Set parameters.
Re = 40.0  # Reynolds number
D = 1.0  # cylinder diameter
U0 = 1.0  # maximum translational velocity
nu = U0 * D / Re  # kinematic viscosity
rho = 1.0  # density


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
    cd = fx / (0.5 * rho * U0**2 * D)
    return t, cd


simus = {}

# Get drag coefficient obtained with dt=0.0005.
label = r'$\Delta t = 0.0005$'
simudir = maindir / 'dt=0.0005'
filepath = simudir / 'output' / 'forces-0.txt'
t, cd = get_drag_coefficient(filepath)
simus[label] = dict(t=t, cd=cd,
                    kwargs=dict(color='black', linestyle='-', zorder=1))

# Get drag coefficient obtained with dt=0.001.
label = r'$\Delta t = 0.001$'
simudir = maindir / 'dt=0.001'
filepath = simudir / 'output' / 'forces-0.txt'
t, cd = get_drag_coefficient(filepath)
simus[label] = dict(t=t, cd=cd,
                    kwargs=dict(color='black', linestyle='--', zorder=2))

# Get drag coefficient obtained with dt=0.002.
label = r'$\Delta t = 0.002$'
simudir = maindir / 'dt=0.002'
filepath = simudir / 'output' / 'forces-0.txt'
t, cd = get_drag_coefficient(filepath)
simus[label] = dict(t=t, cd=cd,
                    kwargs=dict(color='black', linestyle='-.', zorder=3))

# Get drag coefficient obtained with dt=0.001.
label = r'$\Delta t = 0.005$'
simudir = maindir / 'dt=0.005'
filepath = simudir / 'output' / 'forces-0.txt'
t, cd = get_drag_coefficient(filepath)
simus[label] = dict(t=t, cd=cd,
                    kwargs=dict(color='black', linestyle=':', zorder=4))

# Plot the history of the drag coefficients.
pyplot.rc('font', family='serif', size=14)
fig, ax = pyplot.subplots(figsize=(6.0, 4.0))
ax.set_xlabel('$t$')
ax.set_ylabel('$C_D$')
for label, simu in simus.items():
    ax.plot(simu['t'], simu['cd'], label=label, **simu['kwargs'])

if args.extra_data:
    # Read and plot analytical solution from Bar-Lev and Yang (1997).
    # Analytical solution valid for early time.
    t_a, cd_a = rodney.bar_lev_yang_1997_drag_coefficient()
    ax.scatter(t_a, cd_a, label='Bar-Lev & Yang (1997)',
               color='C0', marker='o', s=5, zorder=6)
    # Read and plot numerical solution from Taira and Colonius (2007).
    t_n, cd_n = rodney.taira_colonius_2007_drag_coefficient()
    ax.scatter(t_n, cd_n, label='Taira & Colonius (2007)',
               color='C3', marker='o', s=10, zorder=5)

ax.legend(ncol=1, frameon=False, prop=dict(size=12))
ax.axis((0.0, 3.5, 0.0, 5.0))
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
fig.tight_layout()

if args.save_figures:
    # Save the figure.
    figdir = maindir / 'figures'
    figdir.mkdir(parents=True, exist_ok=True)
    filepath = figdir / 'drag_coefficients.png'
    fig.savefig(filepath, dpi=300, bbox_inches='tight')

if args.show_figures:
    pyplot.show()
