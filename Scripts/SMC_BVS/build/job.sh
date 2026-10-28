#!/usr/bin/env bash
# Persistent Owls jobs, launched with nohup nice -n 19 bash job.sh ... .
# Usage: job.sh SNAPSHOT OUTPUT {build|tests|smoke|adapter} [arguments...]
set -euo pipefail
SNAPSHOT=${1:?snapshot}; OUT=${2:?output}; ACTION=${3:?action}; shift 3
A_ROOT=$(realpath /home/fb31/smcbvs_v3_deploy_20261022/A_build)
SNAPSHOT=$(realpath "$SNAPSHOT"); OUT=$(realpath -m "$OUT")
for path in "$SNAPSHOT" "$OUT"; do
  case "$path/" in "$A_ROOT/"*) ;; *) echo 'Path outside A ownership' >&2; exit 2;; esac
done
if [[ "$ACTION" == smoke ]]; then
  [[ $# -ge 7 && "$6" == 2 ]] || { echo 'A smoke needs explicit 2 GiB allocation and hours' >&2; exit 2; }
  for path in "$2" "$3"; do
    [[ "$path" == /* ]] || { echo 'Smoke paths must be absolute' >&2; exit 2; }
    resolved=$(realpath -m "$path")
    case "$resolved/" in "$A_ROOT/"*) ;; *) echo 'Smoke path outside A ownership' >&2; exit 2;; esac
  done
fi
mkdir -p "$OUT"
exec > >(tee -a "$OUT/job.stdout.log") 2> >(tee -a "$OUT/job.stderr.log" >&2)
trap 'rc=$?; printf "%s\n" "$rc" > "$OUT/exit_status.txt"; date -u +%FT%TZ > "$OUT/finished_utc.txt"' EXIT
date -u +%FT%TZ > "$OUT/started_utc.txt"
printf '%s\n' "$$" > "$OUT/process_id.txt"
printf '%q ' "$0" "$SNAPSHOT" "$OUT" "$ACTION" "$@" > "$OUT/launch_command.txt"
printf '\n' >> "$OUT/launch_command.txt"
source "$SNAPSHOT/build/env.sh"
# Amendment 1 shared-machine admission check. Caller retries >=15 min later on 75.
load1=$(cut -d ' ' -f 1 /proc/loadavg)
available_kb=$(awk '/^MemAvailable:/ {print $2}' /proc/meminfo)
if ! awk -v l="$load1" -v m="$available_kb" 'BEGIN {exit !(l <= 40 && m >= 31457280)}'; then
  echo "Admission deferred: load1=$load1 available_kb=$available_kb" >&2
  exit 75
fi
{
  hostname; date -u; uptime; free -g; gcc --version; Rscript --version
  ps -o pid,ppid,ni,comm -p $$
  ulimit -a; cat /proc/self/limits
  env | sort | grep -E '^(OMP_|OPENBLAS_|MKL_|BLIS_|FLEXIBLAS_|R_LIBS_USER)'
} > "$OUT/environment.txt"
cd "$SNAPSHOT"
sha256sum -c SHA256SUMS > "$OUT/source_validation.txt"
case "$ACTION" in
  build) /usr/bin/time -v -o "$OUT/time.txt" Rscript --vanilla build/build.R "$SNAPSHOT" "$OUT" ;;
  tests) /usr/bin/time -v -o "$OUT/time.txt" bash tests/run_all_seeds.sh "$SNAPSHOT/reference/prototype_core" "$SNAPSHOT/code/core" "$OUT/tests" "$@" ;;
  smoke) /usr/bin/time -v -o "$OUT/time.txt" Rscript --vanilla smoke/run_smoke.R "$@" ;;
  r1checks)
    /usr/bin/time -v -o "$OUT/time.txt" Rscript --vanilla smoke/test_adapter_contract.R "$OUT/adapter_tests"
    Rscript --vanilla build/check_r1_smokes.R "$SNAPSHOT" "$A_ROOT/r1_audit_inputs/smoke500.rds" "$A_ROOT/r1_audit_inputs/smoke1000.rds" "$OUT/smoke_mapping"
    for script in "$SNAPSHOT"/build/nots*.sh; do bash -n "$script"; done
    Rscript --vanilla -e 'invisible(parse("build/nots_build.R"))'
    python3 build/test_nots_finish.py "$SNAPSHOT" "$OUT/nots_exit_tests"
    printf 'NOTS shell and R syntax PASS; NOTS execution NOT PERFORMED\n' > "$OUT/nots_syntax.txt"
    ;;
  smokeaudit) /usr/bin/time -v -o "$OUT/time.txt" Rscript --vanilla build/check_smokes.R "$SNAPSHOT" "$A_ROOT" "$OUT" "$@" ;;
  adapter) /usr/bin/time -v -o "$OUT/time.txt" Rscript --vanilla smoke/test_adapter_contract.R "$OUT/adapter_tests" ;;
  *) echo "Unknown action: $ACTION" >&2; exit 2 ;;
esac
