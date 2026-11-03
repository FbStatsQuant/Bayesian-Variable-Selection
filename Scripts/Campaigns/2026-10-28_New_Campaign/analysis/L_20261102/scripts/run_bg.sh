#!/bin/bash
# run_bg.sh TAG CMD [ARGS...] : detached step runner (launch with PowerShell Start-Process so it survives T3 restarts).
# Writes logs/TAG.log (stdout+stderr), logs/TAG.pid, logs/TAG.rc (exit code, written last). Refuses if TAG.rc absent and TAG.pid is live.
L=/c/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign/analysis/L_20261102/logs
T=${1:?tag}; shift
mkdir -p "$L"
if [ -s "$L/$T.pid" ] && [ ! -e "$L/$T.rc" ] && kill -0 "$(cat "$L/$T.pid")" 2>/dev/null; then echo "run_bg: $T already running" >&2; exit 7; fi
rm -f "$L/$T.rc"
echo $$ > "$L/$T.pid"
echo "START $(date -u +%Y-%m-%dT%H:%M:%SZ) $*" > "$L/$T.log"
"$@" >> "$L/$T.log" 2>&1
rc=$?
echo "END $(date -u +%Y-%m-%dT%H:%M:%SZ) rc=$rc" >> "$L/$T.log"
echo $rc > "$L/$T.rc"
