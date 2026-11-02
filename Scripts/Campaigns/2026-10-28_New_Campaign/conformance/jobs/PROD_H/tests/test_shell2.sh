#!/bin/bash
# test_shell2.sh -- part 2 of test_shell.sh (sourced by it; uses its helpers and variables): precompile, array tasks, rerun, P5, accounting,
# manifests, staging. Starts from a submitted fixture ($FX/fx_main: run folder $RD, scratch $FS, job ids 7001-7003).
runtask() { # runtask SCRIPT TASKID JOBID [UNITS_FILE]
  nenv SLURM_JOB_ID=$3 SLURM_ARRAY_JOB_ID=$3 SLURM_ARRAY_TASK_ID=$2 SLURM_CPUS_PER_TASK=1 -- bash "$RD/runner/$1" "$RD" ${4:+"$4"} > "$W/task_$1_$2_$3.log" 2>&1; }
STUDYM=$(mixed "$STUDY")
att() { echo "$LOG/attempts/$1/attempt_$2.$3"; }
cmdof() { sed -n 's/.*"command":"\([^"]*\)".*/\1/p' "$1"; }

echo "| **precompile and array tasks (stub Rscript)** |" | tee -a "$OUT"
runtask task.sh 1 7002; rc=$?
res "task before precompile: refuses (exit 66), no fit, no attempt record" 66 $rc $([ ! -e "$LOG/attempts" ] && [ ! -s "$SD/runcase_calls.txt" ] && echo 0 || echo 1)
nenv SLURM_JOB_ID=7001 SLURM_CPUS_PER_TASK=1 -- bash "$RD/runner/precompile.sbatch" "$RD" > "$W/precompile.log" 2>&1; rc=$?
KEY=ab12cd34ef56ab12cd34ef56ab12cd34ef56ab12cd34ef56ab12cd34ef56ab12
res "precompile.sbatch: exit 0, precompile.ok holds the compiled_key, cache READY, env record and compile log on scratch" 0 $rc \
  $(grep -q "^compiled_key $KEY" "$RD/precompile.ok" && [ -f "$CODE/core/.cpp_cache/${KEY:0:16}/READY" ] && ls "$LOG"/precompile/env_record_7001.txt "$LOG"/precompile/compile_7001.log >/dev/null 2>&1 && grep -q "so_sha256" "$RD/precompile.ok" && echo 0 || echo 1)
nenv -- bash -c "source '$RD/runner/frozen_check.sh'; nc_check_frozen '$CODE' '$FH/code/core/v2_2_1.SHA256SUMS'" > /dev/null 2>&1
res "after the precompile the frozen check still passes (only core/.cpp_cache was added)" 0 $?
nenv SLURM_JOB_ID=7001 SLURM_CPUS_PER_TASK=1 -- bash "$RD/runner/precompile.sbatch" "$RD" > /dev/null 2>&1; rc=$?
res "precompile.sbatch refuses a second run (precompile.ok exists): exit 65" 65 $rc
# --- p1000 task 1, then p500 task 601
runtask task.sh 1 7002; rc=$?
res "task 1 (p1000, dataset S1 r001): exit 0, both fits ran, c100 before c050" 0 $rc $([ "$(wc -l < "$SD/runcase_calls.txt")" = 2 ] && head -n 1 "$SD/runcase_calls.txt" | grep -q -- "--scale c100" && tail -n 1 "$SD/runcase_calls.txt" | grep -q -- "--scale c050" && echo 0 || echo 1)
V=$W/vectors.txt; : > "$V"
for u in p1000_S1_r001_c100 p1000_S1_r001_c050; do
  e="Rscript --vanilla $CODE/study/run_case.R --case ${u%_c*} --scale c${u##*_c} --study $STUDYM --outroot $FS --run-id $RID --core-dir $CODE/core --mem-gb 2 --hours 6.666666667"
  res "exact Rscript vector, $u (L = 24000 s -> --hours 6.666666667, --mem-gb 2, no seed, no extra flag)" "$e" "$(cmdof "$(att $u 1 start.json)")"
  cmdof "$(att $u 1 start.json)" >> "$V"
  res "attempt record for $u: end record done:true, exit 0; result files in results/<RUN_ID>/p1000/<case_id>/" 0 \
    $(grep -q '"done":true' "$(att $u 1 end.json)" && grep -q '"exit":0' "$(att $u 1 end.json)" && [ -f "$FS/results/$RID/p1000/$u/SMCBVS.done" ] && [ -s "$(att $u 1 log)" ] && echo 0 || echo 1)
done
runtask task.sh 601 7003; rc=$?
u=p0500_S1_r001_c100; e="Rscript --vanilla $CODE/study/run_case.R --case p0500_S1_r001 --scale c100 --study $STUDYM --outroot $FS --run-id $RID --core-dir $CODE/core --mem-gb 2 --hours 1.75"
res "task 601 (p500): exact Rscript vector (L = 6300 s -> --hours 1.75), result under results/<RUN_ID>/p0500/" "$e" "$(cmdof "$(att $u 1 start.json)")" $([ -f "$FS/results/$RID/p0500/$u/SMCBVS.done" ] && echo 0 || echo 1)
cmdof "$(att $u 1 start.json)" >> "$V"; cmdof "$(att p0500_S1_r001_c050 1 start.json)" >> "$V"
res "no vector of the primary tasks carries a seed argument" 0 "$(grep -c -e '--seed' "$V")"
echo resource_limit > "$SD/mode_p1000_S2_r001_c100"; echo fail1 > "$SD/mode_p1000_S2_r001_c050"
runtask task.sh 2 7002; rc=$?
res "task 2: a saved resource_limit (run_case exit 2) and an infrastructure exit 1 are recorded per unit; the task itself exits 0" 0 $rc \
  $(grep -q '"done":true' "$(att p1000_S2_r001_c100 1 end.json)" && grep -q '"exit":2' "$(att p1000_S2_r001_c100 1 end.json)" && grep -q '"v3_status":"resource_limit"' "$(att p1000_S2_r001_c100 1 end.json)" \
     && grep -q '"done":false' "$(att p1000_S2_r001_c050 1 end.json)" && grep -q '"exit":1' "$(att p1000_S2_r001_c050 1 end.json)" && echo 0 || echo 1)
cp "$CODE/core/v3.R" "$W/v3.R.bak"; echo "# tamper" >> "$CODE/core/v3.R"
runtask task.sh 3 7002; rc=$?
res "task refuses a tampered frozen tree (exit 67), no fit" 67 $rc $([ ! -d "$LOG/attempts/p1000_S3_r001_c100" ] && echo 0 || echo 1)
cp "$W/v3.R.bak" "$CODE/core/v3.R"
runtask task.sh 1201 7002; rc=$?
res "task with an index outside the tables (1201) refuses: exit 65" 65 $rc
nenv SLURM_JOB_ID=7002 SLURM_ARRAY_TASK_ID=3 SLURM_CPUS_PER_TASK=2 -- bash "$RD/runner/task.sh" "$RD" > /dev/null 2>&1; res "task refuses a non-1-CPU allocation: exit 65" 65 $?
echo "| **rerun.sh: infrastructure failures only, once** |" | tee -a "$OUT"
mkfix "$W/fx_rr"; SUBMIT > "$W/rr_submit.log" 2>&1
nenv SLURM_JOB_ID=7001 SLURM_CPUS_PER_TASK=1 -- bash "$RD/runner/precompile.sbatch" "$RD" > /dev/null 2>&1
mapfile -t CASES < <(tail -n +2 "$RD/tables/units.tsv" | cut -f1)
c0=${CASES[0]}; c2=${CASES[2]}; c4=${CASES[4]}; c6=${CASES[6]}; c8=${CASES[8]}; c21=${CASES[21]}; c40=${CASES[40]}; c1300=${CASES[1300]}
cat > "$W/spec_rr.json" <<EOF
{"default":"ok","modes":{"$c0":"infra","$c2":"resource_limit","$c4":"hardtimeout","$c6":"infra_repeat","$c8":"stalelock","$c21":"none","$c40":"resource_limit","$c1300":"resource_limit"}}
EOF
nenv -- python3 "$HERE/fabricate.py" "$RD" "$(mixed "$W/spec_rr.json")" > "$W/fab_rr.log" 2>&1; res "fixture: 2,400-unit tree fabricated (ok default; infra, 3 resource_limit, hard timeout, infra_repeat, stale lock, orphan)" 0 $?
SACCT_HEAD='JobID|JobName|State|ExitCode|Elapsed|MaxRSS|NodeList|End|AllocCPUS|CPUTimeRAW'
mksacct() { { echo "$SACCT_HEAD"
  echo "7001|pre|COMPLETED|0:0|00:05:00||n1|2026-10-29T12:05:00|1|300"
  echo "7002_1|a|COMPLETED|0:0|01:00:00||n1|2026-10-29T13:00:00|1|3600"
  echo "7002_1.0|$c0|OUT_OF_MEMORY|0:125|00:10:00|2097152K|n1|2026-10-29T12:10:00|1|600"
  echo "7003_601|b|COMPLETED|0:0|00:30:00||n2|2026-10-29T12:30:00|1|1800"
  for x in "$@"; do echo "$x"; done; } > "$SD/sacct.psv"; }
mksacct; rm -f "$SD/queue.psv" "$SD/queue_r.psv"; rm -f "$SD"/sbatch_*; echo 3 > "$SD/n"
RR() { nenv "$@" -- bash "$RD/runner/rerun.sh" $RR_ARGS; }
RR_ARGS=""
printf '7002_5|smcbvs|RUNNING|None\n' > "$SD/queue_r.psv"; cp "$SD/queue_r.psv" "$SD/queue.psv"; RR > "$W/rr1.log" 2>&1; rc=$?
res "rerun refused while a job of this run is queued/running -> exit 2, no sbatch" 2 $rc $(nocalls)
rm -f "$SD/queue_r.psv"; printf '9001_[1-600%%95]|smcbvs_other|PENDING|x\n' > "$SD/queue.psv"; RR > "$W/rr2.log" 2>&1; rc=$?
res "rerun refused at a throttle overflow (another array %95 + 10 > 100) -> exit 2, no sbatch" 2 $rc $(nocalls)
printf '9001_[1-600%%95]|nothing_to_do_with_smc|PENDING|x\n' > "$SD/queue.psv"; RR > "$W/rr2b.log" 2>&1; rc=$?
res "R2-8: rerun throttle counts ANY fb31 array whatever its name (nothing_to_do_with_smc %95 + 10 > 100) -> exit 2, no sbatch" 2 $rc $(nocalls)
rm -f "$SD/queue.psv"; RR FAKE_HOME_GB=9.6 > "$W/rr3.log" 2>&1; rc=$?
res "rerun refused when the guard refuses -> exit 1, no sbatch" 1 $rc $(nocalls)
RR NC_LOCAL_TEST=0 > "$W/rr4.log" 2>&1; rc=$?
res "rerun refuses a test hook in a non-test environment -> exit 2" 2 $rc $(nocalls)
RR_ARGS="--dry-run"; RR > "$W/rr5.log" 2>&1; rc=$?
res "rerun --dry-run selects exactly the infrastructure unit and the orphan (lock-held unit only warned), no sbatch, lock untouched" 0 $rc \
  $(grep -q "^$c0"$'\t' "$W/rr5.log" && grep -q "^$c21"$'\t' "$W/rr5.log" && ! grep -q "^$c8"$'\t' "$W/rr5.log" && grep -q "lock still present" "$W/rr5.log" && [ -d "$FS/results/$RID/p1000/$c8/SMCBVS.lock" ] && nocalls | grep -q 0 && echo 0 || echo 1)
RR_ARGS=""
# --- R2-7: sbatch ACCEPTS the rerun array, then the jobs.tsv append fails: the accepted job is cancelled by its explicit id
cp "$RD/jobs.tsv" "$W/jobs.rr.bak"
rr_restore() { rm -rf "$RD/jobs.tsv"; cp "$W/jobs.rr.bak" "$RD/jobs.tsv"; rm -rf "$W/$1"; mv "$RD/rerun_1" "$W/$1"; rm -f "$SD"/sbatch_* "$SD/scancel_calls.txt"; echo 3 > "$SD/n"; }
RR BREAK_JOURNAL="$RD/jobs.tsv" BREAK_AT=4 > "$W/rr6j.log" 2>&1; rc=$?
res "R2-7: rerun.sh: sbatch ACCEPTS (7004) but the jobs.tsv append fails -> exit 5, the job is cancelled BY EXPLICIT ID (7004 only), ABORTED.txt says so, no submitted.json" 5 $rc \
  $([ "$(tr '\n' ' ' < "$SD/scancel_calls.txt" | sed 's/ *$//')" = 7004 ] && grep -q "job 7004 was accepted but recording it in jobs.tsv failed" "$RD/rerun_1/ABORTED.txt" && grep -q "scancel 7004 ok" "$RD/rerun_1/ABORTED.txt" && [ ! -e "$RD/rerun_1/submitted.json" ] && echo 0 || echo 1)
rr_restore rerun_1_aborted
RR BREAK_JOURNAL="$RD/jobs.tsv" BREAK_AT=4 SCANCEL="$BIN/scancel_bad" > "$W/rr6k.log" 2>&1; rc=$?
res "R2-7: rerun.sh: a CANCEL FAILURE after the journal failure is recorded visibly (stderr and ABORTED.txt), exit still 5" 5 $rc \
  $(grep -q "CANCEL FAILED for job 7004" "$RD/rerun_1/ABORTED.txt" && grep -q "CANCEL FAILED for job 7004" "$W/rr6k.log" && echo 0 || echo 1)
res "R3-1 (rerun): the failed cancel leaves rerun_1/UNCERTAIN naming job 7004 (the accepted job is not proven terminal), recorded visibly in ABORTED.txt" 0 \
  $(grep -q "^job 7004$" "$RD/rerun_1/UNCERTAIN" && grep -q "UNCERTAIN" "$RD/rerun_1/ABORTED.txt" && echo 0 || echo 1)
rr_restore rerun_1_aborted2
RR > "$W/rr6.log" 2>&1; rc=$?
task_of() { awk -F'\t' -v c="$1" '$1 == c { print $9 }' "$RD/tables/units.tsv"; }
T0=$(task_of $c0); T8=$(task_of $c8); T21=$(task_of $c21); TS=$(printf '%s\n' $T0 $T8 $T21 | sort -n | paste -sd, -)
res "rerun: real run exits 0; the stale lock of the lock-held unit was cleared and logged ON SCRATCH (LOGROOT/locks_cleared.jsonl, nothing in home), then the unit is selected" 0 $rc \
  $([ ! -d "$FS/results/$RID/p1000/$c8/SMCBVS.lock" ] && [ -s "$LOG/locks_cleared.jsonl" ] && [ ! -e "$RD/locks_cleared.jsonl" ] && echo 0 || echo 1)
res "rerun: units.txt = infra + stale-lock + orphan units only (never resource_limit, timeout, infra_repeat, done)" "$(printf '%s\n' $c0 $c8 $c21)" "$(cat "$RD/rerun_1/units.txt")"
exp="--parsable --job-name=smcbvs_${RID}_rerun1 --account=commons --partition=commons --qos=nots_commons --nodes=1 --ntasks=1 --cpus-per-task=1 --mem=4G --time=13:42:00 --constraint=sapphirerapids --export=NONE --no-requeue --chdir=$LOG --array=$TS%10 --output=$LOG/slurm/%A_%a.out --error=$LOG/slurm/%A_%a.err $RD/runner/task.sh $RD $RD/rerun_1/units.txt"
res "rerun: exact sbatch vector (one array over the GLOBAL task indices, %10, --qos=nots_commons, 4G because a step was OUT_OF_MEMORY, --no-requeue, same constraint)" "$exp" "$(getcall 1)"
res "rerun: jobs.tsv gains rerun_1 with the new id" "7004 rerun_1" "$(awk -F'\t' '$2 ~ /^rerun_/ { printf "%s %s", $1, $2 }' "$RD/jobs.tsv")"
res "rerun: the vector is recorded in rerun_1/sbatch_args.txt and the selection in selected.tsv; the scheduler's stderr path is on scratch" 0 $([ -s "$RD/rerun_1/sbatch_args.txt" ] && [ "$(wc -l < "$RD/rerun_1/selected.tsv")" = 3 ] && [ -d "$LOG/submit" ] && ! ls "$RD"/rerun_1/*.err >/dev/null 2>&1 && echo 0 || echo 1)
# the rerun task: runs only listed, eligible units
runtask task.sh $T0 7004 "$RD/rerun_1/units.txt"; rc=$?
res "rerun task: runs the listed unit once more (attempt 2, same seed: no seed argument) and leaves its c050 sibling alone" 0 $rc \
  $([ -f "$(att $c0 2 start.json)" ] && grep -q '"done":true' "$(att $c0 2 end.json)" && [ "$(find "$LOG/attempts" -path "*${c0%_c*}_c050/*" -name 'attempt_*.start.json' | wc -l)" = 1 ] && echo 0 || echo 1)
printf '%s\n' "$c6" > "$W/units_repeat.txt"; n_before=$(wc -l < "$SD/runcase_calls.txt"); runtask task.sh $(task_of $c6) 7004 "$W/units_repeat.txt"
res "rerun task: a unit with two failed attempts (infra_repeat) is NOT run again; the skip is logged" 0 $([ "$(wc -l < "$SD/runcase_calls.txt")" = "$n_before" ] && [ -s "$LOG/attempts/$c6/rerun_skips.jsonl" ] && echo 0 || echo 1)
printf '%s\n' "$c4" > "$W/units_to.txt"; n_before=$(wc -l < "$SD/runcase_calls.txt"); runtask task.sh $(task_of $c4) 7004 "$W/units_to.txt"
res "rerun task: a unit that ended by hard timeout is NOT run again" 0 $([ "$(wc -l < "$SD/runcase_calls.txt")" = "$n_before" ] && [ -s "$LOG/attempts/$c4/rerun_skips.jsonl" ] && echo 0 || echo 1)
# complete the rerun in the fixture, then a second rerun finds nothing
cat > "$W/spec_rr2.json" <<EOF
{"default":"none","rerun_job":"7004","modes":{"$c0":"infra_then_ok","$c8":"infra_then_ok","$c21":"orphan_then_ok"}}
EOF
nenv -- python3 "$HERE/fabricate.py" "$RD" "$(mixed "$W/spec_rr2.json")" > /dev/null 2>&1
n_sb=$(ncalls); RR > "$W/rr7.log" 2>&1; rc=$?
res "second rerun.sh after the rerun finished: nothing infra/orphan left (infra_repeat, timeout, resource_limit are not eligible) -> no sbatch" 0 $rc $([ "$(ncalls)" = "$n_sb" ] && grep -q '"rerun": 0' "$W/rr7.log" && echo 0 || echo 1)

echo "| **P5: the scan as a compute job, one array over the launchable units, one attempt per unit, ever** |" | tee -a "$OUT"
SCANH=$'case_id\tbase\trepeat_m\tprimary_v3_status\tprimary_status\tretry_state\tretry_v3_status\tretry_problem\tretry_artefacts\teligible\tlaunchable'
scanrow() { # scanrow CASE V3 STATE ELIGIBLE LAUNCHABLE [RETRY_V3]
  printf '%s\tSMCBVS\t0\t%s\tfailed,failed\t%s\t%s\tNA\tNA\t%s\t%s\n' "$1" "$2" "$3" "${6:-NA}" "$4" "$5"; }
scanfix() { { echo "$SCANH"; for r in "$@"; do eval "scanrow $r"; done; } > "$SD/p5_scan_fixture.tsv"; }
scan_good() { scanfix "$c2 resource_limit none TRUE TRUE" "$c40 resource_limit none TRUE TRUE" "$c1300 resource_limit none TRUE TRUE" "$c0 completed none FALSE FALSE"; }
scan_good
P5() { nenv STUB_RUN_SCAN=1 "$@" -- bash "$RD/runner/p5_submit.sh" $P5_ARGS; }
SCANRUN() { nenv STUB_RUN_SCAN=1 "$@" -- bash "$RD/runner/p5_scan_run.sh" $SCAN_ARGS; }
p5calls() { cat "$SD/sbatch_calls.txt" 2>/dev/null | awk '/p5_task\.sh/ { n++ } END { print n + 0 }'; }
noarr() { [ "$(p5calls)" = "$1" ] && echo 0 || echo 1; }
klass_of() { awk -F'	' -v c="$1" 'NR == 1 { for (i = 1; i <= NF; i++) h[$i] = i; next } $h["case_id"] == c { print $h["klass"] }' "$RD/reconcile.tsv"; }
ctr() { cat "$SD/n" 2>/dev/null || echo 0; }     # the stub's job-id counter (ids are 7000 + counter); ncalls = number of sbatch calls recorded since the last reset
P5_ARGS=""; n_sb=$(ncalls)
nosb() { [ "$(ncalls)" = "$n_sb" ] && echo 0 || echo 1; }
printf '7004_3|smcbvs|PENDING|None\n' > "$SD/queue_r.psv"; cp "$SD/queue_r.psv" "$SD/queue.psv"; P5 > "$W/p5a.log" 2>&1; rc=$?
res "P5 refused while a job of this run is queued (the rerun array) -> exit 2, no sbatch (no scan job either)" 2 $rc $(nosb)
rm -f "$SD/queue_r.psv" "$SD/queue.psv"; cp "$SD/sacct.psv" "$W/sacct.good"; echo "7003_700|b|RUNNING|0:0|00:30:00||n2||1|1800" >> "$SD/sacct.psv"; P5 > "$W/p5b.log" 2>&1; rc=$?
res "P5 refused while a primary task is not terminal in sacct -> exit 2, no sbatch" 2 $rc $(nosb)
cp "$W/sacct.good" "$SD/sacct.psv"
c30=${CASES[30]}; rm -rf "$FS/results/$RID/p1000/$c30"; echo '{"default":"none","modes":{"'$c30'":"infra"}}' > "$W/spec_open.json"; nenv -- python3 "$HERE/fabricate.py" "$RD" "$(mixed "$W/spec_open.json")" > /dev/null 2>&1
P5 > "$W/p5c.log" 2>&1; rc=$?
res "Q2: P5 still blocks on an INFRA unit (a fresh infrastructure failure awaiting its rerun) -> exit 2, no sbatch, no scan table" 2 $rc $([ ! -e "$RD/p5_scan_primary.tsv" ] && [ "$(klass_of $c30)" = infra ] && nosb || echo 1)
rm -rf "$FS/results/$RID/p1000/$c30" "$LOG/attempts/$c30"
P5 > "$W/p5c2.log" 2>&1; rc=$?
res "Q2: P5 still blocks on an ORPHAN unit (no attempt, no output, nothing queued) -> exit 2, no sbatch, no scan table" 2 $rc $([ ! -e "$RD/p5_scan_primary.tsv" ] && [ "$(klass_of $c30)" = orphan ] && nosb || echo 1)
echo '{"default":"none","modes":{"'$c30'":"ok"}}' > "$W/spec_open.json"; nenv -- python3 "$HERE/fabricate.py" "$RD" "$(mixed "$W/spec_open.json")" > /dev/null 2>&1
printf '7002_30|smcbvs|PENDING|None\n' > "$SD/queue_r.psv"; cp "$SD/queue_r.psv" "$SD/queue.psv"; P5 > "$W/p5c3.log" 2>&1; rc=$?
res "Q2: P5 blocks on a LIVE job (running / not_run / rerun_queued units exist only while a job of the run is queued) -> exit 2, no sbatch" 2 $rc $(nosb); rm -f "$SD/queue_r.psv" "$SD/queue.psv"
P5 FAKE_HOME_GB=9.6 > "$W/p5d.log" 2>&1; rc=$?
res "P5 refused when the guard refuses -> exit 1, no sbatch" 1 $rc $(nosb)
P5 NC_LOCAL_TEST=0 > "$W/p5e.log" 2>&1; rc=$?
res "P5 refuses a test hook in a non-test environment -> exit 2" 2 $rc $(nosb)

# ---- R2-4: the scan is a guarded single-CPU compute job with a completion receipt ---------------------------------------------------------------
SCAN_ARGS="primary"; n0=$(ncalls); SJ=$((7000 + $(ctr) + 1))
SCANRUN > "$W/sc1.log" 2>&1; rc=$?
exp_scan="--parsable --job-name=smcbvs_${RID}_p5scan_primary --account=commons --partition=commons --qos=nots_commons --nodes=1 --ntasks=1 --cpus-per-task=1 --mem=4G --time=01:00:00 --export=NONE --no-requeue --chdir=$LOG --output=$LOG/slurm/%j.out --error=$LOG/slurm/%j.err $RD/runner/p5_scan.sbatch $RD primary"
res "R2-4: p5_scan_run primary: exit 0, ONE sbatch call, exact vector (1 CPU, 4G, 01:00:00, --qos=nots_commons, --no-requeue, --export=NONE, no Sapphire Rapids constraint, logs on scratch)" "$exp_scan" "$(getcall $((n0 + 1)))" $([ "$rc" = 0 ] && [ "$(ncalls)" = $((n0 + 1)) ] && echo 0 || echo 1)
rcpt() { awk -v k="$1" '$1 == k { sub(/^[^ ]+ /, ""); print; exit }' "$RD/p5_scan_primary.receipt"; }
res "R2-4: the completion receipt names phase primary, the scan job id, scanner_exit 0, the table sha256 and row count (4), and the scanner's summary line (launchable=3 locked=0 invalid_inspect=0)" 0 \
  $([ "$(rcpt phase)" = primary ] && [ "$(rcpt job)" = "$SJ" ] && [ "$(rcpt scanner_exit)" = 0 ] && [ "$(rcpt table_sha256)" = "$(sha256sum "$RD/p5_scan_primary.tsv" | cut -d' ' -f1)" ] && [ "$(rcpt rows)" = 4 ] \
    && [[ "$(rcpt summary)" == "p5_scan units=4 primary_resource_limit=3 eligible=3 "*"launchable=3 locked=0 invalid_inspect=0" ]] && echo 0 || echo 1)
res "R2-4/R2-9: the scan job's log is on SCRATCH (LOGROOT/p5_scan/); home holds only the table, the receipt and the job record (no .log); jobs.tsv gains p5scan_primary" 0 \
  $([ -s "$LOG/p5_scan/scan_primary_$SJ.log" ] && grep -q '^p5_scan units=' "$LOG/p5_scan/scan_primary_$SJ.log" && ! ls "$RD"/*.log "$RD"/p5_scan* 2>/dev/null | grep -q '\.log' && [ -s "$RD/p5_scan_primary.job" ] \
    && grep -q "^$SJ"$'\t'"p5scan_primary" "$RD/jobs.tsv" && echo 0 || echo 1)
SCANRUN > "$W/sc2.log" 2>&1; rc=$?
res "R2-4: a second call with a recorded scan job does NOT submit again: it re-verifies (exit 0, still one sbatch call)" 0 $rc $([ "$(ncalls)" = $((n0 + 1)) ] && grep -q "not resubmitted" "$W/sc2.log" && echo 0 || echo 1)
cp "$RD/p5_scan_primary.tsv" "$W/scan_tbl.bak"; echo "tampered" >> "$RD/p5_scan_primary.tsv"; SCANRUN > "$W/sc3.log" 2>&1; rc=$?
res "R2-4: a table changed after the scan (sha256/row count differ from the receipt) is NOT trusted: exit 4" 4 $rc $(grep -q "differs from the receipt" "$W/sc3.log" && echo 0 || echo 1)
cp "$W/scan_tbl.bak" "$RD/p5_scan_primary.tsv"; cp "$RD/p5_scan_primary.receipt" "$W/scan_rcpt.bak"; sed -i 's/^job .*/job 1234/' "$RD/p5_scan_primary.receipt"; SCANRUN > "$W/sc4.log" 2>&1; rc=$?
res "R2-4: a receipt that names another job is NOT trusted: exit 4" 4 $rc $(grep -q "another phase or job" "$W/sc4.log" && echo 0 || echo 1)
cp "$W/scan_rcpt.bak" "$RD/p5_scan_primary.receipt"; rm -f "$RD/p5_scan_primary.job"; SCANRUN > "$W/sc5.log" 2>&1; rc=$?
res "R2-4: a scan table with no recorded scan job is never trusted or overwritten: exit 2, no sbatch" 2 $rc $([ "$(ncalls)" = $((n0 + 1)) ] && echo 0 || echo 1)
rm -f "$RD"/p5_scan_primary.tsv "$RD"/p5_scan_primary.receipt "$RD"/p5_scan_primary.job
n0=$(ncalls); SCANRUN P5SCAN_RC=3 > "$W/sc6.log" 2>&1; rc=$?
res "R2-4: a scan job that FAILS (scanner exit 3) leaves no receipt: the run reports SCAN FAILED, exit 4" 4 $rc $([ ! -e "$RD/p5_scan_primary.receipt" ] && grep -q "SCAN FAILED" "$W/sc6.log" && echo 0 || echo 1)
rm -f "$RD"/p5_scan_primary.*
n0=$(ncalls); SJ=$((7000 + $(ctr) + 1)); printf '%s|smcbvs|RUNNING|None\n' "$SJ" > "$SD/queue_r.psv"
nenv -- bash "$RD/runner/p5_scan_run.sh" primary --no-wait > "$W/sc7.log" 2>&1; rc=$?
res "R2-4: --no-wait with the scan job still running: exit 10, job recorded, nothing else" 10 $rc $([ "$(ncalls)" = $((n0 + 1)) ] && [ -s "$RD/p5_scan_primary.job" ] && echo 0 || echo 1)
P5 NC_SCAN_POLL_S=1 NC_SCAN_MAX_WAIT_S=2 > "$W/sc8.log" 2>&1; rc=$?
res "R2-4: p5_submit while the recorded scan job is still running waits, then exits 10 (the job is reused, nothing resubmitted, no P5 array)" 10 $rc $([ "$(ncalls)" = $((n0 + 1)) ] && noarr 0 | grep -q 0 && echo 0 || echo 1)
rm -f "$SD/queue_r.psv" "$SD/queue.psv"; echo "$SJ|p5scan|COMPLETED|0:0|00:05:00||n1|2026-10-29T17:00:00|1|300" >> "$SD/sacct.psv"
nenv -- bash "$RD/runner/p5_scan_run.sh" primary > "$W/sc9.log" 2>&1; rc=$?
res "R2-4: the scan job COMPLETED in sacct but wrote no table/receipt: not verified, exit 4" 4 $rc $(grep -q "SCAN NOT VERIFIED" "$W/sc9.log" && echo 0 || echo 1)
P5 > "$W/sc10.log" 2>&1; rc=$?
res "R2-4: p5_submit with that unverified scan job: refused (exit 2), the scan record is set aside as failed, no P5 array" 2 $rc $(ls "$RD"/p5_scan_primary.job.failed_* >/dev/null 2>&1 && [ ! -e "$RD/p5_scan_primary.job" ] && noarr 0 | grep -q 0 && echo 0 || echo 1)
rm -f "$RD"/p5_scan_primary.*

# ---- R2-4 selection: launchable == TRUE; refuses on locked / incomplete / invalid_inspect -----------------------------------------------------------
n_sb=$(ncalls)
scanfix "$c2 resource_limit none TRUE TRUE" "$c40 resource_limit none TRUE TRUE" "$c1300 resource_limit none TRUE TRUE" "$c0 completed none FALSE FALSE" "${CASES[100]} resource_limit none TRUE TRUE"
P5 > "$W/p5f.log" 2>&1; rc=$?
res "P5 refused when the scan and reconcile disagree on the resource_limit units -> exit 2, no P5 array, scan record retired" 2 $rc $(noarr 0)
ls "$RD"/p5_scan_primary.tsv.refused_* "$RD"/p5_scan_primary.receipt.refused_* "$RD"/p5_scan_primary.job.refused_* >/dev/null 2>&1; res "P5: the table, receipt and job record of a refused attempt are all set aside (so the legitimate submission writes a fresh set)" 0 $? $([ ! -e "$RD/p5_scan_primary.tsv" ] && echo 0 || echo 1)
for st in locked incomplete invalid_inspect; do
  scanfix "$c2 resource_limit $st TRUE FALSE" "$c40 resource_limit none TRUE TRUE" "$c1300 resource_limit none TRUE TRUE" "$c0 completed none FALSE FALSE"
  P5 > "$W/p5g_$st.log" 2>&1; rc=$?
  res "R2-4: P5 REFUSES while a resource_limit unit is $st (an attempt may have happened: an operator must inspect it) -> exit 2, no P5 array" 2 $rc $(tail -n 1 "$LOG/refusals.log" | grep -q "locked, incomplete or invalid_inspect" && noarr 0 | grep -q 0 && echo 0 || echo 1)
done
scanfix "$c2 resource_limit none TRUE FALSE" "$c40 resource_limit none TRUE TRUE" "$c1300 resource_limit none TRUE TRUE" "$c0 completed none FALSE FALSE"
P5 > "$W/p5h0.log" 2>&1; rc=$?
res "R2-4: a scan row with retry_state none but launchable FALSE is inconsistent -> refused, exit 2" 2 $rc $(tail -n 1 "$LOG/refusals.log" | grep -q "inconsistent" && noarr 0 | grep -q 0 && echo 0 || echo 1)
scanfix "$c2 resource_limit done FALSE FALSE completed" "$c40 resource_limit none TRUE TRUE" "$c1300 resource_limit none TRUE TRUE" "$c0 completed none FALSE FALSE"
P5 > "$W/p5h1.log" 2>&1; rc=$?
res "P5 refused when a resource_limit unit already has a valid P5 retry (at most one attempt per unit, ever) -> exit 2" 2 $rc $(noarr 0)
scan_good
expp5="--parsable --job-name=smcbvs_${RID}_p5 --account=commons --partition=commons --qos=nots_commons --nodes=1 --ntasks=1 --cpus-per-task=1 --mem=4G --time=13:36:00 --constraint=sapphirerapids --export=NONE --no-requeue --chdir=$LOG --array=1-3%3 --output=$LOG/slurm/%A_%a.out --error=$LOG/slurm/%A_%a.err $RD/runner/p5_task.sh $RD"
P5_ARGS="--dry-run"; n_sb=$(ncalls); P5 > "$W/p5dry.log" 2>&1; rc=$?; P5_ARGS=""
res "P5 --dry-run: all gates pass (the scan job ran and its receipt verified), prints the exact vector, no P5 array, no p5/ record, scan artefacts set aside" "DRY-RUN sbatch $expp5" "$(grep '^DRY-RUN sbatch' "$W/p5dry.log" | tr -d '\134')" \
  $([ $rc = 0 ] && [ "$(ncalls)" = $((n_sb + 1)) ] && noarr 0 | grep -q 0 && [ ! -e "$RD/p5" ] && [ ! -e "$RD/p5_scan_primary.tsv" ] && ls "$RD"/p5_scan_primary.tsv.dryrun_* "$RD"/p5_scan_primary.receipt.dryrun_* "$RD"/p5_scan_primary.job.dryrun_* >/dev/null 2>&1 && echo 0 || echo 1)
# ---- R2-7: P5 array accepted, then the journal write fails -> cancelled by explicit id, p5/ABORTED.txt blocks any further P5 submission
cp "$RD/jobs.tsv" "$W/jobs.p5.bak"; rm -f "$SD/scancel_calls.txt"; n1=$(ncalls); k1=$(ctr); PJX=$((7000 + k1 + 2))
P5 BREAK_JOURNAL="$RD/jobs.tsv" BREAK_AT=$((k1 + 2)) > "$W/p5k.log" 2>&1; rc=$?
res "R2-7: P5 array ACCEPTED ($PJX) but the jobs.tsv append fails -> exit 5, cancelled BY EXPLICIT ID (only $PJX), p5/ABORTED.txt says 'scancel $PJX ok', no submitted.json" 5 $rc \
  $([ "$(tr '\n' ' ' < "$SD/scancel_calls.txt" | sed 's/ *$//')" = "$PJX" ] && grep -q "scancel $PJX ok" "$RD/p5/ABORTED.txt" && grep -q "the P5 job $PJX was accepted but recording it" "$RD/p5/ABORTED.txt" && [ ! -e "$RD/p5/submitted.json" ] && echo 0 || echo 1)
P5A0=$(p5calls)
P5 > "$W/p5k2.log" 2>&1; rc=$?
res "R2-7: after the abort every further P5 submission is refused until HQ has looked at p5/ABORTED.txt -> exit 2, no new sbatch call" 2 $rc $([ "$(ncalls)" = $((n1 + 2)) ] && echo 0 || echo 1)
rm -rf "$RD/jobs.tsv"; cp "$W/jobs.p5.bak" "$RD/jobs.tsv"; rm -rf "$W/p5_aborted"; mv "$RD/p5" "$W/p5_aborted"; rm -f "$RD"/p5_scan_primary.tsv "$RD"/p5_scan_primary.receipt "$RD"/p5_scan_primary.job
rm -f "$SD/scancel_calls.txt"; P5 BREAK_JOURNAL="$RD/jobs.tsv" BREAK_AT=$(( $(ctr) + 1 )) SCANCEL="$BIN/scancel_bad" > "$W/p5k3.log" 2>&1; rc=$?
res "R2-7: the scan job accepted but jobs.tsv fails -> the scan job is cancelled by explicit id (a cancel failure is recorded visibly), no P5 array" 2 $rc \
  $(grep -q "CANCEL FAILED for job" "$RD/p5_scan_primary.ABORTED" && noarr $P5A0 | grep -q 0 && echo 0 || echo 1)
rm -rf "$RD/jobs.tsv"; cp "$W/jobs.p5.bak" "$RD/jobs.tsv"; rm -f "$RD"/p5_scan_primary.* "$SD/scancel_calls.txt"
n_sb=$(ncalls)
P5 > "$W/p5i.log" 2>&1; rc=$?
res "P5 submission: exit 0 with exactly two more sbatch calls (the scan job, then ONE P5 array)" 0 $rc $([ "$(ncalls)" = $((n_sb + 2)) ] && [ "$(p5calls)" = $((P5A0 + 1)) ] && echo 0 || echo 1)
PJ=$((7000 + $(cat "$SD/n")))
PA=$(printf '%s\n%s\n%s\n' "$c2" "$c40" "$c1300" | LC_ALL=C sort); P_A=$(echo "$PA" | sed -n 1p); P_B=$(echo "$PA" | sed -n 2p); P_C=$(echo "$PA" | sed -n 3p)
res "P5 selection: only the three launchable resource_limit units, sorted, in p5/units.tsv (select on launchable == TRUE)" "1 $P_A|2 $P_B|3 $P_C" "$(awk -F'\t' 'NR > 1 { printf "%s%s %s", (n++ ? "|" : ""), $1, $2 }' "$RD/p5/units.tsv")"
res "P5 table: units.tsv carries dataset, scale, p and L per unit" "p500 6300 p1000 24000 p1000 24000" "$(awk -F'\t' 'NR > 1 { printf "%sp%s %s", (n++ ? " " : ""), $5, $6 }' "$RD/p5/units.tsv")"
res "P5: exact sbatch vector (ONE array, one unit per task, 4G, wall 2L + margin = 13:36:00, --qos=nots_commons, --no-requeue, same constraint)" "$expp5" "$(getcall $((n_sb + 2)))"
res "P5: jobs.tsv gains the scan job and the p5 job; submitted.json and sbatch_args.txt recorded; the scan table, receipt and job record are kept" 0 \
  $([ "$(awk -F'\t' '$2 == "p5" { print $1 }' "$RD/jobs.tsv")" = "$PJ" ] && [ "$(awk -F'\t' '$2 == "p5scan_primary" { print $1 }' "$RD/jobs.tsv" | tail -n 1)" = "$((PJ - 1))" ] \
    && [ -s "$RD/p5/submitted.json" ] && [ -s "$RD/p5/sbatch_args.txt" ] && [ -s "$RD/p5_scan_primary.tsv" ] && [ -s "$RD/p5_scan_primary.receipt" ] && echo 0 || echo 1)
res "Q2: timeout and infra_repeat units did NOT block P5; they are listed for HQ in p5_exceptions_for_HQ.tsv, are never selected, and are named in the submission output" 0 \
  $(awk -F'\t' -v a="$c4" -v b="$c6" 'NR > 1 { n++; k[$1] = $3 } END { exit !(n == 2 && k[a] == "timeout" && k[b] == "infra_repeat") }' "$RD/p5_exceptions_for_HQ.tsv" \
    && ! grep -q -e "$c4" -e "$c6" "$RD/p5/units.tsv" && grep -q "terminal exceptions listed for HQ (not blocking P5, never retried): 2 unit" "$W/p5i.log" && echo 0 || echo 1)
res "Q1: EVERY sbatch call of this fixture (rerun, scan jobs, P5 array) carries --qos=nots_commons" 0 "$(grep -vc -e '--qos=nots_commons' "$SD/sbatch_calls.txt")"
P5 > "$W/p5j.log" 2>&1; rc=$?
res "second P5 submission refused: one P5 array per run, ever -> exit 2" 2 $rc $([ "$(p5calls)" = $((P5A0 + 1)) ] && echo 0 || echo 1)
mv "$RD/p5/submitted.json" "$W/submitted.json.bak"; mkdir -p "$LOG/p5_attempts"; echo '{}' > "$LOG/p5_attempts/$P_A.start.json"; n_sb=$(ncalls)
P5 > "$W/p5l.log" 2>&1; rc=$?
res "P5 refused when a durable attempt record exists (even without submitted.json): a second attempt of a unit is impossible -> exit 2 (reason in the SCRATCH refusal log)" 2 $rc $([ "$(ncalls)" = "$n_sb" ] && grep -q "attempt record" "$LOG/refusals.log" && [ ! -e "$RD/refusals.log" ] && echo 0 || echo 1)
rm -f "$LOG/p5_attempts/$P_A.start.json"; mv "$W/submitted.json.bak" "$RD/p5/submitted.json"
# --- the P5 tasks (P_C is hard-killed: SIGKILL emulation, exit 137, lock + temporary file left behind)
echo resource_limit > "$SD/pmode_$P_B"; echo killlock > "$SD/pmode_$P_C"; : > "$SD/runcase_calls.txt"
runtask p5_task.sh 1 $PJ; rc=$?
ds=${P_A%_c*}; sc=c${P_A##*_c}
e="Rscript --vanilla $CODE/study/run_case.R --case $ds --scale $sc --study $STUDYM --outroot $FS --run-id $RID --core-dir $CODE/core --mem-gb 2 --hours 1.75 --p5-retry"
res "P5 task 1 (p500): exact vector = primary CLI + --p5-retry with the PRIMARY --mem-gb 2 --hours 1.75 (the adapter doubles them)" "$e" "$(sed -n 's/.*"command":"\([^"]*\)".*/\1/p' "$LOG/p5_attempts/$P_A.start.json")" $rc
sed -n 's/.*"command":"\([^"]*\)".*/\1/p' "$LOG/p5_attempts/$P_A.start.json" >> "$V"
runtask p5_task.sh 2 $PJ; rc=$?
ds=${P_B%_c*}; sc=c${P_B##*_c}
e="Rscript --vanilla $CODE/study/run_case.R --case $ds --scale $sc --study $STUDYM --outroot $FS --run-id $RID --core-dir $CODE/core --mem-gb 2 --hours 6.666666667 --p5-retry"
res "P5 task 2 (p1000): exact vector with --hours 6.666666667 --p5-retry" "$e" "$(sed -n 's/.*"command":"\([^"]*\)".*/\1/p' "$LOG/p5_attempts/$P_B.start.json")" $rc
sed -n 's/.*"command":"\([^"]*\)".*/\1/p' "$LOG/p5_attempts/$P_B.start.json" >> "$V"
runtask p5_task.sh 3 $PJ; rc=$?
pdir() { echo "$FS/results/$RID/p$(printf '%04d' "$((10#${1:1:4}))")/$1/P5_retry"; }
res "P5 task 3: the child is SIGKILLed (exit 137): the task itself exits 0, writes the end record (exit 137, done false, lock_left true) and leaves the lock + temporary file in P5_retry/" 0 $rc \
  $(grep -q '"exit":137' "$LOG/p5_attempts/$P_C.end.json" && grep -q '"done":false' "$LOG/p5_attempts/$P_C.end.json" && grep -q '"lock_left":true' "$LOG/p5_attempts/$P_C.end.json" && [ -d "$(pdir $P_C)/SMCBVS_p5retry.lock" ] && [ -f "$(pdir $P_C)/SMCBVS_p5retry.rds.tmp.4242" ] && echo 0 || echo 1)
res "P5 retry files are written to <case>/P5_retry/ (outside the primary files) and the primary record is untouched" 0 \
  $([ -f "$(pdir $P_A)/SMCBVS_p5retry.done" ] && [ -f "$(pdir $P_B)/SMCBVS_p5retry.done" ] && [ ! -f "$(pdir $P_C)/SMCBVS_p5retry.done" ] && grep -q resource_limit "$FS/results/$RID/p1000/$P_B/SMCBVS.csv" 2>/dev/null; echo $?)
n_before=$(wc -l < "$SD/runcase_calls.txt"); runtask p5_task.sh 1 $PJ; rc=$?
res "P5 task run a SECOND time for the same unit: refused by the attempt record (exit 0, no Rscript call, refusal logged)" 0 $rc \
  $([ "$(wc -l < "$SD/runcase_calls.txt")" = "$n_before" ] && [ -s "$LOG/p5_attempts/$P_A.refused.jsonl" ] && grep -q "at most one P5 attempt" "$W/task_p5_task.sh_1_${PJ}.log" && echo 0 || echo 1)
n_before=$(wc -l < "$SD/runcase_calls.txt"); runtask p5_task.sh 3 $PJ; rc=$?
res "the SIGKILLed P5 unit is never relaunched (a second task for it: refused, no Rscript call)" 0 $rc $([ "$(wc -l < "$SD/runcase_calls.txt")" = "$n_before" ] && echo 0 || echo 1)
rc=0; nenv -- python3 "$RD/runner/reconcile.py" "$RD" --sacct > "$W/rec_after_p5.json" 2>&1 || rc=$?
res "reconcile after P5: the 'p5' section reports two valid retries and the killed one as incomplete; the primary classes are those of the rerun-complete state" 0 $rc \
  $(py -3 -c "import json,sys; j=json.loads(open(sys.argv[1]).read().strip().splitlines()[-1]); assert j['p5']['states']=={'valid':2,'incomplete':1}, j['p5']; assert j['outcomes']['resource_limit']==3 and j['classes']['timeout']==1 and j['classes']['infra_repeat']==1 and j['classes']['done']==2398, j" "$W/rec_after_p5.json" >/dev/null 2>&1; echo $?)
# final scan: the killed unit is reported (never retried a second time)
scanfix "$P_A resource_limit done FALSE FALSE completed" "$P_B resource_limit done FALSE FALSE resource_limit" "$P_C resource_limit locked TRUE FALSE"
n_sb=$(ncalls); SCAN_ARGS="final"; SCANRUN > "$W/p5final.log" 2>&1; rc=$?
res "p5_scan_run final (a scan job again): every selected unit has a valid retry record or is REPORTED (2 valid, 1 reported: the SIGKILLed unit); the NOTE names cleanup_terminal.sh" 0 $rc \
  $(grep -q "selected 3, valid retry record 2, reported (no valid record) 1" "$W/p5final.log" && grep -q "cleanup_terminal.sh" "$W/p5final.log" && [ "$(ncalls)" = $((n_sb + 1)) ] \
    && [ "$(awk -F'\t' -v c="$P_C" '$1 == c { print $2 "/" $6 }' "$RD/p5_final_report.tsv")" = "locked/YES" ] && [ -s "$RD/p5_scan_final.receipt" ] && echo 0 || echo 1)
SCANRUN > "$W/p5final2.log" 2>&1; rc=$?
res "p5_scan_run final again: the recorded job is re-verified, not resubmitted (exit 0)" 0 $rc $([ "$(ncalls)" = $((n_sb + 1)) ] && echo 0 || echo 1)
rm -f "$RD/p5_scan_final.job"; SCANRUN > "$W/p5final3.log" 2>&1; rc=$?
res "p5_scan_run final: an existing scan table without its job record is never overwritten: exit 2" 2 $rc

echo "| **final accounting** |" | tee -a "$OUT"
mksacct_all() {   # the base rows plus one row per recorded rerun / P5 array / scan job (terminal)
  local rows=() id kind rest
  while IFS=$'\t' read -r id kind rest; do
    case "$kind" in
      rerun_*) rows+=("${id}_1|r|COMPLETED|0:0|00:30:00||n1|2026-10-29T14:00:00|1|1800");;
      p5) rows+=("${id}_1|p|COMPLETED|0:0|01:00:00||n1|2026-10-29T15:00:00|1|3600" "${id}_1.0|$P_A|COMPLETED|0:0|01:00:00|1048576K|n1|2026-10-29T15:00:00|1|3600"
                 "${id}_2|p|COMPLETED|0:0|02:00:00||n1|2026-10-29T16:00:00|1|7200" "${id}_3|p|FAILED|137:0|00:30:00||n1|2026-10-29T16:30:00|1|1800");;
      p5scan_*) rows+=("${id}|scan|COMPLETED|0:0|00:05:00||n1|2026-10-29T17:00:00|1|300");;
    esac
  done < <(tail -n +2 "$RD/jobs.tsv")
  mksacct "${rows[@]}"; }
mksacct_all; cp "$SD/sacct.psv" "$W/sacct.base"
FA() { nenv "$@" -- bash "$RD/runner/final_accounting.sh"; }
printf '%s_2|smcbvs|RUNNING|None\n' "$PJ" > "$SD/queue_r.psv"; FA > "$W/fa1.log" 2>&1; rc=$?
res "final_accounting refuses while a job is still in the queue: exit 1" 1 $rc; rm -f "$SD/queue_r.psv"
cp "$SD/sacct.psv" "$W/sacct.full"; sed -i "s/^${PJ}_2|p|COMPLETED/${PJ}_2|p|RUNNING/" "$SD/sacct.psv"; FA > "$W/fa2.log" 2>&1; rc=$?
res "final_accounting: a task that sacct still shows RUNNING -> NOT TERMINAL, exit 1" 1 $rc; cp "$W/sacct.full" "$SD/sacct.psv"
grep -v "^${PJ}" "$W/sacct.full" > "$SD/sacct.psv"; FA > "$W/fa3.log" 2>&1; rc=$?
res "final_accounting: a recorded job (the P5 array) missing from the snapshot -> exit 2 (never silent)" 2 $rc; cp "$W/sacct.full" "$SD/sacct.psv"
FA > "$W/fa4.log" 2>&1; rc=$?
res "final_accounting: terminal snapshot of EVERY job id written (home and logs folder)" 0 $rc $([ -s "$RD/accounting/sacct_final.tsv" ] && [ -s "$LOG/accounting/sacct_final.tsv" ] && [ "$(head -1 "$RD/accounting/sacct_final.tsv")" = "JobID|JobName|State|ExitCode|Elapsed|NodeList|MaxRSS|AllocCPUS|CPUTimeRAW" ] && echo 0 || echo 1)
NSCAN=$(awk -F'\t' '$2 ~ /^p5scan_/' "$RD/jobs.tsv" | wc -l)
res "final_accounting: core-hours by array (precompile 0.08, p1000 1.0, p500 0.5, reruns 0.5, P5 3.5 CPU-h, scan jobs $NSCAN x 300 s) and the two ceilings (native-fit-budget 10,100; requested-wall 10,540 / 10,541)" 0 \
  $(py -3 -c "import json,sys; j=json.load(open(sys.argv[1])); n=int(sys.argv[2]); assert (j['precompile']['alloc_cpu_hours'],j['primary_p1000']['alloc_cpu_hours'],j['primary_p500']['alloc_cpu_hours'],j['reruns']['alloc_cpu_hours'],j['p5']['alloc_cpu_hours'])==(0.08,1.0,0.5,0.5,3.5), j; assert j['p5']['max_step_maxrss_mb']==1024.0; assert j['p5scan']['tasks']==n and j['p5scan']['alloc_cpu_hours']==round(n*300/3600,2), j['p5scan']; assert j['total']['native_fit_budget_ceiling_core_hours']==10100 and j['total']['requested_wall_ceiling_primary_core_hours']==10540 and j['total']['requested_wall_ceiling_with_precompile_core_hours']==10541, j['total']" "$RD/accounting/core_hours.json" "$NSCAN" >/dev/null 2>&1; echo $?)

echo "| **cleanup_terminal.sh: SIGKILLed P5 attempt -> final scan -> cleanup -> manifests (R2-5, R2-6)** |" | tee -a "$OUT"
CT() { nenv "$@" -- bash "$RD/runner/cleanup_terminal.sh" $CT_ARGS; }
MM() { nenv "$@" -- bash "$RD/runner/make_manifests.sh"; }
LK="$(pdir $P_C)/SMCBVS_p5retry.lock"; TMPF="$(pdir $P_C)/SMCBVS_p5retry.rds.tmp.4242"
att_count() { find "$LOG/attempts" "$LOG/p5_attempts" -type f | wc -l; }
CT_ARGS=""
printf '%s_3|smcbvs|RUNNING|None\n' "$PJ" > "$SD/queue_r.psv"; CT > "$W/ct1.log" 2>&1; rc=$?
res "R2-5: cleanup REFUSES while a recorded job is still queued/running -> exit 2, the lock and the temporary file are untouched" 2 $rc $([ -d "$LK" ] && [ -f "$TMPF" ] && echo 0 || echo 1); rm -f "$SD/queue_r.psv"
sed -i "s/^${PJ}_3|p|FAILED/${PJ}_3|p|RUNNING/" "$SD/sacct.psv"; CT > "$W/ct2.log" 2>&1; rc=$?
res "R2-5: cleanup REFUSES when sacct shows a task that is not terminal -> exit 2, nothing touched" 2 $rc $([ -d "$LK" ] && [ -f "$TMPF" ] && echo 0 || echo 1); cp "$W/sacct.full" "$SD/sacct.psv"
grep -v "^${PJ}" "$W/sacct.full" > "$SD/sacct.psv"; CT > "$W/ct3.log" 2>&1; rc=$?
res "R2-5: cleanup REFUSES when a recorded job is missing from sacct (state unknown, fail closed) -> exit 2" 2 $rc $([ -d "$LK" ] && echo 0 || echo 1); cp "$W/sacct.full" "$SD/sacct.psv"
CT SQUEUE_FAIL=1 > "$W/ct4.log" 2>&1; rc=$?
res "R2-5: cleanup REFUSES when squeue fails (fail closed) -> exit 2" 2 $rc $([ -d "$LK" ] && echo 0 || echo 1)
MM > "$W/mm_stale.log" 2>&1; rc=$?
res "R2-6: make_manifests with the killed attempt's lock/temporary file in the LATER folder (p1000): refused (exit 2), names cleanup_terminal.sh, and NOTHING was written: no manifest in p0500, p1000 or logs, no summary, no home manifest" 2 $rc \
  $(grep -q "cleanup_terminal.sh" "$W/mm_stale.log" && [ ! -e "$FS/results/$RID/p0500/MANIFEST.sha256" ] && [ ! -e "$FS/results/$RID/p1000/MANIFEST.sha256" ] && [ ! -e "$LOG/MANIFEST.sha256" ] && [ ! -e "$RD/manifests/summary.tsv" ] && [ ! -e "$RD/HOME_MANIFEST.sha256" ] && echo 0 || echo 1)
n_att=$(att_count); n_rc=$(wc -l < "$SD/runcase_calls.txt"); n_sb=$(ncalls)
CT_ARGS="--dry-run"; CT > "$W/ct5.log" 2>&1; rc=$?; CT_ARGS=""
res "R2-5: cleanup --dry-run lists both artefacts as WOULD ARCHIVE (proven stale: P5 attempt record of this run's array), moves nothing" 0 $rc \
  $([ "$(grep -c '^WOULD ARCHIVE' "$W/ct5.log")" = 2 ] && grep -q "p5 $PJ" "$W/ct5.log" && [ -d "$LK" ] && [ -f "$TMPF" ] && [ ! -e "$LOG/cleanup" ] && echo 0 || echo 1)
CT > "$W/ct6.log" 2>&1; rc=$?
ARCH=$(ls -d "$LOG"/cleanup/*/ 2>/dev/null | head -n 1); ARCH=${ARCH%/}
res "R2-5: cleanup archives the lock (with owner.txt) and the temporary file under LOGROOT/cleanup/<utc>/, CLEANUP_LOG.tsv, a small receipt in home; they are gone from the results tree" 0 $rc \
  $([ ! -e "$LK" ] && [ ! -e "$TMPF" ] && [ -s "$ARCH/p1000/$P_C/P5_retry/SMCBVS_p5retry.lock.archived/owner.txt" ] && [ -s "$ARCH/p1000/$P_C/P5_retry/SMCBVS_p5retry.rds_tmp.4242.archived" ] \
    && [ "$(grep -c PROVEN_STALE "$ARCH/CLEANUP_LOG.tsv")" = 2 ] && ls "$RD"/cleanup/cleanup_*.tsv >/dev/null 2>&1 && echo 0 || echo 1)
res "R2-5: the durable attempt records are kept (same file count, the killed unit's start/end records included), the other P5 retries and all result files are untouched, and NO fit was relaunched" 0 \
  $([ "$(att_count)" = "$n_att" ] && [ -s "$LOG/p5_attempts/$P_C.start.json" ] && [ -s "$LOG/p5_attempts/$P_C.end.json" ] && [ -f "$(pdir $P_A)/SMCBVS_p5retry.done" ] && [ -f "$(pdir $P_B)/SMCBVS_p5retry.done" ] \
    && [ "$(wc -l < "$SD/runcase_calls.txt")" = "$n_rc" ] && [ "$(ncalls)" = "$n_sb" ] && echo 0 || echo 1)
CT > "$W/ct7.log" 2>&1; rc=$?
res "R2-5: a second cleanup finds nothing left (exit 0, idempotent)" 0 $rc $(grep -q "0 lock/temporary artefact" "$W/ct7.log" && echo 0 || echo 1)
mkdir -p "$(pdir $c0)/SMCBVS_p5retry.lock"; printf 'pid 999999999\nhost deadnode\nutc x\n' > "$(pdir $c0)/SMCBVS_p5retry.lock/owner.txt"; CT > "$W/ct8.log" 2>&1; rc=$?
res "R2-5: an artefact that is NOT proven stale (a P5 lock of a unit p5_submit never selected, no attempt record) is reported, left untouched, exit 3" 3 $rc $(grep -q "UNPROVEN" "$W/ct8.log" && [ -d "$(pdir $c0)/SMCBVS_p5retry.lock" ] && echo 0 || echo 1)
MM > "$W/mm_unp.log" 2>&1; rc=$?
res "R2-6: make_manifests still refuses while an unproven artefact remains, and writes nothing" 2 $rc $([ ! -e "$FS/results/$RID/p0500/MANIFEST.sha256" ] && [ ! -e "$RD/HOME_MANIFEST.sha256" ] && echo 0 || echo 1)
rm -rf "$(pdir $c0)"

echo "| **make_manifests.sh: transactional, safe to rerun (R2-6), home manifest (R2-9)** |" | tee -a "$OUT"
printf '%s_3|smcbvs|RUNNING|None\n' "$PJ" > "$SD/queue_r.psv"; MM > "$W/mm0.log" 2>&1; rc=$?
res "make_manifests refuses while a job is queued -> exit 2" 2 $rc; rm -f "$SD/queue_r.psv"
mkdir -p "$FS/results/$RID/p0500/x.lock"; MM > "$W/mm1.log" 2>&1; rc=$?
res "make_manifests refuses with an unfinished lock directory under a result folder -> exit 2, no manifest written" 2 $rc $([ ! -e "$FS/results/$RID/p0500/MANIFEST.sha256" ] && echo 0 || echo 1); rmdir "$FS/results/$RID/p0500/x.lock"
n_res_before=$(find "$FS/results" "$FS/logs" -type f | wc -l)
MM > "$W/mm2.log" 2>&1; rc=$?
res "make_manifests: one manifest per folder (p0500, p1000, logs/<RUN_ID>), self-checked, then the full summary.tsv; nothing deleted" 0 $rc \
  $([ -s "$FS/results/$RID/p0500/MANIFEST.sha256" ] && [ -s "$FS/results/$RID/p1000/MANIFEST.sha256" ] && [ -s "$LOG/MANIFEST.sha256" ] && [ "$(find "$FS/results" "$FS/logs" -type f | wc -l)" = "$((n_res_before + 3))" ] \
    && [ "$(grep -c . "$RD/manifests/summary.tsv")" = 4 ] && [ -s "$ARCH/CLEANUP_LOG.tsv" ] && echo 0 || echo 1)
res "manifest paths are relative to the folder (no leading ./ or /); P5_retry files (also the archived evidence under logs/cleanup) are inside the manifests; accounting is in the logs manifest" 0 \
  $([ "$(grep -c -E '^[0-9a-f]{64}  (\./|/)' "$FS/results/$RID/p1000/MANIFEST.sha256")" = 0 ] && grep -q "P5_retry/SMCBVS_p5retry.done" "$FS/results/$RID/p1000/MANIFEST.sha256" && grep -q "P5_retry/SMCBVS_p5retry.done" "$FS/results/$RID/p0500/MANIFEST.sha256" \
    && grep -q "accounting/core_hours.tsv" "$LOG/MANIFEST.sha256" && grep -q "attempts/$c0/attempt_1.start.json" "$LOG/MANIFEST.sha256" && grep -q "cleanup/.*CLEANUP_LOG.tsv" "$LOG/MANIFEST.sha256" && grep -q "p5_scan/scan_primary_" "$LOG/MANIFEST.sha256" && echo 0 || echo 1)
DL="$W/download"; rm -rf "$DL"; mkdir -p "$DL/results/$RID" "$DL/logs"; cp -r "$FS/results/$RID/p0500" "$FS/results/$RID/p1000" "$DL/results/$RID/"; cp -r "$LOG" "$DL/logs/$RID"
ok=0; for d in "$DL/results/$RID/p0500" "$DL/results/$RID/p1000" "$DL/logs/$RID"; do (cd "$d" && sha256sum --quiet -c MANIFEST.sha256 >/dev/null 2>&1) || ok=1; done
res "manifest round trip: the three downloaded copies verify with sha256sum -c (mirrors C:\\...\\NOTS Data\\New_Campaign\\results\\<RUN_ID>\\p0500 etc.)" 0 $ok
f=$(find "$DL/results/$RID/p1000" -name SMCBVS.rds | head -1); echo tamper >> "$f"; (cd "$DL/results/$RID/p1000" && sha256sum --quiet -c MANIFEST.sha256 >/dev/null 2>&1); res "manifest round trip: a tampered result file FAILS the check" 1 $?
f=$(find "$DL/results/$RID/p0500" -name SMCBVS.csv | head -1); rm -f "$f"; (cd "$DL/results/$RID/p0500" && sha256sum --quiet -c MANIFEST.sha256 >/dev/null 2>&1); res "manifest round trip: a missing result file FAILS the check" 1 $?
f=$(find "$DL/logs/$RID/attempts" -name '*.json' | head -1); echo x >> "$f"; (cd "$DL/logs/$RID" && sha256sum --quiet -c MANIFEST.sha256 >/dev/null 2>&1); res "manifest round trip: a tampered log/attempt file FAILS the check" 1 $?
# R2-9: the home run-summary folder has its own manifest (everything except runner/), verified locally before any pruning
HM=$RD/HOME_MANIFEST.sha256
res "R2-9: HOME_MANIFEST.sha256 covers the small home summaries (tables, receipts, reconcile/scan/P5/accounting/cleanup/manifest files) but not runner/ and not itself" 0 \
  $([ -s "$HM" ] && grep -q "  p5_scan_primary.receipt$" "$HM" && grep -q "  p5_final_report.tsv$" "$HM" && grep -q "  accounting/core_hours.tsv$" "$HM" && grep -q "  manifests/summary.tsv$" "$HM" && grep -q "  cleanup/cleanup_" "$HM" \
    && grep -q "  jobs.tsv$" "$HM" && ! grep -q "  runner/" "$HM" && ! grep -q "HOME_MANIFEST" "$HM" && echo 0 || echo 1)
HD="$W/home_download"; rm -rf "$HD"; mkdir -p "$HD"; (cd "$RD" && tar -cf - --exclude=./runner .) | tar -xf - -C "$HD"; (cd "$HD" && sha256sum --quiet -c HOME_MANIFEST.sha256 >/dev/null 2>&1); res "R2-9: the downloaded home summary folder (without runner/) verifies with sha256sum -c HOME_MANIFEST.sha256" 0 $?
echo x >> "$HD/reconcile.tsv"; (cd "$HD" && sha256sum --quiet -c HOME_MANIFEST.sha256 >/dev/null 2>&1); res "R2-9: a tampered home summary file FAILS the home manifest check" 1 $?
res "R2-9: after the whole run the home folder holds NO execution log (no *.log, *.jsonl, *.err, *.out outside runner/); the scan, refusal, locks and scheduler logs are all on scratch" 0 \
  "$(find "$RD" -type f \( -name '*.log' -o -name '*.jsonl' -o -name '*.err' -o -name '*.out' \) ! -path "$RD/runner/*" | wc -l)" \
  $([ -s "$LOG/refusals.log" ] && [ -s "$LOG/locks_cleared.jsonl" ] && [ -d "$LOG/p5_scan" ] && [ -d "$LOG/submit" ] && echo 0 || echo 1)
sum1=$(sha256sum "$RD/manifests/summary.tsv" | cut -d' ' -f1); m1=$(sha256sum "$FS/results/$RID/p1000/MANIFEST.sha256" | cut -d' ' -f1); h1=$(sha256sum "$HM" | cut -d' ' -f1)
MM > "$W/mm3.log" 2>&1; rc=$?
res "R2-6: rerunning make_manifests on an unchanged tree is safe: exit 0, every manifest 'reused' (revalidated, not replaced), the summary and the home manifest are identical" 0 $rc \
  $([ "$(grep -c ': manifest reused' "$W/mm3.log")" = 3 ] && grep -q "home summary manifest reused" "$W/mm3.log" && [ "$(sha256sum "$RD/manifests/summary.tsv" | cut -d' ' -f1)" = "$sum1" ] && [ "$(sha256sum "$FS/results/$RID/p1000/MANIFEST.sha256" | cut -d' ' -f1)" = "$m1" ] && [ "$(sha256sum "$HM" | cut -d' ' -f1)" = "$h1" ] && echo 0 || echo 1)
rm -f "$LOG/MANIFEST.sha256" "$RD/manifests/summary.tsv"; MM > "$W/mm4.log" 2>&1; rc=$?
res "R2-6: recovery after a partial pass (logs manifest and the summary missing): exit 0, p0500 and p1000 reused, logs rebuilt, the summary rebuilt IN FULL (4 lines)" 0 $rc \
  $(grep -q "results_p0500: manifest reused" "$W/mm4.log" && grep -q "logs: manifest new" "$W/mm4.log" && [ "$(grep -c . "$RD/manifests/summary.tsv")" = 4 ] && [ "$(sha256sum "$RD/manifests/summary.tsv" | cut -d' ' -f1)" = "$sum1" ] && echo 0 || echo 1)
echo extra > "$FS/results/$RID/p0500/extra_file.txt"; MM > "$W/mm5.log" 2>&1; rc=$?
res "R2-6: an existing manifest that no longer matches its folder (a file added) is never replaced silently: exit 2, every manifest unchanged" 2 $rc \
  $(grep -q "INCONSISTENT" "$W/mm5.log" && [ "$(sha256sum "$FS/results/$RID/p1000/MANIFEST.sha256" | cut -d' ' -f1)" = "$m1" ] && ! grep -q extra_file "$FS/results/$RID/p0500/MANIFEST.sha256" && echo 0 || echo 1)
rm -f "$FS/results/$RID/p0500/extra_file.txt"; cp "$RD/reconcile.tsv" "$W/reconcile.bak"; echo x >> "$RD/reconcile.tsv"; MM > "$W/mm6.log" 2>&1; rc=$?
res "R2-9: a home summary changed after HOME_MANIFEST.sha256 was written: refused (exit 2), the home manifest is not replaced" 2 $rc $(grep -q "HOME_MANIFEST.sha256 exists but is INCONSISTENT" "$W/mm6.log" && [ "$(sha256sum "$HM" | cut -d' ' -f1)" = "$h1" ] && echo 0 || echo 1)
cp "$W/reconcile.bak" "$RD/reconcile.tsv"

echo "| **cleanup_terminal.sh: SIGKILLed PRIMARY attempts (task.sh), unproven and live-owner artefacts (R2-5)** |" | tee -a "$OUT"
mkfix "$W/fx_kill"; SUBMIT > "$W/kill_submit.log" 2>&1
nenv SLURM_JOB_ID=7001 SLURM_CPUS_PER_TASK=1 -- bash "$RD/runner/precompile.sbatch" "$RD" > /dev/null 2>&1
echo killlock > "$SD/mode_default"; : > "$SD/runcase_calls.txt"
runtask task.sh 1 7002; rc=$?
KU1=p1000_S1_r001_c100; KP1="$FS/results/$RID/p1000/$KU1/SMCBVS"
res "primary task with SIGKILLed children (exit 137): the task exits 0; both units leave SMCBVS.lock (foreign host: task.sh does not remove it) and a temporary file" 0 $rc \
  $([ -d "$KP1.lock" ] && [ -d "$FS/results/$RID/p1000/p1000_S1_r001_c050/SMCBVS.lock" ] && [ -f "$KP1.rds.tmp.4242" ] && echo 0 || echo 1)
rm -f "$SD/mode_default"
{ echo "$SACCT_HEAD"; echo "7001|pre|COMPLETED|0:0|00:05:00||n1|2026-10-29T12:05:00|1|300"; echo "7002_1|a|FAILED|137:0|00:10:00||n1|2026-10-29T13:00:00|1|600"; echo "7003_601|b|COMPLETED|0:0|00:30:00||n2|2026-10-29T12:30:00|1|1800"; } > "$SD/sacct.psv"
CT_ARGS=""; mkdir -p "$FS/results/$RID/p1000/p1000_S1_r005_c100/SMCBVS.lock"
n_att=$(find "$LOG/attempts" -type f | wc -l); n_rc=$(wc -l < "$SD/runcase_calls.txt")
CT > "$W/ctk1.log" 2>&1; rc=$?
res "R2-5: primary cleanup archives the proven-stale locks and temporary files (attempt records of this run's array), reports the lock of a unit with NO attempt record as UNPROVEN and leaves it: exit 3" 3 $rc \
  $([ ! -d "$KP1.lock" ] && [ ! -e "$KP1.rds.tmp.4242" ] && [ -d "$FS/results/$RID/p1000/p1000_S1_r005_c100/SMCBVS.lock" ] && grep -q "UNPROVEN p1000/p1000_S1_r005_c100/SMCBVS.lock" "$W/ctk1.log" && [ "$(grep -c '^ARCHIVED' "$W/ctk1.log")" = 4 ] && echo 0 || echo 1)
res "R2-5: the primary attempt records are kept (same count), no fit was relaunched, no sbatch call was made" 0 $([ "$(find "$LOG/attempts" -type f | wc -l)" = "$n_att" ] && [ "$(wc -l < "$SD/runcase_calls.txt")" = "$n_rc" ] && echo 0 || echo 1)
rmdir "$FS/results/$RID/p1000/p1000_S1_r005_c100/SMCBVS.lock"
# a lock whose owner is a LIVE process on this host is never removed
sleep 120 & SLP=$!
mkdir -p "$FS/results/$RID/p1000/$KU1/SMCBVS.lock"; printf 'pid %s\nhost %s\nutc x\n' "$SLP" "$(hostname -s)" > "$FS/results/$RID/p1000/$KU1/SMCBVS.lock/owner.txt"
CT > "$W/ctk2.log" 2>&1; rc=$?
res "R2-5: a lock whose owner process is ALIVE on this host is reported UNPROVEN and left untouched: exit 3" 3 $rc $(grep -q "owner alive on this host" "$W/ctk2.log" && [ -d "$FS/results/$RID/p1000/$KU1/SMCBVS.lock" ] && echo 0 || echo 1)
kill "$SLP" 2>/dev/null; wait "$SLP" 2>/dev/null; rm -rf "$FS/results/$RID/p1000/$KU1/SMCBVS.lock"
# an atomic-write remnant inside a lock directory is archived with it and renamed (so no *.tmp.* name survives)
mkdir -p "$FS/results/$RID/p1000/p1000_S1_r001_c050/SMCBVS.lock" 2>/dev/null; echo partial > "$FS/results/$RID/p1000/p1000_S1_r001_c050/SMCBVS.lock/owner.txt.tmp.77"
CT > "$W/ctk3.log" 2>&1; rc=$?
res "R2-5: a temporary file inside a lock directory moves with it and is renamed; no *.tmp.* / *.lock name is left anywhere under results/ or logs/" 0 $rc \
  $([ "$(find "$FS/results" "$LOG" \( -name '*.lock' -o -name '*.tmp.*' -o -name '*.tmp' \) | wc -l)" = 0 ] && echo 0 || echo 1)

echo "| **P5 with no resource_limit unit; staging** |" | tee -a "$OUT"
mkfix "$W/fx_none"; SUBMIT > "$W/none_submit.log" 2>&1; nenv SLURM_JOB_ID=7001 SLURM_CPUS_PER_TASK=1 -- bash "$RD/runner/precompile.sbatch" "$RD" > /dev/null 2>&1
echo '{"default":"ok"}' > "$W/spec_none.json"; nenv -- python3 "$HERE/fabricate.py" "$RD" "$(mixed "$W/spec_none.json")" > /dev/null 2>&1
mksacct; rm -f "$SD/queue.psv" "$SD/queue_r.psv"; scanfix "${CASES[0]} completed none FALSE FALSE"
n_sb=$(ncalls); P5 > "$W/p5none.log" 2>&1; rc=$?
res "P5 with no resource_limit unit: exit 0, the scan job runs, NO P5 array is submitted, 'none_eligible' recorded" 0 $rc $([ "$(ncalls)" = $((n_sb + 1)) ] && [ "$(p5calls)" = 0 ] && [ -s "$RD/p5/none_eligible.json" ] && echo 0 || echo 1)
# ---- Sol review 3 (fixture fx_none: a submitted run with a clean fabricated tree, precompile done, scan fixture, stub scheduler) ----------------------------------------
echo "| **Sol review 3: R3-1 unknown scheduler state is not failure, R3-2 guard inside the scan wrapper, R3-3 empty result folder** |" | tee -a "$OUT"
cp "$SD/sacct.psv" "$W/sacct.r3.bak"; cp "$RD/jobs.tsv" "$W/jobs.r3.bak"
rm -f "$RD"/p5_scan_primary.* "$SD/scancel_calls.txt"; rm -rf "$RD/p5"
jobof() { awk '$1 == "job" { print $2; exit }' "$RD/p5_scan_$1.job" 2>/dev/null; }
retired() { ls "$RD"/p5_scan_primary.*.failed_* "$RD"/p5_scan_primary.*.refused_* "$RD"/p5_scan_primary.*.dryrun_* >/dev/null 2>&1 && echo 1 || echo 0; }
# R3-1, full parent: accepted scan -> transient squeue failure -> repeat invocation = exactly ONE sbatch, the original job record is kept and then used
P5_ARGS="--dry-run"; n0=$(ncalls); SJ=$((7000 + $(ctr) + 1))
P5 STUB_ARM_SQUEUE_FAIL=1 > "$W/r31a.log" 2>&1; rc=$?
res "R3-1: scan job ACCEPTED, then a transient squeue failure: p5_submit exits 2 (state UNKNOWN, 'RESUMED' announced), ONE sbatch, no scancel, no P5 array" 2 $rc \
  $([ "$(ncalls)" = $((n0 + 1)) ] && grep -q "UNKNOWN" "$W/r31a.log" && grep -q "RESUMED" "$W/r31a.log" && [ ! -s "$SD/scancel_calls.txt" ] && noarr 0 | grep -q 0 && echo 0 || echo 1)
res "R3-1: after the outage the scan job record (id $SJ), the table and the receipt are all KEPT in place and nothing was set aside (failed/refused/dryrun)" 0 \
  $([ "$(jobof primary)" = "$SJ" ] && [ -s "$RD/p5_scan_primary.tsv" ] && [ -s "$RD/p5_scan_primary.receipt" ] && [ "$(retired)" = 0 ] && echo 0 || echo 1)
P5 > "$W/r31b.log" 2>&1; rc=$?
res "R3-1: the repeat invocation RESUMES the same scan job $SJ (not resubmitted), verifies it and passes all gates (dry run, exit 0): still exactly ONE sbatch in total" 0 $rc \
  $([ "$(ncalls)" = $((n0 + 1)) ] && grep -q "job $SJ already recorded" "$W/r31b.log" && grep -q "not resubmitted" "$W/r31b.log" && grep -q "^job $SJ$" "$RD"/p5_scan_primary.job.dryrun_* && [ "$(grep -c "^$SJ"$'\t'p5scan_primary "$RD/jobs.tsv")" = 1 ] && noarr 0 | grep -q 0 && echo 0 || echo 1)
rm -f "$RD"/p5_scan_primary.*; P5_ARGS=""
# R3-1, wrapper: an unreadable sacct or squeue never fails or retires the recorded job
SCAN_ARGS="primary"; n0=$(ncalls); SJ=$((7000 + $(ctr) + 1))
SCANRUN > "$W/r31c.log" 2>&1; rc=$?
res "R3-1 setup: a direct scan primary submits ONE scan job and verifies it (exit 0)" 0 $rc $([ "$(ncalls)" = $((n0 + 1)) ] && [ "$(jobof primary)" = "$SJ" ] && echo 0 || echo 1)
SCANRUN SACCT_FAIL=1 > "$W/r31d.log" 2>&1; rc=$?
res "R3-1: sacct unreadable on a re-check: exit 11 (state unknown), the job record, table and receipt are kept, nothing resubmitted" 11 $rc \
  $(grep -q "SCHEDULER QUERY FAILED" "$W/r31d.log" && [ "$(ncalls)" = $((n0 + 1)) ] && [ "$(jobof primary)" = "$SJ" ] && [ -s "$RD/p5_scan_primary.tsv" ] && [ -s "$RD/p5_scan_primary.receipt" ] && echo 0 || echo 1)
SCANRUN SQUEUE_FAIL=1 > "$W/r31e.log" 2>&1; rc=$?
res "R3-1: squeue unreadable on a re-check: exit 11 as well, records kept" 11 $rc $(grep -q "SCHEDULER QUERY FAILED" "$W/r31e.log" && [ "$(ncalls)" = $((n0 + 1)) ] && [ "$(jobof primary)" = "$SJ" ] && echo 0 || echo 1)
SCANRUN > "$W/r31f.log" 2>&1; rc=$?
res "R3-1: the next call (scheduler readable again) resumes the SAME job: exit 0, still one sbatch" 0 $rc $([ "$(ncalls)" = $((n0 + 1)) ] && grep -q "job $SJ already recorded" "$W/r31f.log" && echo 0 || echo 1)
# R3-1, post-acceptance abort whose cancel is uncertain: the accepted job is not proven terminal -> .uncertain, exit 11, no relaunch until proven
rm -f "$RD"/p5_scan_primary.* "$SD/scancel_calls.txt"; n0=$(ncalls); k=$(ctr); SJ=$((7000 + k + 1))
SCANRUN SACCT_FAIL=1 BREAK_JOURNAL="$RD/jobs.tsv" BREAK_AT=$((k + 1)) > "$W/r31g.log" 2>&1; rc=$?
res "R3-1: scan job $SJ accepted, jobs.tsv append fails, cancel issued but squeue/sacct cannot prove it terminal: exit 11, cancelled BY EXPLICIT ID, p5_scan_primary.uncertain names the job, ABORTED says UNCERTAIN" 11 $rc \
  $([ "$(tr '\n' ' ' < "$SD/scancel_calls.txt" | sed 's/ *$//')" = "$SJ" ] && grep -q "^job $SJ$" "$RD/p5_scan_primary.uncertain" && grep -q "UNCERTAIN" "$RD/p5_scan_primary.ABORTED" && [ "$(ncalls)" = $((n0 + 1)) ] && echo 0 || echo 1)
rm -rf "$RD/jobs.tsv"; cp "$W/jobs.r3.bak" "$RD/jobs.tsv"; rm -f "$RD"/p5_scan_primary.tsv "$RD"/p5_scan_primary.receipt "$RD"/p5_scan_primary.job
SCANRUN SACCT_FAIL=1 > "$W/r31h.log" 2>&1; rc=$?
res "R3-1: while the earlier accepted job is not proven terminal (sacct unreadable) a new scan job is NOT submitted: exit 11, no new sbatch, marker kept" 11 $rc $([ "$(ncalls)" = $((n0 + 1)) ] && [ -e "$RD/p5_scan_primary.uncertain" ] && echo 0 || echo 1)
SCANRUN > "$W/r31i.log" 2>&1; rc=$?
res "R3-1: once squeue AND sacct prove the old job terminal the marker is set aside (.cleared_*) and ONE new scan job is submitted: exit 0" 0 $rc \
  $([ "$(ncalls)" = $((n0 + 2)) ] && [ ! -e "$RD/p5_scan_primary.uncertain" ] && ls "$RD"/p5_scan_primary.uncertain.cleared_* >/dev/null 2>&1 && echo 0 || echo 1)
rm -f "$RD"/p5_scan_primary.* "$SD/scancel_calls.txt"
# ---- Sol review 4, R4-1: ONE submitter per run and phase (atomic lock); retirement only of the exact, proven-terminal job ----------------------------------
echo "| **Sol review 4: R4-1 overlapping scan calls (submission lock, exact-id retirement)** |" | tee -a "$OUT"
rm -f "$RD"/p5_scan_primary.* "$SD/scancel_calls.txt"; rm -rf "$RD/p5_scan_primary.submit.lock"; SCAN_ARGS="primary"
# (a) a held submission lock: the direct wrapper exits 12 and submits nothing; the parent refuses (exit 2) and retires nothing
mkdir -p "$RD/p5_scan_primary.submit.lock"; echo "pid 1" > "$RD/p5_scan_primary.submit.lock/owner.txt"; n0=$(ncalls)
SCANRUN > "$W/r41a.log" 2>&1; rc=$?
res "R4-1: the submission lock is held by another call: the direct scan wrapper exits 12, NO sbatch, no job record, the lock is left to its owner" 12 $rc \
  $([ "$(ncalls)" = "$n0" ] && [ ! -e "$RD/p5_scan_primary.job" ] && [ -d "$RD/p5_scan_primary.submit.lock" ] && grep -q "another call holds the primary scan lock" "$W/r41a.log" && echo 0 || echo 1)
P5_ARGS="--dry-run"; P5 > "$W/r41b.log" 2>&1; rc=$?
res "R4-1: p5_submit while the lock is held: refused (exit 2), NO sbatch, nothing retired" 2 $rc \
  $([ "$(ncalls)" = "$n0" ] && grep -q "submission lock" "$W/r41b.log" && [ "$(retired)" = 0 ] && echo 0 || echo 1)
rm -rf "$RD/p5_scan_primary.submit.lock"; rm -f "$RD"/p5_scan_primary.*
# (b) the overlap Sol reproduced: a direct scan (A) and a parent (B) start together while the scheduler answers slowly. Exactly ONE scan job may exist;
#     the loser never submits; the winner's record is kept; a later parent call resumes it and never replaces it.
n0=$(ncalls); SJ=$((7000 + $(ctr) + 1))
SCANRUN STUB_SBATCH_DELAY=45 > "$W/r41c_A.log" 2>&1 & pa=$!
for ((w = 0; w < 100; w++)); do [ -d "$RD/p5_scan_primary.submit.lock" ] && break; sleep 0.1; done
P5 > "$W/r41c_B.log" 2>&1 & pb=$!
wait "$pa"; ra=$?; wait "$pb"; rb=$?
res "R4-1: overlapping direct scan + parent: exactly ONE sbatch in total; the first call (A) finishes its scan (exit 0); the parent (B) runs into the lock and refuses (exit 2)" "0 2 1" "$ra $rb $(( $(ncalls) - n0 ))"
res "R4-1: after the overlap the job record names A's job $SJ, it is in jobs.tsv once, and NOTHING was retired or cancelled" 0 \
  $([ "$(jobof primary)" = "$SJ" ] && [ "$(grep -c "^$SJ"$'\t'p5scan_primary "$RD/jobs.tsv")" = 1 ] && [ "$(retired)" = 0 ] && [ ! -s "$SD/scancel_calls.txt" ] && [ ! -d "$RD/p5_scan_primary.submit.lock" ] && echo 0 || echo 1)
P5 > "$W/r41d.log" 2>&1; rc=$?
res "R4-1: a later parent call RESUMES A's job $SJ (no new sbatch; dry run passes, exit 0); the dry run then retires exactly that proven-terminal job" 0 $rc \
  $([ "$(( $(ncalls) - n0 ))" = 1 ] && grep -q "job $SJ already recorded" "$W/r41d.log" && grep -q "^job $SJ$" "$RD"/p5_scan_primary.job.dryrun_* && echo 0 || echo 1)
rm -f "$RD"/p5_scan_primary.*
# (c) nc_retire_scan is exact: it retires only the expected id, only when the current record names it and squeue AND sacct prove it terminal
RS() { nenv -- bash -c 'source "$1/runner/common.sh"; nc_load_run "$1"; nc_retire_scan "$1" primary failed "$2"' _ "$RD" "$1"; }
printf 'job %s\nphase primary\n' "$SJ" > "$RD/p5_scan_primary.job"; echo t > "$RD/p5_scan_primary.tsv"
RS 9999 > "$W/r41e.log" 2>&1; rc=$?
res "R4-1: nc_retire_scan with an id the record does not name (9999 vs $SJ): returns 1, nothing retired" 1 $rc $([ -e "$RD/p5_scan_primary.job" ] && [ "$(retired)" = 0 ] && grep -q "not 9999" "$W/r41e.log" && echo 0 || echo 1)
RS "" > "$W/r41f.log" 2>&1; rc=$?
res "R4-1: nc_retire_scan without an expected id: returns 1, nothing retired" 1 $rc $([ -e "$RD/p5_scan_primary.job" ] && [ "$(retired)" = 0 ] && echo 0 || echo 1)
printf '%s_1|smcbvs_x|RUNNING|None\n' "$SJ" > "$SD/queue_r.psv"
RS "$SJ" > "$W/r41g.log" 2>&1; rc=$?
res "R4-1: nc_retire_scan of the recorded id while squeue still shows it LIVE: returns 1, nothing retired" 1 $rc $([ -e "$RD/p5_scan_primary.job" ] && [ "$(retired)" = 0 ] && echo 0 || echo 1)
rm -f "$SD/queue_r.psv"
RS "$SJ" > "$W/r41h.log" 2>&1; rc=$?
res "R4-1: nc_retire_scan of the recorded id once squeue AND sacct prove it terminal: returns 0 and the record is set aside (.failed_*)" 0 $rc $([ ! -e "$RD/p5_scan_primary.job" ] && ls "$RD"/p5_scan_primary.job.failed_* >/dev/null 2>&1 && echo 0 || echo 1)
rm -f "$RD"/p5_scan_primary.*; P5_ARGS=""
# ---- Sol review 5: R5-1 retirement under the scan lock; R5-2 a signal during an in-flight sbatch keeps the lock (fail closed) --------------------------------
echo "| **Sol review 5: R5-1 retirement serialised with submission, R5-2 catchable signals during an in-flight sbatch** |" | tee -a "$OUT"
rm -f "$RD"/p5_scan_primary.* "$SD/scancel_calls.txt"; rm -rf "$RD/p5_scan_primary.submit.lock"; SCAN_ARGS="primary"
LK="$RD/p5_scan_primary.submit.lock"
RSD() { local d=$1; shift; nenv STUB_SACCT_DELAY="$d" -- bash -c 'source "$1/runner/common.sh"; nc_load_run "$1"; nc_retire_scan "$1" primary failed "$2"' _ "$RD" "$1"; }
# (R5-1) a slow retirement A of the failed job 8000 holds the lock for its whole check-prove-move; meanwhile B (same id) and a submission C are refused
printf 'job 8000\nphase primary\n' > "$RD/p5_scan_primary.job"; echo t > "$RD/p5_scan_primary.tsv"
echo "8000|p5scan|FAILED|1:0|00:01:00||n1|2026-10-29T17:00:00|1|60" >> "$SD/sacct.psv"
n0=$(ncalls)
RSD 12 8000 > "$W/r51a.log" 2>&1 & pa=$!
for ((w = 0; w < 100; w++)); do grep -q "role retire 8000" "$LK/owner.txt" 2>/dev/null && break; sleep 0.1; done
RSD "" 8000 > "$W/r51b.log" 2>&1; rb=$?
SCANRUN > "$W/r51c.log" 2>&1; rc=$?
wait "$pa"; ra=$?
res "R5-1: while retirement A holds the scan lock, a second retirement B of the same id is refused (1); a scan call C resumes and judges the recorded job 8000 (exit 4) and submits nothing" "1 4 $n0" "$rb $rc $(ncalls)"
res "R5-1: A completes (0): the record of the terminal job 8000 is set aside and the lock is released" 0 $ra \
  $([ ! -e "$RD/p5_scan_primary.job" ] && ls "$RD"/p5_scan_primary.job.failed_* >/dev/null 2>&1 && [ ! -d "$LK" ] && grep -q "another call holds" "$W/r51b.log" && echo 0 || echo 1)
SJ=$((7000 + $(ctr) + 1)); SCANRUN > "$W/r51d.log" 2>&1; rc=$?
res "R5-1: a new scan C2 submits ONE job ($SJ) once the lock is free (exit 0)" 0 $rc $([ "$(ncalls)" = $((n0 + 1)) ] && [ "$(jobof primary)" = "$SJ" ] && echo 0 || echo 1)
RSD "" 8000 > "$W/r51e.log" 2>&1; rc=$?
res "R5-1: a LATE retirement of the old id 8000 refuses (1): the record now names $SJ, which survives untouched" 1 $rc $([ "$(jobof primary)" = "$SJ" ] && grep -q "not 8000" "$W/r51e.log" && [ ! -d "$LK" ] && echo 0 || echo 1)
rm -f "$RD"/p5_scan_primary.*
# (R5-2) TERM / HUP / INT while sbatch is in flight (accepted, id not yet journaled): the lock is KEPT with IN_FLIGHT; the next call exits 12, no new sbatch
for sig in TERM HUP INT; do
  rm -rf "$LK"; rm -f "$RD"/p5_scan_primary.*; n0=$(ncalls)
  SCANRUN STUB_RUN_SCAN=0 STUB_SBATCH_DELAY=8 > "$W/r52_$sig.log" 2>&1 & pw=$!
  for ((w = 0; w < 100; w++)); do [ -e "$LK/IN_FLIGHT" ] && break; sleep 0.1; done
  wpid=$(awk '$1 == "pid" { print $2; exit }' "$LK/owner.txt" 2>/dev/null)
  sleep 1; kill -s "$sig" "$wpid" 2>/dev/null; wait "$pw"; rw=$?
  res "R5-2 ($sig): the wrapper is signalled while its sbatch is in flight: it ends non-zero and the lock with IN_FLIGHT (job name recorded) is KEPT, no job record" 0 \
    $([ "$rw" != 0 ] && [ -d "$LK" ] && grep -q "^job_name smcbvs_" "$LK/IN_FLIGHT" && [ ! -e "$RD/p5_scan_primary.job" ] && echo 0 || echo 1)
  sleep 8
  SCANRUN > "$W/r52_${sig}_next.log" 2>&1; rc=$?
  res "R5-2 ($sig): the next scan call exits 12 (lock kept, IN_FLIGHT named in the message) and submits NOTHING: still one sbatch" 12 $rc \
    $([ "$(ncalls)" = $((n0 + 1)) ] && grep -q "IN_FLIGHT" "$W/r52_${sig}_next.log" && echo 0 || echo 1)
  RSD "" 9999 > "$W/r52_${sig}_ret.log" 2>&1; rc=$?
  res "R5-2 ($sig): a retirement while the in-flight lock is held is refused (1), nothing moved" 1 $rc $([ -d "$LK" ] && echo 0 || echo 1)
done
# ---- Sol review 6, R6-1: a NONZERO sbatch status does not prove that nothing was accepted -> fail closed (exit 13, lock + IN_FLIGHT kept) ----
echo "| **Sol review 6: R6-1 nonzero sbatch status = acceptance UNKNOWN (fail closed)** |" | tee -a "$OUT"
for st in 143 137; do
  rm -rf "$LK"; rm -f "$RD"/p5_scan_primary.* "$SD/accepted_dead"; n0=$(ncalls)
  SCANRUN STUB_RUN_SCAN=0 STUB_SBATCH_ACCEPT_THEN_DIE=$st > "$W/r61_$st.log" 2>&1; rc=$?
  res "R6-1 (client status $st): the scheduler ACCEPTED a job but the sbatch client died before returning its id: wrapper exits 13 (UNKNOWN), lock + IN_FLIGHT KEPT with client_status $st, no job record" 13 $rc \
    $([ -d "$LK" ] && grep -q "^client_status $st$" "$LK/IN_FLIGHT" && [ ! -e "$RD/p5_scan_primary.job" ] && [ -s "$SD/accepted_dead" ] && grep -q "UNKNOWN whether the scheduler accepted" "$W/r61_$st.log" && echo 0 || echo 1)
  SCANRUN > "$W/r61_${st}_next.log" 2>&1; rc=$?
  res "R6-1 (client status $st): the next scan call exits 12 and submits NOTHING: exactly ONE acceptance in total, no replacement" 12 $rc $([ "$(ncalls)" = $((n0 + 1)) ] && echo 0 || echo 1)
done
# an ordinary rejection (FAIL_AT, exit 42) is treated the same way: acceptance cannot be ruled out from the status alone
rm -rf "$LK"; rm -f "$RD"/p5_scan_primary.*; n0=$(ncalls)
SCANRUN FAIL_AT=$(( $(ctr) + 1 )) > "$W/r52_rej.log" 2>&1; rc=$?
res "R6-1: sbatch exits 42 (a rejection, or a failed client): wrapper exits 13, lock + IN_FLIGHT kept with client_status 42 and its stderr; nothing submitted again" 13 $rc \
  $([ -d "$LK" ] && grep -q "^client_status 42$" "$LK/IN_FLIGHT" && grep -q "^client_stderr fabricated sbatch rejection" "$LK/IN_FLIGHT" && echo 0 || echo 1)
# the parent maps wrapper exit 13 to a refusal that names the unknown acceptance and the manual resolution
rm -rf "$LK"; rm -f "$RD"/p5_scan_primary.*; P5_ARGS="--dry-run"
P5 FAIL_AT=$(( $(ctr) + 1 )) > "$W/r61_parent.log" 2>&1; rc=$?
res "R6-1: p5_submit when the scan's sbatch fails: refused (exit 2) naming 'wrapper exit 13' and the kept lock; nothing retired, no P5 array" 2 $rc \
  $(grep -q "wrapper exit 13" "$W/r61_parent.log" && [ -d "$LK" ] && [ "$(retired)" = 0 ] && noarr 0 | grep -q 0 && echo 0 || echo 1)
P5_ARGS=""; rm -rf "$LK"; rm -f "$RD"/p5_scan_primary.* "$SD/accepted_dead"
# ---- Sol review 7, R7-1: the diagnostic append to IN_FLIGHT fails (storage error): still exit 13 / parent 2, exclusion kept, no replacement ----
echo "| **Sol review 7: R7-1 a failed diagnostic append still ends in exit 13** |" | tee -a "$OUT"
n0=$(ncalls); P5_ARGS="--dry-run"
P5 STUB_SBATCH_ACCEPT_THEN_DIE=42 STUB_BREAK_INFLIGHT="$LK/IN_FLIGHT" > "$W/r71_parent.log" 2>&1; rc=$?
res "R7-1: accepted job, client exits 42 AND the append to IN_FLIGHT fails: the parent refuses (exit 2) naming 'wrapper exit 13' (not a guard refusal), the warning is printed, the lock and the IN_FLIGHT entry are kept" 2 $rc \
  $(grep -q "wrapper exit 13" "$W/r71_parent.log" && ! grep -q "OPS guard refused" "$W/r71_parent.log" && grep -q "could not append the sbatch status" "$W/r71_parent.log" && [ -d "$LK" ] && [ -e "$LK/IN_FLIGHT" ] && echo 0 || echo 1)
P5 > "$W/r71_next.log" 2>&1; rc=$?
res "R7-1: the next p5_submit is refused by the kept lock (exit 2), nothing submitted: exactly ONE acceptance, no P5 array" 2 $rc $([ "$(ncalls)" = $((n0 + 1)) ] && noarr 0 | grep -q 0 && echo 0 || echo 1)
P5_ARGS=""; rm -rf "$LK"; rm -f "$RD"/p5_scan_primary.* "$SD/accepted_dead" "$SD/inflight.saved"
# R3-1, rerun.sh uses the same rule (an aborted rerun whose job is not proven terminal blocks the next rerun)
RR_ARGS=""; mkdir -p "$RD/rerun_1"; printf 'job 7999\nutc x\n' > "$RD/rerun_1/UNCERTAIN"; n0=$(ncalls)
RR > "$W/r31j.log" 2>&1; rc=$?
res "R3-1 (rerun): an UNCERTAIN marker whose job is not proven terminal blocks every new rerun: exit 2, no sbatch" 2 $rc $([ "$(ncalls)" = "$n0" ] && grep -q "not proven terminal" "$W/r31j.log" && [ -e "$RD/rerun_1/UNCERTAIN" ] && echo 0 || echo 1)
echo "7999|x|CANCELLED|0:0|00:00:01||n1|2026-10-29T17:00:00|1|1" >> "$SD/sacct.psv"
RR > "$W/r31k.log" 2>&1; rc=$?
res "R3-1 (rerun): once squeue AND sacct prove job 7999 terminal the marker is set aside and rerun.sh proceeds (nothing to rerun here: exit 0, no sbatch)" 0 $rc $([ "$(ncalls)" = "$n0" ] && [ ! -e "$RD/rerun_1/UNCERTAIN" ] && ls "$RD"/rerun_1/UNCERTAIN.cleared_* >/dev/null 2>&1 && echo 0 || echo 1)
rm -rf "$RD/rerun_1"
# R3-2: the wrapper runs the charter guard itself (direct primary and final calls)
rm -rf "$RD/p5"; SCAN_ARGS="final"; n0=$(ncalls)
SCANRUN FAKE_HOME_GB=9.6 > "$W/r32a.log" 2>&1; rc=$?
res "R3-2: a direct FINAL scan with a DENYING guard (home would pass 9.6 GiB): exit 1, NO sbatch, no scan job record, the guard call is recorded in the guard receipt" 1 $rc \
  $([ "$(ncalls)" = "$n0" ] && [ ! -e "$RD/p5_scan_final.job" ] && grep -q "GUARD_CHECK_FAILED" "$RD/p5_scan_final.guard_receipt" && grep -q "call planned=5 rc=1" "$RD/p5_scan_final.guard_receipt" && echo 0 || echo 1)
SCANRUN GUARD="$BIN/guard_old" > "$W/r32b.log" 2>&1; rc=$?
res "R3-2: a direct final scan with the guard that does not enforce the charter limits (7 GiB / 9 GiB): exit 1, NO sbatch" 1 $rc $([ "$(ncalls)" = "$n0" ] && [ ! -e "$RD/p5_scan_final.job" ] && echo 0 || echo 1)
SCAN_ARGS="primary"; SCANRUN FAKE_HOME_GB=9.6 > "$W/r32c.log" 2>&1; rc=$?
res "R3-2: a direct PRIMARY scan with a denying guard: exit 1, NO sbatch, a guard receipt names the refusal" 1 $rc $([ "$(ncalls)" = "$n0" ] && [ ! -e "$RD/p5_scan_primary.job" ] && grep -q "GUARD_CHECK_FAILED" "$RD/p5_scan_primary.guard_receipt" && echo 0 || echo 1)
rm -f "$RD"/p5_scan_primary.*
SCAN_ARGS="final"; SCANRUN > "$W/r32d.log" 2>&1; rc=$?
res "R3-2: a direct final scan with an ALLOWING guard: exit 0, exactly ONE sbatch, guard receipt GUARD_CHECK_OK for the planned 5 MB, job record and jobs.tsv entry created" 0 $rc \
  $([ "$(ncalls)" = $((n0 + 1)) ] && grep -q "GUARD_CHECK_OK" "$RD/p5_scan_final.guard_receipt" && grep -q "planned_mb=5" "$RD/p5_scan_final.guard_receipt" && [ -s "$RD/p5_scan_final.job" ] && grep -q $'\t'p5scan_final$'\t' "$RD/jobs.tsv" && echo 0 || echo 1)
g1=$(sha256sum "$RD/p5_scan_final.guard_receipt" | cut -d' ' -f1)
SCANRUN FAKE_HOME_GB=9.6 > "$W/r32e.log" 2>&1; rc=$?
res "R3-2: re-checking an existing scan job never resubmits and never calls the guard (denying guard, exit 0, same sbatch count, guard receipt unchanged)" 0 $rc \
  $([ "$(ncalls)" = $((n0 + 1)) ] && [ "$(sha256sum "$RD/p5_scan_final.guard_receipt" | cut -d' ' -f1)" = "$g1" ] && grep -q "not resubmitted" "$W/r32e.log" && echo 0 || echo 1)
rm -f "$RD"/p5_scan_final.* "$RD"/p5_scan_primary.*; cp "$W/jobs.r3.bak" "$RD/jobs.tsv"; cp "$W/sacct.r3.bak" "$SD/sacct.psv"; rm -f "$SD/scancel_calls.txt"
# R3-3: an EMPTY result folder is recorded explicitly (zero-line manifest, files=0) and validated without sha256sum -c
RESD="$FS/results/$RID"; PD0="$RESD/p0500"; PD1="$RESD/p1000"
rm -rf "$PD0" "$PD1"; mkdir -p "$PD0/c1" "$PD1/emptysub"; echo "one file" > "$PD0/c1/a.txt"; cp "$PD0/c1/a.txt" "$W/a_txt.bak"
mkdir -p "$RD/accounting"; echo "sacct_final fixture" > "$RD/accounting/sacct_final.tsv"; rm -rf "$RD/manifests" "$RD/HOME_MANIFEST.sha256"
MM > "$W/r33a.log" 2>&1; rc=$?
res "R3-3: first pass with an EMPTY p1000 folder (only an empty sub-folder): exit 0, MANIFEST.sha256 is a 0-byte file, summary records files=0 bytes=0, the log says so" 0 $rc \
  $([ -e "$PD1/MANIFEST.sha256" ] && [ ! -s "$PD1/MANIFEST.sha256" ] && [ "$(awk -F'\t' '$1 ~ /p1000$/ { print $2 "/" $3 }' "$RD/manifests/summary.tsv")" = "0/0" ] && grep -q "results_p1000: manifest new (EMPTY folder recorded explicitly" "$W/r33a.log" \
    && [ "$(wc -l < "$PD0/MANIFEST.sha256")" = 1 ] && echo 0 || echo 1)
sumA=$(sha256sum "$RD/manifests/summary.tsv" | cut -d' ' -f1); homeA=$(sha256sum "$RD/HOME_MANIFEST.sha256" | cut -d' ' -f1)
MM > "$W/r33b.log" 2>&1; rc=$?
res "R3-3: REUSE after the commit: rerun on the unchanged tree with the empty folder: exit 0, p1000 manifest 'reused', summary and home manifest identical" 0 $rc \
  $(grep -q "results_p1000: manifest reused" "$W/r33b.log" && [ ! -s "$PD1/MANIFEST.sha256" ] && [ "$(sha256sum "$RD/manifests/summary.tsv" | cut -d' ' -f1)" = "$sumA" ] && [ "$(sha256sum "$RD/HOME_MANIFEST.sha256" | cut -d' ' -f1)" = "$homeA" ] && echo 0 || echo 1)
DL1="$W/dl_empty_p1000"; rm -rf "$DL1"; mkdir -p "$DL1"; cp -r "$PD1"/. "$DL1"/
(cd "$DL1" && sha256sum --quiet -c MANIFEST.sha256 >/dev/null 2>&1); res "R3-3: why the bundle never runs 'sha256sum -c' on an empty manifest: it exits nonzero (no checksum lines)" 1 $?
(cd "$DL1" && test ! -s MANIFEST.sha256 && test -z "$(find . -type f ! -name MANIFEST.sha256)"); res "R3-3: the laptop acceptance check for an empty folder (0-byte MANIFEST.sha256 and no other file) passes on the downloaded copy" 0 $?
echo stray > "$DL1/stray.txt"; (cd "$DL1" && test ! -s MANIFEST.sha256 && test -z "$(find . -type f ! -name MANIFEST.sha256)"); res "R3-3: the laptop acceptance check FAILS when the downloaded empty folder gained a file" 1 $?
echo late > "$PD1/late.txt"; MM > "$W/r33c.log" 2>&1; rc=$?
res "R3-3: an empty folder that later gains a file is INCONSISTENT: exit 2, the 0-byte manifest and the summary are not replaced" 2 $rc \
  $(grep -q "INCONSISTENT" "$W/r33c.log" && [ ! -s "$PD1/MANIFEST.sha256" ] && [ "$(sha256sum "$RD/manifests/summary.tsv" | cut -d' ' -f1)" = "$sumA" ] && echo 0 || echo 1)
rm -f "$PD1/late.txt"; rm -f "$PD0/c1/a.txt"; MM > "$W/r33d.log" 2>&1; rc=$?
res "R3-3: a folder whose files were all removed after a NON-empty manifest was written is INCONSISTENT too (never silently treated as empty): exit 2" 2 $rc $(grep -q "INCONSISTENT" "$W/r33d.log" && [ "$(wc -l < "$PD0/MANIFEST.sha256")" = 1 ] && echo 0 || echo 1)
cp "$W/a_txt.bak" "$PD0/c1/a.txt"; MM > "$W/r33e.log" 2>&1; rc=$?
res "R3-3: with the file restored everything is 'reused' again (exit 0)" 0 $rc $([ "$(grep -c ': manifest reused' "$W/r33e.log")" = 3 ] && echo 0 || echo 1)
rm -rf "$PD0" "$PD1" "$RD/manifests" "$RD/HOME_MANIFEST.sha256"
bash "$B/stage_local.sh" --stamp $STAMP --out "$W/stage_out" > "$W/stage2.log" 2>&1; res "stage_local refuses a non-empty output folder: exit 3" 3 $?
tl=$(tar -tf "$TAR"); res "tar content: no .cpp_cache, no make_tables.py, no truth/inputs folders; runner (incl. p5_scan.sbatch, cleanup_terminal.sh), tables and the frozen tree are in" 0 \
  $(echo "$tl" | grep -q -E 'cpp_cache|make_tables|truth|/inputs/' && echo 1 || { echo "$tl" | grep -q "runs/$RID/runner/submit.sh" && echo "$tl" | grep -q "runs/$RID/runner/p5_scan.sbatch" && echo "$tl" | grep -q "runs/$RID/runner/cleanup_terminal.sh" && echo "$tl" | grep -q "code/core/v2_2_1.SHA256SUMS" && echo "$tl" | grep -q "runs/$RID/tables/units.tsv" && echo 0 || echo 1; })
X="$W/tar_x"; rm -rf "$X"; mkdir -p "$X"; tar -xf "$TAR" -C "$X"; (cd "$X" && sha256sum --quiet -c "runs/$RID/STAGED_SHA256.txt" >/dev/null 2>&1); res "tar round trip: the extracted tar passes sha256sum -c STAGED_SHA256.txt" 0 $?
echo x >> "$X/runs/$RID/runner/task.sh"; (cd "$X" && sha256sum --quiet -c "runs/$RID/STAGED_SHA256.txt" >/dev/null 2>&1); res "tar round trip: a modified runner file FAILS the staged-hash check" 1 $?
echo x >> "$X/code/core/v2_2_1/core/v3_fit.R"; ( cd "$X/code/core/v2_2_1" && sha256sum --quiet -c ../v2_2_1.SHA256SUMS >/dev/null 2>&1 ); res "tar round trip: a modified frozen-tree file FAILS the manifest check" 1 $?
cp "$V" "$HERE/vectors_final.txt"
