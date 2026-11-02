#!/bin/bash
# watch_multi.sh MAX_MIN NAME LOG PIDFILE REGEX [NAME LOG PIDFILE REGEX ...] : (laptop, LOCAL ONLY, no ssh) wake-up watcher for detached monitors.
# Every 60 s, for each monitor: a NEW line matching REGEX in LOG (counted from the start of this watcher) -> print "EVENT <NAME>: <line>" and exit 0;
# its PID (PIDFILE) no longer alive and no new matching line -> print "GONE <NAME>" and exit 9. MAX_MIN reached -> exit 2 (restart only the watcher).
set -u
MAX=${1:?max_min}; shift
names=(); logs=(); pids=(); rx=(); base=()
while [ $# -ge 4 ]; do names+=("$1"); logs+=("$2"); pids+=("$3"); rx+=("$4"); shift 4; done
for i in "${!names[@]}"; do base[$i]=$(grep -cE "${rx[$i]}" "${logs[$i]}" 2>/dev/null || true); base[$i]=${base[$i]:-0}; done
end=$(( $(date +%s) + MAX*60 ))
while [ "$(date +%s)" -lt "$end" ]; do
  for i in "${!names[@]}"; do
    n=$(grep -cE "${rx[$i]}" "${logs[$i]}" 2>/dev/null || true); n=${n:-0}
    if [ "$n" -gt "${base[$i]}" ]; then echo "EVENT ${names[$i]}: $(grep -E "${rx[$i]}" "${logs[$i]}" | tail -1)"; exit 0; fi
    p=$(cat "${pids[$i]}" 2>/dev/null)
    if [ -z "$p" ] || ! kill -0 "$p" 2>/dev/null; then
      sleep 3; n=$(grep -cE "${rx[$i]}" "${logs[$i]}" 2>/dev/null || true); n=${n:-0}
      [ "$n" -gt "${base[$i]}" ] && { echo "EVENT ${names[$i]}: $(grep -E "${rx[$i]}" "${logs[$i]}" | tail -1)"; exit 0; }
      echo "GONE ${names[$i]} (pid ${p:-none}) $(date -u +%FT%TZ)"; exit 9
    fi
  done
  sleep 60
done
echo "WATCH_TIME_UP $(date -u +%FT%TZ)"; exit 2
