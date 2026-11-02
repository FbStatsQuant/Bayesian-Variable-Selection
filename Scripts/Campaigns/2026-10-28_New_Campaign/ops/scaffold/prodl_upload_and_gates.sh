#!/bin/bash
# prodl_upload_and_gates.sh STAMP : (laptop; run via launch_with_shim.sh so ssh takes the global NOTS lock) upload the PROD-L tar (one ssh),
# then one ssh running prodl_gates_remote.sh (guard 110, extract + STAGED_SHA256, prodl.env, dry run withH). Submits nothing.
set -u
STAMP=${1:?STAMP}; RID="${STAMP}_lowp_prodL"
CAMP=/c/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign
OUT="/c/Users/felip/OneDrive - Rice University/NOTS Data/New_Campaign/runs/$RID/bundle"
TAR="$OUT/prodL_bundle_$STAMP.tar"; EV=$CAMP/ops/evidence/ops6_prodl_${STAMP}
SHA=$(cut -c1-64 "$TAR.sha256"); [ "$(sha256sum "$TAR" | cut -c1-64)" = "$SHA" ] || { echo "local tar hash mismatch"; exit 1; }
MSYS_NO_PATHCONV=1 ssh -o BatchMode=yes -o ConnectTimeout=30 nots "mkdir -p /scratch/fb31/New_Campaign/upload && test ! -e /scratch/fb31/New_Campaign/upload/prodL_bundle_$STAMP.tar && cat > /scratch/fb31/New_Campaign/upload/prodL_bundle_$STAMP.tar && sha256sum /scratch/fb31/New_Campaign/upload/prodL_bundle_$STAMP.tar" < "$TAR" > "${EV}_upload.txt" 2>&1
urc=$?; cat "${EV}_upload.txt"
[ $urc -eq 0 ] && [ "$(cut -c1-64 "${EV}_upload.txt")" = "$SHA" ] || { echo "UPLOAD FAILED or hash differs (rc=$urc)"; exit 1; }
echo "UPLOAD_OK $SHA"
MSYS_NO_PATHCONV=1 ssh -o BatchMode=yes -o ConnectTimeout=30 nots "STAMP=$STAMP TAR_SHA=$SHA bash -s" < "$CAMP/ops/scaffold/prodl_gates_remote.sh" > "${EV}_gates.txt" 2>&1
echo "gates_ssh_rc=$?" >> "${EV}_gates.txt"; cat "${EV}_gates.txt"
