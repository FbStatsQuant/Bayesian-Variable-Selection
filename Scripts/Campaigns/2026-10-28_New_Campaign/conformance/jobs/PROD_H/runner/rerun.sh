#!/usr/bin/env bash
# rerun.sh -- rerun infrastructure failures ONLY, once, with the same seed, run ID and native allocation (GO_2400 C4; GO_2400 C3/C5).
# NOTS login node (OPS).  Usage: bash RUN_DIR/runner/rerun.sh [--dry-run]
# What may be rerun (reconcile classes): `infra` (attempted once, no .done, not a timeout: node failure, OOM-kill outside the fit,
# missing outputs with no native status, exit 1) and `orphan` (its task died before reaching it: a FIRST attempt). Never rerun: done (including
# native resource_limit, which only P5 may redo), timeout (Slurm TIMEOUT or the unit hard kill: reported and held), infra_repeat (second
# failure: reported to HQ), running, rerun_queued, not_run, pulled.
#  0. refuse test hooks; guard; the frozen v2.2.1 tree; the compile cache READY (a rerun never compiles)
#  1. refuse while ANY job of this run (precompile, primary arrays, earlier reruns, P5) is queued, running or held (no double queueing)
#  2. combined throttle: the rerun array adds %10 to ALL queued array jobs of fb31 (any name) and must keep them <= 100 (fail closed)
#  3. reconcile.py --sacct --clear-stale-locks (a dry run clears nothing)
#  4. select infra + orphan units whose lock is gone; ONE array over their global task indices with a units file (task.sh runs only the
#     listed, eligible units), --no-requeue, %10, the original constraint, account and partition; wall = the p1000 wall if a selected unit is p1000
#     else the p500 wall; --mem 4G only if a selected unit's step ended OUT_OF_MEMORY (native --mem-gb stays 2, so unit identity is unchanged)
#  5. append the job to RUN_DIR/jobs.tsv as rerun_N; the exact sbatch vector goes to RUN_DIR/rerun_N/sbatch_args.txt. Every sbatch carries --qos=nots_commons
#     (OPS confirms the QoS exists, JOB.md). A failed jobs.tsv/submitted.json write AFTER the accepted sbatch cancels the job by its explicit id
#     (abort_rerun, exit 5, rerun_N/ABORTED.txt; a cancel failure is recorded visibly). sbatch stderr goes to LOGROOT/submit/ (scratch).
set -euo pipefail
RUNNER_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
source "$RUNNER_DIR/common.sh"; source "$RUNNER_DIR/frozen_check.sh"
nc_refuse_hooks
[[ $# == 0 || ( $# == 1 && $1 == --dry-run ) ]] || { echo "usage: rerun.sh [--dry-run]" >&2; exit 64; }
DRY=${1:-}
RUN_DIR="$HOME_ROOT/runs/$(basename "$(cd "$RUNNER_DIR/.." && pwd)")"
nc_load_run "$RUN_DIR"
PY=$(nc_python)
mkdir -p -- "$SCR_ROOT/tmp"; TMPD=$(mktemp -d "$SCR_ROOT/tmp/rerun.XXXXXX"); trap 'rm -rf -- "$TMPD"; rmdir "$SCR_ROOT/tmp" 2>/dev/null || true' EXIT

for u in "$RUN_DIR"/rerun_*/UNCERTAIN; do   # R3-1: an aborted rerun whose job is not proven terminal (squeue AND sacct) may still write: no further rerun
  [[ -e $u ]] || continue; nc_clear_uncertain "$u" || nc_fail "an aborted rerun job ($u) is not proven terminal: no new rerun is submitted"; done
nc_check_frozen "$CODE" "$SUMS" || nc_fail "the frozen v2.2.1 tree check failed"
nc_cache_ready "$CODE" "$RUN_DIR" || nc_fail "the compile cache is not READY"
if ! nc_run_guard 5 "$TMPD/guard_receipt.txt"; then NC_RC=1 nc_fail "the OPS guard refused or does not enforce the charter limits"; fi
live=$(nc_live_jobs "$RUN_DIR") || nc_fail "squeue failed"
[[ -z $live ]] || nc_fail "job(s) of this run still queued, running or held: $(echo $live): wait for them"
now=$(nc_campaign_throttle 2>"$TMPD/throttle.txt") || nc_fail "could not determine the queued campaign arrays (fail closed)"
(( now + 10 <= 100 )) || nc_fail "combined throttle $now + 10 > 100 over all queued arrays of fb31"

if [[ $DRY == --dry-run ]]; then "$PY" "$RUNNER/reconcile.py" "$RUN_DIR" --sacct >/dev/null
else "$PY" "$RUNNER/reconcile.py" "$RUN_DIR" --sacct --clear-stale-locks >/dev/null; fi
sel=$(awk -F'\t' 'NR == 1 { for (i = 1; i <= NF; i++) c[$i] = i; next }
                  ($c["klass"] == "infra" || $c["klass"] == "orphan") && $c["lock_present"] == "false" {
                    print $c["case_id"] "\t" $c["task"] "\t" $c["klass"] "\t" $c["step_state"] "\t" $c["p"] }' "$RUN_DIR/reconcile.tsv")
blocked=$(awk -F'\t' 'NR == 1 { for (i = 1; i <= NF; i++) c[$i] = i; next }
                      ($c["klass"] == "infra" || $c["klass"] == "orphan") && $c["lock_present"] == "true" { print $c["case_id"] }' "$RUN_DIR/reconcile.tsv")
[[ -z $blocked ]] || echo "WARNING: lock still present, not rerun (inspect by hand): $blocked" >&2
if [[ -z $sel ]]; then echo '{"rerun": 0, "reason": "no infra or orphan units"}'; exit 0; fi
tasks=$(cut -f2 <<< "$sel" | sort -n -u | paste -sd, -)
mem=2G; grep -q $'\tOUT_OF_MEMORY\t' <<< "$sel" && mem=4G
wall=03:52:00; grep -q $'\t1000$' <<< "$sel" && wall=13:42:00
n=1; while [[ -e $RUN_DIR/rerun_$n ]]; do n=$((n + 1)); done
echo "rerun_$n: $(wc -l <<< "$sel") units ($(grep -c $'\torphan\t' <<< "$sel" || true) orphan), tasks $tasks, mem $mem, wall $wall"
[[ $DRY == --dry-run ]] && { echo "$sel"; exit 0; }
R=$RUN_DIR/rerun_$n
mkdir "$R"
cut -f1 <<< "$sel" > "$R/units.txt"
printf '%s\n' "$sel" > "$R/selected.tsv"
cp "$RUN_DIR/reconcile.tsv" "$R/reconcile_before.tsv"
args=(--parsable --job-name="smcbvs_${RUN_ID}_rerun$n" --account=commons --partition=commons --qos=nots_commons --nodes=1 --ntasks=1 --cpus-per-task=1
      --mem="$mem" --time="$wall" --constraint=sapphirerapids --export=NONE --no-requeue --chdir="$LOGROOT"
      --array="$tasks%10" --output="$LOGROOT/slurm/%A_%a.out" --error="$LOGROOT/slurm/%A_%a.err" "$RUNNER/task.sh" "$RUN_DIR" "$R/units.txt")
{ printf 'sbatch'; printf ' %q' "${args[@]}"; echo; } > "$R/sbatch_args.txt"
mkdir -p -- "$LOGROOT/submit"; SBERR=$LOGROOT/submit/rerun${n}_sbatch.err
rc=0; job=$(sbatch "${args[@]}" 2>"$SBERR") || rc=$?
if [[ $rc != 0 ]]; then echo "rerun sbatch failed (exit $rc): $(head -c 300 "$SBERR" | tr '\n' ' ')" >&2; mv "$R" "$R.sbatch_failed"; exit 5; fi
job=${job%%;*}
[[ $job =~ ^[0-9]+$ ]] || { echo "rerun sbatch returned an invalid job id '$job'" >&2; mv "$R" "$R.bad_id"; exit 5; }
# From here on the job is ACCEPTED: any failure of the records below cancels it by this explicit id (R2-7); a cancel failure is recorded visibly.
abort_rerun() {
  echo "RERUN ABORTED: $1" >&2
  { echo "aborted $(nc_utc): $1"; echo "accepted job: $job"; } >> "$R/ABORTED.txt" 2>/dev/null || true
  nc_abort_accepted "$job" "$R/ABORTED.txt" "$R/UNCERTAIN" || true     # cancel by explicit id, then squeue AND sacct proof; UNCERTAIN blocks the next rerun (R3-1)
  exit 5
}
printf '%s\trerun_%d\t%s\t%s\t%d\n' "$job" "$n" "$(date -u +%FT%TZ)" "$tasks" "$(wc -l < "$R/units.txt")" >> "$RUN_DIR/jobs.tsv" \
  || abort_rerun "the job $job was accepted but recording it in jobs.tsv failed"
printf '{"rerun": %d, "job": "%s", "units": %d, "tasks": "%s", "mem": "%s", "wall": "%s"}\n' \
  "$n" "$job" "$(wc -l < "$R/units.txt")" "$tasks" "$mem" "$wall" > "$R/submitted.json" \
  || abort_rerun "the job $job was accepted but writing submitted.json failed"
cat "$R/submitted.json"
