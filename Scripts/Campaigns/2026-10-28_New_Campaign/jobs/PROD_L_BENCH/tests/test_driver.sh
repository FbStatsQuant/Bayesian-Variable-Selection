#!/bin/bash
# test_driver.sh -- acceptance tests of submit_bench.sh (PROD_L_BENCH DESIGN.md sections 1, 4): recorded sbatch vectors for both profiles, launch record, job-id files,
# later waves (bench / benchretry lists), and the negative controls (each must refuse with the stated exit status and submit NOTHING).
#   bash test_driver.sh WORKDIR        (WORKDIR under C:/Users/felip/AppData/Local/Temp/prodl_tests/)
# Main wave = 3 vectors: lowpB_s0_verify, lowpB_s1_bench (array 0-95%32 alone / %16 withH, afterok verify), lowpB_s9_collect (afterany). NO lock / unlock steps. Every vector --no-requeue.
source "$(dirname "$0")/lib.sh"
t_init "${1:-}" test_driver
SRCB=${PRODL_B_SRC:-$B}
[ -f "$SRCB/submit_bench.sh" ]; t_cond "D00 submit_bench.sh exists in the bundle" $?
echo "== building the fake NOTS tree (1,200 dummy inputs, NO truth) =="
t_mkfix "$W/fx" 20261030T1200Z

mk_main_state() {   # what exists after a finished main wave
  mkdir -p "$LOGR/launch/main"
  printf 'wave\tstep\tjobid\tarray\tdependency\nmain\ts0_verify\t6001\t-\t-\nmain\ts1_bench\t6002\t0-95%%32\tafterok:6001\nmain\ts9_collect\t6003\t-\tafterany:6001:6002\n' > "$RUNH/JOBIDS.tsv"
  cp "$RUNH/JOBIDS.tsv" "$LOGR/jobids.tsv"
}
no_hits() { [ ! -s "$T_STUB/sbatch_calls.txt" ]; }
aborted_file() { find "$LOGR" -name SUBMISSION_ABORTED.txt 2>/dev/null | head -n 1; }
guard_called() { [ -s "$T_STUB/guard_calls.txt" ]; }

check_launch() {   # check_launch WAVE NSUB PLANNED_MB
  local wave=$1 n=$2 mb=$3 L="$LOGR/launch/$1" f c g sv
  [ -d "$L" ]; t_cond "launch/$wave folder exists in LOG_RUN" $?
  for f in bench.env bench.env.sha256 STAGED_SHA256.txt OWNER effective_env.txt; do [ -s "$L/$f" ]; t_cond "launch/$wave/$f present" $?; done
  sv=$(ls "$L" 2>/dev/null | grep -E '^sbatch_args' | head -n 1); [ -n "$sv" ] && [ -s "$L/$sv" ]; t_cond "launch/$wave/sbatch_args* present" $?
  ( cd "$L" 2>/dev/null && sha256sum -c bench.env.sha256 >/dev/null 2>&1 ); t_cond "launch/$wave/bench.env.sha256 verifies bench.env" $?
  ls "$L" 2>/dev/null | grep -qi 'bench_lowp'; t_cond "launch/$wave holds the frozen manifest (bench_lowp.SHA256SUMS)" $?
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
  t_cond "D01b main/$prof: effective_env.txt lists only the named variables (a dummy SECRET_TOKEN_TEST is absent)" $?
  t_eq "D02 main/$prof: exactly 3 submissions (verify, bench, collect)" 3 "$(t_nsub)"
  t_vec "D03 main/$prof" --kind main --profile $prof --logrun "$(t_win "$LOGR")"
  check_launch main 3 5       # D57: PLANNED_HOME_MB_MAIN = growth AFTER extraction (the 75 MB stage is reserved by OPS before staging)
  grep -q -e 'truthlock' -e 's0_lock' -e 's8_unlock' "$T_STUB/sbatch_argv.txt"; [ $? -ne 0 ]; t_cond "D04 main/$prof: no truth-lock / lock / unlock step is submitted" $?
done

# ===================================================== B. dry run, --local-test ===============================================================
t_reset_run; DRV_ENV=(); t_run_driver dry --wave main --profile alone --dry-run
t_eq "D10 dry run: exit 0" 0 "$DRV_RC"; no_hits; t_cond "D11 dry run: sbatch is never called" $?
[ ! -e "$LOGR/launch" ] && [ ! -e "$RUNH/JOBIDS.tsv" ]; t_cond "D12 dry run: no launch record and no JOBIDS.tsv created" $?
grep -q '0-95%32' "$DRV_LOG"; t_cond "D13 dry run prints the throttled array 0-95%32" $?
t_eq "D14 dry run prints 3 vectors" 3 "$(grep -c 'sbatch' "$DRV_LOG" | tr -d ' ')"
t_reset_run; DRV_ENV=(PILOT_LOCAL_TEST=1 PILOT_SKIP_MODULES=1); t_run_driver localtest --wave main --profile alone --local-test
t_eq "D15 --local-test + PILOT_LOCAL_TEST=1 + fake NC_HOME_ROOT + hook: exit 0, 3 submissions" "0 3" "$DRV_RC $(t_nsub)"
grep -q 'PILOT_SKIP_MODULES' "$LOGR/launch/main/effective_env.txt" 2>/dev/null; t_cond "D16 the hook is recorded in effective_env.txt" $?
DRV_ENV=()

# ===================================================== C. later waves: bench and benchretry lists =============================================
t_reset_run; mk_main_state; t_mk_unitlist "$RUNH/resubmit/bench_r1.tsv" bench 30
t_run_driver r1 --wave r1 --profile alone --pieces bench
t_eq "D20 wave r1 (bench list of 30 cases = 2 tasks): exit 0, 2 submissions (array + collect)" "0 2" "$DRV_RC $(t_nsub)"
t_vec "D21 wave r1" --kind r --profile alone --pieces bench --tasks bench=2
[ -d "$LOGR/launch/r1" ] && [ -d "$LOGR/launch/main" ]; t_cond "D22 launch/r1 created, launch/main untouched" $?
t_eq "D23 JOBIDS.tsv: main rows kept, 2 rows wave r1" "3 2" "$(awk -F'\t' 'NR>1 && $1=="main"' "$RUNH/JOBIDS.tsv" | wc -l | tr -d ' ') $(awk -F'\t' 'NR>1 && $1=="r1"' "$RUNH/JOBIDS.tsv" | wc -l | tr -d ' ')"
grep -qx 5 "$T_STUB/guard_calls.txt"; t_cond "D24 guard asked for PLANNED_HOME_MB=5 for a non-main wave" $?
t_reset_run; mk_main_state; t_mk_unitlist "$RUNH/resubmit/bench_r2.tsv" bench 30; t_mk_unitlist "$RUNH/resubmit/benchretry_r2.tsv" benchretry 4
t_run_driver r2 --wave r2 --profile withH --pieces bench,benchretry
t_eq "D25 wave r2 (bench + benchretry lists): exit 0, 3 submissions" "0 3" "$DRV_RC $(t_nsub)"
t_vec "D26 wave r2 withH" --kind r --profile withH --pieces bench,benchretry --tasks bench=2,benchretry=1
t_reset_run; mk_main_state; t_mk_unitlist "$RUNH/resubmit/benchretry_r3.tsv" benchretry 3
t_run_driver r3 --wave r3 --profile alone --pieces benchretry
t_eq "D27 wave r3 with a benchretry list only: exit 0, 2 submissions" "0 2" "$DRV_RC $(t_nsub)"
grep -q 'lowpB_s2_benchretry' "$T_STUB/sbatch_argv.txt"; t_cond "D28 ... the array is lowpB_s2_benchretry" $?
t_reset_run; mk_main_state; t_run_driver r1missing --wave r1 --profile alone --pieces bench
[ "$DRV_RC" != 0 ]; t_cond "D29 wave r1 without RUN_HOME/resubmit/bench_r1.tsv: refused (exit $DRV_RC)" $?; no_hits; t_cond "D29b nothing submitted" $?

# ===================================================== D. NEGATIVE CONTROLS ====================================================================
for v in PILOT_DRYRUN PILOT_SKIP_MODULES PILOT_TIME_BIN PRODL_UNIT_CMD PRODL_TEST_WALL_S PRODL_TEST_BUDGET_S PRODL_TEST_NOW_OFFSET_S; do
  t_reset_run; DRV_ENV=("$v=1"); t_run_driver hook_$v --wave main --profile alone
  t_eq "N01 hook $v set without --local-test: exit 2" 2 "$DRV_RC"; t_no_submission; t_cond "N01 hook $v: nothing submitted, nothing created" $?
done
t_reset_run; DRV_ENV=(PILOT_LOCAL_TEST=1); t_run_driver lt_env_only --wave main --profile alone
t_eq "N02 PILOT_LOCAL_TEST=1 without --local-test: exit 2" 2 "$DRV_RC"; t_no_submission; t_cond "N02 nothing submitted" $?
t_reset_run; DRV_ENV=(); DRV_UNSET=(PILOT_LOCAL_TEST); t_run_driver lt_flag_only --wave main --profile alone --local-test
t_eq "N03 --local-test without PILOT_LOCAL_TEST=1: exit 2" 2 "$DRV_RC"; t_no_submission; t_cond "N03 nothing submitted" $?
t_reset_run; DRV_ENV=(PILOT_LOCAL_TEST=1); DRV_UNSET=(NC_HOME_ROOT); t_run_driver lt_noroot --wave main --profile alone --local-test
t_eq "N04 --local-test without a fake NC_HOME_ROOT: exit 2" 2 "$DRV_RC"; no_hits; t_cond "N04 nothing submitted" $?
DRV_ENV=(); DRV_UNSET=()

# --- no truth on NOTS: any path component named truth / holdout (case-insensitive) under the run folder
for nm in truth Truth HOLDOUT holdout; do
  t_reset_run; mkdir -p "$ST/$nm"; t_run_driver notruth_$nm --wave main --profile alone
  t_eq "N10 a directory named '$nm' under the run folder: exit 2" 2 "$DRV_RC"; no_hits; t_cond "N10 nothing submitted ($nm)" $?
  [ ! -e "$LOGR/launch" ]; t_cond "N10 no launch record ($nm)" $?
  rm -rf "$ST/$nm"
done
t_reset_run; mkdir -p "$ST/inputs/p0020/dev/Truth"; t_run_driver notruth_deep --wave main --profile alone
t_eq "N11 a nested component named Truth deep in the study: exit 2" 2 "$DRV_RC"; no_hits; t_cond "N11 nothing submitted" $?
rm -rf "$ST/inputs/p0020/dev"
t_reset_run; : > "$RUNH/code/truth"; t_run_driver notruth_file --wave main --profile alone
t_eq "N12 a FILE named truth under the run folder: exit 2" 2 "$DRV_RC"; no_hits; t_cond "N12 nothing submitted" $?
rm -f "$RUNH/code/truth"
t_reset_run; : > "$ST/manifests/truth_manifest_lowp.csv"; t_run_driver notruth_manifest --wave main --profile alone
[ "$DRV_RC" = 0 ] || [ "$DRV_RC" = 2 ]; t_cond "N13 (informational) a truth_manifest_lowp.csv does not contain a component named exactly truth (exit $DRV_RC)" $?
rm -f "$ST/manifests/truth_manifest_lowp.csv"

# --- PROD-L fitting jobs queued / running: serialised after the SMC lane (D56)
for row in '7002_5|lowpL_s2_smc|RUNNING|2' '7003_[10-95%32]|lowpL_s3_smcrep|PENDING|1' '7001|lowpL_s1_enum20|RUNNING|4' '7005_0|lowpL_s1_enum30|RUNNING|16' '7010_2|lowpL_s4_p5|PENDING|1'; do
  t_reset_run; echo "$row" > "$T_STUB/squeue.txt"; t_run_driver prodl_active --wave main --profile alone
  t_eq "N20 a PROD-L fitting job in squeue ($row): exit 2" 2 "$DRV_RC"; t_no_submission; t_cond "N20 nothing submitted" $?
done
for row in '7000|lowpL_s0_build|RUNNING|2' '7020|lowpL_s9_collect|PENDING|1' '7021|lowpL_s8_unlock|RUNNING|1' '7030|lowpL_s5_p5scan|RUNNING|1'; do
  t_reset_run; echo "$row" > "$T_STUB/squeue.txt"; t_run_driver prodl_nonfit --wave main --profile alone
  t_eq "N21 (control) a PROD-L NON-fitting job ($row) does not block: exit 0" 0 "$DRV_RC"
done
t_reset_run; echo '7002_5|lowpL_s2_smc|RUNNING|2' > "$T_STUB/squeue.txt"; t_run_driver allow_conc --wave main --profile alone --allow-concurrent-prodl
t_eq "N22 --allow-concurrent-prodl (HQ only) with a PROD-L fitting job running: exit 0" 0 "$DRV_RC"
grep -rqi 'allow.concurrent' "$LOGR/launch/main" 2>/dev/null; t_cond "N23 ... the override is recorded in the launch record" $?
t_reset_run; mk_main_state; t_mk_unitlist "$RUNH/resubmit/bench_r1.tsv" bench 30; echo '7002_5|lowpL_s2_smc|RUNNING|2' > "$T_STUB/squeue.txt"
t_run_driver prodl_active_r1 --wave r1 --profile alone --pieces bench
t_eq "N24 a PROD-L fitting job running also blocks a later wave: exit 2" 2 "$DRV_RC"; no_hits; t_cond "N24 nothing submitted" $?

# --- guard
t_reset_run; DRV_ENV=(FAKE_HOME_GB=9.6); t_run_driver guard_refuses --wave main --profile alone
t_eq "N30 guard refuses the planned add (home): exit 1" 1 "$DRV_RC"; t_no_submission; t_cond "N30 nothing submitted, nothing created" $?
t_reset_run; DRV_ENV=(FAKE_CAMP_KB=520000); t_run_driver guard_camp --wave main --profile alone
t_eq "N31 guard refuses (campaign limit): exit 1" 1 "$DRV_RC"; t_no_submission; t_cond "N31 nothing submitted" $?
DRV_ENV=()

# --- frozen bench_lowp tree and staged hashes
F="$RUNH/code/bench_lowp"; cp "$F/run_bench_case.R" "$W/rbc.bak"
t_reset_run; echo tampered >> "$F/run_bench_case.R"; t_restage; t_run_driver frozen1 --wave main --profile alone
t_eq "N40 frozen bench_lowp file modified (staged list regenerated): exit 2" 2 "$DRV_RC"; no_hits; t_cond "N40 nothing submitted" $?
cp "$W/rbc.bak" "$F/run_bench_case.R"
t_reset_run; echo extra > "$F/R/extra_adapter.R"; t_restage; t_run_driver frozen2 --wave main --profile alone
t_eq "N41 unlisted file in the frozen tree: exit 2" 2 "$DRV_RC"; no_hits; t_cond "N41 nothing submitted" $?
rm -f "$F/R/extra_adapter.R"; t_restage
t_reset_run; mv "$RUNH/code/bench_lowp.SHA256SUMS" "$W/sums.bak"; t_restage; t_run_driver frozen3 --wave main --profile alone
t_eq "N42 frozen manifest bench_lowp.SHA256SUMS missing: exit 2" 2 "$DRV_RC"; no_hits; t_cond "N42 nothing submitted" $?
mv "$W/sums.bak" "$RUNH/code/bench_lowp.SHA256SUMS"; t_restage
t_reset_run; cp "$F/ADAPTATIONS.md" "$W/ad.bak"; echo tampered >> "$F/ADAPTATIONS.md"; t_run_driver staged_mismatch --wave main --profile alone
t_eq "N43 a staged file altered AFTER STAGED_SHA256.txt was written: exit 2" 2 "$DRV_RC"; no_hits; t_cond "N43 nothing submitted" $?
cp "$W/ad.bak" "$F/ADAPTATIONS.md"
t_reset_run; echo tampered >> "$BUN/lists/units.tsv"; t_run_driver staged_mismatch2 --wave main --profile alone
t_eq "N44 the staged lists/units.tsv altered: exit 2" 2 "$DRV_RC"; no_hits; t_cond "N44 nothing submitted" $?
cp "${PRODL_B_SRC:-$B}/lists/units.tsv" "$BUN/lists/units.tsv"; t_restage
t_reset_run; mkdir -p "$LOGR/launch/main"; t_run_driver existing --wave main --profile alone
t_eq "N45 launch/main already exists: exit 2" 2 "$DRV_RC"; no_hits; t_cond "N45 nothing submitted" $?

# --- later wave while a job of THIS run is active; scheduler failure; CLOSED
t_reset_run; mk_main_state; t_mk_unitlist "$RUNH/resubmit/bench_r1.tsv" bench 30
for row in '6002_5|lowpB_s1_bench|RUNNING|2' '6003|lowpB_s9_collect|PENDING|1' '6002_[10-95%32]|lowpB_s1_bench|PENDING|2'; do
  echo "$row" > "$T_STUB/squeue.txt"; t_stub_reset_calls=1; rm -f "$T_STUB/sbatch_calls.txt"; t_run_driver active_run --wave r1 --profile alone --pieces bench
  t_eq "N50 wave r1 while a job of this run is queued/running ($row): exit 2" 2 "$DRV_RC"; no_hits; t_cond "N50 nothing submitted" $?
done
t_reset_run; touch "$T_STUB/squeue_fail"; t_run_driver squeue_fail_main --wave main --profile alone
[ "$DRV_RC" != 0 ] && [ "$DRV_RC" != 5 ]; t_cond "N51 squeue failing, main wave: refused before any submission (exit $DRV_RC)" $?; no_hits; t_cond "N51 nothing submitted" $?
t_reset_run; mk_main_state; t_mk_unitlist "$RUNH/resubmit/bench_r1.tsv" bench 30; touch "$T_STUB/squeue_fail"; t_run_driver squeue_fail_r1 --wave r1 --profile alone --pieces bench
[ "$DRV_RC" != 0 ] && [ "$DRV_RC" != 5 ]; t_cond "N52 squeue failing, later wave: refused (exit $DRV_RC)" $?; no_hits; t_cond "N52 nothing submitted" $?
t_reset_run; mk_main_state; mkdir -p "$RUNH/manifests"; echo closed > "$RUNH/manifests/bench.CLOSED"; t_mk_unitlist "$RUNH/resubmit/bench_r1.tsv" bench 30
t_run_driver closed_bench --wave r1 --profile alone --pieces bench
[ "$DRV_RC" != 0 ]; t_cond "N53 --wave r1 --pieces bench with bench CLOSED: refused (exit $DRV_RC)" $?; no_hits; t_cond "N53 nothing submitted" $?
grep -q 'CLOSED' "$DRV_LOG"; t_cond "N53 the message says CLOSED" $?
rm -rf "$RUNH/manifests"

# --- ceiling
t_reset_run; echo '9001|bvs_prodH_s2|RUNNING|2' > "$T_STUB/squeue.txt"; t_run_driver ceil_alone_prodH --wave main --profile alone
t_eq "N60 ceiling: profile alone with a _prodH job present: exit 2" 2 "$DRV_RC"; t_no_submission; t_cond "N60 nothing submitted, nothing created" $?
t_reset_run; printf '9001_[1-600%%50]|bvs_prodH_s2|PENDING|1\n9002_[601-1200%%50]|bvs_prodH_s2|PENDING|1\n9003_[1-600%%30]|BENCH_F3_x|PENDING|1\n' > "$T_STUB/squeue.txt"
t_run_driver ceil_withH_big --wave main --profile withH
t_eq "N61 ceiling: PROD-H 200 billed + BENCH_F3 60 + bench 32 > 192 (withH): exit 2" 2 "$DRV_RC"; t_no_submission; t_cond "N61 nothing submitted" $?
t_reset_run; printf '9001_[1-600%%31]|bvs_prodH_s2|PENDING|1\n9002_[601-1200%%31]|bvs_prodH_s2|PENDING|1\n' > "$T_STUB/squeue.txt"
t_run_driver ceil_withH_ok --wave main --profile withH
t_eq "N62 (control) PROD-H 124 billed + bench 32 = 156 <= 192 (withH): admitted" "0 3" "$DRV_RC $(t_nsub)"
t_reset_run; for i in $(seq 1 65); do echo "$((9500 + i))|other_job|RUNNING|1"; done > "$T_STUB/squeue.txt"; t_run_driver ceil_alone_other --wave main --profile alone
t_eq "N63 ceiling: others 130 billed + bench 64 = 194 > 192 (alone): exit 2" 2 "$DRV_RC"; t_no_submission; t_cond "N63 nothing submitted" $?
t_reset_run; for i in $(seq 1 64); do echo "$((9500 + i))|other_job|RUNNING|1"; done > "$T_STUB/squeue.txt"; t_run_driver ceil_alone_edge --wave main --profile alone
t_eq "N64 (control) others 128 + bench 64 = 192: admitted" "0 3" "$DRV_RC $(t_nsub)"
t_reset_run; printf 'this is not a squeue row\n' > "$T_STUB/squeue.txt"; t_run_driver ceil_garbage --wave main --profile alone
t_eq "N65 ceiling: an unparsable squeue row: refused (exit 2)" 2 "$DRV_RC"; no_hits; t_cond "N65 nothing submitted" $?

# --- sbatch failure at call k: abort, cancel earlier ids by explicit id, SUBMISSION_ABORTED.txt, exit 5
for k in 1 2 3; do
  t_reset_run; DRV_ENV=("FAIL_AT=$k"); t_run_driver fail_$k --wave main --profile alone
  t_eq "N70 sbatch rejected at call $k: exit 5" 5 "$DRV_RC"
  t_eq "N70 call $k: attempts stop at the failure" "$k" "$(t_nsub)"
  af=$(aborted_file); [ -n "$af" ] && [ -s "$af" ]; t_cond "N70 call $k: SUBMISSION_ABORTED.txt written" $?
  want=""; i=1; while [ $i -lt "$k" ]; do want="$want$((7000 + i)) "; i=$((i + 1)); done
  got=$(cat "$T_STUB/scancel_calls.txt" 2>/dev/null | tr -s ' \n' '\n\n' | grep -v '^$' | sort -n | tr '\n' ' ')
  t_eq "N70 call $k: earlier ids cancelled by explicit id" "$want" "$got"
  [ -z "$got" ] || ! grep -qE -- '(^| )-(-user|u|n|-name|-me)' "$T_STUB/scancel_calls.txt" 2>/dev/null; t_cond "N70 call $k: scancel never uses a selector" $?
  t_eq "N70 call $k: no malformed id in jobids.tsv" 0 "$(awk -F'\t' 'NR>1 && $3 !~ /^[0-9]+$/' "$LOGR/jobids.tsv" 2>/dev/null | wc -l | tr -d ' ')"
done
DRV_ENV=()
t_reset_run; DRV_ENV=("BAD_ID_AT=2"); t_run_driver badid --wave main --profile alone
t_eq "N71 sbatch answers with an unparsable id at call 2: exit 5, attempts stop at 2, id 7001 cancelled" "5 2 7001" "$DRV_RC $(t_nsub) $(tr -s ' \n' '  ' < "$T_STUB/scancel_calls.txt" | sed 's/ *$//')"
DRV_ENV=()
t_reset_run
t_summary
