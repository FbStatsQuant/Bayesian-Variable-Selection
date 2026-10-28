#!/bin/bash
#SBATCH --job-name=F4_dev
#SBATCH --partition=commons
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=2G
#SBATCH --time=00:30:00
#SBATCH --array=1-12
#SBATCH --output=/projects/ml75/fb31/BVS/bench20261019/dev_test/F4_MCP_SCAD/logs/%x_%A_%a.out
# Dev test: one dev dataset per task (tasks 1-6: p = 500, S1-S6; 7-12: p = 1000, S1-S6), scale c100,
# method ids F4 and F4_SCAD. Arguments: CODE_DIR (frozen snapshot) RUN_ID.
set -euo pipefail
CODE_DIR=$1; RUN_ID=$2
source "$CODE_DIR/slurm/env.sh"
t=$SLURM_ARRAY_TASK_ID
if [ "$t" -le 6 ]; then p=500; else p=1000; fi
s=$(( (t - 1) % 6 + 1 ))
pp=$(printf "p%04d" $p)
INPUT="$STUDY_DEV/inputs/$pp/dev_${pp}_S${s}_r001.rds"
echo "host $(hostname) job ${SLURM_ARRAY_JOB_ID}_${t} input $INPUT start $(date -u +%FT%TZ)"
Rscript "$CODE_DIR/run_case.R" --input "$INPUT" --out-root "$F4_OUT/results/$RUN_ID" --run-id "$RUN_ID" \
  --scale c100 --methods F4,F4_SCAD --manifest "$STUDY_DEV/manifests/dev_inputs_manifest.csv"
echo "end $(date -u +%FT%TZ)"
