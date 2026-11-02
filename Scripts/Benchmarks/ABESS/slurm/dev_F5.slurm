#!/usr/bin/env bash
# Dev test of F5: 12-task array, task t -> p = 500 (t <= 6) or 1000, scenario ((t-1) % 6) + 1,
# dev replicate 1, scale c100 only. Usage: sbatch --array=1-12 slurm/dev_F5.slurm <code_dir> <run_id>
#SBATCH --job-name=F5_dev
#SBATCH --partition=commons
#SBATCH --account=commons
#SBATCH --cpus-per-task=1
#SBATCH --mem=2G
#SBATCH --time=00:20:00
#SBATCH --output=/projects/ml75/fb31/BVS/bench20261019/dev_test/F5_ABESS/logs/%x_%A_%a.out
#SBATCH --error=/projects/ml75/fb31/BVS/bench20261019/dev_test/F5_ABESS/logs/%x_%A_%a.err
set -euo pipefail
CODE=${1:?code dir}; RUN_ID=${2:?run id}
source "$CODE/slurm/env.sh"
t=${SLURM_ARRAY_TASK_ID:?}
[[ "$t" -ge 1 && "$t" -le 12 ]]
if [ "$t" -le 6 ]; then p=500; else p=1000; fi
s=$(( (t - 1) % 6 + 1 ))
pp=$(printf 'p%04d' "$p")
input="$DEV_ROOT/inputs/$pp/dev_${pp}_S${s}_r001.rds"
Rscript --vanilla "$CODE/run_case.R" --input "$input" \
  --manifest "$DEV_ROOT/manifests/dev_inputs_manifest.csv" \
  --out-root "$F5_OUT" --run-id "$RUN_ID" --scales c100 --methods F5 --code-root "$CODE"
