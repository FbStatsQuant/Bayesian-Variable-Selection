#!/bin/bash
#SBATCH --job-name=F4_canary
#SBATCH --partition=commons
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=2G
#SBATCH --time=00:30:00
#SBATCH --output=/projects/ml75/fb31/BVS/bench20261019/logs/prod/F4_MCP_SCAD/%x_%j.out
# Production canaries (master §IV.3): re-run 3 dev cases with the production snapshot into
# results/<run_id>/canary/ and require the scientific outputs to equal the dev reference run bit for bit.
# Arguments: CODE_DIR (read-only snapshot) RUN_ID.
set -uo pipefail
CODE_DIR=$1; RUN_ID=$2
source "$CODE_DIR/slurm/env.sh" || exit 4
SNAP=$(dirname "$CODE_DIR")
( cd "$CODE_DIR" && sha256sum -c --quiet "$SNAP/code_sha256.txt" ) || { echo "FATAL: code snapshot hash mismatch"; exit 3; }
REF=$STUDY/dev_test/F4_MCP_SCAD/results/20261019T2035Z_F4_dev_test
OUT=$STUDY/results/$RUN_ID/canary
IDS="dev_p0500_S4_r001 dev_p1000_S2_r001 dev_p1000_S6_r001"
fail=0
for d in $IDS; do
  pp=${d#dev_}; pp=${pp%%_*}
  Rscript --vanilla "$CODE_DIR/run_case.R" --input "$STUDY_DEV/inputs/$pp/$d.rds" --out-root "$OUT" --run-id "$RUN_ID" \
    --scale c100 --methods F4,F4_SCAD --manifest "$STUDY_DEV/manifests/dev_inputs_manifest.csv" || { echo "INFRA_FAILED $d"; fail=1; }
done
Rscript --vanilla "$CODE_DIR/compare_canary.R" "$REF" "$OUT" "$(echo $IDS | tr ' ' ',')" "$SNAP/canary_comparison.txt" || fail=1
echo "end $(date -u +%FT%TZ) fail=$fail"
exit $fail
