#!/usr/bin/env bash
# Threshold-log replays (fp_log vs ld_log), one fit at a time; logs are deleted after analysis (they are ~0.1-0.5 GB).
set -uo pipefail
S=$(cd "$(dirname "$0")" && pwd); W=$HOME/api_audit_work
Rscript "$S/compile_test.R" "$W/core_fp_log" && Rscript "$S/compile_test.R" "$W/core_ld_log" || exit 1
for id in ${*:-1 2 3 4 5 6 7 8 9 10}; do
  Rscript "$S/valfp_fit.R" "$W/core_fp_log" thr "$id" "$W/out" 2>&1 | grep "^thr"
  Rscript "$S/valfp_fit.R" "$W/core_ld_log" thr "$id" "$W/out" 2>&1 | grep "^thr"
  ls -la "$W/out/thr$(printf %02d $id)_core_fp_log.bin" | awk '{print "bytes", $5}'
  python3 "$S/analyze_thr.py" "$W/out/thr$(printf %02d $id)_core_fp_log.bin" "$W/out/thr$(printf %02d $id)_core_ld_log.bin" "$id" >> "$W/thr_table.csv"
  rm -f "$W/out/thr$(printf %02d $id)_core_"*_log.bin
done
