#!/usr/bin/env bash
#SBATCH --account=commons
#SBATCH --partition=commons
#SBATCH --cpus-per-task=1
#SBATCH --mem=4G
#SBATCH --time=01:00:00
#SBATCH --job-name=bvs_full_comparison
#SBATCH --output=logs/comparison_%j.out
#SBATCH --error=logs/comparison_%j.err
set -euo pipefail
cd /home/fb31/archive_control/2026-10-15/comparison_final
trap 'rc=$?; echo "$rc" > "comparison_${SLURM_JOB_ID}.exit"' EXIT
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
{ hostname; date -u; env | sort | grep -E '^(SLURM|OMP|OPENBLAS|MKL)'; python3 --version; sha256sum compare_all.py imports.json comparison.slurm; } > "comparison_${SLURM_JOB_ID}.environment.txt"
python3 compare_all.py
