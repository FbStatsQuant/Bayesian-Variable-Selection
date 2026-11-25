#!/bin/bash
# s1_smcbvs_array.sbatch -- S1 SMC-BVS grid on NOTS: ONE fit (setting x rep) per array task. OURS (operational).
# Submitted ONLY through submit_batches.sh, which sets per class (on the command line, overriding the defaults below):
#   --array=<task ids>%K  --mem  --time  --partition  --job-name=s1smc_b<k>_<class>  --export=ALL,S1S2_WALL_SEC=<secs>
# Task ids index slurm/tasks_S1_smcbvs.tsv (task_id = (cell-1)*100 + rep).
# Idempotent: a task whose rep json already exists with "status": "ok" exits 0 without fitting. run_one.R writes the
# rds/json atomically (tmp + rename). If the fit hits the harness wall limit (S1S2_WALL_SEC - 300 s), a minimal
# "failed: harness wall timeout" json is written (only if no json exists), so the task is visible and re-runnable.
# Partition/QOS (sinfo/sacctmgr 2026-11-25): commons = QOS nots_commons, MaxWall 1-00:00:00, per user cpu=1536,
# mem=2304G, MaxSubmitPU 5000; long = nots_long, 3-00:00:00, per user cpu=384, mem=1T. DefMemPerCPU 1024 MB.
#SBATCH --job-name=s1smc
#SBATCH --partition=commons
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=2G
#SBATCH --time=02:00:00
#SBATCH --chdir=/scratch/fb31/SMC-BVS/runs/S1S2/logs
#SBATCH --output=/scratch/fb31/SMC-BVS/runs/S1S2/logs/%x_%A_%a.out
#SBATCH --error=/scratch/fb31/SMC-BVS/runs/S1S2/logs/%x_%A_%a.err
set -euo pipefail
ENG=/home/fb31/SMC-BVS/_local/engineering
DEPLOY=${S1S2_DEPLOY:-$ENG/S1S2/deploy}
RUNS=${S1S2_RUNS:-/scratch/fb31/SMC-BVS/runs/S1S2}
TASKS=$DEPLOY/S1S2/slurm/tasks_S1_smcbvs.tsv
WALL=${S1S2_WALL_SEC:-0}
source "$ENG/envs/S1S2/env.sh"

tid=${SLURM_ARRAY_TASK_ID:?not an array task}
read -r setting rep < <(awk -F'\t' -v t="$tid" 'NR > 1 && $1 == t { print $2, $3 }' "$TASKS") || true
[[ -n "${setting:-}" && -n "${rep:-}" ]] || { echo "FATAL: task $tid not in $TASKS" >&2; exit 2; }
json=$RUNS/smcbvs/$setting/$(printf 'rep_%03d.json' "$rep")
echo "task=$tid setting=$setting rep=$rep job=${SLURM_ARRAY_JOB_ID}_${tid} node=$(hostname) cpu=\"$(lscpu | sed -n 's/^Model name: *//p')\" start=$(date -u +%FT%TZ)"
echo "deploy=$DEPLOY manifest_sha256=$(sha256sum "$DEPLOY/MANIFEST.sha256" | cut -c1-16) R=$(Rscript --version 2>&1 | head -1)"
# top-level status only: run_one.R pretty-prints with a 2-space indent; nested diagnostics may carry their own "status"
if [[ -f "$json" ]] && grep -Eq '^ {2}"status": "ok",?$' "$json"; then echo "SKIP: $json already ok"; exit 0; fi

export TMPDIR=/scratch/fb31/SMC-BVS/tmp/S1S2/${SLURM_ARRAY_JOB_ID}_${tid}
mkdir -p "$TMPDIR"; trap 'rm -rf "$TMPDIR"' EXIT
export SMCBVS_CORE_DIR=$DEPLOY/smcbvs_core@7100bb3b

TIMEV=(); [[ -x /usr/bin/time ]] && TIMEV=(/usr/bin/time -v)     # absent on the login node; sacct has MaxRSS anyway
cmd=(Rscript "$DEPLOY/S1S2/harness/run_one.R" --method smcbvs --setting "$setting" --rep "$rep" --out "$RUNS")
rc=0
if (( WALL > 600 )); then
  timeout --signal=TERM --kill-after=60 $(( WALL - 300 )) "${TIMEV[@]}" "${cmd[@]}" || rc=$?
else
  "${TIMEV[@]}" "${cmd[@]}" || rc=$?
fi
if (( rc == 124 || rc == 137 )) && [[ ! -f "$json" ]]; then
  mkdir -p "$(dirname "$json")"
  printf '{"setting_id":"%s","method":"smcbvs","rep":%d,"status":"failed: harness wall timeout %ss","host":"%s","slurm_job":"%s"}\n' \
    "$setting" "$rep" "$(( WALL - 300 ))" "$(hostname)" "${SLURM_ARRAY_JOB_ID}_${tid}" > "$json.tmp" && mv "$json.tmp" "$json"
fi
echo "rc=$rc end=$(date -u +%FT%TZ) json_status=$(grep -Eo '^ {2}"status": "[^"]*"|^\{"setting_id".*"status":"[^"]*"' "$json" 2>/dev/null | head -1 | sed 's/.*"status": *//')"
exit "$rc"
