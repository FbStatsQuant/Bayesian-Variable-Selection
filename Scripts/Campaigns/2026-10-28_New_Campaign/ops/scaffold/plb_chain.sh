#!/bin/bash
# plb_chain.sh : (laptop; detached via detach_run.sh) after the pull chain and the F3 PROD cell-1 launch: (1) PROD-L cleanup_prodl.sh dry run + --yes
# (only if the PROD-L logs folder was pulled), (2) PROD_L_BENCH upload + guard 75 + stage + dry run + submit (alone), (3) exec its waiter.
set -u
CAMP=/c/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign
S=$CAMP/ops/scaffold; E=$CAMP/ops/evidence; OUT=$E/ops9_plb_chain.txt
STAMP=20261102T1311Z; RID=${STAMP}_lowp_bench
TAR="/c/Users/felip/OneDrive - Rice University/NOTS Data/New_Campaign/runs/$RID/bundle/prodLB_bundle_$STAMP.tar"
until grep -q '^PULL_LIST_DONE' $E/ops_pulls2_20261102.txt 2>/dev/null && grep -q '^ssh_rc=' $E/ops8_f3prod_cell1.txt 2>/dev/null; do sleep 60; done
{ echo "start $(date -u +%FT%TZ)"; grep '^PULL_LIST_DONE' $E/ops_pulls2_20261102.txt; } >> $OUT
if ! grep -q 'PULL /scratch/fb31/New_Campaign/logs/20261030T1811Z_lowp_prodL' $E/ops_pulls2_20261102.txt || ! grep -q '^PULL_LIST_DONE OK' $E/ops_pulls2_20261102.txt; then
  echo "STOP: PROD-L logs not pulled (D58 workaround needed) or pull chain failed: no cleanup, no BENCH submission" >> $OUT; echo "CHAIN_END STOP" >> $OUT; exit 1; fi
# (1) PROD-L clean-up (receipt outside the removed tree, on scratch)
MSYS_NO_PATHCONV=1 ssh -o BatchMode=yes -o ConnectTimeout=30 nots "export STAMP=20261030T1811Z; B=/home/fb31/projects/BVS/New_Campaign/runs/20261030T1811Z_lowp_prodL/code/prod_l; cd /scratch/fb31/New_Campaign && bash \$B/cleanup_prodl.sh 20261030T1811Z < /dev/null 2>&1 | tail -12; echo dry_rc=\${PIPESTATUS[0]}; bash \$B/cleanup_prodl.sh 20261030T1811Z --yes --receipt /scratch/fb31/New_Campaign/upload/cleanup_receipt_20261030T1811Z_lowp_prodL.txt < /dev/null 2>&1 | tail -15; echo cleanup_rc=\${PIPESTATUS[0]}" >> $OUT 2>&1
echo "cleanup_ssh_rc=$?" >> $OUT
grep -q '^cleanup_rc=0' $OUT || { echo "STOP: PROD-L cleanup not verified" >> $OUT; echo "CHAIN_END STOP" >> $OUT; exit 1; }
# (2) PROD_L_BENCH upload + submit
SHA=$(cut -c1-64 "$TAR.sha256")
MSYS_NO_PATHCONV=1 ssh -o BatchMode=yes -o ConnectTimeout=30 nots "mkdir -p /scratch/fb31/New_Campaign/upload && test ! -e /scratch/fb31/New_Campaign/upload/prodLB_bundle_$STAMP.tar && cat > /scratch/fb31/New_Campaign/upload/prodLB_bundle_$STAMP.tar && sha256sum /scratch/fb31/New_Campaign/upload/prodLB_bundle_$STAMP.tar" < "$TAR" >> $OUT 2>&1 || { echo "STOP: upload failed" >> $OUT; echo "CHAIN_END STOP" >> $OUT; exit 1; }
MSYS_NO_PATHCONV=1 ssh -o BatchMode=yes -o ConnectTimeout=30 nots "STAMP=$STAMP TAR_SHA=$SHA bash -s" < $S/plb_submit_remote.sh > $E/ops9_plb_submit.txt 2>&1
echo "submit_ssh_rc=$?" >> $E/ops9_plb_submit.txt; cat $E/ops9_plb_submit.txt >> $OUT
IDS=$(awk -F'\t' 'NR>1 && $1=="main" {print $3}' <(sed -n '/^== jobids/,$p' $E/ops9_plb_submit.txt | tail -n +2) | paste -sd, -)
echo "PLB_JOBIDS=$IDS" >> $OUT; echo "CHAIN_END SUBMITTED" >> $OUT
[ -n "$IDS" ] && exec bash $CAMP/jobs/PROD_L_BENCH/waiter.sh $E/ops9_plb_waiter.log "$IDS" 72
