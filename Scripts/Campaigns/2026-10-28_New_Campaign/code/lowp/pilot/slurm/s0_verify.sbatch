#!/bin/bash
#SBATCH --job-name=lowp_p0_verify
#SBATCH --account=commons
#SBATCH --partition=commons
#SBATCH --constraint=sapphirerapids
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=2G
#SBATCH --time=00:30:00
# P0a: LOWP_SPEC L.6 check 4(b) with lowp_verify_nots.R, a CROSS-PLATFORM GENERATOR CHECK (revision 7d, HQ D44): exact checks on what the fits consume
# (file SHA-256, sealed-array hashes, seeds, foldid, names, dims) and |regenerated - sealed| <= 1e-12 * max(1, |sealed|) for the regenerated floats.
# Exit 0 PASS; 1 MISMATCH; 3 INCOMPLETE/malformed. 1 or 3 is a STOP:
# the job fails, and every fitting step (afterok on this job) is cancelled by Slurm.
set -euo pipefail
HOME_ROOT="${NC_HOME_ROOT:-/home/fb31/projects/BVS/New_Campaign}"
: "${STAMP:?STAMP must be exported by submit_pilot.sh}"
PILOT_DIR="$HOME_ROOT/runs/${STAMP}_lowp_pilot/code/lowp/pilot"
source "$PILOT_DIR/pilot.env"
source "$PILOT_DIR/slurm/common.sh"

pilot_init verify
pilot_modules lowp
pilot_blas_single
mkdir -p -- "$LOG_RUN/p0_verify"
timed verify nots_regen 1 Rscript "$LOWPR_DIR/lowp_verify_nots.R" --manifests "$STUDY/manifests" --dev-manifests "$STUDY/dev/manifests" \
  --study "$STUDY" --out "$LOG_RUN/p0_verify"
if [ "$NFAIL" -ne 0 ]; then
  echo "STOP: lowp_verify_nots.R did not PASS (exit 1 = MISMATCH, exit 3 = INCOMPLETE/malformed; see timing/verify.*.tsv rc and p0_verify/NOTS_REGEN_REPORT.md). Nothing downstream will run." >&2
fi
pilot_finish
