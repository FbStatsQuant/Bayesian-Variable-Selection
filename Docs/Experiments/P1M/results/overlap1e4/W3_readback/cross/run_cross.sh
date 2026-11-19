#!/usr/bin/env bash
set -u
R=/home/fb31/SMC_Engineering_Department/records/overlap1e4/W3; X=/home/fb31/SMC_Engineering_Department/tmp/20261119-w1readback/xeval_build/smcbvs4_xeval
cd "$(dirname "$0")"
for pair in "4-AR-n200-r02 1" "4-AR-n200-r02 2" "4-AR-n200-r03 1" "4-AR-n200-r03 2" "4-AR-n200-r04 1" "4-AR-n200-r04 2"; do
  set -- $pair; ds=$1; s=$2
  V=$R/$ds-V-s$s; Tt=$R/$ds-T-s$s
  nice -n 19 $X cross --a $V/law.bin --b $Tt/law.bin --truth $V/truth.json --data $V/data.bin --data-b $Tt/data.bin --dataset $ds --seed-id $s --threads 3 --out cross_${ds}_s$s.json > cross_${ds}_s$s.stdout 2>&1; echo "cross $ds s$s rc=$?"
  for a in V T; do d=$R/$ds-$a-s$s
    nice -n 19 $X cross --a $d/law.bin --b-truth 1 --truth $d/truth.json --threads 3 --out selfchk_${ds}_${a}_s$s.json > selfchk_${ds}_${a}_s$s.stdout 2>&1; echo "selfchk $ds $a s$s rc=$?"
  done
done
echo ALLDONE
