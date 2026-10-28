#!/bin/bash
# Freeze the A2 code into a read-only snapshot under the output folder, write manifest.json
# (policy §8; master §IV.3.1) and only then submit the 12-task dev-test array from the snapshot;
# the job id is added to manifest.json after submission. After the array ends, run
# slurm/finalize_run.sh <RUN_ID> <JOB> to validate, score and record completion.
# Usage (NOTS login node): bash slurm/freeze_and_submit.sh
set -euo pipefail
SRC=/home/fb31/projects/BVS/Benchmarks/A2_SSL
OUTBASE=/projects/ml75/fb31/BVS/bench20261019/dev_test/A2_SSL
DEV=/projects/ml75/fb31/BVS/bench20261019/dev
RUN_ID=$(date -u +%Y%m%dT%H%MZ)_bench20261019_A2_dev
SNAP=$OUTBASE/runs/$RUN_ID/code
mkdir -p "$SNAP"
cp -r "$SRC"/config.R "$SRC"/common.R "$SRC"/run_case.R "$SRC"/score_dev.R "$SRC"/check_dev.R "$SRC"/methods "$SRC"/tests "$SRC"/slurm "$SNAP"/
CMD="sbatch --parsable --export=ALL,CODE=$SNAP,RUN_ID=$RUN_ID $SNAP/slurm/dev_test.slurm"
JOB=pending
chmod -R a-w "$SNAP"
cd "$SNAP"
TREE=$(for f in config.R common.R methods/fit_A2_ssl.R run_case.R; do printf "%s  %s\n" "$(sha256sum "$f" | cut -d" " -f1)" "$f"; done | head -c -1 | sha256sum | cut -d" " -f1)
python3 - "$OUTBASE/runs/$RUN_ID/manifest.json" "$SNAP" "$RUN_ID" "$JOB" "$CMD" "$TREE" "$DEV" "$OUTBASE" <<'PY'
import hashlib, json, os, sys, socket, subprocess, datetime
out, snap, run_id, job, cmd, tree, dev, outbase = sys.argv[1:]
def sha(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()
files = {}
for root, _, fs in os.walk(snap):
    for f in sorted(fs):
        p = os.path.join(root, f); files[os.path.relpath(p, snap)] = sha(p)
man = os.path.join(dev, 'manifests', 'dev_inputs_manifest.csv')
rows = [l.strip().split(',') for l in open(man)][1:]
m = {"run_id": run_id, "piece": "A2 dev test (single seed: dev replicate 1, scale c100)",
     "created_utc": datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
     "code_snapshot": snap, "code_sha256": files, "source_tree_sha256": tree,
     "sbatch_command": cmd, "submit_host": socket.gethostname(), "slurm_job_id": job, "array": "1-12",
     "method_ids": ["A2", "SSL-RS"], "scale_key": "c100",
     "seeds": {"method_seed": sorted(int(r[6]) for r in rows), "rule": "data seed + 4,000,000; SSL uses no random numbers"},
     "modules": "GCC/14.3.0 R/4.5.2", "r_library": "/projects/ml75/fb31/BVS/bench20261019/lib/R452",
     "package_manifest_sha256": sha('/projects/ml75/fb31/BVS/bench20261019/lib/environment_manifest.txt'),
     "blas": "FlexiBLAS 3.4.5 / OpenBLAS 0.3.30 (threads 1)",
     "inputs": {"dir": os.path.join(dev, 'inputs'), "manifest": man, "manifest_sha256": sha(man)},
     "outputs": {"results": os.path.join(outbase, 'results', run_id), "logs": os.path.join(outbase, 'logs')},
     "status": "frozen, not yet submitted"}
json.dump(m, open(out, 'w'), indent=2)
PY
MAN=$OUTBASE/runs/$RUN_ID/manifest.json
JOB=$($CMD)
python3 - "$MAN" "$JOB" <<'PY'
import json, sys, datetime
m = json.load(open(sys.argv[1])); m["slurm_job_id"] = sys.argv[2]; m["status"] = "submitted"
m["submitted_utc"] = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
json.dump(m, open(sys.argv[1], 'w'), indent=2)
PY
echo "RUN_ID=$RUN_ID JOB=$JOB"
