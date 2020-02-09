"""Plot the contours of the pressure field at final time step."""

from matplotlib import pyplot
from mpl_toolkits.axes_grid1.inset_locator import InsetPosition
import numpy
import pathlib

import petibmpy

import rodney


def get_pressure(simudir, timestep):
    name = 'p'  # name of the vorticity variable
    timestep = 5000  # final time-step index
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
(x1, y1), p1 = get_pressure(simudir1, timestep)
body1 = get_body_coordinates(simudir1)

label2 = r'189 markers ($\Delta s \approx \Delta x$)'
simudir2 = maindir / '189_markers'
(x2, y2), p2 = get_pressure(simudir2, timestep)
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
ax1.contourf(x1, y1, p1, levels=levels, extend='both')
ax1.vlines(x1, ymin=y1[0], ymax=y1[-1], color='grey', linewidth=0.5)
ax1.hlines(y1, xmin=x1[0], xmax=x1[-1], color='grey', linewidth=0.5)
ax1.scatter(*numpy.meshgrid(x1, y1), c='black', s=10, marker='o')
ax1.plot(*body1, color='C3', marker='o')
ax1.text(0.1, 0.8, f'min = {numpy.min(p1):.4f}\nmax = {numpy.max(p1):.4f}',
         transform=ax1.transAxes, bbox=dict(facecolor='white', alpha=1.0))

ax2.set_title(label2, fontsize=14)
ax2.set_xlabel('$x / D$')
ax2.set_ylabel('$y / D$')
cont = ax2.contourf(x2, y2, p2, levels=levels, extend='both')
ax2.vlines(x2, ymin=y2[0], ymax=y2[-1], color='grey', linewidth=0.5)
ax2.hlines(y2, xmin=x2[0], xmax=x2[-1], color='grey', linewidth=0.5)
ax2.scatter(*numpy.meshgrid(x2, y2), c='black', s=10, marker='o')
ax2.plot(*body2, color='C3', marker='o')
ax2.text(0.1, 0.8, f'min = {numpy.min(p2):.4f}\nmax = {numpy.max(p2):.4f}',
         transform=ax2.transAxes, bbox=dict(facecolor='white', alpha=1.0))

for ax in (ax1, ax2):
    ax.axis('scaled', adjustable='box')
    ax.set_xlim(-0.6, -0.4)
    ax.set_ylim(0.1, 0.3)

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
    filepath = figdir / f'p_{timestep:0>7}_zoom.png'
    fig.savefig(filepath, dpi=300, bbox_inches='tight')

if args.show_figures:
    pyplot.show()
