#!/bin/bash
#SBATCH --job-name=F2_prod
#SBATCH --partition=commons
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --output=/projects/ml75/fb31/BVS/bench20261019/logs/prod/F2_ElasticNet/%x_%A_%a.out
# Production F2 (scale c100 only, decision D3). --array, --time and --mem are given by
# submit_prod.sh. Task t (1..120): p = 500 for t <= 60, else 1000; u = (t - 1) mod 60;
# scenario s = floor(u / 10) + 1; replicates 10 (u mod 10) + 1 ... + 10.
# SMOKE=1: run only p1000_S4_r001 (the smoke test). Needs RUN_ID and CODE (snapshot).
set -uo pipefail
: "${RUN_ID:?}" "${CODE:?}"
source "$CODE/slurm/env.sh"
INPUTS=$STUDY/inputs; MANIFEST=$CODE/../inputs_manifest.csv; RESULTS=$STUDY/results   # frozen manifest copy
# Refuse to run from a snapshot whose files changed after freezing.
( cd "$CODE" && sha256sum -c --quiet ../code_sha256.txt ) || { echo "snapshot hash mismatch"; exit 3; }
( cd "$CODE/.." && sha256sum -c --quiet frozen_sha256.txt ) || { echo "frozen manifest hash mismatch"; exit 3; }
T=${SLURM_ARRAY_TASK_ID:-1}
if [ "${SMOKE:-0}" = "1" ]; then
  IDS="p1000_S4_r001"
else
  if [ "$T" -le 60 ]; then P=500; else P=1000; fi
  U=$(( (T - 1) % 60 )); S=$(( U / 10 + 1 )); R0=$(( (U % 10) * 10 ))
  IDS=$(for r in $(seq $((R0 + 1)) $((R0 + 10))); do printf "p%04d_S%d_r%03d " "$P" "$S" "$r"; done)
fi
echo "host $(hostname) job ${SLURM_ARRAY_JOB_ID:-$SLURM_JOB_ID}_${T} datasets: $IDS start $(date -u +%FT%TZ)"
FAIL=0
for ID in $IDS; do
  PP=${ID%%_*}
  Rscript "$CODE/run_case.R" --input "$INPUTS/$PP/$ID.rds" --out "$RESULTS" --run-id "$RUN_ID" \
    --scales c100 --methods F2 --manifest "$MANIFEST" --code-dir "$CODE" || { echo "INFRA_FAIL $ID"; FAIL=1; }
done
echo "end $(date -u +%FT%TZ) fail=$FAIL"
exit $FAIL
