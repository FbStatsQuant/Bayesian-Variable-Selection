#!/usr/bin/env bash
# gc_collect_nots_A.sh -- GC_D (option D; GC_PLAN §5 classes A / A+, NOT the pilot exception): fit.bin, eval.bin, law.bin, setup.bin (A+: one of the four special datasets) and the sidecars are kept; data.bin, calib.bin, raw.bin, the 16 island_*.bin and checkpoints are NOT (B / C). Derived from gc_collect_nots.sh (1M pilot GC_P (GC_PLAN §5, H-41 / H-45 (c) pilot exception): fit.bin, eval.bin, law.bin, data.bin, setup.bin, calib.bin and the 16 island_*.bin are ALL kept (raw.bin and *.ckpt* are not); otherwise as rung_collect_nots.sh. The T6 run dir keeps t6.json, t6/ logs and hash files (island / checkpoint *.bin are not kept). Runs ON NOTS (fed by collect_wave.sh through ONE ssh):  bash -s -- <DEPT> <WAVE> <SETUP_KEEP_CSV> <batch>...
# nice, ONE sacct call, NO deletion. Per run dir:
#   calib_meta.json = `smcbvs4 info calib.bin --meta 1 --record` run with the BATCH's env.sh sourced (O-4, R8; written only when absent: the A0 monitor may have made it);
#   OFFLOAD_FILES.sha256 = sha256 of every file of record (relative paths). Kept = everything EXCEPT rebuildable *.bin (raw, data, calib, island_*, checkpoints) and
#   SHA256SUMS* / OFFLOAD*; KEPT *.bin: fit.bin, eval.bin; law.bin only for the precision fits (-P-) and the A3 fits; setup.bin only for the run ids in SETUP_KEEP_CSV
#   (the A3 fits and their default pairs, R15). data.bin is NOT collected (except the boundary dataset r91 of B1) (rebuildable from its seed; a change from the overlap).
# Per batch: bin_version.json = `version` with the batch env.sh SOURCED (the overlap's version file was written without env.sh and held the false
#   'CXXABI_1.3.15 not found' text: that flaw is fixed; a non-JSON result is stored as bin_version.ERROR.txt and reported), submissions / starts / ends jsonl,
#   the one sacct dump (p1m_cost.py format, with step rows), _batch_files.sha256, _batch_extra.list (driver scripts, bin/smcbvs4.sha256, COPIED_FROM, slurm_out logs).
set -euo pipefail
D=$1; WAVE=$2; KEEP=$3; shift 3; BL="$*"; ids=''
for b in $BL; do ids="$ids,$(grep -o '"job": *"[0-9]*"' "$D/scratch/runs/$b/submissions.jsonl" | grep -o '[0-9][0-9]*' | paste -sd,)"; done
ids=$(echo "$ids" | sed 's/^,*//; s/,,*/,/g; s/,*$//')
SA=$D/scratch/runs/PL_${WAVE}_sacct.txt
sacct -P -n -j "$ids" --format=JobID,JobName,State,ElapsedRaw,AllocCPUS,CPUTimeRAW,MaxRSS,NodeList,Timelimit > "$SA"      # the one sacct call
for b in $BL; do
  R=$D/scratch/runs/$b; S=$D/scripts/$b
  cp "$SA" "$R/sacct_dump.txt"
  v=$( ( set +u; source "$S/env.sh" >/dev/null 2>&1; "$S/bin/smcbvs4" version 2>&1 ) || true )
  if echo "$v" | grep -q '"git_commit"'; then echo "$v" > "$R/bin_version.json"; rm -f "$R/bin_version.ERROR.txt"
  else echo "$v" > "$R/bin_version.ERROR.txt"; echo "WARNING: $b: version did not print JSON even with env.sh (see bin_version.ERROR.txt)" >&2; fi
  for run in "$R"/*/; do
    [[ -d $run ]] || continue; rid=$(basename "$run")
    if [[ -s $run/calib.bin && ! -f $run/calib_meta.json ]]; then
      ( set +u; source "$S/env.sh" >/dev/null 2>&1; nice -n 19 "$S/bin/smcbvs4" info "$run/calib.bin" --meta 1 --record "$run/calib_meta.json" >/dev/null 2>&1 ) \
        || echo "WARNING: $rid: calib_meta.json could not be made" >&2
    fi
    keep_law=1; keep_data=0; keep_setup=1   # GC_PLAN §5: A (fit, law, eval, sidecars) + A+ (setup.bin of option D); data / calib / islands are B / C
    ( cd "$run"; rm -f OFFLOAD_FILES.sha256
      find . -type f ! -name 'SHA256SUMS*' ! -name 'OFFLOAD*' ! -name '*.ckpt*' \
        ! \( -name '*.bin' ! -name fit.bin ! -name eval.bin ! -name law.bin ! -name setup.bin ! -name data.bin \) | sed 's#^\./##' | sort \
        | while read -r f; do
            case $f in law.bin) [[ $keep_law -eq 1 ]] || continue;; setup.bin) [[ $keep_setup -eq 1 ]] || continue;; data.bin) [[ $keep_data -eq 1 ]] || continue;; esac
            echo "$f"
          done | nice -n 19 xargs -r sha256sum > OFFLOAD_FILES.sha256 )
  done
  # (the T6 batch has no starts.jsonl: under pipefail the ls status killed the script, hence the || true)
  ( cd "$R"; { ls -1 submissions.jsonl starts.jsonl ends.jsonl sacct_dump.txt bin_version.json 2>/dev/null || true; } | nice -n 19 xargs -r sha256sum > _batch_files.sha256 )
  { ( cd "$S"; find . -type f ! -path './code/*' ! -path './build*' ! -path './bin/*' ! -name 'SHA256SUMS' | sed 's#^\./#scripts/#' | sort ); echo "scripts/bin/smcbvs4.sha256"; [[ -f $S/bin/COPIED_FROM ]] && echo "scripts/bin/COPIED_FROM"; true; } > "$R/_batch_extra.list"
  ls "$D"/scratch/slurm_out/p1m_${b}_* 2>/dev/null | sed "s#^$D/scratch/#scratch/#" >> "$R/_batch_extra.list" || true
  echo "$b: $(ls -d "$R"/*/ | wc -l) run dirs listed; $(wc -l < "$R/_batch_extra.list") batch extras"
done
echo "collect_nots done: $SA, OFFLOAD_FILES.sha256 + calib_meta.json per run dir"
