#!/bin/bash
# finish_h_f3_remote.sh (ON NOTS via: ssh nots 'bash -s' < this):
#  PROD-H JOB.md G without P5 (HQ D62): final_accounting.sh, cleanup_terminal.sh --dry-run, make_manifests.sh; poll.py --cadence report.
#  BENCH_F3_DEV JOB.md "Submit and collect": retry --dry-run (all primaries terminal), reconcile, accounting, timing, sizing (tee, pipefail), manifests.
set -uo pipefail
cd /scratch/fb31/New_Campaign || exit 3
RH=/home/fb31/projects/BVS/New_Campaign/runs/20261030T0934Z_prodH
RID=20261030T1855Z_bench_f3v2_dev; U=/scratch/fb31/New_Campaign/upload/$RID; L=/scratch/fb31/New_Campaign/logs/$RID; SRC=3e01c77b27ad96ad8ec4761b6b25ea5511d357e8aa08a1db7b2972e71734f42c
echo "date=$(date -u +%FT%TZ)"; squeue -h -u fb31 -o '%i %j %T'
echo "===== PROD-H final_accounting"; bash $RH/runner/final_accounting.sh < /dev/null 2>&1 | tail -25; echo "rc=$?"
echo "===== PROD-H cleanup_terminal --dry-run"; bash $RH/runner/cleanup_terminal.sh --dry-run < /dev/null 2>&1 | tail -10; echo "rc=$?"
echo "===== PROD-H make_manifests"; bash $RH/runner/make_manifests.sh < /dev/null 2>&1 | tail -15; echo "rc=$?"
cat $RH/manifests/summary.tsv 2>&1
echo "===== PROD-H poll --cadence"; python3 $RH/runner/poll.py --cadence $RH < /dev/null 2>&1 | tail -c 2500; echo; echo "rc=${PIPESTATUS[0]}"
echo "===== F3 retry --dry-run"; ( source $U/runner/env.sh; python3 $U/runner/retry.py dev $RID --dry-run ) < /dev/null 2>&1 | tail -15; echo "rc=${PIPESTATUS[0]}"
echo "===== F3 reconcile"; python3 $U/runner/reconcile.py --root /scratch/fb31/New_Campaign/results/$RID --kind dev --run-id $RID --source-sha256 $SRC 2>&1 | tee $L/reconcile.txt | tail -25; echo "rc=${PIPESTATUS[0]}"
echo "===== F3 accounting"; python3 $U/runner/accounting.py $L 2>&1 | tee $L/accounting.tsv | tail -8; echo "rc=${PIPESTATUS[0]}"
echo "===== F3 timing"; python3 $U/runner/collect_timing.py dev $L/timing 2>&1 | tee $L/timing.tsv | tail -30; echo "rc=${PIPESTATUS[0]}"
echo "===== F3 sizing"; python3 $U/runner/sizing.py $L/timing.tsv 2>&1 | tee $L/sizing.tsv; echo "rc=${PIPESTATUS[0]}"
echo "===== F3 manifests"; python3 $U/runner/manifests.py --run-log $L /scratch/fb31/New_Campaign/results/$RID/p0500 /scratch/fb31/New_Campaign/results/$RID/p1000 $L 2>&1 | tail -10; echo "rc=${PIPESTATUS[0]}"
