#!/bin/bash
# W3-SCR: run a task list of scr_fit.R fits with P parallel workers. Usage: run_tasks.sh TASKS OUTDIR LOGDIR P
TASKS=$1; OUTDIR=$2; LOGDIR=$3; P=${4:-6}
i=0
while read -r line; do
  i=$((i+1)); echo "$i $line"
done < "$TASKS" | xargs -P "$P" -L 1 bash -c 'id=$0; shift 0; Rscript --vanilla scr_fit.R core_copy '"$OUTDIR"'/task_$id.jsonl "$@" > '"$LOGDIR"'/task_$id.log 2>&1'
echo DONE
