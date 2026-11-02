#!/bin/bash
# all 12 (p, S) cells, R = 60 conditional-MC draws per dataset and scale; one owls_run job per cell,
# sequential; retries when owls_run refuses (exit 75).
PY=$1
cd "$(dirname "$0")"
for p in 500 1000; do for s in 4 5 3 6 1 2; do
  [ -f ../out/cells_p${p}_S${s}.csv ] && continue
  until /home/fb31/.config/bvs-hq/owls/owls_run -j 2 -- $PY run_cells.py $p $s 60; rc=$?; [ $rc -ne 75 ]; do sleep 30; done
  [ $rc -ne 0 ] && echo FAIL $p $s rc=$rc
done; done
echo ALLDONE
