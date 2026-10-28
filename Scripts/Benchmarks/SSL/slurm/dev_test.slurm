#!/bin/bash
# A2 dev test: 12 dev datasets (6 scenarios x p in {500, 1000}, dev replicate 1), scale c100,
# method ids A2 and SSL-RS. Array task i runs dataset i of the sorted input list.
# Submit with: sbatch --export=ALL,CODE=<frozen code dir>,RUN_ID=<run id> slurm/dev_test.slurm
#SBATCH --job-name=A2_dev
#SBATCH --partition=commons
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=1G
#SBATCH --time=00:30:00
#SBATCH --array=1-12
#SBATCH --output=/projects/ml75/fb31/BVS/bench20261019/dev_test/A2_SSL/logs/%x_%A_%a.out
set -euo pipefail
module load GCC/14.3.0
module load R/4.5.2
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
: "${CODE:?set CODE}" "${RUN_ID:?set RUN_ID}"
DEV=/projects/ml75/fb31/BVS/bench20261019/dev
OUTROOT=/projects/ml75/fb31/BVS/bench20261019/dev_test/A2_SSL/results
mapfile -t FILES < <(ls "$DEV"/inputs/p0500/*.rds "$DEV"/inputs/p1000/*.rds)
[ "${#FILES[@]}" -eq 12 ] || { echo "expected 12 inputs, found ${#FILES[@]}"; exit 1; }
INPUT=${FILES[$((SLURM_ARRAY_TASK_ID-1))]}
echo "host=$(hostname) start=$(date -u +%FT%TZ) input=$INPUT code=$CODE run_id=$RUN_ID"
Rscript "$CODE/run_case.R" --input "$INPUT" --manifest "$DEV/manifests/dev_inputs_manifest.csv" \
  --out "$OUTROOT" --run_id "$RUN_ID" --scale c100 --methods A2,SSL-RS
echo "end=$(date -u +%FT%TZ)"
