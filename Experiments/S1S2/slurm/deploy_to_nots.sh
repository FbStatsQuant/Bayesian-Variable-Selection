#!/usr/bin/env bash
# deploy_to_nots.sh -- run on OWLS. Snapshot Experiments/S1S2 + the vendored SMC-BVS core to NOTS, with a SHA256 manifest.
#   deploy_to_nots.sh [--commit HASH] [--dry-run]
#     --commit HASH : export Experiments/S1S2 from that commit (git archive)  <- the production deploy
#     (default)     : rsync of the current worktree (a pre-commit SNAPSHOT; DEPLOY_INFO.txt says so)
# NOTS layout (POLICIES §8):  DEPLOY=/home/fb31/SMC-BVS/_local/engineering/S1S2/deploy/{S1S2/,smcbvs_core@7100bb3b/,
#   MANIFEST.sha256, DEPLOY_INFO.txt}   ENV=/home/fb31/SMC-BVS/_local/engineering/envs/S1S2/env.sh (from slurm/nots_env.sh)
#   and, if the deploy has slurm/nots_env_bench.sh, ENV_BENCH=.../envs/S1S2/env_bench.sh (benchmark grids; sourced by
#   bench_array.sbatch); without it a WARNING is printed and env_bench.sh on NOTS is left as it is.
# The core's compiled cache (smcbvs_core@7100bb3b/.cpp_cache/) lives on NOTS only: it is excluded from the copy and the
# manifest, and protected from --delete. ONE ssh stream (ControlMaster); nothing is compiled or run here.
set -euo pipefail
REPO=/home/fb31/BVS-wt/P1M
CORE_SRC=/home/fb31/Bayesian-Variable-Selection/_local/engineering/ext/smcbvs_core@7100bb3b
ENG_N=/home/fb31/SMC-BVS/_local/engineering
DEPLOY=$ENG_N/S1S2/deploy
ENVDIR=$ENG_N/envs/S1S2
commit=""; dry=0
while (($#)); do case "$1" in --commit) commit="$2"; shift 2;; --dry-run) dry=1; shift;; *) echo "unknown arg $1" >&2; exit 64;; esac; done

STAGE=/home/fb31/Bayesian-Variable-Selection/_local/tmp/$(date +%Y%m%d)-opusN-s1s2deploy
rm -rf "$STAGE"; mkdir -p "$STAGE"; trap 'rm -rf "$STAGE"' EXIT
if [[ -n "$commit" ]]; then
  git -C "$REPO" cat-file -e "$commit^{commit}"
  git -C "$REPO" archive "$commit" Experiments/S1S2 | tar -x -C "$STAGE"
  mv "$STAGE/Experiments/S1S2" "$STAGE/S1S2"; rmdir "$STAGE/Experiments"
  src="commit $(git -C "$REPO" rev-parse "$commit")"
else
  rsync -a --exclude 'octave-workspace' --exclude '.Rhistory' --exclude '*.tmp' "$REPO/Experiments/S1S2/" "$STAGE/S1S2/"
  src="worktree SNAPSHOT of $REPO (HEAD $(git -C "$REPO" rev-parse --short HEAD); Experiments/S1S2 uncommitted/dirty) -- NOT the production deploy"
fi
rsync -a --exclude '.cpp_cache' "$CORE_SRC/" "$STAGE/smcbvs_core@7100bb3b/"
{ echo "deployed_utc: $(date -u +%FT%TZ)"; echo "source: $src"; echo "core: $CORE_SRC (tag method-v3.1.1-listpip, commit 15a6d841, core tree 61b0a582)";
  echo "manifest: MANIFEST.sha256 (every file except itself and DEPLOY_INFO.txt; .cpp_cache excluded)"; } > "$STAGE/DEPLOY_INFO.txt"
( cd "$STAGE" && find . -type f ! -name MANIFEST.sha256 ! -name DEPLOY_INFO.txt | LC_ALL=C sort | sed 's#^\./##' | xargs -d '\n' sha256sum > MANIFEST.sha256 )
mhash=$(sha256sum "$STAGE/MANIFEST.sha256" | cut -c1-64)
echo "files: $(wc -l < "$STAGE/MANIFEST.sha256")  MANIFEST.sha256 sha256=$mhash"
echo "manifest_sha256: $mhash" >> "$STAGE/DEPLOY_INFO.txt"
bench_env=0; [[ -f "$STAGE/S1S2/slurm/nots_env_bench.sh" ]] && bench_env=1
((bench_env)) || echo "WARNING: slurm/nots_env_bench.sh not in this deploy: env_bench.sh on NOTS not installed/updated (benchmark arrays need it)" >&2
if ((dry)); then echo "[dry-run] would rsync $STAGE/ -> nots:$DEPLOY/ and install env -> nots:$ENVDIR/env.sh$( ((bench_env)) && echo " + env_bench.sh")"; exit 0; fi

ssh nots "mkdir -p '$DEPLOY' '$ENVDIR'"
rsync -a --delete --filter 'P smcbvs_core@7100bb3b/.cpp_cache/' "$STAGE/" "nots:$DEPLOY/"
rsync -a "$STAGE/S1S2/slurm/nots_env.sh" "nots:$ENVDIR/env.sh"
((bench_env)) && rsync -a "$STAGE/S1S2/slurm/nots_env_bench.sh" "nots:$ENVDIR/env_bench.sh"
ssh nots "cd '$DEPLOY' && sha256sum --quiet -c MANIFEST.sha256 && echo 'NOTS manifest check: OK' && sha256sum MANIFEST.sha256 && cmp S1S2/slurm/nots_env.sh '$ENVDIR/env.sh' && echo 'env.sh == deploy copy'"
if ((bench_env)); then ssh nots "cd '$DEPLOY' && cmp S1S2/slurm/nots_env_bench.sh '$ENVDIR/env_bench.sh' && echo 'env_bench.sh == deploy copy'"; fi
