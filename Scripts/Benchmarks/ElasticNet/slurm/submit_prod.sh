#!/bin/bash
# F2 launcher, c050 copy (BRIEF_C050_ENG). Run on the NOTS login node; code folder
# /home/fb31/projects/BVS/Benchmarks/F2_ElasticNet/c050 (copy of the c = 1 production snapshot).
#
#   New run:  bash slurm/submit_prod.sh --mode prod|check|pilot [--time HH:MM:SS] [--mem SIZE] [--tasks A-B] [--dry-run]
#   Resume:   bash slurm/submit_prod.sh --resume <RUN_ID> --time HH:MM:SS --mem SIZE [--tasks A-B] [--dry-run]
#
# Modes: prod  = scale c050, 400 tasks x 3 datasets, %133 (--time and --mem required, from the pilot);
#        check = scale c100, task 301 = p1000_S4_r001-r003, then a dependent job compares the outputs with
#                the c = 1 production run (c050tools/compare_c050check.R);
#        pilot = scale c050, the 12 datasets r001 (one per task, C050_IDS), then a dependent job writes the
#                diagnostics summary (c050tools/pilot_diag_c050.R).
# New run: freezes the code, this launcher and the inputs manifest into a read-only snapshot
# $STUDY/runs/<RUN_ID>/, verifies it, writes manifest.json, THEN submits from the snapshot.
# Resume: re-verifies an existing snapshot and submits more tasks into the SAME run id and
# output tree (the one infrastructure retry; the runner skips valid outputs).
# --dry-run: everything except sbatch.
set -euo pipefail
SRC=/home/fb31/projects/BVS/Benchmarks/F2_ElasticNet/c050
STUDY=/projects/ml75/fb31/BVS/bench20261019
REF_RUN=20261019T2232Z_bench20261019_prod_F2_ElasticNet       # c = 1 production run (reference for check)
PILOT_IDS=p0500_S1_r001:p0500_S2_r001:p0500_S3_r001:p0500_S4_r001:p0500_S5_r001:p0500_S6_r001:p1000_S1_r001:p1000_S2_r001:p1000_S3_r001:p1000_S4_r001:p1000_S5_r001:p1000_S6_r001
DRY=0; MODE=""; TIME=""; MEM=""; TASKS=""; RESUME=""
while [ $# -gt 0 ]; do case "$1" in
  --dry-run) DRY=1; shift;; --mode) MODE=$2; shift 2;;
  --time) TIME=$2; shift 2;; --mem) MEM=$2; shift 2;;
  --tasks) TASKS=$2; shift 2;; --resume) RESUME=$2; shift 2;;
  *) echo "unknown argument $1"; exit 2;; esac; done
if [ -n "$RESUME" ]; then
  case "$RESUME" in *_prodc050_*) MODE=prod;; *_c050check_*) MODE=check;; *_pilotc050_*) MODE=pilot;;
    *) echo "not a c050 run id: $RESUME"; exit 2;; esac
fi
case "$MODE" in
  prod)  SCALE=c050; IDS=""; TMAX=400; CONC="%133"; LABEL=prodc050
         [ -n "$TIME" ] && [ -n "$MEM" ] || { echo "--mode prod needs --time and --mem (from the pilot)"; exit 2; } ;;
  check) SCALE=c100; IDS=""; TMAX=400; CONC=""; LABEL=c050check; TASKS=${TASKS:-301} ;;
  pilot) SCALE=c050; IDS=$PILOT_IDS; TMAX=12; CONC=""; LABEL=pilotc050 ;;
  *) echo "--mode prod|check|pilot is required"; exit 2 ;;
esac
[ -n "$RESUME" ] && { [ -n "$TIME" ] && [ -n "$MEM" ] || { echo "--resume needs --time and --mem"; exit 2; }; }
TIME=${TIME:-05:00:00}; MEM=${MEM:-2G}                          # check/pilot defaults = the c = 1 per-task values
TASKS=${TASKS:-1-$TMAX}
[[ "$TASKS" =~ ^[0-9]+(-[0-9]+)?$ ]] || { echo "bad --tasks $TASKS"; exit 2; }
T_LO=${TASKS%-*}; T_HI=${TASKS#*-}
[ "$T_LO" -ge 1 ] && [ "$T_LO" -le "$T_HI" ] && [ "$T_HI" -le $TMAX ] || { echo "--tasks must satisfy 1 <= start <= end <= $TMAX"; exit 2; }

if [ -z "$RESUME" ]; then
  TS=$(date -u +%Y%m%dT%H%MZ)
  RUN_ID=${TS}_bench20261019_${LABEL}_F2_ElasticNet
  RUN=$STUDY/runs/$RUN_ID
  [ ! -e "$RUN" ] && [ ! -e "$STUDY/results/$RUN_ID" ] || { echo "run dir exists: $RUN"; exit 2; }
  mkdir -p "$RUN/code" "$STUDY/logs/prod/F2_ElasticNet" "$STUDY/results"
  ( cd "$SRC" && cp --parents config.R common.R run_case.R methods/glmnet_helpers.R methods/fit_F2_enet.R \
      check_outputs.R slurm/env.sh slurm/prod.slurm slurm/submit_prod.sh \
      c050tools/compare_c050check.R c050tools/pilot_diag_c050.R "$RUN/code/" )
  cp "$STUDY/manifests/inputs_manifest.csv" "$RUN/inputs_manifest.csv"        # frozen copy used by the tasks
  cp "$STUDY/lib/environment_manifest.txt" "$RUN/environment_manifest.txt"
  ( cd "$RUN/code" && find . -type f | sort | xargs sha256sum > ../code_sha256.txt )
  ( cd "$RUN" && sha256sum inputs_manifest.csv environment_manifest.txt > frozen_sha256.txt )
  chmod -R a-w "$RUN/code" "$RUN/inputs_manifest.csv" "$RUN/environment_manifest.txt" "$RUN/code_sha256.txt" "$RUN/frozen_sha256.txt"
  for f in config.R common.R run_case.R methods/glmnet_helpers.R methods/fit_F2_enet.R slurm/prod.slurm slurm/env.sh slurm/submit_prod.sh \
           c050tools/compare_c050check.R c050tools/pilot_diag_c050.R; do
    cmp -s "$SRC/$f" "$RUN/code/$f" || { echo "snapshot differs from source: $f"; exit 3; }; done
else
  RUN_ID=$RESUME; RUN=$STUDY/runs/$RUN_ID
  [ -d "$RUN/code" ] || { echo "no snapshot for $RUN_ID"; exit 2; }
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

# C050_SCALE / C050_IDS reach the job through the environment (sbatch --export=ALL); they are set explicitly
# by env on the command, so values inherited from the caller's shell are overridden.
CMD="env C050_SCALE=$SCALE C050_IDS=$IDS sbatch --parsable --array=$TASKS$CONC --time=$TIME --mem=$MEM --export=ALL,RUN_ID=$RUN_ID,CODE=$RUN/code $RUN/code/slurm/prod.slurm"
case "$MODE" in
  check) POST="Rscript --vanilla $RUN/code/c050tools/compare_c050check.R $STUDY/results/$RUN_ID $STUDY/results/$REF_RUN p1000_S4_r001,p1000_S4_r002,p1000_S4_r003 F2 $STUDY/results/$RUN_ID/c050check_compare.txt" ;;
  pilot) POST="Rscript --vanilla $RUN/code/c050tools/pilot_diag_c050.R $STUDY/results/$RUN_ID ${IDS//:/,} F2 c050 100 $STUDY/results/$RUN_ID/pilotc050_diag.txt" ;;
  *) POST="" ;;
esac
[ -n "$RESUME" ] && POST=""

if [ -z "$RESUME" ]; then
  source "$RUN/code/slurm/env.sh" >/dev/null 2>&1
  MODULES=$(module -t list 2>&1 | grep -v -i "currently loaded" | tr '\n' ' ' | sed 's/ *$//' || true)
  BLAS=$(Rscript -e 'cat(extSoftVersion()[["BLAS"]], "|", La_library())' 2>/dev/null || true)
  {
    echo "{"
    echo "  \"run_id\": \"$RUN_ID\","
    echo "  \"piece\": \"F2 Elastic net, c050 copy, mode $MODE (scale $SCALE)\","
    echo "  \"code_source\": \"$SRC (copy of the c = 1 snapshot $STUDY/runs/$REF_RUN/code; diff in $SRC/C050_DIFF.txt)\","
    echo "  \"code_dir\": \"$RUN/code\","
    echo "  \"code_files_sha256\": ["
    sed 's/^\([0-9a-f]*\)  \(.*\)$/    {"path": "\2", "sha256": "\1"},/' "$RUN/code_sha256.txt" | sed '$ s/,$//'
    echo "  ],"
    echo "  \"source_tree_sha256\": \"$TREE\","
    echo "  \"scale_key\": \"$SCALE\","
    echo "  \"command\": \"$CMD\","
    echo "  \"post_job\": \"$( [ -n "$POST" ] && echo "afterany dependent job: $POST" )\","
    echo "  \"tasks\": \"$(case $MODE in prod) echo '1-400 %133: t<=200 p=500, else p=1000; u=(t-1)%200; datasets i=3u..3u+2 of the scenario-major order (S=i/100+1, r=i%100+1)';; check) echo 'task 301 of the production map = p1000_S4_r001-r003, at c100';; pilot) echo "1-12: task t runs the t-th of $IDS";; esac); submissions in submissions.log\","
    echo "  \"time\": \"$TIME\", \"mem\": \"$MEM\","
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
PJOB=""
if [ -n "$POST" ] && [ $DRY = 0 ]; then
  PJOB=$(sbatch --parsable --dependency=afterany:$JOB --job-name=F2_c050post --partition=commons --time=00:15:00 --mem=2G \
    --output=$STUDY/logs/prod/F2_ElasticNet/%x_%j.out --wrap "bash -c 'source $RUN/code/slurm/env.sh && $POST'") || PJOB="sbatch failed"
  echo "$(date -u +%FT%TZ) post job=$PJOB (afterany:$JOB) cmd=$POST" >> "$RUN/submissions.log"
fi
echo "RUN_ID=$RUN_ID JOB=$JOB TREE=$TREE POST_JOB=$PJOB"
echo "CMD=$CMD"
