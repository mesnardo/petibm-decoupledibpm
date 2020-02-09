"""Compute and plot the recirculation length over time."""

from matplotlib import pyplot
import numpy
import pathlib

import petibmpy

import rodney


args = rodney.parse_command_line()

# Set directories and parameters.
simudir = pathlib.Path(__file__).absolute().parents[1]
datadir = simudir / 'output'
name = 'u'  # name of the fiedl variable to read

R = 0.5  # radius of cylinder
U = 1.0  # translational speed of cylinder
dt = 0.0005  # time-step size
tstart, tend = 0.5, 3.5  # starting and final time values to consider
times = numpy.arange(tstart, tend + dt / 2, dt)
filepath = datadir / f'probe-{name}.h5'

# Compute the history of the recirculation length.
lengths = numpy.empty_like(times)
for i, time in enumerate(times):
    # Update center of the circle.
    xc, yc = -U * time, 0.0  # center of the circle
    # Load data of the volume probe.
    probe = petibmpy.ProbeVolume(name, name)
    (x, y), u = probe.read_hdf5(filepath, time)
    # Interpolate volume along horizontal line at y=yc.
    u_yc = petibmpy.linear_interpolation(u, y, yc)
    # Compute the coordinates of the end of the recirculation zone.
    buffer = 0.01
    idx = numpy.where((u_yc + U <= 0.0) & (x > xc + R + buffer))[0][-1]
    # x-coordinate computed as where the x-velocity becomes positive.
    xp = petibmpy.linear_interpolation(x[idx: idx + 2],
                                       u_yc[idx: idx + 2] + U, 0.0)
    # Compute the recirculation legnth.
    lengths[i] = abs(xp - (xc + R))

# Plot the history of the recirculation length.
pyplot.rc('font', family='serif', size=14)
fig, ax = pyplot.subplots(figsize=(6.0, 4.0))
ax.set_xlabel('$t$')
ax.set_ylabel('$L_w / D$')
ax.plot(times, lengths, label=r'$\Delta t = {}$'.format(dt), color='black')
if args.extra_data:
    # Load experimental data points from Coutanceau & Bouard (1977).
    t_exp, lw_exp = rodney.coutanceau_bouard_1977_recirculation_length()
    ax.scatter(t_exp, lw_exp, label='Coutanceau & Bouard (1977)',
               c='C0', s=10, marker='o')
ax.legend(frameon=False)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.axis((0.0, 3.5, 0.0, 1.5))
fig.tight_layout()

if args.save_figures:
    # Save the figure.
    figdir = simudir / 'figures'
    figdir.mkdir(parents=True, exist_ok=True)
    filepath = figdir / 'recirculation_length.png'
    fig.savefig(filepath, dpi=300, bbox_inches='tight')

if args.show_figures:
    pyplot.show()
