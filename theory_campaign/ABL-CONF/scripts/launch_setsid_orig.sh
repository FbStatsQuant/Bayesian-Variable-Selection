#!/bin/bash
# launch.sh [njobs=3] -- start ABL-CONF worker jobs FULLY DETACHED (setsid nohup ... < /dev/null &), each one
# `owls_run -j 2` running scripts/run_queue.sh (2 single-threaded fit workers). Run from the RUN checkout
# (/home/fb31/ablconf_work/checkout), never from a T3 worktree that may be removed.
cd "$(dirname "$0")/.."
export ABL_WORK=${ABL_WORK:-/home/fb31/ablconf_work}; W=$ABL_WORK; mkdir -p $W/launch
N=${1:-3}
for i in $(seq 1 $N); do
  out=$W/launch/job_$(date +%Y%m%d-%H%M%S)_$i.out
  setsid nohup ~/.config/bvs-hq/owls/owls_run -j 2 -- bash scripts/run_queue.sh results/queue.txt < /dev/null > $out 2>&1 &
  echo "$(date -Is) launched owls_run wrapper pid $! log $out" | tee -a $W/launch/launches.log
  sleep 5
done
sleep 3; grep -E "START|REFUSED" ~/.config/bvs-hq/owls/jobs.log | tail -$N
