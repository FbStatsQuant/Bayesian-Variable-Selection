# PR #54 re-check (fix round): MERGE

Reviewer: Claude Sonnet 5.5, read-only re-check. Branch `exp/P1M-wp7-o6`; reviewed head `33fd9dd9`, new head `f00a3c784943a91deba362b90f2db1626077bcec` (the binary's recorded `git_commit` is this SHA). The checked-out tree was clean.

The three findings of [PR54_review.md](/home/fb31/Bayesian-Variable-Selection/Docs/Experiments/P1M/reviews/PR54_review.md) (2 MAJOR, 1 MINOR) are closed. Science invariance holds. The quick suite is green. No new CRITICAL or MAJOR finding. Two non-blocking notes are at the end.

Scope: `git diff 33fd9dd9 f00a3c78` is 6 files (+167/−13): INTERFACES.md, `include/v4/wp4_io.h`, `src/island/island_cmd.cpp`, `src/merge/wp4_io.cpp`, and two test files. All of it is in `engine_v4/`. `git diff --check` is clean.

Sandbox: scratch, build and TMPDIR are under `<worktree>/.rc_tmp/` (`TMPDIR=.rc_tmp/tmp`, `P1M_TEST_ROOT=$TMPDIR`). The only files read from outside this worktree are the reviewer's p = 80 fixtures (data, setup, calib, islands), copied read-only into `.rc_tmp/fx/`. Nothing was deleted, no sub-agents, no push, no source edits; tests ran at nice 19 with 3 threads.

## 1. MAJOR-1 — the island command validates τ_cal before any island work: FIXED

[island_cmd.cpp:230-235](/home/fb31/.t3/worktrees/Bayesian-Variable-Selection/t3-85c766ee-cf9abaf943992d2b/Scripts/SMC_BVS/engine_v4/src/island/island_cmd.cpp:230) calls `wp4io::check_calib_tau_cal` for V-mode calibrations. This is the same function `read_calib` now calls ([wp4_io.cpp:320](/home/fb31/.t3/worktrees/Bayesian-Variable-Selection/t3-85c766ee-cf9abaf943992d2b/Scripts/SMC_BVS/engine_v4/src/merge/wp4_io.cpp:320)). It runs after the data and setup dimensions are known and before the budget and admission checks, the plan and the run.

The probe re-ran the reviewer's p = 80 calibration (4,801 inherited models, c = 3,201, τ_cal = `0xc05d7f5402337894`). Each tampered file was written with recomputed container hashes. The island CLI is `smcbvs4 island … --mode V --seed 77 --island 1`. The probe is [recheck_probe.cpp](/home/fb31/.t3/worktrees/Bayesian-Variable-Selection/t3-85c766ee-cf9abaf943992d2b/.rc_tmp/recheck_probe.cpp) and its output is [recheck_probe.log](/home/fb31/.t3/worktrees/Bayesian-Variable-Selection/t3-85c766ee-cf9abaf943992d2b/.rc_tmp/recheck_probe.log).

| calib.bin | `read_calib` | island CLI |
|---|---|---|
| valid (control) | accepted, τ = `0xc05d7f54…` | exit 0, island file written |
| τ = next ulp toward zero | `invalid_input` | **exit 13, no island file** |
| τ = next ulp away from zero | `invalid_input` | exit 13, no file |
| τ = 1e6 | `invalid_input` | exit 13, no file |
| τ = −∞ (while ≥ c distinct models exist) | `invalid_input` | exit 13, no file |

Memory: the check reads the models straight from the mapped file. It makes no per-model copies and does not expand the stores. It does copy the F values (see note 1). It needs the `inh_ptr`, `inh_idx` and `inh_F` arrays. Nothing else is read on the island path.

## 2. MAJOR-2 — distinct inherited models: FIXED

`check_calib_tau_cal` ([wp4_io.cpp:251-278](/home/fb31/.t3/worktrees/Bayesian-Variable-Selection/t3-85c766ee-cf9abaf943992d2b/Scripts/SMC_BVS/engine_v4/src/merge/wp4_io.cpp:251)) first validates every row. It then proves the models distinct: a linear check that the list is strictly increasing in lex order (the exporter's canonical order), else a sort of the row indices that rejects any equal pair. It compares the declared τ_cal bit for bit with `tau_cal_of(F, 40p+1)`, which is the c-th best F over those distinct rows and −∞ when fewer than c.

All duplicate files below carry τ_cal as computed from the row count, which is the strongest tamper, with container hashes valid. Every one is refused by both `read_calib` and the island CLI (exit 13, no island file). The `read_calib` reason is "inherited models are not distinct (D-29: tau_cal is over distinct models)".

| calib.bin (4,801 rows unless stated) | `read_calib` | island CLI |
|---|---|---|
| one model repeated 4,801 times (the reviewer's case) | refused | exit 13 |
| two models alternating | refused | exit 13 |
| all 4,801 distinct plus 3 repeats at the end (separated) | refused | exit 13 |
| canonical order with one adjacent repeat | refused | exit 13 |
| 3,100 distinct + 1,701 repeats (the row count would give a finite τ) | refused | exit 13 |
| the same 4,801 models in reverse order | **accepted**, τ unchanged | exit 0 |
| the same models in a shuffled order | **accepted**, τ unchanged | exit 0 |
| 3,100 distinct rows (< c), τ = −∞ | accepted, τ = −∞ | exit 0 |
| 3,100 distinct rows (< c), finite τ | refused | exit 13 |

The regression tests added by the builder ([test_island_cmd.cpp:272](/home/fb31/.t3/worktrees/Bayesian-Variable-Selection/t3-85c766ee-cf9abaf943992d2b/Scripts/SMC_BVS/engine_v4/tests/test_island_cmd.cpp:272), [test_offer_floor.cpp:291](/home/fb31/.t3/worktrees/Bayesian-Variable-Selection/t3-85c766ee-cf9abaf943992d2b/Scripts/SMC_BVS/engine_v4/tests/test_offer_floor.cpp:291)) cover the same patterns and pass.

**The normal exporter always passes.** `calibrate` writes the inherited export through `InheritedFlat`, built from `sorted_unique_models({top, lead0, lead1}, false)` ([calib_run.cpp:98](/home/fb31/.t3/worktrees/Bayesian-Variable-Selection/t3-85c766ee-cf9abaf943992d2b/Scripts/SMC_BVS/engine_v4/src/calib/calib_run.cpp:98) and [calib_backend.h:81](/home/fb31/.t3/worktrees/Bayesian-Variable-Selection/t3-85c766ee-cf9abaf943992d2b/Scripts/SMC_BVS/engine_v4/include/v4/calib_backend.h:81)). That is sorted lexicographically with `std::unique` applied. Confirmed on the file: the reviewer's p = 80 `calibrate` output is strictly lex-increasing, so the linear scan passes and no sort is needed. All 169 suite cases that calibrate and then `read_calib` or run `island` pass. **`calibrate` never writes duplicates.**

The legacy non-flat writer branch (`CalibWrite::inherited`) is not guarded against duplicates, but production `calibrate` does not use it. The reader would refuse such a file.

## 3. MINOR — merge refuses a `meta.mode` that disagrees with the header: FIXED

`head_island` ([wp4_io.cpp:394-397](/home/fb31/.t3/worktrees/Bayesian-Variable-Selection/t3-85c766ee-cf9abaf943992d2b/Scripts/SMC_BVS/engine_v4/src/merge/wp4_io.cpp:394)) now refuses a `meta.mode` different from the container header's mode. It also refuses a finite floor unless `meta.mode` = "V". The probe merged the reviewer's three floored p = 80 islands (V header, finite floor) with island 2's metadata rewritten, via `merge::run`. See [recheck_merge_probe.log](/home/fb31/.t3/worktrees/Bayesian-Variable-Selection/t3-85c766ee-cf9abaf943992d2b/.rc_tmp/recheck_merge_probe.log) and [recheck_merge_probe.cpp](/home/fb31/.t3/worktrees/Bayesian-Variable-Selection/t3-85c766ee-cf9abaf943992d2b/.rc_tmp/recheck_merge_probe.cpp).

| island 2 | merge result |
|---|---|
| unmodified | completed, estimates available |
| `meta.mode` = law, finite floor (the reviewer's case) | `invalid_input`, no estimates |
| `meta.mode` = compat, finite floor | `invalid_input`, no estimates |
| `meta.mode` = law, floor removed (header-vs-meta mismatch only) | `invalid_input`, no estimates |
| `meta.mode` = V, finite floor | completed |
| `meta.mode` = V, floor removed (−∞) | completed (a −∞ floor is always safe) |

The builder's test also covers the law and compat rewrites and passes.

## 4. Science invariance: holds

- **Builder's end-to-end test, on the quick suite:** `island_command_offer_floor_on_off` (p = 30, τ_cal = −75.091292, islands floored through the CLI; fit.bin identical with and without the floor) PASS. `offer_floor_end_to_end_merge`: the floor dropped 1,599,395 offers over 3 islands and all 41 `fit.bin` science sections are identical (HPM, log Z_r, PIPs, merged store, tail), PASS. The new `island_command_refuses_tampered_tau_cal` PASS.
- **Independent p = 80 re-check, new head:** the floored island (floor `0xc05d7f54…`) was compared section by section, bytes, against the same island with `--offer-floor 0`: all 26 non-meta sections identical, including every `top_*` section. Only `cost`, `offer_floor*` and `timings` differ in meta. It was also compared against the reviewer's floored island written by the old head: all 26 sections identical. Only `binary`, `cost` and `timings` differ in meta. The fix round does not change any science section. This uses [recheck_cmp.cpp](/home/fb31/.t3/worktrees/Bayesian-Variable-Selection/t3-85c766ee-cf9abaf943992d2b/.rc_tmp/recheck_cmp.cpp).

## Test run

```
export TMPDIR="$PWD/.rc_tmp/tmp" P1M_TEST_ROOT="$PWD/.rc_tmp/tmp" OMP_NUM_THREADS=3
nice -n 19 bash Scripts/SMC_BVS/engine_v4/tests/run_tests.sh --quick --threads 3
```

Owls, GCC 11.5.0, flags `-O2 -fno-math-errno -ffp-contract=off -march=x86-64-v2`. Log: [quick_suite.log](/home/fb31/.t3/worktrees/Bayesian-Variable-Selection/t3-85c766ee-cf9abaf943992d2b/.rc_tmp/quick_suite.log).

- **C++ suite: 169 test cases, 0 failed, 0 check failures** (the quick set; the earlier gate review ran 176 in `--full`).
- **WP5 Slurm-driver tests: OK** (28 tests). **Competitor harness: OK** on its missing-package path (glmnet, ncvreg, biglasso, L0Learn, susieR, varbvs, BAS and bigmemory absent). **Install script: OK** (9 guard checks).
- **WP4 golden against core/, quick mode: 528,081 checks, 0 failures.** The `--full` goldens were not re-run; the fix round does not touch calibration scoring, the stores or the merge math.
- The three probes above are extra checks outside the suite.

## Non-blocking notes

1. **The F copy in the check is 8 B per inherited model.** `check_calib_tau_cal` copies the F column (`std::vector<double>(F, F+n)`) because `nth_element` needs a mutable copy. Models and indices are not copied. The builder's "no copy" wording holds for the models but not for F. Measured on a synthetic canonical calib (2,014,950 rows, p = 20,000; [recheck_mem_probe.cpp](/home/fb31/.t3/worktrees/Bayesian-Variable-Selection/t3-85c766ee-cf9abaf943992d2b/.rc_tmp/recheck_mem_probe.cpp), [log](/home/fb31/.t3/worktrees/Bayesian-Variable-Selection/t3-85c766ee-cf9abaf943992d2b/.rc_tmp/recheck_mem_probe.log)): max RSS 64.4 MB for the check against 49.4 MB for a plain touch of all three arrays, a delta of about 15 MB, which is about 8 B per row. Time is about 0.2 s per 2 M rows. If p = 10⁶ has the ~8×10⁷ inherited models quoted in the code comment (the comment's figure, not verified here), this is a transient of about 0.64 GB and about 8 s of CPU. It is freed on return and happens before the plan, admission and any store allocation. The island's top store at c = 4×10⁷ is far larger, so I do not count this as a break of the 10⁶ memory plan. Optional later improvement: select τ with a bounded heap, or note the 8 B per model in the memory plan.
2. **The non-canonical fallback allocates before its size guard.** In the sort fallback (non-canonical order only; the exporter never takes it), `std::vector<uint32_t> ord(n)` is allocated before the `n > 0xFFFFFFFF` check. It is harmless for any file the exporter writes.

## Verdict: MERGE

Zero CRITICAL, zero MAJOR, zero MINOR open. P8 can be closed on this head.
