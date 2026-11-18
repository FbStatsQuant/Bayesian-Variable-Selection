# W3-DIST — PLAN (v1.0, 2026-11-15; lead: Claude Fable 5.2, Claude Third, high)

## Goal
A Song–Liang (2015) Theorems 1–2 analog for the method: (i) Hellinger consistency of the exact coded posterior for the
joint (x, y) law under a random design, at [SL]'s strength (A1 checklist P1–P5); (ii) the same for what the coded SMC
returns (P6). This leg: scoping to CP1.

## The idea in four lines
1. Condition on the design. In the Gaussian conjugate working model everything about the posterior is explicit, so
   the in-sample statement can be proved with exponential probabilities by chi-square tails (Lemma X, Lemma S).
2. Models that overfit by a few variables are *good* for the Hellinger distance. So the inner threshold can be
   e^{−ct} although 1 − π(S₀) cannot be smaller than n^{−1/2}. Distribution consistency is easier than selection.
3. Pass from the n design points to the population by a distribution-free VC bound on a **truncated** squared mean
   error (Lemma H + Lemma T). No moment condition on the predictors is needed for this step.
4. The coded prior does not satisfy [SL]'s sieve conditions (cap K = n/2, size prior ≈ geometric(½)); dimension is
   controlled by the slab's Occam factor, which is present unless columns are nearly exactly dependent ((ND)).

## Steps of this leg
1. Read inputs (done). 2. STATEMENT v1.0, ROUTES, DEPS, ASSUMPTION_MAP (done). 3. Helpers: H1 prior probe (Opus),
H2 numerics harness (Sonnet) — also the boundary-violation numerics of the sharpness gate. 4. Freeze manifest S1;
blind Astra read (statement lock + break + better theorem). 5. Dispositions; STATEMENT changelog if anything changes
(a WEAKER edit to a target = early checkpoint). 6. CHECKPOINT_1.md with the parity table, GO plan, team plan.

## Proof leg (pre-authorized by HQ; details and kill budgets in CHECKPOINT_1.md)
Order: H, T (line-check first) → S → X → DIST-1 → X′/DIST-2 → DIST-3 and fallbacks → P6/DIST-C → bridges B1, B2 →
stretch S-APX, S-EXP → S-FIT (one attempt).
