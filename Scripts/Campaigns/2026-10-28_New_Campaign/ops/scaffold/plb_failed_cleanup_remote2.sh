#!/bin/bash
# plb_failed_cleanup_remote2.sh : (NOTS; started detached by remote_bg.sh) HQ D82, step 2 after the evidence copy of scratch
# logs/20261102T1311Z_lowp_bench was VERIFIED at 22:14Z (30 files; receipt manifest e38e7a28…) but its delete was refused while F3 cell 4 ran.
# (a) no fb31 job queued/running; (b) remote_pack.sh delete <folder> <receipt manifest sha> (re-hashes, refuses on any change or active job);
# (c) cleanup_bench.sh dry run + --yes + receipt (HOME/runs/<PID>, SCR/runs/<PID>_cache, SCR/runs/<PID>_tmp). Requires CLEANUP VERIFIED.
export STAMP=20261102T1311Z
L=/scratch/fb31/New_Campaign/logs/20261102T1311Z_lowp_bench; SHA=e38e7a28ef3190b87e419e3ceb3be08bf234ad3e1724689ef6a830d008871915
B=/home/fb31/projects/BVS/New_Campaign/runs/20261102T1311Z_lowp_bench/code/prod_l_bench
REC=/scratch/fb31/New_Campaign/upload/cleanup_receipt_20261102T1311Z_lowp_bench.txt
cd /scratch/fb31/New_Campaign || { echo "cd failed"; exit 2; }
q=$(squeue -h -u fb31 -o '%i %j %T') || { echo "squeue failed"; exit 2; }
[ -z "$q" ] || { echo "jobs still queued/running: $q"; exit 3; }
echo "== verified delete of $L $(date -u +%FT%TZ)"
bash /home/fb31/projects/BVS/New_Campaign/code/ops/remote_pack.sh delete $L $SHA < /dev/null 2>&1 | tail -5; drc=${PIPESTATUS[0]}; echo "logs_delete_rc=$drc"
[ $drc -eq 0 ] && [ ! -e $L ] || { echo "logs delete failed"; exit 4; }
echo "== cleanup_bench dry run $(date -u +%FT%TZ)"
bash $B/cleanup_bench.sh 20261102T1311Z < /dev/null 2>&1 | tail -15; echo "dry_rc=${PIPESTATUS[0]}"
echo "== cleanup_bench --yes $(date -u +%FT%TZ)"
bash $B/cleanup_bench.sh 20261102T1311Z --yes --receipt $REC < /dev/null 2>&1 | tail -20; rc=${PIPESTATUS[0]}; echo "cleanup_rc=$rc"
echo "== receipt"; tail -10 $REC 2>&1
exit $rc
