import pathlib
import h5py
import numpy
from matplotlib import pyplot


def get_velocity_along_vertical_line(xi, t, name, filepath):
    f = h5py.File(filepath, 'r')
    x, y = f['mesh']['x'][:], f['mesh']['y'][:]
    nx, ny = x.size, y.size
    u = f[name][f'{t:0.6f}'][:].reshape((ny, nx))
    idx = numpy.where(x >= xi)[0][0]
    xa, xb = x[idx - 1], x[idx]
    ua, ub = u[:, idx - 1], u[:, idx]
    ui = ua + (xi - xa) / (xb - xa) * (ub - ua)
    return y, ui


simu_dir = pathlib.Path(__file__).absolute().parents[1]
filepath = simu_dir / 'solution' / 'probe180-u.h5'

f = 0.2
D = 1.0
KC = 5.0
Um = f * D * KC

pyplot.rc('font', family='serif', size=16)
nrows, ncols = 3, 2
fig, ax = pyplot.subplots(nrows=nrows, ncols=ncols, figsize=(10.0, 10.0))
times, phases = [17.5, 17.916, 19.584], [180, 210, 330]
x_targets = [-0.6, 0.0, 0.6, 1.2]
for row in range(nrows):
    for col in range(ncols):
        name = 'u' if col == 0 else 'v'
        t, phase = times[row], phases[row]
        filepath = simu_dir / 'solution' / f'probe{phase}-{name}.h5'
        for xi in x_targets:
            y, u = get_velocity_along_vertical_line(xi, t, name, filepath)
            ax[row, col].plot(u / Um, y / D, label=f'{xi}')
        ax[row, col].set_xlabel('$u / U_m$' if col == 0 else '$v / U_m$')
        ax[row, col].set_ylabel('$y / D$')
        ax[row, col].set_xlim(-1.5, 1.5)
        ax[row, col].set_ylim(-1.1, 1.1)
ax[0, 1].legend(prop={'size': 12})
fig.tight_layout()

# Save the figure.
fig_dir = simu_dir / 'figures'
fig_dir.mkdir(parents=True, exist_ok=True)
filepath = fig_dir / 'velocityCrossSections.png'
fig.savefig(str(filepath), dpi=300)

pyplot.show()
