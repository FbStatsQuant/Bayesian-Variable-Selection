#!/bin/bash
# Freeze the A2 code and submit the production array (policy §8; master §IV.3.1, §IV.2.4; production brief §2).
#
#   New run:   bash slurm/submit_prod.sh --kind KIND [--dry-run] [--array SPEC] [--time HH:MM:SS] [--mem 4G]
#     c = 0.5 copy, run_id <UTC>_bench20261019_<KIND>_A2_SSL (A2 + SSL-RS, 3 datasets per task):
#     prodc050   SCALE=c050, map prod, array 1-400%133 (tasks 1-200 p = 500, 201-400 p = 1000)
#     c050check  SCALE=c100, map prod, array 301 (p1000_S4_r001-r003): reproduction of c = 1 outputs
#     pilotc050  SCALE=c050, map pilot, array 1-4 (replicate 1 of S1-S6 x p 500/1000)
#   Resume:    bash slurm/submit_prod.sh --resume <run_id> [--array SPEC] [--time HH:MM:SS] [--mem 4G] [--dry-run]
#              re-verifies the existing snapshot and submits from it under the same run id (the runner
#              skips every (case, method) with valid outputs of this run, code and input). Use it to promote
#              a dry run, to start the second wave, or for the one infrastructure retry of §IV.2.4 (with
#              doubled --time / --mem after TIMEOUT / OUT_OF_MEMORY). Refused while any earlier launch of
#              the run is pending or running, or when the scheduler cannot be queried.
#   --dry-run  everything except sbatch.
#
# Safety: runs/<run_id> is claimed atomically (mkdir); every submission holds an exclusive lock on
# runs/<run_id>/submit.lock; a launch intent (with a unique token used as the job-name suffix) is
# written to manifest.json before sbatch and completed with the job id after it, so an interrupted
# submission can be found again by its job name; manifest.json is always replaced atomically.
# The job environment (CODE, RUN_ID, DATASETS, A2_SMOKE) is set in the sbatch process itself, so
# nothing inherited from the caller's shell can override it.
set -euo pipefail
DRY=0; KIND=""; RESUME=""; ARRAY=""; TIME=""; MEM=""; MODE=new
while [ $# -gt 0 ]; do
  case "$1" in
    --dry-run) DRY=1 ;;
    --kind) KIND=$2; shift ;;
    --resume) RESUME=$2; MODE=resume; shift ;;
    --array) ARRAY=$2; shift ;;
    --time) TIME=$2; shift ;;
    --mem) MEM=$2; shift ;;
    *) echo "unknown argument $1"; exit 1 ;;
  esac
  shift
done
SRC=/home/fb31/projects/BVS/Benchmarks/A2_SSL/c050
B=/projects/ml75/fb31/BVS/bench20261019
LIB=$B/lib/R452

# Atomic update of manifest.json: python edits a copy, which is renamed over the original.
manifest_update() {  # $1 = python statements acting on dict m; remaining args available as a[0], a[1], ...
  local code=$1; shift
  python3 - "$RUN/manifest.json" "$code" "$@" <<'PY'
import json, os, sys, datetime
p, code, *a = sys.argv[1:]
now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
m = json.load(open(p))
exec(code)
tmp = p + '.tmp'
json.dump(m, open(tmp, 'w'), indent=2)
os.replace(tmp, p)
PY
}

if [ -z "$RESUME" ]; then
  case "$KIND" in prodc050|c050check|pilotc050) ;; *) echo "--kind must be prodc050, c050check or pilotc050"; exit 1 ;; esac
  RUN_ID=$(date -u +%Y%m%dT%H%MZ)_bench20261019_${KIND}_A2_SSL
  RUN=$B/runs/$RUN_ID
  mkdir "$RUN" || { echo "refusing: $RUN exists (another submission claimed it)"; exit 1; }
else
  [ -z "$KIND" ] || { echo "--kind is not allowed with --resume (the run id fixes it)"; exit 1; }
  RUN_ID=$RESUME; RUN=$B/runs/$RUN_ID
  [ -f "$RUN/manifest.json" ] || { echo "refusing: no manifest for $RUN_ID"; exit 1; }
  case "$RUN_ID" in *_prodc050_*) KIND=prodc050 ;; *_c050check_*) KIND=c050check ;; *_pilotc050_*) KIND=pilotc050 ;;
    *) echo "refusing: $RUN_ID is not a c050-copy run"; exit 1 ;; esac
fi
case "$KIND" in prodc050) SCALE=c050 ;; c050check) SCALE=c100 ;; pilotc050) SCALE=c050 ;; esac
exec 9>"$RUN/submit.lock"
flock -n 9 || { echo "refusing: another submission for $RUN_ID holds the lock"; exit 1; }

if [ -z "$RESUME" ]; then
  mkdir -p "$RUN/code" "$RUN/input_manifests" "$B/logs/prod/A2_SSL"
  cp -r "$SRC"/config.R "$SRC"/common.R "$SRC"/run_case.R "$SRC"/run_chunk.R "$SRC"/score_dev.R "$SRC"/check_dev.R \
        "$SRC"/methods "$SRC"/tests "$SRC"/slurm "$SRC"/tools "$RUN/code"/
  cp "$B"/manifests/cells/*_inputs.csv "$RUN/input_manifests"/
  chmod -R a-w "$RUN/code" "$RUN/input_manifests"
  (cd "$RUN/code" && find . -type f | sort | xargs sha256sum) > "$RUN/code_sha256.txt"
  (cd "$RUN/input_manifests" && find . -type f | sort | xargs sha256sum) > "$RUN/input_manifests_sha256.txt"
  # Library / environment: every installed file of the two packages the fits load, plus the G1 manifest.
  { sha256sum "$B/lib/environment_manifest.txt"; find "$LIB/SSLASSO" "$LIB/digest" -type f | sort | xargs sha256sum; } > "$RUN/env_sha256.txt"
  # The source folder must still match what was copied.
  (cd "$SRC" && sha256sum --quiet -c "$RUN/code_sha256.txt") || { echo "refusing: source changed during the freeze"; exit 1; }
  TREE=$(cd "$RUN/code" && for f in config.R common.R methods/fit_A2_ssl.R run_case.R; do printf "%s  %s\n" "$(sha256sum "$f" | cut -d" " -f1)" "$f"; done | head -c -1 | sha256sum | cut -d" " -f1)
  python3 - "$RUN" "$RUN_ID" "$TREE" "$B" "$KIND" "$SCALE" <<'PY'
import json, os, sys, socket, datetime
run, run_id, tree, B, kind, scale = sys.argv[1:]
ndat = {"prodc050": 1200, "c050check": 3, "pilotc050": 12}[kind]
def table(f): return {l.split()[1]: l.split()[0] for l in open(os.path.join(run, f)) if l.strip()}
m = {"run_id": run_id,
     "piece": "A2 + SSL-RS, c050 copy, kind %s (%d cases, %s)" % (kind, ndat, scale),
     "created_utc": datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
     "code_snapshot": os.path.join(run, 'code'), "code_sha256": table('code_sha256.txt'),
     "source_tree_sha256": tree,
     "input_manifests": os.path.join(run, 'input_manifests'), "input_manifests_sha256": table('input_manifests_sha256.txt'),
     "environment_sha256_file": os.path.join(run, 'env_sha256.txt'),
     "inputs_dir": os.path.join(B, 'inputs'),
     "method_ids": ["A2", "SSL-RS"], "scale_key": scale, "kind": kind,
     "task_map": ("pilot map: tasks 1-4 = p0500 S1-S3, p0500 S4-S6, p1000 S1-S3, p1000 S4-S6, replicate 1" if kind == "pilotc050" else
                  "prod map: tasks 1-200 p = 500, 201-400 p = 1000; task t covers positions 3k..3k+2, k = (t-1) mod 200, of the scenario-major order (scenario i div 100 + 1, replicate i mod 100 + 1)"),
     "seeds": "method_seed = data_seed + 4,000,000 (read from each input file); SSL uses no random numbers",
     "modules": "GCC/14.3.0 R/4.5.2", "r_library": os.path.join(B, 'lib', 'R452'),
     "outputs": {"results": os.path.join(B, 'results', run_id), "logs": os.path.join(B, 'logs', 'prod', 'A2_SSL')},
     "validation_command": "Rscript --vanilla <run>/code/check_dev.R --code <run>/code --results <results>/<run_id> --manifest <run>/input_manifests --out <run>/check --scale " + scale + " --source_sha256 " + tree + (" --expected_datasets 1200" if kind == "prodc050" else " --datasets <the run's dataset ids>"),
     "submit_host": socket.gethostname(), "launches": [], "status": "frozen, not submitted"}
tmp = os.path.join(run, 'manifest.json.tmp')
json.dump(m, open(tmp, 'w'), indent=2)
os.replace(tmp, os.path.join(run, 'manifest.json'))
PY
  echo "RUN_ID=$RUN_ID (new snapshot)"
else
  echo "RUN_ID=$RUN_ID (resume)"
  # Earlier launches must be finished. Pending intents (no job id) are first resolved by job name.
  if ! python3 - "$RUN/manifest.json" > "$RUN/launch_check.txt" <<'PY'
import json, subprocess, sys
m = json.load(open(sys.argv[1]))
for l in m["launches"]:
    if l.get("dry_run"):
        continue
    ids = l.get("job_id")
    if not ids:
        r = subprocess.run(["sacct", "-X", "-n", "-P", "-S", l["utc"][:10], "--name", l["job_name"], "-o", "JobID"],
                           capture_output=True, text=True)
        if r.returncode != 0:
            print("ERROR sacct failed for intent", l["token"]); sys.exit(1)
        found = sorted({x.split("_")[0] for x in r.stdout.split()})
        if len(found) > 1:
            print("ERROR several jobs for intent", l["token"], found); sys.exit(1)
        ids = found[0] if found else None
        print("INTENT", l["token"], ids or "none")
    if ids:
        r = subprocess.run(["sacct", "-X", "-n", "-P", "-j", ids, "-o", "State"], capture_output=True, text=True)
        if r.returncode != 0:
            print("ERROR sacct failed for job", ids); sys.exit(1)
        active = [s for s in r.stdout.split() if s.split()[0] in ("PENDING", "RUNNING", "REQUEUED", "RESIZING", "SUSPENDED", "CONFIGURING", "COMPLETING")]
        if active:
            print("ERROR job", ids, "still active:", ",".join(sorted(set(active)))); sys.exit(1)
        print("JOB", ids, "finished")
print("OK")
PY
  then cat "$RUN/launch_check.txt"; echo "refusing: earlier launches active or scheduler query failed"; exit 1; fi
  cat "$RUN/launch_check.txt"
  # Record job ids found for interrupted intents.
  while read -r tag token jid; do
    [ "$tag" = INTENT ] && [ "$jid" != none ] && manifest_update '
for l in m["launches"]:
    if l.get("token") == a[0] and not l.get("job_id"): l["job_id"] = a[1]; l["recovered_utc"] = now' "$token" "$jid"
  done < "$RUN/launch_check.txt"
fi

# Verify the frozen record (code, input manifests, library / environment).
(cd "$RUN/code" && sha256sum --quiet -c "$RUN/code_sha256.txt") || { echo "refusing: snapshot hash mismatch"; exit 1; }
(cd "$RUN/input_manifests" && sha256sum --quiet -c "$RUN/input_manifests_sha256.txt") || { echo "refusing: input manifest hash mismatch"; exit 1; }
sha256sum --quiet -c "$RUN/env_sha256.txt" || { echo "refusing: library / environment hash mismatch"; exit 1; }
echo "snapshot verified: $RUN"

TOKEN=$(date -u +%H%M%S)$$
JOBNAME=A2_${KIND}_$TOKEN
DS=""; SMK=0
case "$KIND" in prodc050) ARRAY=${ARRAY:-1-400%133} ;; c050check) ARRAY=${ARRAY:-301} ;; pilotc050) ARRAY=${ARRAY:-1-4} ;; esac
OPTS="--parsable --job-name=$JOBNAME --array=$ARRAY --export=ALL"
[ -n "$TIME" ] && OPTS="$OPTS --time=$TIME"
[ -n "$MEM" ] && OPTS="$OPTS --mem=$MEM"
CMD="env -u DATASETS -u A2_SMOKE -u SCALE CODE=$RUN/code RUN_ID=$RUN_ID SCALE=$SCALE DATASETS=$DS A2_SMOKE=$SMK sbatch $OPTS $RUN/code/slurm/prod_array.slurm"
manifest_update '
m["launches"].append({"utc": now, "token": a[0], "job_name": a[1], "mode": a[2], "command": a[3],
                      "dry_run": a[4] == "1", "job_id": None})' "$TOKEN" "$JOBNAME" "$MODE" "$CMD" "$DRY"
if [ "$DRY" -eq 1 ]; then
  echo "dry run: would run: $CMD"
  manifest_update 'm["status"] = m["status"] if any(l.get("job_id") for l in m["launches"]) else "dry run (not submitted)"'
  exit 0
fi
JOB=$($CMD)
manifest_update '
for l in m["launches"]:
    if l["token"] == a[0]: l["job_id"] = a[1]
m["status"] = "submitted"' "$TOKEN" "$JOB"
echo "JOB=$JOB"
