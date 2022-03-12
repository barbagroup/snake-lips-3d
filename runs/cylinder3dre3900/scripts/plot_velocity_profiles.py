"""Plot profiles of mean streamwise and transversal velocity components."""

import pathlib

from matplotlib import pyplot

import rodney


# Parse command-line options.
args = rodney.parse_command_line()

# Set directories.
maindir = pathlib.Path(__file__).absolute().parents[1]
figdir = maindir / 'figures'

vel_objs = [
    rodney.VerticalVelocityProfilesData(
        'Smagorinsky', maindir / 'smagorinsky' / 'fine',
        plt_kwargs=dict(color='black', linestyle='-')
    ),
    rodney.VerticalVelocityProfilesData(
        'WALE', maindir / 'wale' / 'fine',
        plt_kwargs=dict(color='black', linestyle='--')
    )
]

time_limits = (50.0, 150.0)
for vel_obj in vel_objs:
    if args.compute:
        vel_obj.compute('x', time_limits=time_limits, verbose=True)
        vel_obj.save(f'u_profiles_50_150.txt')
    else:
        vel_obj.load(f'u_profiles_50_150.txt')

# Set default font family and size of Matplotlib figures.
pyplot.rc('font', family='serif', size=10)

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
                y_offsets[xloc] + (vel_obj.values[xloc] - U_inf) / U_inf,
                label=label, **vel_obj.plt_kwargs)
for label, subdata in data.items():
    ax.scatter(*subdata, label=label, s=10)
ax.set_xlim(-3.0, 3.0)
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 1.0, box.height])
ax.legend(loc='upper left', bbox_to_anchor=(1, 1), frameon=False)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
fig.tight_layout()

if args.save_figures:
    figdir.mkdir(parents=True, exist_ok=True)
    filepath = figdir / 'u_profiles.png'
    fig.savefig(filepath, dpi=300, bbox_inches='tight')

for vel_obj in vel_objs:
    if args.compute:
        vel_obj.compute('y', time_limits=time_limits, verbose=True)
        vel_obj.save('v_profiles_50_150.txt')
    else:
        vel_obj.load('v_profiles_50_150.txt')

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
                y_scale[xloc] + vel_obj.values[xloc] / U_inf,
                label=label, **vel_obj.plt_kwargs)
for label, subdata in data.items():
    ax.scatter(*subdata, label=label, s=10)
ax.set_xlim(-3.0, 3.0)
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 1.0, box.height])
ax.legend(loc='upper left', bbox_to_anchor=(1, 1), frameon=False)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
fig.tight_layout()

if args.save_figures:
    figdir.mkdir(parents=True, exist_ok=True)
    filepath = figdir / 'v_profiles.png'
    fig.savefig(filepath, dpi=300, bbox_inches='tight')

if args.show_figures:
    pyplot.show()
