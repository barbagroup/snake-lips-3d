import pathlib

import numpy
import pyvista

import rodney


# Parse command-line options.
args = rodney.parse_command_line()

# Set directories.
maindir = pathlib.Path(__file__).absolute().parents[1]
datadir = maindir / 'output' / 'LES'
figdir = maindir / 'figures'

times = numpy.arange(120.0, 120.0 + 1, 5.0)

for time in times:
    print(f'[time {time}] Plotting Q-criterion ...')
    reader = pyvista.OpenFOAMReader(str(datadir / 'case.foam'))
    reader.set_active_time_value(time)

    mesh = reader.read()
    internal_mesh = mesh['internalMesh']
    internal_mesh.set_active_scalars('U')

    internal_mesh = internal_mesh.compute_derivative(
        qcriterion=True, vorticity=True, faster=True, progress_bar=True
    )

    contours = internal_mesh.contour(
        isosurfaces=(0.1,), scalars='qcriterion', preference='point'
    )

    filepath = maindir / 'RANS' / 'constant' / 'triSurface' / 'snake.obj'
    body = pyvista.get_reader(str(filepath)).read()

    p = pyvista.Plotter(off_screen=True)
    p.add_mesh(internal_mesh.outline(), color='black')
    p.add_mesh(
        contours, scalars='vorticity', component=0,
        opacity=1.0, cmap='viridis', clim=[-2.0, 2.0], n_colors=3,
        scalar_bar_args=dict(title='wx', color='black')
    )
    p.add_mesh(body, color='black', opacity=0.5)
    p.add_axes(color='black')
    p.show_axes()
    p.set_position((-2, 5, 10))
    p.set_focus((2.0, 0, 0))
    p.background_color='white'

    kwargs = dict()
    if args.save_figures:
        figdir.mkdir(parents=True, exist_ok=True)
        filepath = figdir / f'pyvista_3d_contours_qcrit_{time:0.0f}.png'
        kwargs['screenshot'] = filepath

    p.show(**kwargs)
