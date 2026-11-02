#!/bin/bash
# test_collect.sh -- regression tests for F4 of R1_FIX_PLAN.md: the collector (slurm/s9_collect.sbatch) never runs the guard on a locked or unverified tree.
#   bash test_collect.sh WORKDIR
# Always: the accounting snapshot accounting/<wave>/sacct_collector.tsv. The guard (home du) runs ONLY if LOG_RUN/truthlock/<wave>/WAVE_UNLOCK.txt contains
# WAVE_UNLOCK_VERIFIED AND both truth top directories are mode 755. Otherwise accounting/<wave>/GUARD_SKIPPED.txt (with the recover_truth.sh instruction) and exit 1.
# Sol's R1 reproduction: terminal fits + a FAILED unlock still called the guard and returned success.
source "$(dirname "$0")/lib.sh"
t_init "${1:-}" test_collect
STAMP=20261030T2000Z
t_mkbundle "$W/fx" "$STAMP"
[ -f "${PRODL_B_SRC:-$B}/slurm/s9_collect.sbatch" ]; t_cond "CO00 slurm/s9_collect.sbatch exists" $?

state() {   # state : wave r1 with terminal fitting jobs, an open study tree, no unlock record
  t_stub_reset; chmod -R u+rwx "$LOGR" "$ST" 2>/dev/null; rm -rf "$LOGR" "$ST"; mkdir -p "$LOGR/truthlock/r1" "$ST/truth" "$ST/dev/truth"
  printf 'wave\tstep\tjobid\tarray\tdependency\nr1\ts0_truthlock\t7099\t-\t-\nr1\ts0_lock\t7100\t-\t-\nr1\ts2_smc\t7101\t0-1\t-\nr1\ts8_unlock\t7103\t-\t-\nr1\ts9_collect\t7104\t-\t-\n' > "$LOGR/jobids.tsv"
  printf '7099|lowpL_s0_truthlock|COMPLETED|0:0|00:01:00|60|2|commons|commons\n7100|lowpL_s0_lock|COMPLETED|0:0|00:01:00|60|2|commons|commons\n7101|lowpL_s2_smc|COMPLETED|0:0|01:00:00|3600|2|commons|commons\n7103|lowpL_s8_unlock|COMPLETED|0:0|00:00:30|30|2|commons|commons\n' > "$T_STUB/sacct.txt"
  rm -f "$GUARD_LOG"
}
verified() { printf '# wave unlock\nOPEN_STATE n_truth=1200 n_devtruth=60\nSHA256_AGAINST_PRELOCK equal\nWAVE_UNLOCK_VERIFIED OPEN_STATE n_truth=1200 n_devtruth=60 sha=equal\n' > "$LOGR/truthlock/r1/WAVE_UNLOCK.txt"; }
run_co() {   # run_co LABEL : the real collector with the guard stub (it records each call in $GUARD_LOG)
  ( export NC_HOME_ROOT="$FH" NC_SCR_ROOT="$FS" STAMP WAVE=r1 PATH="$T_BIN:$PATH" STUB_DIR="$T_STUB" GUARD="$T_BIN/guard_good" GUARD_LOG SACCT="$T_BIN/sacct" SACCT_HEADER=1 SQUEUE="$T_BIN/squeue" \
           PILOT_LOCAL_TEST=1 PILOT_SKIP_MODULES=1 PILOT_TIME_BIN="$T_BIN/gnutime" SLURM_JOB_ID=7104
    cd "$W" && bash "$BUN/slurm/s9_collect.sbatch" ) > "$W/co_$1.log" 2>&1
  CO_RC=$?
}
guard_calls() { t_count_lines "$GUARD_LOG"; }
A="$LOGR/accounting/r1"
skipped_ok() { [ "$CO_RC" != 0 ] && [ "$(guard_calls)" = 0 ] && [ -s "$A/GUARD_SKIPPED.txt" ] && grep -q 'recover_truth' "$A/GUARD_SKIPPED.txt" && [ -s "$A/sacct_collector.tsv" ]; }

state; verified; run_co verified
t_eq "CO01 verified unlock record and both truth trees 755: exit 0" 0 "$CO_RC"
[ "$(guard_calls)" -ge 1 ]; t_cond "CO02 ... the guard IS called" $?
[ -s "$A/sacct_collector.tsv" ] && [ -s "$A/guard_after.txt" ]; t_cond "CO03 ... accounting snapshot and guard_after.txt written" $?
[ ! -e "$A/GUARD_SKIPPED.txt" ]; t_cond "CO04 ... no GUARD_SKIPPED.txt" $?

state; printf '# wave unlock\nOPEN_STATE n_truth=1200 n_devtruth=60\nWAVE_UNLOCK_FAILED verify=1 sha=skipped\n' > "$LOGR/truthlock/r1/WAVE_UNLOCK.txt"; run_co failed_record
skipped_ok; t_cond "CO10 unlock record says WAVE_UNLOCK_FAILED: guard NOT called, GUARD_SKIPPED.txt names recover_truth.sh, accounting kept, exit nonzero ($CO_RC)" $?
state; run_co no_record
skipped_ok; t_cond "CO11 no unlock record at all (unlock cancelled / never ran / lock never ran): guard NOT called, GUARD_SKIPPED.txt, exit nonzero ($CO_RC)" $?
state; printf '7099|a|COMPLETED|0:0|0|0|2|c|c\n7100|a|COMPLETED|0:0|0|0|2|c|c\n7101|a|COMPLETED|0:0|0|0|2|c|c\n7103|a|FAILED|1:0|0|0|2|c|c\n' > "$T_STUB/sacct.txt"; run_co sol_repro
skipped_ok; t_cond "CO12 Sol R1 reproduction: terminal fits and a FAILED unlock finalizer: guard NOT called, exit nonzero ($CO_RC)" $?
state; printf '7099|a|COMPLETED|0:0|0|0|2|c|c\n7100|a|COMPLETED|0:0|0|0|2|c|c\n7101|a|COMPLETED|0:0|0|0|2|c|c\n7103|a|CANCELLED by 123|0:0|0|0|2|c|c\n' > "$T_STUB/sacct.txt"; run_co cancelled
skipped_ok; t_cond "CO13 the unlock finalizer was CANCELLED: guard NOT called, exit nonzero ($CO_RC)" $?
state; verified; t_lock_truth_sim; run_co locked_trees
skipped_ok; t_cond "CO14 unlock record verified but a truth tree is not mode 755 (stat -c %a = 0; $T_LOCK_MODE): guard NOT called, exit nonzero ($CO_RC)" $?
t_unlock_truth_sim
state; printf '# lock only\nWAVE_LOCK_VERIFIED LOCK_STATE x\n' > "$LOGR/truthlock/r1/WAVE_UNLOCK.txt"; run_co lock_only
skipped_ok; t_cond "CO15 the record holds only a lock line (no WAVE_UNLOCK_VERIFIED): guard NOT called" $?

# the terminal whitelist: anything that is not a known terminal state is non-terminal
for st in PENDING RUNNING REQUEUED SUSPENDED FOO; do
  state; verified; printf '7099|a|COMPLETED|0:0|0|0|2|c|c\n7100|a|COMPLETED|0:0|0|0|2|c|c\n7101|a|%s|0:0|0|0|2|c|c\n7103|a|COMPLETED|0:0|0|0|2|c|c\n' "$st" > "$T_STUB/sacct.txt"; run_co "state_$st"
  [ "$CO_RC" != 0 ] && [ "$(guard_calls)" = 0 ]; t_cond "CO20 a predecessor in state '$st' is not terminal: exit nonzero ($CO_RC), guard NOT called" $?
done
for st in COMPLETED FAILED CANCELLED TIMEOUT OUT_OF_MEMORY NODE_FAIL PREEMPTED BOOT_FAIL DEADLINE; do
  state; verified; printf '7099|a|COMPLETED|0:0|0|0|2|c|c\n7100|a|COMPLETED|0:0|0|0|2|c|c\n7101_0|a|%s|0:0|0|0|2|c|c\n7103|a|COMPLETED|0:0|0|0|2|c|c\n' "$st" > "$T_STUB/sacct.txt"; run_co "term_$st"
  [ "$(guard_calls)" -ge 1 ]; t_cond "CO21 a predecessor in terminal state '$st' does not stop the verified collector (guard called)" $?
done
state; verified; run_co accounting_only
head -n 1 "$A/sacct_collector.tsv" | grep -q 'JobID'; t_cond "CO30 the accounting snapshot always carries its header (JobID ...)" $?

t_summary
