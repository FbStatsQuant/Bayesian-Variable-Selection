#!/bin/bash
# Shared definition: locks, atomic temporary files, and uncommitted method files.
stale_find() {
  local root dir method ext path
  for root in "$@"; do
    [ -d "$root" ] || continue
    find "$root" -depth \( -type d -name '*.lock' -o -type f -regextype posix-extended -regex '.*/\.(F[1-5]|A[1-3])\.(rds|csv|sha256|done).*' \) -print
    while IFS= read -r -d '' dir; do
      for method in F1 F2 F3 F4 F5 A1 A2 A3; do
        [ ! -e "$dir/$method.done" ] || continue
        for ext in rds csv sha256; do
          path="$dir/$method.$ext"
          [ ! -e "$path" ] || printf '%s\n' "$path"
        done
      done
    done < <(find "$root" -type d -print0)
  done
}
