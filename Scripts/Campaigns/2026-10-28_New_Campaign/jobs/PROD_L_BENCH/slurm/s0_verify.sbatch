#!/bin/bash
#SBATCH --job-name=lowpB_s0_verify
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
source "$HOME_ROOT/runs/${STAMP}_lowp_bench/code/prod_l_bench/bench.env"
source "$PILOT_DIR/slurm/common.sh"
pilot_init verify
pilot_modules bench
pilot_blas_single
mkdir -p -- "$LOG_RUN/p0_verify"
pilot_require_frozen
timed verify inputs 1 Rscript "$PILOT_DIR/R/prodl_inputs_check.R" --study "$STUDY" --out "$LOG_RUN/p0_verify"
probe_args=(--code "$BENCH_DIR" --library "$R_LIBS_BENCH")
if [ "${PILOT_LOCAL_TEST:-0}" = 1 ]; then probe_args+=(--local-test); fi
timed verify bench_env 1 Rscript "$PILOT_DIR/R/bench_env_probe.R" "${probe_args[@]}"
pilot_finish

