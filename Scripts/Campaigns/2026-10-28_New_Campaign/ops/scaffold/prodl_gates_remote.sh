#!/bin/bash
# prodl_gates_remote.sh (ON NOTS via: ssh nots "STAMP=<STAMP> TAR_SHA=<sha> bash -s" < this): PROD-L JOB.md §2, §3 and §5 step 2 (DRY RUN only).
# The tar was uploaded beforehand to /scratch/fb31/New_Campaign/upload/. Submits NOTHING.
set -uo pipefail
: "${STAMP:?}"; : "${TAR_SHA:?}"
RID="${STAMP}_lowp_prodL"; HR=/home/fb31/projects/BVS/New_Campaign; B=$HR/runs/$RID/code/prod_l; TAR=/scratch/fb31/New_Campaign/upload/prodL_bundle_$STAMP.tar
stop() { echo "GATE $1 FAIL: $2"; echo "NOTHING SUBMITTED"; exit 1; }
echo "date=$(date -u +%FT%TZ) host=$(hostname) RID=$RID"
echo "== squeue (all fb31 jobs; PROD-H expected)"; squeue -h -u fb31 -o '%i %j %T' | awk '{print $2}' | sort | uniq -c
squeue -h -u fb31 -o '%j' | grep -q lowp_prodL && stop squeue "a PROD-L job already exists"
echo "GATE no_prodl_jobs OK"
echo "== guard 110 (before staging)"; G=$(bash $HR/code/ops/guard.sh 110 2>&1); grc=$?; echo "GUARDLINE $G | rc=$grc"; [ $grc -eq 0 ] || stop guard "guard refused (rc=$grc)"
echo "GATE guard OK"
[ "$(sha256sum "$TAR" | cut -c1-64)" = "$TAR_SHA" ] || stop tar_sha "uploaded tar hash differs"
echo "GATE tar_sha OK"
cd $HR && test ! -e runs/$RID && tar -xf "$TAR" -C . && sha256sum --quiet -c runs/$RID/STAGED_SHA256.txt && echo STAGED_OK || stop staged "extract/verify failed"
rm -f -- "$TAR" && echo "upload tar removed from scratch (local copy kept)"
echo "frozen manifest sha: $(sha256sum runs/$RID/code/core/v2_2_1.SHA256SUMS | cut -c1-64)"
echo "== §3 prodl.env"; grep -E '^(MODULES|R_LIBS_LOWP|R_LIBS_USER_LOWP|CEIL_[A-Z]+|PLANNED_HOME_MB_[A-Z]+|SMC_MEM_GB|SMC_HOURS)=' $B/prodl.env
echo "== §5.2 dry run --wave main --profile withH"; export STAMP; bash $B/submit_prodl.sh --wave main --profile withH --dry-run < /dev/null 2>&1; echo "dryrun_rc=$?"
