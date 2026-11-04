# LIT-SMC working notes (primary-source quotes)

## [SYED] Syed, Bouchard-Côté, Chern, Doucet. Optimised Annealed SMC Samplers. arXiv:2408.12057v2 (2 Dec 2025).
Read: local PDF Papers/Core_bibliography/02_2026_Syed_et_al_Optimized_annealed_sequential_Monte_Carlo_samplers.pdf
- Performance model: Assumptions 1-4 (integrability; temporal independence; particle independence; "efficient local
  exploration" (X_{t-1},X_t^-) ~ π_{β_{t-1}} ⊗ M). Authors: "not expected to hold exactly in practice".
- D(β,β′) = Rényi-2 divergence of incremental weights. Thm 1(a): Var[Ẑ/Z] = Π_r (1 + (exp(D(B_T,τ_{r-1},τ_r)) − 1)/N) − 1.
- Thm 3: lim_{T→∞} T Var[Ẑ/Z] = E(φ)/N ≥ Λ²/N, Λ = ∫_0^1 λ(β)dβ global barrier; equality iff schedule φ*.
- §(after Prop 5): MCMC kernels + linear (geometric) path: δ(β) = Var_β[V], so λ(β) = sd_{π_β}(V).
=> O-STAGES item 4 (√c·T*(c) → L = ∫ sd_{q_φ}(d)dφ) is the same object as Λ; the dense-limit statement is essentially
   known (Syed et al. 2022 PT; Syed et al. 2024/25 ASMC). O-STAGES Lemma 0 Φ = D₂ = Rényi-2 is also their D under
   perfect mixing. THREAT to novelty of O-STAGES item 4; Theorem G greedy optimality is NOT in SYED (they optimise a
   dense-limit surrogate, not exact finite ESS-threshold grids).

## [LFCV] Le Fay, Chopin, Vihola. On the complexity of standard and waste-free SMC samplers. arXiv:2604.03352v2 (Apr 2026).
Read: local PDF 24_2026_Le_Fay_Chopin_Vihola_...pdf
- Recalls Marion–Mathews–Schmidler (2023, 2025): Assumption 2.1 K_t leaves π_{t-1} invariant; 2.2 1+χ²(π_t|π_{t-1}) ≤ χ̄².
- Thm 2.3 (generalising MMS 2023 Th 3.1 / MMS 2025 Th 1): if M ≥ log(8Tη^{-2})·max(18χ̄², ε^{-2}/2) and
  P ≥ τ(η/(2MT), 2) [TV mixing time], then Pr(|π̂_{T-1}(f) − π_{T-1}(f)| < ε) ≥ 1 − η for |f| ≤ 1.
- Assumption 2.4 spectral gap; Thm 3.2 waste-free analogue; §5 tempering with log-concave targets (Thm 5.2).
=> Premises are (i) bounded successive χ² (our ESS ≥ 0.9 rule gives 1+χ² ≤ 10/9 on the *candidate set V*, i.e. a
   COVER-type statement) and (ii) mixing times of the move kernels. (ii) is exactly what fails/is unknown in the masked
   regime; on LH masking is a property of the start (API-POS) so rapid-mixing results might feed (ii).

## [SVV] Štefankovič, Vempala, Vigoda. Adaptive simulated annealing: a near-optimal connection between sampling and
counting. arXiv:cs/0612058 (Dec 2006); J. ACM 56(3) 2009 (journal version not read). Read: https://arxiv.org/pdf/cs/0612058
- Def 2.3: schedule is **B-Chebyshev** if Z(2β_{i+1} − β_i)Z(β_i)/Z(β_{i+1})² ≤ B for all i.
  ==> identical to O-STAGES' step rule ρ(u,v)^{-1} = exp Φ(u,v) = Z_u Z_{2v−u}/Z_v² ≤ 10/9, i.e. B = 10/9 (w = 2v − u is
  their 2β_{i+1} − β_i). O-STAGES Lemma 0 (reference-state identity) is a one-line consequence of log-affinity.
- Cor 2.4: with a B-Chebyshev schedule of length ℓ, 16Bℓ²/ε² samples give (1±ε)Z w.p. ≥ 3/4 (product estimator, PERFECT
  independent samples at each temperature).
- Thm 4.1: for a partition function of degree n with A = Z(0), Z(∞) ≥ 1, there is an e²-Chebyshev schedule of length
  ≤ 4√(ln A)·ln n·ln ln A (sic: "at most √(4(ln ln A)(ln A) ln n)" in the text layout, read with care).
- Lemma 4.2: f = ln Z convex. Text after Thm 4.1 proof (p.~13): "The optimal Chebyshev cooling schedule can be obtained in a
  greedy manner ... starting with β0 = 0, and then from βi, choosing the maximum βi+1 for which (26) is satisfied. The
  reason why the greedy strategy works is that if we can step from β to β′, then for any γ ∈ [β, β′] we can step from γ to
  β′ ... follows from the convexity of f."
  ==> **O-STAGES Theorem G(i) (greedy grid is shortest valid grid) and Lemma 1(b),(c) are already stated, with the same
  convexity argument, in SVV.** THREAT: Theorem G(i) is not new. G(ii) (target-constrained refinement of pilot points,
  max(T*_V,T_P) ≤ T_grid ≤ T*_V+T_P) and the COVER transfer G(iii) are specific to v3 and are routine extensions.
- Lemma 4.7: Z(β) = (1+e^{−β})^n needs ≥ √(n/(20 ln B)) steps (adaptive lower bound). Section 3: non-adaptive schedules
  need Ω(ln A) in the worst case.
  ==> O-STAGES Theorem M (two-state masked crossing T* = log₂A₀ + O(1) with fixed B = 10/9) is a different, sharper,
  instance-specific count; its *form* (log of depth for a two-level partition function) is not stated in SVV as read.
  The halving mechanism is the B-Chebyshev condition applied to a two-atom f. Treat Theorem M as plausibly new as a
  statement but elementary given SVV's framework.

## [SC13] Schäfer & Chopin (2013) Stat Comput 23:163–184, "SMC on large binary sampling spaces". Local PDF 07_...
- Adaptive geometric bridge; §4.3: "We pick a step length α such that the effective sample size η(α) equals a fixed value η*
  ... Since η is continuous and monotonously increasing in α, we solve η(α,X)=η* using bi-sectional search"; experiments
  use η = 0.9 and n = 1.5×10⁴ particles; applied to BVS. No theorem on consistency, stage count, HPM, or discovery.
  ==> v3's ESS-0.9 bisection grid is Schäfer–Chopin's rule (on a candidate set). Monotonicity is asserted there, not proved.

## [DMDJ06] Del Moral, Doucet, Jasra (2006) JRSSB 68:411–436. Local PDF Papers/SMC/...
- ESS (Liu–Chen) resampling rule; Prop 1 optimal backward kernels; Prop 2 CLT under integrability conditions of Chopin
  (2004)/Del Moral (2004) for no-resampling and resample-every-step. Unbiasedness of Ẑ is classical (Del Moral 2004,
  Feynman–Kac book; UNVERIFIED here, not read).
