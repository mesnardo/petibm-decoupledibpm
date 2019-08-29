"""Plot the contours of the pressure at the middle symmetric plane."""

from matplotlib import pyplot
import numpy
import pathlib

import petibmpy

from kinematics import D, Am, Um, rho, f, dt


simudir = pathlib.Path(__file__).absolute().parents[1]
name = 'p'  # name of the pressure variable in HDF5 files

# Load the grid from file.
filepath = simudir / 'grid.h5'
x, y, z = petibmpy.read_grid_hdf5(filepath, name)

timesteps = [2000, 2200, 2400]
labels = ['$0^o$', '$144^o$', '$288^o$']

# Initialize the figure and axes.
pyplot.rc('font', family='serif', size=14)
fig, ax = pyplot.subplots(ncols=3, figsize=(10.0, 4.0))
# Define the level of the contours to plot.
levels = numpy.linspace(-2 / rho / Um**2, 2 / rho / Um**2, num=30)

for i, (label, timestep) in enumerate(zip(labels, timesteps)):
    # Load the pressure field from file.
    filepath = simudir / 'solution' / '{:0>7}.h5'.format(timestep)
    p = petibmpy.read_field_hdf5(filepath, name)
    p -= p.mean()  # set the mean value to 0.
    # Interpolate the field along the z-direction at z=0.
    p = petibmpy.linear_interpolation(p, z, 0.0)
    # Load the boundary coordinates from file.
    filepath = simudir / 'solution' / 'sphere_{:0>7}.3D'.format(timestep)
    xb, yb, zb = petibmpy.read_body(filepath)
    # Generate the circle at present time step.
    t = timestep * dt
    theta = numpy.linspace(0.0, 2 * numpy.pi, num=51)
    xc, yc = D / 2 * numpy.cos(theta), D / 2 * numpy.sin(theta)
    xc += Am * numpy.sin(2 * numpy.pi * f * t)
    # Plot the contours of the pressure and the boundary.
    ax[i].set_title(label)
    ax[i].set_xlabel('$x$')
    ax[i].set_ylabel('$y$')
    ax[i].contour(x, y, p, levels=levels, colors='black', zorder=1)
    ax[i].scatter(xb, yb, c='C0', s=0.1, zorder=3)
    ax[i].fill(xc, yc, color='grey', zorder=2)
    ax[i].axis('scaled', adjustable='box')
    ax[i].set_xlim(-2.0, 2.0)
    ax[i].set_ylim(-2.0, 2.0)

fig.tight_layout()

# Save the figure.
figdir = simudir / 'figures'
figdir.mkdir(parents=True, exist_ok=True)
filepath = figdir / 'pressure.png'
fig.savefig(filepath, dpi=300, bbox_inches='tight')

pyplot.show()
