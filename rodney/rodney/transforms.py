"""Assistant module with helper functions."""

import numpy
from scipy.spatial import distance


def create_regular_grid_2d(xlims, ylims, nx, ny):
    """Create a 2D regular mesh-grid."""
    xy = numpy.linspace(*xlims, num=nx), numpy.linspace(*ylims, num=ny)
    return tuple(numpy.meshgrid(*xy))


def apply_spatial_mask_2d(xy, values, limits):
    """Get solution in given sub-domain."""
    x, y = xy
    xlims, ylims = limits
    mask = numpy.where((x >= xlims[0]) & (x <= xlims[1]) &
                       (y >= ylims[0]) & (y <= ylims[1]))[0]

    return (x[mask], y[mask]), values[mask]


def sort_section(xy, p, return_index=False):
    """Re-order cross-sectional coordinates and values.

    New order starts from the leading edge and runs counter-clockwise.

    Parameters
    ----------
    xy : tuple(numpy.array)
        x and y surface coordinates, each direction as a 1D array.
    p : numpy.array
        Surface pressure at the coordinates.
    return_index : bool, optional
        If True, return sorted indices.
        If False (default), return sorted coordinates and values.

    Returns
    -------
    tuple(numpy.array)
        Re-ordered x and y coordinates.
    numpy.array
        Re-ordered surface pressure values.

    """
    x, y = xy

    coords = numpy.column_stack(xy)
    num_points = len(coords)

    dist = distance.cdist(coords, coords, 'euclidean')
    skip_val = 100.0
    numpy.fill_diagonal(dist, skip_val)

    index = [numpy.argmax(y)]  # heuristic: starting point is the highest one
    for _ in range(num_points - 1):
        start = index[-1]
        nearest = numpy.argmin(dist[start])  # find index of nearest neighboor
        index.append(nearest)
        dist[:, start] = skip_val  # prevent point from being visited again

    if return_index:
        return numpy.array(index)

    return (x[index], y[index]), p[index]


def _sort_spanwise(xyz, p, return_index=False):
    """Sort coordinates and values along the spanwise direction."""
    x, y, z = xyz

    index = numpy.argsort(z)

    if return_index:
        return index

    return (x[index], y[index], z[index]), p[index]


def sort_sections(xyz, p, return_index=False):
    """Re-order coordinates and values.

    Data are sorted along the spanwise direction and each spanwise section
    is sorted, starting from the leading edge and running counter-clockwise.

    Parameters
    ----------
    xyz : tuple(numpy.array)
        x, y, and z surface coordinates, each direction as a 1D array.
    p : numpy.array
        Surface pressure at the coordinates.
    return_index : bool, optional
        If True, return sorted indices.
        If False (default), return sorted coordinates and values.

    Returns
    -------
    tuple(numpy.array)
        Re-ordered x, y and z coordinates.
    numpy.array
        Re-ordered surface pressure values.

    """
    x, y, z = xyz

    index = _sort_spanwise(xyz, p, return_index=True)
    xb, yb, zb = x[index], y[index], z[index]
    pb = p[index]

    num_points = z.size
    num_sections = numpy.unique(z).size
    num_per_section = num_points // num_sections

    for i in range(num_sections):
        s, e = i * num_per_section, (i + 1) * num_per_section

        x_section, y_section = xb[s:e], yb[s:e]
        p_section = pb[s:e]

        section_index = sort_section((x_section, y_section), p_section,
                                     return_index=True)

        index[s:e] = index[s:e][section_index]

    if return_index:
        return index

    return (x[index], y[index], z[index]), p[index]


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
