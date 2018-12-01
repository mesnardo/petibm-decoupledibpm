"""
Create a circle.
"""

import pathlib
import math
import numpy


# Circle's parameters.
R = 0.5  # radius
xc, yc = 0.0, 0.0  # center's coordinates
ds = 8.0 / 512  # distance between two consecutive points

simu_dir = pathlib.Path(__file__).absolute().parents[1]

# Generate coordinates of the circle.
n = math.ceil(2 * numpy.pi * R / ds)
theta = numpy.linspace(0.0, 2 * numpy.pi, num=n, endpoint=False)
x, y = xc + R * numpy.cos(theta), yc + R * numpy.sin(theta)

# Write coordinates into file.
filepath = simu_dir / 'circle.body'
with open(filepath, 'w') as outfile:
    outfile.write('{}\n'.format(x.size))
with open(filepath, 'ab') as outfile:
    numpy.savetxt(outfile, numpy.c_[x, y])
