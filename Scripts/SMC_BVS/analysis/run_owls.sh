#!/usr/bin/env bash
# Parent's sole Owls funnel launches this script; this script never invokes ssh/scp or Slurm.
set -euo pipefail
umask 077
if [[ $(hostname -s) != owls* ]]; then echo 'Owls required' >&2; exit 64; fi
if [[ $(ps -o ni= -p $$ | tr -d ' ') != 19 ]]; then
  echo 'Launch with nice -n 19 bash run_owls.sh ...' >&2; exit 64
fi
if [[ $# -lt 3 ]]; then
  echo 'Usage: run_owls.sh verify JOB_ID SCORING_DIR | assess JOB_ID CONFIG_JSON' >&2; exit 64
fi
mode=$1
job_name=$2
input=$3
if [[ ! $job_name =~ ^[A-Za-z0-9_-]+$ ]]; then echo 'Unsafe job ID' >&2; exit 64; fi
base="$HOME/smcbvs_v3_deploy_20261022/D_analysis/pipeline"
source_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)
if [[ $source_dir != "$base"/* && $source_dir != "$base" ]]; then echo 'Source must be in owned pipeline folder' >&2; exit 64; fi
launch="$base/jobs/$job_name"
mkdir -p -- "$base/jobs"
mkdir -- "$launch"
exec >"$launch/launcher.log" 2>&1
date -u '+started_utc=%Y-%m-%dT%H:%M:%SZ'
printf 'pid=%s\nmode=%s\nsource=%s\ninput=%s\n' "$$" "$mode" "$source_dir" "$input"
printf '%q ' nice -n 19 bash "$source_dir/run_owls.sh" "$mode" "$job_name" "$input"
printf '\n'
trap 'rc=$?; printf "exit_status=%s\n" "$rc"; date -u "+finished_utc=%Y-%m-%dT%H:%M:%SZ"; exit "$rc"' EXIT
uptime
free -g
# Bash reads the existing system status; all actual analysis remains on Owls.
load=$(cut -d ' ' -f1 /proc/loadavg)
avail_kib=$(awk '/^MemAvailable:/ { print $2 }' /proc/meminfo)
if ! awk -v l="$load" -v a="$avail_kib" 'BEGIN { exit !(l <= 40 && a >= 31457280) }'; then
  echo 'Shared-machine gate failed; parent must wait at least 15 minutes before another batch.'; exit 75
fi
disk_kib=$(du -sk -- "$HOME/smcbvs_v3_deploy_20261022" | cut -f1)
printf 'deployment_disk_kib=%s\n' "$disk_kib"
if (( disk_kib > 16777216 )); then
  echo 'Deployment already exceeds 16GiB; leave headroom under the global 20GB cap.'; exit 75
fi
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
ulimit -v 4194304
ulimit -f 1048576
sha256sum -- "$source_dir"/*.py "$source_dir"/*.R "$source_dir"/*.sh >"$launch/source_sha256.txt"
uname -a
/usr/bin/python3 --version
/usr/bin/Rscript --version
if [[ $mode == verify ]]; then
  /usr/bin/python3 "$source_dir/verify_fixture.py" --work "$launch/validation" --benchmark-scoring "$input"
elif [[ $mode == assess ]]; then
  /usr/bin/python3 "$source_dir/run_pipeline.py" --config "$input"
else
  echo 'Unknown mode'; exit 64
fi
du -sk -- "$base"
