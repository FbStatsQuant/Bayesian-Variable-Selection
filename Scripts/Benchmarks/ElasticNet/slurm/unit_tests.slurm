#!/bin/bash
#SBATCH --job-name=F2_unit
#SBATCH --partition=commons
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=4G
#SBATCH --time=01:00:00
#SBATCH --output=/projects/ml75/fb31/BVS/bench20261019/dev_test/F2_ElasticNet/logs/unit_%j.out
# G3 unit tests for F2 (tests/test_F2_enet.R). Submit from the code folder:
#   sbatch slurm/unit_tests.slurm
set -euo pipefail
CODE=${CODE:-/home/fb31/projects/BVS/Benchmarks/F2_ElasticNet}
source "$CODE/slurm/env.sh"
OUT=$OUTROOT/unit_tests/${SLURM_JOB_ID}
mkdir -p "$OUT"
echo "host $(hostname) job $SLURM_JOB_ID start $(date -u +%FT%TZ)"
Rscript "$CODE/tests/test_F2_enet.R" "$CODE" "$DEV/inputs" "$OUT"
echo "end $(date -u +%FT%TZ)"
