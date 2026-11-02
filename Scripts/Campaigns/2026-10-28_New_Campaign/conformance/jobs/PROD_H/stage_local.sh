#!/bin/bash
# stage_local.sh -- LAPTOP side (Git Bash). Build the PROD-H upload tar and verify it.
#   bash stage_local.sh --stamp YYYYMMDDTHHMMZ --out <empty folder> [--code-root <.../I_2026-10-28_New_Campaign/code>]
# The tar's top-level entries (paths relative to /home/fb31/projects/BVS/New_Campaign):
#   runs/<STAMP>_prodH/{runner/, tables/{units,chunks}.tsv, JOB.md, OWNER, STAGED_SHA256.txt}
#   code/core/v2_2_1/      the frozen tree (core/, study/, tools/, CHANGES_v2_2_1.md); no .cpp_cache, no caches
#   code/core/v2_2_1.SHA256SUMS   the manifest as it stands in the local code tree NOW (read from disk; no hash is hard-coded)
# Verification (all before the tar is left in place): the staged v2.2.1 tree against the manifest (sha256sum -c, no unlisted file except
# core/.cpp_cache); the tables (1,200 datasets / 2,400 fits, p1000 = tasks 1-600, p500 = 601-1200); bash -n on every script; Python compile of
# every .py; then the finished tar is extracted into a scratch folder and STAGED_SHA256.txt is checked from there.
# Nothing here touches NOTS. Upload and extraction commands are in JOB.md.
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CODE_ROOT="$(cd "$HERE/../../../code" 2>/dev/null && pwd || true)"
STAMP=""; OUT=""
while [ $# -gt 0 ]; do case "$1" in
  --stamp) STAMP=$2; shift 2;; --out) OUT=$2; shift 2;; --code-root) CODE_ROOT=$2; shift 2;; *) echo "unknown option $1" >&2; exit 2;; esac; done
[ -n "$STAMP" ] && [ -n "$OUT" ] || { echo "usage: stage_local.sh --stamp STAMP --out DIR [--code-root DIR]" >&2; exit 2; }
[[ "$STAMP" =~ ^[0-9]{8}T[0-9]{4}Z$ ]] || { echo "bad STAMP (YYYYMMDDTHHMMZ)" >&2; exit 2; }
RUN_ID="${STAMP}_prodH"
# shellcheck disable=SC1091
source "$HERE/runner/frozen_check.sh"
need() { [ -e "$1" ] || { echo "missing: $1" >&2; exit 3; }; }
need "$CODE_ROOT/core/v2_2_1/study/run_case.R"; need "$CODE_ROOT/core/v2_2_1/tools/p5_scan.R"; need "$CODE_ROOT/core/v2_2_1.SHA256SUMS"
need "$HERE/tables/units.tsv"; need "$HERE/tables/chunks.tsv"; need "$HERE/JOB.md"
for f in task.sh p5_task.sh submit.sh p5_submit.sh p5_scan_run.sh rerun.sh final_accounting.sh make_manifests.sh common.sh frozen_check.sh guard_check.sh env.sh \
         precompile.sbatch precompile.R poll.py reconcile.py nc_sched.py accounting_summary.py p5_scan.sbatch cleanup_terminal.sh; do need "$HERE/runner/$f"; done
PY=""; for c in python3 python "py -3"; do if $c -c 'import sys; sys.exit(0 if sys.version_info >= (3, 9) else 1)' >/dev/null 2>&1; then PY=$c; break; fi; done
mkdir -p "$OUT"
[ ! -e "$OUT/stage" ] && [ ! -e "$OUT/prodH_bundle_$STAMP.tar" ] || { echo "$OUT already holds a stage or bundle; use an empty folder" >&2; exit 3; }
S="$OUT/stage"; R="$S/runs/$RUN_ID"
trap 'rm -rf "$S" "$OUT/verify_extract"' EXIT
mkdir -p "$R/runner" "$R/tables" "$S/code/core"
# tables: the combined tables of the 2,400 fits, checked before they are staged
[ "$(grep -c . "$HERE/tables/units.tsv")" = 2401 ] && [ "$(grep -c . "$HERE/tables/chunks.tsv")" = 1201 ] || { echo "tables are not 2,400 units / 1,200 datasets" >&2; exit 4; }
awk -F'\t' 'NR > 1 { n++; if ($3 == 1000) { if ($1 < 1 || $1 > 600) bad++ } else if ($3 == 500) { if ($1 < 601 || $1 > 1200) bad++ } else bad++ } END { exit !(n == 1200 && !bad) }' "$HERE/tables/chunks.tsv" \
  || { echo "chunks.tsv: tasks must be p1000 = 1-600, p500 = 601-1200" >&2; exit 4; }
[ "$(cut -f1 "$HERE/tables/units.tsv" | tail -n +2 | sort -u | wc -l)" = 2400 ] || { echo "units.tsv: case ids are not 2,400 unique" >&2; exit 4; }
cp "$HERE/tables/units.tsv" "$HERE/tables/chunks.tsv" "$R/tables/"
cp "$HERE/JOB.md" "$R/JOB.md"
for f in "$HERE"/runner/*; do case "$f" in *make_tables.py) continue;; esac; [ -f "$f" ] && cp "$f" "$R/runner/"; done   # make_tables.py is laptop-only
cp -R "$CODE_ROOT/core/v2_2_1" "$S/code/core/v2_2_1"; cp "$CODE_ROOT/core/v2_2_1.SHA256SUMS" "$S/code/core/v2_2_1.SHA256SUMS"
find "$S" \( -name '.cpp_cache' -o -name '__pycache__' -o -name '*.pyc' -o -name '.Rhistory' -o -name '.RData' -o -name '*.o' -o -name '*.so' \) -prune -exec rm -rf {} + 2>/dev/null || true
# LF line endings for everything NOTS executes (the frozen tree is NOT touched: its bytes must match the manifest)
find "$R" -type f \( -name '*.sh' -o -name '*.sbatch' -o -name '*.py' -o -name '*.R' -o -name '*.tsv' \) | while read -r f; do sed -i 's/\r$//' "$f"; done
chmod +x "$R"/runner/*.sh "$R"/runner/*.sbatch 2>/dev/null || true
nc_check_frozen "$S/code/core/v2_2_1" "$S/code/core/v2_2_1.SHA256SUMS" || { echo "the staged v2.2.1 tree does not match v2_2_1.SHA256SUMS (frozen)" >&2; exit 4; }
echo "frozen v2.2.1 tree verified in the stage: $(grep -c . "$S/code/core/v2_2_1.SHA256SUMS") files match v2_2_1.SHA256SUMS (manifest sha256 $(sha256sum "$S/code/core/v2_2_1.SHA256SUMS" | cut -c1-16))"
for f in "$R"/runner/*.sh "$R"/runner/*.sbatch; do bash -n "$f" || { echo "syntax error in $f" >&2; exit 4; }; done
if [ -n "$PY" ]; then for f in "$R"/runner/*.py; do $PY -c 'import sys; compile(open(sys.argv[1], encoding="utf-8").read(), sys.argv[1], "exec")' "$f" || { echo "syntax error in $f" >&2; exit 4; }; done
else echo "WARNING: no Python >= 3.9 found: .py files were not syntax-checked" >&2; fi
if grep -rIl $'\r' "$R/runner" >/dev/null 2>&1; then echo "CR characters remain in the runner" >&2; exit 4; fi
printf 'prodH %s staged %s from %s\n' "$STAMP" "$(date -u +%FT%TZ)" "$(hostname)" > "$R/OWNER"
# hash list (paths relative to the New_Campaign root; STAGED_SHA256.txt does not list itself)
( cd "$S" && find . -type f ! -name STAGED_SHA256.txt | LC_ALL=C sort | xargs -d '\n' sha256sum > "runs/$RUN_ID/STAGED_SHA256.txt" )
n_files=$(wc -l < "$R/STAGED_SHA256.txt")
STAGED_KB=$(du -sk "$S" | cut -f1)
tar -cf "$OUT/prodH_bundle_$STAMP.tar" -C "$S" .
( cd "$OUT" && sha256sum "prodH_bundle_$STAMP.tar" > "prodH_bundle_$STAMP.tar.sha256" )
# verify the tar itself: extract into a scratch folder and check it as NOTS will
mkdir "$OUT/verify_extract"; tar -xf "$OUT/prodH_bundle_$STAMP.tar" -C "$OUT/verify_extract"
( cd "$OUT/verify_extract" && sha256sum --quiet -c "runs/$RUN_ID/STAGED_SHA256.txt" ) || { echo "tar verification failed: STAGED_SHA256.txt" >&2; rm -f "$OUT/prodH_bundle_$STAMP.tar"; exit 5; }
nc_check_frozen "$OUT/verify_extract/code/core/v2_2_1" "$OUT/verify_extract/code/core/v2_2_1.SHA256SUMS" || { echo "tar verification failed: frozen tree" >&2; rm -f "$OUT/prodH_bundle_$STAMP.tar"; exit 5; }
[ "$(cd "$OUT/verify_extract" && find . -type f | wc -l)" = "$((n_files + 1))" ] || { echo "tar verification failed: file count" >&2; rm -f "$OUT/prodH_bundle_$STAMP.tar"; exit 5; }
echo "bundle: $OUT/prodH_bundle_$STAMP.tar ($(du -k "$OUT/prodH_bundle_$STAMP.tar" | cut -f1) KB, $n_files files + hash list); verified by extraction"
echo "tar sha256: $(cut -d' ' -f1 "$OUT/prodH_bundle_$STAMP.tar.sha256")"
echo "staged footprint on NOTS (disk blocks): ${STAGED_KB} KB (+ compile cache 2 to 5 MB, + summaries); the submit guard is asked for 30 MB; charter limit for the whole campaign: 512 MB"
echo "RUN_ID: $RUN_ID   -- upload and extract with the commands in JOB.md (section 3)"
