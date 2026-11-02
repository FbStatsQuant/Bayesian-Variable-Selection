#!/bin/sh
cd /home/fb31/theory_campaign/A-REV4 || exit 99
date -u > start.txt
uname -a > environment.txt
python3 --version >> environment.txt
sha256sum checks.py SOURCE_MANIFEST.json snapshots/* > remote_sha256.txt
python3 checks.py > results.json 2> stderr.txt
rc=$?
echo "$rc" > exit_status.txt
date -u > end.txt
exit "$rc"
