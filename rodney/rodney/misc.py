"""Assistant module with miscellaneous functions."""

import argparse
import pprint

import numpy


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
    parser.add_argument('--no-compute', dest='compute',
                        action='store_false',
                        help='Do not re-compute; load data from file')
    return parser.parse_args()


def time_to_str(time):
    """Return a time string given a float.

    If the time string ends with '.0', return the string of the integer.

    """
    s = str(time)
    if s.endswith('.0'):
        return s[:-2]
    return s


def get_saved_times(directory, limits=None, stride=1):
    """Return array of time values saved as folders in a directory.

    Parameters
    ----------
    directory : pathlib.Path
        Path of the directory.
    limits : tuple(float, float), optional
        Time interval filter; default is None (and (0, inf) will be used).
    stride : int, optional
        Step at which time values are returned;
        default is 1 (all savedtime values within interval).

    Returns
    -------
    numpy.array
        Saved time values within a given time interval.

    """
    if limits is None:
        limits = (0.0, numpy.inf)
    start, end = limits

    times = numpy.sort([float(child.name) for child in directory.iterdir()])
    mask = numpy.where((times >= start) & (times <= end))[0]

    return times[mask][::stride]


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
