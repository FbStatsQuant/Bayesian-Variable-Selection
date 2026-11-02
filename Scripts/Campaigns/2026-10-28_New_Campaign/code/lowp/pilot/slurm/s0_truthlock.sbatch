#!/bin/bash
#SBATCH --job-name=lowp_p0_truthlock
#SBATCH --account=commons
#SBATCH --partition=commons
#SBATCH --constraint=sapphirerapids
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=2G
#SBATCH --time=00:30:00
# P0c: Linux truth-lock TEST (code/lowp/tests/test_truth_lock_linux.sh) as the ordinary user on the HOME filesystem, on the study COPY
# $STUDY (truth/ 1,200 files, dev/truth/ 60): lock, check unreadable, unlock with one call, recover from two bad states. A GATE: the wave lock
# (s0_lock) and every fitting step depend on its success (afterok). It ends with the trees at 755/444. Its evidence (run.log, pre/post sha lists,
# modes, lock/unlock logs, final_status.txt) goes to LOG/truthlock/evidence on SCRATCH.
set -euo pipefail
HOME_ROOT="${NC_HOME_ROOT:-/home/fb31/projects/BVS/New_Campaign}"
: "${STAMP:?STAMP must be exported by submit_pilot.sh}"
PILOT_DIR="$HOME_ROOT/runs/${STAMP}_lowp_pilot/code/lowp/pilot"
source "$PILOT_DIR/pilot.env"
source "$PILOT_DIR/slurm/common.sh"

pilot_init truthlock
pilot_modules lowp
pilot_blas_single
EVD="$LOG_RUN/truthlock/evidence"
mkdir -p -- "$LOG_RUN/truthlock"
{ echo "# P0c truth-lock test on $(hostname) at $(date -u +%FT%TZ) as $(id -un) (uid $(id -u)); study copy $STUDY"
  echo "# filesystem: $(df -PT "$STUDY" | tail -n 1)"
  echo "# before: truth $(stat -c '%a' "$STUDY/truth") dev/truth $(stat -c '%a' "$STUDY/dev/truth")"; } > "$LOG_RUN/truthlock/TRUTHLOCK_HEADER.txt"
timed truthlock test 1 env RSCRIPT=Rscript bash "$CODE/lowp/tests/test_truth_lock_linux.sh" "$STUDY" "$CODE/lowp/R" --evidence-dir "$EVD"
{ echo "# after: truth $(stat -c '%a' "$STUDY/truth") dev/truth $(stat -c '%a' "$STUDY/dev/truth"); dirs not 755: $(find "$STUDY/truth" "$STUDY/dev/truth" -type d ! -perm 755 | wc -l); files not 444: $(find "$STUDY/truth" "$STUDY/dev/truth" -type f ! -perm 444 | wc -l)"; } > "$LOG_RUN/truthlock/TRUTHLOCK_AFTER.txt"
pilot_finish
