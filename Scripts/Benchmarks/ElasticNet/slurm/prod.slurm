#!/bin/bash
#SBATCH --job-name=F2_prod
#SBATCH --partition=commons
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --output=/projects/ml75/fb31/BVS/bench20261019/logs/prod/F2_ElasticNet/%x_%A_%a.out
# Production F2, c050 copy (BRIEF_C050_ENG). --array, --time and --mem are given by submit_prod.sh.
# Task t (1..400): p = 500 for t <= 200, else 1000; u = (t - 1) mod 200; dataset j = 0..2 of the task is
# index i = 3u + j of the c = 1 order (scenario-major, replicate 1..100): s = floor(i / 100) + 1, r = i mod 100 + 1.
# Scale key: env C050_SCALE (default c100). Env C050_IDS (dataset ids separated by ':'), if set: task t runs
# only the t-th id of the list (pilot). Needs RUN_ID and CODE (snapshot).
set -uo pipefail
: "${RUN_ID:?}" "${CODE:?}"
source "$CODE/slurm/env.sh"
INPUTS=$STUDY/inputs; MANIFEST=$CODE/../inputs_manifest.csv; RESULTS=$STUDY/results   # frozen manifest copy
# Refuse to run from a snapshot whose files changed after freezing.
( cd "$CODE" && sha256sum -c --quiet ../code_sha256.txt ) || { echo "snapshot hash mismatch"; exit 3; }
( cd "$CODE/.." && sha256sum -c --quiet frozen_sha256.txt ) || { echo "frozen manifest hash mismatch"; exit 3; }
SCALE=${C050_SCALE:-c100}; [[ "$SCALE" =~ ^c[0-9]{3}$ ]] || { echo "bad C050_SCALE $SCALE"; exit 2; }
T=${SLURM_ARRAY_TASK_ID:-1}
if [ -n "${C050_IDS:-}" ]; then
  IFS=: read -r -a ALL <<< "$C050_IDS"
  [ "$T" -ge 1 ] && [ "$T" -le ${#ALL[@]} ] || { echo "task $T outside C050_IDS"; exit 2; }
  IDS=${ALL[$((T - 1))]}
else
  [ "$T" -ge 1 ] && [ "$T" -le 400 ] || { echo "task $T outside 1..400"; exit 2; }
  if [ "$T" -le 200 ]; then P=500; else P=1000; fi
  U=$(( (T - 1) % 200 ))
  IDS=$(for J in 0 1 2; do I=$(( 3 * U + J )); printf "p%04d_S%d_r%03d " "$P" $(( I / 100 + 1 )) $(( I % 100 + 1 )); done)
fi
echo "host $(hostname) job ${SLURM_ARRAY_JOB_ID:-$SLURM_JOB_ID}_${T} scale $SCALE datasets: $IDS start $(date -u +%FT%TZ)"
FAIL=0
for ID in $IDS; do
  PP=${ID%%_*}
  Rscript "$CODE/run_case.R" --input "$INPUTS/$PP/$ID.rds" --out "$RESULTS" --run-id "$RUN_ID" \
    --scales "$SCALE" --methods F2 --manifest "$MANIFEST" --code-dir "$CODE" || { echo "INFRA_FAIL $ID"; FAIL=1; }
done
echo "end $(date -u +%FT%TZ) fail=$FAIL"
exit $FAIL
