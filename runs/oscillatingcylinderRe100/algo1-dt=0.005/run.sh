#!/usr/bin/env bash
# Run simulation(s) within Singularity container.

np=2
export CUDA_VISIBLE_DEVICES=0

scriptdir="$( cd "$(dirname "$0")" ; pwd -P )"

simg=""
mpidir=""

print_usage() {
	printf "Usage: [-m] MPI directory [-s] Singularity image [-h] Print this message\n"
}

while getopts 'm:s:h' flag; do
	case "${flag}" in
		m) mpidir="${OPTARG}" ;;
		s) simg="${OPTARG}" ;;
		h) print_usage
		   exit 0 ;;
		*) print_usage
		   exit 1 ;;
	esac
done

export PATH="$mpidir/bin:$PATH"

mpiexec --version
nvidia-smi

cd $scriptdir
mpiexec -np $np singularity exec --nv $simg \
	petibm-lietal2016 \
	-solver oscillating_cylinder \
	-options_left \
	-log_view ascii:view.log
