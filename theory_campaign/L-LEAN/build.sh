#!/bin/bash
# usage: build.sh target...   -> prints errors/warnings only
cd "$(dirname "$0")/SmcBvs"
lake build "$@" > ../build_log.txt 2>&1
rc=$?
grep -v -E "^(âœ”|✔|⣿|.*Replayed|.*Built )" ../build_log.txt | grep -v "Running Mathlib" | head -150
echo "EXIT $rc"
