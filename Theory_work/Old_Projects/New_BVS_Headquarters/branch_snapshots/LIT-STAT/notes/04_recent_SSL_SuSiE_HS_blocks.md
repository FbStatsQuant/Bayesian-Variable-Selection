# Notes 04: SSL, SuSiE, horseshoe, 2023–2026 work, block/merge methods

## Ročková & George (2018) "The Spike-and-Slab LASSO", JASA 113(521) 431–444. READ: Papers/Benchmark_methods/Rockova_George_2018_SSL.pdf
- Thm 6.3, quoted: "Assume λ0 = (1 − θ)/θ = p^d, where d ≥ 2, and n/p < λ1 ≤ 4√(n log p). Assume p > n and n, p → ∞. Then
  sup_{β0} E_{β0} P(β : |γ(β)| > q(1 + K) | Y, θ) → 0", K = (M/(d−1))(1 + 2λ1/(φ̃(S0)²√n log p)). Thm 6.4: prediction/ℓ1/ℓ2 rates.
- Fixed θ with spike/slab odds p^d, d ≥ 2 (complexity-type); dimension and rate results only, NO selection-consistency theorem in the
  sections read; continuous spike (no exact zeros, no HPM over supports). Lemma 3.3 recommends θ ~ B(1, Dp) for calibration.
- Bearing: no overlap with T03♯ beyond the generic "dimension bound" architecture. Complementary.

## SuSiE: Wang, Sarkar, Carbonetto & Stephens (2020), JRSS-B 82(5) 1273–1300. READ: Core_bibliography/29_...pdf
- Results proved are algorithmic: Prop 1/Cor 1 (IBSS is coordinate ascent on the ELBO), Prop 2 (convergence of the IBSS sequence under
  0 < σ, σ0 < ∞, π_j > 0), Prop 3 (identical columns x_j = x_k with π_j = π_k ⇒ IBSS approximate posterior exchangeable in j, k).
  Quoted: credible sets "are not designed, or guaranteed, to have a frequentist coverage of 0.95".
- Two targeted searches (2026-11-02) found NO posterior-consistency/contraction or coverage theorem for SuSiE (2020–2025); later
  work found is methodological (SuSiE 2.0, bioRxiv 2025.11.25.690514; residual-variance calibration, bioRxiv 2025.05.16.654543 — titles
  seen in search results only, NOT read). Status: absence after search, not proof of absence.
- Bearing: SuSiE is a different target (variational, L single effects); nothing in it threatens T03♯/T07. Prop 3 (exchangeability under
  duplicate columns) is the variational analogue of the non-identifiability behind our Prop. D (duplicate-column counterexample).

## Horseshoe: van der Pas, Szabó & van der Vaart (2017) "Uncertainty quantification for the horseshoe", Bayesian Analysis
## (doi 10.1214/17-BA1065 per search result; arXiv:1607.01892). READ: arXiv abstract only (export.arxiv.org/abs/1607.01892).
- Abstract, quoted: "credible balls and marginal credible intervals have good frequentist coverage and optimal size if the sparsity level
  of the prior is set correctly ... the hierarchical and empirical Bayes credible sets based on the horseshoe prior are not honest over the
  full parameter space ... the fraction of false discoveries by the marginal Bayesian procedure is controlled by a correct choice of cut-off."
- Sequence (normal means) model; continuous shrinkage; selection by interval/threshold. No HPM. Complementary only.

## Hou, Wang & Atchadé, "Laplace approximation for Bayesian variable selection via Le Cam's one-step procedure" (arXiv:2407.20580v1,
## 2024; INDEX lists 2026, venue UNVERIFIED). READ: Core_bibliography/31_...pdf
- Prior on δ ∝ p^{−u|δ|}-type complexity prior (u "sparsity parameter"), Gaussian slab; GLMs. Thm 2, quoted: "Suppose that the family of
  one-step estimators ... is model selection consistent with constants c1, c2 ... u ≥ 2(1 + c1), and ... c2 n ≥ 2(u + 1) log(p). Then for all
  j ≥ 0, Π̌(A_j | D) ≥ 1 − 2(1/p^{u(j+1)/2} + 2/e^{c2 n/4})." Plus polynomial mixing of a Gibbs sampler (Thm 4, Thm 6).
- A NON-ASYMPTOTIC posterior bound (explicit in n, p) for an approximate posterior, with complexity prior. Threat to the "finite-n" angle:
  explicit finite-sample statements exist in the literature (for complexity priors); ours (T03♯) is asymptotic with thresholds ≈ 2·10⁶.

## Lee, Chae & Martin, "Advances in Bayesian model selection consistency for high-dimensional GLMs" (arXiv:2408.04359, 2024; no journal
## ref on arXiv page). READ: arXiv abstract only. Quoted: "In the context of Gaussian linear models, both the Bayesian and non-Bayesian
## literature is well-developed and there are no substantial differences in the model selection consistency results available from the two
## schools." Data-dependent prior; "far weaker beta-min conditions". → Confirms that Gaussian-linear selection consistency is regarded as
## mature: T03♯ cannot be sold as a new phenomenon.

## Yang & Pati, "Bayesian model selection consistency and oracle inequality with intractable marginal likelihood" (arXiv:1701.00311).
## READ: abstract only. Prior anti-concentration condition ⇒ selects smallest model containing truth. Rossell (2022) summarises it as setting
## τ growing with n. Complementary.

## Papaspiliopoulos & Rossell (2017), Biometrika 104(2) 343–359 (venue from memory, UNVERIFIED; READ arXiv:1606.03749v2 local PDF).
- Abstract, quoted: "exact Bayesian variable selection and model averaging in linear models under the assumption that the Gram matrix is
  block-diagonal, and as a heuristic for exploring the model space for general designs. In block-diagonal designs our approach returns
  the most probable model of any given size". For general designs: "we approximate the Gram matrix by a block-diagonal using spectral
  clustering and propose an iterative algorithm" — §4: "a forward-backward heuristic".
- Bearing on naive-merge (A-DRAFT Prop M): block-local analysis is EXACT iff the cross-block Gram vanishes; with cross-block correlation it is
  a heuristic. Prop M is the explicit p = 2 quantification of this gap (cross-block proxy ⇒ product of block posteriors includes the proxy
  w.p. → 1 while the full posterior excludes it). The phenomenon is omitted-variable bias of marginal/block-wise fits (the reason screening
  methods over-include); Prop M is a clean formalisation, not a new phenomenon.
## Song & Liang (2015), JRSS-B 77 947–972 — SECOND-HAND via A-DRAFT REPORT §1.2 (A-DRAFT read the publisher text): split-and-merge
## with a second selection stage; Theorem 3 sure screening, Theorem 4 misspecified-posterior consistency. Prop M does NOT refute it.

## Ma (2015) "Scalable Bayesian model averaging through local information propagation", JASA (arXiv:1403.2397). READ: abstract
## (local PDF). Computational (forward-stepwise data augmentation); no selection theorem in scope.
