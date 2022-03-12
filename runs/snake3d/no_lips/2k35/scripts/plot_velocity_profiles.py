"""Plot profiles of mean streamwise and transversal velocity components."""

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
times = rodney.get_saved_times(datadir, limits=(50.0, 100.0), stride=1)

# Set parameters.
U_inf, c = 1.0, 1.0  # freestream speed and chord length

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
    # Load grid-point coordinates from reference file.
    filepath = datadir / rodney.time_to_str(times[0]) / filename
    with open(filepath, 'r') as infile:
        y0, z0 = numpy.loadtxt(infile, unpack=True, usecols=(1, 2))
    # Compute temporal sum of velocity components on surface plane.
    initialized = False
    for time in tqdm.tqdm(times):
        # Load velocity components from file.
        filepath = datadir / rodney.time_to_str(time) / filename
        with open(filepath, 'r') as infile:
            ux, uy = numpy.loadtxt(infile, unpack=True, usecols=(3, 4))
        if not initialized:
            ux_avg, uy_avg = ux.copy(), uy.copy()
            initialized = True
        else:
            ux_avg += ux
            uy_avg += uy
    # Apply spatial mask.
    y, z, ux_avg = rodney.apply_spatial_mask_2d(y0, z0, ux_avg, ylims, zlims)
    y, z, uy_avg = rodney.apply_spatial_mask_2d(y0, z0, uy_avg, ylims, zlims)
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
    profiles[xloc] = dict(y=Yi[0] / c, ux=ux_avg / U_inf, uy=uy_avg / U_inf)

# Save profiles to file.
outdir = maindir / 'data'
outdir.mkdir(parents=True, exist_ok=True)
for xloc, profile in profiles.items():
    filepath = outdir / f'velocity_profile_x{xloc}.txt'
    with open(filepath, 'w') as outfile:
        y, ux, uy = profile['y'], profile['ux'], profile['uy']
        numpy.savetxt(outfile, numpy.c_[y, ux, uy],
                      header='y/c <u>/U_inf <v>/U_inf')

# Set default font family and size of Matplotlib figures.
pyplot.rc('font', family='serif', size=10)

# Plot vertical profiles of the mean streamwise velocity.
fig, ax = pyplot.subplots(figsize=(6.0, 4.0))
ax.set_xlabel('y / D')
ax.set_ylabel(r'$<u> / U_\infty$')
y_offsets = {1.06: 4.5, 1.54: 3.1, 2.02: 2.1,
             4.0: 1.0, 7.0: 0.75, 10.0: 0.21}
for xloc, profile in profiles.items():
    ax.plot(profile['y'], y_offsets[xloc] + profile['ux'] - 1.0,
            color='black')
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
fig.tight_layout()

if args.save_figures:
    # Save Matplotlib figures.
    figdir.mkdir(parents=True, exist_ok=True)
    filepath = figdir / 'u_profiles.png'
    fig.savefig(filepath, dpi=300, bbox_inches='tight')

# Plot vertical profiles of the mean transversal velocity.
fig, ax = pyplot.subplots(figsize=(6.0, 4.0))
ax.set_xlabel('y / D')
ax.set_ylabel(r'$<v> / U_\infty$')
y_scale = {1.06: -0.7, 1.54: -1.4, 2.02: -2.1,
           4.0: -2.5, 7.0: -2.75, 10.0: -2.9}
for xloc, profile in profiles.items():
    ax.plot(profile['y'], y_scale[xloc] + profile['uy'],
            color='black')
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
