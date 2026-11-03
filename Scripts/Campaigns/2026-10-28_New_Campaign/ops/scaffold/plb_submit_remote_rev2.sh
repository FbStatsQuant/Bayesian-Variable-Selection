#!/bin/bash
# plb_submit_remote_rev2.sh (ON NOTS; HQ D85 rev 2: + ledger check on NOTS after extraction via: ssh nots "STAMP=<s> TAR_SHA=<sha> bash -s" < this): PROD_L_BENCH JOB.md §2 (guard 75 before extraction; tar hash;
# test ! -e; extract; STAGED_SHA256) + §3 (bench.env) + §5 step 2 (dry run --profile alone, then submit if rc 0). Prints job ids.
set -uo pipefail
: "${STAMP:?}"; : "${TAR_SHA:?}"
RID="${STAMP}_lowp_bench"; HR=/home/fb31/projects/BVS/New_Campaign; B=$HR/runs/$RID/code/prod_l_bench; TAR=/scratch/fb31/New_Campaign/upload/prodLB_bundle_$STAMP.tar
stop() { echo "GATE $1 FAIL: $2"; echo "NOT SUBMITTED"; exit 1; }
echo "date=$(date -u +%FT%TZ) RID=$RID"; squeue -h -u fb31 -o '%i %j %T' | awk '{print $2}' | sort | uniq -c
squeue -h -u fb31 -o '%j' | grep -q lowpB_ && stop squeue "a PROD_L_BENCH job exists"
squeue -h -u fb31 -o '%j' | grep -qE 'lowpL_s[1-4]' && stop squeue "a PROD-L fitting job is queued/running"
# campaign ceiling (charter: <= 96 tasks / 192 billed CPUs; 1-CPU task bills 2). Concurrency per job: an array with a pending %N throttle counts N;
# otherwise each listed (running) task counts 1. New: PROD_L_BENCH alone profile = %32. (Added 2026-11-02, HQ: respect the ceiling with F3 cell 4.)
SQ=$(squeue -h -u fb31 -o '%F %K %T') || stop ceiling "squeue failed"
cap=$(printf '%s\n' "$SQ" | awk 'NF>=2 {b=$1; if (match($2, /%[0-9]+/)) thr[b]=substr($2, RSTART+1, RLENGTH-1)+0; else n[b]++} END {t=0; for (b in n) if (!(b in thr)) t+=n[b]; for (b in thr) t+=thr[b]; print t}') || stop ceiling "parse failed"
echo "ceiling: existing concurrency=$cap + new 32 = $((cap + 32)) tasks (<= 96), billed $(( 2 * (cap + 32) )) (<= 192)"
[ $((cap + 32)) -le 96 ] || stop ceiling "would exceed 96 tasks / 192 billed CPUs"
G=$(bash $HR/code/ops/guard.sh 75 2>&1); grc=$?; echo "GUARDLINE $G | rc=$grc"; [ $grc -eq 0 ] || stop guard "guard 75 refused"
[ "$(sha256sum "$TAR" | cut -c1-64)" = "$TAR_SHA" ] || stop tar_sha "uploaded tar hash differs"
cd $HR && test ! -e runs/$RID && tar -xf "$TAR" -C . && sha256sum --quiet -c runs/$RID/STAGED_SHA256.txt && echo STAGED_OK || stop staged "extract/verify failed"
L=$B/BUNDLE_SHA256SUMS.txt; [ "$(sha256sum $L | cut -c1-64)" = "${LEDGER_SHA:?}" ] && ( cd $B && sha256sum --quiet -c BUNDLE_SHA256SUMS.txt ) && echo "LEDGER_OK $(wc -l < $L) files $LEDGER_SHA" || stop ledger "ledger hash or file check failed on NOTS"
rm -f -- "$TAR"; find $HR/runs/$RID -ipath '*truth*' -o -ipath '*holdout*' | head -3 | sed 's/^/TRUTH-LIKE PATH: /'
grep -E '^(MODULES_BENCH|R_LIBS_BENCH|CEIL_[A-Z]+|PLANNED_HOME_MB_[A-Z]+)=' $B/bench.env
export STAMP
echo "== dry run"; bash $B/submit_bench.sh --wave main --profile alone --dry-run < /dev/null 2>&1 | tail -25; drc=${PIPESTATUS[0]}; echo "dryrun_rc=$drc"
[ $drc -eq 0 ] || stop dryrun "dry run refused"
echo "== submit"; bash $B/submit_bench.sh --wave main --profile alone < /dev/null 2>&1 | tail -15; echo "submit_rc=${PIPESTATUS[0]}"
echo "== jobids"; cat /scratch/fb31/New_Campaign/logs/$RID/jobids.tsv 2>&1
