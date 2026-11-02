#!/bin/bash
# test_unlock.sh -- acceptance tests of truth_wave.sh (lock / unlock, B2 never-locked path, per-wave evidence dir) and recover_truth.sh (DESIGN.md section 5).
#   bash test_unlock.sh WORKDIR
# Fake study with 1,200 + 60 truth files (tiny) under HOME/runs/<RID>/study and a STAGED_SHA256.txt built the way stage_local.sh builds it. The Linux-only
# permission helpers of truth_lib.sh (chmod / stat modes; tested on NOTS by test_truth_lock_linux.sh) are replaced by a marker-file stub in the STAGED COPY
# of the bundle; tl_sha_list and truth_wave.sh's hash logic are real. A stub Rscript plays lowp_truth_lock(STUDY, TRUE|FALSE) by creating / removing a marker.
source "$(dirname "$0")/lib.sh"
t_init "${1:-}" test_unlock
STAMP=20261030T1700Z
t_mkbundle "$W/fx" "$STAMP"
[ -f "$BUN/truth_wave.sh" ] && [ -f "$BUN/recover_truth.sh" ]; t_cond "UN00 truth_wave.sh and recover_truth.sh exist in the bundle" $?

# ---- fake study -------------------------------------------------------------------------------------------------------------------
for p in 0020 0030; do
  mkdir -p "$ST/truth/p$p" "$ST/dev/truth/p$p"
  for i in $(seq 1 600); do echo "t$p.$i" > "$ST/truth/p$p/f$i.rds"; done
  for i in $(seq 1 30); do echo "d$p.$i" > "$ST/dev/truth/p$p/f$i.rds"; done
done
mkdir -p "$W/rdir"; echo "# stub" > "$W/rdir/lowp_seal.R"
cat > "$BUN/truth_lib.sh" <<'L'
# STUB for the local test: permission states are Linux-only; a marker file stands for "locked"; hash listing is the real function
tl_trees() { TL_TREES=("$1/truth" "$1/dev/truth"); }
tl_plain_unlock() { rm -f "$1/.locked_marker"; }
tl_verify_open() { local nt nd; nt=$(find "$1/truth" -type f | wc -l); nd=$(find "$1/dev/truth" -type f | wc -l); echo "OPEN_STATE n_truth=$nt n_devtruth=$nd (stub: modes not checked)"; [ ! -e "$1/.locked_marker" ] && [ "$nt" = 1200 ] && [ "$nd" = 60 ]; }
tl_verify_locked() { echo "LOCK_STATE stub marker=$([ -e "$1/.locked_marker" ] && echo yes || echo no)"; [ -e "$1/.locked_marker" ]; }
tl_sha_list() { (cd "$1" && find . -type f -print0 | sort -z | xargs -0 sha256sum) > "$2"; }
L
restage() { ( cd "$FH" && find . -type f ! -name STAGED_SHA256.txt ! -name .locked_marker | LC_ALL=C sort | xargs -d '\n' sha256sum > "runs/$RID/STAGED_SHA256.txt" ); }
restage
echo other > "$RUNH/OWNER"; restage
tw() { # tw MODE [PRE_DIR] : run truth_wave.sh; sets TW_RC, OUT ($W/out.txt)
  rm -f "$W/out.txt"; if [ "$1" = lock ]; then
    RSCRIPT="${TW_R:-$T_BIN/Rscript}" PATH="$T_BIN:$PATH" bash "$BUN/truth_wave.sh" lock "$ST" "$W/rdir" "$W/out.txt" > "$W/tw.log" 2>&1
  else
    RSCRIPT="${TW_R:-$T_BIN/Rscript}" PATH="$T_BIN:$PATH" bash "$BUN/truth_wave.sh" unlock "$ST" "$W/rdir" "$W/out.txt" ${2:+"$2"} > "$W/tw.log" 2>&1
  fi; TW_RC=$?
}
mkev() { # mkev DIR : pre-lock evidence lists of the CURRENT truth state
  mkdir -p "$1"; ( cd "$ST/truth" && find . -type f -print0 | sort -z | xargs -0 sha256sum ) > "$1/pre_truth.sha"; ( cd "$ST/dev/truth" && find . -type f -print0 | sort -z | xargs -0 sha256sum ) > "$1/pre_devtruth.sha"
}
outhas() { grep -q "$1" "$W/out.txt" 2>/dev/null; }

# ---- B2: never-locked path ---------------------------------------------------------------------------------------------------------
mkdir -p "$W/ev_empty"
tw unlock "$W/ev_empty"; t_eq "UN01 never locked (no pre-lock lists), files intact: unlock VERIFIED, exit 0" 0 "$TW_RC"
outhas '^LOCK_NEVER_RAN'; t_cond "UN02 LOCK_NEVER_RAN reported" $?
outhas '^WAVE_UNLOCK_VERIFIED .*sha=staged_equal(1260)'; t_cond "UN03 verified against STAGED_SHA256.txt: staged_equal(1260)" $?
cp "$ST/truth/p0020/f7.rds" "$W/f7.bak"; echo tampered > "$ST/truth/p0020/f7.rds"
tw unlock "$W/ev_empty"; t_eq "UN04 never locked, one truth file CHANGED: FAILS (exit 1)" 1 "$TW_RC"
outhas 'STAGED_DIFFERENT'; t_cond "UN05 STAGED_DIFFERENT reported" $?
cp "$W/f7.bak" "$ST/truth/p0020/f7.rds"
mv "$ST/dev/truth/p0030/f3.rds" "$W/f3.bak"; tw unlock "$W/ev_empty"; t_eq "UN06 never locked, one dev truth file MISSING: FAILS (exit 1)" 1 "$TW_RC"; mv "$W/f3.bak" "$ST/dev/truth/p0030/f3.rds"
mv "$RUNH/STAGED_SHA256.txt" "$W/staged.bak"; tw unlock "$W/ev_empty"; t_eq "UN07 never locked, staging list missing: FAILS (exit 1), never assumed fine" 1 "$TW_RC"
outhas 'STAGED_LIST_MISSING'; t_cond "UN08 STAGED_LIST_MISSING reported" $?
mv "$W/staged.bak" "$RUNH/STAGED_SHA256.txt"
dup=$(grep "/study/truth/p0020/f8.rds" "$RUNH/STAGED_SHA256.txt"); cp "$RUNH/STAGED_SHA256.txt" "$W/staged.bak"
awk -v d="$dup" '/\/study\/truth\/p0020\/f7\.rds$/ { print d; next } { print }' "$W/staged.bak" > "$RUNH/STAGED_SHA256.txt"; echo tampered > "$ST/truth/p0020/f7.rds"
tw unlock "$W/ev_empty"; t_eq "UN09 staging list with a DUPLICATE line hiding a changed file: FAILS (exit 1)" 1 "$TW_RC"
cp "$W/f7.bak" "$ST/truth/p0020/f7.rds"; cp "$W/staged.bak" "$RUNH/STAGED_SHA256.txt"
echo extra > "$ST/truth/p0020/f601.rds"; mv "$ST/truth/p0020/f600.rds" "$W/f600.bak"
tw unlock "$W/ev_empty"; t_eq "UN10 an unlisted file present and a listed file absent (counts still 1,200): FAILS (exit 1)" 1 "$TW_RC"
rm -f "$ST/truth/p0020/f601.rds"; mv "$W/f600.bak" "$ST/truth/p0020/f600.rds"
tw unlock "$W/ev_empty"; t_eq "UN11 after restoring, the never-locked unlock verifies again (exit 0)" 0 "$TW_RC"

# ---- normal lock -> unlock with a per-wave evidence dir -------------------------------------------------------------------------------
mkev "$W/ev_main"
tw lock; t_eq "UN20 wave lock (stub R) then verification: WAVE_LOCK_VERIFIED, exit 0" 0 "$TW_RC"
outhas '^WAVE_LOCK_VERIFIED'; t_cond "UN21 WAVE_LOCK_VERIFIED line written" $?
[ -e "$ST/.locked_marker" ]; t_cond "UN22 the trees are in the locked state" $?
tw unlock "$W/ev_main"; t_eq "UN23 wave unlock with the wave's evidence dir (both lists present, equal): VERIFIED, exit 0" 0 "$TW_RC"
outhas '^WAVE_UNLOCK_VERIFIED .*sha=equal'; t_cond "UN24 sha=equal reported (the pre-lock path, not the never-locked path)" $?
outhas 'LOCK_NEVER_RAN'; [ $? -ne 0 ]; t_cond "UN25 a wave with evidence is never treated as never-locked" $?
[ ! -e "$ST/.locked_marker" ]; t_cond "UN26 the trees are open again" $?

TW_R=/bin/true tw lock; t_eq "UN27 lock whose R call changes nothing (not locked): WAVE_LOCK_FAILED, exit 1" 1 "$TW_RC"
outhas '^WAVE_LOCK_FAILED'; t_cond "UN28 WAVE_LOCK_FAILED reported" $?

tw lock; echo tampered > "$ST/truth/p0030/f9.rds"
tw unlock "$W/ev_main"; t_eq "UN30 a truth file changed while locked: unlock FAILS (exit 1, DIFFERENT)" 1 "$TW_RC"
outhas 'SHA256_AGAINST_PRELOCK DIFFERENT'; t_cond "UN31 SHA256_AGAINST_PRELOCK DIFFERENT reported" $?
echo "t0030.9" > "$ST/truth/p0030/f9.rds"
mkdir -p "$W/ev_one"; cp "$W/ev_main/pre_truth.sha" "$W/ev_one/"
tw unlock "$W/ev_one"; t_eq "UN32 only ONE pre-lock list present (inconsistent evidence): FAILS (exit 1)" 1 "$TW_RC"
outhas 'LOCK_NEVER_RAN'; [ $? -ne 0 ]; t_cond "UN33 ... and is not treated as never-locked" $?

# per-wave evidence: a later wave has its own evidence dir; each unlock compares against its own wave's lists
echo "state B" > "$ST/truth/p0020/f10.rds"; mkev "$W/ev_r1"
tw lock; tw unlock "$W/ev_r1"; t_eq "UN40 wave r1: unlock against ITS evidence dir (taken in state B): VERIFIED (exit 0)" 0 "$TW_RC"
tw lock; tw unlock "$W/ev_main"; t_eq "UN41 the same state against the main wave's older evidence: FAILS (exit 1) -- each wave compares to its own dir" 1 "$TW_RC"
echo "t0020.10" > "$ST/truth/p0020/f10.rds"; tw unlock "$W/ev_main"; t_eq "UN42 state A restored, main evidence: VERIFIED again (exit 0)" 0 "$TW_RC"

# ---- recover_truth.sh ---------------------------------------------------------------------------------------------------------------
printf 'wave\tstep\tjobid\tarray\tdependency\nmain\ts2_smc\t7003\t0-95%%32\t-\n' > "$RUNH/JOBIDS.tsv"
rec() { # rec : run recover_truth.sh with the stub scheduler (squeue text in $T_STUB/squeue.txt, accounting in sacct.txt); F1: needs complete terminal accounting
  ( export NC_HOME_ROOT="$FH" NC_SCR_ROOT="$FS" PATH="$T_BIN:$PATH" STUB_DIR="$T_STUB" SQUEUE="$T_BIN/squeue" SACCT="$T_BIN/sacct" STAMP; bash "$BUN/recover_truth.sh" "$STAMP" > "$W/rec.log" 2>&1 ); REC_RC=$?
}
printf '7003|lowpL_s2_smc|COMPLETED|0:0|00:10:00|600|2|commons|commons\n' > "$T_STUB/sacct.txt"
: > "$ST/.locked_marker"; echo '7003_2|lowpL_s2_smc|RUNNING|2' > "$T_STUB/squeue.txt"; rec
t_eq "UN50 recover_truth: a recorded run job (id in column 3) is active: refused, exit 3" 3 "$REC_RC"; [ -e "$ST/.locked_marker" ]; t_cond "UN50 trees left as they were" $?
echo '9999|lowpL_s3_smcrep|PENDING|2' > "$T_STUB/squeue.txt"; rec
t_eq "UN51 recover_truth: a lowpL_* job not in JOBIDS.tsv is queued: refused, exit 3" 3 "$REC_RC"
rm -f "$T_STUB/squeue.txt"; touch "$T_STUB/squeue_fail"; rec
t_eq "UN52 recover_truth: scheduler cannot be queried: refused, exit 3" 3 "$REC_RC"; rm -f "$T_STUB/squeue_fail"
mv "$RUNH/JOBIDS.tsv" "$W/J.bak"; : > "$T_STUB/squeue.txt"; rec
t_eq "UN53 recover_truth: JOBIDS.tsv missing: refused, exit 3" 3 "$REC_RC"; mv "$W/J.bak" "$RUNH/JOBIDS.tsv"
echo '5555|lowp_p2_smc|RUNNING|2' > "$T_STUB/squeue.txt"; rec
t_eq "UN54 recover_truth: a pilot-named job (lowp_p*) is not a PROD-L job: not a reason to refuse (exit 0)" 0 "$REC_RC"
: > "$ST/.locked_marker"; : > "$T_STUB/squeue.txt"; rec
t_eq "UN55 recover_truth: idle scheduler: reopens and verifies 1200 + 60 (exit 0)" 0 "$REC_RC"
[ ! -e "$ST/.locked_marker" ]; t_cond "UN56 the trees are open afterwards" $?

# ---- F1: recover_truth.sh fails CLOSED on scheduler evidence (squeue AND complete terminal accounting of EVERY recorded id of ANY wave) ----------------
printf 'wave\tstep\tjobid\tarray\tdependency\nmain\ts2_smc\t7003\t0-95%%32\t-\nmain\ts9_collect\t7009\t-\t-\nr1\ts2_smc\t7103\t0-1\t-\n' > "$RUNH/JOBIDS.tsv"
printf '7003|lowpL_s2_smc|COMPLETED|0:0|00:10:00|600|2|commons|commons\n7009|lowpL_s9_collect|COMPLETED|0:0|00:00:10|10|2|commons|commons\n7103_0|lowpL_s2_smc|COMPLETED|0:0|00:10:00|600|2|commons|commons\n7103_1|lowpL_s2_smc|FAILED|0:1|00:10:00|600|2|commons|commons\n' > "$T_STUB/sacct.txt"
: > "$T_STUB/squeue.txt"; : > "$ST/.locked_marker"; rec
t_eq "UN60 (control) all recorded ids terminal (array tasks only for 7103): recovery proceeds, exit 0" 0 "$REC_RC"
: > "$ST/.locked_marker"; echo '7103_1|lowpL_s2_smc|RUNNING|2' > "$T_STUB/squeue.txt"; rec
[ "$REC_RC" != 0 ] && [ -e "$ST/.locked_marker" ]; t_cond "UN61 an earlier/other-wave array task (7103_1) is active: refused (exit $REC_RC), trees untouched" $?
echo '7009|lowpL_s9_collect|RUNNING|2' > "$T_STUB/squeue.txt"; rec
[ "$REC_RC" != 0 ] && [ -e "$ST/.locked_marker" ]; t_cond "UN62 ANY recorded id counts for recovery (a running collector): refused (exit $REC_RC)" $?
: > "$T_STUB/squeue.txt"; touch "$T_STUB/sacct_fail"; rec
[ "$REC_RC" != 0 ] && [ -e "$ST/.locked_marker" ]; t_cond "UN63 sacct fails: refused (exit $REC_RC), trees untouched" $?
rm -f "$T_STUB/sacct_fail"
printf '7003|lowpL_s2_smc|COMPLETED|0:0|00:10:00|600|2|commons|commons\n7009|lowpL_s9_collect|COMPLETED|0:0|00:00:10|10|2|commons|commons\n' > "$T_STUB/sacct.txt"; rec
[ "$REC_RC" != 0 ] && [ -e "$ST/.locked_marker" ]; t_cond "UN64 recorded id 7103 has NO accounting row: refused (exit $REC_RC)" $?
printf '7003|lowpL_s2_smc|COMPLETED|0:0|00:10:00|600|2|commons|commons\n7009|lowpL_s9_collect|RUNNING|0:0|00:00:10|10|2|commons|commons\n7103_0|x|COMPLETED|0:0|0|0|2|c|c\n' > "$T_STUB/sacct.txt"; rec
[ "$REC_RC" != 0 ] && [ -e "$ST/.locked_marker" ]; t_cond "UN65 a non-terminal accounting row (RUNNING): refused (exit $REC_RC)" $?
printf '7003|lowpL_s2_smc|COMPLETED|0:0|00:10:00|600|2|commons|commons\n7009||\n7103_0|x|COMPLETED|0:0|0|0|2|c|c\n' > "$T_STUB/sacct.txt"; rec
[ "$REC_RC" != 0 ] && [ -e "$ST/.locked_marker" ]; t_cond "UN66 an unparsable accounting row (empty state): refused (exit $REC_RC)" $?
echo '7103_1|lowpL_s2_smc|RUNNING|2' > "$T_STUB/squeue_mixed"; : > "$T_STUB/squeue.txt"
printf '7003|a|COMPLETED|0:0|0|0|2|c|c\n7009|a|COMPLETED|0:0|0|0|2|c|c\n7103_0|a|COMPLETED|0:0|0|0|2|c|c\n' > "$T_STUB/sacct.txt"; rec
[ "$REC_RC" != 0 ] && [ -e "$ST/.locked_marker" ]; t_cond "UN67 squeue answers with an active row AND an 'Invalid job id' error (exit 1): no inference from the message, refused (exit $REC_RC)" $?
rm -f "$T_STUB/squeue_mixed"

# ---- F1: the REAL slurm/s8_unlock.sbatch ------------------------------------------------------------------------------------------------------------------
# jobids.tsv of LOG_RUN holds main, r1 and p5 rows; fitting ids (steps s1_..s4_) of ALL waves: 7001 7002 7101 7201. This job unlocks wave r1.
mkdir -p "$RUNH/code/lowp/R" "$LOGR/truthlock/r1"; echo "# stub" > "$RUNH/code/lowp/R/lowp_seal.R"
printf 'wave\tstep\tjobid\tarray\tdependency\nmain\ts0_build\t7000\t-\t-\nmain\ts1_enum30\t7001\t0-23%%4\t-\nmain\ts2_smc\t7002\t0-95%%32\t-\nr1\ts0_lock\t7100\t-\t-\nr1\ts2_smc\t7101\t0-1\t-\nr1\ts8_unlock\t7103\t-\t-\np5\ts4_p5\t7201\t0-3\t-\n' > "$LOGR/jobids.tsv"
cp "$LOGR/jobids.tsv" "$RUNH/JOBIDS.tsv"
ALLOK='7000|lowpL_s0_build|COMPLETED|0:0|00:01:00|60|2|commons|commons\n7001|lowpL_s1_enum30|COMPLETED|0:0|00:01:00|60|16|commons|commons\n7002|lowpL_s2_smc|COMPLETED|0:0|00:01:00|60|2|commons|commons\n7101|lowpL_s2_smc|COMPLETED|0:0|00:01:00|60|2|commons|commons\n7201|lowpL_s4_p5|COMPLETED|0:0|00:01:00|60|2|commons|commons\n'
s8_state() {   # s8_state : locked trees, matching evidence of wave r1, clean receipt, terminal accounting, idle scheduler
  rm -f "$ST/.locked_marker" "$T_STUB/squeue_fail" "$T_STUB/sacct_fail" "$T_STUB/squeue_mixed" "$LOGR/truthlock/r1/WAVE_UNLOCK.txt"; rm -rf "$LOGR/truthlock/r1/evidence"
  mkev "$LOGR/truthlock/r1/evidence"; : > "$ST/.locked_marker"; printf "$ALLOK" > "$T_STUB/sacct.txt"; : > "$T_STUB/squeue.txt"
}
run_s8() {   # run_s8 : S8_RC ; the sbatch script is run as a plain bash script with the stubs (local-test hooks only for modules)
  ( export NC_HOME_ROOT="$FH" NC_SCR_ROOT="$FS" STAMP WAVE=r1 PATH="$T_BIN:$PATH" STUB_DIR="$T_STUB" SQUEUE="$T_BIN/squeue" SACCT="$T_BIN/sacct" \
           PILOT_LOCAL_TEST=1 PILOT_SKIP_MODULES=1 PILOT_TIME_BIN="$T_BIN/gnutime" SLURM_JOB_ID=7103
    cd "$W" && bash "$BUN/slurm/s8_unlock.sbatch" ) > "$W/s8.log" 2>&1
  S8_RC=$?
}
s8_stopped() { [ "$S8_RC" != 0 ] && [ -e "$ST/.locked_marker" ] && ! grep -q 'WAVE_UNLOCK_VERIFIED' "$LOGR/truthlock/r1/WAVE_UNLOCK.txt" 2>/dev/null; }
[ -f "$BUN/slurm/s8_unlock.sbatch" ]; t_cond "S8-00 slurm/s8_unlock.sbatch exists" $?
s8_state; run_s8
t_eq "S8-01 (control) every recorded fitting id of every wave terminal, idle scheduler: unlock proceeds, exit 0" 0 "$S8_RC"
grep -q 'WAVE_UNLOCK_VERIFIED' "$LOGR/truthlock/r1/WAVE_UNLOCK.txt" 2>/dev/null && [ ! -e "$ST/.locked_marker" ]; t_cond "S8-01 WAVE_UNLOCK_VERIFIED recorded, trees open" $?
s8_state; echo '7002_5|lowpL_s2_smc|RUNNING' > "$T_STUB/squeue.txt"; run_s8
s8_stopped; t_cond "S8-02 an active task of an EARLIER wave (7002_5, main) while unlocking r1: STOP (exit $S8_RC), trees stay locked" $?
s8_state; echo '7201_[2-3%2]|lowpL_s4_p5|PENDING' > "$T_STUB/squeue.txt"; run_s8
s8_stopped; t_cond "S8-03 a pending ARRAY of another wave (p5) in squeue: STOP (exit $S8_RC)" $?
s8_state; echo '7101_1|lowpL_s2_smc|RUNNING' > "$T_STUB/squeue.txt"; run_s8
s8_stopped; t_cond "S8-04 an active task of THIS wave's array: STOP (exit $S8_RC)" $?
s8_state; touch "$T_STUB/squeue_fail"; run_s8
s8_stopped; t_cond "S8-05 squeue error: STOP (exit $S8_RC), trees stay locked" $?
s8_state; echo '7002_0|lowpL_s2_smc|RUNNING' > "$T_STUB/squeue_mixed"; run_s8
s8_stopped; t_cond "S8-06 Sol R1 reproduction: an active row AND 'Invalid job id' with exit 1 is NOT read as 'nothing active': STOP (exit $S8_RC)" $?
s8_state; touch "$T_STUB/sacct_fail"; run_s8
s8_stopped; t_cond "S8-07 sacct error: STOP (exit $S8_RC)" $?
s8_state; printf "$ALLOK" | grep -v '^7201|' > "$T_STUB/sacct.txt"; run_s8
s8_stopped; t_cond "S8-08 recorded id 7201 (p5) has NO accounting row: STOP (exit $S8_RC)" $?
s8_state; printf "$ALLOK" | sed 's/^7002|lowpL_s2_smc|COMPLETED/7002|lowpL_s2_smc|RUNNING/' > "$T_STUB/sacct.txt"; run_s8
s8_stopped; t_cond "S8-09 a non-terminal accounting row (7002 RUNNING, empty squeue): STOP (exit $S8_RC)" $?
s8_state; printf "$ALLOK" | sed 's/^7101|lowpL_s2_smc|COMPLETED/7101||/' > "$T_STUB/sacct.txt"; run_s8
s8_stopped; t_cond "S8-10 an unparsable accounting row (7101 with no state): STOP (exit $S8_RC)" $?
s8_state; printf '7000|a|COMPLETED|0:0|0|0|2|c|c\n7001|a|COMPLETED|0:0|0|0|2|c|c\n7002_0|a|COMPLETED|0:0|0|0|2|c|c\n7002_1|a|FAILED|0:1|0|0|2|c|c\n7101_0|a|CANCELLED+|0:0|0|0|2|c|c\n7101_1|a|TIMEOUT|0:0|0|0|2|c|c\n7201_0|a|NODE_FAIL|0:0|0|0|2|c|c\n' > "$T_STUB/sacct.txt"; run_s8
t_eq "S8-11 (control) array ids with task rows only, FAILED/CANCELLED+/TIMEOUT/NODE_FAIL are terminal: unlock proceeds, exit 0" 0 "$S8_RC"
s8_state; echo '9001_4|someone_elses_job|RUNNING' > "$T_STUB/squeue.txt"; run_s8
t_eq "S8-12 (control) a foreign job in the user's queue (id not recorded) does not block: exit 0" 0 "$S8_RC"
s8_state; echo '7003|lowpL_s8_unlock|RUNNING' > "$T_STUB/squeue.txt"; run_s8
t_eq "S8-13 (control) this finalizer itself (a non-fitting id) is in squeue: does not block: exit 0" 0 "$S8_RC"
s8_state; echo '7000|lowpL_s0_build|COMPLETING' > "$T_STUB/squeue.txt"; run_s8
t_eq "S8-14 (control) a recorded NON-fitting id still in squeue (s0_build): not a fitting job, exit 0" 0 "$S8_RC"
rm -f "$ST/.locked_marker"

t_summary
