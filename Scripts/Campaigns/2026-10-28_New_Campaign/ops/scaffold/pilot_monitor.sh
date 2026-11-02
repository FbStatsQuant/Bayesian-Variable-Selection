#!/bin/bash
# pilot_monitor.sh LOGFILE JOBIDS [MAX_CHECKS] : (laptop) background waiter for a LOWP pilot run.
# JOBIDS = comma-separated parent job ids. ONE ssh per check, at most one check every 10 minutes; after an ssh failure, back off 15 minutes.
# Exits 0 (ALL_TERMINAL) when squeue lists none of our lowp_p* jobs AND every sacct row of the given ids is in a terminal state
# (COMPLETED FAILED CANCELLED* TIMEOUT OUT_OF_MEMORY NODE_FAIL PREEMPTED BOOT_FAIL DEADLINE); exits 3 at once if any row is FAILED/TIMEOUT/OOM/NODE_FAIL
# (EARLY_FAILURE: OPS inspects instead of waiting); exits 2 after MAX_CHECKS (default 11, < 2 h) so the caller can restart it.
# v2 (2026-10-30, HQ watchdog): v1 split the output with sed '1,/^===$/p', which with an empty squeue ran to EOF and counted sacct rows as queued.
set -u
LOG=${1:?logfile}; IDS=${2:?jobids}; MAX=${3:-11}
n=0
while [ $n -lt "$MAX" ]; do
  n=$((n+1))
  out=$(MSYS_NO_PATHCONV=1 ssh -o BatchMode=yes -o ConnectTimeout=30 nots "squeue -h -u fb31 -o '%i %j %T %R'; echo ===SACCT===; sacct -n -X -j $IDS -o JobID%16,JobName%20,State%14,ExitCode,Elapsed" 2>&1); rc=$?
  { echo "### check $n $(date -u +%FT%TZ) ssh_rc=$rc"; printf '%s\n' "$out"; } >> "$LOG"
  if [ $rc -ne 0 ]; then sleep 900; continue; fi
  q=$(printf '%s\n' "$out" | awk '/^===SACCT===$/{exit} /lowp_p/{c++} END{print c+0}')
  st=$(printf '%s\n' "$out" | awk 'f && NF>=3 {print $3} /^===SACCT===$/{f=1}')
  nrows=$(printf '%s\n' "$st" | awk 'NF' | wc -l)
  nterm=$(printf '%s\n' "$st" | grep -cE '^(COMPLETED|FAILED|CANCELLED.*|TIMEOUT|OUT_OF_ME.*|NODE_FAIL|PREEMPTED|BOOT_FAIL|DEADLINE)$')
  nbad=$(printf '%s\n' "$st" | grep -cE '^(FAILED|TIMEOUT|OUT_OF_ME.*|NODE_FAIL)$')
  echo "check $n: squeue_lowp=$q sacct_rows=$nrows terminal=$nterm failed_like=$nbad states: $(printf '%s\n' "$st" | sort | uniq -c | tr '\n' ' ')" >> "$LOG"
  if [ "$nbad" -gt 0 ]; then echo "EARLY_FAILURE $(date -u +%FT%TZ)" >> "$LOG"; exit 3; fi
  if [ "$q" -eq 0 ] && [ "$nrows" -gt 0 ] && [ "$nterm" -eq "$nrows" ]; then echo "ALL_TERMINAL $(date -u +%FT%TZ)" >> "$LOG"; exit 0; fi
  sleep 600
done
echo "MAX_CHECKS_REACHED $(date -u +%FT%TZ)" >> "$LOG"; exit 2
