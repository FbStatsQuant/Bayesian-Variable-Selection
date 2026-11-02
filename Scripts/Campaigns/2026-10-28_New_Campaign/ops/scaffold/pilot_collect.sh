#!/bin/bash
# pilot_collect.sh STAMP : (laptop) JOB.md section 9 after all jobs are terminal.
#   1. one ssh: squeue (must show no lowp_p job), truth state, final_accounting.sh, list of result folders;
#   2. nots_pull.py <folder> --delete for each existing results folder, then the logs folder (one connection each, sha256-verified, sequential).
# Stops at the first failed pull (nothing else is deleted). Output to ops/evidence/ops4_pilot_<STAMP>_collect.txt.
set -u
STAMP=${1:?STAMP}; PID="${STAMP}_lowp_pilot"
CAMP=/c/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign
PULL=C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign/ops/transfer/nots_pull.py   # Windows path: py does not see /c/... under MSYS_NO_PATHCONV
EV=$CAMP/ops/evidence/ops4_pilot_${STAMP}_collect.txt
S=/scratch/fb31/New_Campaign
MSYS_NO_PATHCONV=1 ssh -o BatchMode=yes -o ConnectTimeout=30 nots "squeue -h -u fb31 -o '%i %j %T'; echo ===; stat -c '%a %n' /home/fb31/projects/BVS/New_Campaign/runs/$PID/study/truth /home/fb31/projects/BVS/New_Campaign/runs/$PID/study/dev/truth; tail -3 $S/logs/$PID/truthlock/WAVE_UNLOCK.txt; echo ===; bash /home/fb31/projects/BVS/New_Campaign/runs/$PID/code/lowp/pilot/final_accounting.sh $STAMP < /dev/null 2>&1 | tail -5; echo final_accounting_rc=\${PIPESTATUS[0]}; echo ===; ls -d $S/results/${PID}_* 2>&1; du -sk $S/results/${PID}_* $S/logs/$PID 2>&1" > "$EV" 2>&1
echo "precheck_ssh_rc=$?" >> "$EV"; cat "$EV"
nq=$(awk '/^===$/{exit} / lowp_p[0-9]/{c++} END{print c+0}' "$EV")   # squeue section only (before the first ===); job names are lowp_p<digit>_...
[ "$nq" -eq 0 ] || { echo "a pilot job is still queued ($nq): not collecting"; exit 2; }
for f in enum20 enum30 scale_t08 scale_t16 scale_t32 smc bench; do
  grep -qx "$S/results/${PID}_$f" "$EV" || { echo "MISSING results folder ${PID}_$f (not pulled)" | tee -a "$EV"; continue; }
  MSYS_NO_PATHCONV=1 py -3 "$PULL" "$S/results/${PID}_$f" --delete 2>&1 | tee -a "$EV"
  [ "${PIPESTATUS[0]}" -eq 0 ] || { echo "PULL FAILED for $f: stopping" | tee -a "$EV"; exit 1; }
done
MSYS_NO_PATHCONV=1 py -3 "$PULL" "$S/logs/$PID" --delete 2>&1 | tee -a "$EV"
[ "${PIPESTATUS[0]}" -eq 0 ] || { echo "PULL FAILED for logs: stopping" | tee -a "$EV"; exit 1; }
echo "COLLECT_DONE" | tee -a "$EV"
