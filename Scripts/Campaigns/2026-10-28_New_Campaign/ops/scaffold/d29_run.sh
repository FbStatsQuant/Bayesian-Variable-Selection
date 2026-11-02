#!/bin/bash
# d29_run.sh dry|yes OUTFILE : (laptop) ONE ssh: verify the deployed executor/list/manifest hashes on NOTS, then run the Sol-R5-accepted executor v5.1.
set -u
MODE=${1:?dry|yes}; OUT=${2:?outfile}
D=/scratch/fb31/New_Campaign/runs/ops4_d29
case "$MODE" in dry) FLAG="";; yes) FLAG=" --yes";; *) echo "mode must be dry or yes" >&2; exit 2;; esac
SUMS="24bd5a586219a8fe189b9dc584e89664cd328348ff236d9380bc1b0c5bad0fae  $D/d29_dbbackups_delete.sh
b5a2f47d5ff1537d305211b26738551e91d6fee51422f494a1e43c0c84571e9c  $D/ops4_dbbackups_delete_list.tsv
d2a67f0dd6e0a695ba5a8e92ad5788e9b540417bb6c9374500b17acddba81816  $D/archive_manifest.sha256"
MSYS_NO_PATHCONV=1 ssh -o BatchMode=yes -o ConnectTimeout=30 nots \
  "printf '%s\n' '$SUMS' | sha256sum -c - && bash $D/d29_dbbackups_delete.sh $D/ops4_dbbackups_delete_list.tsv $D/archive_manifest.sha256$FLAG; echo executor_rc=\$?" > "$OUT" 2>&1
echo "ssh_rc=$?" >> "$OUT"
grep -vE '^(WOULD-DELETE|DELETED|open-scan: skipped helper)' "$OUT"
echo "WOULD-DELETE lines: $(grep -c '^WOULD-DELETE' "$OUT")  DELETED lines: $(grep -c '^DELETED' "$OUT")"
