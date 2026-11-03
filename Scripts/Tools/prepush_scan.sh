#!/usr/bin/env bash
# prepush_scan.sh (v2) -- hygiene scan of exactly what the next commit will publish (PUBLIC repo).
# Usage:  git add <intended changes>;  bash Scripts/Tools/prepush_scan.sh [repo_root]
# Requires bash + GNU grep/coreutils + git. Exit 0 = PASS; any FAIL (including any tool/read error) exits 1 or 2.
# Re-run after every change to the index.
#
# Boundary: everything is read from the git INDEX (stage 0), never from the working tree:
#   - changed files = git diff --cached --name-only --diff-filter=ACMR -z  (NUL-delimited)
#   - the two policy files below are read from their index blobs
#   - sizes are index blob sizes (git cat-file), for every index entry
# FAIL categories, for every changed text blob (the scanner itself included):
#   SECRET  private-key blocks, GitHub/OpenAI/AWS key shapes, Bearer/Authorization headers,
#           password/passwd/secret/token/api-key assignments with any non-empty value
#   EMAIL   e-mail addresses
#   IP      private IPv4 (10/8, 172.16/12, 192.168/16)
#   T3ID    T3 thread/task/scheduled-task ids and thread links
#   WINPATH Windows user paths, unless the path is listed in PINNED_PATH_ALLOWLIST.txt
#   BINARY  a changed blob containing NUL bytes (not text-scannable), unless reviewed (see below)
#   SIZE    changed blob > 5 MiB; any index blob > 50 MiB; index total > 250 MiB (262144000 bytes)
#   UNMERGED / READ / TOOL  unmerged index entries, unreadable blobs, grep/git/wc errors
# Reviewed exceptions: Scripts/Tools/PREPUSH_REVIEWED.tsv, lines "path<TAB>blob_sha256<TAB>CATEGORY<TAB>reason".
#   An exception applies only to that exact blob (sha256 of the staged bytes) and that category;
#   any change to the file re-triggers the check. Categories allowed: SECRET, BINARY.
# INFO (reported, not failing): NOTS cluster paths / NetID (functional; see Docs/PUSH_CHECKLIST.md §2).
set -u
if [ $# -ge 1 ]; then cd "$1" || { echo "FAIL  TOOL  cannot cd to $1"; exit 2; }; fi
top=$(git rev-parse --show-toplevel 2>/dev/null) && cd "$top" || { echo "FAIL  TOOL  not inside a git repository"; exit 2; }
tmp=$(mktemp -d) || { echo "FAIL  TOOL  cannot create temp dir"; exit 2; }
trap 'rm -rf "$tmp"' EXIT

# Pattern literals are split ("a""b") so this file's own text does not match them; the file is still scanned.
PAT_KEY='BEGIN [A-Z ]*PRIVATE KEY|gh''p_[A-Za-z0-9]{20,}|github''_pat_[A-Za-z0-9_]{20,}|\bs''k-[A-Za-z0-9_-]{20,}|AK''IA[0-9A-Z]{16}'
PAT_HDR='[Bb]earer +[A-Za-z0-9._~+/=-]{16,}|Authoriza''tion: *[^ ]+'   # Bearer token >= 16 chars (avoids prose "Bearer or")
PAT_ASSIGN='(pass''w(or)?d|pass''wd|sec''ret|tok''en|api[_-]?k''ey)["'"'"' ]*[:=] *["'"'"']?[^"'"'"' ]'
PAT_EMAIL='[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}'
PAT_IP='\b(10\.[0-9]{1,3}|172\.(1[6-9]|2[0-9]|3[01])|192\.168)\.[0-9]{1,3}\.[0-9]{1,3}\b'
PAT_T3='m''cp:[0-9a-f]{6,}|t3-thr''ead://|node:delegated-ta''sk:|scheduled-ta''sk:[0-9a-f]{6,}'
PAT_WIN='[A-Za-z]:[\\/]+Use''rs[\\/]+|/c/Use''rs/'
PAT_NOTS='/home/fb31|/scratch/fb31|/projects/ml75'
ALLOW_PATH="Scripts/Tools/PINNED_PATH_ALLOWLIST.txt"
REVIEW_PATH="Scripts/Tools/PREPUSH_REVIEWED.tsv"

fail=0
flag() { echo "FAIL  $1  $2"; fail=1; }
die()  { echo "FAIL  TOOL  $1"; echo "FAIL  prepush_scan (tool error; result not trustworthy)"; exit 2; }

# --- index sanity: no unmerged entries --------------------------------------------------------------
git ls-files -u -z > "$tmp/unmerged" || die "git ls-files -u failed"
[ -s "$tmp/unmerged" ] && flag UNMERGED "index has unmerged entries"

# --- policy files from the INDEX -------------------------------------------------------------------
git show ":$ALLOW_PATH" > "$tmp/allow" 2>"$tmp/err" || die "allowlist $ALLOW_PATH not readable from index: $(head -c 200 "$tmp/err")"
git show ":$REVIEW_PATH" > "$tmp/review" 2>"$tmp/err" || die "reviewed-exceptions $REVIEW_PATH not readable from index: $(head -c 200 "$tmp/err")"

# grep wrapper: 0 = match, 1 = no match, anything else = tool error (never treated as clean)
g() { grep "$@"; rc=$?; [ $rc -le 1 ] || die "grep error (rc=$rc) on args: $*"; return $rc; }
reviewed() { # path sha category
  awk -F'\t' -v p="$1" -v s="$2" -v c="$3" '$1==p && $2==s && $3==c {f=1} END{exit !f}' "$tmp/review"
  rc=$?; [ $rc -le 1 ] || die "awk error on reviewed list"; return $rc; }

# --- sizes of ALL index entries (index blobs, not working tree) ------------------------------------
git ls-files -s -z > "$tmp/stage" || die "git ls-files -s failed"
tr '\0' '\n' < "$tmp/stage" | awk '{print $2}' > "$tmp/oids" || die "cannot parse index listing"
n_idx=$(wc -l < "$tmp/oids") || die "wc failed"
git cat-file --batch-check='%(objectsize)' < "$tmp/oids" > "$tmp/sizes" || die "git cat-file failed"
n_sz=$(wc -l < "$tmp/sizes") || die "wc failed"
[ "$n_idx" -eq "$n_sz" ] || die "size count $n_sz != index entries $n_idx"
g -qvE '^[0-9]+$' "$tmp/sizes" && die "non-numeric object size (missing object?)"
total=$(awk '{s+=$1} END{printf "%d", s}' "$tmp/sizes") || die "awk total failed"
big=$(awk '$1>52428800' "$tmp/sizes" | wc -l) || die "wc failed"
[ "$big" -gt 0 ] && flag SIZE "$big index blob(s) exceed 50 MiB"
[ "$total" -gt 262144000 ] && flag SIZE "index total $total bytes > 250 MiB"

# --- changed blobs ---------------------------------------------------------------------------------
# Optional PREPUSH_BASE=<commit>: scan everything changed between that commit and the index
# (e.g. to audit content already committed or pushed); default = changes vs HEAD.
git diff --cached --name-only --diff-filter=ACMR -z ${PREPUSH_BASE:+"$PREPUSH_BASE"} > "$tmp/files" || die "cannot list staged files"
nfiles=0; ninfo=0; nbin=0
while IFS= read -r -d '' f; do
  nfiles=$((nfiles+1))
  git show ":$f" > "$tmp/blob" 2>"$tmp/err" || { flag READ "$f: $(head -c 200 "$tmp/err")"; continue; }
  sz=$(wc -c < "$tmp/blob") || die "wc failed on $f"
  [ "$sz" -gt 5242880 ] && flag SIZE "$f ($sz bytes > 5 MiB)"
  [ "$sz" -eq 0 ] && continue
  sha=$(sha256sum "$tmp/blob" | cut -d' ' -f1); [ ${#sha} -eq 64 ] || die "sha256sum failed on $f"
  nnul=$(tr -cd '\000' < "$tmp/blob" | wc -c) || die "NUL count failed on $f"
  case "$nnul" in (*[!0-9\ ]*|"") die "NUL count not numeric on $f";; esac
  if [ "$nnul" -gt 0 ]; then
    nbin=$((nbin+1)); reviewed "$f" "$sha" BINARY || flag BINARY "$f (NUL bytes; not text-scannable; add a reviewed BINARY exception for sha $sha)"
    continue
  fi
  if g -nIiE "$PAT_KEY|$PAT_HDR|$PAT_ASSIGN" "$tmp/blob" > "$tmp/h"; then
    reviewed "$f" "$sha" SECRET || while IFS= read -r l; do flag SECRET "$f:${l%%:*}"; done < "$tmp/h"
  fi
  if g -nIE "$PAT_EMAIL" "$tmp/blob" > "$tmp/h"; then while IFS= read -r l; do flag EMAIL "$f:${l%%:*}"; done < "$tmp/h"; fi
  if g -nIE "$PAT_IP"    "$tmp/blob" > "$tmp/h"; then while IFS= read -r l; do flag IP    "$f:${l%%:*}"; done < "$tmp/h"; fi
  if g -nIE "$PAT_T3"    "$tmp/blob" > "$tmp/h"; then while IFS= read -r l; do flag T3ID  "$f:${l%%:*}"; done < "$tmp/h"; fi
  if g -qIE "$PAT_WIN" "$tmp/blob"; then
    g -qxF -- "$f" "$tmp/allow" || flag WINPATH "$f (Windows user path; file not on $ALLOW_PATH)"
  fi
  if g -qIE "$PAT_NOTS" "$tmp/blob"; then ninfo=$((ninfo+1)); fi
done < "$tmp/files"

echo "INFO  index entries: $n_idx; index total: $total bytes; changed blobs scanned: $nfiles (binary: $nbin); with NOTS paths/NetID (functional, allowed): $ninfo"
if [ "$fail" -eq 0 ]; then echo "PASS  prepush_scan"; exit 0; else echo "FAIL  prepush_scan (see lines above)"; exit 1; fi
