#!/bin/bash
# laptop: all 12 cells, R = 40 conditional-MC draws per dataset and scale, 4 cores
cd "$(dirname "$0")"
for s in 4 5 1 3 6 2; do for p in 500 1000; do
  [ -f ../out/local_p${p}_S${s}.csv ] && continue
  python run_local.py $p $s 40 || echo FAIL $p $s
done; done
echo ALLDONE
