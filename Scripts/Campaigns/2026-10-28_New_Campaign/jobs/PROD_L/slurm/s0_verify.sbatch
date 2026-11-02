#!/bin/bash
#SBATCH --job-name=lowpL_s0_verify
#SBATCH --account=commons
#SBATCH --partition=commons
#SBATCH --constraint=sapphirerapids
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=2G
#SBATCH --time=00:30:00
set -euo pipefail
PRODL_T0=$(date +%s)
HOME_ROOT="${NC_HOME_ROOT:-/home/fb31/projects/BVS/New_Campaign}"
: "${STAMP:?}" "${WAVE:?}"
source "$HOME_ROOT/runs/${STAMP}_lowp_prodL/code/prod_l/prodl.env"
source "$PILOT_DIR/slurm/common.sh"
pilot_init verify
pilot_modules lowp
pilot_blas_single
mkdir -p -- "$LOG_RUN/p0_verify"
timed verify nots_regen 1 Rscript "$LOWPR_DIR/lowp_verify_nots.R" --manifests "$STUDY/manifests" --dev-manifests "$STUDY/dev/manifests" --study "$STUDY" --out "$LOG_RUN/p0_verify"
timed verify inputs 1 Rscript "$PILOT_DIR/R/prodl_inputs_check.R" --study "$STUDY" --out "$LOG_RUN/p0_verify"
pilot_finish
