#!/usr/bin/env bash
# run_queue.sh <old|new> <core_dir> <units.txt> <root>: work-claiming worker; start several instances for several cores.
# <root> holds out_old/, out_new/, claim_<mode>/ and log_<mode>.txt; env AB_GEN_DIR, AB_RERUN_FILE as in ab_run.R. The new side runs a unit only
# when the old fit exists (a line "<id> old status" in <root>/log_old.txt). Run it as a systemd unit or under setsid, at nice 19.
mode=$1; core=$2; units=$3; root=$4; here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
mkdir -p "$root/out_old" "$root/out_new" "$root/claim_$mode"; cd "$root"
while true; do
  did=0; left=0
  for u in $(grep -v '^#' "$units"); do
    id=${u#*:}; id=$(echo "$id" | sed 's/[^A-Za-z0-9_]/_/g')
    [ -d "claim_$mode/$id" ] && continue
    left=1
    if [ "$mode" = old ] || grep -q "\] $id old status" log_old.txt 2>/dev/null; then
      mkdir "claim_$mode/$id" 2>/dev/null || continue
      nice -n 19 Rscript --vanilla "$here/ab_run.R" "$mode" "$core" "$u" "$root/out_$mode" "$root/out_old" >> "log_$mode.txt" 2>&1
      did=1; break
    fi
  done
  [ $left = 0 ] && break
  [ $did = 0 ] && sleep 60
done
echo "WORKER DONE" >> "log_$mode.txt"
