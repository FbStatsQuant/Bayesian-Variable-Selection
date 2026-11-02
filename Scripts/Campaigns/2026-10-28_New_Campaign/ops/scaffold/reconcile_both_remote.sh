#!/bin/bash
# reconcile_both_remote.sh (ON NOTS via: ssh nots 'bash -s' < this): PROD-H JOB.md E (reconcile --sacct --full-verify, list non-done) and
# PROD-L JOB.md §5.4 (reconcile_prodl.py, inventory, clear_stale.sh LIST only). Read-only except the bundles' own reconcile outputs.
set -u
HR=/home/fb31/projects/BVS/New_Campaign
RH=$HR/runs/20261030T0934Z_prodH
LSTAMP=20261030T1811Z; RL=$HR/runs/${LSTAMP}_lowp_prodL; B=$RL/code/prod_l; LL=/scratch/fb31/New_Campaign/logs/${LSTAMP}_lowp_prodL
echo "date=$(date -u +%FT%TZ)"
squeue -h -u fb31 -o '%i %j %T' | head
echo "===== PROD-H reconcile --sacct --full-verify"; nice -n 19 python3 $RH/runner/reconcile.py $RH --sacct --full-verify 2>&1 | tail -30; echo "rc=${PIPESTATUS[0]}"
echo "== PROD-H units not done"; column -t -s$'\t' $RH/reconcile.tsv 2>/dev/null | awk 'NR==1 || $4!="done"' | head -20
echo "== PROD-H class/outcome counts"; awk -F'\t' 'NR==1{for(i=1;i<=NF;i++)h[$i]=i; next} {c[$h["class"]" "$h["outcome"]]++} END{for(k in c) print k, c[k]}' $RH/reconcile.tsv 2>&1 | sort
echo "===== PROD-L P0 / lock evidence"; tail -3 $LL/p0_verify/*REPORT* 2>/dev/null | cut -c1-200; tail -2 $LL/truthlock/main/WAVE_LOCK.txt 2>&1 | cut -c1-200
echo "===== PROD-L reconcile_prodl.py"; export STAMP=$LSTAMP; nice -n 19 python3 $B/reconcile_prodl.py $LSTAMP 2>&1 | tail -30; echo "rc=${PIPESTATUS[0]}"
echo "== INVENTORY.md"; sed -n 1,60p $RL/inventory_final/INVENTORY.md 2>&1
echo "== clear_stale.sh (list only)"; bash $B/clear_stale.sh $LSTAMP < /dev/null 2>&1 | tail -15; echo "rc=$?"
