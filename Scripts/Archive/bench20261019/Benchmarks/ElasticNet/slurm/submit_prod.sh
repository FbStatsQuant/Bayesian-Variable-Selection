#!/bin/bash
# F2 production launcher (scale c100 only, decision D3). Run on the NOTS login node from the
# code folder /home/fb31/projects/BVS/Benchmarks/F2_ElasticNet.
#
#   New run:  bash slurm/submit_prod.sh --time HH:MM:SS --mem SIZE [--tasks 1-60] [--dry-run] [--smoke]
#   Resume:   bash slurm/submit_prod.sh --resume <RUN_ID> --time HH:MM:SS --mem SIZE [--tasks 61-120] [--dry-run]
#
# New run: freezes the code, this launcher and the inputs manifest into a read-only snapshot
# $STUDY/runs/<RUN_ID>/, verifies it, writes manifest.json, THEN submits from the snapshot.
# Resume: re-verifies an existing snapshot and submits more tasks into the SAME run id and
# output tree (second wave, or the one infrastructure retry; the runner skips valid outputs).
# --tasks: array range (waves: 1-60 = p 500, 61-120 = p 1000). --smoke: one job, p1000_S4_r001.
# --dry-run: everything except sbatch.
set -euo pipefail
SRC=/home/fb31/projects/BVS/Benchmarks/F2_ElasticNet
STUDY=/projects/ml75/fb31/BVS/bench20261019
DRY=0; SMOKE=0; TIME=""; MEM=""; TASKS="1-120"; RESUME=""
while [ $# -gt 0 ]; do case "$1" in
  --dry-run) DRY=1; shift;; --smoke) SMOKE=1; shift;;
  --time) TIME=$2; shift 2;; --mem) MEM=$2; shift 2;;
  --tasks) TASKS=$2; shift 2;; --resume) RESUME=$2; shift 2;;
  *) echo "unknown argument $1"; exit 2;; esac; done
[ -n "$TIME" ] && [ -n "$MEM" ] || { echo "--time and --mem are required"; exit 2; }
[[ "$TASKS" =~ ^[0-9]+(-[0-9]+)?$ ]] || { echo "bad --tasks $TASKS"; exit 2; }
T_LO=${TASKS%-*}; T_HI=${TASKS#*-}
[ "$T_LO" -ge 1 ] && [ "$T_LO" -le "$T_HI" ] && [ "$T_HI" -le 120 ] || { echo "--tasks must satisfy 1 <= start <= end <= 120"; exit 2; }

if [ -z "$RESUME" ]; then
  TS=$(date -u +%Y%m%dT%H%MZ)
  if [ $SMOKE = 1 ]; then RUN_ID=${TS}_bench20261019_prodsmoke_F2_ElasticNet; else RUN_ID=${TS}_bench20261019_prod_F2_ElasticNet; fi
  RUN=$STUDY/runs/$RUN_ID
  [ ! -e "$RUN" ] || { echo "run dir exists: $RUN"; exit 2; }
  mkdir -p "$RUN/code" "$STUDY/logs/prod/F2_ElasticNet" "$STUDY/results"
  ( cd "$SRC" && cp --parents config.R common.R run_case.R methods/glmnet_helpers.R methods/fit_F2_enet.R \
      check_outputs.R slurm/env.sh slurm/prod.slurm slurm/submit_prod.sh "$RUN/code/" )
  cp "$STUDY/manifests/inputs_manifest.csv" "$RUN/inputs_manifest.csv"        # frozen copy used by the tasks
  cp "$STUDY/lib/environment_manifest.txt" "$RUN/environment_manifest.txt"
  ( cd "$RUN/code" && find . -type f | sort | xargs sha256sum > ../code_sha256.txt )
  ( cd "$RUN" && sha256sum inputs_manifest.csv environment_manifest.txt > frozen_sha256.txt )
  chmod -R a-w "$RUN/code" "$RUN/inputs_manifest.csv" "$RUN/environment_manifest.txt" "$RUN/code_sha256.txt" "$RUN/frozen_sha256.txt"
  for f in config.R common.R run_case.R methods/glmnet_helpers.R methods/fit_F2_enet.R slurm/prod.slurm slurm/env.sh slurm/submit_prod.sh; do
    cmp -s "$SRC/$f" "$RUN/code/$f" || { echo "snapshot differs from source: $f"; exit 3; }; done
else
  RUN_ID=$RESUME; RUN=$STUDY/runs/$RUN_ID
  [ -d "$RUN/code" ] || { echo "no snapshot for $RUN_ID"; exit 2; }
  case "$RUN_ID" in *prodsmoke*) SMOKE=1;; esac
  # Stale lock directories (left by a killed task) block their case; clear them only when no
  # F2 production task is queued or running.
  Q=$(squeue -h -u "$USER" -n F2_prod) || { echo "squeue failed; not touching locks"; exit 3; }
  if [ -n "$Q" ]; then echo "F2_prod jobs still queued/running; not resuming"; exit 3; fi
  if [ $DRY = 0 ]; then find "$STUDY/results/$RUN_ID" -maxdepth 3 -type d -name '*.lock' -print -exec rm -r {} + 2>/dev/null || true; fi
fi

# Verify the snapshot and frozen manifests before any submission.
( cd "$RUN/code" && sha256sum -c --quiet ../code_sha256.txt ) || { echo "snapshot hash mismatch"; exit 3; }
( cd "$RUN" && sha256sum -c --quiet frozen_sha256.txt ) || { echo "frozen manifest hash mismatch"; exit 3; }
TREE=$(cd "$RUN/code" && for f in config.R common.R methods/glmnet_helpers.R methods/fit_F2_enet.R run_case.R; do
         printf '%s  %s\n' "$(sha256sum "$f" | cut -d' ' -f1)" "$f"; done | head -c -1 | sha256sum | cut -d' ' -f1)

if [ $SMOKE = 1 ]; then ARRAY=""; EXPORT="ALL,RUN_ID=$RUN_ID,CODE=$RUN/code,SMOKE=1"; else ARRAY="--array=$TASKS%60"; EXPORT="ALL,RUN_ID=$RUN_ID,CODE=$RUN/code"; fi
CMD="sbatch --parsable $ARRAY --time=$TIME --mem=$MEM --export=$EXPORT $RUN/code/slurm/prod.slurm"

if [ -z "$RESUME" ]; then
  source "$RUN/code/slurm/env.sh" >/dev/null 2>&1
  MODULES=$(module -t list 2>&1 | grep -v -i "currently loaded" | tr '\n' ' ' | sed 's/ *$//' || true)
  BLAS=$(Rscript -e 'cat(extSoftVersion()[["BLAS"]], "|", La_library())' 2>/dev/null || true)
  {
    echo "{"
    echo "  \"run_id\": \"$RUN_ID\","
    echo "  \"piece\": \"F2 Elastic net production, scale c100 (D3)$( [ $SMOKE = 1 ] && echo ', SMOKE TEST p1000_S4_r001' )\","
    echo "  \"code_dir\": \"$RUN/code\","
    echo "  \"code_files_sha256\": ["
    sed 's/^\([0-9a-f]*\)  \(.*\)$/    {"path": "\2", "sha256": "\1"},/' "$RUN/code_sha256.txt" | sed '$ s/,$//'
    echo "  ],"
    echo "  \"source_tree_sha256\": \"$TREE\","
    echo "  \"tasks\": \"1-60 p=500, 61-120 p=1000; 10 datasets of one scenario per task; submissions in submissions.log\","
    echo "  \"seeds\": \"method_seed = data_seed + 4000000 read from each input file (data_seed 1410000/1510000 + 10000 s + r)\","
    echo "  \"r_lib\": \"$STUDY/lib/R452\","
    echo "  \"environment_manifest\": {\"frozen_copy\": \"$RUN/environment_manifest.txt\", \"sha256\": \"$(sha256sum $RUN/environment_manifest.txt | cut -d' ' -f1)\"},"
    echo "  \"modules\": \"$MODULES\","
    echo "  \"blas_lapack\": \"$BLAS\","
    echo "  \"inputs\": \"$STUDY/inputs/p0500, $STUDY/inputs/p1000\","
    echo "  \"inputs_manifest\": {\"source\": \"$STUDY/manifests/inputs_manifest.csv\", \"frozen_copy\": \"$RUN/inputs_manifest.csv\", \"sha256\": \"$(sha256sum $RUN/inputs_manifest.csv | cut -d' ' -f1)\"},"
    echo "  \"outputs\": \"$STUDY/results/$RUN_ID\","
    echo "  \"logs\": \"$STUDY/logs/prod/F2_ElasticNet/\","
    echo "  \"frozen_utc\": \"$(date -u +%FT%TZ)\""
    echo "}"
  } > "$RUN/manifest.json"
  chmod a-w "$RUN/manifest.json"
fi

# Submission intent first, then the job id (append-only log next to the manifest).
echo "$(date -u +%FT%TZ) intent tasks=$TASKS dry_run=$DRY cmd=$CMD" >> "$RUN/submissions.log"
if [ $DRY = 1 ]; then JOB="dry-run"; else JOB=$($CMD); fi
echo "$(date -u +%FT%TZ) submitted job=$JOB tasks=$TASKS" >> "$RUN/submissions.log"
echo "RUN_ID=$RUN_ID JOB=$JOB TREE=$TREE"
echo "CMD=$CMD"
