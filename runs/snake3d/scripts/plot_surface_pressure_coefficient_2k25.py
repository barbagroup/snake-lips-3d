"""Plot the surface pressure coefficient."""

import pathlib

import numpy
import pandas
from matplotlib import pyplot

import rodney


# Parse command-line options.
args = rodney.parse_command_line(is_slow=True)

# Set directories.
maindir = pathlib.Path(__file__).absolute().parents[1]
figdir = maindir / 'figures'

cases = {
    'Both': 'both_lips/2k25',
    'Front': 'front_lip/2k25',
    'Back': 'back_lip/2k25',
    'None': 'no_lips/2k25'
}

cp_objs = [
    rodney.SurfacePressureData(label, maindir / folder)
    for label, folder in cases.items()
]

times = numpy.round(
    numpy.arange(start=100, stop=200 + 1e-3, step=0.05),
    decimals=2
)

df = pandas.DataFrame(columns=['Case', 'min(C_p)'])

for cp_obj in cp_objs:
    if args.compute:
        cp_obj.compute(times, from_tarball=True)
        cp_obj.save('surface_pressure_coefficient_100_200.txt')
    else:
        cp_obj.load('surface_pressure_coefficient_100_200.txt')

    mask = numpy.where(abs(cp_obj.x - min(cp_obj.x)) < 0.1)[0]
    cp_min = min(cp_obj.values[mask])
    df.loc[len(df)] = [cp_obj.label, cp_min]

print(df.set_index('Case').round(decimals=2))

# Set default font family and size for Matplotlib figures.
pyplot.rc('font', family='serif', size=12)

wrap = lambda arr: numpy.append(arr, arr[0])

# Plot the surface pressure coefficient.
fig, ax = pyplot.subplots(figsize=(6.0, 4.0))
ax.set_xlabel('$x / c$')
ax.set_ylabel('$C_p$')
for cp_obj in cp_objs:
    ax.plot(wrap(cp_obj.x), wrap(cp_obj.values), label=cp_obj.label)
ax.legend(loc='lower right', ncol=2, frameon=False, fontsize=12)
ax.set_xlim(-0.6, 0.4)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
fig.tight_layout()

if args.save_figures:
    figdir.mkdir(parents=True, exist_ok=True)
    filepath = figdir / 'surface_pressure_coefficient_2k25.png'
    fig.savefig(filepath, dpi=300, bbox_inches='tight')

if args.show_figures:
    pyplot.show()
