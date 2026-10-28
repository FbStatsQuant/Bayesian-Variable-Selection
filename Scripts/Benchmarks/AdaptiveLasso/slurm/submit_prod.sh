#!/bin/bash
# F3 submission, c050 copy (BRIEF_C050_ENG). A new run freezes the code copy into a read-only snapshot,
# writes SHA256SUMS, LIBRARY_SHA256 and manifest.json, verifies source = snapshot = sums, and submits
# from the snapshot. --resume resubmits chosen tasks of an existing run from its snapshot.
#
#   bash slurm/submit_prod.sh --mode prod --time T --mem M [--dry-run] [--array 1-400]   production, c050, %133
#   bash slurm/submit_prod.sh --mode check [--dry-run]   c100 reproduction: task 301 = p1000_S4_r001-r003, then a
#                             dependent job compares with the c = 1 production run (c050tools/compare_c050check.R)
#   bash slurm/submit_prod.sh --mode pilot [--dry-run]   c050 pilot: the 12 datasets r001, one per task, then a
#                             dependent job writes the diagnostics summary (c050tools/pilot_diag_c050.R)
#   bash slurm/submit_prod.sh [--dry-run] --resume <run_id> --array <spec> [--attempt 2]
#                             [--time T] [--mem M]                  same-run resubmission
#
# Tasks 1-200 = p 500, 201-400 = p 1000 (3 datasets per task). Each submission writes an intent file with
# noclobber, so the same task range cannot be submitted twice in one run except as --attempt N (the one
# infrastructure retry; double --time or --mem for TIMEOUT/OOM). A resume is refused while jobs of the run
# are queued or running.
set -eo pipefail
DRY=0; MODE=""; RESUME=""; ARRAY=""; TIME=""; MEM=""; ATTEMPT=1
while [ $# -gt 0 ]; do
  case "$1" in
    --dry-run) DRY=1 ;;
    --mode) MODE=$2; shift ;;
    --resume) RESUME=$2; shift ;;
    --array) ARRAY=$2; shift ;;
    --time) TIME=$2; shift ;;
    --mem) MEM=$2; shift ;;
    --attempt) ATTEMPT=$2; shift ;;
    *) echo "unknown arg $1" >&2; exit 1 ;;
  esac
  shift
done
SRC=/home/fb31/projects/BVS/Benchmarks/F3_AdaptiveLasso/c050
STUDY=/projects/ml75/fb31/BVS/bench20261019
FOLDER=F3_AdaptiveLasso
REF_RUN=20261019T2157Z_bench20261019_prod_F3_AdaptiveLasso       # c = 1 production run (reference for check)
PILOT_IDS=p0500_S1_r001:p0500_S2_r001:p0500_S3_r001:p0500_S4_r001:p0500_S5_r001:p0500_S6_r001:p1000_S1_r001:p1000_S2_r001:p1000_S3_r001:p1000_S4_r001:p1000_S5_r001:p1000_S6_r001
LOGS=$STUDY/logs/prod/$FOLDER
LIBMAN=$STUDY/lib/environment_manifest.txt
FILES="config.R common.R run_case.R score_dev.R methods/glmnet_helpers.R methods/fit_F3_alasso.R tests/test_F3_alasso.R tests/validate_outputs.R slurm/prod_array.slurm slurm/submit_prod.sh c050tools/compare_c050check.R c050tools/pilot_diag_c050.R"
if [ -n "$RESUME" ]; then
  case "$RESUME" in *_prodc050_*) MODE=prod;; *_c050check_*) MODE=check;; *_pilotc050_*) MODE=pilot;;
    *) echo "not a c050 run id: $RESUME" >&2; exit 1;; esac
fi
case "$MODE" in
  prod)  SCALE=c050; IDS=""; CONC="%133"; LABEL=prodc050; ARRAY=${ARRAY:-1-400}
         [ -n "$RESUME" ] || { [ -n "$TIME" ] && [ -n "$MEM" ]; } || { echo "--mode prod needs --time and --mem (from the pilot)" >&2; exit 1; } ;;
  check) SCALE=c100; IDS=""; CONC=""; LABEL=c050check; ARRAY=${ARRAY:-301} ;;
  pilot) SCALE=c050; IDS=$PILOT_IDS; CONC=""; LABEL=pilotc050; ARRAY=${ARRAY:-1-12} ;;
  *) echo "--mode prod|check|pilot is required" >&2; exit 1 ;;
esac
TIME=${TIME:-01:15:00}; MEM=${MEM:-2G}                         # check/pilot defaults = the c = 1 per-task values
if [ -n "$RESUME" ]; then
  RUN_ID=$RESUME
  RUNDIR=$STUDY/runs/$RUN_ID
  SNAP=$RUNDIR/code
  [ -d "$SNAP" ] || { echo "no snapshot for $RUN_ID" >&2; exit 1; }
  if squeue -h -u "$USER" -o "%k" | grep -qx "$RUN_ID"; then echo "jobs of $RUN_ID still queued or running" >&2; exit 1; fi
else
  STAMP=$(date -u +%Y%m%dT%H%MZ)
  RUN_ID=${STAMP}_bench20261019_${LABEL}_$FOLDER
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
NAME=F3_prod
( cd "$SNAP" && sha256sum --quiet -c "$RUNDIR/SHA256SUMS" ) || { echo "snapshot hash mismatch" >&2; exit 1; }
[ "$(sha256sum "$LIBMAN" | cut -d' ' -f1)" = "$(cat "$RUNDIR/LIBRARY_SHA256")" ] \
  || { echo "library manifest changed since the run was frozen" >&2; exit 1; }
STATUS=$LOGS/status/$RUN_ID
mkdir -p "$LOGS" "$STATUS"
# C050_SCALE / C050_IDS are set by env on the command itself, so values inherited from the caller's shell
# are overridden; --export=ALL passes them to the job.
CMD="env C050_SCALE=$SCALE C050_IDS=$IDS sbatch --parsable --array=$ARRAY$CONC --time=$TIME --mem=$MEM --job-name=$NAME --comment=$RUN_ID --output=$LOGS/%x_%A_%a.out --export=ALL,RUN_ID=$RUN_ID,CODE=$SNAP,RUNDIR=$RUNDIR,STATUS=$STATUS $SNAP/slurm/prod_array.slurm"
case "$MODE" in
  check) POST="Rscript --vanilla $SNAP/c050tools/compare_c050check.R $STUDY/results/$RUN_ID $STUDY/results/$REF_RUN p1000_S4_r001,p1000_S4_r002,p1000_S4_r003 F3 $STUDY/results/$RUN_ID/c050check_compare.txt" ;;
  pilot) POST="Rscript --vanilla $SNAP/c050tools/pilot_diag_c050.R $STUDY/results/$RUN_ID ${IDS//:/,} F3 c050 100 $STUDY/results/$RUN_ID/pilotc050_diag.txt" ;;
  *) POST="" ;;
esac
[ -n "$RESUME" ] && POST=""
if [ ! -e "$RUNDIR/manifest.json" ]; then
  case "$MODE" in
    prod) PIECE="1,200 cases = 400 tasks x 3 datasets"
          TASKMAP="task t: p = 500 if t <= 200 else 1000; u = (t-1) mod 200; datasets i = 3u..3u+2 of the scenario-major order, S = i/100 + 1, r = i mod 100 + 1" ;;
    check) PIECE="c100 reproduction check: task 301 = p1000_S4_r001-r003"; TASKMAP="production map, task 301 only" ;;
    pilot) PIECE="c050 pilot: 12 datasets r001"; TASKMAP="task t runs the t-th of $IDS" ;;
  esac
  {
    echo "{"
    echo "  \"run_id\": \"$RUN_ID\","
    echo "  \"piece\": \"F3 adaptive lasso, c050 copy, mode $MODE, scale $SCALE, $PIECE\","
    echo "  \"code_source\": \"$SRC (copy of the c = 1 snapshot $STUDY/runs/$REF_RUN/code; diff in $SRC/C050_DIFF.txt)\","
    echo "  \"scale_key\": \"$SCALE\","
    echo "  \"array_design\": \"$TASKMAP\","
    echo "  \"command\": \"$CMD\","
    echo "  \"post_job\": \"$( [ -n "$POST" ] && echo "afterany dependent job: $POST" )\","
    echo "  \"resources_default\": \"--time=$TIME --mem=$MEM, 1 CPU, commons, array $ARRAY$CONC\","
    echo "  \"frozen_utc\": \"$(date -u +%FT%TZ)\","
    echo "  \"submit_host\": \"$(hostname)\","
    echo "  \"modules\": \"GCC/14.3.0 R/4.5.2\","
    echo "  \"library\": \"$STUDY/lib/R452\","
    echo "  \"library_manifest_sha256\": \"$(cat "$RUNDIR/LIBRARY_SHA256")\","
    echo "  \"inputs\": \"$STUDY/inputs/p{0500,1000}/p{pppp}_S{s}_r{rrr}.rds\","
    echo "  \"input_manifests\": \"$STUDY/manifests/cells/p{pppp}_S{s}_inputs.csv (checked per dataset by run_case.R --manifest)\","
    echo "  \"seeds\": \"method_seed = data_seed + 4000000 (read from each input; data_seed = 1410000/1510000 + 10000 s + r)\","
    echo "  \"outputs\": \"$STUDY/results/$RUN_ID/p{pppp}/<dataset_id>_$SCALE/F3.{rds,csv,sha256,done}\","
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
  [ -n "$POST" ] && echo "POST (afterany): $POST"
  exit 0
fi
( set -C; echo "$CMD" > "$INTENT" ) || { echo "already submitted: $INTENT (use --attempt N for a retry)" >&2; exit 1; }
JOB=$($CMD)
echo "$JOB $(date -u +%FT%TZ)" >> "$INTENT"
echo "$(date -u +%FT%TZ) job=$JOB array=$ARRAY$CONC time=$TIME mem=$MEM attempt=$ATTEMPT scale=$SCALE" >> "$RUNDIR/SUBMISSIONS.log"
PJOB=""
if [ -n "$POST" ]; then
  PJOB=$(sbatch --parsable --dependency=afterany:$JOB --job-name=F3_c050post --partition=commons --time=00:15:00 --mem=2G \
    --output=$LOGS/%x_%j.out --wrap "bash -c 'module load GCC/14.3.0 && module load R/4.5.2 && export R_LIBS_USER= && $POST'") || PJOB="sbatch failed"
  echo "$(date -u +%FT%TZ) post job=$PJOB (afterany:$JOB) cmd=$POST" >> "$RUNDIR/SUBMISSIONS.log"
fi
echo "$RUN_ID $JOB $PJOB"
