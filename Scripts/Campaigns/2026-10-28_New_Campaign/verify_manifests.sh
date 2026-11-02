#!/bin/sh
# verify_manifests.sh -- re-check every New Campaign manifest at its repo path.
# Run from the REPO ROOT (the folder that contains Scripts/). POSIX sh + GNU coreutils (sha256sum, sed, awk, tr).
# Prints one PASS / FAIL line per manifest and a final SUMMARY line. Exit code 0 only if nothing FAILs.
#
# EXPECTED_MISMATCHES.tsv (next to this script, or $EXPECTED): lines "<manifest id><TAB><path as written in the manifest>".
# Those entries are documented supersessions (a later ledger entry changed the file) and are tolerated; any other
# mismatch or missing file is a FAIL.

C="Scripts/Campaigns/2026-10-28_New_Campaign"
HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
EXPECTED="${EXPECTED:-$HERE/EXPECTED_MISMATCHES.tsv}"
TAB=$(printf '\t')
NPASS=0; NFAIL=0
WORK=$(mktemp -d 2>/dev/null || echo "${TMPDIR:-/tmp}/vm.$$"); mkdir -p "$WORK"
trap 'rm -rf "$WORK"' EXIT INT TERM

sha_of() { sha256sum "$1" 2>/dev/null | cut -d' ' -f1; }
is_expected() { [ -f "$EXPECTED" ] && awk -F'\t' -v i="$1" -v p="$2" '$1==i && $2==p {f=1} END{exit !f}' "$EXPECTED"; }

# normalise a sha256sum-style file ("hash  path", "hash *path", optional ./ prefix, optional CRLF) to "hash<TAB>path"
norm_sums() { tr -d '\r' | sed -n 's/^\([0-9a-fA-F]\{64\}\) [ *]\(.*\)$/\1\t\2/p' | sed 's#\t\./#\t#' | awk -F'\t' 'BEGIN{OFS="\t"}{$1=tolower($1);print}'; }

report() { # status id detail
  if [ "$1" = PASS ]; then NPASS=$((NPASS+1)); else NFAIL=$((NFAIL+1)); fi
  printf '%s  %s  %s\n' "$1" "$2" "$3"
}

# check_list ID BASEDIR LISTFILE(hash<TAB>path) [HEADLINE_FILE HEADLINE_HASH_OR_PREFIX]
check_list() {
  id=$1; base=$2; list=$3; hfile=$4; hexp=$5
  ok=0; exp=0; bad=0; tot=0; detail=""
  : > "$WORK/unexp.txt"
  while IFS="$TAB" read -r h p; do
    [ -n "$h" ] || continue
    tot=$((tot+1))
    f="$base/$p"
    if [ -f "$f" ]; then a=$(sha_of "$f"); else a=MISSING; fi
    if [ "$a" = "$h" ]; then ok=$((ok+1))
    elif is_expected "$id" "$p"; then exp=$((exp+1))
    else bad=$((bad+1)); echo "    UNEXPECTED $a (manifest says $h)  $p" >> "$WORK/unexp.txt"; fi
  done < "$list"
  hnote=""
  hfail=0
  if [ -n "$hfile" ] && [ -n "$hexp" ]; then
    hs=$(sha_of "$hfile")
    case "$hs" in "$hexp"*) hnote="; manifest sha256 ${hs%"${hs#????????}"}.. = ledger headline" ;; *) hfail=1; hnote="; MANIFEST SHA256 ${hs} != ledger headline ${hexp}" ;; esac
  fi
  if [ "$tot" -eq 0 ]; then report FAIL "$id" "no entries parsed (is the manifest present at $hfile?)"; return; fi
  if [ "$bad" -eq 0 ] && [ "$hfail" -eq 0 ]; then
    report PASS "$id" "$ok/$tot files OK$( [ "$exp" -gt 0 ] && echo ", $exp documented-superseded")$hnote"
  else
    report FAIL "$id" "$ok/$tot OK, $exp documented-superseded, $bad UNEXPECTED$hnote"
    cat "$WORK/unexp.txt"
  fi
}

# check_manifest ID BASEDIR MANIFESTFILE [HEADLINE]
check_manifest() {
  [ -f "$3" ] || { report FAIL "$1" "manifest file not found: $3"; return; }
  norm_sums < "$3" > "$WORK/list.tsv"
  check_list "$1" "$2" "$WORK/list.tsv" "$3" "$4"
}

# the first fenced ```text block after the first line matching REGEX in the ledger
ledger_block() { # regex
  awk -v re="$1" '$0 ~ re {s=1} s && /^```text/ {b=1; next} b && /^```/ {exit} b' "$C/code/CODE_LEDGER.md"
}
check_ledger_block() { # ID BASEDIR REGEX
  [ -f "$C/code/CODE_LEDGER.md" ] || { report FAIL "$1" "CODE_LEDGER.md not found"; return; }
  ledger_block "$3" | norm_sums > "$WORK/list.tsv"
  check_list "$1" "$2" "$WORK/list.tsv"
}

K="$C/code/core"; BV="$C/code/bench_v2"; BL="$C/code/bench_lowp"; BA="$C/bench_audit/jobs"; PH="$C/conformance/jobs/PROD_H"

# ---- run-time manifests (authoritative) ----
check_manifest "v2_2_1.SHA256SUMS" "$K/v2_2_1" "$K/v2_2_1.SHA256SUMS" d880afdbd0c1b7836862b5dff01a05168197f044deb757716e9549406f2e13e1
check_manifest "v2_2.SHA256SUMS" "$K/v2_2" "$K/v2_2.SHA256SUMS"
check_manifest "CONF_NOTS_IDENTITY/v2_2.SHA256SUMS" "$K/v2_2" "$C/conformance/jobs/CONF_NOTS_IDENTITY/v2_2.SHA256SUMS"
check_manifest "PROD_H/BUNDLE_SHA256SUMS" "$PH" "$PH/BUNDLE_SHA256SUMS" 2a2a8b1fd3d5ad72ef51e677cd17a097515333ac96eb3d076efeefc8823ba5f3
check_manifest "PROD_L_BENCH/BUNDLE_SHA256SUMS.txt" "$C/jobs/PROD_L_BENCH" "$C/jobs/PROD_L_BENCH/BUNDLE_SHA256SUMS.txt" 2a7ceba7
check_manifest "BENCH_F3_PROD/BUNDLE_SHA256SUMS_FINAL" "$BA/BENCH_F3_PROD" "$BA/BENCH_F3_PROD/BUNDLE_SHA256SUMS_FINAL" 90579ad6a592916f2a87e5be614a468901884610421ab0c4809ae86666875e07
check_manifest "BENCH_F3_DEV/BUNDLE_SHA256SUMS_FINAL" "$BA/BENCH_F3_DEV" "$BA/BENCH_F3_DEV/BUNDLE_SHA256SUMS_FINAL" 3353b6f667737e225873bc6b97346c80d7c5b321fd6851983f97ec2e94b964ed
check_manifest "bench_v2/MANIFEST_SHA256.txt" "$BV" "$BV/MANIFEST_SHA256.txt" 8905f52e314f706b54f985994d7915052301c9e22912690264b7b27ab58b0373
check_manifest "lowp_port/BENCH_LOWP_MANIFEST_SHA256_r2.txt" "$BL" "$BV/lowp_port/BENCH_LOWP_MANIFEST_SHA256_r2.txt" 85a182488450e04ac960810b0c496e05e2c951aebf0b85dd9cff34f2bd07a6b7
check_manifest "lowp/enum/vendor/VENDOR_SHA256.txt" "$C/code/lowp/enum/vendor" "$C/code/lowp/enum/vendor/VENDOR_SHA256.txt"
check_manifest "staging/20261102T1252Z_bench_f3v2_prod/UPLOAD_SHA256.txt" "$BA/staging/20261102T1252Z_bench_f3v2_prod" "$BA/staging/20261102T1252Z_bench_f3v2_prod/UPLOAD_SHA256.txt"
check_manifest "staging/20261030T1855Z_bench_f3v2_dev/UPLOAD_SHA256.txt" "$BA/staging/20261030T1855Z_bench_f3v2_dev" "$BA/staging/20261030T1855Z_bench_f3v2_dev/UPLOAD_SHA256.txt"

# ---- ledger blocks ----
check_ledger_block "CODE_LEDGER rev-7d block (2026-10-30)" "$C/code" 'Changed files .sha256.:'
check_ledger_block "CODE_LEDGER LOWP block (2026-10-29)" "$C/code" '^## 2026-10-29 .* LOWP'
# the block under the v2.2 heading is the v2.1 PRODUCTION BASELINE; v2_1_baseline/ is NOT copied: it is checked against the repo's own Scripts/SMC_BVS
if [ -d Scripts/SMC_BVS ]; then
  check_ledger_block "CODE_LEDGER v2.1-baseline block (2026-10-28)" "Scripts/SMC_BVS" '^## 2026-10-28 .* v2.2 core'
else
  report FAIL "CODE_LEDGER v2.1-baseline block (2026-10-28)" "Scripts/SMC_BVS not found (run from the repo root)"
fi

# ---- other records ----
if [ -f "$BV/lowp_port/BENCH_LOWP_MANIFEST_SHA256.txt" ]; then
  norm_sums < "$BV/lowp_port/BENCH_LOWP_MANIFEST_SHA256.txt" > "$WORK/list.tsv"
  check_list "lowp_port/BENCH_LOWP_MANIFEST_SHA256.txt (first)" "$BL" "$WORK/list.tsv" "$BV/lowp_port/BENCH_LOWP_MANIFEST_SHA256.txt" 288e0f8c
fi
if [ -f "$BV/lowp_port/TEST_CODE_SHA256.txt" ]; then
  norm_sums < "$BV/lowp_port/TEST_CODE_SHA256.txt" | grep -v "$TAB\.\./" > "$WORK/list.tsv"
  check_list "lowp_port/TEST_CODE_SHA256.txt" "$BV/lowp_port" "$WORK/list.tsv"
fi
if [ -f "$BV/BASELINE_SHA256.txt" ]; then   # "file | deployed | v2 | identical": the v2 column is the current bench_v2 file
  awk -F' [|] ' 'NF==4 && length($3)==64 {printf "%s\t%s\n", $3, $1}' "$BV/BASELINE_SHA256.txt" > "$WORK/list.tsv"
  check_list "bench_v2/BASELINE_SHA256.txt (v2 column)" "$BV" "$WORK/list.tsv"
fi
if [ -f "$BL/R/SOURCES_SHA256.txt" ]; then   # provenance record; historical rows are expected mismatches
  tr -d '\r' < "$BL/R/SOURCES_SHA256.txt" | sed -n 's/^\([0-9A-Fa-f]\{64\}\)  \(R[\\/][^ ]*\).*$/\1\t\2/p' | tr '\\' '/' | awk -F'\t' 'BEGIN{OFS="\t"}{$1=tolower($1);print}' > "$WORK/list.tsv"
  check_list "bench_lowp/R/SOURCES_SHA256.txt" "$BL" "$WORK/list.tsv"
fi

# ---- freeze.json (BENCH_F3 bundles): manifest digest and the runner source-tree digest ----
FJ="$BA/BENCH_F3_PROD/runner/freeze.json"
if [ -f "$FJ" ]; then
  mdig=$(sed -n 's/.*"manifest_sha256"[^"]*"\([0-9a-f]\{64\}\)".*/\1/p' "$FJ")
  sdig=$(sed -n 's/.*"source_sha256"[^"]*"\([0-9a-f]\{64\}\)".*/\1/p' "$FJ")
  amd=$(sha_of "$BV/MANIFEST_SHA256.txt")
  txt=$(for f in config.R common.R methods/glmnet_helpers.R methods/fit_F3_alasso.R run_case.R; do printf '%s  %s\n' "$f" "$(sha_of "$BV/F3_AdaptiveLasso/$f")"; done)
  asd=$(printf '%s' "$txt" | sha256sum | cut -d' ' -f1)
  if [ "$mdig" = "$amd" ] && [ "$sdig" = "$asd" ]; then report PASS "freeze.json" "manifest_sha256 = bench_v2/MANIFEST_SHA256.txt; source_sha256 = run_case.R CODE_FILES digest"
  else report FAIL "freeze.json" "manifest_sha256 frozen=$mdig actual=$amd; source_sha256 frozen=$sdig actual=$asd"; fi
else
  report FAIL "freeze.json" "not found"
fi

# ---- headline hashes of single files recorded in CODE_LEDGER ----
hl() { # id file expected-prefix
  if [ -f "$2" ]; then a=$(sha_of "$2"); case "$a" in "$3"*) report PASS "$1" "sha256 ${a%"${a#????????}"}.. matches CODE_LEDGER";; *) report FAIL "$1" "sha256 $a != ledger $3";; esac
  else report FAIL "$1" "not found: $2"; fi
}
hl "v2_2_1.diff" "$K/v2_2_1.diff" fabce9fac9d4ac19e7c610a06221e443b44521892de847b6ca49032ab1eab42a
hl "v2_2.diff" "$K/v2_2.diff" 5d7ce9cd4809a1dcae499637de2c0cba9c241c4b8602ab2bf0d1a82fb517bc04
hl "CONF_NOTS_IDENTITY/cmp2.R (D20 amended)" "$C/conformance/jobs/CONF_NOTS_IDENTITY/cmp2.R" f2662113babc300d102957f0d79920a97ba75383fe4ef80b38eeaabaebefa048

printf 'SUMMARY: %d PASS, %d FAIL\n' "$NPASS" "$NFAIL"
[ "$NFAIL" -eq 0 ]
