"""Helper functions for the velocity profiles."""

import pathlib
import re
import tarfile

import numpy

from .misc import time_to_str


def load_Ux_yNormal(times, datadir=None, tarball=None):
    if datadir is not None:
        xz, ux = _load_Ux_yNormal(times, datadir)
    elif tarball is not None:
        xz, ux = _load_Ux_yNormal_from_tarball(times, tarball)
    else:
        raise ValueError('invalid parameters; '
                         'filepath OR tarball must be specified')

    return xz, ux


def _load_Ux_yNormal_from_tarball(times, tarball):
    initialized = False
    times = list(map(time_to_str, times))
    names = [f'postProcessing/surfaceProfiles/{time}/U_yNormal_x0.0.raw'
             for time in times]
    with tarfile.open(tarball, 'r|gz') as tar:
        for member in tar:
            if member.name in names:
                f = tar.extractfile(member)
                *xz, ux = numpy.loadtxt(f, usecols=(0, 2, 3), unpack=True)

                if not initialized:
                    ux_tot = numpy.zeros_like(ux)
                    initialized = True

                ux_tot += ux

                names.remove(member.name)
                if len(names) == 0:
                    break

    return xz, ux_tot / len(times)


def _load_Ux_yNormal(times, datadir):
    times = list(map(time_to_str, times))
    initialized = False
    for time in times:
        filepath = pathlib.Path(datadir) / time / 'U_yNormal_x0.0.raw'
        with open(filepath, 'r') as f:
            *xz, ux = numpy.loadtxt(f, usecols=(0, 2, 3), unpack=True)

        if not initialized:
            ux_tot = numpy.zeros_like(ux)
            initialized = True

        ux_tot += ux

    return xz, ux_tot / len(times)


def load_Uxy_xNormal(xlocs, times, datadir=None, tarball=None):
    if datadir is not None:
        profiles = _load_Uxy_xNormal(xlocs, times, datadir)
    elif tarball is not None:
        profiles = _load_Uxy_xNormal_from_tarball(xlocs, times, tarball)
    else:
        raise ValueError('invalid parameters; '
                         'filepath OR tarball must be specified')

    return profiles


def _load_Uxy_xNormal_from_tarball(xlocs, times, tarball):
    times = list(map(time_to_str, times))

    names = [f'postProcessing/surfaceProfiles/{time}/U_xNormal_x{xloc:.2f}.raw'
             for time in times for xloc in xlocs]

    profiles = dict()
    with tarfile.open(tarball, 'r|gz') as tar:
        for member in tar:
            if member.name in names:
                f = tar.extractfile(member)
                y, z, ux, uy = numpy.loadtxt(f, usecols=(1, 2, 3, 4),
                                             unpack=True)

                xloc = float(re.search('U_xNormal_x(.*?)\.raw',
                                       member.name)[1])

                if xloc not in profiles:
                    profiles[xloc] = dict(
                        yz=(y, z),
                        ux=numpy.zeros_like(ux),
                        uy=numpy.zeros_like(uy)
                    )

                profiles[xloc]['ux'] += ux
                profiles[xloc]['uy'] += uy

                names.remove(member.name)
                if len(names) == 0:
                    break

    for xloc in xlocs:
        profiles[xloc]['ux'] /= len(times)
        profiles[xloc]['uy'] /= len(times)

    return profiles


def _load_Uxy_xNormal(xlocs, times, datadir):
    times = list(map(time_to_str, times))
    profiles = dict()
    for xloc in xlocs:
        initialized = False
        for time in times:
            filepath = (pathlib.Path(datadir) / time /
                        f'U_xNormal_x{xloc:.2f}.raw')
            with open(filepath, 'r') as f:
                y, z, ux, uy = numpy.loadtxt(f, usecols=(1, 2, 3, 4),
                                             unpack=True)

            if not initialized:
                ux_tot = numpy.zeros_like(ux)
                uy_tot = numpy.zeros_like(uy)
                initialized = True

            ux_tot += ux
            uy_tot += uy

        profiles[xloc] = dict(
            yz=(y, z), ux=ux_tot / len(times), uy=uy_tot / len(times)
        )

    return profiles
