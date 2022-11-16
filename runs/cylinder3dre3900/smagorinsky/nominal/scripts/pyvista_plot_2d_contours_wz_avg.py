from curses import noraw
import pathlib

import numpy
import pyvista
from matplotlib import pyplot

import rodney


def slice_z_center(mesh):
    slice_mesh = mesh.slice(normal='z')
    slice_mesh.translate((0, 0, -slice_mesh.center[-1]), inplace=True)
    return slice_mesh


# Parse command-line options.
args = rodney.parse_command_line()

# Set directories.
maindir = pathlib.Path(__file__).absolute().parents[1]
datadir = maindir / 'output' / 'LES-tmp'
figdir = maindir / 'figures'

reader = pyvista.OpenFOAMReader(str(datadir / 'case.foam'))
reader.set_active_time_value(150.0)

mesh = reader.read()
internal_mesh = mesh['internalMesh']
internal_mesh.set_active_scalars('U')

internal_mesh = internal_mesh.compute_derivative(
    vorticity=True, faster=True, progress_bar=True
)

slice_center = internal_mesh.slice(normal='z')

slices = internal_mesh.slice_along_axis(n=21, axis='z')

wz_avg = numpy.zeros_like(slice_center.points[:, 0])

for i in range(len(slices)):
    slice_interp = slice_center.interpolate(slices[i])
    wz = slice_interp.get_array('vorticity', preference='point')[:, 2]
    wz_avg += wz

wz_avg /= len(slices)

pyplot.rc('font', family='serif', size=12)
fig, ax = pyplot.subplots(figsize=(6.0, 6.0))
ax.set_xlabel('x / D')
ax.set_ylabel('y / D')
x, y = slice_center.points[:, 0], slice_center.points[:, 1]
ax.tricontourf(x, y, wz_avg,
               levels=numpy.linspace(-5.0, 5.0, num=20), extend='both')
ax.add_patch(pyplot.Circle((0.0, 0.0), 0.5, color='gray'))
ax.axis('scaled')
ax.set_xlim(-1.0, 8.0)
ax.set_ylim(-2.0, 2.0)
fig.tight_layout()

if args.save_figures:
    figdir.mkdir(parents=True, exist_ok=True)
    filepath = figdir / 'pyvista_2d_contours_wz_avg.png'
    fig.savefig(filepath, dpi=300, bbox_inches='tight')

if args.show_figures:
    pyplot.show()
