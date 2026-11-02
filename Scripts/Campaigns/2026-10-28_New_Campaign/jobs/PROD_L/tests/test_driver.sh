#!/bin/bash
# test_driver.sh -- acceptance tests of submit_prodl.sh (DESIGN.md section 5, 6, 7): recorded sbatch vectors for both profiles, launch record, job-id files,
# later waves, P5, and the negative controls (each must refuse with the stated exit status and submit NOTHING).
#   bash test_driver.sh WORKDIR        (WORKDIR under C:/Users/felip/AppData/Local/Temp/prodl_tests/)
source "$(dirname "$0")/lib.sh"
t_init "${1:-}" test_driver
[ -f "${PRODL_B_SRC:-$B}/submit_prodl.sh" ]; t_cond "D00 submit_prodl.sh exists in the bundle" $?
echo "== building the fake NOTS tree (1,200 inputs + 1,200 truth + 60 + 60 files; takes a minute) =="
t_mkfix "$W/fx" 20261030T1200Z

mk_main_state() {   # what exists after a finished main wave: launch/main, jobids.tsv in both places (wave step jobid array dependency)
  mkdir -p "$LOGR/launch/main"
  printf 'wave\tstep\tjobid\tarray\tdependency\nmain\ts0_build\t6001\t-\t-\nmain\ts2_smc\t6007\t0-95%%32\tafterok:6001\nmain\ts9_collect\t6010\t-\tafterany:6001\n' > "$RUNH/JOBIDS.tsv"
  cp "$RUNH/JOBIDS.tsv" "$LOGR/jobids.tsv"
}
mk_p5() {   # mk_p5 N WAVE : RUN_HOME/p5/units_<wave>.tsv (one unit per task) and the expected inventory expected.tsv (F2)
  t_mk_unitlist "$RUNH/p5/units_$2.tsv" p5 "$1"; cp "$RUNH/p5/units_$2.tsv" "$RUNH/p5/expected.tsv"
}
no_hits() { [ ! -s "$T_STUB/sbatch_calls.txt" ]; }
aborted_file() { find "$LOGR" -name SUBMISSION_ABORTED.txt 2>/dev/null | head -n 1; }
guard_called() { [ -s "$T_STUB/guard_calls.txt" ]; }

# ---- launch record + job-id files of a completed wave ------------------------------------------------------------------------
check_launch() {   # check_launch WAVE NSUB PLANNED_MB
  local wave=$1 n=$2 mb=$3 L="$LOGR/launch/$1" f c g
  [ -d "$L" ]; t_cond "launch/$wave folder exists in LOG_RUN" $?
  for f in prodl.env prodl.env.sha256 STAGED_SHA256.txt OWNER effective_env.txt; do [ -s "$L/$f" ]; t_cond "launch/$wave/$f present" $?; done
  sv=$(ls "$L" 2>/dev/null | grep -E '^sbatch_args' | head -n 1)      # the pilot called it sbatch_args.tsv; DESIGN only says "every sbatch vector"
  [ -n "$sv" ] && [ -s "$L/$sv" ]; t_cond "launch/$wave/sbatch_args* present" $?
  ( cd "$L" 2>/dev/null && sha256sum -c prodl.env.sha256 >/dev/null 2>&1 ); t_cond "launch/$wave/prodl.env.sha256 verifies prodl.env" $?
  ls "$L" 2>/dev/null | grep -qi 'v2_2_1'; t_cond "launch/$wave holds the frozen manifest (v2_2_1.SHA256SUMS)" $?
  [ -s "$L/lists/units.tsv" ]; t_cond "launch/$wave/lists/units.tsv recorded" $?
  g=$(ls "$L" 2>/dev/null | grep -i 'guard' | head -n 1); [ -n "$g" ] && grep -q GUARD_CHECK_OK "$L/$g"; t_cond "launch/$wave guard receipt (GUARD_CHECK_OK)" $?
  c=$(ls "$L" 2>/dev/null | grep -i 'ceiling' | head -n 1); [ -n "$c" ] && [ -s "$L/$c" ]; t_cond "launch/$wave ceiling receipt present" $?
  t_eq "launch/$wave/sbatch_args* holds every sbatch vector (one line each)" "$n" "$(t_count_lines "$L/${sv:-sbatch_args.tsv}")"
  grep -qx "$mb" "$T_STUB/guard_calls.txt" 2>/dev/null; t_cond "guard asked for PLANNED_HOME_MB=$mb for wave $wave" $?
  for f in "$LOGR/jobids.tsv" "$RUNH/JOBIDS.tsv"; do
    t_eq "$(basename "$f"): header columns" $'wave\tstep\tjobid\tarray\tdependency' "$(head -n 1 "$f" 2>/dev/null | tr -d '\r')"
    t_eq "$(basename "$f"): $n rows with wave=$wave" "$n" "$(awk -F'\t' -v w="$wave" 'NR>1 && $1==w' "$f" 2>/dev/null | wc -l | tr -d ' ')"
    t_eq "$(basename "$f"): every job id is digits only" 0 "$(awk -F'\t' 'NR>1 && $3 !~ /^[0-9]+$/' "$f" 2>/dev/null | wc -l | tr -d ' ')"
  done
  t_eq "jobids.tsv in LOG_RUN and JOBIDS.tsv in RUN_HOME agree" "$(sort "$LOGR/jobids.tsv" 2>/dev/null | md5sum)" "$(sort "$RUNH/JOBIDS.tsv" 2>/dev/null | md5sum)"
}

# ===================================================== A. main wave, both profiles ==========================================================
for prof in alone withH; do
  t_reset_run; DRV_ENV=(SECRET_TOKEN_TEST=xyz_secret_value); t_run_driver main_$prof --wave main --profile $prof; DRV_ENV=()
  t_eq "D01 main/$prof: exit 0" 0 "$DRV_RC"
  [ -s "$LOGR/launch/main/effective_env.txt" ] && ! grep -q -e SECRET_TOKEN_TEST -e xyz_secret_value "$LOGR/launch/main/effective_env.txt"
  t_cond "D01b main/$prof: effective_env.txt lists only the named variables (a dummy SECRET_TOKEN_TEST in the environment is absent)" $?
  t_eq "D02 main/$prof: exactly 10 submissions" 10 "$(t_nsub)"
  t_vec "D03 main/$prof" --kind main --profile $prof --logrun "$(t_win "$LOGR")"
  check_launch main 10 10      # HQ D57: after extraction the main wave asks only for the growth (10 MB), never the stage (110 MB) again
done

# ===================================================== B. dry run and piece subsets ==========================================================
t_reset_run; DRV_ENV=(); t_run_driver dry --wave main --profile alone --dry-run
t_eq "D04 dry run: exit 0" 0 "$DRV_RC"
no_hits; t_cond "D05 dry run: sbatch is never called" $?
[ ! -e "$LOGR/launch" ] && [ ! -e "$RUNH/JOBIDS.tsv" ]; t_cond "D06 dry run: no launch record and no JOBIDS.tsv created" $?
grep -q '0-23%4' "$DRV_LOG" && grep -q '0-95%32' "$DRV_LOG" && grep -q '0-479%32' "$DRV_LOG"; t_cond "D07 dry run: prints the vectors with the throttled arrays" $?
t_eq "D08 dry run: prints 10 vectors" 10 "$(grep -c 'sbatch' "$DRV_LOG" | tr -d ' ')"

t_reset_run; t_run_driver sub1 --wave main --profile alone --pieces enum20,enum30
t_eq "D09 --pieces enum20,enum30: exit 0" 0 "$DRV_RC"; t_eq "D10 --pieces enum20,enum30: 8 submissions" 8 "$(t_nsub)"
t_vec "D11 pieces enum20,enum30" --kind main --profile alone --pieces enum20,enum30
t_reset_run; t_run_driver sub2 --wave main --profile withH --pieces smc,smcrep
t_eq "D12 --pieces smc,smcrep: exit 0" 0 "$DRV_RC"; t_eq "D13 --pieces smc,smcrep: 8 submissions" 8 "$(t_nsub)"
t_vec "D14 pieces smc,smcrep withH" --kind main --profile withH --pieces smc,smcrep
t_reset_run; t_run_driver sub3 --wave main --profile alone --pieces smcrep
t_eq "D15 --pieces smcrep: exit 0" 0 "$DRV_RC"; t_eq "D16 --pieces smcrep: 7 submissions" 7 "$(t_nsub)"
t_vec "D17 pieces smcrep" --kind main --profile alone --pieces smcrep

# ===================================================== C. --local-test accepted with its hooks ===============================================
t_reset_run; DRV_ENV=(PILOT_LOCAL_TEST=1 PILOT_SKIP_MODULES=1); t_run_driver localtest --wave main --profile alone --local-test
t_eq "D18 --local-test + PILOT_LOCAL_TEST=1 + fake NC_HOME_ROOT + hook: exit 0" 0 "$DRV_RC"
t_eq "D19 --local-test run: 10 submissions" 10 "$(t_nsub)"
grep -q 'PILOT_SKIP_MODULES' "$LOGR/launch/main/effective_env.txt" 2>/dev/null; t_cond "D20 the hook is recorded in effective_env.txt" $?
DRV_ENV=()

# ===================================================== D. later waves ==========================================================================
t_reset_run; mk_main_state; t_mk_unitlist "$RUNH/resubmit/smc_r1.tsv" smc 30
t_run_driver r1 --wave r1 --profile alone --pieces smc
t_eq "D21 wave r1 (smc, 30 units = 2 tasks): exit 0" 0 "$DRV_RC"
t_eq "D22 wave r1: 5 submissions (truth test, lock, array, unlock, collect)" 5 "$(t_nsub)"
t_vec "D23 wave r1" --kind r --profile alone --pieces smc --tasks smc=2 --id-base 7000
[ -d "$LOGR/launch/r1" ] && [ -d "$LOGR/launch/main" ]; t_cond "D24 launch/r1 created and launch/main untouched" $?
t_eq "D25 JOBIDS.tsv: earlier main rows kept (appended, not overwritten)" 3 "$(awk -F'\t' 'NR>1 && $1=="main"' "$RUNH/JOBIDS.tsv" | wc -l | tr -d ' ')"
t_eq "D26 JOBIDS.tsv: 5 rows with wave r1" 5 "$(awk -F'\t' 'NR>1 && $1=="r1"' "$RUNH/JOBIDS.tsv" | wc -l | tr -d ' ')"
t_eq "D27 jobids.tsv (LOG_RUN): 5 rows with wave r1" 5 "$(awk -F'\t' 'NR>1 && $1=="r1"' "$LOGR/jobids.tsv" | wc -l | tr -d ' ')"
grep -qx 5 "$T_STUB/guard_calls.txt"; t_cond "D28 guard asked for PLANNED_HOME_MB=5 for a non-main wave" $?

t_reset_run; mk_main_state; t_mk_unitlist "$RUNH/resubmit/smc_r2.tsv" smc 30; t_mk_unitlist "$RUNH/resubmit/smcrep_r2.tsv" smcrep 10
t_run_driver r2 --wave r2 --profile withH --pieces smc,smcrep
t_eq "D29 wave r2 (smc + smcrep): exit 0" 0 "$DRV_RC"; t_eq "D30 wave r2: 6 submissions" 6 "$(t_nsub)"
t_vec "D31 wave r2 withH (smcrep afterany smc)" --kind r --profile withH --pieces smc,smcrep --tasks smc=2,smcrep=1

t_reset_run; mk_main_state
t_run_driver r1missing --wave r1 --profile alone --pieces smc
[ "$DRV_RC" != 0 ]; t_cond "D32 wave r1 without RUN_HOME/resubmit/smc_r1.tsv: refused (exit $DRV_RC)" $?
no_hits; t_cond "D33 wave r1 without its list: nothing submitted" $?

# P5 wave
for cfg in "alone 3" "alone 20" "withH 20"; do
  set -- $cfg; prof=$1; n=$2
  t_reset_run; mk_main_state; mk_p5 "$n" p5
  t_run_driver p5_${prof}_$n --wave p5 --profile $prof
  t_eq "D34 wave p5 ($n units, $prof): exit 0" 0 "$DRV_RC"
  t_vec "D35 wave p5 ($n units, $prof)" --kind p5 --profile $prof --p5-n "$n"
done
t_reset_run; mk_main_state; mk_p5 4 p5; cp "$RUNH/p5/units_p5.tsv" "$RUNH/p5/units_p5r1.tsv"
t_run_driver p5r1 --wave p5r1 --profile withH
t_eq "D34b wave p5r1 (second P5 wave, 4 units, withH): exit 0" 0 "$DRV_RC"
t_vec "D35b wave p5r1 (4 units, withH)" --kind p5 --profile withH --p5-n 4
t_reset_run; mk_main_state; t_run_driver p5scan --p5-scan --phase initial --profile alone
t_eq "D36 --p5-scan --phase initial: exit 0" 0 "$DRV_RC"; t_eq "D37 --p5-scan: one submission" 1 "$(t_nsub)"
t_vec "D38 --p5-scan job" --kind p5scan --profile alone
grep -qx 5 "$T_STUB/guard_calls.txt"; t_cond "D39 --p5-scan: guard asked for 5 MB" $?

# ---- HQ D63: the P5 scan time limit scales with the records it reads. The fixed 00:30:00 timed out after the 2,400 smc records and never reached the 12,000 smcrep ones.
#      limit = max(7,200 s, 600 s + ceil(records x 2.0 s)), records = smc + smcrep rows of the staged lists/units.tsv (primaries) + data rows of
#      RUN_HOME/p5/expected.tsv when present (possible P5 retry records; Sol narrow check D63: a final scan reads them too). The staged list is swapped
#      for fake ones (and restored).
cp "$BUN/lists/units.tsv" "$W/units_orig.tsv"
hms2s() { local IFS=:; set -- $1; echo $((10#$1 * 3600 + 10#$2 * 60 + 10#$3)); }
scan_time() { grep -m1 -e '^--time=' "$T_STUB/sbatch_argv.txt" | cut -d= -f2 | tr -d ''; }
nscan_rows() { awk -F'	' 'NR>1 && ($1=="smc" || $1=="smcrep")' "$BUN/lists/units.tsv" | wc -l | tr -d ' '; }
mk_scan_list() {   # mk_scan_list NSMC NSMCREP [NENUM30] : replace the staged lists/units.tsv by a fake list and re-seal STAGED_SHA256.txt
  t_reset_run      # a JOBIDS.tsv left by the previous case must not be sealed into STAGED_SHA256.txt (the next reset would delete it)
  t_mk_unitlist "$W/l_smc.tsv" smc "$1"; t_mk_unitlist "$W/l_rep.tsv" smcrep "$2"; t_mk_unitlist "$W/l_enum.tsv" enum30 "${3:-0}"
  { head -n 1 "$W/l_smc.tsv"; tail -n +2 "$W/l_enum.tsv"; tail -n +2 "$W/l_smc.tsv"; tail -n +2 "$W/l_rep.tsv"; } > "$BUN/lists/units.tsv"
  t_restage
}
scan_case() {   # scan_case ID DESC WANT_HMS [NRETRY [PHASE]] : run --p5-scan on the list in place (NRETRY = rows of an expected.tsv written first; "-" = none)
  local id=$1 desc=$2 want=$3 nr=${4:--} ph=${5:-initial} np n lim
  np=$(nscan_rows)
  t_reset_run; mk_main_state
  if [ "$nr" != - ]; then mkdir -p "$RUNH/p5"; t_mk_unitlist "$RUNH/p5/expected.tsv" p5 "$nr"; else rm -f "$RUNH/p5/expected.tsv"; nr=0; fi
  n=$((np + nr))
  t_run_driver "scan_$id" --p5-scan --phase "$ph" --profile alone
  t_eq "$id $desc: exit 0, one submission" "0/1" "$DRV_RC/$(t_nsub)"
  lim=$(scan_time)
  t_eq "$id $desc ($np primaries + $nr possible retries): the scan vector carries --time=$want" "$want" "$lim"
  grep -q "P5 scan: $n records ($np primaries + $nr possible retries) -> time limit $want" "$DRV_LOG"; t_cond "$id the driver prints 'P5 scan: $n records ($np primaries + $nr possible retries) -> time limit $want'" $?
  [ -n "$lim" ] && [ "$(hms2s "$lim")" -ge $(( (3 * n + 1) / 2 )) ]; t_cond "$id the limit is >= 2 x the observed 0.75 s per record x $n records read ($(( (3 * n + 1) / 2 )) s)" $?
}
t_eq "D40 the staged real list has 14,400 smc + smcrep records (2,400 + 12,000)" 14400 "$(nscan_rows)"
scan_case D40 "real list, initial scan (no expected inventory)" 08:10:00
[ "$(scan_time)" != 00:30:00 ] && [ "$(hms2s "$(scan_time)")" -gt 1800 ]; t_cond "D40 the real-list scan is never 00:30:00 (and exceeds the old 1,800 s)" $?
t_vec "D40 real list" --kind p5scan --profile alone
[ 1800 -lt $(( 14400 * 3 / 4 )) ] && [ "$(hms2s 08:10:00)" -ge $(( 2 * 14400 * 3 / 4 )) ]; t_cond "D46 reproduction: the old 1,800 s is below 0.75 s x 14,400 = 10,800 s; the new 29,400 s is >= 2 x that" $?
scan_case D49 "real list, final scan, header-only expected.tsv (no eligible retry)" 08:10:00 0 final
scan_case D50 "real list, final scan, 100 expected retries (+200 s)" 08:13:20 100 final
scan_case D51 "real list, heavily retried final scan: one retry per primary (28,800 records)" 16:10:00 14400 final
[ "$(hms2s 16:10:00)" -ge $(( 2 * 28800 * 3 / 4 )) ] && [ "$(hms2s 08:10:00)" -lt $(( 2 * 28800 * 3 / 4 )) ]; t_cond "D52 Sol D63 residual reproduced: the primaries-only 08:10:00 is below 2 x 0.75 s x 28,800 = 43,200 s; the retry-aware 58,200 s is not" $?
mk_scan_list 2000 8000;  scan_case D41 "10,000 smc+smcrep records (600 + 20,000 s)" 05:43:20
mk_scan_list 40 60;      scan_case D42 "100 records: the 7,200 s floor" 02:00:00
mk_scan_list 1650 1650;  scan_case D43 "3,300 records: 600 + 6,600 = 7,200 s, exactly the floor" 02:00:00
mk_scan_list 1651 1650;  scan_case D44 "3,301 records: 600 + 6,602 = 7,202 s" 02:00:02
mk_scan_list 1650 1650;  scan_case D53 "3,300 primaries + 1 expected retry: 7,202 s (retries count toward the floor)" 02:00:02 1 final
mk_scan_list 100 0 5000; scan_case D45 "100 smc + 5,000 enum30 rows: only smc + smcrep records count" 02:00:00
mk_scan_list 1 0;        scan_case D47 "1 record: the floor" 02:00:00
t_reset_run; rm -f "$RUNH/p5/expected.tsv"; cp "$W/units_orig.tsv" "$BUN/lists/units.tsv"; t_restage
t_eq "D48 (cleanup) the real staged list is back in place" 14400 "$(nscan_rows)"

# ===================================================== E. NEGATIVE CONTROLS: each refuses and submits nothing ==========================
for v in PILOT_DRYRUN PILOT_SKIP_MODULES PILOT_TIME_BIN PRODL_UNIT_CMD PRODL_TEST_WALL_S PRODL_TEST_BUDGET_S PRODL_TEST_NOW_OFFSET_S; do
  t_reset_run; DRV_ENV=("$v=1"); t_run_driver hook_$v --wave main --profile alone
  t_eq "N01 hook $v set without --local-test: exit 2" 2 "$DRV_RC"
  t_no_submission; t_cond "N01 hook $v: nothing submitted, nothing created" $?
done
t_reset_run; DRV_ENV=(PILOT_LOCAL_TEST=1); t_run_driver lt_env_only --wave main --profile alone
t_eq "N02 PILOT_LOCAL_TEST=1 without --local-test: exit 2" 2 "$DRV_RC"; t_no_submission; t_cond "N02 nothing submitted" $?
t_reset_run; DRV_ENV=(); DRV_UNSET=(PILOT_LOCAL_TEST); t_run_driver lt_flag_only --wave main --profile alone --local-test
t_eq "N03 --local-test without PILOT_LOCAL_TEST=1: exit 2" 2 "$DRV_RC"; t_no_submission; t_cond "N03 nothing submitted" $?
t_reset_run; DRV_ENV=(PILOT_LOCAL_TEST=1); DRV_UNSET=(NC_HOME_ROOT); t_run_driver lt_noroot --wave main --profile alone --local-test
t_eq "N04 --local-test without a fake NC_HOME_ROOT: exit 2" 2 "$DRV_RC"; no_hits; t_cond "N04 nothing submitted" $?
DRV_ENV=(); DRV_UNSET=()

t_reset_run; t_run_driver bench_wave --wave bench --profile alone
t_eq "N05 --wave bench: exit 2" 2 "$DRV_RC"; t_no_submission; t_cond "N05 --wave bench: nothing submitted" $?
grep -q 'BENCH-FIX' "$DRV_LOG"; t_cond "N05 --wave bench: message names the gate (BENCH-FIX + Sol ACCEPT)" $?
t_reset_run; t_run_driver bench_pieces --wave main --profile alone --pieces bench
t_eq "N06 --pieces bench: exit 2" 2 "$DRV_RC"; t_no_submission; t_cond "N06 --pieces bench: nothing submitted" $?
t_reset_run; t_run_driver bench_mixed --wave main --profile alone --pieces smc,bench
t_eq "N07 --pieces smc,bench: exit 2" 2 "$DRV_RC"; t_no_submission; t_cond "N07 --pieces smc,bench: nothing submitted" $?

t_reset_run; t_lock_truth_sim; lockmode=$T_LOCK_MODE
t_run_driver locked --wave main --profile alone
t_eq "N08 truth trees locked (mode 000, $lockmode) at submission: exit 2" 2 "$DRV_RC"
t_no_submission; t_cond "N08 locked truth: nothing submitted, nothing created" $?
guard_called; [ $? -ne 0 ]; t_cond "N09 locked truth: the guard is NOT called" $?
grep -qi 'locked' "$DRV_LOG"; t_cond "N10 locked truth: message says a wave is locked" $?
t_unlock_truth_sim
t_reset_run; mk_main_state; t_mk_unitlist "$RUNH/resubmit/smc_r1.tsv" smc 30; t_lock_truth_sim
t_run_driver locked_r1 --wave r1 --profile alone --pieces smc
t_eq "N11 later wave while truth is locked: exit 2" 2 "$DRV_RC"; no_hits; t_cond "N11 nothing submitted" $?
t_unlock_truth_sim

t_reset_run; DRV_ENV=(FAKE_HOME_GB=9.6); t_run_driver guard_refuses --wave main --profile alone
t_eq "N12 guard refuses the planned add: exit 1" 1 "$DRV_RC"; t_no_submission; t_cond "N12 guard refusal: nothing submitted, nothing created" $?
DRV_ENV=()
t_reset_run; DRV_ENV=(FAKE_CAMP_KB=520000); t_run_driver guard_camp --wave main --profile alone
t_eq "N13 guard refuses for the campaign limit: exit 1" 1 "$DRV_RC"; t_no_submission; t_cond "N13 nothing submitted" $?
DRV_ENV=()

# frozen tree altered / staged hash mismatch
V="$RUNH/code/core/v2_2_1"; cp "$V/study/run_case.R" "$W/run_case.bak"
t_reset_run; echo tampered >> "$V/study/run_case.R"; t_restage; t_run_driver frozen1 --wave main --profile alone
t_eq "N14 frozen v2.2.1 file modified (staged list regenerated): exit 2" 2 "$DRV_RC"; no_hits; t_cond "N14 nothing submitted" $?
cp "$W/run_case.bak" "$V/study/run_case.R"
t_reset_run; echo extra > "$V/study/adapter_lowp.R"; t_restage; t_run_driver frozen2 --wave main --profile alone
t_eq "N15 unlisted file in the frozen tree: exit 2" 2 "$DRV_RC"; no_hits; t_cond "N15 nothing submitted" $?
rm -f "$V/study/adapter_lowp.R"; t_restage
t_reset_run; cp "$RUNH/code/lowp/R/lowp_verify_nots.R" "$W/verify.bak"; echo tampered >> "$RUNH/code/lowp/R/lowp_verify_nots.R"
t_run_driver staged_mismatch --wave main --profile alone
t_eq "N16 STAGED_SHA256.txt mismatch (a staged file altered): exit 2" 2 "$DRV_RC"; no_hits; t_cond "N16 nothing submitted" $?
cp "$W/verify.bak" "$RUNH/code/lowp/R/lowp_verify_nots.R"
t_reset_run; echo tampered >> "$BUN/lists/units.tsv"; t_run_driver staged_mismatch2 --wave main --profile alone
t_eq "N17 staged bundle list file altered: exit 2" 2 "$DRV_RC"; no_hits; t_cond "N17 nothing submitted" $?
cp "${PRODL_B_SRC:-$B}/lists/units.tsv" "$BUN/lists/units.tsv"; t_restage

# existing launch folder
t_reset_run; mkdir -p "$LOGR/launch/main"; t_run_driver existing --wave main --profile alone
t_eq "N18 launch/main already exists: exit 2" 2 "$DRV_RC"; no_hits; t_cond "N18 nothing submitted" $?

# later wave while a job of the run is still queued or running
t_reset_run; mk_main_state; t_mk_unitlist "$RUNH/resubmit/smc_r1.tsv" smc 30
echo '6007_5|lowpL_s2_smc|RUNNING|2' > "$T_STUB/squeue.txt"; t_run_driver active_run --wave r1 --profile alone --pieces smc
t_eq "N19 wave r1 while a run job is RUNNING in squeue: exit 2" 2 "$DRV_RC"; no_hits; t_cond "N19 nothing submitted" $?
t_reset_run; mk_main_state; t_mk_unitlist "$RUNH/resubmit/smc_r1.tsv" smc 30
echo '6010|lowpL_s9_collect|PENDING|2' > "$T_STUB/squeue.txt"; t_run_driver active_pend --wave r1 --profile alone --pieces smc
t_eq "N20 wave r1 while a run job is PENDING in squeue: exit 2" 2 "$DRV_RC"; no_hits; t_cond "N20 nothing submitted" $?
t_reset_run; mk_main_state; t_mk_unitlist "$RUNH/resubmit/smc_r1.tsv" smc 30
echo '6007_[10-95%32]|lowpL_s2_smc|PENDING|2' > "$T_STUB/squeue.txt"; t_run_driver active_arr --wave r1 --profile alone --pieces smc
t_eq "N21 wave r1 while a pending ARRAY of the run is in squeue: exit 2" 2 "$DRV_RC"; no_hits; t_cond "N21 nothing submitted" $?
t_reset_run; mk_main_state; mk_p5 3 p5
echo '6007_5|lowpL_s2_smc|RUNNING|2' > "$T_STUB/squeue.txt"; t_run_driver active_p5 --wave p5 --profile alone
t_eq "N22 wave p5 while a run job is active: exit 2" 2 "$DRV_RC"; no_hits; t_cond "N22 nothing submitted" $?

# scheduler failure: fail closed
t_reset_run; touch "$T_STUB/squeue_fail"; t_run_driver squeue_fail_main --wave main --profile alone
[ "$DRV_RC" != 0 ] && [ "$DRV_RC" != 5 ]; t_cond "N23 squeue failing, main wave: refused before any submission (exit $DRV_RC)" $?
no_hits; t_cond "N23 nothing submitted" $?; [ ! -e "$LOGR/launch" ]; t_cond "N23 no launch record created" $?
t_reset_run; mk_main_state; t_mk_unitlist "$RUNH/resubmit/smc_r1.tsv" smc 30; touch "$T_STUB/squeue_fail"; t_run_driver squeue_fail_r1 --wave r1 --profile alone --pieces smc
[ "$DRV_RC" != 0 ] && [ "$DRV_RC" != 5 ]; t_cond "N24 squeue failing, later wave: refused (exit $DRV_RC)" $?
no_hits; t_cond "N24 nothing submitted" $?

# CPU ceiling refusals
t_reset_run; echo '9001|bvs_prodH_s2|RUNNING|2' > "$T_STUB/squeue.txt"; t_run_driver ceil_alone_prodH --wave main --profile alone
t_eq "N25 ceiling: profile alone with a _prodH job present: exit 2" 2 "$DRV_RC"; t_no_submission; t_cond "N25 nothing submitted, nothing created" $?
t_reset_run; printf '9001_[1-600%%50]|bvs_prodH_s2|PENDING|1\n9002_[601-1200%%50]|bvs_prodH_s2|PENDING|1\n' > "$T_STUB/squeue.txt"
t_run_driver ceil_withH_200 --wave main --profile withH
t_eq "N26 ceiling: PROD-H arrays 2 x (50 x 2 CPUs billed) = 200 > 192 (withH): exit 2" 2 "$DRV_RC"; t_no_submission; t_cond "N26 nothing submitted" $?
t_reset_run; printf '9001_[1-600%%31]|bvs_prodH_s2|PENDING|1\n9002_[601-1200%%31]|bvs_prodH_s2|PENDING|1\n' > "$T_STUB/squeue.txt"
t_run_driver ceil_withH_124 --wave main --profile withH
t_eq "N27 (control) ceiling: PROD-H 124 billed + PROD-L 68 = 192 is ADMITTED (withH)" 0 "$DRV_RC"; t_eq "N27 (control) 10 submissions" 10 "$(t_nsub)"
t_reset_run; printf 'this is not a squeue row\n' > "$T_STUB/squeue.txt"; t_run_driver ceil_garbage --wave main --profile alone
t_eq "N28 ceiling: an unparsable squeue row: refused (exit 2)" 2 "$DRV_RC"; no_hits; t_cond "N28 nothing submitted" $?

# sbatch failure at call k: abort, cancel earlier ids by explicit id, SUBMISSION_ABORTED.txt, exit 5
for k in 1 2 6 10; do
  t_reset_run; DRV_ENV=("FAIL_AT=$k"); t_run_driver fail_$k --wave main --profile alone
  t_eq "N29 sbatch rejected at call $k: exit 5" 5 "$DRV_RC"
  t_eq "N29 call $k: sbatch attempts stop at the failure" "$k" "$(t_nsub)"
  af=$(aborted_file); [ -n "$af" ] && [ -s "$af" ]; t_cond "N29 call $k: SUBMISSION_ABORTED.txt written" $?
  want=""; i=1; while [ $i -lt "$k" ]; do want="$want$((7000 + i)) "; i=$((i + 1)); done
  got=$(cat "$T_STUB/scancel_calls.txt" 2>/dev/null | tr -s ' \n' '\n\n' | grep -v '^$' | sort -n | tr '\n' ' ')
  t_eq "N29 call $k: ids submitted before the failure cancelled by explicit id" "$want" "$got"
  [ -z "$got" ] || ! grep -qE -- '(^| )-(-user|u|n|-name|-me)' "$T_STUB/scancel_calls.txt" 2>/dev/null; t_cond "N29 call $k: scancel is never called with a selector (user/name)" $?
  t_eq "N29 call $k: no malformed id in jobids.tsv" 0 "$(awk -F'\t' 'NR>1 && $3 !~ /^[0-9]+$/' "$LOGR/jobids.tsv" 2>/dev/null | wc -l | tr -d ' ')"
done
DRV_ENV=()
t_reset_run; DRV_ENV=("BAD_ID_AT=3"); t_run_driver badid --wave main --profile alone
t_eq "N30 sbatch answers with an unparsable id at call 3: exit 5" 5 "$DRV_RC"; t_eq "N30 attempts stop at 3" 3 "$(t_nsub)"
t_eq "N30 the two valid ids are cancelled" "7001 7002 " "$(cat "$T_STUB/scancel_calls.txt" 2>/dev/null | tr -s ' \n' '\n\n' | grep -v '^$' | sort -n | tr '\n' ' ')"
DRV_ENV=()

# CLOSED pieces (make_manifests.sh closed them): resubmission and P5 are refused (DESIGN section 8)
mk_closed() { mkdir -p "$RUNH/manifests"; echo "closed by test" > "$RUNH/manifests/$1.CLOSED"; }
t_reset_run; mk_main_state; t_mk_unitlist "$RUNH/resubmit/smc_r1.tsv" smc 30; mk_closed smc
t_run_driver closed_smc --wave r1 --profile alone --pieces smc
[ "$DRV_RC" != 0 ]; t_cond "N31 --wave r1 --pieces smc with smc CLOSED: refused (exit $DRV_RC)" $?; no_hits; t_cond "N31 nothing submitted" $?
grep -q 'CLOSED' "$DRV_LOG"; t_cond "N31 the message says CLOSED" $?
t_reset_run; mk_main_state; t_mk_unitlist "$RUNH/resubmit/smc_r1.tsv" smc 30; t_mk_unitlist "$RUNH/resubmit/enum20_r1.tsv" enum20 3; mk_closed enum20
t_run_driver closed_mixed --wave r1 --profile alone --pieces enum20,smc
[ "$DRV_RC" != 0 ]; t_cond "N32 --wave r1 --pieces enum20,smc with enum20 CLOSED: refused (exit $DRV_RC)" $?; no_hits; t_cond "N32 nothing submitted (all-or-nothing)" $?
t_reset_run; mk_main_state; t_mk_unitlist "$RUNH/resubmit/smc_r1.tsv" smc 30; mk_closed smcrep
t_run_driver open_other --wave r1 --profile alone --pieces smc
t_eq "N33 (control) smc is open while only smcrep is CLOSED: wave r1 --pieces smc is submitted (exit 0)" 0 "$DRV_RC"
t_reset_run; mk_main_state; mk_closed smc
t_run_driver closed_scan --p5-scan --phase initial --profile alone
[ "$DRV_RC" != 0 ]; t_cond "N34 --p5-scan with smc CLOSED: refused (exit $DRV_RC)" $?; no_hits; t_cond "N34 nothing submitted" $?
t_reset_run; mk_main_state; mk_closed smcrep
t_run_driver closed_scan2 --p5-scan --phase initial --profile alone
[ "$DRV_RC" != 0 ]; t_cond "N35 --p5-scan with smcrep CLOSED: refused (exit $DRV_RC)" $?; no_hits; t_cond "N35 nothing submitted" $?
t_reset_run; mk_main_state; mk_p5 3 p5; mk_closed smc
t_run_driver closed_p5 --wave p5 --profile alone
[ "$DRV_RC" != 0 ]; t_cond "N36 --wave p5 with smc CLOSED: refused (exit $DRV_RC)" $?; no_hits; t_cond "N36 nothing submitted" $?
t_reset_run; mk_main_state; mk_p5 3 p5; mk_closed smcrep
t_run_driver closed_p5b --wave p5 --profile alone
[ "$DRV_RC" != 0 ]; t_cond "N37 --wave p5 with smcrep CLOSED: refused (exit $DRV_RC)" $?; no_hits; t_cond "N37 nothing submitted" $?
rm -rf "$RUNH/manifests"

# restore the fixture to an open, clean state
t_unlock_truth_sim
t_summary
