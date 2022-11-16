"""Plot profiles of mean streamwise and transversal velocity components."""

import pathlib

import numpy
from matplotlib import pyplot

import rodney


# Parse command-line options.
args = rodney.parse_command_line(is_slow=True)

# Set directories.
maindir = pathlib.Path(__file__).absolute().parents[1]
figdir = maindir / 'figures'

cases = {'1k': 'Re=1000', '2k': 'Re=2000', '3k': 'Re=3000'}

times = numpy.round(
    numpy.arange(start=100, stop=200 + 1e-3, step=0.05),
    decimals=2
)

data = dict()
for Re in cases.keys():
    vel_obj = rodney.VerticalVelocityProfilesData(
        None, maindir / f'{Re}35'
    )

    if args.compute:
        vel_obj.compute(times, from_tarball=True)
        vel_obj.save(f'velocity_profiles_100_200.txt')
    else:
        vel_obj.load(f'velocity_profiles_100_200.txt')

    data[Re] = vel_obj

# Set default font family and size of Matplotlib figures.
pyplot.rc('font', family='serif', size=12)

# Plot vertical profiles of the mean streamwise velocity.
fig, ax = pyplot.subplots(figsize=(6.0, 4.0))
ax.text(0.01, 0.9, r'$<u> / U_\infty - 1$', transform=ax.transAxes)
ax.set_xlabel('$x / c$')
ax.set_ylabel('$y / c$')
U_inf, c = 1.0, 1.0
xlocs = [1.06, 1.54, 2.02]
for i, (key, vel_obj) in enumerate(data.items()):
    for iloc, xloc in enumerate(xlocs):
        ax.axvline(iloc, color='black', linewidth=0.5)
        label = cases[key] if iloc == 0 else None
        y = vel_obj.y
        ux = vel_obj.values[xloc]['ux']
        ax.plot(iloc + (ux - U_inf) / U_inf, y / c,
                label=label, color=f'C{i}')
ax.legend(loc='lower left', frameon=False, fontsize=12)
ax.set_xticks(range(len(xlocs)))
ax.set_xticklabels(xlocs)
ax.axis([-1.4, 2.1, -3.0, 3.0])
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
fig.tight_layout()

if args.save_figures:
    figdir.mkdir(parents=True, exist_ok=True)
    filepath = figdir / 'u_profiles_35.png'
    fig.savefig(filepath, dpi=300, bbox_inches='tight')

# Plot vertical profiles of the mean transversal velocity.
fig, ax = pyplot.subplots(figsize=(6.0, 4.0))
ax.text(0.01, 0.9, r'$<v> / U_\infty$', transform=ax.transAxes)
ax.set_xlabel('$x / c$')
ax.set_ylabel('$y / c$')
xlocs = [1.06, 1.54, 2.02]
for i, (key, vel_obj) in enumerate(data.items()):
    for iloc, xloc in enumerate(xlocs):
        ax.axvline(iloc, color='black', linewidth=0.5)
        label = cases[key] if iloc == 0 else None
        y = vel_obj.y
        uy = vel_obj.values[xloc]['uy']
        ax.plot(iloc + uy / U_inf, y / c,
                label=label, color=f'C{i}')
ax.legend(loc='lower left', frameon=False, fontsize=12)
ax.set_xticks(range(len(xlocs)))
ax.set_xticklabels(xlocs)
ax.axis([-1.4, 2.1, -3.0, 3.0])
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
fig.tight_layout()

if args.save_figures:
    figdir.mkdir(parents=True, exist_ok=True)
    filepath = figdir / 'v_profiles_35.png'
    fig.savefig(filepath, dpi=300, bbox_inches='tight')

if args.show_figures:
    pyplot.show()
