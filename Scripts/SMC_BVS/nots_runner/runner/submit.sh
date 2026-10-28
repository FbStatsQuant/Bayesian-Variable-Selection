#!/usr/bin/env bash
# Freeze one run and submit its array (NOTS login node). Never overwrites an existing run.
# Usage: [CONSTRAINT=sapphirerapids] submit.sh RUN_ID TABLE_DIR prod|dev L500_S L1000_S THROTTLE [dependency]
# Production (prod_*): needs $CL/GO_2400.md, L500=6300, L1000=24000, CONSTRAINT=sapphirerapids, combined
# throttle <= 100 over all queued prod arrays. A failed sbatch retires RUN_DIR; use a new RUN_ID.
#   TABLE_DIR holds chunks.tsv and units.tsv from make_tables.py.
set -euo pipefail
[[ $# == 6 || $# == 7 ]] || { echo "usage: submit.sh RUN_ID TABLE_DIR prod|dev L500_S L1000_S THROTTLE [dependency]" >&2; exit 64; }
RUN_ID=$1; TABLES=$(realpath "$2"); MODE=$3; L500=$4; L1000=$5; THROTTLE=$6; DEP=${7:-}
[[ $RUN_ID =~ ^[A-Za-z0-9][A-Za-z0-9_.-]*$ && $L500 =~ ^[0-9]+$ && $L1000 =~ ^[0-9]+$ && $THROTTLE =~ ^[0-9]+$ ]] || exit 64
(( THROTTLE >= 1 && THROTTLE <= 100 )) || { echo "throttle must be 1..100 (brief)" >&2; exit 64; }
CL=/home/fb31/projects/BVS/SMC_BVS_v3/deploy/claude
CODE=$CL/code/v2_1
RUN_DIR=$CL/runs/$RUN_ID
OUTROOT=/scratch/fb31/smcbvs_v3_deploy_20261022/claude/$RUN_ID
KILL_MARGIN=300
case $MODE in
  prod) STUDY=/projects/ml75/fb31/BVS/bench20261019; DEV=0 ;;
  dev)  STUDY=/scratch/fb31/smcbvs_v3_deploy_20261022/n0_20261023/smoke_inputs; DEV=1 ;;
  *) exit 64 ;;
esac
[[ ! -e $RUN_DIR && ! -e $OUTROOT ]] || { echo "run $RUN_ID exists; use a new run ID" >&2; exit 66; }
# HQ gate (review F7): a production run other than the single readiness e2e fit needs GO_2400.md,
# which the lead copies to $CL/GO_2400.md only after HQ writes it.
if [[ $MODE == prod && $RUN_ID != e2e_* ]]; then
  [[ -s $CL/GO_2400.md ]] || { echo "no $CL/GO_2400.md: production is gated by HQ" >&2; exit 66; }
  # GO_2400 enforced, not just available (review R6): C1 limits, C2 node pin, combined throttle <= 100.
  [[ $RUN_ID == prod_* ]] || { echo "production run IDs start with prod_" >&2; exit 64; }
  [[ $L500 == 6300 && $L1000 == 24000 ]] || { echo "GO_2400 C1: L500=6300, L1000=24000" >&2; exit 64; }
  [[ ${CONSTRAINT:-} == sapphirerapids ]] || { echo "GO_2400 C2: CONSTRAINT=sapphirerapids required" >&2; exit 64; }
  active=0
  # Capture squeue first (review N5: `squeue | grep -q` under pipefail can fail by SIGPIPE).
  queued=$(squeue -h -u fb31 -o "%i") || { echo "squeue failed" >&2; exit 67; }
  queued=$(sed 's/_.*//' <<< "$queued" | sort -u)
  for m in "$CL"/runs/prod_*/manifest.json; do
    [[ -f $m ]] || continue
    j=$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["slurm_job_id"].split(";")[0])' "$m")
    t=$(python3 -c 'import json,re,sys; print(re.search(r"--array=\S*%(\d+)", json.load(open(sys.argv[1]))["sbatch_args"]).group(1))' "$m")
    if grep -qx "$j" <<< "$queued"; then active=$((active + t)); fi
  done
  (( active + THROTTLE <= 100 )) || { echo "combined throttle $active + $THROTTLE > 100 (brief)" >&2; exit 64; }
fi
# The readiness e2e exception is for a single task only (review R12).
if [[ $MODE == prod && $RUN_ID == e2e_* ]]; then
  [[ $(( $(wc -l < "$TABLES/chunks.tsv") - 1 )) == 1 ]] || { echo "e2e runs have exactly one task" >&2; exit 64; }
fi
compgen -G "$CODE/code/core/.cpp_cache/*/READY" > /dev/null || { echo "no prebuilt cpp cache" >&2; exit 66; }
(cd "$CODE" && sha256sum --strict -c --quiet SHA256SUMS) || { echo "frozen code changed" >&2; exit 66; }
n_tasks=$(( $(wc -l < "$TABLES/chunks.tsv") - 1 ))
max_units=$(awk -F'\t' 'NR > 1 { n = split($4, a, ","); if (n > m) m = n } END { print m }' "$TABLES/chunks.tsv")
# Longest limit among the p values actually present in this table (GO_2400 C1: one array per p,
# so p500 tasks request a short wall).
max_L=$(awk -F'\t' -v a="$L500" -v b="$L1000" 'NR > 1 { L = ($3 == 500) ? a : b; if (L > m) m = L } END { print m }' "$TABLES/chunks.tsv")
[[ $max_L =~ ^[0-9]+$ && $max_L -gt 0 ]] || { echo "bad chunk table" >&2; exit 66; }
# Task wall: every unit at its hard kill (L + margin + 60 s KILL grace) + 10 min for loading and accounting.
task_s=$(( max_units * (max_L + KILL_MARGIN + 60) + 600 ))
task_time=$(printf '%d:%02d:00' $(( (task_s + 59) / 3600 )) $(( ((task_s + 59) % 3600) / 60 )))
mkdir -p "$RUN_DIR" "$OUTROOT/slurm"
cp "$TABLES/chunks.tsv" "$TABLES/units.tsv" "$RUN_DIR/"
# Freeze the runner with the run (review F5): tasks source RUN_DIR/runner, never the live copy.
cp -a "$CL/runner" "$RUN_DIR/runner"; chmod -R a-w "$RUN_DIR/runner"
cat > "$RUN_DIR/config.env" <<EOF
RUN_ID=$RUN_ID
CODE=$CODE
STUDY=$STUDY
OUTROOT=$OUTROOT
DEV=$DEV
MEM_GB=2
L500=$L500
L1000=$L1000
KILL_MARGIN=$KILL_MARGIN
RUNNER=$RUN_DIR/runner
EOF
chmod a-w "$RUN_DIR/config.env" "$RUN_DIR/chunks.tsv" "$RUN_DIR/units.tsv"
args=(--parsable --job-name="smcbvs_$RUN_ID" --account=commons --partition=commons --qos=nots_commons
      --nodes=1 --ntasks=1 --cpus-per-task=1 --mem=2G --time="$task_time" --export=NONE --no-requeue
      --array="1-$n_tasks%$THROTTLE" --output="$OUTROOT/slurm/%A_%a.out" --error="$OUTROOT/slurm/%A_%a.err")
[[ -n $DEP ]] && args+=(--dependency="$DEP")
# Optional node-type pin (commons mixes cascadelake and sapphirerapids nodes); recorded in the manifest.
if [[ -n ${CONSTRAINT:-} ]]; then
  [[ $CONSTRAINT =~ ^(cascadelake|sapphirerapids)$ ]] || { echo "bad CONSTRAINT" >&2; exit 64; }
  args+=(--constraint="$CONSTRAINT")
fi
if ! job=$(sbatch "${args[@]}" "$RUN_DIR/runner/task.sh" "$RUN_DIR"); then
  # Nothing was queued: retire the half-made run so the ID is not silently reused (review F2).
  chmod -R u+w "$RUN_DIR"; mv "$RUN_DIR" "$RUN_DIR.sbatch_failed_$(date -u +%Y%m%dT%H%M%SZ)"
  echo "sbatch failed; run directory retired" >&2; exit 67
fi
trap 'echo "manifest step failed: cancelling $job" >&2; scancel "${job%%;*}"' ERR
python3 - "$RUN_DIR" "$job" "$task_time" "${args[*]}" <<'PY'
import hashlib, json, os, socket, subprocess, sys
from datetime import datetime, timezone
run_dir, job, task_time, args = sys.argv[1:5]
cfg = dict(l.split("=", 1) for l in open(os.path.join(run_dir, "config.env")).read().split())
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
runner = cfg["RUNNER"]
m = dict(run_id=cfg["RUN_ID"], submitted_utc=datetime.now(timezone.utc).isoformat(), host=socket.gethostname(),
         slurm_job_id=job, task_time=task_time, sbatch_args=args, config=cfg,
         code_SHA256SUMS_sha256=sha(os.path.join(cfg["CODE"], "SHA256SUMS")),
         code_manifest_sha256=sha(os.path.join(cfg["CODE"], "manifest.json")),
         runner_sha256={f: sha(os.path.join(runner, f)) for f in sorted(os.listdir(runner)) if os.path.isfile(os.path.join(runner, f))},
         chunks_sha256=sha(os.path.join(run_dir, "chunks.tsv")), units_sha256=sha(os.path.join(run_dir, "units.tsv")),
         seeds="method seed = data seed + 4,000,000; derived per dataset ID by the adapter (see units.tsv)",
         modules="GCC/14.3.0 R/4.5.2", outputs=cfg["OUTROOT"])
if cfg["DEV"] == "0":
    m["inputs_manifest_sha256"] = sha(os.path.join(cfg["STUDY"], "manifests", "inputs_manifest.csv"))
else:
    m["inputs_manifest_sha256"] = sha(os.path.join(cfg["STUDY"], "manifests", "dev_inputs_manifest.csv"))
json.dump(m, open(os.path.join(run_dir, "manifest.json"), "w"), indent=2)
print(json.dumps(dict(run_id=m["run_id"], job=job, task_time=task_time, code=m["code_SHA256SUMS_sha256"][:12])))
PY
chmod a-w "$RUN_DIR/manifest.json"
# Every array job of this run (the original and any reruns), for reconcile.py and poll.sh (GO_2400 C4).
printf 'job\tkind\tsubmitted_utc\tunits\n%s\tinitial\t%s\tall\n' "${job%%;*}" "$(date -u +%FT%TZ)" > "$RUN_DIR/jobs.tsv"
