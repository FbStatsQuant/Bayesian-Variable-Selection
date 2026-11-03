#!/bin/bash
# wait_td.sh MAXMIN : exit 0 when the TD batch reports ALL_WORKERS_EXITED; exit 3 when no new TD row for 20 min (stall/death); exit 4 at MAXMIN.
H2=/c/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign/analysis/H2_20261102
D=$H2/theory/rows_td0_old; LOG=$H2/logs/theory_td0old.launcher.log
end=$(( $(date +%s) + ${1:-90} * 60 )); last=$(ls "$D" | grep -c 'csv$'); t_last=$(date +%s)
while [ "$(date +%s)" -lt "$end" ]; do
  grep -q ALL_WORKERS_EXITED "$LOG" && { echo "DONE $(ls "$D" | grep -c 'csv$') rows, $(ls "$D" | grep -c 'err$') err"; exit 0; }
  n=$(ls "$D" | grep -c 'csv$'); [ "$n" != "$last" ] && { last=$n; t_last=$(date +%s); }
  [ $(( $(date +%s) - t_last )) -gt 1200 ] && { echo "STALL at $n rows (no new row for 20 min)"; exit 3; }
  sleep 60
done
echo "TIMEOUT at $last rows"; exit 4
