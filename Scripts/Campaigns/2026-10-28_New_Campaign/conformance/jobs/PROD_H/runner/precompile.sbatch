#!/bin/bash
# precompile.sbatch: build the shared compile cache core/.cpp_cache of the frozen v2.2.1 tree ONCE, before any array task starts.
# Submitted by submit.sh (all sbatch options are on its command line and recorded in launch/sbatch_args.txt); the arrays depend on it (afterok).
#   sbatch ... precompile.sbatch RUN_DIR
# Pattern of CONF_NOTS_IDENTITY/job.sh: Lmod init + GCC/14.3.0 + R/4.5.2 + one thread (runner/env.sh), manifest check, visible compiler output,
# environment record, .so hashes. Writes RUN_DIR/precompile.ok ONLY on success; the array tasks refuse to run without it (they never compile).
set -euo pipefail
RUN_DIR=$(realpath "$1")
source "$RUN_DIR/config.env"        # RUN_ID CODE SUMS STUDY OUTROOT LOGROOT RUNNER ...
RUNNER_DIR=$RUNNER
source "$RUNNER/env.sh"
source "$RUNNER/frozen_check.sh"
PRE=$LOGROOT/precompile
mkdir -p "$PRE"
EV=$PRE/env_record_${SLURM_JOB_ID}.txt
CLOG=$PRE/compile_${SLURM_JOB_ID}.log
[ ! -e "$RUN_DIR/precompile.ok" ] || { echo "FATAL: $RUN_DIR/precompile.ok exists: this run was already precompiled" >&2; exit 65; }
{ echo "job $SLURM_JOB_ID host $(hostname) start $(date -u +%FT%TZ)"
  echo "run_id $RUN_ID"; echo "constraint ${SLURM_JOB_CONSTRAINTS:-NA}"; } > "$EV"
nc_check_frozen "$CODE" "$SUMS" || { echo "FATAL: frozen v2.2.1 tree check failed" >&2; exit 67; }
echo "manifest_sha256 $(sha256sum "$SUMS" | cut -d' ' -f1)  files $(grep -c . "$SUMS")" >> "$EV"
{ lscpu | grep -E '^(Model name|Flags)' | cut -c1-4000
  echo "gcc $(gcc -dumpfullversion)"; echo "gxx $(g++ -dumpfullversion)"
  Rscript --vanilla -e 'cat(R.version.string, "\n", sep = ""); cat("Rcpp ", as.character(packageVersion("Rcpp")), "\n", sep = "")'
  (module list 2>&1 || true) | sed 's/^/module_list /'
  env | grep -E '_NUM_THREADS|^LC_ALL|^R_LIBS|^LOADEDMODULES' | sort
  echo "R_CMD_config_CXX17 $(R CMD config CXX17) | $(R CMD config CXX17FLAGS) | $(R CMD config CXX17STD)"; } >> "$EV"
# Fresh compile with visible compiler commands (job-side; the frozen sources are untouched). A cache from an earlier build with the same
# source key is reused by v3_compile itself (READY), and its .so hashes are recorded below either way.
Rscript --vanilla "$RUNNER/precompile.R" "$CODE/core" > "$CLOG" 2>&1
key=$(awk '$1 == "compiled_key" { print $2; exit }' "$CLOG")
[[ "$key" =~ ^[0-9a-f]{64}$ ]] || { echo "FATAL: precompile printed no compiled_key (see $CLOG)" >&2; exit 68; }
[ -f "$CODE/core/.cpp_cache/${key:0:16}/READY" ] || { echo "FATAL: cache ${key:0:16} has no READY marker" >&2; exit 68; }
nc_check_frozen "$CODE" "$SUMS" || { echo "FATAL: the frozen tree changed during the precompile" >&2; exit 67; }
{ echo "compiled_key $key"; find "$CODE/core/.cpp_cache" -name '*.so' -exec sha256sum {} \; | sed 's/^/so_sha256 /'; echo "end $(date -u +%FT%TZ)"; } >> "$EV"
# the small durable record the array tasks check (home, a few hundred bytes)
{ echo "compiled_key $key"; echo "job $SLURM_JOB_ID"; echo "host $(hostname)"; echo "utc $(date -u +%FT%TZ)"
  find "$CODE/core/.cpp_cache" -name '*.so' -exec sha256sum {} \; | sed 's/^/so_sha256 /'; } > "$RUN_DIR/precompile.ok.tmp"
mv "$RUN_DIR/precompile.ok.tmp" "$RUN_DIR/precompile.ok"
echo "precompile OK key ${key:0:16}"
