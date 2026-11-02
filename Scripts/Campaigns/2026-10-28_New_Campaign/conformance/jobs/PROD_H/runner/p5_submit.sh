#!/usr/bin/env bash
# p5_submit.sh -- submit the ONE P5 array (DECISIONS D11) over the eligible units only. NOTS login node, OPS.
#   bash RUN_DIR/runner/p5_submit.sh [--dry-run]
# Order of the gates (every refusal exits 2, a guard refusal exits 1, nothing is created before all gates pass, except the scan table):
#   1. test hooks refused; ONE P5 array per run, ever: refuses if p5/submitted.json exists; refuses if ANY P5 attempt record exists
#      (LOGROOT/p5_attempts/*.start.json) -- the durable record that makes a second attempt of a unit impossible
#   2. OPS guard; frozen v2.2.1 tree; compile cache READY
#   3. refuses while ANY job of this run is queued, running or held (squeue; a scan job recorded earlier by p5_scan_run.sh is resumed, not refused),
#      and unless every primary job is terminal in sacct
#   4. reconcile.py --sacct --full-verify: refuses while any unit is running / not_run / rerun_queued / infra (rerun pending) / orphan. Terminal
#      `timeout` and `infra_repeat` units do NOT block P5 (Q2 of Sol review 2): they are individually reconciled, listed in p5_exceptions_for_HQ.tsv
#      for HQ, never retried, and never selected (only primary resource_limit units are).
#   5. p5_scan_run.sh primary (a guarded 1-CPU compute JOB, R2-4; the table is trusted only with its completion receipt; the wrapper runs the charter disk
#      guard itself before its sbatch, R3-2) -> p5_scan_primary.tsv. A scheduler-query failure leaves the recorded scan job, table and receipt paths in place and
#      exits 2 (wrapper exit 11); the next call RESUMES the same job (R3-1). Only a scan proven terminal (squeue AND sacct) is retired as *.failed_*;
#      selected = scan rows with primary resource_limit, base SMCBVS and launchable TRUE; REFUSED if any resource_limit unit is locked, incomplete or
#      invalid_inspect (or has any other retry state: an attempt may have happened); the scan and reconcile must agree on the resource_limit units
#   6. p5/units.tsv (idx case dataset scale p L); ONE array, one unit per task, mem 4G, wall = 2L + margin (max over the selected p), %min(N,10),
#      --qos=nots_commons, combined throttle <= 100 over ALL queued array jobs of fb31; the exact sbatch vector is recorded; the job is appended to
#      jobs.tsv as kind p5. A failed jobs.tsv/submitted.json write AFTER the accepted sbatch cancels the job by its explicit id (a cancel failure is
#      recorded visibly) and leaves p5/ABORTED.txt, which blocks any further P5 submission until HQ has looked at it.
#      --dry-run submits no P5 array; it still runs the read-only scan job (its three artefacts are set aside as *.dryrun_<utc>).
# The tasks run the primary CLI plus --p5-retry with the PRIMARY --mem-gb 2 --hours L/3600 (the adapter doubles them itself).
set -euo pipefail
RUNNER_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
source "$RUNNER_DIR/common.sh"; source "$RUNNER_DIR/frozen_check.sh"
nc_refuse_hooks
[[ $# == 0 || ( $# == 1 && $1 == --dry-run ) ]] || { echo "usage: p5_submit.sh [--dry-run]" >&2; exit 64; }
DRY=${1:-}
RUN_DIR="$HOME_ROOT/runs/$(basename "$(cd "$RUNNER_DIR/.." && pwd)")"
nc_load_run "$RUN_DIR"
PY=$(nc_python)
mkdir -p -- "$SCR_ROOT/tmp"; TMPD=$(mktemp -d "$SCR_ROOT/tmp/p5submit.XXXXXX"); trap 'rm -rf -- "$TMPD"; rmdir "$SCR_ROOT/tmp" 2>/dev/null || true' EXIT
SCAN_MADE=0
refuse() {   # a refusal AFTER the scan retires the scan table (renamed), so a later, legitimate submission can write a fresh one
  echo "$(nc_utc) REFUSED (p5_submit): $*" | tee -a "$LOGROOT/refusals.log" >&2
  if [[ $SCAN_MADE == 1 && ! -e $RUN_DIR/p5/submitted.json ]]; then nc_retire_scan "$RUN_DIR" primary refused "${SCAN_JOB:-}" || echo "(scan record kept: see the message above)" >&2; fi
  exit "${2:-2}"
}
KILL_MARGIN=${KILL_MARGIN:-300}

# 1. one array, one attempt per unit, ever
[[ ! -e $RUN_DIR/p5/submitted.json ]] || refuse "a P5 array was already submitted for $RUN_ID (one P5 array per run, ever)"
[[ ! -e $RUN_DIR/p5/ABORTED.txt ]] || refuse "an earlier P5 submission was aborted after sbatch accepted it ($RUN_DIR/p5/ABORTED.txt): HQ must review before any P5 submission"
if compgen -G "$LOGROOT/p5_attempts/*.start.json" >/dev/null; then refuse "a P5 attempt record already exists in $LOGROOT/p5_attempts: at most one P5 attempt per unit, ever"; fi
# 2. guard, frozen tree, cache
if ! nc_run_guard 10 "$TMPD/guard_receipt.txt"; then refuse "the OPS guard refused or does not enforce the charter limits" 1; fi
nc_check_frozen "$CODE" "$SUMS" 2>"$TMPD/frozen.txt" || refuse "the frozen v2.2.1 tree check failed: $(tr '\n' ' ' < "$TMPD/frozen.txt" | cut -c1-300)"
nc_cache_ready "$CODE" "$RUN_DIR" || refuse "the compile cache is not READY"
# 3. nothing of this run queued, running or held; all primary jobs terminal
live=$(nc_live_jobs "$RUN_DIR" '^p5scan_') || refuse "squeue failed (fail closed)"     # a scan job of an earlier call is resumed below, not a blocker
[[ -z $live ]] || refuse "job(s) of this run are still queued or running: $(echo $live)"
ids=$(nc_job_ids "$RUN_DIR" '^(primary_|rerun_)' | paste -sd, -)
[[ -n $ids ]] || refuse "no primary job ids in jobs.tsv"
sacct -j "$ids" -P -n -X -o JobID,State > "$TMPD/sacct_x.txt" || refuse "sacct failed (fail closed)"
[[ -s $TMPD/sacct_x.txt ]] || refuse "sacct returned nothing for the primary jobs"
bad=$(awk -F'|' '$2 !~ /^(COMPLETED|FAILED|CANCELLED|TIMEOUT|OUT_OF_MEMORY|NODE_FAIL|DEADLINE|BOOT_FAIL|PREEMPTED)/ { print $1 " " $2 }' "$TMPD/sacct_x.txt")
[[ -z $bad ]] || refuse "primary job(s) not terminal in sacct: $(echo $bad | cut -c1-200)"
# 4. reconciled
"$PY" "$RUNNER/reconcile.py" "$RUN_DIR" --sacct --full-verify > "$TMPD/reconcile.json"
cp "$TMPD/reconcile.json" "$RUN_DIR/reconcile_before_p5.json"
open=$(awk -F'\t' 'NR == 1 { for (i = 1; i <= NF; i++) c[$i] = i; next } $c["klass"] ~ /^(running|not_run|rerun_queued|infra|orphan)$/ { n++ } END { print n + 0 }' "$RUN_DIR/reconcile.tsv")
[[ $open == 0 ]] || refuse "$open unit(s) are not reconciled (running, not_run, rerun_queued, infra or orphan): finish or rerun them first (rerun.sh)"
# Terminal exceptions (Q2): `timeout` and `infra_repeat` units do not block P5; they are listed for HQ, never retried, never selected.
awk -F'\t' 'NR == 1 { for (i = 1; i <= NF; i++) c[$i] = i
                      print "case_id\tp\tklass\tattempts\tlast_exit\tstep_state\tnode\tevent_utc"; next }
            $c["klass"] == "timeout" || $c["klass"] == "infra_repeat" {
              print $c["case_id"] "\t" $c["p"] "\t" $c["klass"] "\t" $c["attempts"] "\t" $c["last_exit"] "\t" $c["step_state"] "\t" $c["node"] "\t" $c["event_utc"] }' \
  "$RUN_DIR/reconcile.tsv" > "$TMPD/p5_exceptions_for_HQ.tsv"
n_exc=$(( $(wc -l < "$TMPD/p5_exceptions_for_HQ.tsv") - 1 ))
echo "== terminal exceptions listed for HQ (not blocking P5, never retried): $n_exc unit(s)"; (( n_exc == 0 )) || cat "$TMPD/p5_exceptions_for_HQ.tsv"
# 5. scan and selection
[[ ! -e $RUN_DIR/p5_scan_primary.tsv || -e $RUN_DIR/p5_scan_primary.job ]] || refuse "$RUN_DIR/p5_scan_primary.tsv exists without a recorded scan job (never overwritten, never trusted)"
scan_rc=0; bash "$RUNNER/p5_scan_run.sh" primary || scan_rc=$?
# R3-1: only a scan job PROVEN terminal by squeue AND sacct (wrapper exit 4 = ended not COMPLETED / unverified table; 5 = aborted, cancelled and proven terminal) is
# retired. Every other nonzero exit keeps the recorded job, table path and receipt path: the next call resumes the same job id.
case $scan_rc in
  0) ;;
  10) echo "the scan job is not finished yet: run p5_submit.sh again later (the recorded scan job is reused, nothing is resubmitted)" >&2; exit 10;;
  11) refuse "the state of the P5 scan job is UNKNOWN (scheduler query failed, or an aborted scan job is not proven terminal): its job record, table path and receipt path are KEPT; nothing is retired or resubmitted. Run p5_submit.sh again: the recorded scan job is RESUMED" 2;;
  1) refuse "the OPS guard refused the scan job (p5_scan_run.sh exit 1): nothing was submitted" 1;;
  4) sj=$(awk '$1 == "job" { print $2; exit }' "$RUN_DIR/p5_scan_primary.outcome" 2>/dev/null || true)
     # R4-1: retire ONLY the exact job the wrapper judged, and only if the current record still names it and it is proven terminal
     if nc_retire_scan "$RUN_DIR" primary failed "$sj"; then refuse "the P5 scan job $sj is proven terminal but did not complete or its table/receipt did not verify (exit 4); set aside as p5_scan_primary.*.failed_*"
     else refuse "the P5 scan job '${sj:-?}' did not complete or did not verify (exit 4), but the current scan record was NOT retired (it names another job, or that job is not proven terminal): inspect it"; fi;;
  5) refuse "an accepted scan job could not be recorded (wrapper exit 5): it was cancelled by explicit id and proven terminal (p5_scan_primary.outcome). The current scan record, if any, belongs to another call and is KEPT (R4-1)";;
  12) refuse "another call holds the scan submission lock (wrapper exit 12): nothing was submitted or retired; run p5_submit.sh again" 2;;
  13) refuse "sbatch failed while submitting the P5 scan (wrapper exit 13): whether a scan job was ACCEPTED is unknown, so the scan lock is KEPT with IN_FLIGHT. Resolve it by hand before anything else (JOB.md, stale scan lock); nothing was retired" 2;;
  *) refuse "the P5 scan wrapper refused (exit $scan_rc); a recorded scan job, if any, is kept (it is not proven terminal)";;
esac
SCAN_MADE=1; SCAN_JOB=$(awk '$1 == "job" { print $2; exit }' "$RUN_DIR/p5_scan_primary.job")   # the verified scan's id: later retirements name it (R4-1)
scan=$RUN_DIR/p5_scan_primary.tsv
awk -F'\t' 'NR == 1 { for (i = 1; i <= NF; i++) c[$i] = i
                      split("case_id base primary_v3_status retry_state eligible launchable", need, " ")
                      for (k in need) if (!(need[k] in c)) { print "scan table lacks column " need[k] > "/dev/stderr"; exit 3 }
                      next }
            $c["primary_v3_status"] == "resource_limit" && $c["base"] == "SMCBVS" { print $c["case_id"] "\t" $c["retry_state"] "\t" $c["launchable"] "\t" $c["eligible"] }' "$scan" > "$TMPD/scan_rl.tsv" \
  || refuse "the scan table is malformed"
rec_rl=$(awk -F'\t' 'NR == 1 { for (i = 1; i <= NF; i++) c[$i] = i; next } $c["klass"] == "done" && $c["outcome"] == "resource_limit" { print $c["case_id"] }' "$RUN_DIR/reconcile.tsv" | LC_ALL=C sort)
scan_rl=$(cut -f1 "$TMPD/scan_rl.tsv" | LC_ALL=C sort)
[[ "$rec_rl" == "$scan_rl" ]] || refuse "p5_scan and reconcile disagree on the resource_limit units (scan: $(echo $scan_rl | cut -c1-150); reconcile: $(echo $rec_rl | cut -c1-150))"
bad=$(awk -F'\t' '$2 == "locked" || $2 == "incomplete" || $2 == "invalid_inspect"' "$TMPD/scan_rl.tsv")
[[ -z $bad ]] || refuse "a resource_limit unit is locked, incomplete or invalid_inspect (a retry artefact exists: an attempt may have happened; an operator must inspect it): $(echo $bad | cut -c1-200)"
bad=$(awk -F'\t' '($2 == "none") != ($3 == "TRUE") || ($2 != "none" && $2 != "done")' "$TMPD/scan_rl.tsv")
[[ -z $bad ]] || refuse "the scan table is inconsistent for a resource_limit unit (retry_state vs launchable): $(echo $bad | cut -c1-200)"
bad=$(awk -F'\t' '$2 == "done"' "$TMPD/scan_rl.tsv")
[[ -z $bad ]] || refuse "a resource_limit unit already has a valid P5 retry (at most one attempt per unit, ever): $(echo $bad | cut -c1-200)"
awk -F'\t' '$3 == "TRUE" { print $1 }' "$TMPD/scan_rl.tsv" | LC_ALL=C sort > "$TMPD/eligible.txt"      # select on launchable == TRUE
n=$(wc -l < "$TMPD/eligible.txt")
for c in $(cat "$TMPD/eligible.txt"); do [[ ! -e $LOGROOT/p5_attempts/$c.start.json ]] || refuse "unit $c already has a P5 attempt record"; done
echo "== P5: $n eligible unit(s): $(tr '\n' ' ' < "$TMPD/eligible.txt")"
if (( n == 0 )); then
  if [[ $DRY == --dry-run ]]; then nc_retire_scan "$RUN_DIR" primary dryrun "$SCAN_JOB" || echo "(scan record kept)" >&2; exit 0; fi
  mkdir -p "$RUN_DIR/p5"; cp "$TMPD/p5_exceptions_for_HQ.tsv" "$RUN_DIR/p5_exceptions_for_HQ.tsv"
  printf '{"utc":"%s","eligible":0,"note":"no resource_limit unit: no P5 array"}\n' "$(nc_utc)" > "$RUN_DIR/p5/none_eligible.json"
  echo "no eligible unit: no P5 array is submitted"; exit 0
fi
# 6. units file, vector, submission
{ printf 'idx\tcase_id\tdataset\tscale\tp\tL\n'
  i=0; while IFS= read -r c; do
    [[ $c =~ ^(p(0500|1000)_S[1-6]_r[0-9]{3})_(c100|c050)$ ]] || refuse "bad case id $c"
    ds=${BASH_REMATCH[1]}; sc=${BASH_REMATCH[3]}; p=$((10#${BASH_REMATCH[2]})); L=$L500; [[ $p == 1000 ]] && L=$L1000
    i=$((i + 1)); printf '%d\t%s\t%s\t%s\t%d\t%d\n' "$i" "$c" "$ds" "$sc" "$p" "$L"
  done < "$TMPD/eligible.txt"; } > "$TMPD/units.tsv"
maxL=$(awk -F'\t' 'NR > 1 && $6 > m { m = $6 } END { print m }' "$TMPD/units.tsv")
# per unit: hard kill 2L + 300 (+ 60 s KILL grace) ; task wall = that + 600 s once for loading and hashing
s=$(( 2 * maxL + KILL_MARGIN + 60 + 600 )); wall=$(printf '%d:%02d:00' $(( (s + 59) / 3600 )) $(( ((s + 59) % 3600) / 60 )))
thr=$(( n < 10 ? n : 10 ))
now=$(nc_campaign_throttle 2>"$TMPD/throttle.txt") || refuse "could not determine the queued arrays (fail closed)"
(( now + thr <= 100 )) || refuse "combined throttle $now + $thr > 100 over all queued array jobs of $NC_USER"
args=(--parsable --job-name="smcbvs_${RUN_ID}_p5" --account=commons --partition=commons --qos=nots_commons --nodes=1 --ntasks=1 --cpus-per-task=1
      --mem=4G --time="$wall" --constraint=sapphirerapids --export=NONE --no-requeue --chdir="$LOGROOT"
      --array="1-$n%$thr" --output="$LOGROOT/slurm/%A_%a.out" --error="$LOGROOT/slurm/%A_%a.err" "$RUNNER/p5_task.sh" "$RUN_DIR")
if [[ $DRY == --dry-run ]]; then
  printf 'DRY-RUN sbatch'; printf ' %q' "${args[@]}"; echo
  nc_retire_scan "$RUN_DIR" primary dryrun "$SCAN_JOB" || echo "(scan record kept)" >&2   # the real run writes its own table, receipt and scan job
  echo "== dry run: all gates passed; no P5 array submitted, no P5 record created (the read-only scan job's table, receipt and job record were kept as p5_scan_primary.*.dryrun_*)"; exit 0
fi
mkdir "$RUN_DIR/p5" || refuse "cannot create $RUN_DIR/p5"
mkdir -p "$LOGROOT/p5_attempts" "$LOGROOT/slurm" "$LOGROOT/submit"
cp "$TMPD/units.tsv" "$RUN_DIR/p5/units.tsv"
cp "$TMPD/p5_exceptions_for_HQ.tsv" "$RUN_DIR/p5_exceptions_for_HQ.tsv"
{ printf 'sbatch'; printf ' %q' "${args[@]}"; echo; } > "$RUN_DIR/p5/sbatch_args.txt"
rc=0; job=$(sbatch "${args[@]}" 2>"$LOGROOT/submit/p5_sbatch.err") || rc=$?
if [[ $rc != 0 ]]; then
  echo "P5 sbatch failed (exit $rc): $(head -c 300 "$LOGROOT/submit/p5_sbatch.err" | tr '\n' ' ')" >&2
  mv "$RUN_DIR/p5" "$RUN_DIR/p5.sbatch_failed_$(date -u +%Y%m%dT%H%M%SZ)"; exit 5
fi
job=${job%%;*}
if ! [[ $job =~ ^[0-9]+$ ]]; then echo "P5 sbatch returned an invalid job id '$job'" >&2; mv "$RUN_DIR/p5" "$RUN_DIR/p5.bad_id_$(date -u +%Y%m%dT%H%M%SZ)"; exit 5; fi
# ACCEPTED: a failed record below cancels the job by its explicit id (R2-7), records a cancel failure visibly, and blocks any further P5 submission.
if ! { printf '%s\tp5\t%s\t1-%s%%%s\t%s\n' "$job" "$(nc_utc)" "$n" "$thr" "$n" >> "$RUN_DIR/jobs.tsv" \
       && printf '{"job":"%s","utc":"%s","units":%d,"throttle":%d,"wall":"%s","mem":"4G","eligible":"%s"}\n' "$job" "$(nc_utc)" "$n" "$thr" "$wall" "$(tr '\n' ',' < "$TMPD/eligible.txt")" > "$RUN_DIR/p5/submitted.json"; }; then
  echo "recording the P5 submission failed: cancelling $job by explicit id" >&2
  { echo "aborted $(nc_utc): the P5 job $job was accepted but recording it (jobs.tsv or p5/submitted.json) failed"; } > "$RUN_DIR/p5/ABORTED.txt" 2>/dev/null || true
  nc_abort_accepted "$job" "$RUN_DIR/p5/ABORTED.txt" "$RUN_DIR/p5/UNCERTAIN" || true     # cancel by explicit id, then squeue AND sacct proof; UNCERTAIN is recorded visibly (R3-1); ABORTED.txt blocks any relaunch either way
  exit 5
fi
cat "$RUN_DIR/p5/submitted.json"
echo "== P5 array $job submitted over $n unit(s). After it is terminal: bash $RUNNER/p5_scan_run.sh final"
