# PR #12 (WP5 evaluator / law / driver / competitors) — disposition of the independent review (`PR12_review.md`)

Engineering manager, 2026-11-15. Verdict: ACCEPT-WITH-FIXES (0 CRITICAL, 1 MAJOR, 11 MINOR).
- Maths verified independently: the plug-in d_H² matches quadrature to 8e-14; the conjugate posterior and the raw-scale
  map are correct.
- T7 is a real independent Monte Carlo, 40/40.
- The driver cannot submit.

## MAJOR-1 — the store-law (Π̂^𝒯) metrics do not scale. ADOPT; this is a design decision (DECISIONS D-17)
**Fact (MEASURED by the reviewer).** At the planned (n, p), every S₀ ∪ {j} survives the 1e-12 cut, and together they
weigh 0.5–1.2× S₀. The posterior is spread over ~p one-null additions: the plan's "the weight sits on a handful" is
false. This is consistent with the feasibility study's π(S₀) ≈ 0.3–0.45 at (200, 10⁶). Reported to HQ.

**Decision (measurement methodology; it does not change any statement or definition in W3-DIST):**
1. `law.bin` stays as specified (D-8): it is the store-BMA law, truncated at relative weight 1e-12, capped at 10⁶
   components, with the dropped mass reported.
2. **Exact, cheap metrics over the whole law**, using closed forms per component (O(k²) each) and O(M) in total:
   - E_{π_𝒯}[d_H²(f_{S,θ̄_S,v̄_S}, f*)], the weighted plug-in Hellinger;
   - E_{π_𝒯}[prediction error];
   - the store-mass diagnostics.
3. **The posterior law of d_H under Π̂^𝒯, exact by sampling.** Draw a model ∝ π_𝒯 (binary search on cumulative weights),
   then (θ, v) from its conditional. Draws are stored **sparsely** (per-model columns).
4. **Mixture predictive Hellinger/KL of f̄^𝒯** (needs the mixture density at every (x, y) node). Estimated as
   - **exact top-K components** (K = 1,000 by weight), plus
   - a **stratified importance sample of the tail**: R = 1,000 components drawn ∝ weight (common random numbers across
     rows; refreshed per block of 500 rows).

   This gives an unbiased estimate of f̄ at each node. Report the estimate, its Monte Carlo SE (from ≥ 4 independent
   tail draws), the tail mass, and the exact top-K-only value with the bound
   |d_H(f̄, f*) − d_H(f̄_K, f*)| ≤ √(1 − π_𝒯(top-K)) (from H²(f̄, f̄_K) ≤ ε). The bias of √(estimate) is checked
   in T7′ (below).
5. **Streaming.** x and test rows are generated in row chunks, with only the columns of the components in use (gen_test
   is counter-based), never n_rows × |union of columns|.
6. Hoist the constant lgamma terms out of the per-component Student-t log density.
7. **Scale test T7′:** synthetic M = 10⁵ components, so that eval wall time and RSS are asserted against the driver
   limits (10⁴: ≤ 20 min on 4 CPUs, ≤ 8 GB; 10⁶: ≤ 1 h on 8 CPUs, ≤ 16 GB). Plus agreement of item 4 with the exact
   full-mixture value on a mid-size case (M = 5,000) within 3 MC SE.

## MINORs
| # | disposition |
|---|---|
| 1 FMA guard and binary block in eval/post | ADOPT (after rebasing onto exp/P1M-engine, which now holds WP1's v0.1.2 code, merge a4ca68c) |
| 2 fit.bin names not in INTERFACES | ADOPT: WP1 adds them to INTERFACES v0.1.3 (WP5 sends the list); WP4 uses them |
| 3 law.bin mode hard-coded to V | ADOPT: take the mode from fit.bin |
| 4 GUARD-W fails open | ADOPT: fail closed |
| 5 raw-scale intercept and draw covariance untested | ADOPT: add tests |
| 6 T7 barely exercises the m-term and v ≠ σ²; Σ not checked against gen | ADOPT: extend the fixtures (shifted intercept, v/σ² ∈ {0.5, 2}); test design_cov against gen-sampled covariances |
| 7 `--kill-on-invalid-dep=yes` | ADOPT |
| 8 department-path guards partial | ADOPT: strict, absolute, resolved-symlink checks |
| 9 driver test runs submit.sh with CONFIRM=yes via PATH | ADOPT: stub sbatch explicitly; the test must not be able to reach a real sbatch |
| 10 eval/post without a job manifest | ADOPT |
| 11 competitor package paths untested | DEFER: packages are installed later on NOTS in the department folder (decision pending); a mock test now |

Merge rule: WP5 pushes the fixes, then the same reviewer re-checks the diff (incl. T7′), then merge.
