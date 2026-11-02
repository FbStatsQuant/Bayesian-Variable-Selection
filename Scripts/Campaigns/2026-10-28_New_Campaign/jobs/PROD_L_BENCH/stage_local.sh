#!/bin/bash
# Construct the isolated benchmark stage without copying truth or development data.
set -euo pipefail
HERE=$(cd "$(dirname "$0")" && pwd)
CODE=$(cd "$HERE/../../code" && pwd)
SEALED= STAMP= OUT=
while (($#)); do
  case "$1" in
    --sealed) SEALED=${2:?}; shift 2;;
    --stamp) STAMP=${2:?}; shift 2;;
    --out) OUT=${2:?}; shift 2;;
    *) echo "unknown argument: $1" >&2; exit 2;;
  esac
done
[[ -n $SEALED && -n $OUT && $STAMP =~ ^[0-9]{8}T[0-9]{4}Z$ ]] || exit 2
if command -v cygpath >/dev/null 2>&1; then SEALED=$(cygpath -u "$SEALED"); OUT=$(cygpath -u "$OUT"); fi
manifest="$CODE/bench_v2/lowp_port/BENCH_LOWP_MANIFEST_SHA256_r2.txt"
[ -r "$SEALED/manifests/inputs_manifest_lowp.csv" ] && [ -d "$SEALED/inputs" ] && [ -r "$manifest" ] || exit 3
[ "$(find "$SEALED/inputs" -type f | wc -l)" -eq 1200 ] || { echo "expected 1200 inputs" >&2; exit 3; }
mkdir -p "$OUT"
[ ! -e "$OUT/stage" ] && [ ! -e "$OUT/prodLB_bundle_$STAMP.tar" ] || { echo "stage or archive already exists" >&2; exit 3; }
PID="${STAMP}_lowp_bench"; S="$OUT/stage"; R="$S/runs/$PID"
mkdir -p "$R/code" "$R/study/manifests" "$R/study/inputs"
cp -R "$CODE/bench_lowp" "$R/code/bench_lowp"
# The r2 manifest lists paths without "./"; the reused frozen_check.sh compares against `find .` paths. Stage a normalized copy (same hashes,
# "./"-prefixed paths) and prove it is the r2 manifest up to that prefix: identical (hash, path) pairs, same count.
sed -E 's#^([0-9a-fA-F]{64}) [ *](\./)?#\1  ./#' "$manifest" > "$R/code/bench_lowp.SHA256SUMS"
orig_pairs=$(sed -E 's#^([0-9a-fA-F]{64}) [ *](\./)?#\1 #' "$manifest" | LC_ALL=C sort)
norm_pairs=$(sed -E 's#^([0-9a-fA-F]{64})  \./#\1 #' "$R/code/bench_lowp.SHA256SUMS" | LC_ALL=C sort)
[ "$orig_pairs" = "$norm_pairs" ] && [ "$(grep -c . "$manifest")" = "$(grep -c . "$R/code/bench_lowp.SHA256SUMS")" ] || { echo "normalized manifest differs from r2" >&2; exit 4; }
cp "$manifest" "$R/code/bench_lowp.r2_manifest_original.txt"     # the r2 manifest as frozen (sha256 85a18248...a6b7), for the record
cp -R "$HERE" "$R/code/prod_l_bench"
for excluded in tests review fixtures __pycache__ PROGRESS.md BUILD_NOTES.md BUILD_NOTES_A.md BUILD_NOTES_B.md; do rm -rf -- "$R/code/prod_l_bench/$excluded"; done
find "$R/code/prod_l_bench" -type d -name __pycache__ -prune -exec rm -rf -- {} +
cp "$SEALED/manifests/inputs_manifest_lowp.csv" "$R/study/manifests/"
cp -R "$SEALED/inputs/." "$R/study/inputs/"
source "$HERE/frozen_check.sh"
pilot_check_frozen "$R/code/bench_lowp" "$R/code/bench_lowp.SHA256SUMS" || exit 4
[ "$(sha256sum "$R/code/bench_lowp.r2_manifest_original.txt" | cut -d' ' -f1)" = 85a182488450e04ac960810b0c496e05e2c951aebf0b85dd9cff34f2bd07a6b7 ] || { echo "r2 manifest hash is not 85a18248...a6b7" >&2; exit 4; }
bad=$(find "$R" \( -ipath '*truth*' -o -ipath '*holdout*' -o -iname dev \) -print)
[ -z "$bad" ] || { echo "forbidden staged path: $bad" >&2; exit 4; }
printf 'lowp_bench %s staged %s from %s\n' "$STAMP" "$(date -u +%FT%TZ)" "$(hostname)" > "$R/OWNER"
(cd "$S" && find . -type f ! -name STAGED_SHA256.txt ! -name bench.env -print0 | LC_ALL=C sort -z | xargs -0 sha256sum > "runs/$PID/STAGED_SHA256.txt")
n_files=$(wc -l < "$R/STAGED_SHA256.txt")
staged_kb=$(du -sk "$R" | cut -f1)
tar -cf "$OUT/prodLB_bundle_$STAMP.tar" -C "$S" .
(cd "$OUT" && sha256sum "prodLB_bundle_$STAMP.tar" > "prodLB_bundle_$STAMP.tar.sha256")
rm -rf -- "$S"      # the tar is the archive; no second expanded copy is kept
echo "staged footprint: $staged_kb KB; $n_files files plus hash list; no truth/holdout/dev"
echo "bundle: $OUT/prodLB_bundle_$STAMP.tar"
