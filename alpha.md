# Figures and Tables

## Introduction

![fig_snake_sections](data/figures/modified_sections_aoa35.png)
**Figure:** Original (left) and modified cross sections of the snake during its gliding phase. In addition to the original geometry, we also looked at geometries missing one or two lips.

|  |  |
|:-:|:-:|
| ![fig_snake_meshgrid](./runs/snake3d/both_lips/2k35/figures/pyvista_2d_meshgrid.png) | ![fig_snake_meshgrid_zoom](./runs/snake3d/both_lips/2k35/figures/pyvista_2d_meshgrid_zoom.png) |

**Figure:** Front views of the typical mesh used to compute the flow around a snake cylinder. We show the mesh around a snake cylinder with both lips at $AoA=35^o$. (a) is a view of the near-body wake region; (b) is a zoom near the surface of the cylinder.

## LES of the flow over a circular cylinder at Re=3900

![fig_cylinder_force_coefficients_wale](./runs/cylinder3dre3900/wale/figures/force_coefficients.png)
**Figure:** History of the drag and lift coefficients for a circular cylinder at $Re=3900$. We compare the curves obtained with the base grid and the coarser grid.

![fig_cylinder_cp_wale](./runs/cylinder3dre3900/wale/figures/surface_pressure_coefficient.png)
**Figure:** Mean pressure coefficient on the surface of the circular cylinder at $Re=3900$. The surface pressure is averaged along the spanwise direction and in time (between $100$ and $150$ non-dimensional time units of flow simulation).

![fig_cylinder_u_centerline_wale](./runs/cylinder3dre3900/wale/figures/u_centerline_profile.png)
**Figure:** Mean streamwise velocity along the centerline at $y/D=0$ behind a circular cylinder at $Re=3900$. The velocity profile is averaged along the spanwise direction and over time between $50$ and $150$ time units.

![fig_cylinder_u_profiles_wale](./runs/cylinder3dre3900/wale/figures/u_profiles.png)
![fig_cylinder_v_profiles_wale](./runs/cylinder3dre3900/wale/figures/v_profiles.png)
**Figure:** Mean velocity profiles along the crossflow direction at several locations along the streamwise direction behind a circular cylinder at Re = 3900. Profiles are reported at $x/D = 1.06$, $1.54$, $2.02$, $4.0$, $7.0$, $10.0$. The velocity components are averaged along the spanwise direction and over time (between $50$ and $150$ non-dimensional time units of flow simulation).

![fig_cylinder_qcrit](./runs/cylinder3dre3900/wale/fine/figures/pyvista_3d_contours_qcrit_150.png)
**Figure:** Isosurfaces of the second invariant of the velocity gradient tensor $Q=0.2$ at an instant in time in the near-body wake region. The isosurfaces are colored with the streamwise vorticity $\omega_x$ values.

![fig_cylinder_wz](./runs/cylinder3dre3900/wale/fine/figures/pyvista_2d_contours_wz_135.png)
**Figure:** Snapshot of the spanwise vorticity field $\omega_x$ in the near-body wake of a circular cylinder at $Re = 3900$. The snapshot is taken at mid-spanwise after $135$ non-dimensional time units of flow simulation

![fig_cylinder_ux_plane](./runs/cylinder3dre3900/wale/fine/figures/pyvista_2d_contours_ux_115.png)
![fig_cylinder_uy_plane](./runs/cylinder3dre3900/wale/fine/figures/pyvista_2d_contours_uy_125.png)
**Figure:** Filled contour of the streamwise velocity $u_x$ and crossflow velocity $u_y$ in the $x/z$ plane at $y/D = 0$ behind a circular cylinder at $Re = 3900$. The gray area shows a projection of the circular cylinder in the $x/z$ plane.

## Results

### Mean force coefficients

![fig_snake_mean_force_coefficients](./runs/snake3d/figures/mean_force_coefficients.png)
**Figure:** Mean lift (top) and drag (bottom) coefficients at Reynolds numbers $1000$, $2000$, and $3000$ versus the angle of attack of a snake cross-section with both lips, only the front lip or the back lip, and no lips. All values are averaged along the spanwise direction and in time (between $100$ and $200$ non-dimensional time units of flow simulation).

![fig_snake_lift_to_drag_ratio](./runs/snake3d/figures/mean_lift_drag_ratio.png)
**Figure:** Mean lift-to-drag ratios at Reynolds numbers $1000$, $2000$, and $3000$ versus the angle of attack of a snake cross-section with both lips, only the front lip or the back lip, and no lips. All values are averaged along the spanwise direction and in time (between $100$ and $200$ non-dimensional time units of flow simulation).

![fig_snake_strouhal_number](./runs/snake3d/figures/mean_strouhal.png)
**Figure:** Mean Strouhal number at Reynolds numbers $1000$, $2000$, and $3000$ versus the angle of attack of a snake cross-section with both lips, only the front lip or the back lip, and no lips. The Strouhal number is computed from the lift curve and averaged in time (between $100$ and $200$ non-dimensional time units of flow simulation).

### $Re=2000$ and $AoA=35^o$

![fig_snake_cp_2k35](./runs/snake3d/figures/surface_pressure_coefficient_2k35.png)
**Figure:** Mean surface pressure coefficient on the cylinder for all four cross-sections at $Re=2000$ and $AoA=35^o$. The surface pressure is averaged along the spanwise direction and in time (between $100$ and $200$ non-dimensional time units of flow simulation).

![fig_snake_u_centerline_2k35](./runs/snake3d/figures/u_centerline_profile_2k35.png)
**Figure:** Mean streamwise velocity along the centerline at $y=0$ for the original and modified snake cross-sections at $Re=2000$ and $AoA=35^o$. The velocity profile is averaged along the spanwise direction and in time (between $100$ and $200$ non-dimensional time units of flow simulation).

![fig_snake_u_profiles_2k35](./runs/snake3d/figures/u_profiles_2k35.png)
**Figure:** Vertical profiles of the mean streamwise velocity deficit at several locations along the streamwise direction behind a cylinder, comparing the four cross-sections at $Re=2000$ and $AoA=35^o$. The streamwise velocity is averaged along the spanwise direction and in time (between $100$ and $200$ non-dimensional time units of flow simulation).

![fig_snake_qcrit_2k35_both](./runs/snake3d/both_lips/2k35/figures/pyvista_3d_contours_qcrit_120.png)
**Figure:** Isosurfaces $Q=0.1$ of the second invariant of the velocity gradient tensor ($Q$-criterion) at an instant in time in the near-body wake region. The isosurfaces are colored with the streamwise vorticity $\omega_x$ values.

|  |  |
|:-:|:-:|
| ![fig_snake_ux_plane_2k35_both](./runs/snake3d/both_lips/2k35/figures/pyvista_2d_contours_ux_110.png) | ![fig_snake_ux_plane_2k35_front](./runs/snake3d/front_lip/2k35/figures/pyvista_2d_contours_ux_150.png) |
| ![fig_snake_ux_plane_2k35_back](./runs/snake3d/back_lip/2k35/figures/pyvista_2d_contours_ux_155.png) | ![fig_snake_ux_plane_2k35_none](./runs/snake3d/no_lips/2k35/figures/pyvista_2d_contours_ux_130.png) |

**Figure:** Filled contour of the streamwise velocity $u_x$ in the $x/z$ plane at $y/c = 0$ behind snake cylinders at $Re=2000$ with $AoA=35^o$. The four lips configurations are represented: (a) both lips, (b) front lip, (c) back lip, and (d) no lips. The gray area shows a projection of the snake cylinder in the $x/z$ plane.

|  |  |
|:-:|:-:|
| ![fig_snake_uy_plane_2k35_both](./runs/snake3d/both_lips/2k35/figures/pyvista_2d_contours_uy_175.png) | ![fig_snake_uy_plane_2k35_front](./runs/snake3d/front_lip/2k35/figures/pyvista_2d_contours_uy_180.png) |
| ![fig_snake_uy_plane_2k35_back](./runs/snake3d/back_lip/2k35/figures/pyvista_2d_contours_uy_185.png) | ![fig_snake_uy_plane_2k35_none](./runs/snake3d/no_lips/2k35/figures/pyvista_2d_contours_uy_140.png) |

**Figure:** Filled contour of the crossflow velocity $u_y$ in the $x/z$ plane at $y/c = 0$ behind snake cylinders at $Re=2000$ with $AoA=35^o$. The four lips configurations are represented: (a) both lips, (b) front lip, (c) back lip, and (d) no lips. The gray area shows a projection of the snake cylinder in the $x/z$ plane.

|  |  |
|:-:|:-:|
| ![fig_snake_wz_2k35_both](./runs/snake3d/both_lips/2k35/figures/pyvista_2d_contours_wz_160.png) | ![fig_snake_wz_2k35_front](./runs/snake3d/front_lip/2k35/figures/pyvista_2d_contours_wz_180.png) |
| ![fig_snake_wz_2k35_back](./runs/snake3d/back_lip/2k35/figures/pyvista_2d_contours_wz_150.png) | ![fig_snake_wz_2k35_none](./runs/snake3d/no_lips/2k35/figures/pyvista_2d_contours_wz_195.png) |

**Figure:** Filled contour of the spanwise vorticity field $\omega_z$ in the $x/y$ plane at $z/c = 0$ behind snake cylinders at $Re=2000$ with $AoA=35^o$. The four lips configurations are represented: (a) both lips, (b) front lip, (c) back lip, and (d) no lips.

### $Re=2000$ and $AoA=25^o$

![fig_snake_cp_2k25](./runs/snake3d/figures/surface_pressure_coefficient_2k25.png)
**Figure:** Mean surface pressure coefficient on the cylinder for all four cross-sections at $Re=2000$ and $AoA=25^o$. The surface pressure is averaged along the spanwise direction and in time (between $100$ and $200$ non-dimensional time units of flow simulation).

![fig_snake_u_centerline_2k25](./runs/snake3d/figures/u_centerline_profile_2k25.png)
**Figure:** Mean streamwise velocity along the centerline at $y=0$ for the original and modified snake cross-sections at $Re=2000$ and $AoA=25^o$. The velocity profile is averaged along the spanwise direction and in time (between $100$ and $200$ non-dimensional time units of flow simulation).

![fig_snake_u_profiles_2k25](./runs/snake3d/figures/u_profiles_2k25.png)
**Figure:** Vertical profiles of the mean streamwise velocity deficit at several locations along the streamwise direction behind a cylinder, comparing the four cross-sections at $Re=2000$ and $AoA=25^o$. The streamwise velocity is averaged along the spanwise direction and in time (between $100$ and $200$ non-dimensional time units of flow simulation).

|  |  |
|:-:|:-:|
| ![fig_snake_wz_2k25_both](./runs/snake3d/both_lips/2k25/figures/pyvista_2d_contours_wz_125.png) | ![fig_snake_wz_2k25_back](./runs/snake3d/back_lip/2k25/figures/pyvista_2d_contours_wz_160.png) |
| ![fig_snake_wz_2k25_none](./runs/snake3d/no_lips/2k25/figures/pyvista_2d_contours_wz_180.png) |

**Figure:** Filled contour of the spanwise vorticity field $\omega_z$ in the $x/y$ plane at $z/c = 0$ behind snake cylinders at $Re=2000$ with $AoA=35^o$. The four lips configurations are represented: (a) both lips, (b) back lip, and (c) no lips.
