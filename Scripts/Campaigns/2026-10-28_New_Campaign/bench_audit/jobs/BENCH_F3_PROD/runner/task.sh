#!/usr/bin/env bash
set -euo pipefail
RUNNER=$1; KIND=$2; RUN_ID=$3; SOURCE=$4; ATTEMPT=$5
ROOT=/scratch/fb31/New_Campaign
STUDY=/projects/ml75/fb31/BVS/bench20261019
CODE=/home/fb31/projects/BVS/New_Campaign/code/bench_v2/F3_AdaptiveLasso
source "$RUNNER/env.sh"
python3 "$RUNNER/frozen.py" check "$CODE" "$RUNNER/MANIFEST_SHA256.txt" "$RUNNER/freeze.json"
line=$(python3 "$RUNNER/units.py" "$KIND" --index "$SLURM_ARRAY_TASK_ID" | tail -n 1)
IFS=$'\t' read -r index p scenario replicate scale dataset input_kind <<< "$line"
printf -v pp '%04d' "$p"
if [ "$input_kind" = dev ]; then
 input="$STUDY/dev/inputs/p$pp/$dataset.rds"; manifest="$STUDY/dev/manifests/dev_inputs_manifest.csv"
else
 input="$STUDY/inputs/p$pp/$dataset.rds"; manifest="$STUDY/manifests/inputs_manifest.csv"
fi
logs="$ROOT/logs/$RUN_ID"; mkdir -p "$logs/timing"
echo "task=$index dataset=$dataset scale=$scale host=$(hostname) start=$(date -u +%FT%TZ)"
"$TIME_BIN" -f '%e\t%M' -o "$logs/timing/${index}_attempt${ATTEMPT}.tsv" Rscript --vanilla "$CODE/run_case.R" --input "$input" --out "$ROOT" --run-id "$RUN_ID" --scale "$scale" --methods F3 --manifest "$manifest"
prefix="$ROOT/results/$RUN_ID/p$pp/${dataset}_$scale/F3"
Rscript --vanilla "$RUNNER/validate.R" "$prefix" "$SOURCE" "$input" "$manifest" "$CODE" "$RUN_ID" "$dataset" "$p" "$scenario" "$replicate" "$scale"
echo "finish=$(date -u +%FT%TZ)"
