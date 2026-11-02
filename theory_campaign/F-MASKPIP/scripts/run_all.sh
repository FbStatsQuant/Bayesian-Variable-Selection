#!/bin/bash
# Runs all settings, 3 at a time (<= 3 cores; BLAS threads pinned to 1). Output: results/raw/<setting>.jsonl
cd "$(dirname "$0")/.."
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
for d in masked masked8; do for g in G1 G2 G3; do for n in 640 5120; do for N in 2500 50; do
  r=$([ $N = 2500 ] && echo 20 || echo 40); echo "$d $n $N $g $r"; done; done; done; done |
  xargs -P 3 -L 1 bash -c 'python scripts/masked_sim.py $0 $1 $2 $3 $4 results/raw/$0_n$1_N$2_$3.jsonl >> results/raw/log.txt 2>&1'
