"""Plot the contours of the vorticity field at t=1.0 and 3.5."""

from matplotlib import pyplot
import numpy
import pathlib

import petibmpy

import rodney


args = rodney.parse_command_line()

name = 'wz'  # name of the vorticity variable

# Set the simulation and data directories.
simudir = pathlib.Path(__file__).absolute().parents[1]
datadir = simudir / 'output'

# Load the gridlines from file.
filepath = datadir / 'grid.h5'
x, y = petibmpy.read_grid_hdf5(filepath, name)

# Load the vorticity field at t=1.0.
timestep = 200  # t = 1.0
filepath = datadir / '{:0>7}.h5'.format(timestep)
wz1 = petibmpy.read_field_hdf5(filepath, name)
# Load the body coordinates at the same time.
filepath = datadir / 'cylinder_{:0>7}.2D'.format(timestep)
xb1, yb1 = petibmpy.read_body(filepath, skiprows=1)

# Load the vorticity field at t=3.5.
timestep = 700  # t = 3.5
filepath = datadir / '{:0>7}.h5'.format(timestep)
wz2 = petibmpy.read_field_hdf5(filepath, name)
# Load the body coordinates at the same time.
filepath = datadir / 'cylinder_{:0>7}.2D'.format(timestep)
xb2, yb2 = petibmpy.read_body(filepath, skiprows=1)

# Plot the contours of the vorticity field.
pyplot.rc('font', family='serif', size=12)
fig, (ax1, ax2) = pyplot.subplots(ncols=2, figsize=(8.0, 4.0))
ax1.set_xlabel('$x / D$')
ax1.set_ylabel('$y / D$')
levels = numpy.arange(-3.0, 3.0 + 0.4 / 2, 0.4)
ax1.contour(x, y, wz1, levels=levels, colors='black')
ax1.plot(xb1, yb1, color='red')
ax1.axis('scaled', adjustable='box')
ax1.set_xlim(-5.0, 1.0)
ax1.set_ylim(-2.0, 2.0)
ax1.spines['right'].set_visible(False)
ax1.spines['top'].set_visible(False)
ax2.set_xlabel('$x / D$')
ax2.set_ylabel('$y / D$')
ax2.contour(x, y, wz2, levels=levels, colors='black')
ax2.plot(xb2, yb2, color='red')
ax2.axis('scaled', adjustable='box')
ax2.set_xlim(-5.0, 1.0)
ax2.set_ylim(-2.0, 2.0)
ax2.spines['right'].set_visible(False)
ax2.spines['top'].set_visible(False)
fig.tight_layout()

if args.save_figures:
    # Save the figure.
    figdir = simudir / 'figures'
    figdir.mkdir(parents=True, exist_ok=True)
    filepath = figdir / f'vorticity.png'
    fig.savefig(filepath, dpi=300, bbox_inches='tight')

if args.show_figures:
    pyplot.show()
