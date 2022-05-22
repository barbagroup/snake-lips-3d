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
        'Present (WALE, nominal)', maindir / 'nominal',
        plt_kwargs=dict(color='C0', zorder=1)
    ),
    rodney.VerticalVelocityProfilesData(
        'Present (WALE, fine)', maindir / 'fine',
        plt_kwargs=dict(color='black', zorder=0)
    )
]

times = numpy.round(
    numpy.arange(start=50, stop=150 + 1e-3, step=0.05),
    decimals=2
)

for vel_obj in vel_objs:
    if args.compute:
        vel_obj.compute(times)
        vel_obj.save(f'velocity_profiles_50_150.txt')
    else:
        vel_obj.load(f'velocity_profiles_50_150.txt')

# Set default font family and size of Matplotlib figures.
pyplot.rc('font', family='serif', size=12)

# Load data from literature.
data = rodney.load_u_profiles_literature()

# Plot vertical profiles of the mean streamwise velocity.
fig, ax = pyplot.subplots(figsize=(8.0, 4.0))
ax.set_xlabel('y / D')
ax.set_ylabel(r'$<u> / U_\infty$')
U_inf, D = 1.0, 1.0
y_offsets = {1.06: 4.5, 1.54: 3.1, 2.02: 2.1,
             4.0: 1.0, 7.0: 0.75, 10.0: 0.21}
for vel_obj in vel_objs:
    for xloc in vel_obj.xlocs:
        label = vel_obj.label if xloc == 1.06 else None
        ax.plot(vel_obj.y / D,
                y_offsets[xloc] + (vel_obj.values[xloc]['ux'] - U_inf) / U_inf,
                label=label, **vel_obj.plt_kwargs)
for i, (label, subdata) in enumerate(data.items(), start=1):
    ax.scatter(*subdata, label=label, s=5, color=f'C{i}', marker='o')
ax.set_xlim(-3.0, 3.0)
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 1.0, box.height])
ax.legend(loc='upper left', bbox_to_anchor=(1, 1), frameon=False, fontsize=10)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
fig.tight_layout()

if args.save_figures:
    figdir.mkdir(parents=True, exist_ok=True)
    filepath = figdir / 'u_profiles.png'
    fig.savefig(filepath, dpi=300, bbox_inches='tight')

# Load data from literature.
data = rodney.load_v_profiles_literature()

# Plot vertical profiles of the mean transversal velocity.
fig, ax = pyplot.subplots(figsize=(8.0, 4.0))
ax.set_xlabel('y / D')
ax.set_ylabel(r'$<v> / U_\infty$')
y_scale = {1.06: -0.7, 1.54: -1.4, 2.02: -2.1,
           4.0: -2.5, 7.0: -2.75, 10.0: -2.9}
for vel_obj in vel_objs:
    for xloc in vel_obj.xlocs:
        label = vel_obj.label if xloc == 1.06 else None
        ax.plot(vel_obj.y,
                y_scale[xloc] + vel_obj.values[xloc]['uy'] / U_inf,
                label=label, **vel_obj.plt_kwargs)
for i, (label, subdata) in enumerate(data.items(), start=1):
    ax.scatter(*subdata, label=label, s=5, color=f'C{i}', marker='o')
ax.set_xlim(-3.0, 3.0)
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 1.0, box.height])
ax.legend(loc='upper left', bbox_to_anchor=(1, 1), frameon=False, fontsize=10)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
fig.tight_layout()

if args.save_figures:
    figdir.mkdir(parents=True, exist_ok=True)
    filepath = figdir / 'v_profiles.png'
    fig.savefig(filepath, dpi=300, bbox_inches='tight')

if args.show_figures:
    pyplot.show()
