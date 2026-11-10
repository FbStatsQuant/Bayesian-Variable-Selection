#!/bin/bash
# W3-SCR: run the given task ids (in the given order) of a task list, skipping at job start any task whose output exists.
# Usage: run_ordered.sh TASKS OUTDIR LOGDIR P id1 id2 ...
TASKS=$1; OUTDIR=$2; LOGDIR=$3; P=$4; shift 4
for i in "$@"; do echo "$i $(sed -n "${i}p" "$TASKS")"; done | xargs -P "$P" -L 1 bash -c 'id=$0; [ -s '"$OUTDIR"'/task_$id.jsonl ] || Rscript --vanilla scr_fit.R core_copy '"$OUTDIR"'/task_$id.jsonl "$@" > '"$LOGDIR"'/task_$id.log 2>&1'
echo DONE
