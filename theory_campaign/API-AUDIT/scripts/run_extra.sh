#!/usr/bin/env bash
# GUARD checks (fp_nullguard, fp_stop) and multi-seed final-run replays (fp_seeds, ld_seeds) for fits 1..10.
set -uo pipefail
S=$(cd "$(dirname "$0")" && pwd); W=$HOME/api_audit_work
for id in ${*:-1 2 3 4 5 6 7 8 9 10}; do
  for m in fp_nullguard fp_stop fp_seeds; do Rscript "$S/valfp_fit.R" "$W/core_fp" $m "$id" "$W/out" 2>&1 | tail -1; done
  Rscript "$S/valfp_fit.R" "$W/core_ld" ld_seeds "$id" "$W/out" 2>&1 | tail -1
done
