#!/bin/bash
# Owls (2 cores via owls_run): 3 designs, sequential. Usage: owls_run -j 2 -- bash scripts/run_owls.sh
cd "$(dirname "$0")/.."
for spec in "p0500_S1_r001 c100" "p0500_S4_r001 c050" "p0500_S5_r002 c100"; do
  set -- $spec
  Rscript scripts/ma_fit.R $1 $2 results/fit_$1_$2.rds 32 >> results/run_owls.log 2>&1
done
