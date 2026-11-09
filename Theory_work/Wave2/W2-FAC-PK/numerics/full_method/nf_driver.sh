#!/bin/bash
# Runs the grid, one Rscript per fit, 1200 s wall-clock timeout each. Usage: NF_HOURS=1000 bash nf_driver.sh
export PATH="/c/rtools45/usr/bin:/c/rtools45/x86_64-w64-mingw32.static.posix/bin:$PATH"
unset R_LIBS_USER
export R_LIBS="C:/Users/felip/AppData/Local/R/win-library/4.6"
RS="/c/Users/felip/AppData/Local/Programs/R/R-4.6.1/bin/Rscript"
D="$(cd "$(dirname "$0")" && pwd)"
LOG="${NF_LOG:-$D/nf_log.txt}"
for cell in "600 450 5" "600 570 5" "1200 1100 3" "2000 1900 2"; do
  set -- $cell
  for rep in $(seq 1 $3); do
    s=$(date +%s)
    timeout 1200 "$RS" "$D/nf_run.R" $1 $2 $rep ${NF_HOURS:-1000} >> "$LOG" 2>&1
    rc=$?; e=$(( $(date +%s) - s ))
    if [ $rc -ne 0 ]; then
      echo "n=$1 p=$2 rep=$rep rc=$rc after ${e}s (124 = 1200 s timeout)" | tee -a "$LOG"
      echo "{\"n\":$1,\"p\":$2,\"rep\":$rep,\"status\":\"driver_rc_$rc\",\"elapsed_sec\":$e}" >> "$D/NF_raw.jsonl"
    fi
  done
done
echo ALL_DONE >> "$LOG"
