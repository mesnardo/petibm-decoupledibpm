"""Create a surface mesh on a sphere."""

from matplotlib import pyplot
from mpl_toolkits.mplot3d import Axes3D
import numpy
import pathlib
import sys

import petibmpy

rootdir = pathlib.Path(__file__).absolute().parents[3]
moduledir = rootdir / 'src' / 'python'
sys.path.insert(1, str(moduledir))

import triangulation


R = 0.5  # sphere radius
xc, yc, zc = 0.0, 0.0, 0.0  # sphere center
center = numpy.array([xc, yc, zc])

vertices, faces, centers = triangulation.create_unit_sphere(recursion_level=4)
vertices *= R  # scale
vertices += center  # displace
x, y, z = vertices.T

print(centers.shape)

_, areas = triangulation.surface_variables(vertices, faces)

# Check the sphere is correctly centered.
center_t = [x.mean(), y.mean(), z.mean()]
kwargs = dict(atol=1e-12, rtol=0.0)
assert numpy.allclose(center, center_t, **kwargs), 'Center is not right!'

simudir = pathlib.Path(__file__).absolute().parents[1]
filepath = simudir / 'sphere.body'
petibmpy.write_body(filepath, x, y, z)

print(x.shape, y.shape, z.shape)

fig, ax = pyplot.subplots(subplot_kw=dict(projection='3d'))
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')
ax.plot_trisurf(x, y, z, triangles=faces,
                edgecolor="black", color="C0", alpha=1.0)
ax.axis('scaled', adjustable='box')

pyplot.show()
