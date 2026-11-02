#!/bin/sh
cd /home/fb31/theory_campaign/A-REV7 || exit 99
date -u > started.txt
uname -a > environment.txt
command -v python3 >> environment.txt
/home/fb31/envs/dl/bin/python --version >> environment.txt 2>&1
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
find . -type f ! -path './.git/*' ! -name '*.txt' ! -name '*.json' ! -name '*.log' -exec sha256sum {} \; > input-sha256.txt
/home/fb31/envs/dl/bin/python -u reproduce.py > run.log 2>&1
status=$?
if [ "$status" = 0 ]; then
  /home/fb31/envs/dl/bin/python -u sources/O-BGIBBS/scripts/bg3_popcheck.py 2 > bg3-c2.log 2>&1
  status=$?
fi
echo "$status" > exit-status.txt
date -u > finished.txt
sha256sum results.json run.log > output-sha256.txt
exit "$status"
