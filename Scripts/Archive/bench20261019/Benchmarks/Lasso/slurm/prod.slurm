#!/usr/bin/env bash
# Production array for F1 (master D3: scale c100 only, 1,200 datasets). Task t = 1..120 is a chunk of 10 datasets
# of one p: t <= 60 -> p = 500, else p = 1000; u = (t - 1) % 60; scenario = u / 10 + 1; replicates 10*(u % 10) + 1..10.
# Usage (from the frozen snapshot, see submit_prod.sh):
#   sbatch --array=1-120%60 prod.slurm <snapshot code dir> <run_id>              (production)
#   sbatch prod.slurm <snapshot code dir> <run_id> <dataset_id>                  (one dataset, e.g. the smoke test)
#SBATCH --job-name=F1_prod
#SBATCH --account=commons
#SBATCH --partition=commons
#SBATCH --cpus-per-task=1
#SBATCH --mem=2G
#SBATCH --time=01:15:00
#SBATCH --output=/projects/ml75/fb31/BVS/bench20261019/logs/prod/F1_Lasso/%x_%A_%a.out
#SBATCH --error=/projects/ml75/fb31/BVS/bench20261019/logs/prod/F1_Lasso/%x_%A_%a.err
set -uo pipefail
CODE=${1:?snapshot code dir}; RUN_ID=${2:?run id}; ONE=${3:-}
source "$CODE/slurm/env.sh"
# refuse to run unless the snapshot verifies against its frozen hash list
( cd "$CODE" && sha256sum -c --quiet ../code.sha256 ) || { echo "snapshot hash mismatch: $CODE" >&2; exit 3; }
# frozen copies of the inputs manifest and the library manifest, verified against their submission-time hashes
( cd "$CODE/.." && sha256sum -c --quiet frozen_manifests.sha256 ) || { echo "frozen manifest mismatch" >&2; exit 3; }
MAN=$CODE/../inputs_manifest.csv
# installed study library must match the frozen inventory (package versions)
Rscript --vanilla "$CODE/verify_library.R" "$BENCH_LIB" "$CODE/../environment_manifest.txt" || { echo "library does not match the frozen inventory" >&2; exit 3; }
mkdir -p "$STUDY/logs/prod/F1_Lasso/env"
{ hostname; date -u; module -t list 2>&1; command -v Rscript; Rscript --version 2>&1;
  Rscript --vanilla -e 'cat(extSoftVersion()[["BLAS"]], La_library(), sep = "\n")'; env | sort | grep -E '^(SLURM_JOB_ID|SLURM_ARRAY|OMP|OPENBLAS|MKL|FLEXIBLAS|BENCH_LIB)'; } \
  > "$STUDY/logs/prod/F1_Lasso/env/${SLURM_JOB_ID:-nojob}.txt" 2>&1
export TMPDIR=$(mktemp -d /tmp/fb31_F1_XXXXXX); trap 'rm -rf -- "$TMPDIR"' EXIT
if [[ -n "$ONE" ]]; then
  ids=("$ONE")
else
  t=${SLURM_ARRAY_TASK_ID:?}; [[ "$t" -ge 1 && "$t" -le 120 ]] || exit 2
  if [[ "$t" -le 60 ]]; then p=500; else p=1000; fi
  u=$(( (t - 1) % 60 )); s=$(( u / 10 + 1 )); r0=$(( (u % 10) * 10 ))
  ids=(); for r in $(seq $((r0 + 1)) $((r0 + 10))); do ids+=("$(printf 'p%04d_S%d_r%03d' "$p" "$s" "$r")"); done
fi
echo "host $(hostname) job ${SLURM_JOB_ID:-} task ${SLURM_ARRAY_TASK_ID:-} datasets ${ids[*]}"
nfail=0
for id in "${ids[@]}"; do
  pdir=${id%%_*}
  Rscript --vanilla "$CODE/run_case.R" --code-dir "$CODE" --input "$STUDY/inputs/$pdir/$id.rds" --scale c100 \
    --out-root "$STUDY" --run-id "$RUN_ID" --manifest "$MAN" --lib "$BENCH_LIB" || { echo "FAILED $id" >&2; nfail=$((nfail + 1)); }
done
echo "done: ${#ids[@]} datasets, $nfail runner failure(s)"
if [[ -n "$ONE" ]]; then   # single-dataset run (smoke test): validate its outputs with the dev checker
  Rscript --vanilla "$CODE/check_outputs.R" "$CODE" "$STUDY/results/$RUN_ID" "$MAN" "$F1_OUT/summary/$RUN_ID" "$ONE" || nfail=$((nfail + 1))
fi
[[ "$nfail" -eq 0 ]]
