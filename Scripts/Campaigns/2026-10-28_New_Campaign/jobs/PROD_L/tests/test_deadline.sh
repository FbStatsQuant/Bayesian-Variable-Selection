#!/bin/bash
# test_deadline.sh -- acceptance tests of batch_runner.sh (DESIGN.md section 3, D47.2): the deadline rule, the unit budget, the atomic ledger and the inventory.
#   bash test_deadline.sh WORKDIR
# batch_runner.sh is exercised the way an sbatch script does: after prodl.env / common.sh / pilot_init / pilot_modules / pilot_blas_single, the runner is SOURCED
# (it may end with `exit`). The unit command is replaced by a stub (PRODL_UNIT_CMD) that plays a scripted behaviour per started unit (line k of a file for the
# k-th start), so the tests do not depend on how the runner passes the unit to the command.
# Time arithmetic used below (hooks): D = T0 + WALL - 120 ; NEED = BUDGET + 60 + 120 ; a unit starts iff elapsed + NEED <= WALL - 120.
source "$(dirname "$0")/lib.sh"
t_init "${1:-}" test_deadline
t_mkbundle "$W/fx" 20261030T1300Z
COMMON=$(t_find_common); RUNNER="$BUN/batch_runner.sh"; ENVF="$BUN/prodl.env"
[ -n "$COMMON" ] && [ -f "$RUNNER" ] && [ -f "$ENVF" ]; t_cond "DL00 bundle has common.sh, batch_runner.sh and prodl.env" $? "common=[$COMMON] runner=$([ -f "$RUNNER" ] && echo yes || echo no)"

cat > "$W/harness.sh" <<'H'
#!/bin/bash
# what an sbatch script does around the runner
set -euo pipefail
export T0=$(date +%s) PRODL_T0=$(date +%s)
source "$H_ENVFILE"
LOG_RUN="$H_LOG"; TMP_ROOT="$H_LOG/tmp"
source "$H_COMMON"
# H_PROD=1: the RUNNER must see production mode. The laptop has no verified GNU time outside a local test (the PILOT_TIME_BIN hook is refused), so pilot_init
# and pilot_modules run under PILOT_LOCAL_TEST=1 with the time shim, and the hooks are unset (TIME_BIN stays as resolved) right before batch_runner.sh is sourced.
if [ -n "${H_PROD:-}" ]; then export PILOT_LOCAL_TEST=1 PILOT_TIME_BIN="$H_TIME_BIN"; fi
pilot_init "$PIECE"
if [ -n "${H_FAKE_MODULE:-}" ]; then module() { return 0; }; fi     # production-mode runs on the laptop: a no-op `module` (PILOT_SKIP_MODULES is a hook)
pilot_modules lowp
pilot_blas_single
if [ -n "${H_PROD:-}" ]; then unset PILOT_LOCAL_TEST PILOT_TIME_BIN PRODL_TEST_WALL_S PRODL_TEST_BUDGET_S PRODL_TEST_NOW_OFFSET_S PRODL_UNIT_CMD PILOT_SKIP_MODULES PILOT_DRYRUN; fi
set +e
source "$H_RUNNER"; rc=$?
for fn in prodl_batch_run batch_run run_batch prodl_run_batch batch_runner prodl_batch_runner; do
  if declare -F "$fn" >/dev/null; then "$fn"; rc=$?; break; fi
done
echo "HARNESS_RETURNED rc=$rc"
exit $rc
H
cat > "$W/unitcmd.sh" <<'U'
#!/bin/bash
# stub unit command: k-th start plays line k of $UNIT_STUB_DIR/behaviors (default: exit 0); records the ledger state it can see
d=${UNIT_STUB_DIR:?}
n=$(( $(cat "$d/count" 2>/dev/null || echo 0) + 1 )); echo $n > "$d/count"
echo "$(find "$CASE_LOG/ledger" -name '*.start' 2>/dev/null | wc -l | tr -d ' ') $(find "$CASE_LOG/ledger" -name '*.end' 2>/dev/null | wc -l | tr -d ' ')" >> "$d/obs"
line=$(sed -n "${n}p" "$d/behaviors")
[ -n "$line" ] || exit 0
eval "$line"
U
chmod +x "$W/harness.sh" "$W/unitcmd.sh"

# ---- case runner -------------------------------------------------------------------------------------------------------------
# globals set by the caller: CASE_PIECE CASE_N CASE_TASK TEST_WALL TEST_BUDGET TEST_OFFSET CASE_BEH CASE_EXTRA(array) CASE_NOLT CASE_KEEP CASE_JOB
unit_id() { local ds; printf -v ds 'p0020_S1_r%03d' "$1"; case "$CASE_PIECE" in smc|p5) echo "${ds}_c100";; smcrep) echo "${ds}_c100_rep1";; *) echo "$ds";; esac; }
mk_units() {
  local i ds
  printf 'piece\ttask\tunit\tdataset\tscale\trepeat\n'      # units.tsv format: the header row is part of UNITS_FILE (the runner skips line 1)
  for i in $(seq 1 "$CASE_N"); do
    printf -v ds 'p0020_S1_r%03d' "$i"
    case "$CASE_PIECE" in
      smc)    printf 'smc\t%s\t%s\t%s\tc100\t0\n' "$CASE_TASK" "${ds}_c100" "$ds";;
      smcrep) printf 'smcrep\t%s\t%s\t%s\tc100\t1\n' "$CASE_TASK" "${ds}_c100_rep1" "$ds";;
      p5)     printf 'p5\t%s\t%s\t%s\tc100\t0\tsmc\n' "$CASE_TASK" "${ds}_c100" "$ds";;
      *)      printf '%s\t%s\t%s\t%s\t-\t0\n' "$CASE_PIECE" "$CASE_TASK" "$ds" "$ds";;
    esac
  done
}
run_case() {   # run_case NAME
  local name=$1 wall budget
  CD="$W/cases/$name"; [ "${CASE_KEEP:-0}" = 1 ] || rm -rf "$CD"; mkdir -p "$CD/log" "$CD/stub"
  mk_units > "$CD/units.tsv"; rm -f "$CD/stub/count" "$CD/stub/obs"; printf '%s\n' "$CASE_BEH" > "$CD/stub/behaviors"
  case "$CASE_PIECE" in enum20) wall=3600; budget=300;; enum30) wall=2700; budget=600;; p5) wall=32400; budget=29100;; *) wall=18000; budget=14700;; esac
  CASE_T0=$(date +%s); CASE_JOB=${CASE_JOB:-8100}; TAG="${CASE_JOB}_${CASE_TASK}"
  (
    export STAMP="$T_STAMP" NC_HOME_ROOT="$FH" NC_SCR_ROOT="$FS" PATH="$T_BIN:$PATH" STUB_DIR="$T_STUB"
    export H_TIME_BIN="$T_BIN/gnutime" H_ENVFILE="$ENVF" H_COMMON="$COMMON" H_RUNNER="$RUNNER" H_LOG="$CD/log" CASE_LOG="$CD/log" UNIT_STUB_DIR="$CD/stub"
    export PIECE="$CASE_PIECE" UNITS_FILE="$CD/units.tsv" TASK_ID="$CASE_TASK" PRODL_WALL_S="$wall" UNIT_BUDGET_S="$budget" P5=$([ "$CASE_PIECE" = p5 ] && echo 1 || echo 0)
    export SLURM_ARRAY_JOB_ID="$CASE_JOB" SLURM_ARRAY_TASK_ID="$CASE_TASK" SLURM_JOB_ID="$CASE_JOB"
    if [ "${CASE_NOLT:-0}" != 1 ]; then
      export PILOT_LOCAL_TEST=1 PILOT_SKIP_MODULES=1 PILOT_TIME_BIN="$T_BIN/gnutime" PRODL_UNIT_CMD="$W/unitcmd.sh"
      [ -n "${TEST_WALL:-}" ] && export PRODL_TEST_WALL_S="$TEST_WALL"
      [ -n "${TEST_BUDGET:-}" ] && export PRODL_TEST_BUDGET_S="$TEST_BUDGET"
      [ -n "${TEST_OFFSET:-}" ] && export PRODL_TEST_NOW_OFFSET_S="$TEST_OFFSET"
    fi
    for kv in "${CASE_EXTRA[@]}"; do [ -n "$kv" ] && export "$kv"; done
    cd "$CD" && bash "$W/harness.sh"
  ) > "$CD/out.log" 2>&1
  CASE_RC=$?
}
reset_globals() { CASE_PIECE=smc; CASE_N=3; CASE_TASK=0; TEST_WALL=""; TEST_BUDGET=""; TEST_OFFSET=""; CASE_BEH=""; CASE_EXTRA=(); CASE_NOLT=0; CASE_KEEP=0; CASE_JOB=8100; }

# ---- readers / checks ---------------------------------------------------------------------------------------------------------
ldir() { echo "$CD/log/ledger/$CASE_PIECE/$1"; }
# ledger records are single-space separated key=value pairs (DESIGN section 12); fld FILE N returns the value of the N-th documented key, looked up BY KEY
fld() {
  local f=$1 n=$2 keys
  case "$f" in
    *.start)    keys=(unit piece task job_tag host start_utc deadline_epoch need_s);;
    *.end)      keys=(unit rc outcome wall_s cli_status cli_skipped end_utc);;
    *.deferred) keys=(unit reason now_epoch deadline_epoch need_s);;
  esac
  head -n 1 "$f" 2>/dev/null | tr ' \t' '\n\n' | sed -n "s/^${keys[$((n - 1))]}=//p" | head -n 1
}
# fkey FILE KEY : value of a key=value pair of the record's first line (keys not in the documented positional list, e.g. end_source, end_epoch)
fkey() { head -n 1 "$1" 2>/dev/null | tr ' \t' '\n\n' | sed -n "s/^$2=//p" | head -n 1; }
# fnum FILE N OP VALUE : numeric comparison on a field (OP -ge -le -lt -gt); the value may be a decimal
fnum() { local v; v=$(fld "$1" "$2"); [ -n "$v" ] && awk -v a="$v" -v b="$4" -v op="$3" 'BEGIN{ if (op=="-ge") exit !(a>=b); if (op=="-le") exit !(a<=b); if (op=="-lt") exit !(a<b); if (op=="-gt") exit !(a>b); exit 1 }'; }
count_runs() { cat "$CD/stub/count" 2>/dev/null || echo 0; }
inv_file() { echo "$CD/log/inventory/$CASE_PIECE/$TAG.tsv"; }
inv_outcome() { awk -v u="$1" '$1==u{print $2}' "$(inv_file)" 2>/dev/null; }
numeric() { printf '%s' "$1" | grep -qE '^[0-9]+([.][0-9]+)?$'; }
isoutc() { printf '%s' "$1" | grep -qE '^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}'; }

check_clean() {   # check_clean ID : ledger holds only <JOB_TAG>.start/.end/.deferred ; inventory only <JOB_TAG>.tsv ; no temporary names anywhere
  local id=$1 bad=0 f
  while IFS= read -r f; do
    case "$(basename "$f")" in *.start|*.end|*.deferred) ;; *) bad=$((bad + 1));; esac
    case "$(basename "$f")" in .*|*tmp*|*TMP*|*.swp|*~) bad=$((bad + 1));; esac
  done < <(find "$CD/log/ledger" -type f 2>/dev/null)
  t_eq "$id ledger holds only .start/.end/.deferred files, no temporary leftovers" 0 "$bad"
  bad=0
  while IFS= read -r f; do case "$(basename "$f")" in "$TAG".tsv) ;; *) bad=$((bad + 1));; esac; done < <(find "$CD/log/inventory" -type f 2>/dev/null)
  t_eq "$id inventory holds only <JOB_TAG>.tsv, no temporary leftovers" 0 "$bad"
}
check_started() {   # check_started ID UNIT OUTCOME RC_REGEX : the unit has .start and .end (no .deferred) with the documented fields
  local id=$1 u=$2 oc=$3 rcre=$4 d s e names
  d=$(ldir "$u"); s="$d/$TAG.start"; e="$d/$TAG.end"
  names=$(ls "$d" 2>/dev/null | tr '\n' ' ')
  t_eq "$id $u: ledger folder holds exactly <JOB_TAG>.start and <JOB_TAG>.end" "$TAG.end $TAG.start " "$names"
  t_eq "$id $u .start: unit" "$u" "$(fld "$s" 1)"
  t_eq "$id $u .start: piece" "$CASE_PIECE" "$(fld "$s" 2)"
  t_eq "$id $u .start: task" "$CASE_TASK" "$(fld "$s" 3)"
  t_eq "$id $u .start: job_tag" "$TAG" "$(fld "$s" 4)"
  [ -n "$(fld "$s" 5)" ]; t_cond "$id $u .start: host non-empty" $?
  isoutc "$(fld "$s" 6)"; t_cond "$id $u .start: start_utc is an ISO UTC time" $? "$(fld "$s" 6)"
  numeric "$(fld "$s" 7)"; t_cond "$id $u .start: deadline_epoch numeric" $? "$(fld "$s" 7)"
  t_eq "$id $u .start: need_s = budget + 60 + 120" "$NEED" "$(fld "$s" 8)"
  [ -n "$(fkey "$s" end_source)" ]; t_cond "$id $u .start: end_source recorded (F13)" $?
  numeric "$(fkey "$s" end_epoch)"; t_cond "$id $u .start: end_epoch numeric (F13)" $? "$(fkey "$s" end_epoch)"
  t_eq "$id $u .end: unit" "$u" "$(fld "$e" 1)"
  printf '%s' "$(fld "$e" 2)" | grep -qE "^($rcre)$"; t_cond "$id $u .end: rc matches $rcre" $? "$(fld "$e" 2)"
  t_eq "$id $u .end: outcome" "$oc" "$(fld "$e" 3)"
  numeric "$(fld "$e" 4)"; t_cond "$id $u .end: wall_s numeric" $? "$(fld "$e" 4)"
  [ -n "$(fld "$e" 5)" ]; t_cond "$id $u .end: cli_status field present" $?
  [ -n "$(fld "$e" 6)" ]; t_cond "$id $u .end: cli_skipped field present" $?
  isoutc "$(fld "$e" 7)"; t_cond "$id $u .end: end_utc is an ISO UTC time" $? "$(fld "$e" 7)"
}
check_deferred() {   # check_deferred ID UNIT : only <JOB_TAG>.deferred with unit / reason=deadline / now / deadline / need
  local id=$1 u=$2 d f
  d=$(ldir "$u"); f="$d/$TAG.deferred"
  t_eq "$id $u: ledger folder holds exactly <JOB_TAG>.deferred (never started)" "$TAG.deferred " "$(ls "$d" 2>/dev/null | tr '\n' ' ')"
  t_eq "$id $u .deferred: unit" "$u" "$(fld "$f" 1)"
  t_eq "$id $u .deferred: reason=deadline" "deadline" "$(fld "$f" 2)"
  numeric "$(fld "$f" 3)"; t_cond "$id $u .deferred: now_epoch numeric" $? "$(fld "$f" 3)"
  numeric "$(fld "$f" 4)"; t_cond "$id $u .deferred: deadline_epoch numeric" $? "$(fld "$f" 4)"
  t_eq "$id $u .deferred: need_s" "$NEED" "$(fld "$f" 5)"
  [ -n "$(fkey "$f" end_source)" ]; t_cond "$id $u .deferred: end_source recorded (F13)" $?
  numeric "$(fkey "$f" end_epoch)"; t_cond "$id $u .deferred: end_epoch numeric (F13)" $? "$(fkey "$f" end_epoch)"
}

# =========================================== DL01: everything fits ==================================================================
reset_globals; CASE_PIECE=smc; CASE_N=3; TEST_WALL=1000; TEST_BUDGET=100; NEED=280
# the real run_case.R output (v2.2.1 study/run_case.R lines 52-55): "<prefix> status= <s> skipped= <b> " then one tab-separated key=value line "prefix=..."
smc_out() { echo "printf 'SMCBVS status= ok skipped= $1 \\nprefix=SMCBVS\\tskipped=$1\\tp5_retry=FALSE\\tv3_status=complete\\tstop=NA\\n'; exit 0"; }
OK_LINE=$(smc_out FALSE)
CASE_BEH=$(printf '%s\n%s\n%s' "$OK_LINE" "$OK_LINE" "$OK_LINE")
run_case all_ok
t_eq "DL01 three quick units, window open: task exit 0" 0 "$CASE_RC"
t_eq "DL01 the unit command ran 3 times" 3 "$(count_runs)"
for i in 1 2 3; do check_started "DL01" "$(unit_id $i)" ok 0; done
v=$(fld "$(ldir "$(unit_id 1)")/$TAG.end" 5); [ -n "$v" ] && [ "$v" != NA ] && case "$v" in *ok*|*complete*) true;; *) false;; esac; t_cond "DL01 smc cli_status is parsed from the CLI's last line (status=ok / v3_status=complete), not NA" $?
fnum "$(ldir "$(unit_id 1)")/$TAG.start" 7 -ge $((CASE_T0 + 1000 - 120 - 5)) && fnum "$(ldir "$(unit_id 1)")/$TAG.start" 7 -le $((CASE_T0 + 1000 - 120 + 40)); t_cond "DL02 .start deadline_epoch = T0 + WALL - 120 (WALL from PRODL_TEST_WALL_S)" $?
for i in 1 2 3; do t_eq "DL03 inventory: $(unit_id $i) ok" ok "$(inv_outcome "$(unit_id $i)")"; done
t_eq "DL03 inventory: one row per unit" 3 "$(grep -c "^$(unit_id 1)\|^$(unit_id 2)\|^$(unit_id 3)" "$(inv_file)" 2>/dev/null)"
check_clean DL04
awk 'END{exit !(NR>=4)}' "$CD/log/timing/smc.$TAG.tsv" 2>/dev/null; t_cond "DL05 timed() wrote a timing row per started unit (header + 3)" $?
t_eq "DL06 first start is recorded before the unit ran (obs: 1 start, 0 ends)" "1 0" "$(sed -n 1p "$CD/stub/obs" 2>/dev/null)"
t_eq "DL06 second unit starts after the first .end (obs: 2 starts, 1 end)" "2 1" "$(sed -n 2p "$CD/stub/obs" 2>/dev/null)"

# =========================================== DL10: window already closed -> everything deferred ==========================================
reset_globals; CASE_PIECE=smc; CASE_N=3; TEST_WALL=1000; TEST_BUDGET=100; TEST_OFFSET=640; NEED=280
run_case deferred_all
t_eq "DL10 now+NEED > D before the first unit (offset 640): task exit 0 (deferred is not a failure)" 0 "$CASE_RC"
t_eq "DL11 no unit was started" 0 "$(count_runs)"
for i in 1 2 3; do check_deferred DL12 "$(unit_id $i)"; t_eq "DL13 inventory: $(unit_id $i) deferred" deferred "$(inv_outcome "$(unit_id $i)")"; done
fnum "$(ldir "$(unit_id 1)")/$TAG.deferred" 4 -ge $((CASE_T0 + 1000 - 120 - 5)) && fnum "$(ldir "$(unit_id 1)")/$TAG.deferred" 4 -le $((CASE_T0 + 1000 - 120 + 40)); t_cond "DL14 .deferred deadline_epoch = T0 + WALL - 120" $?
fnum "$(ldir "$(unit_id 1)")/$TAG.deferred" 3 -ge $((CASE_T0 + 640 - 5)) && fnum "$(ldir "$(unit_id 1)")/$TAG.deferred" 3 -le $((CASE_T0 + 640 + 40)); t_cond "DL15 .deferred now_epoch includes PRODL_TEST_NOW_OFFSET_S" $?
check_clean DL16
find "$CD/log/ledger" -name '*.start' | grep -q .; [ $? -ne 0 ]; t_cond "DL17 no .start record exists for a deferred unit" $?

# =========================================== DL20: window still open at offset 560 ==========================================================
reset_globals; CASE_PIECE=smc; CASE_N=2; TEST_WALL=1000; TEST_BUDGET=100; TEST_OFFSET=560; NEED=280
CASE_BEH=$(printf '%s\n%s' "$OK_LINE" "$OK_LINE"); run_case boundary_open
t_eq "DL20 offset 560: 560+280 <= 880 so the first unit AND the next start; exit 0" 0 "$CASE_RC"; t_eq "DL21 both units ran" 2 "$(count_runs)"

# =========================================== DL30: deadline reached in the middle of the task =======================================
reset_globals; CASE_PIECE=smc; CASE_N=3; TEST_WALL=342; TEST_BUDGET=30; NEED=210
CASE_BEH=$(printf '%s\n%s\n%s' "sleep 20; exit 0" "$OK_LINE" "$OK_LINE")
run_case mid_defer
t_eq "DL30 window 12 s, first unit takes 20 s: task exit 0" 0 "$CASE_RC"
t_eq "DL31 only the first unit was started (the first unit always starts when the window allows)" 1 "$(count_runs)"
check_started DL32 "$(unit_id 1)" ok 0
check_deferred DL33 "$(unit_id 2)"; check_deferred DL33 "$(unit_id 3)"
t_eq "DL34 inventory: ok, deferred, deferred" "ok deferred deferred" "$(inv_outcome "$(unit_id 1)") $(inv_outcome "$(unit_id 2)") $(inv_outcome "$(unit_id 3)")"
check_clean DL35

# =========================================== DL40: a unit over its budget is killed ======================================================
reset_globals; CASE_PIECE=smc; CASE_N=2; TEST_WALL=1000; TEST_BUDGET=3; NEED=183
CASE_BEH=$(printf '%s\n%s' "exec sleep 40" "$OK_LINE")
run_case killed
t_eq "DL40 unit 1 outlives its budget (3 s): task exit 1" 1 "$CASE_RC"
check_started DL41 "$(unit_id 1)" killed_timeout '124|137'
fnum "$(ldir "$(unit_id 1)")/$TAG.end" 4 -ge 2 && fnum "$(ldir "$(unit_id 1)")/$TAG.end" 4 -lt 30; t_cond "DL42 the killed unit's wall_s is about its budget, not its 40 s sleep" $?
check_started DL43 "$(unit_id 2)" ok 0
t_eq "DL44 a timeout does not stop the task: unit 2 ran" 2 "$(count_runs)"
t_eq "DL45 inventory: killed_timeout, ok" "killed_timeout ok" "$(inv_outcome "$(unit_id 1)") $(inv_outcome "$(unit_id 2)")"
check_clean DL46

# =========================================== DL50: a failing unit ======================================================================
reset_globals; CASE_PIECE=smc; CASE_N=2; TEST_WALL=1000; TEST_BUDGET=100; NEED=280
CASE_BEH=$(printf '%s\n%s' "echo boom >&2; exit 3" "$OK_LINE"); run_case failed
t_eq "DL50 unit 1 exits 3: task exit 1 (wakes OPS)" 1 "$CASE_RC"
check_started DL51 "$(unit_id 1)" unit_failed 3
check_started DL52 "$(unit_id 2)" ok 0
t_eq "DL53 inventory: unit_failed, ok" "unit_failed ok" "$(inv_outcome "$(unit_id 1)") $(inv_outcome "$(unit_id 2)")"
check_clean DL54

# =========================================== DL60: skipped units ======================================================================
reset_globals; CASE_PIECE=smc; CASE_N=1; TEST_WALL=1000; TEST_BUDGET=100; NEED=280
CASE_BEH=$(smc_out TRUE); run_case skipped_smc
t_eq "DL60 SMC unit already valid (skipped=TRUE): task exit 0" 0 "$CASE_RC"
check_started DL61 "$(unit_id 1)" skipped 0
v=$(fld "$(ldir "$(unit_id 1)")/$TAG.end" 6); [ "${v^^}" = TRUE ]; t_cond "DL62 cli_skipped records TRUE" $?
reset_globals; CASE_PIECE=enum20; CASE_N=1; TEST_WALL=1000; TEST_BUDGET=100; NEED=280
CASE_BEH="echo 'EXACT.done verified (hashes, dataset), nothing to do: /x/p0020/p0020_S1_r001'; exit 0"; run_case skipped_enum
t_eq "DL63 enumerator reports 'nothing to do': task exit 0" 0 "$CASE_RC"
check_started DL64 "$(unit_id 1)" skipped 0
t_eq "DL65 enumerator unit: cli_status is NA" NA "$(fld "$(ldir "$(unit_id 1)")/$TAG.end" 5)"

# =========================================== DL70: SLURM_JOB_END_TIME bounds the deadline ==================================================
reset_globals; CASE_PIECE=smc; CASE_N=2; TEST_WALL=1000; TEST_BUDGET=100; NEED=280
CASE_EXTRA=("SLURM_JOB_END_TIME=$(( $(date +%s) + 250 ))"); CASE_BEH=$(printf '%s\n%s' "$OK_LINE" "$OK_LINE"); run_case jobend_near
t_eq "DL70 SLURM_JOB_END_TIME = now+250: D = end-60 = now+190 < NEED 280: nothing starts, exit 0" 0 "$CASE_RC"
t_eq "DL71 no unit started" 0 "$(count_runs)"; check_deferred DL72 "$(unit_id 1)"
reset_globals; CASE_PIECE=smc; CASE_N=2; TEST_WALL=1000; TEST_BUDGET=100; NEED=280
CASE_EXTRA=("SLURM_JOB_END_TIME=$(( $(date +%s) + 5000 ))"); CASE_BEH=$(printf '%s\n%s' "$OK_LINE" "$OK_LINE"); run_case jobend_far
t_eq "DL73 SLURM_JOB_END_TIME far in the future does not tighten D: units run" 2 "$(count_runs)"
reset_globals; CASE_PIECE=smc; CASE_N=2; TEST_WALL=1000; TEST_BUDGET=100; NEED=280
CASE_EXTRA=("SLURM_JOB_END_TIME=abc"); CASE_BEH=$(printf '%s\n%s' "$OK_LINE" "$OK_LINE"); run_case jobend_junk
t_eq "DL74 (F13) non-numeric SLURM_JOB_END_TIME is treated as ABSENT; in a LOCAL TEST the script-time fallback is allowed: units run, exit 0" "2 0" "$(count_runs) $CASE_RC"
reset_globals; CASE_PIECE=p5; CASE_N=2; CASE_TASK=0; CASE_NOLT=1; CASE_EXTRA=("H_FAKE_MODULE=1" "H_PROD=1" "SLURM_JOB_END_TIME=abc"); CASE_BEH="exit 0"; run_case junk_end_prod
t_eq "DL74b (F13) the same junk end time in PRODUCTION (no local test, no squeue end time): task exit 1" 1 "$CASE_RC"
t_eq "DL74c ... no unit started (no .start or .end record exists)" 0 "$(find "$CD/log/ledger" -name '*.start' -o -name '*.end' 2>/dev/null | wc -l | tr -d ' ')"
for i in 1 2; do u=$(unit_id $i); f="$(ldir "$u")/$TAG.deferred"
  t_eq "DL74d $u deferred with reason=no_scheduler_end_time" no_scheduler_end_time "$(fkey "$f" reason)"; done

# =========================================== DL80: P5 task (one unit, production constants) =================================================
reset_globals; CASE_PIECE=p5; CASE_N=1; CASE_TASK=0; NEED=29280; CASE_BEH="exit 0"; run_case p5_ok
t_eq "DL80 p5 task with production constants (WALL 32400, BUDGET 29100): unit starts, exit 0" "1 0" "$(count_runs) $CASE_RC"
check_started DL81 "$(unit_id 1)" ok 0
reset_globals; CASE_PIECE=p5; CASE_N=1; CASE_TASK=0; TEST_OFFSET=3500; NEED=29280; CASE_BEH="exit 0"; run_case p5_late
t_eq "DL82 p5 task at elapsed 3500 s: 3500 + 29280 > 32280, so deferred (exit 0, unit not started)" "0 0" "$(count_runs) $CASE_RC"
check_deferred DL83 "$(unit_id 1)"

# =========================================== DL90: atomic records are never edited; second job tag adds, does not touch =================
reset_globals; CASE_PIECE=smc; CASE_N=2; TEST_WALL=1000; TEST_BUDGET=100; NEED=280
CASE_BEH=$(printf '%s\n%s' "$OK_LINE" "$OK_LINE"); run_case tags_first
d=$(ldir "$(unit_id 1)"); before=$(cat "$d"/*.start "$d"/*.end 2>/dev/null | md5sum)
CASE_KEEP=1; CASE_JOB=8200; run_case tags_first
d=$(ldir "$(unit_id 1)")
t_eq "DL90 second run of the same unit under another job tag: four ledger files (2 tags x start/end)" 4 "$(ls "$d" | wc -l | tr -d ' ')"
t_eq "DL91 the first job tag's records are byte-identical (never edited)" "$before" "$(cat "$d"/8100_0.start "$d"/8100_0.end 2>/dev/null | md5sum)"
CASE_JOB=8100

# =========================================== F3: no silent requeue ==========================================================================
ledger_sig() { ( cd "$CD/log/ledger" 2>/dev/null && find . -type f | LC_ALL=C sort | xargs md5sum 2>/dev/null | md5sum ); }
reset_globals; CASE_PIECE=smc; CASE_N=2; TEST_WALL=1000; TEST_BUDGET=100; NEED=280
CASE_BEH=$(printf '%s\n%s' "$OK_LINE" "$OK_LINE"); run_case requeue
sig1=$(ledger_sig); inv1=$(cat "$CD/log/inventory/smc/8100_0.tsv" 2>/dev/null | md5sum)
t_eq "RQ00 (setup) first run of job 8100 task 0: exit 0, 2 units" "0 2" "$CASE_RC $(count_runs)"
CASE_KEEP=1; run_case requeue
t_eq "RQ01 the SAME job/task id run a second time: no unit command is started" 0 "$(count_runs)"
[ "$CASE_RC" != 0 ]; t_cond "RQ02 ... the second run refuses (exit $CASE_RC)" $?
t_eq "RQ03 ... the first run's ledger is byte-identical (names and contents; .start/.end not replaced)" "$sig1" "$(ledger_sig)"
t_eq "RQ04 ... the first run's inventory is byte-identical" "$inv1" "$(cat "$CD/log/inventory/smc/8100_0.tsv" 2>/dev/null | md5sum)"
[ -s "$CD/log/refusals/$TAG.txt" ] && grep -q "$(unit_id 1)" "$CD/log/refusals/$TAG.txt"; t_cond "RQ05 ... the refusal evidence is LOG_RUN/refusals/<JOB_TAG>.txt and names the unit (not a file in the unit's ledger folder)" $?
reset_globals; CASE_PIECE=smc; CASE_N=2; TEST_WALL=1000; TEST_BUDGET=100; NEED=280; CASE_EXTRA=("SLURM_RESTART_COUNT=1"); CASE_BEH=$(printf '%s\n%s' "$OK_LINE" "$OK_LINE"); run_case restart1
t_eq "RQ10 SLURM_RESTART_COUNT=1 (a requeued task): exit 71, before any ledger write" 71 "$CASE_RC"
t_eq "RQ11 ... no unit started" 0 "$(count_runs)"
[ ! -e "$CD/log/ledger" ] && [ ! -e "$CD/log/inventory" ]; t_cond "RQ12 ... no ledger and no inventory exists" $?
grep -q '8100' "$CD/out.log"; t_cond "RQ13 ... the refusal message names the job" $?
reset_globals; CASE_PIECE=smc; CASE_N=2; TEST_WALL=1000; TEST_BUDGET=100; NEED=280; CASE_BEH=$(printf '%s\n%s' "$OK_LINE" "$OK_LINE"); run_case restart2
sig2=$(ledger_sig); CASE_KEEP=1; CASE_EXTRA=("SLURM_RESTART_COUNT=2"); CASE_JOB=8100; run_case restart2
t_eq "RQ14 a restart (count 2) after a finished run: exit 71, nothing started, ledger byte-identical" "71 0 $sig2" "$CASE_RC $(count_runs) $(ledger_sig)"
reset_globals; CASE_PIECE=smc; CASE_N=1; TEST_WALL=1000; TEST_BUDGET=100; NEED=280; CASE_EXTRA=("SLURM_RESTART_COUNT=0"); CASE_BEH="$OK_LINE"; run_case restart0
t_eq "RQ15 (control) SLURM_RESTART_COUNT=0 is a normal first start: exit 0, unit runs" "0 1" "$CASE_RC $(count_runs)"
reset_globals; CASE_PIECE=p5; CASE_N=1; CASE_NOLT=1; CASE_EXTRA=("H_FAKE_MODULE=1" "SLURM_RESTART_COUNT=1"); run_case restart_p5
t_eq "RQ16 the refusal applies in production mode and to the p5 arm too (pilot_init, every arm): exit 71" 71 "$CASE_RC"

# =========================================== F13: deadline from the scheduler's end time ================================================================
reset_globals; CASE_PIECE=smc; CASE_N=2; TEST_WALL=1000; TEST_BUDGET=100; NEED=280
END=$(( $(date +%s) + 5000 )); CASE_EXTRA=("SLURM_JOB_END_TIME=$END"); CASE_BEH=$(printf '%s\n%s' "$OK_LINE" "$OK_LINE"); run_case es_env
t_eq "ES01 numeric SLURM_JOB_END_TIME (far): units run, exit 0" "0 2" "$CASE_RC $(count_runs)"
f="$(ldir "$(unit_id 1)")/$TAG.start"
t_eq "ES02 .start: end_epoch = SLURM_JOB_END_TIME" "$END" "$(fkey "$f" end_epoch)"
case "$(fkey "$f" end_source | tr 'A-Z' 'a-z')" in *job_end_time*|*env*) true;; *) false;; esac; t_cond "ES03 .start: end_source names the environment variable ($(fkey "$f" end_source))" $?
reset_globals; CASE_PIECE=smc; CASE_N=2; TEST_WALL=1000; TEST_BUDGET=100; NEED=280
END=$(( $(date +%s) + 5000 )); printf '%s\n' "$(date -d "@$END" +%Y-%m-%dT%H:%M:%S)" > "$T_STUB/squeue_end.txt"
CASE_BEH=$(printf '%s\n%s' "$OK_LINE" "$OK_LINE"); run_case es_squeue
t_eq "ES04 SLURM_JOB_END_TIME absent, squeue -h -j \$SLURM_JOB_ID -o %e gives the end: units run, exit 0" "0 2" "$CASE_RC $(count_runs)"
f="$(ldir "$(unit_id 1)")/$TAG.start"
t_eq "ES05 .start: end_epoch = the squeue end time (parsed with date -d)" "$END" "$(fkey "$f" end_epoch)"
case "$(fkey "$f" end_source | tr 'A-Z' 'a-z')" in *squeue*) true;; *) false;; esac; t_cond "ES06 .start: end_source names squeue ($(fkey "$f" end_source))" $?
grep -q -- '-j 8100' "$T_STUB/squeue_calls.txt" 2>/dev/null; t_cond "ES07 squeue was asked about job 8100 (-j \$SLURM_JOB_ID)" $?
reset_globals; CASE_PIECE=smc; CASE_N=2; TEST_WALL=1000; TEST_BUDGET=100; NEED=280
printf '%s\n' "$(date -d "@$(( $(date +%s) + 250 ))" +%Y-%m-%dT%H:%M:%S)" > "$T_STUB/squeue_end.txt"
CASE_BEH=$(printf '%s\n%s' "$OK_LINE" "$OK_LINE"); run_case es_squeue_near
t_eq "ES08 a near squeue end time (now+250: D = end-60 < NEED 280): nothing starts, exit 0" "0 0" "$CASE_RC $(count_runs)"
check_deferred ES09 "$(unit_id 1)"
reset_globals; CASE_PIECE=smc; CASE_N=2; TEST_WALL=1000; TEST_BUDGET=100; NEED=280
printf 'garbage\n' > "$T_STUB/squeue_end.txt"; END=$(( $(date +%s) + 5000 )); CASE_EXTRA=("SLURM_JOB_END_TIME=$END")
CASE_BEH=$(printf '%s\n%s' "$OK_LINE" "$OK_LINE"); run_case es_env_wins
f="$(ldir "$(unit_id 1)")/$TAG.start"
t_eq "ES10 the numeric environment value wins over squeue (source order): end_epoch" "$END" "$(fkey "$f" end_epoch)"
rm -f "$T_STUB/squeue_end.txt"
reset_globals; CASE_PIECE=smc; CASE_N=2; TEST_WALL=1000; TEST_BUDGET=100; NEED=280; CASE_BEH=$(printf '%s\n%s' "$OK_LINE" "$OK_LINE"); run_case es_local_fallback
t_eq "ES11 neither source, LOCAL TEST: the script-time fallback runs the units, exit 0" "0 2" "$CASE_RC $(count_runs)"
f="$(ldir "$(unit_id 1)")/$TAG.start"; [ -n "$(fkey "$f" end_source)" ]; t_cond "ES12 ... and the fallback is recorded in end_source ($(fkey "$f" end_source))" $?
reset_globals; CASE_PIECE=p5; CASE_N=2; CASE_TASK=0; CASE_NOLT=1; CASE_EXTRA=("H_FAKE_MODULE=1" "H_PROD=1"); CASE_BEH="exit 0"; run_case es_prod_none
t_eq "ES13 neither source and NOT a local test: task exit 1 (wakes OPS)" 1 "$CASE_RC"
t_eq "ES14 ... no unit started (no .start/.end records)" 0 "$(find "$CD/log/ledger" -name '*.start' -o -name '*.end' 2>/dev/null | wc -l | tr -d ' ')"
for i in 1 2; do u=$(unit_id $i); f="$(ldir "$u")/$TAG.deferred"
  t_eq "ES15 $u deferred with reason=no_scheduler_end_time" no_scheduler_end_time "$(fkey "$f" reason)"
  t_eq "ES16 $u .deferred: unit key" "$u" "$(fkey "$f" unit)"; done
t_eq "ES17 inventory: deferred, deferred" "deferred deferred" "$(inv_outcome "$(unit_id 1)") $(inv_outcome "$(unit_id 2)")"
reset_globals; CASE_PIECE=p5; CASE_N=1; CASE_TASK=0; CASE_NOLT=1; END=$(( $(date +%s) + 120 )); CASE_EXTRA=("H_FAKE_MODULE=1" "H_PROD=1" "SLURM_JOB_END_TIME=$END"); CASE_BEH="exit 0"; run_case es_prod_near
t_eq "ES18 PRODUCTION with a numeric but near end time (now+120): the unit is deferred by the deadline rule, not started" "0" "$(find "$CD/log/ledger" -name '*.start' 2>/dev/null | wc -l | tr -d ' ')"
reset_globals

# =========================================== DL95: hooks refused outside a local test =======================================================
for v in PRODL_UNIT_CMD PRODL_TEST_WALL_S PRODL_TEST_BUDGET_S PRODL_TEST_NOW_OFFSET_S; do
  reset_globals; CASE_PIECE=smc; CASE_N=1; CASE_NOLT=1; CASE_EXTRA=("$v=$W/unitcmd.sh"); [ "$v" != PRODL_UNIT_CMD ] && CASE_EXTRA=("$v=5")
  run_case hook_$v
  t_eq "DL95 hook $v without PILOT_LOCAL_TEST: refused by pilot_init (exit 70), no unit started" "70 0" "$CASE_RC $(count_runs)"
done

t_summary
