#!/bin/bash
# pilot_postfail_remote.sh (ON NOTS via: ssh nots "STAMP=<STAMP> bash -s" < this): after an early STOP. Truth integrity vs the staged hash list,
# terminal accounting (JOB.md section 9), and the list of result folders to pull. Read-only except final_accounting.sh's own evidence files.
set -u
: "${STAMP:?}"
PID="${STAMP}_lowp_pilot"; HR=/home/fb31/projects/BVS/New_Campaign; H=$HR/runs/$PID; S=/scratch/fb31/New_Campaign
echo "== squeue"; squeue -h -u fb31 -o '%i %j %T' 2>&1
echo "== truth integrity vs STAGED_SHA256.txt (study/truth + study/dev/truth)"
cd "$HR" || exit 3
grep -E "  \./runs/$PID/study/(dev/)?truth/" "runs/$PID/STAGED_SHA256.txt" > "$S/runs/${PID}_truthsums.txt"
echo "listed: $(wc -l < "$S/runs/${PID}_truthsums.txt")"
sha256sum --quiet -c "$S/runs/${PID}_truthsums.txt" && echo "TRUTH_SHA_OK" || echo "TRUTH_SHA_MISMATCH"
rm -f -- "$S/runs/${PID}_truthsums.txt"
echo "== final_accounting.sh"; bash "$H/code/lowp/pilot/final_accounting.sh" "$STAMP" < /dev/null 2>&1 | tail -20; echo "final_accounting_rc=${PIPESTATUS[0]}"
echo "== result folders"; ls -d "$S/results/${PID}"* 2>&1
echo "== scratch runs"; ls -A "$S/runs" 2>&1
echo "== logs size"; du -sk "$S/logs/$PID" 2>&1
