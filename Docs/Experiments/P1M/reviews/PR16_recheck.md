# PR #16 re-check: WP4 slice 1 fix round (calibration, streaming merge, tail; D-26; INTERFACES v0.1.7)

- **Reviewer:** Opus 5.5 (high), independent re-check. Template: `briefs/REVIEW_PR_template.md`; rules: `briefs/BUILD_COMMON.md`.
- **Scope:** head `083014d2` (`exp/P1M-wp4-calib-merge`) into `exp/P1M-engine`. The PR merges the base at `f982ced` (v0.1.7). The base has since moved to `cded552` (WP5 guard2: tools/ and three lines of `run_tests.sh` only). `git merge-tree` against `cded552` is clean (tree `634b301a`).
- **Inputs:** first review `reviews/PR16_review.md`, disposition `reviews/PR16_disposition.md`, the author's fix list (PR comment).
- **How:** own worktree, detached checkout; read only. Nothing was pushed, commented or branched. Temp files only in `/home/fb31/SMC_Engineering_Department/tmp/20261116-recheck-16`, removed at the end. `nice -n 19`, ≤ 3 threads, no NOTS.

## Verdict: **MERGE** (ACCEPT; 0 CRITICAL, 0 MAJOR, 3 MINOR, 4 INFO; none blocks the merge)

__TESTS_SUMMARY__

## Claims, one by one

| claim | result |
|---|---|
| **F1** streaming merge + `--mem-budget` admission before any island loads; ≈ 11.7 GB at 10⁶ (ESTIMATE) | **Verified** (the 11.7 needs care, see m-2 and I-1) |
| **F2** coded paths golden-tested against `v3_calibrate` on identical forced inputs; bounded(I_max = ℓ) = coded tier 0 | **Verified** |
| **F3** tail uses bounded wave buffers + exact cut-off filter instead of `ThreadLedger` (DEVIATION) | **Argument right; replacement exact, thread-invariant and bounded.** Verified by my own probe (see below) |
| **F4 / D-26** calibration HPM offered with its calibration key, others with index i; bounded rule never escalates, refuses I_max > ℓ; fallback = last good grid, else the pilot schedule | **Verified** |
| **v0.1.7** `schedule_limit` = 6 / exit 16; no final-run leader stores; exactly N terminal supports; WP3-layout round trip | **Verified**, with one robustness bug in the terminal reader (m-1) |
| F5–F8 (minors of the first review) | **Verified** as described in the fix list |

### F1: streaming merge (`include/v4/merge.h:194-260`)
- `merge_stream(IslandSource&, Ledger&& pre, …)`:
  - pass 1 calls only `head(r)` (GUARD-W, plus finite log Ẑ_r);
  - then the admission: `resource_limit`, `fit_state = "not_admitted"`, returned before any `load()`;
  - pass 2 loads one `IslandIn` per iteration, `led.merge`s it and lets it go out of scope. It keeps log Ẑ_r, `pip_r`, ess and the terminal supports.
  - An island that differs at load from its head (r, p, N, status, finite log Ẑ) is refused.
- **Order-free.** `Ledger::merge` = `merge_tally` (HPM by `hpm_better`, provenance by the smallest key, counters added, island_best by max) + `Store::merge` (top-c of the union). So the result does not depend on the island order or on streaming. T9 golden (v4 merge over core islands) still passes.
- `pre` is now taken by rvalue. The harness moves it.
- **Peak (ESTIMATE, from `estimate_merge_memory`, kbar = 8, R′ = 16, N = 2,500, 96 threads, chunk 2,048).**
  - Merged store at 2.5c: 5.80 GB. One island at 2.5c: 5.80 GB. pip_r and terminal supports: 0.26 GB. One tail wave: 0.08 GB.
  - Total **11.94 GB (= 11.1 GiB)**. The PR's "≈ 11.7 GB" is neither unit; trivial.
  - The one-island term is conservative: a compacted island store is ≈ 1.25c with its staging reserve.
  - It is below the 16 GB target and well below the 32 GB NOTS plan. The unit test asserts < 16 GiB.

### F2: coded paths against core (`tests/golden/wp4_golden.R:153-232`, `wp4_harness.cpp:57-90, 191-196`)
- The R reference wraps the **same core entry points** that the harness backend perturbs:
  - `cpp_cal_pilot`: local_limit forced;
  - `cpp_cal_V`: k-th call fails;
  - `cpp_cal_diag`: k-th call fails, after the real call, so the state advances on both sides;
  - `cpp_runtime_check`: k-th call stops;
  - `v3_build_grid`: k-th construction reports `ok = FALSE`.
- Both sides then go through `compare_calib`.
- Each forced path also asserts that it really was reached:
  - `local_limit` fires and escalates;
  - `grid_fallback = last_successful_construction`;
  - `schedule_limit`, `resource_limit` (grid-runtime stop, preflight), `numerical_failure` (V, diagnostics).
- So this is not a vacuous comparison. P1–P5 are covered. Bounded(Serial, I_max = ℓ) is compared with coded tier 0 on triggers, converged, rebuilds, every grid and the frozen grid.
- Note: `Settings::test_force_build_failure` is a test hook inside the production `Settings` (default 0, inert). See I-3.

### F3: the tail without `ThreadLedger`: my view
- **Is the argument right? Yes.**
  - `ThreadLedger` flushes a full buffer into the island stores at once, under the island lock (`ledger.h:88-102`). A flush cannot be undone.
  - With threads, a worker on a later label range can flush offers from positions **after** the first failing position before the failure is known.
  - Its tally (HPM) would also hold those positions. Then the HPM-so-far and the stores would hold models that serial v3 never scored.
  - That state is still reported: `FitOut.hpm` with `hpm_incomplete = true` (`merge.h:289-291`). So it would differ from v3's incomplete HPM, and from run to run.
  - On a successful scan `ThreadLedger` would be exact too. The difference is only on the failure path. But the failure path is a reported state, and the wave design is the simplest way to keep it exact.
- **Is the replacement exact?**
  - The filter is `v ≥ cutoff()`, read at the start of the wave. The stores are not written during the parallel phase, so the read is race-free.
  - The cut-off only rises. `Store::offer` rejects exactly `v < cutoff()` (`store.cpp:38`), so every offer that could enter at application time passes the filter.
  - The HPM is safe as well: the HPM model is in the top store, so `hpmF ≥ cutoff`. A provenance-only update (equal F, smaller key) passes `≥`.
  - Offers are applied serially, in chunk order, with their serial keys.
  - On a failure, the failing chunk's earlier offers are applied, later chunks of the wave are dropped, and the counter stops at the failing position.
- **Deterministic under threads?** Yes.
  - The best-neighbour reduction is a strict total order.
  - The application order is label order.
  - The wave size (4 × threads) changes only which offers are buffered, never what enters.
- **Bounded at 10⁶?** Yes. A wave holds at most 4·threads·chunk offers, whatever p is. That is ≈ 80 MB at 96 threads and chunk 2,048 (ESTIMATE). The store's staging is bounded separately (2.5c).
- **Evidence I added.** The PR's failure test checks only the counter, with the failure in the first wave. The golden `tail_numerical` case checks only the status and the label.
  - So I wrote a probe (TMPDIR, PR untouched): 8 random toy problems (p = 120–211, exact ties, top store capped at 60 so that the filter bites).
  - The failure is a late swap position, so it falls several waves in for small chunks.
  - Threads {1, 3} × chunk {3, 7, 64}. The ledger after the failure (HPM model, F bits, HPM EventKey, top store bits and models, all logical counters) was compared with a serial scan stopped at the failure.
  - Result: **48/48 equal, every run threw.** The F3 claim holds.
- **Contract.** INTERFACES §7(4) literally prescribes "one `ThreadLedger` per worker". The wave buffers satisfy its intent: bounded buffers, cut-off quick rejects, an order-free result. The deviation should still be recorded (I-2).

### F4 / D-26
- **`offer_inherited` (`merge.h:166-173`).**
  - The calibration HPM model gets its CALIBRATION `EventCtx` (seg CALIB = 2). The other models get `inherited_event(i)`, particle = input index. The post-hoc relabel is gone.
  - The three v3 cases follow from the smallest-key rule. TABLE (0) < INHERITED (1) < CALIB (2) < FINAL (3) …; v3 is first-come, then relabels.
  - Unit test `wp4_inherited_provenance_v016`: (i)–(iii), another model as the calibration HPM (index 1), and a later FINAL event.
  - Golden `provenance_cases`: all on `v3_final_run`, (i) on the new p = 30 fixture whose HPM {3, 4} is a table model.
- **Bounded rule (`calib.h:172-179, 246-280`).**
  - `fired = coded && any()`, so there is no escalation.
  - The constructor refuses `tier0 ≠ 0` and I_max ∉ [0, ℓ] with `invalid_input`.
  - The fallback is forced on for bounded at tier 0: the last good grid if `g.g.ok`, else the pilot schedule, flagged in `grid_fallback`.
  - Golden D-26 asserts: preliminary failure → pilot schedule; rebuild failure → last good grid; triggers recorded without escalation; I_max = ℓ + 1 refused; coded + Blocked / refine_m > 1 refused (F7).
- Nit: the comment at `calib.h:260` still says "Bounded rule: escalation only on grid_failure". It is stale after D-26.

### v0.1.7 and terminal supports
- `Status::schedule_limit = 6`. `task_status` maps `schedule_limit` and `grid_failure_no_escalation` to it, and the latter is unreachable from tier 0, as the PR says. `fit_status` places it after `resource_limit`.
- The harness builds the final ledgers with `leaders = false`. The golden asserts that the final leaders are absent (capacity 0), and v3's final leaders are excluded. Calibration leaders, which V needs, are still compared in `compare_calib`.
- **Terminal supports.**
  - The merge accepts exactly N supports, or none; none makes Ẑ_occ unavailable (`merge.h:247`).
  - `wp4_terminal.h` reads `terminal_S_ptr` (i64, N + 1) and `terminal_S` (i32).
  - The layout matches WP3's writer on `exp/P1M-wp3-island2` and `-island3` (`island_file.cpp:64-66`).
  - The round trip uses the WP1 container with that layout, not WP3's writer, which is not merged yet.

## Findings

### m-1 MINOR (robustness): `read_terminal_supports` can read out of bounds on non-monotone offsets
`include/v4/wp4_terminal.h:19-26`

- **Evidence.**
  - The checks are `ptr[0] = 0` and `ptr[N] = |pool|` up front, then `ptr[i+1] ≥ ptr[i]` inside the loop.
  - An offset can overshoot the pool and come back down later, e.g. `ptr = {0, 10⁸, 2}`. Then `Model S(idx + ptr[0], idx + ptr[1])` reads 10⁸ ints past the pool before the decrease is seen.
  - **Reproduced:** a file written with the WP1 `fmt::Writer` and read with `read_terminal_supports(R, 2, 10⁶)` → **segmentation fault**, where `invalid_input` was expected.
  - Reachable only through a writer bug or a hash-consistent corruption, since the island hashes are checked at the merge.
- **Fix.** Check `ptr[i+1] <= ni` (or validate the whole offset array) before building `S`. Add the case to `wp4_terminal_supports_wp3_layout`.
- Side note, not this PR: WP3's own reader (`exp/P1M-wp3-island3`, `island_file.cpp:109`) builds the supports from `tp` with no offset validation at all. Worth one line in the WP3 review.

### m-2 MINOR (scale accounting): the admission estimate assumes no leader stores, but nothing enforces it
`merge.h:96`, `ledger.h:39`

- **Evidence.**
  - `estimate_merge_memory` uses `lead = 0` (v0.1.7).
  - But `merge_stream` keeps whatever store capacities `pre` brings, and `LedgerConfig::leaders` **defaults to true**.
  - A production caller that builds `pre` with the default config gets two 20p leader stores at 10⁶. That is ≈ +5.8 GB at 2.5c (ESTIMATE): ≈ 17.7 GB real against an 11.9 GB admitted estimate.
  - The harness and tests set `leaders = false`, so this is latent until slice 2 builds `pre`.
- **Fix.** In `merge_stream`, refuse (`internal_error`) a `pre` whose `lead0.cap` or `lead1.cap` is non-zero, or compute the estimate from `pre.top.cap + pre.lead0.cap + pre.lead1.cap`.
- Also, in slice 2, take kbar from the island headers (pool sizes) instead of the constant 8. At the plan's s₀ = 5, a kbar of 8 is reasonable, but kbar = 20 would give ≈ 21 GB.

### m-3 MINOR (tests): the F3 exactness on the failure path is not tested in the PR
`tests/test_wp4.cpp:246-256`

- **Evidence.**
  - The failure test fails in the first wave and checks only `logical[LOCAL]`. Golden `tail_numerical` checks only the status and the `hpm_incomplete` label.
  - The property the deviation rests on (HPM-so-far, stores and counters = serial stopped at the failure, ties included) is therefore asserted but not tested.
  - My probe shows it holds (48/48).
- **Fix.** Commit a test like the probe: failure several waves in, threads {1, 3} × chunk {3, 7, 64}, `same_ledger` against `serial_local` with a throwing evaluator. `same_ledger` and `serial_local` already exist in `test_wp4.cpp`.

### I-1 INFO: estimate figures
- The code gives 11.94·10⁹ B (11.1 GiB) for the PR's case, not "≈ 11.7 GB".
- The island term (2.5c) overstates a compacted island (≈ 1.25c), so the real peak is ≈ 9 GB. Both numbers are ESTIMATE.

### I-2 INFO: record the §7(4) deviation
- §7(4) says "one `ThreadLedger` per worker". The tail does not use one, for the reason in F3, which I accept.
- Ask the WP1 owner for a changelog line: "the tail (local search, LS0) uses chunk-ordered wave buffers with the cut-off filter, bounded at 4·threads·chunk offers; exact on the failure path".

### I-3 INFO: a test hook in production `Settings`
- `calib::Settings::test_force_build_failure` is inert by default.
- Slice 2 should not expose it through the CLI or `calib.bin` settings. Alternatively, move it into the backend, as the other fault hooks are.

### I-4 INFO: the bounded rule's last resort
- If the pilot schedule itself failed `check_grid`, the bounded rule would end with `grid_failure_no_escalation` → `schedule_limit`. INTERFACES says that "cannot arise in V-1M".
- The pilot schedule is always a valid 0…1 schedule by construction, so this is unreachable. An `internal_error` there would make the invariant explicit.

## Regressions
- The PR diff against the base touches only WP4 files: `calib*.h`, `merge.h`, `tail.h`, `wp4_par.h`, `wp4_terminal.h`, the golden harness, `test_wp4.cpp`, the bench, and `CMakeLists`/`run_tests.sh`/`.gitignore` lines.
- Nothing outside `engine_v4/`. No hard-coded paths. No large files.
- The other suites in `run_tests.sh --full` (WP1, WP5, golden prep) pass in my run (below).

## Test runs (MEASURED; Owls, Xeon Gold 6148, GCC 11.5.0, R 4.6.0, `nice -n 19`, ≤ 3 threads, 2026-11-16)

__TEST_TABLE__
