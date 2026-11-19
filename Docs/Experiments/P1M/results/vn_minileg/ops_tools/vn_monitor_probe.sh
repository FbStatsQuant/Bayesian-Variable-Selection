#!/usr/bin/env bash
# vn_monitor_probe.sh <WAVE> -- V-N mini-leg. ONE ssh to NOTS = ONE squeue + ONE sacct -X (<= 1 probe per 5 min, normally 20-30), plus plain reads of the wave's run dirs.
# Batches of the wave = VN_<WAVE>_<i> in $STG/current/scripts (V-O3 regexp: VN_V[0-2]_[0-9]+). Raw probe -> $STG/monitor/<WAVE>/probe_<UTC>.txt; verdict of stop_rules_vn.py
# (exit 0 = no stop, 3 = STOP; prints `WAVE STATE: RUNNING|ENDED`). Env: QUOTE=<core-h> (a re-quote; default the committed 50 / 75 / 125), MAKE_CALIB_META=1 (V0 and read-backs: one nice'd
# `smcbvs4 info` per finished calibration writes calib_meta.json in scratch: needed for the arm and the PAIRING identity), PRIOR=<json run_id -> core-h of earlier mini-leg waves>, SOFT_OVERRIDES.
set -euo pipefail; . "$(dirname "$0")/common.sh"
WAVE=${1:?WAVE}; OUT=$STG/monitor/$WAVE; mkdir -p "$OUT"; P=$OUT/probe_$(date -u +%Y%m%dT%H%M%SZ).txt
BL=${BATCHES:-$(batches_of "$STG/current/scripts" "$WAVE")}; [[ -n $BL ]] || { echo "no VN_${WAVE}_* batches" >&2; exit 64; }
ssh $NOTS "bash -s -- $D $WAVE ${MAKE_CALIB_META:-0} $BL" < "$(dirname "$0")/vn_probe_remote.sh" > "$P"
python3 "$(dirname "$0")/stop_rules_vn.py" "$P" --wave "$WAVE" --plans "$STG/current/scripts" --deploy-log "$LOG" ${QUOTE:+--quote $QUOTE} ${PRIOR:+--prior $PRIOR}
