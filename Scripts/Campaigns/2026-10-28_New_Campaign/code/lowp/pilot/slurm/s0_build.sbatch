#!/bin/bash
#SBATCH --job-name=lowp_p0_build
#SBATCH --account=commons
#SBATCH --partition=commons
#SBATCH --constraint=sapphirerapids
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=2
#SBATCH --mem=4G
#SBATCH --time=00:40:00
# P0a: verify the frozen v2.2.1 tree, compile its core and the enumerator once (cache) so the arrays never race on a build; write the environment report.
# Submitted by ../submit_pilot.sh (it adds --output, --error, --array, --dependency and --export=ALL,STAMP=...).
set -euo pipefail
HOME_ROOT="${NC_HOME_ROOT:-/home/fb31/projects/BVS/New_Campaign}"
: "${STAMP:?STAMP must be exported by submit_pilot.sh}"
PILOT_DIR="$HOME_ROOT/runs/${STAMP}_lowp_pilot/code/lowp/pilot"
source "$PILOT_DIR/pilot.env"
source "$PILOT_DIR/slurm/common.sh"

pilot_init build
pilot_modules lowp
pilot_blas_single
pilot_require_frozen
mkdir -p -- "$LOG_RUN/build" "$CACHE_ROOT/enum"
export LOWP_ENUM_CACHE="$CACHE_ROOT/enum" LOWP_CORE_DIR="$CORE_DIR"
# one process compiles the core into $CORE_DIR/.cpp_cache (home, owner-writable) and the enumerator into scratch
timed build compile 1 Rscript "$PILOT_DIR/R/pilot_build.R" --core-dir "$CORE_DIR" --enum-dir "$ENUM_DIR" --out "$LOG_RUN/build"
pilot_finish
