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
