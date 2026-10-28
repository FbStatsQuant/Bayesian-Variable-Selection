#!/bin/bash
# Freezes the code into a read-only snapshot under the output folder, writes manifest.json
# (policy §8, master §IV.3.1) and submits the 12-task dev array. Run on the login node from anywhere:
#   bash slurm/freeze_and_submit_dev.sh
set -euo pipefail
SRC=/home/fb31/projects/BVS/Benchmarks/F4_MCP_SCAD
OUT=/projects/ml75/fb31/BVS/bench20261019/dev_test/F4_MCP_SCAD
TS=$(date -u +%Y%m%dT%H%MZ)
RUN_ID=${TS}_F4_dev_test
SNAP=$OUT/runs/$RUN_ID
mkdir -p "$SNAP/code" "$OUT/logs"
cp -r "$SRC"/config.R "$SRC"/common.R "$SRC"/run_case.R "$SRC"/score_dev.R "$SRC"/validate_dev.R "$SRC"/methods "$SRC"/tests "$SRC"/slurm "$SNAP/code/"
( cd "$SNAP/code" && find . -type f | sort | xargs sha256sum > ../code_sha256.txt )
TREE=$(sha256sum "$SNAP/code_sha256.txt" | cut -d' ' -f1)
chmod -R a-w "$SNAP/code"
CMD="sbatch --parsable $SNAP/code/slurm/dev_array.slurm $SNAP/code $RUN_ID"
JOB=$($CMD)
MAN_IN=/projects/ml75/fb31/BVS/bench20261019/dev/manifests/dev_inputs_manifest.csv
cat > "$SNAP/manifest.json" <<JSON
{
  "run_id": "$RUN_ID",
  "piece": "F4 MCP + F4_SCAD dev test (12 dev datasets, scale c100)",
  "code_tree_sha256": "$TREE",
  "code_files_sha256": "code_sha256.txt",
  "command": "$CMD",
  "submit_host": "$(hostname)",
  "job_id": "$JOB",
  "array": "1-12",
  "seeds": "method_seed = data_seed + 4000000 (6420001-6470001 at p=500, 6520001-6570001 at p=1000; F4 uses no random numbers)",
  "modules": "GCC/14.3.0 R/4.5.2 (FlexiBLAS/OpenBLAS)",
  "library": "/projects/ml75/fb31/BVS/bench20261019/lib/R452 (environment_manifest.txt sha256 $(sha256sum /projects/ml75/fb31/BVS/bench20261019/lib/environment_manifest.txt | cut -d' ' -f1))",
  "inputs": "/projects/ml75/fb31/BVS/bench20261019/dev/inputs/p0500|p1000/dev_p*_S*_r001.rds",
  "inputs_manifest_sha256": "$(sha256sum $MAN_IN | cut -d' ' -f1)",
  "outputs": "$OUT/results/$RUN_ID",
  "submitted_utc": "$(date -u +%FT%TZ)",
  "status": "submitted"
}
JSON
echo "$RUN_ID $JOB"
