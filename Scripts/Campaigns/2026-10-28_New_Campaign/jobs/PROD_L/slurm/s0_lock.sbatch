#!/bin/bash
#SBATCH --job-name=lowpL_s0_lock
#SBATCH --account=commons
#SBATCH --partition=commons
#SBATCH --constraint=sapphirerapids
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=1G
#SBATCH --time=00:10:00
set -euo pipefail
PRODL_T0=$(date +%s)
HOME_ROOT="${NC_HOME_ROOT:-/home/fb31/projects/BVS/New_Campaign}"
: "${STAMP:?}" "${WAVE:?}"
source "$HOME_ROOT/runs/${STAMP}_lowp_prodL/code/prod_l/prodl.env"
source "$PILOT_DIR/slurm/common.sh"
pilot_init lock
pilot_modules lowp
pilot_blas_single
mkdir -p -- "$LOG_RUN/truthlock/$WAVE"
timed lock apply 1 env RSCRIPT=Rscript bash "$PILOT_DIR/truth_wave.sh" lock "$STUDY" "$LOWPR_DIR" "$LOG_RUN/truthlock/$WAVE/WAVE_LOCK.txt"
pilot_finish
