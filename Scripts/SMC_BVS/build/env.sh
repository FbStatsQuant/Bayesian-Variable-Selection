#!/usr/bin/env bash
# Owls environment mandated by BRIEF Amendment 1. All child tools inherit nice 19.
set -euo pipefail
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
export BLIS_NUM_THREADS=1 FLEXIBLAS_NUM_THREADS=1
export MAKEFLAGS=-j1
Rscript --version 2>&1 | grep -q 'version 4.6.0'
gcc -dumpfullversion | grep -qx '11.5.0'
