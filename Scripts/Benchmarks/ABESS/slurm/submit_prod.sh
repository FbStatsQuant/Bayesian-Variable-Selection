#!/usr/bin/env bash
# submit_prod.sh (c050 copy, BRIEF_C050_ENG): freeze the F5 code copy, the 12 input cell manifests and
# the library contract into a read-only snapshot with manifest.json, verify it, and submit from the
# snapshot (PROD_READINESS_BRIEF §2; Astra prod findings 3-5, 7).
#   slurm/submit_prod.sh --mode prod --time T --mem M [--array SPEC] [--dry-run]
#                production, scale c050, 400 tasks x 3 datasets (default array 1-400%133)
#   slurm/submit_prod.sh --mode check [--time T] [--mem M] [--dry-run]
#                c100 reproduction: task 301 = p1000_S4_r001-r003, then a dependent job compares the
#                outputs with the c = 1 production run (c050tools/compare_c050check.R)
#   slurm/submit_prod.sh --mode pilot [--time T] [--mem M] [--dry-run]
#                c050 pilot: the 12 datasets r001, one per task (C050_IDS), then a dependent job writes
#                the diagnostics summary (c050tools/pilot_diag_c050.R)
#   slurm/submit_prod.sh --resume RUN_ID --array SPEC [--time T] [--mem M] [--dry-run]
#   --dry-run  do everything except sbatch (a new snapshot and manifest are still written)
#   --resume   resubmit tasks of an existing run from its own snapshot (G8 retry of
#              infrastructure failures; completed cases are skipped by the runner). No new
#              snapshot: code, manifests and library are re-verified against the run's records.
set -euo pipefail
SRC=/home/fb31/projects/BVS/Benchmarks/F5_ABESS/c050
B=/projects/ml75/fb31/BVS/bench20261019
LIB=$B/lib/R452; LIBM=$B/lib/environment_manifest.txt
LOGS=$B/logs/prod/F5_ABESS
REF_RUN=20261019T2157Z_bench20261019_prod_F5_ABESS             # c = 1 production run (reference for check)
PILOT_IDS=p0500_S1_r001:p0500_S2_r001:p0500_S3_r001:p0500_S4_r001:p0500_S5_r001:p0500_S6_r001:p1000_S1_r001:p1000_S2_r001:p1000_S3_r001:p1000_S4_r001:p1000_S5_r001:p1000_S6_r001
FILES="config.R common.R methods/fit_F5_abess.R run_case.R run_task.R validate_outputs.R score_dev.R tools/compare_runs.R tools/conditioning_diag.R slurm/env.sh slurm/prod_F5.slurm slurm/submit_prod.sh c050tools/compare_c050check.R c050tools/pilot_diag_c050.R"
TIME=""; MEM=""; ARRAY=""; DRY=0; MODE=; RESUME=; ARRAY_SET=0
while [ $# -gt 0 ]; do case "$1" in
  --dry-run) DRY=1; shift;; --mode) MODE=${2:?}; shift 2;;
  --array) ARRAY=${2:?}; ARRAY_SET=1; shift 2;; --time) TIME=${2:?}; shift 2;; --mem) MEM=${2:?}; shift 2;;
  --resume) RESUME=${2:?}; shift 2;;
  *) echo "usage: see header of $0" >&2; exit 2;; esac; done
if [ -n "$RESUME" ]; then
  case "$RESUME" in *_prodc050_*) MODE=prod;; *_c050check_*) MODE=check;; *_pilotc050_*) MODE=pilot;;
    *) echo "not a c050 run id: $RESUME" >&2; exit 2;; esac
fi
case "$MODE" in
  prod)  SCALE=c050; IDS=; LABEL=prodc050; ARRAY=${ARRAY:-1-400%133}
         [ -n "$RESUME" ] || { [ -n "$TIME" ] && [ -n "$MEM" ]; } || { echo "--mode prod needs --time and --mem (from the pilot)" >&2; exit 2; }
         TASKMAP="t<=200: p=500, else p=1000; u=(t-1)%200; datasets i=3u..3u+2 of the scenario-major order: scenario=i%/%100+1, replicate=i%%100+1; scale c050" ;;
  check) SCALE=c100; IDS=; LABEL=c050check; ARRAY=${ARRAY:-301}
         TASKMAP="production map, task 301 = p1000_S4_r001-r003; scale c100" ;;
  pilot) SCALE=c050; IDS=$PILOT_IDS; LABEL=pilotc050; ARRAY=${ARRAY:-1-12}
         TASKMAP="task t runs the t-th of $PILOT_IDS; scale c050" ;;
  *) echo "--mode prod|check|pilot is required" >&2; exit 2 ;;
esac
TIME=${TIME:-00:30:00}; MEM=${MEM:-2G}                          # check/pilot defaults = the c = 1 per-task values
libtree() { (cd "$LIB" && find . -type f -print0 | LC_ALL=C sort -z | xargs -0 sha256sum | sha256sum | cut -d' ' -f1); }
mkdir -p "$B/runs" "$LOGS"

if [ -n "$RESUME" ]; then
  # ---- resubmission into an existing run, from its own snapshot ----
  [ "$ARRAY_SET" = 1 ] || { echo "--resume needs an explicit --array" >&2; exit 2; }
  RID=$RESUME; RUN=$B/runs/$RID; SNAP=$RUN/code; ONLY=
  [ -f "$RUN/manifest.json" ] || { echo "no run $RUN" >&2; exit 1; }
  (cd "$SNAP" && sha256sum -c --quiet ../code.sha256) || { echo "snapshot verification failed" >&2; exit 3; }
  (cd "$RUN/input_manifests" && sha256sum -c --quiet ../input_manifests.sha256) || { echo "input manifests changed" >&2; exit 3; }
  TREE=$(sha256sum "$RUN/code.sha256" | cut -d' ' -f1); IMH=$(sha256sum "$RUN/input_manifests.sha256" | cut -d' ' -f1)
  LIBH=$(sha256sum "$LIBM" | cut -d' ' -f1); LIBTREE=$(libtree)
  python3 - "$RUN/manifest.json" "$TREE" "$IMH" "$LIBH" "$LIBTREE" <<'PY'
import json, sys
d = json.load(open(sys.argv[1]))
want = [d["code_tree_sha256"], d["input_manifests_tree_sha256"], d["library_manifest_sha256"], d["library_tree_sha256"]]
if want != sys.argv[2:6]: sys.exit("run records do not match the current snapshot, manifests or library")
PY
else
  # ---- new run: reserve, freeze, verify ----
  TS=$(date -u +%Y%m%dT%H%MZ)
  RID=${TS}_bench20261019_${LABEL}_F5_ABESS; ONLY=
  RUN=$B/runs/$RID; SNAP=$RUN/code
  [ -e "$B/results/$RID" ] && { echo "refusing: results/$RID exists" >&2; exit 1; }
  # Exclusive reservation of the run id: plain mkdir fails if another submission holds it.
  mkdir "$RUN" || { echo "refusing: $RUN exists (another submission in the same minute?)" >&2; exit 1; }
  for f in $FILES; do [ -f "$SRC/$f" ] || { echo "missing $SRC/$f" >&2; exit 1; }; done
  mkdir "$SNAP" "$RUN/input_manifests"
  (cd "$SRC" && cp --parents $FILES "$SNAP/")
  (cd "$SNAP" && sha256sum $FILES > ../code.sha256)
  # Frozen copies of the 12 input cell manifests; tasks read these, not the live ones.
  for p in p0500 p1000; do for s in 1 2 3 4 5 6; do
    cp "$B/manifests/cells/${p}_S${s}_inputs.csv" "$RUN/input_manifests/"; done; done
  (cd "$RUN/input_manifests" && sha256sum *.csv > ../input_manifests.sha256)
  [ "$(ls "$RUN/input_manifests" | wc -l)" = 12 ] || { echo "expected 12 cell manifests" >&2; exit 3; }
  chmod -R a-w "$SNAP" "$RUN/input_manifests"
  # Verify: the snapshot matches its hash list and the source folder file by file.
  (cd "$SNAP" && sha256sum -c --quiet ../code.sha256) || { echo "snapshot verification failed" >&2; exit 3; }
  (cd "$SRC" && sha256sum -c --quiet "$RUN/code.sha256") || { echo "snapshot differs from source" >&2; exit 3; }
  TREE=$(sha256sum "$RUN/code.sha256" | cut -d' ' -f1)
  IMH=$(sha256sum "$RUN/input_manifests.sha256" | cut -d' ' -f1)
  LIBH=$(sha256sum "$LIBM" | cut -d' ' -f1)
  LIBTREE=$(libtree)    # hash of every installed library file; each task recomputes it
fi
STATUS=$LOGS/status/$RID
# With --export=ALL the submitting environment takes precedence over assignments written in
# --export, so the F5_* and C050_* variables are set here, in the script's own environment, which
# overrides anything inherited from the caller's shell (Astra prod follow-up, point 3).
export F5_TREE=$TREE F5_IMH=$IMH F5_LIBH=$LIBH F5_LIBTREE=$LIBTREE F5_ONLY=$ONLY C050_SCALE=$SCALE C050_IDS=$IDS
CMD="sbatch --parsable --array=$ARRAY --time=$TIME --mem=$MEM --output=$LOGS/%x_%A_%a.out --error=$LOGS/%x_%A_%a.err --export=ALL $SNAP/slurm/prod_F5.slurm $SNAP $RID"
ENVDESC="F5_TREE=$TREE F5_IMH=$IMH F5_LIBH=$LIBH F5_LIBTREE=$LIBTREE F5_ONLY=$ONLY C050_SCALE=$SCALE C050_IDS=$IDS"
case "$MODE" in
  check) POST="Rscript --vanilla $SNAP/c050tools/compare_c050check.R $B/results/$RID $B/results/$REF_RUN p1000_S4_r001,p1000_S4_r002,p1000_S4_r003 F5 $B/results/$RID/c050check_compare.txt" ;;
  pilot) POST="Rscript --vanilla $SNAP/c050tools/pilot_diag_c050.R $B/results/$RID ${IDS//:/,} F5 c050 100 $B/results/$RID/pilotc050_diag.txt" ;;
  *) POST="" ;;
esac
[ -n "$RESUME" ] && POST=""

write_manifest() {   # new runs only; $1 = status, $2 = job id, $3 = post job id; atomic: temp file, then rename
  python3 - "$RUN/manifest.json" "$1" "$2" "$3" <<PY
import json, os, sys
path, status, job, pjob = sys.argv[1:5]
files = dict((l.split(None, 1)[1].strip(), l.split(None, 1)[0]) for l in open("$RUN/code.sha256"))
mans = dict((l.split(None, 1)[1].strip(), l.split(None, 1)[0]) for l in open("$RUN/input_manifests.sha256"))
d = {"run_id": "$RID", "piece": "F5 (ABESS), c050 copy, mode $MODE (scale $SCALE)",
  "mode": "$MODE", "scale_key": "$SCALE", "dry_run": "$DRY" == "1",
  "code_source": "$SRC (copy of the c = 1 snapshot $B/runs/$REF_RUN/code; diff in $SRC/C050_DIFF.txt)",
  "code_dir": "$SNAP", "code_files_sha256": files, "code_tree_sha256": "$TREE",
  "input_manifests_dir": "$RUN/input_manifests", "input_manifests_sha256": mans,
  "input_manifests_tree_sha256": "$IMH",
  "command": "$ENVDESC $CMD", "post_job": ("afterany dependent job: $POST" if "$POST" else ""),
  "host": "$(hostname)", "prepared_utc": "$(date -u +%FT%TZ)",
  "tasks": "$ARRAY", "time": "$TIME", "mem": "$MEM", "cpus": 1, "partition": "commons",
  "task_map": "$TASKMAP",
  "seeds": "method_seed = data_seed + 4000000 (checked against the frozen cell manifest); abess internal seed 1",
  "modules": "GCC/14.3.0 R/4.5.2", "library": "$LIB", "library_tree_sha256": "$LIBTREE",
  "library_manifest": "$LIBM", "library_manifest_sha256": "$LIBH",
  "inputs": "$B/inputs/p{0500,1000}/p{pppp}_S{s}_r{rrr}.rds",
  "outputs": "$B/results/$RID", "logs": "$LOGS", "status_dir": "$STATUS",
  "status": status, "job_id": job, "post_job_id": pjob}
tmp = path + ".tmp"; json.dump(d, open(tmp, "w"), indent=1); os.replace(tmp, path)
PY
}
log_submission() {   # every submission (first or resumed) is appended to submissions.log
  printf '%s\t%s\t%s\t%s %s\n' "$(date -u +%FT%TZ)" "$1" "$ARRAY" "$ENVDESC" "$CMD" >> "$RUN/submissions.log"
}
echo "run_id $RID"; echo "snapshot $SNAP (tree $TREE)"; echo "command: $ENVDESC $CMD"; [ -n "$POST" ] && echo "post (afterany): $POST"
if [ "$DRY" = 1 ]; then [ -z "$RESUME" ] && write_manifest dry_run "" ""; echo "dry run: not submitted"; exit 0; fi
# Submission intent first: if the next step is interrupted, check squeue/sacct for this run
# id before submitting again.
[ -z "$RESUME" ] && write_manifest submitting "" ""
date -u +%FT%TZ > "$RUN/SUBMIT_INTENT"; log_submission intent
# Scheduler receipt goes straight to files (stdout and stderr separately), then is validated.
N=$(date -u +%Y%m%dT%H%M%SZ)
if ! $CMD > "$RUN/sbatch_$N.stdout" 2> "$RUN/sbatch_$N.stderr"; then
  log_submission "sbatch_failed"; [ -z "$RESUME" ] && write_manifest sbatch_failed "" ""
  echo "sbatch failed; see $RUN/sbatch_$N.stderr" >&2; exit 4; fi
JID=$(cut -d';' -f1 "$RUN/sbatch_$N.stdout" | tr -d '[:space:]')
[[ "$JID" =~ ^[0-9]+$ ]] || { log_submission "unparsed receipt"; echo "could not parse job id; check squeue before resubmitting" >&2; exit 5; }
log_submission "job $JID"
PJID=""
if [ -n "$POST" ]; then
  PJID=$(sbatch --parsable --dependency=afterany:$JID --job-name=F5_c050post --partition=commons --time=00:15:00 --mem=2G \
    --output=$LOGS/%x_%j.out --wrap "bash -c 'source $SNAP/slurm/env.sh && $POST'") || PJID="sbatch failed"
  log_submission "post job $PJID"
fi
[ -z "$RESUME" ] && write_manifest submitted "$JID" "$PJID"
echo "submitted job $JID post $PJID"
