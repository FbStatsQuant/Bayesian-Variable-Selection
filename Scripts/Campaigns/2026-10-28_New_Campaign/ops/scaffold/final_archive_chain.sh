#!/bin/bash
# final_archive_chain.sh : (laptop; detached via detach_run.sh) HQ D92 final NOTS sweep, step 1 = ARCHIVE ONLY (no deletion):
# (a) bulk lane, copy-pulls (nots_pull, VERIFIED receipts) of every campaign folder on NOTS into fresh local folders
#     NOTS Data\New_Campaign\nots_home_final\<sub>\<name> and nots_scratch_final\upload\ops_bg;
# (b) control lane, the single files (home README.md, scratch README.md, 3 clean-up receipts): remote sha256 + cat, local sha compare;
#     the PROD-H upload tar is not copied (identical bytes already local: bundle\prodH_bundle_20261030T0934Z.tar 845de40e…) - its remote sha is
#     compared instead. Output ops/evidence/ops_final_archive.txt (ARCHIVE_DONE OK / FAILED).
set -u
CAMP=/c/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign
S=$CAMP/ops/scaffold; E=$CAMP/ops/evidence; O=$E/ops_final_archive.txt
W='C:\Users\felip\OneDrive - Rice University\NOTS Data\New_Campaign'; U="/c/Users/felip/OneDrive - Rice University/NOTS Data/New_Campaign"
H=/home/fb31/projects/BVS/New_Campaign; SC=/scratch/fb31/New_Campaign
export NOTS_SSH_LOCK_WAIT_S=7200
echo "start $(date -u +%FT%TZ)" > $O
bash $S/pull_list.sh $E/ops_final_archive_pulls.txt \
  "$H/code/core|keep|$W\\nots_home_final\\code\\core" "$H/code/v2_2|keep|$W\\nots_home_final\\code\\v2_2" \
  "$H/code/bench_v2|keep|$W\\nots_home_final\\code\\bench_v2" "$H/code/ops|keep|$W\\nots_home_final\\code\\ops" \
  "$H/jobs/CONF_NOTS_IDENTITY|keep|$W\\nots_home_final\\jobs\\CONF_NOTS_IDENTITY" \
  "$H/runs/20261030T0934Z_prodH|keep|$W\\nots_home_final\\runs\\20261030T0934Z_prodH" \
  "$SC/upload/ops_bg|keep|$W\\nots_scratch_final\\upload\\ops_bg"
grep -q '^PULL_LIST_DONE OK' $E/ops_final_archive_pulls.txt || { echo "folder pulls FAILED (see ops_final_archive_pulls.txt)" >> $O; echo "ARCHIVE_DONE FAILED" >> $O; exit 1; }
echo "folders: 7 pulls VERIFIED" >> $O
export NOTS_SSH_LANE=control
fetch() {   # fetch REMOTE LOCALFILE : remote sha256, cat, local compare
  local r=$1 l=$2 rs ls_
  mkdir -p "$(dirname "$l")"
  rs=$(MSYS_NO_PATHCONV=1 ssh -o BatchMode=yes -o ConnectTimeout=30 nots "sha256sum '$r'" | cut -c1-64) || return 1
  MSYS_NO_PATHCONV=1 ssh -o BatchMode=yes -o ConnectTimeout=30 nots "cat '$r'" > "$l" || return 1
  ls_=$(sha256sum "$l" | cut -c1-64)
  [ -n "$rs" ] && [ "$rs" = "$ls_" ] && echo "FILE_OK $r $rs" >> $O || { echo "FILE_MISMATCH $r remote=$rs local=$ls_" >> $O; return 1; }
}
ok=1
fetch $H/README.md "$U/nots_home_final/README.md" || ok=0
fetch $SC/README.md "$U/nots_scratch_final/README.md" || ok=0
for f in cleanup_receipt_20261030T1811Z_lowp_prodL.txt cleanup_receipt_20261102T1311Z_lowp_bench.txt cleanup_receipt_20261102T2309Z_lowp_bench.txt; do
  fetch $SC/upload/$f "$U/nots_scratch_final/upload/$f" || ok=0; done
rs=$(MSYS_NO_PATHCONV=1 ssh -o BatchMode=yes -o ConnectTimeout=30 nots "sha256sum '$SC/upload/prodH_bundle_20261030T0934Z.tar'" | cut -c1-64)
[ "$rs" = 845de40ef7286dee691cf3f2fc8a03ebd1408a9a0084ac982911c8e77df4e72e ] && echo "TAR_SAME_AS_LOCAL $rs (local runs\\20261030T0934Z_prodH\\bundle\\prodH_bundle_20261030T0934Z.tar)" >> $O || { echo "TAR_DIFFERS remote=$rs" >> $O; ok=0; }
[ $ok = 1 ] && echo "ARCHIVE_DONE OK $(date -u +%FT%TZ)" >> $O || echo "ARCHIVE_DONE FAILED" >> $O
