#!/bin/bash
# SuSiE-refine array (refine tree of the A1 c = 0.5 copy; PREREG_c050 R4): method id SuSiE-refine only,
# one scale per run, SCALE (default c100). No canary task (task 401 is not submitted).
# Task map (slurm/bundles.sh::task_datasets), production map: tasks 1..400 of A1_CHUNK = 3 datasets,
#   t = 1..200 -> p = 500, t = 201..400 -> p = 1000; within a p, u = (t - 1) mod 200 covers positions
#   3u .. 3u + 2 of the scenario-major order (scenario i div 100 + 1, replicate i mod 100 + 1).
# Task 401: production canaries (master §IV.3): three dev datasets (dev_p0500_S4_r001,
#   dev_p1000_S2_r001, dev_p1000_S6_r001), always at c100 (the scale of the dev pilot they are
#   compared with), written under case ids with the dev_ prefix, so they are excluded from all
#   production counts.
# Run kinds (from RUN_ID <stamp>_bench20261019_<kind>_SuSiErefine): prodc050 / prodc100 (production map,
#   tasks 1..400, SCALE c050 / c100), pilotc050 / pilotc100 (pilot map, tasks 1..4, SCALE c050 / c100).
# Submitted only by slurm/submit_prod.sh or slurm/retry_prod.sh, which set CODE_DIR (frozen
# snapshot), RUN_ID, A1_CHUNK (3) and SCALE (validated below).
# Resources (--time, --mem, --array, --output) are given on the sbatch command line.
#SBATCH --job-name=A1_refine
#SBATCH --partition=commons
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
module load GCC/14.3.0 || { echo "module load GCC/14.3.0 failed"; exit 1; }
module load R/4.5.2 || { echo "module load R/4.5.2 failed"; exit 1; }
case "$(Rscript --vanilla -e 'cat(R.version.string)')" in "R version 4.5.2 "*) ;; *) echo "wrong R version"; exit 1;; esac
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 FLEXIBLAS_NUM_THREADS=1
export LC_ALL=C
: "${CODE_DIR:?CODE_DIR not set}" "${RUN_ID:?RUN_ID not set}" "${A1_CHUNK:?A1_CHUNK not set}"
SCALE=${SCALE:-c100}
[ "${A1_CHUNK}" = 3 ] || { echo "c050 copy requires A1_CHUNK=3 (got ${A1_CHUNK})"; exit 1; }
case "${RUN_ID}" in
  *_bench20261019_prodc050_SuSiErefine) MAP=prod; WANT=c050 ;;
  *_bench20261019_prodc100_SuSiErefine) MAP=prod; WANT=c100 ;;
  *_bench20261019_pilotc050_SuSiErefine) MAP=pilot; WANT=c050 ;;
  *_bench20261019_pilotc100_SuSiErefine) MAP=pilot; WANT=c100 ;;
  *) echo "unexpected RUN_ID ${RUN_ID}"; exit 1 ;;
esac
[ "${SCALE}" = "${WANT}" ] || { echo "run ${RUN_ID} requires SCALE=${WANT} (got ${SCALE})"; exit 1; }
STUDY=/projects/ml75/fb31/BVS/bench20261019
[ "${CODE_DIR}" = "${STUDY}/runs/${RUN_ID}/code" ] || { echo "CODE_DIR ${CODE_DIR} is not the snapshot of ${RUN_ID}"; exit 1; }
BASELINE=${STUDY}/runs/${RUN_ID}/env_fingerprint.rds
[ -f "${BASELINE}" ] || { echo "missing environment baseline ${BASELINE}"; exit 1; }
source "${CODE_DIR}/slurm/bundles.sh"
t=${SLURM_ARRAY_TASK_ID}
[ "$t" -ne "${A1_CANARY_TASK}" ] || { echo "no canary task in the refine tree"; exit 1; }
IDS=$(task_datasets "$t" "${MAP}") || { echo "task id out of range for map ${MAP}: $t"; exit 1; }
INPUTS=""
for id in ${IDS}; do
  case "$id" in
    dev_*) pp=${id#dev_}; pp=${pp%%_*}; INPUTS="${INPUTS} ${STUDY}/dev/inputs/${pp}/${id}.rds" ;;
    *) pp=${id%%_*}; INPUTS="${INPUTS} ${STUDY}/inputs/${pp}/${id}.rds" ;;
  esac
done
echo "host $(hostname) task $t A1_CHUNK=${A1_CHUNK} SCALE=${SCALE} map ${MAP} RUN_ID=${RUN_ID} code ${CODE_DIR} start $(date -u +%FT%TZ)"
fail=0
for IN in ${INPUTS}; do
  SK=${SCALE}; case "${IN}" in */dev/inputs/*) SK=c100 ;; esac
  Rscript --vanilla "${CODE_DIR}/run_case.R" --code_dir="${CODE_DIR}" --input="${IN}" \
    --out_root="${STUDY}/results" --run_id="${RUN_ID}" --methods=SuSiE-refine --scales="${SK}" --env_baseline="${BASELINE}"
  rc=$?
  echo "dataset ${IN} exit ${rc} $(date -u +%FT%TZ)"
  [ "$rc" -eq 0 ] || fail=$((fail + 1))
done
echo "task $t done: ${fail} dataset(s) with nonzero exit, end $(date -u +%FT%TZ)"
exit $(( fail > 0 ))
