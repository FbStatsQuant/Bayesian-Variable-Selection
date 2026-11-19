#!/usr/bin/env bash
# READ-ONLY: smcbvs4 info <calib.bin> --meta 1 (stdout), batch env.sh sourced, nice 19; only the overlap run dirs' calib.bin; no writes.
D=/home/fb31/SMC_Engineering_Department
for R in $D/scratch/runs/OV_W[0-3]_[TV]*; do
  [ -d "$R" ] || continue
  b=$(basename "$R"); S=$D/scripts/$b
  for cb in "$R"/*/calib.bin; do
    [ -s "$cb" ] || continue
    echo "@@@ $b $(basename "$(dirname "$cb")")"
    ( set +u; source "$S/env.sh" >/dev/null 2>&1; nice -n 19 "$S/bin/smcbvs4" info "$cb" --meta 1 2>&1 )
    echo "@@@END"
  done
done
