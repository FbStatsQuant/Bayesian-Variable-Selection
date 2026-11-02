#!/usr/bin/env bash
# make_manifests.sh -- OPS, on NOTS, after final_accounting.sh (and cleanup_terminal.sh if a killed attempt left locks/temporary files):
# one sha256 manifest per folder to download, plus one for the small home run-summary folder.
#   bash RUN_DIR/runner/make_manifests.sh
# Folders: SCR/results/RUN_ID/p0500, SCR/results/RUN_ID/p1000 (P5_retry files included), SCR/logs/RUN_ID. Each gets MANIFEST.sha256 inside it, with
# paths RELATIVE to that folder (no leading ./), so after the download `cd <folder> && sha256sum -c MANIFEST.sha256` works on the laptop.
# Transactional and safely re-runnable (Sol review 2, R2-6):
#   1. PREFLIGHT of all three folders first (nothing is written): the folder exists, no *.lock / *.tmp.* / *.tmp file (the message names
#      cleanup_terminal.sh); a live job of the run, or a missing final accounting, refuses too.
#   2. BUILD and VERIFY every temporary manifest (on scratch, same filesystem as the folders) before any is committed. An EXISTING manifest is
#      REVALIDATED, never replaced: it must pass `sha256sum -c` and list exactly the files now present; otherwise the script refuses (inconsistent
#      manifest, nothing is overwritten and nothing else is committed).
#   3. COMMIT: new manifests are moved into place (atomic rename) and re-checked; then summary.tsv is rebuilt IN FULL (written aside, then renamed;
#      never truncated up front) from all three manifests, new or revalidated. So a failure part way (or an interrupted run) is recovered by running
#      the same command again.
#   4. HOME MANIFEST: RUN_DIR/HOME_MANIFEST.sha256 covers every file of the home run folder EXCEPT runner/ and itself (the small summaries that are
#      downloaded: tables, receipts, reconcile/scan/P5/accounting/cleanup/manifests files). It is created last, revalidated on a re-run (inconsistent:
#      refuse), and it is what must be verified locally (`cd <runs/RUN_ID copy> && sha256sum -c HOME_MANIFEST.sha256`) before any pruning of the home folder.
# ZERO-FILE FOLDER (Sol review 3, R3-3): an existing folder with no file at all (e.g. a p1000 result folder emptied by cleanup_terminal.sh, or a subgroup that
# entirely failed and is represented only by the attempt logs / terminal exceptions) is recorded EXPLICITLY as empty: MANIFEST.sha256 with ZERO lines (a
# 0-byte file) and `files 0` / `bytes 0` in manifests/summary.tsv. Its membership is validated by nc_verify_manifest WITHOUT `sha256sum -c` (which
# fails on a manifest with no checksum lines): the manifest must be 0 bytes and the folder must hold no file other than MANIFEST.sha256, on the first pass,
# on a re-run and after the commit. An empty folder that later gains a file is INCONSISTENT and refused like any other folder. Laptop check: JOB.md.
# Copies of the manifests and a size/count summary go to RUN_DIR/manifests/ (home, small). NOTHING is deleted by this script.
set -euo pipefail
RUNNER_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
source "$RUNNER_DIR/common.sh"
nc_refuse_hooks
RUN_DIR="$HOME_ROOT/runs/$(basename "$(cd "$RUNNER_DIR/.." && pwd)")"
nc_load_run "$RUN_DIR"
live=$(nc_live_jobs "$RUN_DIR") || nc_fail "squeue failed"
[[ -z $live ]] || nc_fail "job(s) of this run still queued or running: $(echo $live)"
[[ -s $RUN_DIR/accounting/sacct_final.tsv ]] || nc_fail "run final_accounting.sh first (its output goes into the logs folder)"
rmdir "$LOGROOT/tmp" 2>/dev/null || true
FOLDERS=("$RES_RUN/p0500" "$RES_RUN/p1000" "$LOGROOT")
LABELS=(results_p0500 results_p1000 logs)
mkdir -p "$SCR_ROOT/tmp"; TMPD=$(mktemp -d "$SCR_ROOT/tmp/mm.XXXXXX"); trap 'rm -rf -- "$TMPD"; rmdir "$SCR_ROOT/tmp" 2>/dev/null || true' EXIT

# CONF-2b (review-2 fix-up): one manifest line format everywhere, `<64 hex>  <path>` (GNU text form, as on NOTS). Some sha256sum builds
# (Git Bash/Cygwin) print the binary marker `<hash> *<path>`; both are normalised on writing and accepted on reading.
nc_sha_norm() { sed -E 's/^([0-9a-f]{64}) [ *]/\1  /'; }
# nc_verify_manifest DIR MANIFEST(absolute path) : 0 if DIR matches MANIFEST. A ZERO-BYTE manifest (empty folder, R3-3) is valid only if DIR holds no file
#   other than MANIFEST.sha256; `sha256sum -c` is never run on it (it exits nonzero on a manifest without checksum lines). Otherwise `sha256sum -c`.
nc_verify_manifest() {
  if [[ ! -s $2 ]]; then [[ -z $( cd "$1" && find . -type f ! -name MANIFEST.sha256 | head -n 1 ) ]]; return; fi
  ( cd "$1" && sha256sum --quiet -c "$2" >/dev/null 2>&1 )
}
# ---- 1. preflight of ALL folders (read-only) ----------------------------------------------------------------------------------------------
for d in "${FOLDERS[@]}"; do
  [[ -d $d ]] || nc_fail "missing folder $d"
  stale=$(find "$d" \( -name '*.lock' -o -name '*.tmp.*' -o -name '*.tmp' \) | head -3 | tr '\n' ' ')
  [[ -z $stale ]] || nc_fail "unfinished files under $d: $stale (a killed attempt left them: run runner/cleanup_terminal.sh, which archives and removes only proven-stale ones). NOTHING was written."
done

# ---- 2. build and verify every temporary manifest; revalidate existing ones -----------------------------------------------------------------------
STATUS=()
for i in 0 1 2; do
  d=${FOLDERS[$i]}
  ( cd "$d" && find . -type f ! -name MANIFEST.sha256 -printf '%P\n' | LC_ALL=C sort ) > "$TMPD/list_$i.txt"
  ( cd "$d" && tr '\n' '\0' < "$TMPD/list_$i.txt" | xargs -0 -r sha256sum | nc_sha_norm ) > "$TMPD/manifest_$i"
  nc_verify_manifest "$d" "$TMPD/manifest_$i" || nc_fail "temporary manifest self-check failed for $d (a file changed while it was being hashed?)"
  if [[ -e $d/MANIFEST.sha256 ]]; then
    existing=$(awk '{ sub(/^[0-9a-f]+ [ *]/, ""); print }' "$d/MANIFEST.sha256" | LC_ALL=C sort)
    if [[ "$existing" == "$(cat "$TMPD/list_$i.txt")" ]] && nc_verify_manifest "$d" "$d/MANIFEST.sha256"; then STATUS[i]=reused
    else nc_fail "$d/MANIFEST.sha256 exists but is INCONSISTENT with the folder (files added, removed or changed since it was written). It is never replaced silently: inspect it. NOTHING was committed."; fi
  else STATUS[i]=new
  fi
done

# ---- 3. commit new manifests, re-check, rebuild the full summary ---------------------------------------------------------------------------------
MAN=$RUN_DIR/manifests; mkdir -p "$MAN"
for i in 0 1 2; do
  d=${FOLDERS[$i]}
  [[ ${STATUS[$i]} == new ]] && mv "$TMPD/manifest_$i" "$d/MANIFEST.sha256"
  nc_verify_manifest "$d" "$d/MANIFEST.sha256" || nc_fail "manifest self-check failed for $d after the commit"
done
printf 'folder\tfiles\tbytes\tmanifest_sha256\n' > "$TMPD/summary.tsv"
for i in 0 1 2; do
  d=${FOLDERS[$i]}
  n=$(wc -l < "$d/MANIFEST.sha256"); b=$(find "$d" -type f ! -name MANIFEST.sha256 -printf '%s\n' | awk '{ s += $1 } END { print s + 0 }')
  printf '%s\t%d\t%d\t%s\n' "${d#"$SCR_ROOT"/}" "$n" "$b" "$(sha256sum "$d/MANIFEST.sha256" | cut -d' ' -f1)" >> "$TMPD/summary.tsv"
  cp "$d/MANIFEST.sha256" "$MAN/${LABELS[$i]}_MANIFEST.sha256"
  echo "${LABELS[$i]}: manifest ${STATUS[$i]}$([[ $n == 0 ]] && echo ' (EMPTY folder recorded explicitly: zero files, zero-line manifest, files=0)')"
done
cp "$TMPD/summary.tsv" "$MAN/summary.tsv.new" && mv "$MAN/summary.tsv.new" "$MAN/summary.tsv"
cat "$MAN/summary.tsv"

# ---- 4. home manifest (created last; revalidated on a re-run) --------------------------------------------------------------------------------------
home_list() { ( cd "$RUN_DIR" && find . -type f ! -path './runner/*' ! -name HOME_MANIFEST.sha256 ! -name '*.tmp.*' ! -path '*/__pycache__/*' -printf '%P\n' | LC_ALL=C sort ); }
home_list > "$TMPD/home_list.txt"
( cd "$RUN_DIR" && tr '\n' '\0' < "$TMPD/home_list.txt" | xargs -0 -r sha256sum | nc_sha_norm ) > "$TMPD/home_manifest"
if [[ -e $RUN_DIR/HOME_MANIFEST.sha256 ]]; then
  existing=$(awk '{ sub(/^[0-9a-f]+ [ *]/, ""); print }' "$RUN_DIR/HOME_MANIFEST.sha256" | LC_ALL=C sort)
  [[ "$existing" == "$(cat "$TMPD/home_list.txt")" ]] && ( cd "$RUN_DIR" && sha256sum --quiet -c HOME_MANIFEST.sha256 >/dev/null 2>&1 ) \
    || nc_fail "$RUN_DIR/HOME_MANIFEST.sha256 exists but is INCONSISTENT with the home run folder (a summary changed after it was written); it is never replaced silently"
  hstat=reused
else
  ( cd "$RUN_DIR" && sha256sum --quiet -c "$TMPD/home_manifest" ) || nc_fail "home manifest self-check failed"
  cp "$TMPD/home_manifest" "$RUN_DIR/HOME_MANIFEST.sha256.new" && mv "$RUN_DIR/HOME_MANIFEST.sha256.new" "$RUN_DIR/HOME_MANIFEST.sha256"; hstat=new
fi
( cd "$RUN_DIR" && sha256sum --quiet -c HOME_MANIFEST.sha256 ) || nc_fail "home manifest self-check failed after the commit"
echo "home summary manifest $hstat: $RUN_DIR/HOME_MANIFEST.sha256 ($(wc -l < "$RUN_DIR/HOME_MANIFEST.sha256") files, sha256 $(sha256sum "$RUN_DIR/HOME_MANIFEST.sha256" | cut -d' ' -f1))"
echo "manifests written or revalidated; download the three scratch folders AND the home run folder (without runner/), verify each with sha256sum -c (JOB.md) before any pruning. Nothing was deleted."
