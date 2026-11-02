#!/bin/bash
# prodl_finalacct_logs_remote.sh (ON NOTS via: ssh nots 'bash -s' < this): PROD-L JOB.md §5 step 8 tail: final_accounting.sh, then close the logs
# (make_manifests.sh --piece logs). If the staged script refuses (HQ D58), print what it lists; the manual workaround is done separately after review.
set -u
export STAMP=20261030T1811Z
RL=/home/fb31/projects/BVS/New_Campaign/runs/${STAMP}_lowp_prodL; B=$RL/code/prod_l; LL=/scratch/fb31/New_Campaign/logs/${STAMP}_lowp_prodL
cd /scratch/fb31/New_Campaign || exit 3
echo "date=$(date -u +%FT%TZ)"; squeue -h -u fb31 -o '%i %j %T'
echo "===== final_accounting"; bash $B/final_accounting.sh $STAMP < /dev/null 2>&1 | tail -25; echo "rc=${PIPESTATUS[0]}"
echo "===== close logs"; bash $B/make_manifests.sh $STAMP --piece logs < /dev/null 2>&1 | tail -15; echo "close_logs_rc=${PIPESTATUS[0]}"
ls -la $LL/MANIFEST.sha256 2>&1; ls $RL/manifests 2>&1 | tr '\n' ' '; echo; ls -d $RL/p5 $RL/resubmit $RL/inventory_final 2>&1
