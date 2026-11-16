# engine_v4 — large-p SMC-BVS engine (P1M)

Contract between work packages: **[INTERFACES.md](INTERFACES.md)** (binding; copy of
`Docs/Experiments/P1M/INTERFACES.md`). Spec: `Docs/Experiments/P1M/ENGINEERING_SPEC.md` (§0-v2 first).
Reference engine: `../core/` (v3.1 / revision D), **never edited**; copied code cites `core/...:line`.

## Build and test
```sh
export TMPDIR=<your tmp>                       # never /tmp
tests/run_tests.sh [--quick|--full] [--threads 3] [--build-dir DIR] [--fixtures]
```
Targets: `v4_bit` (bit flags `-O2 -fno-math-errno -ffp-contract=off -march=x86-64-v2`), `v4_a` (class A; `-DV4_WIDE_ISA=ON`
for x86-64-v3), `smcbvs4` (CLI), `v4_tests`, `v4_pmath_check`, `v4_bench_score`, `v4_bench_store`. Requires GCC ≥ 11, CMake ≥ 3.20, OpenMP,
libquadmath (tests only). R (Rcpp, digest, jsonlite) is needed only to regenerate fixtures.

## WP1 contents (status)
| component | where | status / evidence |
|---|---|---|
| container format (header, sections, SHA-256, atomic write, mmap reader) | `include/v4/format.h`, `src/common/format.cpp`, `sha256.cpp` | unit tests (round trip, corruption, truncation) |
| JSON, manifests, statuses, CLI, binary block + libm guard | `json.h`, `status.h`, `provenance.h`, `src/cli/main.cpp` | CLI tests: exit codes 0 / 10+status / 20-21, manifest refusal, guard |
| uniforms: Philox4x32-10 addresses; v3 xoshiro compat streams; `CheckedSource` (I5) | `include/v4/rng.h` | Random123 KAT vectors; v3 stream equality; I5 checks |
| Store (flat top-c, staging merge, monotone cut-off), island Ledger + ThreadLedger (bounded buffers) | `store.h`, `ledger.h` | equal to `v3::TopStore` for any order; threaded ThreadLedgers = serial ledger; `tools/bench_store.cpp` |
| compat scorer `Scorer<Arith::Bit>` (Gram-free) | `score.h`, `src/common/score.cpp` | bit-equal to core headers and to R-compiled `cpp_score`; all routes forced |
| `gen` (IND, AR, BLK, ADJ-OPP; test rows for any column subset) | `gen.h`, `src/common/gen.cpp` | thread-invariant bits; moments; truth layout |
| `prep` (R's v3_standardise arithmetic, class B) + `--from-r` fallback | `prep.h`, `src/common/prep.cpp` | bit-equal to R `v3_preprocess` on 5 fixtures incl. an anchored column |
| pinned libm decision | `pmath.h`, `tests/PMATH_REPORT.md` | glibc 2.34 FMA variant + run-time guard |
| fixtures from core/ | `tests/fixtures/` (12.8 MB), `tools/make_fixtures.R`, `tools/v4_read.R` | MANIFEST.json with hashes |
| stubs for WP2–WP5 entry points | `include/v4/stubs.h`, `src/stubs/stubs.cpp` | link from day one |

Fixtures for WP2 (setup objects from `v3_setup`: blocks, `log_r`, start law, neighbours, 2,000 π₀ draws on stream 200)
are in `tests/fixtures/setup/` (format in `index.json`; indices internal 0-based).
