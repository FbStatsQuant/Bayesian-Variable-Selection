#!/bin/bash
#SBATCH --job-name=lowpB_s1_bench
#SBATCH --account=commons
#SBATCH --partition=commons
#SBATCH --constraint=sapphirerapids
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=1G
#SBATCH --time=01:00:00
set -euo pipefail
PRODL_T0=$(date +%s)
HOME_ROOT="${NC_HOME_ROOT:-/home/fb31/projects/BVS/New_Campaign}"
: "${STAMP:?}" "${WAVE:?}"
source "$HOME_ROOT/runs/${STAMP}_lowp_bench/code/prod_l_bench/bench.env"
source "$PILOT_DIR/slurm/common.sh"
pilot_init bench
pilot_modules bench
pilot_blas_single
pilot_require_frozen
TASK_ID=${SLURM_ARRAY_TASK_ID:-0}; PRODL_WALL_S=$WALL_bench; UNIT_BUDGET_S=$BUDGET_bench; P5=0
source "$PILOT_DIR/batch_runner.sh"

