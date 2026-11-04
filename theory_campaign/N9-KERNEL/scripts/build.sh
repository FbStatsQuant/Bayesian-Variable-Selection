#!/bin/bash
# Build the N9 harnesses against the production headers with the production compiler flags (core/cpp/Makevars.v3).
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
repo="$(cd "$here/../../.." && pwd)"
inc="$repo/Scripts/SMC_BVS/core/cpp"
out="${1:-$here/../_build}"
mkdir -p "$out"
FLAGS="-std=c++17 -O2 -fno-math-errno -ffp-contract=off -march=x86-64-v2"
g++ $FLAGS -I"$inc" "$here/n9_harness.cpp" -o "$out/n9_harness"
g++ $FLAGS -I"$inc" "$here/n9_order.cpp" -o "$out/n9_order"
echo "built in $out"
