#!/bin/bash
#SBATCH --job-name=lowp_p1_bitid
#SBATCH --account=commons
#SBATCH --partition=commons
#SBATCH --constraint=sapphirerapids
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=16
#SBATCH --mem=8G
#SBATCH --time=01:00:00
# P1d: enumerator vs the NOTS-compiled core (v3_enumerate) and vs Scorer::score: bit identity of F and eta (pilot/R/pilot_bitid.R).
set -euo pipefail
HOME_ROOT="${NC_HOME_ROOT:-/home/fb31/projects/BVS/New_Campaign}"
: "${STAMP:?STAMP must be exported by submit_pilot.sh}"
PILOT_DIR="$HOME_ROOT/runs/${STAMP}_lowp_pilot/code/lowp/pilot"
source "$PILOT_DIR/pilot.env"
source "$PILOT_DIR/slurm/common.sh"

pilot_init bitid
pilot_modules lowp
pilot_blas_single
THREADS=16
export OMP_NUM_THREADS=$THREADS LOWP_ENUM_CACHE="$CACHE_ROOT/enum" LOWP_CORE_DIR="$CORE_DIR"
mkdir -p -- "$LOG_RUN/bitid"
timed bitid all $THREADS Rscript "$PILOT_DIR/R/pilot_bitid.R" --dev-study "$DEV_STUDY" --core-dir "$CORE_DIR" --enum-dir "$ENUM_DIR" \
  --threads $THREADS --out "$LOG_RUN/bitid"
pilot_finish
