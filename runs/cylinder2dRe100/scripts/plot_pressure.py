"""Plot the contours of the pressure field at final time step."""

from matplotlib import pyplot
from mpl_toolkits.axes_grid1.inset_locator import InsetPosition
import numpy
import pathlib

import petibmpy

import rodney


def get_pressure(simudir, timestep):
    name = 'p'  # name of the field variable to load
    datadir = simudir / 'output'
    # Load the gridlines from file.
    filepath = datadir / 'grid.h5'
    x, y = petibmpy.read_grid_hdf5(filepath, name)
    # Load the pressure field from file.
    filepath = datadir / f'{timestep:0>7}.h5'
    p = petibmpy.read_field_hdf5(filepath, name)
    return (x, y), p


def get_body_coordinates(simudir):
    # Load the boundary coordinates from file.
    filepath = simudir / 'cylinder.body'
    xb, yb = petibmpy.read_body(filepath, skiprows=1)
    return xb, yb


args = rodney.parse_command_line()

maindir = pathlib.Path(__file__).absolute().parents[1]
timestep = 20000  # final time-step index

label1 = r'500 markers ($\Delta s \approx 0.38 \Delta x$)'
simudir1 = maindir / '500_markers'
grid1, p1 = get_pressure(simudir1, timestep)
body1 = get_body_coordinates(simudir1)

label2 = r'189 markers ($\Delta s \approx \Delta x$)'
simudir2 = maindir / '189_markers'
grid2, p2 = get_pressure(simudir2, timestep)
body2 = get_body_coordinates(simudir2)

# Plot the filed contours of the pressure field.
pyplot.rc('font', family='serif', size=14)
gridspec_kw = dict(width_ratios=[1, 1, 0.05])
fig, (ax1, ax2, cax) = pyplot.subplots(ncols=3, figsize=(10.0, 4.0),
                                       gridspec_kw=gridspec_kw)
levels = numpy.linspace(-1.0, 1.0, num=51)

ax1.set_title(label1, fontsize=14)
ax1.set_xlabel('$x / D$')
ax1.set_ylabel('$y / D$')
ax1.contourf(*grid1, p1, levels=levels, extend='both')
ax1.plot(*body1, color='C3')

ax2.set_title(label2, fontsize=14)
ax2.set_xlabel('$x / D$')
ax2.set_ylabel('$y / D$')
cont = ax2.contourf(*grid2, p2, levels=levels, extend='both')
ax2.plot(*body2, color='C3')

for ax in (ax1, ax2):
    ax.axis('scaled', adjustable='box')
    ax.set_xlim(-0.75, 0.75)
    ax.set_ylim(-0.75, 0.75)

# Add colorbar.
ip = InsetPosition(ax2, [1.05, 0, 0.05, 1])
cax.set_axes_locator(ip)
cbar = fig.colorbar(cont, cax=cax, ax=(ax1, ax2))
cbar.set_label('p')
fig.tight_layout()

if args.save_figures:
    # Save the figure.
    figdir = maindir / 'figures'
    figdir.mkdir(parents=True, exist_ok=True)
    filepath = figdir / f'p_{timestep:0>7}.png'
    fig.savefig(filepath, dpi=300, bbox_inches='tight')

if args.show_figures:
    pyplot.show()
