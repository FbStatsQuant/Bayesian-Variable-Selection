#!/usr/bin/env bash
# OPS supplies /scratch/fb31/New_Campaign/upload/RUN_ID with runner, source and manifest.
set -euo pipefail
export PYTHONDONTWRITEBYTECODE=1
UPLOAD=$1
UPLOAD_HASH=$2
[[ "$UPLOAD" =~ ^/scratch/fb31/New_Campaign/upload/[0-9]{8}T[0-9]{4,6}Z_bench_f3v2_(dev|prod)$ ]]
test -d "$UPLOAD/runner"
python3 "$UPLOAD/runner/upload_check.py" "$UPLOAD" "$UPLOAD_HASH"
cmp "$UPLOAD/MANIFEST_SHA256.txt" "$UPLOAD/runner/MANIFEST_SHA256.txt"
bash "$UPLOAD/runner/guard_check.sh" 30
python3 "$UPLOAD/runner/frozen.py" stage "$UPLOAD/F3_AdaptiveLasso" "$UPLOAD/MANIFEST_SHA256.txt" "$UPLOAD/runner/freeze.json" /home/fb31/projects/BVS/New_Campaign/code/bench_v2/F3_AdaptiveLasso
python3 "$UPLOAD/runner/frozen.py" check /home/fb31/projects/BVS/New_Campaign/code/bench_v2/F3_AdaptiveLasso "$UPLOAD/runner/MANIFEST_SHA256.txt" "$UPLOAD/runner/freeze.json"
echo "STAGED_OK"
