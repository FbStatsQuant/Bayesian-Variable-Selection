#!/usr/bin/env bash
# Dev test: F1 on the 12 dev datasets (6 scenarios x p in {500, 1000}, dev replicate 1), scale c100 only.
# Array task t = 1..12: p = 500 for t <= 6, else 1000; scenario = (t - 1) %% 6 + 1.
# Usage: sbatch --array=1-12 dev_test.slurm <code_dir (frozen snapshot)> <run_id>
#SBATCH --job-name=F1_dev
#SBATCH --account=commons
#SBATCH --partition=commons
#SBATCH --cpus-per-task=1
#SBATCH --mem=2G
#SBATCH --time=00:30:00
#SBATCH --output=/projects/ml75/fb31/BVS/bench20261019/dev_test/F1_Lasso/logs/%x_%A_%a.out
#SBATCH --error=/projects/ml75/fb31/BVS/bench20261019/dev_test/F1_Lasso/logs/%x_%A_%a.err
set -euo pipefail
CODE=${1:?code dir}; RUN_ID=${2:?run id}
source "$CODE/slurm/env.sh"
t=${SLURM_ARRAY_TASK_ID:?}
[[ "$t" -ge 1 && "$t" -le 12 ]]
if [[ "$t" -le 6 ]]; then p=500; else p=1000; fi
s=$(( (t - 1) % 6 + 1 ))
id=$(printf 'dev_p%04d_S%d_r001' "$p" "$s")
export TMPDIR=$(mktemp -d /tmp/fb31_F1_XXXXXX); trap 'rm -rf -- "$TMPDIR"' EXIT
Rscript --vanilla "$CODE/run_case.R" --code-dir "$CODE" --input "$DEV_INPUTS/$(printf 'p%04d' "$p")/$id.rds" \
  --scale c100 --out-root "$F1_OUT" --run-id "$RUN_ID" --manifest "$DEV_MANIFEST" --lib "$BENCH_LIB"
