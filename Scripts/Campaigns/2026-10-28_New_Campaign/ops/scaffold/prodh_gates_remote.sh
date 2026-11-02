#!/bin/bash
# prodh_gates_remote.sh (ON NOTS via: ssh nots "STAMP=<STAMP> TAR_SHA=<sha> bash -s" < this): PROD-H JOB.md B, B2 and C (dry run only). Submits NOTHING.
set -uo pipefail
: "${STAMP:?}"; : "${TAR_SHA:?}"
RUN_ID="${STAMP}_prodH"; NC=/home/fb31/projects/BVS/New_Campaign; R=$NC/runs/$RUN_ID; TAR=/scratch/fb31/New_Campaign/upload/prodH_bundle_$STAMP.tar
stop() { echo "GATE $1 FAIL: $2"; echo "NOTHING SUBMITTED"; exit 1; }
echo "date=$(date -u +%FT%TZ) host=$(hostname) RUN_ID=$RUN_ID"
echo "== squeue (all fb31 jobs)"; Q=$(squeue -h -u fb31 -o '%i %j %T %r') || stop squeue "squeue failed"; printf '%s\n' "$Q"
[ -z "$(printf '%s' "$Q" | awk 'NF')" ] || stop squeue "fb31 has queued/running jobs: inspect before submitting"
echo "GATE squeue_empty OK"
echo "== Sapphire Rapids feature"; sinfo -p commons -h -o '%f %D' | sort | uniq; sinfo -p commons -h -o '%f' | grep -q sapphirerapids || stop spr "no sapphirerapids feature"
echo "GATE spr OK"
echo "== B2 QoS"; sacctmgr -nP show assoc where user=fb31 format=Account,Partition,QOS; sacctmgr -nP show qos format=Name,MaxJobsPU,MaxSubmitPU | grep -i nots_commons
sacctmgr -nP show assoc where user=fb31 format=Account,QOS | grep -E '^commons\|' | grep -q nots_commons || stop qos "nots_commons not listed for account commons"
echo "GATE qos OK"
echo "== guard 30"; G=$(bash $NC/code/ops/guard.sh 30 2>&1); grc=$?; echo "GUARDLINE $G | rc=$grc"; [ $grc -eq 0 ] || stop guard "guard refused (rc=$grc)"
echo "GATE guard OK"
echo "== B extract + verify"
[ "$(sha256sum "$TAR" | cut -c1-64)" = "$TAR_SHA" ] || stop tar_sha "uploaded tar hash differs"
ls -d $NC/code/core/v2_2_1 2>&1
cd $NC && test ! -e runs/$RUN_ID && tar -xf "$TAR" -C . --skip-old-files && sha256sum --quiet -c runs/$RUN_ID/STAGED_SHA256.txt && (cd code/core/v2_2_1 && sha256sum --quiet -c ../v2_2_1.SHA256SUMS) && echo STAGED_OK || stop staged "extract/verify failed"
echo "frozen manifest sha: $(sha256sum $NC/code/core/v2_2_1.SHA256SUMS | cut -c1-64)"
ls -A $NC/code/core/v2_2_1/core | grep -c cpp_cache | sed 's/^/cpp_cache entries: /'
echo "== C dry run"; bash $R/runner/submit.sh --dry-run < /dev/null 2>&1; echo "dryrun_rc=$?"
