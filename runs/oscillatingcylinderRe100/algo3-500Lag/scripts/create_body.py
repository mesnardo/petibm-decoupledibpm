"""Create and save coordinates of the circle."""

import math
import numpy
import pathlib

import petibmpy


# Circle's parameters.
R = 0.5  # radius
xc, yc = 0.0, 0.0  # center's coordinates

simudir = pathlib.Path(__file__).absolute().parents[1]

# Generate coordinates of the circle.
n = 500
theta = numpy.linspace(0.0, 2 * numpy.pi, num=n + 1)[:-1]
x, y = xc + R * numpy.cos(theta), yc + R * numpy.sin(theta)

# Save coordinates into file.
filepath = simudir / 'circle.body'
petibmpy.write_body(filepath, x, y)
