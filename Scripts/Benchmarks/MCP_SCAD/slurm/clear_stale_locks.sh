#!/bin/bash
# Removes per-pair locks and temporary files left by killed F4 jobs (TIMEOUT, OOM, node failure) in one
# run, before the infrastructure retry. Refuses while any F4 production or canary job is queued or running.
#   bash slurm/clear_stale_locks.sh <run_id>
set -euo pipefail
RUN_ID=$1
R=/projects/ml75/fb31/BVS/bench20261019/results/$RUN_ID
[ -d "$R" ] || { echo "no such run: $R"; exit 1; }
if squeue -u "$USER" -h -n F4_prod,F4_canary | grep -q .; then echo "F4 jobs still queued or running; refusing"; exit 1; fi
find "$R" -type d -name "*.lock" -print -exec rm -rf {} +
find "$R" -type f -name "*.tmp.*" -print -delete
echo "cleared"
