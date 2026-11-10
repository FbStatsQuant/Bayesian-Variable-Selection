#!/bin/bash
# W3-SCR: run the N2 scenarios that have no SUMMARY line yet, P at a time (single-threaded BLAS).
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
P=${1:-2}
for s in noisecs98 twin99 fac_strong dupnoise twin90 ar_strong twin999 pairs_iid pairs_cs20 pairs_cs50 pairs_cs80 fac_p1000; do
  grep -q SUMMARY n2_out/$s.txt 2>/dev/null || echo $s
done | xargs -P "$P" -I{} bash -c 'py -3.13 n2_boundary.py {} 10 > n2_out/{}.txt 2> n2_out/{}.err'
echo N2DONE
