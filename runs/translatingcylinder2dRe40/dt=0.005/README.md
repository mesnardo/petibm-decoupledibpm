# 2D impulsively started cylinder (Re=40, 158 Lagrangian markers, Dt=0.005)

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

## Run PetIBM simulation

The variable `SIMG` represents the local path of the Singularity image for the PetIBM application.

```shell
export CUDA_VISIBLE_DEVICES=0
mpiexec -np 2 singularity exec --nv $simg petibm-lietal2016 -solver translating_cylinder -options_left -log_view ascii:view.log
```

The simulation completed 700 time steps in less than 5 minutes using:

* 2 MPI processes (Intel(R) Core(TM) i7-3770 CPU @ 3.40GHz)
* 1 NVIDIA K40 GPU device

## Post-processing steps

Plot the history of the drag coefficient:

```shell
python scripts/plot_drag_coefficient.py
```

Figure is saved as a PNG file (`drag_coefficient.png`) in the folder `figures` of the simulation directory.

<img src="figures/drag_coefficient.png" width="600">

Compute the vorticity field:

```shell
singularity exec --nv $simg petibm-vorticity
```

Plot the vorticity field at t=1.0 and t=3.5:

```shell
python scripts/plot_vorticity.py
```

Figure is saved as a PNG file (`vorticity.png`) in the folder `figures` of the simulation directory.

<img src="figures/vorticity.png" width="600">

Compute and plot the history of the recirculation length downstream the cylinder:

```shell
python scripts/plot_recirculation_length.py
```

Figure is saved as a PNG file (`recirculation_length.png`) in the folder `figures` of the simulation directory.

<img src="figures/recirculation_length.png" width="600">
