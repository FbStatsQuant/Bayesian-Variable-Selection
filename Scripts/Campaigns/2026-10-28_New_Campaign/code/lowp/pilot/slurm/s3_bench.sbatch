#!/bin/bash
#SBATCH --job-name=lowp_p3_bench
#SBATCH --account=commons
#SBATCH --partition=commons
#SBATCH --constraint=sapphirerapids
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=6G
#SBATCH --time=02:00:00
# P3: the 8 benchmark methods on the 24 dev cases (array 0-23), one Rscript per method so that each gets its own runtime and max RSS.
# R 4.5.2; --library points to the pinned study library (read only, under the benchmark freeze). Real dev ids, --development, outputs under SCR/results/RID.
# PILOT_BENCH_EXTRA is a local-test hook only (e.g. --test-library for an unpinned laptop library); never set on NOTS.
set -euo pipefail
HOME_ROOT="${NC_HOME_ROOT:-/home/fb31/projects/BVS/New_Campaign}"
: "${STAMP:?STAMP must be exported by submit_pilot.sh}"
PILOT_DIR="$HOME_ROOT/runs/${STAMP}_lowp_pilot/code/lowp/pilot"
source "$PILOT_DIR/pilot.env"
source "$PILOT_DIR/slurm/common.sh"

pilot_init bench
pilot_modules bench
pilot_blas_single
RID="${PILOT_ID}_bench"
line=$(awk -F'\t' -v i="${SLURM_ARRAY_TASK_ID}" 'NR > 1 && $1 == i' "$LISTS/bench_cases.tsv")
[ -n "$line" ] || { echo "no case for array index ${SLURM_ARRAY_TASK_ID}" >&2; exit 66; }
IFS=$'\t' read -r _ ds scale <<< "$line"
METHODS="${PILOT_BENCH_METHODS:-F1 F2 F3 F4 F5 A1 A2 A3}"
for m in $METHODS; do
  timed bench "${ds}_${scale}_${m}" 1 Rscript "$BENCH_DIR/run_bench_case.R" --study "$DEV_STUDY" --outroot "$SCR_ROOT" --run-id "$RID" \
    --case "$ds" --scale "$scale" --methods "$m" --development --threads-check --library "$R_LIBS_BENCH" ${PILOT_BENCH_EXTRA:-}
done
pilot_finish
