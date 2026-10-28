#!/usr/bin/env bash
# Benchmarks/Exact_reference/run_exact.sh — map a Slurm array index to one (scenario, replicate) and enumerate.
# Usage (inside a Slurm array job): run_exact.sh MODE [OUT_DIR]
#   smoke      : array 1-6   -> scenario = index, replicate = 1
#   production : array 1-600 -> scenario = (index-1) %/% 100 + 1, replicate = (index-1) %% 100 + 1
set -euo pipefail
mode=${1:-production}; out_dir=${2:-}
root=${BENCHMARKS_ROOT:-/home/fb31/projects/BVS/Benchmarks}
cd "$root"
source slurm/environment.sh
export E2_CPP_CACHE="${TMPDIR:-/tmp}/exact_cpp_${USER}_${SLURM_JOB_ID:-local}_${SLURM_ARRAY_TASK_ID:-0}"
task=${SLURM_ARRAY_TASK_ID:?must run as a Slurm array}
if [[ "$mode" == smoke ]]; then
  ((task>=1 && task<=6)) || exit 64
  scenario=$task; replicate=1
elif [[ "$mode" == production ]]; then
  ((task>=1 && task<=600)) || exit 64
  scenario=$(( (task-1)/100+1 )); replicate=$(( (task-1)%100+1 ))
else
  echo "unknown mode $mode" >&2; exit 64
fi
exec Rscript --vanilla Exact_reference/compute_exact.R "$scenario" "$replicate" ${out_dir:+"$out_dir"}
