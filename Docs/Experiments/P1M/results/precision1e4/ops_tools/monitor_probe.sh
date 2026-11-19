#!/usr/bin/env bash
# monitor_probe.sh <WAVE> -- PRECISION LEG. ONE ssh to NOTS = ONE squeue + ONE sacct -X (POLICIES §12: <= 1 per 5 min, normally every 20-30 min), plus plain
# reads of the wave's run dirs (submissions, data / truth hashes, calib settings, island T, cost_diag names, bin sha, OUTCOME / resource_limit hits).
# Batches of the wave = PL_<WAVE>_<i> found in $STG/current/scripts (the overlap's regexp OV_<wave>_(T|V)2? is replaced by PL_<wave>_<i>).
# Saves the raw probe to $STG/monitor/<WAVE>/probe_<UTC>.txt and prints the verdict of stop_rules_prec.py (exit 0 = no stop, 3 = STOP).
# Env: QUOTE=<core-h> (re-quote of the wave; default = the committed LEG_PLAN §4 quote), MAKE_CALIB_META=1 (A0 / read-backs: one nice'd `info` per finished
# calibration writes calib_meta.json in scratch), PRIOR=<json {run_id: core_h}> (spent in earlier waves), CUM_STOP, WITH_HELD.
set -euo pipefail; . "$(dirname "$0")/common.sh"
WAVE=${1:?WAVE}; OUT=$STG/monitor/$WAVE; mkdir -p "$OUT"; P=$OUT/probe_$(date -u +%Y%m%dT%H%M%SZ).txt
BL=${BATCHES:-$(batches_of "$STG/current/scripts" "$WAVE")}; [[ -n $BL ]] || { echo "no PL_${WAVE}_* batches" >&2; exit 64; }
ssh $NOTS "bash -s -- $D $WAVE ${MAKE_CALIB_META:-0} $BL" < "$(dirname "$0")/probe_remote.sh" > "$P"
python3 "$(dirname "$0")/stop_rules_prec.py" "$P" --wave "$WAVE" --plans "$STG/current/scripts" --leg-log "$LEG_LOG" ${QUOTE:+--quote $QUOTE} ${PRIOR:+--prior $PRIOR} ${CUM_STOP:+--cum-stop $CUM_STOP} ${WITH_HELD:+--with-held}
