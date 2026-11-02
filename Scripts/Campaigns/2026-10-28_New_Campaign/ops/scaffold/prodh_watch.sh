#!/bin/bash
# prodh_watch.sh LOGFILE [MAX_MIN] : (laptop, LOCAL ONLY, no ssh) wake-up watcher for a DETACHED prodh_poller.sh.
# Checks the poll log every 60 s. Exits:
#   0 the poller wrote a new EXIT line (printed: ALL_LEFT_QUEUE / URGENT / HOLD / POLL_ERROR / P500_LEFT / TIME_UP / ALREADY_RUNNING)
#   9 the poller process is gone without an EXIT line (killed): restart the detached poller
#   2 MAX_MIN (default 110) reached: restart this watcher only (the poller keeps running)
set -u
LOG=${1:?logfile}; MAX=${2:-110}
PIDF="${LOG%.log}.poller.pid"
n0=$(grep -c '^EXIT' "$LOG" 2>/dev/null || echo 0)
end=$(( $(date +%s) + MAX*60 ))
while [ "$(date +%s)" -lt "$end" ]; do
  n=$(grep -c '^EXIT' "$LOG" 2>/dev/null || echo 0)
  if [ "$n" -gt "$n0" ]; then grep '^EXIT' "$LOG" | tail -1; grep '^SUMMARY' "$LOG" | tail -1; exit 0; fi
  if [ ! -s "$PIDF" ] || ! kill -0 "$(cat "$PIDF")" 2>/dev/null; then
    sleep 5; n=$(grep -c '^EXIT' "$LOG" 2>/dev/null || echo 0)
    [ "$n" -gt "$n0" ] && { grep '^EXIT' "$LOG" | tail -1; exit 0; }
    echo "POLLER_GONE $(date -u +%FT%TZ) (no EXIT line)"; grep '^SUMMARY' "$LOG" | tail -1; exit 9
  fi
  sleep 60
done
echo "WATCH_TIME_UP $(date -u +%FT%TZ)"; grep '^SUMMARY' "$LOG" | tail -1; exit 2
