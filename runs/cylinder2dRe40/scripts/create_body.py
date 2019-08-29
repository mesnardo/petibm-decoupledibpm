"""Create the body and write the coordinates to a file."""

import numpy
import pathlib

import petibmpy


# Create the coordinates of the circle.
R = 0.5
N = 500
dx = 1.5 / 90
N = (2 * numpy.pi * R // dx) + 1
if N % 2 != 0:
    N += 1
xc, yc = 0.0, 0.0
theta = numpy.linspace(0.0, 2 * numpy.pi, num=N + 1)[:-1]
x, y = xc + R * numpy.cos(theta), yc + R * numpy.sin(theta)

# Save the coordinates into a file.
simudir = pathlib.Path(__file__).absolute().parents[1]
filepath = simudir / 'cylinder.body'
petibmpy.write_body(filepath, x, y)
