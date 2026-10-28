#!/usr/bin/env bash
# Freezes the F1 c050 code copy into a read-only snapshot $STUDY/runs/<run_id>/code with code.sha256 and manifest.json,
# verifies it, then submits from the snapshot. Run on the NOTS login node.
#   bash submit_prod.sh --mode prod  --time T --mem M [--dry-run]   production c050: 400 tasks x 3 datasets, %133
#   bash submit_prod.sh --mode check [--time T] [--mem M] [--dry-run] c100 reproduction: task 301 = p1000_S4_r001-r003,
#        then a dependent job compares the outputs with the c = 1 production run (c050tools/compare_c050check.R)
#   bash submit_prod.sh --mode pilot [--time T] [--mem M] [--dry-run] c050 pilot: the 12 datasets r001, one per task,
#        then a dependent job writes the diagnostics summary (c050tools/pilot_diag_c050.R)
#   --dry-run: everything except sbatch (snapshot and manifest are written; prints the sbatch command)
set -euo pipefail
MODE=""; TIME=""; MEM=""; DRY=0
while [[ $# -gt 0 ]]; do case "$1" in
  --mode) MODE=${2:?}; shift 2;; --time) TIME=${2:?}; shift 2;; --mem) MEM=${2:?}; shift 2;;
  --dry-run) DRY=1; shift;; *) echo "usage: see header of $0" >&2; exit 2;; esac; done
source /home/fb31/projects/BVS/Benchmarks/F1_Lasso/c050/slurm/env.sh
F1_CODE=/home/fb31/projects/BVS/Benchmarks/F1_Lasso/c050       # the c050 copy (env.sh points to the c = 1 folder)
REF_RUN=20261019T2308Z_bench20261019_prod_F1_Lasso               # c = 1 production run (reference for --mode check)
PILOT_IDS=p0500_S1_r001:p0500_S2_r001:p0500_S3_r001:p0500_S4_r001:p0500_S5_r001:p0500_S6_r001:p1000_S1_r001:p1000_S2_r001:p1000_S3_r001:p1000_S4_r001:p1000_S5_r001:p1000_S6_r001
STAMP=$(date -u +%Y%m%dT%H%MZ)
case "$MODE" in
  prod)  RUN_ID=${STAMP}_bench20261019_prodc050_F1_Lasso; SCALE=c050; IDS=""; ARRAY="1-400%133"
         [[ -n "$TIME" && -n "$MEM" ]] || { echo "--mode prod needs --time and --mem (from the pilot)" >&2; exit 2; } ;;
  check) RUN_ID=${STAMP}_bench20261019_c050check_F1_Lasso; SCALE=c100; IDS=""; ARRAY="301" ;;
  pilot) RUN_ID=${STAMP}_bench20261019_pilotc050_F1_Lasso; SCALE=c050; IDS=$PILOT_IDS; ARRAY="1-12" ;;
  *) echo "--mode prod|check|pilot is required" >&2; exit 2 ;;
esac
TIME=${TIME:-01:15:00}; MEM=${MEM:-2G}                           # check/pilot defaults = the c = 1 per-task values
SNAP=$STUDY/runs/$RUN_ID; CODE=$SNAP/code
[[ ! -e "$SNAP" && ! -e "$STUDY/results/$RUN_ID" ]] || { echo "exists: $SNAP or results/$RUN_ID" >&2; exit 2; }
[[ -f "$STUDY/manifests/inputs_manifest.csv" ]] || { echo "missing production inputs manifest" >&2; exit 2; }
mkdir -p "$CODE" "$STUDY/logs/prod/F1_Lasso"
( cd "$F1_CODE" && cp -r config.R common.R run_case.R check_outputs.R score_dev.R reconcile_prod.R verify_library.R methods tests slurm c050tools "$CODE/" )
cp "$STUDY/manifests/inputs_manifest.csv" "$STUDY/lib/environment_manifest.txt" "$SNAP/"
( cd "$SNAP" && sha256sum inputs_manifest.csv environment_manifest.txt > frozen_manifests.sha256 )
chmod a-w "$SNAP/inputs_manifest.csv" "$SNAP/environment_manifest.txt" "$SNAP/frozen_manifests.sha256"
( cd "$CODE" && find . -type f | sort | xargs sha256sum > ../code.sha256 )
( cd "$F1_CODE" && sha256sum -c --quiet "$SNAP/code.sha256" )      # snapshot equals the source tree
chmod -R a-w "$CODE"; chmod a-w "$SNAP/code.sha256"
( cd "$CODE" && sha256sum -c --quiet ../code.sha256 )
TREE=$(sha256sum "$SNAP/code.sha256" | cut -d' ' -f1)
CMD="env C050_SCALE=$SCALE C050_IDS=$IDS sbatch --parsable --array=$ARRAY --time=$TIME --mem=$MEM $CODE/slurm/prod.slurm $CODE $RUN_ID"
case "$MODE" in
  check) POST="Rscript --vanilla $CODE/c050tools/compare_c050check.R $STUDY/results/$RUN_ID $STUDY/results/$REF_RUN p1000_S4_r001,p1000_S4_r002,p1000_S4_r003 F1 $STUDY/results/$RUN_ID/c050check_compare.txt" ;;
  pilot) POST="Rscript --vanilla $CODE/c050tools/pilot_diag_c050.R $STUDY/results/$RUN_ID ${IDS//:/,} F1 c050 100 $STUDY/results/$RUN_ID/pilotc050_diag.txt" ;;
  *) POST="" ;;
esac
POST_SBATCH="sbatch --parsable --dependency=afterany:<job> --job-name=F1_c050post --partition=commons --time=00:15:00 --mem=2G --output=$STUDY/logs/prod/F1_Lasso/%x_%j.out --wrap"
# the launch record is written BEFORE sbatch; the job id is filled in after submission
JOB="pending"; PJOB=""; [[ "$DRY" == 1 ]] && JOB="(dry run: not submitted)"
write_manifest() {
cat > "$SNAP/manifest.json.tmp" <<JSON
{
  "run_id": "$RUN_ID",
  "piece": "F1 Lasso, c050 copy, mode $MODE (scale $SCALE)",
  "created_utc": "$(date -u +%FT%TZ)",
  "host_submit": "$(hostname)",
  "code_source": "$F1_CODE (copy of the c = 1 snapshot $STUDY/runs/$REF_RUN/code; diff in $F1_CODE/C050_DIFF.txt)",
  "code_dir": "$CODE",
  "code_sha256_list": "$SNAP/code.sha256",
  "code_tree_sha256": "$TREE",
  "sbatch_command": "$CMD",
  "job_id": "$JOB",
  "post_job_command": "$POST_SBATCH \"bash -c 'source $CODE/slurm/env.sh && $POST'\"",
  "post_job_id": "$PJOB",
  "scale_key": "$SCALE",
  "tasks": "$(case $MODE in prod) echo '1-400 (%133): t<=200 p=500, else p=1000; u=(t-1)%200; datasets i=3u..3u+2 of the scenario-major order (S=i/100+1, r=i%100+1)';; check) echo 'task 301 of the production map = p1000_S4_r001-r003, at c100';; pilot) echo "1-12: task t runs the t-th of $IDS";; esac)",
  "time": "$TIME", "mem": "$MEM",
  "seeds": "method_seed = data_seed + 4000000 from each input file (p500: 5420001-5470100; p1000: 5520001-5570100); F1 draws no random numbers",
  "modules": "GCC/14.3.0 R/4.5.2",
  "study_library": "$BENCH_LIB",
  "library_manifest_sha256": "$(sha256sum "$SNAP/environment_manifest.txt" | cut -d' ' -f1) (frozen copy in the run folder)",
  "inputs": "$STUDY/inputs/p0500, $STUDY/inputs/p1000",
  "inputs_manifest": "$SNAP/inputs_manifest.csv (frozen copy of $STUDY/manifests/inputs_manifest.csv)",
  "inputs_manifest_sha256": "$(sha256sum "$SNAP/inputs_manifest.csv" | cut -d' ' -f1)",
  "outputs": "$STUDY/results/$RUN_ID",
  "logs": "$STUDY/logs/prod/F1_Lasso",
  "rerun": "resubmit the same sbatch_command; the runner skips cases with a verified .done",
  "status": "$1"
}
JSON
mv "$SNAP/manifest.json.tmp" "$SNAP/manifest.json"
}
write_manifest "$([[ $DRY == 1 ]] && echo 'dry run' || echo submitting)"
if [[ "$DRY" != 1 ]]; then
  JOB=$($CMD) || { write_manifest "sbatch failed"; echo "sbatch failed" >&2; exit 5; }
  write_manifest "submitted"
  if [[ -n "$POST" ]]; then
    PJOB=$(sbatch --parsable --dependency=afterany:$JOB --job-name=F1_c050post --partition=commons --time=00:15:00 --mem=2G \
      --output=$STUDY/logs/prod/F1_Lasso/%x_%j.out --wrap "bash -c 'source $CODE/slurm/env.sh && $POST'") || PJOB="sbatch failed"
    write_manifest "submitted"
  fi
fi
echo "RUN_ID $RUN_ID"; echo "SNAPSHOT $CODE"; echo "TREE $TREE"; echo "MANIFEST $SNAP/manifest.json"; echo "CMD $CMD"; echo "JOB $JOB"
[[ -n "$POST" ]] && echo "POST $POST" && echo "POST_JOB $PJOB"
exit 0
