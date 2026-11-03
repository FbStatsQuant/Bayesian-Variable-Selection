#!/bin/bash
# plb_submit_remote_rev2b.sh (ON NOTS; started detached by remote_bg.sh; STAMP, TAR_SHA, LEDGER_SHA in env): PROD_L_BENCH rev 2 (HQ D85).
# Replaces rev2 after its 23:10Z stop (nothing submitted): the NOTS ledger check required all 32 ledger entries, but stage_local.sh deliberately
# does not ship ./BUILD_NOTES.md (its documented exclusion list: tests review fixtures __pycache__ PROGRESS.md BUILD_NOTES*.md). Now: ledger file
# hash must equal LEDGER_SHA; every ledger entry present on NOTS must verify; missing entries must all be on that exclusion list.
# Resume-safe: if runs/<RID> already exists (extracted by the 23:10Z attempt) it is re-verified (STAGED_SHA256 + tar hash) instead of re-extracted.
set -uo pipefail
: "${STAMP:?}"; : "${TAR_SHA:?}"; : "${LEDGER_SHA:?}"
RID="${STAMP}_lowp_bench"; HR=/home/fb31/projects/BVS/New_Campaign; B=$HR/runs/$RID/code/prod_l_bench; TAR=/scratch/fb31/New_Campaign/upload/prodLB_bundle_$STAMP.tar
stop() { echo "GATE $1 FAIL: $2"; echo "NOT SUBMITTED"; exit 1; }
echo "date=$(date -u +%FT%TZ) RID=$RID"; squeue -h -u fb31 -o '%i %j %T' | awk '{print $2}' | sort | uniq -c
squeue -h -u fb31 -o '%j' | grep -q lowpB_ && stop squeue "a PROD_L_BENCH job exists"
squeue -h -u fb31 -o '%j' | grep -qE 'lowpL_s[1-4]' && stop squeue "a PROD-L fitting job is queued/running"
SQ=$(squeue -h -u fb31 -o '%F %K %T') || stop ceiling "squeue failed"
cap=$(printf '%s\n' "$SQ" | awk 'NF>=2 {b=$1; if (match($2, /%[0-9]+/)) thr[b]=substr($2, RSTART+1, RLENGTH-1)+0; else n[b]++} END {t=0; for (b in n) if (!(b in thr)) t+=n[b]; for (b in thr) t+=thr[b]; print t}') || stop ceiling "parse failed"
echo "ceiling: existing concurrency=$cap + new 32 = $((cap + 32)) tasks (<= 96), billed $(( 2 * (cap + 32) )) (<= 192)"
[ $((cap + 32)) -le 96 ] || stop ceiling "would exceed 96 tasks / 192 billed CPUs"
G=$(bash $HR/code/ops/guard.sh 75 2>&1); grc=$?; echo "GUARDLINE $G | rc=$grc"; [ $grc -eq 0 ] || stop guard "guard 75 refused"
[ -f "$TAR" ] && [ "$(sha256sum "$TAR" | cut -c1-64)" = "$TAR_SHA" ] || stop tar_sha "uploaded tar missing or hash differs"
cd $HR || stop cd "cannot cd $HR"
if [ -e runs/$RID ]; then
  echo "runs/$RID exists (extracted by the 23:10Z attempt): re-verifying instead of re-extracting"
  sha256sum --quiet -c runs/$RID/STAGED_SHA256.txt && echo "STAGED_OK (re-verified)" || stop staged "existing extraction does not verify"
else
  tar -xf "$TAR" -C . && sha256sum --quiet -c runs/$RID/STAGED_SHA256.txt && echo STAGED_OK || stop staged "extract/verify failed"
fi
L=$B/BUNDLE_SHA256SUMS.txt
[ "$(sha256sum $L | cut -c1-64)" = "$LEDGER_SHA" ] || stop ledger "ledger file hash differs from $LEDGER_SHA"
present=$(cd $B && awk '{f=$2; if (system("test -f \"" f "\"")==0) print}' BUNDLE_SHA256SUMS.txt) || stop ledger "ledger parse failed"
missing=$(cd $B && awk '{f=$2; if (system("test -f \"" f "\"")!=0) print f}' BUNDLE_SHA256SUMS.txt) || stop ledger "ledger parse failed"
( cd $B && printf '%s\n' "$present" | sha256sum --quiet -c - ) || stop ledger "a staged ledger entry does not verify"
for m in $missing; do case "$m" in ./BUILD_NOTES.md|./BUILD_NOTES_A.md|./BUILD_NOTES_B.md|./PROGRESS.md|./tests/*|./review/*|./fixtures/*) ;; *) stop ledger "ledger entry missing on NOTS and not a documented stage exclusion: $m";; esac; done
echo "LEDGER_OK $LEDGER_SHA: $(printf '%s\n' "$present" | grep -c .) staged entries verified; not staged (documented exclusions): $(echo $missing)"
rm -f -- "$TAR"; find $HR/runs/$RID -ipath '*truth*' -o -ipath '*holdout*' | head -3 | sed 's/^/TRUTH-LIKE PATH: /'
grep -E '^(MODULES_BENCH|R_LIBS_BENCH|CEIL_[A-Z]+|PLANNED_HOME_MB_[A-Z]+)=' $B/bench.env
export STAMP
echo "== dry run"; bash $B/submit_bench.sh --wave main --profile alone --dry-run < /dev/null 2>&1 | tail -25; drc=${PIPESTATUS[0]}; echo "dryrun_rc=$drc"
[ $drc -eq 0 ] || stop dryrun "dry run refused"
echo "== submit"; bash $B/submit_bench.sh --wave main --profile alone < /dev/null 2>&1 | tail -15; echo "submit_rc=${PIPESTATUS[0]}"
echo "== jobids"; cat /scratch/fb31/New_Campaign/logs/$RID/jobids.tsv 2>&1
