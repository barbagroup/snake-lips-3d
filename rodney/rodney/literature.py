"""Assistant module with helper functions to load literature data."""

import pathlib

import numpy


DATADIR = pathlib.Path(__file__).absolute().parent / 'data'


def load_u_profiles_literature():
    """Load mean streamwise velocity profiles from literature."""
    data = dict()
    # Load data of Lourenco & Shih (1993).
    filepath = DATADIR / 'lourenco_shih_1993_u_profiles.csv'
    label = 'Lourenco & Shih (1993)'
    with open(filepath, 'r') as infile:
        data[label] = numpy.loadtxt(infile, delimiter=',', unpack=True)
    # Load data on Ong & Wallace (1996).
    filepath = DATADIR / 'ong_wallace_1996_u_profiles.csv'
    label = 'Ong & Wallace (1996)'
    with open(filepath, 'r') as infile:
        data[label] = numpy.loadtxt(infile, delimiter=',', unpack=True)
    # Load data of Parnaudeau et al. (2008).
    filepath = DATADIR / 'parnaudeau_et_al_2008_u_profiles.csv'
    label = 'Parnaudeau et al. (2008)'
    with open(filepath, 'r') as infile:
        data[label] = numpy.loadtxt(infile, delimiter=',', unpack=True)
    return data


def load_v_profiles_literature():
    """Load mean transversal velocity profiles from literature."""
    data = dict()
    # Load data of Lourenco & Shih (1993).
    filepath = DATADIR / 'lourenco_shih_1993_v_profiles.csv'
    label = 'Lourenco & Shih (1993)'
    with open(filepath, 'r') as infile:
        data[label] = numpy.loadtxt(infile, delimiter=',', unpack=True)
    # Load data on Ong & Wallace (1996).
    filepath = DATADIR / 'ong_wallace_1996_v_profiles.csv'
    label = 'Ong & Wallace (1996)'
    with open(filepath, 'r') as infile:
        data[label] = numpy.loadtxt(infile, delimiter=',', unpack=True)
    # Load data of Parnaudeau et al. (2008).
    filepath = DATADIR / 'parnaudeau_et_al_2008_v_profiles.csv'
    label = 'Parnaudeau et al. (2008)'
    with open(filepath, 'r') as infile:
        data[label] = numpy.loadtxt(infile, delimiter=',', unpack=True)
    return data


def load_u_centerline_profiles_literature():
    """Load mean streamwise velocity along centerline from literature."""
    data = dict()
    # Load data of Lourenco & Shih (1993).
    filepath = DATADIR / 'lourenco_shih_1993_u_centerline.csv'
    label = 'Lourenco & Shih (1993)'
    with open(filepath, 'r') as infile:
        data[label] = numpy.loadtxt(infile, delimiter=',', unpack=True)
    # Load data of Parnaudeau et al. (2008).
    filepath = DATADIR / 'parnaudeau_et_al_2008_u_centerline.csv'
    label = 'Parnaudeau et al. (2008)'
    with open(filepath, 'r') as infile:
        data[label] = numpy.loadtxt(infile, delimiter=',', unpack=True)
    # Load data of Lysenko et al. (2012).
    filepath = DATADIR / 'lysenko_et_al_2012_u_centerline.csv'
    label = 'Lysenko et al. (2012)'
    with open(filepath, 'r') as infile:
        data[label] = numpy.loadtxt(infile, delimiter=',', unpack=True)
    return data


def load_surface_pressure_coefficient_literature():
    """Load surface pressure coefficient from literature."""
    data = dict()
    # Load data of Norberg (1994).
    filepath = DATADIR / 'norberg_1994_cp.csv'
    label = 'Norberg (1994)'
    with open(filepath, 'r') as infile:
        data[label] = numpy.loadtxt(infile, delimiter=',', unpack=True)
    return data
