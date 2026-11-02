#!/bin/bash
# pilot_stage_and_submit.sh STAMP : (laptop, Git Bash) LOWP pilot JOB.md rev 7c sections 2 + 5.
#   1. stage_local.sh -> durable bundle in the NOTS Data mirror (runs/<PID>/bundle);  2. upload the tar to scratch (one ssh);
#   3. one ssh running pilot_submit_remote.sh (squeue, GNU time, guard 30, unpack + STAGED_SHA256, pilot.env, submit_pilot.sh).
set -u
STAMP=${1:?STAMP}
[[ "$STAMP" =~ ^[0-9]{8}T[0-9]{4}Z$ ]] || { echo "bad STAMP" >&2; exit 2; }
PID="${STAMP}_lowp_pilot"
CAMP=/c/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign
DM="/c/Users/felip/OneDrive - Rice University/NOTS Data/New_Campaign"
OUT="$DM/runs/$PID/bundle"
EV=$CAMP/ops/evidence/ops4_pilot_${STAMP}
echo "== 1 stage"
bash "$CAMP/code/lowp/pilot/stage_local.sh" --sealed "$DM/inputs/lowp_study" --stamp "$STAMP" --out "$OUT" > "${EV}_stage.txt" 2>&1 || { cat "${EV}_stage.txt"; echo "STAGE FAILED"; exit 1; }
tail -5 "${EV}_stage.txt"
TAR="$OUT/pilot_bundle_$STAMP.tar"
SHA=$(cut -c1-64 "$TAR.sha256")
[ "$(sha256sum "$TAR" | cut -c1-64)" = "$SHA" ] || { echo "local tar hash mismatch"; exit 1; }
echo "tar $(du -k "$TAR" | cut -f1) KB sha256 $SHA"
echo "== 2 upload"
MSYS_NO_PATHCONV=1 ssh -o BatchMode=yes -o ConnectTimeout=30 nots "test ! -e /scratch/fb31/New_Campaign/runs/pilot_bundle_$STAMP.tar && cat > /scratch/fb31/New_Campaign/runs/pilot_bundle_$STAMP.tar && sha256sum /scratch/fb31/New_Campaign/runs/pilot_bundle_$STAMP.tar" < "$TAR" > "${EV}_upload.txt" 2>&1
urc=$?; cat "${EV}_upload.txt"
[ $urc -eq 0 ] && [ "$(cut -c1-64 "${EV}_upload.txt")" = "$SHA" ] || { echo "UPLOAD FAILED or hash differs (rc=$urc)"; exit 1; }
echo "== 3 remote gates + submit"
MSYS_NO_PATHCONV=1 ssh -o BatchMode=yes -o ConnectTimeout=30 nots "STAMP=$STAMP TAR_SHA=$SHA bash -s" < "$CAMP/ops/scaffold/pilot_submit_remote.sh" > "${EV}_submit.txt" 2>&1
echo "ssh_rc=$?" >> "${EV}_submit.txt"
cat "${EV}_submit.txt"
