#!/bin/bash
# run_queue.sh <queue_file> -- run each line "<id> <sk> <arm>" with abl_fit.R, 2 at a time (OWLS_JOB_CORES).
# Launch: owls_run -j 2 -- bash scripts/run_queue.sh results/queue_k.txt   (one fit = one single-threaded process)
cd "$(dirname "$0")"
W=${ABL_WORK:-/home/fb31/abl_work}; mkdir -p $W/fits $W/logs
P=${OWLS_JOB_CORES:-1}
grep -v '^#' "$1" | xargs -P $P -L 1 bash -c 'f='$W'/fits/$0_$1_$2.rds; [ -f $f ] || Rscript abl_fit.R $0 $1 $2 $f >> '$W'/logs/$0_$1_$2.log 2>&1; tail -1 '$W'/logs/$0_$1_$2.log >> '$W'/progress.log'
