#!/usr/bin/env bash
# submit_batches.sh -- run on NOTS from the deploy tree. Builds the per-class job arrays of ONE S1 SMC-BVS batch and
# PRINTS the sbatch commands. It submits ONLY with --go (the owner's GO, relayed by the manager as "SUBMIT BATCH k").
#   submit_batches.sh --batch K --reps LO-HI [--classes P5000N1000,P5000N500,P500N1000,P500N500] [--max-conc 600]
#                     [--dependency afterany:JOBID[:JOBID...]] [--test-only | --go]
# A batch = reps LO..HI of every setting in the chosen classes (all 16 settings, reps 1-25 -> 400 tasks). One array per
# setting class, because Slurm gives every task of an array the same --mem/--time:
#   class        settings      n     p     default mem / time / partition   (override: MEM_<C>, TIME_<C>, PART_<C>)
#   P5000N1000   S1_13-S1_16   1000  5000  8G / 12:00:00 / commons
#   P5000N500    S1_05-S1_08   500   5000  8G / 12:00:00 / commons   (S1_07 smoke still running: provisional)
#   P500N1000    S1_09-S1_12   1000  500   2G / 02:00:00 / commons
#   P500N500     S1_01-S1_04   500   500   2G / 02:00:00 / commons
# Sizing (Owls smoke, 1 core, load ~50): S1_03 299 s, S1_11 215 s, S1_15 11,215 s (tier 0, N 5000, peak 1.80 GB),
# S1_07 > 3.1 h. time = 12 h ~ 3.85x the Owls S1_15 time (manager: ~3x observed, within the 24 h commons max), covering
# a tier-1 escalation (N x4) and the harness diagnostics. mem: p=5000 = the engine's own allocation (mem_gb = 8; its
# preflight bound is 6.68 GB at tier 0, 6.76 GB at tier 1, dominated by the 500p-model cache); p=500 bound 0.34-0.62 GB.
# Arrays are submitted longest class first, so the long p=5000 tasks start first and the short ones backfill.
# Concurrency: the %K throttles of the arrays sum to <= --max-conc (<= 600), split in proportion to the task counts.
# 600 concurrent tasks = 1,200 allocated CPUs (2 per task, see ALLOC_CPUS_PER_TASK), within the 1,536 cap.
# Caps (QOS nots_commons, sacctmgr 2026-11-25): per user cpu=1536, mem=2304G -- SHARED with every other fb31 job on
# NOTS (e.g. BQTF arrays). The script reads fb31's running usage and warns when the batch would not fit beside it;
# Slurm itself never exceeds the cap (excess tasks wait as QOSMaxCpuPerUserLimit / QOSMaxMemoryPerUser).
# --test-only runs `sbatch --test-only` per array (validation only; nothing is queued).
# Re-runnable: --go refuses while any s1smc_b<K>_* job is still in the queue; after the batch has ended, --go again
# resubmits it and every task whose record is already ok exits at once (re-runs failures only).
set -euo pipefail
ENG=/home/fb31/SMC-BVS/_local/engineering
DEPLOY=${S1S2_DEPLOY:-$ENG/S1S2/deploy}
SBATCH_FILE=$DEPLOY/S1S2/slurm/s1_smcbvs_array.sbatch
LOGDIR=/scratch/fb31/SMC-BVS/runs/S1S2/logs
SUBLOG=$ENG/S1S2/logs/submissions.tsv
CPU_CAP=1536; MEM_CAP_G=2304; CPUS_PER_TASK=1
ALLOC_CPUS_PER_TASK=2   # NOTS allocates whole cores (ThreadsPerCore=2): sbatch --test-only reports "using 2 processors"
                        # for --cpus-per-task=1, and the 2 CPUs count against the per-user cpu cap

batch=""; reps=""; classes="P5000N1000,P5000N500,P500N1000,P500N500"; maxconc=600; dep=""; mode=print
while (($#)); do case "$1" in
  --batch) batch="$2"; shift 2;; --reps) reps="$2"; shift 2;; --classes) classes="$2"; shift 2;;
  --max-conc) maxconc="$2"; shift 2;; --dependency) dep="$2"; shift 2;;
  --test-only) mode=test; shift;; --go) mode=go; shift;;
  -h|--help) sed -n '2,27p' "$0"; exit 0;; *) echo "unknown arg $1" >&2; exit 64;; esac; done
[[ "$batch" =~ ^[0-9]+$ ]] || { echo "need --batch K" >&2; exit 64; }
[[ "$reps" =~ ^([0-9]+)-([0-9]+)$ ]] || { echo "need --reps LO-HI" >&2; exit 64; }
lo=${BASH_REMATCH[1]}; hi=${BASH_REMATCH[2]}
(( lo >= 1 && hi <= 100 && lo <= hi )) || { echo "reps must lie in 1-100" >&2; exit 64; }
(( maxconc >= 1 && maxconc <= 600 )) || { echo "--max-conc must be 1..600" >&2; exit 64; }

declare -A CELLS=( [P500N500]="1 2 3 4" [P5000N500]="5 6 7 8" [P500N1000]="9 10 11 12" [P5000N1000]="13 14 15 16" )
declare -A DMEM=( [P500N500]=2G [P500N1000]=2G [P5000N500]=8G [P5000N1000]=8G )
declare -A DTIME=( [P500N500]=02:00:00 [P500N1000]=02:00:00 [P5000N500]=12:00:00 [P5000N1000]=12:00:00 )
IFS=, read -ra CL <<< "$classes"
nrep=$(( hi - lo + 1 )); total=0
for c in "${CL[@]}"; do [[ -n "${CELLS[$c]:-}" ]] || { echo "unknown class $c" >&2; exit 64; }; total=$(( total + 4 * nrep )); done
(( total >= 400 && total <= 600 )) || echo "NOTE: batch has $total tasks (target 400-600)" >&2

secs() { local t=$1 d=0; [[ $t == *-* ]] && { d=${t%%-*}; t=${t#*-}; }; IFS=: read -r h m s <<< "$t"; echo $(( d*86400 + 10#$h*3600 + 10#$m*60 + 10#$s )); }

# manifest check of the deploy before anything is submitted
( cd "$DEPLOY" && sha256sum --quiet -c MANIFEST.sha256 ) || { echo "FATAL: deploy manifest check failed" >&2; exit 65; }
mhash=$(sha256sum "$DEPLOY/MANIFEST.sha256" | cut -c1-64)
echo "# deploy $DEPLOY  manifest_sha256=$mhash  ($(sed -n 's/^source: //p' "$DEPLOY/DEPLOY_INFO.txt"))"

sumK=0; sumMem=0; cmds=()
for c in "${CL[@]}"; do
  ranges=""; for cell in ${CELLS[$c]}; do ranges+="${ranges:+,}$(( (cell-1)*100 + lo ))-$(( (cell-1)*100 + hi ))"; done
  n=$(( 4 * nrep ))
  K=$(( total <= maxconc ? n : (n * maxconc) / total )); (( K >= 1 )) || K=1
  v="MEM_$c"; mem=${!v:-${DMEM[$c]}}; v="TIME_$c"; tl=${!v:-${DTIME[$c]}}; v="PART_$c"; part=${!v:-commons}
  memg=${mem%G}; sumK=$(( sumK + K )); sumMem=$(( sumMem + K * memg ))
  cmd=(sbatch --parsable --job-name="s1smc_b${batch}_${c}" --partition="$part" --cpus-per-task=$CPUS_PER_TASK --mem="$mem" --time="$tl"
       --array="${ranges}%${K}" --export="ALL,S1S2_WALL_SEC=$(secs "$tl")")
  [[ -n "$dep" ]] && cmd+=(--dependency="$dep")
  cmd+=("$SBATCH_FILE")
  cmds+=("$(printf '%q ' "${cmd[@]}")")
  echo "# class $c: settings ${CELLS[$c]// /,} reps $lo-$hi -> $n tasks, %$K concurrent, mem $mem, time $tl, $part"
done
echo "# batch $batch: $total tasks; peak concurrency $sumK tasks = $(( sumK * ALLOC_CPUS_PER_TASK )) allocated CPUs (cap $CPU_CAP), ${sumMem}G requested (cap ${MEM_CAP_G}G)"
(( sumK * ALLOC_CPUS_PER_TASK <= CPU_CAP && sumMem <= MEM_CAP_G )) || { echo "FATAL: batch alone exceeds the per-user cap" >&2; exit 65; }
read -r ucpu umem < <(squeue -u fb31 -h -t R -o "%C %m" | awk '{c+=$1; m=$2; f=1; if (m ~ /M$/) f=1/1024; if (m ~ /T$/) f=1024; sub(/[MGT]$/,"",m); t+=m*f} END {printf "%d %d\n", c, t}')
echo "# fb31 now running on NOTS: ${ucpu} CPUs, ${umem}G -> free under cap: $(( CPU_CAP - ucpu )) CPUs, $(( MEM_CAP_G - umem ))G"
(( ucpu + sumK * ALLOC_CPUS_PER_TASK <= CPU_CAP )) || echo "WARNING: only $(( CPU_CAP - ucpu )) CPUs (= $(( (CPU_CAP - ucpu) / ALLOC_CPUS_PER_TASK )) tasks) free under the cap; the rest wait (QOSMaxCpuPerUserLimit)" >&2
(( umem + sumMem <= MEM_CAP_G )) || echo "WARNING: only $(( MEM_CAP_G - umem ))G free under the mem cap; some tasks wait (QOSMaxMemoryPerUser)" >&2

for c in "${cmds[@]}"; do
  case $mode in
    print) echo "$c";;
    test)  echo "\$ ${c/sbatch --parsable/sbatch --test-only}"; eval "${c/sbatch --parsable/sbatch --test-only}" 2>&1 || true;;
    go)    live=$(squeue -u fb31 -h -o %j | grep -c "^s1smc_b${batch}_" || true)
           (( live == 0 )) || { echo "REFUSED: $live jobs of batch $batch still queued/running (re-run --go only after they end; ok tasks are skipped)" >&2; exit 67; }
           mkdir -p "$LOGDIR" "$(dirname "$SUBLOG")" /scratch/fb31/SMC-BVS/tmp/S1S2
           jid=$(eval "$c"); echo "SUBMITTED $jid  $c"
           printf '%s\t%s\t%s\t%s\t%s\n' "$(date -u +%FT%TZ)" "$batch" "$jid" "$mhash" "$c" >> "$SUBLOG";;
  esac
done
[[ $mode == print ]] && echo "# (printed only; nothing submitted. --test-only validates, --go submits)"
exit 0
