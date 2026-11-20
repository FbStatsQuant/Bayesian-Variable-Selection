#!/usr/bin/env bash
# vn_monitor_probe.sh <WAVE> -- V-N mini-leg. ONE ssh to NOTS = ONE squeue + ONE sacct -X (<= 1 probe per 5 min, normally 20-30), plus plain reads of the wave's run dirs.
# Batches of the wave = VN_<WAVE>_<i> in $STG/current/scripts (V-O3 regexp: VN_V[0-2]_[0-9]+). Raw probe -> $STG/monitor/<WAVE>/probe_<UTC>.txt; verdict of stop_rules_vn.py
# (exit 0 = no stop, 3 = STOP; prints `WAVE STATE: RUNNING|ENDED`). Env: QUOTE=<core-h> (a re-quote; default the committed 50 / 75 / 125), MAKE_CALIB_META=1 (V0 and read-backs: one nice'd
# `smcbvs4 info` per finished calibration writes calib_meta.json in scratch: needed for the arm and the PAIRING identity), PRIOR=<json run_id -> core-h of earlier mini-leg waves>, SOFT_OVERRIDES.
set -uo pipefail; . "$(dirname "$0")/common.sh"   # no -e: a remote/ssh failure must NOT abort before the verdict (it is recorded in the probe file and surfaced by stop_rules_vn.py)
WAVE=${1:?WAVE}; OUT=$STG/monitor/$WAVE; mkdir -p "$OUT"; P=$OUT/probe_$(date -u +%Y%m%dT%H%M%SZ).txt
BL=${BATCHES:-$(batches_of "$STG/current/scripts" "$WAVE")}; [[ -n $BL ]] || { echo "no VN_${WAVE}_* batches" >&2; exit 64; }
# The V1 / V0 probe truncations (ssh rc 255, empty stderr, after the same step; the ssh ControlMaster was found re-created right after) showed that the ssh session itself can be cut while the remote work is
# still running. So the probe script is shipped (stdin -> file, fully read first: nothing can eat it any more), run DETACHED from the connection (setsid nohup: survives a dropped session) into
# $D/scratch/probe_out_<WAVE>.txt (one file per wave, overwritten), and `cat`ed in the same ssh. If that ssh returns non-zero or the output is incomplete, ONE cheap re-fetch (cat of the finished
# file, no squeue/sacct/info re-run) is made after 15 s; both statuses are recorded in the probe file.
OUTF="$D/scratch/probe_out_${WAVE}.txt"; MC=${MAKE_CALIB_META:-0}; NEED=ENGINE_FLAGS
rc=0; ssh $NOTS "cat > $OUTF.sh && setsid nohup bash $OUTF.sh $D $WAVE $MC $BL > $OUTF 2> $OUTF.err < /dev/null; rcs=\$?; cat $OUTF; echo '### REMOTE_SCRIPT_RC'; echo \$rcs" < "$(dirname "$0")/vn_probe_remote.sh" > "$P" 2> "$P.err" || rc=$?
note=""
if [[ $rc -ne 0 ]] || ! grep -q "^### $NEED" "$P"; then
  sleep 15; P2=$P.refetch; rc2=0; ssh $NOTS "cat $OUTF; echo '### REMOTE_SCRIPT_ERR'; head -c 2000 $OUTF.err" > "$P2" 2> "$P2.err" || rc2=$?
  if [[ $rc2 -eq 0 ]] && grep -q "^### $NEED" "$P2"; then note="first ssh rc $rc (connection cut, partial output); the finished probe output was re-fetched from NOTS (ssh rc $rc2); no second probe run"; mv "$P2" "$P"; rc=0
  else note="first ssh rc $rc; re-fetch rc $rc2 did not return a complete probe output"; fi
fi
# the ssh exit status and its stderr are part of the probe file (never silently ignored): stop_rules_vn.py reads REMOTE_RC / REMOTE_STDERR and the section list
{ echo "### REMOTE_RC"; echo "$rc"; echo "### REMOTE_NOTE"; echo "$note"; echo "### REMOTE_STDERR"; head -c 3000 "$P.err" | tail -n 20; } >> "$P"; [[ -s $P.err ]] && head -n 5 "$P.err" >&2
exec python3 "$(dirname "$0")/stop_rules_vn.py" "$P" --wave "$WAVE" --plans "$STG/current/scripts" --deploy-log "$LOG" ${QUOTE:+--quote $QUOTE} ${PRIOR:+--prior $PRIOR}
