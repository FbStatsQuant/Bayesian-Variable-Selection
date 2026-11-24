# PR #47 review — WP7 O1

**Verdict: ACCEPT-WITH-FIXES. Finding 1 must be fixed before merge.**

Counts: **0 CRITICAL, 1 MAJOR, 0 MINOR**.

Reviewer: Codex GPT-6.1 Sol, high, independent of the builder. Reviewed on Owls, 2026-11-16.
PR: https://github.com/FbStatsQuant/Bayesian-Variable-Selection/pull/47
Head: `e3ca47160f3d67d9d2d9e178be0e41d592fccb2c` (`exp/P1M-wp7-o1`).
Base: `8b7f89bea4f5c89fa2dcd26a5b87e1b63e359b2d` (`exp/P1M-engine`).

Scope: REVIEW_PR_template.md, WP7 O1, WP3_ARCH_REVIEW lever 1/R4, BUILD_COMMON, ENGINEERING_SPEC §0-v3 and §0-v2, INTERFACES §4/§5/§7, PROTOCOL, relevant D-26–D-30/H-9–H-11 decisions, and the four additional checks in the review request. No source edits, pushes, GitHub comments, sub-agents, or NOTS access.

## Finding

1. **MAJOR — Final-island failure exits can suppress I1 and still write an island file.**

   Location: [island_run.h:699](/home/fb31/.t3/worktrees/Bayesian-Variable-Selection/t3-3411b82b-fa3fdf4171c61017/Scripts/SMC_BVS/engine_v4/src/island/island_run.h:699), with the step-boundary exit at [island_run.h:673](/home/fb31/.t3/worktrees/Bayesian-Variable-Selection/t3-3411b82b-fa3fdf4171c61017/Scripts/SMC_BVS/engine_v4/src/island/island_run.h:673) and file writer at [island_file.cpp:21](/home/fb31/.t3/worktrees/Bayesian-Variable-Selection/t3-3411b82b-fa3fdf4171c61017/Scripts/SMC_BVS/engine_v4/src/island/island_file.cpp:21).

   `check_stores()` before final export is inside `res.status == 0 || res.status == 1 || calib`. A final-role island with internal `IslandRun::status == 3` (`resource_limit`) skips it. The step-boundary budget exit happens before `maybe_ckpt()`, so that checkpoint guard cannot close the gap. Final-role numerical failures also bypass this final guard. `write_island_file()` accepts these failure results.

   **Reproduced at the pinned head:** AR(0.6), n=100, p=300, data seed 43; run seed 42, island 3, N=48, grid `{0,.05,.15,.35,.65,1}`, L=Hm=2, B=14, label-major, G=16, 3 threads. Use the existing `small_cfg()` and `Fixture` helpers in `tests/test_island.cpp`:

   ```cpp
   Fixture F(100, 300, 43);
   IslandConfig c = small_cfg();
   c.kernel = KernelKind::LabelMajor; c.threads = 3; c.G = 16;
   c.test_admission_k = .5;
   c.mem_budget = plan_island(F.D, F.st, c).total + 1024;
   c.test_corrupt_store_step = 1;
   auto r = run_island<Arith::ClassA>(F.D, F.st, F.nb, c);
   // Observed: r.status == 3, r.ks.store_checks == 0.
   write_island_file(scratch_path, r, Arith::ClassA, v4::Json::object());
   // Observed: a resource_limit island file is written.
   ```

   The log reports predicted peak **21 MiB > budget 13 MiB after step 1**, `checks=0`, and a written island file. With the same configuration plus `check_store_each_step=true`, execution throws `Status::internal_error` (enum value 5): `store invariant I1 violated (top store)`.

   The failure file has an **empty top store and no estimates**; GUARD-W holds. This finding is the suppressed invariant violation and missing mandatory check, **not a claim that a corrupt top-store payload was exported**. It violates the explicit extra requirement that resource-limit paths writing the final island file run I1 first, and the contract that invariant violations yield `internal_error`. Before O1, the per-step check preceded the budget exit.

   **Suggested fix:** run the final `check_stores()` on every engine exit with live stores, after failure cleanup and before result handoff, independently of the conditional that controls exporting store contents. Keep failure-output/estimate filtering intact. An admission refusal before constructing an engine has no live store to validate. Add regression cases for a valid and corrupted store on the step-budget and caught-OOM exits; retain the stop/checkpoint cases. A corrupted live store must raise `internal_error` before a failure file can be written.

## Independent validation

All builds/tests used Owls (`owls.stat.rice.edu`, Xeon Gold 6148), gcc 11.5.0, glibc 2.34, portable `-march=x86-64-v2`, `-O2 -fno-math-errno -ffp-contract=off`, `nice -n 19`, build parallelism ≤3 and `OMP_THREAD_LIMIT=3`. One test suite ran at a time. Scratch, compiler temporaries, archives, builds, and test files were under the review worktree's root `.rc_tmp/` and were removed after recording these results. The existing runner requires `TMPDIR`; it was scoped to that scratch directory.

**Required runner:**

```bash
env TMPDIR="$PWD/.rc_tmp/head_tmp" OMP_THREAD_LIMIT=3 \
  OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 nice -n 19 \
  bash Scripts/SMC_BVS/engine_v4/tests/run_tests.sh \
  --quick --threads 3 --build-dir "$PWD/.rc_tmp/head_build"
```

- Initial C++ run: **118 cases, 117 passed, 1 failed, 2 check failures**, both from `wp4_io_merge_cli_and_driver_manifest`. Its driver subprocess refused worktree scratch outside the normal department root because `P1M_TEST_ROOT` was unset (exit 64), then the expected manifest was absent.
- Reran **only that failed case** with `TMPDIR=P1M_TEST_ROOT="$PWD/.rc_tmp/head_tmp"` and the same thread limits/niceness: **1 case, 0 failures**. All 118 C++ cases therefore passed across the suite and this environment-only rerun; the initial runner itself exited 1. The corresponding case also passed on the clean base build with the scratch-root setting. This is not graded as an O1 regression.
- WP4 reference goldens: **528,081 checks, 0 failures**. WP5 driver: **17 tests passed**; competitor harness and installation guards: **passed** (optional competitor packages absent, as reported by the harness).
- T6 restart, forced kill during write, resubmission/refusal, bit and class-A T3, store tests, addressed/compat island goldens, and calibration success/failure-prefix goldens: **passed**. The golden tests compile unchanged `core/` headers and the WP4 harness compares against the actual v3 calibration/final-run reference, rather than comparing O1 with itself. Existing cases cover ties, empty supports, cap moves, scorer routes, constant columns and failure paths.

**Clean base:** extracted only the committed `Scripts/SMC_BVS/engine_v4` and `Scripts/SMC_BVS/core` trees with `git archive 8b7f89be`, built from scratch using CMake Release and `-j3`, then ran `v4_tests t3_invariance`. Parent-worktree Git discovery was disabled for that archive build. Source files in the archive were unchanged.

| Check | Clean base | O1 default | O1 each-step |
| --- | --- | --- | --- |
| T3 bit reference, data seed 21 | `44a15bfc6fb8d233` | `44a15bfc6fb8d233` | — |
| T3 class-A reference, data seed 21 | `d2df149413596a19` | `d2df149413596a19` | — |
| Independent island bit, data seed 43 | `d54f6fad9ab38ef7` | `d54f6fad9ab38ef7` | `d54f6fad9ab38ef7` |
| Independent island class A, data seed 43 | `361f80e6f6c147b6` | `361f80e6f6c147b6` | `361f80e6f6c147b6` |

T3 passed all eight PM/LM, thread-count, group-size and tile-size configurations in each form at both commits. The independent island used the configuration in finding 1 without budget/corruption overrides. Default checking ran once; each-step checking ran nine times.

For each arithmetic form, all **26 non-metadata sections** of the serialized island files have identical names, types, dimensions, lengths and payload SHA-256 values across base/default/each-step. Each payload digest was recomputed from file bytes. SHA-256 of the sorted section manifest:

- Bit: `6bfc2053a2419ff627eb1af84387520733be184c4ef65ec4dfd72295313c9642`.
- Class A: `13dc1158191cbb5bdef5c509c58241e8d91114073b240a95622b436370b6af58`.

Metadata contains build provenance and measured timings. These comparisons follow the contract's exclusion of metadata from cross-build bit comparisons.

## Additional checks and scope

- **Top and leader stores:** `check_stores()` explicitly checks top, lead0 and lead1. An independent internal-engine probe corrupted each store separately after advancing its generation; `save_ckpt()` rejected each with the appropriate I1 `internal_error`, before creating the checkpoint. A second call on unchanged generations skipped repeat scans. All checkpoint writes pass through `save_ckpt()` and its guard before `fopen()`. A corrupted stop-after-step run was also refused. Normal final export and calibration failure-prefix export are guarded. Final-role failure outputs have the exception in finding 1.
- **Parallel predicate:** independent probes made **594 serial/parallel comparisons**, using both orders, empty/singleton stores and sizes up to 4,099, ties, deliberate hash collisions, order violations, duplicate models, over-cap stores and broken index slots, including partition boundaries. Actual worker counts were 1, 2 and 3. Results agreed throughout. The PR's larger, 60k-cap tests passed too; their requests for 5/8 workers were capped by the review's three-thread limit.
- **Races, determinism, allocation:** the new loop only reads the quiescent published run and index; each adjacent-order comparison and lookup contributes to a Boolean AND reduction. This gives the same predicate for any partition/thread count, with no floating-point reduction or ordering dependence. Call sites follow joined worker regions and ledger synchronization. An independent `operator new` probe recorded **0 C++ allocations in the parallel check**; inspection of the loop and its callees found no worker allocation or mutation. No ThreadSanitizer run or 96-thread execution is claimed.
- **Step path:** source search found no serial invariant call in `src/island/`; the only remaining serial delegation is `threads <= 1` inside `check_invariant_parallel()`. Default `check_store_each_step=false` removes checking from the normal step path. The debug/benchmark flag intentionally restores that placement.
- **Scale and discipline:** the new signed 64-bit iteration index safely covers top cap 40,000,001 and leader caps 20,000,000 at p=10⁶. The checker adds no per-entry scratch or copied store. All five changed files are inside `engine_v4/`; no `core/`, arithmetic flags, file-format definitions, hard-coded machine paths or >50 MB files were introduced. `git diff --check` passed. Production-size timing and the ≈56 ns·CPU/pair saving were not remeasured; the SPR/T5 measurement remains a later gate.

The successful-run bit-preservation and parallel-check requirements pass. The mandatory failure-path coverage requires finding 1's fix.
