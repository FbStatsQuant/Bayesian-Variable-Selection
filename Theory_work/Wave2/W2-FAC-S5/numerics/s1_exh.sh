#!/bin/bash
# S1-EXH: complete scans (every flip and EVERY swap pair) on exact S5 paths; certifies the full uncapped LS0 path.
cd "$(dirname "$0")"
for seed in 1 2 3; do for pn in "200 1e6" "200 1e10" "500 1e6" "500 1e8" "500 1e12"; do
  set -- $pn; py -3.13 s1_path.py $1 $2 $seed 5 .3 .7 4 1.0 exh > "s1_exh/S1X_$1_$2_$seed.json" 2>/dev/null &
  while [ "$(jobs -rp | wc -l)" -ge 6 ]; do sleep 1; done
done; done; wait
