# Pre-registration: benchmark rules for the c = 0.5 runs (and their labels at c = 1)

Registered 2026-10-21 by the lead, approved by the person the same day. Written before any c = 0.5 output from the study data has been scored or inspected for recovery (the c = 0.5 pilots are diagnostics-only and their truth stays locked). Basis: the eight fidelity audits (`verify/fidelity_c050/<method>/REPORT.md`) and the Fable ruling (`verify/fidelity_c050/FABLE_JUDGE.md`). The SHA-256 of this file is recorded in `RUNS.md` when it is frozen; any later change is a new dated section, never an edit.

## R1. Size bound for every EBIC rule (F1–F5, all γ)

- **Primary:** EBIC_γ (Chen & Chen 2008; OLS refit RSS on each path support; γ ∈ {1, 0.5} as before) minimised over path supports with size k ≤ K, **K = ⌊n / log n⌋ = 37** (n = 200). Rule ids `ebic1_K37`, `ebic05_K37` (and `bic_K37` where a BIC rule exists).
- Applies to F1, F2, F3 (companion EBIC rows), F4 (primary `ebic1_K37`), F4_SCAD, F5 (primary `ebic1_K37`).
- **Reason:** Chen & Chen's consistency theorem is stated for a bounded model size; K depends on n only, is the same for every method and invariant to c, and is truth-free. (The attribution of n/log n to Fan & Lv's screening size is from memory, not verified in a source read for this study.)
- **Secondary, kept:** the pre-declared cap-100 rules (`ebic1`, `ebic05`, `bic`), shown directly beneath.
- **Author-tuning rows (S0):** F4 `ebic1_lam005` (EBIC over the part of the path with λ ≥ 0.05·λmax, ncvreg's default end for n < p); F5 `sic_smax` (SIC = n log(RSS/n) + k·log p·log log n over s = 0..⌊n/(log p·log log n)⌋, = 19 at p = 500, 17 at p = 1000; Zhu et al. 2020).
- **Flag:** `ebic_at_largest` is redefined as "selected k > K" (counted for every rule), in addition to cap hits.
- **One code path:** these rows are computed by a single derived-rule unit from the saved per-case fits, for both scales; at c = 1 it must reproduce the existing derived K37 rows for F4, F4_SCAD and F5 exactly.
- **Labels:** at c = 0.5 these rules are pre-registered. At c = 1, `ebic1_K37` headline rows are labelled "post hoc (chosen from size diagnostics after the c = 1 run)", with the original pre-declared row kept beneath and never deleted.

## R2. Lasso-family CV rule (F1, F2, F3)

Primary stays `cv_min` (pre-declared; Tibshirani 1996). Every headline table shows `cv_min`, `cv_1se` and `ebic1_K37` side by side with equal prominence. Runtime tables (T5) footnote that `thresh = 1e-16` and the deep grid inflate glmnet runtimes 20–100× relative to package defaults.

## R3. Elastic net α grid (F2)

Grid frozen at {0.1, 0.25, 0.5, 0.75, 0.9}. Report per cell the α* distribution and the edge rate (α* = 0.9 in 1,200/1,200 cases at c = 1). State that EBIC candidates come from the α* path only.

## R4. SuSiE-refine (A1, new arm)

- New S1 arm `SuSiE-refine`: identical to A1 (L = 50 and all other settings) with `refine = TRUE` (the authors' shipped remedy for local optima). Run at **both** c = 1 and c = 0.5 on the same datasets and seeds.
- A1 default stays primary; SuSiE-refine is reported beside it, never substituted. Fit choice inside refine is by ELBO (package behaviour), not by outcome.
- Report per cell: ELBO gain over default, max |ΔPIP|, runtime.
- At c = 1 its label is "arm added after the c = 1 results were seen; fit selection by ELBO".
- `L_saturated` is renamed in reports to "all L effects active (possible weak-effect over-fitting)"; the 29 (A1) + 16 (L100) c = 1 cases are tabulated (scenario, σ²/var(y), overlap, supports). L is not changed.

## R5. SSL-RS (A2 variant)

Settings frozen. At c = 0.5 it is reported as "SSL with the Ray–Szabó ladder (variance/ladder sensitivity)", with the final σ̂ and the support-settling point of the λ0 ladder by cell.

## R6. Horseshoe (A3)

- D-c050-1 stands: budget 10,000 burn-in + 15,000 kept, thin 5, at every scale; flags (`ess_tau`, `ess_ci95`) reported per scenario × p, results on all fits and on passing fits; a longer-chain sensitivity of flagged fits (both scales) is reported beside, never substituted.
- Added: a diagnostics-only c = 0.5 run on the 12 dev datasets with the production budget and a second chain (different method seed), reporting per p and per scenario the flag rate and the two-chain Jaccard of `ci95`. Any budget change would apply to both scales with c = 1 rerun.
- Captions state that `ci95` is bayesreg's own printed 95%-interval indicator, that `km2` has no verified literature source, and that a marginal 95% rule under-selects by construction when effects are small.

## R7. Rule-driven effects to state in captions

- A3 `ci95` under-selects at weak signals by construction (R6).
- A1 `bfdr10` adds false positives by construction when true PIPs are near 1 (at c = 1 exactly one extra in 1,170/1,200 fits).
- F5 is labelled "ABESS (splicing heuristic)"; its supports are not polished.

## R8. SMC-BVS support bound (person's decision, 2026-10-21)

SMC-BVS keeps its prior support bound ⌊n/2⌋ = 100. The paper states why a candidate-size bound required by EBIC theory (R1) differs from a prior support bound.

## R9. Auditor probes

Some auditors ran local single-seed probes on data from their own generator and seeds (not the study data) and saw TP counts. These counts are never cited as evidence. No rule above has a free parameter set from them.

## What does not change

No existing c = 1 arm is rerun. Fit code, hyperparameters, seeds, data and truth are unchanged for F1–F5, A1 (default), L100, A2, SSL-RS, A3. c = 0.5 production runs the c050 copies, whose diffs are infrastructure-only and whose c = 1 reproduction must be bit-identical before launch.
