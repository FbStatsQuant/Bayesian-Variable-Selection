#!/bin/bash
#SBATCH --job-name=F4_checkprod
#SBATCH --partition=commons
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=2G
#SBATCH --time=00:30:00
#SBATCH --output=/projects/ml75/fb31/BVS/bench20261019/logs/prod/F4_MCP_SCAD/%x_%j.out
# Validates a production (or smoke) run against the 1,200-case inventory, its run id and the frozen
# inputs manifest; lists missing pairs for the one infrastructure retry (§IV.2.4).
# Arguments: CODE_DIR (snapshot) RUN_ID [CASES]   (CASES default PROD; smoke: p1000/p1000_S4_r001_c100)
set -uo pipefail
CODE_DIR=$1; RUN_ID=$2; CASES=${3:-PROD}
source "$CODE_DIR/slurm/env.sh" || exit 4
SNAP=$(dirname "$CODE_DIR")
Rscript --vanilla "$CODE_DIR/validate_dev.R" "$CODE_DIR" "$STUDY/results/$RUN_ID" "$CASES" "$SNAP/validation.txt" \
  "$RUN_ID" "$SNAP/frozen/inputs_manifest.csv"
