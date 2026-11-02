#!/bin/bash
# Pilot batch for goal 4. Each line: scen p scale n rep. Output: ../results/pilot.jsonl (one JSON line per run).
# Usage: bash run_pilots.sh NPROC
cd "$(dirname "$0")"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
NP=${1:-2}
{
for n in 800 1600 3200; do for s in 3 4 6 1; do for p in 500 1000; do for r in 0 1; do echo "$s $p 1.0 $n $r"; done; done; done; done
for n in 1600 3200; do for s in 3 4; do for r in 0 1; do echo "$s 500 0.5 $n $r"; done; done; done
for s in 3 4; do echo "$s 500 1.0 6400 0"; done
} | xargs -P "$NP" -L 1 sh -c 'python3 pilot_sim.py ../results/pilot.jsonl $0 $1 $2 $3 $4 >> ../results/pilot.log 2>&1'
