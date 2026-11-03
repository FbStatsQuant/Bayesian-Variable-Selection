#!/bin/bash
# f3prod_cell4_gate_prefix.sh : prepended (by f3prod_cell4_relaunch.sh) to f3prod_stage_launch_remote.sh for the cell-4 relaunch after the
# 21:02Z launch failed inside launch.py's gate.sh (CalledProcessError, output not captured). Runs gate.sh standalone first so its output
# (guard line, GATE_OK or the failing check) is recorded; stops before any launch if it fails.
: "${RUN_ID:?}"
echo "== gate.sh standalone $(date -u +%FT%TZ)"
bash /scratch/fb31/New_Campaign/upload/$RUN_ID/runner/gate.sh /scratch/fb31/New_Campaign/upload/$RUN_ID/runner $RUN_ID < /dev/null 2>&1; grc=$?
echo "gate_rc=$grc"
[ $grc -eq 0 ] || { echo "gate failed: NOT LAUNCHED"; exit 1; }
# f3prod_stage_launch_remote.sh (ON NOTS via: ssh nots "RUN_ID=<id> UPSHA=<sha> STAGE=0|1 bash -s" < this): BENCH_F3_PROD JOB.md: stage.sh (if STAGE=1),
# campaign ceiling check (fb31 running+pending array tasks + 30 <= 96, i.e. <= 192 billed), launch.py --dry-run, then launch.py (submits at most ONE cell).
set -uo pipefail
: "${RUN_ID:?}"; : "${UPSHA:?}"; STAGE=${STAGE:-1}
U=/scratch/fb31/New_Campaign/upload/$RUN_ID
echo "date=$(date -u +%FT%TZ) RUN_ID=$RUN_ID stage=$STAGE"
squeue -h -u fb31 -o '%i %j %T' 2>&1
if [ "$STAGE" = 1 ]; then
  echo "== stage"; out=$(bash $U/runner/stage.sh $U $UPSHA < /dev/null 2>&1); src=$?; printf '%s\n' "$out"; echo "stage_rc=$src"
  [ $src -eq 0 ] && [[ "$out" == *STAGED_OK* ]] || { echo "staging failed: NOT LAUNCHED"; exit 1; }
fi
# campaign ceiling: count every running task and every pending array's throttle-limited capacity conservatively as its pending task count
nrun=$(squeue -h -u fb31 -t RUNNING -o '%i' | wc -l); npend=$(squeue -h -u fb31 -t PENDING -r -o '%i' | wc -l)
echo "ceiling: running_tasks=$nrun pending_tasks=$npend new_throttle=30 -> $((nrun + npend + 30)) tasks <= 96 required"
[ $((nrun + npend + 30)) -le 96 ] || { echo "CEILING REFUSED: NOT LAUNCHED"; exit 1; }
echo "== dry run"; python3 $U/runner/launch.py prod $RUN_ID --resources $U/runner/resources.json --dry-run < /dev/null 2>&1; drc=$?; echo "dryrun_rc=$drc"
[ $drc -eq 0 ] || { echo "dry run refused: NOT LAUNCHED"; exit 1; }
echo "== launch"; python3 $U/runner/launch.py prod $RUN_ID --resources $U/runner/resources.json < /dev/null 2>&1; echo "launch_rc=$?"
echo "== jobs.tsv"; cat /scratch/fb31/New_Campaign/logs/$RUN_ID/jobs.tsv 2>&1
echo "== squeue"; squeue -u fb31 -o '%i %j %T %r' | head -5
