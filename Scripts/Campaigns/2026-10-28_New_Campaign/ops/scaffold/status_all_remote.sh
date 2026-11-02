#!/bin/bash
# status_all_remote.sh (ON NOTS via: ssh nots 'bash -s' < this): one batched, read-only status of PROD-H, PROD-L main and BENCH_F3_DEV
# (plus PROD-H's poll.py, which appends one poll record). The guard runs only if PROD-L's truth trees are verified unlocked (du fails while locked).
set -u
HR=/home/fb31/projects/BVS/New_Campaign; S=/scratch/fb31/New_Campaign
RH=$HR/runs/20261030T0934Z_prodH
LRID=20261030T1811Z_lowp_prodL; RL=$HR/runs/$LRID; LL=$S/logs/$LRID
echo "date=$(date -u +%FT%TZ) host=$(hostname)"
echo "== squeue (all fb31)"; squeue -h -u fb31 -o '%i %j %T %M %R' 2>&1 | head -60
echo "== sacct PROD-H (state counts, all rows incl. array tasks)"; sacct -n -X -P -j 2469859,2469860,2469861 -o JobID,State 2>&1 | awk -F'|' '{split($1,a,"_"); c[a[1]" "$2]++} END{for(k in c) print k, c[k]}' | sort
echo "== PROD-H poll.py"; python3 $RH/runner/poll.py $RH 2>&1 | tail -c 1500; echo; echo "POLL_RC=${PIPESTATUS[0]}"
echo "== PROD-H jobs.tsv"; cat $RH/jobs.tsv 2>&1
echo "== sacct PROD-L main (state counts by job)"; ids=$(awk -F'\t' 'NR>1 && $1=="main"{print $3}' $LL/jobids.tsv | paste -sd,); echo "ids=$ids"
sacct -n -X -P -j "$ids" -o JobID,JobName,State 2>&1 | awk -F'|' '{split($1,a,"_"); c[a[1]" "$2" "$3]++} END{for(k in c) print k, c[k]}' | sort
echo "== PROD-L unlock"; ls $LL/truthlock/main/ 2>&1; tail -4 $LL/truthlock/main/WAVE_UNLOCK.txt 2>&1
stat -c '%a %n' $RL/study/truth $RL/study/dev/truth 2>&1
UNL=0; grep -q WAVE_UNLOCK_VERIFIED $LL/truthlock/main/WAVE_UNLOCK.txt 2>/dev/null && [ "$(stat -c %a $RL/study/truth)" = 755 ] && UNL=1
echo "unlock_verified=$UNL"
echo "== disk"; du -sk $S/results/* $S/logs/* $S/upload/* 2>/dev/null | sort -k2
if [ $UNL = 1 ]; then bash $HR/code/ops/guard.sh 0; else echo "guard skipped (PROD-L truth not verified open)"; fi
quota -s 2>&1 | tail -1
