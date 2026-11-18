#!/usr/bin/env bash
# collect_wave.sh <WAVE> -- Owls: pull the wave's units into $OWLS_REC/<WAVE>/<run_id>/ (+ _batch_OV_<WAVE>_{T,V}/), verify, desktop-ready.
# Rules: ONE SHA256SUMS per unit, at the unit root; NO nested SHA256SUMS inside a unit (it breaks the desktop pull; serve_pull.sh lists
# units by `find ... -name SHA256SUMS` at depth 1-3 under records/). nice, one stream. Frees NOTHING on NOTS (cleanup only after the
# desktop verified, crews/offload/desktop_verified.txt). Needs collect_nots.sh run first (one ssh).
set -euo pipefail; . "$(dirname "$0")/common.sh"
WAVE=${1:?WAVE}
# W0 = original T, V (evidence) + rebuilds T2, V2; ARMS= overrides. Units of a rebuild batch are <run_id>.<arm> (the run ids repeat across batches).
[[ $WAVE == W0 && $ARMS == "T V" ]] && ARMS="T V T2 V2"
BL=$(for a in $ARMS; do printf "OV_%s_%s " "$WAVE" "$a"; done)
DEST=$OWLS_REC/$WAVE; mkdir -p "$DEST"
ssh $NOTS 'bash -s -- '"$WAVE \"$ARMS\"" < "$(dirname "$0")/collect_nots.sh"
nbad=0; nunit=0
for b in $BL; do
  R=$D/scratch/runs/$b
  runs=$(ssh $NOTS "ls -d $R/*/ | xargs -n1 basename")
  for run in $runs; do
    suf=""; [[ $b == *2 ]] && suf=".${b##*_}"; U=$DEST/$run$suf; mkdir -p "$U"
    ssh $NOTS "cat $R/$run/OFFLOAD_FILES.sha256" > "$U/.sums.new"
    awk '{print $2}' "$U/.sums.new" > "$U/.files.new"
    rs --files-from="$U/.files.new" $NOTS:$R/$run/ "$U"/
    [[ -f $U/fit.bin ]] || { echo "INCOMPLETE: $run has no fit.bin (failed or unfinished; kept for the record: logs, manifests)" | tee "$U/INCOMPLETE.txt" ; }
    mv "$U/.sums.new" "$U/SHA256SUMS"; rm -f "$U/.files.new"
    [[ -f $U/INCOMPLETE.txt ]] && ( cd "$U"; sha256sum INCOMPLETE.txt >> SHA256SUMS )
    ( cd "$U" && sha256sum --quiet -c SHA256SUMS ) && nunit=$((nunit+1)) || { echo "VERIFY FAILED: $run" >&2; nbad=$((nbad+1)); }
    [[ $(find "$U" -name 'SHA256SUMS*' | wc -l) -eq 1 ]] || { echo "NESTED/EXTRA SHA256SUMS in $run" >&2; nbad=$((nbad+1)); }
  done
done
# batch units: driver scripts, bin version + hash, jsonl logs, slurm_out, sacct; then cost fields via p1m_cost.py (from the batch's own scripts dir)
for b in $BL; do
  R=$D/scratch/runs/$b; U=$DEST/_batch_$b; mkdir -p "$U"
  ssh $NOTS "cat $R/_batch_extra.list" > "$U/.extra.list"
  for f in submissions.jsonl starts.jsonl ends.jsonl sacct_dump.txt bin_version.json; do echo "$f"; done > "$U/.top.list"
  rs --files-from="$U/.top.list" $NOTS:$R/ "$U"/ || true
  mkdir -p "$U/scripts" "$U/slurm_out"
  grep '^scripts/' "$U/.extra.list" | sed "s#^scripts/##" > "$U/.scripts.list"; rs --files-from="$U/.scripts.list" $NOTS:$D/scripts/$b/ "$U/scripts/"
  grep '^scratch/slurm_out/' "$U/.extra.list" | sed "s#^scratch/slurm_out/##" > "$U/.so.list" || true; [[ -s $U/.so.list ]] && rs --files-from="$U/.so.list" $NOTS:$D/scratch/slurm_out/ "$U/slurm_out/"
  mkdir -p "$U/scripts/bin"; rs $NOTS:$D/scripts/$b/bin/smcbvs4.sha256 "$U/scripts/bin/"
  rs $NOTS:$D/scripts/$b/SHA256SUMS "$U/scripts/driver_sha256.txt"        # the driver's own sums, renamed: only ONE file named SHA256SUMS per unit
  ( cd "$U" && sha256sum --quiet -c <(ssh $NOTS "cat $R/_batch_files.sha256") ) || { echo "VERIFY FAILED (batch top files) $b" >&2; nbad=$((nbad+1)); }
  # p1m_cost.py (cost fields, billed core-h = CPUTimeRAW/3600) is NOT copied by the driver: run it from the freeze worktree
  mkdir -p "$U/cost"; python3 "${COST_PY:-$STG/current/wt/Scripts/SMC_BVS/engine_v4/tools/slurm/p1m_cost.py}" --sacct "$U/sacct_dump.txt" --submissions "$U/submissions.jsonl" --out-dir "$U/cost"
  rm -f "$U"/.*.list
  ( cd "$U" && find . -type f ! -name SHA256SUMS | sed 's#^\./##' | sort | xargs sha256sum > SHA256SUMS && sha256sum --quiet -c SHA256SUMS ) && nunit=$((nunit+1)) || nbad=$((nbad+1))
  [[ $(find "$U" -name 'SHA256SUMS*' | wc -l) -eq 1 ]] || { echo "NESTED SHA256SUMS in $b (the driver's own SHA256SUMS must not be copied)" >&2; nbad=$((nbad+1)); }
done
echo "collected: $nunit units verified, $nbad problems, under $DEST"; [[ $nbad -eq 0 ]]
