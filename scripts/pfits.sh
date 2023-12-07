#!/bin/bash

# Date: 2023-12-04
# Author: Grégory Sainton
# Purpose: Plot the fits file with zoom and contrast
#         This script will run the python script to plot the fits file with 
#         zoom and contrast
# Version: 1.0 - Initial Version

# Abort on any error
set -e

# Check if ASTROCODE path is set
if [ -z "$ASTROCODE" ]; then
    echo "Error: ASTROCODE path not set"
    echo "Please set the ASTROCODE path in your .bashrc file"
    exit 1
fi


function usage {
    echo "usage: pfits.sh [-h] [-f fitsfile]"
    echo " "
    echo "Plot the fits file with zoom and contrast"
    echo " "
    echo "options:"
    echo "-h, --help                show this help message and exit"
    echo "-f fitsfile, --fitsfile   fits file to plot"
    echo "-d --header               display the header of the fits file"
    exit 2
}

function parse_args {
    while [ $# -gt 0 ]; do
        case "$1" in
            -h|--help)
                usage
                ;;
            -f|--fitsfile)
                fitsfile=$2
                shift
                ;;
            -d|--header)
                header=1
                ;;
            *)
                usage
                ;;
        esac
        shift
    done
}   

function run {
    parse_args "$@"
    if [ -z "$fitsfile" ]; then
        echo "Error: fitsfile not set"
        echo "Please set the fitsfile path"
        exit 1
    fi
    if [ ! -f "$fitsfile" ]; then
        echo "Error: fitsfile not found"
        echo "Please check the fitsfile path"
        exit 1
    fi
    if [ ! -z "$header" ]; then
        python3 $ASTROCODE/plot_fits_v1.1.py $fitsfile -d
    else
        python3 $ASTROCODE/plot_fits_v1.1.py $fitsfile
    fi
}

run "$@"