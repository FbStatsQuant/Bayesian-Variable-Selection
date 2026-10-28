#!/bin/bash
# A2 production array (A2 + SSL-RS in each task), c = 0.5 copy: tasks of 3 datasets (run_chunk.R maps),
# one scale per run, SCALE (default c100). Run kinds (from RUN_ID): prodc050 (map prod, tasks 1-400,
# SCALE=c050), c050check (map prod, SCALE=c100, reproduction of c = 1), pilotc050 (map pilot, tasks 1-4,
# SCALE=c050).
# Submitted only by slurm/submit_prod.sh, from the frozen snapshot, with
#   CODE, RUN_ID, SCALE, DATASETS (empty, or one dataset id with A2_SMOKE=1) set in the sbatch environment, --export=ALL
# (--time and --mem below are the c = 1 values; submit_prod.sh passes the c050 values on the command line.)
# Resources: dev p95 per case (A2 + SSL-RS; 36 cases, three dev runs) 18.8 s -> 3 x 10 x 18.8 s = 9.4 min -> 30 min floor;
# dev max MaxRSS 84 MB -> 2 GB floor.
#SBATCH --job-name=A2_prod
#SBATCH --partition=commons
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=2G
#SBATCH --time=00:30:00
#SBATCH --output=/projects/ml75/fb31/BVS/bench20261019/logs/prod/A2_SSL/%x_%A_%a.out
set -euo pipefail
module load GCC/14.3.0
module load R/4.5.2
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
: "${CODE:?set CODE}" "${RUN_ID:?set RUN_ID}"
DATASETS=${DATASETS:-}; A2_SMOKE=${A2_SMOKE:-0}; SCALE=${SCALE:-c100}
B=/projects/ml75/fb31/BVS/bench20261019
RUN=$B/runs/$RUN_ID
case "$RUN_ID" in
  *_bench20261019_prodc050_A2_SSL) MAP=prod; WANT=c050 ;;
  *_bench20261019_c050check_A2_SSL) MAP=prod; WANT=c100 ;;
  *_bench20261019_pilotc050_A2_SSL) MAP=pilot; WANT=c050 ;;
  *) echo "unexpected RUN_ID $RUN_ID"; exit 2 ;;
esac
[ "$SCALE" = "$WANT" ] || { echo "run $RUN_ID requires SCALE=$WANT (got $SCALE)"; exit 2; }
# A dataset override is allowed only for an explicit single-task smoke job of a prodsmoke run;
# a production run must have no override (both are set by submit_prod.sh in the sbatch process).
if [ -n "$DATASETS" ]; then
  if [ "$A2_SMOKE" != 1 ] || [ "${SLURM_ARRAY_TASK_COUNT:-1}" -ne 1 ] || [[ "$RUN_ID" != *_prodsmoke_* ]]; then
    echo "DATASETS override refused (A2_SMOKE=$A2_SMOKE, tasks=${SLURM_ARRAY_TASK_COUNT:-1}, run=$RUN_ID)"; exit 2
  fi
elif [ "$A2_SMOKE" = 1 ]; then echo "smoke job without a dataset refused"; exit 2; fi
# Refuse to run anything that differs from the frozen record: code, input manifests, library.
(cd "$CODE" && sha256sum --quiet -c "$RUN/code_sha256.txt") || { echo "code snapshot hash mismatch"; exit 2; }
(cd "$RUN/input_manifests" && sha256sum --quiet -c "$RUN/input_manifests_sha256.txt") || { echo "input manifest hash mismatch"; exit 2; }
sha256sum --quiet -c "$RUN/env_sha256.txt" || { echo "library / environment hash mismatch"; exit 2; }
echo "host=$(hostname) cpu=$(grep -m1 'model name' /proc/cpuinfo | cut -d: -f2) start=$(date -u +%FT%TZ) job=${SLURM_ARRAY_JOB_ID:-} task=$SLURM_ARRAY_TASK_ID run_id=$RUN_ID scale=$SCALE map=$MAP"
module list 2>&1 | tr '\n' ' '; echo
Rscript --vanilla "$CODE/run_chunk.R" --task "$SLURM_ARRAY_TASK_ID" --run_id "$RUN_ID" \
  --inputs "$B/inputs" --manifests "$RUN/input_manifests" --out "$B/results" \
  --scale "$SCALE" --map "$MAP" --datasets "$DATASETS" --methods A2,SSL-RS
echo "end=$(date -u +%FT%TZ)"
