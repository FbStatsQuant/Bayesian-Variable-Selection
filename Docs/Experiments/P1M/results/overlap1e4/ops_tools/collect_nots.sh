#!/usr/bin/env bash
# collect_nots.sh <WAVE> -- runs ON NOTS (feed it with: ssh nots 'bash -s -- W0' < collect_nots.sh). nice, one sacct call, no deletion.
# Per run dir: OFFLOAD_FILES.sha256 = sha256 of every file of record (relative paths). Kept = everything EXCEPT the rebuildable
# raw.bin, setup.bin, calib.bin, island_*.bin, checkpoints (and SHA256SUMS*, OFFLOAD* themselves). data.bin IS kept (X, y for the analysis; ~16 MB).
# Per batch: _batch_files.sha256 = driver files (no code/, build*/), bin/smcbvs4.sha256 + bin_version.json, submissions/starts/ends.jsonl,
# slurm_out logs, and ONE sacct dump of both batches (the p1m_cost.py format, with the step rows for MaxRSS).
set -euo pipefail
WAVE=${1:?WAVE}; ARMS=${2:-T V}; BL=$(for a in $ARMS; do printf "OV_%s_%s " "$WAVE" "$a"; done); D=${P1M_OPS_D:-$HOME/SMC_Engineering_Department}; ids=''
for b in $BL; do
  R=$D/scratch/runs/$b; S=$D/scripts/$b
  ids="$ids,$(grep -o '"job": *"[0-9]*"' "$R/submissions.jsonl" | grep -o '[0-9][0-9]*' | paste -sd,)"
done
ids=$(echo "$ids" | sed 's/^,*//; s/,,*/,/g; s/,*$//')
sacct -P -n -j "$ids" --format=JobID,JobName,State,ElapsedRaw,AllocCPUS,CPUTimeRAW,MaxRSS,NodeList,Timelimit > "$D/scratch/runs/OV_${WAVE}_sacct.txt"   # the one sacct call
for b in $BL; do
  R=$D/scratch/runs/$b; S=$D/scripts/$b
  cp "$D/scratch/runs/OV_${WAVE}_sacct.txt" "$R/sacct_dump.txt"
  "$S/bin/smcbvs4" version > "$R/bin_version.json" 2>&1 || true
  for run in "$R"/*/; do
    [[ -d $run ]] || continue
    ( cd "$run"; rm -f OFFLOAD_FILES.sha256
      find . -type f ! -name raw.bin ! -name setup.bin ! -name calib.bin ! -name 'island_*.bin' ! -name '*.ckpt*' ! -name 'SHA256SUMS*' ! -name 'OFFLOAD*' \
        | sed 's#^\./##' | sort | nice -n 19 xargs -r sha256sum > OFFLOAD_FILES.sha256 )
  done
  ( cd "$R"; { ls -1 submissions.jsonl starts.jsonl ends.jsonl sacct_dump.txt bin_version.json 2>/dev/null; } | nice -n 19 xargs -r sha256sum > _batch_files.sha256 )
  # batch-level extras are listed with paths relative to a virtual root: scripts/<b>/..., slurm_out/...
  { ( cd "$S"; find . -type f ! -path './code/*' ! -path './build*' ! -path './bin/*' ! -name 'SHA256SUMS' | sed 's#^\./#scripts/#' | sort ) ; echo "scripts/bin/smcbvs4.sha256"; } > "$R/_batch_extra.list"
  ls "$D"/scratch/slurm_out/p1m_${b}_* 2>/dev/null | sed "s#^$D/scratch/#scratch/#" >> "$R/_batch_extra.list" || true
  echo "$b: $(ls -d "$R"/*/ | wc -l) run dirs listed; $(wc -l < "$R/_batch_extra.list") batch extras"
done
echo "collect_nots done: $D/scratch/runs/OV_${WAVE}_sacct.txt, OFFLOAD_FILES.sha256 per run dir"
