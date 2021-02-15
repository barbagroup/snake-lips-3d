"""Plot the surface pressure coefficient."""

from matplotlib import pyplot
import numpy
import pathlib
import tqdm

import rodney


def get_sorted_indices_all_sections(x, y, z):
    """Return array of sorted indices along the cylinder."""
    n_points = x.size
    z_span = numpy.sort(numpy.unique(z))
    n_sections = z_span.size
    masks = numpy.empty((n_sections, n_points // n_sections), dtype=int)
    indices = numpy.empty((n_sections, n_points // n_sections), dtype=int)
    for s in range(n_sections):
        mask = numpy.where(z == z_span[s])[0]
        masks[s] = mask
        indices[s] = get_sorted_indices_on_section(x[mask], y[mask])
    return masks, indices


def get_sorted_indices_on_section(x, y):
    """Return the list of sorted along a curve."""
    n = x.size  # number of points on curve
    to_skip = 100.0  # awfully large value
    # Compute the distance matrices.
    dist = numpy.zeros((n, n))
    for i, (xi, yi) in enumerate(zip(x, y)):
        for j, (xj, yj) in enumerate(zip(x, y)):
            dist[i, j] = numpy.sqrt((xi - xj)**2 + (yi - yj)**2)
    numpy.fill_diagonal(dist, to_skip)
    # Sort indices based on minimum distance with neighbors.
    start = numpy.argmax(y)  # heuristic: start from highest point
    indices = [start]  # list of sorted indices to fill
    end = start  # initialize
    for _ in range(n - 1):
        start = end
        end = numpy.argmin(dist[start])
        dist[:, start] = to_skip  # do not visit start point again
        indices.append(end)
    return indices


def order_pressure_all_sections(p, masks, indices):
    """Re-order surface pressure along each cross-section."""
    n_sections = indices.shape[0]
    p_new = numpy.empty_like(indices, dtype=float)
    for s in range(n_sections):
        p_new[s] = p[masks[s]][indices[s]]
    return p_new


def save_surface_pressure_coefficients(filepath, x, y, cp):
    """Save data to file."""
    with open(filepath, 'w') as outfile:
        numpy.savetxt(outfile, numpy.c_[x, y, cp], header='x y Cp')


# Parse command-line options.
args = rodney.parse_command_line()

# Set case directory and data directory.
maindir = pathlib.Path(__file__).absolute().parents[1]
casedir = maindir / 'output' / 'LES'
datadir = casedir / 'postProcessing' / 'wallPressure'
figdir = maindir / 'figures'

# Set time range to process.
times = rodney.get_time_directories(datadir, limits=(50.0, 100.0), stride=1)

filename = 'p_snake.raw'  # name of files containing surface pressure

# Get ordering and cross-section coordinates from reference file.
filepath = datadir / rodney.time_to_str(times[0]) / filename
with open(filepath, 'r') as infile:
    x, y, z, _ = numpy.loadtxt(infile, unpack=True)
masks, indices = get_sorted_indices_all_sections(x, y, z)
xs, ys = x[masks[0]][indices[0]], y[masks[0]][indices[0]]

# Compute the time-averaged spanwise-averaged surface pressure.
p_avg = numpy.zeros_like(xs)
for time in tqdm.tqdm(times):
    filepath = datadir / rodney.time_to_str(time) / filename
    with open(filepath, 'r') as infile:
        p = numpy.loadtxt(infile, usecols=(3,), unpack=True)
    p = order_pressure_all_sections(p, masks, indices)
    p_avg += numpy.mean(p, axis=0)  # spanwise averaging
p_avg /= len(times)  # temporal averaging

# Convert to surface pressure coefficient.
rho, U_inf, c = 1.0, 1.0, 1.0  # density, freestream speed, chord-length
p_dyn = 0.5 * rho * U_inf * c
cp = p_avg / p_dyn

# Save surface pressure coefficient to file.
outdir = maindir / 'data'
outdir.mkdir(parents=True, exist_ok=True)
filepath = outdir / 'surface_pressure_coefficient.txt'
save_surface_pressure_coefficients(filepath, xs / c, ys / c, cp)

# Set default font family and size for Matplotlib figures.
pyplot.rc('font', family='serif', size=14)

# Plot the surface pressure coefficient.
fig, ax = pyplot.subplots(figsize=(6.0, 4.0))
ax.set_xlabel('$x / c$')
ax.set_ylabel('$C_p$')
ax.plot(xs / c, cp, color='black')
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
fig.tight_layout()

if args.save_figures:
    # Save Matplotlib figures.
    figdir.mkdir(parents=True, exist_ok=True)
    filepath = figdir / 'surface_pressure_coefficient.png'
    fig.savefig(filepath, dpi=300, bbox_inches='tight')

if args.show_figures:
    # Display the Matplotlib figure.
    pyplot.show()
