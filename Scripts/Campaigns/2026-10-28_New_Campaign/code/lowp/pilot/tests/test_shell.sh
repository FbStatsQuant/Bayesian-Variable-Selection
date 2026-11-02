#!/bin/bash
# test_shell.sh -- LOCAL TEST of the shell side with stubs only (no Slurm, no NOTS): guard_check.sh, submit_pilot.sh (guard refusal, test hooks, sbatch
# failure at the first and in the middle of the chain with cancel-by-explicit-id, invalid job id, the dependency graph, launch record), cleanup_pilot.sh
# (scheduler failure, active ids, missing ownership, retained results, verified / unverified clean, shared trees untouched), recover_truth.sh.
#   bash test_shell.sh <work dir>        exit 0 if every case behaves as expected; writes <work>/SHELL_TESTS.md
set -uo pipefail
W=${1:?usage: test_shell.sh WORKDIR}; mkdir -p "$W"; W=$(cd "$W" && pwd)
PILOT="$(cd "$(dirname "$0")/.." && pwd)"
BIN="$W/bin"; mkdir -p "$BIN"; PASS=0; FAIL=0; OUT="$W/SHELL_TESTS.md"; : > "$OUT"
res() { # res NAME EXPECTED GOT [extra-condition-rc]
  local ok=ok; if [ "$2" != "$3" ] || [ "${4:-0}" != 0 ]; then ok="**WRONG**"; FAIL=$((FAIL + 1)); else PASS=$((PASS + 1)); fi
  echo "| $1 | $2 | $3 | $ok |" | tee -a "$OUT"; }
echo "| Case | Expected | Got | Result |" | tee -a "$OUT"; echo "|---|---|---|---|" | tee -a "$OUT"
# ---- stubs ---------------------------------------------------------------------------------------------------------------
cat > "$BIN/guard_good" <<'G'
#!/bin/bash
# fake guard with the D7 limits written exactly like the OPS guard; usage numbers from FAKE_HOME_GB / FAKE_CAMP_KB
set -uo pipefail
ADD_MB=${1:-0}
CAMP_LIMIT_KB=$((1024 * 1024 / 2))          # 0.5 GiB = 524288 KB
HOME_LIMIT_KB=$((96 * 1024 * 1024 / 10))    # 9.6 GiB
HOME_KB=$(awk -v g="${FAKE_HOME_GB:-8.85}" 'BEGIN{printf "%d", g*1048576}'); CAMP_KB=${FAKE_CAMP_KB:-20000}
S=OK; RC=0; W=""
if [ $((CAMP_KB + ADD_MB * 1024)) -gt $CAMP_LIMIT_KB ]; then S=REFUSE; RC=1; W=" campaign+add>limit"; fi
if [ $((HOME_KB + ADD_MB * 1024)) -gt $HOME_LIMIT_KB ]; then S=REFUSE; RC=1; W="$W home+add>limit"; fi
echo "2026 | home $(awk -v k=$HOME_KB 'BEGIN{printf "%.2f", k/1048576}') GB of 10.00 GB | campaign_home 0.02 GB | campaign_scratch 0.00 GB (info) | planned_add ${ADD_MB} MB | $S${W:+ (${W# })}"
exit $RC
G
sed 's#^CAMP_LIMIT_KB=.*#CAMP_LIMIT_KB=$((7 * 1024 * 1024))#; s#^HOME_LIMIT_KB=.*#HOME_LIMIT_KB=$((9 * 1024 * 1024))#' "$BIN/guard_good" > "$BIN/guard_old"
cat > "$BIN/sbatch" <<'S'
#!/bin/bash
n=$(( $(cat "$STUB_DIR/n" 2>/dev/null || echo 0) + 1 )); echo $n > "$STUB_DIR/n"
printf '%s\n' "$*" >> "$STUB_DIR/sbatch_calls.txt"
if [ "${FAIL_AT:-0}" = "$n" ]; then echo 'fabricated sbatch rejection' >&2; exit 42; fi
if [ "${BAD_ID_AT:-0}" = "$n" ]; then echo 'Submitted batch job (not parsable)'; exit 0; fi
echo $((7000 + n))
S
printf '#!/bin/bash\nprintf "%%s\\n" "$*" >> "$STUB_DIR/scancel_calls.txt"\n' > "$BIN/scancel"
printf '#!/bin/bash\necho "fabricated squeue outage" >&2; exit 17\n' > "$BIN/squeue_fail"
printf '#!/bin/bash\nexit 0\n' > "$BIN/squeue_idle"
printf '#!/bin/bash\necho "7003_2|lowp_p2_smc|RUNNING"\n' > "$BIN/squeue_active"
printf '#!/bin/bash\necho "7001|COMPLETED"\n' > "$BIN/sacct_ok"
chmod +x "$BIN"/*
# ---- guard_check.sh ------------------------------------------------------------------------------------------------------
cd "$W"
GUARD="$BIN/guard_good" bash "$PILOT/guard_check.sh" 30 "$W/g1.txt" >/dev/null 2>&1; res "guard_check: D7 limits enforced -> accepted" 0 $?
GUARD="$BIN/guard_old" bash "$PILOT/guard_check.sh" 30 "$W/g2.txt" >/dev/null 2>&1; res "guard_check: superseded 7 GiB / 9 GiB limits -> refused" 1 $?
GUARD_ALLOW_TEST=1 GUARD="$BIN/guard_good" bash "$PILOT/guard_check.sh" 30 "$W/g3.txt" >/dev/null 2>&1; res "guard_check: GUARD_ALLOW_TEST in the environment -> refused" 1 $?
FAKE_CAMP_KB=520000 GUARD="$BIN/guard_good" bash "$PILOT/guard_check.sh" 30 "$W/g4.txt" >/dev/null 2>&1; res "guard_check: guard refuses the planned add -> refused" 1 $?
FAKE_HOME_GB=9.59 GUARD="$BIN/guard_good" bash "$PILOT/guard_check.sh" 30 "$W/g5.txt" >/dev/null 2>&1; res "guard_check: home too full for the planned add -> refused" 1 $?
# ---- fixture NOTS tree ---------------------------------------------------------------------------------------------------
STAMP=20261029T1100Z; PID=${STAMP}_lowp_pilot
mkfix() { # mkfix ROOTDIR : minimal staged pilot under ROOTDIR/home/New_Campaign/runs/<PID>, scratch under ROOTDIR/scr/New_Campaign
  local H=$1/home/New_Campaign S=$1/scr/New_Campaign R=$1/home/New_Campaign/runs/$PID; chmod -R u+rwx "$1" 2>/dev/null; rm -rf "$1"
  mkdir -p "$H/code/ops" "$S/results" "$S/logs" "$S/runs" "$R/code/lowp/tests" "$R/code/core/v2_2_1/core/cpp" "$R/code/core/v2_2_1/study" "$R/code/core/v2_2_1/tools" "$R/code/lowp/enum" "$R/code/lowp/R" "$R/code/bench_lowp" \
           "$R/inputs/lowp_dev/inputs" "$R/inputs/lowp_dev/manifests" "$R/study/manifests" "$R/study/dev/manifests" "$R/study/truth" "$R/study/dev/truth" "$R/study/inputs"
  cp -R "$PILOT" "$R/code/lowp/pilot"; rm -rf "$R/code/lowp/pilot/tests"
  sed -i 's/^MODULES=""/MODULES="fake"/; s/^MODULES_BENCH=""/MODULES_BENCH="fake"/' "$R/code/lowp/pilot/pilot.env"
  for f in core/v2_2_1/core/v3.R core/v2_2_1/core/cpp/v3_score.h core/v2_2_1/study/run_case.R core/v2_2_1/study/adapter.R core/v2_2_1/tools/p5_scan.R core/v2_2_1/CHANGES_v2_2_1.md lowp/enum/lowp_enum.R lowp/enum/exact_contract.R lowp/enum/run_enum_dataset.R lowp/R/lowp_verify_nots.R bench_lowp/run_bench_case.R lowp/tests/test_truth_lock_linux.sh; do echo fixture > "$R/code/$f"; done
  ( cd "$R/code/core/v2_2_1" && find . -type f | LC_ALL=C sort | xargs sha256sum > "$R/code/core/v2_2_1.SHA256SUMS" )   # manifest of the fixture v2.2.1 tree (paths ./core/..., ./study/...)
  for d in "$R/inputs/lowp_dev/manifests" "$R/study/manifests" "$R/study/dev/manifests"; do echo fixture > "$d/inputs_manifest_lowp.csv"; done
  for d in "$R/study/manifests" "$R/study/dev/manifests"; do echo fixture > "$d/truth_manifest_lowp.csv"; done
  for i in $(seq 1 1200); do : > "$R/study/truth/$i"; done
  for i in $(seq 1 60); do : > "$R/study/dev/truth/$i"; printf -v nm 'dev_p0020_S1_r%03d.rds' "$i"; : > "$R/inputs/lowp_dev/inputs/$nm"; done
  for i in 1 2 3 4 5 6; do : > "$R/study/inputs/$i"; done
  echo "lowp_pilot $STAMP staged fixture" > "$R/OWNER"
  (cd "$H" && find "runs/$PID" -type f ! -name STAGED_SHA256.txt ! -name pilot.env | sort | xargs sha256sum > "runs/$PID/STAGED_SHA256.txt")
  mkdir -p "$H/code/core/shared" "$H/code/lowp_shared"; echo keep > "$H/code/core/shared/x"; echo keep > "$H/code/lowp_shared/y"
}
export STUB_DIR="$W/stub"; mkdir -p "$STUB_DIR"
runsubmit() { # runsubmit LABEL [VAR=val ...]
  rm -f "$STUB_DIR"/*
  ( export NC_HOME_ROOT="$FH" NC_SCR_ROOT="$FS" GUARD="$BIN/guard_good" PATH="$BIN:$PATH" STAMP=$STAMP; for kv in "${@:2}"; do export "$kv"; done
    bash "$FH/runs/$PID/code/lowp/pilot/submit_pilot.sh" > "$W/submit_$1.log" 2>&1 ); }
FX="$W/fx"; FH="$FX/home/New_Campaign"; FS="$FX/scr/New_Campaign"
nocall() { [ ! -f "$STUB_DIR/sbatch_calls.txt" ] && echo 0 || echo 1; }
mkfix "$FX"; runsubmit hook PILOT_LIMIT=2; rc=$?; res "submit: a test hook in the environment -> refused (exit 2), no sbatch" 2 $rc $(nocall)
mkfix "$FX"; runsubmit guard FAKE_HOME_GB=9.59; rc=$?; res "submit: guard refuses -> exit 1, no sbatch, no log folder" 1 $rc $([ ! -f "$STUB_DIR/sbatch_calls.txt" ] && [ ! -e "$FS/logs/$PID" ] && echo 0 || echo 1)
mkfix "$FX"; runsubmit guardold GUARD="$BIN/guard_old"; rc=$?; res "submit: guard with the superseded limits -> refused (exit 1)" 1 $rc $(nocall)
mkfix "$FX"; runsubmit first FAIL_AT=1; rc=$?
res "submit: sbatch rejected at the FIRST call -> abort exit 5, one attempt, abort record" 5 $rc $([ "$(wc -l < "$STUB_DIR/sbatch_calls.txt")" = 1 ] && [ -s "$FS/logs/$PID/launch/SUBMISSION_ABORTED.txt" ] && echo 0 || echo 1)
mkfix "$FX"; runsubmit mid FAIL_AT=6; rc=$?
res "submit: sbatch rejected in the MIDDLE (6th call) -> abort exit 5, 6 attempts, none later" 5 $rc $([ "$(wc -l < "$STUB_DIR/sbatch_calls.txt")" = 6 ] && echo 0 || echo 1)
res "submit: the 5 ids already submitted were cancelled by explicit id" "7001 7002 7003 7004 7005" "$(tr '\n' ' ' < "$STUB_DIR/scancel_calls.txt" | sed 's/ *$//')"
res "submit: no empty or malformed id was recorded in jobids.tsv" 0 "$(awk -F'\t' 'NR>1 && $2 !~ /^[0-9]+$/' "$FS/logs/$PID/jobids.tsv" | wc -l)"
mkfix "$FX"; runsubmit badid BAD_ID_AT=3; rc=$?; res "submit: an unparsable sbatch answer aborts the chain (exit 5, 3 attempts)" 5 $rc $([ "$(wc -l < "$STUB_DIR/sbatch_calls.txt")" = 3 ] && echo 0 || echo 1)
mkfix "$FX"; runsubmit ok; rc=$?; res "submit: complete chain -> exit 0, 12 submissions" 0 $rc $([ "$(wc -l < "$STUB_DIR/sbatch_calls.txt")" = 12 ] && echo 0 || echo 1)
calls="$STUB_DIR/sbatch_calls.txt"
c3=$(sed -n 3p "$calls" | grep -c 'afterok:7002 '); c4=$(sed -n 4p "$calls" | grep -c 'afterok:7003 ')
res "submit: truth-lock test afterok verify; wave lock afterok the test" 2 $((c3 + c4))
bad=0; for n in 5 6 7 8 9 10; do sed -n ${n}p "$calls" | grep -q 'afterok:7001:7002:7003:7004 ' || bad=$((bad + 1)); done
res "submit: all six fitting steps afterok build+verify+test+lock" 0 $bad
u=$(sed -n 11p "$calls" | grep -c 'afterany:7004:7005:7006:7007:7008:7009:7010 '); c=$(sed -n 12p "$calls" | grep -c 'afterany:7001:7002:7003:7011 ')
res "submit: unlock finalizer afterany lock + six fits; collect afterany build, verify, test and unlock" 2 $((u + c))
l=0; [ -s "$FS/logs/$PID/launch/pilot.env" ] && [ -s "$FS/logs/$PID/launch/pilot.env.sha256" ] && grep -q GUARD_CHECK_OK "$FS/logs/$PID/launch/guard_receipt_submit.txt" && [ "$(wc -l < "$FS/logs/$PID/launch/sbatch_args.tsv")" = 12 ] && [ -s "$FS/logs/$PID/launch/effective_env.txt" ] || l=1
res "submit: launch record (final pilot.env + hash, guard receipt, 12 sbatch vectors, effective env) is on scratch" 0 $l
res "submit: all slurm outputs are directed to scratch" 0 "$(grep -vc -- "--output=$FS/logs" "$calls")"
# ---- frozen v2.2.1 tree: the pilot must run exactly the tree of code/core/v2_2_1.SHA256SUMS (every case regenerates STAGED_SHA256.txt so only the frozen check can object) ----
restage() { (cd "$FH" && find "runs/$PID" -type f ! -name STAGED_SHA256.txt ! -name pilot.env | sort | xargs sha256sum > "runs/$PID/STAGED_SHA256.txt"); }
V="$FH/runs/$PID/code/core/v2_2_1"
mkfix "$FX"; echo "tampered" >> "$V/study/run_case.R"; restage; runsubmit frz1; rc=$?
res "frozen: a modified v2.2.1 file (staged hash list regenerated) -> refused (exit 2), no sbatch" 2 $rc $(nocall)
mkfix "$FX"; echo "extra" > "$V/study/adapter_lowp.R"; restage; runsubmit frz2; rc=$?
res "frozen: an unlisted file in the v2.2.1 tree (e.g. a forked adapter) -> refused (exit 2), no sbatch" 2 $rc $(nocall)
mkfix "$FX"; rm "$V/tools/p5_scan.R"; restage; runsubmit frz3; rc=$?
res "frozen: a missing v2.2.1 file -> refused (exit 2), no sbatch" 2 $rc $(nocall)
mkfix "$FX"; rm "$FH/runs/$PID/code/core/v2_2_1.SHA256SUMS"; restage; runsubmit frz4; rc=$?
res "frozen: manifest v2_2_1.SHA256SUMS missing -> refused (exit 2), no sbatch" 2 $rc $(nocall)
mkfix "$FX"; mkdir -p "$V/core/.cpp_cache"; echo cache > "$V/core/.cpp_cache/x.so"; restage; runsubmit frz5; rc=$?
res "frozen: the compile cache core/.cpp_cache is tolerated -> chain complete (exit 0, 12 submissions)" 0 $rc $([ "$(wc -l < "$STUB_DIR/sbatch_calls.txt")" = 12 ] && echo 0 || echo 1)
mkfix "$FX"; runsubmit frz6; rc=$?
res "frozen: manifest copied into the launch record" 0 $rc $([ -s "$FS/logs/$PID/launch/v2_2_1.SHA256SUMS" ] && echo 0 || echo 1)
# ---- CONF-2b (Sol F6): symbolic links are refused anywhere in the frozen tree (outside the tolerated compile cache), even when `sha256sum -c` passes. Real links only
#      (MSYS=winsymlinks:nativestrict on Windows Git Bash makes `ln -s` fail instead of copying); a case whose link cannot be created is reported as SKIPPED and counted as a failure.
mklnk() { MSYS=winsymlinks:nativestrict ln -s "$1" "$2" 2>/dev/null && [ -L "$2" ]; }   # mklnk TARGET LINKNAME
lnkmsg() { grep -q -e 'symbolic links or special entries' -e 'tree is a symbolic link' "$W/$1" && echo 0 || echo 1; }   # the refusal came from the link rule of frozen_check.sh
skiplnk() { echo "| $1 | - | - | **SKIPPED (could not create a real symbolic link here)** |" | tee -a "$OUT"; FAIL=$((FAIL + 1)); }
shaok() { ( cd "$1" && sha256sum --quiet -c "$2" >/dev/null 2>&1 ) && echo 0 || echo 1; }   # 0 = the manifest check alone would pass
mkfix "$FX"
if mklnk adapter.R "$V/study/unlisted_adapter.R"; then restage; runsubmit lnk1; rc=$?
  res "frozen: an unlisted FILE symlink in the v2.2.1 tree (study/unlisted_adapter.R -> adapter.R) -> refused (exit 2), no sbatch" 2 $rc $(( $(nocall) + $(lnkmsg submit_lnk1.log) ))
else skiplnk "frozen: unlisted file symlink"; fi
mkfix "$FX"
if mklnk ../core "$V/study/linkdir" && [ -d "$V/study/linkdir" ]; then restage; runsubmit lnk2; rc=$?
  res "frozen: an unlisted DIRECTORY symlink in the v2.2.1 tree (study/linkdir -> ../core) -> refused (exit 2), no sbatch" 2 $rc $(( $(nocall) + $(lnkmsg submit_lnk2.log) ))
else skiplnk "frozen: unlisted directory symlink"; fi
mkfix "$FX"; cp "$V/study/run_case.R" "$W/identical_run_case.R"; rm "$V/study/run_case.R"
if mklnk "$W/identical_run_case.R" "$V/study/run_case.R" && [ -f "$V/study/run_case.R" ]; then restage; runsubmit lnk3; rc=$?
  res "frozen: a symlink REPLACING the listed study/run_case.R (identical content, sha256sum -c alone passes) -> refused (exit 2), no sbatch" 2 $rc $(( $(nocall) + $(lnkmsg submit_lnk3.log) + $(shaok "$V" "$FH/runs/$PID/code/core/v2_2_1.SHA256SUMS") ))
else skiplnk "frozen: symlink replacing a listed file"; fi
mkfix "$FX"; mkdir -p "$W/outside_cache"; echo cache > "$W/outside_cache/x.so"
if mklnk "$W/outside_cache" "$V/core/.cpp_cache" && [ -d "$V/core/.cpp_cache" ]; then restage; runsubmit lnk4; rc=$?
  res "frozen: core/.cpp_cache as a symlink pointing outside the tree -> refused (exit 2), no sbatch" 2 $rc $(( $(nocall) + $(lnkmsg submit_lnk4.log) ))
else skiplnk "frozen: .cpp_cache symlink"; fi
mkfix "$FX"; mv "$V" "$FH/runs/$PID/code/core/v2_2_1_real"
if mklnk "$FH/runs/$PID/code/core/v2_2_1_real" "$V" && [ -d "$V" ]; then restage; runsubmit lnk5; rc=$?
  res "frozen: the v2.2.1 tree root itself is a symlink -> refused (exit 2), no sbatch" 2 $rc $(( $(nocall) + $(lnkmsg submit_lnk5.log) ))
else skiplnk "frozen: tree-root symlink"; fi
mkfix "$FX"; mkdir -p "$V/core/.cpp_cache"; echo cache > "$V/core/.cpp_cache/x.so"; restage; runsubmit lnk6; rc=$?
res "frozen: a REAL core/.cpp_cache directory is still tolerated after the symlink rule -> chain complete (exit 0, 12 submissions)" 0 $rc $([ "$(wc -l < "$STUB_DIR/sbatch_calls.txt")" = 12 ] && echo 0 || echo 1)
# ---- the SMC task: v2.2.1 CLI with the unchanged flags; refuses a non-frozen tree (exit 67); sbatch scripts of the pilot never mention the retired fork ----
printf '#!/bin/bash\nexit 0\n' > "$BIN/Rscript"; chmod +x "$BIN/Rscript"
smctask() { # smctask TASKID : run s2_smc.sbatch in DRYRUN mode against the fixture tree
  ( export NC_HOME_ROOT="$FH" NC_SCR_ROOT="$FS" PATH="$BIN:$PATH" STAMP=$STAMP PILOT_LOCAL_TEST=1 PILOT_DRYRUN=1 PILOT_SKIP_MODULES=1 SLURM_ARRAY_TASK_ID=$1 SLURM_ARRAY_JOB_ID=7009
    bash "$FH/runs/$PID/code/lowp/pilot/slurm/s2_smc.sbatch" > "$W/smctask.log" 2>&1 ); }
mkfix "$FX"; smctask 0; rc=$?
res "smc task: frozen tree verified, dry-run command is v2.2.1 study/run_case.R with the unchanged flags (primary)" 0 $rc \
    $(grep -q "DRYRUN timed arm=smc .*" "$W/smctask.log" && grep -q -- "core/v2_2_1/study/run_case.R" "$W/smctask.log" && grep -q -- "--core-dir .*core/v2_2_1/core" "$W/smctask.log" && grep -q -- "--mem-gb 2 --hours 4 --development" "$W/smctask.log" && ! grep -q -- "--repeat" "$W/smctask.log" && grep -q "frozen v2.2.1 tree verified" "$W/smctask.log" && echo 0 || echo 1)
smctask 24; rc=$?
res "smc task: repeat fit (array 24) passes --repeat 1 to run_case.R" 0 $rc $(grep -q -- "--repeat 1" "$W/smctask.log" && grep -q -- "run_case.R" "$W/smctask.log" && echo 0 || echo 1)
echo "tampered" >> "$V/core/v3.R"; smctask 0; rc=$?
res "smc task: modified core file -> exit 67 before any fit, no DRYRUN command" 67 $rc $(grep -q "DRYRUN timed" "$W/smctask.log" && echo 1 || echo 0)
mkfix "$FX"; echo extra > "$V/study/adapter_lowp.R"; smctask 0; rc=$?
res "smc task: unlisted adapter file in the v2.2.1 tree -> exit 67" 67 $rc
mkfix "$FX"
if mklnk adapter.R "$V/study/unlisted_adapter.R"; then smctask 0; rc=$?
  res "smc task: unlisted FILE symlink in the v2.2.1 tree (F6) -> exit 67, no DRYRUN command" 67 $rc $(grep -q "DRYRUN timed" "$W/smctask.log" && echo 1 || echo 0)
else skiplnk "smc task: unlisted file symlink"; fi
mkfix "$FX"; cp "$V/study/run_case.R" "$W/identical_run_case.R"; rm "$V/study/run_case.R"
if mklnk "$W/identical_run_case.R" "$V/study/run_case.R" && [ -f "$V/study/run_case.R" ]; then smctask 0; rc=$?
  res "smc task: a symlink replacing the listed study/run_case.R (sha256sum -c alone passes) -> exit 67, no DRYRUN command" 67 $rc $(grep -q "DRYRUN timed" "$W/smctask.log" && echo 1 || echo 0)
else skiplnk "smc task: symlink replacing a listed file"; fi
res "pilot bundle: no sbatch/driver/stage script references lowp/smc, run_smc_case.R or core/v2_2" 0 "$(grep -rnE 'lowp/smc|run_smc_case|adapter_lowp|core/v2_2/|core/v2_2\"|core/v2_2$|SMC_DIR' "$PILOT"/*.sh "$PILOT"/slurm "$PILOT"/pilot.env "$PILOT"/R | grep -vc '^$')"
# ---- the guard-receipt temp file lives in the campaign scratch temp folder, never the system /tmp ------------------------------------
mkfix "$FX"
cat > "$FH/runs/$PID/code/lowp/pilot/guard_check.sh" <<'G'
#!/bin/bash
echo "$2" > "$STUB_DIR/receipt_path"; echo "GUARD_CHECK_OK stub" > "$2"; exit 0
G
(cd "$FH" && find "runs/$PID" -type f ! -name STAGED_SHA256.txt ! -name pilot.env | sort | xargs sha256sum > "runs/$PID/STAGED_SHA256.txt")
POISON="$W/poison_tmp"; rm -rf "$POISON"; mkdir -p "$POISON"
runsubmit tmpdir TMPDIR="$POISON"; rc=$?
rp=$(cat "$STUB_DIR/receipt_path" 2>/dev/null)
case "$rp" in "$FS"/runs/*) inscr=0;; *) inscr=1;; esac
res "submit: guard-receipt temp file is under campaign scratch (runs/<PID>_tmp), not the caller's TMPDIR or /tmp" 0 $inscr $([ -z "$(ls -A "$POISON")" ] && echo 0 || echo 1)
# ---- cleanup_pilot.sh ----------------------------------------------------------------------------------------------------
mkfix "$FX"; printf 'step\tjobid\tarray\tdependency\ns0_build\t7001\t-\t-\n' > "$FH/runs/$PID/JOBIDS.tsv"
cp "$FH/runs/$PID/code/lowp/pilot/cleanup_pilot.sh" "$W/cleanup_copy.sh"
runclean() { ( export NC_HOME_ROOT="$FH" NC_SCR_ROOT="$FS" GUARD="${GUARD_C:-$BIN/guard_good}" SQUEUE="${SQ:-$BIN/squeue_idle}" SACCT="${SA:-$BIN/sacct_ok}"; bash "$W/cleanup_copy.sh" $STAMP "$@" > "$W/clean.log" 2>&1 ); }
SQ="$BIN/squeue_fail" runclean --yes; rc=$?; res "cleanup: squeue fails -> refused (exit 4), nothing deleted" 4 $rc $([ -e "$FH/runs/$PID/OWNER" ] && echo 0 || echo 1)
SQ="$BIN/squeue_active" runclean --yes; rc=$?; res "cleanup: a recorded pilot job is still active -> refused (exit 3)" 3 $rc $([ -e "$FH/runs/$PID/OWNER" ] && echo 0 || echo 1)
mv "$FH/runs/$PID/OWNER" "$W/OWNER.bak"; runclean --yes; rc=$?; res "cleanup: ownership marker missing -> refused (exit 3)" 3 $rc $([ -d "$FH/runs/$PID" ] && echo 0 || echo 1); mv "$W/OWNER.bak" "$FH/runs/$PID/OWNER"
mkdir -p "$FS/results/${PID}_enum20"; runclean --yes; rc=$?; res "cleanup: results still on scratch -> refused (exit 3)" 3 $rc $([ -d "$FH/runs/$PID" ] && echo 0 || echo 1); rmdir "$FS/results/${PID}_enum20"
mv "$FH/runs/$PID/JOBIDS.tsv" "$W/J.bak"; runclean --yes; rc=$?; res "cleanup: job-id record missing -> refused (exit 3)" 3 $rc $([ -d "$FH/runs/$PID" ] && echo 0 || echo 1); mv "$W/J.bak" "$FH/runs/$PID/JOBIDS.tsv"
runclean; rc=$?; res "cleanup: dry run changes nothing (exit 0)" 0 $rc $([ -d "$FH/runs/$PID" ] && echo 0 || echo 1)
FAKE_HOME_GB=9.9 runclean --yes; rc=$?; res "cleanup: removal done but the final guard refuses -> UNVERIFIED (exit 1)" 1 $rc $(grep -q 'CLEANUP UNVERIFIED' "$W/clean.log" && echo 0 || echo 1)
mkfix "$FX"; printf 'step\tjobid\tarray\tdependency\ns0_build\t7001\t-\t-\n' > "$FH/runs/$PID/JOBIDS.tsv"; mkdir -p "$FS/runs/${PID}_cache" "$FS/runs/${PID}_tmp"
runclean --yes; rc=$?; res "cleanup: clean run -> VERIFIED (exit 0)" 0 $rc $(grep -q 'CLEANUP VERIFIED' "$W/clean.log" && echo 0 || echo 1)
res "cleanup: only pilot-owned trees removed; shared code/ trees untouched" 0 0 $([ ! -e "$FH/runs/$PID" ] && [ ! -e "$FS/runs/${PID}_cache" ] && [ -e "$FH/code/core/shared/x" ] && [ -e "$FH/code/lowp_shared/y" ] && echo 0 || echo 1)
# ---- FC6: linked ancestor (junction/symlink) must be refused before any deletion ------------------------------------------
mklink_junction() { # mklink_junction LINK TARGET  (Windows junction; or a real symlink elsewhere)
  if [ "$(uname -o 2>/dev/null)" = "Msys" ] || [ "$(uname -o 2>/dev/null)" = "Cygwin" ]; then
    cmd //c "mklink /J $(cygpath -w "$1") $(cygpath -w "$2")" >/dev/null 2>&1 && [ -d "$1" ]
  else ln -s "$2" "$1" && [ -L "$1" ]; fi; }
mkfix "$FX"; printf 'step\tjobid\tarray\tdependency\ns0_build\t7001\t-\t-\n' > "$FH/runs/$PID/JOBIDS.tsv"
OUTSIDE="$W/outside_runs"; rm -rf "$OUTSIDE"; mkdir -p "$OUTSIDE/$PID"; echo "lowp_pilot $STAMP staged OUTSIDE" > "$OUTSIDE/$PID/OWNER"; printf 'step\tjobid\tarray\tdependency\ns0_build\t7001\t-\t-\n' > "$OUTSIDE/$PID/JOBIDS.tsv"; echo precious > "$OUTSIDE/$PID/precious.txt"
cp "$FH/runs/$PID/code/lowp/pilot/cleanup_pilot.sh" "$W/cleanup_copy.sh"; mv "$FH/runs" "$FH/runs_real"
if mklink_junction "$FH/runs" "$OUTSIDE"; then
  runclean --yes; rc=$?; res "cleanup: 'runs' is a linked directory resolving outside the campaign root -> refused (exit 4), nothing deleted" 4 $rc $([ -e "$OUTSIDE/$PID/precious.txt" ] && echo 0 || echo 1)
  runclean; rc=$?; res "cleanup: the same ancestor link is refused in the dry run too (exit 4)" 4 $rc
  cmd //c "rmdir $(cygpath -w "$FH/runs")" >/dev/null 2>&1 || rm -f "$FH/runs"
else echo "| cleanup: linked-ancestor tests | - | - | **SKIPPED (could not create a junction/symlink here)** |" | tee -a "$OUT"; FAIL=$((FAIL + 1)); fi
mv "$FH/runs_real" "$FH/runs" 2>/dev/null
# a link at runs/<PID> itself
mkfix "$FX"; printf 'step\tjobid\tarray\tdependency\ns0_build\t7001\t-\t-\n' > "$FH/runs/$PID/JOBIDS.tsv"; cp "$FH/runs/$PID/code/lowp/pilot/cleanup_pilot.sh" "$W/cleanup_copy.sh"
mv "$FH/runs/$PID" "$W/pid_real"
if mklink_junction "$FH/runs/$PID" "$OUTSIDE/$PID"; then
  runclean --yes; rc=$?; res "cleanup: runs/<PID> itself is a link to an outside folder -> refused (exit 4), nothing deleted" 4 $rc $([ -e "$OUTSIDE/$PID/precious.txt" ] && echo 0 || echo 1)
  cmd //c "rmdir $(cygpath -w "$FH/runs/$PID")" >/dev/null 2>&1 || rm -f "$FH/runs/$PID"
else echo "| cleanup: linked runs/<PID> test | - | - | **SKIPPED** |" | tee -a "$OUT"; FAIL=$((FAIL + 1)); fi
# ---- recover_truth.sh -----------------------------------------------------------------------------------------------------
mkfix "$FX"; printf 'step\tjobid\tarray\tdependency\ns2_smc\t7003\t0-27\t-\n' > "$FH/runs/$PID/JOBIDS.tsv"
rec() { ( export NC_HOME_ROOT="$FH" SQUEUE="$1"; bash "$FH/runs/$PID/code/lowp/pilot/recover_truth.sh" $STAMP > "$W/rec.log" 2>&1 ); }
rec "$BIN/squeue_active"; res "recover_truth: refuses while a pilot job is active (exit 3)" 3 $?
rec "$BIN/squeue_fail"; res "recover_truth: refuses when the scheduler cannot be queried (exit 3)" 3 $?
rec "$BIN/squeue_idle"; res "recover_truth: idle scheduler -> reopens and verifies 1200 + 60 files (exit 0)" 0 $?
echo; echo "passed $PASS failed $FAIL" | tee -a "$OUT"; [ "$FAIL" = 0 ]
