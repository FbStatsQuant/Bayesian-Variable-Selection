#!/bin/bash
#SBATCH --job-name=lowp_p8_unlock
#SBATCH --account=commons
#SBATCH --partition=commons
#SBATCH --constraint=sapphirerapids
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=1G
#SBATCH --time=00:15:00
# P8: WAVE UNLOCK FINALIZER, afterany of the lock job and of every fitting job. Refuses to open the trees while any recorded fitting job is
# still active (then it FAILS, leaving the trees locked, which is the safe state; OPS recovery: JOB.md section 10, recover_truth.sh).
# On success it verifies 755/444, 1,200 + 60 files, and file hashes equal to the pre-lock lists of the truth-lock test.
set -euo pipefail
HOME_ROOT="${NC_HOME_ROOT:-/home/fb31/projects/BVS/New_Campaign}"
: "${STAMP:?STAMP must be exported by submit_pilot.sh}"
PILOT_DIR="$HOME_ROOT/runs/${STAMP}_lowp_pilot/code/lowp/pilot"
source "$PILOT_DIR/pilot.env"
source "$PILOT_DIR/slurm/common.sh"

pilot_init unlock
pilot_modules lowp
mkdir -p -- "$LOG_RUN/truthlock"
# every fitting job must be terminal (their ids are in jobids.tsv; this job's own id is not a fitting job)
FITS=$(awk -F'\t' 'NR>1 && $1 ~ /^s[123]_/ && $2 ~ /^[0-9]+$/ {print $2}' "$LOG_RUN/jobids.tsv" | paste -sd, -)
if [ -n "$FITS" ]; then
  Q=$(squeue -h -j "$FITS" -o '%i|%T' 2>&1) || { if echo "$Q" | grep -qi 'invalid job id'; then Q=""; else echo "STOP: cannot query the scheduler ($Q): trees stay LOCKED; see recover_truth.sh" >&2; exit 1; fi; }
  if [ -n "$Q" ]; then echo "STOP: fitting jobs still active, trees stay LOCKED:" >&2; echo "$Q" >&2; exit 1; fi
fi
timed unlock apply 1 env RSCRIPT=Rscript bash "$PILOT_DIR/truth_wave.sh" unlock "$STUDY" "$LOWPR_DIR" "$LOG_RUN/truthlock/WAVE_UNLOCK.txt" "$LOG_RUN/truthlock/evidence"
pilot_finish
