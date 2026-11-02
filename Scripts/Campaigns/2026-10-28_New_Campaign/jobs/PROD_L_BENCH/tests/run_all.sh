#!/bin/bash
# run_all.sh WORKDIR -- runs every PROD_L_BENCH acceptance suite one after the other (only test_accept.sh starts R, one process at a time; the 8-process cap is respected).
#   Each suite: stdout+stderr -> WORKDIR/<suite>.log, exit status -> WORKDIR/<suite>.rc, scratch in WORKDIR/w_<suite>.
#   Then WORKDIR/SUMMARY.txt (tab separated: suite, rc, passed, failed). Exit status 0 iff every suite exited 0.
#   WORKDIR must lie under C:/Users/felip/AppData/Local/Temp/prodl_tests/ ; run it as:  bash <B>/tests/run_all.sh C:/Users/felip/AppData/Local/Temp/prodl_tests/run1
HERE=$(cd "$(dirname "$0")" && pwd)
WD=${1:?usage: run_all.sh WORKDIR}
WM=$(cygpath -m "$WD" 2>/dev/null || echo "$WD"); WM=${WM,,}
case "$WM" in c:/users/felip/appdata/local/temp/prodl_tests/?*) ;; *) echo "REFUSED: WORKDIR must be under C:/Users/felip/AppData/Local/Temp/prodl_tests" >&2; exit 64;; esac
case "$WM" in *..*) echo "REFUSED: WORKDIR contains .." >&2; exit 64;; esac
WD=$(cygpath -u "$WD" 2>/dev/null || echo "$WD")
mkdir -p "$WD"
SUITES="test_lists.py test_ceiling.py test_waiter.sh test_jobmd.sh test_deadline.sh test_resubmit.sh test_manifests.sh test_cleanup.sh test_collect.sh test_retune.sh test_reconcile.py test_accept.sh test_stage_guard.sh test_driver.sh"
SUMMARY="$WD/SUMMARY.txt"; printf 'suite\trc\tpassed\tfailed\n' > "$SUMMARY"
ANYFAIL=0
for s in $SUITES; do
  name=${s%.*}; log="$WD/$name.log"; rcf="$WD/$name.rc"; scratch="$WD/w_$name"
  echo "== $s -> $log"
  if [ ! -f "$HERE/$s" ]; then echo "missing suite file $s" > "$log"; echo 127 > "$rcf"
  else
    case "$s" in
      *.py) py -3 -I "$(cygpath -m "$HERE/$s")" "$(cygpath -m "$scratch")" > "$log" 2>&1; rc=$?;;
      *)    bash "$HERE/$s" "$scratch" > "$log" 2>&1; rc=$?;;
    esac
    echo "$rc" > "$rcf"
  fi
  rc=$(cat "$rcf")
  line=$(grep -E '[0-9]+ passed, [0-9]+ failed' "$log" | tail -n 1)
  passed=$(printf '%s' "$line" | sed -n 's/.*[^0-9]\([0-9][0-9]*\) passed, \([0-9][0-9]*\) failed.*/\1/p'); failed=$(printf '%s' "$line" | sed -n 's/.*[^0-9]\([0-9][0-9]*\) passed, \([0-9][0-9]*\) failed.*/\2/p')
  printf '%s\t%s\t%s\t%s\n' "$name" "$rc" "${passed:-NA}" "${failed:-NA}" >> "$SUMMARY"
  [ "$rc" = 0 ] || ANYFAIL=1
done
echo; cat "$SUMMARY"
exit $ANYFAIL
