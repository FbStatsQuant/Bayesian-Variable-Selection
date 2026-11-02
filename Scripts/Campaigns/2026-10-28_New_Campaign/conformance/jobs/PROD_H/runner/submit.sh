#!/bin/bash
# submit.sh -- PROD-H primary submission (OPS runs it on NOTS, as fb31, through the configured `ssh nots` alias; it opens no ssh itself).
#   bash /home/fb31/projects/BVS/New_Campaign/runs/<STAMP>_prodH/runner/submit.sh [--dry-run] [--reuse-cache] [--throttle-p1000 N] [--throttle-p500 N]
# Submits ONE chain: precompile -> array p1000 (tasks 1-600) and array p500 (tasks 601-1200), both afterok the precompile.
#   1. nc_refuse_hooks: no test hook may reach a real submission.
#   2. guard_check.sh + the OPS guard.sh (charter section 2): refuses unless the guard enforces campaign <= 0.5 GiB / home <= 9.6 GiB and admits the planned add.
#   3. preconditions: staged files against STAGED_SHA256.txt; the frozen v2.2.1 tree against code/core/v2_2_1.SHA256SUMS (sha256sum -c, no unlisted
#      file except core/.cpp_cache); the tables; the read-only study; fresh scratch folders; no earlier launch of this run.
#   4. combined throttle of ALL queued ARRAY jobs of fb31, whatever their name (squeue) + this run's two arrays must be <= 100; fail closed.
#   5. launch record in RUN_DIR/launch/ (exact sbatch argument vectors, hashes, environment); config.env; then the submissions.
#      EVERY sbatch failure (or a bad job id, or a failed jobs.tsv/manifest write AFTER an accepted sbatch) aborts: the ids already submitted
#      (the accepted one included) are cancelled BY EXPLICIT ID, a cancel failure is recorded visibly, a SUBMISSION_ABORTED.txt is written,
#      exit status 5. A failed submission retires the run ID: stage a new STAMP. Every sbatch carries --qos=nots_commons (as the historical
#      production run); OPS confirms that this QoS exists for fb31 before launch (JOB.md). Execution logs (refusals, sbatch stderr) go to scratch.
# Exit: 0 submitted (or dry run ok) | 1 guard refused | 2 any other refusal | 5 abort after a partial submission.
set -euo pipefail
RUNNER_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
# shellcheck disable=SC1091
source "$RUNNER_DIR/common.sh"; source "$RUNNER_DIR/frozen_check.sh"
nc_refuse_hooks

DRY=0; REUSE=0; T1=30; T2=30   # HQ D49: 30 + 30 = 60 one-CPU tasks = 120 billed CPUs (NOTS bills 1 CPU as 2); campaign ceiling 192 billed (D47)
while (($#)); do
  case "$1" in
    --dry-run) DRY=1; shift ;;
    --reuse-cache) REUSE=1; shift ;;
    --throttle-p1000) T1=${2:-}; shift 2 ;;
    --throttle-p500) T2=${2:-}; shift 2 ;;
    *) echo "unknown option $1" >&2; exit 64 ;;
  esac
done
[[ $T1 =~ ^[0-9]+$ && $T2 =~ ^[0-9]+$ ]] && (( T1 >= 1 && T2 >= 1 && T1 + T2 <= 100 )) || nc_fail "throttles must be positive integers with p1000 + p500 <= 100"

# ---- run identity -----------------------------------------------------------------------------------------------
RUN_DIR_REAL=$(cd "$RUNNER_DIR/.." && pwd)
RUN_ID=$(basename "$RUN_DIR_REAL")
[[ $RUN_ID =~ ^[0-9]{8}T[0-9]{4}Z_prodH$ ]] || nc_fail "run folder '$RUN_ID' is not <STAMP>_prodH (STAMP = YYYYMMDDTHHMMZ)"
RUN_DIR="$HOME_ROOT/runs/$RUN_ID"
[ "$(cd "$RUN_DIR" && pwd)" = "$RUN_DIR_REAL" ] || nc_fail "this runner is not under $HOME_ROOT/runs/$RUN_ID"
CODE="$HOME_ROOT/code/core/v2_2_1"; SUMS="$HOME_ROOT/code/core/v2_2_1.SHA256SUMS"
LOGROOT="$SCR_ROOT/logs/$RUN_ID"; RES_RUN="$SCR_ROOT/results/$RUN_ID"
L500=6300; L1000=24000; KILL_MARGIN=300; MEM_GB=2; PLANNED_HOME_MB=30
refuse() { echo "$(nc_utc) REFUSED: $*" | tee -a "$(nc_refusal_log "$RUN_ID")" >&2; exit "${2:-2}"; }

mkdir -p -- "$SCR_ROOT/tmp"
TMPD=$(mktemp -d "$SCR_ROOT/tmp/submit.XXXXXX")
trap 'rm -rf -- "$TMPD"; rmdir "$SCR_ROOT/tmp" 2>/dev/null || true' EXIT
echo "== PROD-H submit $RUN_ID (dry-run=$DRY reuse-cache=$REUSE throttle p1000=$T1 p500=$T2)"

# ---- 0. once per run ---------------------------------------------------------------------------------------------
[ ! -e "$RUN_DIR/launch" ] && [ ! -e "$RUN_DIR/config.env" ] && [ ! -e "$RUN_DIR/jobs.tsv" ] || refuse "$RUN_ID was already launched (launch/, config.env or jobs.tsv exists); a run ID is used once"

# ---- 1. guard first ----------------------------------------------------------------------------------------------
echo "== guard_check.sh $PLANNED_HOME_MB"
if ! nc_run_guard "$PLANNED_HOME_MB" "$TMPD/guard_receipt.txt"; then
  refuse "the OPS guard does not enforce the charter limits or refused the planned add of ${PLANNED_HOME_MB} MB. Nothing was submitted." 1
fi

# ---- 2. preconditions --------------------------------------------------------------------------------------------
for f in tables/units.tsv tables/chunks.tsv STAGED_SHA256.txt OWNER runner/task.sh runner/precompile.sbatch runner/reconcile.py runner/env.sh \
         runner/common.sh runner/frozen_check.sh runner/guard_check.sh runner/nc_sched.py runner/poll.py runner/rerun.sh runner/p5_submit.sh runner/p5_task.sh \
         runner/p5_scan_run.sh runner/p5_scan.sbatch runner/cleanup_terminal.sh runner/make_manifests.sh runner/final_accounting.sh runner/accounting_summary.py; do
  [ -r "$RUN_DIR/$f" ] || refuse "missing staged file $RUN_DIR/$f"
done
grep -q "${RUN_ID%_prodH}" "$RUN_DIR/OWNER" || refuse "OWNER marker does not belong to this STAMP"
( cd "$HOME_ROOT" && sha256sum --quiet -c "runs/$RUN_ID/STAGED_SHA256.txt" ) || refuse "staged files do not match STAGED_SHA256.txt"
nc_check_frozen "$CODE" "$SUMS" 2>"$TMPD/frozen.txt" || refuse "the frozen v2.2.1 tree check failed: $(tr '\n' ' ' < "$TMPD/frozen.txt" | cut -c1-300)"
for f in "$CODE/study/run_case.R" "$CODE/study/adapter.R" "$CODE/tools/p5_scan.R" "$CODE/core/v3.R"; do [ -r "$f" ] || refuse "missing $f"; done
[ "$(grep -c . "$RUN_DIR/tables/units.tsv")" = 2401 ] && [ "$(grep -c . "$RUN_DIR/tables/chunks.tsv")" = 1201 ] || refuse "tables are not 2,400 units / 1,200 datasets"
awk -F'\t' 'NR > 1 { n++; if ($3 == 1000) { if ($1 < 1 || $1 > 600) bad++ } else if ($3 == 500) { if ($1 < 601 || $1 > 1200) bad++ } else bad++
                     split($4, s, ","); if (s[1] != "c100" || s[2] != "c050" || length(s) != 2) bad++ }
        END { exit !(n == 1200 && !bad) }' "$RUN_DIR/tables/chunks.tsv" || refuse "chunks.tsv: tasks must be p1000 = 1-600, p500 = 601-1200, scales c100,c050"
[ -r "$STUDY/manifests/inputs_manifest.csv" ] || refuse "the study manifest $STUDY/manifests/inputs_manifest.csv is not readable"
for p in 0500 1000; do
  n=$(find "$STUDY/inputs/p$p" -maxdepth 1 -name "p${p}_S?_r???.rds" 2>/dev/null | wc -l)
  [ "$n" = 600 ] || refuse "expected 600 input files under $STUDY/inputs/p$p, found $n"
done
[ ! -e "$LOGROOT" ] && [ ! -e "$RES_RUN" ] || refuse "scratch folders of $RUN_ID already exist ($LOGROOT or $RES_RUN)"
if [ -e "$CODE/core/.cpp_cache" ] && [ $REUSE = 0 ]; then
  refuse "$CODE/core/.cpp_cache already exists; the run must build a fresh cache. Use --reuse-cache only on HQ's instruction (the precompile job still runs and records the .so hashes)"
fi

# ---- 3. walltimes (GO_2400 C1) ------------------------------------------------------------------------------------
# task wall = 2 fits x (L + 300 s hard-limit margin + 60 s KILL grace) + 600 s once per task (module load, frozen check, hashing, accounting)
walltime() { local s=$(( 2 * ($1 + KILL_MARGIN + 60) + 600 )); printf '%d:%02d:00' $(( (s + 59) / 3600 )) $(( ((s + 59) % 3600) / 60 )); }
W500=$(walltime $L500); W1000=$(walltime $L1000)
[ "$W500" = "3:52:00" ] && [ "$W1000" = "13:42:00" ] || refuse "walltime formula gave $W500 / $W1000, expected 3:52:00 / 13:42:00"
W500=03:52:00; W1000=13:42:00

# ---- 4. combined throttle (fail closed) -----------------------------------------------------------------------------
check_throttle() {   # check_throttle N : existing queued campaign SMC arrays + N <= 100
  local now
  now=$(nc_campaign_throttle 2>"$TMPD/throttle_now.txt") || { echo "could not determine the queued campaign arrays (squeue failed or unparsable)" >&2; return 1; }
  [[ $now =~ ^[0-9]+$ ]] || return 1
  THROTTLE_NOW=$now
  (( now + $1 <= 100 )) || { echo "combined throttle $now + $1 > 100 over all queued campaign SMC arrays of $NC_USER" >&2; return 1; }
  return 0
}
check_throttle $((T1 + T2)) || refuse "combined throttle check failed: $(cat "$TMPD/throttle_now.txt" 2>/dev/null | tr '\n' ';' | cut -c1-400)"

# ---- 5. argument vectors ----------------------------------------------------------------------------------------------
COMMON=(--parsable --account=commons --partition=commons --qos=nots_commons --nodes=1 --ntasks=1 --constraint=sapphirerapids --export=NONE --no-requeue --chdir="$LOGROOT")
pre_args() { PRE_ARGS=("${COMMON[@]}" --job-name="smcbvs_${RUN_ID}_precompile" --cpus-per-task=1 --mem=4G --time=01:00:00
                       --output="$LOGROOT/slurm/%j.out" --error="$LOGROOT/slurm/%j.err" "$RUN_DIR/runner/precompile.sbatch" "$RUN_DIR"); }
arr_args() { # arr_args NAME ARRAYSPEC WALL DEPID -> ARR_ARGS
  ARR_ARGS=("${COMMON[@]}" --job-name="smcbvs_${RUN_ID}_$1" --cpus-per-task=1 --mem=2G --time="$3" --array="$2"
            --dependency="afterok:$4" --kill-on-invalid-dep=yes
            --output="$LOGROOT/slurm/%A_%a.out" --error="$LOGROOT/slurm/%A_%a.err" "$RUN_DIR/runner/task.sh" "$RUN_DIR"); }
if [ $DRY = 1 ]; then
  pre_args; printf 'DRY-RUN sbatch'; printf ' %q' "${PRE_ARGS[@]}"; echo
  arr_args p1000 "1-600%$T1" "$W1000" "<PRECOMPILE_ID>"; printf 'DRY-RUN sbatch'; printf ' %q' "${ARR_ARGS[@]}"; echo
  arr_args p500 "601-1200%$T2" "$W500" "<PRECOMPILE_ID>"; printf 'DRY-RUN sbatch'; printf ' %q' "${ARR_ARGS[@]}"; echo
  echo "== dry run complete: guard, preconditions and throttle passed; nothing was created or submitted"
  exit 0
fi

# ---- 6. launch record --------------------------------------------------------------------------------------------------
mkdir "$RUN_DIR/launch" || refuse "cannot create $RUN_DIR/launch"
LAUNCH=$RUN_DIR/launch
mkdir -p -- "$LOGROOT/slurm" "$LOGROOT/submit" "$RES_RUN"
cp "$TMPD/guard_receipt.txt" "$LAUNCH/guard_receipt.txt"
cp "$SUMS" "$LAUNCH/v2_2_1.SHA256SUMS"
{ echo "frozen v2.2.1 tree OK against $SUMS at $(nc_utc)"; echo "v2_2_1.SHA256SUMS sha256 $(sha256sum "$SUMS" | cut -d' ' -f1) ($(grep -c . "$SUMS") files)"
  echo "inputs_manifest.csv sha256 $(sha256sum "$STUDY/manifests/inputs_manifest.csv" | cut -d' ' -f1)"; } > "$LAUNCH/frozen_check.txt"
cp "$RUN_DIR/STAGED_SHA256.txt" "$LAUNCH/STAGED_SHA256.txt"
cp "$TMPD/throttle_now.txt" "$LAUNCH/throttle_before.txt"; echo "existing_combined_throttle $THROTTLE_NOW; planned p1000 $T1 + p500 $T2" >> "$LAUNCH/throttle_before.txt"
{ echo "# effective environment of the submission $(nc_utc) by $(id -un)@$(hostname)"
  echo "RUN_ID=$RUN_ID"; echo "HOME_ROOT=$HOME_ROOT"; echo "SCR_ROOT=$SCR_ROOT"; echo "GUARD=$GUARD"; echo "STUDY=$STUDY"; echo "CODE=$CODE"
  echo "L500=$L500 L1000=$L1000 KILL_MARGIN=$KILL_MARGIN MEM_GB=$MEM_GB wall_p500=$W500 wall_p1000=$W1000 throttle_p1000=$T1 throttle_p500=$T2 reuse_cache=$REUSE"
  for v in NC_LOCAL_TEST NC_STUB_BIN NC_HOME_ROOT NC_SCR_ROOT; do echo "$v=[${!v:-}]"; done; } > "$LAUNCH/effective_env.txt"
squeue -h -u "$NC_USER" -o "%i|%j|%T" > "$LAUNCH/squeue_before.txt" 2>&1 || true
: > "$LAUNCH/sbatch_args.txt"
cat > "$RUN_DIR/config.env" <<EOF
RUN_ID=$RUN_ID
HOME_ROOT=$HOME_ROOT
CODE=$CODE
SUMS=$SUMS
STUDY=$STUDY
OUTROOT=$SCR_ROOT
LOGROOT=$LOGROOT
MEM_GB=$MEM_GB
L500=$L500
L1000=$L1000
KILL_MARGIN=$KILL_MARGIN
RUNNER=$RUN_DIR/runner
RUN_DIR=$RUN_DIR
EOF
cp "$RUN_DIR/tables/units.tsv" "$RUN_DIR/tables/chunks.tsv" "$RUN_DIR/"
chmod a-w "$RUN_DIR/config.env" "$RUN_DIR/units.tsv" "$RUN_DIR/chunks.tsv"
cp "$RUN_DIR/config.env" "$LAUNCH/config.env"
printf 'job\tkind\tsubmitted_utc\tarray\tunits\n' > "$RUN_DIR/jobs.tsv"

# ---- 7. submission with abort-and-cancel -------------------------------------------------------------------------------------
SUBMITTED=(); SUBMITTED_ID=""
abort_submission() {   # abort_submission REASON : cancel what was submitted (explicit ids only), record, exit 5
  local reason=$1 id cancel_failed=""
  echo "SUBMISSION ABORTED: $reason" >&2
  { echo "aborted $(nc_utc): $reason"; echo "ids submitted before the failure: ${SUBMITTED[*]:-none}"; } >> "$LAUNCH/SUBMISSION_ABORTED.txt" 2>/dev/null || true
  for id in "${SUBMITTED[@]:-}"; do
    [ -n "$id" ] || continue
    nc_cancel_id "$id" "$LAUNCH/SUBMISSION_ABORTED.txt" || cancel_failed=1
  done
  echo "this run ID is retired; stage a new STAMP${cancel_failed:+ (AT LEAST ONE CANCEL FAILED: see above)}" >> "$LAUNCH/SUBMISSION_ABORTED.txt" 2>/dev/null || true
  exit 5
}
submit() {   # submit STEP KIND ARRAY UNITS ARGS... -> sets SUBMITTED_ID (no command substitution: failures must stop the driver)
  local step=$1 kind=$2 arr=$3 units=$4 out rc=0 id; shift 4
  { printf '%s\t' "$step"; printf '%q ' "$@"; echo; } >> "$LAUNCH/sbatch_args.txt" || abort_submission "cannot record the sbatch vector of $step (ids submitted earlier are cancelled)"
  out=$(sbatch "$@" 2>"$LOGROOT/submit/sbatch_$step.err") || rc=$?
  [ $rc = 0 ] || abort_submission "sbatch failed for $step (exit $rc): $(head -c 300 "$LOGROOT/submit/sbatch_$step.err" | tr '\n' ' ')"
  id=${out%%;*}
  [[ "$id" =~ ^[0-9]+$ ]] || abort_submission "sbatch returned an invalid job id '$out' for $step"
  SUBMITTED+=("$id"); SUBMITTED_ID=$id          # from here on the job is accepted: ANY failure below cancels it by this explicit id
  printf '%s\t%s\t%s\t%s\t%s\n' "$id" "$kind" "$(nc_utc)" "$arr" "$units" >> "$RUN_DIR/jobs.tsv" \
    || abort_submission "the job $id ($step) was accepted but recording it in jobs.tsv failed"
}
pre_args; submit precompile precompile - 1 "${PRE_ARGS[@]}";                                   J_PRE=$SUBMITTED_ID
check_throttle "$T1" || abort_submission "combined throttle exceeded before the p1000 array"
arr_args p1000 "1-600%$T1" "$W1000" "$J_PRE"; submit p1000 primary_p1000 "1-600%$T1" 1200 "${ARR_ARGS[@]}";    J_P1000=$SUBMITTED_ID
check_throttle "$T2" || abort_submission "combined throttle exceeded before the p500 array"
arr_args p500 "601-1200%$T2" "$W500" "$J_PRE"; submit p500 primary_p500 "601-1200%$T2" 1200 "${ARR_ARGS[@]}";   J_P500=$SUBMITTED_ID

# ---- 8. manifest.json (launch hashes) --------------------------------------------------------------------------------------
PY=$(nc_python)
if ! "$PY" - "$RUN_DIR" "$J_PRE" "$J_P1000" "$J_P500" "$T1" "$T2" "$W1000" "$W500" "$LAUNCH/sbatch_args.txt" <<'PYEOF'
import hashlib, json, os, socket, sys
from datetime import datetime, timezone
run_dir, pre, p1000, p500, t1, t2, w1000, w500, args_file = sys.argv[1:10]
cfg = dict(l.split("=", 1) for l in open(os.path.join(run_dir, "config.env")).read().split())
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
runner = cfg["RUNNER"]
m = dict(run_id=cfg["RUN_ID"], submitted_utc=datetime.now(timezone.utc).isoformat(), host=socket.gethostname(),
         jobs=dict(precompile=pre, primary_p1000=p1000, primary_p500=p500),
         throttle=dict(p1000=int(t1), p500=int(t2)), task_wall=dict(p1000=w1000, p500=w500),
         constraint="sapphirerapids", config=cfg, sbatch_args_file=args_file,
         code_manifest_sha256=sha(cfg["SUMS"]), inputs_manifest_sha256=sha(os.path.join(cfg["STUDY"], "manifests", "inputs_manifest.csv")),
         runner_sha256={f: sha(os.path.join(runner, f)) for f in sorted(os.listdir(runner)) if os.path.isfile(os.path.join(runner, f))},
         chunks_sha256=sha(os.path.join(run_dir, "chunks.tsv")), units_sha256=sha(os.path.join(run_dir, "units.tsv")),
         seeds="method seed = data seed + 4,000,000; derived per dataset ID by the adapter (never passed)",
         modules="GCC/14.3.0 R/4.5.2 (runner/env.sh)")
json.dump(m, open(os.path.join(run_dir, "manifest.json"), "w"), indent=2)
PYEOF
then abort_submission "writing manifest.json failed"; fi
squeue -h -u "$NC_USER" -o "%i|%j|%T" > "$LAUNCH/squeue_after.txt" 2>&1 || true
chmod a-w "$RUN_DIR/manifest.json" 2>/dev/null || true   # jobs.tsv stays writable: rerun.sh and p5_submit.sh append to it

cat <<EOF

== submitted: precompile $J_PRE | p1000 array $J_P1000 (tasks 1-600, %$T1, wall $W1000) | p500 array $J_P500 (tasks 601-1200, %$T2, wall $W500)
== run id:  $RUN_ID        launch record: $LAUNCH        job ids: $RUN_DIR/jobs.tsv
== OPS next: poll every ~10 minutes (one ssh connection per poll):  $PY $RUN_DIR/runner/poll.py $RUN_DIR
== after both primary arrays are terminal: reconcile, then p5_submit.sh (see JOB.md)
EOF
