#!/bin/bash
# test_shell.sh -- LOCAL dry-run tests of the PROD-H shell side with stub sbatch/squeue/sacct/scontrol/scancel/srun/Rscript (no Slurm, no NOTS, no R).
# The REAL runner scripts, the REAL tables and the REAL frozen v2.2.1 tree are used: stage_local.sh builds the tar, each fixture extracts it exactly
# as OPS will, and the scripts run against fake roots. Only the scheduler and Rscript are stubs (tests/stubs).
#   bash test_shell.sh <work dir>      exit 0 if every case behaves as expected; writes <work>/SHELL_TESTS.md
set -uo pipefail
W=${1:?usage: test_shell.sh WORKDIR}; mkdir -p "$W"; W=$(cd "$W" && pwd)
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"; B="$(cd "$HERE/.." && pwd)"
mixed() { if command -v cygpath >/dev/null 2>&1; then cygpath -m "$1"; else echo "$1"; fi; }   # Python on Windows cannot read /c/... paths from files
PASS=0; FAIL=0; OUT="$W/SHELL_TESTS.md"; : > "$OUT"
res() { # res NAME EXPECTED GOT [extra-condition-rc]
  local ok=ok; if [ "$2" != "$3" ] || [ "${4:-0}" != 0 ]; then ok="**WRONG**"; FAIL=$((FAIL + 1)); else PASS=$((PASS + 1)); fi
  local e=$2 g=$3; [ ${#e} -gt 110 ] && e="${e:0:50}...${e: -50}"; [ ${#g} -gt 110 ] && g="${g:0:50}...${g: -50}"
  echo "| $1 | $e | $g | $ok |" | tee -a "$OUT"; }
echo "| Case | Expected | Got | Result |" | tee -a "$OUT"; echo "|---|---|---|---|" | tee -a "$OUT"
b() { [ "$1" = 0 ] && echo 0 || echo 1; }       # b RC : 0 if the condition command succeeded
# ---- stubs --------------------------------------------------------------------------------------------------------------------------------------
BIN="$W/bin"; rm -rf "$BIN"; mkdir -p "$BIN"; cp "$HERE"/stubs/* "$BIN/"; chmod +x "$BIN"/*
if command -v py >/dev/null 2>&1; then printf '#!/bin/bash\nexec py -3 "$@"\n' > "$BIN/python3"; chmod +x "$BIN/python3"; fi
module() { return 0; }; export -f module           # env.sh needs an Lmod `module` function
STAMP=20261029T1500Z; RID=${STAMP}_prodH; SD="$W/stub"; mkdir -p "$SD"; export STUB_DIR="$SD"
# ---- one real tar, built by stage_local.sh (itself verified by extraction) ---------------------------------------------------------------------------
rm -rf "$W/stage_out"
bash "$B/stage_local.sh" --stamp $STAMP --out "$W/stage_out" > "$W/stage_local.log" 2>&1; res "stage_local: builds and verifies the tar (extraction + STAGED_SHA256 + frozen tree)" 0 $?
TAR="$W/stage_out/prodH_bundle_$STAMP.tar"
# ---- read-only study fixture (600 inputs per p) -----------------------------------------------------------------------------------------------------
STUDY="$W/study"; if [ ! -d "$STUDY/inputs/p1000" ]; then
  mkdir -p "$STUDY/manifests" "$STUDY/inputs/p0500" "$STUDY/inputs/p1000"; echo fixture > "$STUDY/manifests/inputs_manifest.csv"
  for p in 0500 1000; do for s in 1 2 3 4 5 6; do for r in $(seq 1 100); do : > "$STUDY/inputs/p$p/$(printf 'p%s_S%d_r%03d.rds' $p $s $r)"; done; done; done
fi
FX=""; FH=""; FS=""
mkfix() { # mkfix ROOT : fresh fake NOTS (home/New_Campaign, scr/New_Campaign) with the tar extracted as OPS will
  FX=$1; chmod -R u+rwx "$FX" 2>/dev/null; rm -rf "$FX"
  mkdir -p "$FX/home/New_Campaign" "$FX/scr/New_Campaign"
  tar -xf "$TAR" -C "$FX/home/New_Campaign"
  FH=$(mixed "$FX/home/New_Campaign"); FS=$(mixed "$FX/scr/New_Campaign")
  RD="$FH/runs/$RID"; LOG="$FS/logs/$RID"; CODE="$FH/code/core/v2_2_1"
  rm -f "$SD"/*; echo -n > "$SD/.keep"
}
restage() { (cd "$FH" && find . -type f ! -name STAGED_SHA256.txt ! -name refusals.log | LC_ALL=C sort | xargs -d '
' sha256sum > "runs/$RID/STAGED_SHA256.txt"); }
nenv() { # run a command in the fake-NOTS environment: nenv [VAR=val ...] -- cmd args...
  local kv; local -a e=()
  while [ "$1" != "--" ]; do e+=("$1"); shift; done; shift
  ( export NC_LOCAL_TEST=1 NC_HOME_ROOT="$FH" NC_SCR_ROOT="$FS" NC_STUDY="$(mixed "$STUDY")" GUARD="$BIN/guard_good" NC_STUB_BIN="$BIN" PATH="$BIN:$PATH" STUB_DIR="$SD"
    for kv in "${e[@]:-}"; do [ -n "$kv" ] && export "${kv?}"; done
    "$@" ); }
SUBMIT() { nenv "$@" -- bash "$RD/runner/submit.sh" $SUBMIT_ARGS; }
nocalls() { [ ! -s "$SD/sbatch_calls.txt" ] && echo 0 || echo 1; }
ncalls() { [ -f "$SD/sbatch_calls.txt" ] && wc -l < "$SD/sbatch_calls.txt" || echo 0; }
reflog() { if [ -d "$LOG" ]; then echo "$LOG/refusals.log"; else echo "$FS/logs/_refusals/$RID.log"; fi; }   # refusals are logged on scratch (R2-9), never in home

echo "| **submit.sh: refusals (nothing may reach sbatch)** | | | |" | tee -a "$OUT"
SUBMIT_ARGS=""
mkfix "$W/fx_ref"; SUBMIT NC_LOCAL_TEST=0 > "$W/s_hook.log" 2>&1; rc=$?
res "refusal: test hook (NC_STUB_BIN / roots) in a non-test environment -> exit 2, no sbatch" 2 $rc $(nocalls)
mkfix "$W/fx_ref"; SUBMIT FAKE_HOME_GB=9.59 > "$W/s_guard.log" 2>&1; rc=$?
res "refusal: guard refuses (home would pass 9.6 GiB) -> exit 1, no sbatch, no launch record, no scratch folder" 1 $rc $([ ! -e "$RD/launch" ] && [ ! -e "$LOG" ] && nocalls || echo 1)
mkfix "$W/fx_ref"
( export NC_LOCAL_TEST=1 NC_HOME_ROOT="$FH" NC_SCR_ROOT="$FS" NC_STUDY="$(mixed "$STUDY")" GUARD="$BIN/guard_old" NC_STUB_BIN="$BIN" PATH="$BIN:$PATH" STUB_DIR="$SD"; bash "$RD/runner/submit.sh" > "$W/s_guardold.log" 2>&1 ); rc=$?
res "refusal: guard with the superseded limits (7 GiB / 9 GiB) -> exit 1, no sbatch" 1 $rc $(nocalls)
mkfix "$W/fx_ref"; echo "tampered" >> "$CODE/study/run_case.R"; restage; SUBMIT > "$W/s_mism.log" 2>&1; rc=$?
res "refusal: manifest mismatch (run_case.R modified, staged list regenerated) -> exit 2, no sbatch" 2 $rc $(nocalls)
grep -q "frozen v2.2.1 tree check failed" "$(reflog)"; res "refusal: manifest mismatch is reported as a frozen-tree failure" 0 $?
mkfix "$W/fx_ref"; echo "extra" > "$CODE/study/adapter_fork.R"; restage; SUBMIT > "$W/s_extra.log" 2>&1; rc=$?
res "refusal: an unlisted file in the v2.2.1 tree -> exit 2, no sbatch" 2 $rc $(nocalls)
grep -q "does not list" "$(reflog)" || grep -q "frozen" "$(reflog)"; res "refusal: unlisted file is named by the frozen check" 0 $?
mkfix "$W/fx_ref"; echo "x" >> "$RD/runner/task.sh"; SUBMIT > "$W/s_staged.log" 2>&1; rc=$?
res "refusal: a staged runner file differs from STAGED_SHA256.txt -> exit 2, no sbatch" 2 $rc $(nocalls)
mkfix "$W/fx_ref"; rm "$FH/code/core/v2_2_1.SHA256SUMS"; SUBMIT > "$W/s_nosums.log" 2>&1; rc=$?
res "refusal: manifest file missing -> exit 2, no sbatch" 2 $rc $(nocalls)
mkfix "$W/fx_ref"; mkdir -p "$CODE/core/.cpp_cache/old"; echo x > "$CODE/core/.cpp_cache/old/READY"; SUBMIT > "$W/s_cache.log" 2>&1; rc=$?
res "refusal: pre-existing core/.cpp_cache (fresh build required) -> exit 2, no sbatch" 2 $rc $(nocalls)
SUBMIT_ARGS="--dry-run --reuse-cache"; SUBMIT > "$W/s_cache2.log" 2>&1; rc=$?
res "pre-existing cache tolerated by the frozen check and allowed with --reuse-cache (dry run) -> exit 0, no sbatch" 0 $rc $(nocalls)
SUBMIT_ARGS=""
mkfix "$W/fx_ref"; mkdir -p "$LOG"; SUBMIT > "$W/s_scr.log" 2>&1; rc=$?
res "refusal: the scratch log folder of this run already exists -> exit 2, no sbatch" 2 $rc $(nocalls)
mkfix "$W/fx_ref"; SUBMIT_ARGS="--throttle-p1000 60 --throttle-p500 50"; SUBMIT > "$W/s_thr1.log" 2>&1; rc=$?
res "refusal: own throttles 60 + 50 > 100 -> exit 2, no sbatch" 2 $rc $(nocalls)
SUBMIT_ARGS=""
printf '9001_[1-600%%60]|smcbvs_other_p1000|PENDING|Dependency\n' > "$SD/queue.psv"; SUBMIT > "$W/s_thr2.log" 2>&1; rc=$?
res "refusal: throttle overflow, another queued campaign SMC array %60 + our 60 > 100 -> exit 2, no sbatch" 2 $rc $(nocalls)
grep -q "combined throttle" "$(reflog)"; res "refusal: throttle overflow is reported as such, in the scratch refusal log (nothing in home)" 0 $? $([ ! -e "$RD/refusals.log" ] && echo 0 || echo 1)
printf '9001_[1-600]|lowp_p2_smc|PENDING|Priority\n' > "$SD/queue.psv"; SUBMIT > "$W/s_thr3.log" 2>&1; rc=$?
res "refusal: a queued SMC array with NO throttle (unlimited) counts as over the limit (fail closed)" 2 $rc $(nocalls)
{ for i in $(seq 1 41); do echo "9004_$i|smcbvs_x|RUNNING|None"; done; } > "$SD/queue.psv"; SUBMIT > "$W/s_thr4.log" 2>&1; rc=$?
res "refusal: 41 running tasks of another campaign SMC array + our 60 > 100 -> exit 2, no sbatch" 2 $rc $(nocalls)
rm -f "$SD/queue.psv"; SUBMIT SQUEUE_FAIL=1 > "$W/s_thr5.log" 2>&1; rc=$?
res "refusal: squeue fails -> the throttle cannot be established -> exit 2 (fail closed), no sbatch" 2 $rc $(nocalls)
printf '9003_[1-9%%90]|my_other_job|PENDING|Priority\n9005|smcbvs_plain|RUNNING|None\n' > "$SD/queue.psv"; SUBMIT_ARGS="--dry-run"; SUBMIT > "$W/s_thr6.log" 2>&1; rc=$?
res "R2-8 fail closed: an fb31 array whose name does NOT contain 'smc' (my_other_job, %90) still counts: 90 + 60 > 100 -> exit 2, no sbatch" 2 $rc $(nocalls)
printf '9003_[1-9%%3]|trunc|PENDING|Priority\n9006_[1-2]|x|PENDING|Priority\n' > "$SD/queue.psv"; SUBMIT > "$W/s_thr7.log" 2>&1; rc=$?
res "R2-8: a small array with a truncated name (%3) plus an unlimited array named x (9006_[1-2], no %N) -> both counted, refused -> exit 2" 2 $rc $(nocalls)
printf '9003_[1-9%%41]|any_name_at_all|PENDING|Priority\n9005|smcbvs_plain|RUNNING|None\n' > "$SD/queue.psv"; SUBMIT_ARGS="--dry-run"; SUBMIT > "$W/s_thr8.log" 2>&1; rc=$?
res "R2-8: 41 + 60 > 100 -> exit 2 even for an array named any_name_at_all (a plain job never counts)" 2 $rc $(nocalls)
printf '9005|smcbvs_plain|RUNNING|None\n9007|lowp_p2_smc|RUNNING|None\n' > "$SD/queue.psv"; SUBMIT_ARGS="--dry-run"; SUBMIT > "$W/s_thr9.log" 2>&1; rc=$?
res "R2-8: only plain (non-array) jobs queued -> the default 30 + 30 (D49) passes: dry run exit 0" 0 $rc $(nocalls)
printf '9008_[1-1200%%34]|lowp_prodL_smc|PENDING|Priority\n' > "$SD/queue.psv"; SUBMIT_ARGS="--dry-run"; SUBMIT > "$W/s_thr10.log" 2>&1; rc=$?
res "D49: PROD-L queued at its cap (%34 = 68 billed CPUs) + PROD-H default 30 + 30 = 94 tasks <= 100 (188 billed <= 192): dry run passes (exit 0)" 0 $rc $(nocalls)
printf '9008_[1-1200%%50]|lowp_prodL_smc|PENDING|Priority\n' > "$SD/queue.psv"; SUBMIT_ARGS="--dry-run"; SUBMIT > "$W/s_thr11.log" 2>&1; rc=$?
res "D49: a PROD-L array throttled %50 + PROD-H 60 = 110 > 100: refused (exit 2) -- the task guard counts PROD-L too" 2 $rc $(nocalls)
SUBMIT_ARGS=""; rm -f "$SD/queue.psv"

echo "| **submit.sh: dry run and the exact argument vectors** | | | |" | tee -a "$OUT"
mkfix "$W/fx_main"
COMMON9="--parsable --account=commons --partition=commons --qos=nots_commons --nodes=1 --ntasks=1 --constraint=sapphirerapids --export=NONE --no-requeue --chdir=$LOG"
SUBMIT_ARGS="--dry-run"; SUBMIT > "$W/s_dry.log" 2>&1; rc=$?
res "dry run: exit 0, no sbatch call, nothing created (no launch, config.env, jobs.tsv, scratch folder)" 0 $rc $([ ! -e "$RD/launch" ] && [ ! -e "$RD/config.env" ] && [ ! -e "$RD/jobs.tsv" ] && [ ! -e "$LOG" ] && nocalls || echo 1)
dryv() { grep '^DRY-RUN sbatch' "$W/s_dry.log" | sed -n "$1p"; }
exp_pre="DRY-RUN sbatch $COMMON9 --job-name=smcbvs_${RID}_precompile --cpus-per-task=1 --mem=4G --time=01:00:00 --output=$LOG/slurm/%j.out --error=$LOG/slurm/%j.err $RD/runner/precompile.sbatch $RD"
exp_p1000="DRY-RUN sbatch $COMMON9 --job-name=smcbvs_${RID}_p1000 --cpus-per-task=1 --mem=2G --time=13:42:00 --array=1-600%30 --dependency=afterok:<PRECOMPILE_ID> --kill-on-invalid-dep=yes --output=$LOG/slurm/%A_%a.out --error=$LOG/slurm/%A_%a.err $RD/runner/task.sh $RD"
exp_p500="DRY-RUN sbatch $COMMON9 --job-name=smcbvs_${RID}_p500 --cpus-per-task=1 --mem=2G --time=03:52:00 --array=601-1200%30 --dependency=afterok:<PRECOMPILE_ID> --kill-on-invalid-dep=yes --output=$LOG/slurm/%A_%a.out --error=$LOG/slurm/%A_%a.err $RD/runner/task.sh $RD"
norm() { sed 's/\\//g'; }       # printf %q escapes only characters that need it; none of these paths do
res "dry run: precompile vector (1 CPU, 4G, 01:00:00, sapphirerapids, --export=NONE, --no-requeue, account/partition commons)" "$exp_pre" "$(dryv 1 | norm)"
res "dry run: p1000 array vector (tasks 1-600, %30 (D49), 2G, 13:42:00, afterok precompile, logs on scratch)" "$exp_p1000" "$(dryv 2 | norm)"
res "dry run: p500 array vector (tasks 601-1200, %30 (D49), 2G, 03:52:00, afterok precompile, logs on scratch)" "$exp_p500" "$(dryv 3 | norm)"

echo "| **submit.sh: real submission (stub sbatch)** | | | |" | tee -a "$OUT"
SUBMIT_ARGS=""; rm -f "$SD"/sbatch_*; echo 0 > "$SD/n"
SUBMIT > "$W/s_real.log" 2>&1; rc=$?
res "submission: exit 0 with exactly 3 sbatch calls (precompile, p1000, p500)" 0 $rc $([ "$(ncalls)" = 3 ] && echo 0 || echo 1)
getcall() { awk -v n="$1" 'BEGIN { c = 1 } /^---$/ { c++; next } c == n { printf "%s%s", (s++ ? " " : ""), $0 }' "$SD/sbatch_argv.txt"; }
res "submission: precompile argument vector is exactly the specified one" "${exp_pre#DRY-RUN sbatch }" "$(getcall 1)"
res "submission: p1000 array vector is exactly the specified one, dependency on the REAL precompile id 7001" "$(echo "${exp_p1000#DRY-RUN sbatch }" | sed 's/<PRECOMPILE_ID>/7001/')" "$(getcall 2)"
res "submission: p500 array vector is exactly the specified one, dependency on 7001" "$(echo "${exp_p500#DRY-RUN sbatch }" | sed 's/<PRECOMPILE_ID>/7001/')" "$(getcall 3)"
res "launch record: guard receipt says GUARD_CHECK_OK; copies of config.env, STAGED list and manifest; 3 recorded vectors" 0 \
  $(grep -q GUARD_CHECK_OK "$RD/launch/guard_receipt.txt" && [ -s "$RD/launch/config.env" ] && [ -s "$RD/launch/v2_2_1.SHA256SUMS" ] && [ -s "$RD/launch/STAGED_SHA256.txt" ] \
    && [ "$(wc -l < "$RD/launch/sbatch_args.txt")" = 3 ] && [ -s "$RD/launch/effective_env.txt" ] && [ -s "$RD/launch/frozen_check.txt" ] && echo 0 || echo 1)
res "launch record: jobs.tsv holds precompile, primary_p1000, primary_p500 with the three ids" "7001 precompile|7002 primary_p1000|7003 primary_p500" \
  "$(awk -F'\t' 'NR > 1 { printf "%s%s %s", (n++ ? "|" : ""), $1, $2 }' "$RD/jobs.tsv")"
res "launch record: manifest.json has submitted_utc, the code-manifest hash (read from disk), the study-manifest hash and the runner hashes" 0 \
  $(py -3 -c "import json,sys; m=json.load(open(sys.argv[1])); assert m['submitted_utc'] and len(m['code_manifest_sha256'])==64 and len(m['inputs_manifest_sha256'])==64 and 'task.sh' in m['runner_sha256'] and m['jobs']['primary_p500']=='7003'" "$RD/manifest.json" >/dev/null 2>&1; echo $?)
grep -q "^OUTROOT=$FS$" "$RD/config.env" && grep -q "^LOGROOT=$LOG$" "$RD/config.env" && grep -q "^L500=6300$" "$RD/config.env" && grep -q "^L1000=24000$" "$RD/config.env"; res "config.env: OUTROOT/LOGROOT on scratch, L500 = 6300, L1000 = 24000" 0 $?
res "submission: every --output/--error and --chdir is under scratch logs/<RUN_ID>" 0 "$(grep -E '^--(output|error|chdir)=' "$SD/sbatch_argv.txt" | grep -vc "=$LOG")"
SUBMIT > "$W/s_again.log" 2>&1; rc=$?
res "refusal: a second submission of the same run -> exit 2, still 3 sbatch calls" 2 $rc $([ "$(ncalls)" = 3 ] && echo 0 || echo 1)

echo "| **submit.sh: abort mid-chain cancels by explicit id** | | | |" | tee -a "$OUT"
mkfix "$W/fx_abort"; SUBMIT FAIL_AT=3 > "$W/s_ab3.log" 2>&1; rc=$?
res "abort: sbatch rejected at the 3rd call (p500) -> exit 5, 3 attempts" 5 $rc $([ "$(ncalls)" = 3 ] && echo 0 || echo 1)
res "abort: the ids already submitted were cancelled BY EXPLICIT ID (7001, 7002), nothing else" "7001 7002" "$(tr '\n' ' ' < "$SD/scancel_calls.txt" | sed 's/ *$//')"
res "abort: SUBMISSION_ABORTED.txt records the reason and the ids; the failed id is not in jobs.tsv" 0 \
  $(grep -q "fabricated sbatch rejection" "$RD/launch/SUBMISSION_ABORTED.txt" && grep -q "7001 7002" "$RD/launch/SUBMISSION_ABORTED.txt" && [ "$(awk -F'\t' 'NR > 1' "$RD/jobs.tsv" | wc -l)" = 2 ] && echo 0 || echo 1)
res "abort: the scheduler's stderr of the failed call is on SCRATCH (LOGROOT/submit/), not in the home launch folder" 0 \
  $(grep -q "fabricated sbatch rejection" "$LOG/submit/sbatch_p500.err" && ! ls "$RD"/launch/sbatch_*.err >/dev/null 2>&1 && echo 0 || echo 1)
mkfix "$W/fx_abort"; SUBMIT FAIL_AT=1 > "$W/s_ab1.log" 2>&1; rc=$?
res "abort: sbatch rejected at the 1st call -> exit 5, one attempt, no scancel" 5 $rc $([ "$(ncalls)" = 1 ] && [ ! -s "$SD/scancel_calls.txt" ] && echo 0 || echo 1)
mkfix "$W/fx_abort"; SUBMIT BAD_ID_AT=2 > "$W/s_abid.log" 2>&1; rc=$?
res "abort: an unparsable sbatch answer (2nd call) -> exit 5, the first id is cancelled by explicit id" 5 $rc $([ "$(tr '\n' ' ' < "$SD/scancel_calls.txt" | sed 's/ *$//')" = "7001" ] && echo 0 || echo 1)

mkfix "$W/fx_abort"; SUBMIT BREAK_JOURNAL="$RD/jobs.tsv" BREAK_AT=2 > "$W/s_abj.log" 2>&1; rc=$?
res "R2-7: sbatch ACCEPTS the 2nd call (7002) but the jobs.tsv append fails -> abort path, exit 5, no 3rd sbatch call" 5 $rc $([ "$(ncalls)" = 2 ] && echo 0 || echo 1)
res "R2-7: the accepted job AND the earlier one are cancelled BY EXPLICIT ID (7001 7002); the reason and 'scancel 7002 ok' are in SUBMISSION_ABORTED.txt" "7001 7002" "$(tr '\n' ' ' < "$SD/scancel_calls.txt" | sed 's/ *$//')" \
  $(grep -q "7002 (p1000) was accepted but recording it in jobs.tsv failed" "$RD/launch/SUBMISSION_ABORTED.txt" && grep -q "scancel 7002 ok" "$RD/launch/SUBMISSION_ABORTED.txt" && echo 0 || echo 1)
mkfix "$W/fx_abort"; printf '#!/bin/bash\necho "scancel denied" >&2; exit 9\n' > "$BIN/scancel_bad"; chmod +x "$BIN/scancel_bad"
SUBMIT BREAK_JOURNAL="$RD/jobs.tsv" BREAK_AT=1 SCANCEL="$BIN/scancel_bad" > "$W/s_abj2.log" 2>&1; rc=$?
res "R2-7: a CANCEL FAILURE after a journal failure is recorded visibly (stderr and SUBMISSION_ABORTED.txt) and the exit is still 5" 5 $rc \
  $(grep -q "CANCEL FAILED for job 7001" "$RD/launch/SUBMISSION_ABORTED.txt" && grep -q "CANCEL FAILED for job 7001" "$W/s_abj2.log" && grep -q "AT LEAST ONE CANCEL FAILED" "$RD/launch/SUBMISSION_ABORTED.txt" && echo 0 || echo 1)

# ---- the state of fx_main continues in test_shell2.sh ----
mkfix "$W/fx_main"      # recreate so part 2 starts from a clean, submitted fixture
SUBMIT > "$W/s_main.log" 2>&1
source "$HERE/test_shell2.sh"

echo; echo "test_shell: $PASS passed, $FAIL failed"
exit $((FAIL > 0))
