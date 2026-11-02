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

## Web sources (arXiv PDFs downloaded with curl to /tmp/litvenue_dl, converted with pdftotext; venues via Crossref, scripts/crossref.sh)

- YWJ: Yang, Wainwright, Jordan, AoS 44(6) 2497–2532 (2016), DOI 10.1214/15-AOS1417 (venue from search result + Project Euclid
  listing; arXiv 1505.07925 read). Thm 1 (l.461): under Assumptions A, B (s = Ks*), C, D(s*), if Cβ² ≥ c0(L+L̃+α+κ)σ0² log p / n
  "then we have πn(γ*|Y) ≥ 1 − c1 p^{-1} with probability at least 1 − c2 p^{-c3}". Assumption C (l.414): "g ≍ p^{2α} for some
  α > 0, and κ + α ≥ C1(L + L̃)". Assumption D(s*) (l.429): sparsity s* ≲ n/log p with C0 > 4, truncated prior s0.
  Thm 2 (l.525): "the ε-mixing time of the Metropolis–Hastings chain (3) is upper bounded as τε ≤ c1 p s0² [c2 α (n+s0) log p
  + log(1/ε) + 2] with probability at least 1 − 4p^{-c1}". Cor 2 (l.542): after that many iterations γt = γ* w.h.p.
  l.501–506: in the intermediate SNR regime (10) "the MCMC algorithm ... can exhibit slow mixing due to multimodality"
  (example in App. A.2). §3.4 "Illustrative simulations" (l.558), s* = 10.
- GLS: Griffin, Łatuszyński, Steel, Biometrika 108(1) 53–69 (2021), DOI 10.1093/biomet/asaa055 (Crossref). arXiv 1708.05678v3
  read: Prop 1 (l.252) variance of independent/random-walk proposals; Prop 2 (l.303) approximate posterior independence
  of γj, γk via Bayes factors; §3 "Ergodicity of the algorithms" (l.517). No rate.
- RAB: Rossell, Abril, Bhattacharya, "Approximate Laplace approximations for scalable model selection", JRSS-B 83 853–879 (2021),
  DOI 10.1111/rssb.12466 (Crossref). arXiv 2012.07429: Thm 1 (l.608) under misspecification (y,z) ~ F*, ALA screening
  "discards any variable outside the true model"; Thm 2 (l.675): ALA Bayes factor rates, spurious additions
  B̃ = Op(n^{-(pγ − pγ̃*)/2}) for local priors.
- RS: Ray & Szabó, "Variational Bayes for high-dimensional linear regression with sparse priors", JASA 117 1270–1281 (2022 print,
  online 2020), DOI 10.1080/01621459.2020.1847121. arXiv 1904.07150 l.400: VB posterior contracts at minimax rates (Thm 1).
- ZC23: Zhou & Chang, "Complexity analysis of Bayesian learning of high-dimensional DAG models and their equivalence classes",
  AoS 51(3) 1058–1085 (2023), DOI 10.1214/23-AOS2280 (search + Euclid listing). arXiv 2101.04084 l.154–172: rapid mixing of
  RW-GES under high-dim assumptions; needs a "swap" move so that boundary classes of the restricted space are not local modes;
  strong selection consistency (Thm 5); consistency of greedy local search on restricted space.
- CZ26: Chang & Zhou, "Dimension-free relaxation times of informed MCMC samplers on discrete spaces", Bernoulli 32 1404–1431
  (2026), DOI 10.3150/25-BEJ1912 (Crossref; web search had found only arXiv). arXiv 2404.03867 read: R := min_{x≠x*}
  max_{x'∈N(x)} π(x')/π(x) (l.577); "If R > 1, we say π is unimodal with respect to N"; random-walk MH mixes fast if R > M
  (M = max |N(x)|), informed MH needs R > M². Thm 1 (l.672): ρ = R/M > 1 ⇒ π(x*) ≥ 1 − 1/ρ, Gap(P0^lazy)^{-1} ≤ c(ρ)M,
  τ ≤ c(ρ) M log(1/…). Thm 4 (l.1009): multimodal case — restrict to X0 with R|X0 /M > 1, warm start x0 with π(x0) ≥ η and
  π(X0) ≥ 1 − ε²η²/5 ⇒ τ_{x0} ≤ c(ρ) M log(1/(2ε²η²)).
- CLLSZ22: Chang, Lee, Luo, Sang, Zhou, "Rapidly mixing multiple-try Metropolis algorithms for model selection problems",
  NeurIPS 35 (2022) 25842–25855 (Crossref). Abstract read: MTM mixing bound smaller than MH by the number of trials.
- ARZ26: Ascolani, Roberts, Zanella, "Scalability of Metropolis-within-Gibbs schemes for high-dimensional Bayesian models",
  JRSS-B 88 1231–1250 (2026), DOI 10.1093/jrsssb/qkaf084 (Crossref). arXiv 2403.09416 Thm 1 (l.356): conductance comparison
  Pi(∂A) ≥ κi(Pi,K)(Gi(∂A) − π(A∩K^c)) between MwG and Gibbs. Continuous-parameter models; not model space.
- SBCD26: Syed et al. "Optimized annealed SMC samplers", JRSS-B (2026), DOI 10.1093/jrsssb/qkag082 (Crossref).
- JOA20: Jacob, O'Leary, Atchadé, "Unbiased MCMC methods with couplings", JRSS-B 82 543–600 (2020), DOI 10.1111/rssb.12336
  (Crossref). Prop 3.1 (l.332): H_{k:m}(X,Y) has expectation E_π[h], finite variance and finite expected computing time.
- BJV19: Biswas, Jacob, Vanetti, "Estimating convergence of Markov chains with L-lag couplings", arXiv 1905.09971 (NeurIPS 2019:
  venue UNVERIFIED). Thm 2.5 (l.134): d_TV(π_t, π) ≤ E[max(0, ⌈(τ^(L) − L − t)/L⌉)] — an upper bound estimable from coupled
  runs (a Monte Carlo estimate, not a per-run certificate).
- VGSCB21: Vehtari, Gelman, Simpson, Carpenter, Bürkner, improved R̂, Bayesian Analysis 16 667–718 (2021) (Crossref). Diagnostic.
- BKM16: Bertsimas, King, Mazumder, "Best subset selection via a modern optimization lens", AoS 44 813–852 (2016) (Crossref).
  arXiv 1507.03133 l.329: MIO gives a "certificate of suboptimality"; "heuristic methods do not provide such a certificate";
  l.1448: optimality gap evolution for n = 350, p = 64 (Diabetes). Per-run optimality certificate (frequentist L0).
- Duan 2026, "Revisiting Bayesian variable selection via optimization", arXiv 2604.21009 (abstract read): DC algorithm
  converges to the global optimum of the marginal likelihood over latent precision parameters "under mild compact set
  conditions" at a linear rate. Continuous-shrinkage mode, not the model-space HPM.
- CerT-MCMC 2026, Wu, arXiv 2605.30722 (abstract read): computable spectral-gap certificates for flow-based independence MH;
  covering certificate "rapidly weak and eventually vacuous as dimension increases"; tests D = 2–20. Continuous, low-dim.
- HWA: Hou (Wang), Atchadé, AISTATS 2026, PMLR 300:3772–3780 (search result: proceedings.mlr.press/v300/hou26a.html; author
  list differs from arXiv).
- Crossref-only (content NOT read; UNVERIFIED beyond bibliographic data): South, Pettitt, Drovandi, "SMC samplers with
  independent MCMC proposals", Bayesian Analysis 14 753–776 (2019); Barbieri, Berger, George, Ročková, "The median probability
  model and correlated variables", Bayesian Analysis 16 1085–1112 (2021) (local arXiv version read: Thm 3.1 "mini-theorems",
  q = 2 optimality of the median model).
- Also local, 0 theorems found by grep: Schäfer & Chopin (Stat. Comput. 2013; local 07), Zhou, Johansen, Aston (JCGS 25 701–726,
  2016, Crossref; local 25: unbiased Ẑ cited to Del Moral 2004 Prop 7.4.1, l.352), Titsias & Yau (JASA 112 1598–1611, 2017,
  Crossref; local 11).
- Venue of Papaspiliopoulos & Rossell (Biometrika 104, 2017): Crossref query did not return it — UNVERIFIED (from memory and the
  INDEX title only).

## Added late
- García-Donato & Martínez-Beneito, "On sampling strategies in BVS problems with large model spaces", JASA 108 340–352 (2013)
  (Crossref; local 28). §4 (l.264–276): "Given a set of visited models M*, the obvious and most precise way of estimating the
  HPM ... is τ̂ = argmax_{γ∈M*} B_γ0 Pr(M_γ). Notice that the goodness of the estimation of the HPM only depends upon the
  ability of the methods to search for good models in very large model spaces." 0 numbered theorems.
- Clyde, Ghosh, Littman, BAS, JCGS 20 80–101 (2011) (Crossref; local 27). Thm 1: sampling without replacement via updated
  ρ^(t) assigning probability one to unsampled models Γt.
