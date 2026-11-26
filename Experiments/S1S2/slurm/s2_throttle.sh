#!/usr/bin/env bash
# s2_throttle.sh -- run on NOTS (one call per controller run; the Owls timer s2_throttle_ctl.sh calls it over ssh).
# Shares the per-user commons QOS cap (1,536 CPUs = 768 two-CPU tasks) between S1 and S2 (HQ rule 2026-11-26):
# S1 p=5000 is the critical path; S2 must never take a commons slot a pending S1 p=5000 task could use.
#   s2_throttle.sh [--reserve R] [--apply]   (without --apply: prints the decision, changes nothing)
# Decision, from ONE squeue snapshot of fb31's own jobs:
#   q = S1 p=5000 tasks (job name s1smc_*_P5000*) PENDING on commons blocked by OUR per-user QOS cap: reason
#       QOSMaxCpuPerUserLimit counts 1 each (HQ rule); a QOSMax*Mem*PerUser* reason (the 2,304G mem cap binds the same
#       way) counts ceil(S1 task mem / 1G S2 task mem) each, i.e. 8 per 8G S1 task, so that enough S2 memory is freed;
#   q > 0  -> LOWER: S2 total = min(S2 throttle, S2 running) - q   (frees the slots as S2 tasks end; S2 tasks are short)
#   q == 0 -> TRACK: S2 total = 768 - max(R, S1 tasks running on commons) - other fb31 tasks running on commons (BQTF)
#             (S1 p=5000 pending only on Resources/Priority, i.e. no Sapphire Rapids node free, or nothing pending).
#             R = --reserve: commons task slots always left to S1 (HQ 2026-11-26: 300, i.e. S2 = 768 - 300 - BQTF while
#             S1 runs <= 300 there; default 0).
# The total B (net of the running tasks of S2 arrays with nothing left to start) is split over the S2 arrays that still
# have pending tasks so that running S2 never exceeds it: if B >= their running tasks R, each array keeps its running
# count plus a share of the B - R free slots in proportion to its pending tasks; if B < R, each array gets B * r_a / R
# (below its running count: it starts nothing until enough of its tasks end). Each throttle >= 1 (0 = unlimited). It changes ONLY ArrayTaskThrottle of fb31's arrays named s2smc_* (scontrol update), never an S1 or any
# other job. Output: one "THROTTLE ..." line (+ "SET ..." lines with --apply) and the billed CPU-h so far
# (sacct CPUTimeRAW, running tasks included) of the S1 and S2 jobs in submissions.tsv (hard stops 12,000 / 8,000).
set -uo pipefail
ENG=/home/fb31/SMC-BVS/_local/engineering
SUBLOG=$ENG/S1S2/logs/submissions.tsv
TASK_CAP=768; apply=0; reserve=0
while (($#)); do case "$1" in --apply) apply=1; shift;; --reserve) reserve="$2"; shift 2;; *) echo "unknown arg $1" >&2; exit 64;; esac; done
[[ "$reserve" =~ ^[0-9]+$ ]] && (( reserve < TASK_CAP )) || { echo "--reserve must be 0..767" >&2; exit 64; }
snap=$(squeue -u fb31 -h -r -o '%u|%F|%j|%T|%P|%r|%m') || { echo "THROTTLE $(date -u +%FT%TZ) ERROR squeue failed"; exit 1; }
# current throttle of each S2 array with pending tasks (squeue truncates the "<id>_[...%K]" string; scontrol does not)
masters=$(squeue -u fb31 -h -t PD -o '%u|%F|%j' | sort -u | awk -F'|' '$1 == "fb31" && $3 ~ /^s2smc_/' | while IFS='|' read -r u f j; do
  k=$(scontrol show job "$f" 2>/dev/null | grep -m1 -o 'ArrayTaskThrottle=[0-9]*' | cut -d= -f2); echo "$u|$f|$j|${k:-0}"; done) || { echo "THROTTLE $(date -u +%FT%TZ) ERROR squeue failed"; exit 1; }
cpus=$(squeue -u fb31 -h -t R -o '%C' | awk '{ c += $1 } END { print c + 0 }')
# per S2 array: running, pending, current throttle (0 = none set)
plan=$(awk -F'|' -v cap="$TASK_CAP" -v res="$reserve" -v OFS=' ' '
  FNR == NR { if ($1 == "fb31" && $3 ~ /^s2smc_/ && $4 + 0 > 0) thr[$2] = $4 + 0; next }
  $1 != "fb31" { next }
  $3 ~ /^s1smc_/ { if ($4 == "RUNNING") { if ($5 == "commons") s1c++; else if ($5 == "long") s1l++ }
                   if ($4 == "PENDING" && $3 ~ /_P5000/ && $5 == "commons") { if ($6 ~ /^QOSMaxCpuPerUser/) { q++; qc++ }
                     else if ($6 ~ /^QOSMax(Mem|Memory).*PerUser/) { m = $7; f = (m ~ /T$/) ? 1024 : (m ~ /M$/) ? 1 / 1024 : 1; sub(/[MGT]$/, "", m)
                       m = m * f; c = int(m); if (c < m) c++; if (c < 1) c = 1; q += c; qm++ }
                     else oth[$6]++ }
                   if ($4 == "PENDING" && $3 ~ /_P5000/ && $5 == "long") lpd++
                   next }
  $3 ~ /^s2smc_/ { name[$2] = $3; if ($4 == "RUNNING") { r[$2]++; s2r++ } else if ($4 == "PENDING") { p[$2]++; s2p++ }; next }
  $4 == "RUNNING" && $5 == "commons" { oc++ }
  END {
    o = ""; for (k in oth) o = o (o == "" ? "" : ",") k ":" oth[k]
    T = 0; busy = 0; W = 0; na = 0
    for (a in name) { if (p[a] > 0) { na++; T += (a in thr) ? thr[a] : p[a] + r[a]; W += p[a] + r[a] } else busy += r[a] }
    T += busy
    if (q > 0) { mode = "LOWER"; tgt = (T < s2r ? T : s2r) - q } else { mode = "TRACK"; tgt = cap - (s1c > res ? s1c : res) - oc }
    printf "S %d %d %d %d %d %d %d %s %d %d %d %d %s %d\n", oc + 0, s1c, s1l, q + 0, qc + 0, qm + 0, lpd + 0, (o == "" ? "-" : o), s2r + 0, s2p + 0, T, tgt, mode, busy
    B = tgt - busy; R = 0; P = 0; for (a in name) if (p[a] > 0) { R += r[a]; P += p[a] }
    free = B - R; acc = 0; n = 0
    for (a in name) if (p[a] > 0) { n++
      if (free >= 0) { d = (n == na) ? free - acc : int(free * p[a] / P); acc += d; k = r[a] + d }
      else { k = (n == na) ? B - acc : (R > 0 ? int(B * r[a] / R) : 0); acc += k }
      if (k < 1) k = 1
      printf "A %s %s %d %d %d %d\n", a, name[a], r[a], p[a], (a in thr) ? thr[a] : -1, k } }' <(echo "$masters") <(echo "$snap"))
read -r _ oc s1c s1l q qc qm lpd oth s2r s2p T tgt mode busy <<< "$(grep '^S ' <<< "$plan")"
budget=""
if [[ -s "$SUBLOG" ]]; then
  j1=$(awk -F'\t' '$2 !~ /^S2\./ { print $3 }' "$SUBLOG" | sort -u | paste -sd, -); j2=$(awk -F'\t' '$2 ~ /^S2\./ { print $3 }' "$SUBLOG" | sort -u | paste -sd, -)
  h1=$( [[ -n "$j1" ]] && sacct -j "$j1" -X -n -P -o CPUTimeRAW 2>/dev/null | awk '{ s += $1 } END { printf "%.0f", s / 3600 }' || echo 0)
  h2=$( [[ -n "$j2" ]] && sacct -j "$j2" -X -n -P -o CPUTimeRAW 2>/dev/null | awk '{ s += $1 } END { printf "%.0f", s / 3600 }' || echo 0)
  budget=" billed_cpuh S1=${h1:-0}/12000 S2=${h2:-0}/8000"
  (( ${h1:-0} > 11000 )) && budget+=" WARN_S1_BUDGET"; (( ${h2:-0} > 7300 )) && budget+=" WARN_S2_BUDGET"
fi
arrays=$(grep '^A ' <<< "$plan" | awk '{ printf "%s%s:%s(r%d,pd%d)%s->%s", (NR > 1 ? " " : ""), $2, $3, $4, $5, $6, $7 }')
echo "THROTTLE $(date -u +%FT%TZ) mode=$mode reserve=$reserve s1_commons_run=$s1c other_commons_run=$oc s1_long_run=$s1l s1p5k_commons_pd_cpucap=$qc s1p5k_commons_pd_memcap=$qm lower_by=$q s1p5k_commons_pd_other=$oth s1p5k_long_pd=$lpd s2_run=$s2r s2_pd=$s2p s2_throttle_now=$T s2_target=$tgt fb31_cpus_running=$cpus apply=$apply${budget} arrays=[${arrays:-none}]"
(( apply )) || exit 0
while read -r _ a nm r p cur k; do
  [[ "$nm" == s2smc_* && "$a" =~ ^[0-9]+$ && "$k" =~ ^[0-9]+$ ]] || continue
  (( cur == k )) && continue
  # re-check ownership and name of the array right before touching it
  [[ $(squeue -j "$a" -h -o '%u %j' | sort -u) == "fb31 $nm" ]] || { echo "SKIP $a: owner/name check failed"; continue; }
  # scontrol exits non-zero when some tasks of the array have finished ("Job has already finished") although the
  # throttle is applied to the rest, so the result is judged by reading the throttle back
  scontrol update JobId="$a" ArrayTaskThrottle="$k" > /dev/null 2>&1
  now=$(scontrol show job "$a" 2>/dev/null | grep -m1 -o 'ArrayTaskThrottle=[0-9]*' | cut -d= -f2)
  [[ "$now" == "$k" ]] && echo "SET $a $nm ArrayTaskThrottle $cur -> $k" || echo "SET_FAILED $a $nm $cur -> $k (reads ${now:-?})"
done < <(grep '^A ' <<< "$plan")
exit 0
