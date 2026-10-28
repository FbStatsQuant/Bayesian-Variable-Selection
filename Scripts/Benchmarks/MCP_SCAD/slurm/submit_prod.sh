#!/bin/bash
# F4 submission, c050 copy (BRIEF_C050_ENG). Freezes the F4 code copy and the manifests it depends on into a
# read-only snapshot $STUDY/runs/<run_id>/, writes manifest.json, verifies all hashes, and only then submits from
# the snapshot (policy §8; master §IV.3.1).
#   bash slurm/submit_prod.sh --mode prod --time T --mem M [--dry-run]
#        production, scale c050, 400 tasks x 3 datasets, %133, plus the canary job (§IV.3, dev data at c100)
#   bash slurm/submit_prod.sh --mode check [--dry-run]
#        c100 reproduction: task 301 = p1000_S4_r001-r003, then a dependent job compares the outputs with the
#        c = 1 production run (c050tools/compare_c050check.R)
#   bash slurm/submit_prod.sh --mode pilot [--dry-run]
#        c050 pilot: the 12 datasets r001, one per task, then a dependent job writes the diagnostics summary
#        (c050tools/pilot_diag_c050.R)
#   --dry-run : everything except sbatch (snapshot and manifest are written, status "dry-run")
# Retry of missing pairs: bash slurm/clear_stale_locks.sh <run_id>, then resubmit the SAME snapshot and run id
# by hand with the command recorded in manifest.json (the runner skips completed pairs).
set -euo pipefail
DRY=0; MODE=""; TIME=""; MEM=""
while [ $# -gt 0 ]; do case "$1" in
  --dry-run) DRY=1; shift ;; --mode) MODE=$2; shift 2 ;; --time) TIME=$2; shift 2 ;; --mem) MEM=$2; shift 2 ;;
  *) echo "unknown option $1"; exit 2 ;; esac; done
SRC=/home/fb31/projects/BVS/Benchmarks/F4_MCP_SCAD/c050
STUDY=/projects/ml75/fb31/BVS/bench20261019
REF_RUN=20261019T2219Z_bench20261019_prod_F4_MCP_SCAD          # c = 1 production run (reference for check)
PILOT_IDS=p0500_S1_r001:p0500_S2_r001:p0500_S3_r001:p0500_S4_r001:p0500_S5_r001:p0500_S6_r001:p1000_S1_r001:p1000_S2_r001:p1000_S3_r001:p1000_S4_r001:p1000_S5_r001:p1000_S6_r001
TS=$(date -u +%Y%m%dT%H%MZ)
case "$MODE" in
  prod)  RUN_ID=${TS}_bench20261019_prodc050_F4_MCP_SCAD; SCALE=c050; IDS=""; ARR="--array=1-400%133"
         TASKS="400 = 2 p x 200 chunks of 3 datasets (scenario-major order), %133 concurrency"
         [ -n "$TIME" ] && [ -n "$MEM" ] || { echo "--mode prod needs --time and --mem (from the pilot)"; exit 2; } ;;
  check) RUN_ID=${TS}_bench20261019_c050check_F4_MCP_SCAD; SCALE=c100; IDS=""; ARR="--array=301"
         TASKS="task 301 of the production map = p1000_S4_r001-r003, at c100" ;;
  pilot) RUN_ID=${TS}_bench20261019_pilotc050_F4_MCP_SCAD; SCALE=c050; IDS=$PILOT_IDS; ARR="--array=1-12"
         TASKS="12: task t runs the t-th of $IDS" ;;
  *) echo "--mode prod|check|pilot is required"; exit 2 ;;
esac
TIME=${TIME:-00:30:00}; MEM=${MEM:-2G}                          # check/pilot defaults = the c = 1 per-task values
SNAP=$STUDY/runs/$RUN_ID
MAN_IN=$STUDY/manifests/inputs_manifest.csv
LIB_MAN=$STUDY/lib/environment_manifest.txt
[ -f "$MAN_IN" ] || { echo "inputs manifest missing: $MAN_IN"; exit 1; }
[ -f "$LIB_MAN" ] || { echo "environment manifest missing: $LIB_MAN"; exit 1; }
[ ! -e "$STUDY/results/$RUN_ID" ] || { echo "results/$RUN_ID exists"; exit 1; }
mkdir -p "$STUDY/runs" "$STUDY/logs/prod/F4_MCP_SCAD"
mkdir "$SNAP" || { echo "run id already reserved: $SNAP"; exit 1; }     # exclusive reservation (atomic mkdir)
mkdir "$SNAP/code" "$SNAP/frozen"
cp -r "$SRC"/config.R "$SRC"/common.R "$SRC"/run_case.R "$SRC"/score_dev.R "$SRC"/validate_dev.R \
      "$SRC"/compare_canary.R "$SRC"/methods "$SRC"/tests "$SRC"/slurm "$SRC"/c050tools "$SNAP/code/"
cp "$MAN_IN" "$LIB_MAN" "$SNAP/frozen/"
( cd "$SNAP/code" && find . -type f | sort | xargs sha256sum > ../code_sha256.txt )
( cd "$SNAP/frozen" && sha256sum inputs_manifest.csv environment_manifest.txt > ../frozen_sha256.txt )
( cd "$SRC" && sha256sum -c --quiet "$SNAP/code_sha256.txt" ) || { echo "snapshot differs from source"; exit 1; }
cmp -s "$MAN_IN" "$SNAP/frozen/inputs_manifest.csv" && cmp -s "$LIB_MAN" "$SNAP/frozen/environment_manifest.txt" \
  || { echo "frozen manifests differ from the originals"; exit 1; }
chmod -R a-w "$SNAP/code" "$SNAP/frozen"
( cd "$SNAP/code" && sha256sum -c --quiet ../code_sha256.txt ) || { echo "code snapshot hash check failed"; exit 1; }
( cd "$SNAP/frozen" && sha256sum -c --quiet ../frozen_sha256.txt ) || { echo "frozen manifest hash check failed"; exit 1; }
TREE=$(sha256sum "$SNAP/code_sha256.txt" | cut -d' ' -f1)
# C050_SCALE / C050_IDS are set by env on the command itself (overriding the caller's shell); sbatch exports them.
CMD="env C050_SCALE=$SCALE C050_IDS=$IDS sbatch --parsable $ARR --time=$TIME --mem=$MEM $SNAP/code/slurm/prod_array.slurm $SNAP/code $RUN_ID"
if [ "$MODE" = prod ]; then CMD_CANARY="sbatch --parsable $SNAP/code/slurm/canary.slurm $SNAP/code $RUN_ID"; else CMD_CANARY=""; fi
case "$MODE" in
  check) POST="Rscript --vanilla $SNAP/code/c050tools/compare_c050check.R $STUDY/results/$RUN_ID $STUDY/results/$REF_RUN p1000_S4_r001,p1000_S4_r002,p1000_S4_r003 F4,F4_SCAD $STUDY/results/$RUN_ID/c050check_compare.txt" ;;
  pilot) POST="Rscript --vanilla $SNAP/code/c050tools/pilot_diag_c050.R $STUDY/results/$RUN_ID ${IDS//:/,} F4,F4_SCAD c050 100 $STUDY/results/$RUN_ID/pilotc050_diag.txt" ;;
  *) POST="" ;;
esac

write_manifest() {   # $1 status, $2 array job id, $3 canary job id, $4 post job id; written atomically
  cat > "$SNAP/manifest.json.tmp" <<JSON
{
  "run_id": "$RUN_ID",
  "piece": "F4 MCP + F4_SCAD, c050 copy, mode $MODE (scale $SCALE)",
  "code_source": "$SRC (copy of the c = 1 snapshot $STUDY/runs/$REF_RUN/code; diff in $SRC/C050_DIFF.txt)",
  "code_tree_sha256": "$TREE",
  "code_files_sha256": "code_sha256.txt",
  "frozen_files_sha256": "frozen_sha256.txt",
  "scale_key": "$SCALE",
  "command": "$CMD",
  "command_canary": "$CMD_CANARY",
  "post_job": "$( [ -n "$POST" ] && echo "afterany dependent job: $POST" )",
  "submit_host": "$(hostname)",
  "job_id": "$2",
  "canary_job_id": "$3",
  "post_job_id": "$4",
  "tasks": "$TASKS",
  "resources": "partition commons, 1 CPU, --mem=$MEM, --time=$TIME per task; canary job 2G, 30 min",
  "seeds": "method_seed = data_seed + 4000000 (5420001-5470100 at p=500, 5520001-5570100 at p=1000); F4 draws no random numbers",
  "modules": "module purge; GCC/14.3.0; R/4.5.2 (FlexiBLAS/OpenBLAS); OMP/OPENBLAS/MKL threads = 1; Rscript --vanilla",
  "library": "$STUDY/lib/R452",
  "environment_manifest_sha256": "$(sha256sum "$SNAP/frozen/environment_manifest.txt" | cut -d' ' -f1)",
  "inputs": "$STUDY/inputs/p0500|p1000/p*_S*_r*.rds",
  "inputs_manifest": "$SNAP/frozen/inputs_manifest.csv (copy of $MAN_IN)",
  "inputs_manifest_sha256": "$(sha256sum "$SNAP/frozen/inputs_manifest.csv" | cut -d' ' -f1)",
  "canary_reference": "$STUDY/dev_test/F4_MCP_SCAD/results/20261019T2035Z_F4_dev_test (dev_p0500_S4_r001, dev_p1000_S2_r001, dev_p1000_S6_r001)",
  "outputs": "$STUDY/results/$RUN_ID",
  "logs": "$STUDY/logs/prod/F4_MCP_SCAD",
  "written_utc": "$(date -u +%FT%TZ)",
  "status": "$1"
}
JSON
  mv "$SNAP/manifest.json.tmp" "$SNAP/manifest.json"
}

if [ "$DRY" = 1 ]; then write_manifest "dry-run (not submitted)" "-" "-" "-"; echo "$RUN_ID (dry run)"; echo "$CMD"; echo "$CMD_CANARY"; echo "POST: $POST"; exit 0; fi
write_manifest "prepared (submitting)" "-" "-" "-"                       # durable record before sbatch
JOB=$($CMD) || { write_manifest "sbatch of the array FAILED" "-" "-" "-"; exit 1; }
echo "$(date -u +%FT%TZ) array $JOB" >> "$SNAP/submission_receipt.txt"
CJOB="-"
if [ -n "$CMD_CANARY" ]; then
  CJOB=$($CMD_CANARY) || { echo "$(date -u +%FT%TZ) canary sbatch FAILED" >> "$SNAP/submission_receipt.txt"; CJOB="FAILED"; }
  echo "$(date -u +%FT%TZ) canary $CJOB" >> "$SNAP/submission_receipt.txt"
fi
PJOB="-"
if [ -n "$POST" ]; then
  PJOB=$(sbatch --parsable --dependency=afterany:$JOB --job-name=F4_c050post --partition=commons --time=00:15:00 --mem=2G \
    --output=$STUDY/logs/prod/F4_MCP_SCAD/%x_%j.out --wrap "bash -c 'source $SNAP/code/slurm/env.sh && $POST'") || PJOB="FAILED"
  echo "$(date -u +%FT%TZ) post $PJOB" >> "$SNAP/submission_receipt.txt"
fi
write_manifest "submitted" "$JOB" "$CJOB" "$PJOB"
echo "$RUN_ID $JOB $CJOB $PJOB"
echo "$CMD"
