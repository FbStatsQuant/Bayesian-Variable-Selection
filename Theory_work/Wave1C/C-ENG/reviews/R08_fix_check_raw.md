# R08 — check of the R07 fixes (ef33f91..98fac03), Codex gpt-6.1-sol, reasoningEffort high, fresh delegate, read-only.
Verbatim reply, received 2026-11-09 ~00:08 CST.

---

**R07 finding 1 — RESOLVED.**

`Scripts/SMC_BVS/core/v3_fit.R:45` now charges:

```r
(2 * ls0_scans + 4) * (12 * K + 256) +
  96 * ls0_scans + 4 * (8 * W + 4 * K + 96)
```

This provides sufficient allowance for the inspected C++ archive and its simultaneous R representation:

- Archived models are copied at `v3_engine.h:407,412`; outer-vector capacity growth also requires unused vector slots.
- `local_to_list` copies models and parallel arrays while `A0` remains alive (`v3_core.cpp:350–356,478`).
- Appending `move_cap` and `move_cap_rule` (`:479`) can allocate replacement top-level lists and names. These are shallow extensions; they do not duplicate every model.
- Scalar fields, names, termination strings—including the longer `"no_improvement"`—and the rule string require fixed overhead.

Independent R measurements plus separate C++ accounting, including doubled outer-vector slots and simultaneously live list-extension containers, remained below the production allowance:

| K | Maximum scans | Accounted bytes | Allowance |
|---:|---:|---:|---:|
| 3 | 13 | 8,572 | 10,600 |
| 30 | 39 | 35,392 | 55,152 |
| 100 | 112 | 218,568 | 345,216 |
| 1,000 | 1,016 | 16,584,616 | 25,068,160 |

The committed validation provides useful independent R-size evidence, but has the regression-test weakness below.

**R07 finding 2 — RESOLVED.**

`v3_fit.R:45–47` adds the archive component and evaluates total memory before calling `time_fun(K)`. Both initial and escalation preflights use this implementation (`:115,145`).

Independent spies at tiers 0 and 1 confirmed that the large-memory rejection performs **zero benchmark calls**, reports `timed = FALSE`, and returns scalar `exceeds = TRUE`. The skipped benchmark leaves its estimate `NA`, but the memory predicate already establishes rejection; `:65` preserves it without introducing `NA`.

The exact branch retains its shipped benchmark ordering, as required by compatibility.

**New finding — MINOR: Archive regression test does not check the production allowance.**

Location: `Theory_work/Wave1C/C-ENG/tests/test_preflight.R:66–70`

```r
allowance <- (2 * scans + 4) * (12 * K + 256) +
  96 * scans + 4 * (8 * W + 4 * K + 96)
...
check(..., allowance >= r_bytes + cpp_bytes)
```

**Scenario:** Replacing the production archive allowance with zero would leave these four checks passing: they evaluate their own copied formula. The former assertion connecting the memory increment to actual preflight output was removed. The public-fit check verifies only that the component exists.

**Fix:** Obtain `allowance` from an actual `v3_preflight(...)$memory_components[["ls0_archive"]]` call for each fixture. Retain the independent R measurement and explicitly account for outer-vector spare slots, fixed metadata, and temporary shallow list extensions in the C++/conversion calculation.

**Compatibility and limits.** Controlled comparisons against `8a27652` returned identical preflight records in 36 combinations covering both branches, both tiers, several dimensions, and several allocations with the LS0 charge disabled. Both compatibility switches select that unchanged path. The runtime charge remains an explicitly documented operational heuristic; these checks do not establish a rigorous score-plus-cache/store runtime bound.

I performed read-only inspection and in-memory R probes; I did not rerun the artifact-writing full test script.

**Verdict: APPROVE-WITH-FIXES** — both MAJOR findings are resolved; fix the regression-test connection above.

## Disposition (C-ENG)
- New MINOR ACCEPTED: the test now reads the allowance from actual `v3_preflight(...)$memory_components[["ls0_archive"]]`
  calls, keeps the independent R measurement, and adds outer-vector spare slots and 2 KiB of list-extension/name overhead
  to the C++/conversion estimate. A fifth fixture (n = 6, p = 40, K = 3) then showed the fixed overhead exceeding the
  allowance at tiny K; the production allowance gained a fixed + 4096 bytes. All 5 fixtures pass; test 14/14
  (`numerics/out_test_preflight.txt`). The +4096 constant is checked in R09.
