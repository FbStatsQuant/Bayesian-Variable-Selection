#!/bin/bash
# recover_truth.sh -- OPS RECOVERY when the wave unlock did not run or failed (job cancelled, node failure, finalizer error): reopen the
# staged truth trees of one pilot WITHOUT R. Safe only when no pilot job can still be reading: it refuses while any recorded job is active.
#   bash recover_truth.sh STAMP
# Reads RUN_HOME/JOBIDS.tsv (kept in home, a few hundred bytes), asks Slurm about those explicit ids, then reopens directories 755 and files 444
# top-down and verifies counts and modes. Exit 0 verified open; 1 not verified; 3 refused (jobs active, or the scheduler could not be queried).
set -uo pipefail
STAMP="${1:?usage: recover_truth.sh STAMP}"
[[ "$STAMP" =~ ^[0-9]{8}T[0-9]{4}Z$ ]] || { echo "bad STAMP" >&2; exit 2; }
HOME_ROOT="${NC_HOME_ROOT:-/home/fb31/projects/BVS/New_Campaign}"
HERE="$(cd "$(dirname "$0")" && pwd)"
source "$HERE/truth_lib.sh"
RUN_HOME="$HOME_ROOT/runs/${STAMP}_lowp_prodL"; STUDY="$RUN_HOME/study"
SQUEUE="${SQUEUE:-squeue}"
[ -d "$STUDY/truth" ] || [ -d "$STUDY" ] || { echo "no study copy at $STUDY" >&2; exit 3; }
[ -r "$RUN_HOME/JOBIDS.tsv" ] || { echo "REFUSED: $RUN_HOME/JOBIDS.tsv missing: cannot establish that no pilot job is active" >&2; exit 3; }
# Sol R1 F1: fail CLOSED on scheduler evidence. Every refusal exits 3 (documented contract; JOB.md section 8).
q=$("$SQUEUE" -h -u fb31 -o '%i|%j|%T' 2>&1) || { echo "REFUSED: squeue failed ($q)" >&2; exit 3; }
ids=$(awk -F'\t' 'NR>1 {if($3 !~ /^[0-9]+$/)exit 1; print $3}' "$RUN_HOME/JOBIDS.tsv") || { echo "REFUSED: invalid recorded job ID" >&2; exit 3; }
ids=$(printf '%s\n' "$ids" | paste -sd, -)
[ -n "$ids" ] || { echo "REFUSED: no recorded ids" >&2; exit 3; }
# queue: refuse on any row of a recorded id (array root before "_"), on any lowpL_ job (a PROD-L job not recorded here), or on a row that does not parse
printf '%s\n' "$q" | awk -F'|' -v ids="$ids" 'BEGIN{split(ids,a,",");for(i in a)x[a[i]]=1} NF{if(NF<3 || $1 !~ /^[0-9]+(_[^|]+)?$/){bad=1;next} split($1,b,"_");if(x[b[1]] || $2 ~ /^lowpL_/)bad=1} END{exit bad}' || { echo "REFUSED: a run job (or another lowpL_ job) is queued or running, or the queue did not parse:" >&2; printf '%s\n' "$q" >&2; exit 3; }
# accounting: every recorded id present, every row terminal (first two fields JobID|State are used)
acct=$("${SACCT:-sacct}" -X -n -P -j "$ids" -o JobID,State) || { echo "REFUSED: sacct failed" >&2; exit 3; }
printf '%s\n' "$acct" | awk -F'|' -v ids="$ids" 'BEGIN{split(ids,a,",");for(i in a)x[a[i]]=1} NF{if(NF<2 || $1 !~ /^[0-9]+(_[^|]+)?$/){bad=1;next} split($1,b,"_");if(!x[b[1]]){bad=1;next} seen[b[1]]=1;if($2 !~ /^(COMPLETED|FAILED|CANCELLED.*|TIMEOUT|OUT_OF_MEMORY|NODE_FAIL|PREEMPTED|BOOT_FAIL|DEADLINE)$/)bad=1} END{for(i in x)if(!seen[i])bad=1;exit bad}' || { echo "REFUSED: incomplete or non-terminal accounting for the recorded ids" >&2; exit 3; }
echo "recovering truth trees under $STUDY"
tl_plain_unlock "$STUDY"
tl_verify_open "$STUDY"; rc=$?
[ $rc = 0 ] && echo "RECOVERED: truth trees verified 755/444, 1200 + 60 files" || echo "NOT VERIFIED: inspect modes by hand" >&2
exit $rc
