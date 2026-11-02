#!/bin/bash
#SBATCH --job-name=F2_dev
#SBATCH --partition=commons
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=2G
#SBATCH --time=02:00:00
#SBATCH --array=1-12
#SBATCH --output=/projects/ml75/fb31/BVS/bench20261019/dev_test/F2_ElasticNet/logs/dev_%A_%a.out
# Dev test: F2 on the 12 dev datasets (p in {500, 1000} x S1-S6, dev r001), scale c100 only.
# Time: unit tests measured 60-140 s per p = 500 fit (master EST 8-15 s); 2 h allows p = 1000.
# Task t: p = 500 for t <= 6 else 1000; scenario s = (t - 1) mod 6 + 1.
# Needs RUN_ID and CODE (the frozen snapshot) in the environment (see freeze_and_submit_dev.sh).
set -euo pipefail
: "${RUN_ID:?}" "${CODE:?}"
source "$CODE/slurm/env.sh"
T=$SLURM_ARRAY_TASK_ID
if [ "$T" -le 6 ]; then P=500; else P=1000; fi
S=$(( (T - 1) % 6 + 1 ))
PP=$(printf "p%04d" "$P")
ID=$(printf "dev_%s_S%d_r001" "$PP" "$S")
echo "host $(hostname) job ${SLURM_ARRAY_JOB_ID}_${T} dataset $ID start $(date -u +%FT%TZ)"
Rscript "$CODE/run_case.R" --input "$DEV/inputs/$PP/$ID.rds" --out "$OUTROOT/results" \
  --run-id "$RUN_ID" --scales c100 --methods F2 \
  --manifest "$DEV/manifests/dev_inputs_manifest.csv" --code-dir "$CODE"
echo "end $(date -u +%FT%TZ)"
