#!/bin/bash
set -u
cd /home/fb31/theory_campaign/A-REV8
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
mkdir -p results
(date -u; hostname; uname -a; command -v /home/fb31/envs/dl/bin/python; /home/fb31/envs/dl/bin/python --version; env | grep -E '^(OMP|OPENBLAS|MKL)'; sha256sum scripts/check.py) > results/environment.txt
/home/fb31/envs/dl/bin/python scripts/check.py > results/run.log 2>&1
rc=$?
echo "$rc" > results/exit_status.txt
date -u > results/finished.txt
find results -type f ! -name SHA256SUMS -print0 | sort -z | xargs -0 sha256sum > results/SHA256SUMS
exit "$rc"
