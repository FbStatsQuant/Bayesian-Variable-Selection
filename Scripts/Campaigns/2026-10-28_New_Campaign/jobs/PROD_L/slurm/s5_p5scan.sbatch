#!/bin/bash
#SBATCH --job-name=lowpL_s5_p5scan
#SBATCH --account=commons
#SBATCH --partition=commons
#SBATCH --constraint=sapphirerapids
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=2G
#SBATCH --time=08:10:00
# The --time above is a default only: submit_prodl.sh passes --time computed from the number of records scanned, primaries plus possible P5
# retries (HQ D63; 14,400 primaries and no retry -> 08:10:00).
set -euo pipefail
PRODL_T0=$(date +%s)
HOME_ROOT="${NC_HOME_ROOT:-/home/fb31/projects/BVS/New_Campaign}"
: "${STAMP:?}" "${WAVE:?}" "${PHASE:?}"
[[ $PHASE =~ ^(initial|final[0-9]*|r[0-9]+)$ ]] || exit 2
source "$HOME_ROOT/runs/${STAMP}_lowp_prodL/code/prod_l/prodl.env"
source "$PILOT_DIR/slurm/common.sh"
pilot_init p5scan
pilot_modules lowp
pilot_blas_single
pilot_require_frozen
mkdir -p -- "$LOG_RUN/p5"
timed p5scan smc 1 Rscript "$V221_DIR/tools/p5_scan.R" --run-dir "$SCR_ROOT/results/$RUNID_smc" --out "$LOG_RUN/p5/scan_${PHASE}_smc.tsv"
timed p5scan smcrep 1 Rscript "$V221_DIR/tools/p5_scan.R" --run-dir "$SCR_ROOT/results/$RUNID_smcrep" --out "$LOG_RUN/p5/scan_${PHASE}_smcrep.tsv"
if [[ $NFAIL == 0 ]]; then printf 'phase=%s\n' "$PHASE" > "$LOG_RUN/p5/scan_${PHASE}.ok"; fi
pilot_finish
