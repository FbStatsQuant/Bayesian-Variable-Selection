#!/bin/bash
# relaunch.sh -- re-launch missing ABL-CONF fits after jobs died (server restart, reboot, kill).
# 1. releases stale claims (owner worker pid no longer alive), 2. launches (3 - live jobs) new detached jobs.
# Fits with a status file (completed / capped / failed) are never re-run. Safe to run while jobs are alive.
cd "$(dirname "$0")/.."; W=${ABL_WORK:-/home/fb31/ablconf_work}
for c in $W/claims/*/; do
  [ -d "$c" ] || continue; pid=$(awk '{print $2}' $c/owner 2>/dev/null)
  if [ -z "$pid" ] || ! grep -q run_queue /proc/$pid/cmdline 2>/dev/null; then
    echo "$(date -Is) releasing stale claim $(basename $c) (owner pid $pid gone)" | tee -a $W/killed.log; rm -rf "$c"
  fi
done
live=$(ps -u fb31 -o args | grep "[o]wls_run.*run_queue.sh" | wc -l)
need=$(( 3 - live )); left=$(( $(grep -vc "^#" results/queue.txt) - $(ls $W/status | wc -l) ))
echo "live jobs: $live  fits without terminal outcome: $left"
[ $need -gt 0 ] && [ $left -gt 0 ] && bash scripts/launch.sh $need || echo "nothing to launch"
