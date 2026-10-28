#!/usr/bin/env bash
# NOT LAUNCHED. Stratified exact enumeration, one array task per dataset. Task t in 1..600:
#   scenario = (t-1)/100 + 1  (S1..S6),  replicate = (t-1)%100 + 1.
#   sbatch --array=1-600%150 strat.slurm            (smoke first: sbatch --array=1,101,501 strat.slurm)
# Expected: ~9 CPU-min per task (1.08 x the frozen exact reference), < 1 GB, ~90 CPU-h total.
#SBATCH --job-name=bvs_strat
#SBATCH --account=commons
#SBATCH --partition=commons
#SBATCH --cpus-per-task=1
#SBATCH --mem=2G
#SBATCH --time=00:45:00
#SBATCH --output=/home/fb31/projects/BVS/enum_stratified/logs/%x_%A_%a.out
#SBATCH --error=/home/fb31/projects/BVS/enum_stratified/logs/%x_%A_%a.err
set -euo pipefail
ROOT=${ENUM_ROOT:-/home/fb31/projects/BVS/enum_stratified}          # holds exact_stratified.{R,cpp}, run_strat_task.R, engine_copy/
t=${SLURM_ARRAY_TASK_ID:?must run as a Slurm array}
scenario=$(( (t-1)/100 + 1 )); replicate=$(( (t-1)%100 + 1 ))
if (( scenario <= 5 )); then DATA=${BVS_DATA_COMMON:-/home/fb31/projects/BVS/data}; else DATA=${BVS_DATA_S6:-/home/fb31/projects/BVS/Benchmarks/data_S6}; fi
OUT=${ENUM_OUT:-/home/fb31/projects/BVS/enum_stratified/output}
# environment: same module/R setup as Benchmarks/slurm/environment.sh
[ -f /home/fb31/projects/BVS/Benchmarks/slurm/environment.sh ] && source /home/fb31/projects/BVS/Benchmarks/slurm/environment.sh
exec Rscript --vanilla "$ROOT/run_strat_task.R" "$scenario" "$replicate" "$DATA" "$OUT" 1
