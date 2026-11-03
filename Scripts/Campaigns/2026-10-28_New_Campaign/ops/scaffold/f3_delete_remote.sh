#!/bin/bash
# f3_delete_remote.sh : (NOTS; started detached by remote_bg.sh, control lane) delete the 8 F3 dev+prod scratch folders listed in
# ops/F3_DELETION_LIST_20261102.md (Sol-reviewed), each with remote_pack.sh delete <folder> <receipt transfer-manifest sha>; stop at the first
# failure; then rmdir the two empty results parents. Run only when no fb31 job is queued/running (remote_pack refuses otherwise).
set -uo pipefail
cd /scratch/fb31/New_Campaign || { echo "cd failed"; exit 2; }
RP=/home/fb31/projects/BVS/New_Campaign/code/ops/remote_pack.sh
q=$(squeue -h -u fb31 -o '%i %j %T') || { echo "squeue failed"; exit 2; }
[ -z "$q" ] || { echo "REFUSED: fb31 jobs queued/running: $q"; exit 3; }
LIST=(
"/scratch/fb31/New_Campaign/results/20261102T1252Z_bench_f3v2_prod/p0500 344d2713c11b651d1b1df3717da014f6f9f50aac5477ce3b2638ff494a324137"
"/scratch/fb31/New_Campaign/results/20261102T1252Z_bench_f3v2_prod/p1000 d13f0dd38bc58d07f14e8339bef8cc39d1810099951b89a49db861e8c7a77381"
"/scratch/fb31/New_Campaign/logs/20261102T1252Z_bench_f3v2_prod 4f69ac3258e85e431f2f3a0a81b0667454353747a20ecb3f3d48f3cec0a6d1e5"
"/scratch/fb31/New_Campaign/upload/20261102T1252Z_bench_f3v2_prod 17cb83e6045f0316e373106cd4da55c462c1e1e3597878dbf599b41a29f0b3fd"
"/scratch/fb31/New_Campaign/results/20261030T1855Z_bench_f3v2_dev/p0500 f79623e9c9d6f4fbaca15c2f88a8548ef573f3e9f5926fb1eb7b3d8596e2dd27"
"/scratch/fb31/New_Campaign/results/20261030T1855Z_bench_f3v2_dev/p1000 f40fbe059dcfae37509e73250c79bdc37015a5fa3ed50a4a735379bc71a2a616"
"/scratch/fb31/New_Campaign/logs/20261030T1855Z_bench_f3v2_dev 2b07896a8aa3cf82abddc998d3709bc4ee97006826b7405e91767f91a6a87ae6"
"/scratch/fb31/New_Campaign/upload/20261030T1855Z_bench_f3v2_dev 171118367cd3207bc643a9886d17e528da17ee1c858be7ebeedd51dd7fdf3dfa"
)
for row in "${LIST[@]}"; do
  set -- $row; d=$1; sha=$2
  echo "== $(date -u +%FT%TZ) DELETE $d"
  out=$(bash $RP delete "$d" "$sha" < /dev/null 2>&1); rc=$?
  printf '%s\n' "$out" | tail -3
  [ $rc -eq 0 ] && [ ! -e "$d" ] || { echo "STOP: delete failed for $d (rc=$rc)"; exit 4; }
  echo "deleted_rc=0 $d"
done
for p in /scratch/fb31/New_Campaign/results/20261102T1252Z_bench_f3v2_prod /scratch/fb31/New_Campaign/results/20261030T1855Z_bench_f3v2_dev; do
  if [ -d "$p" ]; then rmdir -- "$p" && echo "RMDIR $p" || { echo "STOP: $p not empty: $(ls -A "$p" | head)"; exit 5; }; fi
done
echo "== remaining entries for these runs (must be none)"
ls -d /scratch/fb31/New_Campaign/{results,logs,upload}/*20261102T1252Z_bench_f3v2_prod* /scratch/fb31/New_Campaign/{results,logs,upload}/*20261030T1855Z_bench_f3v2_dev* 2>/dev/null || echo "(none)"
echo "F3_DELETE_DONE $(date -u +%FT%TZ)"
