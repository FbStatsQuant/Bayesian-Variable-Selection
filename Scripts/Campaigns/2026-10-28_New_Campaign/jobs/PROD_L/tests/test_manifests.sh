#!/bin/bash
# test_manifests.sh -- acceptance tests of make_manifests.sh STAMP --piece enum20|enum30|smc|smcrep|logs [--allow-incomplete] (DESIGN.md section 8, manager revision after D49)
#   bash test_manifests.sh WORKDIR
# Fake tree with a small staged lists/units.tsv (6 enum20, 2 enum30, 3 smc, 3 smcrep units), fabricated result folders, ledger-free (done units need no ledger),
# stub squeue/sacct, PYTHON = the py -3 forwarding stub (make_manifests.sh calls reconcile_prodl.py through $PYTHON).
# Exit codes: 3 a run job is active, 4 scheduler error, 2 artefact / already closed / tampered manifest, 6 piece not 100 % done (unless --allow-incomplete).
source "$(dirname "$0")/lib.sh"
t_init "${1:-}" test_manifests
STAMP=20261030T1800Z
t_mkbundle "$W/fx" "$STAMP"
SRCB=${PRODL_B_SRC:-$B}
[ -f "$SRCB/make_manifests.sh" ] && [ -f "$SRCB/make_resubmit.sh" ]; t_cond "MM00 make_manifests.sh and make_resubmit.sh exist in the bundle" $?

# ---- fixtures -------------------------------------------------------------------------------------------------------------------
ds() { local p=0020; [ "$1" = enum30 ] && p=0030; printf 'p%s_S1_r%03d' "$p" "$2"; }       # dataset id of piece / index
unit_of() { case "$1" in smc) echo "$(ds smc "$2")_c100";; smcrep) echo "$(ds smcrep "$2")_c100_rep1";; *) ds "$1" "$2";; esac; }
NU=(0 6 2 3 3); declare -A N=([enum20]=6 [enum30]=2 [smc]=3 [smcrep]=3)
mk_small_units() {
  local f="$BUN/lists/units.tsv" p i sc rp
  printf 'piece\ttask\tunit\tdataset\tscale\trepeat\n' > "$f"
  for p in enum20 enum30 smc smcrep; do for i in $(seq 1 "${N[$p]}"); do
    case $p in smc) sc=c100; rp=0;; smcrep) sc=c100; rp=1;; *) sc=-; rp=0;; esac
    printf '%s\t0\t%s\t%s\t%s\t%s\n' "$p" "$(unit_of $p $i)" "$(ds $p $i)" "$sc" "$rp" >> "$f"
  done; done
}
# the frozen scanner's table (columns of tools/p5_scan.R); scan_row CASE_ID BASE REPEAT_M PRIMARY_V3 RETRY_STATE : eligible = resource_limit & retry not done ; launchable = resource_limit & none
P5_HDR=$'case_id\tbase\trepeat_m\tprimary_v3_status\tprimary_status\tprimary_mem_gb\tprimary_hours\tprimary_stop_where\tprimary_stop_phase\tprimary_stop_checkpoint\tprimary_stop_tier\tprimary_stop_iter\tprimary_stop_stage\tprimary_stop_elapsed_s\tprimary_stop_allocation_s\tretry_state\tretry_problem\tretry_artefacts\tretry_v3_status\tretry_status\tretry_stop_where\tretry_stop_phase\tretry_stop_checkpoint\teligible\tlaunchable'
scan_row() {
  local el=FALSE la=FALSE; [ "$4" = resource_limit ] && [ "$5" != done ] && el=TRUE; [ "$4" = resource_limit ] && [ "$5" = none ] && la=TRUE
  printf '%s\t%s\t%s\t%s\tfailed\t2\t4\tNA\tNA\tNA\tNA\tNA\tNA\tNA\tNA\t%s\tNA\tNA\tNA\tNA\tNA\tNA\tNA\t%s\t%s\n' "$1" "$2" "$3" "$4" "$5" "$el" "$la"
}
res_folder() { echo "$FS/results/${STAMP}_lowp_$1"; }
case_dir() { local p=$1 u=$2 d=$2; [ "$p" = smcrep ] && d=${u%_rep[0-9]}; echo "$(res_folder $p)/p${u:1:4}/$d"; }
prefix_of() { case $1 in enum20|enum30) echo EXACT;; smc) echo SMCBVS;; smcrep) echo "SMCBVS_rep${2##*_rep}";; esac; }
mk_done() {
  local piece=$1 u=$2 d p; d=$(case_dir "$piece" "$u"); p=$(prefix_of "$piece" "$u"); mkdir -p "$d"; echo "rds $u" > "$d/$p.rds"
  if [[ $piece == enum* ]]; then
    ( cd "$d" && sha256sum "$p.rds" > "$p.sha256" ); printf '%s\n2026-10-30T13:00:00Z\n' "$(cut -c1-64 "$d/$p.sha256")" > "$d/$p.done"     # real EXACT.done: hash line + time
  else
    printf 'rule_id,v3_status,status\nhpm,complete,ok\npip05,complete,ok\n' > "$d/$p.csv"; ( cd "$d" && sha256sum "$p.rds" "$p.csv" > "$p.sha256" )
    printf 'status ok,ok\nfinished_utc 2026-10-30T13:00:00Z\n' > "$d/$p.done"
  fi
}
build() {   # build : fresh results for all four pieces (all done), JOBIDS, terminal sacct, empty squeue, accounting NOT yet present
  chmod -R u+rwx "$FS/results" "$FS/logs" 2>/dev/null; rm -rf "$FS/results" "$FS/logs" "$RUNH/manifests" "$RUNH/resubmit" "$RUNH/p5" "$RUNH/JOBIDS.tsv"; mkdir -p "$FS/results" "$LOGR/ledger"; t_stub_reset
  mk_small_units
  local p i; for p in enum20 enum30 smc smcrep; do for i in $(seq 1 "${N[$p]}"); do mk_done $p "$(unit_of $p $i)"; done; done
  echo "slurm out" > "$LOGR/slurm-x.out"
  printf 'wave\tstep\tjobid\tarray\tdependency\nmain\ts0_build\t7001\t-\t-\nmain\ts2_smc\t7002\t0-95%%32\tafterok:7001\nmain\ts9_collect\t7003\t-\tafterany:7001\n' > "$RUNH/JOBIDS.tsv"
  printf '7001|lowpL_s0_build|COMPLETED|0:0|00:01:00|60|2|commons|commons\n7002|lowpL_s2_smc|COMPLETED|0:0|01:00:00|3600|2|commons|commons\n7003|lowpL_s9_collect|COMPLETED|0:0|00:00:30|30|2|commons|commons\n' > "$T_STUB/sacct.txt"
  : > "$T_STUB/squeue.txt"
  # F2 / R2 I1: the zero-eligible P5 path -- an empty expected inventory AND a complete FINAL scan (scan_initial.ok no longer suffices): one row per done unit, job id above every fitting job
  mkdir -p "$RUNH/p5" "$LOGR/p5"; printf 'piece\ttask\tunit\tdataset\tscale\trepeat\tbase_piece\n' > "$RUNH/p5/expected.tsv"; echo "none eligible" > "$RUNH/p5/none_eligible.txt"
  echo ok > "$LOGR/p5/scan_initial.ok"
  { echo "$P5_HDR"; for i in 1 2 3; do scan_row "$(unit_of smc $i)" SMCBVS 0 completed none; done; } > "$LOGR/p5/scan_final_smc.tsv"
  { echo "$P5_HDR"; for i in 1 2 3; do scan_row "$(ds smc $i)_c100" SMCBVS_rep1 1 completed none; done; } > "$LOGR/p5/scan_final_smcrep.tsv"; echo ok > "$LOGR/p5/scan_final.ok"
  printf 'p5scan_final\ts5_p5scan\t7400\t-\t-\n' >> "$RUNH/JOBIDS.tsv"; printf '7400|lowpL_s5_p5scan|COMPLETED|0:0|00:01:00|60|2|commons|commons\n' >> "$T_STUB/sacct.txt"
}
add_accounting() { mkdir -p "$LOGR/accounting"; printf 'JobID\tState\n7001\tCOMPLETED\n' > "$LOGR/accounting/sacct_final.tsv"; printf 'step\tcore_h\ntotal\t1.0\n' > "$LOGR/accounting/core_hours.tsv"; }
run_mm() {   # run_mm LABEL args... ; MM_RC MM_LOG
  local label=$1; shift; MM_LOG="$W/mm_$label.log"
  ( export NC_HOME_ROOT="$FH" NC_SCR_ROOT="$FS" PATH="$T_BIN:$PATH" STUB_DIR="$T_STUB" SQUEUE="$T_BIN/squeue" SACCT="$T_BIN/sacct" PYTHON="$T_BIN/python3" GUARD="$T_BIN/guard_simple" STAMP
    cd "$W" && bash "$BUN/make_manifests.sh" "$STAMP" "$@" ) > "$MM_LOG" 2>&1
  MM_RC=$?
}
has_manifest() { [ -e "$(res_folder "$1")/MANIFEST.sha256" ]; }
closed() { [ -e "$RUNH/manifests/$1.CLOSED" ]; }
manifest_lists_files() {   # manifest_lists_files FOLDER : the manifest verifies and names exactly the other files present
  local d=$1 a b
  MF_WHY=""
  MF_WHY=$( cd "$d" && sha256sum --quiet -c MANIFEST.sha256 2>&1 ) || { MF_WHY="sha256sum -c fails: $(echo $MF_WHY | cut -c1-300); first lines: $(head -n 3 "$d/MANIFEST.sha256" | cut -c1-150 | tr '\n' '|')"; mkdir -p "$W/diag"; cp "$d/MANIFEST.sha256" "$W/diag/$(basename "$d").manifest" 2>/dev/null; return 1; }
  MF_WHY=""
  a=$(sed -E 's/^[0-9a-fA-F]{64} [ *]//; s/^\.\///; s/\r$//' "$d/MANIFEST.sha256" | LC_ALL=C sort)
  b=$(cd "$d" && find . -type f ! -name MANIFEST.sha256 | sed 's/^\.\///' | LC_ALL=C sort)
  [ "$a" = "$b" ] && [ -n "$a" ] || { MF_WHY="listed [$(echo $a)] present [$(echo $b)]"; return 1; }
}

# =============================================== gates ===========================================================================
build; echo '7002_5|lowpL_s2_smc|RUNNING|2' > "$T_STUB/squeue.txt"; run_mm gate_active --piece enum20
t_eq "MM01 a run job is RUNNING in squeue: exit 3" 3 "$MM_RC"; has_manifest enum20; [ $? -ne 0 ]; t_cond "MM01 no manifest written" $?
build; touch "$T_STUB/squeue_fail"; run_mm gate_squeue --piece enum20
t_eq "MM02 squeue fails: fail closed, exit 4" 4 "$MM_RC"
build; touch "$T_STUB/sacct_fail"; run_mm gate_sacct --piece enum20
t_eq "MM03 sacct fails: exit 4" 4 "$MM_RC"
build; printf '7002|lowpL_s2_smc|RUNNING|0:0|00:10:00|600|2|commons|commons\n7001|lowpL_s0_build|COMPLETED|0:0|00:01:00|60|2|commons|commons\n' > "$T_STUB/sacct.txt"; run_mm gate_sacct_run --piece enum20
t_eq "MM04 squeue empty but sacct shows a RUNNING job: exit 3" 3 "$MM_RC"

build; mkdir -p "$(case_dir enum20 "$(unit_of enum20 2)")/EXACT.lock"; echo "pid 1" > "$(case_dir enum20 "$(unit_of enum20 2)")/EXACT.lock/owner.txt"; run_mm lock --piece enum20
t_eq "MM05 a *.lock artefact in the folder: exit 2" 2 "$MM_RC"; has_manifest enum20; [ $? -ne 0 ]; t_cond "MM05 no manifest written" $?
build; echo partial > "$(case_dir enum20 "$(unit_of enum20 2)")/EXACT.rds.tmp.4242"; run_mm tmp --piece enum20
t_eq "MM06 a *.tmp.* artefact in the folder: exit 2" 2 "$MM_RC"
build; echo partial > "$(case_dir enum20 "$(unit_of enum20 2)")/x.tmp"; run_mm tmp2 --piece enum20
t_eq "MM07 a *.tmp artefact in the folder: exit 2" 2 "$MM_RC"

# =============================================== completeness =====================================================================
build; rm -f "$(case_dir enum20 "$(unit_of enum20 3)")/EXACT.done"; run_mm incomplete --piece enum20
t_eq "MM10 a piece with a non-done unit: exit 6" 6 "$MM_RC"
has_manifest enum20; [ $? -ne 0 ]; t_cond "MM11 no manifest written" $?; closed enum20; [ $? -ne 0 ]; t_cond "MM11 not CLOSED" $?
run_mm incomplete_ok --piece enum20 --allow-incomplete
t_eq "MM12 same piece with --allow-incomplete: closes, exit 0" 0 "$MM_RC"
has_manifest enum20 && closed enum20; t_cond "MM13 manifest written and CLOSED marker present" $?
build; rm -rf "$(case_dir smc "$(unit_of smc 2)")"; run_mm incomplete_notrun --piece smc
t_eq "MM14 a not_run unit (no result folder at all): exit 6" 6 "$MM_RC"

# =============================================== a complete piece ==================================================================
build; run_mm close_enum20 --piece enum20
t_eq "MM20 complete piece enum20: exit 0" 0 "$MM_RC"
F=$(res_folder enum20)
manifest_lists_files "$F"; t_cond "MM21 MANIFEST.sha256 verifies with sha256sum -c and lists exactly the files present" $?
[ -e "$RUNH/manifests/enum20.CLOSED" ]; t_cond "MM22 RUN_HOME/manifests/enum20.CLOSED written" $?
[ -s "$RUNH/manifests/enum20.inventory.tsv" ]; t_cond "MM23 RUN_HOME/manifests/enum20.inventory.tsv written" $?
[ "$(t_count_lines "$RUNH/manifests/enum20.inventory.tsv")" -ge 7 ]; t_cond "MM23b the inventory lists the 6 expected units (at least header + 6 rows)" $?
S="$RUNH/manifests/summary.tsv"
grep -q "${STAMP}_lowp_enum20" "$S" 2>/dev/null; t_cond "MM24 summary.tsv has a row for the folder" $?
grep -q "$(sha256sum < "$F/MANIFEST.sha256" | cut -c1-64)" "$S" 2>/dev/null; t_cond "MM25 the row carries the manifest sha256" $?
n=$(find "$F" -type f ! -name MANIFEST.sha256 | wc -l | tr -d ' '); grep "${STAMP}_lowp_enum20" "$S" | grep -q -w "$n"; t_cond "MM26 the row carries the file count ($n)" $?
run_mm close_again --piece enum20
t_eq "MM27 closing a CLOSED piece again: exit 2" 2 "$MM_RC"
manifest_lists_files "$F"; t_cond "MM28 ... the manifest is still intact" $?

# the other pieces close independently, each into its own folder
for p in enum30 smc smcrep; do run_mm close_$p --piece $p; t_eq "MM30 complete piece $p: exit 0" 0 "$MM_RC"; manifest_lists_files "$(res_folder $p)"; t_cond "MM31 $p manifest verifies and lists the files" $? "$MF_WHY"; done
t_eq "MM32 summary.tsv now has 4 piece rows" 4 "$(grep -c "_lowp_" "$S")"
# smcrep prefix check is inside the manifest
grep -q 'SMCBVS_rep1\.done' "$(res_folder smcrep)/MANIFEST.sha256"; t_cond "MM33 smcrep manifest lists SMCBVS_rep1.done" $?

# =============================================== existing manifest: revalidated, never replaced ===============================================
build; F=$(res_folder smc); ( cd "$F" && find . -type f | LC_ALL=C sort | xargs sha256sum > "$W/m.new" ); mv "$W/m.new" "$F/MANIFEST.sha256"
before=$(md5sum < "$F/MANIFEST.sha256"); run_mm preexisting --piece smc
t_eq "MM40 an existing VALID manifest (no CLOSED yet) is revalidated and the piece closes: exit 0" 0 "$MM_RC"
t_eq "MM41 ... the existing manifest file is not replaced" "$before" "$(md5sum < "$F/MANIFEST.sha256")"
build; F=$(res_folder smc); ( cd "$F" && find . -type f | LC_ALL=C sort | xargs sha256sum > "$W/m.new" ); mv "$W/m.new" "$F/MANIFEST.sha256"
echo "tampered after the manifest" >> "$(case_dir smc "$(unit_of smc 1)")/SMCBVS.done"; before=$(md5sum < "$F/MANIFEST.sha256"); run_mm tampered --piece smc
t_eq "MM42 an existing manifest that no longer verifies (tampered file): exit 2" 2 "$MM_RC"
t_eq "MM43 ... the manifest is left as it was" "$before" "$(md5sum < "$F/MANIFEST.sha256")"
closed smc; [ $? -ne 0 ]; t_cond "MM44 ... and the piece is not CLOSED" $?

# =============================================== logs ======================================================================================
build; run_mm logs_noacct --piece logs
[ "$MM_RC" != 0 ]; t_cond "MM50 --piece logs before the final accounting files exist: refused (exit $MM_RC)" $?
[ ! -e "$LOGR/MANIFEST.sha256" ]; t_cond "MM50 no logs manifest written" $?
add_accounting; run_mm logs_nopieces --piece logs
[ "$MM_RC" != 0 ]; t_cond "MM51 --piece logs with accounting but no piece CLOSED: refused (exit $MM_RC)" $?
for p in enum20 enum30 smc; do run_mm close2_$p --piece $p; done
run_mm logs_three --piece logs
[ "$MM_RC" != 0 ]; t_cond "MM52 --piece logs with only 3 of 4 pieces CLOSED: refused (exit $MM_RC)" $?
[ ! -e "$LOGR/MANIFEST.sha256" ]; t_cond "MM52 no logs manifest written" $?
run_mm close2_smcrep --piece smcrep
run_mm logs_ok --piece logs
t_eq "MM53 --piece logs with accounting and all four pieces CLOSED: exit 0" 0 "$MM_RC"
manifest_lists_files "$LOGR"; t_cond "MM54 logs/<RID>/MANIFEST.sha256 verifies and lists exactly the files present" $?
[ -e "$RUNH/manifests/logs.CLOSED" ]; t_cond "MM55 logs.CLOSED written" $?
grep -q "$RID" "$S" 2>/dev/null; t_cond "MM56 summary.tsv has the logs row" $?

# =============================================== CLOSED pieces are refused by make_resubmit.sh =====================================================
build; run_mm pre_close --piece smc; t_eq "MM60 (setup) smc closed" 0 "$MM_RC"
# make the piece look incomplete after the fact: a resubmission request must still be refused because it is CLOSED
rm -f "$(case_dir smc "$(unit_of smc 2)")/SMCBVS.done"
( export NC_HOME_ROOT="$FH" NC_SCR_ROOT="$FS" PATH="$T_BIN:$PATH" STUB_DIR="$T_STUB" SQUEUE="$T_BIN/squeue" SACCT="$T_BIN/sacct" STAMP; cd "$W" && bash "$BUN/make_resubmit.sh" "$STAMP" smc r1 ) > "$W/mr_closed.log" 2>&1; rc=$?
t_eq "MM61 make_resubmit.sh on a CLOSED piece: exit 2" 2 "$rc"
grep -q 'CLOSED' "$W/mr_closed.log"; t_cond "MM62 ... and says CLOSED" $?
[ ! -e "$RUNH/resubmit/smc_r1.tsv" ]; t_cond "MM63 ... no list written" $?
( export NC_HOME_ROOT="$FH" NC_SCR_ROOT="$FS" PATH="$T_BIN:$PATH" STUB_DIR="$T_STUB" SQUEUE="$T_BIN/squeue" SACCT="$T_BIN/sacct" STAMP; cd "$W" && bash "$BUN/make_resubmit.sh" "$STAMP" enum20 r1 ) > "$W/mr_open.log" 2>&1; rc=$?
t_eq "MM64 (control) make_resubmit.sh on a piece that is NOT closed still works: exit 0" 0 "$rc"

# =============================================== F11 / F7: diagnostics on scratch, CLOSED carries the inventory hash ========================================
build; run_mm close_diag --piece enum20; t_eq "MM70 (setup) enum20 closed" 0 "$MM_RC"
ls "$LOGR/reconcile" 2>/dev/null | grep -q '_enum20\.out$'; t_cond "MM71 the reconcile stdout/stderr is kept in LOG_RUN/reconcile/<utc>_enum20.out (scratch)" $?
t_eq "MM72 RUN_HOME/manifests holds only the CLOSED marker, the inventory, the saved exceptions snapshot (R2 I2) and summary.tsv (no diagnostics in home)" "enum20.CLOSED enum20.exceptions.tsv enum20.inventory.tsv summary.tsv " "$(ls -A "$RUNH/manifests" | tr '\n' ' ')"
find "$RUNH" -name '.reconcile*' | grep -q .; [ $? -ne 0 ]; t_cond "MM73 no .reconcile_* diagnostics anywhere under RUN_HOME" $?
want=$(sha256sum "$RUNH/manifests/enum20.inventory.tsv" | cut -c1-64)
grep -q "inventory_sha256=$want" "$RUNH/manifests/enum20.CLOSED"; t_cond "MM74 enum20.CLOSED records inventory_sha256=<sha of enum20.inventory.tsv>" $?

# =============================================== F5: the real CLI temporary names block closing until cleared ===============================================
for nm in EXACT.rds.tmp4242 EXACT.sha256.tmp4242 .done.tmp4242 .lock; do
  build; d=$(case_dir enum20 "$(unit_of enum20 2)")
  case "$nm" in .lock) mkdir -p "$d/.lock"; echo "pid 1" > "$d/.lock/owner";; *) echo partial > "$d/$nm";; esac
  run_mm "stale_$nm" --piece enum20
  t_eq "MM80 stale '$nm' in the piece folder: exit 2" 2 "$MM_RC"; has_manifest enum20; [ $? -ne 0 ]; t_cond "MM80 no manifest written ($nm)" $?
  ( export NC_HOME_ROOT="$FH" NC_SCR_ROOT="$FS" PATH="$T_BIN:$PATH" STUB_DIR="$T_STUB" SQUEUE="$T_BIN/squeue" SACCT="$T_BIN/sacct" STAMP; cd "$W" && bash "$BUN/clear_stale.sh" "$STAMP" --yes ) > "$W/cs_$nm.log" 2>&1
  [ ! -e "$d/$nm" ]; t_cond "MM81 clear_stale.sh --yes moves '$nm'" $?
  run_mm "cleared_$nm" --piece enum20
  t_eq "MM82 after clearing, enum20 closes: exit 0" 0 "$MM_RC"
done
build; d=$(case_dir smc "$(unit_of smc 2)"); echo partial > "$d/SMCBVS.rds.tmp.123"; run_mm stale_smc_tmp --piece smc
t_eq "MM83 adapter-style SMCBVS.rds.tmp.123: exit 2" 2 "$MM_RC"

# =============================================== F6: strict validation inside the close gate ==================================================================
build; d=$(case_dir enum20 "$(unit_of enum20 2)"); : > "$d/EXACT.rds"; ( cd "$d" && sha256sum EXACT.rds > EXACT.sha256 ); printf '%s\nt\n' "$(cut -c1-64 "$d/EXACT.sha256")" > "$d/EXACT.done"
run_mm strict_empty --piece enum20
t_eq "MM90 an EMPTY EXACT.rds with a matching sidecar and marker is not a completion: exit 6" 6 "$MM_RC"
build; d=$(case_dir smc "$(unit_of smc 2)"); printf 'rule_id,foo\nhpm,1\npip05,2\n' > "$d/SMCBVS.csv"; ( cd "$d" && sha256sum SMCBVS.rds SMCBVS.csv > SMCBVS.sha256 )
run_mm strict_csv --piece smc
t_eq "MM91 a malformed SMC CSV (no status/v3_status columns): exit 6" 6 "$MM_RC"

# =============================================== F2: closing smc / smcrep needs a reconciled P5 phase =====================================================
# State: 3 smc units; units 1 and 2 are native resource_limit primaries and are the EXPECTED P5 units (expected.tsv). P5 wave job 7300; scans are jobs of wave 'p5scan_<phase>'.
p5_scan_row() { # p5_scan_row CASE_ID RETRY_STATE : one row with the columns of the frozen p5_scan.R (only the ones the gate reads are meaningful)
  printf '%s\tSMCBVS\t0\tresource_limit\tfailed\t2\t4\tNA\tNA\tNA\tNA\tNA\tNA\tNA\tNA\t%s\tNA\tNA\tNA\tNA\tNA\tNA\tNA\t%s\t%s\n' "$1" "$2" "$([ "$2" = done ] && echo FALSE || echo TRUE)" "$([ "$2" = none ] && echo TRUE || echo FALSE)"
}
P5_HDR=$'case_id\tbase\trepeat_m\tprimary_v3_status\tprimary_status\tprimary_mem_gb\tprimary_hours\tprimary_stop_where\tprimary_stop_phase\tprimary_stop_checkpoint\tprimary_stop_tier\tprimary_stop_iter\tprimary_stop_stage\tprimary_stop_elapsed_s\tprimary_stop_allocation_s\tretry_state\tretry_problem\tretry_artefacts\tretry_v3_status\tretry_status\tretry_stop_where\tretry_stop_phase\tretry_stop_checkpoint\teligible\tlaunchable'
mk_retry() { # mk_retry UNIT : a valid P5 retry record next to the primary
  local u=$1 d; d="$(case_dir smc "$u")/P5_retry"; mkdir -p "$d"; echo "retry rds $u" > "$d/SMCBVS_p5retry.rds"
  printf 'rule_id,v3_status,status\nhpm,complete,ok\npip05,complete,ok\n' > "$d/SMCBVS_p5retry.csv"; ( cd "$d" && sha256sum SMCBVS_p5retry.rds SMCBVS_p5retry.csv > SMCBVS_p5retry.sha256 )
  printf 'status ok,ok\nfinished_utc t\n' > "$d/SMCBVS_p5retry.done"
}
build_p5() { # build_p5 RETRY1 RETRY2 FINALJOB : retry states in the final scan table (done|none), id of the final scan job
  build; local u1 u2 d; u1=$(unit_of smc 1); u2=$(unit_of smc 2)
  for u in $u1 $u2; do d=$(case_dir smc "$u"); printf 'rule_id,v3_status,status\nhpm,resource_limit,failed\npip05,resource_limit,failed\n' > "$d/SMCBVS.csv"
    ( cd "$d" && sha256sum SMCBVS.rds SMCBVS.csv > SMCBVS.sha256 ); printf 'status failed,failed\nfinished_utc t\n' > "$d/SMCBVS.done"; done
  printf 'piece\ttask\tunit\tdataset\tscale\trepeat\tbase_piece\np5\t0\t%s\t%s\tc100\t0\tsmc\np5\t1\t%s\t%s\tc100\t0\tsmc\n' "$u1" "$(ds smc 1)" "$u2" "$(ds smc 2)" > "$RUNH/p5/expected.tsv"; rm -f "$RUNH/p5/none_eligible.txt"
  [ "$1" = done ] && mk_retry "$u1"; [ "$2" = done ] && mk_retry "$u2"
  mkdir -p "$LOGR/p5_attempts"; echo attempt > "$LOGR/p5_attempts/$u1"; echo attempt > "$LOGR/p5_attempts/$u2"
  { echo "$P5_HDR"; p5_scan_row "$u1" "$1"; p5_scan_row "$u2" "$2"; scan_row "$(unit_of smc 3)" SMCBVS 0 completed none; } > "$LOGR/p5/scan_final_smc.tsv"
  { echo "$P5_HDR"; for i in 1 2 3; do scan_row "$(ds smc $i)_c100" SMCBVS_rep1 1 completed none; done; } > "$LOGR/p5/scan_final_smcrep.tsv"; echo ok > "$LOGR/p5/scan_final.ok"
  printf 'wave\tstep\tjobid\tarray\tdependency\nmain\ts2_smc\t7002\t0-95%%32\t-\np5\ts4_p5\t7300\t0-1\t-\np5scan_final\ts5_p5scan\t%s\t-\t-\n' "${3:-7400}" > "$RUNH/JOBIDS.tsv"
  printf '7002|a|COMPLETED|0:0|0|0|2|c|c\n7300|a|COMPLETED|0:0|0|0|2|c|c\n%s|a|COMPLETED|0:0|0|0|2|c|c\n' "${3:-7400}" > "$T_STUB/sacct.txt"
}
build; rm -f "$RUNH/p5/expected.tsv" "$RUNH/p5/none_eligible.txt"; run_mm p5_noexp --piece smc
t_eq "P501 smc closing without RUN_HOME/p5/expected.tsv: exit 6" 6 "$MM_RC"; closed smc; [ $? -ne 0 ]; t_cond "P501 not CLOSED" $?
build; rm -f "$RUNH/p5/expected.tsv" "$RUNH/p5/none_eligible.txt"; run_mm p5_noexp_rep --piece smcrep
t_eq "P502 smcrep closing without expected.tsv: exit 6" 6 "$MM_RC"
build; run_mm p5_zero --piece smc
t_eq "P503 zero-eligible path (header-only expected.tsv + scan_initial.ok): smc closes, exit 0" 0 "$MM_RC"
build_p5 done done 7400; run_mm p5_ok --piece smc
t_eq "P504 (control) 2 expected P5 units, both retries valid and done in the FINAL scan (job 7400 > wave job 7300): smc closes, exit 0" 0 "$MM_RC"
build_p5 done done 7400; rm -f "$LOGR/p5/scan_final.ok" "$LOGR/p5/scan_final_smc.tsv" "$LOGR/p5/scan_final_smcrep.tsv"; run_mm p5_nofinal --piece smc
t_eq "P505 expected units exist but there is no FINAL scan (only the initial one): exit 6" 6 "$MM_RC"
build_p5 done done 7200; run_mm p5_oldscan --piece smc
t_eq "P506 the final scan job (7200) is OLDER than the P5 wave job (7300): exit 6" 6 "$MM_RC"
build_p5 done done 7400; rm -f "$LOGR/p5/scan_final.ok"; run_mm p5_noscanok --piece smc
t_eq "P507 the final scan did not finish (no scan_final.ok): exit 6" 6 "$MM_RC"
build_p5 done none 7400; run_mm p5_unfinished --piece smc
t_eq "P508 one expected P5 unit has no valid retry (scan retry_state none, reconcile not done): exit 6" 6 "$MM_RC"; closed smc; [ $? -ne 0 ]; t_cond "P508 not CLOSED" $?
run_mm p5_unfinished_ok --piece smc --allow-incomplete
t_eq "P509 the same with --allow-incomplete (HQ-acknowledged): closes, exit 0" 0 "$MM_RC"
closed smc; t_cond "P509 CLOSED written" $?
grep -q "$(unit_of smc 2)" "$RUNH/manifests/smc.CLOSED" 2>/dev/null; t_cond "P510 the unfinished P5 unit is listed in smc.CLOSED" $?
build_p5 done done 7400; rm -f "$(case_dir smc "$(unit_of smc 2)")/P5_retry/SMCBVS_p5retry.done"; run_mm p5_scan_done_recon_not --piece smc
t_eq "P511 the scan table says done but the retry's .done is gone (reconcile disagrees): exit 6" 6 "$MM_RC"

# =============================================== R2 I2: exceptions are per piece and survive closing =====================================================
# reconcile writes <out>/exceptions.tsv (piece kind item detail) and a STATUS line in INVENTORY.md: CLEAN (exit 0) | COMPLETE WITH n HQ-ACKNOWLEDGED EXCEPTIONS (exit 4) | INCOMPLETE OR UNRESOLVED (exit 1);
# exit 2 stays for input errors / tampering. make_manifests.sh --piece P refuses (exit 6) while exceptions.tsv has a row for P, unless --allow-incomplete; it saves the rows to
# RUN_HOME/manifests/<piece>.exceptions.tsv (header only when empty) and records exceptions_sha256= and acknowledged_exceptions=<n> in <piece>.CLOSED.
run_rec() {   # run_rec LABEL : REC_RC, REC_OUT
  local o="$W/rec_$1"; rm -rf "$o"
  ( cd "$W" && "$T_BIN/python3" "$BUN/reconcile_prodl.py" "$STAMP" --home-root "$FH" --scr-root "$FS" --lists "$BUN/lists/units.tsv" --out "$o" ) > "$W/rec_$1.log" 2>&1
  REC_RC=$?; REC_OUT="$o"
}
status_line() { grep -i 'STATUS' "$REC_OUT/INVENTORY.md" 2>/dev/null | head -n 1; }
xrows() { awk 'NR>1' "$1" 2>/dev/null | wc -l | tr -d ' '; }
junk() { local d; d="$(res_folder "$1")/p0020/ZZ_unexpected_unit"; mkdir -p "$d"; echo "unexpected scientific output" > "$d/EXACT.rds"; }

build; run_rec x_clean
t_eq "X01 all four pieces done, zero-eligible P5 with a final scan: reconcile exit 0" 0 "$REC_RC"
status_line | grep -q 'CLEAN'; t_cond "X02 INVENTORY.md STATUS line says CLEAN" $?
head -n 1 "$REC_OUT/exceptions.tsv" | grep -q $'^piece\tkind\titem\tdetail'; t_cond "X03 exceptions.tsv has the header piece kind item detail" $?
t_eq "X04 ... and no rows" 0 "$(xrows "$REC_OUT/exceptions.tsv")"

build; junk enum20; run_rec x_unexp
t_eq "X05 an unexpected output folder with every expected unit done: reconcile exit 1" 1 "$REC_RC"
awk -F'\t' 'NR>1 && $1=="enum20" && $2=="unexpected_output" && index($3,"ZZ_unexpected_unit")>0' "$REC_OUT/exceptions.tsv" | grep -q .; t_cond "X06 ... exceptions.tsv: piece enum20, kind unexpected_output, item ZZ_unexpected_unit" $?
status_line | grep -q 'INCOMPLETE OR UNRESOLVED'; t_cond "X07 ... STATUS INCOMPLETE OR UNRESOLVED" $?
run_mm x_close_unexp --piece enum20
t_eq "X08 closing enum20 with the unexpected output: exit 6 (ordinary closure refused)" 6 "$MM_RC"; closed enum20; [ $? -ne 0 ]; t_cond "X09 ... not CLOSED" $?
run_mm x_close_ack --piece enum20 --allow-incomplete
t_eq "X10 with --allow-incomplete (HQ-acknowledged): closes, exit 0" 0 "$MM_RC"
EXF="$RUNH/manifests/enum20.exceptions.tsv"
awk -F'\t' 'NR>1 && $2=="unexpected_output"' "$EXF" | grep -q .; t_cond "X11 manifests/enum20.exceptions.tsv saves the exception row (kind unexpected_output)" $?
want=$(sha256sum "$EXF" | cut -c1-64)
grep -q "exceptions_sha256=$want" "$RUNH/manifests/enum20.CLOSED" && grep -q 'acknowledged_exceptions=1' "$RUNH/manifests/enum20.CLOSED"; t_cond "X12 enum20.CLOSED records exceptions_sha256=<sha of the saved file> and acknowledged_exceptions=1" $?
mkdir -p "$W/downloaded"; mv "$(res_folder enum20)" "$W/downloaded/"; run_rec x_after_pull
t_eq "X13 close with --allow-incomplete -> move the folder away -> reconcile: exit 4 (never 0)" 4 "$REC_RC"
awk -F'\t' 'NR>1 && $1=="enum20" && $2=="unexpected_output" && index($4,"acknowledged=yes")>0' "$REC_OUT/exceptions.tsv" | grep -q .; t_cond "X14 ... the acknowledged exception is still listed (kind kept, acknowledged=yes in the detail)" $?
status_line | grep -q 'COMPLETE WITH 1 HQ-ACKNOWLEDGED EXCEPTIONS'; t_cond "X15 ... STATUS COMPLETE WITH 1 HQ-ACKNOWLEDGED EXCEPTIONS" $?
printf 'enum20\tunexpected_output\tforged_item\tforged\n' >> "$EXF"; run_rec x_tamper
t_eq "X16 a tampered enum20.exceptions.tsv (sha256 differs from CLOSED): reconcile exit 2" 2 "$REC_RC"
printf 'piece\tkind\titem\tdetail\n' > "$EXF"; run_rec x_tamper2
t_eq "X17 an emptied exceptions file is a tampering too: exit 2" 2 "$REC_RC"

build; run_mm x_clean_close --piece enum20
EXF="$RUNH/manifests/enum20.exceptions.tsv"
t_eq "X20 a clean close saves an exceptions file with the header only" "1" "$(t_count_lines "$EXF")"
grep -q "exceptions_sha256=$(sha256sum "$EXF" | cut -c1-64)" "$RUNH/manifests/enum20.CLOSED" && grep -q 'acknowledged_exceptions=0' "$RUNH/manifests/enum20.CLOSED"; t_cond "X21 ... CLOSED records its sha256 and acknowledged_exceptions=0" $?
mv "$(res_folder enum20)" "$W/downloaded/enum20_clean"; run_rec x_clean_after_pull
t_eq "X22 a CLEAN closed piece moved away: reconcile still exit 0" 0 "$REC_RC"; status_line | grep -q 'CLEAN'; t_cond "X23 ... STATUS CLEAN" $?

build; rm -f "$(case_dir smc "$(unit_of smc 2)")/SMCBVS.done"; run_mm x_unrelated --piece enum20
t_eq "X30 an unrelated UNFINISHED piece (smc) does not block closing the clean piece enum20: exit 0" 0 "$MM_RC"
build; rm -f "$(case_dir smc "$(unit_of smc 2)")/SMCBVS.done"; junk smcrep; run_mm x_unrelated2 --piece enum20
t_eq "X31 ... nor does an exception of ANOTHER piece (smcrep): exit 0" 0 "$MM_RC"
build; junk smcrep; run_mm x_other_junk --piece smcrep
t_eq "X32 the piece that owns the exception is refused: exit 6" 6 "$MM_RC"

# =============================================== R2 I3: native-status counts include CLOSED pieces ======================================================
# State: smc units 1 and 2 are committed scientific failures (native resource_limit, status failed) with valid P5 retries (a NONEMPTY P5 inventory), smc unit 3 and the three smcrep units
# are native 'completed' (two native categories). INVENTORY.md's "## SMC native status counts (units)" table must be identical (one count per UNIT) before and after closing / pulling
# one piece, then all pieces; exit 0 each time.
counts() { awk '/^## SMC native status counts/{f=1;next} /^## /{f=0} f && /^\|/ && !/^\|-/ && !/Piece/ {gsub(/\|/," "); print $1 "," $2 "," $3}' "$REC_OUT/INVENTORY.md" 2>/dev/null | LC_ALL=C sort | tr '\n' ';'; }
build_p5 done done 7400; run_rec n0
t_eq "N301 (setup) nonempty P5 inventory, both retries done, final scan complete: reconcile exit 0" 0 "$REC_RC"
C0=$(counts)
t_eq "N302 native counts, one per unit: smc complete 1, smc resource_limit 2, smcrep complete 3 (the fixture CSVs say v3_status=complete)" "smc,complete,1;smc,resource_limit,2;smcrep,complete,3;" "$C0"
run_mm n_smc --piece smc; t_eq "N303 close smc: exit 0" 0 "$MM_RC"
mkdir -p "$W/downloaded"; mv "$(res_folder smc)" "$W/downloaded/n_smc"; run_rec n1
t_eq "N304 smc closed and pulled: reconcile exit 0" 0 "$REC_RC"
t_eq "N305 ... the native counts are unchanged (rebuilt from the hash-verified saved rows, not lost)" "$C0" "$(counts)"
run_mm n_smcrep --piece smcrep; t_eq "N306 close smcrep: exit 0" 0 "$MM_RC"
mv "$(res_folder smcrep)" "$W/downloaded/n_smcrep"; run_rec n2
t_eq "N307 smc and smcrep closed and pulled: reconcile exit 0, counts unchanged" "0 $C0" "$REC_RC $(counts)"
run_mm n_e20 --piece enum20; run_mm n_e30 --piece enum30; mv "$(res_folder enum20)" "$W/downloaded/n_e20"; mv "$(res_folder enum30)" "$W/downloaded/n_e30"; run_rec n3
t_eq "N308 all four pieces closed and pulled: reconcile exit 0, counts unchanged" "0 $C0" "$REC_RC $(counts)"
t_eq "N309 ... and the saved smc inventory holds exactly the 3 unit rows (coverage unchanged)" 3 "$(awk -F'\t' 'NR>1' "$RUNH/manifests/smc.inventory.tsv" | wc -l | tr -d ' ')"

# =============================================== D57 follow-up: the logs folder is NOT scanned for stale artefacts ==========================================
# clear_stale.sh --yes archives a *.lock dir and temp files into LOG_RUN/cleanup/<utc>/ (inside the logs folder); a hidden ledger temp LOG_RUN/ledger/<piece>/<unit>/.<tag>.<pid>.tmp may
# remain. `--piece logs` (final accounting present, all four result pieces CLOSED) must still SUCCEED and its MANIFEST.sha256 must list those archived files; result pieces still
# refuse with a stale artefact in their own folder.
cs_yes() { ( export NC_HOME_ROOT="$FH" NC_SCR_ROOT="$FS" PATH="$T_BIN:$PATH" STUB_DIR="$T_STUB" SQUEUE="$T_BIN/squeue" SACCT="$T_BIN/sacct" STAMP; cd "$W" && bash "$BUN/clear_stale.sh" "$STAMP" --yes ) > "$W/cs_d57.log" 2>&1; }
build; d=$(case_dir enum20 "$(unit_of enum20 2)"); mkdir -p "$d/.lock"; echo "pid 1" > "$d/.lock/owner"; echo partial > "$d/EXACT.rds.tmp4242"
run_mm d57_stale --piece enum20
t_eq "D5701 a result piece still refuses with a stale artefact in its own folder (.lock dir + EXACT.rds.tmp4242): exit 2" 2 "$MM_RC"
cs_yes; CL=$(ls -d "$LOGR"/cleanup/*/ 2>/dev/null | head -n 1)
[ -n "$CL" ] && [ ! -e "$d/.lock" ] && [ ! -e "$d/EXACT.rds.tmp4242" ]; t_cond "D5702 clear_stale.sh --yes archived both into LOG_RUN/cleanup/<utc>/" $?
find "$CL" -name 'EXACT.rds.tmp4242' | grep -q .; t_cond "D5703 ... the temp file is in the archive (inside the logs folder)" $?
ul="$(unit_of smc 1)"; mkdir -p "$LOGR/ledger/smc/$ul"; echo partial > "$LOGR/ledger/smc/$ul/.7002_0.1234.tmp"
for p in enum20 enum30 smc smcrep; do run_mm "d57_$p" --piece $p; t_eq "D5704 result piece $p closes after the archive: exit 0" 0 "$MM_RC"; done
add_accounting; run_mm d57_logs --piece logs
t_eq "D5705 --piece logs with archived stale files in cleanup/ and a hidden ledger temp: exit 0 (the logs folder is not scanned for stale artefacts)" 0 "$MM_RC"
manifest_lists_files "$LOGR"; t_cond "D5706 logs MANIFEST.sha256 verifies and lists exactly the files present" $? "$MF_WHY"
grep -q 'cleanup/.*EXACT.rds.tmp4242' "$LOGR/MANIFEST.sha256" && grep -q 'cleanup/.*\.lock/owner' "$LOGR/MANIFEST.sha256"; t_cond "D5707 ... and lists the archived files (temp file and lock owner) under cleanup/" $?
grep -q '\.7002_0\.1234\.tmp' "$LOGR/MANIFEST.sha256"; t_cond "D5708 ... and the hidden ledger temp file" $?
[ -e "$RUNH/manifests/logs.CLOSED" ]; t_cond "D5709 logs.CLOSED written" $?

t_summary
