"""Create the body and write the coordinates to a file."""

import math
import numpy
import pathlib

import petibmpy


# Create the coordinates of the circle.
R = 0.5  # radius of circle
N = 500  # number of segments
dx = 1.5 / 90  # grid-spacing size of background grid
delta_x, delta_y = 0.01 * dx, 0.01 * dx  # offset center
xc, yc = 0.0 + delta_x, 0.0 + delta_y  # center of circle
theta = numpy.linspace(0.0, 2 * numpy.pi, num=N + 1)[:-1]
x, y = xc + R * numpy.cos(theta), yc + R * numpy.sin(theta)

# Save the coordinates into a file.
simudir = pathlib.Path(__file__).absolute().parents[1]
filepath = simudir / 'cylinder.body'
petibmpy.write_body(filepath, x, y)
