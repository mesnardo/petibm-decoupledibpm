"""Plot the spatial convergence for the streamwise velocity components."""

from matplotlib import pyplot
import numpy
import pathlib
from scipy import interpolate

import petibmpy


rootdir = pathlib.Path(__file__).absolute().parents[1]

name = 'u'  # name of the variable for the x-velocity
f = 0.2  # oscillation frequency
T = 1 / f  # oscillation period
t = 2.8 * T  # time value to monitor
dt = 0.002
timestep = int(t / dt)

u = []
folders = ['algo1-64x64', 'algo1-128x128', 'algo1-256x256',
           'algo1', 'algo1-1024x1024']
dx = 8.0 / numpy.array([64, 128, 256, 512, 1024])

# Load the coarsest grid from file.
simudir = rootdir / folders[0]
filepath = simudir / 'grid.h5'
x_ref, y_ref = petibmpy.read_grid_hdf5(filepath, name)
grid = numpy.array(numpy.meshgrid(y_ref, x_ref, indexing='ij'))
grid = numpy.rollaxis(grid, 0, 3).reshape(x_ref.size * y_ref.size, 2)

for d, folder in zip(dx, folders):
    simudir = rootdir / folder
    # Load the grid from file.
    filepath = simudir / 'grid.h5'
    x, y = petibmpy.read_grid_hdf5(filepath, name)
    # Load the field from file.
    filepath = simudir / 'solution' / '{:0>7}.h5'.format(timestep)
    u_tmp = petibmpy.read_field_hdf5(filepath, name)
    u_int = interpolate.interpn((y, x), u_tmp, grid,
                                method='linear')
    u_int = u_int.reshape((y_ref.size, x_ref.size))
    u.append(u_int)

l2_errors, linf_errors = [], []
for i in range(len(u) - 1):
    l2 = numpy.sqrt(numpy.sum((u[i] - u[-1])**2))
    l2_errors.append(l2)
    linf = numpy.max(numpy.abs(u[i] - u[-1]))
    linf_errors.append(linf)

pyplot.rc('font', family='serif', size=16)
fig, ax = pyplot.subplots(figsize=(6.0, 6.0))
ax.grid()
ax.set_xlabel(r'$\Delta x$')
ax.set_ylabel('Spatial error ($u$)')
ax.loglog(dx[:-1], linf_errors, label=r'$L_\infty$',
          color='black', marker='s')
ax.loglog(dx[:-1], l2_errors, label='$L_2$',
          color='black', marker='s', markerfacecolor='none')
first = linf_errors[0] / dx[0] * numpy.array(dx[:-1])
second = l2_errors[0] / dx[0]**2 * numpy.array(dx[:-1])**2
ax.loglog(dx[:-1], first, label=r'$1^{st}$-order',
          color='black', linestyle='--')
ax.loglog(dx[:-1], second, label=r'$2^{st}$-order',
          color='black', linestyle=':')
ax.legend(prop={'size': 12})
ax.axis('scaled', adjustable='box')
ax.set_xlim(1e-2, 2e-1)
fig.tight_layout()

# Save the figure.
figdir = rootdir / 'figures'
figdir.mkdir(parents=True, exist_ok=True)
filepath = figdir / 'spatial_error.png'
fig.savefig(filepath, dpi=300)

pyplot.show()
