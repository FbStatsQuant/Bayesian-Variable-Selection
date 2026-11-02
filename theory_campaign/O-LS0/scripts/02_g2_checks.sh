#!/usr/bin/env bash
# Run the generator's own gate-G2 checks (Scripts/Data_generators/verify_prod_data.R) on the regenerated data, per cell.
# p = 1000: the script unchanged. p = 500: the same script with its "if (p == 500L) {...}" Oct-14 block removed
# (it compares with sealed files under /scratch on NOTS, not present on Owls). Every other check is unchanged:
# truth placement oracle, standardisation, response = c*signal + eps, folds, seeds, and a fresh-process regeneration
# with a per-dataset chol for r = 1, 50, 100 compared with identical().
set -euo pipefail
WORK=${1:-/home/fb31/ls0_work}; STUDY=${2:-study}; TH=${3:-1}
export FLEXIBLAS=OPENBLAS-OPENMP OMP_NUM_THREADS=$TH OPENBLAS_NUM_THREADS=$TH   # same BLAS pinning as 00_regen_data.sh
REPO=$(git -C "$(dirname "$0")" rev-parse --show-toplevel)
V="$REPO/Scripts/Data_generators/verify_prod_data.R"; GEN="$REPO/Scripts/Data_generators/gen_prod_data.R"
V500="$WORK/verify_prod_data_noOct14.R"
python3 - "$V" "$V500" <<'PY'
import sys
s=open(sys.argv[1]).read()
i=s.index('  if (p == 500L) {   # ')
j=s.index('\n  }\n', i)+4
open(sys.argv[2],'w').write(s[:i]+'  # [O-LS0] Oct-14 /scratch comparison removed (files not on Owls)\n'+s[j:])
PY
cp "$REPO/Scripts/Data_generators/gen_dev_data.R" "$WORK/"   # gen_prod_data.R sources gen_dev_data.R next to the running script
PS=${PS:-"500 1000"}
for p in $PS; do for s in 1 2 3 4 5 6; do
  VS=$V; [ $p = 500 ] && VS=$V500
  nice -n 19 Rscript "$VS" "$WORK/$STUDY" $p $s "$GEN" > "$WORK/logs/g2_p${p}_S${s}.log" 2>&1 &
done; done
wait || true
grep -h "CHECKS\|INFO\|FAIL" "$WORK"/logs/g2_p*_S*.log
