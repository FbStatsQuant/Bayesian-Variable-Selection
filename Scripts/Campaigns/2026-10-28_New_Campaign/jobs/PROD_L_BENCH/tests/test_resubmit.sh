#!/bin/bash
# test_resubmit.sh -- acceptance tests of make_resubmit.sh STAMP rN and clear_stale.sh (PROD_L_BENCH DESIGN.md section 5).
#   bash test_resubmit.sh WORKDIR
# A case is DONE iff all 8 methods F1..F5, A1..A3 have a valid unit. Routing from the ledger history over `bench` and `benchretry`:
#   never started (deferred / not reached / never submitted)            -> resubmit/bench_rN.tsv
#   exactly one start, ended unit_failed or killed_external             -> resubmit/bench_rN.tsv (one rerun)
#   exactly one start, ended killed_timeout                             -> resubmit/benchretry_rN.tsv (doubled budget, once)
#   anything else (>= 2 starts, or a benchretry attempt already made)   -> resubmit/bench_rN_exceptions.tsv (HQ)
# Gate exits 3 (job active / non-terminal) and 4 (scheduler error), SAME_LIST exit 0 / changed state exit 2 / NOTHING_TO_RESUBMIT exit 0, stale artefacts exit 5 until clear_stale.sh moves them,
# CLOSED piece exit 2. Stale kinds: directory F1.lock ; hidden temp `.F1.rds3a9c` ; incomplete method unit (F2.rds + F2.csv without F2.done).
source "$(dirname "$0")/lib.sh"
t_init "${1:-}" test_resubmit
t_mkbundle "$W/fx" 20261030T1400Z
ST_ID=$T_STAMP
METHODS="F1 F2 F3 F4 F5 A1 A2 A3"
RES="$FS/results/${ST_ID}_lowp_benchres"

# ---- fixtures ----------------------------------------------------------------------------------------------------------------
mk_small_units() {   # 60 cases (tasks of 25: 25, 25, 10), p0020 S1 r001..r060 at c100
  local f="$BUN/lists/units.tsv" i ds
  mkdir -p "$BUN/lists"; printf 'piece\ttask\tunit\tdataset\tscale\trepeat\n' > "$f"
  for i in $(seq 1 60); do printf -v ds 'p0020_S1_r%03d' "$i"; printf 'bench\t%d\t%s_c100\t%s\tc100\t0\n' $(((i - 1) / 25)) "$ds" "$ds" >> "$f"; done
}
CU() { local ds; printf -v ds 'p0020_S1_r%03d' "$1"; echo "${ds}_c100"; }
cdir() { echo "$RES/p0020/$1"; }
mk_method() {   # mk_method CASE M [STATUS_OF_FIRST_RULE] : a valid method unit
  local c=$1 m=$2 st=${3:-ok} d; d=$(cdir "$c"); mkdir -p "$d"; echo "rds $c $m" > "$d/$m.rds"
  printf 'rule_id,role,status,method_id,case_id\nr1,primary,%s,%s,%s\nr2,sensitivity,ok,%s,%s\n' "$st" "$m" "$c" "$m" "$c" > "$d/$m.csv"
  ( cd "$d" && sha256sum "$m.rds" "$m.csv" > "$m.sha256" ); printf 'status %s,ok\nfinished_utc 2026-10-30T13:00:00Z\n' "$st" > "$d/$m.done"
}
mk_case() { local m; for m in $METHODS; do mk_method "$1" "$m" "${2:-ok}"; done; }       # mk_case CASE [STATUS]
mk_rec() {   # mk_rec KIND PIECE CASE TAG : a ledger record (start | end_failed | end_timeout | deferred)
  local kind=$1 piece=$2 u=$3 tag=$4 d="$LOGR/ledger/$2/$3"; mkdir -p "$d"
  case "$kind" in
    start)       printf 'unit=%s piece=%s task=0 job_tag=%s host=host1 start_utc=2026-10-30T13:00:00Z deadline_epoch=1700000000 need_s=780 end_source=x end_epoch=1\n' "$u" "$piece" "$tag" > "$d/$tag.start";;
    end_failed)  printf 'unit=%s rc=1 outcome=unit_failed wall_s=5.0 cli_status=NA cli_skipped=NA end_utc=2026-10-30T13:00:09Z\n' "$u" > "$d/$tag.end";;
    end_timeout) printf 'unit=%s rc=124 outcome=killed_timeout wall_s=600 cli_status=NA cli_skipped=NA end_utc=2026-10-30T13:10:00Z\n' "$u" > "$d/$tag.end";;
    end_ok)      printf 'unit=%s rc=0 outcome=ok wall_s=28 cli_status=ok cli_skipped=NA end_utc=2026-10-30T13:00:30Z\n' "$u" > "$d/$tag.end";;
    deferred)    printf 'unit=%s reason=deadline now_epoch=1700000000 deadline_epoch=1700000100 need_s=780 end_source=x end_epoch=1\n' "$u" > "$d/$tag.deferred";;
  esac
}
mk_jobs() {
  printf 'wave\tstep\tjobid\tarray\tdependency\nmain\ts0_verify\t7001\t-\t-\nmain\ts1_bench\t7002\t0-95%%32\tafterok:7001\nmain\ts9_collect\t7003\t-\tafterany:7001:7002\n' > "$RUNH/JOBIDS.tsv"
  mkdir -p "$LOGR"; cp "$RUNH/JOBIDS.tsv" "$LOGR/jobids.tsv"
  printf '7001|lowpB_s0_verify|COMPLETED|0:0|00:01:00|60|2|commons|commons\n7002|lowpB_s1_bench|COMPLETED|0:0|01:00:00|3600|2|commons|commons\n7002_0|lowpB_s1_bench|COMPLETED|0:0|01:00:00|3600|2|commons|commons\n7002_1|lowpB_s1_bench|TIMEOUT|0:15|01:00:00|3600|2|commons|commons\n7003|lowpB_s9_collect|COMPLETED|0:0|00:00:30|30|2|commons|commons\n' > "$T_STUB/sacct.txt"
  : > "$T_STUB/squeue.txt"; rm -f "$T_STUB/squeue_fail" "$T_STUB/sacct_fail"
}
build_state() {
  chmod -R u+rwx "$FS/results" 2>/dev/null; rm -rf "$FS/results" "$LOGR" "$RUNH/resubmit" "$RUNH/JOBIDS.tsv" "$RUNH/manifests"; mkdir -p "$RES"; t_stub_reset
  mk_small_units; mk_jobs
  local i
  for i in $(seq 1 20); do mk_case "$(CU $i)"; mk_rec start bench "$(CU $i)" 7002_0; mk_rec end_ok bench "$(CU $i)" 7002_0; done
  mk_method "$(CU 19)" F4 failed                                                    # a committed failed rule stays DONE
  for i in 22 23; do :; done
  # 21: 7 of 8 methods (A3 absent); one start ended unit_failed -> bench_rN
  local m; for m in F1 F2 F3 F4 F5 A1 A2; do mk_method "$(CU 21)" $m; done; mk_rec start bench "$(CU 21)" 7002_0; mk_rec end_failed bench "$(CU 21)" 7002_0
  # 22: all 8 methods but A3's sidecar no longer verifies; one start ended killed_timeout -> benchretry_rN
  mk_case "$(CU 22)"; echo "tampered after the sidecar" >> "$(cdir "$(CU 22)")/A3.rds"; mk_rec start bench "$(CU 22)" 7002_1; mk_rec end_timeout bench "$(CU 22)" 7002_1
  # 23: deferred only (never started) -> bench_rN
  mk_rec deferred bench "$(CU 23)" 7002_1
  # 24: two starts in bench, no result -> exception
  mk_rec start bench "$(CU 24)" 7002_0; mk_rec end_failed bench "$(CU 24)" 7002_0; mk_rec start bench "$(CU 24)" 7002_1; mk_rec end_failed bench "$(CU 24)" 7002_1
  # 25: one start, no end (killed from outside) -> bench_rN
  mk_rec start bench "$(CU 25)" 7002_0
  # 26: one bench start ended killed_timeout AND a benchretry attempt already made -> exception
  mk_rec start bench "$(CU 26)" 7002_0; mk_rec end_timeout bench "$(CU 26)" 7002_0; mk_rec start benchretry "$(CU 26)" 7002_1; mk_rec end_timeout benchretry "$(CU 26)" 7002_1
  # 27: one start in benchretry only (bench record lost) -> exception (a benchretry attempt exists)
  mk_rec start benchretry "$(CU 27)" 7002_1; mk_rec end_failed benchretry "$(CU 27)" 7002_1
  # 28: a method unit of 8 with a malformed CSV (3 columns only); one start ended unit_failed -> bench_rN
  mk_case "$(CU 28)"; printf 'rule_id,status\nr1,ok\n' > "$(cdir "$(CU 28)")/F2.csv"; ( cd "$(cdir "$(CU 28)")" && sha256sum F2.rds F2.csv > F2.sha256 ); mk_rec start bench "$(CU 28)" 7002_0; mk_rec end_failed bench "$(CU 28)" 7002_0
}
EXPECT_BENCH() { local i; for i in 21 23 25 28 $(seq 29 60); do CU "$i"; done; }      # (task, unit) order
run_mr() {   # run_mr LABEL SCRIPT args...
  local label=$1 script=$2; shift 2; MR_LOG="$W/mr_$label.log"
  ( export NC_HOME_ROOT="$FH" NC_SCR_ROOT="$FS" PATH="$T_BIN:$PATH" STUB_DIR="$T_STUB" SQUEUE="$T_BIN/squeue" SACCT="$T_BIN/sacct" PYTHON="$T_BIN/python3" GUARD="$T_BIN/guard_simple" STAMP="$ST_ID"
    cd "$W" && bash "$BUN/$script" "$@" ) > "$MR_LOG" 2>&1
  MR_RC=$?
}
list_units() { awk -F'\t' '$1!="piece" && NF>=3 {print $3}' "$1" 2>/dev/null; }
list_tasks() { awk -F'\t' '$1!="piece" && NF>=3 {print $2}' "$1" 2>/dev/null; }
LISTF() { echo "$RUNH/resubmit/$1_$2.tsv"; }
EXCF() { echo "$RUNH/resubmit/bench_$1_exceptions.tsv"; }
md5of() { md5sum < "$1" 2>/dev/null; }

[ -f "${PRODL_B_SRC:-$B}/make_resubmit.sh" ] && [ -f "${PRODL_B_SRC:-$B}/clear_stale.sh" ]; t_cond "RS00 make_resubmit.sh and clear_stale.sh exist in the bundle" $?

# =========================================== gates ===========================================================================
build_state; echo '7002_5|lowpB_s1_bench|RUNNING|2' > "$T_STUB/squeue.txt"; run_mr gate_active make_resubmit.sh "$ST_ID" r1
t_eq "RS01 a run job is RUNNING in squeue: exit 3" 3 "$MR_RC"; [ ! -e "$(LISTF bench r1)" ]; t_cond "RS01 nothing written" $?
build_state; echo '7002_[6-95%32]|lowpB_s1_bench|PENDING|2' > "$T_STUB/squeue.txt"; run_mr gate_pending make_resubmit.sh "$ST_ID" r1
t_eq "RS02 a run job array is PENDING in squeue: exit 3" 3 "$MR_RC"
build_state; touch "$T_STUB/squeue_fail"; run_mr gate_squeue_fail make_resubmit.sh "$ST_ID" r1
t_eq "RS03 squeue fails: fail closed, exit 4" 4 "$MR_RC"
build_state; printf '7001|a|COMPLETED|0:0|0|0|2|c|c\n7002|a|RUNNING|0:0|0|0|2|c|c\n7003|a|COMPLETED|0:0|0|0|2|c|c\n' > "$T_STUB/sacct.txt"; run_mr gate_sacct_running make_resubmit.sh "$ST_ID" r1
t_eq "RS04 squeue empty but sacct shows a RUNNING job: exit 3" 3 "$MR_RC"
build_state; printf '7001|a|COMPLETED|0:0|0|0|2|c|c\n7003|a|COMPLETED|0:0|0|0|2|c|c\n' > "$T_STUB/sacct.txt"; run_mr gate_sacct_missing make_resubmit.sh "$ST_ID" r1
[ "$MR_RC" != 0 ]; t_cond "RS05 a recorded id (7002) has no accounting row: refused (exit $MR_RC)" $?
build_state; touch "$T_STUB/sacct_fail"; run_mr gate_sacct_fail make_resubmit.sh "$ST_ID" r1
t_eq "RS06 sacct fails: fail closed, exit 4" 4 "$MR_RC"

# =========================================== routing ===========================================================================
build_state; run_mr route make_resubmit.sh "$ST_ID" r1
t_eq "RS10 base state: exit 0" 0 "$MR_RC"
LB=$(LISTF bench r1); LR=$(LISTF benchretry r1); EX=$(EXCF r1)
t_eq "RS11 bench_r1.tsv = never started (23, 29..60) + one start ended unit_failed (21, 28) + killed_external (25), (task, unit) order" "$(EXPECT_BENCH | tr '\n' ' ')" "$(list_units "$LB" | tr '\n' ' ')"
t_eq "RS12 benchretry_r1.tsv = exactly one start ended killed_timeout (22)" "$(CU 22)" "$(list_units "$LR" | tr '\n' ' ' | sed 's/ $//')"
t_eq "RS13 bench_r1_exceptions.tsv = >= 2 starts (24), a benchretry attempt already made (26, 27)" "$(printf '%s\n' "$(CU 24)" "$(CU 26)" "$(CU 27)" | tr '\n' ' ')" "$(list_units "$EX" | tr '\n' ' ')"
for u in 1 2 19 20; do list_units "$LB" "$LR" 2>/dev/null | grep -qx "$(CU $u)"; [ $? -ne 0 ]; t_cond "RS14 done case $(CU $u) is in no list" $?; done
t_eq "RS15 a committed FAILED rule (case 19, F4 failed) stays done: not listed" 0 "$(list_units "$LB" | grep -cx "$(CU 19)")"
list_units "$LB" | grep -qx "$(CU 21)"; t_cond "RS16 a case with only 7 of 8 methods is NOT done (listed)" $?
list_units "$LR" | grep -qx "$(CU 22)"; t_cond "RS17 a case whose A3 sidecar no longer verifies is NOT done" $?
list_units "$LB" | grep -qx "$(CU 28)"; t_cond "RS18 a case with a malformed CSV in one method is NOT done (listed)" $?
t_eq "RS19 bench list: 36 cases (21, 23, 25, 28, 29..60) in chunks of at most 25, renumbered 0..1" "25 11" "$(list_tasks "$LB" | sort -n | uniq -c | awk '{printf "%s%s", (NR>1?" ":""), $1}')"
t_eq "RS20 benchretry list: one case, task 0" "0" "$(list_tasks "$LR" | sort -un | tr '\n' ' ' | sed 's/ $//')"
awk -F'\t' '$1!="piece" && NF>=6 && $1=="bench" && $5=="c100" && $6=="0"' "$LB" | grep -q .; t_cond "RS21 units.tsv format kept (piece bench, scale c100, repeat 0)" $?
awk -F'\t' '$1!="piece" && NF>=6 && $1=="benchretry"' "$LR" | grep -q .; t_cond "RS22 the benchretry rows carry piece benchretry" $?
# idempotence / changed state
M1=$(md5of "$LB"); M2=$(md5of "$LR")
run_mr again make_resubmit.sh "$ST_ID" r1
t_eq "RS30 same state, same wave: exit 0" 0 "$MR_RC"; grep -q SAME_LIST "$MR_LOG"; t_cond "RS31 ... says SAME_LIST" $?
t_eq "RS32 ... both lists unchanged" "$M1 $M2" "$(md5of "$LB") $(md5of "$LR")"
mk_case "$(CU 23)"
run_mr changed make_resubmit.sh "$ST_ID" r1
t_eq "RS33 state changed (case 23 now done), same wave name: exit 2" 2 "$MR_RC"; t_eq "RS34 ... existing lists untouched" "$M1" "$(md5of "$LB")"
run_mr r2 make_resubmit.sh "$ST_ID" r2
t_eq "RS35 new wave name r2: exit 0" 0 "$MR_RC"
t_eq "RS36 r2 bench list has 35 cases (23 gone)" 35 "$(list_units "$(LISTF bench r2)" | wc -l | tr -d ' ')"
# nothing to resubmit
build_state; for i in $(seq 21 60); do mk_case "$(CU $i)"; done
run_mr nothing make_resubmit.sh "$ST_ID" r3
t_eq "RS40 every case done: exit 0" 0 "$MR_RC"; grep -q NOTHING_TO_RESUBMIT "$MR_LOG"; t_cond "RS41 prints NOTHING_TO_RESUBMIT" $?
[ ! -e "$(LISTF bench r3)" ] && [ ! -e "$(LISTF benchretry r3)" ]; t_cond "RS42 writes no list" $?
# only a benchretry list
build_state; for i in $(seq 21 60); do mk_case "$(CU $i)"; done; rm -f "$(cdir "$(CU 30)")/A1.done"; rm -f "$(cdir "$(CU 30)")/A1.rds" "$(cdir "$(CU 30)")/A1.csv" "$(cdir "$(CU 30)")/A1.sha256"
mk_rec start bench "$(CU 30)" 7002_0; mk_rec end_timeout bench "$(CU 30)" 7002_0
run_mr retry_only make_resubmit.sh "$ST_ID" r4
t_eq "RS43 one killed_timeout case, everything else done: exit 0" 0 "$MR_RC"
t_eq "RS44 ... only benchretry_r4.tsv is written (no bench list)" "$(CU 30)|" "$(list_units "$(LISTF benchretry r4)" | tr '\n' ' ' | sed 's/ $//')|$([ -e "$(LISTF bench r4)" ] && echo bench-list-exists)"
# CLOSED
build_state; mkdir -p "$RUNH/manifests"; echo closed > "$RUNH/manifests/bench.CLOSED"; run_mr closed make_resubmit.sh "$ST_ID" r1
t_eq "RS45 a CLOSED bench piece: exit 2" 2 "$MR_RC"; grep -q CLOSED "$MR_LOG"; t_cond "RS46 ... says CLOSED" $?; rm -rf "$RUNH/manifests"

# =========================================== stale artefacts ==================================================================
# kinds (stale_lib.sh, bench version): directory F1.lock ; hidden temp .F1.rds3a9c (and .F1.csv..., .F1.sha256..., .F1.done...) ; incomplete method unit F2.rds + F2.csv without F2.done
stale_make() {   # stale_make KIND CASE
  local d; d=$(cdir "$2"); mkdir -p "$d"
  case "$1" in
    lock)       mkdir -p "$d/F1.lock"; echo "pid 1" > "$d/F1.lock/owner.txt";;
    hidden)     echo partial > "$d/.F1.rds3a9c";;
    hidden_csv) echo partial > "$d/.F3.csv5b21";;
    hidden_done) echo partial > "$d/.A2.done77aa";;
    incomplete) echo partial > "$d/F2.rds"; echo partial > "$d/F2.csv";;
    incomplete_sha) mk_method "$2" F5; rm -f "$d/F5.done";;
  esac
}
for kind in lock hidden hidden_csv hidden_done incomplete incomplete_sha; do
  build_state; stale_make $kind "$(CU 35)"
  run_mr "stale_$kind" make_resubmit.sh "$ST_ID" r1
  t_eq "ST01 stale kind '$kind' next to a listed case: make_resubmit.sh exit 5" 5 "$MR_RC"
  grep -q clear_stale "$MR_LOG"; t_cond "ST02 ... and names clear_stale.sh ($kind)" $?
  [ ! -e "$(LISTF bench r1)" ]; t_cond "ST03 ... no list written ($kind)" $?
  run_mr "csdry_$kind" clear_stale.sh "$ST_ID"
  t_eq "ST04 clear_stale.sh dry run: exit 0 ($kind)" 0 "$MR_RC"
  case $kind in lock) pat='F1.lock';; hidden) pat='.F1.rds3a9c';; hidden_csv) pat='.F3.csv5b21';; hidden_done) pat='.A2.done77aa';; incomplete) pat='F2.rds';; incomplete_sha) pat='F5.rds';; esac
  grep -q -e "$pat" "$MR_LOG"; t_cond "ST05 ... lists '$pat'" $?
  [ -e "$(cdir "$(CU 35)")" ] && find "$(cdir "$(CU 35)")" -mindepth 1 | grep -q .; t_cond "ST06 ... and moved nothing" $?
done
# a stale artefact in an already DONE case also blocks (make_resubmit and make_manifests refuse while ANY exists)
build_state; stale_make hidden "$(CU 5)"; run_mr stale_done_case make_resubmit.sh "$ST_ID" r1
t_eq "ST07 a hidden temp in a DONE case blocks make_resubmit.sh too: exit 5" 5 "$MR_RC"
# clear_stale --yes moves all kinds at once and never deletes
build_state; stale_make lock "$(CU 35)"; stale_make hidden "$(CU 36)"; stale_make incomplete "$(CU 37)"; stale_make hidden_done "$(CU 38)"
echo '7002_5|lowpB_s1_bench|RUNNING|2' > "$T_STUB/squeue.txt"; run_mr cs_active clear_stale.sh "$ST_ID" --yes
t_eq "ST10 --yes while a run job is active: refused, exit 3" 3 "$MR_RC"; [ -d "$(cdir "$(CU 35)")/F1.lock" ]; t_cond "ST11 ... nothing moved" $?
: > "$T_STUB/squeue.txt"; touch "$T_STUB/squeue_fail"; run_mr cs_sqfail clear_stale.sh "$ST_ID" --yes
t_eq "ST12 --yes with squeue failing: refused, exit 4" 4 "$MR_RC"; rm -f "$T_STUB/squeue_fail"
run_mr cs_yes clear_stale.sh "$ST_ID" --yes
t_eq "ST13 --yes: exit 0" 0 "$MR_RC"
left=$(find "$(cdir "$(CU 35)")" "$(cdir "$(CU 36)")" "$(cdir "$(CU 37)")" "$(cdir "$(CU 38)")" -mindepth 1 | wc -l | tr -d ' ')       # the four prepared case folders hold nothing at all now (they had no valid units)
t_eq "ST14 none of the lock directory, hidden temps and the incomplete unit is left in the result folder" 0 "$left"
CL=$(ls -d "$LOGR"/cleanup/*/ 2>/dev/null | head -n 1)
moved=$(find "$CL" \( -name 'F1.lock' -o -name '.F1.rds3a9c' -o -name 'F2.rds' -o -name 'F2.csv' -o -name '.A2.done77aa' \) 2>/dev/null | wc -l | tr -d ' ')
t_eq "ST15 all were MOVED (not deleted) into LOG_RUN/cleanup/<utc>/ (5 items)" 5 "$moved"
find "$CL" -maxdepth 1 -type f | grep -q .; t_cond "ST16 a listing file is written next to them" $?
run_mr after_clear make_resubmit.sh "$ST_ID" r1
t_eq "ST17 after clearing, make_resubmit.sh no longer refuses: exit 0" 0 "$MR_RC"
find "$RUNH" -name '.reconcile*' -o -name '*.out' 2>/dev/null | grep -q .; [ $? -ne 0 ]; t_cond "ST18 no diagnostics files in RUN_HOME" $?

t_summary
