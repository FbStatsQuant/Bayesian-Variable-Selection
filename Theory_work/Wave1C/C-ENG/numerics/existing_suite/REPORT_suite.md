# C-ENG: existing regression harness `Scripts/SMC_BVS/tests`, run locally (Windows), seed indices 1, 2, 3

Date: 2026-11-08/09. Worktree `t3-68de3711`, branch `w1c/ls0-merge`. Harness = tests dir as in the worktree (unmodified); reference = `Scripts/SMC_BVS/reference/prototype_core`.
Each configuration was run per seed index (1, 2, 3 = method seeds 1, 2, 3 from `seeds.tsv`), each into its own new output dir. Wall time per (config, seed) is about 6 s once the C++ cache was built (the first compiles dominated).

## Configurations (production core under test)
| | production core | source |
|---|---|---|
| A | ORIGINAL core, commit f16ce15 | `git archive f16ce15 Scripts/SMC_BVS/core` piped to `tar -x` into scratch `.../scratchpad/suite/coreA` |
| B | NEW core, switch default OFF | copy of worktree `Scripts/SMC_BVS/core` in `.../suite/coreB`; `getOption("v3.ls0", TRUE)` replaced by `getOption("v3.ls0", FALSE)` in `v3_run.R` (2 places: `v3_run_settings`, `v3_final_run`) and `v3_fit.R` (1 place) |
| C | NEW core unchanged (switch ON) | copy in `.../suite/coreC`; `diff -r` against the worktree core: only `README.md` differs (line endings CRLF/LF), all code files identical |

## What ran (per config, per seed): manual port of `run_suite.sh`
`tools/run_cfg.sh PRODUCTION_CORE OUTDIR INDEX` (copy in `tools/`):
1. `python prep_wrap.py prepare.py prepare OUT --prototype ... --production ... --tests ... --index N`
2. `Rscript --vanilla worker.R <OUT/sources/prototype> prototype OUT/prototype N <OUT/sources/tests>`, and the same for `production` (these two ran concurrently = 2 R processes; compare and audit ran afterwards)
3. `Rscript --vanilla compare.R OUT <frozen tests>`
4. `python prep_wrap.py prepare.py finish OUT`
5. `python summarize.py <config dir> --indices 1,2,3`

Environment as in run_suite.sh: `OMP/OPENBLAS/MKL_NUM_THREADS=1`, `MAKEFLAGS=-j1`.

## Substitutions / workarounds (the harness and core were not edited; only B's switch default differs)
- Skipped the `hostname -f` owls check and the `nice -n 19` re-exec (no nice on Windows); `python` instead of `python3`.
- `prepare.py` uses `os.getpriority` (absent on Windows) and runs `lscpu` (absent). Wrapped by `tools/prep_wrap.py`, which stubs `os.getpriority` to 0 and tolerates a missing command. `manifest.json` "priority" is therefore 0 and `environment.txt` lacks `lscpu`. `uname` and `R --version` are recorded. `g++ --version` on PATH is the 32-bit MinGW 16.2 in `/c/mingw64`, NOT the Rtools45 g++ 14.3 that R actually compiles with, so the compiler string in the cache identity hash is the PATH one.
- `worker.R` calls `ps -o ni=`, which only produces a warning (empty `priority` metadata). The `/proc/self/status` warnings in worker logs (memory probes) are harmless and did not change any check outcome.
- Windows MAX_PATH: `Rcpp::sourceCpp(cacheDir=<scratch>/shared_compile_cache/<64-hex key>/cache/...)` exceeded 260 characters. The shared compile cache (`V3_TEST_COMPILE_CACHE`) was therefore placed at the short path `C:/Users/felip/AppData/Local/Temp/v3c` (deleted afterwards), and the nested `cache/sourceCpp-x86_64-w64-mingw32-1.1.2` directory was pre-created by `tools/warm.R`, which also precompiled all cores. Cache keys are content hashes, so semantics are unchanged. The cache was shared by all three configs (prototype key; A's key; B and C share one key since only R files differ between B and C). It is not part of the evidence dirs, so `summarize.py` wrote no `compile_cache_sha256.json`.
- The prototype worker was run separately in each config (3 times per seed), not reused.
- Compile flags: `Makevars.v3` (`-O2 -fno-math-errno -ffp-contract=off -march=x86-64-v2`) via `R_MAKEVARS_USER` as designed. The platform is Windows/MinGW (R 4.6.1, Rtools45 gcc 14.3), not Owls Linux/R 4.6.0/gcc 11.5, so the bit comparison is between two builds on the same toolchain only.

## Results (all three seeds gave identical pass/fail patterns)
Per seed: `compare.R` has 28 checks; the production worker registers 41 unit labels (config A) and the prototype worker 9.

| config | compare checks, seeds 1 / 2 / 3 | production worker units | `summarize.py` |
|---|---|---|---|
| A (orig f16ce15) | 28/28 PASS, 28/28, 28/28 | 41 PASS, 0 FAIL | **PASS** (3/3 seeds) |
| B (new, ls0 OFF) | 27 PASS + 1 FAIL, each seed | 40 PASS, 1 FAIL | FAIL (3/3 seeds) |
| C (new, ls0 ON) | 27 PASS + 1 FAIL, each seed | 39 PASS, 2 FAIL | FAIL (3/3 seeds) |

The single failing `compare.R` check in B and C is `production_all_units` (it aggregates unit failures). All 26 other bit-for-bit checks (`bits_pre` through `bits_final_outputs_and_flags`, `inputs_and_seed_identity`, `prototype_*`) PASS in B and C. The prototype worker exits 0 in all configs; the production worker exits 1 only because of the failed unit(s).

## Failing checks and classification (identical for seeds 1, 2, 3)
| config | failing unit | cause (verified) | classification |
|---|---|---|---|
| B, C | `production_api_has_no_test_controls` ("root value differs") | First line `exact(names(formals(v3_fit)), c("X","y","seed","allocation"))`: `v3_fit` now has the extra formal `ls0` (`X y seed allocation ls0`). The remaining assertions of that unit (excluded R/C++ profiling interfaces, no `hooks`/`B_override`) were evaluated separately on the B and C copies (`tools/api_rest.R`) and all PASS. | EXPECTED: new documented public switch argument. B fails it too because B only flips the default. The harness line needs `"ls0"` added if the switch stays. |
| C only | `v2_inherited_rescore_failure_retains_hpm_and_is_contained` ("root attributes differ") | First stop at `exact(z$ledger$logical, injected$ledger_before$logical)`: the failed-return ledger has an extra counter row `ls0` (11 vs 10 rows, dimnames differ); same for `$fresh`. Re-running the unit (`tools/repro_rescore.R`) with the `ls0` row dropped from both ledger matrices and the "no estimates" check relaxed to "all NA" (`pip_primary` and `log_Z` are scalar `NA` instead of `NULL`, `estimates_available` FALSE): the entire rest of the unit PASSES. | EXPECTED LS0 difference: the `ls0` counter row is serialised only when LS0 is on, and the GUARD-W/#15 NA estimate fields replace `NULL`. B passes this unit, confirming it depends on LS0 being on. |

Unexpected failures: none.

## Caveats on coverage
- The harness drives the C++ through test wrappers (`test_final` calls `cpp_final_run(setup, grid, ro, seed, ...)` with a hand-built `ro` that has no `ls0`), so LS0 itself is NOT executed in config C. The production LS0 path (v3_final_run to cpp_final_run with `ro$ls0`) is not exercised, and the "final HPM may improve" difference cannot show up. That is why every `bits_*` check (including `bits_final_outputs_and_flags`, `bits_raw_final`, `bits_calibrated_final`) passes in C. What is exercised in C is the changed `v3_start.h` (tie-aware DP in `start_mode`, bit-equal on these seeds' start tables), the changed `v3_ledger.h`/`v3_engine.h`/`v3_runtime.h`, and the R assembly/failure-return changes.
- Only seed indices 1-3 of 32 were run (9 harness runs); this is not the 32-seed gate. The platform differs from the documented Owls environment.
- B passing everything except the API signature line shows the `ls0 = FALSE` path reproduces the original behaviour on these checks.

## Output paths
Root: `Theory_work/Wave1C/C-ENG/numerics/existing_suite/`
- `A_orig_f16ce15/seed_{1,2,3}/`, `B_new_ls0off/seed_{1,2,3}/`, `C_new_ls0on/seed_{1,2,3}/`: each holds `REPORT.md`, `comparison.json`, `exit_status.tsv`, `compare.log`, `prototype|production/{worker.log, raw_results.rds, unit_results.rds, ...}`, frozen `sources/`, `manifest.json`, `output_sha256.json`, `source_validation.json`.
- `<config>/SUITE_SUMMARY.{md,json}` (summarize.py with `--indices 1,2,3`): A PASS; B and C FAIL (reasons above).
- `tools/`: `run_cfg.sh`, `chain.sh`, `prep_wrap.py`, `warm.R`, `repro_rescore.R`, `api_rest.R`.
- Scratch (outside the repo): `C:\Users\felip\AppData\Local\Temp\claude\7f4deb75538d3cf7\03611146-335e-4730-9f01-d3ebd88e845b\scratchpad\suite\` (core copies A/B/C).

No tracked file was edited and no state-changing git command was run. The worktree has since gained commits from other sessions (e.g. `bc62795`); the core code is identical to the copy used for B and C.
