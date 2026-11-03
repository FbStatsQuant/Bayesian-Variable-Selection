#!/bin/bash
# final_archive_files_once.sh : (laptop; detached) HQ D92 sweep step 1b. The first single-file fetch (13:29-13:32Z) opened ~11 connections in a
# burst and they failed (0-byte local files; connection limit, cf. 2026-10-29). After the 15-min back-off, ONE control-lane connection: stdout =
# tar of the scratch README.md + 3 clean-up receipts (paths relative to /), stderr = their sha256 list + the PROD-H upload tar's sha256.
# Locally: extract into nots_scratch_final, sha256sum -c against the remote list, and compare the PROD-H tar hash with the local bundle copy.
# Output ops/evidence/ops_final_archive_files.txt (FILES_DONE OK / FAILED).
set -u
CAMP=/c/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign
S=$CAMP/ops/scaffold; E=$CAMP/ops/evidence; O=$E/ops_final_archive_files.txt
U="/c/Users/felip/OneDrive - Rice University/NOTS Data/New_Campaign"; T=$E/_final_files.tar; L=$E/_final_files.sha256
echo "wait for back-off from $(date -u +%FT%TZ)" > $O
sleep 960
F="scratch/fb31/New_Campaign/README.md scratch/fb31/New_Campaign/upload/cleanup_receipt_20261030T1811Z_lowp_prodL.txt scratch/fb31/New_Campaign/upload/cleanup_receipt_20261102T1311Z_lowp_bench.txt scratch/fb31/New_Campaign/upload/cleanup_receipt_20261102T2309Z_lowp_bench.txt"
NOTS_SSH_LANE=control PATH="$S/sshlock:$PATH" MSYS_NO_PATHCONV=1 ssh -o BatchMode=yes -o ConnectTimeout=30 nots "cd / && sha256sum $F scratch/fb31/New_Campaign/upload/prodH_bundle_20261030T0934Z.tar 1>&2 && tar -cf - $F" > $T 2> $L
echo "ssh_rc=$? $(date -u +%FT%TZ)" >> $O; cat $L >> $O
[ -s $T ] || { echo "FILES_DONE FAILED (empty tar)" >> $O; exit 1; }
mkdir -p $E/_final_files_x && tar -xf $T -C $E/_final_files_x || { echo "FILES_DONE FAILED (extract)" >> $O; exit 1; }
( cd $E/_final_files_x && grep -v prodH_bundle $L | sha256sum -c - ) >> $O 2>&1 || { echo "FILES_DONE FAILED (sha)" >> $O; exit 1; }
th=$(grep prodH_bundle_20261030T0934Z.tar $L | cut -c1-64)
[ "$th" = 845de40ef7286dee691cf3f2fc8a03ebd1408a9a0084ac982911c8e77df4e72e ] && echo "TAR_SAME_AS_LOCAL $th" >> $O || { echo "TAR_DIFFERS remote=$th" >> $O; echo "FILES_DONE FAILED" >> $O; exit 1; }
mkdir -p "$U/nots_scratch_final/upload"
cp $E/_final_files_x/scratch/fb31/New_Campaign/README.md "$U/nots_scratch_final/README.md"
cp $E/_final_files_x/scratch/fb31/New_Campaign/upload/cleanup_receipt_*.txt "$U/nots_scratch_final/upload/"
cp $L "$U/nots_scratch_final/SHA256SUMS_remote.txt"
( cd "$U/nots_scratch_final" && sed 's| scratch/fb31/New_Campaign/| |' SHA256SUMS_remote.txt | grep -v prodH_bundle | sha256sum -c - ) >> $O 2>&1 || { echo "FILES_DONE FAILED (final copy sha)" >> $O; exit 1; }
echo "FILES_DONE OK $(date -u +%FT%TZ)" >> $O
