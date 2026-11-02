#!/bin/bash
# Production array for A1 SuSiE + SuSiE-L100 (scale c100 only, decision D3).
# Tasks 1..120: task t covers 10 datasets of one p: t = 1..60 -> p = 500, t = 61..120 -> p = 1000;
#   within a p, u = (t - 1) mod 60: scenario s = u div 10 + 1, replicates 10*(u mod 10) + 1 .. + 10.
# Task 121: production canaries (master §IV.3): three dev datasets (dev_p0500_S4_r001,
#   dev_p1000_S2_r001, dev_p1000_S6_r001), written under case ids with the dev_ prefix, so they
#   are excluded from all production counts; compared with the dev pilot outputs afterwards.
# Submitted only by slurm/submit_prod.sh or slurm/retry_prod.sh, which set CODE_DIR (frozen
# snapshot), RUN_ID and A1_CHUNK (10 in production, 1 in the smoke test; validated below).
# Resources (--time, --mem, --array, --output) are given on the sbatch command line.
#SBATCH --job-name=A1_prod
#SBATCH --partition=commons
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
module load GCC/14.3.0 || { echo "module load GCC/14.3.0 failed"; exit 1; }
module load R/4.5.2 || { echo "module load R/4.5.2 failed"; exit 1; }
case "$(Rscript --vanilla -e 'cat(R.version.string)')" in "R version 4.5.2 "*) ;; *) echo "wrong R version"; exit 1;; esac
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 FLEXIBLAS_NUM_THREADS=1
export LC_ALL=C
: "${CODE_DIR:?CODE_DIR not set}" "${RUN_ID:?RUN_ID not set}" "${A1_CHUNK:?A1_CHUNK not set}"
case "${RUN_ID}" in
  *_bench20261019_prod_A1_SuSiE) [ "${A1_CHUNK}" = 10 ] || { echo "production run requires A1_CHUNK=10 (got ${A1_CHUNK})"; exit 1; } ;;
  *_bench20261019_prodsmoke_A1_SuSiE) [ "${A1_CHUNK}" -ge 1 ] && [ "${A1_CHUNK}" -le 10 ] || { echo "bad A1_CHUNK ${A1_CHUNK}"; exit 1; } ;;
  *) echo "unexpected RUN_ID ${RUN_ID}"; exit 1 ;;
esac
STUDY=/projects/ml75/fb31/BVS/bench20261019
[ "${CODE_DIR}" = "${STUDY}/runs/${RUN_ID}/code" ] || { echo "CODE_DIR ${CODE_DIR} is not the snapshot of ${RUN_ID}"; exit 1; }
BASELINE=${STUDY}/runs/${RUN_ID}/env_fingerprint.rds
[ -f "${BASELINE}" ] || { echo "missing environment baseline ${BASELINE}"; exit 1; }
t=${SLURM_ARRAY_TASK_ID}
if [ "$t" -ge 1 ] && [ "$t" -le 120 ]; then
  if [ "$t" -le 60 ]; then p=500; else p=1000; fi
  u=$(( (t - 1) % 60 )); s=$(( u / 10 + 1 )); r0=$(( 10 * (u % 10) + 1 ))
  pp=$(printf "p%04d" "$p")
  INPUTS=""
  for r in $(seq "$r0" $(( r0 + A1_CHUNK - 1 ))); do
    INPUTS="${INPUTS} ${STUDY}/inputs/${pp}/${pp}_S${s}_r$(printf %03d "$r").rds"
  done
elif [ "$t" -eq 121 ]; then
  INPUTS="${STUDY}/dev/inputs/p0500/dev_p0500_S4_r001.rds ${STUDY}/dev/inputs/p1000/dev_p1000_S2_r001.rds ${STUDY}/dev/inputs/p1000/dev_p1000_S6_r001.rds"
else
  echo "task id out of range: $t"; exit 1
fi
echo "host $(hostname) task $t A1_CHUNK=${A1_CHUNK} RUN_ID=${RUN_ID} code ${CODE_DIR} start $(date -u +%FT%TZ)"
fail=0
for IN in ${INPUTS}; do
  Rscript --vanilla "${CODE_DIR}/run_case.R" --code_dir="${CODE_DIR}" --input="${IN}" \
    --out_root="${STUDY}/results" --run_id="${RUN_ID}" --methods=A1,SuSiE-L100 --scales=c100     --env_baseline="${BASELINE}"
  rc=$?
  echo "dataset ${IN} exit ${rc} $(date -u +%FT%TZ)"
  [ "$rc" -eq 0 ] || fail=$((fail + 1))
done
echo "task $t done: ${fail} dataset(s) with nonzero exit, end $(date -u +%FT%TZ)"
exit $(( fail > 0 ))
