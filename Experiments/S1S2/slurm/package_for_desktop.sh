#!/usr/bin/env bash
# package_for_desktop.sh -- run on OWLS after a VERIFIED pull. Builds ONE flat desktop-offload unit per batch:
#   ROOT/_local/engineering/records/S1S2_smcbvs_b<K>/{S1_01.tar, ..., S1_16.tar, SHA256SUMS}
# (only tars plus one SHA256SUMS; no nested SHA256SUMS anywhere -- the desktop extractor treats every SHA256SUMS as a
# unit). Each S1_xx.tar holds smcbvs/S1_xx/rep_RRR.{json,rds} of the batch's reps plus smcbvs/S1_xx/FILES_b<K>.sha256
# (per-file sums, a plain list, not named SHA256SUMS).
#   package_for_desktop.sh --batch K --reps LO-HI --manifest <pull manifest> [--src DIR] [--records DIR] [--dry-run]
#                          [--unit-tag b1r --select FILE]
#                          [--suite 1|2] [--slurm-tsv FILE]
# S2 (--suite 2): unit S1S2_smcbvs_s2b<K> with S2_001.tar ... S2_120.tar (FILES_s2b<K>.sha256 inside each).
# Benchmarks (--method M, default smcbvs): unit S1S2_<M>_s<suite>b<K> (S1 too: s1b<K>), tars of <M>/S<suite>_xx/...; every
# manifest path packed must lie under <M>/ (the pull manifest of --method M).
# Partition record (--slurm-tsv FILE, written by sacct_record.sh and copied by watch_batch.sh): FILE must have a
# FILE.sha256 next to it (the NOTS sum) that verifies; it is packed as slurm_<tag>.tar = slurm/<basename FILE> +
# slurm/<basename FILE>.sha256, listed in the unit SHA256SUMS like every other tar.
# Supplementary unit (e.g. the reruns of batch 1): --unit-tag b1r names the unit S1S2_smcbvs_b1r (FILES_b1r.sha256 inside)
# and --select FILE (one relative path per line, e.g. smcbvs/S1_16/rep_005.json) packs only those manifest files.
# Every source file is re-hashed and must match the pull manifest (the NOTS sums) before it is packed. The unit is built
# in ROOT/_local/tmp and moved into records/ in one rename (same filesystem), so serve_pull.sh never sees half a unit.
# The desktop pulls hourly at :20 (crews/offload/serve_pull.sh); when it lists the unit in crews/offload/
# desktop_verified.txt, free_nots_scratch.sh may delete the NOTS copy.
set -euo pipefail
ROOT=/home/fb31/Bayesian-Variable-Selection
SRC=$ROOT/_local/engineering/runs/S1S2
REC=$ROOT/_local/engineering/records
batch=""; reps=""; man=""; dry=0; utag=""; sel=""; suite=1; stsv=""; method=smcbvs
while (($#)); do case "$1" in --batch) batch="$2"; shift 2;; --reps) reps="$2"; shift 2;; --manifest) man="$2"; shift 2;;
  --src) SRC="$2"; shift 2;; --records) REC="$2"; shift 2;; --dry-run) dry=1; shift;;
  --unit-tag) utag="$2"; shift 2;; --select) sel="$2"; shift 2;;
  --suite) suite="$2"; shift 2;; --slurm-tsv) stsv="$2"; shift 2;; --method) method="$2"; shift 2;; *) echo "unknown arg $1" >&2; exit 64;; esac; done
[[ "$batch" =~ ^[0-9]+$ && "$reps" =~ ^([0-9]+)-([0-9]+)$ && -f "$man" ]] || { echo "usage: --batch K --reps LO-HI --manifest FILE" >&2; exit 64; }
lo=${BASH_REMATCH[1]}; hi=${BASH_REMATCH[2]}
[[ "$suite" == 1 || "$suite" == 2 ]] || { echo "--suite must be 1 or 2" >&2; exit 64; }
[[ "$method" =~ ^[a-z0-9_]+$ ]] || { echo "bad --method" >&2; exit 64; }
if [[ "$method" != smcbvs ]]; then utag=${utag:-s${suite}b$batch}; [[ "$utag" =~ ^s${suite}b[0-9]+[a-z0-9]*$ ]] || { echo "bad --unit-tag (benchmarks: s<suite>b<K>...)" >&2; exit 64; }
elif [[ $suite == 1 ]]; then utag=${utag:-b$batch}; [[ "$utag" =~ ^b[0-9]+[a-z0-9]*$ ]] || { echo "bad --unit-tag" >&2; exit 64; }
else utag=${utag:-s2b$batch}; [[ "$utag" =~ ^s2b[0-9]+[a-z0-9]*$ ]] || { echo "bad --unit-tag (S2: s2b<K>...)" >&2; exit 64; }; fi
if [[ -n "$stsv" ]]; then [[ -s "$stsv" && -s "$stsv.sha256" ]] || { echo "--slurm-tsv: file or its .sha256 missing" >&2; exit 64; }
  ( cd "$(dirname "$stsv")" && sha256sum --quiet -c "$(basename "$stsv").sha256" ) || { echo "--slurm-tsv: sha256 mismatch" >&2; exit 1; }; fi
[[ -z "$sel" || -s "$sel" ]] || { echo "--select: empty or missing file" >&2; exit 64; }
unit=S1S2_${method}_${utag}
[[ ! -e "$REC/$unit" ]] || { echo "refusing: $REC/$unit exists" >&2; exit 65; }
stage=$ROOT/_local/tmp/$(date +%Y%m%d)-opusN-pkg-$unit; rm -rf "$stage"; mkdir -p "$stage/$unit"; trap 'rm -rf "$stage"' EXIT
# files of the batch, as listed (and hashed) by the pull manifest
awk -v lo="$lo" -v hi="$hi" -v pre="S${suite}_" '{ f = substr($0, 67); if (index(f, "/" pre) && match(f, /rep_[0-9]+\./)) { r = substr(f, RSTART + 4, RLENGTH - 5) + 0; if (r >= lo && r <= hi) print } }' "$man" > "$stage/batch.sha256"
if [[ "$method" != smcbvs ]] && awk -v m="$method/" 'index(substr($0, 67), m) != 1 { bad = 1 } END { exit !bad }' "$stage/batch.sha256"; then
  echo "refusing: manifest paths outside $method/ (use the pull manifest of --method $method)" >&2; exit 65; fi
if [[ -n "$sel" ]]; then awk 'NR == FNR { want[$0] = 1; next } (substr($0, 67) in want)' "$sel" "$stage/batch.sha256" > "$stage/sel.sha256"
  [[ $(wc -l < "$stage/sel.sha256") -eq $(grep -c . "$sel") ]] || { echo "--select: some paths are not in the manifest" >&2; exit 65; }
  mv "$stage/sel.sha256" "$stage/batch.sha256"; fi
nf=$(wc -l < "$stage/batch.sha256"); (( nf > 0 )) || { echo "no files of reps $lo-$hi in $man" >&2; exit 65; }
( cd "$SRC" && sha256sum --quiet -c "$stage/batch.sha256" ) || { echo "FAILED: Owls copies do not match the pull manifest" >&2; exit 1; }
echo "verified $nf source files against $man"
for sd in $(cut -c67- "$stage/batch.sha256" | xargs -n1 dirname | sort -u); do        # e.g. smcbvs/S1_03
  s=$(basename "$sd")
  grep -F "  $sd/" "$stage/batch.sha256" | sed "s#  $sd/#  #" > "$stage/FILES_${utag}_$s.sha256"
  { grep -F "  $sd/" "$stage/batch.sha256" | cut -c67-; } > "$stage/list_$s"
  mkdir -p "$stage/tree/$sd"; cp "$stage/FILES_${utag}_$s.sha256" "$stage/tree/$sd/FILES_${utag}.sha256"
  tar -cf "$stage/$unit/$s.tar" -C "$SRC" -T "$stage/list_$s" -C "$stage/tree" "$sd/FILES_${utag}.sha256"
  [[ $(tar -tf "$stage/$unit/$s.tar" | wc -l) -eq $(( $(wc -l < "$stage/list_$s") + 1 )) ]] || { echo "tar count mismatch $s" >&2; exit 1; }
done
if [[ -n "$stsv" ]]; then b=$(basename "$stsv"); mkdir -p "$stage/slurm/slurm"; cp "$stsv" "$stsv.sha256" "$stage/slurm/slurm/"
  tar -cf "$stage/$unit/slurm_${utag}.tar" -C "$stage/slurm" "slurm/$b" "slurm/$b.sha256"; echo "partition record: slurm_${utag}.tar ($b)"; fi
( cd "$stage/$unit" && sha256sum -- *.tar > SHA256SUMS && sha256sum --quiet -c SHA256SUMS )
[[ $(find "$stage/$unit" -name SHA256SUMS | wc -l) -eq 1 && -z $(find "$stage/$unit" -mindepth 1 -type d) ]] || { echo "unit not flat" >&2; exit 1; }
echo "unit $unit: $(ls "$stage/$unit" | wc -l) entries, $(du -sh "$stage/$unit" | cut -f1)"
if ((dry)); then ls -la "$stage/$unit"; echo "[dry-run] not moved into $REC"; exit 0; fi
mkdir -p "$REC"; mv "$stage/$unit" "$REC/$unit"
echo "PACKAGED: $REC/$unit (desktop pulls hourly at :20; then check crews/offload/desktop_verified.txt for '$unit')"
