#!/usr/bin/env bash
# submit_g0.sh -- P1M gate G0 submission, run ON NOTS by the Engineering manager after HQ's go (helpers never run it).
# Usage: bash ~/SMC_Engineering_Department/scripts/g0/submit_g0.sh kernel|stage|all
# One sbatch per job type (job arrays): kernel = array of 1 task; stage = array of 2 tasks (5k, 10k).
# After the stage sbatch, task 1 (5k) is lowered from the array limit 17:30:00 to 07:00:00 (users may lower limits).
# Worst-case admission: kernel 96 CPUs x 5 min = 8.0; stage 2 x 7 h + 2 x 17.5 h = 49.0; total 57.0 billed core-h.
# No polling here. Check later with ONE call, at most every 5 minutes:
#   squeue -u fb31 -n p1m_g0_kernel,p1m_g0_stage -o '%.18i %.14j %.8T %.10M %.10l %.6C %R'
set -euo pipefail
WHAT=${1:?kernel|stage|all}
DEPT=/home/fb31/SMC_Engineering_Department
SCR=$DEPT/scripts/g0
LEDGER=$DEPT/scratch/runs/g0/submissions.jsonl
cd "$SCR"
sha256sum --quiet -c SHA256SUMS || { echo "FATAL: scripts differ from SHA256SUMS (deploy again)" >&2; exit 66; }
[[ -d $DEPT/scratch/slurm_out && -d $DEPT/scratch/tmp ]] || { echo "FATAL: scratch/slurm_out or scratch/tmp missing" >&2; exit 66; }
mkdir -p "$DEPT/scratch/runs/g0/build"
log() { printf '{"what":"%s","job":"%s","worst_core_h":%s,"submitted_utc":"%s","script_sha256":"%s"}\n' "$1" "$2" "$3" "$(date -u +%FT%TZ)" "$4" | tee -a "$LEDGER"; }
if [[ $WHAT == kernel || $WHAT == all ]]; then
  jk=$(sbatch --parsable kernel/run_kernel.sbatch)
  log kernel "$jk" 8.0 "$(sha256sum kernel/run_kernel.sbatch | cut -c1-16)"
fi
if [[ $WHAT == stage || $WHAT == all ]]; then
  js=$(sbatch --parsable stage/run_stage.sbatch)
  if scontrol update JobId="${js}_1" TimeLimit=07:00:00; then
    log stage "$js" 49.0 "$(sha256sum stage/run_stage.sbatch | cut -c1-16)"
  else
    log stage_LIMIT_NOT_LOWERED "$js" 70.0 "$(sha256sum stage/run_stage.sbatch | cut -c1-16)"
    echo "WARNING: task ${js}_1 keeps 17:30:00 (worst case 70 core-h for stage). Lower it by hand or scancel ${js}_1." >&2
  fi
fi
