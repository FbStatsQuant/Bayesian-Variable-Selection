#!/bin/bash
# wait_for_line.sh FILE REGEX PIDFILE [MAX_MIN] : (laptop, local only) wait until FILE contains a line matching REGEX (exit 0, prints it), or the
# process in PIDFILE is gone without it (exit 9), or MAX_MIN (default 60) passes (exit 2). Checks every 30 s.
set -u
F=${1:?file}; RX=${2:?regex}; P=${3:?pidfile}; MAX=${4:-60}
end=$(( $(date +%s) + MAX*60 ))
while [ "$(date +%s)" -lt "$end" ]; do
  if grep -qE "$RX" "$F" 2>/dev/null; then grep -E "$RX" "$F" | tail -1; exit 0; fi
  q=$(cat "$P" 2>/dev/null); if [ -n "$q" ] && ! kill -0 "$q" 2>/dev/null; then sleep 3; grep -qE "$RX" "$F" 2>/dev/null && { grep -E "$RX" "$F" | tail -1; exit 0; }; echo "GONE pid $q"; exit 9; fi
  sleep 30
done
echo "TIME_UP"; exit 2
