# THEOREM DEFINITIONS — Song & Liang (2015) ↔ SMC-BVS, and our target theorems

Theory Department, mission TH-SONG-ASSUMPTIONS, 2026-11-27. Task Lead: Opus 5.5. **Draft v1 (after advisor round 1: Astra 6.2, Fable 5.2; SL citation audit: Sol 6.2; data: D1; literature: C2).**
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
| data | X, y centred and scaled (column SD 1, divisor n−1); no intercept parameter | SL Thm 1 standardises and bounds predictors (p. 952) |
| slab | β_S \| S, σ² ~ N(0, nσ²(X_SᵀX_S + I)⁻¹): g = n with unit ridge | same family as SL's SAM prior with precision V_ξ⁻¹ = (X_ξᵀX_ξ + τI)/n (explicit precision on SLs p. 16; SL p. 959 prints it in the covariance slot, an apparent inversion typo given the covariance convention σ²V_ξ of SL p. 951); τ = 0.01 in SL (p. 960) vs τ = 1 here. Theorem S itself is stated for the unregularised precisions I and XᵀX/n; the ridge variant is asserted in the paragraph before Cor S1 (SLs p. 16) via a "Lemma A.2 of the Appendix" that is not in the 20-page supplement |
| σ² | IG(0.01, 0.01) | IG(a₀,b₀), SL use a₀ = b₀ = 1 (p. 960) |
| model prior | BB(1,p): π(S) ∝ ½/C(2p−1,\|S\|) on Ω = {\|S\| ≤ K}, K = min(p, ⌊n/2⌋) | SL (6), p. 951: independent Bernoulli(r_n/P_n) truncated at r̄_n, with r_n/P_n → 0; the choice r_n = P_n^{1−γ} (γ = 0.75 by default) is made separately (EBIC comparison p. 952; default p. 960); stage 1 uses λ_s = \|s\|^{−γ} (pp. 959–960) |
| report | MPM (PIP > ½); HPM stored | SL: PIP thresholding ξ_q = {j : q_j > q} with q from an FDR procedure (p. 956), or MAP (p. 959) |
| algorithm | SMC with frozen tempering (DEFERRED results) | SAMC (SLs §2) |

Two consequences used throughout. (i) The per-variable cost of adding a predictor to a size-k model is
**price(k) = log[(2p−1−k)/(k+1)] + ½ log(n+1)** (prior + Occam), ≈ log(2p/s0) + ½ log n near the truth; on S1/S2 this is
7.5–10 nats. (ii) The size marginal of BB(1,p) decays like 2^{−k} while each model carries a p^{−k}-type multiplicity
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
| SL-0 (posterior (7), EBIC link) | the coded marginal posterior; price(k) (§1) | at small k our per-variable price is log(2p/k) + ½ log(n+1) ≈ EBIC_γ with γ ≈ 1. The EBIC consistency threshold for fixed s0, γ > 1 − 1/(2A) at p = n^A (Luo & Chen arXiv v1 p. 7, attributed to Chen & Chen 2008), is met | context only |
| SL-1, SL-2 (Hellinger consistency) | **TD** (§4.1) = delivered `thm:dist` | Same metric, up to SL's factor √2: Hellinger distance between joint densities, x from its true law. Same exponential form, with exp(−c·nε²) = n^{−cM} inside the window ε² = M log n/n, M ≤ √n/log n. We allow K = n/2, where SL's (9)–(10) would fail at r̄_n ≍ n, and we need no beta-min and no fixed eigenvalue floor. SL allow stretched-exponential P_n | delivered: "Proved and independently checked. Registry row 2.1." **[TARGET] TD′** (dimension-relaxed) and **TD-as** (almost sure) |
| SL-1's approximate sparsity (3) | **TD-A** (optional corollary) | Change of measure to a sparse surrogate (Fable Q7). Not an owner target | optional [TARGET], low priority |
| SL-3 (Cor 1 rates) | TD / TD′ radius | Ours is √(M log(p∨n)/n). TD′ covers p = exp(o(√n)), i.e. SL Cor 1 for α < ½. The range α ∈ [½, 1) needs a model-size cap c·n/log p, as SL's r̄_n provides | delivered for p ≤ n^A; TD′ [TARGET] |
| SL-4 (Condition 2: second moments only) | **TM-a0** (moments-only, fixed dimension) | For growing p our exact-marginal route needs exponential tails on sparse sets, so Condition 2 is not targeted there | non-target with reason (Astra Q7, Fable Q7) |
| SL-5 (Thm 3 sure screening) | **TS-a** (§4.2) | Same route: a Hellinger separation for every model that omits x_j, combined with contraction. SL Condition 3 is implied by sub-Gaussian rows (Fable Q2 [P]), so only the size of the residual signal is assumed | **[TARGET]**, low risk |
| SL-6, SL-7 (Thm S, Cor S1: MAP) | **TS-b** (§4.2); delivered special cases `thm:post-random`, `thm:post-fixed`, `thm:post-margin` | Our conclusion is stronger: π(S0 \| y) → 1 with a rate, HPM = MPM = S0, and every PIP within the rate (SL give pairwise odds only, with no rate). SL's sample eigen-structure (22) is replaced by a vanishing population floor, which is weaker than SL's own replacement (26). A converse (necessity) is added | delivered (fixed signals, fixed floor): "proved and independently checked". **[TARGET] TS-b** (margin form, covers S1 boundary signals) |
| SL-8 (Thm 4: misspecified density consistency) | **TM-a0** (literal: fixed candidate dimension, a.s.); **TM-a** (high-dimensional candidates, with rate) | Both concentrate on the KL projection f₀ of SL (17)/(19) | **[TARGET]**; TM-a0 low risk, TM-a low–medium |
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
- **Posterior and densities.** Π(· | D_n) is the exact posterior of (S, β, σ²) in §1. A posterior draw defines the conditional law N(ȳ + (x − x̄)ᵀβ, σ²) of y | x. f is the joint density with x drawn from its true law, f* is the true joint density, and d_H(f, f*)² = 1 − ∫√(f f*).

Assumption labels refer to `ASSUMPTIONS_AND_PROOF_PATHS.md` §2.

### 4.1 TD: true-distribution consistency (SL Theorems 1–2, Corollary 1)
**Mathematical statement (delivered form, `thm:dist`).** Assume A-GL, A-SPARSE, A-DIM, A-SUBG, A-NEC and A-BS. There are constants c_H > 0, M₀ and n₀, depending only on (s, A, L, c_ψ, b̄), such that for every M ≥ M₀ and every n ≥ n₀ with √n/log n ≥ M,

  P*[ Π( d_H(f, f*) > √(M log n / n) | D_n ) > n^{−c_H M} ] ≤ n^{−c_H M}.

The delivered assumption set includes a level-dependent size window q_n(M) on which A-SUBG and A-NEC are imposed (or6 `asm:dist`).

**TD-as [TARGET, low risk].** Fix the truth as a sequence and choose M with c_H·M > 1. Then
Π(d_H(f, f*) > √(M log n/n) | D_n) → 0 P*-almost surely. Proof path: Borel–Cantelli on the display above, since
Σ_n n^{−c_H M} < ∞. This is the counterpart of SL's almost-sure mode in Thm 4.

**TD′ [TARGET, conjecture, low–medium risk].** Replace A-DIM by A-DIM′, s·M·log p·log(p∨n) ≤ c_dim·n (headline form: (log p)² = o(n) for fixed s and M). The same conclusion is conjectured with radius ε_n² = M log(p∨n)/n.

- The proof path rests on the Fubini size-tail identity E*[m_S(y)/f*(y)] = 1, which bounds posterior model sizes at q_n ≍ s·M·log₂(p√n) for every p. A-DIM′ is then exactly the sample control needed on q_n-sets.
- Advisors disagree on this item. Fable gives the route at [P] level. Astra keeps p ≤ n^A for any released statement until a sieve-entropy/size-tail budget at K = n/2 is written out.
- Hence TD′ is a conjecture, and the released TD stays at p ≤ n^A.

**TD-A [optional TARGET].** Approximate sparsity in the spirit of SL (3): if the tail Σ_{j∉S_n} β*_j x_j is sub-Gaussian with variance ≤ c₀σ*²M log n/n, then TD holds with f* replaced by its s-sparse surrogate. The truth is then within Hellinger distance c·ε_n of that surrogate.

**Plain English.** With probability close to one, the posterior puts almost no weight on regression laws whose predictive distribution of y given a new x differs from the truth by more than about √(log n / n) in Hellinger distance. That is the parametric rate, up to the log factor every method pays for not knowing the model. No signal-strength (beta-min) condition is needed, because weak predictors that cannot be selected also cannot move the predictive law much. TD′ says the same should hold when p grows much faster than any power of n, as long as (log p)² is small compared with n.

### 4.2 TS: true-model (selection) consistency (SL Theorem 3, Theorem S, Corollary S1)
**TS-a, sure screening [TARGET, low risk].** Assume the TD assumptions and A-MARGIN-H: for each j ∈ S0,
inf{ R_n(S) : j ∉ S, |S| ≤ q_n } ≥ C_H(L)·M·σ*²·log(p ∨ n). Then for every j ∈ S0,

  P*[ Π( j ∈ S | D_n ) < 1 − n^{−c_H M} ] ≤ n^{−c_H M}, hence min_{j∈S0} PIP_j → 1 in probability (almost surely if c_H M > 1).

The constant C_H is inexplicit (it comes from the contraction constants), so TS-a is the per-predictor counterpart of SL Thm 3 and makes no claim at boundary signal levels.

**TS-b, exact selection [TARGET, margin form, low risk on correctness].** Assume A-GL, A-SPARSE, A-DIM, A-SUBG, A-NEC, A-BS′ and A-MARGIN-U, defined as follows. There are η > 0, γ ≥ 0 and a_n → ∞ such that, for all large n and every rival S with D ≠ ∅ and m ≤ j0(n),

  √R_n(S)/σ* ≥ (1+η)·[ w_m + √( 2·[ Pr_n(d) − (m/2)·log(n/(C·log p)) + γ log n ]₊ ) ] + a_n,

where w_m is the Gaussian-width allowance of the m added nulls: w_0 = 0, and w_m ≤ √(2 log C(p−s0, m)) ≈ √(2m log p). A simpler sufficient form is R_n(S) ≥ 2(1+η)²(√d + √m)²·σ*²·price_n. Then

  1 − π(S0 | D_n) = O_P( (s0+1)·√(log p/n) + n^{−γ} + n^{−c_H M} ),  P(HPM = MPM = S0) → 1,
  max_j |PIP_j − 1{j ∈ S0}| ≤ 1 − π(S0 | D_n).

- For pure deletions (m = 0), A-MARGIN-U is liminf κ_n > 1. Every nonempty D ⊆ S0 counts, not only singletons: multi-deletions bind on S1.
- j0(n) ≈ s0(1 + 2 log p/log(n/log p)) + 1 is fixed under A-DIM. Rivals with m > j0 are controlled without any signal.

**TS-b converse [TARGET, low risk].** Under the same regularity:
- if limsup κ_n < 1, then π(S0 | D_n) → 0 in probability;
- if √R_n(S0∖{j})/σ* − √(2·price_n) → c ∈ ℝ, then P(π(S0 | D_n) ≤ ½) → Φ(−c) > 0.

The constant 2 is therefore sharp for deletions, and S1 brackets κ = 1 from both sides (SIMULATION_DATA_ANALYSIS, Lead synthesis item 2 and E1).

**TS-b\* (sharp mixed-rival refinement) [TARGET, medium risk].** Replace the width allowance by Fable's MARGIN\*.
- (M1) Constant 2 + η on rivals inside a leakage set Q_n ⊇ S0 with log|Q_n| = o(log(p∨n)).
- (M2) Bounded leakage ϑ_n outside Q_n.

This form is used only if a referee asks why proxy swaps cost √(2m log p). The width term is attained by a factor-proxy design (Fable Q1(3c)), so it cannot be removed without design structure.

**Rejected:** the uniform "constant 2 for every rival" margin of DESIGN_MEMO_R0. Fable Q1(3d) gives a counterexample for fixed j0 when log n = o(log p). The question is OPEN under p ≤ n^A, and it is recorded as a conjecture only.

**Finite-n companion (Proposition, [TARGET]).**

  P(report = S0) ≥ 1 − (s0+1)/√(2πL(n+1)) − Σ_D Φ(−(√R̂(S0∖D)/σ − √(2Pr_n(d)))) − o(1),

with L = 2 log((2p−s0−1)/(s0+1)) + log(n+1). The middle term is the one-null superset ceiling, which is exact for Beta laws. This proposition explains the S1 plateau of 0.92–0.98 and the S2 value of 0.45 without any extra assumption.

**Delivered special case (`thm:post-random`).** Assume A-GL, A-DIM, A-SPARSE, SGR, FSb (fixed b_lo ≤ |β*_j| ≤ b_hi) and EFS (a fixed population floor on sets of size ≤ 5(A+1)(s0+1) log n). Then 1 − π(S0 | y) = O_P(√(log n/n)), P(HPM = MPM = S0) → 1 and max_j |PIP_j − 1{j∈S0}| = O_P(√(log n/n)). Status: "proved and independently checked" (or6 l.83–85). FSb + EFS give R_n(S) ≥ c·n for every rival with m ≤ j0, so A-MARGIN-U holds for large n and TS-b contains this result.

**Plain English.**
- TS-a: every true predictor whose signal the other predictors cannot imitate ends up with inclusion probability near one.
- TS-b: the posterior concentrates on the exact true model. The highest-probability and median-probability models both equal the true model with probability tending to one, and every inclusion probability is near 1 for true predictors and near 0 for nulls.
- The condition for TS-b: leaving out any group of true predictors must leave more unexplained signal than twice what the prior and the Occam factor charge for those predictors, with a little room to spare. When nulls are added in their place, there is an extra allowance for the best-looking nulls among p.
- If the unexplained signal is below twice that charge, the posterior provably drops the true model (converse), so the factor 2 cannot be improved.
- Up to constants, any method faces the same kind of limit (Wainwright 2009; Fletcher, Rangan & Goyal 2009).

### 4.3 TM: consistency under misspecification (SL Theorem 4, Corollary 2)
**Setting.** The method is run on the response and a candidate set C ⊂ [p] that may omit true predictors (SL's subset data D_n^s). C must be fixed in advance or chosen on independent data. The pseudo-true parameters (centred version of SL (17)/(19) and SLs (6), p. 6) are:

- β^C = Σ_CC⁻¹ Cov(x_C, y) and α_C = E y − E x_Cᵀβ^C;
- σ_C² = E(y − α_C − x_Cᵀβ^C)², S0^C = supp β^C, s_C = |S0^C|;
- f₀ = φ(y; α_C + x_Cᵀβ^C, σ_C) ν(x_C);
- the working residual u := y − α_C − x_Cᵀβ^C.

**TM-a0, literal counterpart of SL Thm 4 [TARGET, low risk].** Let the candidate dimension p_C be fixed, rows i.i.d., E‖x_C‖² < ∞, E y² < ∞, Σ_CC nonsingular, and π(S) > 0 for all S ⊆ C. Then Π(d_H(f, f₀) > ε | D_n^C) → 0 almost surely for every ε > 0. If also E[x_j² u²] < ∞ for all j ∈ C, then π(S0^C | D_n^C) → 1 almost surely. This is exact selection, stronger than SL Cor 2's inclusion.

Proof path (Fable Q6(3a)): there are 2^{p_C} models; the SLLN applies to Q_S/n and the LIL to the extra-variable gains. The argument is direct and avoids De Blasi–Walker.

**TM-a, density consistency to f₀ [TARGET, low–medium risk].** Assume A-MIS(iii): u is independent of x_C and u ~ N(0, σ_C²). Assume also A-SPARSE, A-DIM, A-SUBG, A-NEC and A-BS for the candidate problem (x_C, β^C, σ_C²). Then for M ≥ M₀,

  P*[ Π( d_H(f, f₀) > √(M log n / n) | D_n^C ) > n^{−c M} ] ≤ n^{−c M}  (almost surely if c·M > 1).

**TM-b, selection of the pseudo-true support [TARGET, margin form].** Assume A-MIS(iii) and the TS-b assumptions for the candidate problem, with A-MARGIN-U written in σ_C² units on μ_C = X_Cβ^C. Then 1 − π(S0^C | D_n^C) has the TS-b rate, and P(HPM = MPM = S0^C) → 1. In particular, as SL Cor 2's prose claims:
- a true predictor in C is selected iff β^C_j ≠ 0;
- proxies of omitted predictors (β*_j = 0 but β^C_j ≠ 0) are selected;
- cancelled true predictors (β*_j ≠ 0 but β^C_j = 0) are dropped.

**Delivered special case (`thm:omitted`, supplement_or l.135–153).** The assumptions are:
- Gaussian candidate rows and a Gaussian linear homoscedastic working residual (automatic when (x_C, x_omitted) are jointly Gaussian);
- A-DIM, with s_C fixed;
- a floor on sets of size 3(A+1)(s_C+1) log n and bounded projected signal;
- n·min_j Σ_jj(β^C_j)²/(σ_C² log n) → ∞.

The conclusions are E[1 − π(S0^C | y)] = O(√(log n/n)) and P(HPM ≠ S0^C) = O(√(log n/n)). Status (main): "Proved and independently checked."

**Not targeted, stated as remarks with their reason:**
- **(i′)** An independent but non-Gaussian sub-Gaussian residual needs two extra conditions: a model-size cap K_n ≤ c·n log n/(log p)², and a variance-proxy budget ϱ̄ ≤ 1 + (1−ε)·log n/(2 log p). The reason is that the Fubini size tail fails under misspecification. The code uses K = n/2, so this needs an Engineering decision.
- **(ii)** For a heteroscedastic residual, selection survives iff (ϱ̄ − 1)·log p < ½·log n. This is the mechanism behind Grünwald & van Ommen's failure examples in our model, and it is stated as a counter-calculation, not a theorem.

**Plain English.** If some true predictors are missing from the data, the method cannot find them. What it does find is the best approximation available:
- the posterior predictive law converges to the closest Gaussian linear law built from the available predictors (SL's f₀);
- the noise variance absorbs the unexplained part;
- the selected model is exactly the set of available predictors that the best linear predictor uses, including proxies that stand in for missing predictors.

In high dimension this is guaranteed when the leftover error behaves like independent Gaussian noise. When it does not (for example, the error variance depends on x), our counter-calculation shows that selection can fail once p is large enough, which is the effect Grünwald & van Ommen document.

---

## 5. What moves if Engineering changes the method (summary; details in ASSUMPTIONS_AND_PROOF_PATHS.md §5)
Both advisors independently reached the corrections below, which supersede TH_PREP §3 on the size prior.

- **Invariant in form.** All statements concern "the posterior of the coded prior", so their form survives any change of g, of the size prior BB(1, b), of the cap K ≥ s0 + j0(n), of the σ² prior IG(a₀, b₀), or of a reporting rule that is a fixed function of the PIPs.
- **Margin threshold moves with the price.** With slab scale g, price_g(k) = log[(2p−1−k)/(k+1)] + ½ log(1+g).
  - The TS-b threshold 2·Pr_n scales with this price, and the superset mass scales as (s0+1)·√(log p/g). One needs g/log p → ∞ (more precisely, s0² log p = o(g)).
  - g = max(n, p²): the price is ≈ 2 log p, so more signal is needed but the superset mass is smaller. This is a power-for-robustness trade.
  - A fixed (data-free) g can prevent selection.
- **BB(1, p^u), u < 1.** The per-variable prior odds stay ≈ (k+1)/p, so the price changes by at most log 2. What is lost is the geometric 2^{−k} size tail: the size ratio becomes ≈ 1 − p^{u−1}.
  - Consequence: the Fubini size bound is gone, and a cap K_n ≤ c·n·log n/(log p)² is needed.
  - TH_PREP's "(1−u)A < ½" condition belongs to an independent Bernoulli(p^{−u}) prior, not to BB(1, p^u).
  - For u > 1 the price rises by (u−1) log p, the size tail becomes p^{−(u−1)k}, and no new condition is needed.
- **Reporting rule.** HPM = S0 once 1 − π(S0 | y) < ½. MPM with threshold q returns S0 once max_j |PIP_j − 1{j∈S0}| < min(q, 1−q). MPM = S0 needs only s0/√(n log p) → 0 plus the margin, which is weaker than π(S0 | y) → 1.
- **Cap K.** It must satisfy K ≥ s0 + j0(n). A smaller cap K_n ≤ c·n/log p would unlock log p = o(n) (A-DIM″).
- **Ridge and floor.** The vanishing floor c_ψ/n in A-NEC is set by the unit ridge in the slab, not by g.
- **Route-breaking for TM.** A data-free slab V = τ²I, or no scaling, breaks the exact candidate reduction, which uses n(G+I)⁻¹ and the data-scaled σ² rate.
