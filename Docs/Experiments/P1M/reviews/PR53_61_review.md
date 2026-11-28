# Final review: PR #53 (WP6 K2 fix round) and PR #61 (WP6 K5 rolling admission)

Reviewer: Claude Opus 5.5, high effort, 2026-11-17. This review was independent of the author and used no sub-agents. It followed `REVIEW_PR_template.md`, including its Sandbox section. Checkout: detached at `099e8ac6`, the head of #61. #53's head `daae378a` is its first parent. `origin/exp/P1M-wp6-k2` = `daae378a` and `origin/exp/P1M-wp6-k5` = `099e8ac6` at review time.

| PR | Head | Verdict | CRITICAL | MAJOR | MINOR |
|---|---|---|---:|---:|---:|
| #53 K2 fix round | `daae378a` | **ACCEPT** | 0 | 0 | 1 |
| #61 K5 rolling admission | `099e8ac6` (own diff `daae378a..099e8ac6`) | **ACCEPT** | 0 | 0 | 2 |

The minor findings are about test strength and an optional efficiency change. None of them is a bit-identity or allocation defect, and neither PR needs a fix before merge.

---

## A. PR #53: fix of the Codex MAJOR (order-phase I proposal allocated in the parallel region)

Reviewed: `99b1954f` (the fix) and `daae378a` (the merge of engine `2cfaa9e5`, adapted to StartView). I diffed against `2cfaa9e5`, compared `99b1954f` with `daae378a` for the adaptation, and read the full current `island_lm.h`, `island_pm.h`, `start_view.h` and `score.cpp`.

### What the fix does (verified by reading)

The serial preamble in `lm_group` (`src/island/island_lm.h:51-65` at #61's head) sizes everything the order-phase region touches:

- **Nongibbs label lists:** `gb.ng[gi].reserve(m-p)`. The pushes are exactly `m-p` = B+2, then they are sorted in place with no allocation.
- **Proposal particles:** `gb.iprop[gi].S.reserve(K+1)`.
- **Per-thread order scratch:** `LmScratch::ord` is sized to `m`.
- **Per-thread proposal model:** `LmScratch::imodel.reserve(K+1)`.
- **Scorer buffers:** `BitScorer::reserve(kq)` gives capacity only. Every Cholesky-route buffer (`Gs_`, `bufH_`, `bufA_`, `LH_`, `LA_` at k²; `w_`, `beta_`, `tmp_` at k; `flip_` at k+1) is then filled with `assign`, `resize` or copy-assign at or below its capacity, so a draw of size ≤ kq does not allocate (`src/common/score.cpp:149-154`).
- **Copies into the proposal:** `fill()` copy-assigns into `gb.iprop[gi].S`, within its reserved capacity.

After the merge, the block list of the draw is StartView's per-thread `Scratch::nz`. `StartView::prepare(NT)` reserves it to K+1 in the engine constructor (`island_run.h:225`, `start_view.h:99-107`). `cond_row` uses fixed `kRow` arrays, and `submodel` uses the prepared `lv/sc/e/codes`.

**Residual allocations.** These are the QR fallback (`MH_`, `MA_`, `hv_`), a pi_0 draw larger than kq, and the throw path of a `NumericalFailure`, whose message string is built in the region. All three are inside `oom_guard`. A larger draw grows the thread's scorer buffers once, and the capacity is kept afterwards, so these allocations are rare and bounded per thread. I agree with the stated residuals.

### StartView adaptation (`99b1954f` → `daae378a`)

The only change is that `draw_indep` stopped passing a caller-owned block list to a `dep.h` overload. It now calls StartView's `draw_pi0_fast`, the base's own function, which draws the same addressed uniforms in the same order. The `LmScratch::nz` field and its 8(K+1) plan bytes were dropped consistently: `memory.h:20,87-89` changed from 12(K+1) to 4(K+1). The model scratch, label lists, proposal models and scorer reserve were all kept. **Same bits, measured:** T3, the hash matrix and the WP4 goldens below all match.

### lm_scratch plan term

`T (18 tile + 64 kq + 64 + 40 kq² + 24 kq + 4 (K+1)) + 4 G (K+1)` matches the reserves:

- 5 kq² doubles + 3 kq doubles per scorer
- one per-thread model
- one proposal model per slot

The per-thread order (`T m 4`) and the `ng` lists (`G (B+2) 8`) are in `orders`. StartView's draw scratch is in the inputs term (`scratch_bytes`). Two small items are not counted: `flip_` (4(kq+1) bytes per thread) and the scalar fields of `iprop`. Both are negligible. No finding.

### Counting test and negative control

`order_phase_allocates_nothing_in_parallel_{bit,classA}` passes: 0 allocations at threads 1/3 and G 16/48, both forms, on the portable and the x86-64-v4 builds.

I rebuilt the deliberate regression independently: `draw_indep(..., nullptr)` in `lm_group`, in the copy `.rc_tmp/negA/` with build `.rc_tmp/build_negA/`. The test **fails** with 1,490 in-region allocations at threads 3, for G 16 and 48 and both forms. Exit 1, log `.rc_tmp/logs/negA.log`. The gate works at threads 3.

#### MINOR A-1: the threads-1 legs of the counting test can never count

**Where:** `tests/test_island.cpp:36` (`... && omp_in_parallel()`).

**Evidence:** `omp_in_parallel()` is false inside a `num_threads(1)` team, because that region is inactive. A probe in `.rc_tmp/probe/inpar.cpp` (log `.rc_tmp/logs/omp_in_parallel_probe.log`) gives `num_threads(1): omp_in_parallel true in 0/6 iterations, omp_get_level()>0 in 6/6`. Consistent with this, the negA build reports **0** allocations at threads 1 even with the regression in place. Half of the test's eight legs are vacuous, and the PR text's "0 over whole runs, threads 1 / 3" overstates the evidence for threads 1. The same predicate gates the older injection hook at line 42. That hook predates this PR and is noted only.

**Fix:** use `omp_get_level() > 0` in the counting predicate. The test flag is set only around the region, so nothing serial is counted by mistake. Optionally, make the negative control an in-tree test switch, in the style of `test_bound_shrink`, so it runs with the suite instead of being a manual claim.

### Other K2 items (unchanged since the Codex review, re-checked)

- **Packed `fmin`:** `(pos << 32) | label` is still read by both phase A and the walk.
- **I proposal timing:** the deferred I-proposal failure is raised at its own position. `indep_proposal_failure_deferred_to_its_position` passes, and it now also runs with rolling admission, which is the default at G 7 and G 16.
- **Compat path:** it still draws serially (`ipre = !csrc`).

---

## B. PR #61: K5 rolling admission (`git diff daae378a 099e8ac6`, merges ignored)

The diff covers `island_lm.h`, `island_lm_state.h` (`pid`), `island_run.h` (`round`), `island.h` (`rolling_admission`), the test, `bench_island.cpp` and `nots_bench_k1.sh`. `memory.h` is unchanged.

### Bit-identity argument (verified by reading)

Every particle-indexed quantity now goes through `pid[gi]`:

- the Fisher–Yates order address (`draw_order(rc, pid[gi], …)`)
- the I proposal address
- phase-A deletion and tile `i1`
- the walk's `step_nongibbs` particle and keys
- the phase-B `unscored` checks and flip-offer key
- the apply-phase `fail.record` rank

A `grep` finds no remaining `g0 + gi`. Per-slot state is reset on admission: `q`, `e`, `done`, `etype`, `elab` and `ierr` are reset, and `ng` is cleared with its capacity kept. `inv` is fully rewritten, since `ord` is a permutation. `fmin` is reset for every active slot at the start of each pass. `pending` is read only when `etype == 2` in the same pass.

**Order-sensitive points.** These keep group semantics because every tie now breaks on the particle index, not the slot:

- the support-representative tie (`idx` comparator tail `pid[a] < pid[b]`)
- the phase-B consumer order (`sup_parts` sorted by `pid`, line 121, so `first` is the smallest consuming particle)
- `EventKey` compares `particle` before `position` (`ledger.h:28`), so the per-offer key is the minimum over that offer's events

Offers are order-free. Counters add `ncons` per particle, so totals do not depend on how particles are co-batched.

**Failures.** `FailSlot::record` keeps the smallest particle, and an out-of-memory failure ranks at `UINT32_MAX`. Particles admitted after a numerical failure at particle i all have indices greater than i, so the reported failure, its message and `last_fail_particle` match group mode. That in turn keeps calibration's `rebuild_prefix` replay identical. A non-calibration island with status 2 exports no store.

**Memory plan.** The window is `gN = min(G, N)` slots, exactly as for the first group, so it is unchanged. The new `pid`/`admit` vectors are O(G) ints.

**Allocation.** The only parallel region that changed is the admission region, which is the K2 order-phase region applied to the admitted subset. The counting test runs with rolling (G 16 < N 48 re-admits) and reports 0 at threads 3. `admit` is grown serially.

### Measured

| Check | Result |
|---|---|
| `rolling_admission_same_bits_{bit,classA}` (threads 1–3, G 1/5/7/16/48, dense and bounded, NaN-row poisoning on) | PASS. Hashes equal groups. Passes 298 → 199 at G 16. Same on the x86-64-v4 build. |
| Checkpoint/resume at a rolling boundary, p = 2·10⁴, N = 300, G 64, `steps:1 2 2`, stop after step 3, both forms | All 6 runs per form give one hash. The six are: uninterrupted rolling; uninterrupted groups; and resumes from {rolling-written, groups-written} checkpoints × {rolling, groups} (A `7de14525e0b9cbdb`, bit `08cb00e8333b3486`). The resumes really resumed: cumulative pass counters are restored, e.g. 62 rolling + 99 groups = 161, and 144 groups + 48 rolling = 192. Uninterrupted runs: 243 passes with groups → 110 with rolling. Log: `.rc_tmp/logs/ckpt.log`. |
| `t6_restart_bit_identical` (LM G16 → G5 resume, rolling default) | PASS on portable and x86-64-v4 |
| Bench script | `bash -n` passes. Every variant now sets or unsets `V4_NO_ROLLING` explicitly, and the script unsets it at the top. `check_mode` asserts `rolling admission on/off` from the run's own configuration line, which prints the `IslandConfig` value the engine reads, plus the Gram-row evidence for k3/k5. The NOTS run was not executed (no NOTS). |

#### MINOR B-1: no test can fail on the phase-B consumer tie that K5 depends on

**Where:** `src/island/island_lm.h:121` (`sup_parts` sorted by `pid`); `tests/test_island.cpp:433-454`.

**Evidence:** I rebuilt the deliberate bug "consumers in slot order", i.e. the pre-K5 `std::sort(v.begin(), v.end())`, in `.rc_tmp/negB/` with build `.rc_tmp/build_negB/`. `rolling_admission_same_bits_*` still **PASSES**, with the same hashes (log `.rc_tmp/logs/negB.log`). `IslandRun::hash()` includes event keys only through the HPM provenance key (`island_run.h:79`), and stores carry no keys. A wrong `first` therefore changes the output only when the HPM model is first found by a shared-support consumption whose slot order differs from its particle order. That does not happen in the small fixture. The code is correct; the test is blind to this tie.

**Fix:** add a test-only hook that records, per offered model, the minimum flip-offer `EventKey`, or the full multiset of (model, key) offers. Compare it between rolling and groups at G 5/16. Alternatively, add a debug assertion that each `sup_parts[s]` is ascending in `pid`. Then keep negB as an in-tree negative control.

#### MINOR B-2 (optional, efficiency): rolling keeps admitting after a numerical failure

**Where:** `src/island/island_lm.h:74`.

**Evidence:** in group mode the round throws after the failing group. In rolling mode, slots keep taking new particles until all N have run, which wastes up to one round of work on a failed island. The output is unchanged, as argued above.

**Fix (optional):** do not admit while `fail.has` is set for a numerical failure. This is bit-safe, because every later admission has a larger particle index than the recorded failure.

---

## Bits (both PRs; measured at #61's head `099e8ac6`; #53's head is its first parent and its merge carries no further code)

**T3** (`t3_invariance_*`, PM reference vs PM threads 3 and LM threads 1/2/3 at G 1/7/16/48, so LM at G 1/7/16 runs rolling):

| Build | Bit | Class A |
|---|---|---|
| Portable (run_tests default) | `44a15bfc6fb8d233` | `d2df149413596a19` |
| x86-64-v4 (`.rc_tmp/build_v4t`) | `44a15bfc6fb8d233` | `e9cc4ab39f8a72db` (FMA) |

**16-run island hash matrix.** p = 2·10⁴, N = 300, `geo:4 1 1`, tile 128, island ISA x86-64-v4 (`.rc_tmp/build_v4/v4_bench_island`), execution overrides cleared. Script `.rc_tmp/run_matrix.sh`, log `.rc_tmp/logs/matrix.log`.

| Form | PM G64 thr 1, 3 | LM G64 rolling thr 1, 3 | LM G256 rolling thr 1, 3 | LM G64 groups thr 3 | LM G256 groups thr 3 |
|---|---|---|---|---|---|
| A | `263474601a55acb1` ×2 | ×2 | ×2 | ×1 | ×1 |
| bit | `f9c6272ed1ffbae5` ×2 | ×2 | ×2 | ×1 | ×1 |

All 16 runs gave the pinned hash for their form, and threads 1 and 3 are equal. 300 is not a multiple of 64 or 256, so the rolling runs really re-admit.

**Quick suite at `099e8ac6`.** Command: `tests/run_tests.sh --quick --threads 3 --keep --build-dir .rc_tmp/build`, with `TMPDIR = P1M_TEST_ROOT = <worktree>/.rc_tmp/tmp`. Log: `.rc_tmp/logs/quick.log`. **Exit 0.**

- 185 C++ test cases: 0 failed, 0 check failures.
- WP5 Slurm driver: 28 tests OK.
- Competitor harness OK. Eight optional packages are absent here, so their installed runs are not established.
- Install script: 9 checks OK.
- **WP4 golden: 540,419 checks, 0 failures**, all fixtures.

**Extra x86-64-v4 test build.** `t3_invariance`, `rolling_admission`, `order_phase`, `indep_proposal`, `philox*` and `t6_restart` all pass (`.rc_tmp/logs/v4t.log`).

## Contract, scale, discipline

- **Contract:** no INTERFACES or format change. `rolling_admission` is an execution parameter, absent from the checkpoint payload. Mixed-mode resume is verified above.
- **Scale:** at p = 10⁶, K2's net order saving stands. K5 adds O(G) ints. Index arithmetic is unchanged: `(size_t)gi * m`, 32-bit positions, `pid` < N.
- **Discipline:** both diffs touch only `Scripts/SMC_BVS/engine_v4/`. `git diff --check` is clean for both. No large files.

**Integration:** `exp/P1M-engine` has moved six commits to `96137399` (#60/#62, WP7 O4). `git merge-tree` of that tip with `099e8ac6` is clean. I did not build the combined tree.

## Sandbox

- **Location:** all builds, scratch, checkpoints and logs are under `<worktree>/.rc_tmp/`.
- **Resources:** `nice -n 19`, `make -j3`, at most 3 OpenMP threads.
- **Deletions:** I deleted nothing. `run_tests.sh` used `--keep`, so the WP4 work directory stays. The test programs' own cleanup of their temporary files under `.rc_tmp/tmp` is test behaviour; I did not intercept it.
- **Sources:** tracked sources are unmodified. The negative controls are patched copies in `.rc_tmp/negA` and `.rc_tmp/negB`. HEAD is detached at `099e8ac6`.
- **No outside actions:** no push, no GitHub comments, no NOTS, no permission requests.
