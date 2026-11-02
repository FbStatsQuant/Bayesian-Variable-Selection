#!/usr/bin/env bash
# Freezes the F1 code into a read-only snapshot $STUDY/runs/<run_id>/code with code.sha256 and manifest.json,
# verifies it, then submits from the snapshot. Run on the NOTS login node.
#   bash submit_prod.sh --dry-run     everything except sbatch (prints the sbatch command)
#   bash submit_prod.sh               production: 120-task array, %60 concurrency
#   bash submit_prod.sh --smoke       one dataset (p1000_S4_r001, c100) into run id ..._prodsmoke_F1_Lasso, then validate
set -euo pipefail
MODE=${1:-prod}
source /home/fb31/projects/BVS/Benchmarks/F1_Lasso/slurm/env.sh
STAMP=$(date -u +%Y%m%dT%H%MZ)
case "$MODE" in
  --smoke) RUN_ID=${STAMP}_bench20261019_prodsmoke_F1_Lasso ;;
  --dry-run|prod) RUN_ID=${STAMP}_bench20261019_prod_F1_Lasso ;;
  *) echo "usage: submit_prod.sh [--dry-run|--smoke]" >&2; exit 2 ;;
esac
SNAP=$STUDY/runs/$RUN_ID; CODE=$SNAP/code
[[ ! -e "$SNAP" ]] || { echo "exists: $SNAP" >&2; exit 2; }
[[ -f "$STUDY/manifests/inputs_manifest.csv" ]] || { echo "missing production inputs manifest" >&2; exit 2; }
mkdir -p "$CODE" "$STUDY/logs/prod/F1_Lasso"
( cd "$F1_CODE" && cp -r config.R common.R run_case.R check_outputs.R score_dev.R reconcile_prod.R verify_library.R methods tests slurm "$CODE/" )
cp "$STUDY/manifests/inputs_manifest.csv" "$STUDY/lib/environment_manifest.txt" "$SNAP/"
( cd "$SNAP" && sha256sum inputs_manifest.csv environment_manifest.txt > frozen_manifests.sha256 )
chmod a-w "$SNAP/inputs_manifest.csv" "$SNAP/environment_manifest.txt" "$SNAP/frozen_manifests.sha256"
( cd "$CODE" && find . -type f | sort | xargs sha256sum > ../code.sha256 )
( cd "$F1_CODE" && sha256sum -c --quiet "$SNAP/code.sha256" )      # snapshot equals the source tree
chmod -R a-w "$CODE"; chmod a-w "$SNAP/code.sha256"
( cd "$CODE" && sha256sum -c --quiet ../code.sha256 )
TREE=$(sha256sum "$SNAP/code.sha256" | cut -d' ' -f1)
if [[ "$MODE" == "--smoke" ]]; then
  CMD="sbatch --parsable --time=00:30:00 $CODE/slurm/prod.slurm $CODE $RUN_ID p1000_S4_r001"
else
  CMD="sbatch --parsable --array=1-120%60 $CODE/slurm/prod.slurm $CODE $RUN_ID"
fi
# the launch record is written BEFORE sbatch; the job id is filled in after submission
JOB="pending"; [[ "$MODE" == "--dry-run" ]] && JOB="(dry run: not submitted)"
write_manifest() {
cat > "$SNAP/manifest.json.tmp" <<JSON
{
  "run_id": "$RUN_ID",
  "piece": "F1 Lasso production, scale c100 only (master D3)$([[ $MODE == --smoke ]] && echo ' -- SMOKE TEST, one dataset')",
  "created_utc": "$(date -u +%FT%TZ)",
  "host_submit": "$(hostname)",
  "code_dir": "$CODE",
  "code_sha256_list": "$SNAP/code.sha256",
  "code_tree_sha256": "$TREE",
  "sbatch_command": "$CMD",
  "job_id": "$JOB",
  "tasks": "$([[ $MODE == --smoke ]] && echo 'one dataset p1000_S4_r001' || echo '1-120 (%60): t<=60 p=500, else p=1000; 10 datasets per task')",
  "seeds": "method_seed = data_seed + 4000000 from each input file (p500: 5420001-5470100; p1000: 5520001-5570100); F1 draws no random numbers",
  "modules": "GCC/14.3.0 R/4.5.2",
  "study_library": "$BENCH_LIB",
  "library_manifest_sha256": "$(sha256sum "$SNAP/environment_manifest.txt" | cut -d' ' -f1) (frozen copy in the run folder)",
  "inputs": "$STUDY/inputs/p0500, $STUDY/inputs/p1000",
  "inputs_manifest": "$SNAP/inputs_manifest.csv (frozen copy of $STUDY/manifests/inputs_manifest.csv)",
  "inputs_manifest_sha256": "$(sha256sum "$SNAP/inputs_manifest.csv" | cut -d' ' -f1)",
  "outputs": "$STUDY/results/$RUN_ID",
  "logs": "$STUDY/logs/prod/F1_Lasso",
  "rerun": "resubmit the same sbatch_command; the runner skips cases with a verified .done",
  "status": "$([[ $MODE == --dry-run ]] && echo 'dry run' || echo "$1")"
}
JSON
mv "$SNAP/manifest.json.tmp" "$SNAP/manifest.json"
}
write_manifest "submitting"
if [[ "$MODE" != "--dry-run" ]]; then
  JOB=$($CMD) || { write_manifest "sbatch failed"; echo "sbatch failed" >&2; exit 5; }
  write_manifest "submitted"
fi
echo "RUN_ID $RUN_ID"; echo "SNAPSHOT $CODE"; echo "TREE $TREE"; echo "MANIFEST $SNAP/manifest.json"; echo "CMD $CMD"; echo "JOB $JOB"
