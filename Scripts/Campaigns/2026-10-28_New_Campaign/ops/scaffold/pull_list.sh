#!/bin/bash
# pull_list.sh OUTFILE SPEC... : (laptop; detached) pull NOTS folders one at a time with ops/transfer/nots_pull.py, each pull holding the global NOTS
# ssh lock (sshlock/with_lock.sh). SPEC = "<remote folder>|delete" or "<remote folder>|keep". After each pull, if the local copy has a bundle
# MANIFEST.sha256 (or HOME_MANIFEST.sha256), it is also checked locally with sha256sum -c. Stops at the first failure. Appends to OUTFILE.
set -u
OUT=${1:?outfile}; shift
OPSD=/c/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign/ops
PULL=C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign/ops/transfer/nots_pull.py
DM="/c/Users/felip/OneDrive - Rice University/NOTS Data/New_Campaign"
# v2 (2026-11-02): optional third field = local destination (Windows path for nots_pull --local, e.g. home summaries into a fresh sibling such as
# ...\runs\<RID>\home_summary\<name>, never merged into an existing folder).
for spec in "$@"; do
  IFS='|' read -r r mode ldest <<< "$spec"; flag=""; [ "$mode" = delete ] && flag=--delete
  echo "=== $(date -u +%FT%TZ) PULL $r ($mode)${ldest:+ -> $ldest}" >> "$OUT"
  if [ -n "$ldest" ]; then MSYS_NO_PATHCONV=1 bash "$OPSD/scaffold/sshlock/with_lock.sh" py -3 "$PULL" "$r" --local "$ldest" $flag >> "$OUT" 2>&1; rc=$?
  else MSYS_NO_PATHCONV=1 bash "$OPSD/scaffold/sshlock/with_lock.sh" py -3 "$PULL" "$r" $flag >> "$OUT" 2>&1; rc=$?; fi
  echo "pull_rc=$rc" >> "$OUT"
  [ $rc -eq 0 ] || { echo "STOP: pull failed for $r" >> "$OUT"; echo "PULL_LIST_DONE FAILED" >> "$OUT"; exit 1; }
  rel=${r#/scratch/fb31/New_Campaign/}; rel=${rel#/home/fb31/projects/BVS/New_Campaign/}; loc="$DM/$rel"
  [ -n "$ldest" ] && loc=$(cygpath -u "$ldest")
  for m in MANIFEST.sha256 HOME_MANIFEST.sha256; do
    if [ -s "$loc/$m" ]; then ( cd "$loc" && sha256sum --quiet -c "$m" ) >> "$OUT" 2>&1 && echo "LOCAL_BUNDLE_MANIFEST_OK $m $(sha256sum "$loc/$m" | cut -c1-64)" >> "$OUT" || { echo "LOCAL_BUNDLE_MANIFEST_FAIL $m" >> "$OUT"; echo "PULL_LIST_DONE FAILED" >> "$OUT"; exit 1; }; fi
  done
done
echo "PULL_LIST_DONE OK $(date -u +%FT%TZ)" >> "$OUT"
