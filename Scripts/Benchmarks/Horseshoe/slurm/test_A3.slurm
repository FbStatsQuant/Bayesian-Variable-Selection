#!/bin/bash
# G3 unit tests of A3 (master §III.3.8 i), one job, 1 CPU.
#SBATCH --job-name=A3_tests
#SBATCH --partition=commons
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=4G
#SBATCH --time=01:00:00
#SBATCH --output=/projects/ml75/fb31/BVS/bench20261019/dev_test/A3_Horseshoe/logs/tests_%j.out
set -euo pipefail
CODE=${A3_CODE:-/home/fb31/projects/BVS/Benchmarks/A3_Horseshoe}
source "$CODE/slurm/env.sh"
OUTDIR=$A3_OUT/tests/${SLURM_JOB_ID}
mkdir -p "$OUTDIR"
echo "host $(hostname)  nproc $(nproc)  start $(date -u +%FT%TZ)  code $CODE"
Rscript -e 'cat("detectCores:", parallel::detectCores(), "\n")'
Rscript "$CODE/tests/test_A3_horseshoe.R" "$OUTDIR"
echo "end $(date -u +%FT%TZ)"
