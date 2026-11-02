#!/bin/bash
# truth_wave.sh -- lock / unlock the two staged truth trees of the study copy around the FITTING WAVE (LOWP_SPEC L.5: truth is mode 000
# while fits run). Runs as the ordinary user on NOTS (Linux).
#   bash truth_wave.sh lock   STUDY LOWP_R_DIR OUT_FILE
#   bash truth_wave.sh unlock STUDY LOWP_R_DIR OUT_FILE [PRE_DIR]     PRE_DIR = truth-lock test evidence dir with pre_truth.sha / pre_devtruth.sha
# lock: lowp_truth_lock(STUDY, TRUE), then VERIFIES mode 000 / unreadable. Exit 0 only if verified.
# unlock: lowp_truth_lock(STUDY, FALSE) (plain-chmod fallback), then VERIFIES 755/444, counts, and (with PRE_DIR) file hashes equal to before.
# Result lines (appended to OUT_FILE): WAVE_LOCK_VERIFIED ... / WAVE_UNLOCK_VERIFIED ... or the matching *_FAILED line.
set -uo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
source "$HERE/truth_lib.sh"
MODE=${1:-}; STUDY=${2:-}; RDIR=${3:-}; OUT=${4:-}; PRE=${5:-}
[ -n "$MODE" ] && [ -d "$STUDY/truth" ] && [ -d "$STUDY/dev/truth" ] && [ -f "$RDIR/lowp_seal.R" ] && [ -n "$OUT" ] || { echo "usage: truth_wave.sh lock|unlock STUDY LOWP_R_DIR OUT_FILE [PRE_DIR]" >&2; exit 3; }
RS=${RSCRIPT:-Rscript}
say() { echo "$*" | tee -a "$OUT"; }
rcall() { "$RS" --vanilla -e "source('$RDIR/lowp_seal.R'); r <- lowp_truth_lock('$STUDY', $1); print(unlist(r))" 2>&1; }
case "$MODE" in
  lock)
    say "# wave lock at $(date -u +%FT%TZ) by $(id -un) on $(hostname)"
    out=$(rcall TRUE); rc=$?; say "# R: rc=$rc $(echo "$out" | tr '\n' ' ' | cut -c1-200)"
    st=$(tl_verify_locked "$STUDY"); vrc=$?; say "$st"
    if [ $rc = 0 ] && [ $vrc = 0 ]; then say "WAVE_LOCK_VERIFIED $st"; exit 0; fi
    say "WAVE_LOCK_FAILED rc=$rc verify=$vrc"; exit 1 ;;
  unlock)
    say "# wave unlock at $(date -u +%FT%TZ) by $(id -un) on $(hostname)"
    out=$(rcall FALSE); rc=$?; say "# R: rc=$rc $(echo "$out" | tr '\n' ' ' | cut -c1-200)"
    if [ $rc != 0 ]; then say "# R unlock failed: plain-chmod fallback"; tl_plain_unlock "$STUDY"; fi
    st=$(tl_verify_open "$STUDY"); vrc=$?; say "$st"
    sha=skipped; shrc=0
    if [ -n "$PRE" ] && [ ! -e "$PRE/pre_truth.sha" ] && [ ! -e "$PRE/pre_devtruth.sha" ]; then
      # B2 (D44): BOTH pre-lock lists absent = the truth-lock test (P0c) and so the wave lock never ran (an earlier gate stopped the chain). The
      # trees were never locked: that is not a mismatch. Verify instead that every truth file still equals the STAGING list STAGED_SHA256.txt
      # (all 1,200 + 60, nothing missing). The open state is verified above as always.
      say "LOCK_NEVER_RAN: no pre-lock lists in $PRE (the truth-lock test and the wave lock did not run); verifying the truth files against the staging list instead"
      runh=$(dirname "$STUDY"); hroot=$(dirname "$(dirname "$runh")"); rel=${STUDY#"$hroot"/}; staged="$runh/STAGED_SHA256.txt"
      if [ ! -r "$staged" ]; then sha=STAGED_LIST_MISSING; shrc=1
      else
        tmp=$(mktemp -d)
        awk -v a="$rel/truth/" -v b="$rel/dev/truth/" '{ p = $2; sub(/^\*/, "", p); sub(/^\.\//, "", p) } index(p, a) == 1 || index(p, b) == 1' "$staged" > "$tmp/truth_staged.sha"
        nlist=$(wc -l < "$tmp/truth_staged.sha")
        # Sol PILOT7D R7D-2: the list must cover EVERY truth file exactly once: its normalised path set has no duplicate and equals a fresh
        # enumeration of both truth trees (1,200 + 60); only then are the original checksum lines verified.
        awk '{ p = $2; sub(/^\*/, "", p); sub(/^\.\//, "", p); print p }' "$tmp/truth_staged.sha" | LC_ALL=C sort > "$tmp/listed.txt"
        ( cd "$hroot" && find "$rel/truth" "$rel/dev/truth" -type f | LC_ALL=C sort ) > "$tmp/present.txt"
        ndup=$(LC_ALL=C uniq -d "$tmp/listed.txt" | wc -l)
        if [ "$nlist" != 1260 ] || [ "$ndup" != 0 ] || ! cmp -s "$tmp/listed.txt" "$tmp/present.txt"; then
          sha="STAGED_DIFFERENT(listed=$nlist duplicates=$ndup present=$(wc -l < "$tmp/present.txt"); the staging list does not cover each truth file exactly once)"; shrc=1
        elif ( cd "$hroot" && sha256sum --quiet -c "$tmp/truth_staged.sha" ) > "$tmp/chk.txt" 2>&1; then sha="staged_equal(1260)"
        else sha="STAGED_DIFFERENT(listed=$nlist; $(head -c 300 "$tmp/chk.txt" | tr '\n' ' '))"; shrc=1; fi
        rm -rf "$tmp"
      fi
    elif [ -n "$PRE" ]; then
      tmp=$(mktemp -d); sha=equal
      tl_sha_list "$STUDY/truth" "$tmp/t.sha"; tl_sha_list "$STUDY/dev/truth" "$tmp/d.sha"
      cmp -s "$tmp/t.sha" "$PRE/pre_truth.sha" && cmp -s "$tmp/d.sha" "$PRE/pre_devtruth.sha" || { sha=DIFFERENT; shrc=1; }   # one list missing = DIFFERENT too
      rm -rf "$tmp"
    fi
    say "SHA256_AGAINST_PRELOCK $sha"
    if [ $vrc = 0 ] && [ $shrc = 0 ]; then say "WAVE_UNLOCK_VERIFIED $st sha=$sha"; exit 0; fi
    say "WAVE_UNLOCK_FAILED verify=$vrc sha=$sha"; exit 1 ;;
  *) echo "mode must be lock or unlock" >&2; exit 3 ;;
esac
