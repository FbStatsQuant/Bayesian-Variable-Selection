#!/usr/bin/env bash
# vn_collect.sh -- V-N mini-leg F2 identity check: the ONE unit records/vn_minileg/F2_ID/4-AR-n200-r01-V-s1 + _batch_VN_ID_1 (adapted from the precision leg collect_wave.sh). Owls: pull the wave's units into $OWLS_REC/<WAVE>/<run_id>/ (+ _batch_PL_<WAVE>_<i>/), verify, desktop-ready.
# Layout records/precision1e4/<wave>/<run_id>/ (depth 3 under records/, as serve_pull.sh expects). ONE SHA256SUMS per unit, at the unit root; NEVER nested
# (checked: `find <unit> -name 'SHA256SUMS*'` must be exactly 1; the driver's own sums are renamed driver_sha256.txt). nice, one stream. Frees NOTHING on NOTS.
# calib_meta.json per fit (smcbvs4 info calib.bin --meta 1, batch env.sh) is made on NOTS by collect_nots.sh. setup.bin only for the A3 fits and their default pairs
# (30 units, from waves.json); law.bin only for precision and A3 fits; data.bin not collected. BATCHES="..." restricts. COST_PY: p1m_cost.py of the freeze worktree.
set -euo pipefail; . "$(dirname "$0")/common.sh"; OWLS_REC=$D/records/vn_minileg
WAVE=VNID; DEST=$OWLS_REC/F2_ID; mkdir -p "$DEST"
BL=$BATCH
WJ=/dev/null
KEEP=""
ssh $NOTS "bash -s -- $D $WAVE '$KEEP' $BL" < "$(dirname "$0")/collect_nots.sh"
nbad=0; nunit=0
for b in $BL; do
  R=$D/scratch/runs/$b
  for run in $(ssh $NOTS "ls -d $R/*/ | xargs -n1 basename"); do
    U=$DEST/$run; mkdir -p "$U"
    ssh $NOTS "cat $R/$run/OFFLOAD_FILES.sha256" > "$U/.sums.new"
    awk '{print $2}' "$U/.sums.new" > "$U/.files.new"
    rs --files-from="$U/.files.new" $NOTS:$R/$run/ "$U"/
    [[ -f $U/fit.bin ]] || echo "INCOMPLETE: $run has no fit.bin (failed or unfinished; kept for the record: logs, manifests)" | tee "$U/INCOMPLETE.txt"
    [[ -f $U/calib_meta.json ]] || echo "NOTE: $run has no calib_meta.json (calibration did not finish?)"
    mv "$U/.sums.new" "$U/SHA256SUMS"; rm -f "$U/.files.new"
    [[ -f $U/INCOMPLETE.txt ]] && ( cd "$U"; sha256sum INCOMPLETE.txt >> SHA256SUMS )
    ( cd "$U" && sha256sum --quiet -c SHA256SUMS ) && nunit=$((nunit+1)) || { echo "VERIFY FAILED: $run" >&2; nbad=$((nbad+1)); }
    [[ $(find "$U" -name 'SHA256SUMS*' | wc -l) -eq 1 ]] || { echo "NESTED/EXTRA SHA256SUMS in $run" >&2; nbad=$((nbad+1)); }
  done
done
for b in $BL; do   # batch units: driver scripts, bin version (env.sh sourced) + hash, jsonl logs, slurm_out, sacct; cost fields from p1m_cost.py
  R=$D/scratch/runs/$b; U=$DEST/_batch_$b; mkdir -p "$U"
  ssh $NOTS "cat $R/_batch_extra.list" > "$U/.extra.list"
  for f in submissions.jsonl starts.jsonl ends.jsonl sacct_dump.txt bin_version.json; do echo "$f"; done > "$U/.top.list"
  rs --files-from="$U/.top.list" $NOTS:$R/ "$U"/ || true
  mkdir -p "$U/scripts/bin" "$U/slurm_out"
  grep '^scripts/' "$U/.extra.list" | sed "s#^scripts/##" > "$U/.scripts.list"; rs --files-from="$U/.scripts.list" $NOTS:$D/scripts/$b/ "$U/scripts/"
  grep '^scratch/slurm_out/' "$U/.extra.list" | sed "s#^scratch/slurm_out/##" > "$U/.so.list" || true; [[ -s $U/.so.list ]] && rs --files-from="$U/.so.list" $NOTS:$D/scratch/slurm_out/ "$U/slurm_out/"
  rs $NOTS:$D/scripts/$b/SHA256SUMS "$U/scripts/driver_sha256.txt"
  ( cd "$U" && sha256sum --quiet -c <(ssh $NOTS "cat $R/_batch_files.sha256") ) || { echo "VERIFY FAILED (batch top files) $b" >&2; nbad=$((nbad+1)); }
  mkdir -p "$U/cost"; python3 "${COST_PY:-$STG/wt_e993ece2/Scripts/SMC_BVS/engine_v4/tools/slurm/p1m_cost.py}" --sacct "$U/sacct_dump.txt" --submissions "$U/submissions.jsonl" --out-dir "$U/cost"
  rm -f "$U"/.*.list
  ( cd "$U" && find . -type f ! -name SHA256SUMS | sed 's#^\./##' | sort | xargs sha256sum > SHA256SUMS && sha256sum --quiet -c SHA256SUMS ) && nunit=$((nunit+1)) || nbad=$((nbad+1))
  [[ $(find "$U" -name 'SHA256SUMS*' | wc -l) -eq 1 ]] || { echo "NESTED SHA256SUMS in $b" >&2; nbad=$((nbad+1)); }
done
echo "collected: $nunit units verified, $nbad problems, under $DEST"; [[ $nbad -eq 0 ]]
