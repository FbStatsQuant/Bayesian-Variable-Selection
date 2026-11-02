#!/bin/bash
cd /home/fb31/theory_campaign/A-REV3 || exit 99
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
mkdir -p results
exec > results/run.log 2>&1
date -u
hostname
echo "PID=$$"
printf '%s\n' '/home/fb31/envs/dl/bin/python scripts/w4_checks.py; /home/fb31/envs/dl/bin/python scripts/w3_checks.py; /home/fb31/envs/dl/bin/python scripts/validate.py'
sha256sum scripts/* > results/source_sha256.txt
/home/fb31/envs/dl/bin/python scripts/w4_checks.py
a=$?
/home/fb31/envs/dl/bin/python scripts/w3_checks.py
b=$?
/home/fb31/envs/dl/bin/python scripts/validate.py
c=$?
printf 'w4=%s w3=%s validate=%s\n' "$a" "$b" "$c" > results/exit_status.txt
sha256sum results/*.npz results/*.jsonl > results/output_sha256.txt
date -u

