"""Assistant module with helper functions."""

import argparse
import numpy
import pathlib
import pprint
import re


DATADIR = pathlib.Path(__file__).absolute().parent / 'data'


def parse_command_line():
    """Parse the command-line options."""
    formatter_class = argparse.ArgumentDefaultsHelpFormatter
    descr = 'Generic command-line parser for the 3D snake application.'
    parser = argparse.ArgumentParser(description=descr,
                                     formatter_class=formatter_class)
    parser.add_argument('--no-show', dest='show_figures',
                        action='store_false',
                        help='Do not display Matplotlib figures')
    parser.add_argument('--no-save', dest='save_figures',
                        action='store_false',
                        help='Do not save Matplotlib figures')
    parser.add_argument('--no-data', dest='extra_data',
                        action='store_false',
                        help='Add extra data for comparison (if available)')
    return parser.parse_args()


def time_to_str(time):
    """Convert time (float) to string."""
    s = str(time)
    if s.endswith('.0'):
        return s[:-2]
    return s


def remove_parentheses(srcpath, destpath):
    """Remove all parenthesies from file and save into another."""
    with open(srcpath, 'r') as infile:
        lines = infile.readlines()
        for i, line in enumerate(lines):
            lines[i] = re.sub('[()]', '', line)
    with open(destpath, 'w') as outfile:
        outfile.writelines(lines)


def load_forces_3d(filepath, limits=(0.0, numpy.infty)):
    """Load three-dimensional forces from file."""
    tmppath = pathlib.Path(str(filepath) + '.tmp')
    remove_parentheses(filepath, tmppath)
    with open(tmppath, 'r') as infile:
        cols = tuple(range(7))
        data = numpy.loadtxt(infile, usecols=cols, unpack=True)
    tmppath.unlink()
    t = data[0]
    fx = data[1] + data[4]
    fy = data[2] + data[5]
    fz = data[3] + data[6]
    mask = numpy.where((t >= limits[0]) & (t <= limits[1]))[0]
    return t[mask], fx[mask], fy[mask], fz[mask]


def get_stats(t, f, limits=(0.0, numpy.infty), verbose=False):
    """Compute descriptive statistics of signal."""
    mask = numpy.where((t >= limits[0]) & (t <= limits[1]))[0]
    f = f[mask]
    f_mean = numpy.mean(f)
    stats = dict(mean=float(f_mean),
                 std=float(numpy.std(f)),
                 var=float(numpy.var(f)),
                 rms=float(numpy.sqrt(numpy.mean((f - f_mean)**2))))
    if verbose:
        pprint.pprint(stats)
    return stats


def get_time_directories(datadir, limits=(0.0, numpy.infty), stride=1):
    """Get the time directories to process as an array of floats."""
    times = numpy.sort([float(child.name) for child in datadir.iterdir()])
    mask = numpy.where((times >= limits[0]) & (times <= limits[1]))[0]
    return times[mask][::stride]


def create_regular_grid_2d(xlims, ylims, nx, ny):
    """Create a 2D regular mesh-grid."""
    x, y = numpy.linspace(*xlims, num=nx), numpy.linspace(*ylims, num=ny)
    return numpy.meshgrid(x, y)


def apply_spatial_mask_2d(x, y, field, xlims, ylims):
    """Get solution in given sub-domain."""
    mask = numpy.where((x >= xlims[0]) & (x <= xlims[1]) &
                       (y >= ylims[0]) & (y <= ylims[1]))[0]
    return x[mask], y[mask], field[mask]


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
