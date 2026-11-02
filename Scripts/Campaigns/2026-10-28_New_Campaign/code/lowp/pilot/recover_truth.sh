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
RUN_HOME="$HOME_ROOT/runs/${STAMP}_lowp_pilot"; STUDY="$RUN_HOME/study"
SQUEUE="${SQUEUE:-squeue}"
[ -d "$STUDY/truth" ] || [ -d "$STUDY" ] || { echo "no study copy at $STUDY" >&2; exit 3; }
[ -r "$RUN_HOME/JOBIDS.tsv" ] || { echo "REFUSED: $RUN_HOME/JOBIDS.tsv missing: cannot establish that no pilot job is active" >&2; exit 3; }
q=$("$SQUEUE" -h -u "${USER:-fb31}" -o '%i|%j|%T' 2>&1) || { echo "REFUSED: squeue failed ($q)" >&2; exit 3; }
ids=$(awk -F'\t' 'NR>1 && $2 ~ /^[0-9]+$/ {print $2}' "$RUN_HOME/JOBIDS.tsv")
active=$(printf '%s\n' "$q" | awk -F'|' -v ids="$(echo $ids | tr ' ' ',')" 'BEGIN{n=split(ids,a,","); for(i=1;i<=n;i++) want[a[i]]=1} {split($1,b,"_"); if (want[b[1]] || $2 ~ /^lowp_p/) print}')
[ -z "$active" ] || { echo "REFUSED: pilot jobs still queued or running; cancel them by explicit id first (scancel <id>), then rerun:" >&2; echo "$active" >&2; exit 3; }
echo "recovering truth trees under $STUDY"
tl_plain_unlock "$STUDY"
tl_verify_open "$STUDY"; rc=$?
[ $rc = 0 ] && echo "RECOVERED: truth trees verified 755/444, 1200 + 60 files" || echo "NOT VERIFIED: inspect modes by hand" >&2
exit $rc
