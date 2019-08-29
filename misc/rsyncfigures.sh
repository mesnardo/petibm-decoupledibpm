#!/usr/bin/env bash
# Rsync data to be uploaded to Zenodo.

scriptdir="$( cd "$(dirname "$0")" ; pwd -P )"
rootdir="$( cd "$(dirname "$scriptdir")" ; pwd -P )"
outdir="$rootdir/allfigures"

print_usage() {
        printf "Usage: [-m] MPI directory [-s] Singularity image [-h] Print this message\n"
}

while getopts 'm:o:h' flag; do
        case "${flag}" in
                d) rootdir=`realpath "${OPTARG}"` ;;
                o) outdir=`realpath "${OPTARG}"` ;;
                h) print_usage
                   exit 0 ;;
                *) print_usage
                   exit 1 ;;
        esac
done

python $scriptdir/listfigures.py

listpath="$scriptdir/listfigures.txt"
mkdir -p $outdir

rsync -av --files-from=$listpath --delete $rootdir $outdir

rm -f $listpath

exit 0
