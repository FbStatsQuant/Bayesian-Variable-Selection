#!/usr/bin/env bash
# mk_clone.sh <F40> [<PILOT40>] -- Owls: a SHALLOW clone holding only the freeze commit F (and optionally the pilot commit), ~150 MB.
# It is what `git -C CLONE archive F` and freeze_check_1e5.sh's tree check read on NOTS (there is no clone on NOTS; no GitHub needed).
# Needs F in /home/fb31/Bayesian-Variable-Selection (run `git fetch origin` there first). Prepares only; touches nothing on NOTS.
set -euo pipefail; . "$(dirname "$0")/common.sh"
F=${1:?F}; need_full_sha "$F"; SRC=/home/fb31/Bayesian-Variable-Selection
C=$STG/clone_${F:0:8}; rm -rf "$C"; git init -q "$C"
for c in "$@"; do need_full_sha "$c"; nice -n 19 git -C "$C" fetch -q --depth 1 "file://$SRC" "$c"; done
[[ $(git -C "$C" rev-parse "$F:$CORE_PATH") == "$CORE_TREE" ]] || { echo "FATAL: $F core tree is not the pin $CORE_TREE" >&2; exit 3; }
git -C "$C" rev-parse --verify "$F^{commit}"; du -sh "$C"; echo "clone: $C"
