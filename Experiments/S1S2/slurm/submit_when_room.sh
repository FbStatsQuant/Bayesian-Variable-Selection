#!/usr/bin/env bash
# submit_when_room.sh -- run on OWLS as a systemd USER unit. Submits ONE benchmark batch class by class, each class only
# once fb31's queued+running array tasks on NOTS leave room for it under MaxSubmitPU (5000, minus a margin), then
# launches the batch's watcher (watch_batch.sh) once every class is in. For batches too large to submit at once
# (S2 asi b3 = 4,800 tasks, owner release 2026-11-27, while b2's 4,200 are queued).
#   submit_when_room.sh --suite S --method M --batch K --reps LO-HI --classes C1,C2 [--margin 100] [--interval 600]
#                       [--watch-log LOG] [--owner-ok-asi-full]
# Each submission is submit_bench.sh ... --classes C --go on NOTS (all its checks apply: budget hard stop, hold, the
# live-class refusal, MaxSubmitPU). A failed submission is logged and retried at the next interval; it never cancels.
# Logs lines "DEFER ..." to stdout (systemd-run appends them to the watch log's sibling, see the launch below).
#   systemd-run --user --unit=s1s2-defer-s2bm-asi-b3-$(date +%Y%m%d-%H%M%S) --collect --quiet \
#     -p StandardOutput=append:$LOGDIR/S1S2_defer_s2bm_asi_b3.log -p StandardError=append:$LOGDIR/S1S2_defer_s2bm_asi_b3.log \
#     <this script> --suite 2 --method asi --batch 3 --reps 61-100 --classes S2N50P1000,S2N100P1000 --owner-ok-asi-full \
#     --watch-log $LOGDIR/S1S2_watch_s2bm_asi_b3.log
set -uo pipefail
HERE=$(cd "$(dirname "$0")" && pwd)
NSL=/home/fb31/SMC-BVS/_local/engineering/S1S2/deploy/S1S2/slurm
CAP=5000; margin=100; interval=600; suite=""; method=""; batch=""; reps=""; classes=""; wlog=""; ownerok=""
while (( $# )); do case "$1" in
  --suite) suite="$2"; shift 2;; --method) method="$2"; shift 2;; --batch) batch="$2"; shift 2;;
  --reps) reps="$2"; shift 2;; --classes) classes="$2"; shift 2;; --margin) margin="$2"; shift 2;;
  --interval) interval="$2"; shift 2;; --watch-log) wlog="$2"; shift 2;; --owner-ok-asi-full) ownerok="--owner-ok-asi-full"; shift;;
  *) echo "unknown argument $1" >&2; exit 2;; esac; done
[[ -n "$suite" && -n "$method" && -n "$batch" && -n "$reps" && -n "$classes" ]] || { echo "need --suite --method --batch --reps --classes" >&2; exit 2; }
say() { echo "DEFER $(date -u +%FT%TZ) s${suite}bm_${method}_b${batch} $*"; }
IFS=, read -ra CL <<< "$classes"
say "start pid=$$ classes=$classes margin=$margin interval=${interval}s"
for c in "${CL[@]}"; do
  while :; do
    # tasks this class adds = the batch's reps x the class's settings, read from submit_bench.sh's own dry run
    dry=$(ssh -o ConnectTimeout=60 nots "cd $NSL && nice ./submit_bench.sh --suite $suite --method $method --batch $batch --reps $reps --classes $c" 2>&1)
    need=$(sed -nE "s/^# S$suite $method batch $batch: ([0-9]+) tasks.*/\1/p" <<< "$dry" | tail -1)
    q=$(ssh -o ConnectTimeout=60 nots 'squeue -u fb31 -h -r | wc -l' 2>/dev/null)
    if [[ "$need" =~ ^[0-9]+$ && "$q" =~ ^[0-9]+$ ]] && (( q + need <= CAP - margin )); then
      out=$(ssh -o ConnectTimeout=60 nots "cd $NSL && nice ./submit_bench.sh --suite $suite --method $method --batch $batch --reps $reps --classes $c $ownerok --go" 2>&1); rc=$?
      ids=$(sed -nE 's/^SUBMITTED ([0-9]+).*/\1/p' <<< "$out" | paste -sd, -)
      if (( rc == 0 )) && [[ -n "$ids" ]]; then say "SUBMITTED class $c tasks=$need queued_before=$q jobs=$ids"; break; fi
      say "submit of class $c FAILED rc=$rc: $(grep -E 'FATAL|REFUSED' <<< "$out" | head -2 | tr '\n' ' ')"
    else
      say "waiting: class $c needs $need, queued+running $q, cap $CAP - margin $margin"
    fi
    sleep "$interval"
  done
done
if [[ -n "$wlog" ]]; then
  systemd-run --user --unit="s1s2-watch-s${suite}bm-${method}-b${batch}-$(date +%Y%m%d-%H%M%S)" --collect --quiet \
    -p StandardOutput=append:"$wlog" -p StandardError=append:"$wlog" \
    "$HERE/watch_batch.sh" --suite "$suite" --method "$method" --batch "$batch" --reps "$reps" --interval 900 --log "$wlog" \
    && say "all classes in; watcher launched (log $wlog)" || say "all classes in; watcher launch FAILED"
else say "all classes in; no --watch-log, launch the watcher by hand"; fi
