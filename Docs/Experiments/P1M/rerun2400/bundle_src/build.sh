#!/usr/bin/env bash
# build.sh STAGE_DIR -- builds the rerun2400 bundle on Owls (repo is read only: git archive / git show / git ls-tree, no git state changed).
#   OLD = Scripts/Campaigns/2026-10-28_New_Campaign/code/core/v2_2_1 (+ its manifest), copied unchanged (manifest-checked);
#   NEW = git tree 8ff2d876c6a5667edfeeebd00305f02388b736fd (= Scripts/SMC_BVS/core of origin/core/v3.1-listpip 8bd779be), by git archive;
#   gen = Scripts/Data_generators/{gen_dev_data,gen_prod_data}.R; runner/analysis = this folder; tables from units.tsv.
set -euo pipefail
SRC=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd); REPO=/home/fb31/Bayesian-Variable-Selection
B=$1; [ ! -e "$B" ] || { echo "refuse: $B exists" >&2; exit 2; }
TREE=8ff2d876c6a5667edfeeebd00305f02388b736fd
OLDSRC=$REPO/Scripts/Campaigns/2026-10-28_New_Campaign/code/core
mkdir -p "$B"/{old,new/core,gen,runner,tables,analysis,smoke}
# OLD: unchanged copy, verified against its own manifest
( cd "$OLDSRC/v2_2_1" && tar cf - --exclude=.cpp_cache . ) | ( cd "$B/old" && tar xf - )
cp "$OLDSRC/v2_2_1.SHA256SUMS" "$B/old.SHA256SUMS"
source "$SRC/frozen_check.sh"; nc_check_frozen "$B/old" "$B/old.SHA256SUMS" || { echo "OLD tree check failed" >&2; exit 3; }
# NEW: git archive of the tree object, verified blob by blob against the tree
git -C "$REPO" cat-file -e "$TREE^{tree}"
git -C "$REPO" archive "$TREE" | tar x -C "$B/new/core"
n=0; while read -r mode type blob path; do
  [ "$(git -C "$REPO" hash-object "$B/new/core/$path")" = "$blob" ] || { echo "NEW blob mismatch: $path" >&2; exit 3; }; n=$((n+1))
done < <(git -C "$REPO" ls-tree -r "$TREE")
[ "$n" = "$(find "$B/new/core" -type f | wc -l)" ] || { echo "NEW file count differs from the tree" >&2; exit 3; }
( cd "$B/new" && find ./core -type f | LC_ALL=C sort | xargs sha256sum -b > ../new.SHA256SUMS )
nc_check_frozen "$B/new" "$B/new.SHA256SUMS" || { echo "NEW tree check failed" >&2; exit 3; }
{ echo "NEW core = git tree $TREE (Scripts/SMC_BVS/core)"; echo "origin/core/v3.1-listpip head: $(git -C "$REPO" rev-parse origin/core/v3.1-listpip)"
  echo "tree of that head's Scripts/SMC_BVS/core: $(git -C "$REPO" rev-parse origin/core/v3.1-listpip:Scripts/SMC_BVS/core)"
  echo "files verified blob by blob (git hash-object): $n"; } > "$B/NEW_PROVENANCE.txt"
# generator (same bytes as the v3.1 branch's copy, checked)
for f in gen_dev_data.R gen_prod_data.R; do
  cp "$REPO/Scripts/Data_generators/$f" "$B/gen/$f"
  [ "$(git -C "$REPO" hash-object "$B/gen/$f")" = "$(git -C "$REPO" rev-parse origin/core/v3.1-listpip:Scripts/Data_generators/$f)" ] || echo "NOTE: $f differs from the v3.1 branch copy" >> "$B/gen/NOTES.txt"
done
# runner / analysis / tables
for f in env.sh frozen_check.sh precompile.R precompile.sbatch common_gen.R gen_inputs.R new_fit.R task.sh submit.sh; do cp "$SRC/$f" "$B/runner/"; done
for f in comparator.R test_comparator.R collect.sh; do cp "$SRC/$f" "$B/analysis/"; done
cp "$SRC/smoke.sh" "$B/smoke/"; cp "$SRC/README_bundle.md" "$B/README.md"
git -C "$REPO" show origin/core/v3.1-listpip:Scripts/SMC_BVS/nots_runner/tables_production/units.tsv > "$B/tables/units.tsv"
cmp "$B/tables/units.tsv" "$REPO/Scripts/SMC_BVS/nots_runner/tables_production/units.tsv" 2>/dev/null || echo "NOTE: working-tree units.tsv differs from the branch copy" >> "$B/tables/NOTES.txt"
python3 "$SRC/make_tables.py" "$B/tables/units.tsv" "$B/tables"
chmod +x "$B"/runner/*.sh "$B"/runner/precompile.sbatch "$B"/analysis/collect.sh "$B"/smoke/smoke.sh
( cd "$B" && find . -type f ! -name SHA256SUMS | LC_ALL=C sort | xargs sha256sum -b > SHA256SUMS && sha256sum --quiet -c SHA256SUMS )
echo "bundle $B built; SHA256SUMS sha256 $(sha256sum "$B/SHA256SUMS" | cut -d' ' -f1); files $(wc -l < "$B/SHA256SUMS")"
