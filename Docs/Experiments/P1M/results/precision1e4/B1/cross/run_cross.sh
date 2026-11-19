#!/usr/bin/env bash
# B1 cross-Hellinger (V vs T on the same data) + 4 self-checks (B = truth); xeval build b89cba4d (sha256 afef0e46...), nice, no guard bypass. Same flags as overlap W3_readback/cross/run_cross.sh.
set -u
R=/home/fb31/SMC_Engineering_Department/records/precision1e4/B1; X=/home/fb31/SMC_Engineering_Department/tmp/20261119-w1readback/xeval_build/smcbvs4_xeval
cd "$(dirname "$0")"
ds=4-ARweak-n100-r91
for s in 1 2; do
  V=$R/$ds-V-s$s; Tt=$R/$ds-T-s$s
  nice -n 19 $X cross --a $V/law.bin --b $Tt/law.bin --truth $V/truth.json --data $V/data.bin --data-b $Tt/data.bin --dataset $ds --seed-id $s --threads 3 --out cross_${ds}_s$s.json > cross_${ds}_s$s.stdout 2>&1; echo "cross $ds s$s rc=$?"
  for a in V T; do d=$R/$ds-$a-s$s
    nice -n 19 $X cross --a $d/law.bin --b-truth 1 --truth $d/truth.json --threads 3 --out selfchk_${ds}_${a}_s$s.json > selfchk_${ds}_${a}_s$s.stdout 2>&1; echo "selfchk $ds $a s$s rc=$?"
  done
done
echo ALLDONE
