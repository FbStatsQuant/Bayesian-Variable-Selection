#!/bin/sh
# Final-run simulations (Theorem A (A-0) bound check). Output: results/smc_sim.jsonl
cd "$(dirname "$0")"
OUT=../results/smc_sim.jsonl
: > $OUT
for args in "fav_iid 320 0 10 2500" "fav_iid 5120 7 10 2500" "fav_cor 5120 0 10 2500" "fav_cor 163840 5 10 2500" \
            "masked 640 0 10 2500" "masked 5120 0 10 2500" "fav_iid 320 0 40 50" "fav_cor 5120 0 40 50" "masked 5120 0 40 50"; do
  python3 smc_sim.py $args 2>/dev/null >> $OUT
done
