#!/bin/bash
# test_manifests.sh -- make_manifests.sh STAMP --piece bench|logs [--allow-incomplete] and reconcile_bench.py (PROD_L_BENCH DESIGN.md sections 5-6).
#   bash test_manifests.sh WORKDIR
# Small staged lists/units.tsv (6 cases). A case is done iff all 8 methods are valid units. Exits of make_manifests.sh: 3 run job active, 4 scheduler error, 2 stale artefact /
# already closed / tampered manifest, 6 not 100 % done or an unresolved exception (unless --allow-incomplete). reconcile_bench.py: 0 CLEAN, 4 COMPLETE WITH n HQ-ACKNOWLEDGED
# EXCEPTIONS, 1 INCOMPLETE OR UNRESOLVED, 2 input error / tampering; <out>/exceptions.tsv (piece kind item detail); rule-status table per method in INVENTORY.md.
source "$(dirname "$0")/lib.sh"
t_init "${1:-}" test_manifests
STAMP=20261030T1800Z
t_mkbundle "$W/fx" "$STAMP"
SRCB=${PRODL_B_SRC:-$B}
METHODS="F1 F2 F3 F4 F5 A1 A2 A3"
[ -f "$SRCB/make_manifests.sh" ] && [ -f "$SRCB/reconcile_bench.py" ] && [ -f "$SRCB/bench_verify.py" ]; t_cond "MM00 make_manifests.sh, reconcile_bench.py and bench_verify.py exist in the bundle" $?

# ---- fixtures -------------------------------------------------------------------------------------------------------------------
NC=6
CU() { local ds; printf -v ds 'p0020_S1_r%03d' "$1"; echo "${ds}_c100"; }
RES="$FS/results/${STAMP}_lowp_benchres"
cdir() { echo "$RES/p0020/$1"; }
mk_small_units() {
  local f="$BUN/lists/units.tsv" i ds; printf 'piece\ttask\tunit\tdataset\tscale\trepeat\n' > "$f"
  for i in $(seq 1 $NC); do printf -v ds 'p0020_S1_r%03d' "$i"; printf 'bench\t0\t%s_c100\t%s\tc100\t0\n' "$ds" "$ds" >> "$f"; done
}
mk_method() {   # mk_method CASE M [STATUS_OF_RULE_1]
  local c=$1 m=$2 st=${3:-ok} d; d=$(cdir "$c"); mkdir -p "$d"; echo "rds $c $m" > "$d/$m.rds"
  printf 'rule_id,role,status,method_id,case_id\nr1,primary,%s,%s,%s\nr2,sensitivity,ok,%s,%s\n' "$st" "$m" "$c" "$m" "$c" > "$d/$m.csv"
  ( cd "$d" && sha256sum "$m.rds" "$m.csv" > "$m.sha256" ); printf 'status %s,ok\nfinished_utc 2026-10-30T13:00:00Z\n' "$st" > "$d/$m.done"
}
mk_case() { local m; for m in $METHODS; do mk_method "$1" "$m" "${2:-ok}"; done; }
build() {   # build : all cases done, JOBIDS + terminal sacct, empty squeue, no final accounting yet
  chmod -R u+rwx "$FS/results" "$FS/logs" 2>/dev/null; rm -rf "$FS/results" "$FS/logs" "$RUNH/manifests" "$RUNH/resubmit" "$RUNH/JOBIDS.tsv"; mkdir -p "$RES" "$LOGR/ledger"; t_stub_reset
  mk_small_units; local i; for i in $(seq 1 $NC); do mk_case "$(CU $i)"; done
  echo "slurm out" > "$LOGR/slurm-x.out"
  printf 'wave\tstep\tjobid\tarray\tdependency\nmain\ts0_verify\t7001\t-\t-\nmain\ts1_bench\t7002\t0-95%%32\tafterok:7001\nmain\ts9_collect\t7003\t-\tafterany:7001:7002\n' > "$RUNH/JOBIDS.tsv"
  printf '7001|lowpB_s0_verify|COMPLETED|0:0|00:01:00|60|2|commons|commons\n7002|lowpB_s1_bench|COMPLETED|0:0|01:00:00|3600|2|commons|commons\n7003|lowpB_s9_collect|COMPLETED|0:0|00:00:30|30|2|commons|commons\n' > "$T_STUB/sacct.txt"
  : > "$T_STUB/squeue.txt"
}
add_accounting() { mkdir -p "$LOGR/accounting"; printf 'JobID\tState\n7001\tCOMPLETED\n' > "$LOGR/accounting/sacct_final.tsv"; printf 'step\tcore_h\ntotal\t1.0\n' > "$LOGR/accounting/core_hours.tsv"; }
run_mm() {
  local label=$1; shift; MM_LOG="$W/mm_$label.log"
  ( export NC_HOME_ROOT="$FH" NC_SCR_ROOT="$FS" PATH="$T_BIN:$PATH" STUB_DIR="$T_STUB" SQUEUE="$T_BIN/squeue" SACCT="$T_BIN/sacct" PYTHON="$T_BIN/python3" GUARD="$T_BIN/guard_simple" STAMP
    cd "$W" && bash "$BUN/make_manifests.sh" "$STAMP" "$@" ) > "$MM_LOG" 2>&1
  MM_RC=$?
}
run_rec() {   # run_rec LABEL : REC_RC REC_OUT
  local o="$W/rec_$1"; rm -rf "$o"
  ( cd "$W" && "$T_BIN/python3" "$BUN/reconcile_bench.py" "$STAMP" --home-root "$FH" --scr-root "$FS" --lists "$BUN/lists/units.tsv" --out "$o" ) > "$W/rec_$1.log" 2>&1
  REC_RC=$?; REC_OUT="$o"
}
status_line() { grep -i 'STATUS' "$REC_OUT/INVENTORY.md" 2>/dev/null | head -n 1; }
xrows() { awk 'NR>1' "$1" 2>/dev/null | wc -l | tr -d ' '; }
has_manifest() { [ -e "$RES/MANIFEST.sha256" ]; }
closed() { [ -e "$RUNH/manifests/$1.CLOSED" ]; }
manifest_lists_files() {
  local d=$1 a b; MF_WHY=""
  MF_WHY=$( cd "$d" && sha256sum --quiet -c MANIFEST.sha256 2>&1 ) || { MF_WHY="sha256sum -c fails: $(echo $MF_WHY | cut -c1-200)"; return 1; }
  MF_WHY=""
  a=$(sed -E 's/^[0-9a-fA-F]{64} [ *]//; s/^\.\///; s/\r$//' "$d/MANIFEST.sha256" | LC_ALL=C sort)
  b=$(cd "$d" && find . -type f ! -name MANIFEST.sha256 | sed 's/^\.\///' | LC_ALL=C sort)
  [ "$a" = "$b" ] && [ -n "$a" ] || { MF_WHY="listed/present differ"; return 1; }
}
junk() { local d; d="$RES/p0020/ZZ_unexpected_case"; mkdir -p "$d"; echo "unexpected scientific output" > "$d/notes_unexpected.txt"; }     # (not an incomplete method unit: that is a STALE artefact, exit 2)
rule_lines() { grep -E '^\|' "$REC_OUT/INVENTORY.md" 2>/dev/null | grep -E '\b(F[1-5]|A[1-3])\b' | LC_ALL=C sort | md5sum; }

# =============================================== gates ===========================================================================
build; echo '7002_5|lowpB_s1_bench|RUNNING|2' > "$T_STUB/squeue.txt"; run_mm gate_active --piece bench
t_eq "MM01 a run job is RUNNING in squeue: exit 3" 3 "$MM_RC"; has_manifest; [ $? -ne 0 ]; t_cond "MM01 no manifest written" $?
build; touch "$T_STUB/squeue_fail"; run_mm gate_squeue --piece bench; t_eq "MM02 squeue fails: exit 4" 4 "$MM_RC"
build; touch "$T_STUB/sacct_fail"; run_mm gate_sacct --piece bench; t_eq "MM03 sacct fails: exit 4" 4 "$MM_RC"
build; printf '7001|a|COMPLETED|0:0|0|0|2|c|c\n7002|a|RUNNING|0:0|0|0|2|c|c\n7003|a|COMPLETED|0:0|0|0|2|c|c\n' > "$T_STUB/sacct.txt"; run_mm gate_sacct_run --piece bench
t_eq "MM04 squeue empty but sacct shows a RUNNING job: exit 3" 3 "$MM_RC"

# =============================================== stale artefacts (all three kinds) ===============================================
for kind in lock hidden incomplete; do
  build; d=$(cdir "$(CU 2)")
  case $kind in lock) mkdir -p "$d/F1.lock"; echo "pid 1" > "$d/F1.lock/owner.txt";; hidden) echo partial > "$d/.F1.rds3a9c";; incomplete) rm -f "$d/F2.done";; esac
  run_mm "stale_$kind" --piece bench
  t_eq "MM05 stale kind '$kind' in the piece folder: exit 2" 2 "$MM_RC"; has_manifest; [ $? -ne 0 ]; t_cond "MM05 no manifest written ($kind)" $?
done
build; d=$(cdir "$(CU 2)"); echo partial > "$d/.F1.rds3a9c"
( export NC_HOME_ROOT="$FH" NC_SCR_ROOT="$FS" PATH="$T_BIN:$PATH" STUB_DIR="$T_STUB" SQUEUE="$T_BIN/squeue" SACCT="$T_BIN/sacct" STAMP; cd "$W" && bash "$BUN/clear_stale.sh" "$STAMP" --yes ) > "$W/cs.log" 2>&1
run_mm cleared --piece bench; t_eq "MM06 after clear_stale.sh --yes the piece closes: exit 0" 0 "$MM_RC"

# =============================================== completeness (a case is done only with ALL 8 methods valid) =========================
build; rm -f "$(cdir "$(CU 3)")/A3.done" "$(cdir "$(CU 3)")/A3.rds" "$(cdir "$(CU 3)")/A3.csv" "$(cdir "$(CU 3)")/A3.sha256"; run_mm one_method_missing --piece bench
t_eq "MM10 a case with 7 of 8 methods: exit 6" 6 "$MM_RC"; has_manifest; [ $? -ne 0 ]; t_cond "MM11 no manifest" $?; closed bench; [ $? -ne 0 ]; t_cond "MM11 not CLOSED" $?
run_mm incomplete_ok --piece bench --allow-incomplete
t_eq "MM12 with --allow-incomplete (HQ-acknowledged): closes, exit 0" 0 "$MM_RC"; has_manifest && closed bench; t_cond "MM13 manifest and CLOSED written" $?
build; rm -rf "$(cdir "$(CU 4)")"; run_mm not_run --piece bench
t_eq "MM14 a not_run case (no result folder): exit 6" 6 "$MM_RC"
build; d=$(cdir "$(CU 2)"); echo "tampered" >> "$d/F5.rds"; run_mm bad_sidecar --piece bench
t_eq "MM15 a method whose sidecar no longer verifies: exit 6" 6 "$MM_RC"
build; d=$(cdir "$(CU 2)"); : > "$d/F5.rds"; ( cd "$d" && sha256sum F5.rds F5.csv > F5.sha256 ); run_mm empty_rds --piece bench
t_eq "MM16 an EMPTY method rds with a matching sidecar: exit 6" 6 "$MM_RC"
build; d=$(cdir "$(CU 2)"); printf 'rule_id,role,status\nr1,primary,ok\n' > "$d/F5.csv"; ( cd "$d" && sha256sum F5.rds F5.csv > F5.sha256 ); run_mm bad_csv --piece bench
t_eq "MM17 a CSV without the columns method_id and case_id: exit 6" 6 "$MM_RC"
build; d=$(cdir "$(CU 2)"); printf 'status ok\n' > /dev/null; printf 'garbage marker\n' > "$d/F5.done"; run_mm bad_done --piece bench
t_eq "MM18 a malformed .done (first line does not start with 'status '): exit 6" 6 "$MM_RC"
build; mk_method "$(CU 2)" F4 failed; mk_method "$(CU 5)" A2 failed; run_mm failed_rules --piece bench
t_eq "MM19 committed FAILED rules are valid records: the piece closes, exit 0" 0 "$MM_RC"

# =============================================== a complete piece =================================================================
build; run_mm close_bench --piece bench
t_eq "MM20 complete piece: exit 0" 0 "$MM_RC"
manifest_lists_files "$RES"; t_cond "MM21 MANIFEST.sha256 verifies with sha256sum -c and lists exactly the files present" $? "$MF_WHY"
[ -e "$RUNH/manifests/bench.CLOSED" ]; t_cond "MM22 manifests/bench.CLOSED written" $?
[ -s "$RUNH/manifests/bench.inventory.tsv" ] && [ "$(t_count_lines "$RUNH/manifests/bench.inventory.tsv")" -ge $((NC + 1)) ]; t_cond "MM23 manifests/bench.inventory.tsv holds the $NC cases (+ header)" $?
S="$RUNH/manifests/summary.tsv"; grep -q "${STAMP}_lowp_benchres" "$S" 2>/dev/null; t_cond "MM24 summary.tsv has a row for the result folder" $?
grep -q "$(sha256sum < "$RES/MANIFEST.sha256" | cut -c1-64)" "$S" 2>/dev/null; t_cond "MM25 the row carries the manifest sha256" $?
ls "$LOGR/reconcile" 2>/dev/null | grep -q '_bench\.out$'; t_cond "MM26 the reconcile output is kept in LOG_RUN/reconcile/<utc>_bench.out (scratch)" $?
t_eq "MM27 RUN_HOME/manifests holds only CLOSED, inventory, exceptions snapshot and summary" "bench.CLOSED bench.exceptions.tsv bench.inventory.tsv summary.tsv " "$(ls -A "$RUNH/manifests" | tr '\n' ' ')"
EXF="$RUNH/manifests/bench.exceptions.tsv"
t_eq "MM28 a clean close saves a header-only exceptions file" 1 "$(t_count_lines "$EXF")"
want=$(sha256sum "$RUNH/manifests/bench.inventory.tsv" | cut -c1-64); eh=$(sha256sum "$EXF" | cut -c1-64)
grep -q "inventory_sha256=$want" "$RUNH/manifests/bench.CLOSED" && grep -q "exceptions_sha256=$eh" "$RUNH/manifests/bench.CLOSED" && grep -q 'acknowledged_exceptions=0' "$RUNH/manifests/bench.CLOSED"; t_cond "MM29 CLOSED records inventory_sha256, exceptions_sha256 and acknowledged_exceptions=0" $?
run_mm close_again --piece bench; t_eq "MM30 closing a CLOSED piece again: exit 2" 2 "$MM_RC"
build; ( cd "$RES" && find . -type f | LC_ALL=C sort | xargs sha256sum > "$W/m.new" ); mv "$W/m.new" "$RES/MANIFEST.sha256"
before=$(md5sum < "$RES/MANIFEST.sha256"); run_mm preexisting --piece bench
t_eq "MM31 an existing VALID manifest is revalidated and the piece closes: exit 0" 0 "$MM_RC"; t_eq "MM32 ... the manifest is not replaced" "$before" "$(md5sum < "$RES/MANIFEST.sha256")"
build; ( cd "$RES" && find . -type f | LC_ALL=C sort | xargs sha256sum > "$W/m.new" ); mv "$W/m.new" "$RES/MANIFEST.sha256"
echo "tampered after the manifest" >> "$(cdir "$(CU 1)")/F1.done"; before=$(md5sum < "$RES/MANIFEST.sha256"); run_mm tampered --piece bench
t_eq "MM33 an existing manifest that no longer verifies: exit 2" 2 "$MM_RC"; t_eq "MM34 ... left as it was" "$before" "$(md5sum < "$RES/MANIFEST.sha256")"; closed bench; [ $? -ne 0 ]; t_cond "MM35 ... not CLOSED" $?

# =============================================== logs ==============================================================================
build; run_mm logs_noacct --piece logs; [ "$MM_RC" != 0 ]; t_cond "MM40 --piece logs before the final accounting files exist: refused (exit $MM_RC)" $?
add_accounting; run_mm logs_nopiece --piece logs; [ "$MM_RC" != 0 ]; t_cond "MM41 --piece logs with accounting but bench not CLOSED: refused (exit $MM_RC)" $?
run_mm close2 --piece bench; run_mm logs_ok --piece logs
t_eq "MM42 --piece logs with accounting and bench CLOSED: exit 0" 0 "$MM_RC"
manifest_lists_files "$LOGR"; t_cond "MM43 logs/<RID>/MANIFEST.sha256 verifies and lists exactly the files present" $? "$MF_WHY"
[ -e "$RUNH/manifests/logs.CLOSED" ]; t_cond "MM44 logs.CLOSED written" $?

# =============================================== reconcile_bench.py: status, exceptions, rule table =================================
build; run_rec r_clean
t_eq "RC01 everything done, no exception: exit 0" 0 "$REC_RC"; status_line | grep -q 'CLEAN'; t_cond "RC02 STATUS CLEAN" $?
head -n 1 "$REC_OUT/exceptions.tsv" | grep -q $'^piece\tkind\titem\tdetail'; t_cond "RC03 exceptions.tsv header piece kind item detail" $?
t_eq "RC04 ... no rows" 0 "$(xrows "$REC_OUT/exceptions.tsv")"
[ -s "$REC_OUT/inventory/bench.tsv" ]; t_cond "RC05 inventory/bench.tsv written" $?
t_eq "RC06 every expected case exactly once ($NC)" "$NC" "$(awk -F'\t' 'NR>1 && NF>=3' "$REC_OUT/inventory/bench.tsv" | wc -l | tr -d ' ')"
build; mk_method "$(CU 2)" F4 failed; run_rec r_failed
t_eq "RC07 a committed failed rule: the case stays done, exit 0" 0 "$REC_RC"
awk -F'|' '/^\| *Method *\|/{f=1;next} f && $2 ~ /F4/ {gsub(/ /,"",$5); exit !($5+0 >= 1)}' "$REC_OUT/INVENTORY.md"; t_cond "RC08 the failed rule is counted in the 'Rule statuses per method' table (| Method | ok | warning | failed |: F4 failed >= 1)" $?
build; junk; run_rec r_unexp
t_eq "RC10 an unexpected output case folder with every case done: exit 1" 1 "$REC_RC"
awk -F'\t' 'NR>1 && $1=="bench" && $2=="unexpected_output" && index($3,"ZZ_unexpected_case")>0' "$REC_OUT/exceptions.tsv" | grep -q .; t_cond "RC11 exceptions.tsv: bench / unexpected_output / ZZ_unexpected_case" $?
status_line | grep -q 'INCOMPLETE OR UNRESOLVED'; t_cond "RC12 STATUS INCOMPLETE OR UNRESOLVED" $?
build; d=$(cdir "$(CU 3)"); printf 'rule_id,role,status\nr1,primary,ok\n' > "$d/F2.csv"; ( cd "$d" && sha256sum F2.rds F2.csv > F2.sha256 ); run_rec r_malformed
awk -F'\t' 'NR>1 && $1=="bench" && $2=="malformed_record"' "$REC_OUT/exceptions.tsv" | grep -q .; t_cond "RC13 a malformed method record yields an exception of kind malformed_record" $?
[ "$REC_RC" = 1 ]; t_cond "RC14 ... and exit 1 ($REC_RC)" $?
build; rm -f "$(cdir "$(CU 3)")/A1.done"; run_rec r_partial
t_eq "RC15 a case with an incomplete method unit (A1.rds/.csv/.sha256 without .done): exit 1" 1 "$REC_RC"
awk -F'\t' -v u="$(CU 3)" 'NR==1{for(i=1;i<=NF;i++) if($i=="unit") ui=i; for(i=1;i<=NF;i++) if($i=="outcome") oi=i} NR>1 && $ui==u {print $oi}' "$REC_OUT/inventory/bench.tsv" | grep -qx done; [ $? -ne 0 ]; t_cond "RC16 ... that case is not 'done'" $?

# ledger classes: deferred / unit_failed / killed_timeout / killed_external / not_run, by case, over both pieces
build; for i in 2 3 4 5 6; do rm -rf "$(cdir "$(CU $i)")"; done
mkled() { local piece=$1 u=$2 tag=$3 kind=$4 d="$LOGR/ledger/$1/$2"; mkdir -p "$d"
  case $kind in
    start) printf 'unit=%s piece=%s task=0 job_tag=%s host=h start_utc=2026-10-30T13:00:00Z deadline_epoch=1 need_s=1 end_source=x end_epoch=1\n' "$u" "$piece" "$tag" > "$d/$tag.start";;
    end_failed) printf 'unit=%s rc=1 outcome=unit_failed wall_s=1 cli_status=NA cli_skipped=NA end_utc=2026-10-30T13:00:09Z\n' "$u" > "$d/$tag.end";;
    end_timeout) printf 'unit=%s rc=124 outcome=killed_timeout wall_s=600 cli_status=NA cli_skipped=NA end_utc=2026-10-30T13:10:00Z\n' "$u" > "$d/$tag.end";;
    deferred) printf 'unit=%s reason=deadline now_epoch=1 deadline_epoch=1 need_s=1 end_source=x end_epoch=1\n' "$u" > "$d/$tag.deferred";;
  esac; }
mkled bench "$(CU 2)" 7002_0 deferred
mkled bench "$(CU 3)" 7002_0 start; mkled bench "$(CU 3)" 7002_0 end_failed
mkled bench "$(CU 4)" 7002_0 start; mkled bench "$(CU 4)" 7002_0 end_timeout
mkled bench "$(CU 5)" 7002_0 start
mkled bench "$(CU 5)" 7002_0 deferred; rm -f "$LOGR/ledger/bench/$(CU 5)/7002_0.deferred"
# case 6: nothing; the retry piece's ledger counts too: case 4 timed out in bench then started in benchretry and was killed externally -> killed_external (latest history)
mkled benchretry "$(CU 4)" 7010_0 start
run_rec r_classes
out_of() { awk -F'\t' -v u="$1" 'NR==1{for(i=1;i<=NF;i++){if($i=="unit")ui=i; if($i=="outcome")oi=i}} NR>1 && $ui==u {print $oi}' "$REC_OUT/inventory/bench.tsv" 2>/dev/null; }
t_eq "RC20 case 1 (all methods valid): done" done "$(out_of "$(CU 1)")"
t_eq "RC21 case 2 (deferred only): deferred" deferred "$(out_of "$(CU 2)")"
t_eq "RC22 case 3 (start, unit_failed end): unit_failed" unit_failed "$(out_of "$(CU 3)")"
t_eq "RC23 case 5 (start without end): killed_external" killed_external "$(out_of "$(CU 5)")"
t_eq "RC24 case 6 (nothing): not_run" not_run "$(out_of "$(CU 6)")"
t_eq "RC25 case 4 (bench killed_timeout, then a benchretry start without end): killed_external (ledger of both pieces, latest attempt)" killed_external "$(out_of "$(CU 4)")"
[ "$REC_RC" = 1 ]; t_cond "RC26 not everything done: exit 1" $?

# =============================================== exceptions are per piece and survive closing (R2 I2 pattern) ===========================
build; junk; run_mm x_close_unexp --piece bench
t_eq "X01 closing bench with an unexpected output case: exit 6 (ordinary closure refused)" 6 "$MM_RC"; closed bench; [ $? -ne 0 ]; t_cond "X02 not CLOSED" $?
run_mm x_close_ack --piece bench --allow-incomplete
t_eq "X03 with --allow-incomplete (HQ-acknowledged): closes, exit 0" 0 "$MM_RC"
EXF="$RUNH/manifests/bench.exceptions.tsv"
awk -F'\t' 'NR>1 && $2=="unexpected_output"' "$EXF" | grep -q .; t_cond "X04 bench.exceptions.tsv saves the exception row (unexpected_output)" $?
grep -q "exceptions_sha256=$(sha256sum "$EXF" | cut -c1-64)" "$RUNH/manifests/bench.CLOSED" && grep -q 'acknowledged_exceptions=1' "$RUNH/manifests/bench.CLOSED"; t_cond "X05 CLOSED records exceptions_sha256 and acknowledged_exceptions=1" $?
mkdir -p "$W/downloaded"; mv "$RES" "$W/downloaded/"; run_rec x_after_pull
t_eq "X06 close with --allow-incomplete -> move the folder away -> reconcile: exit 4 (never 0)" 4 "$REC_RC"
awk -F'\t' 'NR>1 && $1=="bench" && $2=="unexpected_output" && index($4,"acknowledged=yes")>0' "$REC_OUT/exceptions.tsv" | grep -q .; t_cond "X07 ... the exception is still listed with acknowledged=yes" $?
status_line | grep -q 'COMPLETE WITH 1 HQ-ACKNOWLEDGED EXCEPTIONS'; t_cond "X08 ... STATUS COMPLETE WITH 1 HQ-ACKNOWLEDGED EXCEPTIONS" $?
printf 'bench\tunexpected_output\tforged_item\tforged\n' >> "$EXF"; run_rec x_tamper
t_eq "X09 a tampered bench.exceptions.tsv: reconcile exit 2" 2 "$REC_RC"

# =============================================== CLOSED flow: counts / rule table invariant across close and pull ===========================
build; mk_method "$(CU 2)" F4 failed; mk_method "$(CU 3)" A1 warning; mk_method "$(CU 4)" F4 failed; run_rec n0
t_eq "N01 (setup) committed failed rules and warnings, all cases done: exit 0" 0 "$REC_RC"; R0=$(rule_lines)
awk -F'|' '/^\| *Method *\|/{f=1;next} f && $2 ~ /F4/ {gsub(/ /,"",$5); exit !($5+0 == 2)}' "$REC_OUT/INVENTORY.md"; t_cond "N02 the table counts the 2 failed F4 rules" $?
run_mm n_close --piece bench; t_eq "N03 close bench: exit 0" 0 "$MM_RC"
mkdir -p "$W/downloaded2"; mv "$RES" "$W/downloaded2/"; run_rec n1
t_eq "N04 closed and pulled: reconcile exit 0" 0 "$REC_RC"; t_eq "N05 ... the per-method rule-status table is unchanged (rebuilt from the hash-verified closed inventory)" "$R0" "$(rule_lines)"
t_eq "N06 ... all $NC cases still done" "$NC" "$(awk -F'\t' 'NR>1 && $3=="done"' "$REC_OUT/inventory/bench.tsv" | wc -l | tr -d ' ')"
printf 'bench\tp0020_S1_r099_c100\tdone\tforged\n' >> "$RUNH/manifests/bench.inventory.tsv"; run_rec n2
t_eq "N07 a tampered closed inventory (sha256 differs from CLOSED): reconcile exit 2" 2 "$REC_RC"

# =============================================== D57 follow-up: the logs folder is NOT scanned for stale artefacts ==========================================
# clear_stale.sh --yes archives a *.lock dir and temp files into LOG_RUN/cleanup/<utc>/ (inside the logs folder); a hidden ledger temp LOG_RUN/ledger/<piece>/<unit>/.<tag>.<pid>.tmp may
# remain. `--piece logs` (final accounting present, bench CLOSED) must still SUCCEED and its MANIFEST.sha256 must list those archived files; the result piece still refuses with a
# stale artefact in its own folder.
build; d=$(cdir "$(CU 2)"); mkdir -p "$d/F1.lock"; echo "pid 1" > "$d/F1.lock/owner.txt"; echo partial > "$d/.F1.rds3a9c"
run_mm d57_stale --piece bench
t_eq "D5701 the result piece still refuses with a stale artefact in its own folder (F1.lock dir + .F1.rds3a9c): exit 2" 2 "$MM_RC"
( export NC_HOME_ROOT="$FH" NC_SCR_ROOT="$FS" PATH="$T_BIN:$PATH" STUB_DIR="$T_STUB" SQUEUE="$T_BIN/squeue" SACCT="$T_BIN/sacct" STAMP; cd "$W" && bash "$BUN/clear_stale.sh" "$STAMP" --yes ) > "$W/cs_d57.log" 2>&1
CL=$(ls -d "$LOGR"/cleanup/*/ 2>/dev/null | head -n 1)
[ -n "$CL" ] && [ ! -e "$d/F1.lock" ] && [ ! -e "$d/.F1.rds3a9c" ]; t_cond "D5702 clear_stale.sh --yes archived both into LOG_RUN/cleanup/<utc>/" $?
find "$CL" -name '.F1.rds3a9c' | grep -q .; t_cond "D5703 ... the hidden temp is in the archive (inside the logs folder)" $?
mkdir -p "$LOGR/ledger/bench/$(CU 1)"; echo partial > "$LOGR/ledger/bench/$(CU 1)/.7002_0.1234.tmp"
run_mm d57_bench --piece bench; t_eq "D5704 the result piece closes after the archive: exit 0" 0 "$MM_RC"
add_accounting; run_mm d57_logs --piece logs
t_eq "D5705 --piece logs with archived stale files in cleanup/ and a hidden ledger temp: exit 0 (the logs folder is not scanned for stale artefacts)" 0 "$MM_RC"
manifest_lists_files "$LOGR"; t_cond "D5706 logs MANIFEST.sha256 verifies and lists exactly the files present" $? "$MF_WHY"
grep -q 'cleanup/.*\.F1\.rds3a9c' "$LOGR/MANIFEST.sha256" && grep -q 'cleanup/.*F1\.lock/owner\.txt' "$LOGR/MANIFEST.sha256"; t_cond "D5707 ... and lists the archived files (hidden temp and lock owner) under cleanup/" $?
grep -q '\.7002_0\.1234\.tmp' "$LOGR/MANIFEST.sha256"; t_cond "D5708 ... and the hidden ledger temp file" $?
[ -e "$RUNH/manifests/logs.CLOSED" ]; t_cond "D5709 logs.CLOSED written" $?

t_summary
