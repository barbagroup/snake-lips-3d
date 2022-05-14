import pathlib

import pyvista

import rodney


# Parse command-line options.
args = rodney.parse_command_line()

# Set directories.
maindir = pathlib.Path(__file__).absolute().parents[1]
datadir = maindir / 'output' / 'LES'
figdir = maindir / 'figures'

reader = pyvista.OpenFOAMReader(str(datadir / 'case.foam'))
mesh = reader.read()
front = mesh['boundary']['front']
front.translate((0.0, 0.0, 1.6), inplace=True)


def plot_meshgrid(filename, width, box, show=True, save=False):
    """Plot the meshgrid and optionally save it and show it."""

    def view_xy(width, box):
        """Get x/y view size, position, and focus."""
        xs, xe, ys, ye = box
        xc, yc = 0.5 * (xs + xe), 0.5 * (ys + ye)
        h = abs(ye - ys) / 2
        height = int(width * abs(ye - ys) / abs(xe - xs))

        window_size = (width, height)
        position = (xc, yc, h)
        focus = (xc, yc, -1.6)

        return window_size, position, focus

    window_size, position, focus = view_xy(width, box)
    p = pyvista.Plotter(window_size=window_size, off_screen=not show)
    p.add_mesh(front, color='#0A163B', style='wireframe')
    p.view_xy()
    p.add_axes(line_width=4, color='black',
               xlabel='X', ylabel='Y', zlabel=None)
    p.show_axes()
    p.set_background('white')
    p.set_position(position)
    p.set_focus(focus)
    p.set_viewup([0, 1, 0])
    p.camera.view_angle = 90.0

    kwargs = dict()
    if args.save_figures:
        figdir.mkdir(parents=True, exist_ok=True)
        filepath = figdir / filename
        kwargs['screenshot'] = filepath

    p.show(**kwargs)


kwargs = dict(show=args.show_figures, save=args.save_figures)
plot_meshgrid('pyvista_2d_meshgrid.png',
              1200, (-5, 10, -5, 5), **kwargs)
plot_meshgrid('pyvista_2d_meshgrid_zoom.png',
              600, (-0.6, 0.4, -0.5, 0.5), **kwargs)
