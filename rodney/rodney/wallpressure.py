"""Helper functions for the wall pressure."""

import pathlib
import tarfile

import numpy

from .misc import time_to_str


def load_wall_pressure(times, datadir=None, tarball=None):
    if datadir is not None:
        xyz, p = _load_wall_pressure(times, datadir)
    elif tarball is not None:
        xyz, p = _load_wall_pressure_from_tarball(times, tarball)
    else:
        raise ValueError('invalid parameters; '
                         'filepath OR tarball must be specified')

    return xyz, p


def _load_wall_pressure_from_tarball(times, tarball):
    initialized = False
    times = list(map(time_to_str, times))
    names = [f'postProcessing/wallPressure/{time}/p_snake.raw'
             for time in times]
    with tarfile.open(tarball, 'r|gz') as tar:
        for member in tar:
            if member.name in names:
                f = tar.extractfile(member)
                *xyz, p = numpy.loadtxt(f, unpack=True)

                if not initialized:
                    p_tot = numpy.zeros_like(p)
                    initialized = True

                p_tot += p

                names.remove(member.name)
                if len(names) == 0:
                    break

    return xyz, p_tot / len(times)


def _load_wall_pressure(times, datadir):
    times = list(map(time_to_str, times))
    initialized = False
    for time in times:
        filepath = pathlib.Path(datadir) / time / 'p_snake.raw'
        with open(filepath, 'r') as f:
            *xyz, p = numpy.loadtxt(f, unpack=True)

        if not initialized:
            p_tot = numpy.zeros_like(p)
            initialized = True

        p_tot += p

    return xyz, p_tot / len(times)


def wall_pressure_coefficient(p, rho=1.0, U_inf=1.0, D=1.0):
    """Return the pressure coefficient.

    Parameters
    ----------
    p : numpy.array
        Surface pressure.
    rho : float, optional
        Density; default is 1.
    U_inf : float, optional
        Freestream speed; default is 1.
    D : float, optional
        Characteristic length of the bluff body; default is 1.

    Returns
    -------
    numpy.array
        Surface pressure coefficient.

    """
    p_dyn = 0.5 * rho * U_inf * D
    return p / p_dyn
