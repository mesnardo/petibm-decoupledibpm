"""Plot the contours of the pressure field at final time step."""

from matplotlib import pyplot
import numpy
import pathlib

import petibmpy

import rodney


name = 'p'  # name of the vorticity variable
timestep = 5000  # final time-step index

args = rodney.parse_command_line()

# Set the simulation and data directories.
simudir = pathlib.Path(__file__).absolute().parents[1]
datadir = simudir / 'output'

# Load the gridlines from file.
filepath = datadir / 'grid.h5'
x, y = petibmpy.read_grid_hdf5(filepath, name)

# Load the pressure field from file.
filepath = datadir / f'{timestep:0>7}.h5'
p = petibmpy.read_field_hdf5(filepath, name)
p_min, p_max, p_mean = numpy.min(p), numpy.max(p), numpy.mean(p)
print(f'Pressure: min={p_min}, max={p_max}, mean={p_mean}')

# Load the boundary coordinates from file.
filepath = simudir / 'cylinder.body'
xb, yb = petibmpy.read_body(filepath, skiprows=1)

# Plot the filed contours of the pressure field.
pyplot.rc('font', family='serif', size=14)
fig, ax = pyplot.subplots(figsize=(6.0, 6.0))
ax.set_xlabel('$x / D$')
ax.set_ylabel('$y / D$')
levels = numpy.linspace(-1.0, 1.0, num=51)
ax.contourf(x, y, p, levels=levels, extend='both')
ax.plot(xb, yb, color='C3')
ax.axis('scaled', adjustable='box')
ax.set_xlim(-2.0, 4.0)
ax.set_ylim(-2.0, 2.0)
fig.tight_layout()

if args.save_figures:
    # Save the figure.
    figdir = simudir / 'figures'
    figdir.mkdir(parents=True, exist_ok=True)
    filepath = figdir / f'p_{timestep:0>7}.png'
    fig.savefig(filepath, dpi=300, bbox_inches='tight')

if args.show_figures:
    pyplot.show()
