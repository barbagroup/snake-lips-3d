import pathlib

import numpy
import pyvista
from matplotlib import pyplot

import rodney


# Parse command-line options.
args = rodney.parse_command_line()

# Set directories.
maindir = pathlib.Path(__file__).absolute().parents[1]
datadir = maindir / 'output' / 'LES'
figdir = maindir / 'figures'

pyplot.rc('font', family='serif', size=12)

filepath = maindir / 'RANS' / 'constant' / 'triSurface' / 'snake.obj'
body = pyvista.get_reader(str(filepath)).read()
body = body.slice(normal='z')
xb, yb = body.points[:, 0], body.points[:, 1]

times = numpy.arange(100.0, 150.0 + 1, 5.0)
times = [135]

for time in times:
    reader = pyvista.OpenFOAMReader(str(datadir / 'case.foam'))
    reader.set_active_time_value(time)
    print(f'[time = {reader.active_time_value}]')

    mesh = reader.read()
    internal_mesh = mesh['internalMesh']
    internal_mesh.set_active_scalars('U')

    internal_mesh = internal_mesh.compute_derivative(
        vorticity=True, faster=True, progress_bar=True
    )

    slice_center = internal_mesh.slice(normal='z', origin=(0.0, 0.0, 0.0))
    wz = slice_center.get_array('vorticity', preference='point')[:, 2]

    fig, ax = pyplot.subplots(figsize=(6.0, 6.0))
    ax.set_xlabel('x / c')
    ax.set_ylabel('y / c')
    x, y = slice_center.points[:, 0], slice_center.points[:, 1]
    tcf = ax.tricontourf(
        x, y, wz,
        levels=numpy.linspace(-10.0, 10.0, num=20), extend='both'
    )
    ax.fill(xb, yb, color='gray')
    ax.axis('scaled')
    ax.set_xlim(-1.0, 4.0)
    ax.set_ylim(-1.5, 1.5)
    cax = ax.inset_axes([1.01, 0.0, 0.02, 1.0], transform=ax.transAxes)
    fig.colorbar(tcf, ax=ax, cax=cax,
                 ticks=[-10, -5, 0, 5, 10], extendfrac=0.0)
    fig.tight_layout()

    if args.save_figures:
        figdir.mkdir(parents=True, exist_ok=True)
        filepath = figdir / f'pyvista_2d_contours_wz_{int(time):0>4}.png'
        fig.savefig(filepath, dpi=300, bbox_inches='tight')

    pyplot.close(fig)
