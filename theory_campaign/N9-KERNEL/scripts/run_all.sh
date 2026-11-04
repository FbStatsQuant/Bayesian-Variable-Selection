#!/bin/bash
# Run every N9 check sequentially (one core). Launch through owls_run:
#   ~/.config/bvs-hq/owls/owls_run -j 1 -- bash theory_campaign/N9-KERNEL/scripts/run_all.sh
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
res="$here/../results"; bld="$here/../_build"
mkdir -p "$res"
bash "$here/build.sh" "$bld"
"$bld/n9_order"                         > "$res/order.txt"
# n p design seed nmc phis
"$bld/n9_harness" 20 6 0 20261103 200000 0 0.5 1 > "$res/A_n20_p6_ar1.txt"
"$bld/n9_harness" 20 8 1 20261104 100000 0 0.5 1 > "$res/B_n20_p8_factor.txt"
"$bld/n9_harness" 10 8 1 20261105 100000 0 0.5 1 > "$res/C_n10_p8_factor_capK5.txt"
echo done
