#!/bin/bash
# remote_pack.sh: NOTS side of the New Campaign transfer tool (staged by scp, never inline base64).
# Usage:
#   remote_pack.sh manifest DIR          -> manifest of DIR on stdout (non-zero exit and no output on any failure)
#   remote_pack.sh tar DIR               -> tar stream of DIR's contents on stdout
#   remote_pack.sh delete DIR SHA        -> recompute the manifest; if its sha256 == SHA, delete exactly the
#                                           manifest's files and symlinks, then empty dirs, then DIR; else refuse
# Manifest: "<sha256>  ./<relpath>" per regular file (sorted, LC_ALL=C), then "#SYMLINK ./<relpath> -> <target>"
#   per symlink (sorted), then "#TOTAL files=<n> bytes=<b>". The manifest refuses (exit 2) if DIR holds any other
#   entry type, an entry not owned by fb31, a nested mount, or a name containing a newline or backslash.
# Allowed DIRs: New_Campaign/<subfolder>/<name>[/...] in scratch or home (never the scaffold folders themselves),
#   and, only with ALLOW_LEGACY=1, the two legacy BVS folders approved in ops/CLEANUP_PLAN.md (class A2).
# Failure handling: every step's status is checked explicitly (no reliance on errexit inside conditionals);
#   the manifest is built by a separate bash process (mode _inner) running under set -euo pipefail with all
#   enumerations written to temp files, so any failed cd/find/sort/sha256sum makes the whole manifest fail.
set -uo pipefail
export LC_ALL=C
SELF=$(readlink -e -- "$0") || { echo "remote_pack: cannot resolve self" >&2; exit 2; }
MODE=${1:-}; DIR=${2:-}
LEGACY_OK=(/scratch/fb31/smcbvs_v3_deploy_20261022 /projects/ml75/fb31/BVS/v3_profiling_20261020)

if [ "$MODE" = _inner ]; then
  # bash remote_pack.sh _inner DIR OUTFILE WORKDIR  (fresh process: errexit is fully active here)
  set -euo pipefail
  OUT=$3; W=$4
  cd -- "$DIR"
  find . ! -type f ! -type d ! -type l > "$W/other"
  [ ! -s "$W/other" ] || { echo "remote_pack: $(wc -l < "$W/other") entries of unsupported type" >&2; exit 2; }
  find . ! -user fb31 > "$W/foreign"
  [ ! -s "$W/foreign" ] || { echo "remote_pack: $(wc -l < "$W/foreign") entries not owned by fb31" >&2; exit 2; }
  find . > "$W/all"; find . -xdev > "$W/xdev"
  cmp -s "$W/all" "$W/xdev" || { echo "remote_pack: nested mount" >&2; exit 2; }
  find . \( -name $'*\n*' -o -name '*\\*' \) > "$W/badname"
  [ ! -s "$W/badname" ] || { echo "remote_pack: names with newline/backslash" >&2; exit 2; }
  find . -type f -print0 > "$W/files0"
  sort -z "$W/files0" > "$W/files0s"
  : > "$OUT"
  if [ -s "$W/files0s" ]; then xargs -0 sha256sum < "$W/files0s" >> "$OUT"; fi
  find . -type l -printf '#SYMLINK %p -> %l\n' > "$W/links"
  sort "$W/links" >> "$OUT"
  find . -type f -printf '%s\n' > "$W/sizes"
  awk '{n++; b+=$1} END {printf "#TOTAL files=%d bytes=%d\n", n, b}' "$W/sizes" >> "$OUT"
  NF=$(grep -c -v '^#' "$OUT" || true); NS=$(tr -cd '\0' < "$W/files0s" | wc -c)
  [ "$NF" = "$NS" ] || { echo "remote_pack: hash count $NF != file count $NS" >&2; exit 2; }
  exit 0
fi

allowed() {
  local d a; d=$(readlink -e -- "$1") || return 1
  [ "$d" = "$1" ] || return 1                     # canonical only: no symlinks or ../ in the path
  case "$d" in
    /projects/ml75/fb31/BVS/bench20261019|/projects/ml75/fb31/BVS/bench20261019/*) return 1;;
    /home/fb31/projects/BVS/Benchmarks|/home/fb31/projects/BVS/Benchmarks/*) return 1;;
    /scratch/fb31/New_Campaign/*/?*|/home/fb31/projects/BVS/New_Campaign/*/?*) return 0;;
  esac
  if [ "${ALLOW_LEGACY:-0}" = 1 ]; then for a in "${LEGACY_OK[@]}"; do [ "$d" = "$a" ] && return 0; done; fi
  return 1
}

WORK=$(mktemp -d /tmp/fb31_rp.XXXXXX) || { echo "remote_pack: mktemp failed" >&2; exit 2; }
trap 'rm -rf "$WORK"' EXIT
# manifest_to OUTFILE: separate process, status checked by the caller
manifest_to() { mkdir "$WORK/m$$_$1" || return 2; bash "$SELF" _inner "$DIR" "$WORK/$1" "$WORK/m$$_$1"; }

[ -n "$DIR" ] && [ -d "$DIR" ] || { echo "remote_pack: not a directory: $DIR" >&2; exit 2; }
allowed "$DIR" || { echo "remote_pack: path not allowed: $DIR" >&2; exit 3; }
case "$MODE" in
  manifest)
    manifest_to man; rc=$?
    [ $rc = 0 ] || { echo "remote_pack: manifest failed (rc=$rc)" >&2; exit 2; }
    cat "$WORK/man" || exit 2 ;;
  tar)
    tar -C "$DIR" -cf - . || exit 2 ;;
  delete)
    WANT=${3:-}; [[ "$WANT" =~ ^[0-9a-f]{64}$ ]] || { echo "remote_pack: need manifest sha256" >&2; exit 2; }
    Q=$(squeue -h -u fb31); qrc=$?
    [ $qrc = 0 ] || { echo "remote_pack: squeue failed (rc=$qrc); NOT deleted" >&2; exit 4; }
    [ -z "$Q" ] || { echo "remote_pack: jobs of fb31 queued/running; NOT deleted" >&2; exit 4; }
    manifest_to man; rc=$?
    [ $rc = 0 ] || { echo "remote_pack: manifest failed (rc=$rc); NOT deleted" >&2; exit 4; }
    GOT=$(sha256sum < "$WORK/man") || { echo "remote_pack: sha256 failed; NOT deleted" >&2; exit 4; }
    GOT=${GOT:0:64}
    [ "$GOT" = "$WANT" ] || { echo "remote_pack: manifest changed since verification ($GOT != $WANT); NOT deleted" >&2; exit 4; }
    SZ=$(du -sk -- "$DIR") || { echo "remote_pack: du failed; NOT deleted" >&2; exit 4; }; SZ=${SZ%%[[:space:]]*}
    { grep -v '^#' "$WORK/man" || [ $? = 1 ]; } > "$WORK/f.raw" || { echo "remote_pack: list build failed; NOT deleted" >&2; exit 4; }
    cut -c67- "$WORK/f.raw" > "$WORK/f" || exit 4
    { grep '^#SYMLINK ' "$WORK/man" || [ $? = 1 ]; } > "$WORK/l.raw" || { echo "remote_pack: link list failed; NOT deleted" >&2; exit 4; }
    sed -e 's/^#SYMLINK //' -e 's/ -> .*$//' "$WORK/l.raw" > "$WORK/l" || exit 4
    NFI=$(wc -l < "$WORK/f") && NLI=$(wc -l < "$WORK/l") || exit 4
    cd -- "$DIR" || { echo "remote_pack: cd failed; NOT deleted" >&2; exit 4; }
    if [ "$NFI" -gt 0 ]; then tr '\n' '\0' < "$WORK/f" | xargs -0 rm -- || { echo "remote_pack: PARTIAL file deletion in $DIR" >&2; exit 5; }; fi
    if [ "$NLI" -gt 0 ]; then tr '\n' '\0' < "$WORK/l" | xargs -0 rm -- || { echo "remote_pack: PARTIAL link deletion in $DIR" >&2; exit 5; }; fi
    find . -depth -mindepth 1 -type d -empty -delete || { echo "remote_pack: PARTIAL: dir pruning failed in $DIR" >&2; exit 5; }
    find . -mindepth 1 > "$WORK/left" || { echo "remote_pack: PARTIAL: final enumeration failed in $DIR" >&2; exit 5; }
    [ ! -s "$WORK/left" ] || { echo "remote_pack: PARTIAL: $(wc -l < "$WORK/left") unexpected entries left in $DIR (kept)" >&2; exit 5; }
    cd / && rmdir -- "$DIR" || { echo "remote_pack: PARTIAL: rmdir failed for $DIR" >&2; exit 5; }
    echo "DELETED $DIR kb=$SZ files=$NFI symlinks=$NLI" ;;
  *) echo "remote_pack: unknown mode $MODE" >&2; exit 2 ;;
esac
