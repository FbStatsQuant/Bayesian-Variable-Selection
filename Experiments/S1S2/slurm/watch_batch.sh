#!/usr/bin/env bash
# watch_batch.sh -- run on OWLS as a systemd USER unit (survives T3 restarts; setsid/nohup children do not, see
# ~/.config/bvs-hq/owls/POLICY.md). Every INTERVAL s: ONE ssh to NOTS runs check_batch.sh and counts the batch's jobs
# still in the queue. Appends to LOG; status lines start with "WATCH ". It never submits or deletes anything; it cancels
# only with --cancel-pending-on-stop (below).
#   On a STOP verdict: logs "WATCH ALERT STOP ..." and keeps watching (the manager decides). With --cancel-pending-on-stop
#   (HQ 2026-11-26) it also cancels, once, the batch's PENDING tasks: fb31's queued jobs whose name starts with the
#   batch prefix, via scancel -u fb31 --state=PENDING (running tasks keep running; no other job is touched); logs
#   "WATCH CANCELLED_PENDING ...".
#   When no job of the batch is left in the queue: pull_to_owls.sh (sha-verified); partition record sacct_record.sh ->
#   copied to Owls runs/S1S2/_logs/sacct/sacct_<tag>.tsv (+ .sha256, the NOTS sum, verified); if the final verdict is
#   PASS, also package_for_desktop.sh (with the partition record) -> records/S1S2_smcbvs_<tag>; logs "WATCH DONE ...".
# Suites: --suite 1 (default; S1, job names s1smc_b<K>_*, tag b<K>) or --suite 2 (S2, s2smc_b<K>_*, tag s2b<K>).
# Re-runnable: check/pull/record are idempotent; packaging refuses if the unit already exists.
# Reruns of a batch (e.g. its timed-out tasks under job name s1smc_b1r_<class>): --jobs <their ids> (passed to
# check_batch.sh and sacct_record.sh), --prefix s1smc_b1r_ (queue count), --tag b1r (pull manifest and record tag),
# --no-package (the batch's unit exists).
# Launch:
#   systemd-run --user --unit=s1s2-watch-b1-$(date +%Y%m%d-%H%M%S) --collect --quiet \
#     -p StandardOutput=append:$LOG -p StandardError=append:$LOG  <this script> --batch 1 --reps 1-25 --log $LOG
# Edit this file only by writing a new copy and mv-ing it over (bash reads a running script incrementally).
set -uo pipefail
HERE=$(cd "$(dirname "$0")" && pwd)
NSL=/home/fb31/SMC-BVS/_local/engineering/S1S2/deploy/S1S2/slurm
RDIR=/home/fb31/Bayesian-Variable-Selection/_local/engineering/runs/S1S2/_logs/sacct
batch=""; reps=""; interval=1800; log=/dev/stdout; jobs=""; prefix=""; tag=""; nopkg=0; suite=1; cancel=0
while (($#)); do case "$1" in --batch) batch="$2"; shift 2;; --reps) reps="$2"; shift 2;; --interval) interval="$2"; shift 2;;
  --log) log="$2"; shift 2;; --jobs) jobs="$2"; shift 2;; --prefix) prefix="$2"; shift 2;; --tag) tag="$2"; shift 2;;
  --suite) suite="$2"; shift 2;; --cancel-pending-on-stop) cancel=1; shift;;
  --no-package) nopkg=1; shift;; *) echo "unknown arg $1" >&2; exit 64;; esac; done
[[ "$batch" =~ ^[0-9]+$ && "$reps" =~ ^[0-9]+-[0-9]+$ ]] || { echo "usage: --batch K --reps LO-HI" >&2; exit 64; }
[[ "$suite" == 1 || "$suite" == 2 ]] || { echo "--suite must be 1 or 2" >&2; exit 64; }
[[ -z "$jobs" || "$jobs" =~ ^[0-9,]+$ ]] || { echo "--jobs: comma-separated job ids" >&2; exit 64; }
if [[ $suite == 1 ]]; then prefix=${prefix:-s1smc_b${batch}_}; tag=${tag:-b$batch}; else prefix=${prefix:-s2smc_b${batch}_}; tag=${tag:-s2b$batch}; fi
[[ "$prefix" =~ ^s[12]smc_b[0-9]+[a-z0-9]*_$ && "$tag" =~ ^[A-Za-z0-9_]+$ ]] || { echo "bad --prefix/--tag" >&2; exit 64; }
say() { echo "WATCH $(date -u +%FT%TZ) $tag $*" >> "$log"; }
say "start pid=$$ suite=$suite interval=${interval}s prefix=$prefix tag=$tag jobs=${jobs:-<submissions.tsv>} package=$((1 - nopkg)) cancel_pending_on_stop=$cancel"
cancelled=0
while true; do
  out=$(ssh -o ConnectTimeout=60 nots "$NSL/check_batch.sh --suite $suite --batch $batch --reps $reps ${jobs:+--jobs $jobs} 2>&1; echo LIVE=\$(squeue -u fb31 -h -o %j | grep -c '^${prefix}')" 2>&1)
  rc=$?
  { echo "----- $(date -u +%FT%TZ)"; echo "$out"; } >> "$log"
  live=$(sed -n 's/^LIVE=//p' <<< "$out" | tail -1); verdict=$(grep '^VERDICT' <<< "$out" | tail -1)
  if [[ $rc -ne 0 || -z "$live" ]]; then say "ssh/check error rc=$rc; retry in ${interval}s"; sleep "$interval"; continue; fi
  say "live_jobs=$live $verdict"
  if [[ "$verdict" == "VERDICT: STOP"* && "$live" -gt 0 ]]; then
    say "ALERT STOP (batch still running): $verdict"
    if (( cancel && ! cancelled )); then
      co=$(ssh -o ConnectTimeout=60 nots "ids=\$(squeue -u fb31 -h -t PD -o '%u %j %i' | awk '\$1 == \"fb31\" && index(\$2, \"$prefix\") == 1 { print \$3 }' | paste -sd' ' -);
        echo PENDING_IDS=\$ids; [ -n \"\$ids\" ] && scancel -u fb31 --state=PENDING \$ids; echo SCANCEL_RC=\$?" 2>&1); crc=$?
      echo "$co" >> "$log"
      say "CANCELLED_PENDING rc=$crc $(grep -E '^(PENDING_IDS|SCANCEL_RC)=' <<< "$co" | paste -sd' ' -)"
      (( crc == 0 )) && cancelled=1
    fi
  fi
  if (( live == 0 )); then
    pull=$("$HERE/pull_to_owls.sh" --suite "$suite" --reps "$reps" --tag "$tag" 2>&1); prc=$?
    echo "$pull" >> "$log"
    man=$(sed -n 's/^manifest: \([^ ]*\) .*/\1/p' <<< "$pull" | tail -1)
    if (( prc != 0 )) || ! grep -q '^VERIFIED' <<< "$pull"; then say "DONE pull FAILED rc=$prc; $verdict"; exit 1; fi
    # partition record: written on NOTS, copied, verified against the NOTS sha256
    rec=$(ssh -o ConnectTimeout=60 nots "$NSL/sacct_record.sh --suite $suite --batch $batch --tag $tag ${jobs:+--jobs $jobs}" 2>&1)
    echo "$rec" >> "$log"; stsv=""
    read -r _ rpath rsha rrows < <(grep '^SACCT_RECORD ' <<< "$rec" | tail -1) || true
    if [[ -n "${rsha:-}" ]]; then
      mkdir -p "$RDIR"; b=$(basename "$rpath")
      if rsync -a "nots:$rpath" "$RDIR/$b" && echo "$rsha  $b" > "$RDIR/$b.sha256" && ( cd "$RDIR" && sha256sum --quiet -c "$b.sha256" ); then
        stsv=$RDIR/$b; say "partition record VERIFIED $stsv rows=$rrows sha256=$rsha"
      else say "partition record copy FAILED ($rpath)"; fi
    else say "partition record FAILED on NOTS"; fi
    if (( nopkg )); then
      say "DONE pull=VERIFIED manifest=$man record=${stsv:-MISSING} package=SKIPPED (--no-package) $verdict"
    elif [[ "$verdict" == "VERDICT: PASS"* && -n "$stsv" ]]; then
      pk=$("$HERE/package_for_desktop.sh" --suite "$suite" --batch "$batch" --reps "$reps" --manifest "$man" --slurm-tsv "$stsv" 2>&1); krc=$?
      echo "$pk" >> "$log"; say "DONE pull=VERIFIED manifest=$man record=$stsv package_rc=$krc $verdict"
    else
      say "DONE pull=VERIFIED manifest=$man record=${stsv:-MISSING} package=SKIPPED (verdict not PASS or no record) $verdict"
    fi
    exit 0
  fi
  sleep "$interval"
done
