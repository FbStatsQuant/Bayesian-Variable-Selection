#!/bin/bash
# disk_check.sh (laptop side): run the staged guard.sh on NOTS once and append its line to ops/DISK_LOG.md.
# Usage: bash disk_check.sh [PLANNED_ADD_MB] [NOTE]   Exit code = guard's (0 OK, 1 REFUSE, 2 measurement failure, 255 ssh).
OPS=$(cd "$(dirname "$0")" && pwd)
LOG="$OPS/DISK_LOG.md"
[ -f "$LOG" ] || printf '# DISK_LOG (one line per check; GB = GiB; limits: campaign 0.5 GiB, home 9.6 GiB)\n\n' > "$LOG"
ADD=${1:-0}
# Validate locally: only a bounded decimal integer ever reaches the remote shell (review/SOL_REVIEW_CLASS_B.md F6).
[[ "$ADD" =~ ^(0|[1-9][0-9]{0,6})$ ]] || { echo "disk_check: PLANNED_ADD_MB must be a whole number of MB (0..9999999)" >&2; exit 2; }
OUT=$(ssh -o BatchMode=yes nots "bash /home/fb31/projects/BVS/New_Campaign/code/ops/guard.sh $ADD" 2>&1); RC=$?
echo "- $OUT | rc=$RC${2:+ | $2}" >> "$LOG"
echo "$OUT (rc=$RC)"
exit $RC
