import pathlib

import numpy
import pyvista
from matplotlib import patches, pyplot

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
body = body.slice(normal='y')
xb, zb = body.points[:, 0], body.points[:, 2]

times = numpy.arange(100.0, 200.0 + 1, 5.0)
times = [150, 180]

for time in times:
    reader = pyvista.OpenFOAMReader(str(datadir / 'case.foam'))
    reader.set_active_time_value(time)
    print(f'[time = {reader.active_time_value}]')

    mesh = reader.read()
    internal_mesh = mesh['internalMesh']
    internal_mesh.set_active_scalars('U')

    slice_center = internal_mesh.slice(normal='y')

    ux = slice_center.get_array('U', preference='point')[:, 0]
    uy = slice_center.get_array('U', preference='point')[:, 1]
    x, z = slice_center.points[:, 0], slice_center.points[:, 2]

    fig, ax = pyplot.subplots(figsize=(6.0, 6.0))
    ax.set_xlabel('x / c')
    ax.set_ylabel('z / c')
    tcf = ax.tricontourf(
        x, z, uy,
        levels=numpy.linspace(-1.0, 1.0, num=20), extend='both', cmap='RdBu_r'
    )
    rect = patches.Rectangle([xb.min(), zb.min()],
                             xb.max() - xb.min(), zb.max() - zb.min(),
                             color='gray')
    ax.add_patch(rect)
    ax.axis('scaled')
    ax.set_xlim(0.0, 8.0)
    ax.set_ylim(z.min(), z.max())
    cax = ax.inset_axes([1.01, 0.0, 0.02, 1.0], transform=ax.transAxes)
    fig.colorbar(tcf, ax=ax, cax=cax,
                 ticks=[-1, -0.5, 0, 0.5, 1], extendfrac=0.0)
    fig.tight_layout()

    if args.save_figures:
        figdir.mkdir(parents=True, exist_ok=True)
        filepath = figdir / f'pyvista_2d_contours_uy_{time:0.0f}.png'
        fig.savefig(filepath, dpi=300, bbox_inches='tight')

    pyplot.close(fig)

    fig, ax = pyplot.subplots(figsize=(6.0, 6.0))
    ax.set_xlabel('x / c')
    ax.set_ylabel('z / c')
    ax.tricontourf(x, z, ux,
                   levels=numpy.linspace(-1.0, 1.0, num=20), extend='both',
                   cmap='RdBu_r')
    rect = patches.Rectangle([xb.min(), zb.min()],
                             xb.max() - xb.min(), zb.max() - zb.min(),
                             color='gray')
    ax.add_patch(rect)
    ax.axis('scaled')
    ax.set_xlim(0.0, 8.0)
    ax.set_ylim(z.min(), z.max())
    cax = ax.inset_axes([1.01, 0.0, 0.02, 1.0], transform=ax.transAxes)
    fig.colorbar(tcf, ax=ax, cax=cax,
                 ticks=[-1, -0.5, 0, 0.5, 1], extendfrac=0.0)
    fig.tight_layout()

    if args.save_figures:
        filepath = figdir / f'pyvista_2d_contours_ux_{time:0.0f}.png'
        fig.savefig(filepath, dpi=300, bbox_inches='tight')

    pyplot.close(fig)
