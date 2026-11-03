#!/bin/bash
# plb_close_remote.sh : (NOTS; started detached by remote_bg.sh; PHASE=bench|logs, STAMP in env) PROD_L_BENCH JOB.md §5.
# PHASE=bench: step 4 reconcile_bench.py (STATUS) + clear_stale.sh (list only) + step 5 make_resubmit.sh r1 (must print NOTHING_TO_RESUBMIT,
#              else stop for OPS) + step 6 make_manifests.sh --piece bench (refuses on stale/incomplete). Marker CLOSE_BENCH_OK.
# PHASE=logs : step 6 final_accounting.sh + make_manifests.sh --piece logs. Marker CLOSE_LOGS_OK.
set -uo pipefail
: "${STAMP:?}"; : "${PHASE:?}"
export STAMP
B=/home/fb31/projects/BVS/New_Campaign/runs/${STAMP}_lowp_bench/code/prod_l_bench
cd /scratch/fb31/New_Campaign || { echo "cd failed"; exit 2; }
echo "date=$(date -u +%FT%TZ) PHASE=$PHASE STAMP=$STAMP"
q=$(squeue -h -u fb31 -o '%i %j %T') || { echo "squeue failed"; exit 2; }
printf '%s\n' "$q" | grep -q lowpB_ && { echo "STOP: lowpB_ jobs still queued/running"; exit 3; }
if [ "$PHASE" = bench ]; then
  echo "== reconcile_bench"; python3 $B/reconcile_bench.py "$STAMP" < /dev/null 2>&1 | tail -25; rrc=${PIPESTATUS[0]}; echo "reconcile_rc=$rrc"
  echo "== clear_stale (list only)"; bash $B/clear_stale.sh "$STAMP" < /dev/null 2>&1 | tail -15; echo "clear_stale_rc=${PIPESTATUS[0]}"
  echo "== make_resubmit r1"; mr=$(bash $B/make_resubmit.sh "$STAMP" r1 < /dev/null 2>&1); mrc=$?; printf '%s\n' "$mr" | tail -10; echo "make_resubmit_rc=$mrc"
  printf '%s\n' "$mr" | grep -qx 'NOTHING_TO_RESUBMIT' || { echo "STOP: resubmission lists or exceptions exist (OPS decides / HQ)"; exit 4; }
  [ $rrc -eq 0 ] || { echo "STOP: reconcile_bench nonzero"; exit 4; }
  echo "== make_manifests --piece bench"; bash $B/make_manifests.sh "$STAMP" --piece bench < /dev/null 2>&1 | tail -10; mm=${PIPESTATUS[0]}; echo "make_manifests_bench_rc=$mm"
  [ $mm -eq 0 ] || { echo "STOP: make_manifests bench refused"; exit 5; }
  F=/scratch/fb31/New_Campaign/results/${STAMP}_lowp_benchres
  echo "MANIFEST $F $(sha256sum $F/MANIFEST.sha256 | cut -c1-64) lines=$(wc -l < $F/MANIFEST.sha256)"
  echo "CLOSE_BENCH_OK $(date -u +%FT%TZ)"
elif [ "$PHASE" = logs ]; then
  echo "== final_accounting"; bash $B/final_accounting.sh "$STAMP" < /dev/null 2>&1 | tail -20; fa=${PIPESTATUS[0]}; echo "final_accounting_rc=$fa"
  [ $fa -eq 0 ] || { echo "STOP: final_accounting nonzero"; exit 5; }
  echo "== make_manifests --piece logs"; bash $B/make_manifests.sh "$STAMP" --piece logs < /dev/null 2>&1 | tail -10; mm=${PIPESTATUS[0]}; echo "make_manifests_logs_rc=$mm"
  [ $mm -eq 0 ] || { echo "STOP: make_manifests logs refused"; exit 5; }
  F=/scratch/fb31/New_Campaign/logs/${STAMP}_lowp_bench
  echo "MANIFEST $F $(sha256sum $F/MANIFEST.sha256 | cut -c1-64) lines=$(wc -l < $F/MANIFEST.sha256)"
  ls /home/fb31/projects/BVS/New_Campaign/runs/${STAMP}_lowp_bench/
  echo "CLOSE_LOGS_OK $(date -u +%FT%TZ)"
else echo "bad PHASE"; exit 2; fi
