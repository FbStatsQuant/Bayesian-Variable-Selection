#!/bin/bash
export STAMP=20261102T2309Z
B=/home/fb31/projects/BVS/New_Campaign/runs/20261102T2309Z_lowp_bench/code/prod_l_bench
REC=/scratch/fb31/New_Campaign/upload/cleanup_receipt_20261102T2309Z_lowp_bench.txt
cd /scratch/fb31/New_Campaign || exit 2
echo "== dry run"; bash $B/cleanup_bench.sh 20261102T2309Z < /dev/null 2>&1 | tail -12; echo "dry_rc=${PIPESTATUS[0]}"
echo "== --yes"; bash $B/cleanup_bench.sh 20261102T2309Z --yes --receipt $REC < /dev/null 2>&1 | tail -15; rc=${PIPESTATUS[0]}; echo "cleanup_rc=$rc"; exit $rc
