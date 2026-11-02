#!/bin/bash
# p0a_probe_remote.sh (ON NOTS via: ssh nots "STAMP=<STAMP> bash -s" < this): run p0a_probe.R (uploaded beforehand to $P) on the login node with the pilot's
# R modules, under the default FlexiBLAS backend and under FLEXIBLAS=NETLIB. Read-only; removes $P at the end.
set -u
: "${STAMP:?}"
G=/home/fb31/projects/BVS/New_Campaign/runs/${STAMP}_lowp_pilot/code/lowp/R/lowp_generate.R
P=/scratch/fb31/New_Campaign/runs/p0a_probe.R
[ -f "$P" ] || { echo "probe not uploaded"; exit 3; }
source /etc/profile.d/modules.sh 2>/dev/null; module purge; module load GCC/14.3.0 R/4.5.2
export R_LIBS_USER=/opt/apps/software/R/4.5.2-gfbf-2025b/lib64/R/library OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 FLEXIBLAS_NUM_THREADS=1
echo "host=$(hostname) cpu=$(lscpu | awk -F: '/Model name/{print $2}' | xargs)"
echo "--- default backend"; Rscript --vanilla "$P" "$G" < /dev/null 2>&1
echo "--- FLEXIBLAS=NETLIB"; FLEXIBLAS=NETLIB Rscript --vanilla "$P" "$G" < /dev/null 2>&1
echo "--- flexiblas backends"; flexiblas list < /dev/null 2>&1 | head -20
rm -f -- "$P"
