"""Assistant module with data processing classes."""

import pathlib
from dataclasses import dataclass

import numpy
from scipy import interpolate

from .forces import force_coefficients, load_forces
from .misc import get_stats, get_strouhal
from .transforms import (apply_spatial_mask_2d, create_regular_grid_2d,
                         sort_sections, spanwise_average)
from .velocity import load_Ux_yNormal, load_Uxy_xNormal
from .wallpressure import load_wall_pressure, wall_pressure_coefficient


@dataclass
class ForceCoefficientsData:
    """Data and metadata for the force coefficients."""

    label: str
    simudir: pathlib.Path = None
    times: numpy.ndarray = None
    values: tuple = None
    plt_kwargs: dict = None

    @property
    def raw_datadir(self):
        return (self.simudir / 'output' / 'LES' / 'postProcessing' /
                'forces' / '0')

    @property
    def datadir(self):
        return self.simudir / 'data'

    @property
    def tarball(self):
        return self.simudir / 'output' / 'LES' / 'postProcessing.tar.gz'

    def save(self, filename):
        """Save data to file."""
        data = numpy.empty((1 + len(self.values), self.times.size))
        data[0] = self.times
        data[1:] = self.values
        self.datadir.mkdir(parents=True, exist_ok=True)
        filepath = self.datadir / filename
        with open(filepath, 'w') as outfile:
            numpy.savetxt(outfile, data.T, header='Force coefficients')

    def load(self, filename):
        """Load data from file."""
        filepath = self.simudir / 'data' / filename
        with open(filepath, 'r') as infile:
            self.times, *self.values = numpy.loadtxt(infile, unpack=True)

    def load_raw(self, from_tarball=False):
        kwargs = dict(filepath=self.raw_datadir / 'forces.dat')
        if from_tarball:
            kwargs = dict(tarball=self.tarball,
                          name='postProcessing/forces/0/forces.dat')

        return load_forces(**kwargs)

    def compute(self, from_tarball=False, Lz=numpy.pi):
        """Load and compute the force coefficients."""
        self.times, *self.values = self.load_raw(from_tarball=from_tarball)

        self.values = force_coefficients(self.values, Lz=Lz)

    def get_stats(self, time_limits=None, verbose=False):
        """Compute and return statistics."""
        kwargs = dict(limits=time_limits, verbose=verbose)
        cd, cl, cz = self.values
        cd_stats = get_stats(self.times, cd, **kwargs)
        cl_stats = get_stats(self.times, cl, **kwargs)
        cz_stats = get_stats(self.times, cz, **kwargs)
        return cd_stats, cl_stats, cz_stats

    def get_strouhal(self, L=1.0, U=1.0, time_limits=None, order=1):
        """Compute Strouhal number from the lift-coefficient curve."""
        t = self.times
        cl = self.values[1]
        return get_strouhal(t, cl, L=L, U=U, limits=time_limits, order=order)


@dataclass
class SurfacePressureData:
    """Data and metadata for the surface pressure coefficient."""

    label: str
    simudir: pathlib.Path = None
    x: numpy.ndarray = None
    y: numpy.ndarray = None
    values: numpy.ndarray = None
    plt_kwargs: dict = None

    @property
    def raw_datadir(self):
        return (self.simudir / 'output' / 'LES' / 'postProcessing' / 
                'wallPressure')

    @property
    def datadir(self):
        return self.simudir / 'data'

    @property
    def tarball(self):
        return self.simudir / 'output' / 'LES' / 'postProcessing.tar.gz'

    def save(self, filename):
        """Save processed data to file."""
        self.datadir.mkdir(parents=True, exist_ok=True)
        filepath = self.datadir / filename
        with open(filepath, 'w') as outfile:
            numpy.savetxt(outfile, numpy.c_[self.x, self.y, self.values],
                          header='Surface pressure coefficient (x, y, cp)')

    def load(self, filename):
        """Load processed data from file."""
        filepath = self.datadir / filename
        with open(filepath, 'r') as infile:
            self.x, self.y, self.values = numpy.loadtxt(infile, unpack=True)

    def load_raw(self, times, from_tarball=False):
        kwargs = dict(datadir=self.raw_datadir)
        if from_tarball:
            kwargs = dict(tarball=self.tarball)

        return load_wall_pressure(times, **kwargs)

    def compute(self, times, from_tarball=False):
        """Compute the time-averaged spanwise-averaged surface pressure."""
        # Load instantaneous wall pressure and compute time averaged.
        xyz, p = self.load_raw(times, from_tarball=from_tarball)

        # Sort coordinates and values along the spanwise axis and
        # per cross-section.
        xyz, p = sort_sections(xyz, p)

        # Compute the spanwise average wall pressure.
        xy, p = spanwise_average(xyz, p)

        # Switch to wall pressure coefficient.
        cp = wall_pressure_coefficient(p)

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

    @property
    def raw_datadir(self):
        return (self.simudir / 'output' / 'LES' / 'postProcessing' /
                'surfaceProfiles')

    @property
    def datadir(self):
        return self.simudir / 'data'

    @property
    def tarball(self):
        return self.simudir / 'output' / 'LES' / 'postProcessing.tar.gz'

    def save(self, filename):
        """Save data to file."""
        self.datadir.mkdir(parents=True, exist_ok=True)
        filepath = self.datadir / filename
        with open(filepath, 'w') as outfile:
            numpy.savetxt(
                outfile, numpy.c_[self.x, self.values],
                header='Centerline wake profile of mean x-velocity (x, u)'
            )

    def load(self, filename):
        """Load data from file."""
        filepath = self.datadir / filename
        with open(filepath, 'r') as infile:
            self.x, self.values = numpy.loadtxt(infile, unpack=True)

    def load_raw(self, times, from_tarball=False):
        kwargs = dict(datadir=self.raw_datadir)
        if from_tarball:
            kwargs = dict(tarball=self.tarball)

        return load_Ux_yNormal(times, **kwargs)

    def compute(self, times, from_tarball=False):
        """Compute time-averaged spanwise-average x-velocity at centerline."""
        xz, ux = self.load_raw(times, from_tarball=from_tarball)

        nx, nz = 200, 100
        xlims, zlims = (0.0, 10.0), (-1.6, 1.6)

        xz, ux = apply_spatial_mask_2d(xz, ux, (xlims, zlims))

        XZ = create_regular_grid_2d(xlims, zlims, nx, nz)

        # Interpolate data on regular grid.
        ux = interpolate.griddata(xz, ux, XZ, method='linear')

        # Average along spanwise axis (ignoring NaNs).
        ux = numpy.nanmean(ux, axis=0)

        self.x = XZ[0][0]
        self.values = ux


@dataclass
class VerticalVelocityProfilesData:
    """Data and metadata for the vertical velocity profiles."""

    xlocs = [1.06, 1.54, 2.02, 4.0, 7.0, 10.0]  # locations along x-axis

    label: str
    simudir: pathlib.Path = None
    y: numpy.ndarray = None
    values: dict = None
    plt_kwargs: dict = None

    @property
    def raw_datadir(self):
        return (self.simudir / 'output' / 'LES' / 'postProcessing' /
                'surfaceProfiles')

    @property
    def datadir(self):
        return self.simudir / 'data'

    @property
    def tarball(self):
        return self.simudir / 'output' / 'LES' / 'postProcessing.tar.gz'

    def save(self, filename):
        """Save data to file."""
        data = numpy.empty((1 + 2 * len(self.values), self.y.size))
        data[0] = self.y
        for i, xloc in enumerate(self.xlocs):
            data[2 * i + 1] = self.values[xloc]['ux']
            data[2 * i + 2] = self.values[xloc]['uy']

        self.datadir.mkdir(parents=True, exist_ok=True)
        filepath = self.datadir / filename
        with open(filepath, 'w') as outfile:
            numpy.savetxt(
                outfile, data.T,
                header=('Vertical line profile of the mean velocity '
                        f'at x = {", ".join([str(v) for v in self.xlocs])}')
            )

    def load(self, filename):
        """Load data from file."""
        filepath = self.datadir / filename
        with open(filepath, 'r') as infile:
            data = numpy.loadtxt(infile, unpack=True)
        self.y = data[0]
        self.values = dict()
        for i, xloc in enumerate(self.xlocs):
            self.values[xloc] = dict(ux=data[2 * i + 1], uy=data[2 * i + 2])

    def load_raw(self, xlocs, times, from_tarball=False):
        kwargs = dict(datadir=self.raw_datadir)
        if from_tarball:
            kwargs = dict(tarball=self.tarball)

        return load_Uxy_xNormal(xlocs, times, **kwargs)

    def compute(self, times, from_tarball=False):
        profiles = self.load_raw(self.xlocs, times, from_tarball=from_tarball)

        ny, nz = 200, 100
        ylims, zlims = (-3.0, 3.0), (-1.6, 1.6)
        YZ = create_regular_grid_2d(ylims, zlims, ny, nz)

        for xloc in self.xlocs:
            # Interpolate data on a 2D regular grid.
            yz = profiles[xloc]['yz']
            ux = interpolate.griddata(
                yz, profiles[xloc]['ux'], YZ, method='linear'
            )
            uy = interpolate.griddata(
                yz, profiles[xloc]['uy'], YZ, method='linear'
            )
            # Average data along spanwise axis (ignoring NaNs).
            profiles[xloc] = dict(ux=numpy.nanmean(ux, axis=0),
                                  uy=numpy.nanmean(uy, axis=0))

        self.y = YZ[0][0]
        self.values = profiles
