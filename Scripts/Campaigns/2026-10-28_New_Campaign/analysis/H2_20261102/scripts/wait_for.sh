#!/bin/bash
# wait_for.sh MAXMIN : return when one of the H2 milestones changes (p1000 pull result line, notd old batch done, TD batch done, extraction done) or after MAXMIN minutes.
H2=/c/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign/analysis/H2_20261102
PL=/c/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign/ops/evidence/ops_pulls_20261102.txt
state() { echo "$(grep -c '' "$PL" 2>/dev/null) $(grep -c ALL_WORKERS_EXITED "$H2"/logs/*.launcher.log 2>/dev/null | awk -F: '{s+=$2} END {print s}')"; }
s0=$(state); end=$(( $(date +%s) + ${1:-60} * 60 ))
while [ "$(date +%s)" -lt "$end" ]; do
  sleep 60
  s=$(state); [ "$s" != "$s0" ] && { echo "CHANGED $s0 -> $s"; tail -3 "$PL"; grep -h ALL_WORKERS_EXITED "$H2"/logs/*.launcher.log; exit 0; }
done
echo "TIMEOUT $s0"
