#!/bin/bash
# test_probe_real.sh -- HQ D82: R/bench_env_probe.R run for REAL against the REAL frozen code tree (code/bench_lowp r2: config_lowp.R, common.R,
# production_helpers, methods), no stub. s0_verify job 2510090 failed because the probe called lowp_load_method(..., test_library=FALSE) while the frozen
# signature is lowp_load_method(id, code_dir, p, test_versions = FALSE). Earlier suites missed it: every unit suite replaces Rscript by a stub (lib.sh), so
# no bundle R script ran; TESTS.md listed bench_env_probe.R as "not encoded"; the live run's probe step expected a FAIL (laptop glmnet != pin) without
# checking WHY it failed, and its run1 stopped before reaching it.
#   bash test_probe_real.sh WORKDIR        (one R process at a time; laptop R 4.4.1)
# Pinned library: a throwaway library of metadata-only packages at the frozen pins (tests/mk_pinlib.R: DESCRIPTION + Meta/package.rds; the probe
# loads no package).
# The pins are written here by hand from config_lowp.R r2 (not derived from it), so PR03 also cross-checks the probe's pin extraction. digest
# (any version) is added because the frozen CLI requires it inside the sealed library too; the laptop's own libraries stay on the path, so PR08/PR08b
# prove that a pinned package found OUTSIDE the pinned library is refused (frozen CLI rule "Package outside sealed library").
source "$(dirname "$0")/lib.sh"
t_init "${1:-}" test_probe_real
SRCB=${PRODL_B_SRC:-$B}
RS="/c/Program Files/R/R-4.4.1/bin/Rscript.exe"
CODE="$CAMP/code/bench_lowp"
R2="$CAMP/code/bench_v2/lowp_port/BENCH_LOWP_MANIFEST_SHA256_r2.txt"
PROBE="$SRCB/R/bench_env_probe.R"
CHK="$T_LIB_DIR/check_frozen_calls.R"
PINS="glmnet=5.1 ncvreg=3.16.0 abess=0.4.11 susieR=0.14.2 SSLASSO=1.2.3.9001 bayesreg=1.3 pgdraw=1.1 doParallel=1.0.17"

[ -x "$RS" ] && [ -f "$PROBE" ] && [ -f "$CHK" ] && [ -f "$R2" ]; t_cond "PR00 prerequisites (R 4.4.1, the bundle probe, the checker, the r2 manifest)" $?
# The code tree is the REAL frozen one: every file of the r2 manifest hashes as recorded (no stub, no fixture)
bad=0; while read -r h p; do [ "$(sha256sum "$CODE/$p" | cut -d' ' -f1)" = "$h" ] || bad=$((bad+1)); done < "$R2"
t_eq "PR01 code/bench_lowp equals r2 file by file (34 files, 0 mismatches)" "34/0" "$(wc -l < "$R2" | tr -d ' ')/$bad"
grep -q "^lowp_load_method <- function(id, code_dir, p, test_versions = FALSE)" "$CODE/R/common.R"; t_cond "PR02 frozen signature is lowp_load_method(id, code_dir, p, test_versions = FALSE)" $?

mklib() {   # mklib DIR "pkg=ver ..." : metadata-only packages (tests/mk_pinlib.R; one R process)
  rm -rf "$1"; "$RS" "$(t_win "$T_LIB_DIR/mk_pinlib.R")" "$(t_win "$1")" $2 > "$1.mk.log" 2>&1 || echo "mklib failed: $1" >&2
}
probe() {   # probe LABEL PROBE_FILE LIB [--local-test] : PR_RC, PR_LOG
  PR_LOG="$W/probe_$1.log"
  "$RS" "$(t_win "$2")" --code "$(t_win "$CODE")" --library "$(t_win "$3")" ${4:-} > "$PR_LOG" 2>&1; PR_RC=$?
}

# ---- the real probe on a library at exactly the frozen pins: PASS
mklib "$W/lib_ok" "$PINS digest=0.6.37"
probe ok "$PROBE" "$W/lib_ok" --local-test
t_eq "PR03 real probe, real frozen code, library at the r2 pins: exit 0" 0 "$PR_RC"
grep -qx "PASS benchmark environment" "$PR_LOG"; t_cond "PR04 it prints 'PASS benchmark environment'" $? "$(tail -n 3 "$PR_LOG")"
! grep -q "unused argument" "$PR_LOG"; t_cond "PR05 no 'unused argument' anywhere in its output" $?
# ---- without --local-test on the laptop (R 4.4.1) the R-version gate still refuses
probe rver "$PROBE" "$W/lib_ok"
[ "$PR_RC" = 1 ] && grep -q "FAIL: R 4.5.2 required" "$PR_LOG"; t_cond "PR06 without --local-test on R 4.4.1: exit 1 'R 4.5.2 required'" $? "rc=$PR_RC"
# ---- every pin is enforced strictly (test_versions = FALSE): one wrong version or one missing package fails, for the right reason
for kv in $PINS; do
  pkg=${kv%%=*}
  mklib "$W/lib_v_$pkg" "$(printf '%s\n' $PINS | sed "s/^$pkg=.*/$pkg=0.0.1/" | tr '\n' ' ')"
  probe "v_$pkg" "$PROBE" "$W/lib_v_$pkg" --local-test
  [ "$PR_RC" = 1 ] && grep -q "^FAIL: " "$PR_LOG" && ! grep -q -e "unused argument" -e "could not find function" -e "subscript out of bounds" "$PR_LOG"
  t_cond "PR07 $pkg at 0.0.1 instead of ${kv#*=}: exit 1 on the pin check (not a wiring error)" $? "rc=$PR_RC $(tail -n 1 "$PR_LOG")"
done
mklib "$W/lib_miss" "$(printf '%s
' $PINS | grep -v '^doParallel=' | tr '
' ' ') digest=0.6.37"
probe miss "$PROBE" "$W/lib_miss" --local-test
[ "$PR_RC" = 1 ] && grep -q -e "^FAIL: Package outside sealed library: doParallel" -e "^FAIL: Package missing: doParallel" "$PR_LOG"
t_cond "PR08 doParallel absent from the pinned library (the laptop's own copy is on the path): exit 1, outside sealed library / missing" $? "rc=$PR_RC $(tail -n 1 "$PR_LOG")"
mklib "$W/lib_nodig" "$PINS"
probe nodig "$PROBE" "$W/lib_nodig" --local-test
[ "$PR_RC" = 1 ] && grep -q -e "^FAIL: Package outside sealed library: digest" -e "^FAIL: Package missing: digest" "$PR_LOG"
t_cond "PR08b digest absent from the pinned library: exit 1 (the frozen CLI needs it there too)" $? "rc=$PR_RC $(tail -n 1 "$PR_LOG")"
grep -q "test_versions *= *FALSE" "$PROBE" && ! grep -q "test_versions *= *TRUE" "$PROBE"; t_cond "PR09 the probe keeps the strict pin check (test_versions = FALSE, never TRUE)" $?

# ---- D82 reproduction: the shipped rev-1 line, on the same real code and the same good library, fails exactly as on NOTS
sed 's/test_versions=FALSE/test_library=FALSE/' "$PROBE" > "$W/probe_rev1.R"
grep -q "test_library=FALSE" "$W/probe_rev1.R"; t_cond "PR10 rev-1 copy built (test_library=FALSE)" $?
probe rev1 "$W/probe_rev1.R" "$W/lib_ok" --local-test
[ "$PR_RC" = 1 ] && grep -q "FAIL: unused argument (test_library = FALSE)" "$PR_LOG"; t_cond "PR11 rev-1 probe: exit 1 'unused argument (test_library = FALSE)' (the NOTS failure of job 2510090)" $? "rc=$PR_RC $(tail -n 1 "$PR_LOG")"

# ---- static check of every bundle R script against the frozen definitions (match.call on the formals)
"$RS" "$(t_win "$CHK")" "$(t_win "$CODE")" "$(t_win "$SRCB/R/bench_env_probe.R")" "$(t_win "$SRCB/R/prodl_inputs_check.R")" "$(t_win "$SRCB/accept_bench.R")" > "$W/chk_bundle.log" 2>&1
rc=$?
t_eq "PR12 check_frozen_calls on the bundle R scripts: exit 0" 0 "$rc"
grep -q "^checked=2 bad=0$" "$W/chk_bundle.log"; t_cond "PR13 it checked the 2 calls into frozen code (lowp_load_method, assert_pkg_version) and found 0 bad" $? "$(tail -n 1 "$W/chk_bundle.log")"
"$RS" "$(t_win "$CHK")" "$(t_win "$CODE")" "$(t_win "$W/probe_rev1.R")" > "$W/chk_rev1.log" 2>&1
rc=$?
[ "$rc" = 1 ] && grep -q "^BAD bench_env_probe\|^BAD probe_rev1.R.*test_library" "$W/chk_rev1.log"; t_cond "PR14 the checker flags the rev-1 line (exit 1, BAD ... test_library)" $? "rc=$rc $(head -n 2 "$W/chk_rev1.log")"
# no other R entry point in the bundle: the only R files are the three checked above (the shell scripts call the frozen CLI, covered by the live run)
n=$(find "$SRCB" -path "$SRCB/tests" -prune -o -path "$SRCB/review" -prune -o -type f \( -name '*.R' -o -name '*.r' \) -print | wc -l | tr -d ' ')
t_eq "PR15 the bundle has exactly 3 R scripts outside tests/ and review/ (all checked)" 3 "$n"
# ---- s0_verify passes the probe exactly the flags exercised here (--code BENCH_DIR --library R_LIBS_BENCH [--local-test])
grep -qF 'probe_args=(--code "$BENCH_DIR" --library "$R_LIBS_BENCH")' "$SRCB/slurm/s0_verify.sbatch"; t_cond "PR16 s0_verify calls the probe with --code \$BENCH_DIR --library \$R_LIBS_BENCH" $?
grep -q 'BENCH_DIR="$CODE/bench_lowp"' "$SRCB/bench.env"; t_cond "PR17 bench.env: BENCH_DIR is the staged frozen tree code/bench_lowp" $?

t_summary
