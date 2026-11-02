#!/bin/bash
# test_waiter.sh -- acceptance tests of waiter.sh (DESIGN.md section 8; derived from ops/scaffold/pilot_monitor.sh v2).
#   bash test_waiter.sh WORKDIR
# waiter.sh LOGFILE JOBIDS [MAX_CHECKS] with an ssh shim (prints a canned `squeue ...; echo ===SACCT===; sacct ...` answer in the pilot monitor's format:
# squeue rows "id name state reason", then the line ===SACCT===, then sacct rows "JobID JobName State ExitCode Elapsed") and a sleep shim that records its argument.
# Exit 3 EARLY_FAILURE on any non-COMPLETED terminal state; 0 ALL_TERMINAL; 2 after MAX_CHECKS.
source "$(dirname "$0")/lib.sh"
t_init "${1:-}" test_waiter
WAITER="$B/waiter.sh"
[ -f "$WAITER" ]; t_cond "WT00 waiter.sh exists in the bundle" $?

SHIMS="$W/shims"; mkdir -p "$SHIMS"
printf '#!/bin/bash\nprintf "%%s\\n" "$*" >> "$WT_DIR/ssh_calls.txt"\ncat "$WT_DIR/ssh_out.txt"\nexit $(cat "$WT_DIR/ssh_rc" 2>/dev/null || echo 0)\n' > "$SHIMS/ssh"
printf '#!/bin/bash\nprintf "%%s\\n" "$*" >> "$WT_DIR/sleep_calls.txt"\nexit 0\n' > "$SHIMS/sleep"
chmod +x "$SHIMS/ssh" "$SHIMS/sleep"

HDR='===SACCT==='
CAN="$W/canned.txt"
# F10: the waiter asks `sacct -n -X -P -j IDS -o JobID,State`, so the accounting rows are "JobID|State" (the job name argument is only kept for readability)
row() { printf '%s|%s\n' "$1" "$3"; }
# wait_case NAME EXPECTED_RC MAX_CHECKS [SSH_RC] : the canned ssh answer is the file $CAN (written just before the call)
wait_case() {
  local name=$1 want=$2 max=$3 srcrc=${4:-0} d="$W/c_${1//[^A-Za-z0-9]/_}"; rm -rf "$d"; mkdir -p "$d"
  cp "$CAN" "$d/ssh_out.txt"; echo "$srcrc" > "$d/ssh_rc"
  # WT_FLAG: extra option (e.g. --until-terminal); WT_FLAG_POS=before puts it between JOBIDS and MAX_CHECKS, otherwise after MAX_CHECKS
  if [ -n "${WT_FLAG:-}" ] && [ "${WT_FLAG_POS:-after}" = before ]; then
    ( export WT_DIR="$d" PATH="$SHIMS:$PATH"; bash "$WAITER" "$d/log.txt" 7001,7002,7003 "$WT_FLAG" "$max" ) > "$d/out.txt" 2>&1
  else
    ( export WT_DIR="$d" PATH="$SHIMS:$PATH"; bash "$WAITER" "$d/log.txt" 7001,7002,7003 "$max" ${WT_FLAG:+"$WT_FLAG"} ) > "$d/out.txt" 2>&1
  fi
  WT_RC=$?; WT_D=$d
  t_eq "$name: exit status" "$want" "$WT_RC"
}
nssh() { t_count_lines "$WT_D/ssh_calls.txt"; }
nsleep() { t_count_lines "$WT_D/sleep_calls.txt"; }
inlog() { grep -q "$1" "$WT_D/log.txt" 2>/dev/null; }

# ---- non-COMPLETED terminal states: exit 3 at once (one ssh, no sleep) -----------------------------------------------------------
for st in FAILED TIMEOUT OUT_OF_MEMORY NODE_FAIL CANCELLED "CANCELLED by 123" "CANCELLED+" PREEMPTED BOOT_FAIL DEADLINE; do
  { echo '7002_3 lowpB_s2_smc RUNNING bb1'; echo "$HDR"; row 7001 lowpB_s0_build COMPLETED; row 7002 lowpB_s2_smc "$st"; row 7003 lowpB_s9_collect PENDING; } > "$CAN"
  wait_case "WT01 $st among COMPLETED/PENDING rows" 3 3
  t_eq "WT01 $st: decided at the first check (one ssh)" 1 "$(nssh)"
  t_eq "WT01 $st: no sleep before exiting" 0 "$(nsleep)"
  inlog EARLY_FAILURE; t_cond "WT01 $st: EARLY_FAILURE recorded in the log" $?
done
{ echo "$HDR"; row 7001 lowpB_s0_build COMPLETED; row 7002 lowpB_s2_smc FAILED; } > "$CAN"; wait_case "WT02 FAILED with an EMPTY squeue" 3 2
{ echo "$HDR"; row 7001 lowpB_s0_build FAILED; } > "$CAN"; wait_case "WT03 a single FAILED row" 3 2

# ---- all terminal ---------------------------------------------------------------------------------------------------------------
{ echo "$HDR"; row 7001 lowpB_s0_build COMPLETED; row 7002 lowpB_s2_smc COMPLETED; row 7003 lowpB_s9_collect COMPLETED; } > "$CAN"
wait_case "WT10 all COMPLETED, squeue empty" 0 3
inlog ALL_TERMINAL; t_cond "WT10 ALL_TERMINAL recorded in the log" $?
t_eq "WT10 one ssh, no sleep" "1 0" "$(nssh) $(nsleep)"
{ echo '9001 other_user_job RUNNING n1'; echo "$HDR"; row 7001 lowpB_s0_build COMPLETED; row 7002 lowpB_s2_smc COMPLETED; row 7003 lowpB_s9_collect COMPLETED; } > "$CAN"
wait_case "WT11 squeue lists only jobs that are not lowpB_ (and all sacct rows COMPLETED)" 0 3
{ echo '9100_4 lowpL_s2_smc RUNNING n1'; echo "$HDR"; row 7001 lowpB_s0_verify COMPLETED; row 7002 lowpB_s1_bench COMPLETED; row 7003 lowpB_s9_collect COMPLETED; } > "$CAN"
wait_case "WT11b (bench) a running PROD-L job (lowpL_ prefix) is not ours: all lowpB_ terminal -> exit 0" 0 3
{ echo '7002_4 lowpB_s1_bench RUNNING n1'; echo "$HDR"; row 7001 lowpB_s0_verify COMPLETED; row 7002 lowpB_s1_bench COMPLETED; row 7003 lowpB_s9_collect COMPLETED; } > "$CAN"
wait_case "WT11c (bench) a queued lowpB_ job keeps the waiter waiting: exit 2" 2 1

# ---- not terminal ---------------------------------------------------------------------------------------------------------------
{ echo "$HDR"; row 7001 lowpB_s0_build COMPLETED; row 7002 lowpB_s2_smc PENDING; } > "$CAN"
wait_case "WT20 empty squeue but a PENDING sacct row (OPS-4 lesson): NOT terminal, 1 check" 2 1
inlog MAX_CHECKS; t_cond "WT20 MAX_CHECKS_REACHED recorded" $?
inlog ALL_TERMINAL; [ $? -ne 0 ]; t_cond "WT20 ALL_TERMINAL is NOT recorded" $?
{ echo "$HDR"; row 7001 lowpB_s0_build COMPLETED; row 7002 lowpB_s2_smc RUNNING; } > "$CAN"; wait_case "WT21 RUNNING sacct row" 2 1
{ echo '7002_3 lowpB_s2_smc RUNNING bb1'; echo "$HDR"; row 7001 lowpB_s0_build COMPLETED; row 7002 lowpB_s2_smc RUNNING; } > "$CAN"; wait_case "WT22 RUNNING in squeue and sacct" 2 1
{ echo '7002_[4-95%32] lowpB_s2_smc PENDING (Resources)'; echo "$HDR"; row 7001 lowpB_s0_build COMPLETED; row 7002 lowpB_s2_smc COMPLETED; row 7003 a COMPLETED; } > "$CAN"
wait_case "WT23 sacct all COMPLETED but squeue still lists a lowpB_ job: not terminal" 2 1
echo "$HDR" > "$CAN"; wait_case "WT24 no sacct rows at all (and empty squeue): not terminal" 2 1
{ echo "$HDR"; row 7001 lowpB_s0_build COMPLETED; row 7002 lowpB_s2_smc REQUEUED; } > "$CAN"; wait_case "WT25 REQUEUED sacct row: not terminal" 2 1
{ echo "$HDR"; row 7001 lowpB_s0_build COMPLETED; row 7002 lowpB_s2_smc RUNNING; } > "$CAN"; wait_case "WT26 two checks of a RUNNING job: ends with exit 2 after MAX_CHECKS" 2 2
t_eq "WT26 one ssh per check (2)" 2 "$(nssh)"
awk '$1 >= 600 {n++} END{exit !(n >= 1)}' "$WT_D/sleep_calls.txt" 2>/dev/null; t_cond "WT26 checks are at least 10 minutes apart (sleep >= 600 between them)" $?
awk '$1 == 900 {bad++} END{exit bad > 0}' "$WT_D/sleep_calls.txt" 2>/dev/null; t_cond "WT26 no 15-minute back-off without an ssh failure" $?

# ---- ssh failure: back-off, no crash -----------------------------------------------------------------------------------------------
printf 'ssh: connect to host nots port 22: Connection timed out\n' > "$CAN"; wait_case "WT30 ssh fails (exit 255)" 2 2 255
awk '$1 == 900 {n++} END{exit !(n >= 1)}' "$WT_D/sleep_calls.txt" 2>/dev/null; t_cond "WT30 backs off 900 s after an ssh failure" $?
t_eq "WT30 one ssh per check (2 checks)" 2 "$(nssh)"
inlog 'ssh_rc=255'; t_cond "WT30 the failure is logged with its rc" $?
inlog EARLY_FAILURE; [ $? -ne 0 ]; t_cond "WT30 an ssh error text is never mistaken for a job state" $?
printf 'ssh: Could not resolve hostname nots\nFAILED\n' > "$CAN"; wait_case "WT31 ssh fails and its stderr contains the word FAILED: still no EARLY_FAILURE" 2 1 255

# ---- the command sent to the cluster ------------------------------------------------------------------------------------------------
{ echo "$HDR"; row 7001 lowpB_s0_build COMPLETED; } > "$CAN"; wait_case "WT40 (F10) ONE COMPLETED row for three requested ids, empty squeue: NOT terminal (accounting incomplete)" 2 1
grep -q ALL_TERMINAL "$WT_D/log.txt" 2>/dev/null; [ $? -ne 0 ]; t_cond "WT40b ... ALL_TERMINAL is not recorded" $?
grep -q '7001,7002,7003' "$WT_D/ssh_calls.txt" 2>/dev/null; t_cond "WT40c JOBIDS (7001,7002,7003) are on the ssh command line" $?
grep -q -e '-P' -e 'parsable' "$WT_D/ssh_calls.txt" 2>/dev/null; t_cond "WT40d the sacct query is delimited (-P) so that JobID/State are not truncated" $?
{ echo "$HDR"; row 7001 a COMPLETED; row 7002 a COMPLETED; } > "$CAN"; wait_case "WT43 (F10) ids 7001, 7002 have rows, 7003 has none: UNKNOWN, keep waiting" 2 1
{ echo "$HDR"; row 7001 a COMPLETED; row 7002_0 a COMPLETED; row 7002_1 a COMPLETED; row 7003 a COMPLETED; } > "$CAN"; wait_case "WT44 (F10) an array id represented by its task rows only (7002_0, 7002_1) counts as covered: all terminal" 0 1
{ echo "$HDR"; row 7001 a COMPLETED; row 7002 a COMPLETED; row 7003 a COMPLETED; printf 'garbage line without a state\n'; } > "$CAN"; wait_case "WT45 (F10) an unparsable accounting row: UNKNOWN, never ALL_TERMINAL" 2 1
{ echo "$HDR"; row 7001 a COMPLETED; row 7002 a COMPLETED; printf '7003|\n'; } > "$CAN"; wait_case "WT46 (F10) a row with an empty state: UNKNOWN" 2 1
{ echo "$HDR"; row 7001 a COMPLETED; row 7002 a FAILED; } > "$CAN"; wait_case "WT47 (F10) a real failure is reported at once even though 7003 has no accounting row yet: EARLY_FAILURE" 3 1
{ echo "$HDR"; row 7001 a COMPLETED; row 7002 a COMPLETED; row 7003 a COMPLETED; } > "$CAN"; wait_case "WT48 (F10) complete accounting, all terminal: ALL_TERMINAL" 0 1
{ echo '7003 lowpB_s9_collect PENDING (Dependency)'; echo "$HDR"; row 7001 a COMPLETED; row 7002 a COMPLETED; row 7003 a COMPLETED; } > "$CAN"; wait_case "WT49 (F10) complete accounting but squeue still lists a lowpB_ job: not terminal" 2 1
grep -q 'squeue' "$WT_D/ssh_calls.txt" && grep -q 'sacct' "$WT_D/ssh_calls.txt"; t_cond "WT41 one ssh runs squeue and sacct together" $?
grep -q 'nots' "$WT_D/ssh_calls.txt"; t_cond "WT42 the host is the configured alias nots" $?

# ---- manager ruling F8/F10: --until-terminal (never exits early; 0 all COMPLETED; 4 ALL_TERMINAL_WITH_FAILURES; missing/unparsable accounting keeps waiting) ----------
WT_FLAG=--until-terminal
{ echo "$HDR"; row 7001 a COMPLETED; row 7002 a COMPLETED; row 7003 a COMPLETED; } > "$CAN"; wait_case "UT01 --until-terminal, all COMPLETED: exit 0" 0 2
{ echo "$HDR"; row 7001 a COMPLETED; row 7002 a FAILED; row 7003 a COMPLETED; } > "$CAN"; wait_case "UT02 --until-terminal, every id terminal and one FAILED: exit 4 (ALL_TERMINAL_WITH_FAILURES)" 4 2
inlog ALL_TERMINAL_WITH_FAILURES; t_cond "UT03 ... ALL_TERMINAL_WITH_FAILURES recorded" $?
inlog EARLY_FAILURE; [ $? -ne 0 ]; t_cond "UT04 ... no EARLY_FAILURE in this mode" $?
t_eq "UT05 ... decided at the first check (one ssh, no sleep)" "1 0" "$(nssh) $(nsleep)"
{ echo "$HDR"; row 7001 a COMPLETED; row 7002 a FAILED; row 7003 a RUNNING; } > "$CAN"; wait_case "UT06 --until-terminal, a failure but another id still RUNNING: does NOT exit early, keeps waiting -> exit 2 after MAX_CHECKS" 2 1
inlog EARLY_FAILURE; [ $? -ne 0 ]; t_cond "UT07 ... never EARLY_FAILURE" $?
{ echo '7003 lowpB_s9_collect RUNNING n1'; echo "$HDR"; row 7001 a COMPLETED; row 7002 a FAILED; row 7003 a COMPLETED; } > "$CAN"; wait_case "UT08 --until-terminal, accounting terminal but squeue still lists a lowpB_ job: keeps waiting (exit 2)" 2 1
{ echo "$HDR"; row 7001 a COMPLETED; row 7002 a FAILED; } > "$CAN"; wait_case "UT09 --until-terminal, a FAILED row and id 7003 missing from accounting: keeps waiting (exit 2)" 2 1
{ echo "$HDR"; row 7001 a COMPLETED; row 7002 a COMPLETED; printf '7003|\n'; } > "$CAN"; wait_case "UT10 --until-terminal, an empty state: keeps waiting (exit 2)" 2 1
{ echo "$HDR"; row 7001 a COMPLETED; row 7002_0 a TIMEOUT; row 7002_1 a CANCELLED+; row 7003 a OUT_OF_MEMORY; } > "$CAN"; wait_case "UT11 --until-terminal, array task rows TIMEOUT / CANCELLED+ and OUT_OF_MEMORY, all terminal: exit 4" 4 1
{ echo "$HDR"; row 7001 a COMPLETED; row 7002 a FAILED; row 7003 a COMPLETED; } > "$CAN"; WT_FLAG_POS=before wait_case "UT12 the flag placed between JOBIDS and MAX_CHECKS works the same: exit 4" 4 2
{ echo "$HDR"; row 7001 a COMPLETED; row 7002 a COMPLETED; row 7003 a COMPLETED; } > "$CAN"; WT_FLAG_POS=before wait_case "UT13 the flag placed between JOBIDS and MAX_CHECKS, all COMPLETED: exit 0" 0 2
printf 'ssh: connect to host nots port 22: Connection timed out\n' > "$CAN"; wait_case "UT14 --until-terminal with an ssh failure: backs off, exit 2 after MAX_CHECKS" 2 2 255
awk '$1 == 900 {n++} END{exit !(n >= 1)}' "$WT_D/sleep_calls.txt" 2>/dev/null; t_cond "UT15 ... 900 s back-off" $?
WT_FLAG=
# default mode unchanged by the new flag's existence
{ echo "$HDR"; row 7001 a COMPLETED; row 7002 a FAILED; row 7003 a RUNNING; } > "$CAN"; wait_case "UT20 (default mode) the same rows WITHOUT the flag: exit 3 at the first failure-like row" 3 2

t_summary
