#!/usr/bin/env bash

#SBATCH --job-name="sphere"
#SBATCH --output=slurm-%j.out
#SBATCH --error=slurm-%j.err
#SBATCH --partition=gpu_exp
#SBATCH --nodes=4
#SBATCH --ntasks-per-node=28
#SBATCH --time=15:00:00

module load singularity/2.5.2
module load openmpi/gcc/64/3.1.2

n=4
npernode=28
np=$(($n * $npernode))
export CUDA_VISIBLE_DEVICES=0

nvidia-smi

image="/home/mesnardo/runs/petibm-decoupledibpm/petibm-decoupledibpm_xenial.sif"

simudir="/lustre/groups/barbalab/oscillatingsphere"
indir="/mnt"

mpiexec singularity exec \
	--bind $simudir:$indir \
	--nv $image petibm-lietal2016 \
	-directory $indir \
	-solver oscillating_sphere \
	-options_left \
	-log_view ascii:$indir/view.log
