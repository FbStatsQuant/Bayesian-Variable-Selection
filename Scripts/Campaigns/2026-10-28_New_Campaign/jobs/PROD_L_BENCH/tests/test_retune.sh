#!/bin/bash
# test_retune.sh -- retune_throttle.sh of the benchmark wave (PROD_L_BENCH DESIGN.md section 4; PROD-L F9/M1 behaviour adapted).
#   bash test_retune.sh WORKDIR
# retune_throttle.sh STAMP --profile alone|withH [--yes]: plan from THIS run's LIVE arrays (1 CPU x new throttle: bench alone %32 / withH %16, phase fit) plus every still-live plain own job,
# ceiling_check.py against a fresh squeue (fail closed; alone also refused while _prodH jobs exist); --yes applies `scontrol update JobId=<id> ArrayTaskThrottle=<n>` and re-queries squeue
# to confirm (record LOG_RUN/launch/retune_<utc>.txt). retune_throttle.sh STAMP --check-drained prints PROD-L-bench's RUNNING billed CPUs; exit 0 iff drained to the withH budget.
# Live run: 7001 s1_bench array (1 CPU). alone peak = 2*32 = 64 ; withH = 2*16 = 32 ; combined limit 192.
source "$(dirname "$0")/lib.sh"
t_init "${1:-}" test_retune
STAMP=20261030T2100Z
t_mkbundle "$W/fx" "$STAMP"
[ -f "${PRODL_B_SRC:-$B}/retune_throttle.sh" ]; t_cond "RT00 retune_throttle.sh exists" $?

others() { local n=$1 i; for i in $(seq 1 "$n"); do printf '%s|other_job|RUNNING|1\n' $((9500 + i)); done; }
live() {   # live THR NRUN [PLAIN] : the bench array (NRUN running tasks, pending remainder with throttle THR); PLAIN=1 adds the still-live plain s0_verify job
  local k; [ "${3:-0}" = 1 ] && printf '7000|lowpB_s0_verify|RUNNING|1\n'
  for k in $(seq 1 "$2"); do printf '7001_%s|lowpB_s1_bench|RUNNING|1\n' "$k"; done
  printf '7001_[40-95%%%s]|lowpB_s1_bench|PENDING|1\n' "$1"
}
state() {   # state THR NRUN NOTHERS [PLAIN]
  t_stub_reset; rm -rf "$LOGR"; mkdir -p "$LOGR/launch"
  printf 'wave\tstep\tjobid\tarray\tdependency\nmain\ts0_verify\t7000\t-\t-\nmain\ts1_bench\t7001\t0-95%%%s\tafterok:7000\n' "$1" > "$RUNH/JOBIDS.tsv"
  cp "$RUNH/JOBIDS.tsv" "$LOGR/jobids.tsv"
  { live "$1" "$2" "${4:-0}"; others "$3"; } > "$T_STUB/squeue.txt"
}
run_rt() {
  local label=$1; shift; RT_LOG="$W/rt_$label.log"
  ( export NC_HOME_ROOT="$FH" NC_SCR_ROOT="$FS" PATH="$T_BIN:$PATH" STUB_DIR="$T_STUB" SQUEUE="$T_BIN/squeue" SACCT="$T_BIN/sacct" SCONTROL="$T_BIN/scontrol" PYTHON="$T_BIN/python3" STAMP
    cd "$W" && bash "$BUN/retune_throttle.sh" "$STAMP" "$@" ) > "$RT_LOG" 2>&1
  RT_RC=$?
}
nscontrol() { t_count_lines "$T_STUB/scontrol_calls.txt"; }
rec_files() { ls "$LOGR/launch" 2>/dev/null | grep -c '^retune_'; }

# ---- raising to alone: admission (64 + others <= 192) -----------------------------------------------------------------------------------------
state 16 3 65; run_rt raise_130 --profile alone --yes
[ "$RT_RC" != 0 ]; t_cond "RT01 raise to alone with 130 billed of other work (64 + 130 = 194 > 192): refused (exit $RT_RC)" $?
t_eq "RT02 ... scontrol is never called" 0 "$(nscontrol)"; t_eq "RT03 ... no retune record" 0 "$(rec_files)"
state 16 3 64; run_rt raise_128_dry --profile alone
t_eq "RT04 raise to alone with 128 billed of other work (64 + 128 = 192): admitted in the dry run, exit 0" 0 "$RT_RC"
t_eq "RT05 ... the dry run does not call scontrol" 0 "$(nscontrol)"; grep -q 7001 "$RT_LOG"; t_cond "RT06 ... and reports the array it would update (7001)" $?
state 16 3 64; run_rt raise_128 --profile alone --yes
t_eq "RT07 the same with --yes: exit 0" 0 "$RT_RC"
grep -q 'JobId=7001 ArrayTaskThrottle=32' "$T_STUB/scontrol_calls.txt"; t_cond "RT08 scontrol update JobId=7001 ArrayTaskThrottle=32 (bench alone)" $?
t_eq "RT09 only this run's array is touched (no other job id, no plain job 7000)" 0 "$(grep -v 'JobId=7001 ' "$T_STUB/scontrol_calls.txt" | wc -l | tr -d ' ')"
t_eq "RT10 ... never a selector (user / name)" 0 "$(grep -c -e '--user' -e ' -u ' -e 'Name=' "$T_STUB/scontrol_calls.txt")"
[ "$(rec_files)" = 1 ]; t_cond "RT11 a record LOG_RUN/launch/retune_<utc>.txt is written" $?
f=$(ls "$LOGR"/launch/retune_* 2>/dev/null | head -n 1); grep -q 7001 "$f" 2>/dev/null; t_cond "RT12 ... it lists the updated array" $?
grep -q '7001_\[40-95%32\]' "$T_STUB/squeue.txt"; t_cond "RT13 the scheduler (squeue) now shows the new %32 on the pending array (confirmation by re-query)" $?
state 16 3 64; touch "$T_STUB/scontrol_noop"; run_rt unconfirmed --profile alone --yes
[ "$RT_RC" != 0 ]; t_cond "RT14 scontrol 'succeeds' but squeue still shows the old %N: NOT confirmed, nonzero exit ($RT_RC)" $?

# ---- M1-style: the live plain own job (s0_verify, 1 CPU, billed 2) is in the plan; only arrays are updated -----------------------------------------
state 16 3 63 1; run_rt plain_ok --profile alone --yes
t_eq "RT20 live plain verify job (2) + array 64 + 126 billed of other work = 192: admitted" 0 "$RT_RC"
f=$(ls "$LOGR"/launch/retune_* 2>/dev/null | head -n 1); grep -q -e '7000' -e 's0_verify' "$f" 2>/dev/null; t_cond "RT21 the record's plan shows the plain job" $?
grep -q 'JobId=7000' "$T_STUB/scontrol_calls.txt"; [ $? -ne 0 ]; t_cond "RT22 ... but the plain job is not updated" $?
state 16 3 64 1; run_rt plain_over --profile alone --yes
[ "$RT_RC" != 0 ] && [ "$(nscontrol)" = 0 ]; t_cond "RT23 the same with 128 billed of other work (2 + 64 + 128 = 194): refused, scontrol not called" $?

# ---- other refusals ------------------------------------------------------------------------------------------------------------------------------
state 16 3 0; printf '9001|lowpH_prodH_s2|RUNNING|2\n' >> "$T_STUB/squeue.txt"; run_rt prodh --profile alone --yes
[ "$RT_RC" != 0 ] && [ "$(nscontrol)" = 0 ]; t_cond "RT30 raise to alone while a _prodH job exists: refused, scontrol not called" $?
state 16 3 0; touch "$T_STUB/squeue_fail"; run_rt sqfail --profile alone --yes
[ "$RT_RC" != 0 ] && [ "$(nscontrol)" = 0 ]; t_cond "RT31 squeue fails: fail closed (exit $RT_RC)" $?
state 16 3 0; run_rt bad_profile --profile sideways --yes
[ "$RT_RC" != 0 ] && [ "$(nscontrol)" = 0 ]; t_cond "RT32 unknown profile: refused" $?

# ---- lowering ----------------------------------------------------------------------------------------------------------------------------------------
state 32 3 70; run_rt lower --profile withH --yes
t_eq "RT40 lowering to withH with 140 billed of other work (32 + 140 = 172): exit 0" 0 "$RT_RC"
grep -q 'JobId=7001 ArrayTaskThrottle=16' "$T_STUB/scontrol_calls.txt"; t_cond "RT41 scontrol: 7001 -> 16" $?
grep -q '7001_\[40-95%16\]' "$T_STUB/squeue.txt"; t_cond "RT42 squeue confirms the lower throttle" $?

# ---- --check-drained: only PROD-L-bench's own RUNNING allocation counts -----------------------------------------------------------------------------------
state 16 16 0; run_rt drained_32 --check-drained
t_eq "RT50 running billed = 32: drained to the withH budget, exit 0" 0 "$RT_RC"; grep -q '32' "$RT_LOG"; t_cond "RT51 ... the output prints 32" $?
state 16 40 0; run_rt drained_80 --check-drained
t_eq "RT52 running billed = 80 (over the withH budget): exit 1 (not drained)" 1 "$RT_RC"; grep -q '80' "$RT_LOG"; t_cond "RT53 ... the output prints 80" $?
state 16 40 400; run_rt drained_other --check-drained
t_eq "RT54 other users' running work is not counted (own 80, others 800): still exit 1" 1 "$RT_RC"
state 16 10 400; run_rt drained_other2 --check-drained
t_eq "RT55 own 20 while others run 800 billed: exit 0" 0 "$RT_RC"
state 16 3 0; touch "$T_STUB/squeue_fail"; run_rt drained_sqfail --check-drained
[ "$RT_RC" != 0 ]; t_cond "RT56 squeue fails: no 'drained' verdict, nonzero exit ($RT_RC)" $?

t_summary
