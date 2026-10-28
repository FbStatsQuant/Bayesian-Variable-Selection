#!/bin/bash
# G3 unit tests for A2 (master §III.3.7 i; §IV.3). One CPU, commons partition.
#SBATCH --job-name=A2_tests
#SBATCH --partition=commons
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=2G
#SBATCH --time=00:40:00
#SBATCH --output=/projects/ml75/fb31/BVS/bench20261019/dev_test/A2_SSL/logs/%x_%j.out
set -euo pipefail
module load GCC/14.3.0
module load R/4.5.2
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
CODE=${CODE:-/home/fb31/projects/BVS/Benchmarks/A2_SSL}
OUT=/projects/ml75/fb31/BVS/bench20261019/dev_test/A2_SSL/unit_tests/job_${SLURM_JOB_ID}
DEV_INPUT=/projects/ml75/fb31/BVS/bench20261019/dev/inputs/p0500/dev_p0500_S4_r001.rds
echo "host=$(hostname) start=$(date -u +%FT%TZ) code=$CODE"
Rscript "$CODE/tests/test_A2_ssl.R" --code "$CODE" --out "$OUT" --dev_input "$DEV_INPUT"
Rscript "$CODE/tests/test_check_dev.R" --code "$CODE" --out "$OUT/check_dev_test" --dev_input "$DEV_INPUT" \
  --manifest /projects/ml75/fb31/BVS/bench20261019/dev/manifests/dev_inputs_manifest.csv
echo "end=$(date -u +%FT%TZ)"
