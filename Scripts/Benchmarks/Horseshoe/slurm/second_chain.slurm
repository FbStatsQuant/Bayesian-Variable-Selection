#!/bin/bash
# Two-chain stability check (master §III.3.8 i, O10) on the 12 dev datasets (tasks as in
# dev_A3.slurm). Requires A3_CODE (snapshot of the dev run being checked) and PRIMARY_RUN.
#SBATCH --job-name=A3_chain2
#SBATCH --partition=commons
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=4G
#SBATCH --time=01:00:00
#SBATCH --array=1-12
#SBATCH --output=/projects/ml75/fb31/BVS/bench20261019/dev_test/A3_Horseshoe/logs/chain2_%A_%a.out
set -euo pipefail
: "${A3_CODE:?}" "${PRIMARY_RUN:?}"
source "$A3_CODE/slurm/env.sh"
t=$SLURM_ARRAY_TASK_ID
if [ "$t" -le 6 ]; then p=500; else p=1000; fi
s=$(( (t - 1) % 6 + 1 )); P=$(printf "%04d" $p)
Rscript --vanilla "$A3_CODE/tests/second_chain.R" "$STUDY/dev/inputs/p$P/dev_p${P}_S${s}_r001.rds" \
  "$A3_OUT/results/$PRIMARY_RUN" "$A3_OUT/second_chain/$PRIMARY_RUN"
