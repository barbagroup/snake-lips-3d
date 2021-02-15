"""Plot the surface pressure coefficient."""

from matplotlib import pyplot
import numpy
import pathlib

import rodney


def sort_section(x, y, p):
    """Re-order cross-sectional values."""
    indices = numpy.argsort(numpy.degrees(numpy.arctan2(y, x)))
    return x[indices], y[indices], p[indices]


def sort_sections(x, y, z, p):
    """Re-order values (sorting along spanwise and section)."""
    indices = numpy.argsort(z)
    x, y, z, p = x[indices], y[indices], z[indices], p[indices]
    num_points = p.size
    num_sections = numpy.unique(z).size
    num_per_section = num_points // num_sections
    for i in range(num_sections):
        s, e = i * num_per_section, (i + 1) * num_per_section
        x[s:e], y[s:e], p[s:e] = sort_section(x[s:e], y[s:e], p[s:e])
        if i == 0:
            x_ref, y_ref = x[s:e].copy(), y[s:e].copy()
        else:
            assert (numpy.allclose(x[s:e], x_ref) and
                    numpy.allclose(y[s:e], y_ref))
    return x, y, z, p


def spanwise_average(x, y, z, p):
    """Compute the spanwise-average field."""
    num_points = p.size
    num_sections = numpy.unique(z).size
    num_per_section = num_points // num_sections
    return (x[:num_per_section], y[:num_per_section],
            numpy.mean(p.reshape((num_sections, num_per_section)), axis=0))


# Parse command-line options.
args = rodney.parse_command_line()

# Set case directory and data directory.
maindir = pathlib.Path(__file__).absolute().parents[2]
casedir = maindir / 'output' / 'LES'
datadir = casedir / 'postProcessing' / 'wallPressure'
figdir = maindir / 'figures'

# Set time range to process.
tstart, tend = 50.0, 150.0
times = numpy.sort([float(child.name) for child in datadir.iterdir()])
mask = numpy.where((times >= tstart) & (times <= tend))[0]
times = times[mask]

# Compute the time-averaged spanwise-average surface pressure.
filename = 'p_snake.raw'
for i, time in enumerate(times):
    # Load surface pressure at time-step index.
    folder = str(time)
    if folder.endswith('.0'):
        folder = folder[:-2]
    filepath = datadir / folder / filename
    with open(filepath, 'r') as infile:
        x, y, z, p = numpy.loadtxt(infile, dtype=numpy.float64, unpack=True)

    # Sort values along spanwise axis and per cross-section.
    x, y, z, p = sort_sections(x, y, z, p)

    # Average surface pressure along the spanwise axis.
    xs, ys, p_avg_t = spanwise_average(x, y, z, p)

    if i == 0:
        p_avg = p_avg_t.copy()
    else:
        p_avg += p_avg_t
p_avg /= times.size

# Compute the surface pressure coefficient.
rho, U_inf, D = 1.0, 1.0, 1.0
p_dyn = 0.5 * rho * U_inf * D
cp = p_avg / p_dyn

# Load data from Norberg (1994).
filepath = maindir / 'data' / 'norberg_1994_cp.csv'
with open(filepath, 'r') as infile:
    theta_exp, cp_exp = numpy.loadtxt(infile, delimiter=',', unpack=True)

# Set default font family and size for Matplotlib figures.
pyplot.rc('font', family='serif', size=14)

# Plot the surface pressure coefficient.
fig, ax = pyplot.subplots(figsize=(6.0, 4.0))
ax.set_xlabel(r'$\theta$')
ax.set_ylabel('$C_p$')
angles = 180 + numpy.degrees(numpy.arctan2(ys, xs))
mask = numpy.where(angles <= 180)[0]
ax.plot(angles[mask], cp[mask], label='Present', color='gray')
ax.scatter(theta_exp, cp_exp, label='Norberg (1994)',
           c='black', s=20, marker='s')
ax.set_xlim(0, 180)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.legend(frameon=False)
fig.tight_layout()

if args.save_figures:
    # Save Matplotlib figures.
    figdir.mkdir(parents=True, exist_ok=True)
    filepath = figdir / 'surface_pressure_coefficient.png'
    fig.savefig(filepath, dpi=300, bbox_inches='tight')

if args.show_figures:
    # Display the Matplotlib figure.
    pyplot.show()
