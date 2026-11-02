#!/bin/bash
# common.sh (PROD-L): the accepted pilot rev 7d slurm/common.sh, reused. Sourced (never executed) by every PROD-L sbatch script, AFTER
# `set -euo pipefail` and after prodl.env. Provides: pilot_init, pilot_modules, pilot_blas_single, pilot_require_frozen, timed, pilot_finish.
# PROD-L changes (REUSE.md): the hook list adds the PROD-L test hooks of DESIGN.md section 3; STAMP is exported by submit_prodl.sh; PILOT_ID is
# the PROD-L run id RID (set by prodl.env). Everything else is the pilot's code, unchanged.
# LOCAL-TEST hooks (listed in PILOT_HOOK_VARS) are REFUSED unless PILOT_LOCAL_TEST=1; submit_prodl.sh refuses them too, and records the
# effective environment.

: "${STAMP:?STAMP must be exported by submit_prodl.sh}"
: "${PILOT_ID:?prodl.env was not sourced with STAMP set}"
NFAIL=0

PILOT_HOOK_VARS=(PILOT_DRYRUN PILOT_SKIP_MODULES PILOT_LIMIT PILOT_BENCH_METHODS PILOT_BENCH_EXTRA PILOT_TIME_BIN PRODL_UNIT_CMD PRODL_TEST_WALL_S PRODL_TEST_BUDGET_S PRODL_TEST_NOW_OFFSET_S)
pilot_refuse_hooks() {
  [ "${PILOT_LOCAL_TEST:-0}" = 1 ] && return 0
  local v
  for v in "${PILOT_HOOK_VARS[@]}"; do
    if [ -n "${!v:-}" ]; then echo "pilot: test hook $v is set in a non-test run: refused (a real job must not inherit it)" >&2; exit 70; fi
  done
}

# ---- GNU time resolution (CONF-2b, HQ add-on; OPS-4 found no /usr/bin/time on NOTS) -----------------------------------------------------------
# Candidates, in order: the local-test hook PILOT_TIME_BIN alone (refused outside --local-test), else /usr/bin/time, then the NOTS module
# binary time/1.9 (GCCcore/13.3.0; used by its absolute path, no `module load`, so the R/compiler modules of the task are not disturbed).
# A candidate is accepted ONLY if it is GNU time: (1) `--version` prints "GNU Time" / "GNU time", AND (2) a format probe
# `-f '%e\t%U\t%S\t%M' -o FILE true` writes exactly four tab-separated numeric fields. The first accepted candidate wins.
# Arms whose units enter the sizing (enumeration, thread scaling, SMC, benchmarks) REFUSE to run without it (exit 68, fail closed);
# infrastructure arms (build, locks, verify, bitid, unlock, collect) continue with wall-clock-only timing, so a missing binary can never
# block the truth unlock. Gate thresholds in summarize_pilot.R are unchanged.
PILOT_GNU_TIME_NOTS=/opt/apps/software/time/1.9-GCCcore-13.3.0/bin/time
PILOT_TIME_REQUIRED_ARMS="enum20 enum30 scale smc smcrep p5 bench"   # PROD-L: smcrep and p5 added (their units are sized and logged per fit too)
pilot_is_gnu_time() {   # pilot_is_gnu_time BIN : 0 if BIN is an executable GNU time that honours -f/-o
  local b=$1 v pf line
  [ -x "$b" ] && [ ! -d "$b" ] || return 1
  v=$("$b" --version 2>&1 | head -n 3) || true
  printf '%s' "$v" | grep -qiE 'GNU[[:space:]]+time' || return 1
  pf=$(mktemp "${TMPDIR:-/tmp}/gnutime_probe.XXXXXX") || return 1
  "$b" -f '%e\t%U\t%S\t%M' -o "$pf" true >/dev/null 2>&1 || { rm -f -- "$pf"; return 1; }
  line=$(tail -n 1 "$pf"); rm -f -- "$pf"
  # four tab-separated fields: three valid nonnegative decimals (elapsed, user, sys) and an integer max RSS (Sol review 4, R4-2: no "." or "1..2")
  printf '%s\n' "$line" | grep -qE '^[0-9]+([.][0-9]+)?'$'\t''[0-9]+([.][0-9]+)?'$'\t''[0-9]+([.][0-9]+)?'$'\t''[0-9]+$'
}
pilot_resolve_time() {  # pilot_resolve_time CANDIDATE... : sets TIME_BIN to the first verified GNU time (else empty) and TIME_BIN_NOTE
  local c tried=""
  TIME_BIN=""
  for c in "$@"; do
    [ -n "$c" ] || continue
    if pilot_is_gnu_time "$c"; then TIME_BIN=$c; TIME_BIN_NOTE="verified GNU time: $c"; return 0; fi
    tried="$tried $c"
  done
  TIME_BIN_NOTE="no verified GNU time among:${tried:- (none)}"
  return 1
}
pilot_record_time_bin() {  # one record per task in the run's env folder: which binary timed this task's units, its version and sha256
  local f="$LOG_RUN/env/time_bin_${PILOT_ARM}_${JOB_ID_TAG}.txt"
  { echo "arm=$PILOT_ARM job=$JOB_ID_TAG host=$(hostname) utc=$(date -u +%FT%TZ)"
    echo "time_bin=${TIME_BIN:-none}"
    echo "note=$TIME_BIN_NOTE"
    if [ -n "$TIME_BIN" ]; then
      echo "version=$("$TIME_BIN" --version 2>&1 | head -n 1)"
      echo "sha256=$(sha256sum "$TIME_BIN" 2>/dev/null | cut -d' ' -f1)"
    fi; } > "$f" 2>&1 || true
}

# pilot_init ARM : create log folders, a private TMPDIR (removed on exit) and record where the task runs.
pilot_init() {
  if [[ ${SLURM_RESTART_COUNT:-0} != 0 ]]; then echo "Refusing restarted job ${SLURM_JOB_ID:-unknown}" >&2; exit 71; fi
  PILOT_ARM=$1
  pilot_refuse_hooks
  mkdir -p -- "$LOG_RUN/timing" "$LOG_RUN/units" "$LOG_RUN/env" "$TMP_ROOT"
  JOB_ID_TAG="${SLURM_ARRAY_JOB_ID:-${SLURM_JOB_ID:-local}}_${SLURM_ARRAY_TASK_ID:-0}"
  JOB_TMP="$TMP_ROOT/$JOB_ID_TAG"
  mkdir -p -- "$JOB_TMP"
  export TMPDIR="$JOB_TMP"
  trap 'rm -rf -- "$JOB_TMP"' EXIT
  # GNU time (CONF-2b, HQ add-on after OPS-4 probe job 2466301): NOTS has NO /usr/bin/time (login and Sapphire Rapids compute nodes);
  # GNU time 1.9 is the module time/1.9 (GCCcore/13.3.0) at $PILOT_GNU_TIME_NOTS. See pilot_resolve_time below.
  TIME_BIN=""; TIME_BIN_NOTE=""
  if [ -n "${PILOT_TIME_BIN:-}" ]; then pilot_resolve_time "$PILOT_TIME_BIN"; else pilot_resolve_time /usr/bin/time "$PILOT_GNU_TIME_NOTS"; fi || true
  pilot_record_time_bin
  if [ -z "$TIME_BIN" ] && [[ " $PILOT_TIME_REQUIRED_ARMS " == *" $PILOT_ARM "* ]] && [ "${PILOT_DRYRUN:-0}" != 1 ]; then
    echo "pilot: no verified GNU time binary ($TIME_BIN_NOTE): arm $PILOT_ARM needs user+sys CPU and max RSS for every unit (summarize_pilot.R would mark the pilot INCOMPLETE); refused BEFORE any unit runs" >&2
    exit 68
  fi
  echo "pilot_init arm=$PILOT_ARM host=$(hostname) job=$JOB_ID_TAG cpus=${SLURM_CPUS_PER_TASK:-NA} mem_mb=${SLURM_MEM_PER_NODE:-NA} time_bin=${TIME_BIN:-none}"
  if [ "${SLURM_ARRAY_TASK_ID:-0}" = 0 ]; then
    { echo "host=$(hostname) date=$(date -u +%FT%TZ) arm=$PILOT_ARM job=$JOB_ID_TAG constraint=${SLURM_JOB_CONSTRAINTS:-NA}"
      lscpu 2>/dev/null | grep -E 'Model name|^CPU\(s\)|Thread|Socket|L3|Flags' | sed -E 's/(Flags:).*(avx512[a-z_0-9]*).*/\1 ... \2 .../' | cut -c1-160
      echo "kernel=$(uname -r)"; } > "$LOG_RUN/env/node_${PILOT_ARM}_${JOB_ID_TAG}.txt" 2>&1 || true
  fi
}

# pilot_modules lowp|bench : load the modules named in pilot.env and set the R library search path.
pilot_modules() {
  local kind=$1 mods rl ru
  if [ "$kind" = bench ]; then mods=$MODULES_BENCH; rl=$R_LIBS_BENCH; ru=$R_LIBS_USER_BENCH
  else mods=$MODULES; rl=$R_LIBS_LOWP; ru=$R_LIBS_USER_LOWP; fi
  if [ "${PILOT_SKIP_MODULES:-0}" != 1 ]; then
    if [ -z "$mods" ]; then
      echo "pilot: MODULES$( [ "$kind" = bench ] && echo _BENCH ) is empty in $PILOT_DIR/prodl.env. OPS must fill it (must equal CONF's v2.2.1 NOTS build; the core is byte-identical to v2.2)." >&2
      exit 64
    fi
    set +u
    if ! type module >/dev/null 2>&1; then for f in /etc/profile.d/lmod.sh /etc/profile.d/modules.sh; do if [ -r "$f" ]; then . "$f"; break; fi; done; fi
    module purge
    # shellcheck disable=SC2086
    module load $mods
    set -u
  fi
  command -v Rscript >/dev/null 2>&1 || { echo "pilot: Rscript not on PATH after module load" >&2; exit 65; }
  export R_LIBS="$rl"
  if [ -n "$ru" ]; then export R_LIBS_USER="$ru"; fi
  # Never let R write a site/user profile or history into home
  export R_PROFILE_USER=/dev/null R_ENVIRON_USER=/dev/null R_HISTFILE=/dev/null
  { echo "kind=$kind modules=[$mods] R_LIBS=[$R_LIBS] R_LIBS_USER=[${R_LIBS_USER:-}]"
    Rscript --version 2>&1; (gcc --version 2>&1 | head -1) || true
    Rscript -e 'cat(R.version.string, "\n", paste(.libPaths(), collapse = "\n"), "\n", "BLAS: ", extSoftVersion()[["BLAS"]], "\n", "LAPACK: ", La_library(), "\n", sep = "")' 2>&1
  } > "$LOG_RUN/env/R_${PILOT_ARM}_${kind}_${JOB_ID_TAG}.txt" 2>&1 || true
}

# Single-threaded BLAS/OpenMP libraries (enumeration sets its own OpenMP threads afterwards).
pilot_blas_single() {
  export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
}

# timed ARM UNIT THREADS cmd args... : run the command, write its stdout+stderr to units/ARM.UNIT.log and one row to timing/*.tsv
# (wall, user, sys, max RSS in kB from the verified GNU time TIME_BIN set by pilot_init, else wall only and NA). A failing command is counted, not fatal.
timed() {
  local arm=$1 unit=$2 thr=$3; shift 3
  # PROD-L: the unit log name carries the job tag, so a resubmitted unit never overwrites the evidence of an earlier attempt
  local tfile="$LOG_RUN/timing/${arm}.${JOB_ID_TAG}.tsv" ulog="$LOG_RUN/units/${arm}.${unit}.${JOB_ID_TAG}.log"
  [ -s "$tfile" ] || printf 'arm\tunit\tthreads\trc\twall_s\tuser_s\tsys_s\tmaxrss_kb\thost\tjobid\ttaskid\tstart_utc\n' > "$tfile"
  if [ "${PILOT_DRYRUN:-0}" = 1 ]; then
    printf 'DRYRUN timed arm=%s unit=%s threads=%s :' "$arm" "$unit" "$thr"; printf ' %q' "$@"; echo
    return 0
  fi
  local rc=0 start wall user sys rss tf t0 t1
  start=$(date -u +%FT%TZ); tf="$JOB_TMP/time.$$.$RANDOM"
  if [ -n "$TIME_BIN" ]; then
    "$TIME_BIN" -f '%e\t%U\t%S\t%M' -o "$tf" "$@" > "$ulog" 2>&1 || rc=$?
    IFS=$'\t' read -r wall user sys rss < <(tail -n 1 "$tf") || true
    rm -f -- "$tf"
  else
    t0=$(date +%s.%N)
    "$@" > "$ulog" 2>&1 || rc=$?
    t1=$(date +%s.%N)
    wall=$(awk -v a="$t0" -v b="$t1" 'BEGIN{printf "%.2f", b-a}'); user=NA; sys=NA; rss=NA
  fi
  printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' "$arm" "$unit" "$thr" "$rc" "${wall:-NA}" "${user:-NA}" "${sys:-NA}" "${rss:-NA}" \
    "$(hostname)" "${SLURM_ARRAY_JOB_ID:-${SLURM_JOB_ID:-local}}" "${SLURM_ARRAY_TASK_ID:-0}" "$start" >> "$tfile"
  echo "timed $arm $unit rc=$rc wall=${wall:-NA}s maxrss_kb=${rss:-NA}"
  if [ "$rc" -ne 0 ]; then NFAIL=$((NFAIL + 1)); echo "--- tail of $ulog ---" >&2; tail -n 15 "$ulog" >&2 || true; fi
  return 0
}

# pilot_finish : exit status of the task = number of failed units > 0.
pilot_finish() {
  echo "pilot_finish arm=$PILOT_ARM failed_units=$NFAIL"
  [ "$NFAIL" -eq 0 ] || exit 1
  exit 0
}

# pilot_require_frozen : the staged code/core/v2_2_1 tree must still equal its manifest code/core/v2_2_1.SHA256SUMS (frozen SMC-BVS v2.2.1); exit 67 otherwise.
# Called by s0_build and by every SMC task, so each fit provably ran on the frozen tree (core/.cpp_cache is the only tolerated extra).
# shellcheck disable=SC1091
source "$PILOT_DIR/frozen_check.sh"
pilot_require_frozen() {
  pilot_check_frozen "$V221_DIR" "$V221_SUMS" || { echo "pilot: the staged v2.2.1 tree is not the frozen one (see above): refused" >&2; exit 67; }
  echo "pilot: frozen v2.2.1 tree verified ($(grep -c . "$V221_SUMS") files, manifest sha256 $(sha256sum "$V221_SUMS" | cut -c1-16))"
}
