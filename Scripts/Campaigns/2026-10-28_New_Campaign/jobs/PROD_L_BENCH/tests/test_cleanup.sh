#!/bin/bash
# test_cleanup.sh -- acceptance tests of cleanup_bench.sh (DESIGN.md section 8, B3 and Sol pilot finding 1).
#   bash test_cleanup.sh WORKDIR
# cleanup_bench.sh STAMP [--yes] [--receipt FILE] is run FROM INSIDE the run folder it removes (cwd and script file inside HOME/runs/<RID>/code/prod_l) on a
# fake tree with stub squeue/sacct/guard. Targets: HOME/runs/<RID>, SCR/runs/<RID>_cache, SCR/runs/<RID>_tmp. Exit: 0 CLEANUP VERIFIED; 1 UNVERIFIED;
# 3 refused (results/logs still on scratch, OWNER missing/wrong, job active, ids missing); 4 refused (scheduler error, linked ancestor).
source "$(dirname "$0")/lib.sh"
t_init "${1:-}" test_cleanup
STAMP=20261030T1600Z
mkdir -p "$W/receipts"

mkclean() {   # a finished run: staged tree, truth tree, caches, ids with the wave column, a shared code tree that must survive
  t_mkbundle "$W/fx" "$STAMP"; t_stub_reset
  mkdir -p "$ST/inputs/p0020" "$FS/runs/${RID}_cache" "$FS/runs/${RID}_tmp"
  echo t > "$ST/inputs/p0020/x.rds"; echo cache > "$FS/runs/${RID}_cache/c"; echo tmp > "$FS/runs/${RID}_tmp/t"
  mkdir -p "$FH/code/core/shared" "$FH/code/lowp_shared"; echo keep > "$FH/code/core/shared/x"; echo keep > "$FH/code/lowp_shared/y"
  printf 'wave\tstep\tjobid\tarray\tdependency\nmain\ts0_verify\t7001\t-\t-\nmain\ts1_bench\t7002\t0-95%%32\tafterok:7001\nmain\ts9_collect\t7003\t-\tafterany:7001\n' > "$RUNH/JOBIDS.tsv"
  printf '7001|lowpB_s0_verify|COMPLETED|0:0|00:01:00|60|2|commons|commons\n7002|lowpB_s1_bench|COMPLETED|0:0|01:00:00|3600|2|commons|commons\n7003|lowpB_s9_collect|COMPLETED|0:0|00:00:30|30|2|commons|commons\n' > "$T_STUB/sacct.txt"
}
run_clean() {   # run_clean LABEL args... (cwd = the staged bundle folder inside the tree that is removed)
  local label=$1; shift; CL_LOG="$W/clean_$label.log"
  ( export NC_HOME_ROOT="$FH" NC_SCR_ROOT="$FS" GUARD="${CL_GUARD:-$T_BIN/guard_simple}" SQUEUE="${CL_SQ:-$T_BIN/squeue}" SACCT="${CL_SA:-$T_BIN/sacct}" \
           PATH="$T_BIN:$PATH" STUB_DIR="$T_STUB"
    cd "$BUN" && bash "$BUN/cleanup_bench.sh" "$STAMP" "$@" ) > "$CL_LOG" 2>&1
  CL_RC=$?
}
intact() { [ -e "$RUNH/OWNER" ] && [ -e "$ST/inputs/p0020/x.rds" ] && [ -d "$FS/runs/${RID}_cache" ] && [ -d "$FS/runs/${RID}_tmp" ]; }

[ -f "$B/cleanup_bench.sh" ]; t_cond "CU00 cleanup_bench.sh exists in the bundle" $?

# ---- dry run -------------------------------------------------------------------------------------------------------------------
mkclean; run_clean dry
t_eq "CU01 dry run from inside the tree: exit 0" 0 "$CL_RC"
intact; t_cond "CU02 dry run changes nothing" $?
grep -q "runs/$RID" "$CL_LOG"; t_cond "CU03 dry run lists the targets (runs/<RID>)" $?
grep -qi 'from memory' "$CL_LOG"; [ $? -ne 0 ]; t_cond "CU04 dry run does not re-execute" $?

# ---- real removal, from inside ---------------------------------------------------------------------------------------------------
mkclean; REC="$W/receipts/closure_ok.txt"; run_clean yes --yes --receipt "$REC"
t_eq "CU10 --yes run FROM INSIDE runs/<RID> (cwd and script inside): exit 0" 0 "$CL_RC"
grep -q 'CLEANUP VERIFIED' "$CL_LOG"; t_cond "CU11 prints CLEANUP VERIFIED" $?
grep -qi 'from memory' "$CL_LOG"; t_cond "CU12 re-executed from memory after leaving the tree (B3)" $?
[ ! -e "$RUNH" ] && [ ! -e "$FS/runs/${RID}_cache" ] && [ ! -e "$FS/runs/${RID}_tmp" ]; t_cond "CU13 runs/<RID>, _cache and _tmp are gone (no .nfs/silly-rename residue)" $?
[ -e "$FH/code/core/shared/x" ] && [ -e "$FH/code/lowp_shared/y" ]; t_cond "CU14 shared code trees untouched" $?
[ -s "$REC" ]; t_cond "CU15 operational-closure receipt written OUTSIDE the removed tree (--receipt)" $?
grep -q 'VERIFIED' "$REC" 2>/dev/null; t_cond "CU16 the receipt records the verdict" $?
grep -qi 'guard' "$REC" 2>/dev/null; t_cond "CU17 the receipt records the guard result" $?
grep -qi 'residue' "$REC" 2>/dev/null; t_cond "CU18 the receipt records the residue search" $?

# ---- refusals ---------------------------------------------------------------------------------------------------------------------
mkclean; mkdir -p "$FS/results/${RID%_lowp_bench}_lowp_benchres"; run_clean results --yes
t_eq "CU20 results of the run still on scratch (results/<STAMP>_lowp_smc): exit 3" 3 "$CL_RC"; intact; t_cond "CU20 nothing removed" $?
mkclean; mkdir -p "$FS/logs/$RID"; run_clean logs --yes
t_eq "CU21 logs/<RID> still on scratch: exit 3" 3 "$CL_RC"; intact; t_cond "CU21 nothing removed" $?
mkclean; mkdir -p "$FS/results/${RID%_lowp_bench}_lowp_benchres"; run_clean results_dry
t_eq "CU22 results still on scratch, dry run: also refused (exit 3)" 3 "$CL_RC"

mkclean; echo '7002_5|lowpB_s1_bench|RUNNING|2' > "$T_STUB/squeue.txt"; run_clean active --yes
t_eq "CU30 a job of the run (id in JOBIDS.tsv column 3) is RUNNING: exit 3" 3 "$CL_RC"; intact; t_cond "CU30 nothing removed" $?
mkclean; echo '9999|lowpB_s2_benchretry|PENDING|2' > "$T_STUB/squeue.txt"; run_clean active_name --yes
t_eq "CU31 a job named lowpB_* not in JOBIDS.tsv is queued: exit 3" 3 "$CL_RC"; intact; t_cond "CU31 nothing removed" $?
mkclean; printf '7002|lowpB_s1_bench|RUNNING|0:0|00:10:00|600|2|commons|commons\n' > "$T_STUB/sacct.txt"; run_clean sacct_running --yes
t_eq "CU32 squeue empty but sacct shows a RUNNING job: exit 3" 3 "$CL_RC"; intact; t_cond "CU32 nothing removed" $?
mkclean; touch "$T_STUB/squeue_fail"; run_clean sqfail --yes
t_eq "CU33 squeue fails: refused, exit 4" 4 "$CL_RC"; intact; t_cond "CU33 nothing removed" $?
mkclean; touch "$T_STUB/sacct_fail"; run_clean safail --yes
t_eq "CU34 sacct fails: refused, exit 4" 4 "$CL_RC"; intact; t_cond "CU34 nothing removed" $?

mkclean; echo "lowp_pilot $STAMP staged fixture" > "$RUNH/OWNER"; run_clean owner_pilot --yes
t_eq "CU40 OWNER of another campaign ('lowp_pilot <STAMP>'): exit 3" 3 "$CL_RC"; intact; t_cond "CU40 nothing removed" $?
mkclean; echo "lowp_bench 20200101T0000Z staged fixture" > "$RUNH/OWNER"; run_clean owner_stamp --yes
t_eq "CU41 OWNER of another STAMP: exit 3" 3 "$CL_RC"; intact; t_cond "CU41 nothing removed" $?
mkclean; rm -f "$RUNH/OWNER"; run_clean owner_missing --yes
t_eq "CU42 OWNER missing: exit 3" 3 "$CL_RC"; [ -d "$RUNH" ]; t_cond "CU42 nothing removed" $?
mkclean; rm -f "$RUNH/JOBIDS.tsv"; run_clean ids_missing --yes
t_eq "CU43 JOBIDS.tsv missing: exit 3" 3 "$CL_RC"; [ -d "$RUNH" ]; t_cond "CU43 nothing removed" $?

# ---- guard after the removal ------------------------------------------------------------------------------------------------------
mkclean; REC2="$W/receipts/closure_bad.txt"; CL_GUARD="$T_BIN/guard_refuse_always" run_clean guard_bad --yes --receipt "$REC2"
t_eq "CU50 removal done but the final guard refuses: exit 1" 1 "$CL_RC"
grep -q 'CLEANUP UNVERIFIED' "$CL_LOG"; t_cond "CU51 prints CLEANUP UNVERIFIED" $?
[ -s "$REC2" ] && grep -q 'UNVERIFIED' "$REC2"; t_cond "CU52 the receipt is written for an unverified clean-up too" $?
CL_GUARD=""

# ---- linked ancestor (junction on Windows, symlink elsewhere) ------------------------------------------------------------------------
mklink_junction() {   # LINK TARGET
  if [ "$(uname -o 2>/dev/null)" = "Msys" ] || [ "$(uname -o 2>/dev/null)" = "Cygwin" ]; then
    cmd //c "mklink /J $(cygpath -w "$1") $(cygpath -w "$2")" >/dev/null 2>&1 && [ -d "$1" ]
  else ln -s "$2" "$1" && [ -L "$1" ]; fi
}
rmlink() { if [ "$(uname -o 2>/dev/null)" = "Msys" ]; then cmd //c "rmdir $(cygpath -w "$1")" >/dev/null 2>&1 || rm -f "$1"; else rm -f "$1"; fi; }
mkclean; OUT="$W/outside_runs"; rm -rf "$OUT"; mkdir -p "$OUT/$RID"; echo "lowp_bench $STAMP staged OUTSIDE" > "$OUT/$RID/OWNER"
printf 'wave\tstep\tjobid\tarray\tdependency\nmain\ts0_verify\t7001\t-\t-\n' > "$OUT/$RID/JOBIDS.tsv"; echo precious > "$OUT/$RID/precious.txt"
cp "$BUN/cleanup_bench.sh" "$W/cleanup_copy.sh"; mv "$FH/runs" "$FH/runs_real"
if mklink_junction "$FH/runs" "$OUT"; then
  ( export NC_HOME_ROOT="$FH" NC_SCR_ROOT="$FS" GUARD="$T_BIN/guard_simple" SQUEUE="$T_BIN/squeue" SACCT="$T_BIN/sacct" PATH="$T_BIN:$PATH" STUB_DIR="$T_STUB"; bash "$W/cleanup_copy.sh" "$STAMP" --yes > "$W/clean_link.log" 2>&1 ); rc=$?
  t_eq "CU60 'runs' is a linked directory resolving outside the campaign root: refused, exit 4" 4 "$rc"
  [ -e "$OUT/$RID/precious.txt" ]; t_cond "CU61 nothing deleted below the link" $?
  ( export NC_HOME_ROOT="$FH" NC_SCR_ROOT="$FS" GUARD="$T_BIN/guard_simple" SQUEUE="$T_BIN/squeue" SACCT="$T_BIN/sacct" PATH="$T_BIN:$PATH" STUB_DIR="$T_STUB"; bash "$W/cleanup_copy.sh" "$STAMP" > "$W/clean_link2.log" 2>&1 ); rc=$?
  t_eq "CU62 the same link is refused in the dry run (exit 4)" 4 "$rc"
  rmlink "$FH/runs"
else t_bad "CU60-62 linked-ancestor tests SKIPPED (could not create a junction/symlink here)"; fi
mv "$FH/runs_real" "$FH/runs" 2>/dev/null

t_summary
