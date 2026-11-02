#!/bin/sh
cd /home/fb31/theory_campaign/A-REV5/run_20261102_v2
{ date -u; hostname; uname -a; command -v python3; python3 --version; sha256sum *.py; } > environment.txt 2>&1
python3 independent.py > independent.log 2>&1
s1=$?
python3 thresholds.py > t03.log 2>&1
s2=$?
printf 'independent_exit=%s\nt03_exit=%s\n' "$s1" "$s2" > exit_status.txt
date -u > ended.txt
