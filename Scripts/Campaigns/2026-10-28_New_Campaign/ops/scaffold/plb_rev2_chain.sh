#!/bin/bash
# plb_rev2_chain.sh : (laptop; detached via detach_run.sh) PROD_L_BENCH rev 2 (HQ D85), STAMP 20261102T2309Z: (1) bulk lane: upload the staged
# tar (test ! -e on NOTS; sha256 echoed and compared); (2) control lane, detached on NOTS: plb_submit_remote_rev2.sh (no BENCH/PROD-L job,
# throttle-aware 192 ceiling, guard 75 [never overridden], tar hash, extract, STAGED_SHA256, LEDGER da08f38c… on NOTS, dry run alone, submit);
# (3) record PLB_JOBIDS and exec the bundle waiter. Status: ops9_plb_rev2_chain.txt (CHAIN_END SUBMITTED / STOP).
set -u
CAMP=/c/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign
S=$CAMP/ops/scaffold; E=$CAMP/ops/evidence; OUT=$E/ops9_plb_rev2_chain.txt
STAMP=20261102T2309Z; RID=${STAMP}_lowp_bench; LEDGER=da08f38c39d1701bcca69b5d01faeeb3315d2a7d9ca645142f941fef7fee186a
TAR="/c/Users/felip/OneDrive - Rice University/NOTS Data/New_Campaign/runs/$RID/bundle/prodLB_bundle_$STAMP.tar"
stop() { echo "STOP: $1" >> $OUT; echo "CHAIN_END STOP" >> $OUT; exit 1; }
echo "start $(date -u +%FT%TZ) STAMP=$STAMP" >> $OUT
SHA=$(cut -c1-64 "$TAR.sha256"); [ "$(sha256sum "$TAR" | cut -c1-64)" = "$SHA" ] || stop "local tar hash differs from its .sha256"
export NOTS_SSH_LOCK_WAIT_S=7200
NOTS_SSH_LANE=bulk bash $S/sshlock/with_lock.sh bash -c "MSYS_NO_PATHCONV=1 ssh -o BatchMode=yes -o ConnectTimeout=30 nots 'mkdir -p /scratch/fb31/New_Campaign/upload && test ! -e /scratch/fb31/New_Campaign/upload/prodLB_bundle_$STAMP.tar && cat > /scratch/fb31/New_Campaign/upload/prodLB_bundle_$STAMP.tar && sha256sum /scratch/fb31/New_Campaign/upload/prodLB_bundle_$STAMP.tar' < '$TAR'" >> $OUT 2>&1 || stop "upload failed"
grep -q "^$SHA " $OUT || stop "uploaded tar sha256 differs from $SHA"
echo "UPLOAD_OK $SHA" >> $OUT
NOTS_SSH_LANE=control bash $S/remote_bg.sh plb_submit_$STAMP $S/plb_submit_remote_rev2.sh $E/ops9_plb_rev2_submit.txt STAMP=$STAMP TAR_SHA=$SHA LEDGER_SHA=$LEDGER
echo "submit_bg_rc=$?" >> $E/ops9_plb_rev2_submit.txt; cat $E/ops9_plb_rev2_submit.txt >> $OUT
IDS=$(awk -F'\t' 'NR>1 && $1=="main" {print $3}' <(sed -n '/^== jobids/,$p' $E/ops9_plb_rev2_submit.txt | tail -n +2) | paste -sd, -)
[ -n "$IDS" ] || stop "no job ids (see ops9_plb_rev2_submit.txt)"
echo "PLB_JOBIDS=$IDS" >> $OUT; echo "CHAIN_END SUBMITTED" >> $OUT
export NOTS_SSH_LANE=control
exec bash $CAMP/jobs/PROD_L_BENCH/waiter.sh $E/ops9_plb_rev2_waiter.log "$IDS" 72
