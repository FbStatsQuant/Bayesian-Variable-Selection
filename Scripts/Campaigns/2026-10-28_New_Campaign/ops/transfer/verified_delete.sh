#!/bin/bash
# verified_delete.sh: delete exactly the files (and approved symlinks) of a sha256 list whose laptop copy was
# verified, after re-checking everything on NOTS. Fails closed: any doubt -> nothing deleted, non-zero exit.
# Usage: verified_delete.sh BASE LIST LIST_SHA256 [LINKS LINKS_SHA256]
#   BASE   one of the explicitly approved class-A bases below (canonical path, no symlink in it).
#   LIST   sha256sum lines "<64 hex>  ./<relpath>", paths relative to BASE, exactly as verified on the laptop.
#   LINKS  approved symlinks, lines "./<relpath> -> <target>" (find -printf '%p -> %l'); omitted = none allowed.
# Gates (all before any unlink): BASE in the allowlist; list/link bytes match their sha256 (copied to a private
# temp dir first, so later edits of the inputs do not matter); strict line syntax, no '.'/'..' components, no
# duplicates; the set of regular files found under BASE (find does not follow symlinks) EQUALS the list;
# the symlinks found EQUAL the approved links; no other entry types; every entry owned by fb31; no nested
# mounts; no queued/running jobs of fb31; `sha256sum -c` passes for every entry.
# Deletion: listed files, then approved links (the link objects only, never their targets), then empty dirs,
# then BASE itself. Any residue or failed command -> exit non-zero.
set -euo pipefail
export LC_ALL=C
ALLOWED=(
  /scratch/fb31/smcbvs_v3_deploy_20261022/claude/prod_p0500_20261023T1227Z/results
  /scratch/fb31/smcbvs_v3_deploy_20261022/claude/prod_p1000_20261023T1227Z/results
  /home/fb31/projects/BVS/Others
)
die() { echo "verified_delete: $*; nothing deleted" >&2; exit 4; }
BASE=${1:?}; LIST_IN=${2:?}; WANT=${3:?}; LINKS_IN=${4:-}; LINKS_WANT=${5:-}

CB=$(readlink -e -- "$BASE") || die "base does not exist"
[ "$CB" = "$BASE" ] || die "base is not canonical ($CB)"
ok=0; for a in "${ALLOWED[@]}"; do [ "$CB" = "$a" ] && ok=1; done
# test-only base for tool tests (VDEL_ALLOW_TEST=1): /scratch/fb31/New_Campaign/runs/_vdel_test_<name>
if [ "${VDEL_ALLOW_TEST:-0}" = 1 ]; then case "$CB" in /scratch/fb31/New_Campaign/runs/_vdel_test_?*) ok=1;; esac; fi
[ $ok = 1 ] || die "base not in the class-A allowlist"
case "$CB" in /projects/ml75/fb31/BVS/bench20261019*|/home/fb31/projects/BVS/Benchmarks*) die "frozen path";; esac

TMP=$(mktemp -d /tmp/fb31_vdel.XXXXXX); trap 'rm -rf "$TMP"' EXIT
cp -- "$LIST_IN" "$TMP/list"
[ "$(sha256sum < "$TMP/list" | cut -c1-64)" = "$WANT" ] || die "list sha256 mismatch"
: > "$TMP/links_ok"
if [ -n "$LINKS_IN" ]; then
  cp -- "$LINKS_IN" "$TMP/links_in"
  [ "$(sha256sum < "$TMP/links_in" | cut -c1-64)" = "$LINKS_WANT" ] || die "links sha256 mismatch"
  sort -o "$TMP/links_ok" "$TMP/links_in"
fi

# strict syntax: '<64 hex><2 spaces>./<path>' ; no backslash-escaped names; no empty/'.'/'..' components
BADL=$(grep -cvE '^[0-9a-f]{64}  \./[^\\]+$' "$TMP/list" || true)
[ "$BADL" = 0 ] || die "$BADL malformed list lines"
cut -c67- "$TMP/list" > "$TMP/paths"
BADP=$(awk -F/ '{for(i=2;i<=NF;i++) if($i==""||$i=="."||$i=="..") {n++; break}} END{print n+0}' "$TMP/paths")
[ "$BADP" = 0 ] || die "$BADP list paths with empty, '.' or '..' components"
sort "$TMP/paths" > "$TMP/listed"
[ -z "$(uniq -d "$TMP/listed")" ] || die "duplicate list entries"
N=$(wc -l < "$TMP/listed")

# writer exclusion: no jobs of ours (OPS is the only NOTS session that writes here)
J=$(squeue -h -u fb31 | wc -l); [ "$J" = 0 ] || die "$J jobs of fb31 queued/running"

cd "$CB"
find . -type f > "$TMP/found_raw"; sort "$TMP/found_raw" > "$TMP/found"
cmp -s "$TMP/listed" "$TMP/found" || die "regular files under base differ from the list ($(comm -3 "$TMP/listed" "$TMP/found" | wc -l) differences)"
find . -type l -printf '%p -> %l\n' > "$TMP/links_raw"; sort "$TMP/links_raw" > "$TMP/links_found"
cmp -s "$TMP/links_ok" "$TMP/links_found" || die "symlinks under base differ from the approved list"
OTHER=$(find . ! -type f ! -type d ! -type l | wc -l); [ "$OTHER" = 0 ] || die "$OTHER entries of other types"
FOREIGN=$(find . ! -user fb31 | wc -l); [ "$FOREIGN" = 0 ] || die "$FOREIGN entries not owned by fb31"
[ "$(find . | wc -l)" = "$(find . -xdev | wc -l)" ] || die "nested mount under base"
sha256sum -c --quiet --strict "$TMP/list" >&2 || die "sha256 re-check failed"
KB=$(du -sk . | cut -f1)

# delete
tr '\n' '\0' < "$TMP/paths" | xargs -0 rm --
NLINK=$(wc -l < "$TMP/links_ok")
if [ "$NLINK" -gt 0 ]; then sed 's/ -> .*$//' "$TMP/links_ok" | tr '\n' '\0' | xargs -0 rm --; fi
find . -depth -mindepth 1 -type d -empty -delete
LEFT=$(find . -mindepth 1 | wc -l)
if [ "$LEFT" != 0 ]; then echo "verified_delete: PARTIAL: $LEFT entries left under $CB" >&2; exit 5; fi
cd /; rmdir -- "$CB"
echo "VERIFIED_DELETE base=$CB files=$N symlinks=$NLINK kb=$KB list_sha256=$WANT left=0 base_removed=yes"
