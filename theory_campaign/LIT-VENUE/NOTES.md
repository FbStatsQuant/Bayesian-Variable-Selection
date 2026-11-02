# LIT-VENUE working notes (source log)

Every entry: file/URL actually read, line numbers in the pdftotext dump, verbatim key statement.
Local PDFs: Papers/Core_bibliography/NN_*.pdf, converted with `pdftotext -layout` (scripts/extract.sh).

## Local PDFs read (theorem statements quoted from the text dump)

- [10] Zhou, Yang, Vats, Roberts, Rosenthal, "Dimension-free mixing for high-dimensional BVS", JRSS-B 84(5) 2022 (arXiv 2105.05719).
  Thm 1 (l.638-650): LIT-MH, "Suppose that n = O(p), s0 log p = O(n) and κ = O(s0). If Condition 1 holds for c0 = 2 and
  4 ≤ c1 ≤ nκ1 − κ, then, for sufficiently large n, Tmix ≤ 800 max{nκ1/c1, 3s0}" (Tmix = sup over γ∈M(s0) of TV-1/4 time).
  Condition 1 (l.353-363): (1a) overfitted γ: B(γ,γ∪{j}) ≤ p^{-c0}; (1b) underfitted γ: ∃ j∈γ*\γ with B(γ,γ∪{j}) ≥ p^{c1};
  (1c) underfitted |γ|=s0: a swap with B ≥ p^{c1}. Thm 2 (l.708): general drift-condition mixing bound. Thm S2 restates YWJ 2016.
  Evidence: simulations + one real data set with p = 328,129 (l.453).
- [09] Zanella, "Informed proposals for local MCMC in discrete spaces", JASA 115 (2020) (arXiv 1711.07424).
  Thm 1 (l.222): pointwise informed proposal locally balanced iff g(t) = t g(1/t). Thm 2 (l.266): Peskun-type comparison
  P1 ≥ cP2 ⇒ Gap(P1) ≥ c Gap(P2). Thm 3 (l.286), Thm 4 (l.519): weak limit as n→∞. No BVS-specific consistency/mixing bound.
- [14] Zanella & Roberts, "Scalable importance tempering and BVS", JRSS-B 81 (2019) (arXiv 1805.00541).
  Thm 1 (l.393): var(h,TGS) ≤ b² var(h,GS) + b² var_f(h). Thm 2 (l.975): under independence (16), t_GS = α1 p, t_TGS = α2 p,
  t_wTGS = s(1−q_min). Thm 3 (l.1038): "As p → ∞, ... tGS ≥ O(c^{1/2} h^{-1} p), tTGS ≥ O(p), twTGS = O(s)" (two-variable/
  collinear stylised model). Conjecture t_TGS ≤ O(p) (l.1044).
- [01] Liang, Livingstone, Griffin, ARNI/PARNI, Statistics and Computing 32 (2022) (arXiv 2110.11747).
  Thm 2 (l.1006): "Ergodicity and SLLN ... hold for both the PARNI-KW and PARNI-RM samplers". No rate.
- [08] Staerk, Kateri, Ntzoufras, MAdaSub (arXiv 2105.01039; published Bayesian Analysis 2024 — venue UNVERIFIED here).
  Thm 1 (l.500): "MAdaSub ... is ergodic for all choices of r(0) ∈ (0,1)^p, Lj > 0 and ε ∈ (0,0.5) and fulfils the weak law of
  large numbers" (via Roberts–Rosenthal 2007 simultaneous uniform ergodicity + diminishing adaptation). No rate.
- [18] Shin, Bhattacharya, Johnson, S5 with nonlocal priors, Statistica Sinica 28 (2018) — venue UNVERIFIED (file header arXiv v4).
  Thm 1 (l.729): σ² known, Assumptions 1–5, uniform prior on |k| ≤ q_n: "π(t | y) converges to one in probability as n → ∞";
  Thm 3 same with unknown σ². No theorem about the S5 algorithm.
- [23] Dau & Chopin, "Waste-free SMC", JRSS-B 84 (2022) (arXiv 2011.02328). Thm 1 (l.484), Thm 2 (l.525): CLTs for
  waste-free SMC with M = O(P^α) under Assumptions (M),(G). Asymptotic in N.
- [24] Le Fay, Chopin, Vihola, "On the complexity of standard and waste-free SMC samplers" (arXiv 2604.03352v2, 2026; venue
  not stated). Abstract (l.7-14): "finite sample bounds for the error of standard and waste-free SMC samplers". Thm 2.3
  (l.368): (M,P) sample sizes under A2.1 (Kt leaves π_{t−1} invariant) + A2.2 (1+χ²(πt|πt−1) ≤ χ̄²) via mixing times τ.
  Thm 3.4 (l.501): under spectral gap γ (A2.4) and χ̄² = 2 (A3.1), waste-free SMC with P ≥ 2560T/(γε²) returns Ẑ_T with
  |Ẑ_T/Z_T − 1| < ε w.p. ≥ 3/4. Thm 3.6: median-of-means boost.
- [02] Syed, Bouchard-Côté, Chern, Doucet, "Optimised annealed SMC samplers" (arXiv 2408.12057v2, Dec 2025; venue UNVERIFIED).
  Thm 1 (l.468): variance of Ẑ in terms of accumulated discrepancy D(B_T); Thm 2 (l.628): smoothness of D. Schedule design.
- [12] Papaspiliopoulos & Rossell, "Bayesian block-diagonal variable selection and model averaging", Biometrika 104 (2017)
  (arXiv 1606.03749). Prop 3.2 (l.338), 3.3 (l.373), 3.4 (l.420): under block-diagonal X'X and Zellner prior, the top
  model of each size is given in closed form by ordering scores; "Coolblock outputs a series of models M, each of which has
  largest p(γ | y, ω) amongst all models of its size" (l.481). An exact (certified) HPM-by-size, but only for orthogonal blocks.
- [29] Wang, Sarkar, Carbonetto, Stephens, SuSiE, JRSS-B 82 (2020). Cor 1 (l.487): IBSS is coordinate ascent for the ELBO;
  Prop 2 (l.493): converges to a stationary point of F; Prop 3 (l.517): exchangeability for identical columns. No
  consistency theorem; credible sets judged by simulation coverage.
- [31] Hou, Wang, Atchadé, "Laplace approximation for BVS via Le Cam's one-step procedure" (arXiv 2407.20580v1; venue
  UNVERIFIED). Thm 2 (l.319-336): posterior concentration of the one-step Laplace posterior when c2 n ≥ 2(u+1) log p.
  Thm 4 (l.389-405): MH chain from δ(0) with warm-start condition Π̌(δ(0)|D) ≥ p^{-α}: if N ≥ C(s⋆ + (4α/u) log(1/ζ0) +
  α log p) p then ‖P(δ(N)=·|δ(0)) − Π̌‖_tv ≤ max(ζ0, 4/p^{4u}). Mixing guarantee conditional on a warm start.
