#!/bin/bash
# f3dev_stage_launch_remote.sh (ON NOTS via: ssh nots "RUN_ID=<id> UPSHA=<sha> bash -s" < this): BENCH_F3_DEV JOB.md step 4 (stage.sh), then
# launch.py --dry-run, then the real launch only if staging printed STAGED_OK and the dry run exited 0. Prints the scheduler output.
set -uo pipefail
: "${RUN_ID:?}"; : "${UPSHA:?}"
U=/scratch/fb31/New_Campaign/upload/$RUN_ID
echo "date=$(date -u +%FT%TZ) RUN_ID=$RUN_ID"
squeue -h -u fb31 -o '%j' | grep -q bench_f3v2 && { echo "an F3 job already exists: NOT LAUNCHED"; exit 1; }
echo "== stage"; out=$(bash $U/runner/stage.sh $U $UPSHA < /dev/null 2>&1); src=$?; printf '%s\n' "$out"; echo "stage_rc=$src"
[ $src -eq 0 ] && [[ "$out" == *STAGED_OK* ]] || { echo "staging failed: NOT LAUNCHED"; exit 1; }
echo "== dry run"; python3 $U/runner/launch.py dev $RUN_ID --resources $U/runner/resources.json --dry-run < /dev/null 2>&1; drc=$?; echo "dryrun_rc=$drc"
[ $drc -eq 0 ] || { echo "dry run refused: NOT LAUNCHED"; exit 1; }
echo "== launch"; python3 $U/runner/launch.py dev $RUN_ID --resources $U/runner/resources.json < /dev/null 2>&1; echo "launch_rc=$?"
echo "== squeue"; squeue -u fb31 -o '%i %j %T %r' | grep -E 'JOBID|bench_f3v2|f3' | head
