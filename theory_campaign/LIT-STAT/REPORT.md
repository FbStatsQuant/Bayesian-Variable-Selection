# LIT-STAT — REPORT: statistical literature on BVS posterior concentration, selection consistency and decision rules

Run LIT-STAT, 2026-11-02, branch `theory/LIT-STAT`. This is a literature audit. It contains no new theorem of record. The only
mathematics here is one elementary computation, PROVED, with an exact-arithmetic script: BB(1,p) is not a complexity prior in the sense of
CSvdV (2.2). Every other claim either quotes a source I read (file or URL in §4) or is my **assessment**, labelled as such. Anything I saw
only second-hand is marked UNVERIFIED. Per-source working notes with longer quotations are in `notes/01–05`.

Our objects (from `00_COMMON.md`): standardised X, y; slab β_S ~ N(0, nσ²(G_S+I)⁻¹) (a ridge-stabilised unit-information g = n prior);
σ² ~ IG(0.01, 0.01); size prior BB(1,p) with w(k) = ½/C(2p−1,k) = B(k+1, 2p−k)/B(1,p), capped at K = min(p, ⌊n/2⌋).

## 1. Headline

1. **Thm 1 (T03♯) is a modest extension of known results, not a new phenomenon.** Its architecture (dimension bound, then no strict
   supersets, then beta-min recovery) is the field's standard template (CSvdV 2015; BCG review 2026). The closest prior art is
   **Rossell (2022, Bayesian Analysis)**. He proves concentration for Zellner priors with τ = 1 (unit information), a **non-complexity
   Beta-Binomial** model prior, polynomial p, and eigenvalue quantities anchored at the true model, with L¹ rates. **Moreno–Girón–Casella
   (2015)** prove g = n plus a hierarchical-uniform model prior consistent for k = O(n^b), b ≤ 1. Several things are genuinely ours:
   - BB(1,p) rather than BB(1,1);
   - the cap K = ⌊n/2⌋, which is not o(n) (Rossell needs p̄ ≪ n);
   - the ridge slab;
   - the size-cutoff device m♯_n of T02(i♯), which lets SE be imposed only up to size m♯_n ≈ s₀ + O(log n).
2. **T03♯(3), P(S† ≠ S₀) ≤ 2E₀[1 − π(S₀)], is KNOWN.** It is Rossell (2022) Proposition 1 verbatim, and Rossell states that it also holds
   for the MPM. Thm 4 (T21) and Thm 5(0) inherit this term, so the paper must cite it.
3. **Prop 1 (T07):**
   - (ii)(a), the HPM as the Bayes rule under 0–1 loss, is textbook.
   - (ii)(b), the MPM as the Bayes rule under Hamming loss, is folklore; it is the same coordinate-wise algebra as the proof of
     Barbieri–Berger (2004) Thm 1.
   - (ii)(c), the capped version, is a trivial variant that I did not find stated.
   - (i), the within-size ceiling, is a one-line observation. After targeted searches I found it **not stated** anywhere, including
     Berger–García-Donato–Pericchi (2026), a paper devoted entirely to size-only model priors.

   Prop 1 is correct bookkeeping, not novelty.
4. **The exact BB(1,p) tail (T02(i♯)) is the most distinctive statistical piece.** Under BB(1,p) the dimension prior has ratio
   (p−s+1)/(2p−s) ≈ ½ (PROVED; `scripts/bb_ratios.py`). So BB(1,p) violates CSvdV's exponential-decrease condition (2.2) for every fixed
   A4 > 0, and CSvdV's Thm 1 and Cor 1 do not cover it. CSvdV's own example needs Beta(1, p^u) with u > 1, and Cor 1 needs A4 > 1. I found
   no published dimension or tail bound for the BB(1,p) / g = n pair in which the Occam factor of the slab, not the prior, carries the size
   penalty. Rossell's §5.2 is the nearest result: BB(1,1), with p̄ ≪ n.
5. **The naive-merge proposition (A-DRAFT Prop M) formalises a known phenomenon.** That phenomenon is omitted-variable bias in block-wise
   or marginal fits. Papaspiliopoulos–Rossell (2017) state that block-local exactness requires a block-diagonal Gram matrix and is only a
   heuristic otherwise. Prop M is a clean COUNTEREXAMPLE for motivation, not a contribution.
6. **What the literature lacks.** Nothing I read proves anything about the **reported** (best-scored) HPM of a finite-budget algorithm when
   the posterior is fine but the start is masked. The papers that couple statistics with computation (YWJ 2016, Zhou et al. 2022,
   Hou–Atchadé) assume local Bayes-factor monotonicity ("Condition 1"), complexity priors with κ₀ ≥ 2, and g ≥ p. Our masked-regime results
   (Thms 2, 3, 5) sit outside all of that. API-POS already showed that the LH posterior itself satisfies Condition 1(b), so the novelty is
   the start-law analysis, not posterior multimodality.

## 2. Annotated table, one row per work

Columns:
- **PROVED:** the source's exact statement, compressed, with its conditions.
- **Holds for our designs?** Whether those conditions plausibly hold for the linked-hub family (LH) or the study designs (n = 200,
  p ∈ {500, 1000}, s₀ up to 14, correlated designs with dilution).
- **Relation to ours:** registry IDs and branches.

The "holds for our designs" entries are my **assessment**, except where a computation is shown.

| # | Work | Venue / year | Method | PROVED (source's statement, compressed) | Holds for our designs? | Relation to ours |
|---|---|---|---|---|---|---|
| 1 | Castillo, Schmidt-Hieber & van der Vaart | Ann. Statist. 43(5), 2015 | Point mass plus Laplace(λ) slab; dimension prior with exponential decrease; σ known | Thm 1: Π(\|S\| > s₀ + (M/A4)(1 + 16λ/(φ(S₀)²λ̄))s₀ \| Y) → 0, needing only φ(S₀) (anchored). Thm 4: no strict supersets if A4 > 1. Cor 1: E Π(S = S₀ \| Y) → 1 under compatibility, A4 > 1 and beta-min ≳ \|S₀\|√log p/‖X‖ (uniform over β₀) | **No for our prior**: BB(1,p) has A4 = log 2/log p → 0 (§4 script), and the slab and σ assumptions differ. For LH and the study as data-generating designs, compatibility is plausible for LH but not checked for the study | Same architecture as T03♯ (T02(i♯) ↔ Thm 1; T02(ii♯) ↔ Thm 4; T03♯ ↔ Cor 1). **Complementary**: neither implies the other. CSvdV is uniform in β₀ and allows p ≫ n; T03♯ handles a non-complexity prior with g = n |
| 2 | Castillo & van der Vaart | Ann. Statist. 40(4), 2012 | Sequence model, spike-and-slab | Dimension and recovery theorems under exponential decrease (2.2). Ex. 2.2 gives Beta-binomial calibration κ/(κ+λ) ∈ (c/n, Cp_n/n). Thm 2.8 and the text after it: "g_S needs to have heavy tails" | Sequence model, so not directly. The Gaussian-slab caution is absorbed by our hypothesis R (‖μ‖² ≤ Mn) and the growing unit-information scale (assessment) | Background for T02 and T03♯. The heavy-tail warning is a referee point on the Gaussian slab |
| 3 | Yang, Wainwright & Jordan | Ann. Statist. 44(6), 2016 — **UNVERIFIED** (read only via #4's Thm S2) | g-prior with 1+g = p^{2κ₁}; π₀(γ) ∝ p^{−κ₀\|γ\|} with a hard cap s₀; RW-MH | Conditions A–F, among them: min over **all** \|γ\| ≤ s₀ of Λ_min ≥ nζ; κ₀ ≥ 2; s₀ ≤ n/(32 log p) − C₀/4; β²_min ≥ 128(κ+C₀+C₁)log p/(ζ²n). These give Condition 1 w.p. 1 − O(p^{−a}), hence concentration and rapid mixing | **No.** Our κ₀ ≈ 1 (per-model ratio s/(2p−s)) and g = n < p. At n = 200, s₀ ≤ n/(32 log p) gives s₀ ≤ 1.006 (p = 500) or 0.905 (p = 1000), so it fails for any s₀ ≥ 1 even with C₀ = 0 | Overlaps T03♯ (concentration) under a stronger prior. Complementary to Thms 2, 3 and 5: under Condition 1 there is no masking. Already analysed in API-POS (YWJ/ZYVR applicable to LH with **their** priors) |
| 4 | Zhou, Yang, Vats, Roberts & Rosenthal | JRSS-B 84, 2022 (venue from INDEX, UNVERIFIED; read arXiv:2105.05719v3) | Locally informed MH (LIT-MH) | Thm 1: dimension-free mixing under Condition 1 with c₀, c₁ conditions, n = O(p), s₀ log p = O(n), κ = O(s₀) | As for #3 | Computational. Same relation as #3 |
| 5 | Narisetty & He | Ann. Statist. 42(2), 2014 | Shrinking spike N(0, σ²τ₀²) and diffusing slab N(0, σ²τ₁²); q_n ∼ 1/p | Thm 4.1/4.2: P(Z = t \| Y) → 1 under log p = o(n), nτ₁² ∼ n ∨ p^{2+3δ}, \|t\| fixed, an identifiability Δ_n(K) over \|k\| < K\|t\| anchored at t, and design regularity | **No for our prior.** Their slab gives a per-variable Occam penalty ≳ p^{1+δ}; ours gives √(n+1) < p. Their per-model q_n ∼ 1/p matches BB(1,p)'s per-model ≈ 1/(2p) | Closest in spirit to SE_λ and SE_w: anchored, size-restricted identifiability. Shows anchored conditions are **standard**, not new |
| 6 | Johnson & Rossell | JASA 107, 2012 | Non-local pMOM/piMOM vs local priors | Thm 1: nonlocal (r ≥ 2) ⇒ p(t \| y) →_p 1 for p ≤ n with eigenvalues bounded. **Thm 2: local prior, p(k)/p(t) > δ > 0 and p > n^{1/2+ε} ⇒ p(t \| y) → 0 a.s.** | Thm 2's hypothesis (3) fails for BB(1,p): w(s₀+1)/w(s₀) = (s₀+1)/(2p−1−s₀) → 0. Thm 1 needs p ≤ n, but the study has p > n | **No contradiction with T03♯.** T03♯ (local prior, p = n^A, A > 1) is consistent because BB(1,p) breaks JR's hypothesis (3). Worth a sentence in the paper |
| 7 | Shin, Bhattacharya & Johnson | JASA 113, 2018 | Nonlocal peMOM/piMOM; uniform prior on \|k\| ≤ q_n | Thm 1/3: π(t \| y) →_p 1 under log p = O(n^α) and a sparse Riesz condition over all \|k\| ≤ q_n (unanchored) | Not our prior | Background. Their remark that BB is "asymptotically negligible" for \|k\| ≤ q_n ≺ n is a heuristic |
| 8 | **Rossell** | **Bayesian Analysis 17(2), 2022** | Zellner (τ fixed or growing, known or IG variance) and pMOM; model priors uniform, BB(1,1), Complexity(c); max size p̄ | **Prop 1: P(k̂ ≠ t) ≤ 2E(1 − p(M_t \| y)), for both HPM and MPM.** §5.2 (BB, spurious models): with τ = 1, "can handle p − p_t ≪ n^{a/2}", i.e. polynomial p, with an explicit L¹ rate. §5.4 Prop 9: non-spurious models via v_tm, the smallest nonzero eigenvalue of X_t′(I−H_m)X_t/n (anchored at t), plus (F1). Needs (B1) p̄ ≪ min{n, p, nτ} | Prior class is close (unit information, non-complexity BB, IG on φ), but ours is BB(1,p) with K = n/2, so (B1) fails for our cap. Asymptotic, so it has no force at n = 200 | **Main threat to T03♯'s novelty, and the source of T03♯(3) and the 2E₀δ₁ term of T21 and Thm 5(0).** T03♯ is a modest extension: a different BB, a cap of order n handled by the exact tail, and a ridge slab |
| 9 | Moreno, Girón & Casella | Stat. Sci. 30(2), 2015 | g = n, mixtures, intrinsic priors vs Bernoulli and hierarchical-uniform model priors | Thm 3: for k = O(n^b), (i) Bernoulli prior consistent iff b < ½ (inconsistent for ½ ≤ b ≤ 1); (ii) hierarchical uniform consistent for 0 ≤ b ≤ 1 | k ≤ n only, but the study has p > n | Direct ancestor of "g = n plus a multiplicity-correcting model prior is consistent at polynomial p". T03♯ extends it to A > 1 under SE/BM |
| 10 | Liang, Paulo, Molina, Clyde & Berger | JASA 103, 2008 | Mixtures of g-priors | §4.2 Thm 3: model-selection consistency for fixed p (hyper-g, ZS, EB). Text extraction garbled, so PARTIALLY VERIFIED | Fixed p | Baseline only |
| 11 | Scott & Berger | Ann. Statist. 38(5), 2010 | Fully Bayes vs EB multiplicity | "selecting p = 1/2 does not provide multiplicity correction"; a prior on the inclusion probability gives "an automatic multiple-testing penalty" | n/a (prior design) | Motivates the size prior. Size-only priors adjust multiplicity, not within-size ranking (the context for T07(i)) |
| 12 | Wilson, Iversen, Clyde, Schmidler & Schildkraut | Ann. Appl. Stat. 4(3), 2010 | BetaBinomial(a, b) model prior (eq. 2.7) | Recommends a = 1, with b reflecting the expected model size | n/a | **Origin of our BB(1,p)** in the citation chain. Berger et al. (2026) credit it as "π(p) = Beta(p \| 1, k)" |
| 13 | Barbieri & Berger | Ann. Statist. 32(3), 2004 | Predictive squared-error loss | Thm 1 / Cor 1–2: MPM is the optimal predictive model when Q is diagonal plus (17), for graphical, all-submodel or nested model spaces. The proof is coordinate-wise thresholding at ½ | Q diagonal means an (essentially) orthogonal design, which LH and the study are not | Different loss (prediction). Same algebra as T07(ii)(b). The HPM ≠ optimal-predictive caveat is relevant to how we frame the HPM |
| 14 | Barbieri, Berger, George & Ročková | Bayesian Analysis 16(4), 2021 (venue UNVERIFIED; read arXiv:1807.08336v2) | MPM under correlated designs | Thm 3.1 "mini-theorems" for q = 2 only. The authors report counterexamples to each in dimension 3. Discusses near-duplicates and "dilution" | Correlated designs are exactly the issue, but the loss differs | Complementary. A citation point for dilution with correlated predictors |
| 15 | Papaspiliopoulos & Rossell | Biometrika 104(2), 2017 (venue UNVERIFIED; read arXiv:1606.03749v2) | Exact BVS for block-diagonal Gram matrices; heuristic otherwise | Exact HPM of each size and PIPs when X′X is block-diagonal. For general designs, spectral-clustering block approximation plus a "forward-backward heuristic" | LH and the study are not block-diagonal | **Naive merge (Prop M)**: their exactness condition is what fails. Prop M quantifies the failure at p = 2. Also relevant to the v3 block start (A-DRAFT's computational audit) |
| 16 | Ročková & George | JASA 113(521), 2018 | Spike-and-slab LASSO (continuous spike) | Thm 6.3: Π(\|γ(β)\| > q(1+K) \| Y) → 0 under λ₀ = p^d with d ≥ 2, n/p < λ₁ ≤ 4√(n log p), p > n. Thm 6.4: rates. No selection consistency in the parts read | Different prior (complexity-type spike odds) | Complementary |
| 17 | Wang, Sarkar, Carbonetto & Stephens (SuSiE) | JRSS-B 82(5), 2020 | Variational sum of single effects | Algorithmic only: IBSS is coordinate ascent on the ELBO (Prop 1, Cor 1); convergence (Prop 2); exchangeability under duplicate columns (Prop 3). Credible sets "are not designed, or guaranteed, to have a frequentist coverage" | n/a | No statistical theory found for SuSiE (two searches, 2026-11-02). Complementary. Prop 3 is the variational analogue of our duplicate-column Prop. D |
| 18 | van der Pas, Szabó & van der Vaart | Bayesian Analysis, 2017 (abstract only) | Horseshoe, normal means | Coverage is good if the sparsity level is set correctly; HB/EB credible sets are not honest; the false-discovery fraction is controlled by the cut-off | Sequence model | Complementary |
| 19 | Hou, Wang & Atchadé | arXiv:2407.20580 (2024; INDEX says 2026, venue UNVERIFIED) | Le Cam one-step Laplace posterior; complexity prior p^{−u\|δ\|}-type; GLM | **Thm 2 (non-asymptotic): Π̌(A_j \| D) ≥ 1 − 2(p^{−u(j+1)/2} + 2e^{−c₂n/4})**, given model-selection consistency of the one-step estimators, u ≥ 2(1+c₁) and c₂n ≥ 2(u+1)log p. Polynomial mixing (Thm 4, 6) | Complexity prior (u ≥ 2), not ours. c₁ and c₂ are not computed for our designs | **Threat to any "first finite-n" claim**: explicit finite-sample posterior bounds already exist, for complexity priors and approximate posteriors. Thm N200 (API-N200) is of a different kind (exact composition, measured Π(X)) |
| 20 | Lee, Chae & Martin | arXiv:2408.04359, 2024 (abstract only) | Data-dependent prior, GLMs | Near-optimal selection consistency with weaker beta-min. Abstract: in Gaussian linear models "there are no substantial differences in the model selection consistency results available from the two schools" | n/a | Confirms the field regards Gaussian-linear selection consistency as mature. Frame T03♯ accordingly |
| 21 | Berger, García-Donato & Pericchi | arXiv:2603.19728v2, Sept 2026 | Size-only model priors; weak and strong parsimony | Lemmas 1–3 (WP/SP characterisations; SP for Beta mixtures iff ∫p^{k−1}(1−2p)π(p)dp ≥ 0). §2.6 calls Beta(1, k) (Wilson et al.) "overly parsimonious … which we would not label objective" | n/a | **Referee threat to the choice of BB(1,p)** (a decision, not a theorem). Lives in the class where T07(i) applies, but does not state T07(i) |
| 22 | Womack, Taylor-Rodríguez & Fuentes | arXiv:1511.04745v4, 2025 | Matryoshka-doll model prior | Limiting dimension law is Poisson (abstract); Props 1–2, Thm 4 (isomorphism) | n/a | Alternative size prior. Complementary |
| 23 | Banerjee, Castillo & Ghosal | Review, arXiv:2101.04491v3 (Jun 2026) | Survey | Summarises CSvdV: no supersets, beta-min ⇒ selection consistency | — | Confirms the standard template |
| 24 | Sparks, Khare & Ghosh | Bayesian Analysis 10(3), 2015 (abstract and theorem list) | g-priors with p ∼ n | Necessary and sufficient conditions for sup-norm coefficient consistency | — | Not selection. Complementary |
| 25 | Song & Liang | JRSS-B 77, 2015 — **UNVERIFIED** (second-hand via A-DRAFT §1.2) | Split and merge | Sure screening (Thm 3), misspecified-posterior consistency (Thm 4) | — | Prop M refutes a naive union, **not** Song–Liang's method (A-DRAFT's own caveat) |

(Report continues in §3 onward.)
