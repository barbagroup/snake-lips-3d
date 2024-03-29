"""Plot the centerline mean streamwise velocity."""

import pathlib
from dataclasses import dataclass

import numpy
import pandas
from matplotlib import pyplot

import rodney


# Parse command-line options.
args = rodney.parse_command_line(is_slow=True)

# Set directories.
maindir = pathlib.Path(__file__).absolute().parents[1]
figdir = maindir / 'figures'

vel_objs = [
    rodney.UxCenterlineData(
        'Base grid', maindir / 'fine',
        plt_kwargs=dict(color='C0', zorder=1)
    ),
    rodney.UxCenterlineData(
        'Coarse grid', maindir / 'nominal',
        plt_kwargs=dict(color='black', zorder=0)
    )
]

times = numpy.round(
    numpy.arange(start=50, stop=150 + 1e-3, step=0.05),
    decimals=2
)

df = pandas.DataFrame(columns=['Case', 'L_r/D', 'U_min', 'U_c', 'U_min/U_c'])

for vel_obj in vel_objs:
    if args.compute:
        vel_obj.compute(times)
        vel_obj.save('u_centerline_profile_50_150.txt')
    else:
        vel_obj.load('u_centerline_profile_50_150.txt')

    x, u = vel_obj.x, vel_obj.values
    # Compute the recirculation length.
    idx = numpy.where(u <= 0.0)[0][-1]
    xs, xe = 0.5, numpy.interp(0.0, u[idx:idx+2], x[idx:idx+2])
    Lr = xe - xs
    # Compute the minimum value of the velocity profile.
    U_min = numpy.nanmin(u)
    # Compute the asymptotic value of the velocity profile.
    U_c = numpy.mean(u[-21:-1])
    # Record results in dataframe.
    df.loc[len(df)] = [vel_obj.label, Lr, U_min, U_c, U_min / U_c]

print(df.set_index('Case').round(decimals=3))

# Load data from literature.
data = rodney.load_u_centerline_profiles_literature()

# Set default font family and size of Matplotlib figures.
pyplot.rc('font', family='serif', size=12)

# Plot profile of the mean streamwise velocity along the centerline.
fig, ax = pyplot.subplots(figsize=(6.0, 4.0))
ax.set_xlabel('$x / D$')
ax.set_ylabel(r'$<u> / U_\infty$')
U_inf, D = 1.0, 1.0
for vel_obj in vel_objs:
    ax.plot(vel_obj.x / D, vel_obj.values / U_inf,
            label=vel_obj.label, **vel_obj.plt_kwargs)
for i, (label, subdata) in enumerate(data.items(), start=1):
    ax.scatter(*subdata, label=label, s=5, color=f'C{i}', marker='o')
ax.axis([0.0, 10.0, -0.4, 0.8])
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.legend(frameon=False, fontsize=12)
fig.tight_layout()

if args.save_figures:
    figdir.mkdir(parents=True, exist_ok=True)
    filepath = figdir / 'u_centerline_profile.png'
    fig.savefig(filepath, dpi=300, bbox_inches='tight')

if args.show_figures:
    pyplot.show()
