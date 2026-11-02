#!/bin/bash
# G3 unit tests for F3 (tests/test_F3_alasso.R), one job on commons.
# Submit: sbatch /home/fb31/projects/BVS/Benchmarks/F3_AdaptiveLasso/slurm/run_tests.slurm
#SBATCH --job-name=F3_tests
#SBATCH --partition=commons
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=4G
#SBATCH --time=00:45:00
#SBATCH --output=/projects/ml75/fb31/BVS/bench20261019/dev_test/F3_AdaptiveLasso/logs/tests_%j.out
set -eo pipefail
module load GCC/14.3.0
module load R/4.5.2
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 FLEXIBLAS_NUM_THREADS=1
export R_LIBS_USER=
CODE=${CODE:-/home/fb31/projects/BVS/Benchmarks/F3_AdaptiveLasso}
OUT=/projects/ml75/fb31/BVS/bench20261019/dev_test/F3_AdaptiveLasso
mkdir -p "$OUT/tmp"
echo "host $(hostname) job $SLURM_JOB_ID start $(date -u +%FT%TZ)"
Rscript "$CODE/tests/test_F3_alasso.R" --tmp "$OUT/tmp"
echo "end $(date -u +%FT%TZ)"
