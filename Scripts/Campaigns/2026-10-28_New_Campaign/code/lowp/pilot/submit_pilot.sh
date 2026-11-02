#!/bin/bash
# submit_pilot.sh -- driver of the LOWP NOTS pilot (OPS runs it through the configured `ssh nots` alias, as fb31, after the bundle is staged and
# pilot.env is filled). One connection at a time; this script itself opens no ssh.
#   STAMP=YYYYMMDDTHHMMZ bash submit_pilot.sh [--dry-run] [--local-test]
# 1. guard_check.sh: the OPS-owned guard.sh must enforce the charter limits (campaign <= 0.5 GiB, home <= 9.6 GiB) and admit the planned add;
#    otherwise REFUSED before anything is created. The receipt goes to LOG/launch/.
# 2. refuses test hooks, empty MODULES, missing/altered staged files (STAGED_SHA256.txt AND the frozen v2.2.1 tree against v2_2_1.SHA256SUMS), wrong counts, an existing log folder.
# 3. records the launch (final pilot.env, hashes, lists, JOB.md, exact sbatch argument vectors, effective environment) in LOG/launch/.
# 4. submits ten steps with dependencies. EVERY sbatch failure aborts: the job ids already submitted are cancelled BY EXPLICIT ID and a
#    SUBMISSION_ABORTED.txt record is written; exit status 5. Job ids are validated (digits) before use.
# Dependencies: build and verify free; truth-lock TEST afterok verify; WAVE LOCK afterok test; every fitting step afterok build+verify+test+lock;
# WAVE UNLOCK finalizer afterany lock+all fits; collect afterany of everything. Output only under scratch (+ a few bytes in RUN_HOME).
set -euo pipefail

HOME_ROOT="${NC_HOME_ROOT:-/home/fb31/projects/BVS/New_Campaign}"
STAMP="${STAMP:-$(date -u +%Y%m%dT%H%MZ)}"
export STAMP
[[ "$STAMP" =~ ^[0-9]{8}T[0-9]{4}Z$ ]] || { echo "REFUSED: STAMP '$STAMP' is not YYYYMMDDTHHMMZ" >&2; exit 2; }
# shellcheck disable=SC1091
source "$HOME_ROOT/runs/${STAMP}_lowp_pilot/code/lowp/pilot/pilot.env"
PLANNED_HOME_MB="${PLANNED_HOME_MB:-$PLANNED_HOME_MB_DEFAULT}"
DRY=0; LOCALTEST=0
for a in "$@"; do case "$a" in --dry-run) DRY=1;; --local-test) LOCALTEST=1;; *) echo "unknown option $a" >&2; exit 2;; esac; done
fail() { echo "REFUSED: $*" >&2; exit 2; }

echo "== LOWP pilot $PILOT_ID (dry-run=$DRY local-test=$LOCALTEST)"
# ---- 0. test hooks never reach a real submission ---------------------------------------------------------------------
HOOKS=(PILOT_DRYRUN PILOT_SKIP_MODULES PILOT_LIMIT PILOT_BENCH_METHODS PILOT_BENCH_EXTRA PILOT_TIME_BIN)
if [ $LOCALTEST = 0 ]; then
  [ "${PILOT_LOCAL_TEST:-0}" != 1 ] || fail "PILOT_LOCAL_TEST=1 is set but --local-test was not given"
  for v in "${HOOKS[@]}"; do [ -z "${!v:-}" ] || fail "test hook $v is set in the environment (local tests only)"; done
else
  [ "${PILOT_LOCAL_TEST:-0}" = 1 ] || fail "--local-test needs PILOT_LOCAL_TEST=1"
  [ "${NC_HOME_ROOT:-}" != "" ] || fail "--local-test needs a fake NC_HOME_ROOT (never on the real campaign tree)"
fi

# ---- 1. guard first: limits confirmed, planned add admitted ------------------------------------------------------------
# every transient file of the submission lives in the campaign-owned scratch temp folder (never the system /tmp): set TMPDIR before ANY mktemp
export TMPDIR="$TMP_ROOT"; mkdir -p -- "$TMPDIR"
GRECEIPT_TMP=$(mktemp "$TMPDIR/guard_receipt.XXXXXX"); trap 'rm -f "$GRECEIPT_TMP"; rmdir "$TMP_ROOT" 2>/dev/null || true' EXIT
echo "== guard_check.sh $PLANNED_HOME_MB"
if ! GUARD="$GUARD" REQUIRED_CAMP_LIMIT_KB="$REQUIRED_CAMP_LIMIT_KB" REQUIRED_HOME_LIMIT_KB="$REQUIRED_HOME_LIMIT_KB" \
     bash "$PILOT_DIR/guard_check.sh" "$PLANNED_HOME_MB" "$GRECEIPT_TMP"; then
  echo "REFUSED: the guard does not enforce the charter limits or refused the planned add of ${PLANNED_HOME_MB} MB. Nothing was submitted." >&2
  exit 1
fi

# ---- 2. preconditions --------------------------------------------------------------------------------------------------
if [ -z "$MODULES" ] || [ -z "$MODULES_BENCH" ]; then
  if [ $LOCALTEST = 1 ] || [ $DRY = 1 ]; then echo "WARNING: MODULES / MODULES_BENCH are empty in pilot.env; a real submission would be refused."
  else fail "MODULES and MODULES_BENCH must be filled in $PILOT_DIR/pilot.env (must equal CONF's v2.2.1 NOTS build; core byte-identical to v2.2)"; fi
fi
for f in "$CORE_DIR/v3.R" "$CORE_DIR/cpp/v3_score.h" "$ENUM_DIR/lowp_enum.R" "$ENUM_DIR/exact_contract.R" "$ENUM_DIR/run_enum_dataset.R" "$V221_DIR/study/run_case.R" "$V221_DIR/study/adapter.R" "$V221_DIR/tools/p5_scan.R" "$V221_DIR/CHANGES_v2_2_1.md" "$V221_SUMS" "$LOWPR_DIR/lowp_verify_nots.R" \
         "$BENCH_DIR/run_bench_case.R" "$DEV_STUDY/manifests/inputs_manifest_lowp.csv" \
         "$STUDY/manifests/inputs_manifest_lowp.csv" "$STUDY/manifests/truth_manifest_lowp.csv" \
         "$STUDY/dev/manifests/inputs_manifest_lowp.csv" "$STUDY/dev/manifests/truth_manifest_lowp.csv" \
         "$CODE/lowp/tests/test_truth_lock_linux.sh" "$PILOT_DIR/truth_wave.sh" "$PILOT_DIR/truth_lib.sh" "$LISTS/smc_cases.tsv" "$LISTS/bench_cases.tsv" \
         "$RUN_HOME/OWNER" "$RUN_HOME/STAGED_SHA256.txt"; do
  [ -r "$f" ] || fail "missing staged file $f"
done
n_dev=$(find "$DEV_STUDY/inputs" -name 'dev_p00*_S?_r???.rds' | wc -l)
[ "$n_dev" -eq 60 ] || fail "expected 60 dev input files under $DEV_STUDY/inputs, found $n_dev"
n_tp=$(find "$STUDY/truth" -type f | wc -l); n_td=$(find "$STUDY/dev/truth" -type f | wc -l); n_si=$(find "$STUDY/inputs" -type f | wc -l)
{ [ "$n_tp" -eq 1200 ] && [ "$n_td" -eq 60 ] && [ "$n_si" -eq 6 ]; } || fail "study copy $STUDY must hold 1200 truth, 60 dev truth and 6 pilot input files (found $n_tp, $n_td, $n_si)"
if find "$DEV_STUDY" -type d -name 'truth*' | grep -q .; then fail "a truth folder exists under the dev inputs"; fi
( cd "$HOME_ROOT" && sha256sum --quiet -c "runs/$PILOT_ID/STAGED_SHA256.txt" ) || fail "staged files do not match STAGED_SHA256.txt"
# the pilot must run the frozen SMC-BVS v2.2.1 (core + study + tools), not merely the files that were staged: sha256sum -c against v2_2_1.SHA256SUMS + no unlisted file
source "$PILOT_DIR/frozen_check.sh"
pilot_check_frozen "$V221_DIR" "$V221_SUMS" || fail "the staged code/core/v2_2_1 tree does not match v2_2_1.SHA256SUMS (frozen v2.2.1)"
grep -q "$STAMP" "$RUN_HOME/OWNER" || fail "OWNER marker does not belong to this STAMP"
[ -r "$R_LIBS_BENCH" ] || echo "WARNING: pinned bench library $R_LIBS_BENCH is not readable from here (read-only use; checked on a compute node)"
[ ! -e "$LOG_RUN" ] || fail "$LOG_RUN already exists; use a new STAMP"

# ---- 3. launch record (scratch) ---------------------------------------------------------------------------------------------
if [ $DRY = 0 ]; then
  mkdir -p -- "$SCR_ROOT/results" "$SCR_ROOT/runs" "$LOG_RUN/launch"
  cp "$GRECEIPT_TMP" "$LOG_RUN/launch/guard_receipt_submit.txt"
  cp "$PILOT_DIR/pilot.env" "$LOG_RUN/launch/pilot.env"; sha256sum "$LOG_RUN/launch/pilot.env" > "$LOG_RUN/launch/pilot.env.sha256"
  cp "$RUN_HOME/STAGED_SHA256.txt" "$LOG_RUN/launch/STAGED_SHA256.txt"; cp "$RUN_HOME/OWNER" "$LOG_RUN/launch/OWNER"
  cp "$V221_SUMS" "$LOG_RUN/launch/v2_2_1.SHA256SUMS"      # manifest of the frozen v2.2.1 tree this pilot ran (verified above and again by s0_build and every SMC task)
  cp "$PILOT_DIR/JOB.md" "$LOG_RUN/launch/JOB.md" 2>/dev/null || true
  mkdir -p "$LOG_RUN/launch/lists"; cp "$LISTS"/* "$LOG_RUN/launch/lists/"
  { echo "# effective environment of the submission $(date -u +%FT%TZ) by $(id -un)@$(hostname), local_test=$LOCALTEST"
    echo "STAMP=$STAMP"; echo "HOME_ROOT=$HOME_ROOT"; echo "SCR_ROOT=$SCR_ROOT"; echo "GUARD=$GUARD"; echo "PLANNED_HOME_MB=$PLANNED_HOME_MB"
    echo "MODULES=[$MODULES]"; echo "MODULES_BENCH=[$MODULES_BENCH]"; echo "R_LIBS_LOWP=[$R_LIBS_LOWP]"; echo "R_LIBS_USER_LOWP=[$R_LIBS_USER_LOWP]"
    echo "R_LIBS_BENCH=[$R_LIBS_BENCH]"; echo "R_LIBS_USER_BENCH=[$R_LIBS_USER_BENCH]"
    for v in "${HOOKS[@]}" PILOT_LOCAL_TEST; do echo "$v=[${!v:-}]"; done; } > "$LOG_RUN/launch/effective_env.txt"
  printf 'step\tjobid\tarray\tdependency\n' > "$LOG_RUN/jobids.tsv"
  printf 'step\tjobid\tarray\tdependency\n' > "$RUN_HOME/JOBIDS.tsv"
  : > "$LOG_RUN/launch/sbatch_args.tsv"
fi
rm -f "$GRECEIPT_TMP"

# ---- 4. submission with abort-and-cancel ------------------------------------------------------------------------------
COMMON=(--chdir="$LOG_RUN" --export="ALL,STAMP=$STAMP")
SUBMITTED=()        # explicit ids submitted so far
SUBMITTED_ID=""
SCANCEL="${SCANCEL:-scancel}"
abort_submission() {   # abort_submission REASON : cancel what was submitted (explicit ids only), record, exit 5
  local reason=$1 id rc
  echo "SUBMISSION ABORTED: $reason" >&2
  { echo "aborted $(date -u +%FT%TZ): $reason"; echo "ids submitted before the failure: ${SUBMITTED[*]:-none}"; } >> "$LOG_RUN/launch/SUBMISSION_ABORTED.txt"
  for id in "${SUBMITTED[@]:-}"; do
    [ -n "$id" ] || continue
    if "$SCANCEL" "$id" 2>>"$LOG_RUN/launch/SUBMISSION_ABORTED.txt"; then echo "scancel $id ok" >> "$LOG_RUN/launch/SUBMISSION_ABORTED.txt"
    else rc=$?; echo "scancel $id FAILED rc=$rc: cancel it by hand" | tee -a "$LOG_RUN/launch/SUBMISSION_ABORTED.txt" >&2; fi
  done
  exit 5
}
submit() {   # submit STEP SCRIPT ARRAY|- DEP|-   ->  sets SUBMITTED_ID (no command substitution: failures must stop the driver)
  local step=$1 script=$2 arr=$3 dep=$4 o="$LOG_RUN/slurm-%x-%j.out" e="$LOG_RUN/slurm-%x-%j.err" out rc id
  local args=("${COMMON[@]}")
  if [ "$arr" != "-" ]; then args+=(--array="$arr"); o="$LOG_RUN/slurm-%x-%A_%a.out"; e="$LOG_RUN/slurm-%x-%A_%a.err"; fi
  args+=(--output="$o" --error="$e")
  if [ "$dep" != "-" ]; then args+=(--dependency="$dep" --kill-on-invalid-dep=yes); fi
  if [ $DRY = 1 ]; then
    printf 'DRY-RUN sbatch' >&2; printf ' %q' "${args[@]}" "$PILOT_DIR/slurm/$script" >&2; echo >&2
    SUBMITTED_ID="DRY_${step}"; return 0
  fi
  { printf '%s\t' "$step"; printf '%q ' "${args[@]}" "$PILOT_DIR/slurm/$script"; echo; } >> "$LOG_RUN/launch/sbatch_args.tsv"
  rc=0; out=$(sbatch --parsable "${args[@]}" "$PILOT_DIR/slurm/$script" 2>"$LOG_RUN/launch/sbatch_$step.err") || rc=$?
  [ $rc = 0 ] || abort_submission "sbatch failed for $step (exit $rc): $(head -c 300 "$LOG_RUN/launch/sbatch_$step.err" | tr '\n' ' ')"
  id=${out%%;*}
  [[ "$id" =~ ^[0-9]+$ ]] || abort_submission "sbatch returned an invalid job id '$out' for $step"
  SUBMITTED+=("$id"); SUBMITTED_ID=$id
  printf '%s\t%s\t%s\t%s\n' "$step" "$id" "$arr" "$dep" | tee -a "$LOG_RUN/jobids.tsv" >> "$RUN_HOME/JOBIDS.tsv"
}
submit s0_build s0_build.sbatch - -;                                   J_BUILD=$SUBMITTED_ID
submit s0_verify s0_verify.sbatch - -;                                 J_VERIFY=$SUBMITTED_ID
submit s0_truthlock s0_truthlock.sbatch - "afterok:$J_VERIFY";         J_TEST=$SUBMITTED_ID
submit s0_lock s0_lock.sbatch - "afterok:$J_TEST";                     J_LOCK=$SUBMITTED_ID
GATE="afterok:$J_BUILD:$J_VERIFY:$J_TEST:$J_LOCK"      # fits start only with regeneration PASSED, the permission test PASSED and truth LOCKED and verified
submit s1_enum20 s1_enum20.sbatch - "$GATE";                           J_E20=$SUBMITTED_ID
submit s1_enum30 s1_enum30.sbatch 0-5 "$GATE";                         J_E30=$SUBMITTED_ID
submit s1_scale s1_scale.sbatch - "$GATE";                             J_SCALE=$SUBMITTED_ID
submit s1_bitid s1_bitid.sbatch - "$GATE";                             J_BITID=$SUBMITTED_ID
submit s2_smc s2_smc.sbatch 0-27 "$GATE";                              J_SMC=$SUBMITTED_ID
submit s3_bench s3_bench.sbatch 0-23 "$GATE";                          J_BENCH=$SUBMITTED_ID
submit s8_unlock s8_unlock.sbatch - "afterany:$J_LOCK:$J_E20:$J_E30:$J_SCALE:$J_BITID:$J_SMC:$J_BENCH";   J_UNLOCK=$SUBMITTED_ID
submit s9_collect s9_collect.sbatch - "afterany:$J_BUILD:$J_VERIFY:$J_TEST:$J_UNLOCK";                    J_COLLECT=$SUBMITTED_ID

cat <<EOF

== submitted (dry-run=$DRY): build $J_BUILD | verify $J_VERIFY | truth-test $J_TEST | wave-lock $J_LOCK | enum20 $J_E20 | enum30 $J_E30 | scale $J_SCALE | bitid $J_BITID | smc $J_SMC | bench $J_BENCH | wave-unlock $J_UNLOCK | collect $J_COLLECT
== pilot id:   $PILOT_ID          job ids: $LOG_RUN/jobids.tsv (copy in $RUN_HOME/JOBIDS.tsv)
== the truth trees under $STUDY are LOCKED (mode 000) between wave-lock and wave-unlock; do not run guard.sh/du on the campaign home in that window.
== if wave-unlock fails or is cancelled: bash $PILOT_DIR/recover_truth.sh $STAMP   (JOB.md section 10)
== after collect has finished: bash $PILOT_DIR/final_accounting.sh $STAMP   (terminal snapshot incl. the collector), then pull and delete, one folder at a time:
   $SCR_ROOT/results/${PILOT_ID}_{enum20,enum30,scale_t08,scale_t16,scale_t32,smc,bench}
   $LOG_RUN        (includes launch/, truthlock/evidence/, accounting/)
== then: bash $PILOT_DIR/cleanup_pilot.sh $STAMP --yes
EOF
