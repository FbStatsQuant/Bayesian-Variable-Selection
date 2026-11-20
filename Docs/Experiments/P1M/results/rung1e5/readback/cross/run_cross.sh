#!/usr/bin/env bash
set -u
R=/home/fb31/SMC_Engineering_Department/records; X=/home/fb31/SMC_Engineering_Department/tmp/20261119-w1readback/xeval_build/smcbvs4_xeval; cd /home/fb31/SMC_Engineering_Department/tmp/20261120-rungrb/cross
for pair in "AR:$R/gb/GB_G1a/5-AR-n200-r01-V-s1:$R/rung1e5/RG_1b/5-AR-n200-r01-VN25-s1" "ADJOPP:$R/gb/GB_G2a/5-ADJOPP-n200-r01-V-s1:$R/rung1e5/RG_1b/5-ADJOPP-n200-r01-VN25-s1"; do
  IFS=: read ds A B <<< "$pair"
  nice -n 19 $X cross --a $A/law.bin --b $B/law.bin --truth $A/truth.json --data $A/data.bin --data-b $B/data.bin --dataset 5-$ds-n200-r01 --seed-id 1 --threads 3 --out cross_$ds.json > cross_$ds.stdout 2>&1; echo "cross $ds rc=$?"
  nice -n 19 $X cross --a $A/law.bin --b-truth 1 --truth $A/truth.json --threads 3 --out selfchk_${ds}_N10000.json > selfchk_${ds}_N10000.stdout 2>&1; echo "selfchk $ds N10000 rc=$?"
  nice -n 19 $X cross --a $B/law.bin --b-truth 1 --truth $A/truth.json --threads 3 --out selfchk_${ds}_N2500.json > selfchk_${ds}_N2500.stdout 2>&1; echo "selfchk $ds N2500 rc=$?"
done
echo ALLDONE
