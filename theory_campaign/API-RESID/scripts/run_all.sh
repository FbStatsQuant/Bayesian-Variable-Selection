#!/usr/bin/env bash
# Launch: ~/.config/bvs-hq/owls/owls_run -j 2 -- bash scripts/run_all.sh   (from theory_campaign/API-RESID)
# Two shards (one per allotted core); resumable (skips fits already in the shard CSV).
set -u
N=${OWLS_JOB_CORES:-2}
for s in $(seq 1 $N); do
  Rscript scripts/resid_step0.R results/per_fit_shard$s.csv $s $N > results/run_shard$s.log 2>&1 &
done
wait
