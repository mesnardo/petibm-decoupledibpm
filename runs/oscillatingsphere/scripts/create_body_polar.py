"""Create a surface mesh on a sphere."""

import math
from matplotlib import pyplot
from mpl_toolkits.mplot3d import Axes3D
import numpy
import pathlib

import petibmpy


# Set parameters.
simudir = pathlib.Path(__file__).absolute().parents[1]
R = 0.5  # sphere radius
xc, yc, zc = 0.0, 0.0, 0.0  # sphere center
dx = 4 / 256
plot = False

# Create points on sphere.
# North pole.
x, y, z = xc, yc, zc + R
# Between poles.
n_phi = math.ceil(math.pi * R / dx)
phi_angles = numpy.linspace(0.0, math.pi, num=n_phi)[1:-1]
for phi in phi_angles:
    rsinphi = R * math.sin(phi)
    rcosphi = R * math.cos(phi)
    n_theta = math.ceil(2 * math.pi * rsinphi / dx)
    theta = numpy.linspace(0.0, 2.0 * math.pi, num=n_theta + 1)[:-1]
    x = numpy.append(x, xc + rsinphi * numpy.cos(theta))
    y = numpy.append(y, yc + rsinphi * numpy.sin(theta))
    z = numpy.append(z, zc + rcosphi * numpy.ones(n_theta))
# South pole.
x = numpy.append(x, xc)
y = numpy.append(y, yc)
z = numpy.append(z, zc - R)

# Save coordinates into file.
filepath = simudir / 'sphere.body'
petibmpy.write_body(filepath, x, y, z)

if plot:
    fig, ax = pyplot.subplots(subplot_kw=dict(projection='3d'))
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    ax.scatter(x, y, z)
    ax.axis('scaled', adjustable='box')
    pyplot.show()
