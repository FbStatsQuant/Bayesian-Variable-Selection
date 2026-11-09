# C-MIS numerics — SUMMARY

Environment: Python 3.13 (numpy 2.3.0), run as `py -3.13 run_experiments.py <EXP>`; core `mis_core.py` (exact
posterior of the shipped target on the candidate design, full enumeration of Ω_𝒞, p_𝒞 = 10, K = min(10, ⌊n/2⌋)).
n ∈ {100, 200, 400, 800, 1600, 3200, 6400}, 20 seeds per n; σ² = 1. Raw rows: `<EXP>_results.json`; tables:
`<EXP>_summary.md`; console logs `run_all_output.txt`, `N3b_output.txt`. All statements below are about these runs only.

| Exp | Design | Tests | Result (n = 6400 unless said) |
|---|---|---|---|
| N1 | jointly Gaussian rows, candidates equicorrelated 0.3; omitted x_k = 0.6x₀ + 0.5x₁ − 0.4x₂ + z; β₃ = .8, β₄ = .6, β_k = 1 | Thm MIS (ii)/(iii): S₀^𝒞 = {0,1,2,3,4} (proxies 0,1,2) | median π(S₀^𝒞) .023 → .581 → .828 → .866 → .911 → .945 → **.956**; P(HPM = S₀^𝒞) = 1.00 from n = 400; naive S₀ ∩ 𝒞 = {3,4}: π → 0; null PIPs (5–9) ≤ .012 although all are marginally correlated with x_k; the *sample* projection of x_k on the candidates has 10/10 nonzero coefficients (dense) in every run ⇒ the limit is the population-projection support, not the sample one |
| N1b | as N1, candidate design fixed per n, (z, ε) redrawn | Thm MIS (i) (fixed candidate design, GR) | median π(S₀^𝒞) → **.948**; P(HPM = S₀^𝒞) ≥ .95 from n = 400 |
| N2 | precision chain 0 – 1 – k (Θ₀₁ = Θ₁k = −.45), others independent; β₅ = .7, β_k = 1 | Prop P(d): proxy = graph neighbour only | population γ = (0, .45, 0, …) = −Θ_𝒞k/Θ_kk (printed); corr(x₀, x_k) = .254 ≠ 0; mean PIP₀ → **.005**, PIP₁ → 1.000; median π({1,5}) → **.970** |
| N3 Δ = 0 | fixed design, EP with r = 0; weak signal b₅ = √(6 log n/n) (BM-ratio 6 w.r.t. σ²) | baseline | median π({3,4,5}) → **.963**, PIP₅ ≈ 1 |
| N3 Δ = 4 | same design, deterministic r ⊥ (1, X_𝒞), ‖r‖²/N = 4 (σ²_𝒞 = 5), same b₅ | dilution: BM-ratio w.r.t. σ²_𝒞 is 1.2 | PIP₅ ≈ .20–.35 at every n (not selected); median π({3,4}) → .868; π(S₀^𝒞) stays ≈ .11 — consistent with Theorem F, whose BM is stated with σ²_{𝒞,n} |
| N3b | as N3 Δ = 4 with b₅ = √(30 log n/n) (BM-ratio 6 w.r.t. σ²_𝒞 = 5) | Theorem F | median π(S₀^𝒞) → **.976**; P(HPM = S₀^𝒞) = 1.00 from n = 400; `max|X_𝒞ᵀr|` recorded (numerical zero) |
| N4 cancel | N1 with β₀ = −.6 (= −γ₀): true candidate 0 cancelled | Thm MIS (i) cancellation clause | mean PIP₀ → **.006** although 0 ∈ S₀; median π({1,2,3,4}) → .960 |
| N4 small | N1 with an extra small proxy coefficient a₅ = .08 | beta-min margin on β^𝒞 | PIP₅ = .08, .07, .10, .14, .18, .33, .72 along n: the small projected coefficient is detected only once θ² ≫ σ²_𝒞 log n/n (here θ₅² ≈ .0064 vs 2·log n/n = .0027 at n = 6400) |
| N5 square | ω = x₀² − 1 (non-GR; linear projection 0) | probe outside GR | median π({3,4}) → .962; mean PIP₀ fluctuates (.02–.11) |
| N5 product | ω = x₀x₁ − .3 (non-GR; linear projection 0) | probe outside GR | median π({3,4}) → .966; P(HPM = {3,4}) .85–1.00; mean PIP₁ up to .13 |

**Falsification verdict.** No run contradicts Theorem MIS, Proposition P or Theorem F/Corollary F (bounded p_𝒞 = 10).
The runs single out the population-projection support (not S₀ ∩ 𝒞, not the dense sample-projection support) as the
limit, confirm that proxies are graph neighbours (not merely correlated variables), that cancelled true candidates are
dropped, and that the beta-min scale is σ²_𝒞 (dilution). Rates: 1 − median π(S₀^𝒞) at n = 6400 is .03–.05, the order
of √(log n/n) = .037. Non-GR probes (N5) are exploratory and support no claim.

## Added after the mid-point review (R04)

| Exp | Design | Tests | Result |
|---|---|---|---|
| N6 | candidates as N1; omitted x_k independent of all candidates; y = 2 + x_k + ε (β^𝒞 = 0, σ_𝒞² = 2) | Lemma Z (null projection, bounded p_𝒞) | median π(∅): .904 → .936 → .955 → .963 → .977 → .984 → **.989** (n = 100…6400); P(HPM = ∅) = 1.00 from n = 400; mean PIPs ≤ .009 at n ≥ 1600 and ≤ .001 at n = 6400; 1 − π(∅) ≈ .011 at n = 6400, the order of n^{−1/2} = .0125 |
| N7 | Example E1: x₁, x₂, x₃, z iid N(0,1), x_k = −x₁ + x₂ + z, y = x₁ + x_k + ε | analytic target separation | median π({x₂}) → **.983**; median π({x₁}) (retained truth S₀ ∩ 𝒞) = .0000 at every n; median π({x₁,x₂,x₃}) (sample-projection support) → .0001; P(HPM = {x₂}) ≥ .95 at every n |

Scripts: `run_experiments.py N6`, `run_experiments.py N7` (outputs `N6_null_*`, `N7_*`). Inequality checks for L4:
`check_L4.py` (see `check_L4_summary.md` when present).

## check_L4 (inequality-level falsification of L4; p_𝒞 = 40, S₀^𝒞 = {0,1,2}, EP with Δ ∈ {0.5, 4}, n ∈ {200, 800},
10 seeds × 300 random models per cell; output `check_L4_summary.md`, raw `check_L4_results.json`)

| Check | Statement tested | Worst value over all cells (must be ≤ ~0 / ~1e-8) |
|---|---|---|
| C1 | Lemma S: Q^c_S = Q̃_S + ‖r‖² + 2rᵀe (relative error) | 4.9e-15 |
| C2 | L4.4(b) core: Q^c_S ≥ ‖r‖² + 2rᵀe + ‖(I − P_S)e‖² for S ⊇ S₀^𝒞 (lb − Q) | −2.62 |
| C3 | L4.4(c): 2b + Q^c_S ≤ E_n^𝒞 + V_S for underfitting S (lhs − rhs) | −7.67 |
| C4a | Lemma T uniform denominator: 2b + Q^c_{S′} ≥ ‖r‖² + 2rᵀe + ‖e‖² − ‖P_Ve‖² (lb − lhs) | −4.03 |
| C4b | Lemma T (B3) step: t_{S′} − t_{S₀} ≤ (n/(n+1))[‖(P_{S′} − P_{S₀})e‖² + η_n‖y‖²] (lhs − rhs) | −7.9e-3 |
| G5 | |rᵀe| ≤ σ‖r‖√(2 log n) held in 40/40 data sets; min(‖r‖² + 2rᵀe + 2 log n) = 80.5 > 0 | — |
No violation. (These are pathwise identities/inequalities; the check does not test the asymptotic rates.)
