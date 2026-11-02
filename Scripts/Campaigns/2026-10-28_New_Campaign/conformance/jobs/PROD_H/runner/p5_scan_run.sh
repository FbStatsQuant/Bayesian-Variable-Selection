#!/usr/bin/env bash
# p5_scan_run.sh -- run the frozen tools/p5_scan.R over the run's scratch results AS A GUARDED SINGLE-CPU COMPUTE JOB (Sol review 2, R2-4),
# wait for it, and verify its table and completion receipt. NOTS login node, OPS; also called by p5_submit.sh. The login node only submits one
# small job (p5_scan.sbatch) and reads receipts; the scanner (which hashes and deserializes every primary RDS: minutes of CPU) never runs there.
#   bash RUN_DIR/runner/p5_scan_run.sh primary [--no-wait]   -> RUN_DIR/p5_scan_primary.tsv + .receipt + .job  (before P5)
#   bash RUN_DIR/runner/p5_scan_run.sh final   [--no-wait]   -> p5_scan_final.tsv + p5_final_report.tsv      (after the P5 array is terminal)
# Resources (explicit estimate, see p5_scan.sbatch): 1 CPU, --mem=4G, --time=01:00:00, account/partition commons, --qos=nots_commons, no Sapphire
# Rapids constraint, --no-requeue, --export=NONE; stdout/stderr in LOGROOT/slurm/ and LOGROOT/p5_scan/ (scratch).
# The job id is recorded in RUN_DIR/p5_scan_<phase>.job (noclobber) and in jobs.tsv (kind p5scan_<phase>). A second call with a recorded job does
# NOT submit again: it waits for / checks that job. A table is trusted only when ALL of these hold (verify_scan): the job is COMPLETED in sacct,
# the receipt exists and names the same phase and job, its sha256 equals the table's, its row count equals the table's, the scanner exit was 0
# and the scanner's summary line is present.
# DISK GUARD (Sol review 3, R3-2): the new-job branch calls the charter-limit guard (nc_run_guard, home <= 9.6 GiB, campaign <= 0.5 GiB) with a planned
# allowance for the home table + receipt + job record BEFORE sbatch, and keeps the small guard receipt RUN_DIR/p5_scan_<phase>.guard_receipt. This covers
# the direct primary and final calls. A denying guard = exit 1 and NO sbatch. Re-checking a recorded job never calls the guard and never resubmits.
# UNKNOWN IS NOT FAILED (Sol review 3, R3-1): if squeue or sacct cannot be read, the job record, table path and receipt path are KEPT, the exit is 11
# and the next call RESUMES the same job id. A recorded job is retired (by p5_submit.sh) only when squeue AND sacct prove it terminal (exit 4 / 5). An
# abort after an accepted sbatch that cannot be proven terminal (cancel failed, scheduler unreadable) writes RUN_DIR/p5_scan_<phase>.uncertain, which
# blocks any new submission until squeue AND sacct prove that job terminal.
# Exit: 0 verified | 10 job not finished yet (run the same command again; nothing is resubmitted) | 11 scheduler state unknown (run the same command again) |
# 4 the scan job ended terminal-but-failed or the table/receipt do not verify | 5 abort after an accepted sbatch could not be recorded (cancelled by
# explicit id AND proven terminal) | 12 another call holds the submission lock (R4-1; nothing submitted or retired) | 13 sbatch exited nonzero, acceptance UNKNOWN,
# lock kept with IN_FLIGHT (R6-1) | 1 the guard refused | 2 refusal.
# final also checks the P5 contract: EVERY unit selected by p5_submit.sh (p5/units.tsv) must have a valid retry record
# (<case>/P5_retry/SMCBVS_p5retry.done with matching hashes) or is REPORTED in p5_final_report.tsv (state locked / incomplete / none, never retried
# a second time). The retry files live in <case>/P5_retry/, outside the primary reconciliation counts.
set -euo pipefail
RUNNER_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
source "$RUNNER_DIR/common.sh"; source "$RUNNER_DIR/frozen_check.sh"
nc_refuse_hooks
PHASE=${1:-}; [[ $PHASE == primary || $PHASE == final ]] || { echo "usage: p5_scan_run.sh primary|final [--no-wait]" >&2; exit 64; }
NOWAIT=0; [[ ${2:-} == --no-wait ]] && NOWAIT=1
[[ $# -le 2 && ( $# -lt 2 || $NOWAIT == 1 ) ]] || { echo "usage: p5_scan_run.sh primary|final [--no-wait]" >&2; exit 64; }
RUN_DIR="$HOME_ROOT/runs/$(basename "$(cd "$RUNNER_DIR/.." && pwd)")"
nc_load_run "$RUN_DIR"
SCAN_MEM=4G; SCAN_WALL=01:00:00                        # estimate: 10-20 min on one CPU (see p5_scan.sbatch); wall = 3x ceiling
POLL=30; MAXWAIT=1800
if [[ ${NC_LOCAL_TEST:-0} == 1 ]]; then POLL=${NC_SCAN_POLL_S:-30}; MAXWAIT=${NC_SCAN_MAX_WAIT_S:-1800}; fi   # nc_refuse_hooks refuses both outside tests
OUT=$RUN_DIR/p5_scan_$PHASE.tsv; REC=$RUN_DIR/p5_scan_$PHASE.receipt; JOBF=$RUN_DIR/p5_scan_$PHASE.job
UNC=$RUN_DIR/p5_scan_$PHASE.uncertain; GREC=$RUN_DIR/p5_scan_$PHASE.guard_receipt; PLANNED_MB=5   # PLANNED_MB: home table (<= ~1 MB) + receipt + job record + guard receipt
# ONE SUBMITTER (Sol review 4, R4-1): the "no job record" check, the sbatch and the job-record write run under an atomic lock directory per run and
# phase (mkdir), released before the long wait. A concurrent call that finds the lock exits 12 (nothing submitted, nothing retired; run again).
# A killed submitter leaves the lock with owner.txt: inspect, then remove it by hand. Exits 4/5 write p5_scan_<phase>.outcome naming the job judged,
# so the parent retires only that exact id (nc_retire_scan checks the current record AND the terminal state).
# Sol review 5: the lock is the shared nc_scan_lock (common.sh), which retirement takes too (R5-1). Before sbatch the marker IN_FLIGHT is written in the
# lock; it is removed only once the outcome is SAFE (the job id journaled, sbatch definitely rejected, or an aborted job proven terminal / marked
# uncertain). While it exists, nc_scan_unlock keeps the lock, so a TERM/HUP/INT (or any exit) during an unresolved acceptance fails closed (R5-2).
SUBLOCK=$(nc_scan_lock_path "$RUN_DIR" "$PHASE"); LOCK_HELD=0
release_lock() { if [[ $LOCK_HELD == 1 ]]; then nc_scan_unlock "$RUN_DIR" "$PHASE" && LOCK_HELD=0; fi; return 0; }
trap release_lock EXIT
outcome() { { echo "job $1"; echo "exit $2"; echo "utc $(nc_utc)"; } > "$RUN_DIR/p5_scan_$PHASE.outcome" 2>/dev/null || true; }

recv() { awk -v k="$2" '$1 == k { sub(/^[^ ]+ /, ""); print; exit }' "$1"; }
verify_scan() {   # verify_scan JOB : 0 if the table and the completion receipt of JOB verify; prints the reason otherwise
  local sha rows
  [[ -s $OUT ]] || { echo "no table $OUT"; return 1; }
  [[ -s $REC ]] || { echo "no completion receipt $REC"; return 1; }
  [[ $(recv "$REC" phase) == "$PHASE" && $(recv "$REC" job) == "$1" ]] || { echo "receipt names another phase or job"; return 1; }
  [[ $(recv "$REC" scanner_exit) == 0 ]] || { echo "receipt: scanner did not exit 0"; return 1; }
  sha=$(sha256sum "$OUT" | cut -d' ' -f1); [[ $(recv "$REC" table_sha256) == "$sha" ]] || { echo "table sha256 differs from the receipt"; return 1; }
  rows=$(( $(wc -l < "$OUT") - 1 )); [[ $(recv "$REC" rows) == "$rows" ]] || { echo "table row count differs from the receipt"; return 1; }
  [[ $(recv "$REC" summary) == "p5_scan units=$rows "* ]] || { echo "receipt summary does not match the table"; return 1; }
  return 0
}

JOB=""
if [[ ! -e $JOBF ]]; then
  nc_scan_lock "$RUN_DIR" "$PHASE" "submit" || NC_RC=12 nc_fail "another call holds the $PHASE scan lock ($SUBLOCK: submitting or retiring): nothing was submitted and nothing retired; run the same command again in a minute. If no call is running the lock is stale: follow JOB.md (stale scan lock) -- if $SUBLOCK/IN_FLIGHT exists an sbatch may have been ACCEPTED and must be found and resolved first"
  LOCK_HELD=1
fi
if [[ -e $JOBF ]]; then   # (re-checked under the lock: a call that recorded its job meanwhile is resumed, never duplicated)
  release_lock
  JOB=$(recv "$JOBF" job)
  [[ $JOB =~ ^[0-9]+$ ]] || nc_fail "$JOBF holds no valid job id"
  echo "== p5 scan $PHASE: job $JOB already recorded ($JOBF): not resubmitted, checking it"
else
  [[ ! -e $OUT && ! -e $REC ]] || nc_fail "$OUT or its receipt exists without a recorded scan job: a scan table is never overwritten or trusted without its job"
  nc_check_frozen "$CODE" "$SUMS" || nc_fail "the frozen v2.2.1 tree check failed"
  nc_cache_ready "$CODE" "$RUN_DIR" || nc_fail "the compile cache is not READY"
  [[ -d $RES_RUN ]] || nc_fail "no results folder $RES_RUN"
  nc_clear_uncertain "$UNC" || NC_RC=11 nc_fail "an earlier aborted scan job of this phase is not proven terminal ($UNC): no new scan job is submitted"
  if ! nc_run_guard "$PLANNED_MB" "$GREC"; then NC_RC=1 nc_fail "the OPS guard refused or does not enforce the charter limits for a planned add of ${PLANNED_MB} MB (receipt $GREC): the scan job was NOT submitted"; fi
  mkdir -p -- "$LOGROOT/slurm" "$LOGROOT/submit" "$LOGROOT/p5_scan"
  args=(--parsable --job-name="smcbvs_${RUN_ID}_p5scan_$PHASE" --account=commons --partition=commons --qos=nots_commons --nodes=1 --ntasks=1
        --cpus-per-task=1 --mem="$SCAN_MEM" --time="$SCAN_WALL" --export=NONE --no-requeue --chdir="$LOGROOT"
        --output="$LOGROOT/slurm/%j.out" --error="$LOGROOT/slurm/%j.err" "$RUNNER/p5_scan.sbatch" "$RUN_DIR" "$PHASE")
  # R5-2: from here until the id is journaled an accepted job may exist that no record names: IN_FLIGHT keeps the lock closed on ANY exit
  { echo "job_name smcbvs_${RUN_ID}_p5scan_$PHASE"; echo "user $NC_USER"; echo "since_utc $(nc_utc)"; echo "pid $$"; } > "$SUBLOCK/IN_FLIGHT"
  rc=0; JOB=$(sbatch "${args[@]}" 2>"$LOGROOT/submit/p5scan_${PHASE}_sbatch.err") || rc=$?
  if [[ $rc != 0 ]]; then
    # Sol review 6, R6-1: a nonzero sbatch status proves only that the CLIENT failed, not that the scheduler rejected the job (a client killed
    # after the acceptance also exits nonzero). So acceptance is UNKNOWN: IN_FLIGHT and the lock are KEPT (fail closed) and the outcome is exit 13.
    # best effort (Sol review 7, R7-1): a failure to append these diagnostics must not bypass the exit-13 outcome; the marker itself stays
    { echo "client_status $rc"; echo "client_stderr $(head -c 300 "$LOGROOT/submit/p5scan_${PHASE}_sbatch.err" | tr '\n' ' ')"; } >> "$SUBLOCK/IN_FLIGHT" 2>/dev/null \
      || echo "WARNING: could not append the sbatch status to $SUBLOCK/IN_FLIGHT; the marker and the lock are kept regardless" >&2
    NC_RC=13 nc_fail "sbatch exited $rc while submitting the $PHASE scan, so it is UNKNOWN whether the scheduler accepted a job ($(head -c 200 "$LOGROOT/submit/p5scan_${PHASE}_sbatch.err" | tr '\n' ' ')). The scan lock is KEPT with $SUBLOCK/IN_FLIGHT; nothing will be submitted until OPS resolves it (JOB.md, stale scan lock: look for job name smcbvs_${RUN_ID}_p5scan_$PHASE since the IN_FLIGHT time; cancel any by explicit id and wait until sacct shows it terminal; only then remove the lock)"
  fi
  JOB=${JOB%%;*}
  [[ $JOB =~ ^[0-9]+$ ]] || nc_fail "sbatch returned an invalid job id '$JOB' for the scan: an accepted job may exist without a usable id, so the scan lock is KEPT (IN_FLIGHT); resolve it by hand (JOB.md, stale scan lock)"
  echo "accepted_job $JOB" >> "$SUBLOCK/IN_FLIGHT"
  # ACCEPTED: any failure of the records below cancels it by its explicit id (R2-7)
  if ! ( set -C; { echo "job $JOB"; echo "phase $PHASE"; echo "submitted_utc $(nc_utc)"; echo "mem $SCAN_MEM"; echo "wall $SCAN_WALL"
                   printf 'sbatch'; printf ' %q' "${args[@]}"; echo; } > "$JOBF" ) \
     || ! printf '%s\tp5scan_%s\t%s\t-\t1\n' "$JOB" "$PHASE" "$(nc_utc)" >> "$RUN_DIR/jobs.tsv"; then
    echo "the scan job $JOB was accepted but recording it failed: cancelling it by explicit id" >&2
    if nc_abort_accepted "$JOB" "$RUN_DIR/p5_scan_$PHASE.ABORTED" "$UNC"; then rm -f -- "$SUBLOCK/IN_FLIGHT"; outcome "$JOB" 5; exit 5; fi
    # not proven terminal: the UNCERTAIN marker ($UNC, naming the job) now gates every new submission, so the in-flight state is handed over to it
    [[ -s $UNC ]] && rm -f -- "$SUBLOCK/IN_FLIGHT"
    NC_RC=11 nc_fail "the scan job $JOB was accepted, recording it failed and it is NOT proven terminal after the cancel ($UNC): no new scan job is submitted until squeue AND sacct prove it terminal"
  fi
  rm -f -- "$SUBLOCK/IN_FLIGHT"   # the id is journaled (job record + jobs.tsv): safe
  release_lock
  echo "== p5 scan $PHASE: submitted job $JOB (1 CPU, $SCAN_MEM, $SCAN_WALL); the scanner runs on a compute node"
fi

deadline=$(( $(date +%s) + MAXWAIT )); unknown=0
while :; do
  st=$(nc_job_state "$JOB") || NC_RC=11 nc_fail "SCHEDULER QUERY FAILED (squeue or sacct): the state of scan job $JOB is UNKNOWN, which is not evidence that it failed. Its job record ($JOBF), table ($OUT) and receipt ($REC) are KEPT; nothing is retired or resubmitted. Run the same command again: it resumes job $JOB."
  if [[ $st == unknown ]]; then
    unknown=$((unknown + 1)); (( unknown <= 3 )) || { echo "scan job $JOB: sacct shows no terminal state (accounting lag?): run this command again"; exit 10; }
  elif [[ $st != live ]]; then break
  fi
  [[ $NOWAIT == 0 ]] || { echo "scan job $JOB not finished ($st): run this command again to check it (nothing is resubmitted)"; exit 10; }
  (( $(date +%s) < deadline )) || { echo "scan job $JOB still $st after ${MAXWAIT}s: run this command again to keep waiting (nothing is resubmitted)"; exit 10; }
  sleep "$POLL"
done
[[ $st == COMPLETED ]] || { echo "SCAN FAILED: job $JOB ended $st; see $LOGROOT/slurm/$JOB.err and $LOGROOT/p5_scan/ (the table is not trusted)" >&2; outcome "$JOB" 4; exit 4; }
reason=$(verify_scan "$JOB") || { echo "SCAN NOT VERIFIED: job $JOB COMPLETED but $reason" >&2; outcome "$JOB" 4; exit 4; }
echo "== p5 scan $PHASE verified: job $JOB COMPLETED, receipt and table agree ($(recv "$REC" summary))"
if [[ $PHASE == final ]]; then
  [[ -s $RUN_DIR/p5/units.tsv ]] || { echo "no P5 array was submitted for this run: nothing to check"; exit 0; }
  awk -F'\t' 'FNR == NR { if (FNR > 1) sel[$2] = 1; next }
              FNR == 1 { for (i = 1; i <= NF; i++) f[$i] = i
                         print "case_id\tretry_state\tretry_v3_status\tprimary_v3_status\tvalid_retry_record\treported"; next }
              ($f["case_id"] in sel) { v = ($f["retry_state"] == "done") ? "yes" : "no"
                         print $f["case_id"] "\t" $f["retry_state"] "\t" $f["retry_v3_status"] "\t" $f["primary_v3_status"] "\t" v "\t" (v == "yes" ? "no" : "YES"); seen[$f["case_id"]] = 1 }
              END { for (s in sel) if (!(s in seen)) print s "\tmissing_from_scan\tNA\tNA\tno\tYES" }' \
      "$RUN_DIR/p5/units.tsv" "$OUT" > "$RUN_DIR/p5_final_report.tsv"
  n=$(( $(wc -l < "$RUN_DIR/p5/units.tsv") - 1 )); valid=$(awk -F'\t' 'NR > 1 && $5 == "yes"' "$RUN_DIR/p5_final_report.tsv" | wc -l)
  rep=$(awk -F'\t' 'NR > 1 && $6 == "YES"' "$RUN_DIR/p5_final_report.tsv" | wc -l)
  echo "P5 final: selected $n, valid retry record $valid, reported (no valid record) $rep -> $RUN_DIR/p5_final_report.tsv"
  [[ $((valid + rep)) == "$n" ]] || nc_fail "P5 final report does not cover all $n selected units"
  if awk -F'\t' 'NR > 1 && ($2 == "locked" || $2 == "incomplete")' "$RUN_DIR/p5_final_report.tsv" | grep -q .; then
    echo "NOTE: a selected unit is locked/incomplete (an attempt was killed or left artefacts): run runner/cleanup_terminal.sh (it archives the evidence and removes only proven-stale locks/temporary files; it never relaunches a fit) before make_manifests.sh"
  fi
fi
