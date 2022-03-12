"""Assistant module with data processing classes."""

import pathlib
from dataclasses import dataclass

import numpy
from scipy import interpolate

from .forces import force_coefficients, load_forces_3d
from .misc import get_saved_times, get_stats, time_to_str
from .transforms import (apply_spatial_mask_2d, create_regular_grid_2d,
                         load_wall_pressure, pressure_coefficient,
                         sort_sections, spanwise_average)


@dataclass
class Vector:
    """3D vector."""

    x: numpy.ndarray
    y: numpy.ndarray
    z: numpy.ndarray

    @property
    def values(self):
        return self.x, self.y, self.z


@dataclass
class ForceCoefficientsData:
    """Data and metadata for the force coefficients."""

    label: str
    simudir: pathlib.Path = None

    @property
    def values(self):
        return self._values.values

    def compute(self, Lz=numpy.pi):
        """Load and compute the force coefficients."""
        datadir = (self.simudir / 'output' / 'LES' / 'postProcessing' /
                   'forces' / '0')
        filepath = datadir / 'forces.dat'
        self.times, fx, fy, fz = load_forces_3d(filepath)

        # Compute force coefficients.
        cd, cl, cz = force_coefficients((fx, fy, fz), Lz=Lz)
        self._values = Vector(cd, cl, cz)

    def get_stats(self, time_limits=None, verbose=False):
        """Compute and return statistics."""
        kwargs = dict(limits=time_limits, verbose=verbose)
        cd, cl, cz = self.values
        cd_stats = get_stats(self.times, cd, **kwargs)
        cl_stats = get_stats(self.times, cl, **kwargs)
        cz_stats = get_stats(self.times, cz, **kwargs)
        return cd_stats, cl_stats, cz_stats


@dataclass
class SurfacePressureData:
    """Data and metadata for the surface pressure coefficient."""

    label: str
    simudir: pathlib.Path = None
    x: numpy.ndarray = None
    y: numpy.ndarray = None
    values: numpy.ndarray = None
    plt_kwargs: dict = None

    def save(self, filename):
        """Save data to file."""
        datadir = self.simudir / 'data'
        datadir.mkdir(parents=True, exist_ok=True)
        filepath = datadir / filename
        with open(filepath, 'w') as outfile:
            numpy.savetxt(outfile, numpy.c_[self.x, self.y, self.values],
                          comments='Surface pressure coefficient (x, y, cp)')

    def load(self, filename):
        """Load data from file."""
        filepath = self.simudir / 'data' / filename
        with open(filepath, 'r') as infile:
            self.x, self.y, self.values = numpy.loadtxt(infile, unpack=True)

    def compute(self, time_limits=None):
        """Compute the time-averaged spanwise-averaged surface pressure."""
        # Directory with raw data.
        datadir = (self.simudir / 'output' / 'LES' /
                   'postProcessing' / 'wallPressure')

        # Get time values to process within interval.
        times = get_saved_times(datadir, limits=time_limits)

        initialized = False
        for time in times:
            # Load instantaneous surface pressure.
            xyz, p = load_wall_pressure(datadir, time, 'p_snake.raw')

            # Sort values along spanwise axis and per cross-section.
            if not initialized:
                index = sort_sections(xyz, p, return_index=True)
            x, y, z = xyz
            xyz = (x[index], y[index], z[index])
            p = p[index]

            # Compute the spanwise-averaged surface pressure.
            xy, p_avg = spanwise_average(xyz, p)

            if not initialized:
                p_mean = numpy.zeros_like(p_avg)
                initialized = True
            p_mean += p_avg

        p_mean /= times.size

        # Compute surface pressure coefficient.
        cp = pressure_coefficient(p_mean)

        self.x, self.y = xy
        self.values = cp


@dataclass
class UxCenterlineData:
    """Data and metadata for the centerline wake x-velocity profile."""

    label: str
    simudir: pathlib.Path = None
    x: numpy.ndarray = None
    values: numpy.ndarray = None
    plt_kwargs: dict = None

    def save(self, filename):
        """Save data to file."""
        datadir = self.simudir / 'data'
        datadir.mkdir(parents=True, exist_ok=True)
        filepath = datadir / filename
        with open(filepath, 'w') as outfile:
            numpy.savetxt(
                outfile, numpy.c_[self.x, self.values],
                comments='Centerline wake profile of mean x-velocity (x, u)'
            )

    def load(self, filename):
        """Load data from file."""
        datadir = self.simudir / 'data'
        filepath = datadir / filename
        with open(filepath, 'r') as infile:
            self.x, self.values = numpy.loadtxt(infile, unpack=True)

    def compute(self, time_limits=None, stride=1,
                xlims=(0.5, 10.0), zlims=(-1.6, 1.6), nx=200, nz=100):
        """Compute time-averaged spanwise-average x-velocity at centerline."""
        datadir = (self.simudir / 'output' / 'LES' / 'postProcessing' /
                   'surfaceProfiles')

        times = get_saved_times(datadir, limits=time_limits, stride=stride)

        X, Z = create_regular_grid_2d(xlims, zlims, nx, nz)

        # Compute the time-averaged centerline x-velocity.
        initialized = False
        for time in times:
            filepath = datadir / time_to_str(time) / 'U_yNormal_x0.0.raw'
            with open(filepath, 'r') as infile:
                x, z, ux = numpy.loadtxt(infile, usecols=(0, 2, 3),
                                         unpack=True)
            x, z, ux = apply_spatial_mask_2d(x, z, ux, xlims, zlims)
            if not initialized:
                ux_avg = numpy.zeros_like(ux)
                initialized = True
            ux_avg += ux
        ux_avg /= times.size

        # Interpolate data on regular grid.
        ux_avg = interpolate.griddata((x, z), ux_avg, (X, Z), method='linear')

        # Average along spanwise axis.
        ux_avg = numpy.mean(ux_avg, axis=0)

        self.x = X[0]
        self.values = ux_avg


@dataclass
class VerticalVelocityProfilesData:
    """Data and metadata for the vertical velocity profiles."""

    xlocs = [1.06, 1.54, 2.02, 4.0, 7.0, 10.0]  # locations along x-axis

    label: str
    simudir: pathlib.Path = None
    y: numpy.ndarray = None
    values: dict = None
    plt_kwargs: dict = None

    def save(self, filename):
        """Save data to file."""
        data = numpy.empty((1 + len(self.values), self.y.size))
        data[0] = self.y
        data[1:] = [self.values[xloc] for xloc in self.xlocs]
        datadir = self.simudir / 'data'
        datadir.mkdir(parents=True, exist_ok=True)
        filepath = datadir / filename
        with open(filepath, 'w') as outfile:
            numpy.savetxt(
                outfile, data.T,
                comments=('Vertical line profile of the mean velocity '
                          f'at x = {", ".join([str(v) for v in self.xlocs])}')
            )

    def load(self, filename):
        """Load data from file."""
        datadir = self.simudir / 'data'
        filepath = datadir / filename
        with open(filepath, 'r') as infile:
            data = numpy.loadtxt(infile, unpack=True)
        self.y = data[0]
        self.values = {k: data[i] for i, k in enumerate(self.xlocs, start=1)}

    def compute(self, dir, time_limits=None, stride=1, verbose=False):
        """Compute time-averaged spanwise-average x-velocity at centerline."""
        if dir not in ('x', 'y'):
            raise ValueError("dir must be either 'x' or 'y'")

        datadir = (self.simudir / 'output' / 'LES' / 'postProcessing' /
                   'surfaceProfiles')

        times = get_saved_times(datadir, limits=time_limits, stride=stride)

        ylims, zlims = (-3.0, 3.0), (-1.6, 1.6)
        ny, nz = 200, 100
        Y, Z = create_regular_grid_2d(ylims, zlims, ny, nz)
        self.y = Y[0]

        self.values = dict()
        for xloc in self.xlocs:
            if verbose:
                print(f'Computing average velocity profiles at x={xloc} ...')
            # Compute the time-averaged x and y velocity components.
            initialized = False
            for time in times:
                filepath = (datadir / time_to_str(time) /
                            f'U_xNormal_x{xloc:.2f}.raw')
                with open(filepath, 'r') as infile:
                    dir_to_index = {'x': 3, 'y': 4}
                    y0, z0, v = numpy.loadtxt(
                        infile, unpack=True, usecols=(1, 2, dir_to_index[dir])
                    )
                y, z, v = apply_spatial_mask_2d(y0, z0, v, ylims, zlims)
                if not initialized:
                    v_avg = numpy.zeros_like(v)
                    initialized = True
                v_avg += v
            v_avg /= times.size

            # Interpolate data on 2D regular grid.
            v_avg = interpolate.griddata((y, z), v_avg, (Y, Z),
                                         method='linear')

            # Average data along spanwise axis.
            v_avg = numpy.mean(v_avg, axis=0)

            self.values[xloc] = v_avg
