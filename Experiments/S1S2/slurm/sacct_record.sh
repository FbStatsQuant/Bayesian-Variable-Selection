#!/usr/bin/env bash
# sacct_record.sh -- run on NOTS (read-only Slurm queries). Partition record of one batch, written at the batch's DONE:
#   sacct_record.sh [--suite 1|2] --batch K [--jobs JOBID,...] [--tag TAG]
#   -> _local/engineering/S1S2/logs/sacct_<TAG>.tsv  (TAG default b<K> for S1, s2b<K> for S2); prints
#      "SACCT_RECORD <path> <sha256> <rows>" (watch_batch.sh copies the file to Owls and checks that sha256).
# One row per array task (tasks moved to long by scontrol keep their ArrayJobId and get their own JobIDRaw):
#   JobID (JobIDRaw, the id Slurm accounts under)  task (<ArrayJobId>_<TaskId>)  JobName  Partition  NodeList
#   Elapsed  ElapsedRaw  State  ExitCode  AllocCPUS  CPUTimeRAW (billed CPU-s)  MaxRSS (of the .batch step)
#   Features (node features, sinfo)  CPU_model (from the features: cascadelake = Intel Xeon Gold 6230, sapphirerapids =
#   Intel Xeon Platinum 8468, as recorded by lscpu in every task's .out on NOTS; anything else "unknown")
# --jobs defaults to the array ids logged for the batch in _local/engineering/S1S2/logs/submissions.tsv.
set -euo pipefail
ENG=/home/fb31/SMC-BVS/_local/engineering
SUBLOG=$ENG/S1S2/logs/submissions.tsv
suite=1; batch=""; jobs=""; tag=""
while (($#)); do case "$1" in --suite) suite="$2"; shift 2;; --batch) batch="$2"; shift 2;; --jobs) jobs="$2"; shift 2;;
  --tag) tag="$2"; shift 2;; *) echo "unknown arg $1" >&2; exit 64;; esac; done
[[ "$batch" =~ ^[0-9]+$ && ( "$suite" == 1 || "$suite" == 2 ) ]] || { echo "usage: [--suite 1|2] --batch K" >&2; exit 64; }
[[ $suite == 1 ]] && bkey=$batch || bkey=S2.$batch
[[ $suite == 1 ]] && tag=${tag:-b$batch} || tag=${tag:-s2b$batch}
[[ "$tag" =~ ^[A-Za-z0-9_]+$ ]] || { echo "bad --tag" >&2; exit 64; }
[[ -z "$jobs" ]] && jobs=$(awk -F'\t' -v b="$bkey" '$2 == b { print $3 }' "$SUBLOG" | paste -sd, -)
[[ "$jobs" =~ ^[0-9]+(,[0-9]+)*$ ]] || { echo "no job ids for batch $bkey" >&2; exit 65; }
out=$ENG/S1S2/logs/sacct_${tag}.tsv
tmp=$(mktemp -d /scratch/fb31/SMC-BVS/tmp/S1S2/sacctrec.XXXXXX); trap 'rm -rf "$tmp"' EXIT
sinfo -N -h -o '%N|%f' | sort -u > "$tmp/feat"
sacct -j "$jobs" -n -P -o JobIDRaw,JobID,JobName,Partition,NodeList,Elapsed,ElapsedRaw,State,ExitCode,AllocCPUS,CPUTimeRAW,MaxRSS > "$tmp/sa"
awk -F'|' -v OFS='\t' '
  FNR == NR { feat[$1] = $2; next }
  $2 ~ /\.batch$/ { id = $2; sub(/\.batch$/, "", id); rss[id] = $12; next }
  $2 ~ /\./ { next }
  { n++; row[n] = $0; key[n] = $2 }
  END {
    print "JobID", "task", "JobName", "Partition", "NodeList", "Elapsed", "ElapsedRaw", "State", "ExitCode", "AllocCPUS", "CPUTimeRAW", "MaxRSS", "Features", "CPU_model"
    for (i = 1; i <= n; i++) { split(row[i], f, "|"); st = f[8]; sub(/ .*/, "", st)
      fe = (f[5] in feat) ? feat[f[5]] : ""; cpu = "unknown"
      if (fe ~ /cascadelake/) cpu = "Intel Xeon Gold 6230"; else if (fe ~ /sapphirerapids/) cpu = "Intel Xeon Platinum 8468"
      print f[1], f[2], f[3], f[4], f[5], f[6], f[7], st, f[9], f[10], f[11], (key[i] in rss) ? rss[key[i]] : "", fe, cpu } }' \
  "$tmp/feat" "$tmp/sa" > "$tmp/out"
mv "$tmp/out" "$out"
echo "SACCT_RECORD $out $(sha256sum "$out" | cut -c1-64) $(( $(wc -l < "$out") - 1 ))"
