#!/bin/bash
# Dev test submission (policy §8; master §IV.3.1).
#   bash slurm/submit_dev.sh new [ARRAY]      freeze the code into a read-only snapshot under the
#                                             output folder, write manifest.json, submit ARRAY (default 1-12)
#   bash slurm/submit_dev.sh RUN_ID ARRAY     submit more tasks of an existing run with the same snapshot
set -euo pipefail
SRC=/home/fb31/projects/BVS/Benchmarks/A3_Horseshoe
STUDY=/projects/ml75/fb31/BVS/bench20261019
A3_OUT=$STUDY/dev_test/A3_Horseshoe
MODE=${1:?usage: submit_dev.sh new [ARRAY] | RUN_ID ARRAY}
ARRAY=${2:-1-12}
if [ "$MODE" = new ]; then
  RUN_ID=dev_$(date -u +%Y%m%dT%H%MZ)_A3
  RUN_DIR=$A3_OUT/runs/$RUN_ID
  [ -e "$RUN_DIR" ] && { echo "run dir exists: $RUN_ID"; exit 1; }
  SNAP=$RUN_DIR/code
  mkdir -p "$SNAP" "$A3_OUT/logs"
  cp -r "$SRC"/config.R "$SRC"/common.R "$SRC"/run_case.R "$SRC"/score_dev.R "$SRC"/check_outputs.R \
        "$SRC"/methods "$SRC"/tests "$SRC"/slurm "$SNAP"/
  ( cd "$SNAP" && find . -type f | sort | xargs sha256sum ) > "$RUN_DIR/code_sha256.txt"
  chmod -R a-w "$SNAP"
  TREE=$(sha256sum "$RUN_DIR/code_sha256.txt" | cut -d' ' -f1)
  {
    echo "{"
    echo "  \"run_id\": \"$RUN_ID\","
    echo "  \"piece\": \"A3 dev test, 12 dev datasets (6 scenarios x p 500/1000, dev r001), scale c100\","
    echo "  \"code_snapshot\": \"$SNAP\","
    echo "  \"code_files_sha256\": \"code_sha256.txt\","
    echo "  \"code_tree_sha256\": \"$TREE\","
    echo "  \"seeds\": \"method_seed = data_seed + 4000000 per dataset (dev_inputs_manifest.csv)\","
    echo "  \"modules\": \"GCC/14.3.0 R/4.5.2\","
    echo "  \"library\": \"$STUDY/lib/R452\","
    echo "  \"library_manifest_sha256\": \"$(sha256sum $STUDY/lib/environment_manifest.txt | cut -d' ' -f1)\","
    echo "  \"inputs\": \"$STUDY/dev/inputs/p0500, $STUDY/dev/inputs/p1000\","
    echo "  \"inputs_manifest_sha256\": \"$(sha256sum $STUDY/dev/manifests/dev_inputs_manifest.csv | cut -d' ' -f1)\","
    echo "  \"outputs\": \"$A3_OUT/results/$RUN_ID\","
    echo "  \"created_utc\": \"$(date -u +%FT%TZ)\""
    echo "}"
  } > "$RUN_DIR/manifest.json"
else
  RUN_ID=$MODE
  RUN_DIR=$A3_OUT/runs/$RUN_ID
  SNAP=$RUN_DIR/code
  [ -d "$SNAP" ] || { echo "no snapshot for $RUN_ID"; exit 1; }
fi
CMD="sbatch --parsable --array=$ARRAY --export=ALL,RUN_ID=$RUN_ID,A3_CODE=$SNAP $SNAP/slurm/dev_A3.slurm"
JOB=$($CMD)
echo "$(date -u +%FT%TZ)  host $(hostname)  job $JOB  array $ARRAY  cmd: $CMD" >> "$RUN_DIR/submissions.log"
echo "$RUN_ID $JOB"
