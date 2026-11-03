#!/bin/bash
# launch_extract.sh NEWLIST OLDLIST OUTDIR NWORKERS TAG : NWORKERS extract_h2.R workers in the background; wait. Run detached; resumable.
set -u
H2=/c/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign/analysis/H2_20261102
RS="/c/Program Files/R/R-4.4.1/bin/Rscript.exe"
NEWL=$1; OLDL=$2; OUT=$3; N=$4; TAG=$5
echo $$ > "$H2/logs/extract_$TAG.pid"
echo "$(date -u +%FT%TZ) LAUNCH $TAG new=$NEWL N=$N" >> "$H2/logs/extract_$TAG.launcher.log"
# Paths must be absolute. ALL_WORKERS_EXITED is NOT success: success = ALL_WORKERS_OK + expected file counts + no *.err (Sol R1 #7).
pids=()
for k in $(seq 1 "$N"); do
  "$RS" "$H2/scripts/extract_h2.R" "$NEWL" "$OLDL" "$OUT" "$k" "$N" >> "$H2/logs/extract_${TAG}_w$k.log" 2>&1 &
  pids+=($!)
done
bad=0; k=0
for p in "${pids[@]}"; do k=$((k+1)); wait "$p"; rc=$?; echo "$(date -u +%FT%TZ) worker $k rc=$rc" >> "$H2/logs/extract_$TAG.launcher.log"; [ $rc -eq 0 ] || bad=$((bad+1)); done
echo "$(date -u +%FT%TZ) ALL_WORKERS_EXITED $TAG failed_workers=$bad" >> "$H2/logs/extract_$TAG.launcher.log"
[ $bad -eq 0 ] && echo "$(date -u +%FT%TZ) ALL_WORKERS_OK $TAG" >> "$H2/logs/extract_$TAG.launcher.log"
