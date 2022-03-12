"""Assistant module with functions to process forces."""

import re
import pathlib

import numpy


def load_forces_3d(filepath, limits=(0.0, numpy.infty)):
    """Load three-dimensional forces from file."""
    tmppath = pathlib.Path(str(filepath) + '.tmp')
    _remove_parentheses(filepath, tmppath)
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


def _remove_parentheses(srcpath, destpath):
    """Remove all parenthesies from file and save into another."""
    with open(srcpath, 'r') as infile:
        lines = infile.readlines()
        for i, line in enumerate(lines):
            lines[i] = re.sub('[()]', '', line)
    with open(destpath, 'w') as outfile:
        outfile.writelines(lines)


def force_coefficients(forces, rho=1.0, U_inf=1.0, D=1.0, Lz=numpy.pi):
    """Calculate the force coefficients.

    Parameters
    ----------
    forces : tuple(numpy.array)
        Directional forces; each direction as a 1D array.
    rho : float, optional
        Density; default is 1.
    U_inf : float, optional
        Freestream speed; default is 1.
    D : float, optional
        Characteristic length of the bluff body; default is 1.
    Lz : float, optional
        Spanwise length; default is pi.

    Returns
    -------
    tuple(numpy.array)
        Direction force coefficients.

    """
    p_dyn = 0.5 * rho * U_inf * D * Lz  # dynamic pressure
    return tuple(f / p_dyn for f in forces)
