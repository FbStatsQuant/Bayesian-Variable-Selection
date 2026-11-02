#!/bin/bash
# test_retune.sh -- regression tests for F9 of R1_FIX_PLAN.md: retune_throttle.sh with admission and drain check.
#   bash test_retune.sh WORKDIR
# retune_throttle.sh STAMP --profile alone|withH [--yes]   builds a plan from THIS run's LIVE arrays (cpus x new throttle, phase fit, smc/smcrep serial rule),
#   runs ceiling_check.py against a fresh squeue (fail closed; alone is also refused while _prodH jobs exist), --yes applies `scontrol update JobId=<id>
#   ArrayTaskThrottle=<n>` and re-queries squeue to confirm each pending array shows the new %N (record LOG_RUN/launch/retune_<utc>.txt).
# retune_throttle.sh STAMP --check-drained   prints PROD-L's RUNNING billed CPUs; exit 0 iff <= 68 (CEIL_WITHH).
# Live run: 7000 enum20 (RUNNING, 4 CPUs), 7001 enum30 array (16 CPUs; 2 running tasks), 7002 smc array (1 CPU). alone peak = 4 + 4*16 + 32*2 = 132 ; withH = 68.
source "$(dirname "$0")/lib.sh"
t_init "${1:-}" test_retune
STAMP=20261030T2100Z
t_mkbundle "$W/fx" "$STAMP"
[ -f "${PRODL_B_SRC:-$B}/retune_throttle.sh" ]; t_cond "RT00 retune_throttle.sh exists" $?

others() { local n=$1 i; for i in $(seq 1 "$n"); do printf '%s|other_job|RUNNING|1\n' $((9500 + i)); done; }   # n rows of another user's work = 2n billed
live() {   # live THR30 THRSMC NRUN_SMC : this run's rows (pending arrays carry the CURRENT throttles)
  printf '7000|lowpL_s1_enum20|RUNNING|4\n7001_3|lowpL_s1_enum30|RUNNING|16\n7001_4|lowpL_s1_enum30|RUNNING|16\n7001_[5-23%%%s]|lowpL_s1_enum30|PENDING|16\n' "$1"
  local k; for k in $(seq 1 "$3"); do printf '7002_%s|lowpL_s2_smc|RUNNING|1\n' "$k"; done
  printf '7002_[40-95%%%s]|lowpL_s2_smc|PENDING|1\n' "$2"
}
state() {   # state THR30 THRSMC NRUN_SMC NOTHERS
  t_stub_reset; rm -rf "$LOGR"; mkdir -p "$LOGR/launch"
  printf 'wave\tstep\tjobid\tarray\tdependency\nmain\ts0_build\t6999\t-\t-\nmain\ts1_enum20\t7000\t-\t-\nmain\ts1_enum30\t7001\t0-23%%%s\t-\nmain\ts2_smc\t7002\t0-95%%%s\t-\nmain\ts3_smcrep\t7003\t0-479%%%s\t-\n' "$1" "$2" "$2" > "$RUNH/JOBIDS.tsv"
  cp "$RUNH/JOBIDS.tsv" "$LOGR/jobids.tsv"
  { live "$1" "$2" "$3"; others "$4"; } > "$T_STUB/squeue.txt"
}
run_rt() {   # run_rt LABEL args... : RT_RC RT_LOG
  local label=$1; shift; RT_LOG="$W/rt_$label.log"
  ( export NC_HOME_ROOT="$FH" NC_SCR_ROOT="$FS" PATH="$T_BIN:$PATH" STUB_DIR="$T_STUB" SQUEUE="$T_BIN/squeue" SACCT="$T_BIN/sacct" SCONTROL="$T_BIN/scontrol" PYTHON="$T_BIN/python3" STAMP
    cd "$W" && bash "$BUN/retune_throttle.sh" "$STAMP" "$@" ) > "$RT_LOG" 2>&1
  RT_RC=$?
}
nscontrol() { t_count_lines "$T_STUB/scontrol_calls.txt"; }
rec_files() { ls "$LOGR/launch" 2>/dev/null | grep -c '^retune_'; }

# ---- raising to alone: admission -------------------------------------------------------------------------------------------------------------------
state 2 16 3 35; run_rt raise_70 --profile alone --yes
[ "$RT_RC" != 0 ]; t_cond "RT01 raise to alone with 70 billed CPUs of other work (132 + 70 = 202 > 192): refused (exit $RT_RC)" $?
t_eq "RT02 ... scontrol is never called" 0 "$(nscontrol)"
t_eq "RT03 ... no retune record is written" 0 "$(rec_files)"
state 2 16 3 30; run_rt raise_60_dry --profile alone
t_eq "RT04 raise to alone with 60 billed of other work (132 + 60 = 192): admitted in the dry run, exit 0" 0 "$RT_RC"
t_eq "RT05 ... the dry run does not call scontrol" 0 "$(nscontrol)"
grep -q 7001 "$RT_LOG" && grep -q 7002 "$RT_LOG"; t_cond "RT06 ... the dry run reports the arrays it would update (7001, 7002)" $?
state 2 16 3 30; run_rt raise_60 --profile alone --yes
t_eq "RT07 the same with --yes: exit 0" 0 "$RT_RC"
grep -q 'JobId=7001 ArrayTaskThrottle=4' "$T_STUB/scontrol_calls.txt"; t_cond "RT08 scontrol update JobId=7001 ArrayTaskThrottle=4 (enum30 alone)" $?
grep -q 'JobId=7002 ArrayTaskThrottle=32' "$T_STUB/scontrol_calls.txt"; t_cond "RT09 scontrol update JobId=7002 ArrayTaskThrottle=32 (smc alone)" $?
t_eq "RT10 only this run's arrays are touched (no other job id, no JobId=7000 plain job)" 0 "$(grep -v -e 'JobId=7001 ' -e 'JobId=7002 ' -e 'JobId=7003 ' "$T_STUB/scontrol_calls.txt" | wc -l | tr -d ' ')"
t_eq "RT11 ... and never a selector (user/name)" 0 "$(grep -c -e '--user' -e ' -u ' -e 'Name=' "$T_STUB/scontrol_calls.txt")"
[ "$(rec_files)" = 1 ]; t_cond "RT12 a confirmation record LOG_RUN/launch/retune_<utc>.txt is written" $?
f=$(ls "$LOGR"/launch/retune_* 2>/dev/null | head -n 1); grep -q 7001 "$f" 2>/dev/null && grep -q 7002 "$f" 2>/dev/null; t_cond "RT13 ... it lists the updated arrays" $?
grep -q '7001_\[5-23%4\]' "$T_STUB/squeue.txt" && grep -q '7002_\[40-95%32\]' "$T_STUB/squeue.txt"; t_cond "RT14 the scheduler (squeue) now shows the new %N on both pending arrays (confirmation by re-query)" $?
state 2 16 3 30; touch "$T_STUB/scontrol_noop"; run_rt unconfirmed --profile alone --yes
[ "$RT_RC" != 0 ]; t_cond "RT15 scontrol 'succeeds' but squeue still shows the old %N: NOT confirmed, nonzero exit ($RT_RC)" $?
f=$(ls "$LOGR"/launch/retune_* 2>/dev/null | head -n 1); [ -n "$f" ] && grep -qi 'unconfirmed\|not confirmed\|mismatch' "$f"; t_cond "RT16 ... the record says so" $?

# ---- other refusals ----------------------------------------------------------------------------------------------------------------------------
state 2 16 3 0; printf '9001|lowpH_prodH_s2|RUNNING|2\n' >> "$T_STUB/squeue.txt"; run_rt prodh --profile alone --yes
[ "$RT_RC" != 0 ] && [ "$(nscontrol)" = 0 ]; t_cond "RT20 raise to alone while a _prodH job exists: refused, scontrol not called" $?
state 2 16 3 0; touch "$T_STUB/squeue_fail"; run_rt sqfail --profile alone --yes
[ "$RT_RC" != 0 ] && [ "$(nscontrol)" = 0 ]; t_cond "RT21 squeue fails: fail closed, scontrol not called (exit $RT_RC)" $?
state 2 16 3 0; run_rt bad_profile --profile sideways --yes
[ "$RT_RC" != 0 ] && [ "$(nscontrol)" = 0 ]; t_cond "RT22 unknown profile: refused" $?

# ---- lowering -----------------------------------------------------------------------------------------------------------------------------------
state 4 32 3 50; run_rt lower --profile withH --yes
t_eq "RT30 lowering to withH with 100 billed of other work (68 + 100 = 168): exit 0" 0 "$RT_RC"
grep -q 'JobId=7001 ArrayTaskThrottle=2' "$T_STUB/scontrol_calls.txt" && grep -q 'JobId=7002 ArrayTaskThrottle=16' "$T_STUB/scontrol_calls.txt"; t_cond "RT31 scontrol: 7001 -> 2 and 7002 -> 16" $?
grep -q '7001_\[5-23%2\]' "$T_STUB/squeue.txt" && grep -q '7002_\[40-95%16\]' "$T_STUB/squeue.txt"; t_cond "RT32 squeue confirms the lower throttles" $?

# ---- --check-drained ------------------------------------------------------------------------------------------------------------------------------
# running billed of PROD-L = enum20 4 + 2 enum30 tasks x 16 + smc running tasks x 2
state 2 16 16 0; run_rt drained_68 --check-drained
t_eq "RT40 running billed = 4 + 32 + 32 = 68 (= CEIL_WITHH): exit 0" 0 "$RT_RC"
grep -q '68' "$RT_LOG"; t_cond "RT41 ... the output prints the running billed CPUs (68)" $?
state 2 16 17 0; run_rt drained_70 --check-drained
t_eq "RT42 running billed = 70 > 68: exit 1 (not drained)" 1 "$RT_RC"
grep -q '70' "$RT_LOG"; t_cond "RT43 ... the output prints 70" $?
state 2 16 0 0; run_rt drained_36 --check-drained
t_eq "RT44 running billed = 36: exit 0" 0 "$RT_RC"
state 2 16 17 400; run_rt drained_other --check-drained
t_eq "RT45 PROD-L running 70 (others 800 billed are not counted): exit 1" 1 "$RT_RC"
state 2 16 0 400; run_rt drained_other2 --check-drained
t_eq "RT46 PROD-L running 36 while others run 800 billed: exit 0 (only PROD-L's own running allocation counts)" 0 "$RT_RC"
state 2 16 0 0; touch "$T_STUB/squeue_fail"; run_rt drained_sqfail --check-drained
[ "$RT_RC" != 0 ]; t_cond "RT47 squeue fails: no 'drained' verdict, nonzero exit ($RT_RC)" $?

# ---- R2 M1: the plan also holds every still-live NON-array own job (the plain enum20 job: 4 CPUs, 1 task, phase fit); only arrays are updated -------------------------
# alone = enum20 4 + enum30 4*16 = 64 + smc 32*2 = 64 -> 132 ; with 60 billed of other work = 192 (admitted), 62 and 64 are refused. Without the enum20 row the 62 case would pass (128 + 62 = 190).
state 2 16 3 31; run_rt m1_62 --profile alone
[ "$RT_RC" != 0 ]; t_cond "RT50 live enum20 (4 CPUs) + 62 billed of other work (132 + 62 = 194 > 192): refused (exit $RT_RC)" $?
state 2 16 3 32; run_rt m1_64 --profile alone --yes
[ "$RT_RC" != 0 ] && [ "$(nscontrol)" = 0 ]; t_cond "RT51 live enum20 + 64 billed: refused, scontrol not called" $?
state 2 16 3 30; run_rt m1_60 --profile alone --yes
t_eq "RT52 live enum20 + 60 billed (4 + 64 + 64 + 60 = 192): admitted, exit 0" 0 "$RT_RC"
f=$(ls "$LOGR"/launch/retune_* 2>/dev/null | head -n 1)
grep -q -e '7000' -e 's1_enum20' "$f" 2>/dev/null; t_cond "RT53 the record's plan shows the enum20 row (job 7000 / s1_enum20)" $?
grep -q 'JobId=7000' "$T_STUB/scontrol_calls.txt"; [ $? -ne 0 ]; t_cond "RT54 ... but the plain job is not 'updated' (only arrays get scontrol update)" $?
state 2 16 3 30; sed '/^7000|/d' "$T_STUB/squeue.txt" > "$T_STUB/squeue.new"; mv "$T_STUB/squeue.new" "$T_STUB/squeue.txt"; printf '%s|other_job|RUNNING|1\n%s|other_job|RUNNING|1\n' 9901 9902 >> "$T_STUB/squeue.txt"
run_rt m1_finished --profile alone
t_eq "RT55 (control) enum20 no longer live (finished) + 64 billed of other work (128 + 64 = 192): admitted" 0 "$RT_RC"

t_summary
