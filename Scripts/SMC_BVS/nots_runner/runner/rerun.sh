#!/usr/bin/env bash
# Rerun infrastructure failures ONLY, once, with the same seed, run ID and native allocation (GO_2400 C4;
# ASSUMPTIONS #5); also give `orphan` units (task died before reaching them) their FIRST attempt.
# NOTS login node.  Usage: rerun.sh RUN_DIR [--dry-run]
# 0. refuse while ANY job of this run (original or rerun) is still queued: no double queueing (review R2),
#    and the rerun never adds to a running array's throttle (combined %100, review R6)
# 1. reconcile.py --sacct --clear-stale-locks (a dry run clears nothing)
# 2. select classes `infra` and `orphan` (never done, pulled, timeout, infra_repeat, running, queued)
#    and drop any selected unit whose lock is still present (review R8)
# 3. one array over their task indices with a units file (task.sh runs only listed, eligible units),
#    --no-requeue, %10, the original constraint and task wall; --mem 4G only if a selected unit's step
#    ended OUT_OF_MEMORY (master §IV.2.4; native --mem-gb stays 2, so unit identity is unchanged)
# 4. append the job to RUN_DIR/jobs.tsv
set -euo pipefail
[[ $# == 1 || ( $# == 2 && $2 == --dry-run ) ]] || { echo "usage: rerun.sh RUN_DIR [--dry-run]" >&2; exit 64; }
RUN_DIR=$(realpath "$1"); DRY=${2:-}
source "$RUN_DIR/config.env"
# Capture squeue first (review N5): `squeue | grep -q` under pipefail can fail by SIGPIPE and pass a check.
sq_ids=$(squeue -h -r -u fb31 -o "%i") || { echo "squeue failed" >&2; exit 67; }
sq_names=$(squeue -h -u fb31 -o "%j") || { echo "squeue failed" >&2; exit 67; }
queued=$(sed 's/_.*//' <<< "$sq_ids" | sort -u)
for j in $(awk -F'\t' 'NR > 1 { print $1 }' "$RUN_DIR/jobs.tsv"); do
  if grep -qx "$j" <<< "$queued"; then echo "refusing: job $j of this run is still queued" >&2; exit 66; fi
done
# Combined throttle (brief: at most %100 across the campaign): no rerun while any production array is queued.
if grep -q '^smcbvs_prod_' <<< "$sq_names"; then
  [[ $RUN_ID == prod_* ]] && { echo "refusing: a production array is still queued (combined %100)" >&2; exit 66; }
fi
if [[ $DRY == --dry-run ]]; then
  python3 "$RUN_DIR/runner/reconcile.py" "$RUN_DIR" --sacct
else
  python3 "$RUN_DIR/runner/reconcile.py" "$RUN_DIR" --sacct --clear-stale-locks
fi
sel=$(awk -F'\t' 'NR == 1 { for (i = 1; i <= NF; i++) c[$i] = i; next }
                  ($c["klass"] == "infra" || $c["klass"] == "orphan") && $c["lock_present"] == "false" {
                    print $c["case_id"] "\t" $c["task"] "\t" $c["klass"] "\t" $c["step_state"] }' "$RUN_DIR/reconcile.tsv")
blocked=$(awk -F'\t' 'NR == 1 { for (i = 1; i <= NF; i++) c[$i] = i; next }
                      ($c["klass"] == "infra" || $c["klass"] == "orphan") && $c["lock_present"] == "true" { print $c["case_id"] }' "$RUN_DIR/reconcile.tsv")
[[ -z $blocked ]] || echo "WARNING: lock still present, not rerun (inspect by hand): $blocked" >&2
if [[ -z $sel ]]; then echo '{"rerun": 0, "reason": "no infra or orphan units"}'; exit 0; fi
tasks=$(cut -f2 <<< "$sel" | sort -n -u | paste -sd, -)
mem=2G; grep -q $'\tOUT_OF_MEMORY' <<< "$sel" && mem=4G
n=1; while [[ -e $RUN_DIR/rerun_$n ]]; do n=$((n + 1)); done
echo "rerun_$n: $(wc -l <<< "$sel") units ($(grep -c $'\torphan\t' <<< "$sel" || true) orphan), tasks $tasks, mem $mem"
[[ $DRY == --dry-run ]] && { echo "$sel"; exit 0; }
R=$RUN_DIR/rerun_$n
mkdir "$R"
cut -f1 <<< "$sel" > "$R/units.txt"
printf '%s\n' "$sel" > "$R/selected.tsv"
cp "$RUN_DIR/reconcile.tsv" "$R/reconcile_before.tsv"
task_time=$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["task_time"])' "$RUN_DIR/manifest.json")
constraint=$(python3 -c 'import json,re,sys; m=re.search(r"--constraint=(\S+)", json.load(open(sys.argv[1]))["sbatch_args"]); print(m.group(1) if m else "")' "$RUN_DIR/manifest.json")
args=(--parsable --job-name="smcbvs_${RUN_ID}_rerun$n" --account=commons --partition=commons --qos=nots_commons
      --nodes=1 --ntasks=1 --cpus-per-task=1 --mem="$mem" --time="$task_time" --export=NONE --no-requeue
      --array="$tasks%10" --output="$OUTROOT/slurm/%A_%a.out" --error="$OUTROOT/slurm/%A_%a.err")
[[ -n $constraint ]] && args+=(--constraint="$constraint")
job=$(sbatch "${args[@]}" "$RUN_DIR/runner/task.sh" "$RUN_DIR" "$R/units.txt")
printf '%s\trerun_%d\t%s\t%d\n' "${job%%;*}" "$n" "$(date -u +%FT%TZ)" "$(wc -l < "$R/units.txt")" >> "$RUN_DIR/jobs.tsv"
printf '{"rerun": %d, "job": "%s", "units": %d, "tasks": "%s", "mem": "%s", "args": "%s"}\n' \
  "$n" "${job%%;*}" "$(wc -l < "$R/units.txt")" "$tasks" "$mem" "${args[*]}" | tee "$R/submitted.json"
