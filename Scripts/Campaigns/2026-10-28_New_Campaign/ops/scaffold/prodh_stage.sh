#!/bin/bash
# prodh_stage.sh STAMP : (laptop) PROD-H JOB.md section 3 A + upload (B part 1).
#   1. every bundle file against BUNDLE_SHA256SUMS (expected manifest sha 2a2a8b1f…) and the frozen manifest hash (d880afdb…13e1);
#   2. stage_local.sh --stamp STAMP --out <NOTS Data>/runs/<RUN_ID>/bundle;
#   3. upload the tar to /scratch/fb31/New_Campaign/upload/ over one ssh and compare its sha256.
set -u
STAMP=${1:?STAMP}; RUN_ID="${STAMP}_prodH"
CAMP=/c/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign
B=$CAMP/conformance/jobs/PROD_H
OUT="/c/Users/felip/OneDrive - Rice University/NOTS Data/New_Campaign/runs/$RUN_ID/bundle"
EV=$CAMP/ops/evidence/ops5_prodh_${STAMP}
[ "$(sha256sum "$B/BUNDLE_SHA256SUMS" | cut -c1-64)" = 2a2a8b1fd3d5ad72ef51e677cd17a097515333ac96eb3d076efeefc8823ba5f3 ] || { echo "BUNDLE_SHA256SUMS hash differs from HQ's"; exit 1; }
( cd "$B" && sha256sum --quiet -c BUNDLE_SHA256SUMS ) || { echo "bundle files do not match BUNDLE_SHA256SUMS"; exit 1; }
echo "BUNDLE_OK 53 files"
[ "$(sha256sum "$CAMP/code/core/v2_2_1.SHA256SUMS" | cut -c1-64)" = d880afdbd0c1b7836862b5dff01a05168197f044deb757716e9549406f2e13e1 ] || { echo "frozen manifest hash differs"; exit 1; }
echo "FROZEN_MANIFEST_OK d880afdb…13e1"
bash "$B/stage_local.sh" --stamp "$STAMP" --out "$OUT" > "${EV}_stage.txt" 2>&1 || { cat "${EV}_stage.txt"; echo "STAGE FAILED"; exit 1; }
tail -8 "${EV}_stage.txt"
TAR="$OUT/prodH_bundle_$STAMP.tar"; [ -f "$TAR" ] || { echo "tar missing"; exit 1; }
SHA=$(sha256sum "$TAR" | cut -c1-64); echo "tar sha256 $SHA ($(du -k "$TAR" | cut -f1) KB)"
MSYS_NO_PATHCONV=1 ssh -o BatchMode=yes -o ConnectTimeout=30 nots "mkdir -p /scratch/fb31/New_Campaign/upload && test ! -e /scratch/fb31/New_Campaign/upload/prodH_bundle_$STAMP.tar && cat > /scratch/fb31/New_Campaign/upload/prodH_bundle_$STAMP.tar && sha256sum /scratch/fb31/New_Campaign/upload/prodH_bundle_$STAMP.tar" < "$TAR" > "${EV}_upload.txt" 2>&1
urc=$?; cat "${EV}_upload.txt"
[ $urc -eq 0 ] && [ "$(cut -c1-64 "${EV}_upload.txt")" = "$SHA" ] || { echo "UPLOAD FAILED or hash differs (rc=$urc)"; exit 1; }
echo "UPLOAD_OK $SHA"
