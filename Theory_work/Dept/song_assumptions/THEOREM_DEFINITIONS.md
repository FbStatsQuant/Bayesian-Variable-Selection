# THEOREM DEFINITIONS — Song & Liang (2015) ↔ SMC-BVS, and our target theorems

Theory Department, mission TH-SONG-ASSUMPTIONS, 2026-11-27. Task Lead: Opus 5.5. **v1.4 (senior review: completeness, generality and naturalness; converged text in council/V14_CHANGESPEC.md). v1.3 = council round-2 revision (advisor rounds Astra 6.2 R1–R2, Fable 5.2 R1; SL citation audit: Sol 6.2; data: D1; literature: C2). See COUNCIL_RECORD.md.**
Scope: define the targets and their assumptions. **No proofs are claimed here.** Statuses of results already delivered for
v3.1.1 are quoted from the manuscript/registry; everything marked **[TARGET]** is a conjecture whose proof path is in
`ASSUMPTIONS_AND_PROOF_PATHS.md`.

Sources read directly for this file:
- SL = Song, Q. & Liang, F. (2015) *J. R. Statist. Soc. B* 77(5), 947–972 (journal pagination);
- SLs = its online supplement (20 pp., printed page numbers = PDF pages; obtained from the OUP article page's supplement
  link 2026-11-27; local read-only copy in the main clone `Papers/Core_bibliography/32b_2015_Song_Liang_supplement.pdf`
  and in this worktree's `.rc_tmp/song/papers/`, not tracked: the repo is public). Main-text journal page = PDF page + 946;
- our statements: manuscript on main (`Docs/Writing/manuscript/sections/or6_theorems.tex`, `supplement.tex`,
  `s4_results.tex`) and `Theory_work/Dept/prep/TH_PREP.md`.

Owner scope ruling (2026-11-27, TH_PREP §0a): the three targets are (1) true-distribution consistency, (2) true-model
(selection) consistency, (3) consistency under misspecification. Sampler (particle-limit) and reported-model results are
DEFERRED; they are catalogued below only so the 1-to-1 map is complete.

---

## 1. The object of every theorem: the posterior of SMC-BVS v3.1.1 as coded

| element | as coded | SL counterpart |
|---|---|---|
| data | the method runs on the predictors that are not constant in the sample; X, y centred and scaled (column SD s_{x_j}, s_y, divisor n−1); no intercept parameter. The posterior is undefined if fewer than two predictors remain or y is constant; such data sets are counted in the exceptional event of every theorem (or6 l.116) | SL Thm 1 standardises and bounds predictors (p. 952) |
| raw-unit map | a coded draw (S, b, v) maps to β_j = s_y b_j/s_{x_j} (j ∈ S), σ² = s_y² v, and the conditional law N(ȳ + (x − x̄)ᵀβ, σ²) of y given x | SL work in standardised units |
| slab | β_S \| S, σ² ~ N(0, nσ²(X_SᵀX_S + I)⁻¹): g = n with unit ridge | same family as SL's SAM prior with precision V_ξ⁻¹ = (X_ξᵀX_ξ + τI)/n (explicit precision on SLs p. 16; SL p. 959 prints it in the covariance slot, an apparent inversion typo given the covariance convention σ²V_ξ of SL p. 951); τ = 0.01 in SL (p. 960) vs τ = 1 here. Theorem S itself is stated for the unregularised precisions I and XᵀX/n; the ridge variant is asserted in the paragraph before Cor S1 (SLs p. 16) via a "Lemma A.2 of the Appendix" that is not in the 20-page supplement |
| σ² | IG(0.01, 0.01) on the coded (standardised) outcome, i.e. raw-unit rate b₀s_y² | IG(a₀,b₀), SL use a₀ = b₀ = 1 (p. 960) |
| model prior | BB(1,p): π(S) ∝ ½/C(2p−1,\|S\|) on Ω = {\|S\| ≤ K}, K = min(p, ⌊n/2⌋) | SL (6), p. 951: independent Bernoulli(r_n/P_n) truncated at r̄_n, with r_n/P_n → 0; the choice r_n = P_n^{1−γ} (γ = 0.75 by default) is made separately (EBIC comparison p. 952; default p. 960); stage 1 uses λ_s = \|s\|^{−γ} (pp. 959–960) |
| report | MPM (PIP > ½); HPM stored | SL: PIP thresholding ξ_q = {j : q_j > q} with q from an FDR procedure (p. 956), or MAP (p. 959) |
| algorithm | SMC with frozen tempering (DEFERRED results) | SAMC (SLs §2) |

Engine decision (HQ, SMC-PERF closed, memo 1b319090): v3.1.1, g = n, truncated BB(1, p) and MPM are confirmed; Fix E
(output-only) and C1 (compute-only) do not touch the theorems; proof writing and Lean stay on hold. Notation follows the
manuscript spec: coded coefficients θ_S/θ*, raw coefficients β*.

Two consequences used throughout. (i) The per-variable cost of adding a predictor to a size-k model is
**price(k) = log[(2p−1−k)/(k+1)] + ½ log(n+1)** (prior + Occam), ≈ log(2p/s0) + ½ log n near the truth (for scale only:
7.6–10.4 nats at S1/S2's sizes, D1 tables). (ii) The size marginal of BB(1,p) decays like 2^{−k} while each model carries a p^{−k}-type multiplicity
penalty (Scott & Berger 2010); SL instead use r_n/P_n → 0 (p. 951) and a small cap r̄_n.

---

## 2. Every important result in Song & Liang (2015), read directly

Notation of SL: P_n predictors, t = true model, ξ = a model, ε_n a radius, r_n/P_n the prior inclusion probability, r̄_n the
model-size cap, B(r_n) = sup_{|ξ|=r_n} ch₁(V_ξ⁻¹), B̃_n = sup_{|ξ|≤r̄_n} ch₁(V_ξ), Δ(r_n) = inf_{|ξ|=r_n} Σ_{i∉ξ}|β*_i|, d the Hellinger
distance between joint densities of (x, y). SL p. 952 define d² = ∫∫(√f₁ − √f₂)², which is **2×** our d_H² = 1 − ∫√(ff*) (the supplement's proofs use the 1 − ∫√ convention); radii differ by the factor √2, which is immaterial to rates. Model (1) of SL (p. 947) has no intercept.

Standing assumptions of SL §2 (p. 950, page image checked): P_n ≻ n^θ for some θ > 0 (SL's notation: b_n ≻ a_n means
a_n/b_n → 0, so P_n grows faster than some power of n — a lower bound, not a cap), plus sparsity (3) or (4).

| # | SL result (page) | exact content | conditions |
|---|---|---|---|
| SL-0 | **Posterior (7)** and its EBIC link (pp. 951–952) | marginal posterior of ξ after integrating β_ξ, σ²; with V_ξ⁻¹ = X_ξᵀX_ξ/n, a₀ = b₀ ≈ 0 and r_n = P_n^{1−γ}: log π(ξ \| D_n) ≈ −EBIC_γ(ξ) + C, EBIC_γ(ξ) = −l̂(ξ) + (\|ξ\|/2) log n + γ\|ξ\| log P_n (p. 952) | approximation, not a theorem |
| SL-1 | **Theorem 1**, posterior consistency (p. 952) | P*[π{d(f,f*) > ε_n \| D_n} > exp(−c₁nε_n²)] < exp(−c₁nε_n²) for large n (display (15)) | D_n from model (1); ε_n ∈ (0,1); all predictors standardised and \|x_i\| ≤ 1; approximate sparsity (3): lim Σ_j\|β*_j\| < ∞; nε_n² ≻ 1 and (8) Δ(r_n) ≺ ε_n, (9) r̄_n ln(1/ε_n²) ≺ nε_n², (10) r̄_n ln(P_n) ≺ nε_n², (11) r̄_n ln(nε_n²B̃_n) ≺ nε_n², (12) 1 ≤ r_n ≤ r̄_n < P_n, (13) r_n ≺ P_n, (14) B(r_n) ≺ nε_n²; asymptotics with P_n ≻ n^θ (p. 950). Proof via SLs Lemma 1.1 (p. 1), attributed to Jiang (2005) Thm 6; the main text introduces Thm 1 as following Jiang (2007) |
| SL-2 | **Theorem 2** (p. 953) | same conclusion as (15) | D_n from model (1); Condition 1 (p. 953): E exp{(Σ_{i≤r} a_i x_{j_i}/r)²} ≤ e^M for every r ≤ r̄_n subvector and \|a_i\| ≤ δ (exponential moments on sparse directions); ε_n → 0, nε_n² → ∞; (9)–(14); strict sparsity (4): lim Σ_j 1{β*_j ≠ 0} < ∞; r_n ≻ 1; (8) is then redundant (p. 953–954) |
| SL-3 | **Corollary 1**, rates (p. 954) | ε_n = O{n^{−(1−α)/2} log^{k/2} n} if r_n < r̄_n ≺ log^k n; ε_n = O(n^{−min{1−α−q, 1−vq}/2}) if r_n < r̄_n ≺ n^q, 0 < q < min{1−α, 1/v} | Theorem 2's premises; strict sparsity; prior of §2.1.1; P_n < exp(Cn^α), α ∈ (0,1) (stretched-exponential, not exp(cn)); B(r_n) ≤ Br_n^v, B̃_n ≤ Bn^v with B, v > 0 |
| SL-4 | **Condition 2 ⇒ (16)** (p. 954) | lim_n P*[π{d(f,f*) > ε_n \| D_n} > exp(−c₁nε_n²)] = 0 (in-probability version) | Condition 2 (second moments only: E(Σ a_i x_{j_i}/r)² ≤ M on the same sparse subvectors) **replacing Condition 1**, all other premises of Theorem 2 retained |
| SL-5 | **Theorem 3**, sure screening (p. 956) | for each identifiable true x_t: P*[π{t ∈ ξ \| D_n} < 1 − exp(−c₁nε_n²)] < exp(−c₁nε_n²); under Condition 2 the weaker in-probability form. Hence π(t ⊂ ξ_q) →_P 1 if all true predictors are identifiable (p. 956) | Theorem 2's conditions + Condition 3 (p. 955), identifiability: E exp{−(x_k + Σ_{i≤r̄_n} b_i x_{j_i})²} ≤ 1 − δ_n with δ_n ≻ ε_n² for all choices of at most r̄_n predictors **other than x_k** and all b_i ∈ ℝ; for jointly Gaussian x this holds if var(x_k + Σ b_i x_{j_i}) ≻ ε_n² (pp. 955–956) — a **vanishing** residual-variance floor. Proof (SLs §1.2, pp. 5–6): any f omitting x_t has d²(f*,f) ≥ min{δ_n, β_t*²δ_n/(20σ*²), 1 − √0.8} ≻ ε_n² when β_t*²/σ*² is fixed positive (more generally one needs β_t*²δ_n/σ*² ≻ ε_n²), i.e. a residual-signal margin at the Hellinger scale. (Sol audit: the contrast in the proof may involve up to r̄_n + \|t\| − 1 other predictors while Condition 3 covers r̄_n; a careful restatement covers the actual contrast sizes.) |
| SL-6 | **Theorem S**, MAP consistency (SLs p. 13) | max_{k≠t} π(k \| D_n)/π(t \| D_n) →_P 0 (display (24)) — pairwise odds; does not by itself give π(t \| D_n) → 1 | D_n from model (1) with sparse t; condition (12); fixed-design sample eigen-structure (22) with {l_n} non-increasing and {l'_n} non-decreasing: n l_n < ch'₁(X_ζᵀX_ζ) ≤ ch₁(X_ζᵀX_ζ) < n l'_n for all \|ζ\| = min{\|t\| + r̄_n, n}; (23) r̄_n log P_n ≺ n l_n; and either V_ξ⁻¹ = I with n l_n ≻ log l'_n, log(√(n l_n)/r_n) ≻ √(log P_n), or V_ξ⁻¹ = X_ξᵀX_ξ/n with n l_n ≻ l'_n, log(√n/r_n) ≻ √(log P_n). The proof (SLs pp. 14–15) uses a noncentrality ≥ n l_n c², c = min_{i∈t}\|β*_i\| treated as fixed, so that (23) gives n l_n c² ≫ log r̄_n + r̄_n log P_n (our reading: an implicit diverging-multiple beta-min × eigenvalue floor; not a separately stated hypothesis). Sol audit: the printed step bounds a maximum over underfitted models where a minimum is needed. SL's own remark (SLs p. 15): "(22) is hardly satisfied"; they replace it by the random-design condition (26): for **each** set \|ζ\| = r̄_n + \|t\|, P[λ_min(X_ζᵀX_ζ) < n l_n or λ_max > n l'_n] < e^{−nC}, then a union bound (unnumbered display, SLs p. 15) using r̄_n log P_n ≺ n; SLs p. 16 say it holds for Gaussian designs with eigenvalues of Var(x) bounded by l_n, l'_n (Fan & Lv 2008, App. A.7) — concentration needs slack between population and sample thresholds |
| SL-7 | **Corollary S1** (SLs p. 16) | MAP consistency | sparse t; prior of §2.1.1; P_n < n^{κ log n}, κ ∈ (0, 1/4) (quasi-polynomial p); V_ξ⁻¹ = X_ξᵀX_ξ/n (+τI/n); r̄_n ≺ log^{k₁} n (k₁ > 0) or r̄_n ≺ n^q with q ≤ ½ − √κ; l'_n = l_n⁻¹ = √n/log^{k₂} n (k₂ > 0). Audit note (Sol, Astra): at log P_n ≍ κ(log n)², log(√n/r_n)/√(log P_n) stays bounded, so Theorem S's printed ≻ condition does not follow by substitution at that endpoint; quote the corollary as printed |
| SL-8 | **Theorem 4**, misspecified subset (p. 957) | for a fixed subset s not containing all true predictors: π[{f ∈ P_s : d(f₀, f) > ε} \| D_n^s] → 0 almost surely, every ε > 0 (display (18), p. 957); f₀ = KL projection of f* onto P_s, defined in display (17), p. 956. Proof: SLs Lemma 1.2 (p. 6) = De Blasi & Walker (2013) Cor 1 (KL-neighbourhood prior mass + summable covering-set masses ⇒ a.s. concentration at the KL minimisers). Minimising the KL formula SLs (6) (p. 6) gives f₀ = φ(y; β₀ᵀx_s, σ₀)ν(x_s), σ₀² = σ*² + E(β₀ᵀx_s − β*ᵀx)², and (19), p. 957: β₀ = Σ_s⁻¹Σ_{s,t}β*_t (centred reading; with an intercept use covariances) | Condition 4 (p. 957): E{(aᵀx_s)²} < ∞ for \|a_i\| ≤ δ; IG prior on σ², Gaussian slab, π(ξ) > 0 for every ξ ⊆ s; \|s\| fixed (finitely many models, SLs p. 7) |
| SL-9 | **Corollary 2** (p. 957) | π(s̃ ⊂ ξ \| D_n^s) →_P 1, s̃ = supp β₀ (inclusion of the pseudo-true support; unnumbered display, p. 957; β₀ from (19)). The following prose claims selection "if and only if β₀,t ≠ 0", but the corollary's inclusion conclusion gives no exclusion guarantee | Theorem 4 + no exact multicollinearity in x_s (no a ≠ 0 with P(aᵀx_s = 0) = 1). Explicitly not claimed under a binding size cap (p. 958, remark (c)) |
| SL-10 | **Condition 5** + iterative procedure (p. 958) | \|cov(x_t, y)\| > 0 for every true x_t ⇒ re-screening the unselected predictors until no further selections keeps every true predictor of x_s | within the screening setup of SL-8/9; the implementation stops after 2 rounds (remark (b), p. 958) |
| SL-11 | SAM consistency (p. 959, §3.1) | "Clearly, it follows from the theory … that the SAM approach will lead to a consistent selection of true predictors" | informal composition of SL-5/6/8/9/10; no separate theorem |
| SL-12 | Time complexity (§6, pp. 968–969) | parallel cost O(P_n^{(1+α)/2} + nP_n) with K_n = O(√P_n) subsets (p. 968); serial O(√P_n[P_n^{(1+α)/2} + nP_n]) (p. 968) | enough processors, equal blocks, T = O((P_n/K_n)^α), α ≥ 1, small caps, bounded retained size; algorithmic analysis, not a theorem |
| SL-13 | SAMC estimator (SLs §2, p. 12; Lemma S2, p. 17) | estimator (21) on SLs p. 12; q̂_j → q_j a.s. as the number of iterations N → ∞ (SLs p. 13, citing Liang 2009); SAMC regional log-weight limit (SLs pp. 9–10). Lemma S2 (SLs pp. 16–17): consistency of the sample maximum used for MAP search (no PIP content) | algorithm convergence |

---

## 3. One-to-one map: each SL result → our counterpart

Legend. **Delivered** = a v3.1.1 result exists (status quoted verbatim). **[TARGET]** = a theorem this mission defines, with a
proof-path sketch and assumptions in `ASSUMPTIONS_AND_PROOF_PATHS.md`; no proof is claimed. Each target carries a risk tag
from the advisors. **Deferred** = outside the owner's scope ruling. **N/A** = no counterpart, by design.

| SL | our counterpart | relation | status |
|---|---|---|---|
| SL-0 (posterior (7), EBIC link) | the coded marginal posterior; price(k) (§1) | at small k our per-variable price is log(2p/k) + ½ log(n+1) ≈ EBIC_γ with γ ≈ 1. The EBIC consistency threshold for fixed s0, γ > 1 − 1/(2A) at p = n^A (Luo & Chen arXiv v1 p. 7, attributed to Chen & Chen 2008), is met. This is a heuristic comparison only: SL's EBIC link is a first-order approximation under its own slab and prior, and the Luo–Chen threshold concerns EBIC under its own identifiability assumptions, so it does not transfer consistency to the coded score (Sol R2) | context only |
| SL-1, SL-2 (Hellinger consistency) | **TD** (§4.1) = delivered `thm:dist` | Same metric, up to SL's factor √2: Hellinger distance between joint densities, x from its true law. Same exponential form, with exp(−c·nε²) = n^{−cM} inside the window ε² = M log n/n, M ≤ √n/log n. We allow K = n/2, where SL's (9)–(10) would fail at r̄_n ≍ n, and we need no beta-min and no fixed eigenvalue floor. SL's p. 951 remark (after Jiang 2007 (38)) that the cap can be removed has its counterpart in our window q_n: the BB(1, p) size tail gives an effective prior-tail cutoff of the same order as SL's sieve r̄_n ≍ M log n/log 2; q_n must still pay the true-model denominator and does not inherit SL's entropy conditions. Delivered alternatives: `prop:dist(ii)` (no eigenvalue floor, A-SUBG on singletons only, slower radius) and `thm:dist-param` (a rate analogue under detectable signals and a fixed floor on its own window); neither recovers SL's growing-p second-moment theorem. SL allow stretched-exponential P_n | delivered: "Proved and independently checked. Registry row 2.1." **[TARGET] TD′** (dimension-relaxed) and **TD-as** (almost sure) |
| SL-1's approximate sparsity (3), p. 950 | **A-BS** (direct counterpart); **TD-A** (optional corollary) | lim Σ_j \|β*_j\| < ∞ with standardised predictors and fixed σ* implies A-BS. TD-A relaxes strict sparsity by a change of measure to a sparse surrogate (Fable Q7); not an owner target | A-BS: assumption; TD-A optional [TARGET], low priority |
| SL-3 (Cor 1 rates) | TD / TD′ radius (**partial analogue**) | Different prior, sparsity/cap and rate trade-off. Ours is √(M log(p∨n)/n). TD′'s dimension envelope would overlap SL Cor 1 for α < ½ without recovering the corollary in full, and its proof route is open (high risk, Astra R2). For α ∈ [½, 1) the *current route* would also need a model-size cap c·n/log p for isometry; a cap does not fix the testing step; this is a statement about our route, not about all proofs | delivered for p ≤ n^A; TD′ conjecture, high risk |
| SL-4 (Condition 2: second moments only) | **TM-a0** (moments-only, fixed dimension; **partial analogue**) | SL-4 weakens tails while keeping growing dimension and the other Thm 2 premises; TM-a0 matches the moments only at fixed dimension. For growing p our exact-marginal route needs exponential tails on sparse sets, so Condition 2 is not targeted there | non-target with reason (Astra Q7, Fable Q7) |
| SL-5 (Thm 3 sure screening) | **TS-a** (§4.2), per predictor first, then jointly | Same route: a Hellinger separation for every model that omits x_j, combined with contraction; like SL Thm 3, TS-a is stated for each predictor that satisfies its own margin, whatever the other signals do. SL Condition 3's role (residual identifiability) is taken by A-MARGIN-H, a lower bound on R. SL Condition 3's Gaussian sufficient form ch₁{var(x)} ≻ ε_n² (pp. 955–956) is the precedent for the vanishing floor of A-NEC; A-NEC at the 1/n scale does not supply SL's screening separation, which is A-MARGIN-H's job; A-SUBG only converts R into Hellinger separation, d_H² ≥ c_L·min{1, R/(nσ²)} (it does **not** imply Condition 3: Gaussian duplicates have R = 0; Astra R2 Q4). SL's thresholded-PIP consequence needs a threshold kept away from one or a rate comparison with the omitted posterior mass; SL's FDR threshold discussion (p. 956) is separate from the fixed-q consequence | **[TARGET]**, low risk |
| SL-6, SL-7 (Thm S, Cor S1: MAP) | **TS-b** (§4.2); previously delivered analogues `thm:post-random`, `thm:post-fixed`, `thm:post-margin` | Our conclusion is stronger: π(S0 \| y) → 1 with a rate, HPM = MPM = S0, and every PIP within the rate (SL give pairwise odds only, with no rate). SL's sample eigen-structure (22) is replaced by a vanishing population floor used together with A-SUBG; SL's (26) is a two-sided sample condition with a vanishing lower threshold l_n ≫ r̄_n log P_n/n and a growing upper threshold, on sets of size r̄_n + |t|; where the regimes overlap c_ψ/n lies below l_n, but the objects, normalisations and windows differ, so this is not a uniform dominance (and NH14's p_n^{−κ} floor can be smaller than c_ψ/n at large p). A converse (under A-NEC on T) is added | delivered (fixed signals, fixed floor): "proved and independently checked" (previously delivered analogues). **[TARGET] TS-b** (population margin form A-MARGIN-U; S1/S2 evidence in SIMULATION_DATA_ANALYSIS, not in the statement) |
| SL-8 (Thm 4: misspecified density consistency) | **TM-a0** (fixed candidate dimension, a.s.; a partial analogue with added score moments); **TM-a** (high-dimensional candidates, with rate) | Both concentrate on the KL projection f₀ of SL (17)/(19). SL Thm 4 assumes a fixed candidate subset, Condition 4, a Gaussian parent model and positive priors; it does not invoke global strict sparsity (4). SLs Lemma 1.2 (= De Blasi–Walker Cor 1) is the tool SL use | **[TARGET]**; TM-a0 low risk, TM-a low–medium |
| SL-9 (Cor 2: inclusion of the pseudo-true support) | **TM-a0-inc** (direct counterpart, fixed dimension, second moments only); **TM-b**; previously delivered analogue `thm:omitted` | TM-a0-inc is SL Cor 2's inclusion statement. TM-a0 and TM-b go further: exact selection of S0^C = supp β^C, which SL's prose claims but their inclusion-only display does not give | delivered: "Proved and independently checked". **[TARGET] TM-a0-inc** (low risk), **TM-b** (margin form) |
| SL-10 (Condition 5, iterative screening) | none needed | We do not split predictors, so there is no screening stage whose misses must be repaired | N/A by design |
| SL-11 (SAM consistency, informal) | TS-b on the full data | Our method runs on all p predictors, so TS-b *is* the end-to-end selection guarantee for the exact posterior | N/A (covered by TS-b) |
| SL-12 (§6 time complexity) | SMC cost analysis | Not a theorem in SL either | Deferred |
| SL-13 (SAMC q̂_j → q_j; Lemma S2) | particle-limit theorems (TH_PREP §2) | algorithm convergence | Deferred (owner scope ruling) |

---

## 4. Target theorems: exact mathematical and plain-English statements

**Common setting.** Data D_n = {(x_i, y_i)}_{i≤n} are i.i.d. (random design) unless stated otherwise.

- True model: y = α* + xᵀβ* + ε, with ε ~ N(0, σ*²) independent of x, x ∈ ℝ^p, covariance Σ, correlation matrix R.
- S0 = supp β* and s0 = |S0|. For a rival model S, write D = S0∖S (d = |D|, the true predictors it misses) and N = S∖S0 (m = |N|, the nulls it adds).

**Notation.**

- **Residual signal.** R_n(S) := n·inf_{a,b} E(xᵀβ* − a − x_Sᵀb)². This is n times the population linear-projection error of the true signal on x_S. The Schur form n·β*_Dᵀ Σ_{DD·S} β*_D holds for any design with finite second moments (no Gaussianity needed). Its sample twin is R̂(S) = ‖(I − P_S)Xβ*‖² (centred X).
- **Leakage.** For B ⊆ S, ϑ(B, S∖B) := 1 − R_n(S)/R_n(B) ∈ [0, 1] is the share of the signal left unexplained by B that S∖B explains.
- **Price of a rival.**
  Pr_n(d, m) := log[C(2p−1, s0)/C(2p−1, s0−d+m)] + ((d−m)/2)·log(n+1), and Pr_n(d) := Pr_n(d, 0) = Σ_{k=s0−d}^{s0−1} price(k).
  This is the prior × Occam log-cost of a single rival S relative to S0 (Fable notation). It is distinct from a summed class bound such as v1.3's B_Dm. In generic-prior form, Pr_n(d) = max_{|D|=d} log[π(S0∖D)/π(S0)] + (d/2)·log(n+1); for another prior the price must be re-derived.
- **Margin ratio.** κ_n := min_{∅≠D⊆S0} R_n(S0∖D) / (2σ*²·Pr_n(|D|)).
- **Posterior and densities.** Π(· | D_n) is the exact posterior of (S, β, σ²) in §1. A posterior draw defines the conditional law N(ȳ + (x − x̄)ᵀβ, σ²) of y | x. f is the joint density with respect to ν(dx)dy, ν the true law of x (so discrete predictors are covered; Sol R2), f* is the true joint density, and d_H(f, f*)² = 1 − ∫√(f f*).

Assumption labels refer to `ASSUMPTIONS_AND_PROOF_PATHS.md` §2. They form four blocks:
- **Model:** A-GL, A-SPARSE, A-DIM, A-BS.
- **Design:** A-SUBG, A-NEC (on sets of size ≤ k_n, below).
- **Signal:** A-MARGIN-H for screening, A-MARGIN-U for exact selection.
- **Omitted variables:** A-MIS(iii) with A-SPARSE-C; A-MOM for the fixed-dimension results.

No assumption names a design family or a simulation constant; S1/S2 enter only as evidence (SIMULATION_DATA_ANALYSIS, DOSSIER).

**Windows.** A-SUBG and A-NEC are imposed on sets of size ≤ k_n, a deterministic design order with k_n ≥ q_n(M) at the claimed level: for fixed-level statements it suffices, across all fixed levels, to impose them on sets of size ≤ c·log n for every fixed c (a single fixed level needs only one such window); for M = M_n → ∞ (the delivered `thm:dist` range M ≤ √n/log n) it is q_n(M_n); for TD′ it is the enlarged q_n. The constants L and c_ψ are common.

### 4.1 TD: true-distribution consistency (SL Theorems 1–2, Corollary 1)
**Mathematical statement (delivered form, `thm:dist`).** Assume A-GL, A-SPARSE, A-DIM, A-SUBG, A-NEC and A-BS. There are constants c_H > 0, M₀ and n₀, depending only on (s, A, L, c_ψ, b̄), such that for every M ≥ M₀ and every n ≥ n₀ with √n/log n ≥ M,

  P*[ Π( d_H(f, f*) > √(M log n / n) | D_n ) > n^{−c_H M} ] ≤ n^{−c_H M}.

The delivered assumption set imposes A-SUBG and A-NEC on the level-dependent size window q_n(M) (or6 `asm:dist`); in the general form above this is the window k_n ≥ q_n(M).

**TD-as [TARGET, low risk].** Fix the truth as a sequence (all D_n on a common probability space) and choose M ≥ M₀ with c_H·M > 1. Then
Π(d_H(f, f*) > √(M log n/n) | D_n) → 0 P*-almost surely. Proof path: Borel–Cantelli on the display above, since
Σ_n n^{−c_H M} < ∞. This is the counterpart of SL's almost-sure mode in Thm 4.

**TD′ [conjecture, HIGH proof risk at the proposed rate].** Replace A-DIM by A-DIM′, (s+1)·M·log p·log(p∨n) ≤ c_dim·n (the conjecture's regime is log p = o(√n); this product form is a sufficient isometry budget only, not the same condition: at fixed M, log p ∼ a√n with small a > 0 satisfies the budget but not the regime). Conjectured statement (exact, Sol R2): keep 2 ≤ p and the coded input domain with its exceptional event, and impose A-SUBG and A-NEC on the enlarged window q_n = min{p, ⌈C′(s+1)M log(p∨n)⌉}. Then there are c > 0 and M₀ such that for every M ≥ M₀ with M log(p∨n) ≤ c√n and ε_n² = M log(p∨n)/n,

  P*[ Π( d_H(f, f*) > ε_n | D_n ) > exp(−cM log(p∨n)) ] ≤ exp(−cM log(p∨n)).

- Fable's route: the Fubini size-tail identity gives a coarse size cutoff q_n ≍ min{p, (s+1)·M·log₂(p√n)}, and A-DIM′ gives sample isometry on q_n-sets.
- **The route fails at the testing step** (Astra R2 Q1). At fixed s, M and log p = n^{1/3}, A-DIM′ holds and q_n ≍ L, but the entropy log C(p, q_n) ≍ n^{2/3} exceeds the testing budget nε_n² = M·L ≍ n^{1/3}. The delivered thm:dist also localises to s0 + O(t/log n) by fractional Bayes-factor moments, whose factor p^{1−λ}n^{−λ/2} is not controlled for superpolynomial p.
- A proof needs localisation at a testing-compatible size (≈ t/log p) or a direct prior-weighted predictive bound. A cap of order n/log p fixes the isometry inequality, not the testing inequality. No impossibility follows from the failed route.
- Hence TD′ is a conjecture with high proof risk, and every released statement stays at p ≤ n^A.

**TD-A [optional TARGET].** Approximate sparsity in the spirit of SL (3): if the centred tail r(x) = Σ_{j∉S_n} β*_j (x_j − Ex_j) has sub-Gaussian variance **proxy** ≤ c₀σ*²M log n/n (a small ordinary variance with an unspecified sub-Gaussian norm does not control E exp(r²/σ²); Sol R2), then TD should hold with f* replaced by its s-sparse surrogate. One-observation Hellinger closeness is not enough: the proof needs a full-data change of measure, E_sur[(dP*/dP_sur)²] = (E exp(r²/σ²))^n ≤ exp(O(c₀t)), with Cauchy–Schwarz on exceptional events, c₀ small, and the intercept/mean accounted for (Astra R2 Q5).

**Plain English.** With probability close to one, the posterior puts almost no weight on regression laws whose predictive distribution of y given a new x differs from the truth by more than about √(log n / n) in Hellinger distance. That is the parametric rate up to a logarithmic factor, within the delivered tuning window (M ≥ M₀, p ≤ n^A). No signal-strength (beta-min) condition is needed, because weak predictors that cannot be selected also cannot move the predictive law much. TD′ asks whether the same holds when p grows faster than any power of n; that is open, and our best route fails.

### 4.2 TS: true-model (selection) consistency (SL Theorem 3, Theorem S, Corollary S1)
**TS-a, sure screening [TARGET, low risk].** Assume the TD assumptions at level M.
- **(a) Per predictor.** Let j ∈ S0 satisfy A-MARGIN-H: for every fixed k, inf{ R_n(S) : j ∉ S, |S| ≤ k }/(σ*² log n) → ∞. Then for every fixed c′_H < c_H and large n,

  P*[ Π( j ∈ S | D_n ) < 1 − n^{−c′_H M} ] ≤ n^{−c_H M},

  whatever the other signals do (the counterpart of SL Thm 3, which is also stated per identifiable predictor).
- **(b) Jointly.** If every j ∈ S0 satisfies A-MARGIN-H, then min_{j∈S0} PIP_j → 1 in probability (almost surely, for posterior tails, if c′_H M > 1).

The diverging ratio gives screening at every fixed level M; at an unspecified speed it gives nothing uniform for M = M_n → ∞. **Remark (fixed-level form).** At a fixed level M it suffices that inf R_n(S)/(σ*² log n) ≥ C_L·M over S with j ∉ S and |S| ≤ min(K, J), J := ⌊s + C_s M⌋ (prop:dist(i)), with C_L above the inverse Hellinger-conversion constant; this is sharper for finite-ratio signals and gives the a.s. corollary at a large fixed level. C_L is inexplicit, so TS-a makes no claim at boundary signal levels.

**TS-b, exact selection [TARGET, population margin form, low–medium risk].** Assume A-GL, A-SPARSE, A-DIM, A-SUBG, A-NEC, A-BS and **A-MARGIN-U (population form)**, stated here in full. Write T = S0, s = s0. For a rival S ⊉ T, its **base** is B := S ∩ Q_n, N := S ∖ Q_n, d := |T∖B|, and k := |B∖T| + |N| is the number of added predictors. Let m̄_d := ⌈(2A+1)d⌉ + 1 (the range of delivered `asm:margin`(b) with s replaced by d) and ā(B, N) := min{1, √(2(1 − √(1 − ϑ(B, N))))}.

*A-MARGIN-U.* Fix η > 0 and a deterministic **accounting set** Q_n ⊇ T with log|Q_n| = o(log n). For all large n:
- **(U1) Deletions.** R_n(T∖D) ≥ 2(1+η)·σ*²·Pr_n(|D|) for every nonempty D ⊆ T (equivalently κ_n ≥ 1+η).
- **(U2a) Bases.** R_n(B) ≥ 2(1+η)·σ*²·Pr_n(d) for every B ⊆ Q_n with B ⊉ T and |B∖T| ≤ m̄_d.
- **(U2b) Outside nulls.** For every such B and every N ⊆ Q_n^c with 1 ≤ |N| = m and |B∖T| + m ≤ m̄_d,

  √( R_n(B ∪ N)/σ*² ) ≥ √( 2(1+η)·Pr_n(d) ) + ā(B, N)·√( 2 log C(p−s, m) ).

Q_n is an accounting device, not an object to be found: any such Q_n may be used, enlarging it moves rivals from (U2b) to (U2a), and leakage outside Q_n need not vanish, since it is priced by ā (√ϑ ≤ ā ≤ √(2ϑ) for ϑ ≤ 3/4). Special cases, not separate assumptions: (i) Q_n = T, "no proxies", where every null is priced by its own leakage; (ii) if max ϑ·log p → 0 outside Q_n, (U2a) with η implies (U2b) with every η′ < η; (iii) ā ≡ 1, the structure-free fallback (coefficient 1). Rivals with k > m̄_d need no signal condition: for p ≤ n^A their summed prior-plus-Occam odds are ≤ n^{−γ} for some γ > 0 (TS-b step 2). Classes are restricted to the sieve s − d + k ≤ min(K, J), k ≤ p − s; (U2) and C-i range only over such feasible rivals.

Then, for some γ > 0 depending on (η, A),

  1 − π(S0 | D_n) = O_P( (s0+1)·√(log p/n) + n^{−γ} + n^{−c_H M} ),  P(HPM = MPM = S0) → 1,
  max_j |PIP_j − 1{j ∈ S0}| ≤ 1 − π(S0 | D_n).

- **Population sufficient conditions (corollaries).** (C-i) Strong separation: min R_n(S)/[σ*² log(p∨n)] → ∞ over feasible underfits with |S∖T| ≤ m̄_s implies (U1)–(U2) with Q_n = T. (C-ii) Sparse eigenvalue plus beta-min: if φ² lower-bounds λ_min(Corr(x_V)) over |V| ≤ s + m̄_s and θ_min := min_{j∈T}|β*_j|·sd(x_j)/σ* ≥ (1+η)(1 + √m̄_s)·√(2 log(2p√(n+1))/n)/φ, then (U1) and (U2) hold with ā ≡ 1. For an orthogonal design, a sufficient coordinatewise form of (U1) is β*_j²Var(x_j) ≥ 2(1+η)σ*²·log(2p√(n+1))/n for every j ∈ T; exact (U1) requires n·Σ_{j∈D} β*_j²Var(x_j) ≥ 2(1+η)σ*²·Pr_n(|D|) for each nonempty D.
- **Bridge to the proof (Lemma W, ASSUMPTIONS §2).** The population form implies the **base-indexed** design-conditional width condition on a design event of probability 1 − o(1); TS-b step 3 is run per base. It does **not** imply the v1.3 class-level conditional-width condition when Q_n ≠ T. That condition is kept as a parallel sufficient condition, the **refined design-conditional form** (ASSUMPTIONS §3.3, with credit constant C = 1 by convention); E9/E9b are diagnostics of the refined form only.
- For pure deletions, (U1) is liminf κ_n > 1. Every nonempty D ⊆ S0 counts, not only singletons.
- Models larger than J are handled by the size lemma prop:dist(i), which is proved under A-BS; that is why TS-b keeps A-BS (A-BS′ needs the lemma extended first). Proof obligations (ASSUMPTIONS §3.3): the truncated superset sum, the coded mixed odds per base, and the k > m̄_d step remain to be written out.
- p is the raw dimension, on the event that all columns survive centring (singleton isometry gives this event with probability → 1; Sol R2).

**TS-b converse [TARGET, low risk].** Assume only its minimal set: A-GL, sparse isometry and A-NEC on T (a two-sided determinant refund d·log(n+1)/2 + O(1); a one-sided refund bound cannot prove the converse), and A-BS for the ridge term; the price-scale restriction Pr_n(1) = O(log n) holds under A-DIM. No forward margin is assumed.
- If limsup κ_n < 1, then π(S0 | D_n) → 0 in probability.
- If √R_n(S0∖{j})/σ* − √(2·price_n) → c ∈ ℝ, then liminf P(π(S0 | D_n) ≤ ½) ≥ Φ(−c) > 0. Boundary remainder: log odds = Pr_n(1) − (√λ̂ + Z)²/2 + O_P(1) at λ = O(log n), with V_n/n = 1 + O_P(n^{−1/2}) and λ̂ − λ = o_P(1) by fixed-support relative transfer (relative error O_P(n^{−1/2}) on T, from A-DIM and relative A-SUBG on T); the O_P(1) remainder suffices because the leading fluctuation is √(2Pr_n)·(c+Z). Equality would need control of all other odds (Astra R2 Q3).

The constant 2 is therefore sharp for deletions. The S1 evidence (the transition is bracketed between SNR 1 and SNR 2, not located) is in SIMULATION_DATA_ANALYSIS item 2 (E1) and the U2a check.

**MARGIN\* (v1.3 open refinement) is superseded** by the population form: (U2a) charges every base inside the accounting set the full deletion price, whereas Fable's M1 let inside proxies pay for their entry (the weaker-variant remark, ASSUMPTIONS §2), and the leakage-priced (U2b) replaces M2. A factor-proxy design (Fable Q1(3c)) shows the width term is needed at one (d, m); there is no necessity result for (U2b) in general.

**Rejected:** the uniform "constant 2 for every rival" margin of DESIGN_MEMO_R0. Fable Q1(3d) gives a counterexample for a fixed number m of added nulls when log n = o(log p). The question is OPEN under p ≤ n^A, and it is recorded as a conjecture only.

**Finite-n diagnostic (not a target; withdrawn as a proposition per Astra R2 Q3).** In the idealised χ² score approximation the expected number of one-null extensions beating S0 is E K₁ ≈ (s0+1)/√(2πL(n+1)), L = 2 log((2p−s0−1)/(s0+1)) + log(n+1); this is 0.031–0.050 at S1's (n, p) (0.033–0.056 under Fable's exact-Beta tail). It is a mode-type diagnostic (rivals beating S0 in exact score, an HPM event; MPM failure is separate; Sol R2), a factor ≍ L below the posterior-mass rate term, which is 0.87–1.44 and so not informative at S1's sizes. It is consistent with the S1 shortfall at SNR ≥ 2 (2–8%, 40/41 failures supersets), but P(K₁ ≥ 1) ≤ E K₁ bounds one failure type only and gives no ceiling or lower bound on success (correlated nulls, swaps, higher-order rivals, ridge/IG terms and HPM/MPM/sampler differences are uncontrolled).

**Delivered special case (`thm:post-random`).** Assume A-GL, A-DIM, A-SPARSE, SGR, FSb (fixed b_lo ≤ |β*_j| ≤ b_hi) and EFS (a fixed population floor on sets of size ≤ 5(A+1)(s0+1) log n). Then 1 − π(S0 | y) = O_P(√(log n/n)), P(HPM = MPM = S0) → 1 and max_j |PIP_j − 1{j∈S0}| = O_P(√(log n/n)). Status: "proved and independently checked" (or6 l.83–85). This is a **previously delivered analogue**, not a strict special case: FSb with EFS gives R_n(S) ≥ c·n for every feasible underfit, so A-MARGIN-U holds for large n by corollary C-i with Q_n = S0, but EFS on its window does not imply A-NEC on the possibly wider TD window, so TS-b contains it only under that additional hypothesis.

**Plain English.**
- TS-a: every true predictor whose signal the other predictors cannot imitate ends up with inclusion probability near one.
- TS-b: the posterior concentrates on the exact true model. The highest-probability and median-probability models both equal the true model with probability tending to one, and every inclusion probability is near 1 for true predictors and near 0 for nulls.
- The condition for TS-b: leaving out any group of true predictors must leave more unexplained signal than twice what the prior and the Occam factor charge for those predictors, with a little room to spare. When nulls stand in for the missing predictors, each null must also pay for how much of the missing signal it can explain: its "leakage". A null that explains none of it pays nothing extra; one that explains all of it pays at most the cost of the best-looking null among p, about √(2m log p) on the root scale. A small group of close proxies may be listed in advance and charged the deletion price instead.
- If the unexplained signal is below twice that charge (and the design is not nearly collinear on the true model, A-NEC), the posterior drops the true model (converse target), so the factor 2 cannot be improved.
- Up to constants, comparable limits hold in the Gaussian ensembles and asymptotic regimes of Wainwright (2009) and Fletcher, Rangan & Goyal (2009); FRG's constant is derived in a growing-sparsity regime and does not calibrate our fixed-s coded price.

### 4.3 TM: consistency under misspecification (SL Theorem 4, Corollary 2)
**Setting.** The method is run on the response and a candidate set C ⊂ [p] that may omit true predictors (SL's subset data D_n^s). C must be fixed before the analysis sample is seen or chosen on independent data; all TM statements are **conditional on each admissible C**, with the candidate dimension p_C in the cap, price, window and prior. The pseudo-true parameters (centred version of SL (17)/(19) and SLs (6), p. 6) are:

- β^C = Σ_CC⁻¹ Cov(x_C, y) and α_C = E y − E x_Cᵀβ^C;
- σ_C² = E(y − α_C − x_Cᵀβ^C)², S0^C = supp β^C, s_C = |S0^C|;
- f₀ = φ(y; α_C + x_Cᵀβ^C, σ_C) ν(x_C);
- the working residual u := y − α_C − x_Cᵀβ^C.

**TM-a0, literal counterpart of SL Thm 4 [TARGET, low risk].** Fix **one** i.i.d. law (not an n-dependent truth: with β_n = 1/n even fixed-p support selection fails) along a nested sample sequence. Let the candidate dimension p_C ≥ 2 be fixed (the coded posterior is undefined with fewer than two retained predictors; with n ≥ 2p_C the cap is K = p_C), E‖x_C‖² < ∞, E y² < ∞, σ_C² > 0, Σ_CC nonsingular, the coded fixed BB(1, p_C) prior (so π(S) > 0 for all S ⊆ C; arbitrary n-dependent positive masses are not allowed), and work in raw units with the coded centring (plug-in ȳ, x̄; no intercept parameter with a prior; Z = (1, x_Cᵀ)ᵀ; draws mapped back as in §1). Data sets with a constant sample column or response are in the exceptional event, which is eventually empty a.s. Then Π(d_H(f, f₀) > ε | D_n^C) → 0 almost surely for every ε > 0. If also E[Z_j² u²] < ∞ for all coordinates of Z (a mixed second moment of the scores, not fourth moments of x and y), then π(S0^C | D_n^C) → 1 almost surely. This is exact selection, stronger than SL Cor 2's inclusion. TM-a0 lies outside A-GL.

**TM-a0-inc, inclusion of the pseudo-true support [TARGET, low risk; the direct counterpart of SL Cor 2].** Under the TM-a0 setting with A-MOM's second moments only (E‖x_C‖² < ∞, E y² < ∞, σ_C² > 0, Σ_CC nonsingular), Π(S ⊇ S0^C | D_n^C) → 1 almost surely. Proof path: full rank and finitely many underfits give a positive population risk gap, which the SLLN transfers against the O(log n) Occam cost. The score moments E[Z_j²u²] < ∞ enter only for exclusion (TM-a0's exact selection). For discrete y, f₀ is defined by expected Gaussian log score.

Proof path (Fable Q6(3a), fixes by Astra R2 Q4): there are 2^{p_C} models; the SLLN applies to RSS_S/n; ‖Σ Z_i u_i‖ = O_a.s.(√(n log log n)) (LIL) makes the extra-variable gains O_a.s.(log log n), against (m/2) log n. The argument is direct and avoids De Blasi–Walker.

**TM-a, density consistency to f₀ [TARGET, low–medium risk; a corollary of TD for each admissible C].** Assume A-MIS(iii): u is independent of x_C and u ~ N(0, σ_C²). In primitive form: for the omitted true predictors O, x_Oᵀβ*_O = a + x_Cᵀγ + e with e ~ N(0, τ²) independent of x_C, τ² ≥ 0, so β^C = β*_C + γ and σ_C² = σ*² + τ² (equivalent by Cramér's decomposition). Assume also A-SPARSE-C (|supp β^C| ≤ s_C fixed), A-DIM, A-SUBG, A-NEC and A-BS for the candidate problem (x_C, β^C, σ_C²). Then for M ≥ M₀, in TD's M-window,

  P*[ Π( d_H(f, f₀) > √(M log n / n) | D_n^C ) > n^{−c M} ] ≤ n^{−c M}  (the a.s. corollary, for posterior tails, if c·M > 1).

An unconditional statement (over a data-dependent C) needs common constants and a common validity threshold over admissible candidate sets, and then adds + P(C inadmissible), which vanishes identically under almost-sure admissibility; the a.s. corollary needs summable exception probabilities.

**TM-b, selection of the pseudo-true support [TARGET, margin form; a corollary of TS-b for each admissible C].** Assume A-MIS(iii), A-SPARSE-C and the TS-b assumptions for the candidate problem, with A-MARGIN-U written in σ_C² units on μ_C = X_Cβ^C, and assume a nonempty pseudo-support S0^C := supp β^C ≠ ∅ (the forward steps would also go through with S0^C = ∅, where the deletion and mixed classes are empty, but that case is not claimed; the converse needs S0^C ≠ ∅). Then 1 − π(S0^C | D_n^C) has the TS-b in-probability rate (the delivered `thm:omitted` gives an expectation bound, which TM-b does not reproduce), and P(HPM = MPM = S0^C) → 1. In particular, as SL Cor 2's prose claims:
- a true predictor in C is selected iff β^C_j ≠ 0;
- proxies of omitted predictors (β*_j = 0 but β^C_j ≠ 0) are selected;
- cancelled true predictors (β*_j ≠ 0 but β^C_j = 0) are dropped.

**Previously delivered analogue (`thm:omitted`, supplement_or `asm:omitted` from l.126).** The assumptions are:
- Gaussian candidate rows and a Gaussian linear homoscedastic working residual (automatic when (x_C, x_omitted) are jointly Gaussian);
- A-DIM, with s_C fixed;
- a floor on sets of size 3(A+1)(s_C+1) log n and bounded projected signal;
- n·min_j Σ_jj(β^C_j)²/(σ_C² log n) → ∞.

The conclusions are E[1 − π(S0^C | y)] = O(√(log n/n)) and P(HPM ≠ S0^C) = O(√(log n/n)). Status (main): "Proved and independently checked."

**Not targeted, stated as remarks with their reason:**
- **(i′)** For an independent but non-Gaussian sub-Gaussian residual, a suggested **sufficient** set (not shown necessary) is a model-size cap K_n ≤ c·n log n/(log p)² and a variance-proxy budget ϱ̄ ≤ 1 + (1−ε)·log n/(2 log p). The reason is that the Fubini size tail fails under misspecification. The code uses K = n/2, so this would need an Engineering decision.
- **(ii)** For a heteroscedastic residual, a variance-proxy/union heuristic suggests selection survives when (ϱ̄ − 1)·log p < ½·log n and can fail otherwise. This is a heuristic budget, not an iff and not a theorem; it is the mechanism suggested for Grünwald & van Ommen's failure examples in our model.

**Plain English.** If some true predictors are missing from the data, the method cannot find them. What it does find is the best approximation available:
- the posterior predictive law converges to the closest Gaussian linear law built from the available predictors (SL's f₀);
- the noise variance absorbs the unexplained part;
- the selected model is exactly the set of available predictors that the best linear predictor uses, including proxies that stand in for missing predictors.

In high dimension this is guaranteed when the leftover error behaves like independent Gaussian noise. When it does not (for example, the error variance depends on x), our heuristic calculation suggests that selection can fail once p is large enough, which is the effect Grünwald & van Ommen document.

---

## 5. What moves if Engineering changes the method (summary; details in ASSUMPTIONS_AND_PROOF_PATHS.md §5)
**Engine decision (HQ, SMC-PERF closed, memo 1b319090).** v3.1.1, g = n, truncated BB(1, p) and MPM are confirmed. Fix E (output-only) and C1 (compute-only) do not touch the theorems. Proof writing and Lean stay on hold. The sensitivity notes below are therefore contingency notes only.

Both advisors independently reached the corrections below, which supersede TH_PREP §3 on the size prior.

- **Invariant in form.** All statements concern "the posterior of the coded prior", so their form survives any change of g, of the size prior BB(1, b), of any fixed cap K ≥ s0, of the σ² prior IG(a₀, b₀), or of a reporting rule that is a fixed function of the PIPs. This is about the form of the statements only: price and prior algebra may transfer, but the conclusions need re-checking, since a fixed g can prevent selection and model-space changes can alter the result (Sol R2).
- **Margin threshold moves with the price.** With slab scale g, price_g(k) = log[(2p−1−k)/(k+1)] + ½ log(1+g).
  - The TS-b threshold 2·Pr_n moves with this price: changing g = n to c·n shifts the price by ½ log[(1+cn)/(1+n)] at fixed k. Heuristically the superset mass scales as (s0+1)·√(log p/g), suggesting s0² log p = o(g). A small g also enlarges the slab loss O(n/g), so the nominal price alone does not describe the change (Astra R2).
  - g = max(n, p²): when p² ≥ n the price is ≈ 2 log p at fixed small k and growing p, so more signal is needed but the superset mass is smaller (a power-for-robustness trade); when p² < n, g = n and nothing changes.
  - A fixed (data-free) g can prevent selection.
- **BB(1, p^u), u < 1.** The per-variable prior odds stay ≈ (k+1)/p, so the price changes by at most log 2. What is lost is the geometric 2^{−k} size tail: the size ratio becomes ≈ 1 − p^{u−1}.
  - Consequence: the Fubini size bound is lost; a size cap (Fable's union route suggests K_n ≤ c·n·log n/(log p)², sufficient, not shown necessary) restores a size tail. Sound for fixed small k (Astra R2).
  - TH_PREP's "(1−u)A < ½" condition belongs to an independent Bernoulli(p^{−u}) prior, not to BB(1, p^u).
  - For u > 1 the price rises by (u−1) log p, the size tail becomes p^{−(u−1)k}, and no new condition is needed.
- **Reporting rule.** HPM = S0 once 1 − π(S0 | y) < ½. MPM with threshold q returns S0 once max_j |PIP_j − 1{j∈S0}| < min(q, 1−q). A marginal PIP threshold has no universal single-model log-score shift.
- **Cap K.** Any fixed cap K ≥ s0 preserves S0 and only removes competitors; K ≥ s0 + m (m the number of added nulls) is not necessary (Astra R2). A cap K_n ≤ c·n/log p fixes the isometry step for log p = o(n) (A-DIM″), not the testing step.
- **Ridge and floor.** The vanishing floor c_ψ/n in A-NEC is set by the unit ridge in the slab, not by g.
- **Route-breaking.** A data-free slab V = τ²I, or no scaling, breaks the proofs' reliance on today's coded score (n(G+I)⁻¹, the data-scaled σ² rate), so TD, TS-b and TM-a/b would need re-derivation for the new implementation; it cannot break the conditional data-law identity in A-MIS(iii).
