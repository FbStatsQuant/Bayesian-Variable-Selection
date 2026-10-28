#!/bin/bash
#SBATCH --job-name=F4_prod
#SBATCH --partition=commons
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=2G
#SBATCH --time=00:30:00
#SBATCH --output=/projects/ml75/fb31/BVS/bench20261019/logs/prod/F4_MCP_SCAD/%x_%A_%a.out
# Production array for F4 (MCP) and F4_SCAD, c050 copy (BRIEF_C050_ENG): 400 tasks x 3 datasets of one p.
# t = 1..200 -> p = 500, t = 201..400 -> p = 1000; within a p, u = (t - 1) mod 200 and dataset j = 0..2 of the task
# is index i = 3u + j of the c = 1 order (scenario-major, replicate 1..100): S = i/100 + 1, r = i mod 100 + 1.
# Scale key: env C050_SCALE (default c100). Env C050_IDS (dataset ids separated by ':'), if set: task t runs only
# the t-th id of the list (pilot).
# Arguments: CODE_DIR (read-only snapshot) RUN_ID [DATASET_ID]  (DATASET_ID: one-dataset test).
# Submitted only by slurm/submit_prod.sh. The runner skips (case, method) pairs that already have a
# valid .done for the same request, so a resubmission of the same snapshot redoes only missing pairs.
set -uo pipefail
CODE_DIR=$1; RUN_ID=$2; ONLY=${3:-}
source "$CODE_DIR/slurm/env.sh" || exit 4
SNAP=$(dirname "$CODE_DIR")
# Refuse to run code or manifests that differ from the frozen snapshot.
( cd "$CODE_DIR" && sha256sum -c --quiet "$SNAP/code_sha256.txt" ) || { echo "FATAL: code snapshot hash mismatch"; exit 3; }
( cd "$SNAP/frozen" && sha256sum -c --quiet "$SNAP/frozen_sha256.txt" ) || { echo "FATAL: frozen manifest hash mismatch"; exit 3; }
MANIFEST="$SNAP/frozen/inputs_manifest.csv"
echo "modules: $(module -t list 2>&1 | tr '\n' ' ')"
SCALE=${C050_SCALE:-c100}; [[ "$SCALE" =~ ^c[0-9]{3}$ ]] || { echo "FATAL: bad C050_SCALE $SCALE"; exit 2; }
t=${SLURM_ARRAY_TASK_ID:-1}
if [ -n "$ONLY" ]; then
  LIST="$ONLY"
elif [ -n "${C050_IDS:-}" ]; then
  IFS=: read -r -a ALL <<< "$C050_IDS"
  [ "$t" -ge 1 ] && [ "$t" -le ${#ALL[@]} ] || { echo "FATAL: task $t outside C050_IDS"; exit 2; }
  LIST=" ${ALL[$((t - 1))]}"
else
  [ "$t" -ge 1 ] && [ "$t" -le 400 ] || { echo "FATAL: task $t outside 1..400"; exit 2; }
  if [ "$t" -le 200 ]; then p=500; else p=1000; fi
  u=$(( (t - 1) % 200 ))
  LIST=""
  for j in 0 1 2; do i=$(( 3 * u + j )); LIST="$LIST $(printf "p%04d_S%d_r%03d" $p $(( i / 100 + 1 )) $(( i % 100 + 1 )))"; done
fi
echo "host $(hostname) job ${SLURM_ARRAY_JOB_ID:-$SLURM_JOB_ID}_$t run $RUN_ID scale $SCALE datasets:$LIST start $(date -u +%FT%TZ)"
fail=0
for d in $LIST; do
  pp=${d%%_*}
  Rscript --vanilla "$CODE_DIR/run_case.R" --input "$STUDY/inputs/$pp/$d.rds" --out-root "$STUDY/results/$RUN_ID" \
    --run-id "$RUN_ID" --scale "$SCALE" --methods F4,F4_SCAD --manifest "$MANIFEST" || { echo "INFRA_FAILED $d"; fail=1; }
done
echo "end $(date -u +%FT%TZ) fail=$fail"
exit $fail
