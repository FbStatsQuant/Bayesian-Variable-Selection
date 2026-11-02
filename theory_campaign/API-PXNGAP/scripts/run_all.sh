#!/bin/bash
# API-PXNGAP: all checks, sequential, single owls_run job (-j 2).
cd "$(dirname "$0")"
python3 check_trJ.py > ../results/check_trJ.txt 2>&1
python3 check_margins.py > ../results/check_margins.txt 2>&1
python3 check_lemmaE.py > ../results/check_lemmaE.txt 2>&1
python3 check_route.py > ../results/check_route.txt 2>&1
echo DONE >> ../results/check_route.txt
