#!/bin/bash
# METH-AUDIT default test, 10 study designs (NOT RUN by METH-AUDIT; for the OPS thread to submit).
# Each task: production calibration + serial R=4 final run, the same 4 islands as concurrent workers (bitwise check),
# and R=32 islands x 312 particles on the same frozen grid. 2 CPUs per task (islands run 2 at a time).
# Needs: repo checkout at $REPO (branch theory/METH-AUDIT), study inputs at $STUDY (same layout as Owls
# /home/fb31/ls0_work/study), R >= 4.6 with Rcpp, digest, jsonlite. Edit ma_fit.R's `study` path or symlink.
#SBATCH --job-name=meth_audit10
#SBATCH --partition=commons
#SBATCH --array=1-10
#SBATCH --cpus-per-task=2
#SBATCH --mem=4G
#SBATCH --time=02:00:00
#SBATCH --output=/scratch/fb31/New_Campaign/meth_audit/log_%a.out
set -euo pipefail
REPO=${REPO:-$HOME/BVS_GH}
OUT=/scratch/fb31/New_Campaign/meth_audit; mkdir -p "$OUT"
SPECS=("p0500_S1_r001 c100" "p0500_S2_r001 c050" "p0500_S3_r002 c100" "p0500_S4_r001 c050" "p0500_S5_r002 c100"
       "p0500_S6_r001 c050" "p0500_S1_r003 c050" "p0500_S3_r004 c050" "p0500_S5_r005 c050" "p0500_S6_r002 c100")
set -- ${SPECS[$((SLURM_ARRAY_TASK_ID-1))]}
export OWLS_JOB_CORES=$SLURM_CPUS_PER_TASK MA_WORK=/scratch/fb31/New_Campaign/meth_audit/work
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
Rscript "$REPO/theory_campaign/METH-AUDIT/scripts/ma_fit.R" "$1" "$2" "$OUT/fit_$1_$2.rds" 32
