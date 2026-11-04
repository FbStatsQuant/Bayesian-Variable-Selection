#!/usr/bin/env bash
set -euo pipefail
script_dir="$(cd -- "$(dirname -- "$0")" && pwd)"
cxx_flags=(-std=c++17 -O2 -fno-math-errno -ffp-contract=off -march=x86-64-v2)
g++ "${cxx_flags[@]}" -I"$script_dir/code_39db138" "$script_dir/n9_original/n9_harness.cpp" -o "$script_dir/n9_harness"
g++ "${cxx_flags[@]}" -I"$script_dir/code_39db138" "$script_dir/n9_original/n9_order.cpp" -o "$script_dir/n9_order"
"$script_dir/n9_harness" 20 6 0 20261103 5000 0 0.5 1 > "$script_dir/n9_A.txt"
"$script_dir/n9_harness" 8 6 1 20261105 5000 0 0.5 1 > "$script_dir/n9_cap.txt"
"$script_dir/n9_order" > "$script_dir/n9_order.txt"
# Targeted longer replay after two small p-values in the short AR(1) MC checks.
"$script_dir/n9_harness" 20 6 0 20261103 50000 0 0.5 1 > "$script_dir/n9_A_mc50000.txt"
