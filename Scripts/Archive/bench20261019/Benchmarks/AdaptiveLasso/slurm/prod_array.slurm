#!/bin/bash
# F3 production array: 120 tasks x 10 datasets of one p, scale c100 only (decision D3).
# Task t = 1..60  -> p = 500,  t = 61..120 -> p = 1000; within a p, local task u = 1..60 maps to
# scenario S = ceil(u / 10) and replicates 10*((u-1) mod 10) + 1 .. + 10.
# Submitted only by slurm/submit_prod.sh, which sets RUN_ID, CODE (frozen snapshot), RUNDIR,
# STATUS, SMOKE and ONLY_DATASET and passes the resources on the sbatch command line.
# ONLY_DATASET is honoured only when SMOKE=1 (Astra finding 1). The runner skips (case, method)
# pairs that already have a valid result of this run; the task fails unless every expected case
# ends with a .done file.
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
if [ "${SMOKE:-0}" != "1" ] && [ -n "$ONLY_DATASET" ]; then echo "ONLY_DATASET set outside smoke mode" >&2; exit 3; fi
module load GCC/14.3.0
module load R/4.5.2
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 FLEXIBLAS_NUM_THREADS=1
export R_LIBS_USER=
STUDY=/projects/ml75/fb31/BVS/bench20261019
# Refuse to run unless the code snapshot and the library manifest match the submission record.
( cd "$CODE" && sha256sum --quiet -c "$RUNDIR/SHA256SUMS" ) || { echo "snapshot hash mismatch" >&2; exit 2; }
LIBNOW=$(sha256sum "$STUDY/lib/environment_manifest.txt" | cut -d' ' -f1)
[ "$LIBNOW" = "$(cat "$RUNDIR/LIBRARY_SHA256")" ] || { echo "library manifest changed since submission" >&2; exit 2; }
if [ "$t" -le 60 ]; then P=0500; u=$t; else P=1000; u=$((t - 60)); fi
S=$(( (u - 1) / 10 + 1 ))
R0=$(( ((u - 1) % 10) * 10 ))
echo "host $(hostname) job ${SLURM_ARRAY_JOB_ID}_${t} p$P S$S r$((R0 + 1))-r$((R0 + 10)) start $(date -u +%FT%TZ)"
fails=0; expected=0; missing=0
for i in $(seq 1 10); do
  ID=$(printf "p%s_S%d_r%03d" "$P" "$S" $((R0 + i)))
  if [ "${SMOKE:-0}" = "1" ] && [ -n "$ONLY_DATASET" ] && [ "$ID" != "$ONLY_DATASET" ]; then continue; fi
  expected=$((expected + 1))
  Rscript "$CODE/run_case.R" --input "$STUDY/inputs/p$P/$ID.rds" --out "$STUDY" --run-id "$RUN_ID" \
    --scale c100 --methods F3 --manifest "$STUDY/manifests/cells/p${P}_S${S}_inputs.csv" \
    || { echo "RUNNER_ERROR $ID" >&2; fails=$((fails + 1)); }
  [ -f "$STUDY/results/$RUN_ID/p$P/${ID}_c100/F3.done" ] || { echo "MISSING $ID" >&2; missing=$((missing + 1)); }
done
echo "end $(date -u +%FT%TZ) expected $expected runner_errors $fails missing $missing"
[ "$expected" -ge 1 ] && [ "$fails" -eq 0 ] && [ "$missing" -eq 0 ]
date -u +%FT%TZ > "$TAG.finished.${SLURM_JOB_ID}"
