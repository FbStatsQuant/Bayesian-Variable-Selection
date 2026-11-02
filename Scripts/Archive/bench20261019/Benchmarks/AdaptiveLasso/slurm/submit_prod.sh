#!/bin/bash
# F3 production submission. A new run freezes the code into a read-only snapshot, writes
# SHA256SUMS, LIBRARY_SHA256 and manifest.json, verifies source = snapshot = sums, and submits
# from the snapshot. --resume resubmits chosen tasks of an existing run from its snapshot.
#
#   bash slurm/submit_prod.sh [--dry-run] [--array 1-120]          new production run
#   bash slurm/submit_prod.sh [--dry-run] --smoke                   one-dataset smoke run
#   bash slurm/submit_prod.sh [--dry-run] --resume <run_id> --array <spec> [--attempt 2]
#                             [--time T] [--mem M]                  same-run resubmission
#
# --array defaults to 1-120 (tasks 1-60 = p 500, 61-120 = p 1000). A wave per p (master
# §IV.2.4) is --array 1-60, then --resume <run_id> --array 61-120 after the audit. Concurrency
# %60. Each submission writes an intent file with noclobber, so the same task range cannot be
# submitted twice in one run except as --attempt N (the one infrastructure retry; double --time
# or --mem for TIMEOUT/OOM). A resume is refused while jobs of the run are queued or running.
set -eo pipefail
DRY=0; SMOKE=0; RESUME=""; ARRAY="1-120"; TIME=00:30:00; MEM=2G; ATTEMPT=1
while [ $# -gt 0 ]; do
  case "$1" in
    --dry-run) DRY=1 ;;
    --smoke) SMOKE=1 ;;
    --resume) RESUME=$2; shift ;;
    --array) ARRAY=$2; shift ;;
    --time) TIME=$2; shift ;;
    --mem) MEM=$2; shift ;;
    --attempt) ATTEMPT=$2; shift ;;
    *) echo "unknown arg $1" >&2; exit 1 ;;
  esac
  shift
done
SRC=/home/fb31/projects/BVS/Benchmarks/F3_AdaptiveLasso
STUDY=/projects/ml75/fb31/BVS/bench20261019
FOLDER=F3_AdaptiveLasso
LOGS=$STUDY/logs/prod/$FOLDER
LIBMAN=$STUDY/lib/environment_manifest.txt
FILES="config.R common.R run_case.R score_dev.R methods/glmnet_helpers.R methods/fit_F3_alasso.R tests/test_F3_alasso.R tests/validate_outputs.R slurm/prod_array.slurm slurm/submit_prod.sh"
ONLY=""
if [ -n "$RESUME" ]; then
  RUN_ID=$RESUME
  RUNDIR=$STUDY/runs/$RUN_ID
  SNAP=$RUNDIR/code
  [ -d "$SNAP" ] || { echo "no snapshot for $RUN_ID" >&2; exit 1; }
  if squeue -h -u "$USER" -o "%k" | grep -qx "$RUN_ID"; then echo "jobs of $RUN_ID still queued or running" >&2; exit 1; fi
  case "$RUN_ID" in *prodsmoke*) SMOKE=1 ;; esac
else
  STAMP=$(date -u +%Y%m%dT%H%MZ)
  if [ $SMOKE -eq 1 ]; then KIND=prodsmoke; else KIND=prod; fi
  RUN_ID=${STAMP}_bench20261019_${KIND}_$FOLDER
  RUNDIR=$STUDY/runs/$RUN_ID
  SNAP=$RUNDIR/code
  if [ -e "$RUNDIR" ] || [ -e "$STUDY/results/$RUN_ID" ]; then echo "run $RUN_ID exists" >&2; exit 1; fi
  mkdir -p "$SNAP"
  ( cd "$SRC" && tar cf - $FILES ) | ( cd "$SNAP" && tar xf - )
  ( cd "$SNAP" && sha256sum $FILES ) > "$RUNDIR/SHA256SUMS"
  sha256sum "$LIBMAN" | cut -d' ' -f1 > "$RUNDIR/LIBRARY_SHA256"
  chmod -R a-w "$SNAP"
  ( cd "$SRC" && sha256sum --quiet -c "$RUNDIR/SHA256SUMS" ) || { echo "source differs from snapshot" >&2; exit 1; }
fi
if [ $SMOKE -eq 1 ]; then ARRAY=91; ONLY=p1000_S4_r001; CONC=""; NAME=F3_smoke; else CONC="%60"; NAME=F3_prod; fi
( cd "$SNAP" && sha256sum --quiet -c "$RUNDIR/SHA256SUMS" ) || { echo "snapshot hash mismatch" >&2; exit 1; }
[ "$(sha256sum "$LIBMAN" | cut -d' ' -f1)" = "$(cat "$RUNDIR/LIBRARY_SHA256")" ] \
  || { echo "library manifest changed since the run was frozen" >&2; exit 1; }
STATUS=$LOGS/status/$RUN_ID
mkdir -p "$LOGS" "$STATUS"
CMD="sbatch --parsable --array=$ARRAY$CONC --time=$TIME --mem=$MEM --job-name=$NAME --comment=$RUN_ID --output=$LOGS/%x_%A_%a.out --export=ALL,RUN_ID=$RUN_ID,CODE=$SNAP,RUNDIR=$RUNDIR,STATUS=$STATUS,SMOKE=$SMOKE,ONLY_DATASET=$ONLY $SNAP/slurm/prod_array.slurm"
if [ ! -e "$RUNDIR/manifest.json" ]; then
  if [ $SMOKE -eq 1 ]; then PIECE="smoke test: p1000_S4_r001"; else PIECE="1,200 cases = 120 tasks x 10 datasets"; fi
  {
    echo "{"
    echo "  \"run_id\": \"$RUN_ID\","
    echo "  \"piece\": \"F3 adaptive lasso production, c100 only (D3), $PIECE\","
    echo "  \"array_design\": \"task t: p = 500 if t <= 60 else 1000; u = t or t - 60; S = ceil(u/10); replicates 10*((u-1) mod 10)+1..+10\","
    echo "  \"resources_default\": \"--time=$TIME --mem=$MEM, 1 CPU, commons, %60\","
    echo "  \"frozen_utc\": \"$(date -u +%FT%TZ)\","
    echo "  \"submit_host\": \"$(hostname)\","
    echo "  \"modules\": \"GCC/14.3.0 R/4.5.2\","
    echo "  \"library\": \"$STUDY/lib/R452\","
    echo "  \"library_manifest_sha256\": \"$(cat "$RUNDIR/LIBRARY_SHA256")\","
    echo "  \"inputs\": \"$STUDY/inputs/p{0500,1000}/p{pppp}_S{s}_r{rrr}.rds\","
    echo "  \"input_manifests\": \"$STUDY/manifests/cells/p{pppp}_S{s}_inputs.csv (checked per dataset by run_case.R --manifest)\","
    echo "  \"seeds\": \"method_seed = data_seed + 4000000 (read from each input; data_seed = 1410000/1510000 + 10000 s + r)\","
    echo "  \"outputs\": \"$STUDY/results/$RUN_ID/p{pppp}/<dataset_id>_c100/F3.{rds,csv,sha256,done}\","
    echo "  \"logs\": \"$LOGS\","
    echo "  \"status\": \"$STATUS\","
    echo "  \"submissions\": \"$RUNDIR/SUBMISSIONS.log\","
    echo "  \"code_sha256\": {"
    sed -E 's/^([0-9a-f]+)  (.*)$/    "\2": "\1",/' "$RUNDIR/SHA256SUMS" | sed '$ s/,$//'
    echo "  }"
    echo "}"
  } > "$RUNDIR/manifest.json"
fi
INTENT="$RUNDIR/submit_$(echo "$ARRAY" | tr -c '0-9A-Za-z\n' '_')_attempt$ATTEMPT.intent"
if [ $DRY -eq 1 ]; then
  echo "DRY RUN: $RUN_ID snapshot verified; intent file would be $INTENT; not submitted."
  echo "$CMD"
  exit 0
fi
( set -C; echo "$CMD" > "$INTENT" ) || { echo "already submitted: $INTENT (use --attempt N for a retry)" >&2; exit 1; }
JOB=$($CMD)
echo "$JOB $(date -u +%FT%TZ)" >> "$INTENT"
echo "$(date -u +%FT%TZ) job=$JOB array=$ARRAY time=$TIME mem=$MEM attempt=$ATTEMPT" >> "$RUNDIR/SUBMISSIONS.log"
echo "$RUN_ID $JOB"
