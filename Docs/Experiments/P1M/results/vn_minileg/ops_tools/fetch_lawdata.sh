#!/usr/bin/env bash
# fetch_lawdata.sh -- V-N mini-leg: data.bin (all 15 fits) and law.bin (where the main unit has none: the r04 pair) as sibling units <run>.lawdata (hard links on Owls), like the VF units of the leg.
set -euo pipefail; . "$(dirname "$0")/tools/common.sh"; REC=$D/records/vn_minileg
declare -A BAT   # run -> wave
for w in V0 V1 V2; do for u in $REC/$w/4-*/; do BAT[$(basename $u)]=$w; done; done
ssh $NOTS "cd $D/scratch/runs && for b in VN_V0_1 VN_V0_2 VN_V0_3 VN_V1_1 VN_V1_2 VN_V2_1 VN_V2_2 VN_V2_3; do for r in \$b/4-*/; do echo \"\${r%/}\"; done; done" 2>/dev/null | grep '^VN_' > .runs.list
n=0
while read -r br <&3; do
  b=${br%%/*}; run=${br#*/}; w=${BAT[$run]}; U=$REC/$w/$run.lawdata; mkdir -p "$U"
  ssh $NOTS "cd $D/scratch/runs/$br && nice -n 19 sha256sum data.bin law.bin" > "$U/.nots.sums" 2>/dev/null
  rs $NOTS:$D/scratch/runs/$br/data.bin "$U/data.bin"
  if [[ -f $REC/$w/$run/law.bin ]]; then ln -f "$REC/$w/$run/law.bin" "$U/law.bin"; else rs $NOTS:$D/scratch/runs/$br/law.bin "$U/law.bin"; fi
  ( cd "$U" && sha256sum data.bin law.bin > SHA256SUMS && diff -q <(awk '{print $1}' .nots.sums) <(awk '{print $1}' SHA256SUMS) >/dev/null ) || { echo "MISMATCH $run" >&2; exit 1; }
  rm -f "$U/.nots.sums"
  echo "law.bin and data.bin of unit $w/$run (added after the collection of the wave; the N contrast and any cross need them). Same bytes as in the unit directory where law.bin was collected (hard links on Owls); sha256 verified against NOTS. 2026-11-20." > "$U/FOR_UNIT.txt"
  n=$((n+1)); echo "ok $w/$run"
done 3< .runs.list
echo "lawdata done: $n units"
