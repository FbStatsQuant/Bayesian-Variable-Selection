# PR #16 review: WP4 slice 1 (calibration with coded and bounded rules, merge, threaded tail, statuses)

- **Reviewer:** Opus 5.5, independent of the author. Template: `briefs/REVIEW_PR_template.md`, N = 16.
- **Scope:** head `fe86e6d` (`exp/P1M-wp4-calib-merge`) into `exp/P1M-engine` (`ce73f15`, INTERFACES v0.1.6). The branch is based on `a4ca68c` and coded against v0.1.2.
- **How:** own worktree, detached checkout, read only. Nothing was pushed or commented.

## Verdict: **ACCEPT-WITH-FIXES**

| grade | count |
|---|---|
| CRITICAL | 0 |
| MAJOR | 1 |
| MINOR | 7 |
| information | 3 |

- The calibration driver, the grid rules, the ledger merge, the threaded tail and the assembly copy core's arithmetic and control flow.
- I re-ran the PR's evidence and it reproduces exactly: 39 cases pass, and the golden run gives **974,641 checks, 0 failures**.
- I also checked three things the PR did not claim:
  - 533,657 more golden checks on trigger paths the PR does not exercise, all bit-identical;
  - the harness reference against core built the normal way (`core/v3.R`): identical;
  - the PR merged onto the current base (v0.1.6): clean merge, all tests pass.
- The one MAJOR finding is a design issue for p = 10⁶. Fix it before slice 2 locks in the island-reader API.

## Test runs (MEASURED; Owls, Xeon Gold 6148, GCC 11.5.0, R 4.6.0, `nice -n 19`, ≤ 3 threads, load 30–226, 2026-11-15)

`TMPDIR=/home/fb31/SMC_Engineering_Department/tmp/20261116-review-pr16`, removed afterwards.

| # | what | result |
|---|---|---|
| 1 | `tests/run_tests.sh --full --threads 3` at head `fe86e6d` | `v4_tests` **39 cases, 0 failed**; `wp4_golden.R full 3` **974,641 checks, 0 failures**; 25 min 0 s wall, 25 min 36 s user |
| 2 | reviewer's extra golden cases, harness + R driver kept in TMPDIR, PR untouched (see below) | **141,186 + 338,943 + 53,528 checks, 0 failures** |
| 3 | `core/v3.R` canonical build (unmodified copy of core) vs the harness-TU reference, 4 quick cases: calibration status, flags, frozen, HPM, ledger; final HPM + provenance, log Ẑ, PIPs, MPM, both local-search archives, flags, top store, counters, near ties, island_best | **92,541 checks, 0 mismatches** |
| 4 | PR merged onto `origin/exp/P1M-engine` (`git merge-tree`: clean, tree `3af3103`), `run_tests.sh --quick` | **45 cases, 0 failed; golden 253,073 checks, 0 failures** (3 min 51 s) |

The extra cases in run 2 are all coded-rule runs compared bit for bit with `v3_calibrate`:
- **P1** `grid_fallback = FALSE` on the T_e = 3 case gives `schedule_limit`.
- **P2** start at tier 1.
- **P3** preflight blocks the escalation: `resource_limit`, `escalation_blocked`. This needed a 2-line preflight hook in my copy of the harness.
- **P4/P5** ℓ = 1 and ℓ = 0.
- T_e sweeps at p = 60, 120, 300 (ℓ = 4 and 6): escalation, pilot-schedule fallback, and tier-1 rebuild loops that do or do not converge.
- **Bounded rule (Serial, I_max = ℓ) equals core's tier 0**, bit for bit, on the 4 quick cases: triggers, all grids, rebuilds, frozen grid.

## Findings

### F1 MAJOR (scale): the merge holds every island ledger in memory at once
`include/v4/merge.h:35-47, 162-169`

- **Evidence.**
  - `merge_and_tail(const std::vector<IslandSlot>& slots, Ledger pre, ...)` takes all R′ `IslandIn`, each with a full `Ledger`.
  - At p = 10⁶ one island's top store is 4·10⁷ + 1 entries, ≈ 2.2 GB at 56 B per entry (ES1 / Sol F3); the leader stores add more in compat.
  - With R′ = 16 that is ≈ 36 GB resident. On top come the pre-ledger, the merged ledger and `Store::merge` staging (peak ≈ 2.5c), so ≈ 45 GB **(ESTIMATE)**. The NOTS task plan is 32 GB.
  - `pre` is also taken by value. The harness passes an lvalue, so it is copied; in tests only.
- **Fix.**
  - Make the merge streaming. Pass 1 is GUARD-W over manifests, headers and hashes only. Pass 2 loads one island, `led.merge`s it and frees it, keeping only the small per-island fields (logZ, `pip_r`, ess, terminal supports, `rb_*`).
  - Take `pre` by rvalue reference.
  - Do this in slice 2, before the `island_r.bin` → `IslandSlot` reader fixes the API.

### F2 MINOR (tests): the golden test does not cover every coded-rule path against core
- **Evidence.**
  - The PR's golden test reaches three paths: no escalation; escalation on E triggers / `grid_unconverged`; preliminary failure with the pilot-schedule fallback.
  - My extra runs add schedule_limit, preflight-blocked, tier-1 start, ℓ = 0/1 and bounded = coded at tier 0. All are bit-identical.
  - Still not compared with core:
    - the `local_limit` trigger (it never fired, even at ℓ = 0/1);
    - the **`last_successful_construction`** C-DLV fallback (a tier-1 rebuild failing after a successful construction; not reached in 15 T_e settings);
    - the grid-runtime `resource_limit`;
    - numerical failure in V and in the diagnostic islands.
  - The mock tests cover some of these, but against hand-written expectations, not core.
  - By reading, `calib.h:165-277` follows `v3_calib.R:28-193` line for line on all of these paths (fail-time trigger snapshot, `g` kept at the last success on `break`, fallback precedence, flags). So this is a test gap, not a known bug.
- **Fix.**
  - Add a preflight hook and a `grid_fallback` switch to the harness, and cases P1–P3.
  - Add a fault-injecting core backend that forces (i) `local_limit` (e.g. ℓ = 0 with a pilot centre that is not a local optimum) and (ii) a tier-1 rebuild construction failure (e.g. lower T_e after the preliminary grid). Compare both with `v3_calibrate` run on the same forced inputs.

### F3 MINOR (contract §7(4), Sol F2): the tail's offer buffers are unbounded, though ThreadLedger already exists
`include/v4/tail.h:47-52, 115-116`

- **Evidence.**
  - Each chunk buffers every offer that passes `would_enter`, with no bound.
  - Known gap 3 says the tail will switch "when WP1 ships" `ThreadLedger` / `cutoff()`. Both are already in `a4ca68c` (`ledger.h:56-94`, `store.h:31`).
  - In practice the merged stores are full at p = 10⁶, so the filter rejects almost everything. Still, INTERFACES §7(4) and Sol F2 require bounded worker buffers.
- **Fix.** Use `ThreadLedger` with bounded buffers (provenance stays order-free through the smaller-key rule), or cap each chunk buffer and flush it in chunk order.

### F4 MINOR (contract §4.2 v0.1.5/v0.1.6): inherited-HPM provenance uses v3's post-hoc rewrite, not the v0.1.6 rule
`include/v4/merge.h:108-115`

- **Evidence.**
  - `apply_inherited_provenance` rewrites `hpm_ev` after the inherited offers when `phase == PH_INHERITED` and the model equals the calibration HPM. That is v3's `v3_core.cpp:428-440`.
  - v0.1.6 instead requires the calibration HPM model's inherited offer to carry its CALIBRATION EventCtx.
  - The two give the same result in every reachable case, because the calibration HPM is ⪰ every table model and every inherited model. The cases are those of PR17_review (a):
    - it is a table model → TABLE wins;
    - it is inherited only → CALIB, which is smaller than FINAL/LOCAL/LS0;
    - it is absent → no change.
  - But the PR form depends on call order: the rewrite must follow the inherited offers.
  - `inherited_event()` sets `particle = 0` for every model, while the v0.1.5 table says `particle = i` (input order).
  - The tests PR17_review asked of WP4 are missing: HPM in both the tables and the inherited list, and HPM in the inherited list only.
- **Fix.**
  - Offer the calibration HPM model with its calibration EventCtx and drop the rewrite.
  - Give `inherited_event(i)` an index.
  - Add the two tests: a v4-only unit test, plus a golden case with p ≤ block size so that the HPM is a table model.

### F5 MINOR: Ẑ_occ has no guard for zero occupancy
`include/v4/merge.h:255-261`

- **Evidence.**
  - If no terminal support lies in the top-M set (likely for M = 1 at large p), then `occ = 0` and `log_Z_occ = +Inf`.
  - A single island with `o = 0` gives `log_Z_occ_r = +Inf`, and then `sd_log_Z_occ_r = NaN`.
  - Nothing flags this. The χ² is skipped only for the pooled `pin` ∈ {0, 1}.
- **Fix.** Report the row as unavailable (NA plus a flag) when the pooled or a per-island occupancy is 0. Exclude such islands from the sd and χ², and record the count.

### F6 MINOR: grid refinement ×m leaves loose ends
`calib.h:269-273`, `calib_rules.h:194-206`

- **Proven.** For u < v, the points u + (v − u)·(k/m) are non-decreasing in k. The endpoints are copied exactly, so the grid starts at exactly 0 and ends at exactly 1. Strictness is enforced by `check_grid`; the run checks it too: length 4(n − 1) + 1, increasing, ⊇ the calibrated grid. **(b) holds.**
- Loose ends:
  - (i) `frozen.rho_V` keeps the unrefined length. `v3_stage_table` maps `rho[seq_len(n)]` (`v3_run.R:56`), so ρ_V and stages misalign for m > 1.
  - (ii) Nothing checks the refined interval count against T_e, or records a decision that it may exceed T_e (D-12 is silent).
  - (iii) An interval too short to split throws `std::runtime_error`, which ends the whole fit. Bisection can produce intervals of a few ulps.
- **Fix.**
  - Record `rho_V` as unrefined, under a separate name, or expand it.
  - Ask the manager to decide (ii).
  - Throw `Error(internal_error)`, or leave an unsplittable interval whole and flag it.
  - Record m and `grid_unrefined` in `calib.bin` meta.

### F7 MINOR: no guard that theory mode uses theory arithmetic
`calib.h:49-58`

- **Evidence.**
  - `Settings` accepts `Rule::coded` together with `SumMode::Blocked` or `refine_m > 1`.
  - Either one silently breaks the class-B claim of theory mode T.
- **Fix.** Refuse those combinations (`invalid_input`), or derive `sum_mode` and `refine_m` from the mode.

### F8 MINOR: E2 with NaN behaves differently from R
`calib.h:211`, `merge.h:282`

- **Evidence.**
  - In R, `stats::sd(log_Z_r) > 1` is NA when any `log_Z_r` is NaN or ±Inf. `any(unlist(trig))` then errors (`v3_calib.R:154-155`); in the final run, `checks_passed_final` becomes NA.
  - v4 treats NaN > 1 as false: no trigger, and `checks_passed` = true.
  - This is an edge case: no case reaches it.
- **Fix.** Map a non-finite `log_Z_r` to `numerical_failure` in both places, or document the deviation.

### F9 information: contract deltas from v0.1.2 to v0.1.6, and statuses
- The PR merges cleanly onto v0.1.6 and passes there (run 4).
- Still open for slice 2:
  - `calib.bin` meta: m, block size 4096 (part of the class-C arithmetic), `grid_unrefined`.
  - The §5.2 `CalibResult` has a `Ledger led` and the inherited export, but the Driver does not own them. Today they come from the backend (`cpp_cal_export` in the harness).
- `schedule_limit` / `grid_failure_no_escalation` → `resource_limit` (`calib.h:39-45`) needs the manager's decision, as the PR says.

### F10 information: what the golden test proves
- **(e) holds.**
  - core/ is identical to `origin/main` and to the base; it is copied to TMPDIR and never written.
  - The harness reference is unmodified `v3_core.cpp` concatenated with test code.
  - Run 3 shows that this reference equals the canonical `v3.R` build bit for bit, so the TU merge and `-fopenmp` change nothing.
- **Note: calibration compares core against core here.** The calibration HPM, stores and counters in `compare_calib` come from **core's** ledger in both arms, because the `CoreBackend` drives core's `CalState`. They prove that the driver called core in the same order. They do not test v4's `Ledger` in calibration.
- **T9 does test v4 code:** v4 merge, tail and assembly over core islands.

### F11 information: threads, the tail and scale
- **(d) holds.**
  - The best-neighbour reduction is a max under a strict total order (F descending, then lexicographic), applied first within chunks and then across chunks in order. It is associative, so the result does not depend on chunk size or threads, ties included.
  - Offers are applied in label order, which equals position order, with serial keys.
  - The failure path matches serial: offers before the failing position are kept, counters stop at it.
  - Positions match `Engine::local_search` for the K cap (deletions only, `below(j) + 1`) and for swaps.
  - The tests cover exact ties, a binding K and a binding move cap at threads {1, 3} × chunks {7, 64, 10⁵}.
  - Caveat: a NaN F would break invariance (the first element of each chunk is accepted unconditionally), so the v4 scorer must keep throwing `NumericalFailure` on non-finite scores. Stores already refuse NaN (v0.1.3).
- **Calibration threads hardly help at these sizes.** In run 1 (MEASURED), calibration wall time is the same at 1 and 3 threads, and user ≈ real. The serial core islands dominate.
- **Scale.**
  - `uint32` positions are safe: ≤ p + K·p ≈ 1.01·10⁸ at 10⁶.
  - FV at |V| = 4·10⁷ needs 320 MB for its threaded buffer.
  - One 4096-member block size is fixed and independent of threads.
  - Nothing else blocks 10⁶ apart from F1.

## Discipline
- Every file the PR changes is under `engine_v4/`.
- No hard-coded paths.
- The largest tracked file is 4.7 MB (an existing fixture).
- `.gitignore` adds `.nfs*`.
