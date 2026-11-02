#!/bin/bash
#SBATCH --job-name=lowp_p2_smc
#SBATCH --account=commons
#SBATCH --partition=commons
#SBATCH --constraint=sapphirerapids
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=2G
#SBATCH --time=04:00:00
# P2: SMC-BVS v2.2.1 (code/core/v2_2_1/study/run_case.R, regime L) on the 24 dev cases (array 0-23, primary seed) and 4 repeat fits (array 24-27); one core each; production allocation 2 GB / 4 h.
set -euo pipefail
HOME_ROOT="${NC_HOME_ROOT:-/home/fb31/projects/BVS/New_Campaign}"
: "${STAMP:?STAMP must be exported by submit_pilot.sh}"
PILOT_DIR="$HOME_ROOT/runs/${STAMP}_lowp_pilot/code/lowp/pilot"
source "$PILOT_DIR/pilot.env"
source "$PILOT_DIR/slurm/common.sh"

pilot_init smc
pilot_modules lowp
pilot_blas_single
pilot_require_frozen
RID="${PILOT_ID}_smc"
line=$(awk -F'\t' -v i="${SLURM_ARRAY_TASK_ID}" 'NR > 1 && $1 == i' "$LISTS/smc_cases.tsv")
[ -n "$line" ] || { echo "no case for array index ${SLURM_ARRAY_TASK_ID}" >&2; exit 66; }
IFS=$'\t' read -r _ ds scale rep <<< "$line"
args=(--case "$ds" --scale "$scale" --study "$DEV_STUDY" --outroot "$SCR_ROOT" --run-id "$RID" --core-dir "$CORE_DIR" --mem-gb 2 --hours 4 --development)
unit="${ds}_${scale}"
if [ "$rep" -gt 0 ]; then args+=(--repeat "$rep"); unit="${unit}_rep${rep}"; fi
timed smc "$unit" 1 Rscript "$V221_DIR/study/run_case.R" "${args[@]}"
pilot_finish
