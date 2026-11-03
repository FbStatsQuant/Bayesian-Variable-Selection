#!/bin/bash
# finish_pulls3.sh : (laptop, local only) complete the pull_list bookkeeping that the corrupted with_lock (in-place rewrite of with_lock.sh during
# HQ D76 while the 18:11Z pull was running) never wrote: local sha256sum -c of the PROD-L logs bundle MANIFEST, then pull_rc / LOCAL_BUNDLE_*
# / PULL_LIST_DONE lines in ops_pulls3_20261102.txt (with a NOTE). The pull itself had printed VERIFIED (20:08:52Z) and DELETED (21:26:53Z).
set -u
E=/c/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign/ops/evidence; OUT=$E/ops_pulls3_20261102.txt
L="/c/Users/felip/OneDrive - Rice University/NOTS Data/New_Campaign/logs/20261030T1811Z_lowp_prodL"
grep -q 'VERIFIED' <(grep 'PULL /scratch/fb31/New_Campaign/logs/20261030T1811Z_lowp_prodL ->' $OUT) || { echo "no VERIFIED line: refusing"; exit 2; }
grep -q 'DELETED /scratch/fb31/New_Campaign/logs/20261030T1811Z_lowp_prodL' $OUT || { echo "no DELETED line: refusing"; exit 2; }
echo "NOTE $(date -u +%FT%TZ): OPS completes this pull's bookkeeping by hand: the pull printed VERIFIED + DELETED above, then the running with_lock.sh (rewritten in place at ~18:15Z for HQ D76) executed garbage ('eck: command not found') and stalled; pull_list 9403 / with_lock 9409 / pull_resume 9391 stopped by explicit PID. pull_rc taken as 0 from the VERIFIED/DELETED lines; local bundle MANIFEST checked now." >> $OUT
echo "pull_rc=0" >> $OUT
if ( cd "$L" && sha256sum --quiet -c MANIFEST.sha256 ) >> $OUT 2>&1; then
  echo "LOCAL_BUNDLE_MANIFEST_OK MANIFEST.sha256 $(sha256sum "$L/MANIFEST.sha256" | cut -c1-64)" >> $OUT
  echo "PULL_LIST_DONE OK $(date -u +%FT%TZ)" >> $OUT
else
  echo "LOCAL_BUNDLE_MANIFEST_FAIL MANIFEST.sha256" >> $OUT; echo "PULL_LIST_DONE FAILED" >> $OUT; exit 1
fi
tail -3 $OUT
