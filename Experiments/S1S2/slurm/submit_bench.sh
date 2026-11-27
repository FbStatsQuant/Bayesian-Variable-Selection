#!/usr/bin/env bash
# submit_bench.sh -- run on NOTS from the deploy tree. S1 / S2 BENCHMARK grids (owner GO 2026-11-26/27 via HQ), one
# method at a time, in the staged batches. Sibling of submit_s2_batches.sh, same conventions: it PRINTS the sbatch
# commands and submits ONLY with --go.
#   submit_bench.sh --suite 1|2 --method M --batch K --reps LO-HI [--classes C1,C2] [--max-conc N]
#                   [--dependency afterany:JOBID[:JOBID...]] [--owner-ok-asi-full] [--test-only | --go]
# Methods: a (suite, method) row of slurm/bench_budget.tsv and a name in harness/methods.R; never smcbvs (S1 asi signed by
# the owner 2026-11-27). Batches (HQ protocol): K=1 reps 1-25, K=2 26-60, K=3 61-100 (--reps must be exactly that range;
# it is a cross-check). A batch = reps LO..HI of every setting of the suite in the chosen classes.
# Packing: one array task = one (setting, block of reps), block from bench_budget.tsv; the task list
# slurm/tasks_S<suite>_bench_<M>.tsv (task_id = (cell-1)*100 + rep_lo, make_bench_tasks.sh) is regenerated here and must
# equal the deployed copy. One array per class (one --mem/--time per array):
#   S2: S2N50P1000 cells 1-60 (n 50), S2N100P1000 cells 61-120 (n 100), p 1000
#   S1: P500N500 cells 1-4, P5000N500 5-8, P500N1000 9-12, P5000N1000 13-16 (cross-checked against settings.tsv)
#   mem = bench_budget.tsv mem (mem_p5000 for the p=5000 classes), time = block x per-rep limit + 600 s (limit =
#   fit_limit_sec; fit_limit_p5000 for the p=5000 classes when not "-"; at most 24 h = commons MaxWall), partition
#   commons, --constraint=cascadelake (S1 SMC-BVS keeps the Sapphire Rapids nodes; S2 rule); override per class with
#   MEM_<C>, TIME_<C>, PART_<C>, CONSTRAINT_<C> (empty = unpinned).
# Concurrency: HARD ceiling 468 running benchmark tasks in total (s1bm_* + s2bm_*, all methods), and never the commons
# slots kept for S1 SMC-BVS: the initial %K throttles sum to --max-conc (default min(468, 768 - max(300, S1 SMC tasks
# running on commons) - other fb31 tasks running on commons) - benchmark tasks already running; at least 1), split over
# the classes in proportion to their task counts; minus the PENDING tasks of higher-priority benchmark arrays (queue
# order, owner 2026-11-27: S1 cheap four > S1 asi > S2 cheap four > S2 asi); s2_throttle.sh (Owls timer, 10 min) re-tunes
# them live in that priority order.
# Budget (HARD stop per (suite, method), bench_budget.tsv budget_cpuh): --go refuses when the billed CPU-h of all the
# method's s<suite>bm jobs (sacct CPUTimeRAW of the job ids logged under S<suite>bm.<M>.*) already reach it; while
# running, check_batch.sh turns it into a STOP (the watcher then cancels the pending tasks).
# Hold (bench_budget.tsv hold = owner_ok_after_b1, i.e. S2 asi; S1 asi has none): --go for any batch other than 1 refuses unless
# --owner-ok-asi-full is given; that flag is recorded in column 6 of submissions.tsv.
# Job names s<suite>bm_<M>_b<K>_<class>; submissions.tsv batch field "S<suite>bm.<M>.<K>" (never matches S1 "K" or
# S2 SMC "S2.K"). --go refuses while any s<suite>bm_<M>_b<K>_* job is queued; after the batch has ended, --go again
# resubmits it and every rep whose record is already ok is skipped (resubmitting a block re-fits only its non-ok reps).
# --oom-pass [--oom-mem 64G] (HQ ruling 2026-11-27, S2 bas_mc3; run after batch K has ended): ONE re-fit pass, at
# --oom-mem, of exactly the reps of batch K whose json is the memory-kill stub "failed: harness: R process exited rc=137
# during the fit" (bench_array.sbatch with S1S2_REFIT_OOM=1 re-fits only those; failed-for-another-reason reps stay).
# Only the array tasks holding such reps are submitted; job names s<suite>bm_<M>_b<K>m_<class>, submissions.tsv batch
# field "S<suite>bm.<M>.<K>m" (counts toward the method budget). An rc=137 rep that is killed again at --oom-mem keeps a
# stub (new slurm_job) = computational failure; there is no further pass. Watch it with watch_batch.sh --jobs <its ids>
# --prefix s<suite>bm_<M>_b<K>m_ --tag <M>_s<suite>b<K>m --no-package.
# Watch / pull / package / record with --suite S --method M (watch_batch.sh, check_batch.sh, pull_to_owls.sh,
# sacct_record.sh, package_for_desktop.sh); unit S1S2_<M>_s<suite>b<K>.
set -euo pipefail
ENG=/home/fb31/SMC-BVS/_local/engineering
DEPLOY=${S1S2_DEPLOY:-$ENG/S1S2/deploy}
SL=$DEPLOY/S1S2/slurm
SBATCH_FILE=$SL/bench_array.sbatch
CONF=$SL/bench_budget.tsv
SETTINGS=$DEPLOY/S1S2/specs/settings.tsv
LOGDIR=${S1S2_LOGDIR:-/scratch/fb31/SMC-BVS/runs/S1S2/logs}
SUBLOG=${S1S2_SUBLOG:-$ENG/S1S2/logs/submissions.tsv}
CPU_CAP=1536; TASK_CAP=768; MEM_CAP_G=2304; SUBMIT_CAP=5000; BENCH_CAP=468; RESERVE=300; ALLOC_CPUS_PER_TASK=2

suite=""; method=""; batch=""; reps=""; classes=""; maxconc=""; dep=""; mode=print; ownerok=0; oompass=0; oommem=64G
while (($#)); do case "$1" in
  --suite) suite="$2"; shift 2;; --method) method="$2"; shift 2;; --batch) batch="$2"; shift 2;; --reps) reps="$2"; shift 2;;
  --classes) classes="$2"; shift 2;; --max-conc) maxconc="$2"; shift 2;; --dependency) dep="$2"; shift 2;;
  --owner-ok-asi-full) ownerok=1; shift;; --oom-pass) oompass=1; shift;; --oom-mem) oommem="$2"; shift 2;; --test-only) mode=test; shift;; --go) mode=go; shift;;
  -h|--help) sed -n '2,41p' "$0"; exit 0;; *) echo "unknown arg $1" >&2; exit 64;; esac; done
[[ "$suite" == 1 || "$suite" == 2 ]] || { echo "need --suite 1|2" >&2; exit 64; }
[[ "$method" =~ ^[a-z0-9_]+$ && "$method" != smcbvs ]] || { echo "need --method <benchmark method> (not smcbvs)" >&2; exit 64; }
[[ "$batch" =~ ^[1-3]$ ]] || { echo "need --batch 1|2|3" >&2; exit 64; }
[[ "$reps" =~ ^([0-9]+)-([0-9]+)$ ]] || { echo "need --reps LO-HI" >&2; exit 64; }
lo=${BASH_REMATCH[1]}; hi=${BASH_REMATCH[2]}
[[ "$oommem" =~ ^[0-9]+G$ ]] || { echo "--oom-mem: e.g. 64G" >&2; exit 64; }
RUNS=${S1S2_RUNS:-/scratch/fb31/SMC-BVS/runs/S1S2}
bsfx=$batch; (( oompass )) && bsfx=${batch}m
plan=(x 1-25 26-60 61-100)
[[ "$lo-$hi" == "${plan[$batch]}" ]] || { echo "batch $batch is reps ${plan[$batch]} (HQ plan), not $lo-$hi" >&2; exit 64; }
awk -v m="$method" '$1 == m && $2 == "=" && $3 ~ /^list\(file/ { f = 1 } END { exit !f }' "$DEPLOY/S1S2/harness/methods.R" ||
  { echo "FATAL: method $method not in harness/methods.R" >&2; exit 65; }
row=$(awk -F'\t' -v s="$suite" -v m="$method" 'NR > 1 && $1 == s && $2 == m' "$CONF")
[[ -n "$row" ]] || { echo "REFUSED: no (suite $suite, $method) row in bench_budget.tsv (not configured / not signed)" >&2; exit 67; }
IFS=$'\t' read -r _ _ block budget limit cmem cmem5k hold _ lim5k _ <<< "$row"
[[ "${lim5k:--}" == - ]] && lim5k=$limit
[[ "$block" =~ ^[0-9]+$ && "$limit" =~ ^[0-9]+$ && "$lim5k" =~ ^[0-9]+$ && "$budget" =~ ^[0-9]+(\.[0-9]+)?$ && "$cmem" =~ ^[0-9]+G$ ]] ||
  { echo "FATAL: bad bench_budget.tsv row: $row" >&2; exit 65; }
[[ "$cmem5k" == - ]] && cmem5k=$cmem
TASKS=$SL/tasks_S${suite}_bench_${method}.tsv
"$SL/make_bench_tasks.sh" --suite "$suite" --method "$method" --config "$CONF" | cmp -s - "$TASKS" ||
  { echo "FATAL: $TASKS missing or not what make_bench_tasks.sh gives for bench_budget.tsv (regenerate + redeploy)" >&2; exit 65; }

if [[ $suite == 2 ]]; then
  declare -A CELLS=( [S2N50P1000]="$(seq -s' ' 1 60)" [S2N100P1000]="$(seq -s' ' 61 120)" )
  declare -A NVAL=( [S2N50P1000]=50 [S2N100P1000]=100 ); declare -A PVAL=( [S2N50P1000]=1000 [S2N100P1000]=1000 )
  classes=${classes:-S2N50P1000,S2N100P1000}
else
  declare -A CELLS=( [P500N500]="1 2 3 4" [P5000N500]="5 6 7 8" [P500N1000]="9 10 11 12" [P5000N1000]="13 14 15 16" )
  declare -A NVAL=( [P500N500]=500 [P5000N500]=500 [P500N1000]=1000 [P5000N1000]=1000 )
  declare -A PVAL=( [P500N500]=500 [P5000N500]=5000 [P500N1000]=500 [P5000N1000]=5000 )
  classes=${classes:-P500N500,P500N1000,P5000N500,P5000N1000}
fi
IFS=, read -ra CL <<< "$classes"
nrep=$(( hi - lo + 1 ))
for c in "${CL[@]}"; do
  [[ -n "${CELLS[$c]:-}" ]] || { echo "unknown class $c for suite $suite" >&2; exit 64; }
  want=$(awk -F'\t' -v s="$suite" -v n="${NVAL[$c]}" -v p="${PVAL[$c]}" '$2 == s && $4 == n && $5 == p { print $3 }' "$SETTINGS" | sort -n | paste -sd' ' -)
  [[ "$want" == "${CELLS[$c]}" ]] || { echo "FATAL: class $c cells do not match settings.tsv" >&2; exit 65; }
done

secs() { local t=$1 d=0; [[ $t == *-* ]] && { d=${t%%-*}; t=${t#*-}; }; IFS=: read -r h m s <<< "$t"; echo $(( d*86400 + 10#$h*3600 + 10#$m*60 + 10#$s )); }
hms() { printf '%02d:%02d:%02d' $(( $1 / 3600 )) $(( $1 % 3600 / 60 )) $(( $1 % 60 )); }

( cd "$DEPLOY" && sha256sum --quiet -c MANIFEST.sha256 ) || { echo "FATAL: deploy manifest check failed" >&2; exit 65; }
mhash=$(sha256sum "$DEPLOY/MANIFEST.sha256" | cut -c1-64)
echo "# deploy $DEPLOY  manifest_sha256=$mhash  ($(sed -n 's/^source: //p' "$DEPLOY/DEPLOY_INFO.txt"))"
echo "# S$suite $method batch $batch reps $lo-$hi: block $block reps/task, per-rep limit ${limit}s (p=5000: ${lim5k}s), budget ${budget} billed CPU-h, hold ${hold}"

# billed CPU-h so far of ALL this method's benchmark jobs on this suite (every batch)
bjobs=$( [[ -f "$SUBLOG" ]] && awk -F'\t' -v k="S${suite}bm.${method}." 'index($2, k) == 1 { print $3 }' "$SUBLOG" | sort -u | paste -sd, - || true)
used=0.0
if [[ -n "$bjobs" ]]; then used=$( { sacct -j "$bjobs" -X -n -P -o CPUTimeRAW 2>/dev/null || true; } | awk '{ s += $1 } END { printf "%.1f", s / 3600 }'); fi
echo "# billed CPU-h so far (S${suite}bm.${method}.*: ${bjobs:-no jobs}): ${used} of ${budget}"
over=$(awk -v u="$used" -v b="$budget" 'BEGIN { print (u >= b) ? 1 : 0 }')

snap=$(squeue -u fb31 -h -r -t R -o '%P|%j')
s1c=$(awk -F'|' '$1 == "commons" && $2 ~ /^s1smc_/' <<< "$snap" | wc -l)
oc=$(awk -F'|' '$1 == "commons" && $2 !~ /^(s1smc_|s2smc_|s[12]bm_)/' <<< "$snap" | wc -l)
bmr=$(awk -F'|' '$2 ~ /^s[12]bm_/' <<< "$snap" | wc -l)
# benchmark priority tier (same function as s2_throttle.sh): 1 S1 cheap four, 2 S1 asi, 3 S2 cheap four, 4 S2 asi
tier() { case "$1" in s1bm_asi_*) echo 2;; s1bm_*) echo 1;; s2bm_asi_*) echo 4;; s2bm_*) echo 3;; *) echo 0;; esac; }
mytier=$(tier "s${suite}bm_${method}_")
hpd=$(squeue -u fb31 -h -r -t PD -o '%j' | awk -v t="$mytier" '
  /^s[12]bm_/ { x = /^s1bm_asi_/ ? 2 : /^s1bm_/ ? 1 : /^s2bm_asi_/ ? 4 : 3; if (x < t) n++ } END { print n + 0 }')
if [[ -z "$maxconc" ]]; then
  room=$(( TASK_CAP - (s1c > RESERVE ? s1c : RESERVE) - oc )); (( room > BENCH_CAP )) && room=$BENCH_CAP
  maxconc=$(( room - bmr - hpd )); (( maxconc >= 1 )) || maxconc=1
fi
(( maxconc >= 1 && maxconc <= BENCH_CAP )) || { echo "--max-conc must be 1..$BENCH_CAP" >&2; exit 64; }
echo "# commons running: S1 SMC $s1c, other $oc; benchmark tasks running $bmr, pending in higher-priority tiers $hpd (this is tier $mytier) -> initial concurrency $maxconc (ceiling $BENCH_CAP benchmark tasks; s2_throttle.sh re-tunes it)"

# per class: the batch's task ids, compressed per cell as first-last:step
total=0; declare -A IDS NT
for c in "${CL[@]}"; do
  read -r ids n fits < <(awk -F'\t' -v b="$batch" -v cells=" ${CELLS[$c]} " '
    NR > 1 && $5 == b { cell = ($1 - $3) / 100 + 1; if (index(cells, " " cell " ")) { k[cell] = k[cell] " " $1; n++; f += $4 - $3 + 1 } }
    END { out = ""
      for (cell = 1; cell <= 200; cell++) if (cell in k) { m = split(substr(k[cell], 2), a, " "); s = ""
        if (m == 1) s = a[1]; else { d = a[2] - a[1]; ok = 1; for (i = 3; i <= m; i++) if (a[i] - a[i-1] != d) ok = 0
          if (ok) s = a[1] "-" a[m] (d == 1 ? "" : ":" d); else for (i = 1; i <= m; i++) s = s (i > 1 ? "," : "") a[i] }
        out = out (out == "" ? "" : ",") s }
      print out, n + 0, f + 0 }' "$TASKS")
  ncell=$(wc -w <<< "${CELLS[$c]}")
  (( fits == ncell * nrep )) || { echo "FATAL: class $c: task list covers $fits fits, expected $(( ncell * nrep ))" >&2; exit 65; }
  if (( oompass )); then   # only the tasks of this batch holding an rc=137 stub rep
    oids=(); nstub=0
    for cell in ${CELLS[$c]}; do
      if [[ $suite == 2 ]]; then st=$(printf 'S2_%03d' "$cell"); else st=$(printf 'S1_%02d' "$cell"); fi
      for (( r = lo; r <= hi; r++ )); do
        j=$(printf '%s/%s/%s/rep_%03d.json' "$RUNS" "$method" "$st" "$r")
        if [[ -f "$j" ]] && grep -Eq '"status": ?"failed: harness: R process exited rc=137 during the fit"' "$j"; then
          t=$(awk -F'\t' -v s="$st" -v r="$r" 'NR > 1 && $2 == s && $3 <= r && r <= $4 { print $1 }' "$TASKS")
          [[ "$t" =~ ^[0-9]+$ ]] || { echo "FATAL: no task for $st rep $r" >&2; exit 65; }
          oids+=("$t"); nstub=$(( nstub + 1 ))
        fi
      done
    done
    ids=$(printf '%s\n' "${oids[@]}" | awk 'NF' | sort -nu | paste -sd, -); n=$( [[ -n "$ids" ]] && tr ',' '\n' <<< "$ids" | wc -l || echo 0)
    echo "# oom-pass class $c: $nstub rc=137 reps in $n tasks${ids:+: $ids}"
    (( n > 0 )) || continue
  fi
  IDS[$c]=$ids; NT[$c]=$n; total=$(( total + n ))
done
if (( oompass )); then
  CL2=(); for c in "${CL[@]}"; do [[ -n "${NT[$c]:-}" ]] && CL2+=("$c"); done; CL=("${CL2[@]}")
  (( total > 0 )) || { echo "# oom-pass: no rc=137 stub in S$suite $method batch $batch; nothing to submit"; exit 0; }
fi

sumK=0; sumMem=0; cmds=()
for c in "${CL[@]}"; do
  n=${NT[$c]}
  K=$(( total <= maxconc ? n : (n * maxconc) / total )); (( K >= 1 )) || K=1
  dm=$cmem; dl=$limit; (( ${PVAL[$c]} == 5000 )) && { dm=$cmem5k; dl=$lim5k; }
  (( oompass )) && dm=$oommem
  dtime=$(hms $(( block * dl + 600 )))
  v="MEM_$c"; mem=${!v:-$dm}; v="TIME_$c"; tl=${!v:-$dtime}; v="PART_$c"; part=${!v:-commons}
  v="CONSTRAINT_$c"; cons=${!v-cascadelake}
  (( $(secs "$tl") <= 86400 )) || { echo "FATAL: class $c time $tl > 24 h (commons MaxWall)" >&2; exit 65; }
  memg=${mem%G}; sumK=$(( sumK + K )); sumMem=$(( sumMem + K * memg ))
  xenv=""; (( oompass )) && xenv=",S1S2_REFIT_OOM=1"
  cmd=(sbatch --parsable --job-name="s${suite}bm_${method}_b${bsfx}_${c}" --partition="$part" --cpus-per-task=1 --mem="$mem" --time="$tl"
       --array="${IDS[$c]}%${K}" --export="ALL,S1S2_SUITE=$suite,S1S2_METHOD=$method$xenv")
  [[ -n "$cons" ]] && cmd+=(--constraint="$cons")
  [[ -n "$dep" ]] && cmd+=(--dependency="$dep")
  cmd+=("$SBATCH_FILE")
  cmds+=("$(printf '%q ' "${cmd[@]}")")
  echo "# class $c: cells ${CELLS[$c]%% *}-${CELLS[$c]##* } reps $lo-$hi -> $n tasks ($(( $(wc -w <<< "${CELLS[$c]}") * nrep )) fits), %$K concurrent, mem $mem, time $tl, $part${cons:+, constraint $cons}"
done
echo "# S$suite $method batch $batch: $total tasks; peak concurrency $sumK tasks = $(( sumK * ALLOC_CPUS_PER_TASK )) allocated CPUs (cap $CPU_CAP), ${sumMem}G requested (cap ${MEM_CAP_G}G)"
(( sumK * ALLOC_CPUS_PER_TASK <= CPU_CAP && sumMem <= MEM_CAP_G )) || { echo "FATAL: batch alone exceeds the per-user cap" >&2; exit 65; }
read -r ucpu umem < <(squeue -u fb31 -h -t R -o "%C %m" | awk '{c+=$1; m=$2; f=1; if (m ~ /M$/) f=1/1024; if (m ~ /T$/) f=1024; sub(/[MGT]$/,"",m); t+=m*f} END {printf "%d %d\n", c, t}')
queued=$(squeue -u fb31 -h -r | wc -l)
echo "# fb31 now on NOTS: running ${ucpu} CPUs, ${umem}G; ${queued} jobs/array tasks queued or running (submit cap $SUBMIT_CAP)"
(( queued + total <= SUBMIT_CAP )) || { echo "FATAL: $queued queued + $total tasks would exceed MaxSubmitPU $SUBMIT_CAP (submit the classes separately with --classes)" >&2; exit 65; }

note=-
if [[ "$hold" == owner_ok_after_b1 && "$batch" != 1 ]]; then
  if (( ownerok )); then note=owner_ok_asi_full; echo "# HOLD $method after batch 1: lifted by --owner-ok-asi-full (recorded in submissions.tsv)"
  else echo "# HOLD: $method batches after 1 need the owner's OK (--owner-ok-asi-full); --go refuses without it"; fi
fi
if [[ $mode == go ]]; then
  if [[ "$hold" == owner_ok_after_b1 && "$batch" != 1 ]] && (( ! ownerok )); then
    echo "REFUSED: $method batch $batch is on hold until the owner OKs the full grid (--owner-ok-asi-full)" >&2; exit 68; fi
  (( over == 0 )) || { echo "REFUSED: S$suite $method billed CPU-h $used >= budget $budget (hard stop)" >&2; exit 69; }
  live=$(squeue -u fb31 -h -o %j | grep -Ec "^s${suite}bm_${method}_b${batch}m?_" || true)
  (( live == 0 )) || { echo "REFUSED: $live jobs of S$suite $method batch $batch (or its oom-pass) still queued/running (re-run --go only after they end; ok reps are skipped)" >&2; exit 67; }
fi
for c in "${cmds[@]}"; do
  case $mode in
    print) echo "$c";;
    test)  echo "\$ ${c/sbatch --parsable/sbatch --test-only}"; eval "${c/sbatch --parsable/sbatch --test-only}" 2>&1 || true;;
    go)    mkdir -p "$LOGDIR" "$(dirname "$SUBLOG")" /scratch/fb31/SMC-BVS/tmp/S1S2
           jid=$(eval "$c"); echo "SUBMITTED $jid  $c"
           printf '%s\t%s\t%s\t%s\t%s\t%s\n' "$(date -u +%FT%TZ)" "S${suite}bm.${method}.${bsfx}" "$jid" "$mhash" "$c" "$note" >> "$SUBLOG";;
  esac
done
[[ $mode == print ]] && echo "# (printed only; nothing submitted. --test-only validates, --go submits)"
exit 0
