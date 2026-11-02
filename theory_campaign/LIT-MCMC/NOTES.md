# LIT-MCMC working notes (source log)

Every entry: what I actually read (file/URL), verbatim key statement, conditions. Text extracted with pdftotext
from arXiv PDFs downloaded to /tmp (not committed) or from `Papers/Core_bibliography/` (local copies).
"UNVERIFIED" = seen only second-hand (search snippet / citing paper).

## N1. Yang, Wainwright, Jordan (2016), AoS 44(6):2497–2532 — arXiv:1505.07925v1 (read: abstract, §3.2–3.3, App. A.2)
- Thm 2 (verbatim, v1): "Suppose that Assumption A, Assumption B with s = s0, Assumption C, and Assumption D(s0) all hold.
  Then under either the high SNR condition (9a) or the low SNR condition (9b), there are universal constants c1, c2 such that,
  for any ε ∈ (0, 1), the ε-mixing time of the Metropolis-Hastings chain (3) is upper bounded as
  τε ≤ c1 p s0² [c2 α (n + s0) log p + log(1/ε) + 2] with probability at least 1 − 4p^{−c1}."
- Cor 2: after t ≥ c1 p s0²[c2 α(n+s0) log p + log p + 2] iterations, γ_t = γ* w.p. ≥ 1 − c2 p^{−c3}.
- After Cor 2 (verbatim): "Theorem 2 does not characterize the intermediate regime ... we suspect that the Markov chain
  might be slowly mixing in this regime, but we do not have a proof of this statement."
- App. A.2 "Example of slow mixing" (PROVED in paper): p = n, g = p^{2α}, α > 1, Y = w ~ N(0, I_n) (null truth), UNTRUNCATED
  prior Cp^{−κ|γ|} on {0,1}^p: the MH chain (3) has mixing time exponential in n w.p. ≥ 1/2, by a conductance bound with
  B = {full model} (the saturated model, R² = 1, is a trap). Verbatim: "although a size constraint |γ| ≤ s0 ... is not
  needed for Bayesian model selection consistency, it is necessary for MCMC to mix rapidly."
- Detailed hypothesis-by-hypothesis check on LH: see API-POS REPORT §4.1 (not redone here).

## N2. Chang & Zhou, "Dimension-free relaxation times of informed MCMC samplers on discrete spaces",
## arXiv:2404.03867v2 (28 Jul 2025), "Accepted by Bernoulli" (arXiv listing). Read: §3.1–3.3, §5, Thms 1, 4, 5, Cor 5.
- Definitions: M = max_x |N(x)|; R = min_{x≠x*} max_{y∈N(x)} π(y)/π(x). "If R > 1, we say π is unimodal w.r.t. N."
- Thm 1 (random-walk MH, verbatim): "Assume ρ = R/M > 1. Then, we have π(x*) ≥ 1 − ρ^{−1}, Gap(P0^lazy)^{−1} ≤ c(ρ)M and
  τ(P0^lazy, ε) ≤ c(ρ) M log(1/(ε π_min))."
- Thm 2/3 (informed MH): needs R > M²; relaxation time then free of M ("dimension-free").
- Thm 4 (multimodal / restricted, verbatim): "Let X0 ⊂ X, x0 ∈ X0, η ∈ (0,1) be such that (i) ρ = R|X0 /M > 1,
  (ii) π(x0) ≥ η, and (iii) π(X0) ≥ 1 − ε²η²/5. We have τ_{x0}(P0^lazy, ε) ≤ c(ρ) M log(1/(2ε²η²))."
  So the start enters only through log(1/π(x0)).
- Cor 5: RW-MH on unrestricted add-delete-swap space under YWJ-type (A1)–(A5), start δ0 ∈ V_s with
  π_n(δ0) ≥ 5ε^{−1}p^{−κs/4}: τ_{δ0} = O_p(p² κ s log p).
- Text: "In order to achieve rapid mixing, such unimodal conditions are arguably necessary, since for general multimodal
  targets, the chain can get trapped at some local mode for an arbitrarily large amount of time."
- Text: Example 3 (p = 3, X1'X2 = −0.8n): "π can be unimodal but decrease when we move towards the true model δ* by flipping a
  coordinate different from δ*" — a suppressor-type example, same mechanism as LH linked pairs.

## N3. Mathews & Schmidler, "Finite sample complexity of SMC estimators on multimodal target distributions",
## AAP 34(1):1199–1223 (2024) (venue from search snippet + Le Fay et al. ref list; UNVERIFIED pages). Read arXiv:2208.06672v1: abstract, §2, Thm 1, §6 (comparison with tempering).
- Abstract (verbatim): "We prove finite sample complexities for sequential Monte Carlo (SMC) algorithms which require only local
  mixing times of the associated Markov kernels. ... in such cases our approach establishes benefits of SMC over the
  corresponding Markov chain Monte Carlo (MCMC) estimator. ... SMC provides a fully polynomial time randomized approximation
  scheme for some difficult multimodal problems where the corresponding Markov chain sampler is exponentially slow."
- Setting: partition A = {A_j} of X (typically modes); µ⋆ := min_v min_j µ_v(A_j) = smallest mass of any partition element
  along the WHOLE bridge; W, Z bound incremental weights / normalising-constant ratios.
- Thm 1: with N > ε^{-2}·max{3456 V W Z²/µ⋆ · log(64Vp/µ⋆), ...} particles and t > max_{v,j} τ_{v,j}(ε²/(16NV), 7) local
  (restricted-to-A_j) mixing steps, |N^{-1}Σ f(X_V^i) − E_π f| ≤ ε with prob ≥ 3/4. (Constants transcribed from pdftotext;
  check against PDF before quoting numerically.)
- Applications are continuous (mixtures of log-concave densities with equal scales in a location-scale family). No binary/BVS example.
- §6: compares with Woodard–Schmidler–Huber persistence/overlap: "dependence of N on γ(A) is quadratic ... rather than exponential in |A|".
- READING FOR US: the particle cost scales like 1/µ⋆. In the masked regime the S₀ basin has start mass π₀(S₀) ≍ n^{-c/2}
  (chain-masking law, Thm 2), so µ⋆ ≲ n^{-c/2} and this theorem would demand N ≳ n^{c/2} particles — it does NOT by itself
  certify a fixed-N SMC in the masked regime. Our masked results get around µ⋆ by MCMC moves that leave the start mode,
  which is a global-mixing (not local-mixing) mechanism.

## N4. Woodard, Schmidler, Huber (2009b), "Sufficient conditions for torpid mixing of parallel and simulated tempering",
## EJP 14:780–804, doi:10.1214/EJP.v14-638. Read: EJP PDF (maths.tcd.ie EMIS mirror, article 638), §3, Thm 3.1.
- Persistence: γ(A, φ) = min{1, φ[A]/π[A]}; conductance Φ_P(A) = (1_A, P1_{A^c})_µ /(µ(A)µ(A^c)).
- Thm 3.1 (stated "for any swapping or simulated tempering chain with a set of densities φ_k not necessarily tempered versions
  of π"): for any A and k*, Gap(P_sc) ≤ 12 max{ max_{k≥k*} Φ_{T_k}(A), max_{k≥k*, l<k*} δ(A,k,l), max_{k<k*} γ(A,k) }-type
  bound (and a 192·(·)^{1/4} bound for simulated tempering). Torpid mixing needs BOTH low persistence at the hot levels AND
  low conductance (a metastable A) at the cold levels.
- Verbatim: "If A has low persistence for small values of β, then a parallel or simulated tempering chain starting in A^c may
  take a long time to discover A at high temperatures".
- READING FOR US: the masked regime is exactly "low persistence of the S₀ basin under the start φ_0 = π₀". But on LH the
  cold-level conductance is NOT small: the target is unimodal there (API-POS Prop U, enumeration), so Chang–Zhou Thm 1 gives
  Gap ≥ 1/(c(ρ)M) and Cheeger gives Φ ≥ Gap. So WSH's torpidity mechanism does not bite on LH; it would bite only for a
  family where the target itself has a second metastable mode (T37-type designs / study dilution?).

## N5. Gamarnik & Zadik, "Sparse high-dimensional linear regression. Algorithmic barriers and a local search algorithm",
## arXiv:1711.04952v2 (2019). Read: abstract, §1, §2.4 (LSA), Thm 2.7. (A related AoS 50(2) 2022 paper "Estimating squared
## error and a phase transition" exists — seen only on projecteuclid listing, UNVERIFIED content.)
- Model: X iid N(0,1) entries, k-sparse β*, noise N(0,σ²). n_alg := k log p; n* := 2k log p/log(2k/σ² + 1).
- Abstract (verbatim): "nalg, up to a multiplicative constant factor, is a phase transition point for the appearance of a certain
  Overlap Gap Property (OGP) over the space of k-sparse vectors ... if n > C nalg ... a very simple algorithm based on a local
  search improvement rule is able both to ℓ2-stably recover the unknown vector β* and to infer correctly its support".
- Thm 2.7: ∃ c, C: if n ≥ C n_alg and σ² ≤ c|β*|²_min min{log p/(log log p), k}, LSA (swap-type best-improvement local search
  over k-sparse supports, from ANY k-sparse start) terminates with Support(β̂) = Support(β*), ‖β̂ − β*‖ ≤ σ, w.h.p.
- OGP is presented as EVIDENCE of hardness (no MCMC lower bound is proved in this paper).
- Study scale: S1 (iid design), s₀ = 14, n = 200: n/(s₀ log p) = 2.33 (p = 500), 2.07 (p = 1000). Constants c, C are
  unspecified, so the study is not certifiably on either side.

## N6. Zhou & Smith, "Rapid convergence of informed importance tempering", AISTATS 2022 (PMLR 151); arXiv:2107.10827v2. Read: §3, Assumption 1, Lemma 3, Thm 1.
- Assumption 1 (verbatim): "max_x |N(x)| ≤ p^α ... There exist a state x*, an operator T : X → X and some constants ν > α
  such that T(x) ∈ N(x) and π(T(x)) ≥ p^ν π(x) for each x ≠ x*."
- Lemma 3: Gap(P) ≥ κ(p,α,ν) min_{x≠x*} P(x, T(x)), κ = ½{1 − p^{−(ν−α)/2}}³. Thm 1: Gap(Q_h) ≥ κ h(p^ν)/E_π[Z_h];
  e.g. ≥ κ p^{ν−α}/2 for h = h_{+1}.
- Same unimodal-with-strong-ratio hypothesis as YWJ/ZYVR/Chang–Zhou.

## N7. Li, Smith, Zhou, "Importance is important: generalized Markov chain importance sampling methods", arXiv:2304.06251v2 (Oct 2024). Read: abstract, §1.
- Rejection-free multiple-try / informed importance-sampling schemes on discrete spaces with "a general theory on its
  complexity" (Thm 1: asymptotic-variance comparison with the M–H version given Gap(P̃) < 1). Variable selection is an example.
  No new landscape condition; inherits the unimodal assumptions above.

## N8. Atchadé, "Approximate spectral gaps for Markov chains mixing times in high dimensions", arXiv:1903.11745v2
## (SIAM J. Math. Data Sci. 2021 per search snippet; venue UNVERIFIED). Read: abstract, H2, Thm 6 and discussion.
- Abstract: "for well-chosen initial distributions the mixing time of the Gibbs sampler is polynomial in the dimension".
- Thm 6: Gibbs sampler for spike-and-slab regression, initialised at ν0 = Π(·|δ^(i), z) with δ^(i) ⊇ δ̃* (a SUPERSET of the
  truth with FP false positives); mixing time polynomial under H1 (well-specified, sub-Gaussian) and H2 (sparse-eigenvalue
  condition on L_δ^{-1}, "rules out settings where a small number of columns of X have the same linear span as all the columns").
- Verbatim: "the initialization strategy sometimes used in practice where δ^(i) is taken as the zero vector is sub-optimal,
  and might result in Markov chain with exponential mixing times" (a suggestion, not proved).
- READING FOR US: the closest published analogue of "the start matters": a warm start must CONTAIN S₀. Our masked start
  is exactly a start whose mode does not contain S₀.

## N9. Jiang, "From estimation to sampling for Bayesian linear regression with spike-and-slab prior", arXiv:2307.05558v1 (2023). Read: abstract, §1.1, Prop 2.8 heading.
- Prop 2.8 (Gibbs convergence rate) under event E_s with a warm start "made possible by frequentist estimators"; Thm 3.7:
  stochastic-localization sampler guarantee. Quotes YWJ's slow-mixing example as the reason for the size cap.
  Venue UNVERIFIED.

## N10. ZYVR (2022) re-check of Condition 1 / Thm 1 (local copy Papers/Core_bibliography/10_..., arXiv:2105.05719v3)
- Condition 1 (1a) overfitted: B(γ, γ∪{j}) ≤ p^{−c0}; (1b) underfitted: ∃ j ∈ γ*∖γ with B(γ, γ∪{j}) ≥ p^{c1};
  (1c) underfitted with |γ| = s0: ∃ swap with B ≥ p^{c1}.
- Thm 1 (verbatim): "Suppose that n = O(p), s0 log p = O(n) and κ = O(s0). If Condition 1 holds for c0 = 2 and
  4 ≤ c1 ≤ nκ1 − κ, then, for sufficiently large n, we have Tmix ≤ 800 max{nκ1/c1, 3s0}."
- API-POS measured on LH at n = 200 (paper's target): c1(1b) = 2.81 (c = 1), −0.34 (c = 2); c0 = −0.30 / 0.22. So the
  numerical requirements c0 = 2, c1 ≥ 4 fail at n = 200 even at p ≤ 20.

## N11. Pozza & Zanella, "On the fundamental limitations of multiproposal MCMC", arXiv:2410.23174v1; Biometrika 2025
## (doi 10.1093/biomet/asaf019 per search snippet, UNVERIFIED). Read: abstract, Thm 1/Cor 1 statements.
- Cor 1: Gap(P^(K)) ≤ K·Gap(P̃) for ANY multiproposal scheme with K candidates (arbitrary targets, incl. discrete).

## N12. Others read briefly (local PDFs)
- Liang, Livingstone, Griffin (2022, Stat. Comput.; local 01 = arXiv:2110.11747): ARN/PARNI samplers. Thm 2 (verbatim):
  "ergodicity (44) and a strong law of large numbers (45) hold for both the PARNI-KW and PARNI-RM samplers". No rate.
- Staerk, Kateri, Ntzoufras (2024, Bayesian Analysis per INDEX; local 08 = arXiv:2105.01039v2): MAdaSub. Thm 1 (verbatim):
  "The MAdaSub algorithm (Algorithm 1) is ergodic ... and fulfils the weak law of large numbers." No rate.
- Griffin, Łatuszyński, Steel (2021, Biometrika 108(1)): ergodicity + SLLN, no rate (via API-POS §2, which read arXiv:1708.05678v3;
  I re-downloaded it but did not re-read the proofs).
- Zanella (2020, JASA; local 09 = arXiv:1711.07424): Thm 2/3 Peskun-type comparison: for any g, the balanced g̃(t) =
  min{g(t), t g(1/t)} gives P_g̃(x,y) ≥ (c_g c_g̃)^{-1} P_g(x,y) ∀ x ≠ y; Thm 4: weak limit of the first k coordinates under
  informed proposals as n → ∞ (product-type targets). No BVS mixing-time theorem.
- Zanella & Roberts (2019, JRSS-B 81(3); local 14): Thm 1 (verbatim): "For every h ∈ L2(X, f) we have
  var(h, TGS) ≤ b² var(h, GS) + b² var_f(h)." §3.3: TGS overcomes strong pairwise and k-wise negative correlations, "does not
  help significantly in overcoming strong k-wise positive correlations". §4.5 quantitative results only for diagonal and
  fully collinear X (API-POS §1.4).
- Schäfer & Chopin (2013, Stat. Comput.; local 07 = arXiv:1101.6037v4): SMC on binary spaces for BVS with adaptive
  logistic-conditional proposals; claims (§1.2, empirical): "global methods ... are often more robust than local methods
  based on Markov chain Monte Carlo. The latter are more prone to get trapped in the neighbourhood of local modes." No theorem
  on discovery or complexity.
- Le Fay, Chopin, Vihola (2026, arXiv:2604.03352v2; local 24): finite-sample bounds for standard and waste-free SMC.
  Thm 2.3 / 3.2 assume each kernel K_t has spectral gap γ_t > 0 and use γ = min_t γ_t (Assumption 2.4) and a χ²-bound
  1 + χ²(π_t | π_{t−1}) ≤ χ̄² between successive targets (Assumption 2.2). Recalls Marion, Mathews, Schmidler (2023, 2025).
  i.e. the bound is only as good as the GLOBAL gap of the mutation kernels.
- Zhou & Chang (2023, AoS 51(3):1058–1085; arXiv:2101.04084): general finite-state mixing bound (Thm 1–2) under a
  Condition 1 of the same unimodal-ratio type; applied to DAG equivalence classes. Not BVS-specific.
- Kim & Ročková, "On mixing rates for Bayesian CART", arXiv:2306.00126 (EJS 19 (2025) 3041–3067 per search snippet,
  UNVERIFIED): abstract only: grow/prune Bayesian CART "cannot reach deep isolated signals" faster than exponential mixing time.
  (A lower bound in a neighbouring discrete model; I read only the abstract.)

## N13. Own numerical check (scripts/rz_lh.py → results/rz_lh.md)
See REPORT §4.
