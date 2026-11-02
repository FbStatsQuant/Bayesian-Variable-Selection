#!/bin/bash
#SBATCH --job-name=lowpL_s0_build
#SBATCH --account=commons
#SBATCH --partition=commons
#SBATCH --constraint=sapphirerapids
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=2
#SBATCH --mem=4G
#SBATCH --time=00:40:00
# Main wave step 1: verify the frozen v2.2.1 tree, compile its core (into $CORE_DIR/.cpp_cache) and the enumerator (into scratch) once, so the
# arrays never race on a build; write the environment report. Reused from the pilot's s0_build.sbatch; R/pilot_build.R is the pilot's file, unchanged.
set -euo pipefail
PRODL_T0=$(date +%s)
HOME_ROOT="${NC_HOME_ROOT:-/home/fb31/projects/BVS/New_Campaign}"
: "${STAMP:?}" "${WAVE:?}"
source "$HOME_ROOT/runs/${STAMP}_lowp_prodL/code/prod_l/prodl.env"
source "$PILOT_DIR/slurm/common.sh"
pilot_init build
pilot_modules lowp
pilot_blas_single
pilot_require_frozen
mkdir -p -- "$LOG_RUN/build" "$CACHE_ROOT/enum"
export LOWP_ENUM_CACHE="$CACHE_ROOT/enum" LOWP_CORE_DIR="$CORE_DIR"
timed build compile 1 Rscript "$PRODL_DIR/R/pilot_build.R" --core-dir "$CORE_DIR" --enum-dir "$ENUM_DIR" --out "$LOG_RUN/build"
pilot_finish
