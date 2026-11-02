#!/bin/bash
# Adapted from ops/scaffold/pilot_monitor.sh v2. One SSH per check.
#   bash waiter.sh LOGFILE JOBIDS [MAX_CHECKS] [--until-terminal]
# Default (watch) mode: exit 3 EARLY_FAILURE at the first failure-like row (wake OPS for triage); 0 ALL_TERMINAL when every requested id is
# terminal (complete accounting) and none of ours is queued; 2 after MAX_CHECKS.
# --until-terminal (after triage, manager ruling on Sol R1 F8/F10): never exits early; 0 ALL_TERMINAL (all COMPLETED), 4 ALL_TERMINAL_WITH_FAILURES
# (every id terminal, some failed: OPS proceeds to the unlock check and reconciliation), 2 after MAX_CHECKS.
set -u
UNTIL=0; ARGS=()
for a in "$@"; do if [ "$a" = --until-terminal ]; then UNTIL=1; else ARGS+=("$a"); fi; done
set -- "${ARGS[@]}"
LOG=${1:?logfile}; IDS=${2:?jobids}; MAX=${3:-11}
[[ "$IDS" =~ ^[0-9]+(,[0-9]+)*$ && "$MAX" =~ ^[1-9][0-9]*$ ]] || { echo 'invalid job ids or MAX_CHECKS' >&2; exit 2; }
n=0
while [ "$n" -lt "$MAX" ]; do
  n=$((n+1))
  out=$(MSYS_NO_PATHCONV=1 ssh -o BatchMode=yes -o ConnectTimeout=30 nots "squeue -h -u fb31 -o '%i %j %T %R' || exit 1; echo ===SACCT===; sacct -n -X -P -j $IDS -o JobID,State" 2>&1); rc=$?
  { echo "### check $n $(date -u +%FT%TZ) ssh_rc=$rc"; printf '%s\n' "$out"; } >> "$LOG"
  if [ "$rc" -ne 0 ]; then [ "$n" -lt "$MAX" ] && sleep 900; continue; fi
  q=$(printf '%s\n' "$out" | awk '/^===SACCT===$/{exit} /lowpL_/{c++} END{print c+0}')
  st=$(printf '%s\n' "$out" | awk -F'|' 'f && NF==2 {print $2} /^===SACCT===$/{f=1}')
  nrows=$(printf '%s\n' "$st" | awk 'NF{n++} END{print n+0}')
  nterm=$(printf '%s\n' "$st" | awk '/^(COMPLETED|FAILED|CANCELLED.*|TIMEOUT|OUT_OF_MEMORY|NODE_FAIL|PREEMPTED|BOOT_FAIL|DEADLINE)$/ {n++} END{print n+0}')
  nbad=$(printf '%s\n' "$st" | awk '/^(FAILED|CANCELLED.*|TIMEOUT|OUT_OF_MEMORY|NODE_FAIL|PREEMPTED|BOOT_FAIL|DEADLINE)$/ {n++} END{print n+0}')
  echo "check $n: squeue_lowp=$q sacct_rows=$nrows terminal=$nterm failed_like=$nbad states: $(printf '%s\n' "$st" | sort | uniq -c | tr '\n' ' ')" >> "$LOG"
  if [ "$nbad" -gt 0 ] && [ "$UNTIL" = 0 ]; then echo "EARLY_FAILURE $(date -u +%FT%TZ)" >> "$LOG"; exit 3; fi
  complete=$(printf '%s\n' "$out" | awk -F'|' -v ids="$IDS" 'BEGIN{split(ids,a,",");for(i in a)x[a[i]]=1} /^===SACCT===$/{f=1;next} f && NF{if(NF!=2 || $1 !~ /^[0-9]+(_[^|]+)?$/){bad=1;next} split($1,b,"_");if(!x[b[1]]){bad=1;next} seen[b[1]]=1;if($2 !~ /^(COMPLETED|FAILED|CANCELLED.*|TIMEOUT|OUT_OF_MEMORY|NODE_FAIL|PREEMPTED|BOOT_FAIL|DEADLINE)$/)bad=1} END{for(i in x)if(!seen[i])bad=1;print bad?"UNKNOWN":"complete"}')
  if [ "$q" -eq 0 ] && [ "$complete" = complete ]; then
    if [ "$nbad" -gt 0 ]; then echo "ALL_TERMINAL_WITH_FAILURES failed_like=$nbad $(date -u +%FT%TZ)" >> "$LOG"; exit 4; fi
    echo "ALL_TERMINAL $(date -u +%FT%TZ)" >> "$LOG"; exit 0
  fi
  echo "UNKNOWN: not terminal or accounting incomplete" >> "$LOG"
  [ "$n" -lt "$MAX" ] && sleep 600
done
echo "MAX_CHECKS_REACHED $(date -u +%FT%TZ)" >> "$LOG"; exit 2
