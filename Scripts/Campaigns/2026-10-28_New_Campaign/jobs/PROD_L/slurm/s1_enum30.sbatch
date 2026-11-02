#!/bin/bash
#SBATCH --job-name=lowpL_s1_enum30
#SBATCH --account=commons
#SBATCH --partition=commons
#SBATCH --constraint=sapphirerapids
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=16
#SBATCH --mem=1G
#SBATCH --time=00:45:00
set -euo pipefail
PRODL_T0=$(date +%s)
HOME_ROOT="${NC_HOME_ROOT:-/home/fb31/projects/BVS/New_Campaign}"
: "${STAMP:?}" "${WAVE:?}"
source "$HOME_ROOT/runs/${STAMP}_lowp_prodL/code/prod_l/prodl.env"
source "$PILOT_DIR/slurm/common.sh"
pilot_init enum30
pilot_modules lowp
pilot_blas_single
TASK_ID=${SLURM_ARRAY_TASK_ID:-0}; PRODL_WALL_S=$WALL_enum30; UNIT_BUDGET_S=$BUDGET_enum30; P5=0
source "$PILOT_DIR/batch_runner.sh"
