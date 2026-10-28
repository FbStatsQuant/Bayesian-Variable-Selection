#!/bin/bash
# Diagnosis of unit test i.2 (build flags versus patch). One CPU, commons partition.
#SBATCH --job-name=A2_diag_i2
#SBATCH --partition=commons
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=2G
#SBATCH --time=00:20:00
#SBATCH --output=/projects/ml75/fb31/BVS/bench20261019/dev_test/A2_SSL/logs/%x_%j.out
set -euo pipefail
module load GCC/14.3.0
module load R/4.5.2
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
CODE=/home/fb31/projects/BVS/Benchmarks/A2_SSL
Rscript "$CODE/tests/diag_i2_build.R" --code "$CODE" \
  --out /projects/ml75/fb31/BVS/bench20261019/dev_test/A2_SSL/unit_tests/diag_i2_${SLURM_JOB_ID} \
  --dev_input /projects/ml75/fb31/BVS/bench20261019/dev/inputs/p0500/dev_p0500_S4_r001.rds
