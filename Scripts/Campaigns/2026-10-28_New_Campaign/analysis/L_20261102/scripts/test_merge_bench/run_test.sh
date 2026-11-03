#!/bin/bash
# run_test.sh : Sol R1 finding-1 test. Scores chunk_00 and chunk_01 (theory off) with enum20 + the synthetic benchmark root, then checks the filter.
A=/c/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign
L=$A/analysis/L_20261102; W=$L/work/test_bench
STUDY="/c/Users/felip/OneDrive - Rice University/NOTS Data/New_Campaign/inputs/lowp_study"
R="/c/Program Files/R/R-4.4.1/bin/Rscript.exe"
# Windows-form paths: MSYS converts only the first /c/ path of a comma-separated argument
ROOTS="C:/Users/felip/OneDrive - Rice University/NOTS Data/New_Campaign/results/20261030T1811Z_lowp_enum20,C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign/analysis/L_20261102/work/test_bench/synth_root"
for k in 00 01; do
  "$R" "$A/code/scoring/run_scoring.R" --study "$STUDY" --results "$ROOTS" --out "$W/out_$k" --cases "$L/work/chunks/chunk_$k.txt" \
       --theory 0 --core "$A/code/core/v2_2_1/core" > "$W/out_$k.log" 2>&1 || { echo "scoring chunk $k failed"; exit 1; }
done
"$R" "$L/scripts/test_merge_bench/check_own_filter.R" "$W" "$L/work/chunks"
