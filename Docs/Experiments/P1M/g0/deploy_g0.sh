#!/usr/bin/env bash
# deploy_g0.sh -- copy the G0 scripts from the repo (Owls) to NOTS ~/SMC_Engineering_Department/scripts/g0/.
# Run on Owls by the Engineering manager (helpers never run it). Two sequential uses of the multiplexed `ssh nots`
# connection: one rsync, one check. Light files only (about 150 kB).
# Usage: bash Docs/Experiments/P1M/g0/deploy_g0.sh
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")"
FILES=(SHA256SUMS README.md submit_g0.sh
       kernel/g0_bench.cpp kernel/build.sh kernel/run_kernel.sbatch kernel/kernel_summary.sh kernel/core_copy/v3_score.h kernel/core_copy/v3_util.h
       stage/stage_measure.R stage/stage_readback.R stage/ws_common.R stage/env_scale.sh stage/revD_SHA256SUMS stage/run_stage.sbatch stage/README.md)
sha256sum --quiet -c SHA256SUMS || { echo "FATAL: repo files differ from SHA256SUMS" >&2; exit 66; }
printf '%s\n' "${FILES[@]}" | rsync -a --files-from=- ./ nots:SMC_Engineering_Department/scripts/g0/
ssh nots 'cd ~/SMC_Engineering_Department/scripts/g0 && sha256sum --quiet -c SHA256SUMS && echo "deployed: $(wc -l < SHA256SUMS) files match"'
