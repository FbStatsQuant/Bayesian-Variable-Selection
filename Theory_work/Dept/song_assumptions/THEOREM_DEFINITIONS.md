# THEOREM DEFINITIONS — Song & Liang (2015) ↔ SMC-BVS, and our target theorems

Theory Department, mission TH-SONG-ASSUMPTIONS, 2026-11-27. Task Lead: Opus 5.5. **v1.3 (council round-2 revision; after advisor rounds Astra 6.2 R1–R2, Fable 5.2 R1; SL citation audit: Sol 6.2; data: D1; literature: C2). See COUNCIL_RECORD.md.**
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
| σ² | IG(0.01, 0.01) | IG(a₀,b₀), SL use a₀ = b₀ = 1 (p. 960) |
| model prior | BB(1,p): π(S) ∝ ½/C(2p−1,\|S\|) on Ω = {\|S\| ≤ K}, K = min(p, ⌊n/2⌋) | SL (6), p. 951: independent Bernoulli(r_n/P_n) truncated at r̄_n, with r_n/P_n → 0; the choice r_n = P_n^{1−γ} (γ = 0.75 by default) is made separately (EBIC comparison p. 952; default p. 960); stage 1 uses λ_s = \|s\|^{−γ} (pp. 959–960) |
| report | MPM (PIP > ½); HPM stored | SL: PIP thresholding ξ_q = {j : q_j > q} with q from an FDR procedure (p. 956), or MAP (p. 959) |
| algorithm | SMC with frozen tempering (DEFERRED results) | SAMC (SLs §2) |

Two consequences used throughout. (i) The per-variable cost of adding a predictor to a size-k model is
**price(k) = log[(2p−1−k)/(k+1)] + ½ log(n+1)** (prior + Occam), ≈ log(2p/s0) + ½ log n near the truth; on S1/S2 this is
7.6–10.4 nats (P1 convention, D1 tables). (ii) The size marginal of BB(1,p) decays like 2^{−k} while each model carries a p^{−k}-type multiplicity
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
| SL-1, SL-2 (Hellinger consistency) | **TD** (§4.1) = delivered `thm:dist` | Same metric, up to SL's factor √2: Hellinger distance between joint densities, x from its true law. Same exponential form, with exp(−c·nε²) = n^{−cM} inside the window ε² = M log n/n, M ≤ √n/log n. We allow K = n/2, where SL's (9)–(10) would fail at r̄_n ≍ n, and we need no beta-min and no fixed eigenvalue floor. SL allow stretched-exponential P_n | delivered: "Proved and independently checked. Registry row 2.1." **[TARGET] TD′** (dimension-relaxed) and **TD-as** (almost sure) |
| SL-1's approximate sparsity (3) | **TD-A** (optional corollary) | Change of measure to a sparse surrogate (Fable Q7). Not an owner target | optional [TARGET], low priority |
| SL-3 (Cor 1 rates) | TD / TD′ radius (**partial analogue**) | Different prior, sparsity/cap and rate trade-off. Ours is √(M log(p∨n)/n). TD′'s dimension envelope would overlap SL Cor 1 for α < ½ without recovering the corollary in full, and its proof route is open (high risk, Astra R2). For α ∈ [½, 1) the *current route* would also need a model-size cap c·n/log p for isometry; a cap does not fix the testing step; this is a statement about our route, not about all proofs | delivered for p ≤ n^A; TD′ conjecture, high risk |
| SL-4 (Condition 2: second moments only) | **TM-a0** (moments-only, fixed dimension; **partial analogue**) | SL-4 weakens tails while keeping growing dimension and the other Thm 2 premises; TM-a0 matches the moments only at fixed dimension. For growing p our exact-marginal route needs exponential tails on sparse sets, so Condition 2 is not targeted there | non-target with reason (Astra Q7, Fable Q7) |
| SL-5 (Thm 3 sure screening) | **TS-a** (§4.2) | Same route: a Hellinger separation for every model that omits x_j, combined with contraction. SL Condition 3's role (residual identifiability) is taken by A-MARGIN-H, a lower bound on R; A-SUBG only converts R into Hellinger separation, d_H² ≥ c_L·min{1, R/(nσ²)} (it does **not** imply Condition 3: Gaussian duplicates have R = 0; Astra R2 Q4). SL's thresholded-PIP consequence needs a threshold kept away from one or a rate comparison with the omitted posterior mass; SL's FDR threshold discussion (p. 956) is separate from the fixed-q consequence | **[TARGET]**, low risk |
| SL-6, SL-7 (Thm S, Cor S1: MAP) | **TS-b** (§4.2); previously delivered analogues `thm:post-random`, `thm:post-fixed`, `thm:post-margin` | Our conclusion is stronger: π(S0 \| y) → 1 with a rate, HPM = MPM = S0, and every PIP within the rate (SL give pairwise odds only, with no rate). SL's sample eigen-structure (22) is replaced by a vanishing population floor used together with A-SUBG; SL's (26) is a two-sided sample condition with a vanishing lower threshold l_n ≫ r̄_n log P_n/n and a growing upper threshold, on sets of size r̄_n + |t|; where the regimes overlap c_ψ/n lies below l_n, but the objects, normalisations and windows differ, so this is not a uniform dominance (and NH14's p_n^{−κ} floor can be smaller than c_ψ/n at large p). A converse (under A-NEC on T) is added | delivered (fixed signals, fixed floor): "proved and independently checked" (previously delivered analogues). **[TARGET] TS-b** (margin form; S1 boundary signals: deletion part bracketed by data, mixed part: an E9/E9b zero-slack diagnostic for d ≤ 3, m = 1 and m = 2 at p = 500; m ≥ 3 not evaluated) |
| SL-8 (Thm 4: misspecified density consistency) | **TM-a0** (fixed candidate dimension, a.s.; a partial analogue with added score moments); **TM-a** (high-dimensional candidates, with rate) | Both concentrate on the KL projection f₀ of SL (17)/(19). SL Thm 4 assumes a fixed candidate subset, Condition 4, a Gaussian parent model and positive priors; it does not invoke global strict sparsity (4). SLs Lemma 1.2 (= De Blasi–Walker Cor 1) is the tool SL use | **[TARGET]**; TM-a0 low risk, TM-a low–medium |
| SL-9 (Cor 2: inclusion of the pseudo-true support) | **TM-b**; delivered special case `thm:omitted` | Our conclusion is stronger: exact selection of S0^C = supp β^C, which SL's prose claims but their inclusion-only display does not give | delivered: "Proved and independently checked". **[TARGET] TM-b** (margin form) |
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

- **Residual signal.** R_n(S) := n·inf_{a,b} E(xᵀβ* − a − x_Sᵀb)². This is n times the linear-projection risk of the true signal on x_S. For Gaussian x it equals n·β*_Dᵀ Σ_{DD·S} β*_D. Its sample twin is R̂(S) = ‖(I − P_S)Xβ*‖² (centred X).
- **Price of a rival.**
  Pr_n(d, m) := log[C(2p−1, s0)/C(2p−1, s0−d+m)] + ((d−m)/2)·log(n+1), and Pr_n(d) := Pr_n(d, 0) = Σ_{k=s0−d}^{s0−1} price(k).
  This is the prior × Occam log-cost of S relative to S0 (Fable notation; Astra's B_Dm is the same object).
- **Margin ratio.** κ_n := min_{∅≠D⊆S0} R_n(S0∖D) / (2σ*²·Pr_n(|D|)).
- **Posterior and densities.** Π(· | D_n) is the exact posterior of (S, β, σ²) in §1. A posterior draw defines the conditional law N(ȳ + (x − x̄)ᵀβ, σ²) of y | x. f is the joint density with respect to ν(dx)dy, ν the true law of x (so discrete predictors are covered; Sol R2), f* is the true joint density, and d_H(f, f*)² = 1 − ∫√(f f*).

Assumption labels refer to `ASSUMPTIONS_AND_PROOF_PATHS.md` §2.

### 4.1 TD: true-distribution consistency (SL Theorems 1–2, Corollary 1)
**Mathematical statement (delivered form, `thm:dist`).** Assume A-GL, A-SPARSE, A-DIM, A-SUBG, A-NEC and A-BS. There are constants c_H > 0, M₀ and n₀, depending only on (s, A, L, c_ψ, b̄), such that for every M ≥ M₀ and every n ≥ n₀ with √n/log n ≥ M,

  P*[ Π( d_H(f, f*) > √(M log n / n) | D_n ) > n^{−c_H M} ] ≤ n^{−c_H M}.

The delivered assumption set includes a level-dependent size window q_n(M) on which A-SUBG and A-NEC are imposed (or6 `asm:dist`).

**TD-as [TARGET, low risk].** Fix the truth as a sequence (all D_n on a common probability space) and choose M ≥ M₀ with c_H·M > 1. Then
Π(d_H(f, f*) > √(M log n/n) | D_n) → 0 P*-almost surely. Proof path: Borel–Cantelli on the display above, since
Σ_n n^{−c_H M} < ∞. This is the counterpart of SL's almost-sure mode in Thm 4.

**TD′ [conjecture, HIGH proof risk at the proposed rate].** Replace A-DIM by A-DIM′, (s+1)·M·log p·log(p∨n) ≤ c_dim·n (headline form: (log p)² = o(n) for fixed s and M; a sufficient isometry budget only). Conjectured statement (exact, Sol R2): keep 2 ≤ p and the coded input domain with its exceptional event, and impose A-SUBG and A-NEC on the enlarged window q_n = min{p, ⌈C′(s+1)M log(p∨n)⌉}. Then there are c > 0 and M₀ such that for every M ≥ M₀ with M log(p∨n) ≤ c√n and ε_n² = M log(p∨n)/n,

  P*[ Π( d_H(f, f*) > ε_n | D_n ) > exp(−cM log(p∨n)) ] ≤ exp(−cM log(p∨n)).

- Fable's route: the Fubini size-tail identity gives a coarse size cutoff q_n ≍ (s+1)·M·log₂(p√n), and A-DIM′ gives sample isometry on q_n-sets.
- **The route fails at the testing step** (Astra R2 Q1). At fixed s, M and log p = n^{1/3}, A-DIM′ holds and q_n ≍ L, but the entropy log C(p, q_n) ≍ n^{2/3} exceeds the testing budget nε_n² = M·L ≍ n^{1/3}. The delivered thm:dist also localises to s0 + O(t/log n) by fractional Bayes-factor moments, whose factor p^{1−λ}n^{−λ/2} is not controlled for superpolynomial p.
- A proof needs localisation at a testing-compatible size (≈ t/log p) or a direct prior-weighted predictive bound. A cap of order n/log p fixes the isometry inequality, not the testing inequality. No impossibility follows from the failed route.
- Hence TD′ is a conjecture with high proof risk, and every released statement stays at p ≤ n^A.

**TD-A [optional TARGET].** Approximate sparsity in the spirit of SL (3): if the centred tail r(x) = Σ_{j∉S_n} β*_j (x_j − Ex_j) has sub-Gaussian variance **proxy** ≤ c₀σ*²M log n/n (a small ordinary variance with an unspecified sub-Gaussian norm does not control E exp(r²/σ²); Sol R2), then TD should hold with f* replaced by its s-sparse surrogate. One-observation Hellinger closeness is not enough: the proof needs a full-data change of measure, E_sur[(dP*/dP_sur)²] = (E exp(r²/σ²))^n ≤ exp(O(c₀t)), with Cauchy–Schwarz on exceptional events, c₀ small, and the intercept/mean accounted for (Astra R2 Q5).

**Plain English.** With probability close to one, the posterior puts almost no weight on regression laws whose predictive distribution of y given a new x differs from the truth by more than about √(log n / n) in Hellinger distance. That is the parametric rate up to a logarithmic factor, within the delivered tuning window (M ≥ M₀, p ≤ n^A). No signal-strength (beta-min) condition is needed, because weak predictors that cannot be selected also cannot move the predictive law much. TD′ asks whether the same holds when p grows faster than any power of n; that is open, and our best route fails.

### 4.2 TS: true-model (selection) consistency (SL Theorem 3, Theorem S, Corollary S1)
**TS-a, sure screening [TARGET, low risk].** Assume the TD assumptions and A-MARGIN-H (on the effective sieve, council R1): for each j ∈ S0,
inf{ R_n(S) : j ∉ S, |S| ≤ min(K, J) } ≥ C_H(L)·M·σ*²·log n, J := ⌊s + C_s M⌋ (prop:dist(i)). Then for every fixed c′_H < c_H, large n and every j ∈ S0,

  P*[ Π( j ∈ S | D_n ) < 1 − n^{−c′_H M} ] ≤ n^{−c_H M}, hence min_{j∈S0} PIP_j → 1 in probability (almost surely, for posterior tails, if c′_H M > 1).

The constant C_H is inexplicit (it comes from the contraction constants), so TS-a is the per-predictor counterpart of SL Thm 3 and makes no claim at boundary signal levels.

**TS-b, exact selection [TARGET, margin form, low–medium risk].** Assume A-GL, A-SPARSE, A-DIM, A-SUBG, A-NEC, A-BS and A-MARGIN-U (Astra R2 form), defined as follows. Fix an admissible M independently of n and let J := ⌊s + C_s·M⌋ (the bounded-size event of prop:dist(i)). There are fixed 0 < δ < 1, γ > 0 and t_n → ∞ (t_n ≤ a small fraction of the surplus) such that, for all large n and every nonempty rival class (D, m) with D ≠ ∅, m ≤ J and **B_Dm > 0**,

  √( (1−δ)·min_{|N|=m} R_n(S)/σ*² ) ≥ w_Dm + t_n + √( 2(1+δ)·B_Dm ),   B_Dm := Pr_n(d) − (m/2)·log(n/(C·log p)) + γ log n,

where C is a fixed constant for which the superset step's containing-model bound holds with a tight multiplier (ASSUMPTIONS §3.3 step 2). At S1's sizes the implied C ≍ (s0+1)² makes the credit ≈ 0, so the cap on active m is asymptotic (Opus R2). Classes with B_Dm ≤ 0 need no signal condition (containing-model credit; council R1). Here w_Dm is the one-sided conditional Gaussian width of the m added nulls, w_Dm = E_g max_{|N|=m}(−⟨v_S, g⟩) with v_S the normalised residual direction (I−P_S)μ/‖(I−P_S)μ‖: w_D0 = 0, and one may use the worst case over D, a deterministic bound holding with design probability 1 − o(1), or w_Dm ≤ √(2 log C(p−s0, m)) ≈ √(2m log p) outright. The condition is stated on a design event of probability 1 − o(1), since w_Dm(X) is conditional on the design. The combinatorial width and the squared form R_n(S) ≥ 2(1+η)²(√d+√m)²σ*²·price_n are worst-case (factor-proxy) forms and do **not** cover S1 at SNR 2; on S1's AR(1) designs the estimated width is 0.1–0.6 (E9), and the estimated zero-slack surplus is positive for every evaluated class (d ≤ 3; m = 1, and m = 2 at p = 500; ≥ 2.39 at SNR 2 even without containing-model credit, E9b). m = 2 at p = 5,000 and m ≥ 3 are not evaluated, and E9 does not test the positive-slack inequality or its design-event quantifier. Then

  1 − π(S0 | D_n) = O_P( (s0+1)·√(log p/n) + n^{−γ} + n^{−c_H M} ),  P(HPM = MPM = S0) → 1,
  max_j |PIP_j − 1{j ∈ S0}| ≤ 1 − π(S0 | D_n).

- For pure deletions (m = 0), A-MARGIN-U is implied by liminf κ_n > 1 for *some* small δ, γ > 0 (since Pr_n ≳ log n); it does not imply a prescribed γ. Every nonempty D ⊆ S0 counts, not only singletons: multi-deletions bind on S1.
- Models larger than J are handled by the size lemma prop:dist(i), which is proved under A-BS; that is why TS-b keeps A-BS (A-BS′ needs the lemma extended first). Proof obligation: at fixed M the superset/mixed classes form a finite union over m ≤ J (ASSUMPTIONS §3.3 step 2); the truncated-Beta bound with its constants and the coded-likelihood mixed-class bound (step 3) remain to be written out.
- p is the raw dimension, on the event that all columns survive centring (singleton isometry gives this event with probability → 1; Sol R2).

**TS-b converse [TARGET, low risk].** Under the same regularity **with A-NEC on T** (two-sided determinant refund d·log(n+1)/2 + O(1); a one-sided refund bound cannot prove the converse), but without the forward margin:
- if limsup κ_n < 1, then π(S0 | D_n) → 0 in probability;
- if √R_n(S0∖{j})/σ* − √(2·price_n) → c ∈ ℝ, then liminf P(π(S0 | D_n) ≤ ½) ≥ Φ(−c) > 0. Equality would need control of all other odds (Astra R2 Q3).

The constant 2 is therefore sharp for deletions. S1 is consistent with this: κ_pop 0.64–0.70 (0/100 exact) at SNR 1 and 2.54–2.80 (92–96/100) at SNR 2 (SIMULATION_DATA_ANALYSIS item 2, E1; restricted data proxy, while the exact all-deletion κ_n is 0.626–0.693 and 2.505–2.771, Sol R2); the transition is bracketed, not located.

**MARGIN\* (open refinement; not a defined target, council R1).** Fable's MARGIN\* would replace the width allowance by (M1) constant 2 + η on rivals inside a leakage set Q_n ⊇ S0 with log|Q_n| = o(log(p∨n)), and (M2) bounded leakage ϑ_n outside Q_n. It has no testable statement yet (M1's inequality and domain, M2's bound R_n(B∪N) ≥ (1−ϑ_n)R_n(B) with quantified B, N and ϑ_n, a cutoff tied to the sieve, and a conclusion are all still to be fixed), and its key lemma is a conjecture (ASSUMPTIONS §6 item 2).

It would matter only if a referee asks why proxy swaps cost up to √(2m log p). A factor-proxy design (Fable Q1(3c)) shows the width term is needed at one (d, m); this is not optimality of every constant in A-MARGIN-U.

**Rejected:** the uniform "constant 2 for every rival" margin of DESIGN_MEMO_R0. Fable Q1(3d) gives a counterexample for a fixed number m of added nulls when log n = o(log p). The question is OPEN under p ≤ n^A, and it is recorded as a conjecture only.

**Finite-n diagnostic (not a target; withdrawn as a proposition per Astra R2 Q3).** In the idealised χ² score approximation the expected number of one-null extensions beating S0 is E K₁ ≈ (s0+1)/√(2πL(n+1)), L = 2 log((2p−s0−1)/(s0+1)) + log(n+1); this is 0.031–0.050 at S1's (n, p) (0.033–0.056 under Fable's exact-Beta tail). It is a mode-type diagnostic (rivals beating S0 in exact score, an HPM event; MPM failure is separate; Sol R2), a factor ≍ L below the posterior-mass rate term, which is 0.87–1.44 and so not informative at S1's sizes. It is consistent with the S1 shortfall at SNR ≥ 2 (2–8%, 40/41 failures supersets), but P(K₁ ≥ 1) ≤ E K₁ bounds one failure type only and gives no ceiling or lower bound on success (correlated nulls, swaps, higher-order rivals, ridge/IG terms and HPM/MPM/sampler differences are uncontrolled).

**Delivered special case (`thm:post-random`).** Assume A-GL, A-DIM, A-SPARSE, SGR, FSb (fixed b_lo ≤ |β*_j| ≤ b_hi) and EFS (a fixed population floor on sets of size ≤ 5(A+1)(s0+1) log n). Then 1 − π(S0 | y) = O_P(√(log n/n)), P(HPM = MPM = S0) → 1 and max_j |PIP_j − 1{j∈S0}| = O_P(√(log n/n)). Status: "proved and independently checked" (or6 l.83–85). This is a **previously delivered analogue**, not a strict special case: FSb gives R_n(S) ≥ c·n for every rival with m ≤ J, so A-MARGIN-U holds for large n, but EFS on its window does not imply A-NEC on the possibly wider TD window, so TS-b contains it only under that additional hypothesis.

**Plain English.**
- TS-a: every true predictor whose signal the other predictors cannot imitate ends up with inclusion probability near one.
- TS-b: the posterior concentrates on the exact true model. The highest-probability and median-probability models both equal the true model with probability tending to one, and every inclusion probability is near 1 for true predictors and near 0 for nulls.
- The condition for TS-b: leaving out any group of true predictors must leave more unexplained signal than twice what the prior and the Occam factor charge for those predictors, with a little room to spare. When nulls are added in their place, there is an extra allowance for the best-looking nulls among p; this allowance is at most about √(2m log p) and much smaller on typical designs (0.1–0.6 on S1). Rivals whose prior-plus-Occam saving from the added nulls already exceeds the deletion price need no condition at all.
- If the unexplained signal is below twice that charge (and the design is not nearly collinear on the true model, A-NEC), the posterior drops the true model (converse target), so the factor 2 cannot be improved.
- Up to constants, comparable limits hold in the Gaussian ensembles and asymptotic regimes of Wainwright (2009) and Fletcher, Rangan & Goyal (2009); FRG's constant is derived in a growing-sparsity regime and does not calibrate our fixed-s coded price.

### 4.3 TM: consistency under misspecification (SL Theorem 4, Corollary 2)
**Setting.** The method is run on the response and a candidate set C ⊂ [p] that may omit true predictors (SL's subset data D_n^s). C must be fixed in advance or chosen on independent data. The pseudo-true parameters (centred version of SL (17)/(19) and SLs (6), p. 6) are:

- β^C = Σ_CC⁻¹ Cov(x_C, y) and α_C = E y − E x_Cᵀβ^C;
- σ_C² = E(y − α_C − x_Cᵀβ^C)², S0^C = supp β^C, s_C = |S0^C|;
- f₀ = φ(y; α_C + x_Cᵀβ^C, σ_C) ν(x_C);
- the working residual u := y − α_C − x_Cᵀβ^C.

**TM-a0, literal counterpart of SL Thm 4 [TARGET, low risk].** Fix **one** i.i.d. law (not an n-dependent truth: with β_n = 1/n even fixed-p support selection fails) along a nested sample sequence. Let the candidate dimension p_C ≥ 2 be fixed (the coded posterior is undefined with fewer than two retained predictors; with n ≥ 2p_C the cap is K = p_C), E‖x_C‖² < ∞, E y² < ∞, σ_C² > 0, Σ_CC nonsingular, the coded fixed BB(1, p_C) prior (so π(S) > 0 for all S ⊆ C; arbitrary n-dependent positive masses are not allowed), and work in raw units with the coded centring (plug-in ȳ, x̄; no intercept parameter with a prior; Z = (1, x_Cᵀ)ᵀ; draws mapped back as in §1). Data sets with a constant sample column or response are in the exceptional event, which is eventually empty a.s. Then Π(d_H(f, f₀) > ε | D_n^C) → 0 almost surely for every ε > 0. If also E[Z_j² u²] < ∞ for all coordinates of Z (a mixed second moment of the scores, not fourth moments of x and y), then π(S0^C | D_n^C) → 1 almost surely. This is exact selection, stronger than SL Cor 2's inclusion. TM-a0 lies outside A-GL. For discrete y, f₀ is defined by expected Gaussian log score.

Proof path (Fable Q6(3a), fixes by Astra R2 Q4): there are 2^{p_C} models; the SLLN applies to RSS_S/n; ‖Σ Z_i u_i‖ = O_a.s.(√(n log log n)) (LIL) makes the extra-variable gains O_a.s.(log log n), against (m/2) log n. The argument is direct and avoids De Blasi–Walker.

**TM-a, density consistency to f₀ [TARGET, low–medium risk].** Assume A-MIS(iii): u is independent of x_C and u ~ N(0, σ_C²). Assume also A-SPARSE, A-DIM, A-SUBG, A-NEC and A-BS for the candidate problem (x_C, β^C, σ_C²). Then for M ≥ M₀, in TD's M-window,

  P*[ Π( d_H(f, f₀) > √(M log n / n) | D_n^C ) > n^{−c M} ] ≤ n^{−c M}  (the a.s. corollary, for posterior tails, if c·M > 1).

**TM-b, selection of the pseudo-true support [TARGET, margin form].** Assume A-MIS(iii) and the TS-b assumptions for the candidate problem, with A-MARGIN-U written in σ_C² units on μ_C = X_Cβ^C, and assume a nonempty pseudo-support S0^C := supp β^C ≠ ∅ (the forward steps would also go through with S0^C = ∅, where the deletion and mixed classes are empty, but that case is not claimed; the converse needs S0^C ≠ ∅). Then 1 − π(S0^C | D_n^C) has the TS-b in-probability rate (the delivered `thm:omitted` gives an expectation bound, which TM-b does not reproduce), and P(HPM = MPM = S0^C) → 1. In particular, as SL Cor 2's prose claims:
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
