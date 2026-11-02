#!/bin/bash
# F3 dev test: 12 dev datasets (S1-S6 x p = 500, 1000; dev replicate 1), scale c100 only.
# Task t = 1..6 -> p = 500, S = t; t = 7..12 -> p = 1000, S = t - 6.
# Submitted by slurm/submit_dev.sh, which sets RUN_ID and CODE (the frozen snapshot).
#SBATCH --job-name=F3_dev
#SBATCH --partition=commons
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=2G
#SBATCH --time=00:20:00
#SBATCH --array=1-12
#SBATCH --output=/projects/ml75/fb31/BVS/bench20261019/dev_test/F3_AdaptiveLasso/logs/dev_%A_%a.out
set -eo pipefail
: "${RUN_ID:?RUN_ID not set}" "${CODE:?CODE not set}"
module load GCC/14.3.0
module load R/4.5.2
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 FLEXIBLAS_NUM_THREADS=1
export R_LIBS_USER=
DEV=/projects/ml75/fb31/BVS/bench20261019/dev
OUT=/projects/ml75/fb31/BVS/bench20261019/dev_test/F3_AdaptiveLasso
t=$SLURM_ARRAY_TASK_ID
if [ "$t" -le 6 ]; then P=0500; S=$t; else P=1000; S=$((t - 6)); fi
echo "host $(hostname) job ${SLURM_ARRAY_JOB_ID}_${t} p$P S$S start $(date -u +%FT%TZ)"
Rscript "$CODE/run_case.R" --input "$DEV/inputs/p$P/dev_p${P}_S${S}_r001.rds" --out "$OUT" \
  --run-id "$RUN_ID" --scale c100 --methods F3 --manifest "$DEV/manifests/dev_inputs_manifest.csv"
echo "end $(date -u +%FT%TZ)"
