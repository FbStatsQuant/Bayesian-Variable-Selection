#!/bin/bash
#SBATCH --job-name=S_score
#SBATCH --partition=commons
#SBATCH --cpus-per-task=1
#SBATCH --mem=4G
#SBATCH --time=01:00:00
#SBATCH --output=/projects/ml75/fb31/BVS/bench20261019/scoring/logs/%x_%j.out
#
# Scoring job (thread S). Arguments: a list of tasks, each one of
#   tests                        unit tests on fixtures
#   dev:<method folder>:<method ids comma-separated>   score + aggregate the latest dev run of a method
#   prod:<run_id>                score + aggregate one production run
set -euo pipefail
S=/projects/ml75/fb31/BVS/bench20261019
CODE=$S/scoring/code
module load GCC/14.3.0 R/4.5.2 >/dev/null 2>&1
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
echo "host $(hostname) job ${SLURM_JOB_ID:-none} start $(date -u +%FT%TZ)"
R --version | head -1
echo "== code sha256"; (cd $CODE && sha256sum registry.R score.R aggregate.R combine.R pair.R a3_flags.R a3_longchain.R score_derived.R tests/test_scoring.R slurm/score_job.slurm)

for task in "$@"; do
  echo; echo "######## $task  $(date -u +%FT%TZ)"
  case $task in
    tests)
      Rscript --vanilla $CODE/tests/test_scoring.R ;;
    dev:*)
      folder=$(echo $task | cut -d: -f2); methods=$(echo $task | cut -d: -f3)
      head -2 $S/dev/manifests/dev_inputs_manifest.csv | cut -c1-200; head -2 $S/dev/manifests/dev_truth_manifest.csv | cut -c1-200
      run=$(ls -d $S/dev_test/$folder/results/* | tail -1)
      out=$S/scoring/out/dev/$folder/$(basename $run)
      Rscript --vanilla $CODE/score.R --results $run --manifest $S/dev/manifests/dev_inputs_manifest.csv \
        --truth $S/dev/truth --truth-manifest $S/dev/manifests/dev_truth_manifest.csv --out $out \
        --methods $methods --expect dev || { echo "score failed for $task"; continue; }
      Rscript --vanilla $CODE/aggregate.R --dir $out || echo "aggregate failed for $task"
      (cd $CODE && sha256sum registry.R score.R aggregate.R) > $out/code_sha256.txt ;;
    prod:*)
      run_id=${task#prod:}
      out=$S/scoring/out/$run_id
      Rscript --vanilla $CODE/score.R --results $S/results/$run_id --manifest $S/manifests/inputs_manifest.csv \
        --truth $S/truth_scoring --truth-manifest $S/truth_scoring/truth_manifest.csv --out $out --expect prod
      Rscript --vanilla $CODE/aggregate.R --dir $out
      (cd $CODE && sha256sum registry.R score.R aggregate.R) > $out/code_sha256.txt
      (cd $out && sha256sum *.csv summary.md > outputs_sha256.txt) ;;
    combine)
      # The eight production runs, one per method folder (all must already be scored).
      out=$S/scoring/out/combined
      runs=$(ls -d $S/scoring/out/*_prod_{F1_Lasso,F2_ElasticNet,F3_AdaptiveLasso,F4_MCP_SCAD,F5_ABESS,A1_SuSiE,A2_SSL,A3_Horseshoe})
      echo "$runs"; [ $(echo "$runs" | wc -l) -eq 8 ] || { echo "combine: expected 8 scored runs"; exit 1; }
      Rscript --vanilla $CODE/combine.R --out $out $runs
      (cd $CODE && sha256sum registry.R score.R aggregate.R combine.R score_derived.R) > $out/code_sha256.txt
      (cd $out && sha256sum *.csv *.md > outputs_sha256.txt) ;;
    run:*)
      # run:<outroot>:<run_id>  score + aggregate with the scale read from the run and, when the derived
      # file exists, the derived rows merged; outputs in $S/scoring/out/<outroot>/runs/<run_id>/.
      outroot=$(echo $task | cut -d: -f2); run_id=$(echo $task | cut -d: -f3)
      scale=$(echo $task | cut -d: -f4); [ -n "$scale" ] || scale=auto     # optional 4th field: c100 / c050
      out=$S/scoring/out/$outroot/runs/$run_id
      der=$S/derived/$run_id/derived_rules/derived_rule_rows.csv
      dopt=""; [ -f $der ] && dopt="--derived $der"
      Rscript --vanilla $CODE/score.R --results $S/results/$run_id --manifest $S/manifests/inputs_manifest.csv         --truth $S/truth_scoring --truth-manifest $S/truth_scoring/truth_manifest.csv --out $out --expect prod --scale $scale $dopt
      Rscript --vanilla $CODE/aggregate.R --dir $out
      (cd $CODE && sha256sum registry.R score.R aggregate.R) > $out/code_sha256.txt
      (cd $out && sha256sum *.csv summary.md > outputs_sha256.txt) ;;
    combine_out:*)
      # combine_out:<outroot>  combine every scored run under $S/scoring/out/<outroot>/runs/.
      outroot=${task#combine_out:}; out=$S/scoring/out/$outroot
      runs=$(ls -d $out/runs/*); echo "$runs"
      Rscript --vanilla $CODE/combine.R --out $out $runs
      (cd $CODE && sha256sum registry.R score.R aggregate.R combine.R) > $out/code_sha256.txt
      (cd $out && sha256sum *.csv *.md > outputs_sha256.txt) ;;
    pair:*)
      # pair:<outroot c = 0.5>:<outroot c = 1>  paired exact recovery on the same datasets.
      o5=$(echo $task | cut -d: -f2); o1=$(echo $task | cut -d: -f3)
      Rscript --vanilla $CODE/pair.R --c050 $S/scoring/out/$o5/runs --c100 $S/scoring/out/$o1/runs --out $S/scoring/out/$o5
      (cd $S/scoring/out/$o5 && sha256sum paired_c100_c050.csv paired_c100_c050.md >> outputs_sha256.txt) ;;
    a3flags:*)
      # a3flags:<outroot c050>:<outroot c100>  ESS-flag listing and all vs passing counts for A3 (PREREG R6).
      o5=$(echo $task | cut -d: -f2); o1=$(echo $task | cut -d: -f3)
      Rscript --vanilla $CODE/a3_flags.R --c050 $(ls -d $S/scoring/out/$o5/runs/*_A3_Horseshoe)         --c100 $(ls -d $S/scoring/out/$o1/runs/*_A3_Horseshoe) --out $S/scoring/out/$o5
      (cd $S/scoring/out/$o5 && sha256sum A3_ess_flagged_cases.csv A3_ess_flags_by_cell.csv >> outputs_sha256.txt) ;;
    a3long:*)
      # a3long:<long c050 run id>:<long c100 run id>  A3 8x long-chain sensitivity (PREREG R6), into combined_c050.
      l5=$(echo $task | cut -d: -f2); l1=$(echo $task | cut -d: -f3); o=$S/scoring/out/combined_c050
      Rscript --vanilla $CODE/a3_longchain.R --long050 $S/results/$l5 --long100 $S/results/$l1         --prod050 $(ls -d $o/runs/*_A3_Horseshoe) --prod100 $(ls -d $S/scoring/out/combined_v3/runs/*_A3_Horseshoe)         --manifest $S/manifests/inputs_manifest.csv --truth $S/truth_scoring --truth-manifest $S/truth_scoring/truth_manifest.csv --out $o
      (cd $o && sha256sum A3_longchain_sensitivity.csv A3_longchain_sensitivity.md A3_longchain_per_case.csv A3_longchain_problems.csv >> outputs_sha256.txt) ;;
    posthoc:*)
      # posthoc:<run_id>:<derived CSV file name>:<rule>:<methods comma-separated>
      run_id=$(echo $task | cut -d: -f2); csv=$(echo $task | cut -d: -f3)
      rule=$(echo $task | cut -d: -f4); methods=$(echo $task | cut -d: -f5)
      ddir=$S/derived/$run_id; out=$S/scoring/out/$run_id/posthoc_$rule
      echo "== derived SHA256SUMS check"; (cd $ddir && sha256sum -c SHA256SUMS) || echo "SHA256SUMS check reported a failure"
      Rscript --vanilla $CODE/score_derived.R --derived $ddir/$csv --prod-out $S/scoring/out/$run_id \
        --manifest $S/manifests/inputs_manifest.csv --truth $S/truth_scoring \
        --truth-manifest $S/truth_scoring/truth_manifest.csv --out $out --rule $rule --role S0_posthoc --cap 37 \
        --methods $methods
      (cd $CODE && sha256sum registry.R score.R aggregate.R score_derived.R) > $out/code_sha256.txt
      (cd $out && sha256sum *.csv summary_posthoc.md > outputs_sha256.txt) ;;
  esac
done
echo "end $(date -u +%FT%TZ)"
