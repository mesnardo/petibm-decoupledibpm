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
		m) mpidir=`realpath "${OPTARG}"` ;;
		s) simg=`realpath "${OPTARG}"` ;;
		h) print_usage
		   exit 0 ;;
		*) print_usage
		   exit 1 ;;
	esac
done

declare -a folders=(
"dt=0.005"
"dt=0.002"
"dt=0.001"
"dt=0.0005"
)

for folder in "${folders[@]}"
do
    subdir="$scriptdir/$folder"
    echo $subdir
    cd $subdir
    ./run.sh -m $mpidir -s $simg > stdout.txt 2> stderr.txt
done
