#!/bin/bash
#SBATCH --job-name=lowp_p0_lock
#SBATCH --account=commons
#SBATCH --partition=commons
#SBATCH --constraint=sapphirerapids
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=1G
#SBATCH --time=00:10:00
# P0d: WAVE LOCK. After regeneration (P0a) and the permission test (P0c) passed, lock BOTH staged truth trees (mode 000) and VERIFY the lock
# (modes, ls denied, no file visible) before any fitting job is released: every fitting step depends on this job (afterok). The trees stay
# locked until the s8_unlock finalizer (afterany of all fitting jobs). If this job fails, fitting never starts and s8_unlock still restores.
set -euo pipefail
HOME_ROOT="${NC_HOME_ROOT:-/home/fb31/projects/BVS/New_Campaign}"
: "${STAMP:?STAMP must be exported by submit_pilot.sh}"
PILOT_DIR="$HOME_ROOT/runs/${STAMP}_lowp_pilot/code/lowp/pilot"
source "$PILOT_DIR/pilot.env"
source "$PILOT_DIR/slurm/common.sh"

pilot_init lock
pilot_modules lowp
pilot_blas_single
mkdir -p -- "$LOG_RUN/truthlock"
timed lock apply 1 env RSCRIPT=Rscript bash "$PILOT_DIR/truth_wave.sh" lock "$STUDY" "$LOWPR_DIR" "$LOG_RUN/truthlock/WAVE_LOCK.txt"
pilot_finish
