#!/bin/bash
# array_monitor.sh LOGFILE JOBIDS NAME_REGEX [MAX_CHECKS] : (laptop; run detached via detach_run.sh so ssh goes through the shim/lock)
# Generic waiter (pilot_monitor.sh v2 logic). One ssh per check, 10 min apart; 15 min back-off after an ssh failure.
# squeue lines whose job name matches NAME_REGEX count as queued/running. Writes one of these end lines to LOGFILE:
#   EARLY_FAILURE (any FAILED/TIMEOUT/OOM/NODE_FAIL row; exit 3) | ALL_TERMINAL (exit 0) | MAX_CHECKS_REACHED (exit 2)
set -u
LOG=${1:?logfile}; IDS=${2:?jobids}; RX=${3:?name regex}; MAX=${4:-11}
n=0
while [ $n -lt "$MAX" ]; do
  n=$((n+1))
  out=$(MSYS_NO_PATHCONV=1 ssh -o BatchMode=yes -o ConnectTimeout=30 nots "squeue -h -u fb31 -o '%i %j %T %R'; echo ===SACCT===; sacct -n -X -j $IDS -o JobID%24,JobName%30,State%14,ExitCode,Elapsed" 2>&1); rc=$?
  { echo "### check $n $(date -u +%FT%TZ) ssh_rc=$rc"; printf '%s\n' "$out"; } >> "$LOG"
  if [ $rc -ne 0 ]; then sleep 900; continue; fi
  q=$(printf '%s\n' "$out" | awk -v rx="$RX" '/^===SACCT===$/{exit} $2 ~ rx {c++} END{print c+0}')
  st=$(printf '%s\n' "$out" | awk 'f && NF>=3 {print $3} /^===SACCT===$/{f=1}')
  nrows=$(printf '%s\n' "$st" | awk 'NF' | wc -l)
  nterm=$(printf '%s\n' "$st" | grep -cE '^(COMPLETED|FAILED|CANCELLED.*|TIMEOUT|OUT_OF_ME.*|NODE_FAIL|PREEMPTED|BOOT_FAIL|DEADLINE)$')
  nbad=$(printf '%s\n' "$st" | grep -cE '^(FAILED|TIMEOUT|OUT_OF_ME.*|NODE_FAIL)$')
  echo "check $n: queued=$q sacct_rows=$nrows terminal=$nterm failed_like=$nbad states: $(printf '%s\n' "$st" | sort | uniq -c | tr '\n' ' ')" >> "$LOG"
  if [ "$nbad" -gt 0 ]; then echo "EARLY_FAILURE $(date -u +%FT%TZ)" >> "$LOG"; exit 3; fi
  if [ "$q" -eq 0 ] && [ "$nrows" -gt 0 ] && [ "$nterm" -eq "$nrows" ]; then echo "ALL_TERMINAL $(date -u +%FT%TZ)" >> "$LOG"; exit 0; fi
  sleep 600
done
echo "MAX_CHECKS_REACHED $(date -u +%FT%TZ)" >> "$LOG"; exit 2
