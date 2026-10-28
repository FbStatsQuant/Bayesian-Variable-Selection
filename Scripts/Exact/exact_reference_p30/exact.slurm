#!/usr/bin/env bash
# Benchmarks/Exact_reference/exact.slurm — exact 2^30 posterior per sealed dataset (one array task each).
#   smoke:      sbatch --array=1-6       Exact_reference/exact.slurm smoke
#   production: sbatch --array=1-600%300 Exact_reference/exact.slurm production
# Output: Exact_reference/output/exact/<case_id>.{rds,json}. Experiment 1 measured ~8 min and < 1 GB per enumeration.
#SBATCH --job-name=bvs_exact
#SBATCH --account=commons
#SBATCH --partition=commons
#SBATCH --cpus-per-task=1
#SBATCH --mem=2G
#SBATCH --time=01:00:00
#SBATCH --output=/home/fb31/projects/BVS/Benchmarks/logs/%x_%A_%a.out
#SBATCH --error=/home/fb31/projects/BVS/Benchmarks/logs/%x_%A_%a.err
set -euo pipefail
exec bash "${BENCHMARKS_ROOT:-/home/fb31/projects/BVS/Benchmarks}/Exact_reference/run_exact.sh" "$@"
