#!/usr/bin/env bash
# Output checks and scoring of the dev test (check_outputs.R, then score_dev.R; the latter reads dev truth).
# Usage: sbatch score.slurm <code_dir> <run_id>
#SBATCH --job-name=F1_score
#SBATCH --account=commons
#SBATCH --partition=commons
#SBATCH --cpus-per-task=1
#SBATCH --mem=2G
#SBATCH --time=00:15:00
#SBATCH --output=/projects/ml75/fb31/BVS/bench20261019/dev_test/F1_Lasso/logs/%x_%j.out
#SBATCH --error=/projects/ml75/fb31/BVS/bench20261019/dev_test/F1_Lasso/logs/%x_%j.err
set -euo pipefail
source /home/fb31/projects/BVS/Benchmarks/F1_Lasso/slurm/env.sh
CODE=${1:?code dir}; RUN_ID=${2:?run id}
RES=$F1_OUT/results/$RUN_ID
Rscript --vanilla "$CODE/check_outputs.R" "$CODE" "$RES" "$DEV_MANIFEST" "$F1_OUT/summary/$RUN_ID"
Rscript --vanilla "$CODE/score_dev.R" "$RES" "$STUDY/dev/truth" "$F1_OUT/summary/$RUN_ID"
Rscript --vanilla "$CODE/reconcile_prod.R" "$CODE" "$RES" "$DEV_MANIFEST" "$F1_OUT/summary/$RUN_ID/reconcile"
