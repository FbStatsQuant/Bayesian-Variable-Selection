#!/bin/bash
# pilot_recover_and_diag_remote.sh (ON NOTS via: ssh nots "STAMP=<STAMP> bash -s" < this): JOB.md section 6 truth recovery, then read-only diagnosis of P0a.
set -u
: "${STAMP:?}"
PID="${STAMP}_lowp_pilot"; H=/home/fb31/projects/BVS/New_Campaign/runs/$PID; L=/scratch/fb31/New_Campaign/logs/$PID
echo "date=$(date -u +%FT%TZ) host=$(hostname)"
echo "== squeue"; squeue -h -u fb31 -o '%i %j %T' 2>&1
echo "== modes before"; stat -c '%a %n' "$H/study/truth" "$H/study/dev/truth" 2>&1
echo "== recover_truth.sh"; bash "$H/code/lowp/pilot/recover_truth.sh" "$STAMP" < /dev/null 2>&1; echo "recover_rc=$?"
echo "== modes after"; stat -c '%a %n' "$H/study/truth" "$H/study/dev/truth" 2>&1
echo "   files not 444 (truth):     $(find "$H/study/truth" "$H/study/dev/truth" -type f ! -perm 444 2>&1 | wc -l)"
echo "   dirs not 755 (truth):      $(find "$H/study/truth" "$H/study/dev/truth" -type d ! -perm 755 2>&1 | wc -l)"
echo "   truth files:               $(find "$H/study/truth" -type f 2>&1 | wc -l) + $(find "$H/study/dev/truth" -type f 2>&1 | wc -l)"
echo "== sacct"; sacct -n -X -j 2467487,2467488,2467489,2467490,2467491,2467492,2467493,2467494,2467495,2467496,2467497,2467498 -o JobID%16,JobName%20,State%14,ExitCode,Elapsed,NodeList 2>&1
echo "== log tree"; find "$L" -maxdepth 2 2>&1 | sort | head -80
for f in $(ls "$L"/slurm-*2467488* "$L"/slurm-*2467497* 2>/dev/null); do echo "===== $f"; cat "$f"; done
for d in p0_verify truthlock; do [ -d "$L/$d" ] && { echo "===== dir $d"; ls -la "$L/$d"; for f in "$L/$d"/*; do [ -f "$f" ] && { echo "--- $f"; tail -n 40 "$f"; }; done; }; done
echo "===== env"; ls "$L/env" 2>&1 | head; for f in "$L"/env/R_*verify* "$L"/env/node_*verify*; do [ -f "$f" ] && { echo "--- $f"; cat "$f"; }; done
