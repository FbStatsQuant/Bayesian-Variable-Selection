#!/bin/bash
# stage_local.sh -- LAPTOP side (Git Bash). Assemble the pilot bundle as one tar whose ONLY top-level entry is runs/<STAMP>_lowp_pilot (paths relative to
# /home/fb31/projects/BVS/New_Campaign), with a sha256 list that NOTS re-checks (STAGED_SHA256.txt) and an OWNER marker. Everything the pilot stages is
# inside that folder, so nothing shared (code/, inputs/, manifests/) is overwritten and the clean-up removes exactly one pilot-owned folder.
#   bash stage_local.sh --sealed <sealed study root> --stamp YYYYMMDDTHHMMZ --out <empty durable run folder>
#
#   <sealed study root> = the folder produced by `Rscript code/lowp/R/lowp_seal.R <root>`: manifests/, inputs/, truth/, dev/{inputs,truth,manifests}/.
#   --out should be the DURABLE local run folder (e.g. C:\...\NOTS Data\New_Campaign\runs\<STAMP>_lowp_pilot\bundle): the tar and its hash stay there
#   as the source archive of this pilot.
#   Staged (nothing else): code/core/v2_2_1/{core,study,tools,CHANGES_v2_2_1.md} + code/core/v2_2_1.SHA256SUMS (no .cpp_cache; verified against the manifest), code/lowp/{R,enum (no tests),pilot,tests/test_truth_lock_linux.sh}, code/bench_lowp
#   (no smoke), inputs/lowp_dev/{inputs,manifests} (dev inputs; NO truth there), and study/ = a COPY of the sealed study for P0 and the truth-lock test:
#   manifests/, dev/manifests/, truth/ (all 1,200), dev/truth/ (all 60), inputs/ (only the 6 pilot datasets).
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
CODE="$(cd "$HERE/../.." && pwd)"                                   # .../code
SEALED=""; STAMP=""; OUT=""
while [ $# -gt 0 ]; do case "$1" in --sealed) SEALED=$2; shift 2;; --stamp) STAMP=$2; shift 2;; --out) OUT=$2; shift 2;; *) echo "unknown $1" >&2; exit 2;; esac; done
[ -n "$SEALED" ] && [ -n "$STAMP" ] && [ -n "$OUT" ] || { echo "usage: stage_local.sh --sealed DIR --stamp STAMP --out DIR" >&2; exit 2; }
[[ "$STAMP" =~ ^[0-9]{8}T[0-9]{4}Z$ ]] || { echo "bad STAMP" >&2; exit 2; }
PID="${STAMP}_lowp_pilot"
need() { [ -e "$1" ] || { echo "missing: $1" >&2; exit 3; }; }
need "$SEALED/manifests/inputs_manifest_lowp.csv"; need "$SEALED/manifests/truth_manifest_lowp.csv"
need "$SEALED/dev/manifests/inputs_manifest_lowp.csv"; need "$SEALED/dev/manifests/truth_manifest_lowp.csv"
n_dev=$(find "$SEALED/dev/inputs" -name 'dev_p00*_S?_r???.rds' | wc -l); [ "$n_dev" -eq 60 ] || { echo "expected 60 dev inputs, found $n_dev" >&2; exit 3; }
IDENT="p0020_S1_r001 p0020_S4_r050 p0020_S6_r100 p0030_S1_r001 p0030_S4_r050 p0030_S6_r100"
for id in $IDENT; do need "$SEALED/inputs/${id:0:5}/$id.rds"; done
for d in core/v2_2_1/core core/v2_2_1/study core/v2_2_1/tools core/v2_2_1/CHANGES_v2_2_1.md core/v2_2_1.SHA256SUMS lowp/R lowp/enum lowp/enum/exact_contract.R lowp/pilot lowp/tests/test_truth_lock_linux.sh bench_lowp; do need "$CODE/$d"; done
mkdir -p "$OUT"
[ ! -e "$OUT/stage" ] && [ ! -e "$OUT/pilot_bundle_$STAMP.tar" ] || { echo "$OUT already holds a stage or bundle; use an empty dir" >&2; exit 3; }
S="$OUT/stage"; R="$S/runs/$PID"
mkdir -p "$R/code/core" "$R/code/lowp/tests" "$R/inputs/lowp_dev" "$R/study/inputs" "$R/study/dev"

cp -R "$CODE/core/v2_2_1" "$R/code/core/v2_2_1"; cp "$CODE/core/v2_2_1.SHA256SUMS" "$R/code/core/v2_2_1.SHA256SUMS"   # the whole frozen v2.2.1 tree + its manifest
cp -R "$CODE/lowp/R" "$R/code/lowp/R"; cp -R "$CODE/lowp/pilot" "$R/code/lowp/pilot"
cp -R "$CODE/lowp/enum" "$R/code/lowp/enum"; rm -rf "$R/code/lowp/enum/tests"
cp -R "$CODE/bench_lowp" "$R/code/bench_lowp"; rm -rf "$R/code/bench_lowp/smoke"
cp "$CODE/lowp/tests/test_truth_lock_linux.sh" "$R/code/lowp/tests/"
STUDY_COPY="$R/study"
cp -R "$SEALED/manifests" "$STUDY_COPY/manifests"; cp -R "$SEALED/truth" "$STUDY_COPY/truth"
cp -R "$SEALED/dev/manifests" "$STUDY_COPY/dev/manifests"; cp -R "$SEALED/dev/truth" "$STUDY_COPY/dev/truth"
cp -R "$SEALED/dev/inputs" "$R/inputs/lowp_dev/inputs"; cp -R "$SEALED/dev/manifests" "$R/inputs/lowp_dev/manifests"
for id in $IDENT; do p=${id:0:5}; mkdir -p "$STUDY_COPY/inputs/$p"; cp "$SEALED/inputs/$p/$id.rds" "$STUDY_COPY/inputs/$p/"; done
# exclusions and hygiene
find "$S" \( -name '.cpp_cache' -o -name '__pycache__' -o -name '*.pyc' -o -name '.Rhistory' -o -name '.RData' -o -name '*.o' -o -name '*.so' \) -prune -exec rm -rf {} + 2>/dev/null || true
find "$S" \( -name '*.sh' -o -name '*.sbatch' -o -name 'pilot.env' \) | while read -r f; do sed -i 's/\r$//' "$f"; done
# the staged code/core/v2_2_1 must be EXACTLY the frozen v2.2.1 (sha256sum -c against v2_2_1.SHA256SUMS, no unlisted file), after the cache/hygiene removal above
source "$HERE/frozen_check.sh"
pilot_check_frozen "$R/code/core/v2_2_1" "$R/code/core/v2_2_1.SHA256SUMS" || { echo "staged code/core/v2_2_1 does not match v2_2_1.SHA256SUMS (frozen v2.2.1)" >&2; exit 4; }
echo "frozen v2.2.1 tree verified in the stage: $(grep -c . "$R/code/core/v2_2_1.SHA256SUMS") files match v2_2_1.SHA256SUMS"
# truth separation: the only truth folders allowed are inside the study copy
bad=$(find "$S" -type d -iname 'truth*' ! -path "$STUDY_COPY/*" || true)
[ -z "$bad" ] || { echo "truth folder staged outside the study copy: $bad" >&2; exit 4; }
[ ! -e "$R/inputs/lowp_dev/truth" ] && [ "$(find "$STUDY_COPY/truth" -type f | wc -l)" = 1200 ] && [ "$(find "$STUDY_COPY/dev/truth" -type f | wc -l)" = 60 ] || { echo "truth staging wrong (dev truth next to dev inputs, or counts != 1200/60)" >&2; exit 4; }
printf 'lowp_pilot %s staged %s from %s\n' "$STAMP" "$(date -u +%FT%TZ)" "$(hostname)" > "$R/OWNER"
# hash list (pilot.env is excluded: OPS edits it, and submit_pilot.sh saves its final copy with the run logs; paths relative to the New_Campaign root)
( cd "$S" && find . -type f ! -name STAGED_SHA256.txt ! -name pilot.env | LC_ALL=C sort | xargs -d '\n' sha256sum > "runs/$PID/STAGED_SHA256.txt" )
n_files=$(wc -l < "$R/STAGED_SHA256.txt")
tar -cf "$OUT/pilot_bundle_$STAMP.tar" -C "$S" .
( cd "$OUT" && sha256sum "pilot_bundle_$STAMP.tar" > "pilot_bundle_$STAMP.tar.sha256" )
STAGED_KB=$(du -sk "$R" | cut -f1); rm -rf "$S"      # the tar is the archive; do not leave a second copy of the truth next to it
echo "bundle: $OUT/pilot_bundle_$STAMP.tar ($(du -k "$OUT/pilot_bundle_$STAMP.tar" | cut -f1) KB, $n_files files + hash list)"
echo "staged footprint on NOTS (planned home add, disk blocks): ${STAGED_KB} KB (+ compile cache 2 to 5 MB); charter limit for the whole campaign: 512 MB"
echo "NOTS (one connection, through the configured alias):"
echo "  cd /home/fb31/projects/BVS/New_Campaign && test ! -e runs/$PID && tar -xf <path>/pilot_bundle_$STAMP.tar -C . && sha256sum --quiet -c runs/$PID/STAGED_SHA256.txt"
