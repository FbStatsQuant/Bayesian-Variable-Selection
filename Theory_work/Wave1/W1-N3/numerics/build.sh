#!/bin/sh
# Build the harness against the frozen header (read-only include path). SSE2 doubles, no FMA contraction.
FROZEN=../../../../Scripts/Campaigns/2026-10-28_New_Campaign/code/core/v2_2_1/core/cpp
g++ -O2 -std=gnu++17 -D_USE_MATH_DEFINES -msse2 -mfpmath=sse -ffp-contract=off -I"$FROZEN" sm_harness.cpp -o sm_harness.exe
