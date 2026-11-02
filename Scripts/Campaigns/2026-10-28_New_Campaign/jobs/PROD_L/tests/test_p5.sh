#!/bin/bash
# test_p5.sh -- regression tests for F2 of R1_FIX_PLAN.md: P5 is a reconciled, closable phase.
#   bash test_p5.sh WORKDIR
# A. driver: scan phases (--p5-scan --phase initial|final[N]|rN, launch/p5scan_<phase>, reuse refused)       B. slurm/s5_p5scan.sbatch: scan_<phase>_{smc,smcrep}.tsv + scan_<phase>.ok
# C. make_p5_list.sh STAMP --from-scan initial -> p5/expected.tsv (once, idempotent), scan_initial.receipt, refusals, zero-eligible path
# D. make_p5_list.sh STAMP --wave p5|p5rN -> p5/units_<wave>.tsv (never-started units), p5/exceptions_<wave>.tsv (attempted, no valid retry; never relisted)
# E. reconcile_prodl.py: inventory/p5.tsv (done / attempt_failed / deferred / killed_external / not_run), PENDING without expected.tsv, exit nonzero until all done
# (The make_manifests.sh closing gates for P5 are in test_manifests.sh, cases P501-P511.)
# Scan tables are fabricated with the columns of CAMP/code/core/v2_2_1/tools/p5_scan.R.
source "$(dirname "$0")/lib.sh"
t_init "${1:-}" test_p5
STAMP=20261030T1900Z
SRCB=${PRODL_B_SRC:-$B}
[ -f "$SRCB/make_p5_list.sh" ] && [ -f "$SRCB/slurm/s5_p5scan.sbatch" ]; t_cond "P500 make_p5_list.sh and slurm/s5_p5scan.sbatch exist in the bundle" $?

# ---- the frozen scanner's table -----------------------------------------------------------------------------------------------------------------------
P5_HDR=$'case_id\tbase\trepeat_m\tprimary_v3_status\tprimary_status\tprimary_mem_gb\tprimary_hours\tprimary_stop_where\tprimary_stop_phase\tprimary_stop_checkpoint\tprimary_stop_tier\tprimary_stop_iter\tprimary_stop_stage\tprimary_stop_elapsed_s\tprimary_stop_allocation_s\tretry_state\tretry_problem\tretry_artefacts\tretry_v3_status\tretry_status\tretry_stop_where\tretry_stop_phase\tretry_stop_checkpoint\teligible\tlaunchable'
scan_row() {   # scan_row CASE_ID BASE REPEAT_M PRIMARY_V3 RETRY_STATE : eligible = resource_limit & retry not done ; launchable = resource_limit & state none
  local el=FALSE la=FALSE
  [ "$4" = resource_limit ] && [ "$5" != done ] && el=TRUE
  [ "$4" = resource_limit ] && [ "$5" = none ] && la=TRUE
  printf '%s\t%s\t%s\t%s\tfailed\t2\t4\tNA\tNA\tNA\tNA\tNA\tNA\tNA\tNA\t%s\tNA\tNA\tNA\tNA\tNA\tNA\tNA\t%s\t%s\n' "$1" "$2" "$3" "$4" "$5" "$el" "$la"
}
ds() { printf 'p0020_S1_r%03d' "$1"; }
SU() { echo "$(ds "$1")_c100"; }
RU() { echo "$(ds "$1")_c100_rep$2"; }
mk_main_state() {
  mkdir -p "$LOGR/launch/main"
  printf 'wave\tstep\tjobid\tarray\tdependency\nmain\ts0_build\t6001\t-\t-\nmain\ts2_smc\t6007\t0-95%%32\tafterok:6001\nmain\ts9_collect\t6010\t-\tafterany:6001\n' > "$RUNH/JOBIDS.tsv"
  cp "$RUNH/JOBIDS.tsv" "$LOGR/jobids.tsv"
}

# =================================================== A. driver: scan phases ============================================================================
echo "== building the fake NOTS tree =="
t_mkfix "$W/fx" "$STAMP"
t_reset_run; mk_main_state
t_run_driver ph_initial --p5-scan --phase initial --profile alone
t_eq "PH01 --p5-scan --phase initial: exit 0" 0 "$DRV_RC"; t_eq "PH02 one submission" 1 "$(t_nsub)"
t_vec "PH03 scan job" --kind p5scan --profile alone
[ -d "$LOGR/launch/p5scan_initial" ]; t_cond "PH04 launch record in launch/p5scan_initial" $?
grep -q 'PHASE=initial' "$T_STUB/sbatch_argv.txt"; t_cond "PH05 the job environment carries PHASE=initial" $?
grep -q 's5_p5scan' "$RUNH/JOBIDS.tsv"; t_cond "PH06 the scan job is recorded in JOBIDS.tsv" $?
t_run_driver ph_initial_again --p5-scan --phase initial --profile alone
[ "$DRV_RC" != 0 ]; t_cond "PH07 reusing the phase name 'initial': refused (exit $DRV_RC)" $?
t_eq "PH08 ... nothing more was submitted" 1 "$(t_nsub)"
t_stub_reset; t_run_driver ph_final --p5-scan --phase final --profile alone
t_eq "PH09 a new phase name (final): exit 0, one submission" "0 1" "$DRV_RC $(t_nsub)"
[ -d "$LOGR/launch/p5scan_final" ]; t_cond "PH10 launch/p5scan_final created, launch/p5scan_initial untouched" $?
for ph in r1 final2; do t_stub_reset; t_run_driver "ph_$ph" --p5-scan --phase $ph --profile withH; t_eq "PH11 phase '$ph' is valid (withH): exit 0" 0 "$DRV_RC"; done
for ph in bogus Initial final_x r r1a ''; do t_stub_reset; t_run_driver "ph_bad_$ph" --p5-scan --phase "$ph" --profile alone
  [ "$DRV_RC" != 0 ] && [ ! -s "$T_STUB/sbatch_calls.txt" ]; t_cond "PH12 invalid phase name '$ph': refused, nothing submitted" $?; done
t_stub_reset; echo '6007_5|lowpL_s2_smc|RUNNING|2' > "$T_STUB/squeue.txt"; t_run_driver ph_active --p5-scan --phase r2 --profile alone
[ "$DRV_RC" != 0 ] && [ ! -s "$T_STUB/sbatch_calls.txt" ]; t_cond "PH13 a scan phase while a run job is active: refused" $?
: > "$T_STUB/squeue.txt"

# =================================================== B. slurm/s5_p5scan.sbatch ==============================================================================
run_scan() {   # run_scan PHASE : the real sbatch script with the frozen-scanner stub
  ( export NC_HOME_ROOT="$FH" NC_SCR_ROOT="$FS" STAMP PHASE="$1" WAVE="p5scan_$1" PATH="$T_BIN:$PATH" STUB_DIR="$T_STUB" PILOT_LOCAL_TEST=1 PILOT_SKIP_MODULES=1 PILOT_TIME_BIN="$T_BIN/gnutime" SLURM_JOB_ID=7500 SLURM_ARRAY_TASK_ID=0
    cd "$W" && bash "$BUN/slurm/s5_p5scan.sbatch" ) > "$W/scan_$1.log" 2>&1
  SC_RC=$?
}
P="$LOGR/p5"
t_stub_reset; { echo "$P5_HDR"; scan_row "$(SU 1)" SMCBVS 0 resource_limit none; scan_row "$(SU 3)" SMCBVS 0 complete none; } > "$T_STUB/scan_smc.tsv"
{ echo "$P5_HDR"; scan_row "$(SU 1)" SMCBVS_rep2 2 resource_limit none; } > "$T_STUB/scan_smcrep.tsv"
rm -rf "$P"; run_scan initial
t_eq "SC01 scan phase 'initial', both scans succeed: exit 0" 0 "$SC_RC"
[ -s "$P/scan_initial_smc.tsv" ] && [ -s "$P/scan_initial_smcrep.tsv" ]; t_cond "SC02 LOG_RUN/p5/scan_initial_smc.tsv and scan_initial_smcrep.tsv written" $?
[ -e "$P/scan_initial.ok" ]; t_cond "SC03 scan_initial.ok written (both scans exited 0)" $?
cmp -s "$P/scan_initial_smc.tsv" "$T_STUB/scan_smc.tsv"; t_cond "SC04 the table is the scanner's output (copied unchanged)" $?
touch "$T_STUB/scan_fail_smcrep"; run_scan r1
[ "$SC_RC" != 0 ]; t_cond "SC05 the smcrep scan fails: the task exits nonzero ($SC_RC)" $?
[ ! -e "$P/scan_r1.ok" ]; t_cond "SC06 ... and scan_r1.ok is NOT written" $?
rm -f "$T_STUB/scan_fail_smcrep"; run_scan final
t_eq "SC07 the failed phase repeated under a NEW name (final): exit 0" 0 "$SC_RC"
[ -e "$P/scan_final.ok" ] && [ -s "$P/scan_final_smc.tsv" ]; t_cond "SC08 scan_final.ok and its tables written" $?
[ ! -e "$P/scan_smc.tsv" ] && [ ! -e "$P/scan_smcrep.tsv" ]; t_cond "SC09 no un-phased scan_smc.tsv / scan_smcrep.tsv (old fixed names) is written" $?

# =================================================== switch to a small lists/units.tsv (the driver tests are over) ==============================================
mk_small_units() {   # smc 6 primaries, smcrep 2 repeat units
  local f="$BUN/lists/units.tsv" i
  printf 'piece\ttask\tunit\tdataset\tscale\trepeat\n' > "$f"
  for i in 1 2 3 4 5 6; do printf 'smc\t0\t%s\t%s\tc100\t0\n' "$(SU $i)" "$(ds $i)" >> "$f"; done
  for i in 1 2; do printf 'smcrep\t0\t%s\t%s\tc100\t2\n' "$(RU $i 2)" "$(ds $i)" >> "$f"; done
}
# ---- result-tree helpers (strict-valid records) ----
res_dir() { echo "$FS/results/${STAMP}_lowp_$1/p0020/${2%_rep[0-9]}"; }
prefix_of() { case $1 in smc) echo SMCBVS;; smcrep) echo "SMCBVS_rep${2##*_rep}";; esac; }
mk_rec_files() {   # mk_rec_files DIR PREFIX V3 STATUS
  local d=$1 p=$2; mkdir -p "$d"; echo "rds $p $RANDOM" > "$d/$p.rds"
  printf 'rule_id,v3_status,status\nhpm,%s,%s\npip05,%s,%s\n' "$3" "$4" "$3" "$4" > "$d/$p.csv"; ( cd "$d" && sha256sum "$p.rds" "$p.csv" > "$p.sha256" )
  printf 'status %s,%s\nfinished_utc 2026-10-30T13:00:00Z\n' "$4" "$4" > "$d/$p.done"
}
mk_primary() { mk_rec_files "$(res_dir "$1" "$2")" "$(prefix_of "$1" "$2")" "$3" "$4"; }                    # mk_primary PIECE UNIT V3 STATUS
mk_retry() { mk_rec_files "$(res_dir "$1" "$2")/P5_retry" "$(prefix_of "$1" "$2")_p5retry" complete ok; }     # a valid P5 retry
mk_attempt() { mkdir -p "$LOGR/p5_attempts"; echo "attempt $1" > "$LOGR/p5_attempts/$1"; }
mk_led() {   # mk_led KIND PIECE UNIT TAG [OUTCOME]
  local d="$LOGR/ledger/$2/$3"; mkdir -p "$d"
  case $1 in
    start)    printf 'unit=%s piece=%s task=0 job_tag=%s host=h start_utc=2026-10-30T13:00:00Z deadline_epoch=1 need_s=1 end_source=x end_epoch=1\n' "$3" "$2" "$4" > "$d/$4.start";;
    end)      printf 'unit=%s rc=1 outcome=%s wall_s=1 cli_status=NA cli_skipped=NA end_utc=2026-10-30T13:00:09Z\n' "$3" "${5:-unit_failed}" > "$d/$4.end";;
    deferred) printf 'unit=%s reason=deadline now_epoch=1 deadline_epoch=1 need_s=1 end_source=x end_epoch=1\n' "$3" > "$d/$4.deferred";;
  esac
}
terminal_jobs() {
  printf 'wave\tstep\tjobid\tarray\tdependency\nmain\ts2_smc\t7002\t0-95%%32\t-\nmain\ts9_collect\t7003\t-\t-\n' > "$RUNH/JOBIDS.tsv"
  printf '7002|lowpL_s2_smc|COMPLETED|0:0|01:00:00|3600|2|commons|commons\n7003|lowpL_s9_collect|COMPLETED|0:0|00:00:30|30|2|commons|commons\n' > "$T_STUB/sacct.txt"; : > "$T_STUB/squeue.txt"
}
fresh() {   # fresh : empty results/logs/p5 state, small lists, terminal jobs, primaries ds1..ds4 (smc) and smcrep ds1 rep2 are native resource_limit (valid, done); ds5, ds6 complete
  chmod -R u+rwx "$FS/results" "$FS/logs" 2>/dev/null; rm -rf "$FS/results" "$FS/logs" "$RUNH/p5" "$RUNH/manifests" "$RUNH/resubmit"; mkdir -p "$FS/results" "$LOGR/p5" "$RUNH/p5"; t_stub_reset
  mk_small_units; terminal_jobs
  local i; for i in 1 2 3 4; do mk_primary smc "$(SU $i)" resource_limit failed; done; for i in 5 6; do mk_primary smc "$(SU $i)" complete ok; done
  mk_primary smcrep "$(RU 1 2)" resource_limit failed; mk_primary smcrep "$(RU 2 2)" complete ok
}
write_scans() {   # write_scans PHASE : initial-style tables (nothing retried yet) of the fresh() state
  { echo "$P5_HDR"; for i in 1 2 3 4; do scan_row "$(SU $i)" SMCBVS 0 resource_limit none; done; for i in 5 6; do scan_row "$(SU $i)" SMCBVS 0 complete none; done; } > "$LOGR/p5/scan_$1_smc.tsv"
  { echo "$P5_HDR"; scan_row "$(SU 1)" SMCBVS_rep2 2 resource_limit none; scan_row "$(SU 2)" SMCBVS_rep2 2 complete none; } > "$LOGR/p5/scan_$1_smcrep.tsv"; echo ok > "$LOGR/p5/scan_$1.ok"
}
run_ml() {   # run_ml LABEL args... : make_p5_list.sh STAMP args
  local label=$1; shift; ML_LOG="$W/ml_$label.log"
  ( export NC_HOME_ROOT="$FH" NC_SCR_ROOT="$FS" PATH="$T_BIN:$PATH" STUB_DIR="$T_STUB" SQUEUE="$T_BIN/squeue" SACCT="$T_BIN/sacct" PYTHON="$T_BIN/python3" GUARD="$T_BIN/guard_simple" STAMP
    cd "$W" && bash "$BUN/make_p5_list.sh" "$STAMP" "$@" ) > "$ML_LOG" 2>&1
  ML_RC=$?
}
units_of() { awk -F'\t' 'NR>1 && NF>=3 {print $3}' "$1" 2>/dev/null; }
col_of() { awk -F'\t' -v n="$2" 'NR>1 && NF>=3 {print $n}' "$1" 2>/dev/null; }
EXP="$RUNH/p5/expected.tsv"

# =================================================== C. make_p5_list.sh --from-scan initial ====================================================================
fresh; write_scans initial; run_ml from_scan --from-scan initial
t_eq "EX01 --from-scan initial: exit 0" 0 "$ML_RC"
[ -s "$EXP" ]; t_cond "EX02 RUN_HOME/p5/expected.tsv written" $?
t_eq "EX03 expected = the eligible primary resource_limit rows of both tables (smc 1-4, smcrep ds1 rep2)" "$(printf '%s\n' "$(SU 1)" "$(SU 2)" "$(SU 3)" "$(SU 4)" "$(RU 1 2)" | sort | tr '\n' ' ')" "$(units_of "$EXP" | sort | tr '\n' ' ')"
t_eq "EX04 piece column is p5 on every row" 0 "$(awk -F'\t' 'NR>1 && NF>=3 && $1!="p5"' "$EXP" | wc -l | tr -d ' ')"
head -n 1 "$EXP" | grep -q 'base_piece'; t_cond "EX05 the table has the base_piece column" $?
t_eq "EX06 base_piece smc for the primaries, smcrep for the repeat unit" "smc smc smc smc smcrep" "$(awk -F'\t' 'NR==1{for(i=1;i<=NF;i++) if($i=="base_piece") c=i} NR>1{print $c}' "$EXP" | tr '\n' ' ' | sed 's/ $//')"
t_eq "EX07 the repeat column carries the scan's repeat_m (2) for the repeat unit" 2 "$(awk -F'\t' 'NR==1{for(i=1;i<=NF;i++) if($i=="repeat") c=i} NR>1 && $3 ~ /_rep2$/{print $c}' "$EXP")"
R="$RUNH/p5/scan_initial.receipt"
[ -s "$R" ] && grep -q "$(sha256sum < "$LOGR/p5/scan_initial_smc.tsv" | cut -c1-64)" "$R" && grep -q "$(sha256sum < "$LOGR/p5/scan_initial_smcrep.tsv" | cut -c1-64)" "$R"; t_cond "EX08 scan_initial.receipt holds the sha256 of both scan tables" $?
[ ! -e "$RUNH/p5/none_eligible.txt" ]; t_cond "EX09 no none_eligible.txt when units are eligible" $?
m1=$(md5sum < "$EXP"); run_ml from_scan_again --from-scan initial
t_eq "EX10 second run with the same scan: exit 0 (idempotent)" 0 "$ML_RC"; t_eq "EX11 ... expected.tsv unchanged" "$m1" "$(md5sum < "$EXP")"
{ echo "$P5_HDR"; for i in 1 2 3 4 5; do scan_row "$(SU $i)" SMCBVS 0 resource_limit none; done; scan_row "$(SU 6)" SMCBVS 0 complete none; } > "$LOGR/p5/scan_initial_smc.tsv"; run_ml from_scan_changed --from-scan initial
t_eq "EX12 a DIFFERENT initial scan: expected.tsv is written once, exit 2" 2 "$ML_RC"; t_eq "EX13 ... and left unchanged" "$m1" "$(md5sum < "$EXP")"
for st in locked incomplete invalid_inspect; do
  fresh; write_scans initial; { echo "$P5_HDR"; scan_row "$(SU 1)" SMCBVS 0 resource_limit none; scan_row "$(SU 2)" SMCBVS 0 resource_limit $st; scan_row "$(SU 5)" SMCBVS 0 complete none; } > "$LOGR/p5/scan_initial_smc.tsv"
  run_ml "state_$st" --from-scan initial
  t_eq "EX20 a resource_limit row in state '$st': refused, exit 2" 2 "$ML_RC"; [ ! -e "$EXP" ]; t_cond "EX20 no expected.tsv written ($st)" $?
done
fresh; write_scans initial; { echo "$P5_HDR"; for i in 1 2; do scan_row "$(SU $i)" SMCBVS 0 complete none; done; } > "$LOGR/p5/scan_initial_smc.tsv"; { echo "$P5_HDR"; } > "$LOGR/p5/scan_initial_smcrep.tsv"
run_ml zero --from-scan initial
t_eq "EX30 zero eligible rows: exit 0" 0 "$ML_RC"
t_eq "EX31 ... expected.tsv holds the header only" 1 "$(t_count_lines "$EXP")"
[ -e "$RUNH/p5/none_eligible.txt" ]; t_cond "EX32 ... and none_eligible.txt is written" $?
fresh; write_scans initial; echo '7002_5|lowpL_s2_smc|RUNNING|2' > "$T_STUB/squeue.txt"; run_ml gate_active --from-scan initial
t_eq "EX40 a run job is active: the gate refuses, exit 3" 3 "$ML_RC"; [ ! -e "$EXP" ]; t_cond "EX40 nothing written" $?
fresh; write_scans initial; touch "$T_STUB/squeue_fail"; run_ml gate_sq --from-scan initial
t_eq "EX41 squeue fails: exit 4" 4 "$ML_RC"
fresh; run_ml no_scan --from-scan initial
[ "$ML_RC" != 0 ] && [ ! -e "$EXP" ]; t_cond "EX42 no scan_initial tables at all: refused (exit $ML_RC), nothing written" $?

# =================================================== D. P5 waves: never-started units are relisted, attempted units are exceptions ==============================
# expected: U1 smc1 (attempt + valid retry = done), U2 smc2 (attempt, no valid retry), U3 smc3 and U4 smc4 (never started), U5 smcrep ds1 rep2 (never started)
dfresh() { fresh; write_scans initial; run_ml dfresh --from-scan initial; mk_attempt "$(SU 1)"; mk_retry smc "$(SU 1)"; mk_attempt "$(SU 2)"; mk_led start p5 "$(SU 2)" 7300_1; mk_led end p5 "$(SU 2)" 7300_1; }
dfresh; run_ml wave_p5 --wave p5
t_eq "WV01 --wave p5: exit 0" 0 "$ML_RC"
W1="$RUNH/p5/units_p5.tsv"; X1="$RUNH/p5/exceptions_p5.tsv"
t_eq "WV02 units_p5.tsv = the never-started units only (U3, U4, U5)" "$(printf '%s\n' "$(SU 3)" "$(SU 4)" "$(RU 1 2)" | sort | tr '\n' ' ')" "$(units_of "$W1" | sort | tr '\n' ' ')"
t_eq "WV03 one unit per task, tasks 0..k-1" "0 1 2" "$(col_of "$W1" 2 | sort -n | tr '\n' ' ' | sed 's/ $//')"
t_eq "WV04 the attempted unit without a valid retry (U2) is an exception" "$(SU 2)" "$(units_of "$X1" | tr '\n' ' ' | sed 's/ $//')"
units_of "$W1" | grep -qx "$(SU 1)"; [ $? -ne 0 ]; t_cond "WV05 the unit with a valid retry (U1) is neither listed nor an exception" $?
units_of "$X1" | grep -qx "$(SU 1)"; [ $? -ne 0 ]; t_cond "WV05b ... (not an exception either)" $?
m1=$(md5sum < "$W1"); run_ml wave_p5_again --wave p5
t_eq "WV06 same state, same wave: exit 0" 0 "$ML_RC"; grep -q SAME_LIST "$ML_LOG"; t_cond "WV07 ... says SAME_LIST" $?
mk_attempt "$(SU 3)"; run_ml wave_p5_changed --wave p5
t_eq "WV08 state changed (U3 now has an attempt), same wave name: exit 2 (new wave name needed)" 2 "$ML_RC"; t_eq "WV09 ... the existing list is untouched" "$m1" "$(md5sum < "$W1")"
mk_led start p5 "$(SU 3)" 7301_0                                                                      # U3 started and was killed: attempted, no valid retry
run_ml wave_p5r1 --wave p5r1
t_eq "WV10 --wave p5r1: exit 0" 0 "$ML_RC"
t_eq "WV11 units_p5r1.tsv = the units still never started (U4, U5); U3 is NOT relisted" "$(printf '%s\n' "$(SU 4)" "$(RU 1 2)" | sort | tr '\n' ' ')" "$(units_of "$RUNH/p5/units_p5r1.tsv" | sort | tr '\n' ' ')"
t_eq "WV12 exceptions_p5r1.tsv = U2 and U3 (attempted, no valid retry; never relisted)" "$(printf '%s\n' "$(SU 2)" "$(SU 3)" | sort | tr '\n' ' ')" "$(units_of "$RUNH/p5/exceptions_p5r1.tsv" | sort | tr '\n' ' ')"
mk_attempt "$(SU 4)"; mk_attempt "$(RU 1 2)"
run_ml wave_p5r2 --wave p5r2
t_eq "WV20 every expected unit has an attempt or a retry: exit 0" 0 "$ML_RC"
grep -q NOTHING_TO_SUBMIT "$ML_LOG"; t_cond "WV21 prints NOTHING_TO_SUBMIT" $?
[ ! -e "$RUNH/p5/units_p5r2.tsv" ]; t_cond "WV22 and writes no units_p5r2.tsv" $?
dfresh; echo '7002_5|lowpL_s2_smc|RUNNING|2' > "$T_STUB/squeue.txt"; run_ml wave_gate --wave p5
t_eq "WV30 a run job is active: refused, exit 3" 3 "$ML_RC"; [ ! -e "$W1" ]; t_cond "WV30 nothing written" $?
dfresh; run_ml wave_bad --wave p6
[ "$ML_RC" != 0 ] && [ ! -e "$RUNH/p5/units_p6.tsv" ]; t_cond "WV31 an invalid wave name (p6): refused (exit $ML_RC)" $?
fresh; write_scans initial; run_ml wave_noexp --wave p5
dfresh_noexp=1; rm -f "$EXP"; run_ml wave_noexp2 --wave p5
[ "$ML_RC" != 0 ]; t_cond "WV32 --wave p5 without expected.tsv: refused (exit $ML_RC)" $?

# =================================================== E. reconcile_prodl.py: the P5 inventory =====================================================================
run_rec() {   # run_rec LABEL : REC_RC ; tables in $W/rec_<label>/inventory/<piece>.tsv
  local o="$W/rec_$1"; rm -rf "$o"
  ( cd "$W" && "$T_BIN/python3" "$BUN/reconcile_prodl.py" "$STAMP" --home-root "$FH" --scr-root "$FS" --lists "$BUN/lists/units.tsv" --out "$o" ) > "$W/rec_$1.log" 2>&1
  REC_RC=$?; REC_OUT="$o"
}
outcome_of() { awk -F'\t' -v u="$2" 'NR==1{for(i=1;i<=NF;i++){if($i=="unit")ui=i; if($i=="outcome")oi=i}} NR>1 && $ui==u {print $oi}' "$REC_OUT/inventory/$1.tsv" 2>/dev/null; }
fresh; write_scans initial; run_ml e_expected --from-scan initial
U1=$(SU 1); U2=$(SU 2); U3=$(SU 3); U4=$(SU 4); U5=$(RU 1 2)
mk_attempt "$U1"; mk_retry smc "$U1"                                                            # done
mk_attempt "$U2"; mk_led start p5 "$U2" 7300_0; mk_led end p5 "$U2" 7300_0                       # attempt_failed
mk_led deferred p5 "$U3" 7300_1                                                                  # deferred (never started)
mk_attempt "$U4"; mk_led start p5 "$U4" 7300_2                                                   # killed_external (start, no end; NODE_FAIL)
                                                                                                  # U5 (smcrep): not_run
run_rec p5_states
[ "$REC_RC" != 0 ]; t_cond "RP01 reconcile exits nonzero while P5 units are unfinished (exit $REC_RC) although every primary is done" $?
[ -s "$REC_OUT/inventory/p5.tsv" ]; t_cond "RP02 inventory/p5.tsv written" $?
head -n 1 "$REC_OUT/inventory/p5.tsv" | grep -q $'^piece\tunit\toutcome\tdetail'; t_cond "RP03 header is piece unit outcome detail" $?
t_eq "RP04 U1 (valid P5_retry record): done" done "$(outcome_of p5 "$U1")"
t_eq "RP05 U2 (attempt record + failed end, no valid retry): attempt_failed" attempt_failed "$(outcome_of p5 "$U2")"
t_eq "RP06 U3 (ledger deferred only): deferred" deferred "$(outcome_of p5 "$U3")"
t_eq "RP07 U4 (attempt + start, no end): killed_external" killed_external "$(outcome_of p5 "$U4")"
t_eq "RP08 U5 (nothing): not_run" not_run "$(outcome_of p5 "$U5")"
t_eq "RP09 every expected P5 unit exactly once (5 rows)" 5 "$(awk -F'\t' 'NR>1 && NF>=3' "$REC_OUT/inventory/p5.tsv" | wc -l | tr -d ' ')"
grep -qi 'P5' "$REC_OUT/INVENTORY.md"; t_cond "RP10 INVENTORY.md has a P5 section" $?
t_eq "RP11 the primaries themselves are reported done (smc U1)" done "$(outcome_of smc "$U1")"
# interrupted P5 (start without end under a NODE_FAIL job) keeps reconcile nonzero even with everything else finished
for u in "$U2" "$U3" "$U5"; do mk_attempt "$u"; done
mk_retry smc "$U2"; mk_retry smc "$U3"; mk_retry smcrep "$U5"
run_rec p5_one_left
[ "$REC_RC" != 0 ]; t_cond "RP12 one expected unit (U4, killed) still has no valid retry: exit nonzero" $?
t_eq "RP13 U2, U3, U5 are done now; U4 stays killed_external" "done done done killed_external" "$(outcome_of p5 "$U2") $(outcome_of p5 "$U3") $(outcome_of p5 "$U5") $(outcome_of p5 "$U4")"
mk_retry smc "$U4"; run_rec p5_all_done
t_eq "RP14 every expected P5 unit done and every primary done: exit 0" 0 "$REC_RC"
t_eq "RP15 all five P5 rows are done" "done" "$(awk -F'\t' 'NR>1 && NF>=3{print $3}' "$REC_OUT/inventory/p5.tsv" | sort -u | tr '\n' ' ' | sed 's/ $//')"
# a retry record that is not valid is not done
printf 'tampered\n' >> "$(res_dir smc "$U4")/P5_retry/SMCBVS_p5retry.rds"; run_rec p5_bad_retry
[ "$REC_RC" != 0 ] && [ "$(outcome_of p5 "$U4")" != done ]; t_cond "RP16 a P5 retry whose sidecar no longer verifies is not done (exact-file validation, F6)" $?
# without expected.tsv: pending
fresh; run_rec p5_pending
grep -q 'p5_scan_pending' "$REC_OUT/inventory/smc.tsv" 2>/dev/null; t_cond "RP20 without expected.tsv the smc rows carry detail p5_scan_pending" $?
grep -q 'p5_scan_pending' "$REC_OUT/inventory/smcrep.tsv" 2>/dev/null; t_cond "RP21 ... and the smcrep rows too" $?
grep -qi 'PENDING' "$REC_OUT/INVENTORY.md" 2>/dev/null; t_cond "RP22 INVENTORY.md says the P5 status is PENDING" $?
[ ! -e "$REC_OUT/inventory/p5.tsv" ] || [ "$(awk 'NR>1' "$REC_OUT/inventory/p5.tsv" | wc -l | tr -d ' ')" = 0 ]; t_cond "RP23 ... and has no P5 rows" $?

# =================================================== R2 / I1: no eligible P5 unit can be missed, whenever its primary completed =====================================
# Sol's reproductions repro_r2.sh and repro_r2_late_complete_scan.sh as regressions. Rules under test (R2_FIX_PLAN.md I1):
#  1. make_p5_list.sh STAMP --from-scan <phase> accepts ANY phase with scan_<phase>.ok (initial, rN, finalN); creates expected.tsv if absent; otherwise APPENDS newly eligible units
#     (never removes or reorders rows); every use appends a line to p5/expected_history.tsv (utc phase scan_smc_sha256 scan_smcrep_sha256 rows_before rows_after); same phase twice adds nothing;
#     locked / incomplete / invalid_inspect on a resource_limit row refuses for every phase.
#  2. closing smc/smcrep needs a FINAL scan (final*) that succeeded, whose job id is greater than EVERY fitting job id (s1_-s4_, all waves), and passes a coverage check against the piece:
#     every done unit is a row (case_id + repeat_m), no row for a unit that is not done, every resource_limit row is in expected.tsv, no unsafe retry_state -> else exit 6 (also for zero-expected runs).
#  3. reconcile uses the newest successful scan phase and reports a resource_limit primary missing from expected.tsv as exception kind p5_unlisted_eligible (nonzero exit).
run_mm() {   # run_mm LABEL args... : make_manifests.sh STAMP args
  local label=$1; shift; MM_LOG="$W/mm_$label.log"
  ( export NC_HOME_ROOT="$FH" NC_SCR_ROOT="$FS" PATH="$T_BIN:$PATH" STUB_DIR="$T_STUB" SQUEUE="$T_BIN/squeue" SACCT="$T_BIN/sacct" PYTHON="$T_BIN/python3" GUARD="$T_BIN/guard_simple" STAMP
    cd "$W" && bash "$BUN/make_manifests.sh" "$STAMP" "$@" ) > "$MM_LOG" 2>&1
  MM_RC=$?
}
jobs_add() {   # jobs_add WAVE STEP ID [STATE] : a recorded job with a (terminal) accounting row
  printf '%s\t%s\t%s\t-\t-\n' "$1" "$2" "$3" >> "$RUNH/JOBIDS.tsv"; printf '%s|lowpL_%s|%s|0:0|00:01:00|60|2|commons|commons\n' "$3" "$2" "${4:-COMPLETED}" >> "$T_STUB/sacct.txt"
}
smc_tab() { local p=$1; shift; { echo "$P5_HDR"; local r; for r in "$@"; do printf '%s\n' "$r"; done; } > "$LOGR/p5/scan_${p}_smc.tsv"; }
rep_tab() { local p=$1; shift; { echo "$P5_HDR"; local r; for r in "$@"; do printf '%s\n' "$r"; done; } > "$LOGR/p5/scan_${p}_smcrep.tsv"; }
ok_scan() { echo "phase=$1" > "$LOGR/p5/scan_$1.ok"; }
row() { scan_row "$@"; }                      # row CASE_ID BASE REPEAT_M PRIMARY_V3 RETRY_STATE
REPROW() { row "$(SU 1)" SMCBVS_rep1 1 completed none; }
lf() {   # lf : units smc ds1..ds3 + smcrep ds1 rep1. ds1 and the repeat are done and completed; ds2, ds3 are NOT fitted yet (a later r1 wave will). Initial scan phase finished: nothing eligible.
  chmod -R u+rwx "$FS/results" "$FS/logs" 2>/dev/null; rm -rf "$FS/results" "$FS/logs" "$RUNH/p5" "$RUNH/manifests" "$RUNH/resubmit"; mkdir -p "$FS/results" "$LOGR/p5" "$RUNH/p5"; t_stub_reset
  local f="$BUN/lists/units.tsv" i; printf 'piece\ttask\tunit\tdataset\tscale\trepeat\n' > "$f"
  for i in 1 2 3; do printf 'smc\t0\t%s\t%s\tc100\t0\n' "$(SU $i)" "$(ds $i)" >> "$f"; done; printf 'smcrep\t0\t%s\t%s\tc100\t1\n' "$(RU 1 1)" "$(ds 1)" >> "$f"
  printf 'wave\tstep\tjobid\tarray\tdependency\n' > "$RUNH/JOBIDS.tsv"; : > "$T_STUB/sacct.txt"; : > "$T_STUB/squeue.txt"
  jobs_add main s2_smc 7002; jobs_add p5scan_initial s5_p5scan 7003
  mk_primary smc "$(SU 1)" completed warning; mk_primary smcrep "$(RU 1 1)" completed warning
  smc_tab initial "$(row "$(SU 1)" SMCBVS 0 completed none)"; rep_tab initial "$(REPROW)"; ok_scan initial
}
late() {   # late : an ordinary r1 wave finishes ds2 (native resource_limit) and ds3 (completed)
  jobs_add r1 s2_smc 7010; mk_primary smc "$(SU 2)" resource_limit failed; mk_primary smc "$(SU 3)" completed ok
}
fin() {   # fin PHASE JOBID DS2_V3 DS2_RETRY [DS1_V3 DS1_RETRY] : final tables of lf+late, then the scan job
  local ph=$1 job=$2
  smc_tab "$ph" "$(row "$(SU 1)" SMCBVS 0 "${5:-completed}" "${6:-none}")" "$(row "$(SU 2)" SMCBVS 0 "$3" "$4")" "$(row "$(SU 3)" SMCBVS 0 completed none)"
  rep_tab "$ph" "$(REPROW)"; ok_scan "$ph"; jobs_add "p5scan_$ph" s5_p5scan "$job"
}
exc_has() { awk -F'\t' -v k="$2" -v i="$3" 'NR>1 && $2==k && index($3,i)>0' "$REC_OUT/exceptions.tsv" 2>/dev/null | grep -q .; }
xcount() { awk 'NR>1' "$1" 2>/dev/null | wc -l | tr -d ' '; }

# ---- I1-a  the reproduced path: EMPTY initial inventory -> a later r1 wave commits a resource_limit primary -> the FINAL scan lists it as eligible ---------------
lf; run_ml i1a_init --from-scan initial
t_eq "L101 (setup) empty initial inventory from the initial scan: exit 0, expected.tsv header only" "0 1" "$ML_RC $(t_count_lines "$EXP")"
late; fin final 7011 resource_limit none
run_rec i1a
[ "$REC_RC" != 0 ]; t_cond "L102 late resource_limit primary absent from expected.tsv: reconcile exits NONZERO ($REC_RC)" $?
exc_has x p5_unlisted_eligible "$(SU 2)"; t_cond "L103 ... exceptions.tsv lists it as kind p5_unlisted_eligible" $?
head -n 1 "$REC_OUT/exceptions.tsv" | grep -q $'^piece\tkind\titem\tdetail'; t_cond "L104 ... exceptions.tsv header is piece kind item detail" $?
grep -qi 'final' "$REC_OUT/INVENTORY.md"; t_cond "L105 INVENTORY.md states which scan phase the P5 check used (final)" $?
run_mm i1a_close --piece smc
t_eq "L106 closing smc: exit 6 (an eligible unit is missing from the expected inventory)" 6 "$MM_RC"; [ ! -e "$RUNH/manifests/smc.CLOSED" ]; t_cond "L107 ... not CLOSED" $?

# ---- I1-b  the same with a NONEMPTY initial list plus one later eligible unit ------------------------------------------------------------------------------------
lf; mk_primary smc "$(SU 1)" resource_limit failed; smc_tab initial "$(row "$(SU 1)" SMCBVS 0 resource_limit none)"; ok_scan initial
run_ml i1b_init --from-scan initial; U1=$(SU 1); mk_attempt "$U1"; mk_retry smc "$U1"
late; fin final 7011 resource_limit none resource_limit done
run_rec i1b
[ "$REC_RC" != 0 ]; t_cond "L110 nonempty initial list + a later eligible unit (ds2): reconcile exits nonzero ($REC_RC)" $?
exc_has x p5_unlisted_eligible "$(SU 2)"; t_cond "L111 ... only the NEW unit is reported unlisted" $?
exc_has x p5_unlisted_eligible "$(SU 1)"; [ $? -ne 0 ]; t_cond "L112 ... the already-listed ds1 is not reported" $?
run_mm i1b_close --piece smc
t_eq "L113 closing smc: exit 6" 6 "$MM_RC"

# ---- I1-c  extension from a LATER phase: append exactly the new unit, history line, idempotent, then closure succeeds after its retry and a NEWER final scan ----------------
before_head=$(head -n 2 "$EXP" | md5sum)
smc_tab r1 "$(row "$(SU 1)" SMCBVS 0 resource_limit done)" "$(row "$(SU 2)" SMCBVS 0 resource_limit none)" "$(row "$(SU 3)" SMCBVS 0 completed none)"; rep_tab r1 "$(REPROW)"; ok_scan r1; jobs_add p5scan_r1 s5_p5scan 7012
run_ml i1c_ext --from-scan r1
t_eq "L120 --from-scan r1 (a successful scan phase after a fitting wave): exit 0" 0 "$ML_RC"
t_eq "L121 expected.tsv now has exactly 2 rows: ds1 then ds2" "$(printf '%s\n' "$(SU 1)" "$(SU 2)" | tr '\n' ' ')" "$(units_of "$EXP" | tr '\n' ' ')"
t_eq "L122 the existing row is neither removed nor changed (header + first row byte-identical)" "$before_head" "$(head -n 2 "$EXP" | md5sum)"
H="$RUNH/p5/expected_history.tsv"
[ -s "$H" ] && awk -F'\t' '$2=="r1"{f=1; b=$5; a=$6} END{exit !(f && b==1 && a==2)}' "$H"; t_cond "L123 expected_history.tsv has a line for phase r1 with rows_before=1 rows_after=2 (utc phase sha sha before after)" $?
awk -F'\t' '$2=="r1"{print $3, $4}' "$H" | grep -q "$(sha256sum < "$LOGR/p5/scan_r1_smc.tsv" | cut -c1-64) $(sha256sum < "$LOGR/p5/scan_r1_smcrep.tsv" | cut -c1-64)"; t_cond "L124 ... and carries the sha256 of both scan tables" $?
m=$(md5sum < "$EXP"); hn=$(t_count_lines "$H"); run_ml i1c_again --from-scan r1
t_eq "L125 the same phase a second time: exit 0, expected.tsv unchanged (adds nothing)" "0 $m" "$ML_RC $(md5sum < "$EXP")"
[ "$(t_count_lines "$H")" = "$hn" ] || awk -F'\t' 'END{exit !($5==$6)}' "$H"; t_cond "L126 ... no history line is added, or the added line shows rows_before == rows_after" $?
run_ml i1c_wave --wave p5
t_eq "L127 --wave p5 lists exactly the new, never-started unit (ds2)" "$(SU 2)" "$(units_of "$RUNH/p5/units_p5.tsv" | tr '\n' ' ' | sed 's/ $//')"
mk_attempt "$(SU 2)"; mk_retry smc "$(SU 2)"; jobs_add p5 s4_p5 7020
fin final2 7030 resource_limit done resource_limit done
run_rec i1c_done
t_eq "L128 after the new unit's retry is done and a newer final scan exists: reconcile exits 0" 0 "$REC_RC"
run_mm i1c_close --piece smc
t_eq "L129 ... and closure of smc succeeds (the newest final scan, job 7030 > every fitting job, passes coverage)" 0 "$MM_RC"
[ -e "$RUNH/manifests/smc.CLOSED" ]; t_cond "L130 ... CLOSED written" $?

# ---- I1-d  the zero-eligible control: a FINAL scan is required and sufficient --------------------------------------------------------------------------------------
lf; run_ml i1d_init --from-scan initial; jobs_add r1 s2_smc 7010; mk_primary smc "$(SU 2)" completed ok; mk_primary smc "$(SU 3)" completed ok
run_mm i1d_noscan --piece smc
t_eq "L140 zero expected units and only scan_initial.ok (no final scan): exit 6 (the shortcut is gone)" 6 "$MM_RC"
fin final 7011 completed none
run_mm i1d_final --piece smc
t_eq "L141 zero expected units with a complete newer final scan: closes, exit 0" 0 "$MM_RC"

# ---- I1-e  coverage violations of the final scan --------------------------------------------------------------------------------------------------------------------
good() { lf; run_ml g_init --from-scan initial; late_ok; fin final 7011 completed none; }
late_ok() { jobs_add r1 s2_smc 7010; mk_primary smc "$(SU 2)" completed ok; mk_primary smc "$(SU 3)" completed ok; }
good; run_mm cov_control --piece smc; t_eq "L150 (control) the all-good zero-expected state closes: exit 0" 0 "$MM_RC"
good; smc_tab final "$(row "$(SU 1)" SMCBVS 0 completed none)" "$(row "$(SU 3)" SMCBVS 0 completed none)"; run_mm cov_missing --piece smc
t_eq "L151 a DONE unit (ds2) is missing from the final scan table: exit 6" 6 "$MM_RC"
good; smc_tab final "$(row "$(SU 1)" SMCBVS 0 completed none)" "$(row "$(SU 2)" SMCBVS 0 completed none)" "$(row "$(SU 3)" SMCBVS 0 completed none)" "$(row "$(ds 9)_c100" SMCBVS 0 completed none)"; run_mm cov_extra --piece smc
t_eq "L152 the final scan has a row for a unit that is not a done unit of the piece (ds9): exit 6" 6 "$MM_RC"
good; jobs_add r2 s2_smc 7012; run_mm cov_older --piece smc
t_eq "L153 a fitting wave (r2, job 7012) newer than the final scan job (7011): exit 6" 6 "$MM_RC"
good; jobs_add p5 s4_p5 7015; run_mm cov_older_p5 --piece smc
t_eq "L154 a P5 wave job (7015) newer than the final scan job: exit 6" 6 "$MM_RC"
good; jobs_add main s1_enum30 7016; run_mm cov_older_enum --piece smc
t_eq "L155 ANY fitting job counts, not only smc/P5 waves (an s1_ job 7016 newer than the final scan): exit 6" 6 "$MM_RC"
for st in locked incomplete invalid_inspect; do
  good; smc_tab final "$(row "$(SU 1)" SMCBVS 0 completed none)" "$(row "$(SU 2)" SMCBVS 0 resource_limit $st)" "$(row "$(SU 3)" SMCBVS 0 completed none)"
  run_mm "cov_$st" --piece smc; t_eq "L156 a resource_limit row in state '$st' in the final scan: exit 6" 6 "$MM_RC"
done
good; rm -f "$LOGR/p5/scan_final.ok"; run_mm cov_nook --piece smc
t_eq "L157 the final scan has no .ok (did not finish): exit 6" 6 "$MM_RC"
good; smc_tab final "$(row "$(SU 1)" SMCBVS 0 completed none)"; run_mm cov_allow2 --piece smc --allow-incomplete
t_eq "L158 coverage violations can be acknowledged with --allow-incomplete: exit 0" 0 "$MM_RC"

# ---- I1-f  --from-scan <rN> creates expected.tsv when the INITIAL scan failed (II1 removed by code) -----------------------------------------------------------------
lf; rm -f "$LOGR/p5/scan_initial.ok" "$LOGR/p5/scan_initial_smc.tsv" "$LOGR/p5/scan_initial_smcrep.tsv"
smc_tab r1 "$(row "$(SU 1)" SMCBVS 0 completed none)" "$(row "$(SU 2)" SMCBVS 0 resource_limit none)"; rep_tab r1 "$(REPROW)"; ok_scan r1; jobs_add p5scan_r1 s5_p5scan 7012
run_ml i1f_r1 --from-scan r1
t_eq "L160 initial scan failed, r1 succeeded: --from-scan r1 creates expected.tsv, exit 0" 0 "$ML_RC"
t_eq "L161 ... with the eligible unit (ds2)" "$(SU 2)" "$(units_of "$EXP" | tr '\n' ' ' | sed 's/ $//')"
awk -F'\t' '$2=="r1"{f=1; b=$5; a=$6} END{exit !(f && b==0 && a==1)}' "$H"; t_cond "L162 ... and expected_history.tsv records rows_before=0 rows_after=1" $?
lf; run_ml i1f_initial_missing --from-scan initial
t_eq "L163 (control) the initial phase is still accepted when its tables and .ok exist: exit 0" 0 "$ML_RC"
lf; smc_tab r2 "$(row "$(SU 1)" SMCBVS 0 completed none)"; rep_tab r2 "$(REPROW)"; run_ml i1f_no_ok --from-scan r2
[ "$ML_RC" != 0 ]; t_cond "L164 a phase without scan_<phase>.ok is refused (exit $ML_RC)" $?
for st in locked incomplete invalid_inspect; do
  lf; run_ml i1g_init --from-scan initial; m=$(md5sum < "$EXP")
  smc_tab r1 "$(row "$(SU 1)" SMCBVS 0 completed none)" "$(row "$(SU 2)" SMCBVS 0 resource_limit $st)"; rep_tab r1 "$(REPROW)"; ok_scan r1; jobs_add p5scan_r1 s5_p5scan 7012
  run_ml "i1g_$st" --from-scan r1
  t_eq "L170 phase r1 with a resource_limit row in state '$st': refused, exit 2" 2 "$ML_RC"; t_eq "L171 ... expected.tsv unchanged ($st)" "$m" "$(md5sum < "$EXP")"
done
lf; run_ml i1h_init --from-scan initial
smc_tab final2 "$(row "$(SU 1)" SMCBVS 0 completed none)" "$(row "$(SU 2)" SMCBVS 0 resource_limit none)"; rep_tab final2 "$(REPROW)"; ok_scan final2; jobs_add p5scan_final2 s5_p5scan 7040
run_ml i1h_final2 --from-scan final2
t_eq "L172 a finalN phase can extend the inventory too: exit 0, ds2 appended" "0 $(SU 2)" "$ML_RC $(units_of "$EXP" | tr '\n' ' ' | sed 's/ $//')"

t_summary
