#!/bin/bash
# precompile.sbatch (rerun2400): build the shared compile cache core/.cpp_cache of BOTH frozen trees (old = v2.2.1, new = v3.1) once, before any
# array task. Pattern of PROD_H/runner/precompile.sbatch (Lmod init + GCC/14.3.0 + R/4.5.2 + one thread via env.sh, manifest check, visible compiler
# output, env + .so hashes). Writes RUN_DIR/precompile.ok.old and precompile.ok.new ONLY on success; tasks refuse to run without them.
#   sbatch ... precompile.sbatch RUN_DIR
set -euo pipefail
RUN_DIR=$(realpath "$1")
source "$RUN_DIR/config.env"
source "$RUNNER/env.sh"
source "$RUNNER/frozen_check.sh"
PRE=$OUTROOT/precompile; mkdir -p "$PRE"
EV=$PRE/env_record_${SLURM_JOB_ID}.txt
{ echo "job $SLURM_JOB_ID host $(hostname) start $(date -u +%FT%TZ)"; echo "run_id $RUN_ID"; echo "constraint ${SLURM_JOB_CONSTRAINTS:-NA}"
  lscpu | grep -E '^(Model name|Flags)' | cut -c1-4000
  echo "gcc $(gcc -dumpfullversion)"; echo "gxx $(g++ -dumpfullversion)"
  Rscript --vanilla -e 'cat(R.version.string, "\n", sep = ""); cat("Rcpp ", as.character(packageVersion("Rcpp")), "\n", sep = "")'
  (module list 2>&1 || true) | sed 's/^/module_list /'
  env | grep -E '_NUM_THREADS|^LC_ALL|^R_LIBS|^LOADEDMODULES' | sort
  echo "R_CMD_config_CXX17 $(R CMD config CXX17) | $(R CMD config CXX17FLAGS) | $(R CMD config CXX17STD)"; } > "$EV"
( cd "$BUNDLE" && sha256sum --quiet -c SHA256SUMS ) || { echo "FATAL: bundle does not match SHA256SUMS" >&2; exit 67; }
for side in old new; do
  if [[ $side == old ]]; then CODE=$CODE_OLD; SUMS=$SUMS_OLD; else CODE=$CODE_NEW; SUMS=$SUMS_NEW; fi
  [ ! -e "$RUN_DIR/precompile.ok.$side" ] || { echo "FATAL: precompile.ok.$side exists" >&2; exit 65; }
  nc_check_frozen "$CODE" "$SUMS" || { echo "FATAL: frozen $side tree check failed" >&2; exit 67; }
  CLOG=$PRE/compile_${side}_${SLURM_JOB_ID}.log
  Rscript --vanilla "$RUNNER/precompile.R" "$CODE/core" > "$CLOG" 2>&1
  key=$(awk '$1 == "compiled_key" { print $2; exit }' "$CLOG")
  [[ "$key" =~ ^[0-9a-f]{64}$ ]] || { echo "FATAL: precompile printed no compiled_key for $side (see $CLOG)" >&2; exit 68; }
  [ -f "$CODE/core/.cpp_cache/${key:0:16}/READY" ] || { echo "FATAL: cache ${key:0:16} has no READY marker ($side)" >&2; exit 68; }
  nc_check_frozen "$CODE" "$SUMS" || { echo "FATAL: the frozen $side tree changed during the precompile" >&2; exit 67; }
  { echo "compiled_key $key"; find "$CODE/core/.cpp_cache" -name '*.so' -exec sha256sum {} \; | sed "s/^/so_sha256_$side /"; } >> "$EV"
  { echo "compiled_key $key"; echo "job $SLURM_JOB_ID"; echo "host $(hostname)"; echo "utc $(date -u +%FT%TZ)"
    find "$CODE/core/.cpp_cache" -name '*.so' -exec sha256sum {} \; | sed 's/^/so_sha256 /'; } > "$RUN_DIR/precompile.ok.$side.tmp"
  mv "$RUN_DIR/precompile.ok.$side.tmp" "$RUN_DIR/precompile.ok.$side"
  echo "precompile OK $side key ${key:0:16}"
done
echo "end $(date -u +%FT%TZ)" >> "$EV"
