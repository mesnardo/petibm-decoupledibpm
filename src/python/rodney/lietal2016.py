"""Helper functions to load data digitized from Li et al. (2016)."""

import numpy
import pathlib


ROOTDIR = pathlib.Path(__file__).absolute().parents[3]
DATADIR = ROOTDIR / 'data'


def lietal2016_load_cp(Re):
    """Load and return the surface pressure for a stationary cylinder.

    Parameters
    ----------
    Re : int
        Reynolds number; choices are 40 and 100.

    Returns
    -------
    numpy.ndarray
        Array with angular positions along the cylinder.
    numpy.ndarray
        Array with corresponding values of the pressure coefficient.

    """
    filepath = DATADIR / f'li_et_al_2016_cylinder2dRe{round(Re)}_cp.csv'
    with open(filepath, 'r') as infile:
        theta, cp = numpy.loadtxt(infile, delimiter=',', unpack=True)
    return theta, cp


def coutanceau_bouard_1977_recirculation_length():
    """Load the history recirculation length behind translating cylinder.

    The Reynolds number is 40.

    Returns
    -------
    numpy.ndarray
        Time values as a 1D array of floats.
    numpy.ndarray
        Recirculation length over time normalize by cylinder diameter,
        as a 1D array of floats.

    """
    filepath = DATADIR / 'coutanceau_bouard_1977_recirculation_length.csv'
    with open(filepath, 'r') as infile:
        t, lw = numpy.loadtxt(infile, delimiter=',', unpack=True)
    return t, lw


def taira_colonius_2007_drag_coefficient():
    """Load history of the drag coefficient for cylinder at Re=40.

    Cylinder is impulsively started and translate in the negative x-direction.
    Data from Taira & Colonius (2007), reported in Li et al. (2016), and
    digitized from Figure 10 of Li et al. (2016).

    Returns
    -------
    numpy.ndarray
        Time values as a 1D array of floats.
    numpy.ndarray
        History of the drag coefficient as a 1D array of floats.

    """
    filepath = DATADIR / 'taira_colonius_2007_cylinder2dRe40_cd.csv'
    with open(filepath, 'r') as infile:
        t, cd = numpy.loadtxt(infile, delimiter=',', unpack=True)
    return t, cd


def bar_lev_yang_1997_drag_coefficient():
    """Load history of the drag coefficient for cylinder at Re=40.

    Cylinder is impulsively started and translate in the negative x-direction.
    Data from Bar-Lev & Yang (1997), reported in Li et al. (2016), and
    digitized from Figure 10 of Li et al. (2016).

    Returns
    -------
    numpy.ndarray
        Time values as a 1D array of floats.
    numpy.ndarray
        History of the drag coefficient as a 1D array of floats.

    """
    filepath = DATADIR / 'bar-lev_yang_1997_cylinder2dRe40_cd.csv'
    with open(filepath, 'r') as infile:
        t, cd = numpy.loadtxt(infile, delimiter=',', unpack=True)
    return t, cd
