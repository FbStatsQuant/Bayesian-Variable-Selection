#!/bin/bash
# prodl_p5_remote.sh (ON NOTS via: ssh nots 'bash -s' < this): PROD-L JOB.md §5 step 6 after the initial scan: show the scan job and its state; if it is
# COMPLETED, build the P5 lists (make_p5_list.sh --from-scan initial, then --wave p5). Submits nothing. Also sacct of the F3 dev job.
set -u
export STAMP=20261030T1811Z
RL=/home/fb31/projects/BVS/New_Campaign/runs/${STAMP}_lowp_prodL; B=$RL/code/prod_l; LL=/scratch/fb31/New_Campaign/logs/${STAMP}_lowp_prodL
echo "date=$(date -u +%FT%TZ)"; squeue -h -u fb31 -o '%i %j %T'
echo "== jobids.tsv"; cat $LL/jobids.tsv
echo "== logs/p5"; ls -laR $LL/p5 2>&1 | head -30
ids=$(awk -F'\t' 'NR>1 && $1 !~ /^main$/ {print $3}' $LL/jobids.tsv | paste -sd,)
echo "== sacct non-main ids=$ids"; [ -n "$ids" ] && sacct -n -X -P -j "$ids" -o JobID,JobName,State,ExitCode,Elapsed 2>&1
st=$( [ -n "$ids" ] && sacct -n -X -P -j "$ids" -o JobName,State 2>/dev/null | grep -i p5scan | tail -1 | cut -d'|' -f2 )
echo "scan_state=${st:-none}"
if [ "$st" = COMPLETED ]; then
  echo "== make_p5_list --from-scan initial"; bash $B/make_p5_list.sh $STAMP --from-scan initial < /dev/null 2>&1 | tail -12; echo "rc=${PIPESTATUS[0]}"
  echo "== make_p5_list --wave p5"; bash $B/make_p5_list.sh $STAMP --wave p5 < /dev/null 2>&1 | tail -12; echo "rc=${PIPESTATUS[0]}"
  ls -la $RL/p5 2>&1 | head
fi
echo "== sacct F3 dev 2496644"; sacct -n -X -j 2496644 -o JobID%16,State%12,ExitCode,Elapsed,MaxRSS 2>&1 | awk '{print $2}' | sort | uniq -c
