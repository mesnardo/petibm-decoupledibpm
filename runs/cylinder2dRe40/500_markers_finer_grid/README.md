# 2D flow over a stationary cylinder (Re=40, 500 Lagrangian markers, finer Eulerian grid)

## Pre-processing steps (optional)

Create the cylinder geometry:

```shell
python scripts/create_body.py
```

ASCII file with boundary coordinates (`cylinder.body`) is saved in the simulation directory.

Create the YAML file with the configuration of the Cartesian grid:

```shell
python scripts/create_mesh_yaml.py
```

YAML file with configuration of the Cartesian grid (`mesh.yaml`) is saved in the simulation directory.

## Run the PetIBM simulation

The variable `SIMG` represents the local path of the Singularity image for the PetIBM application.

```shell
export CUDA_VISIBLE_DEVICES=0
mpiexec -np 2 singularity exec --nv $simg petibm-lietal2016 -options_left -log_view ascii:view.log
```

The simulation completed 5,000 time steps in about 18 minutes using:

* 2 MPI processes (Intel(R) Core(TM) i7-3770 CPU @ 3.40GHz)
* 1 NVIDIA K40 GPU device

## Post-processing steps

Plot the history of the force coefficients:

```shell
python scripts/plot_force_coefficients.py
```

Figure is saved as a PNG file (`force_coefficients.png`) in the folder `figures` of the simulation directory.

<img src="figures/force_coefficients.png" width="400">

Compute the vorticity field:

```shell
singularity exec --nv $simg petibm-vorticity
```

Plot the vorticity field after 5,000 time steps:

```shell
python scripts/plot_vorticity.py
```

Figure is saved as a PNG file (`wz_0005000.png`) in the folder `figures` of the simulation directory.

<img src="figures/wz_0005000.png" width="400">

Plot the pressure coefficient along the surface of the cylinder:

```shell
python scripts/plot_pressure_coefficient.py
```

Figure is saved as a PNG file (`pressure_coefficient.png`) in the folder `figures` of the simulation directory.

<img src="figures/cp_0005000.png" width="400">
