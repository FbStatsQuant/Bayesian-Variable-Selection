#!/bin/bash
# test_collect.sh -- slurm/s9_collect.sbatch of the benchmark wave (PROD_L_BENCH DESIGN.md section 4): NO truth, so NO unlock receipt is involved. The collector writes the
# accounting snapshot accounting/<wave>/sacct_collector.tsv, requires every predecessor of the wave to be TERMINAL (whitelist: COMPLETED FAILED CANCELLED* TIMEOUT OUT_OF_MEMORY
# NODE_FAIL PREEMPTED BOOT_FAIL DEADLINE; anything else is non-terminal -> exit 1, guard not called), then runs the guard (home du) and records guard_after.txt.
#   bash test_collect.sh WORKDIR
source "$(dirname "$0")/lib.sh"
t_init "${1:-}" test_collect
STAMP=20261030T2000Z
t_mkbundle "$W/fx" "$STAMP"
[ -f "${PRODL_B_SRC:-$B}/slurm/s9_collect.sbatch" ]; t_cond "CO00 slurm/s9_collect.sbatch exists" $?

state() {   # state : wave r1 with a verify-less array wave: bench array 7101, benchretry array 7102, collector 7104 (self)
  t_stub_reset; chmod -R u+rwx "$LOGR" 2>/dev/null; rm -rf "$LOGR"; mkdir -p "$LOGR"
  printf 'wave\tstep\tjobid\tarray\tdependency\nr1\ts1_bench\t7101\t0-1\t-\nr1\ts2_benchretry\t7102\t0-0\t-\nr1\ts9_collect\t7104\t-\tafterany:7101:7102\n' > "$LOGR/jobids.tsv"
  printf '7101|lowpB_s1_bench|COMPLETED|0:0|01:00:00|3600|2|commons|commons\n7102|lowpB_s2_benchretry|COMPLETED|0:0|00:30:00|1800|2|commons|commons\n' > "$T_STUB/sacct.txt"
  rm -f "$GUARD_LOG"
}
run_co() {
  ( export NC_HOME_ROOT="$FH" NC_SCR_ROOT="$FS" STAMP WAVE=r1 PATH="$T_BIN:$PATH" STUB_DIR="$T_STUB" GUARD="$T_BIN/guard_good" GUARD_LOG SACCT="$T_BIN/sacct" SACCT_HEADER=1 SQUEUE="$T_BIN/squeue" \
           PILOT_LOCAL_TEST=1 PILOT_SKIP_MODULES=1 PILOT_TIME_BIN="$T_BIN/gnutime" SLURM_JOB_ID=7104
    cd "$W" && bash "$BUN/slurm/s9_collect.sbatch" ) > "$W/co_$1.log" 2>&1
  CO_RC=$?
}
guard_calls() { t_count_lines "$GUARD_LOG"; }
A="$LOGR/accounting/r1"

state; run_co terminal
t_eq "CO01 every predecessor terminal (COMPLETED): exit 0" 0 "$CO_RC"
[ "$(guard_calls)" -ge 1 ]; t_cond "CO02 ... the guard IS called" $?
[ -s "$A/sacct_collector.tsv" ] && [ -s "$A/guard_after.txt" ]; t_cond "CO03 ... accounting snapshot and guard_after.txt written" $?
head -n 1 "$A/sacct_collector.tsv" | grep -q 'JobID'; t_cond "CO04 ... the snapshot carries its header" $?
[ ! -e "$A/GUARD_SKIPPED.txt" ]; t_cond "CO05 ... and there is no unlock-receipt logic: no GUARD_SKIPPED.txt" $?
[ ! -d "$LOGR/truthlock" ]; t_cond "CO06 no truthlock folder is read or created (the benchmark wave has no truth)" $?

for st in FAILED CANCELLED TIMEOUT OUT_OF_MEMORY NODE_FAIL PREEMPTED BOOT_FAIL DEADLINE; do
  state; printf '7101_0|a|%s|0:0|0|0|2|c|c\n7101_1|a|COMPLETED|0:0|0|0|2|c|c\n7102|a|COMPLETED|0:0|0|0|2|c|c\n' "$st" > "$T_STUB/sacct.txt"; run_co "term_$st"
  [ "$(guard_calls)" -ge 1 ]; t_cond "CO10 a predecessor in terminal state '$st' does not stop the collector (guard called)" $?
done
state; printf '7101_0|a|CANCELLED by 1234|0:0|0|0|2|c|c\n7101_1|a|CANCELLED+|0:0|0|0|2|c|c\n7102|a|COMPLETED|0:0|0|0|2|c|c\n' > "$T_STUB/sacct.txt"; run_co cancelled_suffix
[ "$(guard_calls)" -ge 1 ]; t_cond "CO11 CANCELLED with any suffix ('by 1234', '+') is terminal" $?

for st in PENDING RUNNING REQUEUED SUSPENDED FOO; do
  state; printf '7101_0|a|COMPLETED|0:0|0|0|2|c|c\n7102|a|%s|0:0|0|0|2|c|c\n' "$st" > "$T_STUB/sacct.txt"; run_co "state_$st"
  [ "$CO_RC" != 0 ] && [ "$(guard_calls)" = 0 ]; t_cond "CO20 a predecessor in state '$st' is not terminal: exit nonzero ($CO_RC), guard NOT called" $?
  [ -s "$A/sacct_collector.tsv" ]; t_cond "CO21 ... the accounting snapshot is still written ($st)" $?
done
state; printf '7101_0|a|COMPLETED|0:0|0|0|2|c|c\n' > "$T_STUB/sacct.txt"; run_co missing_id
[ "$CO_RC" != 0 ] && [ "$(guard_calls)" = 0 ]; t_cond "CO22 an id of the wave (7102) with no accounting row is not terminal: exit nonzero ($CO_RC), guard NOT called" $?
state; rm -f "$LOGR/jobids.tsv"; run_co no_ids
[ "$CO_RC" != 0 ] && [ "$(guard_calls)" = 0 ]; t_cond "CO23 no recorded predecessor ids: exit nonzero, guard NOT called" $?
state; CO_GUARD_RC=1; ( export NC_HOME_ROOT="$FH" NC_SCR_ROOT="$FS" STAMP WAVE=r1 PATH="$T_BIN:$PATH" STUB_DIR="$T_STUB" GUARD="$T_BIN/guard_refuse_always" SACCT="$T_BIN/sacct" SACCT_HEADER=1 SQUEUE="$T_BIN/squeue" \
  PILOT_LOCAL_TEST=1 PILOT_SKIP_MODULES=1 PILOT_TIME_BIN="$T_BIN/gnutime" SLURM_JOB_ID=7104; cd "$W" && bash "$BUN/slurm/s9_collect.sbatch" ) > "$W/co_guard_bad.log" 2>&1; rc=$?
[ "$rc" != 0 ]; t_cond "CO30 the guard refuses after the wave (home over the limit): the collector exits nonzero ($rc)" $?
grep -q 'guard_rc=1' "$A/guard_after.txt" 2>/dev/null; t_cond "CO31 ... and records guard_rc=1" $?

t_summary
