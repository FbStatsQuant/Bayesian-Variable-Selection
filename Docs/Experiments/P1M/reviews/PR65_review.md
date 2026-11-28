# PR #65 review: WP4 merge memory (inherited models read from the mapped calib.bin, table stores released, plan by phase)

Reviewer: Opus 5.5 (independent of the author), final gate review, 2026-11-17. PR head `32f862c0`, base `exp/P1M-engine` = `423decb5`
(the merge base; the head already contains the base). Scope +614/−40, 10 files, all under `Scripts/SMC_BVS/engine_v4/`.
Read-only: no push, no comment, no merge. Owls, `nice -n 19`, ≤ 3 threads, one suite at a time, no sub-agents.

| Verdict | CRITICAL | MAJOR | MINOR |
|---|---|---|---|
| **ACCEPT-WITH-FIXES** | 0 | 2 | 6 |

**Bottom line.** Bit identity holds. On three inputs, every data section of `fit.bin` (41 of 41) and every non-execution
meta key (143 of 143) is identical between base and head, at 1 and 3 threads. Among them: the merged top store, HPM, PIP_eq,
PIP_Z, PIP_T, logZ, LS and LS0 paths, near-ties, occupancy and logical counters. The quick suite passes on the PR head:
193/193 unit tests, and the WP4 golden ran **540,419 checks with 0 failures**. The golden's T9-files leg goes through
`merge::run`, so it exercises the new mapped path. The mapped path is memory-safe against 18 malformed calib.bin variants.
The two MAJOR findings need fixes before the merge, and both are small:
- **M-1:** the admission check of the plan's largest phase at 10⁶ (`offers`) runs only after that phase.
- **M-2:** the INTERFACES v0.1.25 number collides with PR #64.

The 48G request for the 10⁶ merge is plausible but rests on a probe projection. See m-5 for the conditions.

## Tests I ran (PR head 32f862c0, Owls, Xeon Gold 6148, g++ 11.5.0)
- `TMPDIR=.rc_tmp/tmp P1M_TEST_ROOT=$TMPDIR tests/run_tests.sh --quick --threads 3 --keep --build-dir .rc_tmp/build_head`:
  **193 PASS / 0 FAIL**, the WP5 driver (38 tests), the competitor harness and the install script all OK, **WP4 golden: 540419 checks, 0
  failures**, rc = 0 (log `.rc_tmp/head_quick.log`). This is the quick golden rerun **after** the last base merge, which the
  author's run predates. `wp4_merge_mem_plan_bounds_peak` printed: p = 4000, measured peak 111.8 MB, plan 206.2 MB (×1.84).
- **Base vs head on the same inputs.** I built the base `smcbvs4` from `423decb5` (`.rc_tmp/build_base`) and compared the outputs
  with `.rc_tmp/adv/cmpfit.py`: per-section SHA-256 from `smcbvs4 info`, plus a key-by-key diff of the meta. Three inputs:
  1. A real CLI pipeline (`gen AR n=150 p=400` → `prep` → `setup` → `calibrate --mode V` → 4 × `island` → `merge`). It has
     23,975 inherited models, a calibration HPM and an offer floor (tau_cal = −167.08). Merged at 1 and 3 threads, base and head.
  2. The PR's probe at p = 4,000, R′ = 4.
  3. The PR's probe at p = 20,000, R′ = 4 (800,001-entry stores, 1.6 M inherited models).

  In every pair, the only differing section is `meta`. Within the meta, the only differing keys are `binary`, `mem_estimate`
  and `timings`, all execution statistics. `fit.json` differs only in `fit_bin` (the file hash, which changes because the meta
  changes), `binary`, `timings` and the new fields (`peak_rss_kb`, `end_*`, `write_fit_seconds`, `timings.phases`).
  Measured peak at p = 2·10⁴: base 764 MB, head 532 MB (−30%, as reported). The record's `peak_rss_kb` equals `/usr/bin/time`'s
  `ru_maxrss` exactly (110,604 and 531,516 kB).
- **Malformed calib.bin** (`.rc_tmp/adv/adv_calib.cpp`). Hash-consistent rewritten copies were run through
  `read_calib(keep_inherited = true / false)`:
  - offsets: ptr[0] ≠ 0, last too short or too long, non-monotone, 2⁴⁰ mid, negative mid, one extra entry, empty;
  - pool: index ≥ p, index < 0, unsorted;
  - arrays: F, logm or lg0 one element short or long; F = Inf; logm = NaN;
  - a truncated file.

  Plus `offer_inherited_file` on another file of the same shape. **All 18 cases are refused with `invalid_input`, with the same
  message on both paths; nothing was accepted.** (ASan and UBSan runtimes are not installed on Owls, so this was a release build;
  the bounds argument below rests on reading the code.)
- **Admission order** (see M-1): probe p = 2·10⁴ with `--mem-budget 692000000`, which lies between the early check (688.8 MB)
  and the plan total (696.1 MB). Result: rc = 11, `not_admitted`. The phases recorded before the refusal are `setup_read`,
  `calib_read`, `heads_checked`, `tables_offered`, `tables_released`, `inherited_offered` and `pre_compacted`.
- **Plan vs measured with the PR's probe** (3 threads):

  | p | measured peak | plan total | ratio | largest planned phase vs peak |
  |---|---|---|---|---|
  | 4,000 | 107.5 MB | 206.2 MB | ×1.83 | — |
  | 20,000 | 518.4 MB | 696.1 MB | ×1.28 | `load_setup` 532.4 MB, 2.7% above the peak; the ×1.15 margin is the real slack |

## Focus 1: bit identity
- `store.cpp`: the only change is the new `Store::release()` (`src/common/store.cpp:22`). `better`, `offer`, `compact` and the
  index are untouched, so ordering, tie-breaking and arithmetic are unchanged.
- `offer_inherited_file` (`src/merge/wp4_io.cpp:372-386`) offers model i = 0..n−1 in file order, the same order as
  `merge::offer_inherited` (`include/v4/merge.h:230-237`), with the same arguments:
  - `ModelView S` over the same labels;
  - `zob.hash(S)`, the same single `Zobrist::hash(ModelView)`, `model.h:37`;
  - F, lg0 and logm read bit for bit from the file;
  - `is_hpm` computed as size and element equality, equivalent to `m.S == calib_hpm`;
  - the same `C.hpm_ev` / `inherited_event(i)`.

  `Ledger::offer_stores` takes a `ModelView` in both cases (`ledger.h:68`). Store content is offer-order independent anyway
  (`store.h` header comment), but here the order is also identical, so HPM tie handling by smallest key is unchanged.
- Releasing the table stores after `offer_tables` is safe. The only readers of `ttop`, `tlead0` and `tlead1` in the merge are
  `offer_tables` (`wp4_io.cpp:765-771`) and `bytes_resident` (called at :1076, before the release at :1097). `BitEval` uses
  `logr` and the block arrays, which are kept.
- `merge.h` changes outside `estimate_merge_memory` are only `phase_hook` calls on the main thread. They have no effect on outputs.

## Focus 2: memory safety of the mapped path
- **Lifetime.** `offer_inherited_file` opens its own `fmt::Reader` (`wp4_io.cpp:374`), and every pointer it uses (ptr, idx, F,
  L, M) lives inside that function. Nothing outlives the mapping, and `CalibIn` holds no pointer into a mapping.
- **Validation before reads.**
  - `validate_inherited_in_place` (`wp4_io.cpp:302-316`) checks: ptr[0] = 0 and ptr[n] = |idx|; monotone and ≤ |idx|; the three
    value arrays of length n **before** any F[i] is read; every model through `check_model`; finite values. That is the same set
    of checks as `models_checked` plus the old loop.
  - Truncated or corrupt files are refused by `Reader` (size == header `file_bytes`; section ranges checked overflow-safe,
    `format.cpp:118-135`) and by the full section-hash check in `read_calib`.
  - The `(uint32_t)` length cast is pre-existing and harmless: with ptr monotone and covering, every view lies inside the pool.
- **Use after release.** None found (see above).
- The one weak point is the second, unvalidated mapping (m-3).

## Focus 3: the plan formula, the refusals and the ratio test
- At 10⁶ the formula is consistent: plugging in the MERGE_MEM sizes reproduces every row (load_setup 22.1, load_calib 21.8,
  offers 24.4, streaming 20.2 GB; total 28.2 GB = 26.2 GiB).
- The size-based refusal is not an upper bound (m-1). The admission of the largest phase comes late (M-1).
- The ≥ 1.1 test is not vacuous but is weak at p = 4,000 (m-2).
- `peak_rss_kb` is Linux-only, and the phase samples are approximate (m-4).

## Findings

### MAJOR-1: the plan's largest phase at 10⁶ (`offers`) is admitted only after it has run
**Where:** `src/merge/wp4_io.cpp:1055-1072`, the early check, which covers only `load_peak`. The full plan is first checked in
`merge_stream` at `include/v4/merge.h:292-296`, which runs after `offer_tables` (:1095), `offer_inherited_file` (:1099) and
`pre.compact()`, and after pass 1 has hashed every island head (:1090). The binding rule is INTERFACES §7
(`INTERFACES.md:547`): "Over budget, admission refuses deterministically … before any allocation. … The merge applies the same
rule to its own plan".

**Evidence:** at 10⁶ the projected `offers` phase (24.4 GB) is larger than both load phases (22.1 and 21.8 GB). So the phase
that sets `total` is never checked before it runs. Measured at p = 2·10⁴ with a budget between the early need and the total:
the merge ran setup read, calib read, island heads, table offers and inherited offers, and only then refused (`reason`
"merge not admitted: estimated peak 696113114 B > --mem-budget 692000000 B").

At 10⁶ that is minutes of hashing (≈ 58 GB: setup 10.1 + calib 9.8 + island heads 37 + data 1.6) before a refusal. If the budget is set near the cgroup limit, the outcome is an OOM
kill during the offers instead of a clean `resource_limit` (exit 11). The PR rewrote the admission precisely so that a mis-sized
request is refused cleanly, and this leaves its peak phase uncovered.

**Fix:** every input of the full plan is known right after `phases.mark("heads_checked")` (:1091):
- kbar from `src.heads()`;
- `setup_all` / `setup_resident` from `S.bytes_resident`;
- file sizes; `Rp`, `N`, `threads` and `chunk` from the arguments.

Move the `ms` setup (:1103-1114) above `offer_tables` and refuse there with the same not-admitted record. Keep the `merge_stream`
check as a backstop. Add a suite case with a budget between `early_need` and `total` and assert that no phase after
`heads_checked` is recorded.

### MAJOR-2: INTERFACES version collision with PR #64, and the header was not bumped
**Where:** `INTERFACES.md:441`, `:549` and `:726` claim **v0.1.25**. PR #64 (WP7 O3, `exp/P1M-wp7-o3-leaders`, head `9fa534e7`)
also claims v0.1.25: its header line, its §5.1 `t_compact_lead` note and its changelog line. Separately, this PR leaves the
binding header line at **v0.1.23** (`INTERFACES.md:3`), already stale on the base, which has a v0.1.24 changelog entry.

**Fix:** whichever of #64 and #65 merges second renumbers its lines to **v0.1.26**: the §5.1 note, the §7 "Merge plan" tag, the
changelog line and the header. If #65 merges first, it must also bump the header line 3 to v0.1.25. The merge commit of the
second PR must resolve the header to v0.1.26.

### MINOR-1: the early refusal assumes "the copies are no larger than the files"; measured, the copy is 2.6% larger
**Where:** `wp4_io.cpp:1053` (comment) and `:1056` (`setup_all = setup_resident = b_setup`); `INTERFACES.md:551`
("copy of setup.bin (≤ its size)").

**Evidence:** the SetupView copy is larger than setup.bin. The ratio `setup_all / setup.bin` is 1.0258 at p = 4·10³ and 1.0259
at p = 2·10⁴. The cause is per-entry state the file does not hold: the stores' `hidx_` at 4 B per entry, and the (hash, index)
pair sort inside `load_unique_sorted`. At 10⁶ that is ≈ 0.26 GB. The ×1.15 margin absorbs it, so nothing fails today, but the
documented upper bound is false.

**Fix:** use an honest bound. Either `setup_all ≤ b_setup + 4 B × (table entries)`, where the entry counts are readable from the
section table without reading any section, or simply 1.05 × b_setup. Correct the comment and the INTERFACES wording.

### MINOR-2: the default-suite "≥ 1.1" test is dominated by the 80 MiB constant at p = 4,000
**Where:** `tests/test_merge_mem.cpp:220-227`.

**Evidence:** plan 206.2 MB against a measured 111.8 MB. The constant (83.9 MB) alone is 75% of the measured peak, and VmHWM is
already 65 MB at `start`. The check `total ≥ 1.1 × peak` would still pass if the variable part of the plan
(1.15 × the largest phase) underestimated the true variable part by ~28%. So the test is not vacuous, but it does not guard
the per-phase model that the 10⁶ request depends on. The ×1.22 and ×1.25 ratios come from the opt-in probe only.

**Fix:**
- Assert on the variable part, for example `(total − 80 MiB) / 1.15 ≥ 1.0 × (peak − hwm_at_start)`, or per phase
  (each `phases[i].hwm_kb` ≤ the planned phase).
- Add a p = 2·10⁴, R′ = 4 case to `--full` (≈ 45 s here, ratio ×1.28).

### MINOR-3: `offer_inherited_file` re-maps calib.bin and reads it without re-validating
**Where:** `wp4_io.cpp:374-384`.

**Evidence:** the second `Reader` is opened with `verify = false`, and only the header/table hash and the array lengths are
compared. `ptr[i]` is then used as a pool offset without the monotone / ≤ |idx| checks. A replacement by rename is caught
(content hash, as shown in my probe and the PR's test). An in-place modification of section bytes between `read_calib` and the
offers is not caught, and could produce an out-of-bounds read. Engine files are written by rename (`format.cpp:109`), so this
is a TOCTOU window, not a live bug.

**Fix (any of):**
- keep `read_calib`'s Reader alive in `CalibIn` (`keep_alive()` plus the five pointers) and offer from the mapping that was
  validated, which also saves the reopen;
- or repeat the O(n) ptr bounds check in the offer loop, which costs nothing next to the offers.

### MINOR-4: `peak_rss_kb` and the phase RSS are Linux-only and approximate
**Where:** `include/v4/proc_mem.h:16`.

**Evidence:** `/proc/self/status` is Linux-only, and the code correctly falls back to −1. The kernel documents
RssAnon/RssFile/VmRSS there as approximate (split per-thread counters). I saw this at p = 2·10⁴: `tables_released` shows no RSS
drop after ~65 MB was freed (360.3 → 360.3 MB), and the drop appears one phase later. The end-of-run VmHWM is exact: it equals
`ru_maxrss`.

**Fix:**
- take `peak_rss_kb` from `getrusage(RUSAGE_SELF).ru_maxrss` (portable; kB on Linux);
- read phase samples from `/proc/self/smaps_rollup` (exact) or document them as approximate in INTERFACES §5.1.

### MINOR-5: the evidence for the 48G request, and the documentation around it
**Where:** `Docs/Experiments/P1M/results/MERGE_MEM.md` (on `exp/P1M`; it is **not** on the PR branch, contrary to the brief);
`tools/slurm/p1m_driver.py:77-78`.

**Assessment: plausible, not yet measured.**
- The plan formula at the pilot's sizes gives 26.2 GiB. The `--mem-budget` at 48G (90% = 43.2 GiB) admits it with 1.65× slack.
  At n = 1,000 IND the same formula gives ≈ 33 GiB (data.bin 8 GB), still admitted, assuming setup.bin and calib.bin keep the
  n = 200 sizes. My runs confirm that the plan bounds the process peak on the probe (×1.28 at 2·10⁴). The page-cache account of
  the 75.1 GiB is coherent with the P7 setup-task evidence.
- However, four inputs are projected rather than measured:
  - the attribution of 75.1 GiB to page cache is INFERENCE; no process peak from NOTS exists yet;
  - calib.bin ≈ 9.8 GB is a probe ratio, and it enters the largest phase (`offers`) 1:1;
  - the "≈ 34 GiB" (pre-fix) and "≈ 24 GiB" (post-fix) per-column extrapolations use the probe's setup layout
    (≈ 12.3 KB/col against the pilot's 10.1 KB/col), so they are not comparable with the 26.2 GiB plan computed at real sizes;
  - the probe ran 3 threads against 32 in production.
- The driver still requests 80G with the old comment.

**Fix / conditions:**
1. Before submitting, check `ls -l` of the pilot's calib.bin and island files on NOTS and re-evaluate the plan at those sizes.
2. Wire 48G into `p1m_driver.py` with a comment pointing to MERGE_MEM.md.
3. After the next 10⁶ merge, read `peak_rss_kb` and `timings.phases` and confirm `peak_rss_kb ≤ total`. Keep 80G as the
   documented fallback on an OOM.
4. Ideally land M-1 first, so that a mis-sized plan is refused before the offers.
5. Label the 34 and 24 GiB figures in MERGE_MEM.md as probe-layout extrapolations.

### MINOR-6: test coverage of the in-place validation, and a duplicated release helper
**Where:** `tests/test_wp4_io.cpp:546-595`, `src/common/store.cpp:22`, `include/v4/calib_plan.h:44`.

**Evidence:**
- The suite tests only the NaN-lg0 refusal and the different-file refusal for `keep_inherited = false`. The offsets, index,
  sortedness and length refusals are untested on the new path; my 18-case probe shows that they work.
- `Store::release()` duplicates `calib_plan.h`'s `release_table_stores` (`S.ttop = Store()` …).

**Fix:**
- Add the offset, index and length cases (a loop over mutations like those in `.rc_tmp/adv/adv_calib.cpp`; note that
  `fmt::Writer::add` keeps a pointer, so the edited vectors must outlive `write()`).
- Use one helper for the release.

## Contract and discipline
- **Writes:** everything is inside `engine_v4/`. There are no hard-coded paths and no file over 50 MB.
- **Contract:** the new fields match INTERFACES §5.1 (`meta.timings.phases`, the record's `peak_rss_kb`, `end_rss_kb`,
  `end_file_kb`, `write_fit_seconds`, the per-phase `mem_estimate`). They are execution statistics outside the bit-compared
  sections, as stated. The meanings of the existing `mem_estimate.total`, `one_island` and `extra` change: they are estimates,
  and no reader in the repository consumes them (grep of tools/ and tests/).
- **Scale:** the 32-bit offer index `inherited_event((uint32_t)i)` is unchanged from the base, and 8·10⁷ < 2³². The phase list
  grows with 2R′ entries, which is negligible.

## Sandbox
Everything was written under `<worktree>/.rc_tmp/`:
- builds: `build_head`, `build_base`;
- `TMPDIR`: `.rc_tmp/tmp`;
- the base checkout: `git worktree add --detach .rc_tmp/base 423decb5`;
- the probes, `e2e/` and `adv/`.

Nothing was deleted (the suite ran with `--keep`). No command needed approval and nothing outside the worktree was touched.
The review worktree is detached at `32f862c0`.
