# Testing `smcbvs4`

How to run the engine's tests, what each suite covers, how long it takes, what a pass means, how to update the pinned
references legitimately, and the traps. Timings are **MEASURED** on Owls (Xeon Gold 6148, GCC 11.5, 3 threads, `nice -n 19`)
with the engine at commit `9fb28c89` plus this change, at a machine load average of about 21 (Owls is shared, so expect
the times to move by a third either way). Paths are relative to `Scripts/SMC_BVS/engine_v4/`.

Contents: 1 The one command · 2 The suites · 3 What "pass" means · 4 What `run_tests.sh` does not run · 5 Pinned references and
how to update them · 6 The traps · 7 Debugging a failure · 8 Writing a test

---

## 1. The one command

```sh
export TMPDIR=<a scratch directory>          # required; never /tmp. The build goes to $TMPDIR/v4_build
tests/run_tests.sh --list                    # the suites, in order, and the options (needs no TMPDIR, no build)
tests/run_tests.sh --quick --threads 3       # the default; about 25 minutes (§2)
tests/run_tests.sh --full --threads 3        # adds the tagged "full" cases
tests/run_tests.sh --only driver,golden      # just these suites (the build always runs)
```

Owls rules (BUILD_COMMON): `nice -n 19` (the script does it), **at most 3 threads**, one suite at a time.

| option | meaning |
|---|---|
| `--quick` (default), `--full` | the C++ cases tagged `full` (6 of them) and the R golden's extra cases run only with `--full` |
| `--threads k` | `OMP_NUM_THREADS` for every suite (default 3) |
| `--build-dir DIR` | build here instead of `$TMPDIR/v4_build` |
| `--only a,b` | run only these suites: `cpp`, `driver`, `competitors`, `install`, `golden` |
| `--allow-skip` | a SKIPPED suite (R or python3 missing) does not make the run fail |
| `--fixtures` | first regenerate `tests/fixtures` from `core/` (§5.1; needs R) |
| `--allow-missing-fixtures` | do not fail a case whose fixture is missing (otherwise a missing fixture is a FAIL) |
| `--keep` | keep the golden's work directory `$TMPDIR/wp4_golden` for debugging |
| `--list` | print the suites and exit |

The run ends with a table and **one summary line**:

```
== suite summary (quick, 3 threads)
  build        PASS          2 s  …/v4_build
  cpp          PASS       1012 s  198 test cases, 0 failed, 0 check failures
  driver       PASS         14 s  Ran 55 tests in 13.385s
  competitors  PASS         46 s  packages missing here: glmnet, ncvreg, biglasso, L0Learn, susieR, varbvs, BAS, bigmemory
  install      PASS         15 s  23 checks
  golden       PASS        437 s  WP4 golden: 540419 checks, 0 failures
SUMMARY: PASS build 2s | PASS cpp 1012s | PASS driver 14s | PASS competitors 46s | PASS install 15s | PASS golden 437s | total 1526s | exit 0
```

**Exit status:** `0` every suite that was asked for ran and passed · `1` a suite FAILED or the build failed · `2` bad usage
(unknown option or suite, `TMPDIR` unset) · `3` nothing failed but a suite was **SKIPPED** because R (or python3) is missing:
the run is not a full pass. Use `--allow-skip` to accept that on a machine without R; the summary still names the
skipped suite.

## 2. The suites

| suite | what it runs | needs | quick | full |
|---|---|---|---:|---:|
| `build` | `cmake` + `make -j3 smcbvs4 v4_tests v4_pmath_check` into `$TMPDIR/v4_build` | GCC ≥ 11, CMake ≥ 3.20, OpenMP, libquadmath | 110 s cold, 2–4 s warm | = quick |
| `cpp` | `v4_tests`: 198 C++ cases (unit, golden-vs-core, end-to-end) | the build | 1012 s | 2937 s (207 cases) |
| `driver` | `tools/slurm/test_p1m_driver.py`: 55 tests of the SLURM plan driver and its tools | python3 (stdlib) | 14 s | = quick |
| `competitors` | `tools/competitors/test_competitors.sh`: the competitor harness end to end, no installs | R | 46 s | = quick |
| `install` | `tools/competitors/test_install_script.sh`: the install script's guards and offline route, on dummy packages | R | 15 s | = quick |
| `golden` | `tests/golden/wp4_golden.R`: the WP4 calibration, merge and failure paths against `core/`, bit for bit | R with Rcpp, digest, jsonlite | 437 s | 4598 s (2,522,655 checks) |
| **all** | | | **≈ 1,530 s (25 min)** | **≈ 7,600 s (2 h 07 min)** |

The slowest C++ cases (quick): `mem_plan_bounds_measured_peak_2e4` 136 s, `island_command_end_to_end` 87 s,
`island_command_refusals_and_budget` 64 s, the `start_view_*` cases 30–62 s each, `wp4_io_merge_cli_and_driver_manifest`
39 s. Run one alone with `build/v4_tests <part of the name>` (§7).

### 2.1 `cpp`: what the 198 cases cover

| file (under `tests/`) | cases | what it covers |
|---|---:|---|
| `test_sha256`, `test_format`, `test_rng`, `test_gen` | 3, 4, 6, 6 | SHA-256 known answers; the binary container (round trip, corruption, truncation); Philox known answers, address rules, the v3 compat streams; the data generator (thread-invariant bits, moments, truth layout) |
| `test_prep`, `test_score`, `test_pmath` | 7, 4, 1 | `prep` against R's `v3_preprocess` on fixtures; the bit-form scorer against `core/`'s `v3::Scorer`; the pinned libm and its self-test |
| `test_store`, `test_ledger` | 5, 4 | the top-c store and the ledgers: equal to the reference for any offer order or thread count |
| `test_setup`, `golden/golden_setup` | 18, 9 | `setup` (blocks, tables, start law; truncated = exact below the cut; thread and tile invariance) and its golden bits against `core/` |
| `test_island`, `test_island_golden`, `test_start_view`, `test_offer_floor`, `test_island_cmd` | 59, 7, 5, 4, 10 | the island sampler: kernels (bit form = scorer bits, class A ≤ 1e-9), **T3 invariance** (same hash for every thread count, group size, tile), the memory plan, checkpoints and restart, leader stores, the offer floor, the `island` command; golden against `core/`'s engine compiled unchanged |
| `test_wp4`, `test_wp4_io`, `test_merge_mem` | 9, 14, 3 | calibration rules, the merge and its file formats (input validation by content hash), the merge's memory plan against its measured peak |
| `test_cli` | 5 | exit codes, records, manifest refusal, `prep` data outcomes, the libm guard |
| `wp5/test_eval`, `test_golden_v3`, `test_post_e2e`, `test_scale`, `test_t7` | 12, 1, 2, 8, 1 | the evaluator and `post`: quadrature, closed forms, posterior, draws, metrics, thread invariance, the gen → prep → merge → eval path, scale, gate T7 |

(The per-file counts are the `TEST…(…)` macros, 207 in all of which 6 are `full`-only; the run reports the authoritative
number: 198 cases in a quick run.)
The six `full` cases are `wp4_merge_mem_plan_bounds_peak_2e4`, `mem_plan_bounds_measured_peak_1e5`,
`T11_truncated_equals_exact_below_cut_full` and the three `TEST_SLOW` cases of `wp5/` (T7 closed forms against Monte Carlo,
the top-K mixture tail, T7′ at scale).

### 2.2 `golden`: the R side

`wp4_golden.R` copies `core/` into a work directory (never written), compiles it, and compares, **bit for bit**:

1. the coded calibration (`v4::calib::Driver`, rule `coded`) with `core/v3_calib.R::v3_calibrate`, at 1 and k threads;
2. the final run as R′ = 4 process islands + the v4 merge + the threaded tail with `core/v3_run.R::v3_final_run` (v3.1 with
   LS0), on every compared field (only `fresh` counters, cache statistics and timings are not compared);
3. the failure paths (missing, corrupt, hash-mismatched or numerically failed island; failure in the tail): a declared
   status and no estimate field;
4. the bounded rule (I_max = 0 and 1) and blocked sums, end to end (no reference: these are the V changes).

`--full` adds larger cases. It reads **no stored reference file**: the reference is the live `core/`, so there is nothing to
refresh (§5.3).

### 2.3 `driver`, `competitors`, `install`

- `driver`: plan resolution and validation (every rule of ERRORS.md §4), the generated scripts, the fake-sbatch submission
  graph, the local chain with a stub binary, restart chains and T6, the cost tools, the manifest tool, `info --meta`.
  It writes under `$TMPDIR` (and sets `P1M_TEST_ROOT` itself); run directly it needs `TMPDIR` set (§6).
- `competitors`: runs the harness on a small simulated problem; methods whose R package is missing must give a
  `package_missing` record, which `eval` accepts without metrics. "packages missing here: …" in the summary is normal.
- `install`: the install script's guards and its offline route on dummy packages. **Its install part is skipped when
  `TMPDIR` is not inside `$HOME/SMC_Engineering_Department`** (it prints `skip install tests: TMPDIR is not inside …` and
  the check count is lower than 23, and the summary says `PARTIAL`): keep `TMPDIR` inside the department folder to run all
  of it.

## 3. What "pass" means

- **Per suite.** `cpp`: every case passes, `0 failed, 0 check failures` (a case with a missing fixture fails unless
  `--allow-missing-fixtures`). `driver`: `unittest` ends with `OK`. `competitors`: every method is `completed` or
  `package_missing` and `eval` exits 0 for each. `install`: all checks `ok`. `golden`: `WP4 golden: N checks, 0 failures`.
- **The run.** `SUMMARY: … exit 0` with six PASS and no SKIPPED. A run with a SKIPPED suite exits 3 and is **not** a full
  pass; it is acceptable only on a machine without R, and then `--allow-skip` says so on purpose.
- **A pass is evidence, not proof.** The suites test bits against `core/` on small fixtures and the properties of §2.1; the
  large-scale gates (T5 at 10⁵, T6 by real kills, the 10⁶ pilot) are NOTS runs documented in `tools/slurm/T5_AND_PILOT.md`
  and `T6_AND_RESTART.md`.

## 4. What `run_tests.sh` does not run

- **The v3 R regression** of `core/` (`Scripts/SMC_BVS/tests/`: 32 seeds, old core against new, run by
  `run_all_seeds.sh` / `run_suite.sh`; hours, and Root launches it). `Scripts/SMC_BVS/tests/README.md` describes it.
- **R unit tests of added fields.** When the list-renormalised PIP work (PR #68) lands, its R tests
  (`Scripts/SMC_BVS/tests/list_pip_units.R`, 110 checks per its description) belong to that directory, not to this runner;
  the C++ side (`tests/test_list_pip.cpp`) joins the `cpp` suite through that PR's CMake change.
- **Benchmarks** (`tools/bench_*.cpp`, `tools/nots_bench_*.sh`) and the NOTS gates.
- **The documentation replay**: the commands of README.md and REPRODUCIBILITY.md are checked by hand when those documents
  change (the smoke test of README §3 A takes about 4 minutes).

## 5. Pinned references and how to update them

A *pinned reference* is a value the tests compare against that does not come from the code under test. The rule for all of
them: **never refresh a reference to make a test pass.** First find out why it moved. A refresh is a separate commit whose
message says what changed and why the new value is right, and it needs a reviewer.

### 5.1 The fixtures and `tests/fixtures/MANIFEST.json`

`tests/fixtures/` holds reference outputs made by running `core/` (preprocessing, scores, setup tables, …), written by
`tools/make_fixtures.R` and `tools/golden_setup_ref.R`. `MANIFEST.json` records where they came from: the `core/` commit,
the SHA-256 of **each pinned `core/` file** (`reference.core_files_sha256`, 20 files), R, the compiler and the libm.

The test `fixtures_pinned_reference_matches_core` fails, with `core file changed since the fixtures were made: <file>`, as
soon as any pinned `core/` file differs from its recorded hash: the golden tests would otherwise compare against a stale
reference. (The `files` entry of the manifest, the hash of every fixture file, is provenance; no test asserts it.) Three cases:

**(a) `core/` did not change.** Nothing to do.

**(b) `core/` changed additively and cannot change any fixture value** (for example new output fields, as in the list-PIP
change). The fixtures stay; only the recorded hashes move. Check first that the change really is additive: the golden suite
passes unchanged (540,419 checks) and the T3 hashes of REPRODUCIBILITY.md §4.4 are the same. Then update **only**
`reference.core_files_sha256` (and `reference.core_commit`) in the manifest, and say so in the PR. To see what moved:

```python
import hashlib, json
fx, core = "Scripts/SMC_BVS/engine_v4/tests/fixtures/MANIFEST.json", "Scripts/SMC_BVS/core"
ref = json.load(open(fx))["reference"]["core_files_sha256"]
now = {f: hashlib.sha256(open(core + "/" + f, "rb").read()).hexdigest() for f in ref}
print({f: h for f, h in now.items() if h != ref[f]})      # {} on a tree whose fixtures are current (verified)
```

(run from the repository root; `git log -1 --format=%H -- Scripts/SMC_BVS/core` gives the new `core_commit`).

**(c) `core/`'s science changed** (any number a fixture holds). Do not patch hashes. Regenerate:
`tests/run_tests.sh --fixtures` (runs `make_fixtures.R` and `golden_setup_ref.R`, needs R with Rcpp, digest, jsonlite),
review the diff of every changed fixture file and explain each, rerun the whole suite, and get HQ's approval: the bits the
engine is held to have changed.

### 5.2 Pinned hashes and numbers

| value | where it is recorded | what checks it | when it may change |
|---|---|---|---|
| T3 reference hashes: bit `44a15bfc6fb8d233`; class A `d2df149413596a19` (portable) / `e9cc4ab39f8a72db` (x86-64-v3, v4) | REPRODUCIBILITY.md §4.4 | `t3_invariance_*` asserts that **every configuration equals its own reference**; the literal values are checked by the project's pre-release check, not by an `assert` | only when the science of the sampler changes on purpose (HQ) |
| the libm reference hashes of the self-test | `src/common/pmath_info.cpp` (the reference hashes, line ~73), `tests/fixtures/pmath_owls_glibc234_fma.json`, `tests/PMATH_REPORT.md` | every command's self-test; `test_pmath.cpp` | only by re-measuring on a reference machine (`v4_pmath_check`); it changes the libm pin, an HQ decision |
| the island `output_hash` of the smoke test (`0x94b566338ba911de`) | README.md §3 A | by hand when the README changes | when the sampler's output changes on purpose |

### 5.3 The R golden

It compares against the live `core/`, so a failure means the engine and `core/` now disagree. That is a finding to explain
(who is right?), not a reference to refresh.

## 6. The traps

**The stale `TMPDIR` trap.** CMake remembers the source directory a build directory was configured for. A directory left in
`$TMPDIR` by *another checkout* makes the next configure stop with
`CMake Error: The source "…/CMakeLists.txt" does not match the source "…" used to generate cache`. Two directories are
exposed: `$TMPDIR/v4_build` (the build) and `$TMPDIR/wp4_golden/` (the golden's work directory, normally removed after the
run, but left behind by `--keep` or a crash). `run_tests.sh` now checks both before using them and fails the suite with a
clear line (`… was configured for another checkout`) instead of the CMake error. **Fix:** remove the named directory, or use
a fresh `TMPDIR` or `--build-dir`. Worktrees are separate checkouts: give each its own `TMPDIR`.

**Other `TMPDIR` rules.**
- `TMPDIR` unset: `run_tests.sh` exits 2 (`set TMPDIR`). The Python driver tests, run directly, need it too, because the
  sandbox's `/tmp` may be unusable and they then fail with `No such file or directory` on files they just wrote:
  `TMPDIR=<dir> python3 tools/slurm/test_p1m_driver.py`.
- Keep `TMPDIR` inside `$HOME/SMC_Engineering_Department` on Owls to run the whole `install` suite (§2.3).
- Never point `TMPDIR` at `/tmp`.

**Load.** Owls is shared: timings vary with the load (this document's were taken at a load average of about 21), and a
time-limit test can fail under heavy load without a bug. Rerun it alone before concluding anything.

**R missing.** The golden, competitors and install suites are SKIPPED, and the run exits 3 (§1). Do not read a green
`cpp` as a full pass.

## 7. Debugging a failure

- Every suite's output is kept in the build directory: `v4_tests.log`, `wp5_driver_tests.log`, `wp5_competitors.log`,
  `wp5_install.log`, `wp4_golden.log`, and `cmake.log`.
- One C++ case, or all cases whose name contains a string: `$TMPDIR/v4_build/v4_tests <part of the name>` (add `--full` for
  the full-tagged ones). A failing check prints `FAIL <case> (<file>:<line>): …` on stderr.
- One Python test: `python3 tools/slurm/test_p1m_driver.py TestResolve.test_enum_signal` (with `TMPDIR` set).
- The golden's work directory: `--keep`, and remember the stale-directory trap before the next run.
- A threads question: `OMP_NUM_THREADS=1 v4_tests …` and again with 3; a test that only fails at one of them is a finding.

## 8. Writing a test

- C++: `TEST(name) { … CHECK(…); }` from `tests/tk.h`; `TEST_TAGGED(name, "full")` (or `TEST_SLOW` in `wp5/`) for a case
  that belongs only to `--full`. Put it in the file of its component (§2.1).
- Fixtures: the `Fixture F(n, p, seed)` helper of `test_island.cpp` builds a small design.
- **A test must be able to fail.** For new machinery add a *negative control*: a test-only switch that plants the bug the
  new code guards against, and assert that the test notices (`test_bound_shrink`, `test_drop_leader_stage`). A test that
  never reaches the code it is named for passes with the code broken.
- **Assert only what is deterministic.** Counts that depend on the thread schedule (how often a compaction trigger fires)
  may vary from run to run; either assert something that holds for every schedule (`> 0` with a margin the test establishes)
  or remove the dependence (the leader-trigger test uses 1-entry buffers so that every offer flushes at once).
- Owls rules apply to tests too: `nice -n 19`, at most 3 threads, no files outside `TMPDIR`, clean up what you create.
