"""Create a YAML file with info about the structured Cartesian mesh."""

import collections
import math
import pathlib

import petibmpy


simudir = pathlib.Path(__file__).absolute().parents[1]

# Define regions of the grid and grid-spacing size.
Box = collections.namedtuple('Box', ['xstart', 'xend', 'ystart', 'yend'])
box1 = Box(-15.0, 35.0, -25.0, 25.0)  # limits of the domain
box2 = Box(-0.75, 0.75, -0.75, 0.75)  # limits of the uniform region

# Compute the grid-spacing size in the uniform region
# to have a similar resolution than the Lagrangian surface mesh
# on which 500 equally spaced markers are placed.
R = 0.5  # cylinder radius
p = 2 * math.pi * R  # cylinder perimeter
ds = p / 500  # distance between two adjacent Lagrangian markers
length = box2.xend - box2.xstart  # length of the uniform region
n = math.ceil(length / ds)  # number of cells along one direction
width = length / n  # grid-spacing size in the uniform region
max_width = 20 * width

# Set configuration of the grid in the x direction.
config_x = [dict(start=box1.xstart, end=box2.xstart,
                 width=width, stretchRatio=1.05, reverse=True,
                 max_width=max_width),
            dict(start=box2.xstart, end=box2.xend, width=width),
            dict(start=box2.xend, end=box1.xend,
                 width=width, stretchRatio=1.01, max_width=max_width)]

# Set configuration of the grid in the y direction.
config_y = [dict(start=box1.ystart, end=box2.ystart,
                 width=width, stretchRatio=1.05, reverse=True,
                 max_width=max_width),
            dict(start=box2.ystart, end=box2.yend, width=width),
            dict(start=box2.yend, end=box1.yend,
                 width=width, stretchRatio=1.05, max_width=max_width)]

# Set the configuration of the grid.
config = [dict(direction='x', start=box1.xstart, subDomains=config_x),
          dict(direction='y', start=box1.ystart, subDomains=config_y)]

# Create the grid and save configuration in YAML file.
grid = petibmpy.CartesianGrid(config)
print(grid)
grid.print_info()
filepath = simudir / 'mesh.yaml'
grid.write_yaml(filepath, ndigits=10)
