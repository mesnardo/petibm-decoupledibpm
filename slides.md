name: first
class: center, middle

# Decoupled IBPM (Replication Study)

**Olivier Mesnard** (mesnardo@gwu.edu)

---

## PetIBM

.bigger[

* Open source, BSD 3-Clause, [GitHub](https://github.com/barbagroup/PetIBM)
* 2D/3D incompressible Navier-Stokes equations
* Projection method *a la* Perot (1993)
* Distributed-memory architectures (PETSc)
* Iterative solvers on distributed GPUs (AmgX, AmgXWrapper)
* Immersed Boundary Methods
  * IBPM (Taira and Colonius, 2007)
  * Decoupled IBPM (Li et al., 2016)

]

---

### Replication

.medium[

> *"Replicability is obtaining consistent results across studies aimed at answering the same scientific question, each of which has obtained its own data."*

]

NASEM, "Reproducibility and Replicability in Science" (doi: [10.17226/25303](https://doi.org/10.17226/25303))

![li_et_al_2016_header](./figures/li_et_al_2016_header.png)

---

### Decoupled IBPM

<br>

`
$$
\begin{cases}
    \frac{\partial \mathbf{u}}{\partial t} + \mathbf{u} \cdot \nabla \mathbf{u} = -\nabla p + \frac{1}{Re} \nabla^2 \mathbf{u} + \int_{s}{\mathbf{f} \left( \mathbf{\xi} \left( \mathit{s}, \mathit{t} \right) \right) \delta_h \left( \mathbf{\xi} - \mathbf{x} \right)} d\mathit{s} \\
    \nabla \cdot \mathbf{u} = 0 \\
    \mathbf{u} \left( \mathbf{\xi} \left( \mathit{s}, t \right) \right) = \int_{\mathbf{x}}{\mathbf{u} \left( \mathbf{x} \right)} \delta_h \left( \mathbf{x} - \mathbf{\xi} \right) d\mathbf{x} = \mathbf{u}_B
\end{cases}
$$
`

<br>
Full discretization (space and time) to form an algebraic system:

`
$$
\begin{bmatrix}
    A & G & -H \\
    D & 0 & 0 \\
    E & 0 & 0
\end{bmatrix}
\begin{pmatrix}
    u^{n+1} \\
    \delta p \\
    \delta f
\end{pmatrix}
=
\begin{pmatrix}
    r^n \\
    0 \\
    u_B^{n+1}
\end{pmatrix}
+
\begin{pmatrix}
    {bc}_1 \\
    {bc}_2 \\
    0
\end{pmatrix}
$$
`

---

### Decoupled IBPM

Set $\gamma \equiv \begin{pmatrix} u^{n+1} \\ \delta f \end{pmatrix}$

and rewrite the system:

`
$$
\begin{bmatrix}
    \bar{A} & \bar{G} \\
    \bar{D} & 0
\end{bmatrix}
\begin{pmatrix}
    \gamma \\
    \delta p
\end{pmatrix}
=
\begin{pmatrix}
    \bar{r}_1 \\
    \bar{r}_2
\end{pmatrix}
$$
`

where

`
$$
\bar{A} \equiv \begin{bmatrix} A & -H \\ E & 0 \end{bmatrix} ;\;
\bar{G} \equiv \begin{bmatrix} G \\ 0 \end{bmatrix} ;\;
\bar{D} \equiv \begin{bmatrix} D & 0 \end{bmatrix}
$$
`

and

`
$$
\bar{r}_1 \equiv \begin{pmatrix} r_n + {bc}_1 \\ u_B^{n+1} \end{pmatrix} ;\;
\bar{r}_2 \equiv {bc}_2
$$
`

---

### Decoupled IBPM

**Idea:** Apply two successive block-LU factorizations to decouple the unknowns.

<br>
First block-LU decomposition:

`
$$
\begin{bmatrix}
    \bar{A} & \bar{G} \\
    \bar{D} & 0
\end{bmatrix}
\begin{pmatrix}
    \gamma \\
    \delta p
\end{pmatrix}
=
\begin{pmatrix}
    \bar{r}_1 \\
    \bar{r}_2
\end{pmatrix}
$$
`

<br>

`
$$
\begin{bmatrix}
    \bar{A} & 0 \\
    \bar{D} & -\bar{D}\bar{A}^{-1}\bar{G}
\end{bmatrix}
\begin{bmatrix}
    I & \bar{A}^{-1}\bar{G} \\
    0 & I
\end{bmatrix}
\begin{pmatrix}
    \gamma \\
    \delta p
\end{pmatrix}
=
\begin{bmatrix}
    \bar{A} & 0 \\
    \bar{D} & -\bar{D}\bar{A}^{-1}\bar{G}
\end{bmatrix}
\begin{pmatrix}
    \gamma^* \\
    \delta p
\end{pmatrix}
=
\begin{pmatrix}
    \bar{r}_1 \\
    \bar{r}_2
\end{pmatrix}
$$
`

<br>
to get the sequence:

`
$$
\begin{aligned}
    & \bar{A} \gamma^* = \bar{r}_1 \\
    & \bar{D}\bar{A}^{-1}\bar{G} \delta p = \bar{D} \gamma^* - \bar{r}_2 \\
    & \gamma = \gamma^* - \bar{A}^{-1}\bar{G} \delta p
\end{aligned}
$$
`

---

### Decoupled IBPM

<br>
Second block-LU decomposition:

`
$$
\bar{A}
\begin{pmatrix}
    u^* \\
    \delta f
\end{pmatrix}
=
\begin{bmatrix}
    A & -H \\
    E & 0
\end{bmatrix}
\begin{pmatrix}
    u^* \\
    \delta f
\end{pmatrix}
=
\begin{pmatrix}
    r^n + {bc}_1 \\
    u_B^{n+1}
\end{pmatrix}
$$
`

<br>

`
$$
\begin{bmatrix}
    A & 0 \\
    E & EA^{-1}H
\end{bmatrix}
\begin{bmatrix}
    I & -A^{-1}H \\
    0 & I
\end{bmatrix}
\begin{pmatrix}
    u^* \\
    \delta f
\end{pmatrix}
=
\begin{bmatrix}
    A & 0 \\
    E & EA^{-1}H
\end{bmatrix}
\begin{pmatrix}
    u^{**} \\
    \delta f
\end{pmatrix}
=
\begin{pmatrix}
    r^n + {bc}_1 \\
    u_B^{n+1}
\end{pmatrix}
$$
`

<br>
to get the sequence:

`
$$
\begin{aligned}
    & A u^{**} = r^n + {bc}_1 \\
    & EA^{-1}H \delta f = u_B^{n+1} - E u^{**} \\
    & u^* = u^{**} + A^{-1}H \delta f
\end{aligned}
$$
`

---

### Decoupled IBPM

**Algo 1:**

`
$$
\begin{aligned}
    & A u^{**} = r^n + {bc}_1 \\
    & EA^{-1}H \delta f = u_B^{n+1} - E u^{**} \\
    & u^* = u^{**} + A^{-1}H \delta f \\
    & DA^{-1}G \delta p = D u^* - {bc}_2 \\
    & u^{n+1} = u^* - A^{-1}G \delta p
\end{aligned}
$$
`

<br>
Sequence of operations:

1. Solve system for intermediate velocity.
2. Enforce the no-slip condition at the immersed boundary.
3. Solve a pressure Poisson system.
4. Project the velocity onto divergence-free space.

$\Rightarrow$ Constraints are satisfied sequentially, not simultaneously.

---

### Variants

**Algo 2** (solve an additional system for the velocity):

`
$$
\begin{aligned}
    & A u^{**} = r^n + {bc}_1 \\
    & EA^{-1}H \delta f = u_B^{n+1} - E u^{**} \\
    & A u^* = A u^{**} + H \delta f \\
    & DA^{-1}G \delta p = D u^* - {bc}_2 \\
    & u^{n+1} = u^* - A^{-1}G \delta p
\end{aligned}
$$
`

<br>
**Algo 3** (group velocity and pressure together):

`
$$
\begin{aligned}
    & A u^{**} = r^n + {bc}_1 \\
    & DA^{-1}G \delta p = D u^{**} - {bc}_2 \\
    & u^* = u^{**} - A^{-1}G \delta p \\
    & EA^{-1}H \delta f = u_B^{n+1} - E u^* \\
    & u^{n+1} = u^* + A^{-1}H \delta f
\end{aligned}
$$
`

---

### Force prediction scheme

Explicit terms in the RHS of the velocity system:

`
$$
r^n = \frac{1}{\Delta t} u^n - G \tilde{p} + \frac{3}{2} N\left( u^n \right) - \frac{1}{2} N\left( u^{n-1} \right) + \frac{1}{2 Re} L\left( u^n \right) + H \tilde{f}
$$
`

Different schemes to predict the forces $\tilde{f}$:

* set $\tilde{f} = 0$ (scheme 1)
* set $\tilde{f} = f^n$ (scheme 2)
* solve $EA^{-1}H \tilde{f} = u_B^{n+1} - E u^n$ (scheme 3)
* solve $EA^{-1}H \tilde{f} = u_B^{n+1} - E \tilde{u}$ (scheme 4)
  * with $\frac{\tilde{u} - u^n}{\Delta t} + N u^n = -G \tilde{p} + \frac{1}{Re} L u^n + {bc}_1$

---

### Examples reported in Li et al. (2016)

.big[

* 2D flow over stationary cylinder ($Re=40$ and $100$)
* 2D flow around inline oscillating cylinder ($Re=100$)
* 2D flow around impulsively started cylinder ($Re=40$)
* Spatial and temporal convergence
* 3D flow around inline oscillating sphere
* 3D flow around a dragonfly in straight flight

]

---

### Differences

.big[

* Li et al. (2016) used delta function of Peskin (2002); $4$-point support.
  * With PetIBM, we use the function of Roma et al. (1999); $3$-point support.
* They used implicit Crank-Nicolson for both convective and viscous terms.
  * We do explicit Adams-Bashforth for the convective terms.
* They use a higher resolution for the Lagrangian mesh than for the Eulerian grid.
  * If we do that, we get noisy solutions (forces, near-boundary pressure).
* Hydrodynamic forces are computed by integrating the Eulerian momentum forcing.
  * We simply integrate the Lagrangian forces.

]

.medium[

What's missing in their article:

* Collocated/Staggered grid arrangement?
* Iterative solvers used and exit criteria?
* External libraries?
* Some details about the grid generation.
* The geometry for the dragonfly application.

]

---

### Reproducible workflow

![workflow](./figures/workflow.png)

.medium[

* Application code available on GitHub: [petibm-decoupledibpm](https://github.com/mesnardo/petibm-decoupledibpm) (BSD 3-Clause)
* Reproducible Replication study to be submitted to [ReScience](https://rescience.github.io)

]

---

### 2D flow over stationary cylinder

.center[

| $Re=40$ | $Re=100$ |
|:-:|:-:|
| <img src="runs/cylinder2dRe40/figures/vorticity.png" alt="cylinder2dRe40_vorticity" width="400"/> | <img src="runs/cylinder2dRe100/figures/vorticity.png" alt="cylinder2dRe100_vorticity" width="400"/> |

Vorticity contours around the cylinder.

]

---

### 2D flow over stationary cylinder

.center[

| $Re=40$ | $Re=100$ |
|:-:|:-:|
| <img src="runs/cylinder2dRe40/figures/pressure_coefficient.png" alt="cylinder2dRe40_cp" width="400"/> | <img src="runs/cylinder2dRe100/figures/pressure_coefficient.png" alt="cylinder2dRe100_cp" width="400"/> |

Pressure coefficient along the cylinder surface.

]

---

### Li et al. (2016)

.medium[

> "The pressure coefficient (`$C_p = (p - p_\infty) / 0.5 \rho U_\infty^2$`) along the cylinder surface is plotted in Fig. 3, which was usually not provided for the continuous approach in literature, since the pressure jump across the IB is smeared by the regularized delta function. Since the 4-point regularized delta function (Peskin, 2002) is adopted in the present study, here we first interpolate the pressure along a circle, which locates at three times of the Eulerian grid spacings away from the cylinder surface and is outside of the support region of the regularized delta function. Then it is used as the pressure on the cylinder surface by assuming zero pressure gradient in the wall-normal direction."

]

---

### 2D flow over stationary cylinder (Re=40)

.center[

<img src="runs/lagrangian-resolution/cylinder2dRe40/figures/pressure_coefficient_all.png" alt="cylinder2dRe40_cp_lag" width="700">

]

---

### 2D flow over stationary cylinder (Re=40, pressure)

.center[

<img src="runs/lagrangian-resolution/cylinder2dRe40/figures/pressure_all.png" alt="cylinder2dRe40_pressure_lag" width="550">

]

---

### 2D flow over stationary cylinder (Re=40, pressure)

.center[

<img src="runs/lagrangian-resolution/cylinder2dRe40/figures/pressure_all_zoom.png" alt="cylinder2dRe40_pressure_lag_zoom" width="550">

]

---

### 2D flow over stationary cylinder (Re=40, x-velocity)

.center[

<img src="runs/lagrangian-resolution/cylinder2dRe40/figures/ux_all.png" alt="cylinder2dRe40_ux_lag" width="550">

]

---

### 2D flow over stationary cylinder (Re=40, y-velocity)

.center[

<img src="runs/lagrangian-resolution/cylinder2dRe40/figures/uy_all.png" alt="cylinder2dRe40_uy_lag" width="550">

]

---

### 2D flow over stationary cylinder (Re=100)

.center[

<img src="runs/lagrangian-resolution/cylinder2dRe100/figures/pressure_coefficient_all.png" alt="cylinder2dRe100_cp_lag" width="700">

]

---

### 2D flow around inline oscillating cylinder

.center[

<img src="runs/oscillatingcylinderRe100/algo1/figures/vorticity.png" alt="oscillatingcylinder_vorticity" width="550"/>
<img src="runs/oscillatingcylinderRe100/algo1/figures/pressure.png" alt="oscillatingcylinder_pressure" width="550"/>

Contours of the vorticity (top) and pressure (bottom) at $Re=100$.

]

---

### 2D flow around inline oscillating cylinder

.center[

<img src="runs/oscillatingcylinderRe100/algo1/figures/velocity_profiles.png" alt="oscillatingcylinder_velocity" width="500"/>

Velocity profiles at different $x$ locations and phase angles.

]

---

### 2D flow around inline oscillating cylinder

.center[

<img src="runs/oscillatingcylinderRe100/figures/drag_coefficient.png" alt="oscillatingcylinder_cd" width="600"/>

History of the drag coefficient with Algos 1, 2, and 3, and with scheme 3.

]

---

### 2D flow around inline oscillating cylinder

.center[

<table><tr>
<td> <img src="runs/oscillatingcylinderRe100/figures/drag_coefficient_dt.png" alt="oscillatingcylinder_cd_dt", width="400"> </td>
<td> <img src="runs/oscillatingcylinderRe100/figures/drag_coefficient_dx.png" alt="oscillatingcylinder_cd_dx", width="400"> </td>
</table></tr>

History of the drag coefficient for different values of $\Delta t$ (left) and $\Delta x$ (right), with Algo 1 and scheme 3.

]

---

### 2D flow around inline oscillating cylinder

.center[

<img src="runs/oscillatingcylinderRe100/figures/drag_coefficient_algo1_delta.png" alt="oscillatingcylinder_cd_delta", width="800">

History of the drag coefficient with Algo 1 (scheme 3), using two different regularized delta functions.

]

---

### 2D flow around inline oscillating cylinder

.center[

<img src="runs/oscillatingcylinderRe100/figures/drag_coefficient_lag.png" alt="oscillatingcylinder_cd_lag", width="800">

History of the drag coefficient obtained with two different Lagrangian mesh resolutions.

]

---

### 2D flow around inline oscillating cylinder

.center[

<img src="runs/oscillatingcylinderRe100/figures/drag_coefficient_lag_dt.png" alt="oscillatingcylinder_cd_lag_dt", width="800">

History of the drag coefficient obtained with two different Lagrangian mesh resolutions.

]

---

### Taira and Colonius (2007)

.medium[

> "Some care must be taken to make $Q^T B^N Q$ positive-definite and well-conditioned. First, as in the traditional factional step method, one of the discrete pressure values must be pinned to a certain value to remove the zero eigenvalue. Second, no repeating Lagrangian points are allowed to avoid $Q^T B^N Q$ from becoming singular. Also to achieve a reasonable condition number and to prevent penetration of streamlines caused by a lack of Lagrangian points, the distance between adjacent Lagrangian points, $\Delta s$, is set approximately to the Cartesian grid spacing."

]

---

### Krishnan (2015, PhD)

.medium[

> "In immersed boundary methods where the discrete delta function is used to transfer values between the body and the fluid mesh, we do not require information about the connectivity between the boundary nodes. The body force is spread near the boundary nodes to grid points that are within the support of the delta function. What this means is that if the boundary nodes are sufficiently separated from each other, the fluid can leak through the immersed boundary. At the same time, placing boundary points too close to each other can also cause problems, as the width of the delta function is a fixed size. Taira and Colonius (2007) observed that the condition number of their pressure-force linear system worsened as the distance between points decreased, and recommended using a spacing approximately equal to the cell width of the underlying grid near the boundary."

]

---

### Krishnan (2015, PhD)

.medium[

> "Uhlmann (2005) tried an alternative approach to solve the problem of spurious force oscillations. He decided to use the discrete delta function for interpolation and spreading, in the context of the direct forcing method. The body was represented using Lagrangian markers, but the forces at the boundary points were calculated directly, without the use of any constitutive relations."

> "The method by Uhlmann still caused mild oscillations in the forces, which could be further reduced by choosing the discrete delta function carefully. Yang et al. (2009) investigated this and concluded that smoothed delta functions whose derivatives also satisfy higher-order moment conditions produce fewer spurious forces in flows with moving geometries."

> "Yang and Balaras (2006) also noted that such problems are minimal for earlier immersed boundary methods that used the discrete delta function for interpolation because of the smooth transition between the solid and the fluid."

]

---

### 2D flow around impulsively started cylinder

.center[

<img src="runs/translatingcylinder2dRe40/dt=0.0005/figures/vorticity.png" alt="translatingcylinder_vorticity", width="450">
<img src="runs/translatingcylinder2dRe40/figures/drag_coefficient.png" alt="oscillatingcylinder_cd_dt", width="350">

Vorticity contours (top) around cylinder at $Re=40$ and history of drag coefficient (bottom).

]

---

### 3D flow around inline oscillating cylinder

.center[

<img src="runs/oscillatingsphere/figures/pressure.png" alt="oscillatingsphere_pressure" width="800">

Contours of the pressure around a sphere ($Re=78.54$) in the $x$/$y$ plane at $z=0$ for different phase angles.

]

---

### Dragonfly in straight flight

.center[

<img src="figures/dragonfly_geometry.png" alt="dragonfly_geometry" width=600>

Model of a dragonfly in straight flight. (Figure from Li et al., 2016.)

]

---

### Dragonfly in straight flight

.center[

<img src="figures/dragonfly_vorticity.png" alt="dragonfly_vorticity" width=700>

Instantaneous vortex structures at four instants. (Figure from Li et al., 2016.)

]

---

### Next

.big[

* Resolve problem with Eulerian/Lagrangian mesh resolution.
* Post-process oscillating sphere simulation (pressure drag coefficient).
* Run dragonfly simulation.
* Write manuscript for ReScience.

]
