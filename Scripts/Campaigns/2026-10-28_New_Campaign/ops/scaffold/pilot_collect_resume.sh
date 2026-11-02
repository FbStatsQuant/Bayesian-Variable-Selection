#!/bin/bash
# pilot_collect_resume.sh STAMP WAIT_S FOLDER... : (laptop) resume a collection after an ssh timeout: wait WAIT_S seconds (charter back-off),
# then nots_pull.py <folder> --delete for each listed results suffix (e.g. scale_t32 smc bench) and the word "logs" for the logs folder.
# Sequential, one connection each; stops at the first failure. Appends to ops/evidence/ops4_pilot_<STAMP>_collect.txt.
set -u
STAMP=${1:?STAMP}; WAIT=${2:?wait seconds}; shift 2
PID="${STAMP}_lowp_pilot"; S=/scratch/fb31/New_Campaign
EV=/c/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign/ops/evidence/ops4_pilot_${STAMP}_collect.txt
PULL=C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign/ops/transfer/nots_pull.py
echo "RESUME $(date -u +%FT%TZ) waiting ${WAIT}s then: $*" | tee -a "$EV"
sleep "$WAIT"
for f in "$@"; do
  if [ "$f" = logs ]; then R=$S/logs/$PID; else R=$S/results/${PID}_$f; fi
  MSYS_NO_PATHCONV=1 py -3 "$PULL" "$R" --delete 2>&1 | tee -a "$EV"
  [ "${PIPESTATUS[0]}" -eq 0 ] || { echo "PULL FAILED for $f: stopping" | tee -a "$EV"; exit 1; }
done
echo "COLLECT_DONE $(date -u +%FT%TZ)" | tee -a "$EV"
