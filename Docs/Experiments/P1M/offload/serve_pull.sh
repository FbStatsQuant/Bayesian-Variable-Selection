#!/usr/bin/env bash
# serve_pull.sh -- Owls side of the PC pull (OFFLOAD.md step 3/4). Engineering transfer crew. ONE ssh connection per pull:
#   stdin  = the client's list of units it has already verified (paths relative to records/, one per line)
#   stdout = an uncompressed tar of the next pending units (oldest first, at most MAX_GB), relative to records/
# A "unit" is a directory under records/ (depth 1-3) that contains a file named SHA256SUMS (sha256sum format, paths
# relative to the unit). Nothing but the tar is written to stdout; the log goes to crews/offload/serve.log.
# Usage (from the PC): ssh <alias> "bash ~/SMC_Engineering_Department/crews/offload/serve_pull.sh <client> <max_gb>"
set -euo pipefail
DEPT=/home/fb31/SMC_Engineering_Department
REC="${SMC_OFFLOAD_RECORDS:-$DEPT/records}"            # override only for tests, and only inside the department folder
case "$(realpath -m "$REC")/" in "$(realpath -m "$DEPT")"/*) ;; *) echo "refusing: records root outside $DEPT" >&2; exit 64 ;; esac
CREW="$DEPT/crews/offload"; mkdir -p "$CREW"
client="${1:?client name}"; max_gb="${2:-50}"
[[ "$client" =~ ^[a-z0-9_-]{1,32}$ ]] || { echo "refusing: bad client name" >&2; exit 64; }
[[ "$max_gb" =~ ^[0-9]{1,4}$ && "$max_gb" -ge 1 ]] || { echo "refusing: bad max_gb" >&2; exit 64; }
log() { printf '%s %s %s\n' "$(date -Iseconds)" "$client" "$*" >> "$CREW/serve.log"; }
tmp=$(mktemp -d "$CREW/.serve.XXXXXX"); trap 'rm -rf "$tmp"' EXIT
# 1. the client's verified list (strip CR from Windows line ends; keep only safe relative paths)
tr -d '\r' | grep -E '^[A-Za-z0-9._/-]+$' | grep -v '\.\.' | sort -u > "$tmp/have" || true
cp "$tmp/have" "$CREW/${client}_verified.txt.tmp" && mv "$CREW/${client}_verified.txt.tmp" "$CREW/${client}_verified.txt"
# 2. pending units, oldest first, up to max_gb
cd "$REC"
find . -mindepth 2 -maxdepth 4 -type f -name SHA256SUMS -printf '%T@ %h\n' | sed 's# \./# #' | sort -n | awk '{print $2}' > "$tmp/all"
grep -vxF -f "$tmp/have" "$tmp/all" > "$tmp/pending" || true
cap=$(( max_gb * 1024 * 1024 * 1024 )); tot=0; : > "$tmp/send"
while read -r u; do
  [[ -n "$u" ]] || continue
  sz=$(du -sb -- "$u" | cut -f1)
  if (( tot > 0 && tot + sz > cap )); then break; fi      # always send at least one unit, even if it alone exceeds the cap
  echo "$u" >> "$tmp/send"; tot=$(( tot + sz ))
done < "$tmp/pending"
n=$(wc -l < "$tmp/send"); left=$(( $(wc -l < "$tmp/pending") - n ))
log "verified=$(wc -l < "$tmp/have") sending=$n units bytes=$tot pending_after=$left"
# 3. the tar (an empty, valid tar when nothing is pending)
nice -n 10 tar -cf - --files-from "$tmp/send"
