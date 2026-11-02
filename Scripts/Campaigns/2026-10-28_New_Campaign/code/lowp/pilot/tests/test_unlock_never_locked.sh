#!/bin/bash
# test_unlock_never_locked.sh -- local test of the wave-unlock decision in truth_wave.sh (B2, HQ D44).
#   bash tests/test_unlock_never_locked.sh WORKDIR
# A fake HOME/runs/<PID> holds study/truth (1,200 files), study/dev/truth (60) and a STAGED_SHA256.txt built exactly as stage_local.sh builds it
# (find . | sha256sum from the HOME root). truth_wave.sh is copied next to a STUB truth_lib.sh: the Linux-only permission helpers (chmod / stat
# modes, tested on NOTS by test_truth_lock_linux.sh) are replaced by "open"; tl_sha_list and the hash logic are real.
set -u
W=${1:?usage: test_unlock_never_locked.sh WORKDIR}; rm -rf "$W"; mkdir -p "$W"; W=$(cd "$W" && pwd)
HERE=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd); PILOT=$(cd "$HERE/.." && pwd); RDIR=$(cd "$PILOT/../R" && pwd)
STAMP=20261030T0313Z; PID=${STAMP}_lowp_pilot
H=$W/home; RH=$H/runs/$PID; ST=$RH/study; P=$W/pilot
FAIL=0; N=0
res() { N=$((N + 1)); if [ "$2" = "$3" ] && [ "${4:-0}" = 0 ]; then echo "| $1 | $2 | $3 | ok |"; else echo "| $1 | $2 | $3 (extra=${4:-0}) | **WRONG** |"; FAIL=$((FAIL + 1)); fi; }
mkdir -p "$P" "$ST/truth/p0020" "$ST/truth/p0030" "$ST/dev/truth/p0020" "$ST/dev/truth/p0030" "$W/pre"
cp "$PILOT/truth_wave.sh" "$P/"
cat > "$P/truth_lib.sh" <<'L'
# STUB for the local test: permission states are Linux-only; hash listing is the real function
tl_trees() { TL_TREES=("$1/truth" "$1/dev/truth"); }
tl_plain_unlock() { :; }
tl_verify_open() { local nt nd; nt=$(find "$1/truth" -type f | wc -l); nd=$(find "$1/dev/truth" -type f | wc -l); echo "OPEN_STATE n_truth=$nt n_devtruth=$nd (stub: modes not checked)"; [ "$nt" = 1200 ] && [ "$nd" = 60 ]; }
tl_verify_locked() { echo "LOCK_STATE stub"; return 1; }
tl_sha_list() { (cd "$1" && find . -type f -print0 | sort -z | xargs -0 sha256sum) > "$2"; }
L
printf '#!/bin/bash\nexit 1\n' > "$W/Rscript_stub"; chmod +x "$W/Rscript_stub"
for p in 20 30; do for i in $(seq 1 600); do echo "t$p.$i" > "$ST/truth/p00$p/f$i.rds"; done; for i in $(seq 1 30); do echo "d$p.$i" > "$ST/dev/truth/p00$p/f$i.rds"; done; done
echo other > "$RH/OWNER"
( cd "$H" && find . -type f ! -name STAGED_SHA256.txt | LC_ALL=C sort | xargs -d '\n' sha256sum > "runs/$PID/STAGED_SHA256.txt" )
unlock() { rm -f "$W/out.txt"; RSCRIPT="$W/Rscript_stub" bash "$P/truth_wave.sh" unlock "$ST" "$RDIR" "$W/out.txt" "$W/pre" > "$W/run.log" 2>&1; echo $?; }
echo "| Case | Expected | Got | Result |"; echo "|---|---|---|---|"
rc=$(unlock); res "never locked (no pre-lock lists), files intact: VERIFIED, exit 0, LOCK_NEVER_RAN and staged_equal(1260) reported" 0 "$rc" \
  $(grep -q "^LOCK_NEVER_RAN" "$W/out.txt" && grep -q "^WAVE_UNLOCK_VERIFIED .*sha=staged_equal(1260)" "$W/out.txt" && echo 0 || echo 1)
cp "$ST/truth/p0020/f7.rds" "$W/f7.bak"; echo tampered > "$ST/truth/p0020/f7.rds"
rc=$(unlock); res "never locked, one truth file CHANGED: a real mismatch still FAILS (exit 1, STAGED_DIFFERENT)" 1 "$rc" $(grep -q "STAGED_DIFFERENT" "$W/out.txt" && grep -q "^WAVE_UNLOCK_FAILED" "$W/out.txt" && echo 0 || echo 1)
cp "$W/f7.bak" "$ST/truth/p0020/f7.rds"; mv "$ST/dev/truth/p0030/f3.rds" "$W/f3.bak"
rc=$(unlock); res "never locked, one dev truth file MISSING: FAILS (exit 1)" 1 "$rc" $(grep -q "^WAVE_UNLOCK_FAILED" "$W/out.txt" && echo 0 || echo 1)
mv "$W/f3.bak" "$ST/dev/truth/p0030/f3.rds"; mv "$RH/STAGED_SHA256.txt" "$W/staged.bak"
rc=$(unlock); res "never locked but the staging list is missing: FAILS (exit 1, STAGED_LIST_MISSING), never assumed fine" 1 "$rc" $(grep -q "STAGED_LIST_MISSING" "$W/out.txt" && echo 0 || echo 1)
mv "$W/staged.bak" "$RH/STAGED_SHA256.txt"
# R7D-2: a malformed staging list whose line for f7 is replaced by a DUPLICATE of another valid line (still 1,260 lines), with f7 then changed
cp "$RH/STAGED_SHA256.txt" "$W/staged.bak"; dup=$(grep "/study/truth/p0020/f8.rds" "$W/staged.bak")
awk -v d="$dup" '/\/study\/truth\/p0020\/f7\.rds$/ { print d; next } { print }' "$W/staged.bak" > "$RH/STAGED_SHA256.txt"; echo tampered > "$ST/truth/p0020/f7.rds"
rc=$(unlock); res "R7D-2: staging list with a DUPLICATE line hiding an omitted, CHANGED truth file: FAILS (exit 1), duplicates reported" 1 "$rc" $(grep -q "duplicates=1" "$W/out.txt" && grep -q "^WAVE_UNLOCK_FAILED" "$W/out.txt" && echo 0 || echo 1)
cp "$W/f7.bak" "$ST/truth/p0020/f7.rds"; mv "$W/staged.bak" "$RH/STAGED_SHA256.txt"
echo extra > "$ST/truth/p0020/f601.rds"; mv "$ST/truth/p0020/f600.rds" "$W/f600.bak"
rc=$(unlock); res "R7D-2: an unlisted file present and a listed file absent (counts still 1,200): FAILS (exit 1), path sets differ" 1 "$rc" $(grep -q "does not cover each truth file" "$W/out.txt" && echo 0 || echo 1)
rm -f "$ST/truth/p0020/f601.rds"; mv "$W/f600.bak" "$ST/truth/p0020/f600.rds"
rc=$(unlock); res "after restoring, never-locked unlock VERIFIES again (exit 0)" 0 "$rc"
( cd "$ST/truth" && find . -type f -print0 | sort -z | xargs -0 sha256sum ) > "$W/pre/pre_truth.sha"
rc=$(unlock); res "only ONE pre-lock list present (inconsistent evidence): FAILS (exit 1, DIFFERENT), not treated as never locked" 1 "$rc" $(grep -q "SHA256_AGAINST_PRELOCK DIFFERENT" "$W/out.txt" && ! grep -q LOCK_NEVER_RAN "$W/out.txt" && echo 0 || echo 1)
( cd "$ST/dev/truth" && find . -type f -print0 | sort -z | xargs -0 sha256sum ) > "$W/pre/pre_devtruth.sha"
rc=$(unlock); res "both pre-lock lists present and equal (the lock ran): VERIFIED, exit 0, sha=equal (unchanged path)" 0 "$rc" $(grep -q "^WAVE_UNLOCK_VERIFIED .*sha=equal" "$W/out.txt" && echo 0 || echo 1)
echo tampered > "$ST/truth/p0030/f9.rds"
rc=$(unlock); res "both pre-lock lists present, a file changed after the lock: FAILS (exit 1, DIFFERENT; unchanged path)" 1 "$rc" $(grep -q "SHA256_AGAINST_PRELOCK DIFFERENT" "$W/out.txt" && echo 0 || echo 1)
echo; echo "test_unlock_never_locked: $((N - FAIL)) passed, $FAIL failed"
[ "$FAIL" = 0 ]
