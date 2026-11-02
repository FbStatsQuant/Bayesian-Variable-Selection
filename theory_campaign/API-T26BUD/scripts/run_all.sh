#!/bin/bash
# Sweep for realised_T.py; run inside owls_run (uses OWLS_JOB_CORES parallel processes). Output: results/realised_T.jsonl
cd "$(dirname "$0")/.."
for seed in 0 1 2 3 4 5; do for n in 160 320 640 1280 2560 5120 10240 40960; do for des in fav_iid fav_cor masked orth; do
  echo "$des $n $seed"; done; done; done |
xargs -P "${OWLS_JOB_CORES:-1}" -L 1 bash -c 'python3 scripts/realised_T.py "$0" "$1" "$2" >> results/realised_T.jsonl 2>> results/realised_T.err'
