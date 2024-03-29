"""Plot profiles of mean streamwise and transversal velocity components."""

import pathlib

from matplotlib import pyplot
import numpy

import rodney


# Parse command-line options.
args = rodney.parse_command_line(is_slow=True)

# Set directories.
maindir = pathlib.Path(__file__).absolute().parents[1]
figdir = maindir / 'figures'

vel_objs = [
    rodney.VerticalVelocityProfilesData(
        'Base grid', maindir / '2k35_fine',
        plt_kwargs=dict(color='C0', zorder=1)
    ),
    rodney.VerticalVelocityProfilesData(
        'Coarse grid', maindir / '2k35_nominal',
        plt_kwargs=dict(color='black', zorder=0)
    )
]

times = numpy.round(
    numpy.arange(start=50, stop=100 + 1e-3, step=0.05),
    decimals=2
)

for vel_obj in vel_objs:
    if args.compute:
        vel_obj.compute(times, from_tarball=True)
        vel_obj.save(f'velocity_profiles_50_100.txt')
    else:
        vel_obj.load(f'velocity_profiles_50_100.txt')

# Set default font family and size of Matplotlib figures.
pyplot.rc('font', family='serif', size=12)

# Plot vertical profiles of the mean streamwise velocity.
fig, ax = pyplot.subplots(figsize=(8.0, 4.0))
ax.text(0.01, 0.9, r'$<u> / U_\infty - 1$', transform=ax.transAxes)
ax.set_xlabel('$x / c$')
ax.set_ylabel('$y / c$')
U_inf, c = 1.0, 1.0
xlocs = [1.06, 1.54, 2.02, 4.0]
for vel_obj in vel_objs:
    for iloc, xloc in enumerate(xlocs):
        ax.axvline(iloc, color='black', linewidth=0.5)
        plt_label = vel_obj.label if iloc == 0 else None
        y = vel_obj.y
        ux = vel_obj.values[xloc]['ux']
        ax.plot(iloc + (ux - U_inf) / U_inf, y / c,
                label=plt_label, **vel_obj.plt_kwargs)
ax.legend(loc='lower left', frameon=False, fontsize=12)
ax.set_xticks(range(len(xlocs)))
ax.set_xticklabels(xlocs)
ax.axis([-1.5, 3.5, -3.0, 3.0])
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
ax.set_xlabel('$x / c$')
ax.set_ylabel('$y / c$')
xlocs = [1.06, 1.54, 2.02, 4.0]
for vel_obj in vel_objs:
    for iloc, xloc in enumerate(xlocs):
        ax.axvline(iloc, color='black', linewidth=0.5)
        plt_label = vel_obj.label if iloc == 0 else None
        y = vel_obj.y
        uy = vel_obj.values[xloc]['uy']
        ax.plot(iloc + uy / U_inf, y / c,
                label=plt_label, **vel_obj.plt_kwargs)
ax.legend(loc='lower left', frameon=False, fontsize=12)
ax.set_xticks(range(len(xlocs)))
ax.set_xticklabels(xlocs)
ax.axis([-1.5, 3.5, -3.0, 3.0])
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
fig.tight_layout()

if args.save_figures:
    figdir.mkdir(parents=True, exist_ok=True)
    filepath = figdir / 'v_profiles.png'
    fig.savefig(filepath, dpi=300, bbox_inches='tight')

if args.show_figures:
    pyplot.show()
