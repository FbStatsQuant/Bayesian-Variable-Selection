#!/bin/bash
# frozen_check.sh: sourced (never executed) by stage_local.sh, submit_pilot.sh and the sbatch scripts (via slurm/common.sh).
# pilot_check_frozen TREE SUMS : the pilot must run exactly the frozen SMC-BVS v2.2.1 tree.
#   TREE = .../code/core/v2_2_1 (core/, study/, tools/, CHANGES_v2_2_1.md), SUMS = .../code/core/v2_2_1.SHA256SUMS (paths ./core/..., ./study/...,
#   ./tools/..., ./CHANGES_v2_2_1.md, relative to TREE). Passes only if (1) `sha256sum -c` succeeds for every listed file and (2) the tree holds no file the
#   manifest does not list. The only tolerated extra is the core's compile cache core/.cpp_cache (created by s0_build, never staged). Prints the reason
#   on stderr and returns 1 on any deviation.
pilot_check_frozen() {
  local tree=$1 sums=$2 listed present extra odd
  [ -d "$tree" ] || { echo "frozen v2.2.1 tree missing: $tree" >&2; return 1; }
  [ -r "$sums" ] || { echo "frozen v2.2.1 manifest missing: $sums" >&2; return 1; }
  [ "$(grep -c . "$sums")" -gt 0 ] || { echo "frozen v2.2.1 manifest is empty: $sums" >&2; return 1; }
  # CONF-2b (Sol F6): no symbolic link (to a file or a directory) and no special entry anywhere in the tree, the tree root included, except
  # inside the tolerated compile cache; only regular files and directories may make up the frozen tree.
  [ -L "$tree" ] && { echo "frozen v2.2.1 tree is a symbolic link: $tree" >&2; return 1; }
  odd=$( cd "$tree" && find . ! -type f ! -type d ! -path './core/.cpp_cache/*' | LC_ALL=C sort )
  if [ -n "$odd" ]; then echo "frozen v2.2.1 tree holds symbolic links or special entries: $(printf '%s' "$odd" | head -5 | tr '\n' ' ')" >&2; return 1; fi
  if ! ( cd "$tree" && sha256sum --quiet -c "$sums" >&2 ); then echo "frozen v2.2.1 tree does not match $sums" >&2; return 1; fi
  listed=$(sed -E 's/^[0-9a-fA-F]{64} [ *]//; s/\r$//' "$sums" | LC_ALL=C sort)
  present=$( cd "$tree" && find . -type f ! -path './core/.cpp_cache/*' | LC_ALL=C sort )
  extra=$(LC_ALL=C comm -13 <(printf '%s\n' "$listed") <(printf '%s\n' "$present"))
  if [ -n "$extra" ]; then echo "frozen v2.2.1 tree holds files the manifest does not list: $(printf '%s' "$extra" | head -5 | tr '\n' ' ')" >&2; return 1; fi
  return 0
}
