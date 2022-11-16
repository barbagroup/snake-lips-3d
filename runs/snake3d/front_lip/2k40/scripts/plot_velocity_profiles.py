"""Plot profiles of mean streamwise and transversal velocity components."""

import pathlib

import numpy
from matplotlib import pyplot

import rodney


# Parse command-line options.
args = rodney.parse_command_line()

# Set directories.
maindir = pathlib.Path(__file__).absolute().parents[1]
figdir = maindir / 'figures'

vel_obj = rodney.VerticalVelocityProfilesData('Present', maindir)

times = numpy.round(
    numpy.arange(start=100, stop=200 + 1e-3, step=0.05),
    decimals=2
)

if args.compute:
    vel_obj.compute(times, from_tarball=True)
    vel_obj.save(f'velocity_profiles_100_200.txt')
else:
    vel_obj.load(f'velocity_profiles_100_200.txt')

# Set default font family and size of Matplotlib figures.
pyplot.rc('font', family='serif', size=10)

# Plot vertical profiles of the mean streamwise velocity.
fig, ax = pyplot.subplots(figsize=(8.0, 4.0))
ax.text(0.01, 0.9, r'$<u> / U_\infty - 1$', transform=ax.transAxes)
ax.set_xlabel('x / c')
ax.set_ylabel('y / c')
U_inf, c = 1.0, 1.0
for iloc, xloc in enumerate(vel_obj.xlocs):
    y = vel_obj.y
    ux = vel_obj.values[xloc]['ux']
    ax.plot(iloc + (ux - U_inf) / U_inf, y / c, color='black')
    ax.axvline(iloc, color='black', linestyle=':', linewidth=0.5)
ax.set_xticks(range(len(vel_obj.xlocs)))
ax.set_xticklabels(vel_obj.xlocs)
ax.set_ylim(-3.0, 3.0)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
fig.tight_layout()

if args.save_figures:
    figdir.mkdir(parents=True, exist_ok=True)
    filepath = figdir / 'u_profiles.png'
    fig.savefig(filepath, dpi=300, bbox_inches='tight')

# Plot vertical profiles of the mean transversal velocity.
fig, ax = pyplot.subplots(figsize=(8.0, 4.0))
ax.text(0.01, 0.9, r'$<v> / U_\infty$', transform=ax.transAxes)
ax.set_xlabel('x / c')
ax.set_ylabel('y / c')
for iloc, xloc in enumerate(vel_obj.xlocs):
    y = vel_obj.y
    uy = vel_obj.values[xloc]['uy']
    ax.plot(iloc + uy / U_inf, y / c, color='black')
    ax.axvline(iloc, color='black', linestyle=':', linewidth=0.5)
ax.set_xticks(range(len(vel_obj.xlocs)))
ax.set_xticklabels(vel_obj.xlocs)
ax.set_ylim(-3.0, 3.0)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
fig.tight_layout()

if args.save_figures:
    figdir.mkdir(parents=True, exist_ok=True)
    filepath = figdir / 'v_profiles.png'
    fig.savefig(filepath, dpi=300, bbox_inches='tight')

if args.show_figures:
    pyplot.show()
