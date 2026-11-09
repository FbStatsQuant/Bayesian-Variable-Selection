#!/bin/bash
# S1 grid: S5 design, uncapped LS0 path from the full model; one output file per run (no concurrent appends).
cd "$(dirname "$0")"
run() { py -3.13 s1_path.py "$@" > "s1_out/S1_$(echo "$@" | tr ' ' '_').json" 2> /dev/null; }
for seed in 1 2 3; do
  for pn in "500 1e6" "500 1e8" "500 1e12" "2000 1e6" "2000 1e8" "2000 1e12" "2000 1e4 5 .3 .7 4 3" "2000 4001 5 .3 .7 4 3" "500 1001 5 .3 .7 4 3"; do
    set -- $pn; run $1 $2 $seed ${@:3} &
    while [ "$(jobs -rp | wc -l)" -ge 6 ]; do sleep 1; done
  done
done
wait
