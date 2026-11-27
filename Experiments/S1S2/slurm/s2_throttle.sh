#!/usr/bin/env bash
# s2_throttle.sh -- run on NOTS (one call per controller run; the Owls timer s2_throttle_ctl.sh calls it over ssh).
# Shares the per-user commons QOS cap (1,536 CPUs = 768 two-CPU tasks) between S1 and S2 (HQ rule 2026-11-26):
# S1 p=5000 is the critical path; S2 must never take a commons slot a pending S1 p=5000 task could use.
#   s2_throttle.sh [--reserve R] [--bench-cap C] [--apply]   (without --apply: prints the decision, changes nothing)
# MANAGED arrays (2026-11-27): fb31's s2smc_* (S2 SMC-BVS, complete) AND the benchmark arrays s1bm_* / s2bm_*
# (submit_bench.sh, all methods, both suites), as ONE pool. C = --bench-cap (default 468 = 768 - 300): HARD ceiling on
# the pool's total, in both modes (HQ: <= 468 running benchmark tasks in total). Below, "S2" = the managed pool.
# Decision, from ONE squeue snapshot of fb31's own jobs:
#   q = S1 SMC-BVS tasks (job name s1smc_*; 2026-11-27: any class, before: p=5000 only, which is all that is left)
#       PENDING on commons blocked by OUR per-user QOS cap: reason QOSMaxCpuPerUserLimit counts 1 each (HQ rule); a
#       QOSMax*Mem*PerUser* reason (the 2,304G mem cap binds the same way) counts ceil(S1 task mem / u) each, u = the
#       smallest mem of a managed task (1G if none), so that enough managed memory is freed;
#   q > 0  -> LOWER: S2 total = min(S2 throttle, S2 running) - q   (frees the slots as S2 tasks end; S2 tasks are short)
#   q == 0 -> TRACK: S2 total = 768 - max(R, S1 tasks running on commons) - other fb31 tasks running on commons (BQTF)
#             (S1 p=5000 pending only on Resources/Priority, i.e. no Sapphire Rapids node free, or nothing pending).
#             R = --reserve: commons task slots always left to S1 (HQ 2026-11-26: 300, i.e. S2 = 768 - 300 - BQTF while
#             S1 runs <= 300 there; default 0).
# PRIORITY (owner 2026-11-27; queue order: S1 SMC tail > S1 cheap four > S1 asi > S2 cheap four > S2 asi). The S1 SMC
# tail is never managed (it yields nothing; the pool yields to it, above). Inside the pool, tiers by job name:
#   0 s2smc_* (S2 SMC-BVS, complete)   1 s1bm_<lasso_cv|scad|susie|bas_mc3>_*   2 s1bm_asi_*
#   3 s2bm_<lasso_cv|scad|susie|bas_mc3>_*   4 s2bm_asi_*
# The total B (net of the running tasks of pool arrays with nothing left to start) is split over the arrays that still
# have pending tasks so that the pool never exceeds it: each such array gets a floor of 1 (0 = unlimited), and the rest
# X = B - (number of such arrays) goes tier by tier, highest priority first, each tier taking at most its demand
# (running + pending - 1 per array). So a lower-priority array's throttle is lowered whenever a higher-priority array has
# pending tasks: the lower tiers get only what the higher tiers' running AND pending tasks leave (possibly just the floor
# of 1, below their running count: they start nothing until enough of their tasks end, and the slots freed go to the
# higher tier). Within a tier: if its share X_t >= its running tasks (r_a - 1 each, net of the floor), each array keeps
# its running count plus a share of the free slots in proportion to its pending tasks; else each array gets X_t in
# proportion to its running tasks. A batch submitted later into a higher tier takes the lower tiers' slots as their
# tasks end (submit_bench.sh also starts a lower tier small when higher tiers have pending tasks).
# It changes ONLY ArrayTaskThrottle of fb31's arrays named s2smc_* / s1bm_* / s2bm_* (scontrol update), never an S1
# SMC-BVS or any other job. Output: one "THROTTLE ..." line (+ "SET ..." lines with --apply) and the billed CPU-h so far
# (sacct CPUTimeRAW, running tasks included) of the S1 and S2 jobs in submissions.tsv (hard stops 12,000 / 8,000).
set -uo pipefail
ENG=/home/fb31/SMC-BVS/_local/engineering
SUBLOG=$ENG/S1S2/logs/submissions.tsv
TASK_CAP=768; apply=0; reserve=0; bcap=468
CONF=$(cd "$(dirname "$0")" && pwd)/bench_budget.tsv
while (($#)); do case "$1" in --apply) apply=1; shift;; --reserve) reserve="$2"; shift 2;; --bench-cap) bcap="$2"; shift 2;;
  *) echo "unknown arg $1" >&2; exit 64;; esac; done
[[ "$bcap" =~ ^[0-9]+$ ]] && (( bcap >= 1 && bcap <= TASK_CAP )) || { echo "--bench-cap must be 1..$TASK_CAP" >&2; exit 64; }
[[ "$reserve" =~ ^[0-9]+$ ]] && (( reserve < TASK_CAP )) || { echo "--reserve must be 0..767" >&2; exit 64; }
snap=$(squeue -u fb31 -h -r -o '%u|%F|%j|%T|%P|%r|%m') || { echo "THROTTLE $(date -u +%FT%TZ) ERROR squeue failed"; exit 1; }
# current throttle of each S2 array with pending tasks (squeue truncates the "<id>_[...%K]" string; scontrol does not)
masters=$(squeue -u fb31 -h -t PD -o '%u|%F|%j' | sort -u | awk -F'|' '$1 == "fb31" && $3 ~ /^(s2smc_|s[12]bm_)/' | while IFS='|' read -r u f j; do
  k=$(scontrol show job "$f" 2>/dev/null | grep -m1 -o 'ArrayTaskThrottle=[0-9]*' | cut -d= -f2); echo "$u|$f|$j|${k:-0}"; done) || { echo "THROTTLE $(date -u +%FT%TZ) ERROR squeue failed"; exit 1; }
cpus=$(squeue -u fb31 -h -t R -o '%C' | awk '{ c += $1 } END { print c + 0 }')
# per S2 array: running, pending, current throttle (0 = none set)
plan=$(awk -F'|' -v cap="$TASK_CAP" -v res="$reserve" -v bcap="$bcap" -v OFS=' ' '
  function gb(m,  f) { f = (m ~ /T$/) ? 1024 : (m ~ /M$/) ? 1 / 1024 : 1; sub(/[MGT]$/, "", m); return m * f }
  function tier(j) { return j ~ /^s1bm_asi_/ ? 2 : j ~ /^s1bm_/ ? 1 : j ~ /^s2bm_asi_/ ? 4 : j ~ /^s2bm_/ ? 3 : 0 }
  FNR == NR { if ($1 == "fb31" && $3 ~ /^(s2smc_|s[12]bm_)/ && $4 + 0 > 0) thr[$2] = $4 + 0; next }
  $1 != "fb31" { next }
  $3 ~ /^s1smc_/ { if ($4 == "RUNNING") { if ($5 == "commons") s1c++; else if ($5 == "long") s1l++ }
                   if ($4 == "PENDING" && $5 == "commons") { if ($6 ~ /^QOSMaxCpuPerUser/) { q++; qc++ }
                     else if ($6 ~ /^QOSMax(Mem|Memory).*PerUser/) { s1m[++nm1] = gb($7); qm++ }
                     else oth[$6]++ }
                   if ($4 == "PENDING" && $3 ~ /_P5000/ && $5 == "long") lpd++
                   next }
  $3 ~ /^(s2smc_|s[12]bm_)/ { name[$2] = $3; mg = gb($7); if (mg > 0 && (um == 0 || mg < um)) um = mg
                   if ($4 == "RUNNING") { r[$2]++; s2r++ } else if ($4 == "PENDING") { p[$2]++; s2p++ }; next }
  $4 == "RUNNING" && $5 == "commons" { oc++ }
  END {
    o = ""; for (k in oth) o = o (o == "" ? "" : ",") k ":" oth[k]
    if (um <= 0) um = 1
    for (i = 1; i <= nm1; i++) { c = s1m[i] / um; ci = int(c); if (ci < c) ci++; if (ci < 1) ci = 1; q += ci }
    T = 0; busy = 0; W = 0; na = 0
    for (a in name) { if (p[a] > 0) { na++; T += (a in thr) ? thr[a] : p[a] + r[a]; W += p[a] + r[a] } else busy += r[a] }
    T += busy
    if (q > 0) { mode = "LOWER"; tgt = (T < s2r ? T : s2r) - q } else { mode = "TRACK"; tgt = cap - (s1c > res ? s1c : res) - oc }
    if (tgt > bcap) tgt = bcap
    printf "S %d %d %d %d %d %d %d %s %d %d %d %d %s %d\n", oc + 0, s1c, s1l, q + 0, qc + 0, qm + 0, lpd + 0, (o == "" ? "-" : o), s2r + 0, s2p + 0, T, tgt, mode, busy
    # split of B over the arrays with pending tasks: every such array keeps a floor of 1 (0 would mean unlimited); the
    # rest X = B - (number of such arrays) goes tier by tier in priority order, each tier taking at most its demand
    # (running + pending - 1 per array), so a lower tier gets only what the running AND pending tasks of higher tiers leave
    B = tgt - busy; X = B - na; if (X < 0) X = 0
    for (t = 0; t <= 4; t++) {
      nt = 0; D = 0; Rt = 0; Pt = 0
      for (a in name) if (p[a] > 0 && tier(name[a]) == t) { nt++; D += r[a] + p[a] - 1; Rt += (r[a] > 1 ? r[a] - 1 : 0); Pt += p[a] }
      if (!nt) continue
      Xt = (X < D) ? X : D; X -= Xt
      # within a tier (the former rule): keep the running tasks and share the free slots in proportion to the pending
      # tasks; if Xt is below the running tasks, each array gets Xt in proportion to its running tasks
      free = Xt - Rt; acc = 0; n = 0
      for (a in name) if (p[a] > 0 && tier(name[a]) == t) { n++; ra = (r[a] > 1 ? r[a] - 1 : 0)
        if (free >= 0) { d = (n == nt) ? free - acc : int(free * p[a] / Pt); acc += d; e = ra + d }
        else { e = (n == nt) ? Xt - acc : (Rt > 0 ? int(Xt * ra / Rt) : 0); acc += e }
        printf "A %s %s %d %d %d %d %d\n", a, name[a], r[a], p[a], (a in thr) ? thr[a] : -1, 1 + e, t } } }' <(echo "$masters") <(echo "$snap"))
read -r _ oc s1c s1l q qc qm lpd oth s2r s2p T tgt mode busy <<< "$(grep '^S ' <<< "$plan")"
budget=""; hold=" "
if [[ -s "$SUBLOG" ]]; then
  j1=$(awk -F'\t' '$2 !~ /^S/ { print $3 }' "$SUBLOG" | sort -u | paste -sd, -); j2=$(awk -F'\t' '$2 ~ /^S2\./ { print $3 }' "$SUBLOG" | sort -u | paste -sd, -)
  h1=$( [[ -n "$j1" ]] && sacct -j "$j1" -X -n -P -o CPUTimeRAW 2>/dev/null | awk '{ s += $1 } END { printf "%.0f", s / 3600 }' || echo 0)
  h2=$( [[ -n "$j2" ]] && sacct -j "$j2" -X -n -P -o CPUTimeRAW 2>/dev/null | awk '{ s += $1 } END { printf "%.0f", s / 3600 }' || echo 0)
  budget=" billed_cpuh S1=${h1:-0}/12000 S2=${h2:-0}/8000"
  (( ${h1:-0} > 11000 )) && budget+=" WARN_S1_BUDGET"; (( ${h2:-0} > 7300 )) && budget+=" WARN_S2_BUDGET"
  # benchmarks: billed CPU-h per (suite, method) vs bench_budget.tsv; at/over budget the method's arrays are held at 1
  # (check_batch.sh STOPs and the watcher cancels their pending tasks; this only limits the damage until then)
  if [[ -f "$CONF" ]]; then
    while IFS=$'\t' read -r su me bud; do
      jb=$(awk -F'\t' -v k="S${su}bm.${me}." 'index($2, k) == 1 { print $3 }' "$SUBLOG" | sort -u | paste -sd, -)
      [[ -n "$jb" ]] || continue
      hb=$(sacct -j "$jb" -X -n -P -o CPUTimeRAW 2>/dev/null | awk '{ s += $1 } END { printf "%.1f", s / 3600 }')
      budget+=" S${su}bm.${me}=${hb:-0}/${bud}"
      if awk -v u="${hb:-0}" -v b="$bud" 'BEGIN { exit !(u >= b) }'; then budget+="_OVER_BUDGET_HOLD"; hold+="s${su}bm_${me}_ "
      elif awk -v u="${hb:-0}" -v b="$bud" 'BEGIN { exit !(u >= 0.9 * b) }'; then budget+="_WARN"; fi
    done < <(awk -F'\t' 'NR > 1 { print $1 "\t" $2 "\t" $4 }' "$CONF")
  fi
fi
arrays=$(grep '^A ' <<< "$plan" | awk '{ printf "%s%s:%s(t%d,r%d,pd%d)%s->%s", (NR > 1 ? " " : ""), $2, $3, $8, $4, $5, $6, $7 }')
echo "THROTTLE $(date -u +%FT%TZ) mode=$mode reserve=$reserve bench_cap=$bcap s1_commons_run=$s1c other_commons_run=$oc s1_long_run=$s1l s1p5k_commons_pd_cpucap=$qc s1p5k_commons_pd_memcap=$qm lower_by=$q s1p5k_commons_pd_other=$oth s1p5k_long_pd=$lpd s2_run=$s2r s2_pd=$s2p s2_throttle_now=$T s2_target=$tgt fb31_cpus_running=$cpus apply=$apply${budget} arrays=[${arrays:-none}]"
(( apply )) || exit 0
while read -r _ a nm r p cur k _; do
  [[ ( "$nm" == s2smc_* || "$nm" == s[12]bm_* ) && "$a" =~ ^[0-9]+$ && "$k" =~ ^[0-9]+$ ]] || continue
  for hp in $hold; do [[ "$nm" == "$hp"* ]] && k=1; done
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
