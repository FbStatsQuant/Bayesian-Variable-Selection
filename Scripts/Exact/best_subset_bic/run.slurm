#!/usr/bin/env bash
# Benchmarks/Exact_best_sub/run.slurm — production array for exact best subset + BIC: 600 datasets.
#   sbatch Exact_best_sub/run.slurm RUN_DIR            (RUN_DIR must be new; see slurm/submit_campaign.sh)
#SBATCH --job-name=bench_Exact_best_sub
#SBATCH --account=commons
#SBATCH --partition=commons
#SBATCH --cpus-per-task=1
#SBATCH --mem=4G
#SBATCH --time=01:00:00
#SBATCH --array=1-600%300
#SBATCH --output=/home/fb31/projects/BVS/Benchmarks/logs/%x_%A_%a.out
#SBATCH --error=/home/fb31/projects/BVS/Benchmarks/logs/%x_%A_%a.err
set -euo pipefail
exec bash "${BENCHMARKS_ROOT:-/home/fb31/projects/BVS/Benchmarks}/slurm/run_method.sh" "Exact_best_sub" "${1:?RUN_DIR required}" production
