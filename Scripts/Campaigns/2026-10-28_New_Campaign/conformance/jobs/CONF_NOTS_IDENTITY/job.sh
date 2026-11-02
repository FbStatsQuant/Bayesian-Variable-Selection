#!/bin/bash
# CONF_NOTS_IDENTITY: two historical p500 units with code v2.2, production environment (runner/env.sh of the 2,400-fit run).
#SBATCH --job-name=conf_identity
#SBATCH --nodes=1 --ntasks=1 --cpus-per-task=1 --mem=2G
#SBATCH --time=03:40:00
#SBATCH --constraint=sapphirerapids
#SBATCH --export=NONE --no-requeue
#SBATCH --output=/home/fb31/projects/BVS/New_Campaign/logs/conf_identity/%j.out
set -euo pipefail
BUNDLE=/home/fb31/projects/BVS/New_Campaign/jobs/CONF_NOTS_IDENTITY
CODE=/home/fb31/projects/BVS/New_Campaign/code/v2_2
STUDY=/projects/ml75/fb31/BVS/bench20261019
OUT=/scratch/fb31/New_Campaign/results/conf_identity
EV="$BUNDLE/run_env_${SLURM_JOB_ID}.txt"
CASE=none
trap 'rc=$?; { echo "failed_case $CASE"; echo "end $(date -u +%FT%TZ)"; echo "final_status $rc"; } >> "$EV"' EXIT
{ echo "job $SLURM_JOB_ID host $(hostname) start $(date -u +%FT%TZ)"; echo "command sbatch $BUNDLE/job.sh"
  (cd "$BUNDLE" && sha256sum job.sh env.sh precompile.R v2_2.SHA256SUMS compare_identity.R cmp2.R); } > "$EV"
source "$BUNDLE/env.sh"
# Fresh gate: refuse a pre-built compile cache or pre-existing outputs (they would be reused, not re-run). Never delete them here.
if [[ -e "$CODE/core/.cpp_cache" ]]; then echo "FATAL: $CODE/core/.cpp_cache exists; upload a fresh tree" >&2; exit 65; fi
if [[ -e "$OUT/results/conf_identity" ]]; then echo "FATAL: $OUT/results/conf_identity exists; use a fresh location" >&2; exit 65; fi
(cd "$CODE" && sha256sum --strict -c --quiet "$BUNDLE/v2_2.SHA256SUMS")      # frozen v2.2 tree
{ lscpu | grep -E '^(Model name|Flags)' | cut -c1-4000
  echo "gcc $(gcc -dumpfullversion)"
  Rscript --vanilla -e 'cat(R.version.string, "\n", sep = ""); cat("Rcpp ", as.character(packageVersion("Rcpp")), "\n", sep = "")'
  env | grep -E '_NUM_THREADS|^LC_ALL|^R_LIBS|^LOADEDMODULES' | sort
  echo "R_CMD_config_CXX17 $(R CMD config CXX17) | $(R CMD config CXX17FLAGS) | $(R CMD config CXX17STD)"; } >> "$EV"
# Fresh compile with visible compiler commands (job-side precompile; frozen sources untouched); both units then reuse this cache.
CASE=precompile
Rscript --vanilla "$BUNDLE/precompile.R" "$CODE/core" > "$BUNDLE/compile_${SLURM_JOB_ID}.log" 2>&1
grep '^compiled_key ' "$BUNDLE/compile_${SLURM_JOB_ID}.log" >> "$EV"
find "$CODE/core/.cpp_cache" -name '*.so' -exec sha256sum {} \; | sed 's/^/so_sha256 /' >> "$EV"
for CASE in p0500_S3_r044_c100 p0500_S5_r059_c100; do
  cmd=(Rscript --vanilla "$CODE/study/run_case.R" --case "$CASE" --scale c100 --study "$STUDY" --outroot "$OUT"
       --run_id conf_identity --mem_gb 2 --hours 1.75)
  echo "run ${cmd[*]}" >> "$EV"
  "${cmd[@]}"
  echo "case $CASE exit $?" >> "$EV"
  test -f "$OUT/results/conf_identity/p0500/$CASE/SMCBVS.done"
  (cd "$OUT/results/conf_identity/p0500/$CASE" && sha256sum --strict -c --quiet SMCBVS.sha256)
done
CASE=none
