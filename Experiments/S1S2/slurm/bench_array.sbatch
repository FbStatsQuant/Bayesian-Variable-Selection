#!/bin/bash
# bench_array.sbatch -- S1 / S2 BENCHMARK grids on NOTS (lasso_cv, scad, susie, bas_mc3, asi on both suites; S1 asi
# signed by the owner 2026-11-27).
# OURS (operational). ONE array task = one (suite, method, setting, block of reps): ONE R process loads the adapter once and fits the block
# (harness/run_one.R --reps), writing the usual per-rep rds/json under $RUNS/<method>/<setting>/rep_RRR.*.
# Submitted ONLY through submit_bench.sh, which sets per class (on the command line, overriding the defaults below):
#   --array=<task ids>%K --mem --time --partition --constraint=cascadelake --job-name=s<suite>bm_<method>_b<K>_<class>
#   --export=ALL,S1S2_SUITE=<suite>,S1S2_METHOD=<method>
# Task ids index slurm/tasks_S<suite>_bench_<method>.tsv (task_id = (cell-1)*100 + rep_lo; make_bench_tasks.sh). The
# method must be in harness/methods.R and have a (suite, method) row in slurm/bench_budget.tsv (fit_limit_sec, ctrl;
# for p = 5000 settings fit_limit_p5000 / ctrl_p5000 when not "-");
# smcbvs is refused (it keeps s1_smcbvs_array.sbatch).
# Environment: envs/S1S2/env_bench.sh (R 4.5.2 + benchmark packages + Octave/ASI paths; installed by deploy_to_nots.sh
# from slurm/nots_env_bench.sh). TMPDIR = a per-task folder on scratch, created BEFORE sourcing env_bench.sh (it points
# S1S2_ASI_TMP at TMPDIR) and removed at task exit.
# Idempotent: reps whose json already has top-level status ok are skipped (by run_one.R); a resubmitted task fits only
# the rest. Per-rep wall limit (fit_limit_sec): a watchdog reads run_one.R's --progress file; when the current rep has
# run longer than the limit it kills the R process group (TERM, KILL after 60 s; Octave children included), writes
#   {"setting_id":..,"method":..,"rep":..,"status":"failed: harness wall timeout <limit>s","host":..,"slurm_job":..}
# for that rep (computational failure, diagnostics.R) and restarts R for the reps after it. If R dies during a rep for
# any other reason, that rep gets "failed: harness: R process exited rc=<rc> during the fit" and the loop continues.
# Exit status: 0 when every rep of the block has a json, else 1 (the task then shows FAILED in sacct).
#SBATCH --job-name=bench
#SBATCH --partition=commons
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=2G
#SBATCH --time=01:00:00
#SBATCH --chdir=/scratch/fb31/SMC-BVS/runs/S1S2/logs
#SBATCH --output=/scratch/fb31/SMC-BVS/runs/S1S2/logs/%x_%A_%a.out
#SBATCH --error=/scratch/fb31/SMC-BVS/runs/S1S2/logs/%x_%A_%a.err
set -euo pipefail
ENG=/home/fb31/SMC-BVS/_local/engineering
DEPLOY=${S1S2_DEPLOY:-$ENG/S1S2/deploy}
RUNS=${S1S2_RUNS:-/scratch/fb31/SMC-BVS/runs/S1S2}
TMPBASE=${S1S2_TMPBASE:-/scratch/fb31/SMC-BVS/tmp/S1S2}
ENVF=${S1S2_ENV_BENCH:-$ENG/envs/S1S2/env_bench.sh}
POLL=${S1S2_WATCHDOG_POLL:-2}
M=${S1S2_METHOD:?S1S2_METHOD not set}; SU=${S1S2_SUITE:?S1S2_SUITE not set}
[[ "$SU" == 1 || "$SU" == 2 ]] || { echo "FATAL: S1S2_SUITE must be 1 or 2" >&2; exit 2; }
SL=$DEPLOY/S1S2/slurm; CONF=$SL/bench_budget.tsv; TASKS=$SL/tasks_S${SU}_bench_$M.tsv
# method: registry name (harness/methods.R), not smcbvs, present in the config
awk -v m="$M" '$1 == m && $2 == "=" && $3 ~ /^list\(file/ { f = 1 } END { exit !f }' "$DEPLOY/S1S2/harness/methods.R" ||
  { echo "FATAL: method '$M' not in harness/methods.R" >&2; exit 2; }
[[ "$M" != smcbvs && "$M" =~ ^[a-z0-9_]+$ ]] || { echo "FATAL: method '$M' is not a benchmark method" >&2; exit 2; }
IFS=$'\t' read -r _ _ _ _ LIMIT _ _ _ CTRL LIMIT5K CTRL5K < <(awk -F'\t' -v s="$SU" -v m="$M" 'NR > 1 && $1 == s && $2 == m' "$CONF") || true
[[ "${LIMIT:-}" =~ ^[0-9]+$ ]] || { echo "FATAL: no (suite $SU, $M) row with fit_limit_sec in $CONF" >&2; exit 2; }
[[ -f "$TASKS" ]] || { echo "FATAL: no task list $TASKS" >&2; exit 2; }

tid=${SLURM_ARRAY_TASK_ID:?not an array task}
jobtag=${SLURM_ARRAY_JOB_ID:-0}_${tid}
read -r setting rlo rhi < <(awk -F'\t' -v t="$tid" 'NR > 1 && $1 == t { print $2, $3, $4 }' "$TASKS") || true
[[ -n "${setting:-}" && "${rlo:-}" =~ ^[0-9]+$ && "${rhi:-}" =~ ^[0-9]+$ ]] || { echo "FATAL: task $tid not in $TASKS" >&2; exit 2; }
# p = 5000 settings (S1): fit_limit_p5000 / ctrl_p5000 replace fit_limit_sec / ctrl when not "-"
P=$(awk -F'\t' -v s="$setting" 'NR == 1 { for (i = 1; i <= NF; i++) if ($i == "p") c = i; next } $1 == s { print $c }' "$DEPLOY/S1S2/specs/settings.tsv")
[[ "$P" =~ ^[0-9]+$ ]] || { echo "FATAL: no p for $setting in specs/settings.tsv" >&2; exit 2; }
if (( P == 5000 )); then
  [[ -n "${LIMIT5K:-}" && "$LIMIT5K" != - ]] && LIMIT=$LIMIT5K
  [[ -n "${CTRL5K:-}" && "$CTRL5K" != - ]] && CTRL=$CTRL5K
fi
[[ "$LIMIT" =~ ^[0-9]+$ ]] || { echo "FATAL: bad fit limit '$LIMIT' for $setting" >&2; exit 2; }

export TMPDIR=$TMPBASE/$jobtag
mkdir -p "$TMPDIR"; trap 'rm -rf "$TMPDIR"' EXIT
source "$ENVF"
# adapter ctrl: config column (JSON object or "-") + optional $S1S2_CTRL_<method> from env_bench.sh (flat JSON objects)
v="S1S2_CTRL_$M"; ectrl=${!v:-}
[[ "$CTRL" == "-" || -z "$CTRL" ]] && CTRL='{}'
[[ "$CTRL" =~ ^\{.*\}$ && ( -z "$ectrl" || "$ectrl" =~ ^\{.*\}$ ) ]] || { echo "FATAL: ctrl is not a JSON object" >&2; exit 2; }
if [[ -n "$ectrl" && "$ectrl" != '{}' ]]; then
  if [[ "$CTRL" == '{}' ]]; then CTRL=$ectrl; else CTRL="${CTRL%\}},${ectrl#\{}"; fi
fi

dir=$RUNS/$M/$setting; mkdir -p "$dir"
jpath() { printf '%s/rep_%03d.json' "$dir" "$1"; }
is_ok() { [[ -f "$1" ]] && grep -Eq '^ {2}"status": "ok",?$' "$1"; }   # top-level status (run_one.R: 2-space indent)
echo "task=$tid suite=$SU method=$M setting=$setting reps=$rlo-$rhi limit=${LIMIT}s job=$jobtag node=$(hostname) cpu=\"$(lscpu | sed -n 's/^Model name: *//p')\" start=$(date -u +%FT%TZ)"
echo "deploy=$DEPLOY manifest_sha256=$(sha256sum "$DEPLOY/MANIFEST.sha256" | cut -c1-16) R=$(Rscript --version 2>&1 | head -1) ctrl=$CTRL"

fail_json() {   # rep, status: written only if the rep has no ok json (atomic tmp + rename)
  local j; j=$(jpath "$1"); is_ok "$j" && return 0
  printf '{"setting_id":"%s","method":"%s","rep":%d,"status":"%s","host":"%s","slurm_job":"%s"}\n' \
    "$setting" "$M" "$1" "$2" "$(hostname)" "$jobtag" > "$j.tmp" && mv "$j.tmp" "$j"
  echo "REP $1: $2"
}

todo=(); for (( r = rlo; r <= rhi; r++ )); do is_ok "$(jpath "$r")" || todo+=("$r"); done
echo "todo=${#todo[@]} of $(( rhi - rlo + 1 )) reps: ${todo[*]:-none}"
prog=$TMPDIR/progress; rc_all=0
while (( ${#todo[@]} )); do
  list=$(IFS=,; echo "${todo[*]}"); : > "$prog"
  # own process group (setsid without fork: a background child of a non-interactive shell is no group leader), so the
  # watchdog's kill reaches R and every process it started (Octave)
  setsid Rscript "$DEPLOY/S1S2/harness/run_one.R" --method "$M" --setting "$setting" --reps "$list" --out "$RUNS" \
    --ctrl "$CTRL" --progress "$prog" &
  pid=$!; killed=""
  while kill -0 "$pid" 2>/dev/null; do
    sleep "$POLL"
    read -r ev cur t0 < <(tail -n 1 "$prog" 2>/dev/null) || true
    if [[ "${ev:-}" == start && "${t0:-}" =~ ^[0-9]+$ ]] && (( $(date +%s) - t0 > LIMIT )); then
      killed=$cur; echo "WATCHDOG: rep $cur over ${LIMIT}s; killing process group $pid"
      kill -TERM -- -"$pid" 2>/dev/null || true
      for _ in $(seq 60); do kill -0 "$pid" 2>/dev/null || break; sleep 1; done
      kill -KILL -- -"$pid" 2>/dev/null || true
      break
    fi
  done
  rc=0; wait "$pid" || rc=$?
  # the rep in progress when R ended (a "start" line without its "end" line), if any
  read -r ev cur _ < <(tail -n 1 "$prog" 2>/dev/null) || true
  inprog=""; [[ "${ev:-}" == start ]] && inprog=$cur
  if [[ -n "$killed" ]]; then fail_json "$killed" "failed: harness wall timeout ${LIMIT}s"; inprog=$killed
  elif [[ -n "$inprog" ]]; then fail_json "$inprog" "failed: harness: R process exited rc=$rc during the fit"; fi
  (( rc == 0 )) || rc_all=$rc
  # next round: the reps after the one in progress (not attempted yet; run_one.R skips any that are ok). None in
  # progress -> R ended on its own (all done, or it died before/between reps: stop; missing reps stay visible)
  [[ -n "$inprog" ]] || break
  rest=(); after=0
  for r in "${todo[@]}"; do
    if (( after )); then rest+=("$r"); fi
    if [[ "$r" == "$inprog" ]]; then after=1; fi
  done
  todo=("${rest[@]}")
  if (( ${#todo[@]} )); then echo "RESTART: R again for reps ${todo[*]}"; fi
done
miss=0; for (( r = rlo; r <= rhi; r++ )); do [[ -f "$(jpath "$r")" ]] || miss=$(( miss + 1 )); done
nok=0; for (( r = rlo; r <= rhi; r++ )); do is_ok "$(jpath "$r")" && nok=$(( nok + 1 )); done
echo "end=$(date -u +%FT%TZ) reps=$(( rhi - rlo + 1 )) ok=$nok missing=$miss last_rc=$rc_all"
(( miss == 0 )) || exit 1
exit 0
