#!/bin/bash
# O10 diagnostic: one 60,000-iteration chain per dev dataset (tasks as in dev_A3.slurm).
#SBATCH --job-name=A3_long
#SBATCH --partition=commons
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=8G
#SBATCH --time=01:00:00
#SBATCH --array=1-12
#SBATCH --output=/projects/ml75/fb31/BVS/bench20261019/dev_test/A3_Horseshoe/logs/long_%A_%a.out
set -euo pipefail
CODE=${A3_CODE:-/home/fb31/projects/BVS/Benchmarks/A3_Horseshoe}
source "$CODE/slurm/env.sh"
t=$SLURM_ARRAY_TASK_ID
if [ "$t" -le 6 ]; then p=500; else p=1000; fi
s=$(( (t - 1) % 6 + 1 )); P=$(printf "%04d" $p)
Rscript "$CODE/tests/diag_long_chain.R" "$STUDY/dev/inputs/p$P/dev_p${P}_S${s}_r001.rds" "$A3_OUT/o10_long_chain" 60000
