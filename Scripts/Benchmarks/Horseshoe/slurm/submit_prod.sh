#!/bin/bash
# Production submission for A3 (policy §8; master §IV.3.1, §IV.2.4; PROD_READINESS_BRIEF section 2).
# Longer-chain sensitivity copy (PREREG_c050 R6): run id <UTC>_bench20261019_<KIND>_A3_Horseshoe, one fit
# per task over a frozen case list (the ess_tau-flagged production fits), 8 x production budget:
#   longc050 (A3_SCALE=c050, cases/cases_longc050.txt, reference run 20261021T1818Z_bench20261019_prodc050_A3_Horseshoe)
#   longc100 (A3_SCALE=c100, cases/cases_longc100.txt, reference run 20261019T2209Z_bench20261019_prod_A3_Horseshoe)
#   bash slurm/submit_prod.sh --kind KIND [--array LIST] [--time HH:MM:SS] [--mem NG] [--dry-run]
#   bash slurm/submit_prod.sh --resume RUN_ID [--array LIST] [--time HH:MM:SS] [--mem NG] [--dry-run]
#                         resubmit tasks of an existing run from its own snapshot, mode and frozen inputs
#                         manifest (the runner redoes only cases without a valid .done)
# Order: freeze code, inputs manifest and mode -> verify hashes -> write manifest.json (job_id
# "pending") and an exclusive submission-intent file -> sbatch -> record the job id, remove the
# intent. A leftover intent file means an earlier submission's outcome is unknown: check squeue,
# then remove it by hand. Every task re-verifies the snapshot and the frozen files.
set -euo pipefail
SRC=/home/fb31/projects/BVS/Benchmarks/A3_Horseshoe/c050/longchain
STUDY=/projects/ml75/fb31/BVS/bench20261019
LOGDIR=$STUDY/logs/prod/A3_Horseshoe
FOLDER=A3_Horseshoe
# Resources (brief section 2): --time = 3 x (dev p95 per case x 10), rounded up, >= 30 min;
# --mem = 2 x dev max MaxRSS, >= 2 GB. Basis recorded in README.md.
TIME=06:00:00     # one fit at 8 x budget; production worst fit 1,645 s on a slow node x 8 = 3.7 h
MEM=16G          # production MaxRSS 1.2 GB at p = 1000 scales with stored draws (x 8): ~9.5 GB projected
ARRAY=""

DRY=0; SMOKE=""; RESUME=""; ARRAY_SET=0; KIND=""
while [ $# -gt 0 ]; do
  case "$1" in
    --dry-run) DRY=1; shift ;;
    --kind) KIND=$2; shift 2 ;;
    --resume) RESUME=$2; shift 2 ;;
    --array) ARRAY=$2; ARRAY_SET=1; shift 2 ;;
    --time) TIME=$2; shift 2 ;;
    --mem) MEM=$2; shift 2 ;;
    *) echo "unknown argument $1"; exit 1 ;;
  esac
done
[ "$TIME" != "__TIME__" ] && [ "$MEM" != "__MEM__" ] || { echo "TIME/MEM not set"; exit 1; }
[ -n "$KIND" ] && [ -n "$RESUME" ] && { echo "--kind and --resume are exclusive (a resume keeps the run's own kind)"; exit 1; }

if [ -n "$RESUME" ]; then
  RUN_ID=$RESUME
  RUN_DIR=$STUDY/runs/$RUN_ID; SNAP=$RUN_DIR/code
  [ -d "$SNAP" ] && [ -f "$RUN_DIR/frozen.env" ] || { echo "no snapshot or frozen.env for $RUN_ID"; exit 1; }
  # shellcheck disable=SC1091
  source "$RUN_DIR/frozen.env"            # MODE (= kind), SCALE, DATASETS, MANIFEST_SHA256, LIBMAN_SHA256
else
  case "$KIND" in longc050|longc100) ;; *) echo "--kind must be longc050 or longc100"; exit 1 ;; esac
  STAMP=$(date -u +%Y%m%dT%H%MZ)
  RUN_ID=${STAMP}_bench20261019_${KIND}_$FOLDER; MODE=$KIND; DATASETS=""
  case "$KIND" in longc100) SCALE=c100; PROD_RUN=20261019T2209Z_bench20261019_prod_A3_Horseshoe ;;
    *) SCALE=c050; PROD_RUN=20261021T1818Z_bench20261019_prodc050_A3_Horseshoe ;; esac
  RUN_DIR=$STUDY/runs/$RUN_ID; SNAP=$RUN_DIR/code
  [ -e "$RUN_DIR" ] && { echo "run dir exists: $RUN_DIR"; exit 1; }
  mkdir -p "$SNAP" "$LOGDIR"
  cp -r "$SRC"/config.R "$SRC"/common.R "$SRC"/run_case.R "$SRC"/check_outputs.R "$SRC"/score_dev.R \
        "$SRC"/methods "$SRC"/tests "$SRC"/slurm "$SRC"/tools "$SRC"/cases "$SNAP"/
  ( cd "$SNAP" && find . -type f | LC_ALL=C sort | xargs sha256sum ) > "$RUN_DIR/code_sha256.txt"
  cp "$STUDY/manifests/inputs_manifest.csv" "$RUN_DIR/inputs_manifest.csv"
  MANIFEST_SHA256=$(sha256sum "$RUN_DIR/inputs_manifest.csv" | cut -d' ' -f1)
  LIBMAN_SHA256=$(sha256sum "$STUDY/lib/environment_manifest.txt" | cut -d' ' -f1)
  cp "$SNAP/cases/cases_${KIND}.txt" "$RUN_DIR/cases.txt"
  CASES_SHA256=$(sha256sum "$RUN_DIR/cases.txt" | cut -d' ' -f1)
  printf 'MODE=%s\nSCALE=%s\nDATASETS=%s\nMANIFEST_SHA256=%s\nLIBMAN_SHA256=%s\nPROD_RUN=%s\nCASES_SHA256=%s\n' "$MODE" "$SCALE" "$DATASETS" "$MANIFEST_SHA256" "$LIBMAN_SHA256" "$PROD_RUN" "$CASES_SHA256" > "$RUN_DIR/frozen.env"
  chmod -R a-w "$SNAP"; chmod a-w "$RUN_DIR/inputs_manifest.csv" "$RUN_DIR/frozen.env" "$RUN_DIR/code_sha256.txt" "$RUN_DIR/cases.txt"
fi

NCASES=$(grep -c . "$RUN_DIR/cases.txt")
[ "$(sha256sum "$RUN_DIR/cases.txt" | cut -d' ' -f1)" = "${CASES_SHA256:-}" ] || { echo "REFUSED: frozen case list changed"; exit 2; }
case "$MODE" in longc050) WANT=c050; DEF=1-$NCASES ;; longc100) WANT=c100; DEF=1-$NCASES ;;
  *) echo "REFUSED: $RUN_ID is not a longchain run (mode $MODE)"; exit 2 ;; esac
[ "${SCALE:-}" = "$WANT" ] || { echo "REFUSED: run kind $MODE requires scale $WANT (frozen: ${SCALE:-none})"; exit 2; }
[ "$ARRAY_SET" -eq 1 ] || ARRAY=$DEF

# Refuse if the snapshot or the frozen files differ from what was recorded, or (new runs) if the
# source folder changed during the freeze.
( cd "$SNAP" && sha256sum --quiet -c "$RUN_DIR/code_sha256.txt" ) || { echo "REFUSED: snapshot hash mismatch"; exit 2; }
[ "$(sha256sum "$RUN_DIR/inputs_manifest.csv" | cut -d' ' -f1)" = "$MANIFEST_SHA256" ] || { echo "REFUSED: frozen inputs manifest changed"; exit 2; }
[ "$(sha256sum "$STUDY/lib/environment_manifest.txt" | cut -d' ' -f1)" = "$LIBMAN_SHA256" ] || { echo "REFUSED: library manifest changed"; exit 2; }
if [ -z "$RESUME" ]; then
  ( cd "$SRC" && sha256sum --quiet -c "$RUN_DIR/code_sha256.txt" ) || { echo "REFUSED: source changed during freeze"; exit 2; }
fi
# No overlapping submissions of one run: refuse while an earlier job of this run is queued or running.
if [ -f "$RUN_DIR/submissions.log" ]; then
  JOBS=$(awk '{for (i = 1; i <= NF; i++) if ($i == "job") print $(i + 1)}' "$RUN_DIR/submissions.log" | paste -sd, -)
  if [ -n "$JOBS" ] && [ -n "$(squeue -h -j "$JOBS" 2>/dev/null)" ]; then echo "REFUSED: jobs of $RUN_ID still active: $JOBS"; exit 2; fi
fi

# A3_DATASETS is always set explicitly, so an inherited value can never replace the task mapping.
EXPORT="ALL,RUN_ID=$RUN_ID,A3_CODE=$SNAP,A3_SCALE=$SCALE,A3_CASES=$RUN_DIR/cases.txt,A3_CASES_SHA256=$CASES_SHA256,A3_PROD_RUN=$PROD_RUN,A3_DATASETS=$DATASETS,A3_MANIFEST=$RUN_DIR/inputs_manifest.csv,A3_MANIFEST_SHA256=$MANIFEST_SHA256,A3_LIBMAN_SHA256=$LIBMAN_SHA256"
JOBNAME=A3_$MODE
CMD="sbatch --parsable --job-name=$JOBNAME --array=$ARRAY --time=$TIME --mem=$MEM --export=$EXPORT $SNAP/slurm/prod_A3.slurm"
TREE=$(sha256sum "$RUN_DIR/code_sha256.txt" | cut -d' ' -f1)

write_manifest() {   # $1 = job id ("pending", "dry-run" or the SLURM id)
  local tmp="$RUN_DIR/manifest.json.tmp.$$"
  {
    echo "{"
    echo "  \"run_id\": \"$RUN_ID\","
    echo "  \"piece\": \"A3 Horseshoe longer-chain sensitivity (PREREG_c050 R6), kind $MODE, scale $SCALE, $NCASES ess_tau-flagged fits of $PROD_RUN, budget 80000 + 120000 kept, thin 5 (8 x production)\","
    echo "  \"case_list\": \"$RUN_DIR/cases.txt\", \"case_list_sha256\": \"$CASES_SHA256\", \"production_reference_run\": \"$PROD_RUN\","
    echo "  \"scale_key\": \"$SCALE\","
    echo "  \"code_snapshot\": \"$SNAP\","
    echo "  \"code_files_sha256\": ["
    awk 'BEGIN{n=0} {a[n++]=$0} END{for(i=0;i<n;i++){split(a[i],f,"  "); printf "    {\"file\": \"%s\", \"sha256\": \"%s\"}%s\n", f[2], f[1], (i<n-1?",":"")}}' "$RUN_DIR/code_sha256.txt"
    echo "  ],"
    echo "  \"code_tree_sha256\": \"$TREE\","
    echo "  \"sbatch_command\": \"$CMD\","
    echo "  \"submit_host\": \"$(hostname)\","
    echo "  \"job_id\": \"$1\","
    echo "  \"array\": \"$ARRAY\","
    echo "  \"seeds\": \"method_seed = data_seed + 4000000 per dataset, from inputs_manifest.csv; data_seed = 1410000/1510000 + 10000 s + r\","
    echo "  \"modules\": \"GCC/14.3.0 R/4.5.2\","
    echo "  \"library\": \"$STUDY/lib/R452\","
    echo "  \"library_manifest\": \"$STUDY/lib/environment_manifest.txt\","
    echo "  \"library_manifest_sha256\": \"$LIBMAN_SHA256\","
    echo "  \"inputs\": \"$STUDY/inputs/p0500, $STUDY/inputs/p1000\","
    echo "  \"inputs_manifest_frozen\": \"$RUN_DIR/inputs_manifest.csv\","
    echo "  \"inputs_manifest_sha256\": \"$MANIFEST_SHA256\","
    echo "  \"outputs\": \"$STUDY/results/$RUN_ID\","
    echo "  \"logs\": \"$LOGDIR\","
    echo "  \"time\": \"$TIME\", \"mem\": \"$MEM\","
    echo "  \"written_utc\": \"$(date -u +%FT%TZ)\""
    echo "}"
  } > "$tmp"
  mv -f "$tmp" "$RUN_DIR/manifest.json"
}

if [ "$DRY" -eq 1 ]; then
  [ -z "$RESUME" ] && write_manifest "dry-run"
  echo "DRY RUN (nothing submitted): $RUN_ID"
  echo "$CMD"
  exit 0
fi
( set -o noclobber; echo "$(date -u +%FT%TZ) host $(hostname) pid $$ array $ARRAY" > "$RUN_DIR/submit.intent" ) 2>/dev/null \
  || { echo "REFUSED: unresolved submission intent $RUN_DIR/submit.intent (check squeue, then remove it)"; exit 2; }
if [ -z "$RESUME" ] || grep -q '"job_id": "dry-run"' "$RUN_DIR/manifest.json" 2>/dev/null; then write_manifest "pending"; fi
JOB=$($CMD) || { echo "sbatch failed or its outcome is unknown; intent left in place: $RUN_DIR/submit.intent"; exit 1; }
if [ -z "$RESUME" ] || grep -q '"job_id": "pending"' "$RUN_DIR/manifest.json"; then write_manifest "$JOB"; fi
echo "$(date -u +%FT%TZ)  host $(hostname)  job $JOB  array $ARRAY  mode $MODE  cmd: $CMD" >> "$RUN_DIR/submissions.log"
rm -f "$RUN_DIR/submit.intent"
echo "$RUN_ID $JOB"
