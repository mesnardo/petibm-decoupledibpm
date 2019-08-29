#!/usr/bin/env bash
# Run simulation(s) within Singularity container.

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

declare -a folders=(
"algo1"
"algo2"
"algo3"
"algo1-1024x1024"
"algo1-256x256"
"algo1-128x128"
"algo1-64x64"
"algo1-dt=0.0005"
"algo1-dt=0.001"
"algo1-dt=0.005"
"algo1-dt=0.01"
"algo1-peskin"
"algo2-peskin"
"algo3-dt=0.0005"
"algo3-dt=0.001"
"algo3-peskin"
"algo3-500Lag"
)

for folder in "${folders[@]}"
do
    subdir="$scriptdir/$folder"
    echo $subdir
    cd $subdir
    ./run.sh -m $mpidir -s $simg
done
