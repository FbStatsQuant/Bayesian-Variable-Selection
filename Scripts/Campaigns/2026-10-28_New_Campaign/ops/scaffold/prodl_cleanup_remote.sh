#!/bin/bash
# prodl_cleanup_remote.sh : (NOTS; started detached by remote_bg.sh) PROD-L JOB.md §5 step 9: cleanup_prodl.sh dry run, then --yes with the
# receipt outside the removed tree (scratch upload/). Prints dry_rc= and cleanup_rc=; requires CLEANUP VERIFIED in the --yes output.
export STAMP=20261030T1811Z
B=/home/fb31/projects/BVS/New_Campaign/runs/20261030T1811Z_lowp_prodL/code/prod_l
REC=/scratch/fb31/New_Campaign/upload/cleanup_receipt_20261030T1811Z_lowp_prodL.txt
cd /scratch/fb31/New_Campaign || { echo "cd failed"; exit 2; }
echo "== dry run $(date -u +%FT%TZ)"
bash $B/cleanup_prodl.sh 20261030T1811Z < /dev/null 2>&1 | tail -15; echo "dry_rc=${PIPESTATUS[0]}"
echo "== --yes $(date -u +%FT%TZ)"
bash $B/cleanup_prodl.sh 20261030T1811Z --yes --receipt $REC < /dev/null 2>&1 | tail -20; rc=${PIPESTATUS[0]}; echo "cleanup_rc=$rc"
echo "== receipt"; cat $REC 2>&1 | tail -10
exit $rc
