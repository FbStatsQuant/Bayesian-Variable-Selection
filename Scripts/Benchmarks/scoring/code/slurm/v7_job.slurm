#!/bin/bash
#SBATCH --job-name=S_v7
#SBATCH --partition=commons
#SBATCH --cpus-per-task=1
#SBATCH --mem=8G
#SBATCH --time=01:00:00
#SBATCH --output=/projects/ml75/fb31/BVS/bench20261019/scoring/logs/%x_%j.out
# v7 (thread S, 2026-10-22): k_gt_K counted for F1-F3 CV rules. Re-aggregates combined_c050 and combined_v3
# from their existing per-run scoring outputs into NEW folders combined_c050_v7 and combined_v3_v7 (old
# folders untouched), regenerates the cross-run files, then diffs old vs new cell by cell.
set -euo pipefail
S=/projects/ml75/fb31/BVS/bench20261019; O=$S/scoring/out; CODE=$S/scoring/code
module load GCC/14.3.0 R/4.5.2 >/dev/null 2>&1
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
echo "host $(hostname) job ${SLURM_JOB_ID:-none} start $(date -u +%FT%TZ)"
(cd $CODE && sha256sum registry.R score.R aggregate.R combine.R pair.R a3_flags.R a3_longchain.R compare_versions.R tests/test_scoring.R slurm/v7_job.slurm)
Rscript --vanilla $CODE/tests/test_scoring.R | tail -1
for old in combined_c050 combined_v3; do
  new=${old}_v7
  [ -e $O/$new ] && { echo "$new exists; stop"; exit 1; }
  for r in $(ls $O/$old/runs); do
    mkdir -p $O/$new/runs/$r
    # scoring outputs are copied unchanged (scoring itself is not affected); aggregation is re-run
    (cd $O/$old/runs/$r && cp -p scored_rows.csv coverage.csv problems.csv files_extra.csv truth_signals.csv score_log.txt $O/$new/runs/$r/)
    Rscript --vanilla $CODE/aggregate.R --dir $O/$new/runs/$r > /dev/null
    (cd $CODE && sha256sum registry.R score.R aggregate.R) > $O/$new/runs/$r/code_sha256.txt
    (cd $O/$new/runs/$r && sha256sum *.csv summary.md > outputs_sha256.txt)
  done
  Rscript --vanilla $CODE/combine.R --out $O/$new $(ls -d $O/$new/runs/*)
done
N5=$O/combined_c050_v7; N1=$O/combined_v3_v7
Rscript --vanilla $CODE/pair.R --c050 $N5/runs --c100 $N1/runs --out $N5
Rscript --vanilla $CODE/a3_flags.R --c050 $(ls -d $N5/runs/*_A3_Horseshoe) --c100 $(ls -d $N1/runs/*_A3_Horseshoe) --out $N5
Rscript --vanilla $CODE/a3_longchain.R --long050 $S/results/20261021T2048Z_bench20261019_longc050_A3_Horseshoe \
  --long100 $S/results/20261021T2048Z_bench20261019_longc100_A3_Horseshoe --prod050 $(ls -d $N5/runs/*_A3_Horseshoe) \
  --prod100 $(ls -d $N1/runs/*_A3_Horseshoe) --manifest $S/manifests/inputs_manifest.csv --truth $S/truth_scoring \
  --truth-manifest $S/truth_scoring/truth_manifest.csv --out $N5
for n in $N5 $N1; do (cd $CODE && sha256sum registry.R score.R aggregate.R combine.R pair.R a3_flags.R a3_longchain.R) > $n/code_sha256.txt; (cd $n && sha256sum *.csv *.md > outputs_sha256.txt); done
mkdir -p $O/v7_diff
echo "######## diff combined_c050"; Rscript --vanilla $CODE/compare_versions.R --old $O/combined_c050 --new $N5 --out $O/v7_diff/c050
echo "######## diff combined_v3";   Rscript --vanilla $CODE/compare_versions.R --old $O/combined_v3 --new $N1 --out $O/v7_diff/v3
echo "end $(date -u +%FT%TZ)"
