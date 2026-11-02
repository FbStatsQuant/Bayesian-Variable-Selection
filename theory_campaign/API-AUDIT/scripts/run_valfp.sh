#!/usr/bin/env bash
# Whole VAL-FP pipeline as ONE sequential job (one owls_run slot): compile both cores, then for each fit id:
# production fp fit, ld replay of the final run on the fp frozen C, ld full fit. Usage: bash run_valfp.sh [ids...]
set -uo pipefail
S=$(cd "$(dirname "$0")" && pwd); W=$HOME/api_audit_work
IDS=${*:-1 2 3 4 5 6 7 8 9 10}
Rscript "$S/compile_test.R" "$W/core_fp" && Rscript "$S/compile_test.R" "$W/core_ld" || exit 1
for id in $IDS; do
  Rscript "$S/valfp_fit.R" "$W/core_fp" fp "$id" "$W/out" 2>&1 | tail -1
  Rscript "$S/valfp_fit.R" "$W/core_ld" ld_replay "$id" "$W/out" 2>&1 | tail -1
  Rscript "$S/valfp_fit.R" "$W/core_ld" ld_full "$id" "$W/out" 2>&1 | tail -1
done
