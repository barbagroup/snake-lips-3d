"""Plot profiles of mean streamwise and transversal velocity components."""

from matplotlib import pyplot
import numpy
import pathlib
from scipy import interpolate

import rodney


# Parse command-line options.
args = rodney.parse_command_line()

# Set directories.
maindir = pathlib.Path(__file__).absolute().parents[1]
casedir = maindir / 'output' / 'LES'
datadir = casedir / 'postProcessing' / 'surfaceProfiles'
figdir = maindir / 'figures'

# Get time values to process.
times = rodney.get_time_directories(datadir, limits=(50.0, 150.0), stride=1)

# Set parameters.
U_inf, D = 1.0, 1.0

# Create interpolation grid.
ylims, zlims = (-3.0, 3.0), (-1.6, 1.6)
ny, nz = 200, 100
Yi, Zi = rodney.create_regular_grid_2d(ylims, zlims, ny, nz)

# Compute profiles of the mean streamwise and transversal velocities.
xlocs = [1.06, 1.54, 2.02, 4.0, 7.0, 10.0]  # locations along x-axis
profiles = dict()
for xloc in xlocs:
    print(f'[INFO] Computing average velocity at x/D={xloc} ...')
    filename = f'U_xNormal_x{xloc:.2f}.raw'
    initialized = False
    for time in times:
        filepath = datadir / rodney.time_to_str(time) / filename
        with open(filepath, 'r') as infile:
            y0, z0, ux, uy = numpy.loadtxt(infile, unpack=True,
                                           usecols=(1, 2, 3, 4))
        y, z, ux = rodney.apply_spatial_mask_2d(y0, z0, ux, ylims, zlims)
        y, z, uy = rodney.apply_spatial_mask_2d(y0, z0, uy, ylims, zlims)
        if not initialized:
            ux_avg, uy_avg = ux.copy(), uy.copy()
            initialized = True
        else:
            ux_avg += ux
            uy_avg += uy
    # Average data over time.
    ux_avg /= times.size
    uy_avg /= times.size
    # Interpolate data on 2D regular grid.
    ux_avg = interpolate.griddata((y, z), ux_avg, (Yi, Zi), method='linear')
    uy_avg = interpolate.griddata((y, z), uy_avg, (Yi, Zi), method='linear')
    # Average data along spanwise axis.
    ux_avg = numpy.mean(ux_avg, axis=0)
    uy_avg = numpy.mean(uy_avg, axis=0)
    # Record profiles.
    profiles[xloc] = dict(y=Yi[0], ux=ux_avg, uy=uy_avg)

# Set default font family and size of Matplotlib figures.
pyplot.rc('font', family='serif', size=10)

# Load data from literature.
data = rodney.load_u_profiles_literature()

# Plot vertical profiles of the mean streamwise velocity.
fig, ax = pyplot.subplots(figsize=(6.0, 4.0))
ax.set_xlabel('y / D')
ax.set_ylabel(r'$<u> / U_\infty$')
y_offsets = {1.06: 4.5, 1.54: 3.1, 2.02: 2.1,
             4.0: 1.0, 7.0: 0.75, 10.0: 0.21}
for xloc, profile in profiles.items():
    label = f'x/D = {xloc}'
    label = 'Present' if xloc == 1.06 else None
    ax.plot(profile['y'], y_offsets[xloc] + (profile['ux'] - U_inf) / U_inf,
            label=label, color='black')
for label, subdata in data.items():
    ax.scatter(*subdata, label=label)
ax.legend(frameon=False)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
fig.tight_layout()

if args.save_figures:
    # Save Matplotlib figures.
    figdir.mkdir(parents=True, exist_ok=True)
    filepath = figdir / 'u_profiles.png'
    fig.savefig(filepath, dpi=300, bbox_inches='tight')

# Load data from literature.
data = rodney.load_v_profiles_literature()

# Plot vertical profiles of the mean transversal velocity.
fig, ax = pyplot.subplots(figsize=(6.0, 4.0))
ax.set_xlabel('y / D')
ax.set_ylabel(r'$<v> / U_\infty$')
y_scale = {1.06: -0.7, 1.54: -1.4, 2.02: -2.1,
           4.0: -2.5, 7.0: -2.75, 10.0: -2.9}
for xloc, profile in profiles.items():
    label = 'Present' if xloc == 1.06 else None
    ax.plot(profile['y'], y_scale[xloc] + profile['uy'] / U_inf,
            label=label, color='black')
for label, subdata in data.items():
    ax.scatter(*subdata, label=label)
ax.legend(frameon=False)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
fig.tight_layout()

if args.save_figures:
    # Save Matplotlib figures.
    figdir.mkdir(parents=True, exist_ok=True)
    filepath = figdir / 'v_profiles.png'
    fig.savefig(filepath, dpi=300, bbox_inches='tight')

if args.show_figures:
    # Display Matplotlib figures.
    pyplot.show()
