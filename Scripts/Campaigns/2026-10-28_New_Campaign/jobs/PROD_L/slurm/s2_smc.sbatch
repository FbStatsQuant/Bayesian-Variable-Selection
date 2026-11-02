#!/bin/bash
#SBATCH --job-name=lowpL_s2_smc
#SBATCH --account=commons
#SBATCH --partition=commons
#SBATCH --constraint=sapphirerapids
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=2G
#SBATCH --time=05:00:00
set -euo pipefail
PRODL_T0=$(date +%s)
HOME_ROOT="${NC_HOME_ROOT:-/home/fb31/projects/BVS/New_Campaign}"
: "${STAMP:?}" "${WAVE:?}"
source "$HOME_ROOT/runs/${STAMP}_lowp_prodL/code/prod_l/prodl.env"
source "$PILOT_DIR/slurm/common.sh"
pilot_init smc
pilot_modules lowp
pilot_blas_single
pilot_require_frozen
TASK_ID=${SLURM_ARRAY_TASK_ID:-0}; PRODL_WALL_S=$WALL_smc; UNIT_BUDGET_S=$BUDGET_smc; P5=0
source "$PILOT_DIR/batch_runner.sh"
