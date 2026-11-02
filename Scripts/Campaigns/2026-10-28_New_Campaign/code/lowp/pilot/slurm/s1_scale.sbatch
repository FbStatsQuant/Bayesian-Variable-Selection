#!/bin/bash
#SBATCH --job-name=lowp_p1_scale
#SBATCH --account=commons
#SBATCH --partition=commons
#SBATCH --constraint=sapphirerapids
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=32
#SBATCH --mem=8G
#SBATCH --time=01:00:00
# P1c: thread scaling on dev_p0030_S4_r001: 3% task subset at 1 and 8 threads (two repetitions each), full enumeration at 8, 16 and 32 threads.
set -euo pipefail
HOME_ROOT="${NC_HOME_ROOT:-/home/fb31/projects/BVS/New_Campaign}"
: "${STAMP:?STAMP must be exported by submit_pilot.sh}"
PILOT_DIR="$HOME_ROOT/runs/${STAMP}_lowp_pilot/code/lowp/pilot"
source "$PILOT_DIR/pilot.env"
source "$PILOT_DIR/slurm/common.sh"

pilot_init scale
pilot_modules lowp
pilot_blas_single
export LOWP_ENUM_CACHE="$CACHE_ROOT/enum" LOWP_CORE_DIR="$CORE_DIR"
DS=dev_p0030_S4_r001
mkdir -p -- "$LOG_RUN/scaling"
# (1) subset hook: the same 3% of the 1,024 tasks at 1 and 8 threads, two repetitions each
for rep in 1 2; do
  for thr in 1 8; do
    export OMP_NUM_THREADS=$thr
    timed scale "subset_t${thr}_rep${rep}" $thr Rscript "$PILOT_DIR/R/pilot_scaling_subset.R" --input "$DEV_STUDY/inputs/p0030/$DS.rds" \
      --threads $thr --fraction 0.03 --rep $rep --core-dir "$CORE_DIR" --out "$LOG_RUN/scaling/scaling_subset.csv"
  done
done
# (2) full enumeration through the production CLI at 8, 16, 32 threads (separate run ids; the results must be identical)
for thr in 8 16 32; do
  export OMP_NUM_THREADS=$thr
  timed scale "full_t${thr}" $thr Rscript "$ENUM_DIR/run_enum_dataset.R" --dataset "$DS" --development --study "$DEV_STUDY" --outroot "$SCR_ROOT" \
    --run-id "$(printf '%s_scale_t%02d' "$PILOT_ID" $thr)" --threads $thr --core-dir "$CORE_DIR"
done
pilot_finish
