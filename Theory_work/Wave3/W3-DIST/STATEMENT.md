# W3-DIST — STATEMENT (candidate statements; v1.1, 2026-11-15; lead: Claude Fable 5.2, Claude Third, high)

**Status of everything in this file: CANDIDATE (scoping leg; nothing here is proved).** v1.1 = v1.0.2 with the
dispositions of the blind read S1 (`reviews/S1_astra.md`, `reviews/S1_disposition.md`). Changelog: table at the foot
(PROTOCOL_v4 §4.2). Target clauses: `TARGET.md` §5. Statuses of consumed results are verbatim from their files, from
`Theory_work/INFRA/registry/claims.tsv`, or from HQ notes where marked.

Aliases: **[W3P]** = `Theory_work/Wave3/W3-POST/STATEMENT.md` (v1.4); **[P2]** = `Theory_work/Wave3/W3-POST2/STATEMENT.md`
(v1.2.1); **[D]** = `W3-POST2/lemmas/D_hellinger.md`; **[SL]** = Song & Liang (2015), journal pages; **[SAMP]** =
`Theory_work/Wave3/W3-SAMP/STATEMENT.md`; **[CC]** = `W3-SAMP/lemmas/CC_code_check.md`; **H1** =
`work/prior_probe/REPORT.md` (helper, unchecked).

## 0. Setting and objects

**Data (RD).** Triangular array. Rows (x_i, y^r_i), i ≤ n, i.i.d.: x_i ~ ν_x, an **arbitrary** law on ℝ^{p_raw},
p_raw = p_{raw,n}; y^r_i = α* + x_iᵀβ* + ε_i with ε_i ~ N(0, σ*²) independent of the design (Gaussian noise, as in [SL]
model (1)); σ*² > 0 fixed. **Strict sparsity** ([SL] (4)): |supp β*| = s₀^r fixed (s₀^r = 0 allowed).
p_raw ≤ n^A, A ≥ 1 fixed; p_raw ≫ n allowed. True joint density f*(x, y) = ν_x(dx) φ(y; α* + xᵀβ*, σ*²).
P* = law of the data; **P⊗** = joint law of the data and the algorithm's streams, as in [SAMP] §1 (used only in §2).

**Raw and retained dimensions [S1-02].** The code drops the columns that are constant in the sample. **p := p_ret(X)**
is the number of retained columns; it is design-measurable, p_ret ≤ p_raw ≤ n^A. The coded prior w, the model space Ω,
the cap K = min(p, ⌊n/2⌋), (ND) and the store capacity use p = p_ret; the transfer class of Lemma T uses p_raw.
Domain event **𝒟_n := {p_ret ≥ 2}** (the inherited lemmas need p ≥ 2); its complement is put in the remainder of every
theorem (the cases p_ret ∈ {0, 1} are finite problems, to be treated directly in the proof leg or left in the remainder).

**The exact posterior (prior as coded).** Π(· | D_n) is the exact working-model posterior of (S, θ_S, v) of [W3P] §0
and [D] D0 on the response scale: models S ∈ Ω = {|S| ≤ K} over the retained columns; prior w(k) = ½/C(2p−1, k)
(BB(1, p) capped at K); slab N(0, n v (G_S + I)⁻¹) on sample-standardised columns; IG(0.01, 0.01) on the standardised
response scale (rate b₀s_y² on the response scale). No tuning is added. θ* = D_xβ* restricted to retained columns,
S₀ = supp θ*, s₀ = |S₀|, μ = CX^rβ* (a dropped true column contributes 0 to μ). **s₀ is design-measurable with values
in {0, …, s₀^r}**; constants below depend on s₀^r (maxima over this range), every statement covers s₀ = 0, and
s₀ ≤ K = min(p, ⌊n/2⌋) holds for n ≥ 2s₀^r (s₀ ≤ p always).

**The density attached to a posterior draw.** For (S, θ, v): raw coefficients b_j = θ_j/ŝ_j (ŝ_j = sample SD of column
j; b_j = 0 off S and on dropped columns), plug-in intercept â = ȳ^r − x̄ᵀb, and
  f_{S,θ,v}(x, y) := ν_x(dx) φ(y; â + xᵀb, v).
Remark R1 [S1-09]: drawing in addition α ~ N(â, v/n) is a *post-processing extension* of the coded posterior (it is
not claimed to be the posterior of an uncentred model with a flat intercept prior and the same IG prior; that model
has shape 0.01 + (n−1)/2). The statements below are for the plug-in intercept; the extension changes constants only
(candidate).

**Distance.** d_H²(f, g) := 1 − ∫√(fg). [SL]'s d² = ∫(√f − √f*)² = 2 d_H². Both densities share the x-marginal, so
d_H²(f_{S,θ,v}, f*) = E_x H²(N(â + xᵀb, v), N(α* + xᵀβ*, σ*²)), x ~ ν_x independent of the data: the distance of [SL]
Theorems 1–2, not the in-sample average of [D].

**Sample-level interfaces (X-measurable; design-agnostic; at a given n).**
- **(E; M)** energy: ‖μ‖² ≤ nM. ([W3P] §2.)
- **(C; M′)** coefficient cost: ‖θ*‖² ≤ nM′. Used only through **(L₀; B)**: L_{S₀} := μ_cᵀ(I − M_{S₀})μ_c ≤ B, which
  (C) and (E) imply with B = M + M′ ([D] D1; [P2] B_T(ϑ)). (L₀) can hold when (C) fails. [(E) ∧ (F₀) give the far
  stronger ‖θ*‖² ≤ 1.5M/φ₀².]
- **(ND; c_D, m)** no degeneracy on average = [P2] (ADG; c_D) on the range 1 ≤ j ≤ min(m, p − s₀):
  C(p − s₀, j)⁻¹ Σ_{J⊆[p]∖S₀, |J|=j} (D_{S₀}/D_{S₀∪J})^{1/2} ≤ [c_D(n + 1)]^{−j/2}.
  Sufficient: [P2] (DG; c_D), or [W3P] (F_w; g₀) with c_D = g₀/(1 + g₀) ([P2] A0, "PROVED (by this seat, unchecked)").
  It fails only under near-exact linear dependence (unnormalised Gram eigenvalues of order 1 or less). It is not an
  identifiability or beta-min condition. **It is a geometric condition on the design that [SL] Theorems 1–2 do not
  have** [S1-04]; DIST-2 is the statement without it. H1 F1: the weaker [P2] (OS) is *not* enough for the exponential
  form.
Cutoff (X-measurable through p and s₀; deterministic given X [S1-02]):
m_n(t) := min{K, s₀ + ⌈(s₀ log(2p) + ((s₀+2)/2) log(n+1) + 3t)/log 2⌉}.
Throughout, κ₀ ∈ (0, 1) is fixed and "constants" may depend on (s₀^r, A, σ*², M, M′ or B, κ₀) and, where (ND) is assumed,
c_D; ℓ_n := log(p_raw ∨ n).

## 1. Candidate theorems for the exact posterior (target (i); P1–P5)

**Theorem DIST-1 (joint Hellinger contraction, exponential form, sharp rate).** There are constants c ∈ (0, 1], C, C′,
M₀, n₀ such that, in (RD), for every n ≥ n₀ and every real t with M₀ log n ≤ t ≤ n^{1−κ₀}:
  P*[ Π( d_H(f, f*) > C√(t/n)  or  |S| > s₀ + C′t/log n | D_n ) > e^{−ct} ]
     ≤ 3e^{−ct} + P*( 𝒟_nᶜ ∪ (E; M)ᶜ ∪ (C; M′)ᶜ ∪ (ND; c_D, m_n(t))ᶜ ).   (1.1)
Equivalently, for every sequence ε_n with C²M₀ log n/n ≤ ε_n² ≤ C²n^{−κ₀} and c₁ := c/C²:
  P*[ Π( d_H(f, f*) > ε_n | D_n ) > e^{−c₁nε_n²} ] ≤ 3e^{−c₁nε_n²} + P*(interfaces fail):
[SL] (15) with an explicit remainder. Consequences:
- (a) **[SL] (15)-form** whenever P*(interfaces fail) ≤ e^{−c₁nε_n²}. At the best rate the right side is n^{−cM₀}, a
  polynomial, so polynomial-probability control of the design events is enough there.
- (b) **[SL] (16)-form**: if P*(interfaces fail) → 0 then lim P*[Π(d_H > ε_n | D_n) > e^{−c₁nε_n²}] = 0.
- (c) **Rate (P3)**: ε_n² = C²M₀ log n/n with M₀ of order (1 + s₀^r)(A + 1): of order (1 + s₀) log p/n when p = n^A
  (the "1 +" is the intercept and the variance; s₀ = 0 is covered) [S1-07]. No beta-min and no identifiability
  condition ([SL] Condition 3 is not used).
- (d) **No condition on ν_x enters the passage from the sample to the population distance** (Lemma T); the law of x
  matters only through the probability of the interfaces.
- (e) **Posterior predictive.** With f̄ := ∫ f dΠ(f | D_n): on the complement of the event in (1.1) (the success
  event), d_H²(f̄, f*) ≤ C²t/n + e^{−ct} (convexity of d_H² in its first argument) [S1-11].

**Theorem DIST-2 (no geometric condition on the design; one logarithm slower).** There are c, C, M₀, n₀ (depending on
(s₀^r, A, σ*², M, M′, κ₀)) such that for n ≥ n₀ and M₀ log n ≤ t ≤ n^{1−κ₀}:
  P*[ Π( d_H(f, f*) > C√(tℓ_n/n) | D_n ) > e^{−ct} ] ≤ 3e^{−ct} + P*( 𝒟_nᶜ ∪ (E; M)ᶜ ∪ (C; M′)ᶜ ).   (1.2)
Interfaces: Gaussian noise independent of the design, (E), (C); nothing on the dependence among predictors. Best rate
ε_n² ≍ (1 + s₀^r) log n · ℓ_n/n: one logarithm slower than DIST-1 at polynomial p. In [SL]'s form the exponent is
c nε_n²/ℓ_n, not c nε_n² (comparison with [SL]: TARGET.md §2) [S1-04, S1-07].

**Theorem DIST-3 (oracle bound with an additive selection error; parametric rate) [S1-03, BT1, BT2].** Let
**(TR₀; C_T)** be the X-event { E_x(a + uᵀx)² ≤ C_T · n⁻¹Σ_i(a + uᵀx_i)² for all a ∈ ℝ and all u supported on supp β* }.
There are c, C such that for every n ≥ n₀, every 1 ≤ u ≤ n^{1−κ₀} and every design in 𝒟_n ∩ (E; M) ∩ (L₀; B) ∩ (TR₀; C_T),
outside a noise event of probability ≤ Ce^{−cu}:
  Π( d_H(f, f*) > C√(u/n) | D_n ) ≤ δ_n + Ce^{−cu},  δ_n := 1 − π(S₀),   and   Π( d_H(f, f*) > C√(u/n) | S = S₀, D_n ) ≤ Ce^{−cu}.
Hence, if δ_n → 0 in P*-probability (e.g. under [W3P] Theorem 1, [P2] Claim A1 or Claim E with their beta-min
conditions) and the four design events have probability → 1, then for every M_n → ∞:
  Π( d_H(f, f*) > M_n/√n | D_n ) → 0 in P*-probability.
Notes. (i) No eigenvalue floor on S₀ is assumed ((F₀) of v1.0 dropped; no coefficient-recovery claim is made).
(ii) (TR₀) holds with probability → 1 for any C_T > 1 when the law of x_{supp β*} is fixed with finite second moments
(degenerate directions included); for triangular arrays it is an explicit assumption. (iii) Mere δ_n → 0 gives no
exponential control of the term δ_n, which is why the second display is in probability; no impossibility is claimed.

**Stretch statements (not target clauses; listed so the routes are on record).**
- **S-APX (approximate sparsity, [SL] (3)/(8)).** Replace S₀ by a reference (T, ϑ) with cost B_T(ϑ) ≤ B ([P2] Claim B;
  Lemma S is already stated in this form) and bias ‖μ − X_Tϑ‖² ≤ nΔ_n². Candidate: (1.1)/(1.2) with ε² + CΔ_n²; the
  out-of-sample part of the bias needs its own control.
- **S-EXP (exponential p).** Candidate: (1.1) with log n replaced by ℓ_n for ℓ_n = o(n^{κ₀}); Lemma S already has no
  p ≤ n^A restriction.
- **S-FIT (sharp rate with no design condition).** Without (ND), the posterior size has a geometric tail of ratio ≈ ½
  and no better (duplicate columns: [T03R] Proposition D; H1 F4), so the size clause of (1.1) is false in general. But
  near-duplicate columns fit almost no extra noise, so the *distance* clause of (1.1) may still hold without (ND)
  through a fit tail (effective dimension eᵀM_Se instead of |S|). OPEN. H1 derived (unchecked) the design-free
  superset bound Σ_{|J|=j} π(S₀∪J)/π(S₀) ≤ poly(j)(√(1+η)/2)^j·O_P(1) (Lemma V); non-supersets are open.

## 2. Candidate theorem for the method as coded (target (ii); P6)

**Code facts (pins; core = commit 4676af6, unchanged at fe9a1d7; scope: the output of the final SMC run — the separate
exact-enumeration branch is excluded, as in [SAMP]).** On a completed run the fit returns `hpm`
(`Scripts/SMC_BVS/core/v3_run.R:142`), `pip_r` and `pip_primary` (`:159-162`), `mpm` (`:163`), `log_Z` (`:154`), and
`top_store` (`:210`; `cpp/v3_core.cpp:358-366`): the 40p + 1 (p = p_ret) best-scored distinct models offered to the
final-run ledger (`cpp/v3_ledger.h:43-56, 78`) with their exact scores F(S) = log ϖ(S) + log m(S) ([CC] CC2, status
"CODE-CHECKED"). **The run returns no particles, no draws of (β, σ²) and no predictive distribution.** A
distribution has to be defined from the returned output:
- **Store BMA.** 𝒯 := `top_store` models; π_𝒯(S) := e^{F(S)}/Σ_{S′∈𝒯}e^{F(S′)}; Π̂^𝒯 := Σ_{S∈𝒯} π_𝒯(S) Π(· | S, D_n)
  (= Π(· | S ∈ 𝒯, D_n) under EX-A, exact arithmetic).
- **HPM plug-in.** Π̂^H := Π(· | S = Ŝ, D_n), Ŝ = `hpm` (the model is plugged in; its conditional parameter posterior
  is kept — no point estimate of parameters).
- **MPM plug-in.** Π̂^M := Π(· | S = MPM, D_n), MPM from `pip_primary` (when |MPM| ≤ K).
- More generally, any output-measurable law Q on Ω with the exact conditional kernels: QΠ := Σ_S Q(S)Π(· | S, D_n).
`pip_primary` is a vector of marginal probabilities, not a law on models; its consistency is [SAMP]'s selection-level
statement and is not restated.

**Theorem DIST-C (coded output; under P⊗; jointly with output; conditional as labelled).** Let B_n be the bad set of
(1.1) (or (1.2), with its rate) and q_n := e^{−ct}.
- (C-0) **Domination transfer (deterministic) [BT4].** If Q(S) ≤ L_n π(S) for all S ∈ Ω, then QΠ(B) ≤ L_n Π(B | D_n) for
  every measurable B. Store BMA: L_n = 1/π(𝒯). A single model Ŝ: L_n = 1/π(Ŝ).
- (C-i) **Store BMA.** For every λ ∈ [0, c): P⊗( {completed} ∩ {π(𝒯) ≥ e^{−λt}} ∩ {Π̂^𝒯(B_n) > e^{−(c−λ)t}} ) ≤
  3e^{−ct} + P*(interfaces fail); on the complementary success event the store-BMA predictive density satisfies
  d_H²(f̄^𝒯, f*) ≤ C²t/n + e^{−(c−λ)t}. (λ = 0, π(𝒯) ≥ η: the fixed-fraction case.)
- (C-ii) **When does the store hold enough mass?** (α) With selection: on {completed} ∩ {S₀ ∈ 𝓜} ∩ {δ_n < ½}, S₀ ∈ 𝒯
  and π(𝒯) > ½ (S₀ is then the unique maximiser of F and the top store keeps the best-scored offered model:
  `cpp/v3_ledger.h:49-56`; direct, no further premise). P⊗({completed} ∩ {S₀ ∉ 𝓜}) → 0 is supplied by [SAMP] Theorem D
  (D-i) with P-OVL (discovery by a π₀ draw; P-MAP is needed for identification, not for discovery), or by
  W3-RM2:RM2-F/RM2-R, under their own premises (ideal streams and algorithm premises retained). (β) Without beta-min:
  π(𝒯) ≥ e^{−λt} is a **premise (P-STORE)** about the run; the output does not certify it in general ([SAMP] LT-f).
- (C-iii) **HPM plug-in.** 𝔅_n := {S : Π(B_n | S, D_n) > q_n^{1/2}} has π(𝔅_n) ≤ q_n^{1/2} on the success event of DIST-1.
  If the final-run ledger contains a model S′ with π(S′) > q_n^{1/2} (**premise P-HIT**; implied by S₀ ∈ 𝓜 and δ_n < ½),
  then Ŝ ∉ 𝔅_n and Π̂^H(B_n) ≤ q_n^{1/2}. With selection ((α)), Ŝ = S₀ and Π̂^H = Π(· | S₀, D_n); **under the hypotheses of
  DIST-3 ((E), (L₀), (TR₀))** it satisfies DIST-3's second display (exponential oracle bound at √(u/n)).
- (C-iv) **MPM plug-in.** On {MPM = S₀} (P⊗-probability statements: [SAMP] LT-e, C-v, TR-d, under their premises),
  Π̂^M = Π(· | S₀, D_n); **under the hypotheses of DIST-3** the same oracle bound holds.
- **Honest label.** (C-0) and the deterministic parts of (C-i)–(C-iii) need no sampler premise. Everything that says
  the store or the ledger contains enough is conditional on a delivery premise (discovery of S₀, P-STORE, P-HIT) and
  is intersected with {completed}; P⊗(completed) → 1 is neither assumed nor claimed. Bad output events are contained in
  bad data events, so the data-only bounds extend to P⊗ without an independence assumption. EX-A for floating point.
  No statement is made about a particle approximation, because none is returned.

## 3. Key lemmas (stated precisely; ids as in DEPS.tsv)

**Lemma H (Hellinger reduction; deterministic).** For every (S, θ, v) with v > 0, with Δ(x) := (â + xᵀb) − (α* + xᵀβ*):
  d_H²(f_{S,θ,v}, f*) ≤ (v/σ*² − 1)² + E_x[min{1, Δ(x)²/(4σ*²)}].
*Proof.* Pointwise in x, H² = 1 − A·B(x) ≤ (1 − A) + (1 − B(x)); 1 − A ≤ 1 − A² = (√r − 1)²/(r + 1) ≤ (r − 1)², r = v/σ*²;
1 − B(x) = 1 − exp(−Δ(x)²/(4(v + σ*²))) ≤ min{1, Δ(x)²/(4σ*²)}. Integrate over ν_x. ∎ (S1: "SOUND-AS-STATED"; not a
line check.) In-sample: Δ_i := Δ(x_i) = ε̄ + (μ̂ − μ)_i, so n⁻¹Σ_iΔ_i² = ε̄² + ‖μ̂ − μ‖²/n, μ̂ = X_Sθ; valid when true
columns were dropped.

**Lemma T (distribution-free sample-to-population transfer on sparse directions) [S1-01].** Let x₁, …, x_n be i.i.d.
from any law on ℝ^{p_raw}, **1 ≤ d ≤ min(p_raw, n − 1)**, δ ∈ (0, 1). With probability ≥ 1 − δ, simultaneously for all
a ∈ ℝ, c > 0 and u ∈ ℝ^{p_raw} with |supp u| ≤ d:
  E_x[min{1, (a + uᵀx)²/c}] ≤ 2·n⁻¹Σ_i min{1, (a + uᵀx_i)²/c} + η²_n(d, δ),
  η²_n(d, δ) := (4/n)[d log(ep_raw/d) + 2(d + 1) log(2en/(d + 1)) + log(4/δ)]  (all three terms ≥ 0 on this range).
No moment, tail, small-ball or eigenvalue condition. *Route:* level sets {|a + uᵀx| > s} are unions of two affine
half-spaces of a d-dimensional coordinate subspace (supports of size < d are enlarged to size d); growth function ≤
C(p_raw, d)·(2en/(d+1))^{2(d+1)} at 2n points; relative deviation inequality
P(sup_A (P(A) − P_n(A))/√P(A) > η) ≤ 4 S(2n) e^{−nη²/4} (**attribution and constant to be verified or the inequality
proved in the proof leg** — S1 could not check the source); layer-cake and Cauchy–Schwarz give Pg − P_ng ≤ η√(Pg),
hence Pg ≤ 2P_ng + η². Applications use d = min(p_raw, n − 1, d_t + s₀^r) (DIST-1) and min(p_raw, n − 1, m_n(t) + s₀^r)
(DIST-2).

**Lemma S (size tail with an exponential tail; reference-adaptive; no p ≤ n^A) [BT3].** Fixed design with p ≥ 2,
noise G, ‖μ‖² ≤ nM. Let T ∈ Ω and ϑ ∈ ℝ^T be design-measurable with B_T(ϑ) := ‖μ − X_Tϑ‖² + (‖X_Tϑ‖² + ‖ϑ‖²)/n ≤ B.
There are C, c, n₀ depending on (σ*², M, B, κ₀) such that for n ≥ n₀, 1 ≤ t ≤ n^{1−κ₀} and every integer m with
  log R^T_m + ½ log D_T + ½ log n + C[1 + √t + t/√n] ≤ −2t   (R^T_m := Σ_{k>m} q_k/w(|T|)):
  P_ε[ π(|S| > m) > e^{−t} ] ≤ Ce^{−t} + Ce^{−cn}.
With T = S₀, ϑ = θ* (B = M + M′), R_m ≤ 2(2p)^{s₀}2^{−m} and D_{S₀} ≤ (n+1)^{s₀}, m = m_n(t) qualifies for t ≥ log n.
(Strengthens the tail of [W3P] Lemma 1a′ / [P2] Claim B, whose failure probability is of order 1/log L. S1:
"SOUND-AS-STATED" for the S₀-reference form; not a line check.)

**Lemma V (helper H1, unchecked).** For S = S₀ ∪ J ⊇ S₀ and η > 0: (a) Q_{S₀} − Q_S ≤ eᵀD′e + (1 + 2/η)ρ′ with
0 ⪯ D′, ‖D′‖ < 1; (b) E[(D_{S₀}/D_S)^{1/2} exp(eᵀD′e/(2σ*²))] ≤ (1 + η)^{s₀+|J|/2}; (c) eᵀD′e ≤ σ*²χ²_{d_J} + ‖P_{S₀}e‖².
No floor is used. (Exact definitions of D′, ρ′: H1 §3, A2.)

**Lemma X (in-sample exponential core; fixed design; the key new lemma) [S1-06].** Fixed design with p ≥ 2, any
s₀ ∈ {0, …, s₀^r} with s₀ ≤ K, noise G, p ≤ n^A. Under (E; M), (C; M′), (ND; c_D, m_n(t)): there are c, C, C′, M₀ and **one
n₀ valid for every t in the range**, such that for n ≥ n₀ and M₀ log n ≤ t ≤ n^{1−κ₀}, with d_t := s₀ + ⌈C′t/log n⌉:
  P_ε[ Π( ‖μ̂ − μ‖² > Cσ*²t  or  |v/σ*² − 1| > C√(t/n)  or  |S| > d_t | y ) > e^{−ct} ] ≤ 2e^{−ct}.
Structure: (X1) noise event; (X2) good models (|S| ≤ d_t, L_S ≤ C″σ*²t) have conditional mass ≤ e^{−ct} outside the
ball; (X3) small models with large ridge loss have total mass ≤ e^{−ct}π(S₀); (X4) models with |S| > d_t have total mass
≤ e^{−ct} with probability ≥ 1 − e^{−ct}: supersets by truncated Occam moments under (ND) with Lemma V — **paying the
factor exp(‖P_{S₀}e‖²/2σ*²) ≤ e^{C(t + s₀ log n)}, the union multiplicity 2^{s₀}(2p)^{s₀}(n+1)^{s₀/2} and the variance
surcharge ε_{n,t}(j log n + t), ε_{n,t} = O(√(t/n) + (m_n(t)+s₀) log n/n), before Markov** —; other large models through
their union with S₀; sizes above m_n(t) by Lemma S.

**Lemma X′ (the same without (ND)).** Under (E; M), (C; M′) only, with constants depending also on κ₀: the conclusion
of Lemma X holds with ‖μ̂ − μ‖² > Cσ*²tℓ_n and |S| > m_n(t) in place of ‖μ̂ − μ‖² > Cσ*²t and |S| > d_t (the variance
displacement O(tℓ_n/n) is absorbed in C√(t/n) since √(t/n)·ℓ_n → 0 on the range) [S1-07].

**Lemma P6 (deterministic).** (a) [BT4] If Q ≤ Lπ on Ω then QΠ(B) ≤ LΠ(B | D_n). (b) For **a > 0** and
𝔅 := {S : Π(B | S, D_n) > a}: π(𝔅) ≤ Π(B | D_n)/a [S1-11].

**Bridges (examples; candidates; not target clauses).**
- **B1 [S1-05].** If the coefficient-weighted true coordinates β*_j(x_j − E x_j), j ∈ supp β*, are uniformly sub-Gaussian
  with constant K_x (which controls xᵀβ* as well), then P*((E; M) ∩ (C; M′))ᶜ ≤ e^{−c(K_x)n} for M, M′ ≥ M(K_x). If only
  their second moments are bounded and uniformly integrable (or the law is fixed), P*((E; M) ∩ (C; M′)) → 1.
  (v1.0's version, with sub-Gaussian raw coordinates and signal only, is **false**: S1-05 counterexample.)
- **B2.** (ND) from population quantities (small-ball lower bound for sparse sample covariances; sparse condition
  number ≤ cn; control of max_j ŝ_j²/Var(x_j)). For Gaussian rows implied by W3-POST Corollary 1R (LSF). To be stated
  exactly in the proof leg.

## 4. Consumes table (claim id, recorded status, exact statement used)

| consumed | recorded status | used for | exact content used |
|---|---|---|---|
| W3-POST2:D (v1.1.0; D.D(a) 1.0.0, D.D(b) 1.2.0) | **HQ note 2026-11-15: "council-passed C1 (11-09); D(b) repaired after the council, single Sol check (PC2); diff round in progress"** (registry: "PROVED (by this seat, unchecked)") | Lemma H and X2 use only the computations D0, D1 (re-derived here); **D(a) is no longer consumed** (DIST-3 v1.1 is self-contained); **D(b) only in fallback F-b**, which is conditional on it (rule 11) | Lemma D0; D1(a)–(d); D(b) (fallback only) |
| W3-POST2:A0, A1 (1.0.0) | "PROVED (by this seat, unchecked)" | (ND) interface; X4 | (F_w) ⇒ (DG) ⇒ (ADG); truncated Occam weights a_J (re-derived with t-scaled truncation) |
| W3-POST2:B (1.0.0) | "PROVED (by this seat, unchecked)" | Lemma S (proof re-run with exponential tails) | Steps 1–4 of `B_tail_approx.md` |
| W3-POST2:E (1.0.0) | "PROVED (by this seat, unchecked)" | X3 (template) | Lemma E1(b) |
| W3-POST:Lemma-1a′ (1.0.0) | "PROVED (by this seat, unchecked)" | Lemma S (starting point) | design-free size tail |
| W3-POST:Thm-1 (1.0.0), item 6 | "T03♯: PROVED; SF VERIFIED (W2-VT03R); XF VERIFIED (A-REV2)" | DIST-3 (a source of δ_n → 0) | items 1, 6 |
| W3-POST:Cor-1R (1.0.0) | "PROVED (by this seat, unchecked)" | example for B2 | Gaussian rows + LSF ⇒ (F_w) events |
| T04 (`Docs/Theory/proofs/T04_A3_contraction/`) | "proved (Opus 5.5 lead; reviewed by 2 independent Opus 5.5 xhigh, CP + CW); not adopted"; **not in the registry** | route guide for X′ | **not consumed as a premise** |
| C-PACK SL0/SL2 (`Wave1C/C-PACK/lemmas/I4_SL_corollaries.md`) | "PROVED (by this seat, unchecked)", R34-checked; council C1 passed | DIST-C framing | SL0(iv) (δ < ½ ⇒ unique maximiser); SL2's store-restricted object |
| W3-SAMP:CC (1.1.1) | "CODE-CHECKED (lead; SL1, LC1, SW1, both council seats)" | code facts | CC2, CC3 |
| W3-SAMP:D (2.1.1), LT♯ (2.0.1), C (1.1.1), TR (2.1.1) | "PROVED-CHECKED" | DIST-C (C-ii)–(C-iv) delivery premises | D-i with P-OVL; LT-e; C-v; TR-d |
| W3-RM2:RM2-F, RM2-R (1.0.0) | "PROVED-CHECKED, conditional on SOP:TH09" / "… conditional on W2-APP:POST" | DIST-C (C-ii)(α), cited conditional alternative | S₀ ∈ 𝓜 jointly with output (not verified by S1: files outside its packet) |
| SOP:TH09 (1.0.0), W2-APP:POST (1.0.1), W1-PXN (P) | "T03♯: PROVED; SF VERIFIED …"; "PROVED (by this seat, unchecked); R02 VERIFIED-WITH-AMENDMENTS, applied"; "XF VERIFIED" | DIST-3 instances | δ_n = O_P(√(log n/n)) |
SOP:TH04 M4(c) is no longer consumed (retention is proved directly from the store order). Rule 11: every consumed
premise below PROVED-CHECKED is an explicit hypothesis of the result that uses it. DIST-1, DIST-2, DIST-3 and Lemmas H,
T, S, V, X, X′, P6 are planned **self-contained**: their only inherited premise is the identification of the coded
posterior with the contrast model (locked T01, [P1] `thm:T01i`, `lem:spec`, `lem:num`, `thm:Ta`).

## Changelog (PROTOCOL_v4 §4.2). Tags are the lead's; a reviewer confirms each non-EQUAL tag before the next freeze.

| version | clause | tag | reason | trigger (review file) | check (review file) |
|---|---|---|---|---|---|
| 1.0 | all | — | first version (baseline) | — | `reviews/S1_astra.md` (blind read of v1.0.2) |
| 1.0.1 | DIST-1, X, S: range of t | EQUAL (vs A1) | t ≤ n^{1−κ₀} instead of t ≤ c₀n (variance plug-in error near t ≍ n) | lead self-check | S1: range used throughout, no objection |
| 1.0.1 | §0: s₀ ≤ s₀^r | EQUAL | dropped true columns made explicit | lead self-check | S1-02, S1-07 (extended in 1.1) |
| 1.0.2 | stretch S-DIM → S-FIT | EQUAL (not a target) | size form refuted by duplicates | `work/prior_probe/REPORT.md` F4 | S1 "Checks" (duplicates) |
| 1.0.2 | Lemma V recorded | EQUAL | tool for X4 | `work/prior_probe/REPORT.md` §3 | pending (line check in the proof leg) |
| 1.1 | Lemma T: 1 ≤ d ≤ min(p_raw, n−1); η² with 2en | EQUAL (domain repair; applications unaffected) | T false as stated outside the growth bound's range | `reviews/S1_astra.md` S1-01 | pending |
| 1.1 | §0: p_raw vs p_ret; 𝒟_n in every remainder; cutoff X-measurable; s₀ = 0 covered | WEAKER (non-target: a used hypothesis made explicit — remainder gains P(p_ret < 2)) | posterior was ill-defined when dimensions differ | S1-02, S1-07 | pending |
| 1.1 | DIST-3: impossibility parenthesis deleted | EQUAL | false as a blanket claim | S1-03 | pending |
| 1.1 | DIST-3: (F₀) → (L₀); oracle exponential bound with additive δ_n | STRONGER | weaker hypothesis, stronger conclusion; no longer consumes W3-POST2 D(a) | S1 Better-theorem 1, 2 | pending |
| 1.1 | DIST-1(c), DIST-2: rate wording (1 + s₀^r, ℓ_n); "[SL] short by a logarithm" removed | EQUAL | quantifiers; comparison moved to TARGET.md | S1-04, S1-07 | pending |
| 1.1 | DIST-1: size clause added to the bad set | STRONGER | needed by the transfer; was implicit | S1-06 | pending |
| 1.1 | DIST-2, X′: κ₀ fixed; constants depend on it | EQUAL | quantifier | S1-07 | pending |
| 1.1 | Lemma S: reference-adaptive, no p ≤ n^A | STRONGER (lemma, non-target) | exact determinant; supports S-APX, S-EXP | S1 Better-theorem 3 | pending |
| 1.1 | DIST-C: P⊗; (C-0) domination; λ-budget in (C-i); DIST-3 hypotheses imported in (C-iii), (C-iv); scope = final SMC run; M4(c) not consumed | STRONGER ((C-0), (C-i)); EQUAL (rest) | general transfer; explicit premises | S1-08, Better-theorem 4 | pending |
| 1.1 | P6(b): a > 0; DIST-1(e): "success event" | EQUAL | literal qualifications | S1-11 | pending |
| 1.1 | Remark R1 (intercept) | EQUAL | post-processing extension, not a flat-prior model | S1-09 | pending |
| 1.1 | B1: weighted sub-Gaussian coordinates | WEAKER (bridge, non-target) | v1.0's B1 false (counterexample) | S1-05 | pending |
| 1.1 | consumes table: W3-POST2:D status | EQUAL | HQ note 2026-11-15 | HQ note | — |
No WEAKER row touches a target clause (TARGET.md §5).
