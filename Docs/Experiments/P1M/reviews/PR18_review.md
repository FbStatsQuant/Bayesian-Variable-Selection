# PR #18 review — WP5 follow-up to PR #12: what the √δ truncation bound covers; disjoint rows in the x-doubling check

Reviewer: Opus 5.5 (independent of the author), high effort; brief `briefs/REVIEW_PR_template.md` (N = 18).
Scope: `exp/P1M-wp5-followup` @ eb3ea86 into `exp/P1M-engine` (base d04a219 = merge of PR #12), one commit, 5 files,
+41 / −16, all under `Scripts/SMC_BVS/engine_v4/`. Context: PR12_review.md final re-check, notes N-1 and N-2; Sol F9.
Checkout: detached worktree, read only (no pushes, no GitHub comments).

## Verdict: **MERGE** (ACCEPT)

Both notes from the PR #12 re-check are closed.
- **N-1.** The truncation bound is now stated per field, and every stated bound is correct (derivations below).
- **N-2.** The x-doubling check now compares estimates on disjoint row sets, against the combined SE.

Production behaviour does not change: `x_row0` defaults to 0, and the CLI does not expose it. The two notes below are
non-blocking.

Counts: CRITICAL 0 · MAJOR 0 · MINOR 0 · notes 2.

## Tests I ran (Owls, `nice -n 19`, 3 threads, TMPDIR `~/SMC_Engineering_Department/tmp/20261116-review-pr1819`, removed after)
- `tests/run_tests.sh --quick --threads 3`: **61 test cases, 0 failed**, rc = 0.
  - WP5 Slurm-driver tests: OK (12).
  - Competitor harness: OK (packages missing on Owls, as before).
- `wp5_predictive_numerical_error_doubling`:
  - GH 64 → 128 changes d_H² by 1.3e-15 and KL by 1.2e-16.
  - The estimate on disjoint rows 4,000 … 11,999 differs from the one on rows 0 … 3,999 by **1.9e-4** for d_H²
    (combined x-SE 1.6e-4, z ≈ 1.2) and by **7.3e-4** for KL (combined SE 6.2e-4, z ≈ 1.2). These match the README
    exactly.
- `wp5_e2e_post_and_eval` asserts the new `law_truncation` fields (`not_covered` has 3 entries, `kl_upper_add`,
  `post_dH_tail_prob_bound`).

## (1) The truncation statement, field by field (dist.cpp:458-481; README_WP5.md:44-49)
Write the store law as (1 − δ)·law + δ·omitted, where δ = `dropped_mass`. That is the summed omitted mass over all of
𝒯, so the law's own weights are normalised to sum to 1. I checked each claim:
- **Predictive d_H, within √δ.** f̄_store ≥ (1 − δ) f̄_law pointwise, so the Bhattacharyya coefficient is at least
  √(1 − δ). Hence H² ≤ 1 − √(1 − δ) ≤ δ, and the triangle inequality gives the √δ bound. **Correct**; the code now
  says "predictive d_H only".
- **`weighted_plugin.h2`, within δ.** The store value is (1 − δ)·h_law + δ·h_om with both in [0, 1], so the
  difference δ(h_om − h_law) ∈ [−δ, δ]. **Correct.**
- **`post_dH`.**
  - Tail probabilities: |F_store − F_law| ≤ δ for every threshold. **Correct.**
  - Mean of d_H ∈ [0, 1]: same argument as `weighted_plugin.h2`. **Correct.**
  - Quantiles: let q be the law's α-quantile. Then F_store(q) ≥ α − δ gives q ≥ q_store(α − δ). For t < q,
    F_store(t) < α + δ gives q ≤ q_store(α + δ). **Correct.**
- **KL and mlpd, one-sided.** f̄_store ≥ (1 − δ) f̄_law gives KL(f*‖f̄_store) ≤ KL_law − log(1 − δ) and
  mlpd_store ≥ mlpd_law + log(1 − δ). **Correct**, assuming KL is taken under f*. It is: the KL rule is under f*
  (PR12 review §a). `log1p(−δ)` is the right numerically stable form.
- **Not covered: `plugin`, `weighted_plugin.pred_error`, `test.mse`.** These are means of unbounded functionals of the
  omitted models, or plug-ins at the BMA posterior mean. **Correct** to leave them unbounded.

## (2) Disjoint rows (dist.cpp:577, 612; eval.h:142; test_scale.cpp:183-215)
- `x_row0` shifts the integration rows. The test rows follow at x_row0 + n_x, so integration and test rows stay
  disjoint within a call.
- Rows come from `gen::generate_test_rows` and are counter-addressed. The 8,000-row estimate on rows 4,000 … 11,999 is
  therefore independent of the 4,000-row estimate. The law is exact (`pa.exact` is asserted), so there is no tail
  sampling noise.
- The combined SE √(SE₄₀₀₀² + SE₈₀₀₀²) is the right SD of the difference. A 5-SE threshold is now 5 SDs of the
  difference, not about 7 as in v1. N-2 is resolved.
- The first call's test rows (4,000 … 4,199) overlap the second call's integration rows. This is harmless: test
  metrics are not compared.

## Notes (non-blocking; fix whenever the README is next touched)
- **N-a: some fields of the dist block are not classified.** The list covers the main fields, but four are in neither
  list:
  - `predictive.h2` (= d_H²): the bound is on d_H. For d_H² it is |h2_store − h2_law| ≤ √δ·(2·dH_law + √δ).
  - the `n_h2` scalings: the bound is multiplied by n.
  - `weighted_plugin.h2_sd`;
  - `h2_topK` / `dH_topK`.

  Add one line naming these, or state that `not_covered` lists only the unbounded fields.
- **N-b.** `x_row0 + n_x + n_test` is computed in uint32. It cannot overflow at any realistic size, and `x_row0` is a
  test-only field. If the field is ever exposed in the CLI, validate it there.

## Checklist items with no finding
- **Discipline.** Nothing is written outside `engine_v4/`; there are no new hard-coded paths and no large files.
- **Contract.** `law_truncation` only gains new keys; existing keys and values are unchanged (`dH_bound_truncation`
  is still √δ, and the e2e test still asserts that).
