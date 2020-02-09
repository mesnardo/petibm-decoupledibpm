"""Create a YAML file with info about the structured Cartesian mesh."""

import collections
import pathlib

import petibmpy


Box = collections.namedtuple('Box', ['xstart', 'xend', 'ystart', 'yend'])
box1 = Box(-16.5, 13.5, -15.0, 15.0)
box2 = Box(-5.0, 1.0, -1.0, 1.0)
width = 0.02
max_width = 20 * width

config_x = [dict(start=box1.xstart, end=box2.xstart,
                 width=width, stretchRatio=1.02, max_width=max_width,
                 reverse=True),
            dict(start=box2.xstart, end=box2.xend, width=width),
            dict(start=box2.xend, end=box1.xend,
                 width=width, stretchRatio=1.02, max_width=max_width)]

config_y = [dict(start=box1.ystart, end=box2.ystart,
                 width=width, stretchRatio=1.02, max_width=max_width,
                 reverse=True),
            dict(start=box2.ystart, end=box2.yend, width=width),
            dict(start=box2.yend, end=box1.yend,
                 width=width, stretchRatio=1.02, max_width=max_width)]

config = [dict(direction='x', start=box1.xstart, subDomains=config_x),
          dict(direction='y', start=box1.ystart, subDomains=config_y)]

grid = petibmpy.CartesianGrid(config)
print(grid)
simudir = pathlib.Path(__file__).absolute().parents[1]
filepath = simudir / 'mesh.yaml'
grid.write_yaml(filepath, ndigits=10)
