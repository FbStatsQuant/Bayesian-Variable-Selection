#!/usr/bin/env bash
# Regenerate the 1,200 production datasets (p in {500,1000} x S1-S6 x r = 1..100) with the repository generator,
# unchanged: Scripts/Data_generators/gen_prod_data.R (seed scheme in its header; it sources gen_dev_data.R).
# Output (outside git): $WORK/$STUDY/{inputs,truth,manifests/cells}. 12 cells run in parallel, nice 19.
# BLAS pinning: X = Z %*% chol(Sigma) goes through BLAS, and its last bits depend on the BLAS kernel AND thread count
# (checked: OpenBLAS 1 vs 2..8 vs 16 threads give different X for S2-S6). The canonical copy uses FlexiBLAS
# OPENBLAS-OPENMP with ONE thread: this configuration reproduces byte-for-byte the two Owls dev inputs whose hashes
# are recorded in Docs/Records/SMC_BVS_v3_deploy/NOTS_READINESS.md (01_verify_data.R). The NOTS production files
# (R 4.5.2 / NOTS BLAS) are NOT reproducible bit-for-bit on Owls; see REPORT.md section "Data".
# Usage: bash 00_regen_data.sh [WORK=/home/fb31/ls0_work] [STUDY=study] [THREADS=1]
set -euo pipefail
WORK=${1:-/home/fb31/ls0_work}; STUDY=${2:-study}; TH=${3:-1}
export FLEXIBLAS=OPENBLAS-OPENMP OMP_NUM_THREADS=$TH OPENBLAS_NUM_THREADS=$TH
REPO=$(git -C "$(dirname "$0")" rev-parse --show-toplevel)
GEN="$REPO/Scripts/Data_generators/gen_prod_data.R"
mkdir -p "$WORK/$STUDY" "$WORK/logs"
for p in 500 1000; do for s in 1 2 3 4 5 6; do
  nice -n 19 Rscript "$GEN" "$WORK/$STUDY" $p $s > "$WORK/logs/gen_p${p}_S${s}.log" 2>&1 &
done; done
wait
cat "$WORK"/logs/gen_p*_S*.log
