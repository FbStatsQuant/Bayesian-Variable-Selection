#!/bin/bash
# Cross-node reproducibility diagnostic for A2. Submit once per node type, e.g.
#   sbatch --constraint=cascadelake --export=ALL,TAG=cascadelake slurm/diag_node.slurm
#SBATCH --job-name=A2_diag_node
#SBATCH --partition=commons
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=1G
#SBATCH --time=00:15:00
#SBATCH --output=/projects/ml75/fb31/BVS/bench20261019/dev_test/A2_SSL/logs/%x_%j.out
set -euo pipefail
module load GCC/14.3.0
module load R/4.5.2
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
: "${TAG:?set TAG}"
CODE=/home/fb31/projects/BVS/Benchmarks/A2_SSL
OUT=/projects/ml75/fb31/BVS/bench20261019/dev_test/A2_SSL/unit_tests/diag_node
mkdir -p "$OUT"
Rscript "$CODE/tests/diag_node_repro.R" --code "$CODE" --out "$OUT/fit_${TAG}.rds" \
  --dev_input /projects/ml75/fb31/BVS/bench20261019/dev/inputs/p0500/dev_p0500_S4_r001.rds
