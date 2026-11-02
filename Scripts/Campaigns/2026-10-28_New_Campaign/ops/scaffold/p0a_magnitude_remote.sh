#!/bin/bash
# p0a_magnitude_remote.sh (ON NOTS via: ssh nots "STAMP=<STAMP> bash -s" < this): run p0a_magnitude.R (uploaded beforehand to $P) on the login node. Read-only; removes $P.
set -u
: "${STAMP:?}"
H=/home/fb31/projects/BVS/New_Campaign/runs/${STAMP}_lowp_pilot
P=/scratch/fb31/New_Campaign/runs/p0a_magnitude.R
[ -f "$P" ] || { echo "probe not uploaded"; exit 3; }
source /etc/profile.d/modules.sh 2>/dev/null; module purge; module load GCC/14.3.0 R/4.5.2
export R_LIBS_USER=/opt/apps/software/R/4.5.2-gfbf-2025b/lib64/R/library OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 FLEXIBLAS_NUM_THREADS=1
Rscript --vanilla "$P" "$H/code/lowp/R/lowp_generate.R" "$H/study" < /dev/null 2>&1
rm -f -- "$P"
