#!/bin/bash
# f3prod_cell4_gate_prefix.sh : prepended (by f3prod_cell4_relaunch.sh) to f3prod_stage_launch_remote.sh for the cell-4 relaunch after the
# 21:02Z launch failed inside launch.py's gate.sh (CalledProcessError, output not captured). Runs gate.sh standalone first so its output
# (guard line, GATE_OK or the failing check) is recorded; stops before any launch if it fails.
: "${RUN_ID:?}"
echo "== gate.sh standalone $(date -u +%FT%TZ)"
bash /scratch/fb31/New_Campaign/upload/$RUN_ID/runner/gate.sh /scratch/fb31/New_Campaign/upload/$RUN_ID/runner $RUN_ID < /dev/null 2>&1; grc=$?
echo "gate_rc=$grc"
[ $grc -eq 0 ] || { echo "gate failed: NOT LAUNCHED"; exit 1; }
