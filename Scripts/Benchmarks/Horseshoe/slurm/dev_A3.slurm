#!/bin/bash
# Dev test of A3 on the 12 dev datasets (6 scenarios x p in {500, 1000}, dev r001), scale c100.
# Task t = 1..12: p = 500 for t <= 6 else 1000; scenario s = (t - 1) mod 6 + 1.
# Requires RUN_ID and A3_CODE (the frozen snapshot) exported by submit_dev.sh.
#SBATCH --job-name=A3_dev
#SBATCH --partition=commons
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=4G
#SBATCH --time=01:00:00
#SBATCH --array=1-12
#SBATCH --output=/projects/ml75/fb31/BVS/bench20261019/dev_test/A3_Horseshoe/logs/dev_%A_%a.out
set -euo pipefail
: "${RUN_ID:?}" "${A3_CODE:?}"
source "$A3_CODE/slurm/env.sh"
t=$SLURM_ARRAY_TASK_ID
if [ "$t" -le 6 ]; then p=500; else p=1000; fi
s=$(( (t - 1) % 6 + 1 ))
P=$(printf "%04d" $p)
INPUT=$STUDY/dev/inputs/p$P/dev_p${P}_S${s}_r001.rds
echo "host $(hostname)  task $t  p $p  S$s  run $RUN_ID  start $(date -u +%FT%TZ)"
Rscript -e 'cat("detectCores:", parallel::detectCores(), "\n")'
Rscript "$A3_CODE/run_case.R" --input "$INPUT" --manifest "$STUDY/dev/manifests/dev_inputs_manifest.csv" \
  --outroot "$A3_OUT" --run-id "$RUN_ID" --methods A3 --scales c100
echo "end $(date -u +%FT%TZ)"
