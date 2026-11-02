#!/bin/bash
# Freeze the code into a read-only snapshot with manifest.json (policy §8; master §IV.3.1),
# then submit the 12-task dev-test array from the snapshot. Run on the NOTS login node from
# the code folder:  bash slurm/freeze_and_submit_dev.sh
set -euo pipefail
SRC=/home/fb31/projects/BVS/Benchmarks/F2_ElasticNet
OUTROOT=/projects/ml75/fb31/BVS/bench20261019/dev_test/F2_ElasticNet
DEV=/projects/ml75/fb31/BVS/bench20261019/dev
TS=$(date -u +%Y%m%dT%H%MZ)
RUN_ID=${TS}_bench20261019_F2_devtest
RUN=$OUTROOT/runs/$RUN_ID
mkdir -p "$RUN/code" "$OUTROOT/logs" "$OUTROOT/results"
( cd "$SRC" && cp --parents config.R common.R run_case.R score_dev.R check_outputs.R \
    methods/glmnet_helpers.R methods/fit_F2_enet.R tests/test_F2_enet.R \
    slurm/env.sh slurm/dev_test.slurm "$RUN/code/" )
( cd "$RUN/code" && find . -type f | sort | xargs sha256sum > ../code_sha256.txt )
# Tree hash with run_case.R::code_hashes' convention: sha256 of the lines "<sha256>  <path>"
# for CODE_FILES in that order, joined by newlines, no trailing newline.
TREE=$(cd "$RUN/code" && for f in config.R common.R methods/glmnet_helpers.R methods/fit_F2_enet.R run_case.R; do
         printf '%s  %s\n' "$(sha256sum "$f" | cut -d' ' -f1)" "$f"; done | head -c -1 | sha256sum | cut -d' ' -f1)
source "$RUN/code/slurm/env.sh" >/dev/null 2>&1
MODULES=$(module -t list 2>&1 | grep -v -i "currently loaded" | tr '\n' ' ' | sed 's/ *$//' || true)
BLAS=$(Rscript -e 'cat(extSoftVersion()[["BLAS"]], "|", La_library())' 2>/dev/null || true)
chmod -R a-w "$RUN/code"
CMD="sbatch --parsable --export=ALL,RUN_ID=$RUN_ID,CODE=$RUN/code $RUN/code/slurm/dev_test.slurm"
JOB=$(RUN_ID=$RUN_ID CODE=$RUN/code $CMD)
MANI_SHA=$(sha256sum "$DEV/manifests/dev_inputs_manifest.csv" | awk '{print $1}')
LIB_SHA=$(sha256sum /projects/ml75/fb31/BVS/bench20261019/lib/environment_manifest.txt | awk '{print $1}')
{
  echo "{"
  echo "  \"run_id\": \"$RUN_ID\","
  echo "  \"piece\": \"F2 dev test (12 dev datasets, c100)\","
  echo "  \"code_dir\": \"$RUN/code\","
  echo "  \"code_files_sha256\": ["
  sed 's/^\([0-9a-f]*\)  \(.*\)$/    {"path": "\2", "sha256": "\1"},/' "$RUN/code_sha256.txt" | sed '$ s/,$//'
  echo "  ],"
  echo "  \"source_tree_sha256\": \"$TREE\","
  echo "  \"sbatch_command\": \"$CMD\","
  echo "  \"submit_host\": \"$(hostname)\","
  echo "  \"job_id\": \"$JOB\","
  echo "  \"array\": \"1-12\","
  echo "  \"seeds\": \"method_seed = data_seed + 4000000 from each input file (dev data seeds 2420001..2460001, 2520001..2560001)\","
  echo "  \"modules\": \"$MODULES\","
  echo "  \"blas_lapack\": \"$BLAS\","
  echo "  \"r_lib\": \"/projects/ml75/fb31/BVS/bench20261019/lib/R452\","
  echo "  \"environment_manifest_sha256\": \"$LIB_SHA\","
  echo "  \"inputs\": \"$DEV/inputs/p0500, $DEV/inputs/p1000 (dev_*_S1..S6_r001.rds)\","
  echo "  \"inputs_manifest\": {\"path\": \"$DEV/manifests/dev_inputs_manifest.csv\", \"sha256\": \"$MANI_SHA\"},"
  echo "  \"outputs\": \"$OUTROOT/results/$RUN_ID\","
  echo "  \"logs\": \"$OUTROOT/logs/dev_${JOB}_*.out\","
  echo "  \"submitted_utc\": \"$(date -u +%FT%TZ)\","
  echo "  \"status\": \"submitted\""
  echo "}"
} > "$RUN/manifest.json"
echo "RUN_ID=$RUN_ID JOB=$JOB"
