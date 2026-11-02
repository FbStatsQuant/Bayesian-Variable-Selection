#!/bin/bash
# submit_bench.sh -- driver of the PROD-L benchmark wave (PROD_L_BENCH). Derived from PROD_L's submit_prodl.sh (REUSE.md): same hook refusal,
# guard check, staged/frozen checks, ceiling check, launch record and all-or-abort submission with cancel by explicit id.
# Changes (DESIGN.md section 4): no truth-lock steps (no truth is staged for this run); a no-truth check instead; refusal while any PROD-L
# fitting job (lowpL_s1..s4_) is queued or running (benchmarks serialized after the SMC/repeat lane) unless --allow-concurrent-prodl (HQ only).
#   STAMP=... bash submit_bench.sh --wave main|rN --profile alone|withH [--pieces bench,benchretry] [--allow-concurrent-prodl] [--dry-run] [--local-test]
# Exit 0 submitted (or dry run printed); 1 guard refused; 2 another refusal (nothing created); 5 submission aborted (submitted ids cancelled).
set -euo pipefail
HERE=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
STAMP=${STAMP:-$(date -u +%Y%m%dT%H%MZ)}; export STAMP
[[ $STAMP =~ ^[0-9]{8}T[0-9]{4}Z$ ]] || exit 2
source "$HERE/bench.env"
SBATCH=${SBATCH:-sbatch}; SQUEUE=${SQUEUE:-squeue}; SCANCEL=${SCANCEL:-scancel}; PYTHON=${PYTHON:-python3}
wave=; profile=; pieces=; dry=0; localtest=0; concurrent=0
while (($#)); do case $1 in --wave) wave=${2:?}; shift 2;; --profile) profile=${2:?}; shift 2;; --pieces) pieces=${2:?}; shift 2;;
  --allow-concurrent-prodl) concurrent=1; shift;; --dry-run) dry=1; shift;; --local-test) localtest=1; shift;; *) echo "unknown option $1" >&2; exit 2;; esac; done
fail() { echo "REFUSED: $*" >&2; exit 2; }
[[ $profile == alone || $profile == withH ]] || fail 'invalid profile (alone|withH)'
[[ $wave == main || $wave =~ ^r[1-9][0-9]*$ ]] || fail 'invalid wave (main|rN)'
hooks=(PILOT_DRYRUN PILOT_SKIP_MODULES PILOT_LIMIT PILOT_BENCH_METHODS PILOT_BENCH_EXTRA PILOT_TIME_BIN PRODL_UNIT_CMD PRODL_TEST_WALL_S PRODL_TEST_BUDGET_S PRODL_TEST_NOW_OFFSET_S PRODL_BENCH_EXTRA)
if ((localtest)); then [[ ${PILOT_LOCAL_TEST:-0} == 1 && -n ${NC_HOME_ROOT:-} && $NC_HOME_ROOT != /home/fb31/projects/BVS/New_Campaign ]] || fail 'local test needs fake NC_HOME_ROOT and PILOT_LOCAL_TEST=1'
else [[ ${PILOT_LOCAL_TEST:-0} != 1 ]] || fail 'local test hook'; for v in "${hooks[@]}"; do [[ -z ${!v:-} ]] || fail "test hook $v"; done; fi
# ---- no truth for this run (replaces PROD-L's truth-lock check) -------------------------------------------------------------------
[[ -d $RUN_HOME ]] || fail "no staged run folder $RUN_HOME"
bad=$(find "$RUN_HOME" \( -ipath '*truth*' -o -ipath '*holdout*' \) -print -quit)
[[ -z $bad ]] || fail "a truth/holdout path exists under the run folder ($bad): this wave must not have truth on NOTS"
# ---- run idle (later waves) and PROD-L fitting lane finished ------------------------------------------------------------------------
ids=; if [[ -f $RUN_HOME/JOBIDS.tsv ]]; then ids=$(awk -F '\t' 'NR>1 {if($3 !~ /^[0-9]+$/) exit 2; print $3}' "$RUN_HOME/JOBIDS.tsv" | paste -sd, -) || fail 'bad JOBIDS'; fi
[[ $wave == main || -n $ids ]] || fail 'missing previous run job ids'
q=$("$SQUEUE" -h -u fb31 -o '%i|%j|%T|%C') || fail 'squeue failed'
if [[ $wave != main && -n $ids ]] && printf '%s\n' "$q" | awk -F'|' -v ids="$ids" 'BEGIN{split(ids,a,",");for(i in a)x[a[i]]=1} NF{split($1,b,"_");if(x[b[1]])f=1} END{exit !f}'; then fail 'run has active jobs'; fi
lane=$(printf '%s\n' "$q" | awk -F'|' 'NF>=2 && $2 ~ /^lowpL_s[1-4]_/' | head -n 5)
if [[ -n $lane ]]; then
  ((concurrent)) || fail "PROD-L fitting jobs are queued or running (benchmarks are serialized after PROD-L's SMC/repeat lane; HQ may allow --allow-concurrent-prodl): $(printf '%s' "$lane" | tr '\n' ' ')"
  echo "NOTE: --allow-concurrent-prodl given: PROD-L fitting jobs are active; the ceiling check below still applies"
fi
# ---- guard and preconditions ----------------------------------------------------------------------------------------------------------
# HQ D57: the stage was reserved once, BEFORE staging (JOB.md section 2: guard.sh $PLANNED_HOME_MB_STAGE); it is now extracted and already part
# of home usage, so only the growth still to come is asked for here (never the stage size a second time)
planned=$PLANNED_HOME_MB_WAVE; [[ $wave != main ]] || planned=$PLANNED_HOME_MB_MAIN
stage_kb=$(du -sk -- "$RUN_HOME" | cut -f1)
echo "stage on disk: ${stage_kb} KB (already counted in home usage); guard asked for the remaining growth: ${planned} MB"
guardout=$(GUARD="$GUARD" REQUIRED_CAMP_LIMIT_KB="$REQUIRED_CAMP_LIMIT_KB" REQUIRED_HOME_LIMIT_KB="$REQUIRED_HOME_LIMIT_KB" bash "$HERE/guard_check.sh" "$planned" /dev/stdout) || { echo "REFUSED: guard $guardout" >&2; exit 1; }
[[ -n $MODULES_BENCH ]] || fail 'MODULES_BENCH empty'
for f in "$RUN_HOME/OWNER" "$RUN_HOME/STAGED_SHA256.txt" "$BENCH_SUMS" "$LISTS/units.tsv" "$BENCH_DIR/run_bench_case.R" "$BENCH_DIR/R/common.R" "$BENCH_DIR/R/config_lowp.R" \
         "$STUDY/manifests/inputs_manifest_lowp.csv" "$HERE/R/prodl_inputs_check.R" "$HERE/R/bench_env_probe.R" "$HERE/batch_runner.sh"; do [[ -r $f ]] || fail "missing $f"; done
grep -q "lowp_bench $STAMP" "$RUN_HOME/OWNER" || fail 'OWNER mismatch'
[[ $(find "$STUDY/inputs" -type f | wc -l) -eq 1200 ]] || fail 'expected 1,200 staged inputs'
(cd "$HOME_ROOT" && sha256sum --quiet -c "$RUN_HOME/STAGED_SHA256.txt") || fail 'staged hashes mismatch'
source "$HERE/frozen_check.sh"; pilot_check_frozen "$BENCH_DIR" "$BENCH_SUMS" || fail 'frozen benchmark tree mismatch (r2)'
[[ ! -e $LOG_RUN/launch/$wave ]] || fail 'launch exists (use a new wave name)'
[[ ! -e $RUN_HOME/manifests/bench.CLOSED ]] || fail 'bench is CLOSED (make_manifests.sh): no further wave may write to it'
[[ -n $pieces ]] || { [[ $wave == main ]] && pieces=bench || fail '--pieces is required for an rN wave'; }
IFS=, read -r -a ps <<< "$pieces"
declare -A files counts
for piece in "${ps[@]}"; do
 [[ $piece == bench || $piece == benchretry ]] || fail "invalid piece $piece"
 [[ $wave != main || $piece == bench ]] || fail 'the main wave runs the bench piece only'
 [[ -z ${files[$piece]+x} ]] || fail 'duplicate piece'
 f=$LISTS/units.tsv; [[ $wave == main ]] || f=$RUN_HOME/resubmit/${piece}_${wave}.tsv
 [[ -r $f ]] || fail "missing $f"
 max=$(awk -F '\t' -v p="$piece" 'NR>1 && $1==p {if($2 !~ /^[0-9]+$/) exit 2; if(!n++ || $2>m)m=$2} END{if(n)print m;else exit 2}' "$f") || fail 'empty or invalid list'
 files[$piece]=$f; counts[$piece]=$((max+1))
done
thr() { local v; if [[ $profile == alone ]]; then v=THR_A_$1; else v=THR_H_$1; fi; local n=${!v}; ((n<=counts[$1])) || n=${counts[$1]}; echo "$n"; }
step_of() { case $1 in bench) echo s1_bench;; benchretry) echo s2_benchretry;; esac; }
plan() {
 printf 'step\tcpus\tmax_concurrent_tasks\tphase\n'
 [[ $wave != main ]] || printf 's0_verify\t1\t1\tpre\n'
 for piece in "${ps[@]}"; do v=CPUS_$piece; printf '%s\t%s\t%s\tfit\n' "$(step_of "$piece")" "${!v}" "$(thr "$piece")"; done
 printf 's9_collect\t1\t1\tpost\n'
}
export CEIL_ALONE CEIL_WITHH CEIL_COMBINED
mkdir -p -- "$TMP_ROOT"; cdir=$(mktemp -d "$TMP_ROOT/ceiling.XXXXXX")
plan > "$cdir/plan.tsv"; printf '%s' "$q" > "$cdir/squeue.txt"
crc=0; "$PYTHON" "$HERE/ceiling_check.py" --profile "$profile" --plan "$cdir/plan.tsv" --squeue "$cdir/squeue.txt" --own-ids "$ids" --receipt "$cdir/receipt.txt" > "$cdir/stdout.txt" 2>&1 || crc=$?
ceiling=$(cat "$cdir/receipt.txt" 2>/dev/null; cat "$cdir/stdout.txt")
rm -rf -- "$cdir"
[[ $crc == 0 ]] || fail "ceiling check refused (exit $crc): $ceiling"
echo "$ceiling"
launch=
if ((!dry)); then
 mkdir -p "$LOG_RUN/launch/$wave" "$SCR_ROOT/results" "$SCR_ROOT/runs"; launch=$LOG_RUN/launch/$wave
 { printf '%s\n' "$guardout"; echo "D57 stage_on_disk_kb=$stage_kb planned_add_mb=$planned (stage reserved once, before extraction)"; } > "$launch/guard_receipt.txt"
 printf '%s\n' "$ceiling" > "$launch/ceiling_receipt.txt"
 cp "$HERE/bench.env" "$RUN_HOME/STAGED_SHA256.txt" "$RUN_HOME/OWNER" "$BENCH_SUMS" "$launch/"
 sha256sum "$launch/bench.env" > "$launch/bench.env.sha256"; [[ ! -r $HERE/JOB.md ]] || cp "$HERE/JOB.md" "$launch/"
 cp -R "$LISTS" "$launch/lists"; plan > "$launch/plan.tsv"; printf '%s\n' "$q" > "$launch/squeue.txt"
 { echo "# effective environment of the submission $(date -u +%FT%TZ) by $(id -un)@$(hostname) wave=$wave profile=$profile local_test=$localtest allow_concurrent_prodl=$concurrent"
   for v in STAMP RID HOME_ROOT SCR_ROOT GUARD MODULES_BENCH R_LIBS_BENCH R_LIBS_USER_BENCH SBATCH SQUEUE SCANCEL PYTHON PILOT_LOCAL_TEST NC_HOME_ROOT NC_SCR_ROOT "${hooks[@]}"; do echo "$v=[${!v:-}]"; done
 } > "$launch/effective_env.txt"
 for f in "$LOG_RUN/jobids.tsv" "$RUN_HOME/JOBIDS.tsv"; do [[ -e $f ]] || printf 'wave\tstep\tjobid\tarray\tdependency\n' > "$f"; done
fi
submitted=(); next=1000; jid=
abort() { echo "SUBMISSION ABORTED: $*" >&2; echo "$*" >> "$launch/SUBMISSION_ABORTED.txt"; for id in "${submitted[@]}"; do "$SCANCEL" "$id" >> "$launch/SUBMISSION_ABORTED.txt" 2>&1 || echo "cancel failed $id" >> "$launch/SUBMISSION_ABORTED.txt"; done; exit 5; }
submit() {
 local step=$1 cpu=$2 mem=$3 wall=$4 arr=$5 dep=$6 piece=${7:-} exportv="ALL,STAMP=$STAMP,WAVE=$wave" out
 [[ -z $piece ]] || exportv+=",PIECE=$piece,UNITS_FILE=${files[$piece]}"
 local pat='%j'; [[ $arr == - ]] || pat='%A_%a'
 local args=(--no-requeue --parsable "--job-name=lowpB_$step" --account=commons --partition=commons --constraint=sapphirerapids "--chdir=$LOG_RUN" "--export=$exportv" "--cpus-per-task=$cpu" "--mem=$mem" "--time=$wall" "--output=$LOG_RUN/slurm-%x-$pat.out" "--error=$LOG_RUN/slurm-%x-$pat.err")
 [[ $arr == - ]] || args+=("--array=$arr"); [[ $dep == - ]] || args+=("--dependency=$dep" --kill-on-invalid-dep=yes)
 args+=("$HERE/slurm/$step.sbatch")
 if ((dry)); then printf 'sbatch'; printf ' %q' "${args[@]}"; echo; jid=$next; ((next+=1)); return; fi
 { printf 'sbatch'; printf ' %q' "${args[@]}"; echo; } >> "$launch/sbatch_args.txt"
 out=$("$SBATCH" "${args[@]}") || abort "sbatch failed $step"; [[ $out =~ ^[0-9]+$ ]] || abort "bad id $out"
 jid=$out; submitted+=("$jid")
 for f in "$LOG_RUN/jobids.tsv" "$RUN_HOME/JOBIDS.tsv"; do printf '%s\t%s\t%s\t%s\t%s\n' "$wave" "$step" "$jid" "$arr" "$dep" >> "$f" || abort "record failed $jid"; done
}
verify=; dep=-
if [[ $wave == main ]]; then submit s0_verify 1 2G 00:30:00 - -; verify=$jid; dep="afterok:$verify"; fi
fits=()
for piece in bench benchretry; do
 [[ -n ${files[$piece]+x} ]] || continue
 c=CPUS_$piece; m=MEM_$piece; w=WALL_$piece; seconds=${!w}; printf -v wall '%02d:%02d:%02d' "$((seconds/3600))" "$((seconds%3600/60))" "$((seconds%60))"
 submit "$(step_of "$piece")" "${!c}" "${!m}" "$wall" "0-$((counts[$piece]-1))%$(thr "$piece")" "$dep" "$piece"; fits+=("$jid")
done
cdep="afterany"; [[ -z $verify ]] || cdep+=":$verify"; for id in "${fits[@]}"; do cdep+=":$id"; done
submit s9_collect 1 1G 00:15:00 - "$cdep"
