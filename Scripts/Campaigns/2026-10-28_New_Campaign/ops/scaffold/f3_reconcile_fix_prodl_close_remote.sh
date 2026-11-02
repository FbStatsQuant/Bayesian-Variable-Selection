#!/bin/bash
# f3_reconcile_fix_prodl_close_remote.sh (ON NOTS via: ssh nots 'bash -s' < this):
#  1. BENCH_F3_DEV: the first reconcile crashed (Rscript not on PATH: env.sh was sourced only in the retry subshell). Keep the crashed output and the
#     too-early logs manifest as evidence (renamed), rerun reconcile WITH env.sh (as JOB.md), then regenerate the logs manifest (p0500/p1000 unchanged).
#  2. PROD-L: close smc and smcrep with --allow-incomplete under HQ D63 (P5 scan not completed; all 14,400 units natively completed).
set -uo pipefail
cd /scratch/fb31/New_Campaign || exit 3
U=/scratch/fb31/New_Campaign/upload/20261030T1855Z_bench_f3v2_dev; RID=20261030T1855Z_bench_f3v2_dev; L=/scratch/fb31/New_Campaign/logs/$RID
SRC=3e01c77b27ad96ad8ec4761b6b25ea5511d357e8aa08a1db7b2972e71734f42c; T=$(date -u +%Y%m%dT%H%M%SZ)
echo "date=$(date -u +%FT%TZ)"; squeue -h -u fb31 -o '%i %j %T'
echo "===== F3 evidence of the crashed run"
cp -p $L/reconcile.txt $L/reconcile_partial_$T.txt && mv $L/MANIFEST.sha256 $L/MANIFEST.sha256.superseded_$T && ls $L | tr '\n' ' '; echo
echo "===== F3 reconcile (env.sh sourced)"
source $U/runner/env.sh > /dev/null 2>&1; command -v Rscript
python3 $U/runner/reconcile.py --root /scratch/fb31/New_Campaign/results/$RID --kind dev --run-id $RID --source-sha256 $SRC 2>&1 | tee $L/reconcile.txt | tail -12; echo "reconcile_rc=${PIPESTATUS[0]}"
echo "===== F3 logs manifest"; python3 $U/runner/manifests.py --run-log $L $L 2>&1 | tail -3; echo "rc=${PIPESTATUS[0]}"
echo "===== F3 verify all three"; python3 $U/runner/manifests.py /scratch/fb31/New_Campaign/results/$RID/p0500 /scratch/fb31/New_Campaign/results/$RID/p1000 $L --verify 2>&1 | tail -4; echo "rc=${PIPESTATUS[0]}"
echo "===== PROD-L close smc + smcrep (--allow-incomplete, HQ D63)"
export STAMP=20261030T1811Z; B=/home/fb31/projects/BVS/New_Campaign/runs/${STAMP}_lowp_prodL/code/prod_l
for p in smc smcrep; do echo "== $p"; bash $B/make_manifests.sh $STAMP --piece $p --allow-incomplete < /dev/null 2>&1 | tail -8; echo "close_${p}_rc=${PIPESTATUS[0]}"; done
cat /home/fb31/projects/BVS/New_Campaign/runs/${STAMP}_lowp_prodL/manifests/summary.tsv 2>&1
