#!/bin/bash
# truth_lib.sh: functions shared by truth_wave.sh (lock/unlock for the fitting wave) and recover_truth.sh (OPS recovery). Sourced, Linux only.
# The two truth trees of a study copy are STUDY/truth (1,200 files) and STUDY/dev/truth (60). Locked = mode 000 on directories and files.

tl_trees() { TL_TREES=("$1/truth" "$1/dev/truth"); }

# Open both trees without R: top-down (a 000 directory must be reopened before its children can be listed), then dirs 755, files 444.
tl_plain_unlock() {
  local t d n
  tl_trees "$1"
  for t in "${TL_TREES[@]}"; do
    [ -d "$t" ] || continue
    chmod 755 "$t" 2>/dev/null || true
    n=0
    while d=$(find "$t" -type d ! -perm -700 2>/dev/null | head -n 1) && [ -n "$d" ] && [ $n -lt 10000 ]; do chmod 755 "$d" 2>/dev/null || break; n=$((n + 1)); done
    find "$t" -type d -exec chmod 755 {} + 2>/dev/null || true
    find "$t" -type f -exec chmod 444 {} + 2>/dev/null || true
  done
}

# Verified OPEN: 1,200 / 60 files, every directory 755, every file 444.
tl_verify_open() {
  local nt nd bd bf rc=0
  tl_trees "$1"
  nt=$(find "${TL_TREES[0]}" -type f | wc -l); nd=$(find "${TL_TREES[1]}" -type f | wc -l)
  bd=$(( $(find "${TL_TREES[0]}" -type d ! -perm 755 | wc -l) + $(find "${TL_TREES[1]}" -type d ! -perm 755 | wc -l) ))
  bf=$(( $(find "${TL_TREES[0]}" -type f ! -perm 444 | wc -l) + $(find "${TL_TREES[1]}" -type f ! -perm 444 | wc -l) ))
  [ "$nt" = 1200 ] && [ "$nd" = 60 ] && [ "$bd" = 0 ] && [ "$bf" = 0 ] || rc=1
  echo "OPEN_STATE n_truth=$nt n_devtruth=$nd dirs_not_755=$bd files_not_444=$bf"
  return $rc
}

# Verified LOCKED: both top directories mode 000, ls denied, find lists no file (as the ordinary user; root bypasses permissions).
tl_verify_locked() {
  local m0 m1 denied=0 visible=0 rc=0
  tl_trees "$1"
  [ "$(id -u)" -ne 0 ] || { echo "LOCK_STATE cannot verify as root"; return 1; }
  m0=$(stat -c %a "${TL_TREES[0]}"); m1=$(stat -c %a "${TL_TREES[1]}")
  ls "${TL_TREES[0]}" >/dev/null 2>&1 || denied=$((denied + 1)); ls "${TL_TREES[1]}" >/dev/null 2>&1 || denied=$((denied + 1))
  visible=$(find "${TL_TREES[0]}" "${TL_TREES[1]}" -type f 2>/dev/null | wc -l)
  [ "$m0" = 0 ] && [ "$m1" = 0 ] && [ "$denied" = 2 ] && [ "$visible" = 0 ] || rc=1
  echo "LOCK_STATE truth_mode=$m0 devtruth_mode=$m1 ls_denied=$denied files_visible=$visible"
  return $rc
}

tl_sha_list() { (cd "$1" && find . -type f -print0 | sort -z | xargs -0 sha256sum) > "$2"; }
