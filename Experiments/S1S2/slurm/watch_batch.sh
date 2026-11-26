#!/usr/bin/env bash
# watch_batch.sh -- run on OWLS as a systemd USER unit (survives T3 restarts; setsid/nohup children do not, see
# ~/.config/bvs-hq/owls/POLICY.md). Every INTERVAL s: ONE ssh to NOTS runs check_batch.sh and counts the batch's jobs
# still in the queue. Appends to LOG; status lines start with "WATCH ". It never submits, cancels or deletes anything.
#   On a STOP verdict: logs "WATCH ALERT STOP ..." and keeps watching (the manager decides).
#   When no job of the batch is left in the queue: pull_to_owls.sh (sha-verified); if the final verdict is PASS, also
#   package_for_desktop.sh -> records/S1S2_smcbvs_b<K>; logs "WATCH DONE ..." and exits.
# Re-runnable: check/pull are idempotent; packaging refuses if the unit already exists.
# Launch:
#   systemd-run --user --unit=s1s2-watch-b1-$(date +%Y%m%d-%H%M%S) --collect --quiet \
#     -p StandardOutput=append:$LOG -p StandardError=append:$LOG  <this script> --batch 1 --reps 1-25 --log $LOG
set -uo pipefail
HERE=$(cd "$(dirname "$0")" && pwd)
NSL=/home/fb31/SMC-BVS/_local/engineering/S1S2/deploy/S1S2/slurm
MAN_DIR=/home/fb31/Bayesian-Variable-Selection/_local/engineering/runs/S1S2/_manifests
batch=""; reps=""; interval=1800; log=/dev/stdout
while (($#)); do case "$1" in --batch) batch="$2"; shift 2;; --reps) reps="$2"; shift 2;; --interval) interval="$2"; shift 2;;
  --log) log="$2"; shift 2;; *) echo "unknown arg $1" >&2; exit 64;; esac; done
[[ "$batch" =~ ^[0-9]+$ && "$reps" =~ ^[0-9]+-[0-9]+$ ]] || { echo "usage: --batch K --reps LO-HI" >&2; exit 64; }
say() { echo "WATCH $(date -u +%FT%TZ) b$batch $*" >> "$log"; }
say "start pid=$$ interval=${interval}s"
while true; do
  out=$(ssh -o ConnectTimeout=60 nots "$NSL/check_batch.sh --batch $batch --reps $reps 2>&1; echo LIVE=\$(squeue -u fb31 -h -o %j | grep -c '^s1smc_b${batch}_')" 2>&1)
  rc=$?
  { echo "----- $(date -u +%FT%TZ)"; echo "$out"; } >> "$log"
  live=$(sed -n 's/^LIVE=//p' <<< "$out" | tail -1); verdict=$(grep '^VERDICT' <<< "$out" | tail -1)
  if [[ $rc -ne 0 || -z "$live" ]]; then say "ssh/check error rc=$rc; retry in ${interval}s"; sleep "$interval"; continue; fi
  say "live_jobs=$live $verdict"
  [[ "$verdict" == "VERDICT: STOP"* && "$live" -gt 0 ]] && say "ALERT STOP (batch still running): $verdict"
  if (( live == 0 )); then
    pull=$("$HERE/pull_to_owls.sh" --reps "$reps" --tag "b$batch" 2>&1); prc=$?
    echo "$pull" >> "$log"
    man=$(sed -n 's/^manifest: \([^ ]*\) .*/\1/p' <<< "$pull" | tail -1)
    if (( prc != 0 )) || ! grep -q '^VERIFIED' <<< "$pull"; then say "DONE pull FAILED rc=$prc; $verdict"; exit 1; fi
    if [[ "$verdict" == "VERDICT: PASS"* ]]; then
      pk=$("$HERE/package_for_desktop.sh" --batch "$batch" --reps "$reps" --manifest "$man" 2>&1); krc=$?
      echo "$pk" >> "$log"; say "DONE pull=VERIFIED manifest=$man package_rc=$krc $verdict"
    else
      say "DONE pull=VERIFIED manifest=$man package=SKIPPED (verdict not PASS) $verdict"
    fi
    exit 0
  fi
  sleep "$interval"
done
