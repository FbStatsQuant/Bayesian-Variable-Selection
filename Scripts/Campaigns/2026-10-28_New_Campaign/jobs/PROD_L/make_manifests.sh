#!/bin/bash
# make_manifests.sh -- per-folder download manifests and piece CLOSING (DESIGN section 8; HQ D49: pull, verify and delete each piece's folder as
# soon as that piece is final).
#   bash make_manifests.sh STAMP --piece enum20|enum30|smc|smcrep [--allow-incomplete]     close one result piece
#   bash make_manifests.sh STAMP --piece logs                                              the logs folder (last; needs final accounting)
# Gate (all forms): every job of the run is out of squeue and terminal in sacct (scheduler error: exit 4; not terminal: exit 3); no *.lock or
# *.tmp* artefact in the folder (exit 2: run clear_stale.sh).
# A result piece is closed only if reconcile_prodl.py reports EVERY expected unit of that piece `done` (else exit 6), unless --allow-incomplete
# is given for units HQ has acknowledged as exceptions (the non-done units are then listed in the closing record). Closing writes
#   <folder>/MANIFEST.sha256 (every file, relative paths; an existing manifest is revalidated, never replaced),
#   RUN_HOME/manifests/<piece>.CLOSED (utc, files, bytes, manifest sha256, incomplete count) and <piece>.inventory.tsv (the piece's inventory at
#   closing: the authoritative record once the folder has left scratch), and updates RUN_HOME/manifests/summary.tsv.
# After closing, make_resubmit.sh and submit_prodl.sh refuse the piece: its folder may be pulled and deleted (ops/transfer/nots_pull.py --delete).
# Exit 0 = manifest written/verified and piece closed.
set -euo pipefail
STAMP=${1:?usage: make_manifests.sh STAMP --piece PIECE [--allow-incomplete]}; shift
piece=; allow=0
while (($#)); do case $1 in --piece) piece=${2:?}; shift 2;; --allow-incomplete) allow=1; shift;; *) echo "unknown option $1" >&2; exit 2;; esac; done
[[ $STAMP =~ ^[0-9]{8}T[0-9]{4}Z$ ]] || { echo "bad STAMP" >&2; exit 2; }
[[ $piece == enum20 || $piece == enum30 || $piece == smc || $piece == smcrep || $piece == logs ]] || { echo "--piece must be enum20|enum30|smc|smcrep|logs" >&2; exit 2; }
export STAMP
HERE=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd); source "$HERE/prodl.env"
SQUEUE=${SQUEUE:-squeue}; SACCT=${SACCT:-sacct}; PYTHON=${PYTHON:-python3}
# ---- gate: the whole run is idle and terminal ------------------------------------------------------------------------------
[[ -r $RUN_HOME/JOBIDS.tsv ]] || { echo 'missing JOBIDS' >&2; exit 3; }
ids=$(awk -F '\t' 'NR>1 {if($3 !~ /^[0-9]+$/) exit 1; print $3}' "$RUN_HOME/JOBIDS.tsv" | paste -sd, -) || exit 3
[[ -n $ids ]] || exit 3
q=$("$SQUEUE" -h -u fb31 -o '%i|%j|%T|%C') || exit 4
if printf '%s\n' "$q" | awk -F'|' -v ids="$ids" 'BEGIN{split(ids,a,",");for(i in a)x[a[i]]=1} NF{split($1,b,"_");if(x[b[1]])f=1} END{exit !f}'; then echo 'active jobs' >&2; exit 3; fi
acct=$("$SACCT" -X -n -P -j "$ids" -o JobID,State) || exit 4
printf '%s\n' "$acct" | awk -F'|' -v ids="$ids" 'BEGIN{split(ids,a,",");for(i in a)x[a[i]]=1} NF>=2{split($1,b,"_");if(x[b[1]]){seen[b[1]]=1;if($2 !~ /^(COMPLETED|FAILED|CANCELLED|TIMEOUT|OUT_OF_MEMORY|NODE_FAIL|DEADLINE|BOOT_FAIL|PREEMPTED)/)bad=1}} END{for(i in x)if(!seen[i])bad=1;exit bad}' || { echo 'accounting not terminal or missing' >&2; exit 3; }

mdir=$RUN_HOME/manifests; mkdir -p "$mdir"
if [[ $piece == logs ]]; then
  d=$LOG_RUN
  [[ -s $LOG_RUN/accounting/sacct_final.tsv && -s $LOG_RUN/accounting/core_hours.tsv ]] || { echo "run final_accounting.sh first" >&2; exit 2; }
  for p in enum20 enum30 smc smcrep; do [[ -e $mdir/$p.CLOSED ]] || { echo "close every result piece before the logs (missing $p.CLOSED)" >&2; exit 2; }; done
else
  rv=RUNID_$piece; d=$SCR_ROOT/results/${!rv}
fi
[[ -e $mdir/$piece.CLOSED ]] && { echo "$piece is already CLOSED ($mdir/$piece.CLOSED)" >&2; exit 2; }
[[ -d $d && ! -L $d ]] || { echo "no folder $d" >&2; exit 2; }
source "$HERE/stale_lib.sh"
# the logs folder is evidence, not results: clear_stale.sh archives artefacts INTO LOG_RUN/cleanup/, and an interrupted ledger write may leave a
# hidden temporary file; neither may block closing the logs (post-READY fix, found while building PROD_L_BENCH). Result pieces are scanned as before.
if [[ $piece != logs ]]; then
  stale=$(stale_find "$d") || { echo "stale inspection failed for $d" >&2; exit 2; }
  if [[ -n $stale ]]; then echo "stale artifacts in $d: run clear_stale.sh" >&2; exit 2; fi
fi

# ---- completeness (result pieces) --------------------------------------------------------------------------------------------
incomplete=0; p5ok=1
if [[ $piece != logs ]]; then
  inv=$RUN_HOME/inventory_final
  mkdir -p "$LOG_RUN/reconcile"; diag="$LOG_RUN/reconcile/$(date -u +%Y%m%dT%H%M%SZ)_$piece.out"
  rc=0; "$PYTHON" "$HERE/reconcile_prodl.py" "$STAMP" --home-root "$HOME_ROOT" --scr-root "$SCR_ROOT" --lists "$LISTS/units.tsv" --out "$inv" > "$diag" 2>&1 || rc=$?
  [[ $rc == 0 || $rc == 1 || $rc == 4 ]] || { echo "reconcile_prodl.py failed (exit $rc): see $diag" >&2; exit 2; }
  [[ -s $inv/inventory/$piece.tsv ]] || { echo "no inventory for $piece" >&2; exit 2; }
  incomplete=$(awk -F'\t' 'NR>1 && $3 != "done"' "$inv/inventory/$piece.tsv" | wc -l)
  expected=$(awk -F'\t' -v p="$piece" 'NR>1 && $1==p' "$LISTS/units.tsv" | wc -l)
  rows=$(($(wc -l < "$inv/inventory/$piece.tsv") - 1))
  [[ $rows == "$expected" ]] || { echo "inventory has $rows rows, expected $expected" >&2; exit 2; }
  if [[ $piece == smc || $piece == smcrep ]]; then
    p5ok=0
    if [[ -f $RUN_HOME/p5/expected.tsv && -f $inv/inventory/p5.tsv ]]; then
      p5ok=1
      awk -F'\t' -v p="$piece" 'NR==FNR {if(NR>1 && $7==p) wanted[$3]=1; next} FNR>1 && ($2 in wanted) {seen[$2]=1; if($3!="done")bad=1} END{for(u in wanted)if(!(u in seen))bad=1; exit bad}' "$RUN_HOME/p5/expected.tsv" "$inv/inventory/p5.tsv" || p5ok=0
      if ! "$PYTHON" - "$HERE" "$RUN_HOME" "$LOG_RUN" "$inv" "$piece" <<'PY'
import csv, pathlib, sys
sys.path.insert(0, sys.argv[1])
from reconcile_prodl import scan_phases, scan_table
home, logs, inv, piece = pathlib.Path(sys.argv[2]), pathlib.Path(sys.argv[3]), pathlib.Path(sys.argv[4]), sys.argv[5]
try:
 with (home/'JOBIDS.tsv').open(newline='') as f:
  fits=[int(r[2]) for r in csv.reader(f,delimiter='\t') if len(r)>=3 and r[1].startswith(('s1_','s2_','s3_','s4_')) and r[2].isdigit()]
 phases=[(i,p) for i,p in scan_phases(home,logs) if p.startswith('final') and i>max(fits,default=0)]
 if not phases: raise ValueError('missing final scan newer than all fitting jobs')
 phase=phases[-1][1]
 scans=scan_table(logs/'p5'/('scan_'+phase+'_'+piece+'.tsv'),piece)
 with (inv/'inventory'/(piece+'.tsv')).open(newline='') as f:
  done={r['unit'] for r in csv.DictReader(f,delimiter='\t') if r['outcome']=='done'}
 with (home/'p5'/'expected.tsv').open(newline='') as f:
  expected={r['unit'] for r in csv.DictReader(f,delimiter='\t') if r['base_piece']==piece}
 seen=set(); violations=[]
 for r in scans:
  unit=r['case_id']+('_rep'+r['repeat_m'] if piece=='smcrep' else '')
  seen.add(unit)
  if r['primary_v3_status']=='resource_limit':
   if unit not in expected: violations.append('unlisted resource_limit: '+unit)
   if r['retry_state'] in ('locked','incomplete','invalid_inspect'): violations.append('unsafe retry: '+unit+' '+r['retry_state'])
   if r['retry_state'] != 'done': violations.append('unfinished retry: '+unit)
 if done != seen:
  violations.append('missing scan rows: '+str(sorted(done-seen))+'; scan rows not done: '+str(sorted(seen-done)))
 if violations: raise ValueError('; '.join(violations))
except (OSError, ValueError, KeyError, csv.Error) as e:
 print('P5 final scan gate: '+str(e),file=sys.stderr); sys.exit(1)
PY
      then p5ok=0; fi
    fi
    if (( !p5ok )); then incomplete=$((incomplete+1)); echo "P5 closure requirements incomplete" >&2; fi
  fi
  exception_count=$(awk -F'\t' -v p="$piece" 'NR>1 && $1==p {n++} END{print n+0}' "$inv/exceptions.tsv")
  if (( exception_count )); then
    echo "$piece exceptions:" >&2
    awk -F'\t' -v p="$piece" 'NR>1 && $1==p {print}' "$inv/exceptions.tsv" >&2
    incomplete=$((incomplete+exception_count))
  fi
  if [[ $incomplete != 0 && $allow != 1 ]]; then echo "$piece has $incomplete units not done: resubmit, or close with --allow-incomplete after HQ acknowledges them" >&2; exit 6; fi
  cp "$inv/inventory/$piece.tsv" "$mdir/.$piece.inventory.tsv.tmp"; mv -f "$mdir/.$piece.inventory.tsv.tmp" "$mdir/$piece.inventory.tsv"
  awk -F'\t' -v p="$piece" 'NR==1 || $1==p' "$inv/exceptions.tsv" > "$mdir/$piece.exceptions.tsv"
  if [[ $piece == smc || $piece == smcrep ]] && [[ -f $inv/inventory/p5.tsv ]]; then
    "$PYTHON" - "$RUN_HOME/p5/expected.tsv" "$inv/inventory/p5.tsv" "$piece" "$mdir/$piece.p5.tsv" <<'PY'
import csv, sys
with open(sys.argv[1],newline='') as f: wanted={r['unit'] for r in csv.DictReader(f,delimiter='\t') if r['base_piece']==sys.argv[3]}
with open(sys.argv[2],newline='') as f: rows=[r for r in csv.DictReader(f,delimiter='\t') if r['unit'] in wanted]
with open(sys.argv[4],'w',newline='') as f:
 w=csv.DictWriter(f,['piece','unit','outcome','detail'],delimiter='\t',lineterminator='\n'); w.writeheader(); w.writerows(rows)
PY
  fi
fi

# ---- manifest -------------------------------------------------------------------------------------------------------------------
if [[ -e $d/MANIFEST.sha256 ]]; then
  ( cd "$d" && sha256sum --quiet -c MANIFEST.sha256 ) || { echo "existing manifest in $d does not verify" >&2; exit 2; }
  listed=$(sed -E 's/^[0-9a-f]{64} [ *]//' "$d/MANIFEST.sha256" | LC_ALL=C sort)
  present=$( cd "$d" && find . -type f ! -name MANIFEST.sha256 | LC_ALL=C sort )
  [[ $listed == "$present" ]] || { echo "existing manifest in $d does not list exactly the files present" >&2; exit 2; }
else
  # the temporary manifest lives OUTSIDE the folder being listed (in RUN_HOME/manifests), so find can never list it (tester finding MM21/28/31)
  mtmp="$mdir/.MANIFEST_$piece.sha256.tmp"
  ( cd "$d" && find . -type f ! -name MANIFEST.sha256 -print0 | LC_ALL=C sort -z | xargs -0 -r sha256sum ) > "$mtmp"
  mv -f -- "$mtmp" "$d/MANIFEST.sha256"
fi
count=$(find "$d" -type f ! -name MANIFEST.sha256 | wc -l)
bytes=$(find "$d" -type f ! -name MANIFEST.sha256 -printf '%s\n' | awk '{s+=$1} END{printf "%.0f", s}')
hash=$(sha256sum "$d/MANIFEST.sha256" | cut -d' ' -f1)
{ echo "piece=$piece folder=$d closed_utc=$(date -u +%FT%TZ) by=$(id -un)@$(hostname)"
  echo "files=$count bytes=$bytes manifest_sha256=$hash incomplete_units=$incomplete allow_incomplete=$allow"
  [[ $piece == logs ]] || echo "inventory_sha256=$(sha256sum "$mdir/$piece.inventory.tsv" | cut -d' ' -f1)"
  [[ $piece == logs ]] || echo "exceptions_sha256=$(sha256sum "$mdir/$piece.exceptions.tsv" | cut -d' ' -f1) acknowledged_exceptions=$exception_count"
  if (( !p5ok )); then
    echo "p5_gate=incomplete"
    if [[ -f $inv/inventory/p5.tsv ]]; then awk -F'\t' 'NR>1 && $3!="done" {print "p5_exception=" $2 " outcome=" $3 " detail=" $4}' "$inv/inventory/p5.tsv"; fi
  fi
  if [[ -f $mdir/$piece.p5.tsv ]]; then echo "p5_inventory_sha256=$(sha256sum "$mdir/$piece.p5.tsv" | cut -d' ' -f1)"; fi; } > "$mdir/.$piece.CLOSED.tmp"
mv -f "$mdir/.$piece.CLOSED.tmp" "$mdir/$piece.CLOSED"
summary=$mdir/summary.tsv; tmp=$mdir/.summary.tsv.tmp
{ printf 'folder\tfiles\tbytes\tmanifest_sha256\n'; [[ ! -s $summary ]] || awk -F'\t' -v d="$d" 'NR>1 && $1 != d' "$summary"; printf '%s\t%s\t%s\t%s\n' "$d" "$count" "$bytes" "$hash"; } > "$tmp"
mv -f "$tmp" "$summary"
echo "CLOSED $piece: $d ($count files, $bytes bytes, MANIFEST.sha256 $hash). It may now be pulled with nots_pull.py --delete."
