#!/bin/bash
#SBATCH --job-name=lowpL_s0_truthlock
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
pilot_init truthlock
pilot_modules lowp
pilot_blas_single
EVD="$LOG_RUN/truthlock/$WAVE/evidence"
mkdir -p -- "$LOG_RUN/truthlock/$WAVE"
{ echo "# truth-lock test $(date -u +%FT%TZ) host=$(hostname) study=$STUDY"; df -PT "$STUDY"; stat -c '%a %n' "$STUDY/truth" "$STUDY/dev/truth"; } > "$LOG_RUN/truthlock/$WAVE/TRUTHLOCK_HEADER.txt"
timed truthlock test 1 env RSCRIPT=Rscript bash "$CODE/lowp/tests/test_truth_lock_linux.sh" "$STUDY" "$LOWPR_DIR" --evidence-dir "$EVD"
pilot_finish
