"""Write the YAML configuration file for the probes."""

import collections
import numpy
import pathlib
import yaml


class Limits(list):
    pass


def represent_dictionary_order(self, dict_data):
    return self.represent_mapping('tag:yaml.org,2002:map', dict_data.items())


def represent_limits(self, data):
    return self.represent_sequence('tag:yaml.org,2002:seq', data,
                                   flow_style=True)


def setup_yaml():
    yaml.add_representer(collections.OrderedDict, represent_dictionary_order)
    yaml.add_representer(Limits, represent_limits)


simudir = pathlib.Path(__file__).absolute().parents[1]

probe = collections.OrderedDict({})
probe['name'] = 'probe-p'
probe['type'] = 'VOLUME'
probe['field'] = 'p'
probe['viewer'] = 'hdf5'
probe['path'] = 'solution/' + probe['name'] + '.h5'
probe['n_sum'] = 1000
xlim, ylim = (-0.75, 0.75), (-0.75, 0.75)
probe['box'] = collections.OrderedDict({'x': Limits(xlim),
                                        'y': Limits(ylim)})

filepath = simudir / 'probes.yaml'
setup_yaml()
with open(filepath, 'w') as outfile:
    yaml.dump({'probes': [probe]}, outfile, default_flow_style=False)
