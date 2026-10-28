#!/usr/bin/env bash
# Freezes the F1 code into a read-only snapshot with manifest.json (policy §8, master §IV.3.1),
# then submits the 12-task dev-test array from the snapshot. Run on the login node.
# Usage: bash launch_dev.sh
set -euo pipefail
source /home/fb31/projects/BVS/Benchmarks/F1_Lasso/slurm/env.sh
RUN_ID=dev_$(date -u +%Y%m%dT%H%MZ)_F1
SNAP=$F1_OUT/runs/$RUN_ID
[[ ! -e "$SNAP" ]]
mkdir -p "$SNAP/code"
( cd "$F1_CODE" && cp -r config.R common.R run_case.R check_outputs.R score_dev.R reconcile_prod.R verify_library.R methods tests slurm "$SNAP/code/" )
( cd "$SNAP/code" && find . -type f | sort | xargs sha256sum > ../code.sha256 )
TREE=$(sha256sum "$SNAP/code.sha256" | cut -d' ' -f1)
chmod -R a-w "$SNAP/code"
CMD="sbatch --parsable --array=1-12 $SNAP/code/slurm/dev_test.slurm $SNAP/code $RUN_ID"
JOB=$($CMD)
MAN=$(sha256sum "$DEV_MANIFEST" | cut -d' ' -f1)
LIBMAN=$(sha256sum "$STUDY/lib/environment_manifest.txt" | cut -d' ' -f1)
cat > "$SNAP/manifest.json" <<JSON
{
  "run_id": "$RUN_ID",
  "piece": "F1 Lasso dev test (12 dev datasets, scale c100, single seed each)",
  "created_utc": "$(date -u +%FT%TZ)",
  "host_submit": "$(hostname)",
  "code_dir": "$SNAP/code",
  "code_sha256_list": "$SNAP/code.sha256",
  "code_tree_sha256": "$TREE",
  "sbatch_command": "$CMD",
  "job_id": "$JOB",
  "array": "1-12",
  "seeds": "method_seed = data_seed + 4000000 from each dev input (6420001-6470001, 6520001-6570001); F1 draws no random numbers",
  "modules": "GCC/14.3.0 R/4.5.2",
  "study_library": "$BENCH_LIB",
  "library_manifest_sha256": "$LIBMAN",
  "inputs": "$DEV_INPUTS/p0500, $DEV_INPUTS/p1000 (dev_p*_S*_r001.rds)",
  "inputs_manifest": "$DEV_MANIFEST",
  "inputs_manifest_sha256": "$MAN",
  "outputs": "$F1_OUT/results/$RUN_ID",
  "status": "submitted"
}
JSON
echo "$RUN_ID $JOB"
