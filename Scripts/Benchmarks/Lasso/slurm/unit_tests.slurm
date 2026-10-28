#!/usr/bin/env bash
# G3 unit tests for F1 (tests/test_common.R, tests/test_F1_lasso.R), one job.
# Submit from anywhere: sbatch /home/fb31/projects/BVS/Benchmarks/F1_Lasso/slurm/unit_tests.slurm <code_dir>
#SBATCH --job-name=F1_unit
#SBATCH --account=commons
#SBATCH --partition=commons
#SBATCH --cpus-per-task=1
#SBATCH --mem=4G
#SBATCH --time=03:00:00
#SBATCH --output=/projects/ml75/fb31/BVS/bench20261019/dev_test/F1_Lasso/logs/%x_%j.out
#SBATCH --error=/projects/ml75/fb31/BVS/bench20261019/dev_test/F1_Lasso/logs/%x_%j.err
set -euo pipefail
source /home/fb31/projects/BVS/Benchmarks/F1_Lasso/slurm/env.sh
CODE=${1:-$F1_CODE}
OUT=$F1_OUT/unit_tests/${SLURM_JOB_ID}
mkdir -p "$OUT"
export TMPDIR=$(mktemp -d /tmp/fb31_F1_XXXXXX); trap 'rm -rf -- "$TMPDIR"' EXIT
{ hostname; date -u; module -t list 2>&1; Rscript --version 2>&1; env | sort | grep -E '^(SLURM_JOB_ID|OMP|OPENBLAS|MKL|BENCH_LIB)'; } > "$OUT/environment.txt"
rc=0
Rscript --vanilla "$CODE/tests/test_common.R" "$CODE" "$OUT" || rc=1
Rscript --vanilla "$CODE/tests/test_F1_lasso.R" "$CODE" "$DEV_INPUTS" "$OUT" || rc=1
echo "unit tests exit $rc"
exit $rc
