#!/usr/bin/env bash
set -euo pipefail
RUNNER=$1; RUN_ID=$2
[[ "$RUN_ID" =~ ^[0-9]{8}T[0-9]{4,6}Z_bench_f3v2_(dev|prod)$ ]]
bash "$RUNNER/guard_check.sh" 30
source "$RUNNER/env.sh"
python3 "$RUNNER/frozen.py" check /home/fb31/projects/BVS/New_Campaign/code/bench_v2/F3_AdaptiveLasso "$RUNNER/MANIFEST_SHA256.txt" "$RUNNER/freeze.json"
test -r /projects/ml75/fb31/BVS/bench20261019/manifests/inputs_manifest.csv
test -r /projects/ml75/fb31/BVS/bench20261019/dev/manifests/dev_inputs_manifest.csv
mkdir -p "/scratch/fb31/New_Campaign/logs/$RUN_ID/slurm" "/scratch/fb31/New_Campaign/results/$RUN_ID/p0500" "/scratch/fb31/New_Campaign/results/$RUN_ID/p1000"
echo "GATE_OK $(date -u +%FT%TZ)"
