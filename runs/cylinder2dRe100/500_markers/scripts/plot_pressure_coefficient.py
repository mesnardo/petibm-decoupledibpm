"""Plot the surface pressure coefficient at final time step."""

from matplotlib import pyplot
import numpy
import pathlib

import petibmpy

import rodney


name = 'p'  # name of the field variable to load
time = 200.0  # final probe record

# Set the simulation and data directories.
args = rodney.parse_command_line()
simudir = pathlib.Path(__file__).absolute().parents[1]
datadir = simudir / 'output'

# Load data from last record of the probe.
probe = petibmpy.ProbeVolume(name, name)
filepath = datadir / 'probe-p.h5'
(x, y), p = probe.read_hdf5(filepath, time)

# Define circle outside support region of delta function.
N = 500
dx = 1.5 / 90  # grid-spacing size in the uniform region
R = 0.5 + 3 * dx  # radius 3 cells away from real boundary
theta = numpy.linspace(0.0, 2 * numpy.pi, num=N + 1)[:-1]
xc, yc = 0.0, 0.0
xb_ext, yb_ext = xc + R * numpy.cos(theta), yc + R * numpy.sin(theta)

# Interpolate the field on extended boundary.
pb = numpy.empty_like(xb_ext)
for i, (xbi, ybi) in enumerate(zip(xb_ext, yb_ext)):
    pi = petibmpy.linear_interpolation(p, y, ybi)
    pb[i] = petibmpy.linear_interpolation(pi, x, xbi)

# Compute the pressure coefficient.
rho = 1.0  # fluid density
U_inf = 1.0  # freestream speed
p_inf = 0.0  # far-away pressure
cp = (pb - p_inf) / (0.5 * rho * U_inf**2)

# Re-arrange values to split apart lower and upper surfaces.
cp_lower = numpy.append(cp[N // 2:], [cp[-1]])
theta_lower = numpy.linspace(0.0, 180.0, num=cp_lower.size)
cp_upper = cp[:N // 2 + 1][::-1]
theta_upper = numpy.linspace(0.0, 180.0, num=cp_upper.size)

# Plot the distribution of the surface pressure coefficient.
pyplot.rc('font', family='serif', size=14)
fig, ax = pyplot.subplots(figsize=(6.0, 4.0))
ax.set_xlabel(r'$\theta$')
ax.set_ylabel('$C_p$')
ax.plot(theta_lower, cp_lower, label='Lower surface')
ax.plot(theta_upper, cp_upper, label='Upper surface', linestyle='--')

if args.extra_data:
    # Load digitized values from Li et al. (2016).
    theta_li, cp_li = rodney.lietal2016_load_cp(100)
    ax.scatter(theta_li, cp_li, label='Li et al. (2016)',
               c='black', marker='s', s=10)

ax.legend(frameon=False)
ax.set_xlim(0.0, 180.0)
ax.set_ylim(-1.5, 1.5)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
fig.tight_layout()

if args.save_figures:
    # Save the figure.
    figdir = simudir / 'figures'
    figdir.mkdir(parents=True, exist_ok=True)
    filepath = figdir / f'pressure_coefficient.png'
    fig.savefig(filepath, dpi=300, bbox_inches='tight')

if args.show_figures:
    pyplot.show()
