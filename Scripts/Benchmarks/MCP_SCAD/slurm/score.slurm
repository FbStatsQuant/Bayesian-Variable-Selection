#!/bin/bash
#SBATCH --job-name=F4_score
#SBATCH --partition=commons
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=1G
#SBATCH --time=00:10:00
#SBATCH --output=/projects/ml75/fb31/BVS/bench20261019/dev_test/F4_MCP_SCAD/logs/%x_%j.out
# Scoring of the dev test (score_dev.R; reads truth/). Arguments: CODE_DIR RUN_ID.
set -euo pipefail
CODE_DIR=$1; RUN_ID=$2
source "$CODE_DIR/slurm/env.sh"
Rscript "$CODE_DIR/score_dev.R" "$F4_OUT/results/$RUN_ID" "$STUDY_DEV/truth" "$F4_OUT/scoring/$RUN_ID"
