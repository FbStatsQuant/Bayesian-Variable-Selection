#!/usr/bin/env bash
# gc_wave_check_run.sh <WAVE> -- the H-48 wave check end to end: (1) ship gc_ess_nots.py to NOTS scratch and run it DETACHED (nice 19, read-only seeks of st_phi / st_ess / grid of the wave's island files; nothing is written to the runs),
# (2) poll with ONE light ssh per ~2.5 min until it is done, (3) fetch the small JSON, (4) run gc_wave_check.py on the collected records (records/gc1m/<batch>) -> wave_check_<W>.md + .json in $OUT (staging/gc1m/wave_check/<W>).
# Needs the wave COLLECTED first (records/gc1m/<batch>/<run_id>/ with eval.bin.json, calib_meta.json). Exit 2 = FLAG: STOP (low_ESS with an E-flag / sigma-hat > 0.5 / C2 failure / HPM != S0).
set -euo pipefail; . "$(dirname "$0")/common.sh"
WAVE=${1:?WAVE}; BL=${BATCHES:-$(batches_of "$SCRIPTS" "$WAVE")}; OUT=$STG/wave_check/$WAVE; mkdir -p "$OUT"
ssh $NOTS "cat > $D/scratch/gc_ess_nots.py" < "$(dirname "$0")/gc_ess_nots.py"
RD=""; for b in $BL; do RD="$RD $D/scratch/runs/$b/6-*/"; done
ssh $NOTS "setsid nohup bash -c 'cd $D/scratch && nice -n 19 python3 -I gc_ess_nots.py $RD > gc_ess_$WAVE.json 2> gc_ess_$WAVE.err; echo \$? > gc_ess_$WAVE.rc' > /dev/null 2>&1 < /dev/null & echo started"
for i in $(seq 1 40); do sleep 150; rc=$(ssh $NOTS "cat $D/scratch/gc_ess_$WAVE.rc 2>/dev/null" 2>/dev/null | tail -1 || true); [[ -n $rc ]] && break; done
[[ ${rc:-} == 0 ]] || { echo "ESS extraction on NOTS failed or timed out (rc '${rc:-}'): see $D/scratch/gc_ess_$WAVE.err" >&2; exit 1; }
rs $NOTS:$D/scratch/gc_ess_$WAVE.json "$OUT/ess_$WAVE.json"
RECS=""; for b in $BL; do RECS="$RECS $OWLS_REC/$b"; done
python3 "$(dirname "$0")/gc_wave_check.py" --wave "$WAVE" --records-dir $RECS --ess-json "$OUT/ess_$WAVE.json" --out-dir "$OUT"
