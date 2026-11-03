#!/bin/bash
# plb_failed_cleanup_remote.sh : (NOTS; started detached by remote_bg.sh) HQ D82: remove what is left of the failed PROD_L_BENCH run
# 20261102T1311Z_lowp_bench (s0_verify 2510090 FAILED, bundle defect) with the bundle's own cleanup_bench.sh: dry run, then --yes with the
# receipt on scratch upload/ (outside the removed trees). Targets (per cleanup_bench.sh): HOME/runs/<PID>, SCR/runs/<PID>_cache, SCR/runs/<PID>_tmp.
# cleanup_bench.sh --yes re-executes itself from memory after cd / (D44 B3), so nothing of the removed tree stays open. Requires CLEANUP VERIFIED.
# The scratch logs/<PID> folder is pulled + verified + deleted (nots_pull --delete) BEFORE this runs (cleanup_bench refuses otherwise).
export STAMP=20261102T1311Z
B=/home/fb31/projects/BVS/New_Campaign/runs/20261102T1311Z_lowp_bench/code/prod_l_bench
REC=/scratch/fb31/New_Campaign/upload/cleanup_receipt_20261102T1311Z_lowp_bench.txt
cd /scratch/fb31/New_Campaign || { echo "cd failed"; exit 2; }
echo "== dry run $(date -u +%FT%TZ)"
bash $B/cleanup_bench.sh 20261102T1311Z < /dev/null 2>&1 | tail -15; echo "dry_rc=${PIPESTATUS[0]}"
echo "== --yes $(date -u +%FT%TZ)"
bash $B/cleanup_bench.sh 20261102T1311Z --yes --receipt $REC < /dev/null 2>&1 | tail -20; rc=${PIPESTATUS[0]}; echo "cleanup_rc=$rc"
echo "== receipt"; tail -10 $REC 2>&1
exit $rc
