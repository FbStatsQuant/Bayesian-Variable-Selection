#!/bin/bash
#SBATCH --job-name=lowp_p1_enum20
#SBATCH --account=commons
#SBATCH --partition=commons
#SBATCH --constraint=sapphirerapids
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=4G
#SBATCH --time=01:00:00
# P1a: exact enumeration of the 30 dev datasets at p = 20, 4 OpenMP threads, one CLI call per dataset (as in production).
set -euo pipefail
HOME_ROOT="${NC_HOME_ROOT:-/home/fb31/projects/BVS/New_Campaign}"
: "${STAMP:?STAMP must be exported by submit_pilot.sh}"
PILOT_DIR="$HOME_ROOT/runs/${STAMP}_lowp_pilot/code/lowp/pilot"
source "$PILOT_DIR/pilot.env"
source "$PILOT_DIR/slurm/common.sh"

pilot_init enum20
pilot_modules lowp
pilot_blas_single
THREADS=4
export OMP_NUM_THREADS=$THREADS LOWP_ENUM_CACHE="$CACHE_ROOT/enum" LOWP_CORE_DIR="$CORE_DIR"
RID="${PILOT_ID}_enum20"
while read -r id; do
  timed enum20 "$id" $THREADS Rscript "$ENUM_DIR/run_enum_dataset.R" --dataset "$id" --development --study "$DEV_STUDY" --outroot "$SCR_ROOT" \
    --run-id "$RID" --threads $THREADS --core-dir "$CORE_DIR"
done < <(head -n "${PILOT_LIMIT:-1000}" "$LISTS/enum20.txt")
pilot_finish
