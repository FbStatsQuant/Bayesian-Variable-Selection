#!/usr/bin/env bash
# vf_cross.sh -- criterion H for the 14 VF fits: smcbvs4_xeval cross VF law vs the overlap T law (same dataset, same seed id), plus the self-checks (A vs the truth) of
# every VF law and every T law. nice 19, 3 threads. Scratch: this dir. No guard bypass (xeval refuses a data mismatch).
set -u; H=$(cd "$(dirname "$0")" && pwd); X=/home/fb31/SMC_Engineering_Department/tmp/20261119-w1readback/xeval_build/smcbvs4_xeval; mkdir -p $H/cross; cd $H/cross
while IFS=$'\t' read -r wave rid ds s vf t; do
  nice -n 19 $X cross --a $vf/law.bin --b $t/law.bin --truth $vf/truth.json --data $vf/data.bin --data-b $t/data.bin --dataset $ds --seed-id $s --threads 3 --out cross_${ds}_s$s.json > cross_${ds}_s$s.stdout 2>&1; echo "cross $rid rc=$?"
  nice -n 19 $X cross --a $vf/law.bin --b-truth 1 --truth $vf/truth.json --threads 3 --out selfchk_VF_${ds}_s$s.json > selfchk_VF_${ds}_s$s.stdout 2>&1; echo "selfchk VF $rid rc=$?"
  nice -n 19 $X cross --a $t/law.bin --b-truth 1 --truth $vf/truth.json --threads 3 --out selfchk_T_${ds}_s$s.json > selfchk_T_${ds}_s$s.stdout 2>&1; echo "selfchk T $ds s$s rc=$?"
done < $H/pairs.tsv
echo ALLDONE
