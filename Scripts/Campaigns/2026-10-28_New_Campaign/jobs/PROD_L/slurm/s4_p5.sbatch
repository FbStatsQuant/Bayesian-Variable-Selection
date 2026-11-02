#!/bin/bash
#SBATCH --job-name=lowpL_s4_p5
#SBATCH --account=commons
#SBATCH --partition=commons
#SBATCH --constraint=sapphirerapids
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=4G
#SBATCH --time=09:00:00
set -euo pipefail
PRODL_T0=$(date +%s)
HOME_ROOT="${NC_HOME_ROOT:-/home/fb31/projects/BVS/New_Campaign}"
: "${STAMP:?}" "${WAVE:?}"
source "$HOME_ROOT/runs/${STAMP}_lowp_prodL/code/prod_l/prodl.env"
source "$PILOT_DIR/slurm/common.sh"
pilot_init p5
[ -n "$TIME_BIN" ] || [ "${PILOT_DRYRUN:-0}" = 1 ] || { echo "GNU time required for fitting" >&2; exit 68; }
pilot_modules lowp
pilot_blas_single
pilot_require_frozen
TASK_ID=${SLURM_ARRAY_TASK_ID:-0}; PRODL_WALL_S=$WALL_p5; UNIT_BUDGET_S=$BUDGET_p5; P5=1
source "$PILOT_DIR/batch_runner.sh"
