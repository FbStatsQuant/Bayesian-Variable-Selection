#!/bin/bash
# make_manifests.sh -- download manifest and CLOSING of the benchmark results folder, then of the logs folder (DESIGN.md section 6; HQ D49:
# pull, verify and delete each folder as soon as it is final). Derived from PROD_L's make_manifests.sh without the P5 gates.
#   bash make_manifests.sh STAMP --piece bench [--allow-incomplete]
#   bash make_manifests.sh STAMP --piece logs                (last; needs final_accounting.sh and bench CLOSED)
# Gate: every job of the run out of squeue and terminal in sacct (scheduler error 4; not terminal 3). For bench: no stale artefact in the results
# folder (exit 2: clear_stale.sh), every case done and no exception in reconcile_bench.py (exit 6 unless --allow-incomplete, after HQ
# acknowledges). The logs folder is evidence, not results: it is not scanned for stale artefacts (archived artefacts live in LOG_RUN/cleanup).
# Writes <folder>/MANIFEST.sha256 (revalidated if present, never replaced), RUN_HOME/manifests/<piece>.CLOSED (+ bench.inventory.tsv and
# bench.exceptions.tsv, hash-bound in CLOSED) and manifests/summary.tsv. After closing, make_resubmit.sh and submit_bench.sh refuse bench.
set -euo pipefail
STAMP=${1:?usage: make_manifests.sh STAMP --piece bench|logs [--allow-incomplete]}; shift
piece=; allow=0
while (($#)); do case $1 in --piece) piece=${2:?}; shift 2;; --allow-incomplete) allow=1; shift;; *) echo "unknown option $1" >&2; exit 2;; esac; done
[[ $STAMP =~ ^[0-9]{8}T[0-9]{4}Z$ ]] || { echo "bad STAMP" >&2; exit 2; }
[[ $piece == bench || $piece == logs ]] || { echo "--piece must be bench|logs" >&2; exit 2; }
export STAMP
HERE=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd); source "$HERE/bench.env"
SQUEUE=${SQUEUE:-squeue}; SACCT=${SACCT:-sacct}; PYTHON=${PYTHON:-python3}
[[ -r $RUN_HOME/JOBIDS.tsv ]] || { echo 'missing JOBIDS' >&2; exit 3; }
ids=$(awk -F '\t' 'NR>1 {if($3 !~ /^[0-9]+$/) exit 1; print $3}' "$RUN_HOME/JOBIDS.tsv" | paste -sd, -) || exit 3
[[ -n $ids ]] || exit 3
q=$("$SQUEUE" -h -u fb31 -o '%i|%j|%T|%C') || exit 4
if printf '%s\n' "$q" | awk -F'|' -v ids="$ids" 'BEGIN{split(ids,a,",");for(i in a)x[a[i]]=1} NF{split($1,b,"_");if(x[b[1]])f=1} END{exit !f}'; then echo 'active jobs' >&2; exit 3; fi
acct=$("$SACCT" -X -n -P -j "$ids" -o JobID,State) || exit 4
printf '%s\n' "$acct" | awk -F'|' -v ids="$ids" 'BEGIN{split(ids,a,",");for(i in a)x[a[i]]=1} NF>=2{split($1,b,"_");if(x[b[1]]){seen[b[1]]=1;if($2 !~ /^(COMPLETED|FAILED|CANCELLED|TIMEOUT|OUT_OF_MEMORY|NODE_FAIL|DEADLINE|BOOT_FAIL|PREEMPTED)/)bad=1}} END{for(i in x)if(!seen[i])bad=1;exit bad}' || { echo 'accounting not terminal or missing' >&2; exit 3; }

mdir=$RUN_HOME/manifests; mkdir -p "$mdir"
incomplete=0; exception_count=0
if [[ $piece == logs ]]; then
  d=$LOG_RUN
  [[ -s $LOG_RUN/accounting/sacct_final.tsv && -s $LOG_RUN/accounting/core_hours.tsv ]] || { echo "run final_accounting.sh first" >&2; exit 2; }
  [[ -e $mdir/bench.CLOSED ]] || { echo "close the bench results folder before the logs" >&2; exit 2; }
else
  d=$SCR_ROOT/results/$RUNID_bench
fi
[[ -e $mdir/$piece.CLOSED ]] && { echo "$piece is already CLOSED ($mdir/$piece.CLOSED)" >&2; exit 2; }
[[ -d $d && ! -L $d ]] || { echo "no folder $d" >&2; exit 2; }
if [[ $piece == bench ]]; then
  source "$HERE/stale_lib.sh"
  stale=$(stale_find "$d") || { echo "stale inspection failed for $d" >&2; exit 2; }
  [[ -z $stale ]] || { echo "stale artifacts in $d: run clear_stale.sh" >&2; exit 2; }
  inv=$RUN_HOME/inventory_final
  mkdir -p "$LOG_RUN/reconcile"; diag="$LOG_RUN/reconcile/$(date -u +%Y%m%dT%H%M%SZ)_bench.out"
  rc=0; "$PYTHON" "$HERE/reconcile_bench.py" "$STAMP" --home-root "$HOME_ROOT" --scr-root "$SCR_ROOT" --lists "$LISTS/units.tsv" --out "$inv" > "$diag" 2>&1 || rc=$?
  [[ $rc == 0 || $rc == 1 || $rc == 4 ]] || { echo "reconcile_bench.py failed (exit $rc): see $diag" >&2; exit 2; }
  [[ -s $inv/inventory/bench.tsv ]] || { echo "no inventory" >&2; exit 2; }
  expected=$(awk -F'\t' 'NR>1 && $1=="bench"' "$LISTS/units.tsv" | wc -l)
  rows=$(($(wc -l < "$inv/inventory/bench.tsv") - 1))
  [[ $rows == "$expected" ]] || { echo "inventory has $rows rows, expected $expected" >&2; exit 2; }
  incomplete=$(awk -F'\t' 'NR>1 && $3 != "done"' "$inv/inventory/bench.tsv" | wc -l)
  exception_count=$(awk -F'\t' 'NR>1 && $1=="bench" {n++} END{print n+0}' "$inv/exceptions.tsv")
  if (( exception_count )); then echo "bench exceptions:" >&2; awk -F'\t' 'NR>1 && $1=="bench"' "$inv/exceptions.tsv" >&2; fi
  if (( incomplete + exception_count )) && [[ $allow != 1 ]]; then
    echo "bench has $incomplete cases not done and $exception_count exceptions: resubmit, or close with --allow-incomplete after HQ acknowledges them" >&2; exit 6
  fi
  cp "$inv/inventory/bench.tsv" "$mdir/.bench.inventory.tsv.tmp"; mv -f "$mdir/.bench.inventory.tsv.tmp" "$mdir/bench.inventory.tsv"
  awk -F'\t' 'NR==1 || $1=="bench"' "$inv/exceptions.tsv" > "$mdir/.bench.exceptions.tsv.tmp"; mv -f "$mdir/.bench.exceptions.tsv.tmp" "$mdir/bench.exceptions.tsv"
fi
if [[ -e $d/MANIFEST.sha256 ]]; then
  ( cd "$d" && sha256sum --quiet -c MANIFEST.sha256 ) || { echo "existing manifest in $d does not verify" >&2; exit 2; }
  listed=$(sed -E 's/^[0-9a-f]{64} [ *]//' "$d/MANIFEST.sha256" | LC_ALL=C sort)
  present=$( cd "$d" && find . -type f ! -name MANIFEST.sha256 | LC_ALL=C sort )
  [[ $listed == "$present" ]] || { echo "existing manifest in $d does not list exactly the files present" >&2; exit 2; }
else
  mtmp="$mdir/.MANIFEST_$piece.sha256.tmp"      # outside the folder being listed
  ( cd "$d" && find . -type f ! -name MANIFEST.sha256 -print0 | LC_ALL=C sort -z | xargs -0 -r sha256sum ) > "$mtmp"
  mv -f -- "$mtmp" "$d/MANIFEST.sha256"
fi
count=$(find "$d" -type f ! -name MANIFEST.sha256 | wc -l)
bytes=$(find "$d" -type f ! -name MANIFEST.sha256 -printf '%s\n' | awk '{s+=$1} END{printf "%.0f", s}')
hash=$(sha256sum "$d/MANIFEST.sha256" | cut -d' ' -f1)
{ echo "piece=$piece folder=$d closed_utc=$(date -u +%FT%TZ) by=$(id -un)@$(hostname)"
  echo "files=$count bytes=$bytes manifest_sha256=$hash incomplete_units=$incomplete allow_incomplete=$allow"
  if [[ $piece == bench ]]; then
    echo "inventory_sha256=$(sha256sum "$mdir/bench.inventory.tsv" | cut -d' ' -f1)"
    echo "exceptions_sha256=$(sha256sum "$mdir/bench.exceptions.tsv" | cut -d' ' -f1) acknowledged_exceptions=$exception_count"
  fi; } > "$mdir/.$piece.CLOSED.tmp"
mv -f "$mdir/.$piece.CLOSED.tmp" "$mdir/$piece.CLOSED"
summary=$mdir/summary.tsv; tmp=$mdir/.summary.tsv.tmp
{ printf 'folder\tfiles\tbytes\tmanifest_sha256\n'; [[ ! -s $summary ]] || awk -F'\t' -v d="$d" 'NR>1 && $1 != d' "$summary"; printf '%s\t%s\t%s\t%s\n' "$d" "$count" "$bytes" "$hash"; } > "$tmp"
mv -f "$tmp" "$summary"
echo "CLOSED $piece: $d ($count files, $bytes bytes, MANIFEST.sha256 $hash). It may now be pulled with nots_pull.py --delete."
