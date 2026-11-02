#!/bin/bash
# pilot_summarize.sh STAMP : (laptop) JOB.md section 9/10: summarize_pilot.R on the downloaded results and logs (local R 4.4.1). Exit = summarizer's (0 accepted, 2 FAIL, 3 INCOMPLETE).
set -u
STAMP=${1:?STAMP}; PID="${STAMP}_lowp_pilot"
D="C:/Users/felip/OneDrive - Rice University/NOTS Data/New_Campaign"
CAMPW=C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign
RS="C:/Program Files/R/R-4.4.1/bin/Rscript.exe"
RES=""
for f in enum20 enum30 scale_t08 scale_t16 scale_t32 smc bench; do RES="$RES${RES:+,}$D/results/${PID}_$f"; done
"$RS" "$CAMPW/code/lowp/pilot/summarize_pilot.R" --results "$RES" --logs "$D/logs/$PID" --out "$CAMPW/code/lowp/pilot/summary_$PID" --rscript "$RS" \
  > "$CAMPW/ops/evidence/ops4_pilot_${STAMP}_summarize.txt" 2>&1
rc=$?
echo "summarize_rc=$rc" >> "$CAMPW/ops/evidence/ops4_pilot_${STAMP}_summarize.txt"
tail -40 "$CAMPW/ops/evidence/ops4_pilot_${STAMP}_summarize.txt"
exit $rc
