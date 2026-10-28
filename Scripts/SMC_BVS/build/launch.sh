#!/usr/bin/env bash
# Owls-only persistent launch. Run through the A root's single SSH connection.
# All code/output stays in the A-owned directory. One job uses one numerical core.
set -euo pipefail
SNAPSHOT=$(realpath "${1:?snapshot}"); RUN=${2:?run name}; ACTION=${3:?action}; shift 3
A_ROOT=$(realpath /home/fb31/smcbvs_v3_deploy_20261022/A_build)
case "$SNAPSHOT/" in "$A_ROOT/"*) ;; *) echo 'Snapshot outside A ownership' >&2; exit 2;; esac
[[ "$RUN" =~ ^[a-zA-Z0-9_-]+$ ]] || exit 2
OUT=$(realpath -m "$A_ROOT/runs/$RUN")
case "$OUT/" in "$A_ROOT/"*) ;; *) echo 'Output outside A ownership' >&2; exit 2;; esac
if [[ "$ACTION" == smoke ]]; then
  [[ $# -ge 7 ]] || { echo 'Smoke must explicitly declare memory and hours' >&2; exit 2; }
  for path in "$2" "$3"; do
    [[ "$path" == /* ]] || { echo 'Smoke paths must be absolute' >&2; exit 2; }
    resolved=$(realpath -m "$path")
    case "$resolved/" in "$A_ROOT/"*) ;; *) echo 'Smoke path outside A ownership' >&2; exit 2;; esac
  done
  [[ "$6" == 2 ]] || { echo 'A smoke allocation must be 2 GiB' >&2; exit 2; }
fi
if [[ -e "$OUT" ]]; then echo "Run exists: $OUT" >&2; exit 2; fi
load1=$(cut -d ' ' -f 1 /proc/loadavg)
available_kb=$(awk '/^MemAvailable:/ {print $2}' /proc/meminfo)
if ! awk -v l="$load1" -v m="$available_kb" 'BEGIN {exit !(l <= 40 && m >= 31457280)}'; then
  echo "Deferred: load1=$load1 available_kb=$available_kb; wait >=15min" >&2; exit 75
fi
mkdir -p "$OUT"
printf '%s\n' "$SNAPSHOT" > "$OUT/snapshot.txt"
sha256sum "$SNAPSHOT/manifest.json" "$SNAPSHOT/SHA256SUMS" > "$OUT/frozen_source.sha256"
date -u +%FT%TZ > "$OUT/submitted_utc.txt"
{
  printf '%q ' nohup nice -n 19 bash "$SNAPSHOT/build/job.sh" "$SNAPSHOT" "$OUT" "$ACTION" "$@"
  printf '\n'
} > "$OUT/submission_command.txt"
# A uses at most three concurrent jobs, <=2 GiB address space each, single-thread BLAS.
# This is a resource guard, independent of the fit's declared allocation and budgets.
(
  ulimit -v 2097152
  exec nohup nice -n 19 bash "$SNAPSHOT/build/job.sh" "$SNAPSHOT" "$OUT" "$ACTION" "$@"
) > "$OUT/launcher.log" 2>&1 < /dev/null &
pid=$!
printf '%s\n' "$pid" > "$OUT/launch_pid.txt"
printf 'RUN=%s PID=%s OUT=%s\n' "$RUN" "$pid" "$OUT"
