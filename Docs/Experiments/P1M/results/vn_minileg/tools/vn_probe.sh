#!/usr/bin/env bash
# vn_probe.sh -- ONE ssh = one squeue + one sacct -X for the identity-check batch (<= 1 probe per 10 min). Prints the states and WAVE STATE.
set -euo pipefail; . "$(dirname "$0")/common.sh"
ssh $NOTS "set -u; R=$D/scratch/runs/$BATCH; ids=\$(grep -o '\"job\": *\"[0-9]*\"' \$R/submissions.jsonl | grep -o '[0-9][0-9]*' | paste -sd,)
  echo \"UTC \$(date -u +%FT%TZ)\"; echo '--- squeue'; squeue -u fb31 -h -o '%i|%j|%T|%r|%M' | grep -E \"p1m_${BATCH}_\" || true
  echo '--- sacct -X'; sacct -X -P -n -j \"\$ids\" --format=JobID,JobName,State,ElapsedRaw,AllocCPUS,CPUTimeRAW" | python3 -c "
import sys
t=sys.stdin.read(); print(t.rstrip())
rows=[l.split('|') for l in t.split('--- sacct -X')[1].strip().split('\n') if l.strip()]
q=[l for l in t.split('--- squeue')[1].split('--- sacct -X')[0].strip().split('\n') if l.strip()]
term={'COMPLETED','FAILED','TIMEOUT','OUT_OF_MEMORY','CANCELLED','NODE_FAIL','BOOT_FAIL'}
cost=sum(int(r[5] or 0) for r in rows)/3600.0
nt=[r for r in rows if r[2].split()[0] not in term]
bad=[r for r in rows if r[2].split()[0] in term-{'COMPLETED'}]
print('billed so far %.2f core-h (cap 46.8; expected 2.4); %d sacct rows; failed/timeout: %d' % (cost,len(rows),len(bad)))
print('WAVE STATE: ENDED' if (not q and rows and not nt) else 'WAVE STATE: RUNNING')"
