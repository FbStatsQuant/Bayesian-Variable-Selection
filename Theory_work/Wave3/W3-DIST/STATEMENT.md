# W3-DIST — STATEMENT (v1.4.8, 2026-11-16; lead: Claude Fable 5.2, Claude Third, high)

**Status: targets TC1–TC9 fixed by HQ at CP1; proofs are in `lemmas/` and `work/<stream>/`; the check state of every item is
in `DEPS.tsv` (a statement here is checked only if its row says OK).** v1.4 = v1.3.1 with the dispositions of the blind read S2
(`reviews/S2_sol.md`, `reviews/S2_disposition.md`) and the wording edits queued from the proof leg. v1.3 = v1.2 with the dispositions of the same-family pre-check P1 (`reviews/P1_opus_precheck.md`,
`reviews/P1_disposition.md`) and the lead's final form of the reader versions. v1.2 = v1.1 + reader versions
(§1R) and precise bridges (§3), after HQ steer A5. v1.1 = v1.0.2 with the
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
P* = law of the data; **P⊗** = joint law of the data and the algorithm's streams, as in [SAMP] §0 (used only in §2).
**Reading of the master statements [P5 E-01].** In (1.1), (1.2), DIST-3 and Lemmas X, X′, S the constants and n₀ depend
only on the listed constants, never on the law of the data: for each n ≥ n₀ the bound holds for every law in (RD) at
that n (the proofs are for a fixed design and are uniform over designs satisfying the interfaces).

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
- **(C; M′)** coefficient cost: ‖θ*‖² ≤ nM′. With (E) it bounds ρ′ := θ*ᵀ(G_{S₀} + I)θ*/n = (‖μ‖² + ‖θ*‖²)/n ≤ B := M + M′, which is
  what Lemma V(a) and step X4 of Lemma X use. The weaker **(L₀; B)**: L_{S₀} := μ_cᵀ(I − M_{S₀})μ_c ≤ B (implied by (E), (C)
  since L_{S₀} ≤ ρ′) suffices for DIST-3 and for Lemma S with reference S₀, but **not** for Lemma X [P6 C-7]. [(E) ∧ (F₀)
  give the far stronger ‖θ*‖² ≤ 1.5M/φ₀².]
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
- (c) **Rate (P3)**: ε_n² = C²M₀ log n/n, where C depends only on (A, σ*², M, M′) and M₀ ≤ 16 + 4(1 + s₀^r)(A + 1) + 3(M + M′)/(2σ*²)
  (`lemmas/DIST12.md` D.4, `lemmas/X.md` §0). So for fixed (σ*², M, M′), M₀ is of order (1 + s₀^r)(A + 1) and ε_n² is of order
  (1 + s₀^r) log p_raw/n when p_raw = n^A (the "1 +" is the intercept and the variance; s₀^r = 0 is covered; s₀^r is the raw
  sparsity) [S1-07, L6-01]. No beta-min and no identifiability condition ([SL] Condition 3 is not used).
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
**(TR₀; C_T)** be the X-event { E_x(a + wᵀx)² ≤ C_T · n⁻¹Σ_i(a + wᵀx_i)² for all a ∈ ℝ and all w supported on supp β* }.
There are c = 1, C = C(s₀^r, σ*², M, B, C_T, κ₀) and n₀ = n₀(s₀^r, σ*², M, B, κ₀) such that for every n ≥ n₀, every 1 ≤ u ≤ n^{1−κ₀}
and every design in 𝒟_n ∩ (E; M) ∩ (L₀; B) ∩ (TR₀; C_T) (M, B, C_T fixed) [P4],
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
- **S-FIT (sharp rate with no design condition).** Status after Proposition NEC (§3): at the level of the fixed-design
  core, the exponential form at the sharp radius is **false** without (ND) (posterior mass of order 1/n at radius of order
  log n). A random-design version of that counterexample is not written. What remains open is the in-probability form:
  whether Π(‖μ̂ − μ‖² > M_nσ*² log n | y) → 0 for every M_n → ∞ under (E), (C) alone (proved for supersets of S₀ and completely for
  s₀ = 0 in the API attempt `work/api_attempts/dist1b/F-a-r2.md`, unchecked; non-supersets open). Not pursued in this leg.

## 1R. Reader versions (PROGRAM "Readability"; PROTOCOL_v4 H6) — candidates; corollaries of §1–2 through the bridges of §3

Reader version = master theorem + bridges. Theorem A (i), (ii) = DIST-1 (1.1) + bridges B0, B1, B2; its "without (A4)"
sentence = DIST-2 (1.2) + B0, B1 (size clause from Lemma X′). Theorem B = DIST-3 + B0, B1, B2, B3, **conditional on
W3-POST:Thm-1@1.0.0** (selection consistency of the exact posterior; status "T03♯: PROVED; SF VERIFIED (W2-VT03R); XF
VERIFIED (A-REV2)"). Corollary C = DIST-C (C-0), (C-i), (C-ii)(α) + Theorem A. The form is the lead's choice (HQ's
settled note of 2026-11-15); the text between the rules is the proposed main-text wording, with no internal ids.
Review record: `DEPS.tsv` and the changelog.

---
**Setup.** We observe D_n = {(x_i, y_i) : i = 1, …, n}: n independent copies of a pair (x, y), where x ∈ ℝ^p is a
vector of p predictors and y is a real response. The number of predictors p may grow with n and may be much larger
than n; the law of (x, y) may change with n.

*What the method does.* (1) It removes the predictors that are constant in the sample, and centres and scales every
other predictor, and the response, by its sample mean and sample standard deviation. Let r be the number of predictors
that remain (r ≤ p). (2) On the standardised data it uses one fixed prior, with no tuning parameter: the number of
included predictors has the beta-binomial BB(1, r) distribution restricted to at most min(r, ⌊n/2⌋), and given that
number all sets S of that size are equally likely; given S and the noise variance, the coefficients of the predictors
in S are jointly normal with mean zero and covariance n × (noise variance) × (G_S + I)⁻¹, where G_S is the sample Gram
matrix of the standardised predictors in S and I is the identity matrix of the same size; the noise variance has an
inverse-gamma prior with shape 0.01 and rate 0.01. (3) The posterior is mapped back to the original units.
Π(· | D_n) denotes the resulting posterior distribution of (S, β, σ²): S is the set of included predictors, β ∈ ℝ^p the
coefficient vector in the original units (zero outside S and for removed predictors), and σ² the noise variance in the
original units. If fewer than two predictors remain, or the response is constant in the sample, the posterior is not
defined here; under the assumptions below such data sets have probability smaller than the exceptional probabilities
in the theorems and are counted in them (in particular r = p outside them).

*The distribution attached to a posterior draw.* A draw (S, β, σ²) defines a joint density f for a new pair (x, y): x
has its true distribution and, given x, y is normal with mean ȳ + (x − x̄)ᵀβ and variance σ², where ȳ and x̄ are the
sample means of the response and of the predictors. f* is the true joint density of (x, y).

*Notation.* d_H(f, g) = (1 − ∫√(fg))^{1/2} is the Hellinger distance between two densities. P* is the distribution of the
data D_n. sd(·), Var(·) and Corr(·) are population standard deviations, variances and correlation matrices.
z_j = (x_j − E x_j)/sd(x_j) is the j-th standardised predictor and z = (z_1, …, z_p). For a set T of predictors, x_T is
the sub-vector of x. λ_min(·) is the smallest eigenvalue of a symmetric matrix. |S| is the number of predictors in S.
log is the natural logarithm.

**Constants, the level M and the window q_n.** s ≥ 0 is an integer and A ≥ 1, K ≥ 1, c_ψ > 0, b̄ > 0 are constants; none
depends on n. Fix a number M ≥ 1, the *level*: a larger M gives a larger ball and a smaller exceptional probability.
The *window* is

    q_n = min{ p, ⌈C_q·M·log n⌉ },   where C_q = 2(s(A + 2) + 4)/log 2.

It is the largest number of predictors that assumptions (A3) and (A4) constrain jointly; for a fixed level M it is of
order log n. (K below is the constant of (A3); the cap on the model size is always written min(r, ⌊n/2⌋).)

**Assumptions.**
- **(A1) Gaussian linear model.** y = α* + xᵀβ* + ε, where ε is normal with mean 0 and variance σ*² > 0 and is independent
  of x. (α*, β*, σ* and the law of x may depend on n.)
- **(A2) Sparsity and dimension.** At most s coordinates of β* are nonzero, and 2 ≤ p ≤ n^A.
- **(A3) Sub-Gaussian predictors.** Every predictor has positive variance, and for every vector u ∈ ℝ^p with at most q_n
  nonzero entries and every real λ:   E exp(λ·uᵀz) ≤ exp(K²λ²·Var(uᵀz)/2).
- **(A4) No near-exact collinearity.** For every set T of at most q_n predictors:   λ_min(Corr(x_T)) ≥ c_ψ/n.
- **(A5) Bounded signal.** |β*_j|·sd(x_j) ≤ b̄·σ* for every j.
No lower bound on the nonzero coefficients is assumed (no beta-min condition), and no fixed lower bound on
eigenvalues: under (A4) predictors may be correlated up to 1 − c_ψ/n. ((A4) still makes sparse coefficient vectors
distinguishable in principle; the statement without (A4) below needs no such condition.)

**Theorem A (the posterior recovers the joint distribution of predictors and response).** There are constants c > 0,
C₁, M₀ and n₀, depending only on (s, A, K, c_ψ, b̄), such that the following holds whenever n ≥ n₀, M₀ ≤ M ≤ √n/log n and
(A1)–(A5) hold with the window q_n of this M:

    (i)   P*[ Π( d_H(f, f*) > √(M·log n / n) | D_n ) > n^{−cM} ] ≤ n^{−cM},

    (ii)  P*[ Π( |S| > s + C₁·M | D_n ) > n^{−cM} ] ≤ n^{−cM}.

In words. (i) Except on a set of data sets of probability at most n^{−cM}, the posterior gives probability at most
n^{−cM} to joint distributions farther than √(M log n/n) from the truth in Hellinger distance: the posterior contracts
at the rate √(log n/n). (ii) On the same data sets the posterior gives probability at most n^{−cM} to models with more
than s + C₁M predictors. Statement (ii) bounds the number of selected predictors; it does not say that they are the
true ones. The two exceptional sets of data sets can be taken to be the same set. The bounds are uniform over all laws
of the data that satisfy (A1)–(A5) with the given constants.

*Without (A4).* If (A4) is dropped, and (A3) is required only for single predictors (vectors u with one nonzero
entry), then (i) holds with the radius √(M·log n·log(p ∨ n)/n), which is larger by the factor √(log(p ∨ n)), and (ii) holds
with s + C₁·M·log n in place of s + C₁·M. (Here p ∨ n is the larger of p and n.)

*Example.* Jointly Gaussian predictors satisfy (A3) with K = 1; independent predictors satisfy it when each of them
satisfies it with a common constant K. (A4) holds for all large n whenever every q_n × q_n principal block of the correlation matrix has
smallest eigenvalue at least a fixed ψ > 0: for instance correlation ρ^{|j−k|} with |ρ| < 1, or equal correlation
ρ ∈ [0, 1).

**Theorem B (parametric rate when the true predictors are detectable).** Assume (A1)–(A5) with the window q_n of M = 1
and with exactly s ≥ 1 nonzero coordinates of β*, **and in addition**
- **(A6) Detectable signal.** (a) λ_min(Corr(x_T)) ≥ ψ for a constant ψ > 0 and every set T of at most (2A + 3)s + 2
  predictors; (b) min{ |β*_j|·sd(x_j)/σ* : β*_j ≠ 0 } ≥ b_n, where b_n > 0 and b_n²·n/log n → ∞.
Then for every sequence M_n → ∞:

    Π( d_H(f, f*) > M_n/√n | D_n ) → 0   in P*-probability.

**Corollary C (the output of the sampler).** The method uses a sequential Monte Carlo sampler to explore the models and to compute summaries
of the posterior; it does not compute the full posterior
(small problems that it solves by exact enumeration are not covered here). A run is *completed* when the method
reports the status "completed"; runs that stop early are not covered. The output of a completed run contains a list 𝒯
of at most 40r + 1 distinct models: the best-scoring models among those offered to the final run of the sampler —
the models scored in that run, together with models the method scored earlier and carries into it (its precomputed
tables for small groups of predictors, and models kept from its calibration stage). Each model in the list comes with
the logarithm of its unnormalised posterior weight, which we take to be computed in exact arithmetic. The output
contains no draws of (β, σ²). Let π(𝒯) be the posterior probability of the list, and let Π̂ — not computed by the method —
be the posterior restricted to the list: the models in 𝒯, weighted in proportion to the exponentials of their returned
log-weights, each with its exact conditional posterior distribution of (β, σ²). Under the conditions of Theorem A,
with P*-probability at least 1 − n^{−cM} over the data, **every** completed run (whatever its random numbers) with
π(𝒯) ≥ n^{−cM/2} satisfies

    Π̂( d_H(f, f*) > √(M·log n / n) ) ≤ n^{−cM/2}.

If a completed run scored the true model {j : β*_j ≠ 0} and the posterior probability of that model exceeds ½, then the
list contains it, it is the model the method reports as most probable, and π(𝒯) > ½. More generally π(𝒯) is the total
posterior probability of the listed models, and no single model needs to carry most of it: the posterior is in general
a mixture over many models (typically the true model together with many models that add one predictor to it), and the
condition above concerns the list as a whole. Whether the list carries enough posterior probability is a property of the
run: this corollary does not assert it, and the output does not certify it.

**Notation table.**
| symbol | meaning |
|---|---|
| n, p, r | number of observations; number of predictors (p ≤ n^A, possibly p ≫ n); number of predictors not constant in the sample |
| (x, y), D_n | a predictor vector and its response; the n observed pairs |
| α*, β*, σ* | true intercept, coefficient vector and noise standard deviation |
| s | maximal number of nonzero coordinates of β* |
| S, β, σ² | a set of included predictors, a coefficient vector and a noise variance (a posterior draw) |
| Π(· \| D_n) | the posterior distribution of (S, β, σ²) under the method's prior |
| f, f* | joint density of (x, y) defined by a posterior draw; true joint density |
| d_H | Hellinger distance, d_H(f, g) = (1 − ∫√(fg))^{1/2} |
| P* | distribution of the data |
| sd, Var, Corr | population standard deviation, variance, correlation matrix |
| z_j, z | standardised predictor (x_j − E x_j)/sd(x_j); the vector of all of them |
| x_T, λ_min | sub-vector of x for a set T of predictors; smallest eigenvalue |
| M, q_n | the level (M ≥ 1, chosen by the reader); the window min{p, ⌈C_q M log n⌉} |
| K, c_ψ, b̄, ψ, b_n | constants of (A3), (A4), (A5); eigenvalue bound and beta-min level (b_n > 0) of (A6) |
| c, C₁, M₀, n₀ | constants of Theorem A, depending only on (s, A, K, c_ψ, b̄) |
| 𝒯, π(𝒯), Π̂ | the sampler's returned list of models; its posterior probability; the posterior restricted to it |

---
Remarks (not part of the reader statements). (1) General radii: (i) holds for every ε_n with M₀ log n/n ≤ ε_n² ≤ n^{−1/2}
in the form P*[Π(d_H > ε_n | D_n) > e^{−c nε_n²}] ≤ e^{−c nε_n²}, provided (A3), (A4) hold on the window of the level M = nε_n²/log n,
i.e. min{p, ⌈C_q nε_n²⌉} [P5 E-03, S2-04]. (2) M ≤ √n/log n is the range t ≤ n^{1−κ₀} of (1.1) with κ₀ = ½. (3) Under (A3), with
probability ≥ 1 − 4p·e^{−cn/K⁴} no column is constant in the sample, so r = p_ret = p and s₀ = |supp β*|. (4) Constants: (1.1) is
applied at t = M log n/C² (C ≥ 1 its radius constant), so the reader constants are c_reader = c/(2C²), M₀,reader = C²M₀ and
**C₁ = max{C′/C², 1 + s + (sA + s + 5)/log 2}** (the second term serves the sentence without (A4)); the common exceptional
event comes from the joint bad set of (1.1) [P5 E-02, S2-04]. (5) The dependence of M₀ on (s, A, b̄, K, c_ψ) is not made
explicit. (6) The HPM/MPM plug-in versions of Corollary C are DIST-C (C-iii), (C-iv). (7) Why each assumption is there
and whether it is necessary: TARGET.md §6. (8) In §1R, K is the constant of (A3); elsewhere in this file K denotes the cap min(p, ⌊n/2⌋).

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
(1.1) (or (1.2), with its rate) and ϱ_n := e^{−ct} (n₀ enlarged so that ϱ_n ≤ ¼ on the range of t).
- (C-0) **Domination transfer (deterministic) [BT4].** If Q(S) ≤ L_n π(S) for all S ∈ Ω, then QΠ(B) ≤ L_n Π(B | D_n) for
  every measurable B. Store BMA: L_n = 1/π(𝒯). A single model Ŝ: L_n = 1/π(Ŝ).
- (C-i) **Store BMA.** For every λ ∈ [0, c): P⊗( {completed} ∩ {π(𝒯) ≥ e^{−λt}} ∩ {Π̂^𝒯(B_n) > e^{−(c−λ)t}} ) ≤
  3e^{−ct} + P*(interfaces fail); on {completed} ∩ {π(𝒯) ≥ e^{−λt}} ∩ {Π̂^𝒯(B_n) ≤ e^{−(c−λ)t}} the store-BMA predictive density satisfies
  d_H²(f̄^𝒯, f*) ≤ C²t/n + e^{−(c−λ)t}. Threshold form: for every a ∈ (0, 1], on the success event of DIST-1 every completed
  run with π(𝒯) ≥ a has Π̂^𝒯(B_n) ≤ ϱ_n/a (pathwise; proved in `work/D_output/P6_DISTC.md` as (C-i°)) [stream D SCR-2].
- (C-ii) **When does the store hold enough mass?** (α) With selection: on {completed} ∩ {S₀ ∈ 𝓜} ∩ {δ_n < ½}, S₀ ∈ 𝒯
  and π(𝒯) > ½ (S₀ is then the unique maximiser of F and the top store keeps the best-scored offered model:
  `cpp/v3_ledger.h:49-56`; direct, no further premise). P⊗({completed} ∩ {S₀ ∉ 𝓜}) → 0 is supplied by [SAMP] Theorem D
  (D-i) with P-OVL (discovery by a π₀ draw; P-MAP is needed for identification, not for discovery), or by
  W3-RM2:RM2-F/RM2-R — a **conditional alternative that no proof here uses** (two links unchecked: whether RM2's output
  event covers {completed}, and whether its reported model is `hpm`) [P3 D-01]. (β) Without beta-min:
  π(𝒯) ≥ e^{−λt} is a **premise (P-STORE)** about the run; the output does not certify it in general ([SAMP] LT-f).
  (γ) Description, not a claim: π(𝒯) = Σ_{S∈𝒯}π(S), and (C-0), (C-i) need no model of posterior probability above ½. The store law
  Π̂^𝒯 is in general **a mixture over many models** — typically S₀ and many supersets S₀ ∪ {j} — and (C-i) applies to it as
  it is (measured by the Engineering Department at n = 200, p = 10⁴–10⁵: the one-extra-variable supersets together weigh
  0.5–1.2 times S₀; `Docs/Experiments/P1M/DECISIONS.md` row D-17).
- (C-iii) **HPM plug-in.** 𝔅_n := {S : Π(B_n | S, D_n) > ϱ_n^{1/2}} has π(𝔅_n) ≤ ϱ_n^{1/2} on the success event of DIST-1.
  If the final-run ledger contains a model S′ with π(S′) > ϱ_n^{1/2} (**premise P-HIT**; implied by S₀ ∈ 𝓜 and δ_n < ½),
  then Ŝ ∉ 𝔅_n and Π̂^H(B_n) ≤ ϱ_n^{1/2}. With selection ((α)), Ŝ = S₀ and Π̂^H = Π(· | S₀, D_n); **under the hypotheses of
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
1 − B(x) = 1 − exp(−Δ(x)²/(4(v + σ*²))) ≤ min{1, Δ(x)²/(4σ*²)}. Integrate over ν_x. ∎ (not line-checked.) In-sample: Δ_i := Δ(x_i) = ε̄ + (μ̂ − μ)_i, so n⁻¹Σ_iΔ_i² = ε̄² + ‖μ̂ − μ‖²/n, μ̂ = X_Sθ; valid when true
columns were dropped.

**Lemma T (distribution-free sample-to-population transfer on sparse directions) [S1-01].** Let x₁, …, x_n be i.i.d.
from any law on ℝ^{p_raw}, **1 ≤ d ≤ min(p_raw, n − 1)**, δ ∈ (0, 1). With probability ≥ 1 − δ, simultaneously for all
a ∈ ℝ, c > 0 and u ∈ ℝ^{p_raw} with |supp u| ≤ d:
  E_x[min{1, (a + uᵀx)²/c}] ≤ 2·n⁻¹Σ_i min{1, (a + uᵀx_i)²/c} + η²_n(d, δ),
  η²_n(d, δ) := (4/n)[d log(ep_raw/d) + 2(d + 1) log(2en/(d + 1)) + log(4/δ)]  (all three terms ≥ 0 on this range).
No moment, tail, small-ball or eigenvalue condition. *Proof:* `work/B_transfer/T.md` — level sets {|a + uᵀx| > s} are unions
of two affine half-spaces on d coordinates (growth function ≤ C(p_raw, d)·(2en/(d+1))^{2(d+1)} at 2n points); a one-sided
inequality P(∃A: P(A) > 2P_n(A) + η²) ≤ 2S(2n)e^{−nη²/4} for nη² ≥ 25 is proved in that file (ghost sample with Cantelli's bound,
random swaps with Hoeffding's), with no external result; a layer-cake step gives the truncated loss. (The ratio-type
inequality quoted in v1.3 is not used.) [P4]
Applications (`lemmas/DIST12.md`) use the **deterministic** levels d₁ = min{p_raw, 2s₀^r + ⌈32t/log n⌉} (DIST-1) and
d₂ = min{p_raw, s₀^r + ⌈C_m t⌉} (DIST-2), both ≤ n − 1 for n ≥ n₀: Lemma T is stated for a fixed d, so d must not depend on the
sample through s₀ or p_ret [BR1-01].

**Lemma S (size tail with an exponential tail; reference-adaptive; no p ≤ n^A) [BT3].** Fixed design with p ≥ 2,
noise G, ‖μ‖² ≤ nM. Let T ∈ Ω and ϑ ∈ ℝ^T be design-measurable with B_T(ϑ) := ‖μ − X_Tϑ‖² + (‖X_Tϑ‖² + ‖ϑ‖²)/n ≤ B.
There are C, c, n₀ depending on (σ*², M, B, κ₀) such that for n ≥ n₀, 1 ≤ t ≤ n^{1−κ₀} and every integer m with
  log R^T_m + ½ log D_T + ½ log n + C[1 + √t + t/√n] ≤ −2t   (R^T_m := Σ_{k=max(m+1,0)}^{K} q_k/w(|T|), the sum stopping at the cap K [L5-02]):
  P_ε[ π(|S| > m) > e^{−t} ] ≤ Ce^{−t} + Ce^{−cn}.
With T = S₀, ϑ = θ* (B = M + M′), R_m ≤ 2(2p)^{s₀}2^{−m} and D_{S₀} ≤ (n+1)^{s₀}, m = m_n(t) qualifies for t ≥ log n.
(Strengthens the tail of [W3P] Lemma 1a′ / [P2] Claim B, whose failure probability is of order 1/log L.)

**Lemma V.** (Proof: `work/C_size/V.md`.) Q denotes the contrast-scale Q^c, ρ′ := θ*ᵀ(G_{S₀} + I)θ*/n. For S = S₀ ∪ J ⊇ S₀ and η > 0:
(a) Q_{S₀} − Q_S ≤ eᵀD′e + (1 + 2/η)ρ′ with
0 ⪯ D′, ‖D′‖ < 1; (b) E[(D_{S₀}/D_S)^{1/2} exp(eᵀD′e/(2σ*²))] ≤ (1 + η)^{s₀+|J|/2}; (c) eᵀD′e ≤ σ*²χ²_{d_J} + ‖P_{S₀}e‖².
No floor is used. (D′ := M_S^{(1/c)} − M_{S₀}^{(c)}, c = 1 + η, M_T^{(c)} := X_{c,T}(G_T + c(G_T + I)/n)⁻¹X_{c,T}ᵀ.) [P6 C-6]

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

**Proposition NEC (sharpness of Lemma X's hypothesis; fixed design; not a target clause).** (Proof: `lemmas/NEC.md`.) For
every n large enough there is a standardised design with p = ⌊√n⌋ + 1 columns such that, for the null truth (s₀ = 0, μ = 0; so
(E; M), (C; M′) hold for all M, M′ ≥ 0), for every integer k ≥ 1 and all n ≥ n₄(k):
P_e[Π(‖μ̂ − μ‖² ≥ (k/24)σ*² log n | y) ≥ c₄(k)/(2n)] ≥ 0.6, with c₄(k) > 0. Consequently the conclusion of Lemma X cannot hold under
(E), (C) alone, for any constants, even with its outer probability replaced by a sequence tending to 0: the distance
clause, not only the size clause, needs (ND) or a substitute. The design violates (ND), so Lemma X, (1.1) and every target
clause are untouched; Lemma X′ and (1.2) are not contradicted; nothing is asserted about a random-design statement or
about the in-probability form.

**Lemma P6 (deterministic).** (a) [BT4] If Q ≤ Lπ on Ω then QΠ(B) ≤ LΠ(B | D_n). (b) For **a > 0** and
𝔅 := {S : Π(B | S, D_n) > a}: π(𝔅) ≤ Π(B | D_n)/a [S1-11].

**Bridges (candidates; on the critical path of the reader versions since HQ steer A5; z_j := (x_j − E x_j)/sd(x_j)).**
- **B0 (scale; pathwise) [P1-05].** Put ỹ := (y^r − α*1)/σ*; it follows the unit-noise model with coefficients β*/σ* and
  intercept 0. By W3-MISR:R′@1.0.0 (a′) ("PROVED-CHECKED; council R2"), Π(· | x, y^r) is the image of Π(· | x, ỹ) under
  (S, θ, v) ↦ (S, σ*θ, σ*²v), for every data set on which the coded posterior is defined (non-constant response, at least
  one retained column) [S2-05]; the plug-in intercepts satisfy â(y^r) = α* + σ*·â(ỹ). Hence, draw by
  draw, d_H between the density built from (x, y^r) and f* equals d_H between the density built from (x, ỹ) and the
  unit-noise truth. So σ* = 1 without loss of generality (σ* may depend on n), with (E), (C) read in units of σ*².
- **B1 ((A3) for single coordinates, (A5) ⇒ 𝒟_n, (E), (C)).** If E exp(λz_j) ≤ exp(K²λ²/2) for all j ≤ p and λ ∈ ℝ, then
  for n ≥ 3, with probability ≥ 1 − 4p·exp(−c₁n/K⁴) (c₁ absolute): ½ ≤ ŝ_j²/Var(x_j) ≤ 2 for every j ≤ p. On this event no
  column is dropped (p_ret = p ≥ 2, s₀ = |supp β*|), and under (A5): ‖μ‖² ≤ 2s²b̄²σ*²·n and ‖θ*‖² ≤ 2sb̄²σ*², i.e. (E; 2s²b̄²) and
  (C; 2sb̄²) in units of σ*². (Triangle inequality ‖μ‖ ≤ Σ_j|β*_j|·ŝ_j√(n−1).) For DIST-2 only the coordinates in supp β*
  and two others are needed. (v1.0's B1 was false; v1.2's variant B1′ is dropped — it implied (A5).)
- **B2-core (sparse lower bound for the sample second moments, with an intercept) [P1-07].** Under (A3) with sparsity q,
  put q′ := min(q, p). If q′·log(ep/q′) ≤ c₂n/K⁴ then with probability ≥ 1 − exp(−c₂n/K⁴): for all a ∈ ℝ and all u with at
  most q nonzero entries, n⁻¹Σ_i(a + uᵀz_i)² ≥ ½(a² + Var(uᵀz)); in particular uᵀΣ̂^z u ≥ ½·uᵀCorr(x)u for the centred sample
  covariance Σ̂^z of the z's. (Net-plus-Bernstein argument; the intercept is handled by augmenting z with a constant.)
- **B2 ((A3), (A4) ⇒ (ND)).** On the events of B1 and B2-core, for every T with |T| ≤ q:
  λ_min(G_T) = (n − 1)·λ_min(R̂_T) ≥ (n − 1)·λ_min(Σ̂^z_T)/max_j(ŝ_j²/Var(x_j)) ≥ (n − 1)c_ψ/(4n) ≥ c_ψ/8. This is [W3P] (F_w; g₀) with
  g₀ = c_ψ/8 on all sets of size ≤ q, hence (DG) and (ND; c_D, m) with c_D = g₀/(1 + g₀) for every m with
  min{p, s₀ + m} ≤ q (only unions S₀ ∪ J inside [p] need control):
  by eigenvalue interlacing, D_{S∪{j}}/D_S ≥ φ(λ_min(G_{S∪{j}})) ≥ (n+1)g₀/(1+g₀), φ(λ) := ((n+1)λ + 1)/(λ + 1) increasing
  ([P2] A0's route; the Schur-complement formula of v1.2 was wrong, P1-04). Since ⌈C_qM log n⌉ ≥ m_n(M log n) + s for every
  n ≥ 2 and M ≥ 1, the window q_n = min{p, ⌈C_qM log n⌉} satisfies min{p, s₀ + m_n(M log n)} ≤ q_n (automatic when q_n = p), which is
  the (ND) of (1.1) at t ≤ M log n. (v1.3's phrase "q_n ≥ m_n(M log n) + s" was false for small p: stream E, S2-02.) For Gaussian rows compare W3-POST Corollary 1R, which
  needs ψ_n√n/(log n)^{3/2} → ∞; the multiplicative bound of B2-core is what allows ψ_n ≍ 1/n.
- **B3 (for Theorem B).** On the same events with the fixed floor ψ on sets of size ≤ (2A + 3)s + 2: (i) (TR₀; 2) holds
  (B2-core restricted to supp β*, intercept included); (ii) the events of [W3P] Theorem 1 item 6 hold with common
  constants: (E) from B1, (F_λ) with φ₀² = ψ/4 (sets S₀ ∪ J, |J| ≤ j₀ = ⌈(2A+1)s⌉ + 1), (F_w) with g₀ = c_ψ/8 on sets of
  size ≤ min{p, m♯_n + s₀} (≤ q_n for n large; automatic when q_n = p), and BM-∞ with the deterministic envelope
  b_n²nφ₀²/(2 log n) → ∞, which uses **b_n > 0** [S2-01] (θ*_j = ŝ_jβ*_j,
  ŝ_j² ≥ Var(x_j)/2). Hence δ_n → 0 in P*-probability (conditional on W3-POST:Thm-1), and (L₀) from (E), (C).
- Failure probabilities of B1–B3 are ≤ 5p·exp(−c n/K⁴) ≤ n^{−cM} for n ≥ n₀ uniformly in M ≤ √n/log n, which is what turns the
  remainder of (1.1) into the displays of Theorem A, with one n₀ for all M ≤ √n/log n.

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
| W3-MISR:R′ (1.0.0) | "PROVED-CHECKED; council R2, MANIFEST 217d6708…" | bridge B0 (σ* arbitrary) | (a′) equivariance of the parameter posterior; (b) reduction to unit noise |
SOP:TH04 M4(c) is no longer consumed (retention is proved directly from the store order). Rule 11: every consumed
premise below PROVED-CHECKED is an explicit hypothesis of the result that uses it. DIST-1, DIST-2, DIST-3 and Lemmas H,
T, S, V, X, X′, P6 are planned **self-contained**: their only inherited premise is the identification of the coded
posterior with the contrast model (locked T01, [P1] `thm:T01i`, `lem:spec`, `lem:num`, `thm:Ta`).

## Changelog (PROTOCOL_v4 §4.2). Tags are the lead's; a reviewer confirms each non-EQUAL tag before the next freeze.

| version | clause | tag | reason | trigger (review file) | check (review file) |
|---|---|---|---|---|---|
| 1.0 | all | — | first version (baseline) | — | `reviews/S1_astra.md` (blind read of v1.0.2) |
| 1.0.1 | DIST-1, X, S: range of t | EQUAL (vs A1) → **WEAKER in range** per S2 | t ≤ n^{1−κ₀} instead of t ≤ c₀n (variance plug-in error near t ≍ n) | lead self-check | `reviews/S2_sol.md`: CONTESTED — literally a narrower range; before CP1 (the CP1 baseline has t ≤ n^{1−κ₀}) |
| 1.0.1 | §0: s₀ ≤ s₀^r | EQUAL | dropped true columns made explicit | lead self-check | S1-02, S1-07 (extended in 1.1) |
| 1.0.2 | stretch S-DIM → S-FIT | EQUAL (not a target) | size form refuted by duplicates | `work/prior_probe/REPORT.md` F4 | S1 "Checks" (duplicates) |
| 1.0.2 | Lemma V recorded | EQUAL | tool for X4 | `work/prior_probe/REPORT.md` §3 | statement: `reviews/S2_sol.md` Part 2 (see the row "Statement-change check of v1.1–v1.3" below; before the CP1 baseline); proofs: the line checks listed in `REPORT.md` §2 |
| 1.1 | Lemma T: 1 ≤ d ≤ min(p_raw, n−1); η² with 2en | EQUAL (domain repair; applications unaffected) | T false as stated outside the growth bound's range | `reviews/S1_astra.md` S1-01 | statement: `reviews/S2_sol.md` Part 2 (see the row "Statement-change check of v1.1–v1.3" below; before the CP1 baseline); proofs: the line checks listed in `REPORT.md` §2 |
| 1.1 | §0: p_raw vs p_ret; 𝒟_n in every remainder; cutoff X-measurable; s₀ = 0 covered | WEAKER (non-target: a used hypothesis made explicit — remainder gains P(p_ret < 2)) | posterior was ill-defined when dimensions differ | S1-02, S1-07 | statement: `reviews/S2_sol.md` Part 2 (see the row "Statement-change check of v1.1–v1.3" below; before the CP1 baseline); proofs: the line checks listed in `REPORT.md` §2 |
| 1.1 | DIST-3: impossibility parenthesis deleted | EQUAL | false as a blanket claim | S1-03 | statement: `reviews/S2_sol.md` Part 2 (see the row "Statement-change check of v1.1–v1.3" below; before the CP1 baseline); proofs: the line checks listed in `REPORT.md` §2 |
| 1.1 | DIST-3: (F₀) → (L₀); oracle exponential bound with additive δ_n | STRONGER | weaker hypothesis, stronger conclusion; no longer consumes W3-POST2 D(a) | S1 Better-theorem 1, 2 | statement: `reviews/S2_sol.md` Part 2 (see the row "Statement-change check of v1.1–v1.3" below; before the CP1 baseline); proofs: the line checks listed in `REPORT.md` §2 |
| 1.1 | DIST-1(c), DIST-2: rate wording (1 + s₀^r, ℓ_n); "[SL] short by a logarithm" removed | EQUAL | quantifiers; comparison moved to TARGET.md | S1-04, S1-07 | statement: `reviews/S2_sol.md` Part 2 (see the row "Statement-change check of v1.1–v1.3" below; before the CP1 baseline); proofs: the line checks listed in `REPORT.md` §2 |
| 1.1 | DIST-1: size clause added to the bad set | STRONGER | needed by the transfer; was implicit | S1-06 | statement: `reviews/S2_sol.md` Part 2 (see the row "Statement-change check of v1.1–v1.3" below; before the CP1 baseline); proofs: the line checks listed in `REPORT.md` §2 |
| 1.1 | DIST-2, X′: κ₀ fixed; constants depend on it | EQUAL | quantifier | S1-07 | statement: `reviews/S2_sol.md` Part 2 (see the row "Statement-change check of v1.1–v1.3" below; before the CP1 baseline); proofs: the line checks listed in `REPORT.md` §2 |
| 1.1 | Lemma S: reference-adaptive, no p ≤ n^A | STRONGER (lemma, non-target) | exact determinant; supports S-APX, S-EXP | S1 Better-theorem 3 | statement: `reviews/S2_sol.md` Part 2 (see the row "Statement-change check of v1.1–v1.3" below; before the CP1 baseline); proofs: the line checks listed in `REPORT.md` §2 |
| 1.1 | DIST-C: P⊗; (C-0) domination; λ-budget in (C-i); DIST-3 hypotheses imported in (C-iii), (C-iv); scope = final SMC run; M4(c) not consumed | STRONGER ((C-0), (C-i)); EQUAL (rest) | general transfer; explicit premises | S1-08, Better-theorem 4 | statement: `reviews/S2_sol.md` Part 2 (see the row "Statement-change check of v1.1–v1.3" below; before the CP1 baseline); proofs: the line checks listed in `REPORT.md` §2 |
| 1.1 | P6(b): a > 0; DIST-1(e): "success event" | EQUAL | literal qualifications | S1-11 | statement: `reviews/S2_sol.md` Part 2 (see the row "Statement-change check of v1.1–v1.3" below; before the CP1 baseline); proofs: the line checks listed in `REPORT.md` §2 |
| 1.1 | Remark R1 (intercept) | EQUAL | post-processing extension, not a flat-prior model | S1-09 | statement: `reviews/S2_sol.md` Part 2 (see the row "Statement-change check of v1.1–v1.3" below; before the CP1 baseline); proofs: the line checks listed in `REPORT.md` §2 |
| 1.1 | B1: weighted sub-Gaussian coordinates | WEAKER (bridge, non-target) | v1.0's B1 false (counterexample) | S1-05 | statement: `reviews/S2_sol.md` Part 2 (see the row "Statement-change check of v1.1–v1.3" below; before the CP1 baseline); proofs: the line checks listed in `REPORT.md` §2 |
| 1.1 | consumes table: W3-POST2:D status | EQUAL | HQ note 2026-11-15 | HQ note | — |
| 1.2 | §1R reader versions: Theorem A, Theorem B, Corollary C | NEW-CLAIM (corollaries of §1–2 + bridges) | owner's readability rule | HQ steer A5 (PROGRAM "Readability", PROTOCOL_v4 H6) | statement: `reviews/S2_sol.md` Part 2 (see the row "Statement-change check of v1.1–v1.3" below; before the CP1 baseline); proofs: the line checks listed in `REPORT.md` §2 |
| 1.2 | bridges B0, B1 (primitive form), B2-core, B2, B3 stated; B1 of v1.1 kept as B1′ | NEW-CLAIM (B0, B2-core, B3); STRONGER (B1, B2 made precise) | bridges are on the critical path | HQ steer A5 | statement: `reviews/S2_sol.md` Part 2 (see the row "Statement-change check of v1.1–v1.3" below; before the CP1 baseline); proofs: the line checks listed in `REPORT.md` §2 |
| 1.2 | consumes: W3-MISR:R′@1.0.0 added; W3-POST:Thm-1 is a premise of Theorem B | EQUAL (master); conditional status of Theorem B stated | B0; Theorem B | HQ steer A5 | statement: `reviews/S2_sol.md` Part 2 (see the row "Statement-change check of v1.1–v1.3" below; before the CP1 baseline); proofs: the line checks listed in `REPORT.md` §2 |
| 1.3 | Theorem B: "(A4) and, in addition, (A6)" | EQUAL (intended meaning made explicit; the v1.2 wording was false if read as a replacement) | counterexample under the replacement reading | `reviews/P1_opus_precheck.md` P1-01 | statement: `reviews/S2_sol.md` Part 2 (see the row "Statement-change check of v1.1–v1.3" below; before the CP1 baseline); proofs: the line checks listed in `REPORT.md` §2 |
| 1.3 | Theorem A: M fixed before the assumptions; window q_n = min{p, ⌈C_qM log n⌉}; one n₀ | EQUAL | quantifier order | P1-03, P1-07 | statement: `reviews/S2_sol.md` Part 2 (see the row "Statement-change check of v1.1–v1.3" below; before the CP1 baseline); proofs: the line checks listed in `REPORT.md` §2 |
| 1.3 | Theorem A, Corollary C: range M ≤ √n/log n (was M ≤ √n) | WEAKER (reader clause, not yet fixed at CP1; range only) | P1-10 | P1-10 | statement: `reviews/S2_sol.md` Part 2 (see the row "Statement-change check of v1.1–v1.3" below; before the CP1 baseline); proofs: the line checks listed in `REPORT.md` §2 |
| 1.3 | Theorem A: display (ii) on posterior model size added | STRONGER (from the size clause of (1.1)) | lead (clarity of what is proved) | — | statement: `reviews/S2_sol.md` Part 2 (see the row "Statement-change check of v1.1–v1.3" below; before the CP1 baseline); proofs: the line checks listed in `REPORT.md` §2 |
| 1.3 | Setup: constant columns removed; σ² in original units; intercept ȳ + (x − x̄)ᵀβ per draw; triangular arrays; notation table | EQUAL | P1-06, P1-13 | P1-06, P1-13 | statement: `reviews/S2_sol.md` Part 2 (see the row "Statement-change check of v1.1–v1.3" below; before the CP1 baseline); proofs: the line checks listed in `REPORT.md` §2 |
| 1.3 | Corollary C: "completed", exact arithmetic, scope, run-uniform wording; retention sentence restored | EQUAL / STRONGER (retention: an evaluated true model with posterior probability > ½ is kept) | P1-09, P1-12 | P1-09, P1-12 | statement: `reviews/S2_sol.md` Part 2 (see the row "Statement-change check of v1.1–v1.3" below; before the CP1 baseline); proofs: the line checks listed in `REPORT.md` §2 |
| 1.3 | bridges: B0 pathwise; B1 n ≥ 3; B2-core with q ∧ p; B2 by interlacing; B1′ dropped | EQUAL (B0, B1, B2-core); repair of a wrong formula with the same conclusion (B2) | P1-04, P1-05, P1-07, P1-11, P1-14 | as listed | statement: `reviews/S2_sol.md` Part 2 (see the row "Statement-change check of v1.1–v1.3" below; before the CP1 baseline); proofs: the line checks listed in `REPORT.md` §2 |
| 1.3.1 | body annotations quoting earlier review verdicts removed (blind-read hygiene) | EQUAL (editorial only) | PROTOCOL_v4 standing rule | lead, before blind read S2 | — |
| — | **Statement-change check of v1.1–v1.3 by `reviews/S2_sol.md` (Part 2).** CONFIRMED: 1.1 raw/retained WEAKER; 1.1 DIST-3 STRONGER; 1.1 size clause STRONGER; 1.1 Lemma S STRONGER; 1.1 B1 WEAKER; 1.2 reader versions NEW-CLAIM; 1.3 M range WEAKER; 1.3 model-size display STRONGER; 1.3 retention STRONGER. CONTESTED or not assessable from the current text (mixed or EQUAL tags whose literal comparison needs the old wording): 1.0.1 t range; 1.1 DIST-C "rest"; 1.2 bridges "STRONGER"; 1.3 "(A4) and in addition" (literally stronger hypotheses than a replacement reading); 1.3 quantifiers of M; 1.3 Setup (see 1.4: p vs r); 1.3 B0–B2 repairs. All of these precede the CP1 baseline (v1.3). | — | — | — | `reviews/S2_sol.md` |
| 1.4 | §1R Setup: the prior uses r = the number of predictors not constant in the sample (BB(1, r), cap min(r, ⌊n/2⌋)); posterior undefined when r < 2 or the response is constant, counted in the exceptional probability | EQUAL for TC9's mathematics (definition made faithful to the code; v1.3 wrote p, which is a different prior on data sets with a dropped column — an event of probability ≤ 4p·e^{−cn/K⁴} under (A3)) | faithfulness to the coded prior | `reviews/S2_sol.md` S2-03 | `reviews/D1_sol_diff.md`: CONFIRMED (scoped to TC9) |
| 1.4 | §1R: "no identifiability condition" → "no beta-min and no fixed lower bound on eigenvalues" (with a note that (A4) makes sparse coefficients distinguishable in principle) | WEAKER (a descriptive sentence, not a clause of Theorem A; TC9's assumptions and displays unchanged) | (A4) is a weak sparse-injectivity condition | S2-07 | `reviews/D1_sol_diff.md`: CONFIRMED |
| 1.4 | Theorem A: "the two exceptional sets can be taken to be the same set"; window "of order log n for fixed M"; Example "jointly Gaussian", "common constant K" | EQUAL / STRONGER (joint event, from the joint bad set of (1.1)) | clarity | S2-04; P5 E-07 | `reviews/D1_sol_diff.md`: CONFIRMED |
| 1.4 | Theorem B (A6)(b): b_n > 0 | **WEAKER** (companion clause, non-target: a hypothesis is added; it turns a statement that was false as written — b_n = −1 counterexample — into a true one). Reported at the next checkpoint; no early checkpoint | missing positivity | S2-01 | `reviews/D1_sol_diff.md`: CONFIRMED |
| 1.4 | Corollary C: final-run scope; the list described as the best of the models offered to the final run (scored there or carried in); log-weights exponentiated; stopped runs not covered; 40r + 1; "reports as most probable"; "does not certify" | EQUAL (description made faithful to the code) and **STRONGER** (added conclusion: under the retention condition the true model is the model the method reports as most probable; proved in `work/D_output/COR_C.md` C2 and `work/D_output/P6_DISTC.md` Corollary R1; companion result, beyond what CP1 approved: **HQ go 2026-11-16**, PROTOCOL_v4 §4.2) [tag split per D1-04] | reader text said slightly more than the code delivers | stream D (RC-1…RC-5); P3 D-02, D-03; S2-06 | `reviews/D1_sol_diff.md`: the v1.4 tag EQUAL was CONTESTED (D1-04: the added conclusion is STRONGER; its proof is valid); tag corrected in v1.4.8: `reviews/D3_sol_diff.md` CONFIRMED |
| 1.4 | Remarks of §1R: general radii need the window at that level; constants (c, M₀, C₁ = max{…}); the v1.3 changelog's remark on the threshold n₀ withdrawn | EQUAL (constants, explanatory edits) and **WEAKER** (non-target, a remark: Remark (1) on general radii now requires (A3), (A4) on the window of the level M = nε_n²/log n; v1.3 claimed those radii without this) [tag split per D1-04] | constants | P5 E-02, E-03, E-04; S2-04 | `reviews/D1_sol_diff.md`: the v1.4 tag EQUAL was CONTESTED (D1-04); tag corrected in v1.4.8: `reviews/D3_sol_diff.md` CONFIRMED |
| 1.4 | §0: law-free reading of the master statements; (C) vs (L₀) sentence corrected | EQUAL (TC2–TC4, TC6, TC7 unchanged; a false explanatory sentence corrected) | P5 E-01; P6 C-7 | as listed | `reviews/D1_sol_diff.md`: CONFIRMED (scoped to the named targets) |
| 1.4 | DIST-3: c = 1, dependence of C (on C_T) and n₀ stated; direction renamed w | EQUAL | quantifiers | P4; stream B | `reviews/D1_sol_diff.md`: CONFIRMED |
| 1.4 | DIST-C: ϱ_n (name clash with the window); threshold form replaces the "λ = 0" parenthesis; (C-iii) needs ϱ_n ≤ ¼ (n₀ enlarged); RM2 route labelled conditional and unused; P⊗ per [SAMP] §0 | EQUAL (TC8's deterministic transfers unchanged; one incorrect parenthesis replaced by a proved form) | stream D SCR-1…SCR-5; P3 D-01 | as listed | `reviews/D1_sol_diff.md`: CONFIRMED (scoped to TC8); SCR-4 was not yet in the statement (D1-02): applied in v1.4.8 (`reviews/D3_sol_diff.md`: RESOLVED) |
| 1.4 | §3: Lemma T's route text points to the proved one-sided inequality; Lemma V with Q^c, ρ′, D′ defined | EQUAL (statements of Lemmas T, V unchanged) | P4; P6 C-6 | as listed | `reviews/D1_sol_diff.md`: CONFIRMED |
| 1.4 | §3 bridges (non-target): B2 and B3 window claims "q_n ≥ m_n + s" / "m♯_n + s ≤ q_n" replaced by min{p, s₀ + m} ≤ q_n; B3 requires b_n > 0; B0 restricted to data sets on which the posterior is defined | mixed [tag split per D1-04, D1-03]: **STRONGER** (B2: the determinant-to-(ND) implication now covers every m with min{p, s₀ + m} ≤ q_n, which contains the old range m ≤ q_n − s) and **WEAKER** (bridge remarks, non-target: B0 restricted to data sets on which the posterior is defined; B3 requires b_n > 0; false uncapped window claims withdrawn; the last bridge bullet states its failure bound uniformly for M ≤ √n/log n, where v1.3.1 said M ≤ √n). Theorem A's statement is unaffected | stream E; S2-01, S2-02, S2-05 | as listed | `reviews/D1_sol_diff.md`: the v1.4 tag WEAKER was CONTESTED (D1-04: mixed directions; D1-03: the range change of the last bullet was not recorded); corrected in v1.4.8: `reviews/D3_sol_diff.md` CONFIRMED |
| 1.4.1 | Lemma S: R^T_m written with its upper limit K | EQUAL (the proof's definition; with the sum to p the sentence "m = m_n(t) qualifies" would be false at the cap, while the probability bound is unaffected) | ambiguity | `reviews/L5_astra_SV.md` L5-02 | `reviews/D1_sol_diff.md`: CONFIRMED |
| 1.4.2 | Corollary C, opening sentence: "uses a sequential Monte Carlo sampler to explore the models and to compute summaries of the posterior; it does not compute the full posterior" | EQUAL (description of the method made accurate; companion clause) | the method does not compute the full posterior | `reviews/L2_sol_D.md` L2D-01 | `reviews/D1_sol_diff.md`: CONFIRMED |
| 1.4.3 | §3, sentence on the applications of Lemma T: deterministic sparsity levels d₁, d₂ | EQUAL (Lemma T's statement unchanged; the application is now valid as written). The proof of (1.1), (1.2) from Lemmas H, T, X, X′ is `lemmas/DIST12.md` (with the intercept event and C′ = 33) | Lemma T needs a deterministic d | `reviews/BR1_astra_break.md` BR1-01..03 | `reviews/D1_sol_diff.md`: CONFIRMED |
| 1.4.4 | §1R Remarks: the remark on the numerical size of the threshold n₀ removed from this file (owner's standing rule: all results are asymptotic and asymptotics are not framed as a limitation); the fact is kept as one internal line of REPORT.md, "explicit constants, not optimised" | EQUAL (a remark; no statement changes) | owner's rule | manager's note, 2026-11-15 | `reviews/D1_sol_diff.md`: CONFIRMED |
| 1.4.5 | §3: Proposition NEC added (sharpness of Lemma X's hypothesis (ND); fixed design); stretch item S-FIT restated accordingly | NEW-CLAIM (non-target; touches no target clause: the design violates (ND)) | necessity gate for (ND) | API attempt F-b-r2; `reviews/P7_opus_precheck_NEC.md` | `reviews/D1_sol_diff.md`: CONFIRMED (classification); proof: `reviews/L7_sol_NEC.md` VERIFIED |
| 1.4.6 | DIST-C (C-ii)(γ) added; Corollary C's closing sentences: the condition concerns the total posterior probability of the list, and the posterior is in general a mixture over many models | EQUAL (descriptive sentences; no statement relied on a point-mass posterior — (C-ii)(α) and the retention sentence use π(S₀) > ½ only as a sufficient condition) | cross-department finding: at moderate n the store law is a mixture over S₀ and many one-extra-variable supersets | Engineering via HQ and the manager (`Docs/Experiments/P1M/DECISIONS.md` D-17) | `reviews/D1_sol_diff.md`: CONFIRMED |
| 1.4.7 | DIST-1 (c): the dependence of the rate constant on the sparsity is written out (C free of s₀^r; explicit bound on M₀; raw sparsity s₀^r in place of s₀) | EQUAL on TC3 ("M₀ = O((1 + s₀^r)(A + 1))" is now proved as written, for fixed (σ*², M, M′); v1.3's sentence was not established by the proof files: the constants of `lemmas/X.md` v0.3 gave M₀ ≳ s log s and C growing with s). Proof files: `lemmas/X.md` v0.4, `lemmas/DIST12.md` v0.2 (constants only) | a claimed constant dependence was not established | `reviews/L6_sol_DIST12.md` L6-01 (MAJOR) | `reviews/D1_sol_diff.md`: **CONFIRMED (EQUAL on TC3)**; the repair VERIFIED (Part A items 1–7) |
| 1.4.8 | DIST-C (C-i): "on the complementary success event" replaced by the explicit event {completed} ∩ {π(𝒯) ≥ e^{−λt}} ∩ {Π̂^𝒯(B_n) ≤ e^{−(c−λ)t}}; changelog tags of three v1.4 rows split | EQUAL on TC8 (TC8 fixes the delivery statements "jointly with {completed} and under its named premise", which is this event; the loose phrase, read literally, also covered stopped runs and lists of small posterior probability, where nothing was proved or intended; the probability display and (C-0) are unchanged) | the statement did not match the proved form (`work/D_output/P6_DISTC.md` SCR-4) | `reviews/D1_sol_diff.md` D1-02, D1-03, D1-04 | `reviews/D3_sol_diff.md`: **CONFIRMED (EQUAL on TC8)**; D1-01 … D1-04 RESOLVED; Corollary C's reported-model conclusion VERIFIED |
Target clauses TC1–TC9 were fixed by HQ at CP1 (2026-11-15) in their v1.3 form; TC10 = companion results. **Relative to that
baseline, no row of v1.4 weakens the mathematics of a target clause** (per S2: this sentence is about the CP1 baseline, not
about the history before it — the pre-CP1 rows 1.0.1, 1.1 and 1.3 marked WEAKER did narrow ranges or add remainder events).
