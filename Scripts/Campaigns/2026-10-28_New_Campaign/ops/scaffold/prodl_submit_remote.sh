#!/bin/bash
# prodl_submit_remote.sh (ON NOTS via: ssh nots "STAMP=<STAMP> PROFILE=withH bash -s" < this): PROD-L JOB.md §5 step 2. Dry run; submit only if the
# dry run exits 0 and no PROD-L job exists yet. Prints the job ids.
set -uo pipefail
: "${STAMP:?}"; PROFILE=${PROFILE:-withH}
RID="${STAMP}_lowp_prodL"; B=/home/fb31/projects/BVS/New_Campaign/runs/$RID/code/prod_l; L=/scratch/fb31/New_Campaign/logs/$RID
export STAMP
echo "date=$(date -u +%FT%TZ) RID=$RID profile=$PROFILE"
squeue -h -u fb31 -o '%j' | grep -q lowp_prodL && { echo "a PROD-L job already exists: NOT SUBMITTED"; exit 1; }
[ ! -e "$L/jobids.tsv" ] || { echo "jobids.tsv already exists: NOT SUBMITTED"; cat "$L/jobids.tsv"; exit 1; }
echo "== dry run"; bash $B/submit_prodl.sh --wave main --profile $PROFILE --dry-run < /dev/null 2>&1; drc=$?; echo "dryrun_rc=$drc"
[ $drc -eq 0 ] || { echo "dry run refused: NOT SUBMITTED"; exit 1; }
echo "== submit"; bash $B/submit_prodl.sh --wave main --profile $PROFILE < /dev/null 2>&1; echo "submit_rc=$?"
echo "== jobids"; cat "$L/jobids.tsv" 2>&1
echo "== squeue"; squeue -u fb31 -o '%i %j %T %r' | grep -E 'JOBID|lowp_' | head -20
