#!/bin/bash
#SBATCH --job-name=F4_unit
#SBATCH --partition=commons
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=4G
#SBATCH --time=00:45:00
#SBATCH --output=/projects/ml75/fb31/BVS/bench20261019/dev_test/F4_MCP_SCAD/logs/%x_%j.out
# G3 unit tests for F4 (tests/test_F4_mcp.R). Submit from the code folder:
#   sbatch slurm/unit_tests.slurm [CODE_DIR]
set -euo pipefail
CODE_DIR=${1:-/home/fb31/projects/BVS/Benchmarks/F4_MCP_SCAD}
source "$CODE_DIR/slurm/env.sh"
echo "host $(hostname) job $SLURM_JOB_ID cores $(nproc) start $(date -u +%FT%TZ)"
Rscript "$CODE_DIR/tests/test_F4_mcp.R" "$CODE_DIR" "$STUDY_DEV/inputs" "$F4_OUT/unit_tests/job_$SLURM_JOB_ID"
echo "end $(date -u +%FT%TZ)"
