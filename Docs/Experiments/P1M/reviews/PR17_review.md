# PR #17 review — WP1: INTERFACES v0.1.6 (inherited calibration HPM provenance, gen row ranges, §6 x87 wording)

**Reviewer:** Opus 5.5 (reviewer of PRs #11, #14, #15), 2026-11-16.

**PR:** `75cef83` → `exp/P1M-engine`.

**Scope:** `git diff origin/exp/P1M-engine...75cef83` only.
- One commit, 6 files, +48 / −11, all inside `Scripts/SMC_BVS/engine_v4/`.
- The branch's `INTERFACES.md` (v0.1.6) is identical to the docs copy.

**Method:** read-only, in my own worktree; nothing pushed, nothing posted on GitHub.

## Verdict: **MERGE**

There are 0 blocking findings and two informational notes.

## Test run (MEASURED)

| Item | Value |
|---|---|
| Machine | Owls, GCC 11.5.0, glibc 2.34 |
| Command | `TMPDIR=/home/fb31/SMC_Engineering_Department/tmp/20261116-review-pr17 tests/run_tests.sh --full --threads 3` (nice 19, -j3), clean build |
| Result | **41 / 41 PASS**, 0 check failures, 48.0 s wall |
| New case | `gen_test_row_ranges` passes, as does the existing `gen_test_rows` |

## (a) Inherited calibration HPM keeps its calibration EventCtx (INTERFACES §4.2): correct

The new rule: every inherited-step offer of the calibration HPM model carries that model's calibration EventCtx, and
every other inherited model carries an INHERITED key. I checked it against what v3 does
(`core/cpp/v3_core.cpp:416-440`):
- v3 offers each inherited model with the INHERITED context.
- After that, v3 replaces the HPM provenance with the calibration provenance only if both of these hold:
  - the ledger's HPM still has phase INHERITED;
  - that HPM is the calibration HPM model.

With the new rule, the smallest-key rule gives the same result in every case:

1. **The HPM model is also a table model.** v3 keeps TABLE, because the table offer came first and an equal later offer
   does not replace it. In v4 the table key (segment 0) is smaller than the calibration key (segment 2), so v4 also
   keeps TABLE ✓.
2. **The HPM model is not a table model, but is in the inherited list.** v3 replaces "inherited" with the calibration
   provenance. In v4 that model's inherited offer already carries the calibration key, so there is no INHERITED key to
   win. Later final-island events (segment 3) and local-search events (segments 4–5) have larger keys. The result is
   the calibration provenance ✓. This is the case named in the PR.
3. **The HPM model is not in the inherited list.** v3 compares `to_internal(hp$model) == led.hpmS`, which fails, so
   nothing is replaced. v4 has no offer of that model to label, so there is nothing to compare ✓.

Counters are unaffected. Inherited offers emit 0 logical events (§4.2 table) and do not touch `island_best`, so the
calibration phase and mechanism labels carried by that offer cannot leak into `logical[PH_DIAG]` or similar counters.

**Note 1 (information).** This is contract text only; WP4's merge implements it.
- WP4 should add a test with the HPM model present in both the inherited list and the tables, and with it present only
  in the inherited list.
- v3 replaces the provenance only when the calibration output contains a `provenance` field
  (`hp.containsElementNamed("provenance")`). v4's calibration record always carries `hpm_ev`, so this guard has no v4
  counterpart. That is fine.

## (b) `gen::generate_test_rows(s, a, b, …)`: correct

How it works:
- **Addresses** use the global row i (`particle = (uint32_t)i`), and the output is indexed by the local row r = i − a
  (`src/common/gen.cpp`).
- **Range check:** a < 0, b < a or b > 2³² − 1 is refused with `invalid_input`.
- **`generate_test(s, nt, …)`** is now `generate_test_rows(s, 0, nt, …)`. The per-row arithmetic is unchanged, so it
  produces the same bits as before.
- **Threads:** rows are independent, so the bits do not depend on the thread count.

Test `gen_test_row_ranges` (`tests/test_gen.cpp`):
- **4 designs** (AR, IND, BLK, ADJ-OPP) × **5 ranges**: [0, 37), [5, 6), [10, 30), [36, 37) and the empty range
  [12, 12).
- Every value of X and y is bit-identical to the matching row of the full 37-row design.
- The column set (`out_cols`) is the same.
- A reversed range is refused.

The existing `gen_test_rows` test still checks the AR Markov transition against `normal_at` directly.

**Note 2 (information).** The bounds check accepts b up to 2³² − 1, so `(size_t)(b − a) × |cols|` doubles can be
requested in one call. That is a caller-side memory concern only; WP5's chunking makes it moot.

## (c) INTERFACES §6 wording after the NOTS x87 result: correct

- §6 now says the x87 rows are measured equal on NOTS (jobs 2747666 and 2747875).
- This matches `results/PMATH_NOTS.md` §"Re-run with the x87 rows": `expl` 90880997… and `logl` 475c1128… are equal on
  NOTS, and all 8 guarded rows match.
- These are exactly the `REF` hashes in `src/common/pmath_info.cpp`, whose comment and the one in `pmath.h` were updated
  to match.
- The PR15 review's N5 is therefore closed.

Temporary files: `/home/fb31/SMC_Engineering_Department/tmp/20261116-review-pr17` was removed after the run.
