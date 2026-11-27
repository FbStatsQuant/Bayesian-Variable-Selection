# THEOREM DEFINITIONS — Song & Liang (2015) ↔ SMC-BVS, and our target theorems

Theory Department, mission TH-SONG-ASSUMPTIONS, 2026-11-27. Task Lead: Opus 5.5. **Draft v0 (pre-advisor).**
Scope: define the targets and their assumptions. **No proofs are claimed here.** Statuses of results already delivered for
v3.1.1 are quoted from the manuscript/registry; everything marked **[TARGET]** is a conjecture whose proof path is in
`ASSUMPTIONS_AND_PROOF_PATHS.md`.

Sources read directly for this file:
- SL = Song, Q. & Liang, F. (2015) *J. R. Statist. Soc. B* 77(5), 947–972 (journal pagination);
- SLs = its online supplement (20 pp., printed page numbers; obtained from the OUP article page 2026-11-27; local
  read-only copy `Papers/Core_bibliography/32b_2015_Song_Liang_supplement.pdf`, not tracked: the repo is public);
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
| slab | β_S \| S, σ² ~ N(0, nσ²(X_SᵀX_S + I)⁻¹): g = n with unit ridge | **identical in form** to SL's SAM prior V_ξ⁻¹ = (X_ξᵀX_ξ + τI)/n (SL p. 959; SLs p. 16), τ = 1 vs SL's τ = 0.01 |
| σ² | IG(0.01, 0.01) | IG(a₀,b₀), SL use a₀ = b₀ = 1 (p. 960) |
| model prior | BB(1,p): π(S) ∝ ½/C(2p−1,\|S\|) on Ω = {\|S\| ≤ K}, K = min(p, ⌊n/2⌋) | SL (6): independent Bernoulli(r_n/P_n) truncated at r̄_n, r_n = P_n^{1−γ} (p. 951, 960) |
| report | MPM (PIP > ½); HPM stored | SL: PIP thresholding at an FDR level (ξ_q, p. 956) or MAP |
| algorithm | SMC with frozen tempering (DEFERRED results) | SAMC (SLs §2) |

Two consequences used throughout. (i) The per-variable cost of adding a predictor to a size-k model is
**price(k) = log[(2p−1−k)/(k+1)] + ½ log(n+1)** (prior + Occam), ≈ log(2p/s0) + ½ log n near the truth; on S1/S2 this is
7.5–10 nats. (ii) The size marginal of BB(1,p) decays like 2^{−k} while each model carries a p^{−k}-type multiplicity
penalty (Scott & Berger 2010); SL instead use r_n/P_n → 0 (p. 951) and a small cap r̄_n.

---

## 2. Every important result in Song & Liang (2015), read directly

Notation of SL: P_n predictors, t = true model, ξ = a model, ε_n a radius, r_n/P_n the prior inclusion probability, r̄_n the
model-size cap, B(r_n) = sup_{|ξ|=r_n} ch₁(V_ξ⁻¹), B̃_n = sup_{|ξ|≤r̄_n} ch₁(V_ξ), Δ(r_n) = inf_{|ξ|=r_n} Σ_{i∉ξ}|β*_i|, d the Hellinger
distance between joint densities of (x, y).

| # | SL result (page) | exact content | conditions |
|---|---|---|---|
| SL-1 | **Theorem 1**, posterior consistency (p. 952) | P*[π{d(f,f*) > ε_n \| D_n} > exp(−c₁nε_n²)] < exp(−c₁nε_n²) for large n (display (15)) | all predictors standardised and \|x_i\| ≤ 1; approximate sparsity (3): lim Σ_j\|β*_j\| < ∞; nε_n² ≻ 1 and (8) Δ(r_n) ≺ ε_n, (9) r̄_n ln(1/ε_n²) ≺ nε_n², (10) r̄_n ln(P_n) ≺ nε_n², (11) r̄_n ln(nε_n²B̃_n) ≺ nε_n², (12) 1 ≤ r_n ≤ r̄_n < P_n, (13) r_n ≺ P_n, (14) B(r_n) ≺ nε_n²; asymptotics with P_n ≻ n^θ (p. 950). Proof via Jiang (2005) Thm 6 (SLs Lemma 1.1, p. 1) |
| SL-2 | **Theorem 2** (p. 953) | same conclusion as (15) | Condition 1 (p. 953): E exp{(Σ_{i≤r} a_i x_{j_i}/r)²} ≤ e^M for every r ≤ r̄_n subvector and \|a_i\| ≤ δ (exponential moments on sparse directions); ε_n → 0, nε_n² → ∞; (9)–(14); strict sparsity (4): lim Σ_j 1{β*_j ≠ 0} < ∞; r_n ≻ 1 |
| SL-3 | **Corollary 1**, rates (p. 954) | ε_n = O{n^{−(1−α)/2} log^{k/2} n} if r_n < r̄_n ≺ log^k n; ε_n = O(n^{−min{1−α−q, 1−vq}/2}) if r_n < r̄_n ≺ n^q, 0 < q < min{1−α, 1/v} | strict sparsity; P_n < exp(Cn^α), α ∈ (0,1); B(r_n) ≤ Br_n^v, B̃_n ≤ Bn^v |
| SL-4 | **Condition 2 ⇒ (16)** (p. 954) | lim_n P*[π{d(f,f*) > ε_n \| D_n} > exp(−c₁nε_n²)] = 0 (in-probability version) | second moments only: E(Σ a_i x_{j_i}/r)² ≤ M |
| SL-5 | **Theorem 3**, sure screening (p. 956) | for each identifiable true x_t: P*[π{t ∈ ξ \| D_n} < 1 − exp(−c₁nε_n²)] < exp(−c₁nε_n²); under Condition 2 the weaker in-probability form. Hence π(t ⊂ ξ_q) →_P 1 if all true predictors are identifiable (p. 956) | Theorem 2's conditions + Condition 3 (p. 955), identifiability: E exp{−(x_k + Σ_{i≤r̄_n} b_i x_{j_i})²} ≤ 1 − δ_n with δ_n ≻ ε_n² for all choices; for Gaussian x this holds if var(x_k + Σ b_i x_{j_i}) ≻ ε_n² (pp. 955–956) — a **vanishing** residual-variance floor. Proof (SLs §1.2, pp. 5–6): any f omitting x_t has d²(f*,f) ≥ min{δ_n, β_t*²δ_n/(20σ*²), 1 − √0.8} ≻ ε_n², i.e. a residual-signal margin at the Hellinger scale |
| SL-6 | **Theorem S**, MAP consistency (SLs p. 13) | max_{k≠t} π(k \| D_n)/π(t \| D_n) →_P 0 (display (24)) — pairwise odds; does not by itself give π(t \| D_n) → 1 | condition (12); fixed-design sample eigen-structure (22): n l_n < ch'₁(X_ζᵀX_ζ) ≤ ch₁(X_ζᵀX_ζ) < n l'_n for all \|ζ\| = min{\|t\| + r̄_n, n}; (23) r̄_n log P_n ≺ n l_n; and either V_ξ⁻¹ = I with n l_n ≻ log l'_n, log(√(n l_n)/r_n) ≻ √(log P_n), or V_ξ⁻¹ = X_ξᵀX_ξ/n with n l_n ≻ l'_n, log(√n/r_n) ≻ √(log P_n). The proof (SLs pp. 14–15) uses a noncentrality ≥ n l_n c², c = min_{i∈t}\|β*_i\|, and needs n l_n c² ≫ log r̄_n + r̄_n log P_n (a diverging-multiple beta-min × eigenvalue floor). SL's own remark (SLs p. 15): "(22) is hardly satisfied"; they replace it by the random-design condition (26), P[eigen bounds fail on \|ζ\| = r̄_n + \|t\|] < e^{−nC}, true for Gaussian designs with bounded population eigenvalues (Fan & Lv 2008, App. A.7; SLs p. 16) |
| SL-7 | **Corollary S1** (SLs p. 16) | MAP consistency | P_n < n^{κ log n}, κ ∈ (0, 1/4) (quasi-polynomial p); V_ξ⁻¹ = X_ξᵀX_ξ/n (+τI/n); r̄_n ≺ log^{k₁} n or n^q with q ≤ ½ − √κ; l'_n = l_n⁻¹ = √n/log^{k₂} n |
| SL-8 | **Theorem 4**, misspecified subset (p. 957) | for a fixed subset s not containing all true predictors: π[{f ∈ P_s : d(f₀, f) > ε} \| D_n^s] → 0 almost surely, every ε > 0; f₀ = KL projection of f* onto P_s, display (17); by SLs Lemma 1.2 (= De Blasi & Walker 2013 Cor 1, SLs p. 6) f₀ = φ(y; β₀ᵀx_s, σ₀)ν(x_s), β₀ = Σ_s⁻¹Σ_{s,t}β*_t, σ₀² = σ*² + E(β₀ᵀx_s − β*ᵀx)² (SLs p. 6) | Condition 4 (p. 957): E{(aᵀx_s)²} < ∞ for \|a_i\| ≤ δ; π(ξ) > 0 for every ξ ⊆ s; \|s\| fixed (finitely many models, SLs p. 7) |
| SL-9 | **Corollary 2** (p. 957) | π(s̃ ⊂ ξ \| D_n^s) →_P 1, s̃ = supp β₀ (inclusion of the pseudo-true support; display (19)) | Theorem 4 + no exact multicollinearity in x_s (no a ≠ 0 with P(aᵀx_s = 0) = 1). Explicitly not claimed under a binding size cap (p. 958, remark (c)) |
| SL-10 | **Condition 5** + iterative procedure (p. 958) | \|cov(x_t, y)\| > 0 for every true x_t ⇒ iterating the subset screening keeps every true predictor of x_s | — |
| SL-11 | SAM consistency (p. 959, §3.1) | "Clearly, it follows from the theory … that the SAM approach will lead to a consistent selection of true predictors" | informal composition of SL-5/6/8/9/10; no separate theorem |
| SL-12 | Time complexity (§6, pp. 968–969) | O(P_n^{(1+α)/2} + nP_n) with K_n = O(√P_n) subsets | algorithmic analysis, not a theorem |
| SL-13 | SAMC estimator (SLs §2, p. 12; Lemma S2, p. 17) | q̂_j → q_j a.s. as the number of iterations N → ∞ (Liang 2009); Lemma S2: consistency of the sample-based MAP/PIP estimator | algorithm convergence |

---

## 3. One-to-one map: each SL result → our counterpart

Legend. **Delivered** = a v3.1.1 result exists (status quoted). **[TARGET]** = a theorem this mission defines, with a proof path
and assumptions in `ASSUMPTIONS_AND_PROOF_PATHS.md` (no proof claimed). **Deferred** = owner scope ruling. **N/A** = no
counterpart by design.

| SL | our counterpart | relation | status |
|---|---|---|---|
| SL-1, SL-2 (Hellinger consistency) | **TD** (§4.1) = delivered `thm:dist` (or6 l.125) | same metric (Hellinger between joint densities, x from its true law), same exponential form exp(−cnε²) = n^{−cM} inside the window ε² = M log n/n, M ≤ √n/log n; SL allow larger radii and exponential P_n; we allow K = n/2 (SL's (9)–(10) would fail at r̄_n ≍ n) and no beta-min/fixed floor | delivered: "Proved and independently checked. Registry row 2.1"; **[TARGET] TD′** = dimension-relaxed form (§4.1) |
| SL-1's approximate sparsity (3) | none (we assume strict sparsity) | gap; not a target (owner's three targets use strict sparsity, as SL Thms 2–4 do) | noted, not targeted |
| SL-3 (rates) | TD's radius √(M log n/n) | ours is the near-parametric rate at polynomial p; SL's rate n^{−(1−α)/2}log^{k/2}n covers exponential p | delivered for p ≤ n^A; TD′ targets log p = o(n^{α₀}) |
| SL-4 (second moments only) | none | dominated in our Gaussian-noise / sub-Gaussian-design setting; not a target | noted |
| SL-5 (sure screening) | **TS-a** (§4.2) | same route (Hellinger margin + contraction), stated with our identifiability margin in residual-signal form | **[TARGET]** (new; follows from TD + a margin) |
| SL-6, SL-7 (MAP consistency) | **TS-b** (§4.2) = delivered `thm:post-random` (or6 l.71) plus `thm:post-fixed`, `thm:post-margin` (supplement) | ours is stronger in conclusion: π(S0 \| y) → 1 at rate √(log n/n), HPM = MPM = S0, all PIPs within the rate (SL: pairwise odds only, no rate); same prior family (g = n ridge slab); SL need sample eigen-structure (22) which they call "hardly satisfied", we use the random-design population floor, i.e. SL's own replacement (26) | delivered (fixed signals): "proved and independently checked"; **[TARGET] TS-b′** = margin form covering boundary signals |
| SL-8 (misspecified density consistency) | **TM-a** (§4.3) | Hellinger contraction of the candidate-only posterior to the KL projection f₀ (SL's f₀) at a rate, in probability | **[TARGET]** (jointly Gaussian case: TD applied to the candidate data; beyond: conjecture) |
| SL-9 (Cor 2: inclusion of pseudo-true support) | **TM-b** (§4.3) = delivered `thm:omitted` (supplement l.135) + C-MIS MIS(i)–(iii) | ours is stronger in conclusion: exact selection of S0^C = supp β^C with E[1 − π(S0^C \| y)] = O(√(log n/n)); narrower in setting (Gaussian linear working residual) | delivered: main status "Proved and independently checked"; **[TARGET] TM-b′** = margin form |
| SL-10 (Condition 5, iterative screening) | none needed | we do not split predictors; the full-data posterior has no screening stage whose miss must be repaired | N/A by design |
| SL-11 (SAM consistency) | composition TS-b (full data) | our method runs on all p predictors, so TS-b *is* the end-to-end selection guarantee for the exact posterior | N/A by design (covered by TS-b) |
| SL-12 (time complexity) | SMC cost analysis | not a theorem in SL either | Deferred |
| SL-13 (SAMC q̂_j → q_j) | particle-limit theorem (T4a/T4b in TH_PREP §2) | algorithm convergence | **Deferred** (owner scope ruling) |

---

## 4. Target theorems — exact mathematical and plain-English statements

Common setting and notation. Data D_n = {(x_i, y_i)}_{i≤n}, i.i.d. (random design) unless stated. True model
y = α* + xᵀβ* + ε, ε ~ N(0, σ*²) independent of x, x ∈ ℝ^p with covariance Σ (correlation matrix R). S0 = supp β*,
s0 = |S0|. For S ⊆ [p]: **R_n(S) := n·Var(xᵀβ* | x_S)** (population unexplained signal of S; for Gaussian x,
R_n(S) = n β*_Dᵀ Σ_{DD·S} β*_D with D = S0∖S). price_n := log(2p/s0) + ½ log(n+1). Π(· | D_n) is the exact posterior of
(S, β, σ²) of §1. A posterior draw defines the conditional law N(ȳ + (x − x̄)ᵀβ, σ²) of y | x; f is the joint density with x
from its true law, f* the true one; d_H(f, f*)² = 1 − ∫√(f f*). Assumption labels refer to
`ASSUMPTIONS_AND_PROOF_PATHS.md` §2.

### 4.1 TD — true-distribution consistency (SL Theorems 1–2, Corollary 1)
**Mathematical statement (delivered form, `thm:dist`).** Assume A-GL, A-SPARSE, A-DIM, A-SUBG, A-NEC, A-BS. There are
c_H > 0, M₀, n₀ depending only on (s, A, L, c_ψ, b̄) such that for every M ≥ M₀ and n ≥ n₀ with √n/log n ≥ M,

  P*[ Π( d_H(f, f*) > √(M log n / n) | D_n ) > n^{−c_H M} ] ≤ n^{−c_H M}.

**[TARGET] TD′ (dimension-relaxed).** Same conclusion with radius ε_n² = M log(p ∨ n)/n under A-DIM′ in place of A-DIM
(exact form of A-DIM′ fixed after advisor round 1).

**Plain English.** With probability close to one, the posterior puts almost no weight on regression laws whose predictive
distribution of y given a new x differs from the truth by more than about √(log n / n) in Hellinger distance — the parametric
rate up to the log factor every method pays for not knowing the model. No signal-strength (beta-min) condition is needed:
weak predictors that cannot be selected also cannot move the predictive law much.

### 4.2 TS — true-model (selection) consistency (SL Theorem 3, Theorem S, Corollary S1)
**TS-a, sure screening [TARGET].** Assume the TD assumptions and A-MARGIN-H. Then for every j ∈ S0,

  P*[ Π( j ∈ S | D_n ) < 1 − n^{−c_H M} ] ≤ n^{−c_H M}, hence min_{j∈S0} PIP_j → 1 in probability.

**TS-b, exact selection [TARGET, margin form].** Assume A-GL, A-DIM, A-SPARSE, A-SUBG (or Gaussian rows), A-NEC, A-BS,
A-FLOOR0 and A-MARGIN. Then

  1 − π(S0 | D_n) = O_P( √(log(p∨n)/n) + n^{−c η} ),  P(HPM = MPM = S0) → 1,
  max_j |PIP_j − 1{j ∈ S0}| ≤ 1 − π(S0 | D_n).

**Delivered special case (`thm:post-random`).** Under A-GL, A-DIM, A-SPARSE, SGR, FSb (fixed b_lo ≤ |β*_j| ≤ b_hi) and EFS
(fixed population floor on sets of size ≤ 5(A+1)(s0+1) log n): 1 − π(S0 | y) = O_P(√(log n/n)), P(HPM = MPM = S0) → 1,
max_j |PIP_j − 1{j∈S0}| = O_P(√(log n/n)). Status: "proved and independently checked" (or6 l.83–85). FSb + EFS imply
A-MARGIN for large n, so TS-b contains it.

**Plain English.** TS-a: every true predictor whose signal cannot be imitated by other predictors ends up with inclusion
probability near one. TS-b: the posterior concentrates on the exact true model — the highest-probability model and the
median-probability model are the true model with probability tending to one, and every inclusion probability is near 1 for
true predictors and near 0 for null ones. The condition is that each true predictor leaves, when it is left out, an amount
of unexplained signal larger than twice the price the prior charges for one extra predictor — a requirement any method
faces up to constants (information-theoretic limits).

### 4.3 TM — consistency under misspecification (SL Theorem 4, Corollary 2)
Setting: the method is run on the response and a candidate set C ⊂ [p] that may omit true predictors (SL's subset data
D_n^s). Pseudo-true parameters (SL's f₀, SLs p. 6): β^C = argmin_b E(y − x_Cᵀb)² = Σ_CC⁻¹ Cov(x_C, y),
σ_C² = E(y − x_Cᵀβ^C)², S0^C = supp β^C, f₀ = φ(y; x_Cᵀβ^C, σ_C) ν(x_C).

**TM-a, density consistency to the KL projection [TARGET].** Assume A-MIS (working-residual condition), and A-SPARSE,
A-DIM, A-SUBG, A-NEC, A-BS for the candidate problem (x_C, β^C, σ_C²). Then for M ≥ M₀,

  P*[ Π( d_H(f, f₀) > √(M log n / n) | D_n^C ) > n^{−c M} ] ≤ n^{−c M}.

**TM-b, selection of the pseudo-true support [TARGET, margin form].** Assume A-MIS and the TS-b assumptions for the
candidate problem, with A-MARGIN stated for (x_Cᵀβ^C, σ_C²). Then E[1 − π(S0^C | D_n^C)] → 0 (rate as TS-b), and
P(HPM = MPM = S0^C) → 1. In particular (SL Cor 2 strengthened), a true predictor in C is selected iff β^C_j ≠ 0; proxies of
omitted predictors (β*_j = 0, β^C_j ≠ 0) are selected; cancelled true predictors (β*_j ≠ 0 = β^C_j) are dropped.

**Delivered special case (`thm:omitted`).** Gaussian candidate rows and Gaussian linear homoscedastic working residual
(automatic when (x_C, x_omitted) are jointly Gaussian), floor on 3(A+1)(s_C+1)log n sets, bounded projected signal and
n min Σ_jj(β^C_j)²/(σ_C² log n) → ∞: E[1 − π(S0^C | y)] = O(√(log n/n)) and P(HPM ≠ S0^C) = O(√(log n/n)). Status (main):
"Proved and independently checked" (supplement_or l.149–153).

**Plain English.** If some true predictors are missing from the data, the method cannot find them; what it does find is the
best approximation available: the posterior predictive law converges to the closest Gaussian linear law built from the
available predictors (SL's f₀), the noise variance absorbs the unexplained part, and the selected model is exactly the set
of available predictors that the best linear predictor uses — including proxies that stand in for missing predictors.

---

## 5. What moves if Engineering changes the method (summary; details in ASSUMPTIONS_AND_PROOF_PATHS.md §5)
- **Invariant in form:** all three statements are about "the posterior of the coded prior"; their *form* survives any
  change of g (slab scale), size prior BB(a,b), cap K ≥ c·s0 log p, σ² prior IG(a₀,b₀), or reporting rule that is a fixed
  function of PIPs returning S0 when all PIPs are within δ of their indicators.
- **Constants only:** g = c·n; BB(1, c·p); BB(1,p^u), u ≥ 1; IG(a₀,b₀); MPM ↔ HPM; fixed PIP threshold q.
- **Margin threshold moves:** A-MARGIN is stated in terms of price_n, which contains ½ log(g+1) and the size prior's
  log-ratio; a smaller g or a lighter size prior lowers the threshold (helps boundary signals), a larger g (e.g. max(n, p²))
  raises it.
- **New condition:** BB(1,p^u) with u < 1 or g ≪ n: the per-variable price may fall below log p, so superset control needs
  a DIM-type condition (1−u)A < ½ (TH_PREP §3); BB(1,1) loses the 2^{−k}-plus-multiplicity structure (route-breaking).
- **Route-breaking for TM:** a data-free slab V = τ²I or no scaling (the exact candidate reduction uses n(G+I)⁻¹ and the
  data-scaled σ² rate).
