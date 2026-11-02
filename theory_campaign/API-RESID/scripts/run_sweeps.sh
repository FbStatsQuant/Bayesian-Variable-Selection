#!/usr/bin/env bash
# Launch: ~/.config/bvs-hq/owls/owls_run -j 2 -- bash scripts/run_sweeps.sh   (from theory_campaign/API-RESID)
set -u
N=${OWLS_JOB_CORES:-2}
for s in $(seq 1 $N); do
  Rscript scripts/resid_sweeps.R results/sweeps_shard$s.csv $s $N > results/sweeps_shard$s.log 2>&1 &
done
wait
