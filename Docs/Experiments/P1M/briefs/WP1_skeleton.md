# WP1 — engine skeleton, the INTERFACES contract, data generator, preprocessing, compat scorer (Opus 5.5 builder)
Read BUILD_COMMON.md first. Branch: `exp/P1M-wp1-skeleton`.

## Deliverable 0, FIRST, within your first working session: `Docs/Experiments/P1M/INTERFACES.md`
Four other builders (WP2 setup, WP3 island kernel, WP4 calibration/merge, WP5 eval/driver) start in parallel and code
against it. Write it **directly** into the shared clone at
`/home/fb31/Bayesian-Variable-Selection/Docs/Experiments/P1M/INTERFACES.md` (the department's docs folder; HQ snapshots
it). Later copy it into `engine_v4/` in your branch. Mark it `v0.1 (binding; changes only by the WP1 owner with a
changelog line)`. It must fix, concretely (C++ declarations where useful), from ENGINEERING_SPEC §0-v2 and §1–§3:
1. directory layout of `Scripts/SMC_BVS/engine_v4/` (src/, include/, tests/, tools/, cmake), namespaces, the build
   targets, and the test runner;
2. core types: `Data` (n, p, K, Xs column-major f64, ys, z, diag(G), column stats, kept map), `Partition`, `Tables`,
   `Start`, `Neighbours` (CSR), `Model` (sorted int32 support), `Score` (log m, route, …), the hash (Zobrist as in
   `core/cpp/v3_util.h`);
3. the **uniform addressing API** (spec §0-v2.2 #3; FEASIBILITY §1): the address tuple (seed, role, phase, stage or round,
   particle, position, slot), the counter-based generator (pick one, e.g. Philox4x32-10, and justify), and how compat
   mode maps to the v3 serial xoshiro256** streams (`core/cpp/v3_util.h:47`);
4. `Store` (top-c under a strict order; flat arrays + pool), `Ledger` (events, HPM and provenance, `island_best`,
   logical counters; per-thread instances + a deterministic merge);
5. the records `IslandResult`, `CalibResult`, `FitResult`, and the **binary file formats** of spec §1 (header: magic,
   version, mode, section table with offset, length and sha256), plus the JSON manifest schema;
6. the two arithmetic forms of the scorer (bit form = v3 bits; class A), as one interface;
7. status codes and error handling (spec §6), and threading conventions (OpenMP or std::thread; deterministic
   reductions).
Keep it short and precise (≤ 300 lines). Tell the manager the moment v0.1 is written.

## Then build
- CMake skeleton + test runner; CI-friendly (no network).
- `gen`: data generator for the designs IND, AR(ρ) (one sequential recursion over columns), BLK(b, ρ) and ADJ-OPP (spec
  plan §2.2, OWNER_DECISIONS OD-14), seeded and hashed. It also produces test rows for any column subset (AR by the
  Markov bridge).
- `prep`: standardisation. Compat mode **must reproduce `core/v3_preprocess.R:35-51` bits** (R's two-pass long-double
  mean). If C++ cannot match it, accept R-standardised X as binary input in compat mode and declare the C++ path class A.
  Test both.
- The compat **scorer**, copied from `core/cpp/v3_score.h` (Cholesky route, refactor, QR fallback), Gram-free (entries by
  the sequential sum of `v3_score.h:45-53`). Golden bit tests against `core/` on fixtures at p ≤ 2k.
- **Pinned transcendental functions**: decide whether to bundle exp/log/log1p/lgamma (spec §3; review §4.9). Measure
  whether glibc on Owls already gives the v3.1 record bits. Report.
- Fixtures: a small set of datasets + v3 reference outputs (scores, tables, start mode) generated on Owls from `core/`,
  stored in `engine_v4/tests/fixtures/` (≤ 20 MB in total).
