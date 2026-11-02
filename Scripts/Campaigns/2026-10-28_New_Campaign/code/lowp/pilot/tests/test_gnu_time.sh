#!/bin/bash
# test_gnu_time.sh -- local test of the GNU time resolution in slurm/common.sh (CONF-2b, HQ add-on after OPS-4: NOTS has no /usr/bin/time;
# GNU time 1.9 is the module binary /opt/apps/software/time/1.9-GCCcore-13.3.0/bin/time).
#   bash tests/test_gnu_time.sh WORKDIR        -> prints a result table; exit 0 iff every case behaves as expected.
# Fake binaries stand in for the real ones (none exists on this PC): a GNU-like time (--version "time (GNU Time) 1.9", honours -f/-o),
# a non-GNU time, a binary that CLAIMS GNU but ignores -f, and missing paths. Every pilot_init case runs in its own bash process.
set -u
W=${1:?usage: test_gnu_time.sh WORKDIR}; rm -rf "$W"; mkdir -p "$W/bin"; W=$(cd "$W" && pwd)
HERE=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd); PILOT=$(cd "$HERE/.." && pwd)
FAIL=0; N=0
res() { N=$((N + 1)); if [ "$2" = "$3" ]; then echo "| $1 | $2 | $3 | ok |"; else echo "| $1 | $2 | $3 | **WRONG** |"; FAIL=$((FAIL + 1)); fi; }

# --- fake binaries -----------------------------------------------------------------------------------------------------------------------------------------
cat > "$W/bin/gnutime" <<'B'
#!/bin/bash
# GNU-like: `--version`; `-f FMT -o FILE cmd...` runs cmd and writes FMT with %e %U %S %M replaced (tabs from \t)
if [ "${1:-}" = --version ]; then echo "time (GNU Time) 1.9"; exit 0; fi
fmt=""; out=""
while [ $# -gt 0 ]; do case "$1" in -f) fmt=$2; shift 2;; -o) out=$2; shift 2;; *) break;; esac; done
"$@"; rc=$?
line=${fmt//%e/0.01}; line=${line//%U/0.02}; line=${line//%S/0.00}; line=${line//%M/2048}; line=${line//\\t/$'\t'}
if [ -n "$out" ]; then printf '%s\n' "$line" > "$out"; else printf '%s\n' "$line" >&2; fi
exit $rc
B
cat > "$W/bin/bsdtime" <<'B'
#!/bin/bash
if [ "${1:-}" = --version ]; then echo "usage: time [-lp] utility" >&2; exit 1; fi
"$@"
B
cat > "$W/bin/liar" <<'B'
#!/bin/bash
# claims GNU in --version but ignores -f (writes the default POSIX format)
if [ "${1:-}" = --version ]; then echo "time (GNU Time) 1.9"; exit 0; fi
out=""; while [ $# -gt 0 ]; do case "$1" in -f) shift 2;; -o) out=$2; shift 2;; *) break;; esac; done
"$@"; printf 'real 0.00\nuser 0.00\nsys 0.00\n' > "${out:-/dev/stderr}"
B
cat > "$W/bin/malformed" <<'B'
#!/bin/bash
# claims GNU and honours -o, but writes the line in $FAKE_LINE (tabs from \t) instead of real figures (Sol review 4, R4-2 controls)
if [ "${1:-}" = --version ]; then echo "time (GNU Time) 1.9"; exit 0; fi
out=""; while [ $# -gt 0 ]; do case "$1" in -f) shift 2;; -o) out=$2; shift 2;; *) break;; esac; done
"$@"; line=${FAKE_LINE//\\t/$'\t'}; printf '%s\n' "$line" > "${out:-/dev/stderr}"
B
chmod +x "$W/bin/"*

# --- resolver unit cases (source common.sh in a subshell with the minimum it needs) ------------------------------------------------------------------------------
resolve() { ( export STAMP=T PILOT_ID=T PILOT_DIR="$PILOT" TMPDIR="$W"; source "$PILOT/slurm/common.sh" >/dev/null 2>&1
              pilot_resolve_time "$@" >/dev/null 2>&1; echo "${TIME_BIN:-none}|$TIME_BIN_NOTE" ); }
echo "| Case | Expected | Got | Result |"; echo "|---|---|---|---|"
r=$(resolve "$W/bin/gnutime"); res "resolver: a GNU time (version + -f/-o probe) is accepted" "$W/bin/gnutime" "${r%%|*}"
r=$(resolve "$W/bin/bsdtime"); res "resolver: a non-GNU time is rejected" none "${r%%|*}"
r=$(resolve "$W/bin/liar"); res "resolver: a binary that claims GNU but ignores -f is rejected (format probe)" none "${r%%|*}"
r=$(resolve "$W/bin/missing" "$W/bin/gnutime"); res "resolver: order -- a missing first candidate (as /usr/bin/time on NOTS), then the GNU one is used" "$W/bin/gnutime" "${r%%|*}"
r=$(resolve "$W/bin/bsdtime" "$W/bin/gnutime"); res "resolver: order -- a non-GNU first candidate is skipped, the next GNU one is used" "$W/bin/gnutime" "${r%%|*}"
r=$(resolve "$W/bin/missing" "$W/bin/bsdtime"); res "resolver: none valid -> none, the note lists every candidate tried" "none|no verified GNU time among: $W/bin/missing $W/bin/bsdtime" "$r"
r=$(resolve "$W/bin"); res "resolver: a directory is not a binary" none "${r%%|*}"
for bad in '.\t1..2\t0.0\t1024' '1.5\t0.2\t0.0\t12.5' '1.5\t0.2\t0.0\t1024\t7' '1.5\t\t0.0\t1024' '1.\t0.2\t0.0\t1024' 'x\t0.2\t0.0\t1024'; do
  r=$(FAKE_LINE="$bad" resolve "$W/bin/malformed"); res "resolver (R4-2): a 'GNU' probe line with malformed fields is rejected: $bad" none "${r%%|*}"
done
r=$(FAKE_LINE='12\t0\t0\t1024' resolve "$W/bin/malformed"); res "resolver (R4-2): integer-only decimals are well formed and accepted: 12 0 0 1024" "$W/bin/malformed" "${r%%|*}"
c=$(grep -c '^PILOT_GNU_TIME_NOTS=/opt/apps/software/time/1.9-GCCcore-13.3.0/bin/time$' "$PILOT/slurm/common.sh"); res "common.sh: the NOTS module path time/1.9 (GCCcore/13.3.0) is the second default candidate after /usr/bin/time" 1 "$c"
c=$(grep -c 'pilot_resolve_time /usr/bin/time "$PILOT_GNU_TIME_NOTS"' "$PILOT/slurm/common.sh"); res "common.sh: pilot_init tries /usr/bin/time then the module path (no hook set)" 1 "$c"

# --- pilot_init / timed integration (each in its own process; LOCAL-TEST hooks allowed) ------------------------------------------------------------------------
pinit() { # pinit ARM TIMEBIN DRYRUN : run pilot_init ARM (+ one timed unit) and print the exit status
  local arm=$1 tb=$2 dry=$3 L="$W/run_${1}_$(basename "$2")_$3"; rm -rf "$L"
  ( export STAMP=T PILOT_ID=T PILOT_DIR="$PILOT" PILOT_LOCAL_TEST=1 PILOT_TIME_BIN="$tb" PILOT_DRYRUN="$dry" LOG_RUN="$L" TMP_ROOT="$L/tmp" SLURM_ARRAY_TASK_ID=1 SLURM_ARRAY_JOB_ID=900
    set -euo pipefail; source "$PILOT/slurm/common.sh"; pilot_init "$arm"; timed "$arm" u1 1 true; exit 0 ) > "$L.out" 2>&1
  echo $?
}
rc=$(pinit enum20 "$W/bin/bsdtime" 0); res "pilot_init enum20 without GNU time: refused BEFORE any unit (exit 68, fail closed)" 68 "$rc"
res "  ... and no unit was timed (no timing file)" 0 "$(find "$W/run_enum20_bsdtime_0" -name '*.tsv' 2>/dev/null | wc -l)"
res "  ... the refusal names the reason" 1 "$(grep -c 'no verified GNU time' "$W/run_enum20_bsdtime_0.out")"
for a in enum30 scale smc bench; do rc=$(pinit "$a" "$W/bin/liar" 0); res "pilot_init $a with a fake 'GNU' time that ignores -f: refused (exit 68)" 68 "$rc"; done
for a in build lock truthlock verify bitid unlock collect; do rc=$(pinit "$a" "$W/bin/bsdtime" 0); res "pilot_init $a (infrastructure arm) without GNU time: continues, wall-only timing (exit 0)" 0 "$rc"; done
res "  unlock without GNU time: its record says time_bin=none and why" 2 "$(grep -cE '^time_bin=none$|^note=no verified GNU time' "$W/run_unlock_bsdtime_0/env/time_bin_unlock_900_1.txt")"
rc=$(pinit smc "$W/bin/bsdtime" 1); res "dry run (local test) of a required arm without GNU time: continues (dry runs time nothing)" 0 "$rc"
rc=$(pinit smc "$W/bin/gnutime" 0); res "pilot_init smc with GNU time: runs (exit 0)" 0 "$rc"
R="$W/run_smc_gnutime_0"
res "  env record names the binary, its --version and its sha256" 3 "$(grep -cE "^time_bin=$W/bin/gnutime$|^version=time \(GNU Time\) 1.9$|^sha256=[0-9a-f]{64}$" "$R/env/time_bin_smc_900_1.txt")"
row=$(tail -n 1 "$R/timing/smc.900_1.tsv" | cut -f5-8 | tr '\t' ' ')
res "  timed() row carries GNU time's wall, user, sys and max RSS (not NA)" "0.01 0.02 0.00 2048" "$row"
res "  pilot_init log line names the binary" 1 "$(grep -c "time_bin=$W/bin/gnutime" "$R.out")"
rc=$( ( export STAMP=T PILOT_ID=T PILOT_DIR="$PILOT" PILOT_TIME_BIN="$W/bin/gnutime" LOG_RUN="$W/hook" TMP_ROOT="$W/hook/tmp"; set -euo pipefail; source "$PILOT/slurm/common.sh"; pilot_init smc ) > /dev/null 2>&1; echo $? )
res "the PILOT_TIME_BIN hook outside a local test is still refused (exit 70)" 70 "$rc"

echo; echo "test_gnu_time: $((N - FAIL)) passed, $FAIL failed"
[ "$FAIL" = 0 ]
