"""Plot the centerline mean streamwise velocity."""

from matplotlib import pyplot
import numpy
import pathlib
from scipy import interpolate

import rodney


# Parse command-line options.
args = rodney.parse_command_line()

# Set directories.
maindir = pathlib.Path(__file__).absolute().parents[1]
figdir = maindir / 'figures'
folders = ['nominal', 'fine']
plot_kwargs = [dict(label='nominal', color='black', linestyle='-'),
               dict(label='fine', color='black', linestyle='--')]

# Set parameters.
U_inf, D = 1.0, 1.0

# Create interpolation grid.
xlims, zlims = (0.5, 10.0), (-1.6, 1.6)
nx, nz = 200, 100
Xi, Zi = rodney.create_regular_grid_2d(xlims, zlims, nx, nz)

ux_avg_all = []
for i, folder in enumerate(folders):
    casedir = maindir / folder / 'output' / 'LES'
    datadir = casedir / 'postProcessing' / 'surfaceProfiles'

    # Get time values to process.
    times = rodney.get_time_directories(datadir, limits=(50.0, 150.0), stride=1)

    filename = 'U_yNormal_x0.0.raw'
    initialized = False
    for time in times:
        filepath = datadir / rodney.time_to_str(time) / filename
        with open(filepath, 'r') as infile:
            x, z, ux = numpy.loadtxt(infile, usecols=(0, 2, 3), unpack=True)
        x, z, ux = rodney.apply_spatial_mask_2d(x, z, ux, xlims, zlims)
        if not initialized:
            ux_avg = ux.copy()
            initialized = True
        else:
            ux_avg += ux
    # Average in time.
    ux_avg /= times.size
    # Interpolate data on regular grid.
    ux_avg = interpolate.griddata((x, z), ux_avg, (Xi, Zi), method='linear')
    # Average along spanwise axis.
    ux_avg = numpy.mean(ux_avg, axis=0)

    # Record.
    ux_avg_all.append(ux_avg)

# Load data from literature.
data = rodney.load_u_centerline_profiles_literature()

# Set default font family and size of Matplotlib figures.
pyplot.rc('font', family='serif', size=14)

# Plot profile of the mean streamwise velocity along the centerline.
fig, ax = pyplot.subplots(figsize=(6.0, 4.0))
ax.set_xlabel('x / D')
ax.set_ylabel(r'$<u> / U_\infty$')
for ux_avg, plot_kw in zip(ux_avg_all, plot_kwargs):
    ax.plot(Xi[0], ux_avg / U_inf, **plot_kw)
for label, subdata in data.items():
    ax.scatter(*subdata, label=label, s=10)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.legend(frameon=False)
fig.tight_layout()

if args.save_figures:
    # Save Matplotlib figures.
    figdir.mkdir(parents=True, exist_ok=True)
    filepath = figdir / 'u_centerline_profile.png'
    fig.savefig(filepath, dpi=300, bbox_inches='tight')

if args.show_figures:
    # Display Matplotlib figures.
    pyplot.show()
