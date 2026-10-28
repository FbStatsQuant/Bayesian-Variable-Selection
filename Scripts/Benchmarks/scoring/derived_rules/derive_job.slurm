#!/bin/bash
#SBATCH --job-name=S_derive
#SBATCH --partition=commons
#SBATCH --cpus-per-task=1
#SBATCH --mem=4G
#SBATCH --time=01:00:00
#SBATCH --output=/projects/ml75/fb31/BVS/bench20261019/scoring/logs/%x_%j.out
# Derived-rule unit (thread S). Arguments: run ids. Writes $STUDY/derived/<run_id>/derived_rules/.
set -euo pipefail
S=/projects/ml75/fb31/BVS/bench20261019
CODE=$S/scoring/derived_rules
module load GCC/14.3.0 R/4.5.2 >/dev/null 2>&1
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
echo "host $(hostname) job ${SLURM_JOB_ID:-none} start $(date -u +%FT%TZ)"
(cd $CODE && sha256sum derive_rules.R test_derive.R compare_k37.R derive_job.slurm)
Rscript --vanilla $CODE/test_derive.R
for run in "$@"; do
  echo; echo "######## $run $(date -u +%FT%TZ)"
  out=$S/derived/$run/derived_rules
  mkdir -p $out
  Rscript --vanilla $CODE/derive_rules.R --results $S/results/$run --out $out --selfcheck
  (cd $out && sha256sum derived_rule_rows.csv derive_log.txt selfcheck_cap100.csv > SHA256SUMS && cp $CODE/derive_rules.R . && sha256sum derive_rules.R >> SHA256SUMS)
done
# Independent check at c = 1: this unit's ebic1_K37 rows against the existing derived K37 rows (outputs only).
CMP=$CODE/compare; mkdir -p $CMP
F4R=20261019T2219Z_bench20261019_prod_F4_MCP_SCAD; F5R=20261019T2157Z_bench20261019_prod_F5_ABESS
if [ -f $S/derived/$F4R/derived_rules/derived_rule_rows.csv ]; then
  Rscript --vanilla $CODE/compare_k37.R --mine $S/derived/$F4R/derived_rules/derived_rule_rows.csv     --theirs $S/derived/$F4R/ebic1_K37_rule_rows.csv --out $CMP --tag F4_F4SCAD; fi
if [ -f $S/derived/$F5R/derived_rules/derived_rule_rows.csv ]; then
  Rscript --vanilla $CODE/compare_k37.R --mine $S/derived/$F5R/derived_rules/derived_rule_rows.csv     --theirs $S/derived/$F5R/F5_ebic1_K37.csv --out $CMP --tag F5; fi
echo "end $(date -u +%FT%TZ)"
