#!/bin/bash
# launch_theory.sh LIST OUTDIR NWORKERS TD TAG : start NWORKERS theory_runner.R workers in the background and wait for all.
# Run detached (PowerShell Start-Process hidden bash). Resumable: rerun the same command; finished cases are skipped.
set -u
H2=/c/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign/analysis/H2_20261102
RS="/c/Program Files/R/R-4.4.1/bin/Rscript.exe"
LIST=$1; OUT=$2; N=$3; TD=$4; TAG=$5
echo $$ > "$H2/logs/theory_$TAG.pid"
echo "$(date -u +%FT%TZ) LAUNCH $TAG list=$LIST td=$TD N=$N" >> "$H2/logs/theory_$TAG.launcher.log"
# LIST and OUT must be absolute paths. ALL_WORKERS_EXITED is NOT success: success = ALL_WORKERS_OK + expected row count + no *.err (Sol R1 #7).
pids=()
for k in $(seq 1 "$N"); do
  "$RS" "$H2/scripts/theory_runner.R" "$LIST" "$OUT" "$k" "$N" "$TD" >> "$H2/logs/theory_${TAG}_w$k.log" 2>&1 &
  pids+=($!)
done
bad=0; k=0
for p in "${pids[@]}"; do k=$((k+1)); wait "$p"; rc=$?; echo "$(date -u +%FT%TZ) worker $k rc=$rc" >> "$H2/logs/theory_$TAG.launcher.log"; [ $rc -eq 0 ] || bad=$((bad+1)); done
echo "$(date -u +%FT%TZ) ALL_WORKERS_EXITED $TAG failed_workers=$bad" >> "$H2/logs/theory_$TAG.launcher.log"
[ $bad -eq 0 ] && echo "$(date -u +%FT%TZ) ALL_WORKERS_OK $TAG" >> "$H2/logs/theory_$TAG.launcher.log"
