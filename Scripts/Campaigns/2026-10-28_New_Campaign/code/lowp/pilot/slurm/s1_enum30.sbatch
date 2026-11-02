#!/bin/bash
#SBATCH --job-name=lowp_p1_enum30
#SBATCH --account=commons
#SBATCH --partition=commons
#SBATCH --constraint=sapphirerapids
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=16
#SBATCH --mem=4G
#SBATCH --time=01:00:00
# P1b: exact enumeration of the p = 30 dev datasets, r = 1, scenarios S1..S6 (array 0-5), 16 threads (as the production enum30 task).
set -euo pipefail
HOME_ROOT="${NC_HOME_ROOT:-/home/fb31/projects/BVS/New_Campaign}"
: "${STAMP:?STAMP must be exported by submit_pilot.sh}"
PILOT_DIR="$HOME_ROOT/runs/${STAMP}_lowp_pilot/code/lowp/pilot"
source "$PILOT_DIR/pilot.env"
source "$PILOT_DIR/slurm/common.sh"

pilot_init enum30
pilot_modules lowp
pilot_blas_single
THREADS=16
export OMP_NUM_THREADS=$THREADS LOWP_ENUM_CACHE="$CACHE_ROOT/enum" LOWP_CORE_DIR="$CORE_DIR"
RID="${PILOT_ID}_enum30"
id=$(sed -n "$((SLURM_ARRAY_TASK_ID + 1))p" "$LISTS/enum30.txt")
[ -n "$id" ] || { echo "no dataset for array index ${SLURM_ARRAY_TASK_ID}" >&2; exit 66; }
timed enum30 "$id" $THREADS Rscript "$ENUM_DIR/run_enum_dataset.R" --dataset "$id" --development --study "$DEV_STUDY" --outroot "$SCR_ROOT" \
  --run-id "$RID" --threads $THREADS --core-dir "$CORE_DIR"
pilot_finish
