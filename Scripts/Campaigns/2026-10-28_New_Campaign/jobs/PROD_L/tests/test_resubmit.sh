#!/bin/bash
# test_resubmit.sh -- acceptance tests of make_resubmit.sh and clear_stale.sh (DESIGN.md section 4, D47.2).
#   bash test_resubmit.sh WORKDIR
# A fabricated result tree + ledger + JOBIDS.tsv + stub squeue/sacct under a fake NC_HOME_ROOT/NC_SCR_ROOT. The staged lists/units.tsv is replaced by a small
# one (12 enum20, 60 smc in tasks of 25, 10 smcrep units) so that "expected units" are few; everything else is read as the real script reads it.
source "$(dirname "$0")/lib.sh"
t_init "${1:-}" test_resubmit
t_mkbundle "$W/fx" 20261030T1400Z
ST_ID=$T_STAMP

# ---- fixtures ----------------------------------------------------------------------------------------------------------------
mk_small_units() {
  local f="$BUN/lists/units.tsv" i m ds
  mkdir -p "$BUN/lists"; printf 'piece\ttask\tunit\tdataset\tscale\trepeat\n' > "$f"
  for i in $(seq 1 12); do printf -v ds 'p0020_S1_r%03d' "$i"; printf 'enum20\t0\t%s\t%s\t-\t0\n' "$ds" "$ds" >> "$f"; done
  for i in $(seq 1 60); do printf -v ds 'p0020_S1_r%03d' "$i"; printf 'smc\t%d\t%s_c100\t%s\tc100\t0\n' $(((i - 1) / 25)) "$ds" "$ds" >> "$f"; done
  for i in 1 2 3 4 5; do for m in 1 2; do printf -v ds 'p0020_S1_r%03d' "$i"; printf 'smcrep\t0\t%s_c100_rep%d\t%s\tc100\t%d\n' "$ds" "$m" "$ds" "$m" >> "$f"; done; done
}
SU() { local ds; printf -v ds 'p0020_S1_r%03d' "$1"; echo "${ds}_c100"; }          # smc unit i
EU() { local ds; printf -v ds 'p0020_S1_r%03d' "$1"; echo "$ds"; }                # enum20 unit i
RU() { local ds; printf -v ds 'p0020_S1_r%03d' "$1"; echo "${ds}_c100_rep$2"; }   # smcrep unit i, repeat m
res_dir() { local piece=$1 u=$2 d=$2; [ "$piece" = smcrep ] && d=${u%_rep[0-9]}; echo "$FS/results/${ST_ID}_lowp_${piece}/p0020/$d"; }
prefix_of() { case $1 in enum20|enum30) echo EXACT;; smc) echo SMCBVS;; smcrep) echo "SMCBVS_rep${2##*_rep}";; esac; }
mk_done() {   # mk_done PIECE UNIT : a valid completed unit (files + sidecar listing them + .done)
  local piece=$1 u=$2 d p; d=$(res_dir "$piece" "$u"); p=$(prefix_of "$piece" "$u"); mkdir -p "$d"
  echo "rds $u" > "$d/$p.rds"
  if [ "$piece" = enum20 ]; then
    ( cd "$d" && sha256sum "$p.rds" > "$p.sha256" ); printf '%s\n2026-10-30T13:00:00Z\n' "$(cut -c1-64 "$d/$p.sha256")" > "$d/$p.done"      # the real EXACT.done: hash line + time (F6)
  else
    printf 'rule_id,v3_status,status\nhpm,complete,ok\npip05,complete,ok\n' > "$d/$p.csv"; ( cd "$d" && sha256sum "$p.rds" "$p.csv" > "$p.sha256" )
    printf 'status ok,ok\nfinished_utc 2026-10-30T13:00:00Z\n' > "$d/$p.done"
  fi
}
corrupt_done() { local piece=$1 u=$2 d p; d=$(res_dir "$piece" "$u"); p=$(prefix_of "$piece" "$u"); echo "tampered after the sidecar was written" >> "$d/$p.rds"; }
mk_rec() {   # mk_rec KIND PIECE UNIT TAG : a ledger record (start | end | deferred)
  local kind=$1 piece=$2 u=$3 tag=$4 d="$LOGR/ledger/$2/$3"; mkdir -p "$d"
  case "$kind" in
    start)    printf 'unit=%s piece=%s task=0 job_tag=%s host=host1 start_utc=2026-10-30T13:00:00Z deadline_epoch=1700000000 need_s=14880\n' "$u" "$piece" "$tag" > "$d/$tag.start";;
    end)      printf 'unit=%s rc=1 outcome=unit_failed wall_s=5.0 cli_status=NA cli_skipped=NA end_utc=2026-10-30T13:00:09Z\n' "$u" > "$d/$tag.end";;
    deferred) printf 'unit=%s reason=deadline now_epoch=1700000000 deadline_epoch=1700000100 need_s=14880\n' "$u" > "$d/$tag.deferred";;
  esac
}
mk_jobs() {   # JOBIDS.tsv of the run and a terminal sacct
  printf 'wave\tstep\tjobid\tarray\tdependency\nmain\ts0_build\t7001\t-\t-\nmain\ts2_smc\t7002\t0-95%%32\tafterok:7001\nmain\ts9_collect\t7003\t-\tafterany:7001\n' > "$RUNH/JOBIDS.tsv"
  mkdir -p "$LOGR"; cp "$RUNH/JOBIDS.tsv" "$LOGR/jobids.tsv"
  printf '7001|lowpL_s0_build|COMPLETED|0:0|00:01:00|60|2|commons|commons\n7002|lowpL_s2_smc|COMPLETED|0:0|01:00:00|3600|2|commons|commons\n7002_0|lowpL_s2_smc|COMPLETED|0:0|01:00:00|3600|2|commons|commons\n7002_1|lowpL_s2_smc|TIMEOUT|0:15|05:00:00|18000|2|commons|commons\n7003|lowpL_s9_collect|COMPLETED|0:0|00:00:30|30|2|commons|commons\n' > "$T_STUB/sacct.txt"
  : > "$T_STUB/squeue.txt"; rm -f "$T_STUB/squeue_fail" "$T_STUB/sacct_fail"
}
build_state() {   # the base state S for piece smc
  chmod -R u+rwx "$FS/results" 2>/dev/null; rm -rf "$FS/results" "$LOGR" "$RUNH/resubmit" "$RUNH/JOBIDS.tsv"; mkdir -p "$FS/results"; t_stub_reset
  mk_small_units; mk_jobs
  local i
  for i in $(seq 1 20); do mk_done smc "$(SU $i)"; mk_rec start smc "$(SU $i)" 7002_0; mk_rec "end" smc "$(SU $i)" 7002_0 >/dev/null; done
  mk_rec start smc "$(SU 3)" 7002_1                                              # unit 3: two starts but done -> neither listed nor exception
  mk_done smc "$(SU 21)"; corrupt_done smc "$(SU 21)"; mk_rec start smc "$(SU 21)" 7002_0   # corrupted sidecar: NOT done, one start -> listed
  mk_rec deferred smc "$(SU 22)" 7002_1                                          # deferred-only -> listed
  mk_rec start smc "$(SU 23)" 7002_0; mk_rec start smc "$(SU 23)" 7002_1         # two starts, no .done -> exception
  mk_rec start smc "$(SU 24)" 7002_0; mk_rec "end" smc "$(SU 24)" 7002_0         # one failed start -> listed
  mk_done smc "$(SU 25)"; rm -f "$(res_dir smc "$(SU 25)")/SMCBVS.sha256"        # .done without sidecar -> NOT done -> listed
}
EXPECT_LIST() { local i; for i in 21 22 24 25 $(seq 26 60); do SU "$i"; done; }   # in (original task, unit) order
run_mr() {   # run_mr LABEL SCRIPT args...   (SCRIPT = make_resubmit.sh | clear_stale.sh)
  local label=$1 script=$2; shift 2; MR_LOG="$W/mr_$label.log"
  ( export NC_HOME_ROOT="$FH" NC_SCR_ROOT="$FS" PATH="$T_BIN:$PATH" STUB_DIR="$T_STUB" SQUEUE="$T_BIN/squeue" SACCT="$T_BIN/sacct" GUARD="$T_BIN/guard_simple" STAMP="$ST_ID"
    cd "$W" && bash "$BUN/$script" "$@" ) > "$MR_LOG" 2>&1
  MR_RC=$?
}
list_units() { awk -F'\t' '$1!="piece" && NF>=3 {print $3}' "$1" 2>/dev/null; }
list_tasks() { awk -F'\t' '$1!="piece" && NF>=3 {print $2}' "$1" 2>/dev/null; }
LISTF() { echo "$RUNH/resubmit/$1_$2.tsv"; }
EXCF() { echo "$RUNH/resubmit/$1_$2_exceptions.tsv"; }
md5of() { md5sum < "$1" 2>/dev/null; }

[ -f "$BUN/make_resubmit.sh" ] && [ -f "$BUN/clear_stale.sh" ]; t_cond "RS00 make_resubmit.sh and clear_stale.sh exist in the bundle" $?

# =========================================== gates ===========================================================================
build_state; echo '7002_5|lowpL_s2_smc|RUNNING|2' > "$T_STUB/squeue.txt"; run_mr gate_active make_resubmit.sh "$ST_ID" smc r1
t_eq "RS01 a run job is RUNNING in squeue: exit 3" 3 "$MR_RC"
[ ! -e "$(LISTF smc r1)" ] && [ ! -e "$(EXCF smc r1)" ]; t_cond "RS01 nothing written" $?
build_state; echo '7002_[6-95%32]|lowpL_s2_smc|PENDING|2' > "$T_STUB/squeue.txt"; run_mr gate_pending make_resubmit.sh "$ST_ID" smc r1
t_eq "RS02 a run job array is PENDING in squeue: exit 3" 3 "$MR_RC"
build_state; touch "$T_STUB/squeue_fail"; run_mr gate_squeue_fail make_resubmit.sh "$ST_ID" smc r1
t_eq "RS03 squeue fails: fail closed, exit 4" 4 "$MR_RC"; [ ! -e "$(LISTF smc r1)" ]; t_cond "RS03 nothing written" $?
build_state; printf '7002|lowpL_s2_smc|RUNNING|0:0|00:10:00|600|2|commons|commons\n7001|lowpL_s0_build|COMPLETED|0:0|00:01:00|60|2|commons|commons\n' > "$T_STUB/sacct.txt"
run_mr gate_sacct_running make_resubmit.sh "$ST_ID" smc r1
t_eq "RS04 squeue empty but sacct shows a RUNNING job: exit 3" 3 "$MR_RC"
build_state; printf '7002|lowpL_s2_smc|PENDING|0:0|00:00:00|0|2|commons|commons\n7001|lowpL_s0_build|COMPLETED|0:0|00:01:00|60|2|commons|commons\n' > "$T_STUB/sacct.txt"
run_mr gate_sacct_pending make_resubmit.sh "$ST_ID" smc r1
t_eq "RS05 squeue empty but sacct shows a PENDING job (OPS-4 lesson): exit 3" 3 "$MR_RC"
build_state; touch "$T_STUB/sacct_fail"; run_mr gate_sacct_fail make_resubmit.sh "$ST_ID" smc r1
t_eq "RS06 sacct fails: fail closed, exit 4" 4 "$MR_RC"

# =========================================== the list =============================================================================
build_state; run_mr list make_resubmit.sh "$ST_ID" smc r1
t_eq "RS10 base state: exit 0" 0 "$MR_RC"
LF=$(LISTF smc r1)
[ -s "$LF" ]; t_cond "RS11 RUN_HOME/resubmit/smc_r1.tsv written" $?
t_eq "RS12 list = expected units without a verified .done/.sha256, in (task, unit) order" "$(EXPECT_LIST | tr '\n' ' ')" "$(list_units "$LF" | tr '\n' ' ')"
for u in 1 2 5 20; do list_units "$LF" | grep -qx "$(SU $u)"; [ $? -ne 0 ]; t_cond "RS13 verified unit $(SU $u) is not listed" $?; done
list_units "$LF" | grep -qx "$(SU 21)"; t_cond "RS14 a unit with a CORRUPTED sidecar IS listed" $?
list_units "$LF" | grep -qx "$(SU 22)"; t_cond "RS15 a deferred-only unit (never started) is listed" $?
list_units "$LF" | grep -qx "$(SU 24)"; t_cond "RS16 a unit with one failed start is listed (one attempt only)" $?
list_units "$LF" | grep -qx "$(SU 25)"; t_cond "RS17 a unit whose .done has no .sha256 is listed" $?
list_units "$LF" | grep -qx "$(SU 23)"; [ $? -ne 0 ]; t_cond "RS18 a unit with 2 starts and no .done is NOT in the list" $?
EF=$(EXCF smc r1)
list_units "$EF" | grep -qx "$(SU 23)"; t_cond "RS19 ... it is in smc_r1_exceptions.tsv" $?
t_eq "RS20 exceptions file holds only that unit (unit 3 has 2 starts but is done; unit 24 has 1 start)" 1 "$(list_units "$EF" | wc -l | tr -d ' ')"
t_eq "RS21 list rows: 39" 39 "$(list_units "$LF" | wc -l | tr -d ' ')"
t_eq "RS22 tasks renumbered from 0 in chunks of at most 25: sizes" "25 14" "$(list_tasks "$LF" | sort -n | uniq -c | awk '{printf "%s%s", (NR>1?" ":""), $1}')"
t_eq "RS23 task ids are exactly 0 and 1" "0 1" "$(list_tasks "$LF" | sort -un | tr '\n' ' ' | sed 's/ $//')"
t_eq "RS24 units keep their original (task, unit) order across the chunks" "$(EXPECT_LIST | tr '\n' ' ')" "$(awk -F'\t' '$1!="piece" && NF>=3 {print $2 "\t" $3}' "$LF" | sort -s -k1,1n | awk -F'\t' '{print $2}' | tr '\n' ' ')"
t_eq "RS25 piece column is smc on every row" 0 "$(awk -F'\t' '$1!="piece" && NF>=3 && $1!="smc"' "$LF" | wc -l | tr -d ' ')"
awk -F'\t' '$1!="piece" && NF>=6 && $3 ~ /_c100$/ && $5=="c100" && $6=="0"' "$LF" | grep -q .; t_cond "RS26 units.tsv format kept (dataset, scale c100, repeat 0)" $?

# idempotence / changed state
M1=$(md5of "$LF")
run_mr list_again make_resubmit.sh "$ST_ID" smc r1
t_eq "RS30 running twice with the same state: exit 0" 0 "$MR_RC"
grep -q 'SAME_LIST' "$MR_LOG"; t_cond "RS31 ... and says SAME_LIST" $?
t_eq "RS32 ... file unchanged" "$M1" "$(md5of "$LF")"
mk_done smc "$(SU 24)"
run_mr list_changed make_resubmit.sh "$ST_ID" smc r1
t_eq "RS33 state changed (unit 24 now done), same wave name: exit 2 (new WAVE name needed)" 2 "$MR_RC"
t_eq "RS34 ... existing file untouched" "$M1" "$(md5of "$LF")"
run_mr list_r2 make_resubmit.sh "$ST_ID" smc r2
t_eq "RS35 new wave name r2 with the changed state: exit 0" 0 "$MR_RC"
t_eq "RS36 r2 list has 38 units (unit 24 gone), chunks 25 + 13" "38 25 13" "$(list_units "$(LISTF smc r2)" | wc -l | tr -d ' ') $(list_tasks "$(LISTF smc r2)" | sort -n | uniq -c | awk '{printf "%s%s", (NR>1?" ":""), $1}')"

# dry run
build_state; run_mr dry make_resubmit.sh "$ST_ID" smc r7 --dry-run
t_eq "RS37 --dry-run: exit 0" 0 "$MR_RC"; [ ! -e "$(LISTF smc r7)" ]; t_cond "RS38 --dry-run writes no list file" $?
grep -q "$(SU 26)" "$MR_LOG"; t_cond "RS39 --dry-run reports the units it would list" $?

# nothing to resubmit
build_state; for i in $(seq 21 60); do mk_done smc "$(SU $i)"; done
run_mr nothing make_resubmit.sh "$ST_ID" smc r3
t_eq "RS40 everything done (unit 23 is only an exception): exit 0" 0 "$MR_RC"
grep -q NOTHING_TO_RESUBMIT "$MR_LOG"; t_cond "RS41 prints NOTHING_TO_RESUBMIT" $?
[ ! -e "$(LISTF smc r3)" ]; t_cond "RS42 writes no list file" $?

# stale lock / tmp file for a listed unit
build_state; d=$(res_dir smc "$(SU 26)"); mkdir -p "$d/SMCBVS.lock"; echo "pid 123" > "$d/SMCBVS.lock/owner.txt"
run_mr stale_lock make_resubmit.sh "$ST_ID" smc r4
t_eq "RS50 stale SMCBVS.lock for a listed unit: exit 5" 5 "$MR_RC"
grep -q clear_stale "$MR_LOG"; t_cond "RS51 ... names clear_stale.sh" $?
[ ! -e "$(LISTF smc r4)" ]; t_cond "RS52 ... no list written" $?
build_state; d=$(res_dir smc "$(SU 27)"); mkdir -p "$d"; echo partial > "$d/SMCBVS.rds.tmp.4242"
run_mr stale_tmp make_resubmit.sh "$ST_ID" smc r4
t_eq "RS53 stale *.tmp.* file for a listed unit: exit 5" 5 "$MR_RC"
build_state; d=$(res_dir smc "$(SU 5)"); mkdir -p "$d/SMCBVS.lock"; echo "pid 1" > "$d/SMCBVS.lock/owner.txt"
run_mr stale_unlisted make_resubmit.sh "$ST_ID" smc r4
t_eq "RS54 a lock on a unit that is NOT listed (already done) does not block: exit 0" 0 "$MR_RC"

# prefixes per piece
build_state; for i in 1 2 3 4; do mk_done enum20 "$(EU $i)"; done; mk_done smc "$(SU 5)"            # SMCBVS.* of case 5 is not an EXACT record
mkdir -p "$(res_dir enum20 "$(EU 5)")"; cp "$(res_dir smc "$(SU 5)")"/SMCBVS.* "$(res_dir enum20 "$(EU 5)")/"
run_mr enum make_resubmit.sh "$ST_ID" enum20 r1
t_eq "RS60 enum20: exit 0" 0 "$MR_RC"
t_eq "RS61 enum20: prefix EXACT -- units 5..12 listed (an SMCBVS.done does not count), one task" "$(for i in $(seq 5 12); do EU $i; done | tr '\n' ' ')|0" "$(list_units "$(LISTF enum20 r1)" | tr '\n' ' ')|$(list_tasks "$(LISTF enum20 r1)" | sort -un | tr '\n' ' ' | sed 's/ $//')"
build_state; mk_done smcrep "$(RU 1 1)"; mk_done smcrep "$(RU 2 1)"; mk_done smc "$(SU 3)"
run_mr rep make_resubmit.sh "$ST_ID" smcrep r1
t_eq "RS62 smcrep: exit 0" 0 "$MR_RC"
t_eq "RS63 smcrep: prefix SMCBVS_rep<m> -- 8 units listed (rep1 of datasets 1,2 done; a primary SMCBVS.done in case 3 does not count)" "8|$(RU 1 2)" "$(list_units "$(LISTF smcrep r1)" | wc -l | tr -d ' ')|$(list_units "$(LISTF smcrep r1)" | sed -n 1p)"
list_units "$(LISTF smcrep r1)" | grep -qx "$(RU 1 1)"; [ $? -ne 0 ]; t_cond "RS64 smcrep: a done repeat unit is not listed" $?

# =========================================== clear_stale.sh ====================================================================
build_state; d1=$(res_dir smc "$(SU 26)"); d2=$(res_dir smc "$(SU 27)"); mkdir -p "$d1/SMCBVS.lock" "$d2"
echo "pid 123" > "$d1/SMCBVS.lock/owner.txt"; echo partial > "$d2/SMCBVS.rds.tmp.4242"; echo partial > "$d2/x.tmp"
run_mr cs_dry clear_stale.sh "$ST_ID"
t_eq "CS01 dry run: exit 0" 0 "$MR_RC"
[ -d "$d1/SMCBVS.lock" ] && [ -f "$d2/SMCBVS.rds.tmp.4242" ] && [ -f "$d2/x.tmp" ] && [ ! -e "$LOGR/cleanup" ]; t_cond "CS02 dry run changes nothing (no cleanup folder either)" $?
grep -q 'SMCBVS.lock' "$MR_LOG" && grep -q 'SMCBVS.rds.tmp.4242' "$MR_LOG" && grep -q 'x.tmp' "$MR_LOG"; t_cond "CS03 dry run lists the lock directory and both temporary files" $?
echo '7002_5|lowpL_s2_smc|RUNNING|2' > "$T_STUB/squeue.txt"; run_mr cs_active clear_stale.sh "$ST_ID" --yes
t_eq "CS04 --yes while a run job is active: refused (exit 3)" 3 "$MR_RC"
[ -d "$d1/SMCBVS.lock" ] && [ -f "$d2/x.tmp" ]; t_cond "CS05 ... nothing moved" $?
: > "$T_STUB/squeue.txt"; touch "$T_STUB/squeue_fail"; run_mr cs_sqfail clear_stale.sh "$ST_ID" --yes
t_eq "CS06 --yes with squeue failing: refused (exit 4)" 4 "$MR_RC"; rm -f "$T_STUB/squeue_fail"
run_mr cs_yes clear_stale.sh "$ST_ID" --yes
t_eq "CS07 --yes: exit 0" 0 "$MR_RC"
[ ! -e "$d1/SMCBVS.lock" ] && [ ! -e "$d2/SMCBVS.rds.tmp.4242" ] && [ ! -e "$d2/x.tmp" ]; t_cond "CS08 the lock directory and the temporary files are gone from the result folders" $?
CL=$(ls -d "$LOGR"/cleanup/*/ 2>/dev/null | head -n 1)
[ -n "$CL" ]; t_cond "CS09 they were MOVED to LOG_RUN/cleanup/<utc>/" $?
find "$CL" -name owner.txt | grep -q .; t_cond "CS10 the moved lock keeps its owner.txt (nothing deleted)" $?
find "$CL" -type f -name 'SMCBVS.rds.tmp.4242' | grep -q . && find "$CL" -type f -name 'x.tmp' | grep -q .; t_cond "CS11 the moved temporary files are kept" $?
find "$CL" -maxdepth 1 -type f | grep -q .; t_cond "CS12 a listing file is written next to them" $?
[ -f "$(res_dir smc "$(SU 5)")/SMCBVS.done" ]; t_cond "CS13 verified results were not touched" $?
run_mr list_after_clear make_resubmit.sh "$ST_ID" smc r1
t_eq "CS14 after clear_stale.sh --yes, make_resubmit.sh no longer refuses: exit 0" 0 "$MR_RC"

# =========================================== F5: the REAL CLI temporary names (one shared definition) =====================================================
# enumerator: EXACT.rds.tmp<PID>, EXACT.sha256.tmp<PID>, hidden .done.tmp<PID>, directory .lock ; adapter: SMCBVS.rds.tmp.<PID>, SMCBVS.lock
stale_names=(EXACT.rds.tmp4242 EXACT.sha256.tmp4242 .done.tmp4242 .lock)
for nm in "${stale_names[@]}"; do
  build_state; d=$(res_dir enum20 "$(EU 7)"); mkdir -p "$d"
  case "$nm" in .lock) mkdir -p "$d/.lock"; echo "pid 1" > "$d/.lock/owner";; *) echo partial > "$d/$nm";; esac
  run_mr "stale_enum_$nm" make_resubmit.sh "$ST_ID" enum20 r1
  t_eq "ST01 make_resubmit.sh refuses a stale '$nm' next to a listed unit: exit 5" 5 "$MR_RC"
  grep -q clear_stale "$MR_LOG"; t_cond "ST02 ... and names clear_stale.sh ($nm)" $?
  run_mr "cs_dry_$nm" clear_stale.sh "$ST_ID"
  grep -q -e "$nm" "$MR_LOG"; t_cond "ST03 clear_stale.sh dry run lists '$nm'" $?
done
build_state; i=0
for nm in EXACT.rds.tmp4242 EXACT.sha256.tmp4242 .done.tmp4242 .lock; do
  i=$((i + 1)); d=$(res_dir enum20 "$(EU $((i + 3)))"); mkdir -p "$d"
  case "$nm" in .lock) mkdir -p "$d/.lock"; echo "pid 1" > "$d/.lock/owner";; *) echo "partial $nm" > "$d/$nm";; esac
done
d=$(res_dir smc "$(SU 30)"); mkdir -p "$d/SMCBVS.lock"; echo "pid 2" > "$d/SMCBVS.lock/owner.txt"; echo partial > "$d/SMCBVS.rds.tmp.123"
run_mr cs_all clear_stale.sh "$ST_ID" --yes
t_eq "ST10 clear_stale.sh --yes with all six stale kinds present: exit 0" 0 "$MR_RC"
left=$(find "$FS/results" \( -name '*.lock' -o -name '*.tmp*' \) 2>/dev/null | wc -l | tr -d ' ')
t_eq "ST11 ... none of them is left in the result folders" 0 "$left"
CL=$(ls -d "$LOGR"/cleanup/*/ 2>/dev/null | head -n 1)
moved=$(find "$CL" \( -name 'EXACT.rds.tmp4242' -o -name 'EXACT.sha256.tmp4242' -o -name '.done.tmp4242' -o -name '.lock' -o -name 'SMCBVS.lock' -o -name 'SMCBVS.rds.tmp.123' \) 2>/dev/null | wc -l | tr -d ' ')
t_eq "ST12 ... all six were MOVED into LOG_RUN/cleanup/<utc>/ (not deleted)" 6 "$moved"
find "$CL" -name owner -o -name owner.txt | grep -q .; t_cond "ST13 ... the lock owner files travel with their directories" $?
run_mr after_all_clear make_resubmit.sh "$ST_ID" enum20 r1
t_eq "ST14 after clearing, make_resubmit.sh no longer refuses (enum20): exit 0" 0 "$MR_RC"

# =========================================== F6: strict completion validation shared with make_resubmit.sh ==================================================
# enum20 units 1..5 are malformed in five different ways, 6..12 are valid; smc units 1..6 are malformed, 7 is a committed scientific failure (done), 8..60 valid.
sha_of() { sha256sum "$1" | cut -c1-64; }
chk_enum() { # chk_enum UNIT KIND
  local u=$1 k=$2 d p=EXACT h; d=$(res_dir enum20 "$u"); mkdir -p "$d"; echo "rds $u" > "$d/$p.rds"; h=$(sha_of "$d/$p.rds")
  case $k in
    missing_rds) rm -f "$d/$p.rds"; echo "other file" > "$d/unrelated.bin"; ( cd "$d" && sha256sum unrelated.bin > $p.sha256 ); printf '%s\nt\n' "$(cut -c1-64 "$d/$p.sha256")" > "$d/$p.done";;
    two_lines)   printf '%s  EXACT.rds\n%s  EXACT.rds\n' "$h" "$h" > "$d/$p.sha256"; printf '%s\nt\n' "$h" > "$d/$p.done";;
    done_other)  printf '%s  EXACT.rds\n' "$h" > "$d/$p.sha256"; printf '%s\nt\n' "$(printf 'x' | sha256sum | cut -c1-64)" > "$d/$p.done";;
    empty_rds)   : > "$d/$p.rds"; h=$(sha_of "$d/$p.rds"); printf '%s  EXACT.rds\n' "$h" > "$d/$p.sha256"; printf '%s\nt\n' "$h" > "$d/$p.done";;
    wrong_name)  printf '%s  other.rds\n' "$h" > "$d/$p.sha256"; printf '%s\nt\n' "$h" > "$d/$p.done";;
  esac
}
chk_smc() { # chk_smc UNIT KIND
  local u=$1 k=$2 d p=SMCBVS; d=$(res_dir smc "$u"); mkdir -p "$d"; echo "rds $u" > "$d/$p.rds"
  printf 'rule_id,v3_status,status\nhpm,complete,ok\npip05,complete,ok\n' > "$d/$p.csv"; printf 'status ok,ok\nfinished_utc t\n' > "$d/$p.done"
  case $k in
    one_line)  ( cd "$d" && sha256sum $p.rds > $p.sha256 );;
    duplicate) ( cd "$d" && sha256sum $p.rds $p.rds > $p.sha256 );;
    bad_done)  ( cd "$d" && sha256sum $p.rds $p.csv > $p.sha256 ); printf 'garbage marker\n' > "$d/$p.done";;
    bad_csv)   printf 'rule_id,foo\nhpm,1\npip05,2\n' > "$d/$p.csv"; ( cd "$d" && sha256sum $p.rds $p.csv > $p.sha256 );;
    three_rows) printf 'rule_id,v3_status,status\nhpm,complete,ok\npip05,complete,ok\nx,complete,ok\n' > "$d/$p.csv"; ( cd "$d" && sha256sum $p.rds $p.csv > $p.sha256 );;
    escaping)  echo "elsewhere" > "$d/../escape.rds"; ( cd "$d" && sha256sum ../escape.rds $p.csv > $p.sha256 );;
    failure_ok) printf 'rule_id,v3_status,status\nhpm,resource_limit,failed\npip05,resource_limit,failed\n' > "$d/$p.csv"; ( cd "$d" && sha256sum $p.rds $p.csv > $p.sha256 ); printf 'status failed,failed\nfinished_utc t\n' > "$d/$p.done";;
  esac
}
build_state; for i in $(seq 6 12); do mk_done enum20 "$(EU $i)"; done
n=0; for k in missing_rds two_lines done_other empty_rds wrong_name; do n=$((n + 1)); chk_enum "$(EU $n)" $k; done
for i in $(seq 8 60); do :; done
run_mr strict_enum make_resubmit.sh "$ST_ID" enum20 r1
t_eq "VE00 enum20 with 5 malformed and 7 valid completions: exit 0" 0 "$MR_RC"
t_eq "VE01 only the 5 malformed units are listed (missing RDS with a sidecar for another file; two-line sidecar; .done of another hash; empty RDS; sidecar naming another file)" "$(for i in 1 2 3 4 5; do EU $i; done | tr '\n' ' ')" "$(list_units "$(LISTF enum20 r1)" | tr '\n' ' ')"
build_state; SMC_BAD=(1 2 4 5 6 8); n=0     # units 3 and 23 are avoided: build_state gives them two starts (exception rule)
for k in one_line duplicate bad_done bad_csv three_rows escaping; do chk_smc "$(SU "${SMC_BAD[$n]}")" $k; n=$((n + 1)); done
chk_smc "$(SU 7)" failure_ok
run_mr strict_smc make_resubmit.sh "$ST_ID" smc r1
t_eq "VE10 smc strict controls: exit 0" 0 "$MR_RC"
l=$(list_units "$(LISTF smc r1)" | tr '\n' ' ')
for n in "${SMC_BAD[@]}"; do case " $l " in *" $(SU $n) "*) t_ok "VE11 malformed SMC completion (unit $n) is NOT done (listed)";; *) t_bad "VE11 malformed SMC completion (unit $n) is NOT done (listed)";; esac; done
case " $l " in *" $(SU 7) "*) t_bad "VE12 a committed scientific failure (valid record, status failed, v3_status resource_limit) stays DONE";; *) t_ok "VE12 a committed scientific failure (valid record, status failed, v3_status resource_limit) stays DONE";; esac
case " $l " in *" $(SU 9) "*) t_bad "VE13 a valid ordinary completion stays done";; *) t_ok "VE13 a valid ordinary completion stays done";; esac

# =========================================== F11: no diagnostics in home =====================================================================================
find "$RUNH" -name '.reconcile*' -o -name '*.out' 2>/dev/null | grep -q .; [ $? -ne 0 ]; t_cond "ST20 no reconcile/diagnostic .out files appear in RUN_HOME after the resubmit runs" $?

t_summary
