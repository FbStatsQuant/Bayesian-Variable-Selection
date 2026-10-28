#!/bin/bash
# F3 production array, c050 copy (BRIEF_C050_ENG): 400 tasks x 3 datasets of one p.
# Task t = 1..200 -> p = 500, t = 201..400 -> p = 1000; within a p, u = (t - 1) mod 200 and dataset j = 0..2
# of the task is index i = 3u + j of the c = 1 order (scenario-major, replicate 1..100): S = i/100 + 1, r = i mod 100 + 1.
# Scale key: C050_SCALE (default c100). If C050_IDS is set (dataset ids separated by ':'), task t runs only the t-th
# id of the list (pilot).
# Submitted only by slurm/submit_prod.sh, which sets RUN_ID, CODE (frozen snapshot), RUNDIR,
# STATUS, C050_SCALE and C050_IDS and passes the resources on the sbatch command line.
# The runner skips (case, method) pairs that already have a valid result of this run; the task
# fails unless every expected case ends with a .done file.
#SBATCH --job-name=F3_prod
#SBATCH --partition=commons
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
set -eo pipefail
: "${RUN_ID:?RUN_ID not set}" "${CODE:?CODE not set}" "${RUNDIR:?RUNDIR not set}" "${STATUS:?STATUS not set}"
t=$SLURM_ARRAY_TASK_ID
TAG="$STATUS/task_$(printf %03d "$t")"
date -u +%FT%TZ > "$TAG.started.${SLURM_JOB_ID}"
finish() { rc=$?; echo "$rc $(date -u +%FT%TZ) job ${SLURM_ARRAY_JOB_ID}_${t}" > "$TAG.exit.${SLURM_JOB_ID}"; }
trap finish EXIT
SCALE=${C050_SCALE:-c100}; [[ "$SCALE" =~ ^c[0-9]{3}$ ]] || { echo "bad C050_SCALE $SCALE" >&2; exit 3; }
module load GCC/14.3.0
module load R/4.5.2
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 FLEXIBLAS_NUM_THREADS=1
export R_LIBS_USER=
STUDY=/projects/ml75/fb31/BVS/bench20261019
# Refuse to run unless the code snapshot and the library manifest match the submission record.
( cd "$CODE" && sha256sum --quiet -c "$RUNDIR/SHA256SUMS" ) || { echo "snapshot hash mismatch" >&2; exit 2; }
LIBNOW=$(sha256sum "$STUDY/lib/environment_manifest.txt" | cut -d' ' -f1)
[ "$LIBNOW" = "$(cat "$RUNDIR/LIBRARY_SHA256")" ] || { echo "library manifest changed since submission" >&2; exit 2; }
if [ -n "$C050_IDS" ]; then
  IFS=: read -r -a ALL <<< "$C050_IDS"
  [ "$t" -ge 1 ] && [ "$t" -le ${#ALL[@]} ] || { echo "task $t outside C050_IDS" >&2; exit 3; }
  IDS=${ALL[$((t - 1))]}
else
  [ "$t" -ge 1 ] && [ "$t" -le 400 ] || { echo "task $t outside 1..400" >&2; exit 3; }
  if [ "$t" -le 200 ]; then P=0500; else P=1000; fi
  u=$(( (t - 1) % 200 ))
  IDS=$(for j in 0 1 2; do i=$(( 3 * u + j )); printf "p%s_S%d_r%03d " "$P" $(( i / 100 + 1 )) $(( i % 100 + 1 )); done)
fi
echo "host $(hostname) job ${SLURM_ARRAY_JOB_ID}_${t} scale $SCALE datasets $IDS start $(date -u +%FT%TZ)"
fails=0; expected=0; missing=0
for ID in $IDS; do
  P=${ID:1:4}; S=${ID#*_S}; S=${S%%_*}
  expected=$((expected + 1))
  Rscript "$CODE/run_case.R" --input "$STUDY/inputs/p$P/$ID.rds" --out "$STUDY" --run-id "$RUN_ID" \
    --scale "$SCALE" --methods F3 --manifest "$STUDY/manifests/cells/p${P}_S${S}_inputs.csv" \
    || { echo "RUNNER_ERROR $ID" >&2; fails=$((fails + 1)); }
  [ -f "$STUDY/results/$RUN_ID/p$P/${ID}_${SCALE}/F3.done" ] || { echo "MISSING $ID" >&2; missing=$((missing + 1)); }
done
echo "end $(date -u +%FT%TZ) expected $expected runner_errors $fails missing $missing"
[ "$expected" -ge 1 ] && [ "$fails" -eq 0 ] && [ "$missing" -eq 0 ]
date -u +%FT%TZ > "$TAG.finished.${SLURM_JOB_ID}"
