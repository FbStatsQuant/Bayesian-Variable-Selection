#!/bin/bash
# f3_manifest_prodl_close_remote.sh (ON NOTS via: ssh nots 'bash -s' < this): continuation after the 11:48Z run (reconcile rerun rc 0).
#  1. BENCH_F3_DEV manifests.py with all three folders (it preflights both result folders + the logs; existing p0500/p1000 manifests must match), then --verify.
#  2. PROD-L close smc and smcrep with --allow-incomplete (HQ D63). env.sh is NOT sourced here (it enables errexit).
set -uo pipefail
cd /scratch/fb31/New_Campaign || exit 3
U=/scratch/fb31/New_Campaign/upload/20261030T1855Z_bench_f3v2_dev; RID=20261030T1855Z_bench_f3v2_dev; L=/scratch/fb31/New_Campaign/logs/$RID; R=/scratch/fb31/New_Campaign/results/$RID
echo "date=$(date -u +%FT%TZ)"; squeue -h -u fb31 -o '%i %j %T'
echo "== reconcile.txt tail"; tail -6 $L/reconcile.txt | cut -c1-200
echo "===== F3 manifests (3 folders)"; python3 $U/runner/manifests.py --run-log $L $R/p0500 $R/p1000 $L 2>&1 | tail -5; echo "rc=${PIPESTATUS[0]}"
echo "===== F3 verify"; python3 $U/runner/manifests.py --run-log $L $R/p0500 $R/p1000 $L --verify 2>&1 | tail -5; echo "rc=${PIPESTATUS[0]}"
echo "===== PROD-L close smc + smcrep (--allow-incomplete, HQ D63)"
export STAMP=20261030T1811Z; B=/home/fb31/projects/BVS/New_Campaign/runs/${STAMP}_lowp_prodL/code/prod_l
for p in smc smcrep; do echo "== $p"; bash $B/make_manifests.sh $STAMP --piece $p --allow-incomplete < /dev/null 2>&1 | tail -8; echo "close_${p}_rc=${PIPESTATUS[0]}"; done
cat /home/fb31/projects/BVS/New_Campaign/runs/${STAMP}_lowp_prodL/manifests/summary.tsv 2>&1
