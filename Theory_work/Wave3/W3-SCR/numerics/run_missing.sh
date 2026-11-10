#!/bin/bash
# W3-SCR: rerun the tasks of a task list whose output file is missing (after an interruption). Usage: run_missing.sh TASKS OUTDIR LOGDIR P
TASKS=$1; OUTDIR=$2; LOGDIR=$3; P=${4:-5}
i=0
while read -r line; do
  i=$((i+1)); [ -s "$OUTDIR/task_$i.jsonl" ] || echo "$i $line"
done < "$TASKS" | xargs -P "$P" -L 1 bash -c 'id=$0; Rscript --vanilla scr_fit.R core_copy '"$OUTDIR"'/task_$id.jsonl "$@" > '"$LOGDIR"'/task_$id.log 2>&1'
echo DONE
