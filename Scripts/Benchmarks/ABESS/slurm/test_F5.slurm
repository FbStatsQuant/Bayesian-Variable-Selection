#!/usr/bin/env bash
# G3 unit tests for F5 (one SLURM job). Submit from anywhere: sbatch slurm/test_F5.slurm <code_dir>
#SBATCH --job-name=F5_tests
#SBATCH --partition=commons
#SBATCH --account=commons
#SBATCH --cpus-per-task=1
#SBATCH --mem=2G
#SBATCH --time=00:30:00
#SBATCH --output=/projects/ml75/fb31/BVS/bench20261019/dev_test/F5_ABESS/logs/%x_%j.out
#SBATCH --error=/projects/ml75/fb31/BVS/bench20261019/dev_test/F5_ABESS/logs/%x_%j.err
set -euo pipefail
CODE=${1:?code dir}
source "$CODE/slurm/env.sh"
OUT="$F5_OUT/tests/${SLURM_JOB_ID}"
mkdir -p "$OUT"
{ hostname; date -u; module -t list 2>&1; Rscript --version; nproc; } > "$OUT/environment.txt" 2>&1
(cd "$CODE" && sha256sum config.R common.R methods/*.R run_case.R run_task.R validate_outputs.R score_dev.R tests/*.R slurm/*) > "$OUT/code.sha256"
rc=0
Rscript --vanilla "$CODE/tests/test_common.R" "$CODE" "$OUT" || rc=1
Rscript --vanilla "$CODE/tests/test_F5_abess.R" "$CODE" "$OUT" "$DEV_ROOT" /projects/ml75/fb31/BVS/bench20261019 || rc=1
echo "tests exit $rc"
exit $rc
