#!/bin/bash
# Same job list as run_pilots.sh, reverse order (second runner; pilot_sim.py skips finished configurations).
cd "$(dirname "$0")"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
NP=${1:-3}
{
for n in 800 1600 3200; do for s in 3 4 6 1; do for p in 500 1000; do for r in 0 1; do echo "$s $p 1.0 $n $r"; done; done; done; done
for n in 1600 3200; do for s in 3 4; do for r in 0 1; do echo "$s 500 0.5 $n $r"; done; done; done
for s in 3 4; do echo "$s 500 1.0 6400 0"; done
} | tac | xargs -P "$NP" -L 1 sh -c 'python3 pilot_sim.py ../results/pilot.jsonl $0 $1 $2 $3 $4 >> ../results/pilot.log 2>&1'
