#!/bin/bash
# common.sh: sourced (never executed) by submit.sh, rerun.sh, p5_submit.sh, p5_scan_run.sh, final_accounting.sh, make_manifests.sh and
# the task scripts. Functions only: sourcing it runs nothing except the definitions below.
#
# Test hooks. The local dry-run tests substitute the scheduler and the roots through NC_LOCAL_TEST=1, NC_HOME_ROOT, NC_SCR_ROOT, GUARD,
# NC_STUB_BIN. A real submission refuses all of them (nc_refuse_hooks), exactly as the LOWP pilot does.

NC_REAL_HOME=/home/fb31/projects/BVS/New_Campaign
NC_REAL_SCR=/scratch/fb31/New_Campaign
NC_STUDY_DEFAULT=/projects/ml75/fb31/BVS/bench20261019
NC_USER=fb31

nc_utc() { date -u +%Y-%m-%dT%H:%M:%SZ; }
nc_fail() { echo "REFUSED: $*" >&2; exit "${NC_RC:-2}"; }

# nc_refuse_hooks : call first in every entry script.
nc_refuse_hooks() {
  local v
  if [ "${NC_LOCAL_TEST:-0}" != 1 ]; then
    for v in NC_STUB_BIN NC_HOME_ROOT NC_SCR_ROOT NC_STUDY GUARD GUARD_ALLOW_TEST GUARD_TEST_CAMP_LIMIT_MB GUARD_TEST_HOME_LIMIT_MB \
             REQUIRED_CAMP_LIMIT_KB REQUIRED_HOME_LIMIT_KB SCANCEL NC_SCAN_POLL_S NC_SCAN_MAX_WAIT_S; do
      [ -z "${!v:-}" ] || nc_fail "test hook $v is set in the environment (local tests only; unset it)"
    done
  else
    [ -n "${NC_HOME_ROOT:-}" ] && [ "$NC_HOME_ROOT" != "$NC_REAL_HOME" ] || nc_fail "NC_LOCAL_TEST=1 needs a fake NC_HOME_ROOT (never the real campaign tree)"
  fi
  HOME_ROOT="${NC_HOME_ROOT:-$NC_REAL_HOME}"
  SCR_ROOT="${NC_SCR_ROOT:-$NC_REAL_SCR}"
  STUDY="${NC_STUDY:-$NC_STUDY_DEFAULT}"
  GUARD="${GUARD:-$HOME_ROOT/code/ops/guard.sh}"
  SCANCEL="${SCANCEL:-scancel}"
  export HOME_ROOT SCR_ROOT STUDY GUARD
}

# nc_load_run RUN_DIR : source RUN_DIR/config.env (written by submit.sh) and verify it describes this run folder.
nc_load_run() {
  RUN_DIR=$1
  [ -r "$RUN_DIR/config.env" ] || nc_fail "no $RUN_DIR/config.env: this run was never submitted"
  # shellcheck disable=SC1091
  source "$RUN_DIR/config.env"   # RUN_ID HOME_ROOT CODE SUMS STUDY OUTROOT LOGROOT MEM_GB L500 L1000 KILL_MARGIN RUNNER RUN_DIR_CFG
  [ "$(basename "$RUN_DIR")" = "$RUN_ID" ] || nc_fail "run folder name does not match RUN_ID $RUN_ID"
  RES_RUN="$OUTROOT/results/$RUN_ID"
}

# nc_python : the interpreter for reconcile.py, poll.py, accounting_summary.py (Python 3.9+ standard library).
nc_python() { command -v python3 >/dev/null 2>&1 && echo python3 || echo python; }

# nc_cache_ready CODE RUN_DIR : the compile cache named by the precompile job's record must be READY (tasks never compile).
nc_cache_ready() {
  local key
  [ -r "$2/precompile.ok" ] || { echo "no $2/precompile.ok: the precompile job has not finished" >&2; return 1; }
  key=$(awk '$1 == "compiled_key" { print $2; exit }' "$2/precompile.ok")
  [[ "$key" =~ ^[0-9a-f]{64}$ ]] || { echo "precompile.ok holds no valid compiled_key" >&2; return 1; }
  [ -f "$1/core/.cpp_cache/${key:0:16}/READY" ] || { echo "compile cache ${key:0:16} is not READY under $1/core/.cpp_cache" >&2; return 1; }
  return 0
}

# nc_run_guard PLANNED_MB RECEIPT : the OPS guard through guard_check.sh (limits confirmed, planned add admitted). Returns guard_check's status.
nc_run_guard() {
  GUARD="$GUARD" REQUIRED_CAMP_LIMIT_KB="${REQUIRED_CAMP_LIMIT_KB:-524288}" REQUIRED_HOME_LIMIT_KB="${REQUIRED_HOME_LIMIT_KB:-10066329}" \
    bash "$RUNNER_DIR/guard_check.sh" "$1" "$2"
}

# nc_campaign_throttle : prints the combined concurrency ceiling (an integer) of EVERY queued ARRAY job of user fb31, from squeue only.
#   Fail closed (Sol review 2, R2-8): NO name filter. Every array job of fb31 counts, whatever its name (smcbvs_<RUN_ID>_*, lowp_p2_smc,
#   PROD-L's arrays, an unrelated, renamed or truncated name): an unknown array can never be ignored. Plain (non-array) jobs are not arrays.
#   An array contributes max(running tasks, throttle of its pending record "JOBID_[range%N]"); a pending record without "%N" is unlimited
#   (counts 100000, so the check fails). squeue failing or an unparsable job id returns non-zero and prints nothing.
#   A one-line description of each counted array goes to stderr (the receipt).
nc_campaign_throttle() {
  local out
  out=$(squeue -h -u "$NC_USER" -o "%i|%j|%T") || { echo "squeue failed" >&2; return 1; }
  awk -F'|' '
    { id = $1; if (id == "") next
      if (id !~ /_/) next                                   # a plain (non-array) job
      base = id; sub(/_.*/, "", base)
      if (base !~ /^[0-9]+$/) { bad = 1; next }
      rest = id; sub(/^[0-9]+_/, "", rest)
      if (rest ~ /^[0-9]+$/) { run[base]++; seen[base] = $2; next }
      if (rest ~ /^\[[0-9,-]+(%[0-9]+)?\]$/) {
        t = 100000; if (match(rest, /%[0-9]+/)) t = substr(rest, RSTART + 1, RLENGTH - 1) + 0
        if (t > pend[base]) pend[base] = t; seen[base] = $2; next }
      bad = 1 }
    END { if (bad) { print "unparsable squeue job id" > "/dev/stderr"; exit 3 }
          total = 0
          for (b in seen) { c = run[b] + 0; if ((b in pend) && pend[b] > c) c = pend[b]; total += c
                            print "counted array " b " (" seen[b] "): " c > "/dev/stderr" }
          print total }' <<< "$out"
}

# nc_refusal_log RUN_ID : where a refusal is appended (scratch, never home; CHARTER section 2). Once the run's log folder exists it is
#   LOGROOT/refusals.log; before the launch (that folder must not exist yet) it is SCR_ROOT/logs/_refusals/RUN_ID.log.
nc_refusal_log() {
  if [ -d "$SCR_ROOT/logs/$1" ]; then echo "$SCR_ROOT/logs/$1/refusals.log"
  else mkdir -p -- "$SCR_ROOT/logs/_refusals" 2>/dev/null; echo "$SCR_ROOT/logs/_refusals/$1.log"; fi
}

# nc_cancel_id ID RECEIPT : cancel one job BY ITS EXPLICIT ID. A cancel failure is never silent: stderr and RECEIPT (best effort). Returns scancel's status.
nc_cancel_id() {
  local rc=0 msg
  "$SCANCEL" "$1" 2>/dev/null || rc=$?
  if [ $rc = 0 ]; then echo "scancel $1 ok" >> "$2" 2>/dev/null || true
  else msg="CANCEL FAILED for job $1 (scancel rc=$rc): cancel it by hand with the explicit id"; echo "$msg" >&2; echo "$msg" >> "$2" 2>/dev/null || true; fi
  return $rc
}

# nc_job_ids RUN_DIR [KIND_REGEX] [EXCLUDE_KIND_REGEX] : job ids recorded in RUN_DIR/jobs.tsv (kind matches the regex, default all, and not the exclusion).
nc_job_ids() { awk -F'\t' -v re="${2:-.}" -v ex="${3:-}" 'NR > 1 && $1 ~ /^[0-9]+$/ && $2 ~ re && (ex == "" || $2 !~ ex) { print $1 }' "$1/jobs.tsv"; }

# nc_live_jobs RUN_DIR [EXCLUDE_KIND_REGEX] : prints the run's job ids that are still queued, running or held (any kind except the excluded), one per line. Fail closed.
nc_live_jobs() {
  local sq ids j base
  sq=$(squeue -h -r -u "$NC_USER" -o "%i") || { echo "squeue failed" >&2; return 1; }
  ids=$(sed 's/_.*//' <<< "$sq" | sort -u)
  for j in $(nc_job_ids "$1" . "${2:-}"); do
    base=${j%%_*}
    if grep -qx "$base" <<< "$ids"; then echo "$base"; fi
  done
  return 0
}

# nc_retire_scan RUN_DIR PHASE TAG : set the four artefacts of a scan aside (table, completion receipt, job record, guard receipt) as <file>.<TAG>_<utc>, never delete.
# Call it ONLY when the scan job is PROVEN terminal (squeue AND sacct, R3-1): a job whose state is merely unknown may still be writing the table and receipt.
# Sol review 4, R4-1: the caller names the EXPECTED job id. Nothing is retired unless the current job record names exactly that id AND squeue AND sacct
# prove that id terminal; otherwise (another call's live scan owns the record, or the state is unknown) every artefact is KEPT and 1 is returned.
# Sol review 5, R5-1: retirement takes the SAME per-run/per-phase lock as submission (nc_scan_lock), and the record check, the terminal proof and the
# moves all happen while it is held. So a submission cannot record a new job in the middle of a retirement, and a late retirement whose expected id
# is no longer the record's refuses. On contention (another call holds the lock) nothing is retired and 1 is returned.
nc_retire_scan() {   # nc_retire_scan RUN_DIR PHASE TAG EXPECTED_JOB_ID
  local f ts cur st="" rc=0; ts=$(date -u +%Y%m%dT%H%M%SZ)
  [[ ${4:-} =~ ^[0-9]+$ ]] || { echo "nc_retire_scan: no expected job id given: nothing retired" >&2; return 1; }
  nc_scan_lock "$1" "$2" "retire $4" || { echo "nc_retire_scan: another call holds the $2 scan lock ($(nc_scan_lock_path "$1" "$2")): nothing retired" >&2; return 1; }
  cur=$(awk '$1 == "job" { print $2; exit }' "$1/p5_scan_$2.job" 2>/dev/null || true)
  if [[ $cur != "$4" ]]; then
    echo "nc_retire_scan: the $2 scan record names job '${cur:-none}', not $4: nothing retired (it belongs to another call)" >&2; rc=1
  elif ! st=$(nc_job_state "$4") || ! [[ $st =~ $NC_TERMINAL_RE ]]; then
    echo "nc_retire_scan: scan job $4 is not proven terminal by squeue AND sacct (${st:-scheduler unreadable}): nothing retired" >&2; rc=1
  else
    for f in tsv receipt job guard_receipt outcome; do [ -e "$1/p5_scan_$2.$f" ] && mv "$1/p5_scan_$2.$f" "$1/p5_scan_$2.$f.$3_$ts" 2>/dev/null; done
  fi
  nc_scan_unlock "$1" "$2" || true
  return $rc
}

# ---- per-run/per-phase scan lock (Sol reviews 4 and 5: R4-1, R5-1, R5-2) -----------------------------------------------------------------------
# One atomic lock directory RUN_DIR/p5_scan_<phase>.submit.lock (mkdir) serialises scan SUBMISSION and scan RETIREMENT. owner.txt names the holder.
# While an sbatch may have been accepted but its id is not yet journaled, the holder keeps the marker IN_FLIGHT inside the lock: nc_scan_unlock then
# REFUSES to release (fail closed), so neither a catchable signal (TERM/HUP/INT) nor any other exit can open the way to a duplicate scan. Recovery of
# such a lock is by hand (JOB.md): find the possibly accepted job by its name in squeue/sacct, cancel it by explicit id or record it, then remove the lock.
nc_scan_lock_path() { echo "$1/p5_scan_$2.submit.lock"; }
nc_scan_lock() {   # nc_scan_lock RUN_DIR PHASE ROLE : 0 if this call now holds the lock, 1 if another call holds it
  local L; L=$(nc_scan_lock_path "$1" "$2")
  mkdir -- "$L" 2>/dev/null || return 1
  { echo "pid $$"; echo "host $(hostname)"; echo "utc $(nc_utc)"; echo "role $3"; } > "$L/owner.txt"
}
nc_scan_unlock() {   # nc_scan_unlock RUN_DIR PHASE : release, unless a submission is IN FLIGHT (then the lock is kept and 1 is returned)
  local L; L=$(nc_scan_lock_path "$1" "$2")
  [ -d "$L" ] || return 0
  if [ -e "$L/IN_FLIGHT" ]; then
    echo "KEPT $L: an sbatch was in flight and may have been ACCEPTED without its id being recorded ($(tr '\n' ' ' < "$L/IN_FLIGHT")). No new scan can be submitted until OPS resolves it (JOB.md)." >&2
    return 1
  fi
  rm -f -- "$L/owner.txt"; rmdir -- "$L" 2>/dev/null || true
  return 0
}

# ---- scheduler state of ONE job: "unknown" is never "failed" (Sol review 3, R3-1) ---------------------------------------------------------------
NC_TERMINAL_RE='^(COMPLETED|FAILED|CANCELLED|TIMEOUT|OUT_OF_MEMORY|NODE_FAIL|DEADLINE|BOOT_FAIL|PREEMPTED)'
# nc_job_state JOB : prints live | <terminal Slurm state> | unknown. Returns 1 (prints nothing) when squeue or sacct cannot be read: that is NOT evidence
#   that the job is dead. Only a terminal Slurm state from sacct, with JOB absent from squeue, proves that the job can no longer write.
nc_job_state() {
  local sq sa st
  sq=$(squeue -h -r -u "$NC_USER" -o "%i") || return 1
  if sed 's/_.*//' <<< "$sq" | grep -qx "$1"; then echo live; return 0; fi
  sa=$(sacct -j "$1" -P -n -X -o JobID,State) || return 1
  st=$(awk -F'|' 'NR == 1 { split($2, a, " "); print a[1] }' <<< "$sa")
  [[ $st =~ $NC_TERMINAL_RE ]] && echo "$st" || echo unknown
}
# nc_abort_accepted JOB RECEIPT MARKER : abort an ACCEPTED job whose records could not be written. Cancel by explicit id, then try (3 times) to PROVE with
#   squeue AND sacct that it is terminal. Proven: returns 0. Otherwise (cancel failed, scheduler unreadable, job still shown): MARKER ("job N ...") is
#   written, RECEIPT says UNCERTAIN, returns 1; the caller must keep every record and must not relaunch (nc_clear_uncertain gates the next submission).
nc_abort_accepted() {
  local rc=0 k st pause=10
  [ "${NC_LOCAL_TEST:-0}" = 1 ] && pause=${NC_SCAN_POLL_S:-1}
  nc_cancel_id "$1" "$2" || rc=$?
  if [ $rc = 0 ]; then
    for k in 1 2 3; do
      if st=$(nc_job_state "$1") && [[ $st =~ $NC_TERMINAL_RE ]]; then echo "job $1 proven terminal after the cancel ($st): squeue and sacct agree" >> "$2" 2>/dev/null || true; return 0; fi
      sleep "$pause"
    done
  fi
  { echo "job $1"; echo "utc $(nc_utc)"; echo "note cancel failed or the job is not proven terminal by squeue AND sacct: it may still be queued or running and writing"; } > "$3" 2>/dev/null || true
  echo "UNCERTAIN: job $1 is not proven terminal (squeue AND sacct) after the abort: it may still write; nothing will be relaunched until it is proven terminal. Cancel it by hand with its explicit id if it is still shown." >&2
  echo "UNCERTAIN: job $1 not proven terminal (see $3)" >> "$2" 2>/dev/null || true
  return 1
}
# nc_clear_uncertain MARKER : 0 if there is no marker or its job is now PROVEN terminal (the marker is set aside as .cleared_<utc>); 1 otherwise.
nc_clear_uncertain() {
  local j st
  [ -e "$1" ] || return 0
  j=$(awk '$1 == "job" { print $2; exit }' "$1")
  [[ $j =~ ^[0-9]+$ ]] || { echo "$1 names no valid job id" >&2; return 1; }
  if st=$(nc_job_state "$j") && [[ $st =~ $NC_TERMINAL_RE ]]; then mv "$1" "$1.cleared_$(date -u +%Y%m%dT%H%M%SZ)"; return 0; fi
  echo "job $j (marker $1) is not proven terminal by squeue AND sacct (state: ${st:-scheduler unreadable}): it may still write. Wait for it or cancel it by hand with its explicit id, then run the command again." >&2
  return 1
}
