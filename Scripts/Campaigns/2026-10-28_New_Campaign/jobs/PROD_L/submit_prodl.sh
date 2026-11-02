#!/bin/bash
set -euo pipefail
HERE=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
STAMP=${STAMP:-$(date -u +%Y%m%dT%H%MZ)}; export STAMP
[[ $STAMP =~ ^[0-9]{8}T[0-9]{4}Z$ ]] || exit 2
source "$HERE/prodl.env"
SBATCH=${SBATCH:-sbatch}; SQUEUE=${SQUEUE:-squeue}; SCANCEL=${SCANCEL:-scancel}; PYTHON=${PYTHON:-python3}
wave=; profile=; pieces=; phase=; dry=0; localtest=0; scan=0
while (($#)); do case $1 in --wave) wave=${2:?}; shift 2;; --profile) profile=${2:?}; shift 2;; --pieces) pieces=${2:?}; shift 2;; --phase) phase=${2:?}; shift 2;; --p5-scan) scan=1; shift;; --dry-run) dry=1; shift;; --local-test) localtest=1; shift;; *) exit 2;; esac; done
fail() { echo "REFUSED: $*" >&2; exit 2; }
[[ $wave != bench && ,$pieces, != *,bench,* ]] || fail 'benchmark arm gated on BENCH-FIX + Sol ACCEPT (D36.2, D42.7); see bench_hook/README.md'
if ((scan)) && [[ -z $profile ]]; then profile=withH; fi
[[ $profile == alone || $profile == withH ]] || fail 'invalid profile'
if ((scan)); then [[ -z $wave && -z $pieces && $phase =~ ^(initial|final[0-9]*|r[0-9]+)$ ]] || fail 'invalid scan options'; wave=p5scan_$phase; else [[ -z $phase && ( $wave == main || $wave == p5 || $wave =~ ^p5r[1-9][0-9]*$ || $wave =~ ^r[1-9][0-9]*$ ) ]] || fail 'invalid wave'; fi
hooks=(PILOT_DRYRUN PILOT_SKIP_MODULES PILOT_LIMIT PILOT_BENCH_METHODS PILOT_BENCH_EXTRA PILOT_TIME_BIN PRODL_UNIT_CMD PRODL_TEST_WALL_S PRODL_TEST_BUDGET_S PRODL_TEST_NOW_OFFSET_S)
if ((localtest)); then [[ ${PILOT_LOCAL_TEST:-0} == 1 && -n ${NC_HOME_ROOT:-} && $NC_HOME_ROOT != /home/fb31/projects/BVS/New_Campaign ]] || fail 'local test needs fake NC_HOME_ROOT and PILOT_LOCAL_TEST=1'
else [[ ${PILOT_LOCAL_TEST:-0} != 1 ]] || fail 'local test hook'; for v in "${hooks[@]}"; do [[ -z ${!v:-} ]] || fail "test hook $v"; done; fi
for d in "$STUDY/truth" "$STUDY/dev/truth"; do [[ -d $d && -r $d && $(stat -c %a "$d") == 755 ]] || fail 'a wave is locked: do not run the guard; wait for its unlock or use recover_truth.sh'; done
for d in "$STUDY/truth" "$STUDY/dev/truth"; do [[ -z $(find "$d" -type f ! -readable -print -quit) ]] || fail 'a wave is locked: do not run the guard; wait for its unlock or use recover_truth.sh'; done
ids=; if [[ -f $RUN_HOME/JOBIDS.tsv ]]; then ids=$(awk -F '\t' 'NR>1 {if($3 !~ /^[0-9]+$/) exit 2; print $3}' "$RUN_HOME/JOBIDS.tsv" | paste -sd, -) || fail 'bad JOBIDS'; fi
[[ $wave == main || -n $ids ]] || fail 'missing previous run job ids'
if [[ $wave != main && -n $ids ]]; then
 q=$("$SQUEUE" -h -u fb31 -o '%i|%j|%T|%C') || fail 'squeue failed'
 if printf '%s\n' "$q" | awk -F'|' -v ids="$ids" 'BEGIN{split(ids,a,",");for(i in a)x[a[i]]=1} NF{split($1,b,"_");if(x[b[1]])f=1} END{exit !f}'; then fail 'run has active jobs'; fi
fi
planned=$PLANNED_HOME_MB_WAVE; [[ $wave != main ]] || planned=$PLANNED_HOME_MB_MAIN
guardout=$(GUARD="$GUARD" REQUIRED_CAMP_LIMIT_KB="$REQUIRED_CAMP_LIMIT_KB" REQUIRED_HOME_LIMIT_KB="$REQUIRED_HOME_LIMIT_KB" bash "$HERE/guard_check.sh" "$planned" /dev/stdout) || { echo "REFUSED: guard $guardout" >&2; exit 1; }
[[ -n $MODULES ]] || fail 'MODULES empty'
for f in "$RUN_HOME/OWNER" "$RUN_HOME/STAGED_SHA256.txt" "$V221_SUMS" "$LISTS/units.tsv" "$V221_DIR/study/run_case.R" "$V221_DIR/study/adapter.R" "$V221_DIR/tools/p5_scan.R" "$CORE_DIR/v3.R" "$CORE_DIR/cpp/v3_score.h" "$ENUM_DIR/lowp_enum.R" "$ENUM_DIR/exact_contract.R" "$ENUM_DIR/run_enum_dataset.R" "$LOWPR_DIR/lowp_verify_nots.R" "$STUDY/manifests/inputs_manifest_lowp.csv" "$STUDY/manifests/truth_manifest_lowp.csv" "$STUDY/dev/manifests/inputs_manifest_lowp.csv" "$STUDY/dev/manifests/truth_manifest_lowp.csv" "$CODE/lowp/tests/test_truth_lock_linux.sh" "$HERE/truth_wave.sh" "$HERE/truth_lib.sh"; do [[ -r $f ]] || fail "missing $f"; done
grep -q "lowp_prodL $STAMP" "$RUN_HOME/OWNER" || fail 'OWNER mismatch'
for spec in inputs:1200 truth:1200 dev/truth:60; do d=${spec%:*}; n=${spec#*:}; [[ $(find "$STUDY/$d" -type f | wc -l) -eq $n ]] || fail "wrong count $d"; done
(cd "$HOME_ROOT" && sha256sum --quiet -c "$RUN_HOME/STAGED_SHA256.txt") || fail 'staged hashes mismatch'
source "$HERE/frozen_check.sh"; pilot_check_frozen "$V221_DIR" "$V221_SUMS" || fail 'frozen mismatch'
[[ ! -e $LOG_RUN/launch/$wave ]] || fail 'launch exists'
[[ -n $pieces ]] || { case $wave in p5|p5r*) pieces=p5;; p5scan_*) pieces=;; *) pieces=enum20,enum30,smc,smcrep;; esac; }
IFS=, read -r -a ps <<< "$pieces"
# a CLOSED piece (make_manifests.sh) may already have been pulled and deleted from scratch: no wave may write to it again
closed_of() { case $1 in p5) printf 'smc smcrep';; *) printf '%s' "$1";; esac; }
if ((scan)); then chk="smc smcrep"; else chk=; for piece in "${ps[@]}"; do chk+=" $(closed_of "$piece")"; done; fi
for c in $chk; do [[ ! -e $RUN_HOME/manifests/$c.CLOSED ]] || fail "$c is CLOSED (make_manifests.sh): no further wave or scan may use it"; done
declare -A files counts
for piece in "${ps[@]}"; do
 [[ $piece == enum20 || $piece == enum30 || $piece == smc || $piece == smcrep || $piece == p5 ]] || fail "invalid piece $piece"
 [[ $wave == p5* && $piece == p5 || $wave != p5* && $piece != p5 ]] || fail 'invalid piece for wave'
 [[ -z ${files[$piece]+x} ]] || fail 'duplicate piece'
 f=$LISTS/units.tsv; [[ $wave != r* ]] || f=$RUN_HOME/resubmit/${piece}_${wave}.tsv; [[ $wave != p5* ]] || f=$RUN_HOME/p5/units_${wave}.tsv
 [[ -r $f ]] || fail "missing $f"
 max=$(awk -F '\t' -v p="$piece" 'NR>1 && $1==p {if($2 !~ /^[0-9]+$/) exit 2; if(!n++ || $2>m)m=$2} END{if(n)print m;else exit 2}' "$f") || fail 'empty or invalid list'
 files[$piece]=$f; counts[$piece]=$((max+1))
done
thr() { local v; if [[ $profile == alone ]]; then v=THR_A_$1; else v=THR_H_$1; fi; local n=${!v}; ((n<=counts[$1])) || n=${counts[$1]}; echo "$n"; }
plan() {
 printf 'step\tcpus\tmax_concurrent_tasks\tphase\n'
 if ((scan)); then printf 's5_p5scan\t1\t1\tpre\n'; return; fi
 [[ $wave != main ]] || printf 's0_build\t2\t1\tpre\ns0_verify\t1\t1\tpre\n'
 printf 's0_truthlock\t1\t1\tpre\ns0_lock\t1\t1\tpre\n'
 for piece in "${ps[@]}"; do v=CPUS_$piece; case $piece in enum20) step=s1_enum20;; enum30) step=s1_enum30;; smc) step=s2_smc;; smcrep) step=s3_smcrep;; p5) step=s4_p5;; esac; printf '%s\t%s\t%s\tfit\n' "$step" "${!v}" "$(thr "$piece")"; done
 printf 's8_unlock\t1\t1\tpost\ns9_collect\t1\t1\tpost\n'
}
q=$("$SQUEUE" -h -u fb31 -o '%i|%j|%T|%C') || fail 'squeue failed'
export CEIL_ALONE CEIL_WITHH CEIL_COMBINED
# real files (not /dev/stdout or <(...)): portable to any Python, and kept as evidence. Transient copies live in the run's scratch tmp folder.
mkdir -p -- "$TMP_ROOT"; cdir=$(mktemp -d "$TMP_ROOT/ceiling.XXXXXX")
plan > "$cdir/plan.tsv"; printf '%s' "$q" > "$cdir/squeue.txt"
crc=0; "$PYTHON" "$HERE/ceiling_check.py" --profile "$profile" --plan "$cdir/plan.tsv" --squeue "$cdir/squeue.txt" --own-ids "$ids" --receipt "$cdir/receipt.txt" > "$cdir/stdout.txt" 2>&1 || crc=$?
ceiling=$(cat "$cdir/receipt.txt" 2>/dev/null; cat "$cdir/stdout.txt")
rm -rf -- "$cdir"
[[ $crc == 0 ]] || fail "ceiling check refused (exit $crc): $ceiling"
echo "$ceiling"
if ((!dry)); then
 mkdir -p "$LOG_RUN/launch/$wave" "$SCR_ROOT/results" "$SCR_ROOT/runs"; launch=$LOG_RUN/launch/$wave
 printf '%s\n' "$guardout" > "$launch/guard_receipt.txt"; printf '%s\n' "$ceiling" > "$launch/ceiling_receipt.txt"
 cp "$HERE/prodl.env" "$RUN_HOME/STAGED_SHA256.txt" "$RUN_HOME/OWNER" "$V221_SUMS" "$launch/"
 sha256sum "$launch/prodl.env" > "$launch/prodl.env.sha256"; [[ ! -r $HERE/JOB.md ]] || cp "$HERE/JOB.md" "$launch/"
 cp -R "$LISTS" "$launch/lists"; plan > "$launch/plan.tsv"; printf '%s\n' "$q" > "$launch/squeue.txt"
 # named variables only (as the pilot): never dump the whole login environment, which may hold tokens (charter section 3)
 { echo "# effective environment of the submission $(date -u +%FT%TZ) by $(id -un)@$(hostname) wave=$wave profile=$profile local_test=$localtest"
   for v in STAMP RID HOME_ROOT SCR_ROOT GUARD MODULES R_LIBS_LOWP R_LIBS_USER_LOWP SBATCH SQUEUE SCANCEL PYTHON PILOT_LOCAL_TEST NC_HOME_ROOT NC_SCR_ROOT "${hooks[@]}"; do echo "$v=[${!v:-}]"; done
 } > "$launch/effective_env.txt"
 for f in "$LOG_RUN/jobids.tsv" "$RUN_HOME/JOBIDS.tsv"; do [[ -e $f ]] || printf 'wave\tstep\tjobid\tarray\tdependency\n' > "$f"; done
fi
submitted=(); next=1000; jid=
abort() { echo "SUBMISSION ABORTED: $*" >&2; echo "$*" >> "$launch/SUBMISSION_ABORTED.txt"; for id in "${submitted[@]}"; do "$SCANCEL" "$id" >> "$launch/SUBMISSION_ABORTED.txt" 2>&1 || echo "cancel failed $id" >> "$launch/SUBMISSION_ABORTED.txt"; done; exit 5; }
submit() {
 local step=$1 cpu=$2 mem=$3 wall=$4 arr=$5 dep=$6 piece=${7:-} exportv="ALL,STAMP=$STAMP,WAVE=$wave,PHASE=$phase" out
 [[ -z $piece ]] || exportv+=",PIECE=$piece,UNITS_FILE=${files[$piece]}"
 local pat='%j'; [[ $arr == - ]] || pat='%A_%a'      # as the pilot: %j for plain jobs, %A_%a for array tasks
 local args=(--no-requeue --parsable "--job-name=lowpL_$step" --account=commons --partition=commons --constraint=sapphirerapids "--chdir=$LOG_RUN" "--export=$exportv" "--cpus-per-task=$cpu" "--mem=$mem" "--time=$wall" "--output=$LOG_RUN/slurm-%x-$pat.out" "--error=$LOG_RUN/slurm-%x-$pat.err")
 [[ $arr == - ]] || args+=("--array=$arr"); [[ $dep == - ]] || args+=("--dependency=$dep" --kill-on-invalid-dep=yes)
 args+=("$HERE/slurm/$step.sbatch")
 if ((dry)); then printf 'sbatch'; printf ' %q' "${args[@]}"; echo; jid=$next; ((next+=1)); return; fi
 { printf 'sbatch'; printf ' %q' "${args[@]}"; echo; } >> "$launch/sbatch_args.txt"
 out=$("$SBATCH" "${args[@]}") || abort "sbatch failed $step"; [[ $out =~ ^[0-9]+$ ]] || abort "bad id $out"
 jid=$out; submitted+=("$jid")
 for f in "$LOG_RUN/jobids.tsv" "$RUN_HOME/JOBIDS.tsv"; do printf '%s\t%s\t%s\t%s\t%s\n' "$wave" "$step" "$jid" "$arr" "$dep" >> "$f" || abort "record failed $jid"; done
}
# HQ D63: the scan's time limit scales with the records it reads (smc + smcrep units of the run's list), never the old fixed 30 minutes
if ((scan)); then
 nprim=$(awk -F'\t' 'NR>1 && ($1=="smc" || $1=="smcrep")' "$LISTS/units.tsv" | wc -l)
 # P5 retry records the scan also reads: at most one per row of the expected P5 inventory (none before the initial scan)
 nretry=0; [[ ! -f $RUN_HOME/p5/expected.tsv ]] || nretry=$(awk 'NR>1 && NF' "$RUN_HOME/p5/expected.tsv" | wc -l)
 nscan=$((nprim + nretry))
 ssec=$(( P5SCAN_BASE_S + (nscan * P5SCAN_MS_PER_UNIT + 999) / 1000 )); (( ssec >= P5SCAN_MIN_S )) || ssec=$P5SCAN_MIN_S
 printf -v swall '%02d:%02d:%02d' "$((ssec/3600))" "$((ssec%3600/60))" "$((ssec%60))"
 echo "P5 scan: $nscan records ($nprim primaries + $nretry possible retries) -> time limit $swall (D63: max(${P5SCAN_MIN_S}s, ${P5SCAN_BASE_S}s + ${P5SCAN_MS_PER_UNIT} ms x records))"
 submit s5_p5scan 1 2G "$swall" - -; exit 0
fi
build=; verify=; if [[ $wave == main ]]; then submit s0_build 2 4G 00:40:00 - -; build=$jid; submit s0_verify 1 2G 00:30:00 - -; verify=$jid; fi
dep=-; [[ -z $verify ]] || dep=afterok:$verify
submit s0_truthlock 1 2G 00:30:00 - "$dep"; truth=$jid
submit s0_lock 1 1G 00:10:00 - "afterok:$truth"; lock=$jid
base="afterok:$truth:$lock"; [[ -z $build ]] || base="afterok:$build:$verify:$truth:$lock"
fits=(); smcid=
for piece in enum20 enum30 smc smcrep p5; do
 [[ -n ${files[$piece]+x} ]] || continue
 case $piece in enum20) step=s1_enum20;; enum30) step=s1_enum30;; smc) step=s2_smc;; smcrep) step=s3_smcrep;; p5) step=s4_p5;; esac
 c=CPUS_$piece; m=MEM_$piece; w=WALL_$piece; seconds=${!w}; printf -v wall '%02d:%02d:%02d' "$((seconds/3600))" "$((seconds%3600/60))" "$((seconds%60))"
 arr="0-$((counts[$piece]-1))%$(thr "$piece")"; [[ $wave != main || $piece != enum20 ]] || arr=-
 dep=$base; [[ $piece != smcrep || -z $smcid ]] || dep+=",afterany:$smcid"
 submit "$step" "${!c}" "${!m}" "$wall" "$arr" "$dep" "$piece"; fits+=("$jid"); [[ $piece != smc ]] || smcid=$jid
done
dep="afterany:$lock"; for id in "${fits[@]}"; do dep+=":$id"; done
submit s8_unlock 1 1G 00:15:00 - "$dep"; unlock=$jid
dep="afterany:$truth:$unlock"; [[ -z $build ]] || dep="afterany:$build:$verify:$truth:$unlock"
submit s9_collect 1 1G 00:15:00 - "$dep"
