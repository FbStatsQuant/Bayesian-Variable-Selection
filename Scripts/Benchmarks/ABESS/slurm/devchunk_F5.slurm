#!/usr/bin/env bash
# Dev chunk test: the 12 dev datasets (c100) as ONE production-style task through run_task.R
# (chunk timing and memory across cases), then validation, scoring, the canary comparison
# with the reference dev run, and the conditioning diagnostic.
# Usage: sbatch slurm/devchunk_F5.slurm <snapshot code dir> <run_id> <reference run_id>
#SBATCH --job-name=F5_devchunk
#SBATCH --partition=commons
#SBATCH --account=commons
#SBATCH --cpus-per-task=1
#SBATCH --mem=2G
#SBATCH --time=00:30:00
#SBATCH --output=/projects/ml75/fb31/BVS/bench20261019/dev_test/F5_ABESS/logs/%x_%j.out
#SBATCH --error=/projects/ml75/fb31/BVS/bench20261019/dev_test/F5_ABESS/logs/%x_%j.err
set -euo pipefail
SNAP=${1:?}; RID=${2:?}; REF=${3:?}
source "$SNAP/slurm/env.sh"
(cd "$SNAP" && sha256sum -c --quiet ../code.sha256)
CASES=$(for p in p0500 p1000; do for s in 1 2 3 4 5 6; do printf "dev_%s_S%d_r001_c100," $p $s; done; done); CASES=${CASES%,}
t0=$(date +%s)
Rscript --vanilla "$SNAP/run_task.R" --dev 1 --data-root "$DEV_ROOT" --out-root "$F5_OUT" --run-id "$RID" \
  --code-root "$SNAP" --status-dir "$F5_OUT/status/$RID"
echo "chunk wall seconds: $(( $(date +%s) - t0 ))"
Rscript --vanilla "$SNAP/validate_outputs.R" "$SNAP" "$F5_OUT/results/$RID" "$DEV_ROOT/manifests/dev_inputs_manifest.csv" "$CASES" "$DEV_ROOT/inputs"
mkdir -p "$F5_OUT/scored"
Rscript --vanilla "$SNAP/score_dev.R" "$F5_OUT/results/$RID" "$DEV_ROOT" "$F5_OUT/scored/$RID" | tail -4
Rscript --vanilla "$SNAP/tools/compare_runs.R" "$F5_OUT/results/$REF" "$F5_OUT/results/$RID"
Rscript --vanilla "$SNAP/tools/conditioning_diag.R" "$F5_OUT/results/$RID" "$DEV_ROOT/inputs"
