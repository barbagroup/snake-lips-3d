"""Plot the centerline mean streamwise velocity."""

from matplotlib import pyplot
import numpy
import pathlib
from scipy import interpolate
import tqdm

import rodney


# Parse command-line options.
args = rodney.parse_command_line()

# Set directories.
maindir = pathlib.Path(__file__).absolute().parents[1]
casedir = maindir / 'output' / 'LES'
datadir = casedir / 'postProcessing' / 'surfaceProfiles'
figdir = maindir / 'figures'

# Get time values to process.
times = rodney.get_time_directories(datadir, limits=(50.0, 100.0), stride=1)

# Set parameters.
U_inf, c = 1.0, 1.0  # freestream speed and chord length

# Create interpolation grid.
xlims, zlims = (0.3, 10.0), (-1.6, 1.6)
nx, nz = 200, 100
Xi, Zi = rodney.create_regular_grid_2d(xlims, zlims, nx, nz)

filename = 'U_yNormal_x0.0.raw'
initialized = False
for time in tqdm.tqdm(times):
    filepath = datadir / rodney.time_to_str(time) / filename
    with open(filepath, 'r') as infile:
        x, z, ux = numpy.loadtxt(infile, usecols=(0, 2, 3), unpack=True)
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

# Save mean streamwise velocity along centerline to file.
outdir = maindir / 'data'
outdir.mkdir(parents=True, exist_ok=True)
filepath = outdir / 'u_centerline_profile.txt'
with open(filepath, 'w') as outfile:
    numpy.savetxt(outfile, numpy.c_[Xi[0] / c, ux_avg / U_inf],
                  header='x/c <u>/U')

# Set default font family and size of Matplotlib figures.
pyplot.rc('font', family='serif', size=14)

# Plot profile of the mean streamwise velocity along the centerline.
fig, ax = pyplot.subplots(figsize=(6.0, 4.0))
ax.set_xlabel('x / c')
ax.set_ylabel(r'$<u> / U_\infty$')
ax.plot(Xi[0] / c, ux_avg / U_inf, color='black')
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
fig.tight_layout()

if args.save_figures:
    # Save Matplotlib figures.
    figdir.mkdir(parents=True, exist_ok=True)
    filepath = figdir / 'u_centerline_profile.png'
    fig.savefig(filepath, dpi=300, bbox_inches='tight')

if args.show_figures:
    # Display Matplotlib figures.
    pyplot.show()
