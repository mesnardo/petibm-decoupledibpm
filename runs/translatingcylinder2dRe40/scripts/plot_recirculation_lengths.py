"""Compute and plot the recirculation length over time."""

from matplotlib import pyplot
import numpy
import pathlib

import petibmpy

import rodney


def get_recirculation_length_history(simudir, dt, time_limits=(0.5, 3.5)):
    datadir = simudir / 'output'
    name = 'u'  # name of the field variable to read
    R = 0.5  # radius of cylinder
    U = 1.0  # translational speed of cylinder
    tstart, tend = time_limits  # starting and final time values to consider
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
    return times, lengths


args = rodney.parse_command_line()
maindir = pathlib.Path(__file__).absolute().parents[1]

# Compute the history of the recirculation length for each simulation.
simus = {}
dt_values = [0.0005, 0.001, 0.002, 0.005]
linestyles = ['-', '--', '-.', ':']
for i, (dt, linestyle) in enumerate(zip(dt_values, linestyles)):
    label = r'$\Delta t = {}$'.format(dt)
    simudir = maindir / f'dt={dt}'
    t, lw = get_recirculation_length_history(simudir, dt)
    simus[label] = dict(t=t, lw=lw,
                        plot_kwargs=dict(color='black',
                                         linestyle=linestyle,
                                         zorder=i + 1))

# Plot the history of the recirculation length.
pyplot.rc('font', family='serif', size=14)
fig, ax = pyplot.subplots(figsize=(6.0, 4.0))
ax.set_xlabel('$t$')
ax.set_ylabel('$L_w / D$')
for label, simu in simus.items():
    ax.plot(simu['t'], simu['lw'], label=label, **simu['plot_kwargs'])

if args.extra_data:
    # Load experimental data points from Coutanceau & Bouard (1977).
    t_exp, lw_exp = rodney.coutanceau_bouard_1977_recirculation_length()
    ax.scatter(t_exp, lw_exp, label='Coutanceau & Bouard (1977)',
               c='C0', s=10, marker='o')
ax.legend(frameon=False, prop=dict(size=11))
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.axis((0.0, 3.5, 0.0, 1.5))
fig.tight_layout()

if args.save_figures:
    # Save the figure.
    figdir = maindir / 'figures'
    figdir.mkdir(parents=True, exist_ok=True)
    filepath = figdir / 'recirculation_lengths.png'
    fig.savefig(filepath, dpi=300, bbox_inches='tight')

if args.show_figures:
    pyplot.show()
