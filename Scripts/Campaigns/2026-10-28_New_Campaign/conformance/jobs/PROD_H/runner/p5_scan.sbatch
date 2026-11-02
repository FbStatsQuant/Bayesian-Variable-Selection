#!/bin/bash
# p5_scan.sbatch -- the frozen tools/p5_scan.R as a guarded SINGLE-CPU compute job (Sol review 2, R2-4). Submitted by p5_scan_run.sh only:
#   sbatch ... p5_scan.sbatch RUN_DIR primary|final
# Why a job: the scanner hashes AND deserializes every primary RDS (about 2,400 files, about 4 GB) in both directions (CSV vs RDS native status);
# that is minutes of CPU, not a metadata scan, so it never runs on the login node. Sapphire Rapids is NOT required (no compiled core is run).
# Resource estimate (explicit, set in p5_scan_run.sh): about 0.2 s of readRDS per record + hashing about 4 GB + CLI start, i.e. 10 to 20 minutes on
# one CPU; one record is held at a time (a few tens of MB), so 4G is ample; wall 01:00:00 is a ceiling of about 3x the estimate.
# The job writes RUN_DIR/p5_scan_<phase>.tsv (the scanner's own atomic write) and then, ONLY after verifying it, the immutable completion receipt
# RUN_DIR/p5_scan_<phase>.receipt (noclobber, written atomically): phase, job, host, utc, wall, table sha256, row count, the scanner's summary line.
# p5_submit.sh selects units only from a table whose receipt verifies. Logs: LOGROOT/p5_scan/ and LOGROOT/slurm/ (scratch). It reads results
# only (no truth), changes nothing under results/, and never overwrites an existing table or receipt.
set -euo pipefail
RUN_DIR=$(realpath "$1"); PHASE=${2:-}
[[ $PHASE == primary || $PHASE == final ]] || { echo "FATAL: usage: p5_scan.sbatch RUN_DIR primary|final" >&2; exit 64; }
[[ -n ${SLURM_JOB_ID:-} && ${SLURM_CPUS_PER_TASK:-} == 1 ]] || { echo "FATAL: not a 1-CPU Slurm job" >&2; exit 65; }
source "$RUN_DIR/config.env"        # RUN_ID CODE SUMS STUDY OUTROOT LOGROOT RUNNER ...
source "$RUNNER/env.sh"
source "$RUNNER/frozen_check.sh"
source "$RUNNER/common.sh"
RES_RUN=$OUTROOT/results/$RUN_ID
OUT=$RUN_DIR/p5_scan_$PHASE.tsv; REC=$RUN_DIR/p5_scan_$PHASE.receipt
SL=$LOGROOT/p5_scan; mkdir -p "$SL"
LOG=$SL/scan_${PHASE}_${SLURM_JOB_ID}.log
[[ ! -e $OUT && ! -e $REC ]] || { echo "FATAL: $OUT or its receipt already exists: a scan table is never overwritten" >&2; exit 65; }
[[ -d $RES_RUN ]] || { echo "FATAL: no results folder $RES_RUN" >&2; exit 65; }
nc_check_frozen "$CODE" "$SUMS" || { echo "FATAL: the v2.2.1 tree is not the frozen one" >&2; exit 67; }
nc_cache_ready "$CODE" "$RUN_DIR" || { echo "FATAL: compile cache not READY" >&2; exit 66; }
t0=$(date +%s); start_utc=$(nc_utc)
rc=0
Rscript --vanilla "$CODE/tools/p5_scan.R" --run-dir "$RES_RUN" --out "$OUT" > "$LOG" 2>&1 || rc=$?
[[ $rc == 0 && -s $OUT ]] || { echo "FATAL: p5_scan.R exited $rc or wrote no table (see $LOG)" >&2; exit 70; }
summary=$(grep -a '^p5_scan units=' "$LOG" | tail -n 1 || true)
[[ -n $summary ]] || { echo "FATAL: p5_scan.R printed no summary line (see $LOG)" >&2; exit 71; }
for f in units primary_resource_limit eligible retried retry_outcomes incomplete launchable locked invalid_inspect; do
  [[ $summary == *" $f="* ]] || { echo "FATAL: summary line lacks $f=: $summary" >&2; exit 71; }
done
rows=$(( $(wc -l < "$OUT") - 1 )); units=$(sed -n 's/^p5_scan units=\([0-9]*\) .*/\1/p' <<< "$summary")
[[ $units == "$rows" ]] || { echo "FATAL: summary says units=$units but the table has $rows rows" >&2; exit 72; }
header=$(head -n 1 "$OUT")
for c in case_id base primary_v3_status retry_state retry_problem retry_artefacts eligible launchable; do
  [[ $'\t'$header$'\t' == *$'\t'$c$'\t'* ]] || { echo "FATAL: the scan table lacks column $c" >&2; exit 73; }
done
( set -C
  { echo "phase $PHASE"; echo "job $SLURM_JOB_ID"; echo "host $(hostname -s)"; echo "started_utc $start_utc"; echo "finished_utc $(nc_utc)"
    echo "wall_s $(( $(date +%s) - t0 ))"; echo "scanner_exit 0"; echo "table $(basename "$OUT")"; echo "table_sha256 $(sha256sum "$OUT" | cut -d' ' -f1)"
    echo "rows $rows"; echo "log $LOG"; echo "summary $summary"; } > "$REC.tmp.$SLURM_JOB_ID" ) || { echo "FATAL: cannot write the completion receipt" >&2; exit 74; }
mv "$REC.tmp.$SLURM_JOB_ID" "$REC"
echo "p5 scan $PHASE OK: $rows rows, receipt $REC"
