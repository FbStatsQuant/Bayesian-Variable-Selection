# Numerics: build and regeneration (W1-N1)

Toolchain used (2026-11-08): Rtools45 `x86_64-w64-mingw32.static.posix` g++ 14.3.0; Python 3.13 with numpy 2.3.

```sh
# from Theory_work/Wave1/W1-N1/numerics/cpp
export PATH=/c/rtools45/x86_64-w64-mingw32.static.posix/bin:$PATH
CODE=../../../../../Scripts/Campaigns/2026-10-28_New_Campaign/code/core/v2_2_1/core/cpp   # production headers (unmodified)
g++ -O2 -std=c++17 -I instr -I $CODE n1_harness.cpp -o n1_harness_v2.exe
#   instr/v3_engine.h = production v3_engine.h + the 2 read-only lines in instr.diff; all other headers from $CODE.
#   Check: sha256sum $CODE/*.h  vs  production_headers.sha256

# from Theory_work/Wave1/W1-N1/numerics ; SP = any scratch directory
for d in 0 1 2 3 4 5 6 7 8 9; do mkdir -p $SP/d$d; ./cpp/n1_harness_v2.exe export $d $SP/d$d > $SP/d$d/export.log 2>&1; done
for d in 0 1 2 3 4 5 6 7 8 9; do py -3.13 n1_exact.py $SP/d$d; done            # asserts tolerances
for d in 0 1 2 3 4 5 6 7 8 9; do py -3.13 n1_mc.py $SP/d$d 2 200000; py -3.13 n1_mc.py $SP/d$d 8 50000; done
PYTHONIOENCODING=utf-8 py -3.13 make_results.py --archive $SP                  # copies small outputs to json/, hashes all
```

Everything is deterministic: data seeds `seed_stream(1000 + id, 777)`, pilot stream `seed_stream(5000 + id, 0)`, Monte
Carlo island r = 0, 1, … uses `seed_stream(70000 + 100·id + N, 10 + r)` (an independent stream per island under H-U; not
the production 9 + r labelling, which only matters for reproducing a production run). Budget reading: the protocol's
"simulations ≤ 20 seeds" is read as ≤ 20 design seeds (10 here); each design uses 2·10⁵ (N = 2) and 5·10⁴ (N = 8)
independent island streams. Kernel binaries (`K_*.bin`, up to ~100 MB per design) and raw
Monte Carlo endpoints (`mc_*.bin`) are not archived; their SHA-256 are in `json/MANIFEST.sha256`. `make_results.py` without
arguments rebuilds RESULTS.md from `json/` alone.
