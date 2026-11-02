#!/bin/bash
# prodh_poller.sh RUN_ID LOGFILE [MAX_MIN] : (laptop) PROD-H stop-rule poller (JOB.md 3 D). ONE ssh per poll, about 9 min apart
# (sleep 510 s + ssh time: inside the 5–10 min window, never more often than 5 min). Each poll runs runner/poll.py and counts the run's jobs in squeue.
# Exit codes (the caller acts on them):
#   0 ALL_LEFT_QUEUE   no job of the run in squeue (both primary arrays terminal) -> JOB.md E
#   3 URGENT           poll.py exit 3 / decision HOLD_FAILED -> manual scontrol hold per URGENT_HOLD_FAILED.md, tell HQ
#   4 HOLD             decision HOLD or STILL_HELD -> send HQ_REQUEST_*.md to HQ, wait
#   5 POLL_ERROR       poll.py exit 1 (ok false) or unparsable output -> inspect
#   6 P500_LEFT        the p500 array left the queue (reported once per run: flag file) -> copy pull of p0500
#   2 TIME_UP          MAX_MIN reached (default 110) -> restart the poller at once (keep the cadence)
# After an ssh failure: back off 15 min (charter); the next poll will be LATE and recorded by poll.py (explain to HQ).
set -u
RUN_ID=${1:?RUN_ID}; LOG=${2:?logfile}; MAX=${3:-110}
R=/home/fb31/projects/BVS/New_Campaign/runs/$RUN_ID
FLAG="${LOG%.log}.p500_left.flag"
# single instance (2026-10-30: a poller that T3 reported "stopped" was still alive and two ran in parallel, giving early polls):
# PID file next to the log; a live owner -> exit 7; a dead owner (T3 kill) is taken over.
PIDF="${LOG%.log}.poller.pid"
if [ -s "$PIDF" ] && kill -0 "$(cat "$PIDF")" 2>/dev/null; then echo "EXIT ALREADY_RUNNING pid $(cat "$PIDF") $(date -u +%FT%TZ)" >> "$LOG"; exit 7; fi
echo $$ > "$PIDF"; trap '[ "$(cat "$PIDF" 2>/dev/null)" = "$$" ] && rm -f -- "$PIDF"' EXIT
end=$(( $(date +%s) + MAX*60 ))
while [ "$(date +%s)" -lt "$end" ]; do
  out=$(MSYS_NO_PATHCONV=1 ssh -o BatchMode=yes -o ConnectTimeout=30 nots "python3 $R/runner/poll.py $R; echo POLL_RC=\$?; echo RUNJOBS=\$(squeue -h -u fb31 -o '%j' | grep -c $RUN_ID); echo P500JOBS=\$(squeue -h -u fb31 -o '%j' | grep -c ${RUN_ID}_p500)" 2>&1); rc=$?
  ts=$(date -u +%FT%TZ)
  { echo "### $ts ssh_rc=$rc"; printf '%s\n' "$out"; } >> "$LOG"
  if [ $rc -ne 0 ]; then echo "BACKOFF $ts ssh failed rc=$rc: 15 min" >> "$LOG"; sleep 900; continue; fi
  prc=$(printf '%s\n' "$out" | sed -n 's/^POLL_RC=//p'); rj=$(printf '%s\n' "$out" | sed -n 's/^RUNJOBS=//p'); p5j=$(printf '%s\n' "$out" | sed -n 's/^P500JOBS=//p')
  dec=$(printf '%s\n' "$out" | grep -o '"decision": "[A-Z_a-z]*"' | head -1 | sed 's/.*: "//; s/"//')
  fin=$(printf '%s\n' "$out" | grep -o '"finished": [0-9]*' | head -1 | sed 's/.*: //')
  echo "SUMMARY $ts poll_rc=$prc decision=${dec:-?} finished=${fin:-?} run_jobs=$rj p500_jobs=$p5j" >> "$LOG"
  [ "$prc" = 3 ] || [ "$dec" = HOLD_FAILED ] && { echo "EXIT URGENT" >> "$LOG"; exit 3; }
  [ "$dec" = HOLD ] || [ "$dec" = STILL_HELD ] && { echo "EXIT HOLD" >> "$LOG"; exit 4; }
  { [ "$prc" != 0 ] || [ -z "$dec" ]; } && { echo "EXIT POLL_ERROR" >> "$LOG"; exit 5; }
  [ "$rj" = 0 ] && { echo "EXIT ALL_LEFT_QUEUE" >> "$LOG"; exit 0; }
  if [ "$p5j" = 0 ] && [ ! -e "$FLAG" ]; then date -u +%FT%TZ > "$FLAG"; echo "EXIT P500_LEFT" >> "$LOG"; exit 6; fi
  sleep 510
done
echo "EXIT TIME_UP $(date -u +%FT%TZ)" >> "$LOG"; exit 2
