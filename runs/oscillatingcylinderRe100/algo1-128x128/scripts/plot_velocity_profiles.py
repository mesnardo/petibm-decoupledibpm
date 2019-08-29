"""Plot the velocity profiles at 4 cross-sections and 3 phase angles."""

from matplotlib import pyplot
import numpy
import pathlib

import petibmpy

from kinematics import D, Um


display_figure = True  # if True, display the figure(s).
simudir = pathlib.Path(__file__).absolute().parents[1]

pyplot.rc('font', family='serif', size=16)
nrows, ncols = 3, 2
fig, ax = pyplot.subplots(nrows=nrows, ncols=ncols, figsize=(10.0, 10.0))
phases = [180, 210, 330]  # phase angles (in degrees)
times = [17.5, 17.916, 19.584]  # corresponding time units
x_locs = [-0.6, 0.0, 0.6, 1.2]  # cross-section locations
for row in range(nrows):
    for col in range(ncols):
        name = 'u' if col == 0 else 'v'
        time, phase = times[row], phases[row]
        filepath = simudir / 'solution' / f'probe{phase}-{name}.h5'
        for xi in x_locs:
            (x, y), u = petibmpy.read_probe_volume_hdf5(filepath, name, time)
            ui = petibmpy.linear_interpolation(u.T, x, xi)
            ax[row, col].plot(ui / Um, y / D, label=f'{xi}')
        ax[row, col].set_xlabel('$u / U_m$' if col == 0 else '$v / U_m$')
        ax[row, col].set_ylabel('$y / D$')
        ax[row, col].set_xlim(-1.5, 1.5)
        ax[row, col].set_ylim(-1.1, 1.1)
ax[0, 1].legend(prop={'size': 12})
fig.tight_layout()

# Save the figure.
figdir = simudir / 'figures'
figdir.mkdir(parents=True, exist_ok=True)
filepath = figdir / 'velocity_profiles.png'
fig.savefig(filepath, dpi=300)

if display_figure:
    pyplot.show()
