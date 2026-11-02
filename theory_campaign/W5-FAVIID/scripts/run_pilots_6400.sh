#!/bin/bash
# n = 6400 (and 12800 for S3) pilot runs, appended after the main batch (seed index 5/6 in pilot_sim.NS).
cd "$(dirname "$0")"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
{ for s in 1 3 4 6; do for p in 500 1000; do for r in 0 1; do echo "$s $p 1.0 6400 $r"; done; done; done
  echo "3 500 1.0 12800 0"; echo "4 500 1.0 12800 0"; } | xargs -P 4 -L 1 sh -c 'python3 pilot_sim.py ../results/pilot.jsonl $0 $1 $2 $3 $4 >> ../results/pilot.log 2>&1'
