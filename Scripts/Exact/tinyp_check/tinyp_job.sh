#!/usr/bin/env bash
# Tiny-p check (CRITERIA.md) as ONE Slurm job per part.
# Submit: sbatch --export=NONE,OUT=<scratch dir>,PART=fit|exact|compare ... tinyp_job.sh
set -euo pipefail
CL=/home/fb31/projects/BVS/SMC_BVS_v3/deploy/claude
T=$CL/readiness/tinyp
[[ -n ${SLURM_JOB_ID:-} && ${SLURM_CPUS_PER_TASK:-} == 1 && -n ${OUT:-} && -n ${PART:-} ]] || exit 65
mkdir -p "$OUT"; exec > "$OUT/$PART.job.log" 2>&1
echo "job $SLURM_JOB_ID part $PART host $(hostname -f) start $(date -u +%FT%TZ)"
source "$CL/runner/env.sh"
export TMPDIR=$OUT/tmp_$PART; mkdir -p "$TMPDIR"
case $PART in
  fit) nice -n 19 Rscript --vanilla "$T/gen_and_fit.R" "$CL/code/v2_1/code/core" "$OUT/run" ;;
  exact|compare)
    set +u; module load SciPy-bundle/2025.07; set -u
    unset PYTHONOPTIMIZE; export PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1
    python3 -c 'import sys, numpy, scipy, mpmath; print(sys.version, numpy.__version__, scipy.__version__, mpmath.__version__)'
    if [[ $PART == exact ]]; then
      # Wait for part "fit" to have written all 10 datasets (fits run sequentially after each dataset).
      for i in $(seq 1 360); do [[ $(ls "$OUT"/run/data/D*_rep*.json 2>/dev/null | wc -l) == 10 ]] && break; sleep 10; done
      nice -n 19 python3 -B "$T/exact.py" "$CL/readiness/b_battery/b_payload/oracle" "$OUT/run/data" "$OUT/exact"
    else
      python3 -B "$T/compare.py" "$OUT/run/fits" "$OUT/exact" "$OUT/result"
    fi ;;
  *) exit 64 ;;
esac
echo "end $(date -u +%FT%TZ)"
