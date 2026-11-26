#!/usr/bin/env bash
# submit_s2_batches.sh -- run on NOTS from the deploy tree. S2 SMC-BVS (120 settings x 100 reps = 12,000 fits) in batches.
# Sibling of submit_batches.sh (S1), same conventions; it PRINTS the sbatch commands and submits ONLY with --go
# (S2 GO 2026-11-26 via the manager: commons, Cascade Lake, 8 h, hard stop 8,000 billed CPU-h).
#   submit_s2_batches.sh --batch K --reps LO-HI [--classes S2N50P1000,S2N100P1000] [--max-conc N]
#                        [--dependency afterany:JOBID[:JOBID...]] [--test-only | --go]
# A batch = reps LO..HI of every S2 setting in the chosen classes (120 settings x nrep; reps 1-5 -> 600 tasks). One
# array per class (one --mem/--time per array); task ids index slurm/tasks_S2_smcbvs.tsv, task_id = (cell-1)*100 + rep,
# data_seed = 5e8 + 1e6*2 + 1e3*cell + rep (harness/generate.R). The class cells are cross-checked against settings.tsv.
#   class        cells    n    p     s0   default mem / time / partition / constraint
#   S2N50P1000   1-60     50   1000  5    1G / 08:00:00 / commons / cascadelake
#   S2N100P1000  61-120   100  1000  10   1G / 08:00:00 / commons / cascadelake
#   (override: MEM_<C>, TIME_<C>, PART_<C>, CONSTRAINT_<C>; an empty CONSTRAINT_<C> unpins)
# Sizing: Owls smoke (load 50-120) S2_016 (n 50) 752 s at tier 1 (escalated, N 10,000), peak 0.26 GB; S2_076 (n 100)
# 40 s at tier 0, peak 0.21 GB; engine preflight 0.11 / 0.17 GB. NOTS runs the S1 fits 0.8-1.7x the Owls speed.
# mem 1G = 4x the observed peak (preflight 0.11 / 0.17 GB). time 08:00:00 both classes (HQ; covers the Gold slowdown).
# Cascade Lake only (HQ rule 2026-11-26): S2 never competes with S1 p=5000 (Sapphire Rapids) for nodes; it shares only
# the per-user commons QOS cap (1,536 CPUs = 768 two-CPU tasks), which s2_throttle.sh re-tunes live (ArrayTaskThrottle).
# Concurrency: the initial %K throttles sum to --max-conc (default 768 - S1 tasks running on commons, at least 1),
# split over the classes in proportion to their task counts; the throttle controller takes over within 10 min.
# Job names s2smc_b<K>_<class>; submissions.tsv batch field "S2.<K>" (never matches an S1 batch number).
# Re-runnable: --go refuses while any s2smc_b<K>_* job is queued (checked once, before the first sbatch); after the batch
# has ended, --go again resubmits it and every task whose record is already ok exits at once.
# Watch / pull / package / record with --suite 2 (check_batch.sh, watch_batch.sh, pull_to_owls.sh, package_for_desktop.sh,
# sacct_record.sh); unit S1S2_smcbvs_s2b<K>.
set -euo pipefail
ENG=/home/fb31/SMC-BVS/_local/engineering
DEPLOY=${S1S2_DEPLOY:-$ENG/S1S2/deploy}
SBATCH_FILE=$DEPLOY/S1S2/slurm/s1_smcbvs_array.sbatch
TASKS=$DEPLOY/S1S2/slurm/tasks_S2_smcbvs.tsv
SETTINGS=$DEPLOY/S1S2/specs/settings.tsv
LOGDIR=/scratch/fb31/SMC-BVS/runs/S1S2/logs
SUBLOG=$ENG/S1S2/logs/submissions.tsv
CPU_CAP=1536; TASK_CAP=768; MEM_CAP_G=2304; SUBMIT_CAP=5000; CPUS_PER_TASK=1; ALLOC_CPUS_PER_TASK=2

batch=""; reps=""; classes="S2N50P1000,S2N100P1000"; maxconc=""; dep=""; mode=print
while (($#)); do case "$1" in
  --batch) batch="$2"; shift 2;; --reps) reps="$2"; shift 2;; --classes) classes="$2"; shift 2;;
  --max-conc) maxconc="$2"; shift 2;; --dependency) dep="$2"; shift 2;;
  --test-only) mode=test; shift;; --go) mode=go; shift;;
  -h|--help) sed -n '2,24p' "$0"; exit 0;; *) echo "unknown arg $1" >&2; exit 64;; esac; done
[[ "$batch" =~ ^[0-9]+$ ]] || { echo "need --batch K" >&2; exit 64; }
[[ "$reps" =~ ^([0-9]+)-([0-9]+)$ ]] || { echo "need --reps LO-HI" >&2; exit 64; }
lo=${BASH_REMATCH[1]}; hi=${BASH_REMATCH[2]}
(( lo >= 1 && hi <= 100 && lo <= hi )) || { echo "reps must lie in 1-100" >&2; exit 64; }
[[ -z "$maxconc" ]] || (( maxconc >= 1 && maxconc <= TASK_CAP )) || { echo "--max-conc must be 1..$TASK_CAP" >&2; exit 64; }
[[ -f "$TASKS" && $(wc -l < "$TASKS") -eq 12001 ]] || { echo "FATAL: $TASKS missing or not 12,000 rows" >&2; exit 65; }

declare -A CELLS=( [S2N50P1000]="$(seq -s' ' 1 60)" [S2N100P1000]="$(seq -s' ' 61 120)" )
declare -A NVAL=( [S2N50P1000]=50 [S2N100P1000]=100 )
declare -A DMEM=( [S2N50P1000]=1G [S2N100P1000]=1G )
declare -A DTIME=( [S2N50P1000]=08:00:00 [S2N100P1000]=08:00:00 )
declare -A DCONS=( [S2N50P1000]=cascadelake [S2N100P1000]=cascadelake )
IFS=, read -ra CL <<< "$classes"
nrep=$(( hi - lo + 1 )); total=0
for c in "${CL[@]}"; do
  [[ -n "${CELLS[$c]:-}" ]] || { echo "unknown class $c" >&2; exit 64; }
  # cross-check: the class cells are exactly the suite-2 cells with this n and p = 1000
  want=$(awk -F'\t' -v n="${NVAL[$c]}" '$2 == 2 && $4 == n && $5 == 1000 { print $3 }' "$SETTINGS" | sort -n | paste -sd' ' -)
  [[ "$want" == "${CELLS[$c]}" ]] || { echo "FATAL: class $c cells do not match settings.tsv" >&2; exit 65; }
  total=$(( total + 60 * nrep ))
done

secs() { local t=$1 d=0; [[ $t == *-* ]] && { d=${t%%-*}; t=${t#*-}; }; IFS=: read -r h m s <<< "$t"; echo $(( d*86400 + 10#$h*3600 + 10#$m*60 + 10#$s )); }

( cd "$DEPLOY" && sha256sum --quiet -c MANIFEST.sha256 ) || { echo "FATAL: deploy manifest check failed" >&2; exit 65; }
mhash=$(sha256sum "$DEPLOY/MANIFEST.sha256" | cut -c1-64)
echo "# deploy $DEPLOY  manifest_sha256=$mhash  ($(sed -n 's/^source: //p' "$DEPLOY/DEPLOY_INFO.txt"))"
s1c=$(squeue -u fb31 -h -r -t R -o '%P %j' | awk '$1 == "commons" && $2 ~ /^s1smc_/' | wc -l)
if [[ -z "$maxconc" ]]; then maxconc=$(( TASK_CAP - s1c )); (( maxconc >= 1 )) || maxconc=1; fi
echo "# S1 tasks running on commons: $s1c -> S2 initial concurrency $maxconc (cap $TASK_CAP tasks; s2_throttle.sh re-tunes it)"

sumK=0; sumMem=0; cmds=()
for c in "${CL[@]}"; do
  ranges=""; for cell in ${CELLS[$c]}; do ranges+="${ranges:+,}$(( (cell-1)*100 + lo ))-$(( (cell-1)*100 + hi ))"; done
  n=$(( 60 * nrep ))
  K=$(( total <= maxconc ? n : (n * maxconc) / total )); (( K >= 1 )) || K=1
  v="MEM_$c"; mem=${!v:-${DMEM[$c]}}; v="TIME_$c"; tl=${!v:-${DTIME[$c]}}; v="PART_$c"; part=${!v:-commons}
  v="CONSTRAINT_$c"; cons=${!v-${DCONS[$c]}}
  memg=${mem%G}; sumK=$(( sumK + K )); sumMem=$(( sumMem + K * memg ))
  cmd=(sbatch --parsable --job-name="s2smc_b${batch}_${c}" --partition="$part" --cpus-per-task=$CPUS_PER_TASK --mem="$mem" --time="$tl"
       --array="${ranges}%${K}" --export="ALL,S1S2_WALL_SEC=$(secs "$tl"),S1S2_TASKS=$TASKS")
  [[ -n "$cons" ]] && cmd+=(--constraint="$cons")
  [[ -n "$dep" ]] && cmd+=(--dependency="$dep")
  cmd+=("$SBATCH_FILE")
  cmds+=("$(printf '%q ' "${cmd[@]}")")
  echo "# class $c: cells ${CELLS[$c]%% *}-${CELLS[$c]##* } reps $lo-$hi -> $n tasks, %$K concurrent, mem $mem, time $tl, $part${cons:+, constraint $cons}"
done
echo "# S2 batch $batch: $total tasks; peak concurrency $sumK tasks = $(( sumK * ALLOC_CPUS_PER_TASK )) allocated CPUs (cap $CPU_CAP), ${sumMem}G requested (cap ${MEM_CAP_G}G)"
(( sumK * ALLOC_CPUS_PER_TASK <= CPU_CAP && sumMem <= MEM_CAP_G )) || { echo "FATAL: batch alone exceeds the per-user cap" >&2; exit 65; }
read -r ucpu umem < <(squeue -u fb31 -h -t R -o "%C %m" | awk '{c+=$1; m=$2; f=1; if (m ~ /M$/) f=1/1024; if (m ~ /T$/) f=1024; sub(/[MGT]$/,"",m); t+=m*f} END {printf "%d %d\n", c, t}')
queued=$(squeue -u fb31 -h -r | wc -l)
echo "# fb31 now on NOTS: running ${ucpu} CPUs, ${umem}G; ${queued} jobs/array tasks queued or running (submit cap $SUBMIT_CAP)"
(( ucpu + sumK * ALLOC_CPUS_PER_TASK <= CPU_CAP )) || echo "WARNING: only $(( CPU_CAP - ucpu )) CPUs free under the cap; the rest wait (QOSMaxCpuPerUserLimit)" >&2
(( queued + total <= SUBMIT_CAP )) || { echo "FATAL: $queued queued + $total tasks would exceed MaxSubmitPU $SUBMIT_CAP" >&2; exit 65; }

if [[ $mode == go ]]; then
  live=$(squeue -u fb31 -h -o %j | grep -c "^s2smc_b${batch}_" || true)
  (( live == 0 )) || { echo "REFUSED: $live jobs of S2 batch $batch still queued/running (re-run --go only after they end; ok tasks are skipped)" >&2; exit 67; }
fi
for c in "${cmds[@]}"; do
  case $mode in
    print) echo "$c";;
    test)  echo "\$ ${c/sbatch --parsable/sbatch --test-only}"; eval "${c/sbatch --parsable/sbatch --test-only}" 2>&1 || true;;
    go)    mkdir -p "$LOGDIR" "$(dirname "$SUBLOG")" /scratch/fb31/SMC-BVS/tmp/S1S2
           jid=$(eval "$c"); echo "SUBMITTED $jid  $c"
           printf '%s\t%s\t%s\t%s\t%s\n' "$(date -u +%FT%TZ)" "S2.$batch" "$jid" "$mhash" "$c" >> "$SUBLOG";;
  esac
done
[[ $mode == print ]] && echo "# (printed only; nothing submitted. --test-only validates, --go submits)"
exit 0
