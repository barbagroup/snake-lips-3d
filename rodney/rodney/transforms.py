"""Assistant module with helper functions."""

import numpy

from .misc import time_to_str


def create_regular_grid_2d(xlims, ylims, nx, ny):
    """Create a 2D regular mesh-grid."""
    x, y = numpy.linspace(*xlims, num=nx), numpy.linspace(*ylims, num=ny)
    return numpy.meshgrid(x, y)


def apply_spatial_mask_2d(x, y, field, xlims, ylims):
    """Get solution in given sub-domain."""
    mask = numpy.where((x >= xlims[0]) & (x <= xlims[1]) &
                       (y >= ylims[0]) & (y <= ylims[1]))[0]
    return x[mask], y[mask], field[mask]


def load_wall_pressure(directory, time, filename):
    """Load the surface pressure from file at given time.

    Parameters
    ----------
    directory : pathlib.Path
        Directory containing time folders.
    time : float
        Time at which to read the surface pressure.
    filename : str
        Name of the file containing the surface pressure data.

    Returns
    -------
    tuple(numpy.array)
        x, y, and z coordinates of the surface points;
        each direction as 1D array.
    numpy.array
        Surface pressure values.

    """
    filepath = directory / time_to_str(time) / filename
    with open(filepath, 'r') as infile:
        x, y, z, p = numpy.loadtxt(infile, dtype=numpy.float64, unpack=True)
    return (x, y, z), p


def sort_section(xy, p):
    """Re-order cross-sectional coordinates and values.

    New order starts from the leading edge and runs counter-clockwise.

    Parameters
    ----------
    xy : tuple(numpy.array)
        x and y surface coordinates, each direction as a 1D array.
    p : numpy.array
        Surface pressure at the coordinates.

    Returns
    -------
    tuple(numpy.array)
        Re-ordered x and y coordinates.
    numpy.array
        Re-ordered surface pressure values.

    """
    x, y = xy
    indices = numpy.argsort(numpy.degrees(numpy.arctan2(y, x)))

    return (x[indices], y[indices]), p[indices]


def _sort_spanwise(xyz, p):
    """Sort coordinates and values along the spanwise direction."""
    x, y, z = xyz
    indices = numpy.argsort(z)

    return (x[indices], y[indices], z[indices]), p[indices]


def sort_sections(xyz, p):
    """Re-order coordinates and values.

    Data are sorted along the spanwise direction and each spanwise section
    is sorted, starting from the leading edge and running counter-clockwise.

    Parameters
    ----------
    xyz : tuple(numpy.array)
        x, y, and z surface coordinates, each direction as a 1D array.
    p : numpy.array
        Surface pressure at the coordinates.

    Returns
    -------
    tuple(numpy.array)
        Re-ordered x, y and z coordinates.
    numpy.array
        Re-ordered surface pressure values.

    """
    xyz, p = _sort_spanwise(xyz, p)
    x, y, z = xyz

    num_points = p.size
    num_sections = numpy.unique(z).size
    num_per_section = num_points // num_sections

    for i in range(num_sections):
        s, e = i * num_per_section, (i + 1) * num_per_section

        xy_section, p_section = (x[s:e], y[s:e]), p[s:e]
        xy_section, p_section = sort_section(xy_section, p_section)

        x[s:e], y[s:e] = xy_section
        p[s:e] = p_section

        assert(numpy.allclose(x[s:e], x[:num_per_section]) and
               numpy.allclose(y[s:e], y[:num_per_section]))

    return (x, y, z), p


def spanwise_average(xyz, p):
    """Compute the spanwise-average field.

    Values are averaged along the spanwise direction.

    Parameters
    ----------
    xyz : tuple(numpy.array)
        x, y, and z surface coordinates, each direction as a 1D array.
    p : numpy.array
        Surface value at the coordinates.

    Returns
    -------
    tuple(numpy.array)
        x and y surface coordinates.
    numpy.array
        Spanwise-averaged surface values.

    """
    x, y, z = xyz

    num_points = p.size
    num_sections = numpy.unique(z).size
    num_per_section = num_points // num_sections

    x, y = x[:num_per_section], y[:num_per_section]
    p_avg = numpy.mean(p.reshape((num_sections, num_per_section)), axis=0)

    return (x, y), p_avg


def pressure_coefficient(p, rho=1.0, U_inf=1.0, D=1.0):
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
