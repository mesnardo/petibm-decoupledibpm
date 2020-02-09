# Decoupled Immersed Boundary Projection Method with PetIBM

[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://github.com/mesnardo/petibm-decoupledibpm/raw/master/LICENSE)
[![Docker Hub](https://img.shields.io/badge/hosted-docker--hub-informational.svg)](https://cloud.docker.com/u/mesnardo/repository/docker/mesnardo/petibm-decoupledibpm)
[![Singularity Hub](https://www.singularity-hub.org/static/img/hosted-singularity--hub-%23e32929.svg)](https://singularity-hub.org/collections/3171)

## Flow over a stationary circular cylinder ($Re=40$ and $100$)

![cylinderRe40_vorticity](runs/cylinder2dRe40/189_markers/figures/wz_0005000.png)
**Figure:** Vorticity contours around the cylinder at Reynolds number $40$. (Contour levels between $-3D/U_\infty$ and $3D/U_\infty$ with increments of $0.4$.)

![cylinderRe100_vorticity](runs/cylinder2dRe100/189_markers/figures/wz_0020000.png)
**Figure:** Vorticity contours around the cylinder at Reynolds number $100$ after $200$ time units of flow simulation. (Contour levels between $-3D/U_\infty$ and $3D/U_\infty$ with increments of $0.4$.)

![cylinderRe40_pressure_coefficient](runs/cylinder2dRe40/189_markers/figures/cp_0005000.png)
**Figure:** Pressure coefficient along the upper and lower surfaces of the cylinder at Reynolds number $40$. We compare with the results from Li et al. (2016).

![cylinderRe100_pressure_coefficient](runs/cylinder2dRe100/189_markers/figures/pressure_coefficient.png)
**Figure:** Pressure coefficient along the upper and lower surfaces of the cylinder at Reynolds number $100$. We compare with the results from Li et al. (2016).

## Flow around an inline oscillating circular cylinder ($Re=100$)

![oscillatingcylinderRe100_vorticity](runs/oscillatingcylinderRe100/algo1/figures/vorticity.png)
**Figure:** Contours of the vorticity field around an inline oscillating cylinder at different phase angles ($\phi = 2 \pi f t$): $\phi = 0^o$ (left) and $\phi = 288^o$ (right). (Contour levels between $-20 U_m / D$ and $20 U_m / D$ using $30$ increments.)

![oscillatingcylinderRe100_pressure](runs/oscillatingcylinderRe100/algo1/figures/pressure.png)
**Figure:** Contours of the pressure field around an inline oscillating cylinder at different phase angles ($\phi = 2 \pi f t$): $\phi = 0^o$ (left) and $\phi = 288^o$ (right). (Contour levels between $-1 \rho U_m^2$ and $1 \rho U_m^2$ using $50$ increments.)

![oscillatingcylinderRe100_velocity](runs/oscillatingcylinderRe100/algo1/figures/velocity_profiles.png)
**Figure:** Profile of the velocity components ($u$: left, $v$: right) at four locations along the centerline for various phase angles $\phi$.

![oscillatingcylinderRe100_drag_coefficient](runs/oscillatingcylinderRe100/figures/drag_coefficient.png)
**Figure:** History of the drag coefficient of the inline oscillating cylinder obtained using different algorithms. We also show zooms at early and developed stages.

![oscillatingcylinderRe100_drag_coefficient_dt](runs/oscillatingcylinderRe100/figures/drag_coefficient_dt.png)
![oscillatingcylinderRe100_drag_coefficient_dx](runs/oscillatingcylinderRe100/figures/drag_coefficient_dx.png)
**Figure:** History of the drag coefficient obtained with Algorithm 1 for different time-step sizes and different grid sizes.

![oscillatingcylinderRe100_temporal_error](runs/oscillatingcylinderRe100/figures/temporal_error.png)
**Figure:** Variations of the $L_\infty$ and $L_2$ norm errors of the streamwise velocity as a function of the computational time-step size.

![oscillatingcylinderRe100_temporal_error](runs/oscillatingcylinderRe100/figures/spatial_error.png)
**Figure:** Variations of the $L_\infty$ and $L_2$ norm errors of the streamwise velocity as a function of the computational grid spacing.

![oscillatingcylinderRe100_cd_lag](runs/oscillatingcylinderRe100/figures/drag_coefficient_lag.png)
**Figure:** History of the drag coefficient using Algorithm 3 with force-prediction scheme 3. We compared the history obtained with different Lagrangian mesh resolutions: $N_b = 500$ Lagrangian markers on the boundary and $N_b = 202$ markers (the latter one corresponding to the same resolution as the Eulerian background grid).

## Flow around an impulsively started circular cylinder (Re=40)

![translatingcylinder2dRe40_cd](runs/translatingcylinder2dRe40/figures/drag_coefficients.png)
**Figure:** History of the drag coefficient of the impulsively started cylinder. Comparison with the analytical solution of Bar-Lev & Yang (1997) and the numerical results from Taira & Colonius (2007).

![translatingcylinder2dRe40_wz](runs/translatingcylinder2dRe40/dt=0.0005/figures/vorticity.png)
**Figure:** Vorticity contours around the impulsively started circular cylinder at $t=1.0$ (left) and $t=3.5$ (right). Contour levels between $-3 \omega_z D / U_o$ and $3 \omega_z D / U_o$ with increments of $0.4$.

![translatingcylinder2dRe40_lw](runs/translatingcylinder2dRe40/figures/recirculation_lengths.png)
**Figure:** History of the recirculation length measured in the reference frame of the impulsively start cylinder at Reynolds number 40 and for different time-step sizes.

## Three-dimensional flow around an inline oscillating sphere ($Re=78.54$)

![sphere_pressure](runs/oscillatingsphere/figures/pressure.png)
**Figure:** Contours of the pressure field in the $x$/$y$ at $z=0$ at three phase angles. Contour levels between $-2 p / \rho U_m^2$ and $2 p / \rho U_m^2$ with $30$ increments.
