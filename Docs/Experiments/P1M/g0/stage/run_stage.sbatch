#!/usr/bin/env bash
# run_stage.sbatch -- P1M gate G0, Part S: stage-level island records with revision D UNMODIFIED. One array, 2 tasks:
#   task 1: p =  5,000, tier-0 calibration + 16 islands of N = 2,500; guard 6.70 h; limit 07:00:00 (set after submission)
#   task 2: p = 10,000, tier-0 calibration +  8 islands of N = 2,500; guard 17.20 h; limit 17:30:00 (the array limit)
# Single thread; --cpus-per-task=1 gives 2 allocated (billed) CPUs = one core, as in W3-SCALE B3.
# Limits = 1.5 x B3 timings (5k: 1.9 h + 16 x 0.17 h; 10k: 5.9 h + 8 x 0.7 h). --mem = 2 x B3 MaxRSS (1.22 / 2.38 GB),
# rounded up to the larger task: 5G for both (memory is not billed).
# An array has one --time: it is submitted with 17:30:00 and task 1 is lowered at once with
#   scontrol update JobId=<array job>_1 TimeLimit=07:00:00
# (submit_g0.sh does both). Worst-case admission: 2 x 7 h + 2 x 17.5 h = 14 + 35 = 49 billed core-h.
# The runtime guard (--hours) stops the run cleanly before the limit and the record is saved; an R-level timeout is not
# needed. Task 1 also runs under `timeout 6h57m` so it cannot exceed 7 h even if the scontrol update was not applied.
#SBATCH --job-name=p1m_g0_stage
#SBATCH --account=commons
#SBATCH --partition=commons
#SBATCH --qos=nots_commons
#SBATCH --array=1-2
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=5G
#SBATCH --time=17:30:00
#SBATCH --constraint=sapphirerapids
#SBATCH --export=NONE
#SBATCH --no-requeue
#SBATCH --output=/home/fb31/SMC_Engineering_Department/scratch/slurm_out/%x_%A_%a.out
#SBATCH --error=/home/fb31/SMC_Engineering_Department/scratch/slurm_out/%x_%A_%a.err
set -euo pipefail
DEPT=/home/fb31/SMC_Engineering_Department
SCR=$DEPT/scripts/g0/stage
CODE=/scratch/fb31/w3scale/code/v32dev_6866f57/Scripts/SMC_BVS/core_v32dev     # revision D, read only
B3=/scratch/fb31/w3scale/out                                                    # B3 census records, read only
RUN=$DEPT/scratch/runs/g0/stage_${SLURM_ARRAY_JOB_ID}
case $SLURM_ARRAY_TASK_ID in
  1) P=5000;  R=16; HOURS=6.70;  WRAP=(timeout 6h57m) ;;
  2) P=10000; R=8;  HOURS=17.20; WRAP=() ;;
  *) echo "no task $SLURM_ARRAY_TASK_ID" >&2; exit 65 ;;
esac
source "$SCR/env_scale.sh" >/dev/null 2>&1      # GCC 14.3.0, R 4.5.2, one numerical thread (W3-SCALE environment)
export TMPDIR=$DEPT/scratch/tmp/$SLURM_JOB_ID
mkdir -p "$RUN/res" "$RUN/log" "$TMPDIR"; trap 'rm -rf "$TMPDIR"' EXIT
( cd "$SCR" && sha256sum stage_measure.R ws_common.R env_scale.sh revD_SHA256SUMS run_stage.sbatch ) > "$RUN/log/scripts_sha256_task${SLURM_ARRAY_TASK_ID}.txt"
printf '{"task":%s,"job":"%s","p":%d,"islands":%d,"host":"%s","cpu":"%s","start":"%s"}\n' "$SLURM_ARRAY_TASK_ID" "${SLURM_ARRAY_JOB_ID}" "$P" "$R" \
  "$(hostname -s)" "$(grep -m1 'model name' /proc/cpuinfo | sed 's/.*: //')" "$(date -u +%FT%TZ)" >> "$RUN/log/starts.jsonl"
t0=$(date +%s); rc=0
cd "$SCR"
"${WRAP[@]}" Rscript --vanilla stage_measure.R --core-dir "$CODE" --p "$P" --seed 20261111 --n-cal 2500 --n-isl 2500 --islands "$R" \
  --hours "$HOURS" --b3-rds "$B3/b3_p$P/res/census_p$P.rds" --manifest "$SCR/revD_SHA256SUMS" \
  --out "$RUN/res/stage_p$P.rds" > "$RUN/log/task_${SLURM_ARRAY_TASK_ID}_p$P.log" 2>&1 || rc=$?
printf '{"task":%s,"job":"%s","rc":%d,"wall_s":%d,"end":"%s"}\n' "$SLURM_ARRAY_TASK_ID" "${SLURM_ARRAY_JOB_ID}" "$rc" "$(( $(date +%s) - t0 ))" "$(date -u +%FT%TZ)" >> "$RUN/log/ends.jsonl"
exit $rc
