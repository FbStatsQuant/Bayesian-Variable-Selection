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
   **Correction after a later check (§12):** per model, BB(1,p) and BB(1,1) penalise each added variable at the same order (ratios
   (k+1)/(2p−1−k) vs (k+1)/(p−k)). BB(1,p) ≈ BB(1,1) × ((p+1)/2)·2^{−k}, i.e. BB(1,1) tilted by a Geometric(½) size law. So the gap is
   narrow: it is "Rossell's BB(1,1) spurious-model analysis does not reach a cap K ≍ n; the geometric size tilt of BB(1,p) plus T02(i♯)
   does". The novelty of T02(i♯) is **modest**, not a new mechanism.
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


## 3. Gaps: what nobody has proved that we prove or could prove

These are my **assessment**. "Not found" means not found in the sources in §8 plus the searches logged in `notes/`. It is not a proof
of absence.

- **G1. Concentration under BB(1,p) with a g = n slab and a cap of order n.**
  - Every concentration theorem I read uses one of three things to beat the multiplicity of large models: a complexity or exponentially
    decreasing dimension prior (CSvdV, YWJ, Hou–Atchadé, Ročková–George), a slab variance growing like p^{2+δ} (Narisetty–He; YWJ's
    g = p^{2κ₁}), or a maximum size p̄ ≪ n (Rossell; Shin et al.).
  - T03♯ uses none of these. BB(1,p) has dimension ratio ≈ ½ (PROVED, §6), g = n < p, and K = ⌊n/2⌋.
  - The device that makes this work is T02(i♯)'s exact tail. It bounds Π(|S| > m | y) by the prior tail ratio R_m times
    (n+1)^{s₀/2}√n, with a tight factor Θ♯, and so moves the SE requirement down to sizes ≤ m♯_n ≈ s₀ + O(log n). Prop. D (duplicate
    columns) shows that some log n growth of the cutoff is necessary without SE.
  - I found no published analogue of either the upper bound (exact BB(1,p) tail) or the lower bound (Prop. D) for a non-complexity BB prior.
  - **This is the defensible statistical novelty of Thm 1. It is modest.** It is narrowed further by §12: BB(1,p) is BB(1,1) times a
    Geometric(½) size tilt, so Rossell's per-model accounting carries over up to constants. What remains new is handling a cap of order n
    (Rossell's (B1) needs p̄ ≪ n) through the geometric tail and the exact cutoff m♯_n, together with Prop. D's matching lower bound.
- **G2. Guarantees for the reported HPM of a finite-budget algorithm whose start law masks the truth while the posterior concentrates.**
  - The statistics papers stop at the posterior (π, the global HPM, the MPM).
  - The computation-plus-statistics papers (YWJ, Zhou et al., Hou–Atchadé) get recovery through rapid mixing under Condition 1, from any
    start, with priors stronger than ours.
  - Nothing I read separates "posterior fine, start masked, a repair move needed", which is the content of Thm 2 masking, Thm 3 and
    Thm 5(b). API-POS's finding (Condition 1(b) holds on LH for the posterior) sharpens this: the gap is about the **start law and the
    algorithm as run**, not about the posterior.
  - T21's composition adds a "truth never scored" term to Rossell's 2E[1 − π] term. It is elementary, but I did not find it stated for
    a best-ever-scored HPM.
- **G3. Decision-theoretic bookkeeping for a capped model space.** The capped Hamming-optimal rule (T07(ii)(c)) and the within-size
  ceiling (T07(i)) are unstated but trivial. They fill a gap in presentation, not in mathematics.
- **G4. Finite-n relevance at n = 200.**
  - No asymptotic theorem in the table has force at n = 200, p ∈ {500, 1000}.
  - YWJ's (E) already fails for every s₀ ≥ 1 (§2 row 3). Rossell's (B1) fails for our cap. T03♯'s own thresholds are about 2·10⁶.
  - The only explicit finite-sample posterior bound found (Hou–Atchadé Thm 2) is for a complexity prior and an approximate posterior,
    with constants c₁ and c₂ that are not computable from the design alone.
  - Nobody has a usable finite-n selection theorem for designs like the study's. API-N200's measured-Π(X) route is a different kind of
    object (a composition plus measurement), not a competitor to any paper here.
- **G5 (not ours to fill).** No statistical consistency or coverage theory for SuSiE was found.

## 4. Threats: results that make one of ours standard, weaker or redundant

| # | Threat | Affected result | Severity | What the paper must do |
|---|---|---|---|---|
| H1 | **Rossell (2022) Prop 1**: P(HPM ≠ t) ≤ 2E(1 − p(M_t \| y)), also for the MPM | T03♯(3); the 2E₀δ₁ term of Thm 4 (T21) and Thm 5(0) | **High for novelty, none for correctness** | Cite it as Rossell's. Do not present it as ours |
| H2 | **Rossell (2022) §5 and Moreno–Girón–Casella (2015) Thm 3**: unit-information g plus a multiplicity-correcting BB model prior is consistent at polynomial p, with anchored eigenvalue quantities | Thm 1 (T03♯) as "the" consistency theorem | **Medium–High (raised in §12).** T03♯ becomes a modest extension (BB(1,p), K ≍ n, ridge slab, exact tail) | Cite both. State T03♯ as consistency **of the method's own target**, and put the novelty in the exact BB(1,p) tail and size-restricted SE (G1) |
| H3 | Narisetty–He (2014) Δ_n(K) and Rossell's v_tm: identifiability anchored at the truth and restricted in size is standard | The "anchored SE" wording in Thm 1 | Low to medium | Do not call anchoring new. W6-FIXREV2 already notes that SE_w ⇔ λ_min(G_T) ≥ g₀ for all T with \|T∖S₀\| ≤ m♯_n, which is close to Rossell's v̄ over sizes in [p_t, p̄] |
| H4 | YWJ (2016) and Zhou et al. (2022) with **their** priors cover LH (API-POS) | Any claim that polynomial-time recovery on LH is new | High for that claim | Already flagged by API-POS. Keep the claim to "for the paper's own target and start" |
| H5 | Hou–Atchadé Thm 2 (explicit non-asymptotic posterior bound) | Any "first finite-sample BVS guarantee" wording | Medium | Avoid "first finite-n". Thm N200 is a composition with a measured Π(X), which is a different kind of result |
| H6 | Johnson–Rossell (2012) Thm 2 (local priors fail for p > n^{1/2+ε} when prior ratios are bounded below) and MGC Thm 3(i) (g = n plus Bernoulli fails for b ≥ ½) | Referees may claim T03♯ contradicts them | Low (no contradiction) | One sentence: BB(1,p) violates JR's hypothesis (3), since w(s₀+1)/w(s₀) → 0. This matches MGC's positive part (ii) |
| H7 | Barbieri–Berger (2004): the HPM is generally **not** the optimal predictive model | The framing of Prop 1, "the HPM is the right decision" | Low to medium | Say "Bayes rule for 0–1 support loss (exact recovery)". Note that under predictive loss the MPM can be optimal (BB 2004) |
| H8 | Berger, García-Donato & Pericchi (2026) call Beta(1, k) "overly parsimonious … not … objective". Castillo–van der Vaart (2012) say the slab "needs to have heavy tails" | The fixed prior choices (Felipe's decisions), not any theorem | Medium as a referee point | Defend BB(1,p) via T03♯'s need for multiplicity control at p = n^A, and the Gaussian slab via hypothesis R and the unit-information scale. Disclose both |
| H9 | Papaspiliopoulos–Rossell (2017) block-diagonal exactness; omitted-variable bias of block-wise fits | Naive-merge Prop M (A-DRAFT) | Medium for novelty | Present Prop M as a motivating COUNTEREXAMPLE that quantifies a known phenomenon, citing PR2017. Do not claim it refutes Song–Liang (A-DRAFT's own caveat) |
| H10 | Barbieri–Berger (2004) Thm 1's proof (coordinate-wise thresholding at ½) | T07(ii)(b) | Low | Cite as standard |

## 5. Statements (citation-framed wording proposed for the paper)

No new mathematics. These are proposed wordings that attach the correct provenance to our existing statements.

- **Thm 1 (T03♯), clause (iii).** "P₀(S† ≠ S₀) ≤ 2E₀[1 − π(S₀)] → 0. The inequality is Rossell (2022, Prop. 1); the convergence follows
  from (i) by bounded convergence."
- **Thm 1, lead sentence.** "Under the method's own target (ridge unit-information slab, IG variance, BB(1,p) size prior capped at
  ⌊n/2⌋), … [T03♯ as of record]. Comparable results for Zellner priors with Beta-Binomial(1,1) model priors and p̄ ≪ n are in Rossell
  (2022, §5), and for g = n with k = O(n^b), b ≤ 1, in Moreno, Girón & Casella (2015). The new ingredient is the exact BB(1,p) size tail
  (T02(i♯)): BB(1,p) is not a complexity prior in the sense of Castillo et al. (2015, (2.2)), since its dimension ratio is
  (p−s+1)/(2p−s) → ½."
- **Prop 1 (T07).** "(ii)(a)–(b) are the standard Bayes rules for 0–1 and Hamming support loss (cf. the coordinate-wise argument in
  Barbieri & Berger, 2004, Thm 1). (ii)(c) adapts (b) to the capped model space. (i) records that a size-only prior, the class studied
  by Scott & Berger (2010) and Berger, García-Donato & Pericchi (2026), cannot reorder models of equal size."

## 6. Evidence

- `scripts/bb_ratios.py` → `results/bb_ratios.txt`. Exact rational arithmetic, deterministic, run via `owls_run -j 2`. It checks three
  things:
  1. w(k) = ½/C(2p−1,k) = B(k+1, 2p−k)/B(1,p), for k ≤ min(p, 60) and p ∈ {20, 500, 1000}.
  2. The dimension ratio is π_p(s)/π_p(s−1) = (p−s+1)/(2p−s), asserted exactly. The implied CSvdV exponent is A4 = −log(ratio)/log p,
     which is 0.1003–0.1080 at p = 1000 and 0.111–0.130 at p = 500 for s ≤ 100, and tends to 0 as p → ∞ for fixed s.
  3. The per-model ratio is w(s)/w(s−1) = s/(2p−s).

  **PROVED** (elementary algebra, with exact numerical confirmation): BB(1,p) satisfies CSvdV (2.2) for no fixed A4 > 0 uniformly in p,
  so CSvdV Thms 1, 4 and Cor 1 do not apply to our size prior.
- YWJ (E) at the study's sizes: n/(32 log p) = 200/(32 ln 500) = 1.006 and 200/(32 ln 1000) = 0.905. With C₀ ≥ 0 the condition forces
  s₀ ≤ 1. This is arithmetic on the condition as quoted in Zhou et al.'s Thm S2.

## 7. What fails and why (routes tried)

- **Finding a SuSiE consistency theory.** Two searches found none; only methods papers (titles seen, not read).
- **Locating a published statement of T07(i).** Searches and reading of Scott–Berger, Berger et al. (2026) and Wilson et al. found no
  explicit statement. The search-engine summary agreed that it is implied but not stated.
- **Reading YWJ (2016) directly.** Not done, for budget reasons. Its conditions are quoted from Zhou et al.'s Thm S2, so they are
  UNVERIFIED against YWJ itself. API-POS read further.
- **WebFetch summaries.** These refuse verbatim abstracts. I switched to downloading arXiv PDFs and abstract metadata with curl and
  extracting text locally (untrusted files kept in /tmp, not committed).

## 8. Sources actually read

Local PDFs were read through `pdftotext`; web PDFs were downloaded from arXiv and read the same way. "Abstract only" means the arXiv
abstract metadata from `export.arxiv.org/abs/<id>`.

| Work | Source actually read | Depth |
|---|---|---|
| CSvdV 2015 | `Papers/Priors_and_decision_rules/Castillo_SchmidtHieber_vanderVaart2015_Sparse_priors_regression.pdf` | (2.2), Ex. 4–5, Thms 1, 4, 5, Cor 1 |
| Castillo–vdV 2012 | `Papers/Priors_and_decision_rules/Castillo_vanderVaart2012_Needles_and_straw.pdf` | Ex. 2.2, the text after Thm 2.8 |
| Zhou et al. 2022 (and YWJ 2016 second-hand) | `Papers/Core_bibliography/10_2022_Zhou_et_al_...pdf` | §2, Condition 1, Supplement S3 Thm S2 |
| Johnson–Rossell 2012 | `Papers/Core_bibliography/17_2012_Johnson_Rossell_...pdf` | Thms 1–2, Cors 1–2 |
| Shin–Bhattacharya–Johnson 2018 | `Papers/Core_bibliography/18_2018_Shin_...pdf` | Assumptions 1–5, Thms 1, 3 |
| Rossell 2022 | https://arxiv.org/pdf/1806.04071 | Prop 1, Cors 1–2, §2.3 conditions, §5.2, §5.4 (Prop 9, Lemma 3) |
| Narisetty–He 2014 | https://arxiv.org/pdf/1405.6545 | §4.1 Conditions 4.1–4.5, Lemma 4.1 (extraction partly garbled) |
| Moreno–Girón–Casella 2015 | https://arxiv.org/pdf/1507.08041 | Abstract, Thm 3 |
| Sparks–Khare–Ghosh 2015 | https://arxiv.org/pdf/1509.01060 | Abstract, theorem list |
| Banerjee–Castillo–Ghosal review | https://arxiv.org/pdf/2101.04491 (v3) | Linear-regression section |
| Liang et al. 2008 | `Papers/Core_bibliography/15_2008_Liang_et_al_...pdf` | §4.2 (garbled) |
| Scott–Berger 2010 | `Papers/Core_bibliography/04_2010_Scott_Berger_...pdf` | §3 passages |
| Wilson et al. 2010 | `Papers/Priors_and_decision_rules/Wilson_etal2010_MISA_BetaBinomial_1_p.pdf` | Eq. (2.7), §2.4.1 |
| Barbieri–Berger 2004 | `Papers/Priors_and_decision_rules/Barbieri_Berger_2004_Optimal_predictive_model_selection.pdf` | Introduction, Thm 1 and proof, Cors 1–2 |
| Barbieri et al. 2021 | `Papers/Core_bibliography/22_2021_Barbieri_et_al_...pdf` (arXiv v2) | Thm 3.1, dilution and replicates passages |
| Papaspiliopoulos–Rossell 2017 | `Papers/Core_bibliography/12_2017_Papaspiliopoulos_Rossell_...pdf` | Abstract, §4 heuristic |
| Ma 2015 | `Papers/Core_bibliography/13_2015_Ma_...pdf` | Abstract |
| Ročková–George 2018 | `Papers/Benchmark_methods/Rockova_George_2018_SSL.pdf` | Lemma 3.3 remark, Thms 6.3–6.4 |
| SuSiE (Wang et al. 2020) | `Papers/Core_bibliography/29_2020_Wang_et_al_...pdf` | Props 1–3, Cor 1, credible-set remark |
| Hou–Wang–Atchadé | `Papers/Core_bibliography/31_2026_Hou_Atchade_...pdf` (arXiv:2407.20580v1) | Abstract, Thm 2 |
| Berger–García-Donato–Pericchi 2026 | `Papers/Priors_and_decision_rules/Berger_GarciaDonato_Pericchi2026_Model_prior_probabilities.pdf` | Abstract, §2.6, WP/SP, Lemma 3 |
| Womack et al. 2025 | `Papers/Priors_and_decision_rules/Womack_TaylorRodriguez_Fuentes2025_Matryoshka_doll_prior.pdf` | Abstract, statement list |
| Li–Tokdar–Xu 2025; Kowal 2022 | local PDFs | Abstracts only (decision-theoretic estimation and subset selection for prediction; not support-loss results) |
| van der Pas–Szabó–vdV 2017 | https://export.arxiv.org/abs/1607.01892 | Abstract only |
| Lee–Chae–Martin 2024 | https://export.arxiv.org/abs/2408.04359 | Abstract only |
| Yang–Pati | https://export.arxiv.org/abs/1701.00311 | Abstract only |

Second-hand only (UNVERIFIED):
- YWJ 2016, via Zhou et al.;
- Song–Liang 2015, via A-DRAFT;
- Fernández–Ley–Steel 2001, via Liang et al.;
- the venues of Zhou et al. 2022, Barbieri et al. 2021 and Papaspiliopoulos–Rossell 2017;
- SuSiE 2.0 and the residual-variance preprint (search-result titles only).

## 9. Needs escalation

- **E1. Confirm G1 independently.** Is there really no published dimension or size-tail bound for a non-complexity BB(1, p^u) prior
  with u ≤ 1 combined with a unit-information slab? Candidates to check: the Rossell (2022) supplement (Lemmas S15–S16, Section S3),
  Castillo–vdV 2012 §2 (lower bounds), and Martin, Mess & Walker (2017), whom Rossell cites on p̄ ≤ n. I did not read these.
- **E2. Check YWJ (2016) directly.** My statement that YWJ's (E) fails at n = 200 for any s₀ ≥ 1 relies on Zhou et al.'s transcription
  of the condition.

## 10. Outside scope

- Barbieri et al. (2021) and Berger et al. (2026) both discuss **dilution** of model priors under correlated or near-duplicate
  predictors. That is the name, and arguably the mechanism, of the study's masking (W8-SYNTH "dilution"). Their discussion concerns prior
  probabilities, whereas ours concerns the σ²-dilution of the start law. The overlap in vocabulary should be handled in the paper to avoid
  confusion. I did not pursue it.

## 11. Confidence card

The column headings are:
- **True?** Confidence that the statement is true.
- **New?** My assessment of its novelty against the literature.
- **Provable at reasonable cost?** Whether it is already proved, or could be proved cheaply.
- **Method change?** Whether the method would have to change.

| Target | Refined statement | True? | New? | Provable at reasonable cost? | Crux | Method change? |
|---|---|---|---|---|---|---|
| Thm 1 (T03♯) | As of record (W6-FIXREV2 §1.2), with clause (iii) credited to Rossell (2022) Prop 1 | High (PROVED, XF-verified) | **Modest extension** of Rossell (2022) and MGC (2015). Not standard for BB(1,p) / g = n / K ≍ n | Already proved | Exact BB(1,p) tail plus SE only up to m♯_n | No |
| T02(i♯) exact BB(1,p) tail | As of record | High | **Modest extension** (G1 as narrowed in §12): new only in reaching a cap K ≍ n via the geometric size tilt. Low-to-medium confidence in the novelty, pending E1 | Already proved | Prior tail ratio R_m against the S₀ Occam factor (n+1)^{s₀/2}√n | No |
| Prop 1 (T07) | As of record, with (ii)(a)–(b) labelled standard | High (locked, Lean) | **Standard or folklore.** (i) and (ii)(c) are unstated but trivial | Already proved | — | No |
| T03♯(3) / the 2E₀δ₁ term | Rossell (2022) Prop 1 | High | **Known** | — | — | No |
| Naive merge (A-DRAFT Prop M) | As in A-DRAFT §3.1 | High (complete proof per A-DRAFT; A-REV4 uses it) | **Known phenomenon** (omitted-variable bias; PR2017's block-diagonal exactness condition), cleanly formalised | Already proved | Cross-block correlation ρ ≠ 0 | No |
| Masked-regime reported-HPM results (Thms 2, 3, 5(b)) | Not re-stated here | — | **No prior art found** (G2). Strongest novelty claim relative to this literature | — | Start law vs posterior (API-POS) | — |

## 12. Addendum: BB(1,p) versus Rossell's BB(1,1) (checked after the first draft)

`scripts/bb11_vs_bb1p.py` → `results/bb11_vs_bb1p.txt` (exact rationals, deterministic, run via `owls_run -j 2`). It shows:

- The per-model ratios are w(k+1)/w(k) = (k+1)/(p−k) for BB(1,1) and (k+1)/(2p−1−k) for BB(1,p), both asserted exactly. They agree to
  within a factor of about 2.
- w_{BB(1,p)}(k)/w_{BB(1,1)}(k) = (p+1)C(p,k)/(2C(2p−1,k)). This equals ((p+1)/2)·2^{−k}·(1 + o(1)) for k ≪ √p. The bracketed
  correction is 1.000 at k = 0 and 0.96 at k = 14 (p = 1000), and only 0.0045 at k = 100 (p = 500), where BB(1,p) is even lighter.

**PROVED** (elementary): BB(1,p) is BB(1,1) multiplied by a size-only factor that is at most ((p+1)/2)·2^{−k}. The inequality
C(p,k)/C(2p−1,k) ≤ 2^{−k} holds because (p−i)/(2p−1−i) ≤ ½ for every i ≥ 0.

Consequences for this audit:
- **Spurious models.** Rossell's (2022) §5.2 accounting of spurious models (per-model prior ratio times a Bayes-factor bound) transfers to
  BB(1,p) up to the constant (p+1)/2 at the denominator S₀ and an extra 2^{−(k−s₀)} that only helps.
- **Cap.** His requirement p̄ ≪ n comes from summing a flat size law up to p̄. The geometric tilt is exactly what lets T02(i♯) live with
  K = ⌊n/2⌋.
- **Revised verdicts.** T03♯ is a **modest extension of Rossell (2022)** to a geometric-size-tilted BB prior, a cap of order n and a
  ridge slab, rather than a different mechanism. H2's severity rises from Medium to **Medium–High**. G1 narrows to the cap and the exact
  cutoff, with Prop. D's lower bound.
- **E1 updated.** Rossell's supplement (Lemma S15, Lemma S21, read in the same arXiv PDF) treats BB(1,1), uniform and Complexity
  priors only. It has no BB(1,p) and no cap of order n. A stronger reviewer should still check Martin, Mess & Walker (2017), which I did
  not read.
