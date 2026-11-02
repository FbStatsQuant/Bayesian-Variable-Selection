#!/bin/bash
# Freezes the code into a read-only snapshot, writes manifest.json and submits the
# 12-task dev array from the snapshot. Usage: bash slurm/submit_dev.sh
set -eo pipefail
CODE=/home/fb31/projects/BVS/Benchmarks/F3_AdaptiveLasso
OUT=/projects/ml75/fb31/BVS/bench20261019/dev_test/F3_AdaptiveLasso
DEV=/projects/ml75/fb31/BVS/bench20261019/dev
RUN_ID=$(date -u +%Y%m%dT%H%MZ)_bench20261019_devtest_F3
RUNDIR=$OUT/runs/$RUN_ID
SNAP=$RUNDIR/code
if [ -e "$RUNDIR" ]; then echo "run dir exists: $RUNDIR" >&2; exit 1; fi
mkdir -p "$SNAP" "$OUT/logs"
cp -r "$CODE"/config.R "$CODE"/common.R "$CODE"/run_case.R "$CODE"/score_dev.R \
      "$CODE"/methods "$CODE"/tests "$CODE"/slurm "$SNAP"/
chmod -R a-w "$SNAP"
CMD="sbatch --parsable --export=ALL,RUN_ID=$RUN_ID,CODE=$SNAP $SNAP/slurm/dev_array.slurm"
JOB=$($CMD)
cd "$SNAP"
{
  echo "{"
  echo "  \"run_id\": \"$RUN_ID\","
  echo "  \"piece\": \"F3 dev test, 12 dev datasets x c100\","
  echo "  \"job_id\": \"$JOB\","
  echo "  \"sbatch\": \"$CMD\","
  echo "  \"submit_host\": \"$(hostname)\","
  echo "  \"submitted_utc\": \"$(date -u +%FT%TZ)\","
  echo "  \"modules\": \"GCC/14.3.0 R/4.5.2\","
  echo "  \"library\": \"/projects/ml75/fb31/BVS/bench20261019/lib/R452\","
  echo "  \"library_manifest_sha256\": \"$(sha256sum /projects/ml75/fb31/BVS/bench20261019/lib/environment_manifest.txt | cut -d' ' -f1)\","
  echo "  \"inputs_manifest\": \"$DEV/manifests/dev_inputs_manifest.csv\","
  echo "  \"inputs_manifest_sha256\": \"$(sha256sum $DEV/manifests/dev_inputs_manifest.csv | cut -d' ' -f1)\","
  echo "  \"seeds\": \"method_seed = data_seed + 4000000 per dataset (dev manifest)\","
  echo "  \"outputs\": \"$OUT/results/$RUN_ID\","
  echo "  \"code_sha256\": {"
  find . -type f | sort | while read -r f; do echo "    \"${f#./}\": \"$(sha256sum "$f" | cut -d' ' -f1)\","; done | sed '$ s/,$//'
  echo "  }"
  echo "}"
} > "$RUNDIR/manifest.json"
echo "$RUN_ID $JOB"
