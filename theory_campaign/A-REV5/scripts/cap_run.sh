#!/bin/sh
cd /home/fb31/theory_campaign/A-REV5/run_20261102_v2
date -u > cap_started.txt
python3 cap_witness.py > cap_witness.log 2>&1
printf "%s\n" "$?" > cap_exit.txt
sha256sum cap_witness.py > cap_hash.txt
date -u > cap_ended.txt
