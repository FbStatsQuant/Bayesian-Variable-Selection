# Theorems DIST-1 and DIST-2 — proof from Lemmas H, T, X, X′ (W3-DIST, stream A; lead: Claude Fable 5.2)

Status: **DRAFT (by this seat)**. v0.2, 2026-11-15 (v0.2: the constant C_T and the paragraph on the dependence on the sparsity). Statements: `../STATEMENT.md` §1, displays (1.1) and (1.2) (target clauses
TC1–TC4, TC6), with §0 for the setting (RD), the retained dimension, the interfaces and the cutoff m_n(t).
Inputs, used exactly as stated in `../STATEMENT.md` §3: Lemma H (proof `../work/B_transfer/H.md`), Lemma T (proof
`../work/B_transfer/T.md`), Lemma X and Lemma X′ (proofs `X.md` §0–§7 and §9). Nothing else is used. Three points of the
passage that an earlier sketch left open are written out here: the sparsity level at which Lemma T is applied is
deterministic (D.1); the sample mean of the noise is controlled by its own event (D.2); the size clause of (1.1) uses a
constant that absorbs the rounding in Lemma X (D.5).

## D.0 Notation and conventions
(RD) holds: rows i.i.d., ε ~ N_n(0, σ²I) (σ := σ*) independent of the raw design X^r; s := s₀^r = |supp β*|; p_raw ≤ n^A.
Given X^r, the retained standardised design X, p = p_ret, θ*, S₀, s₀ ≤ s, μ, K and m_n(t) are deterministic; the contrast
noise e = Uᵀε ~ N_N(0, σ²I), N = n − 1, and ε̄ := n⁻¹Σ_iε_i ~ N(0, σ²/n) (these two are independent, which is not used).
Π(· | D_n) is the posterior of (S, θ, v) of STATEMENT §0; by the locked T01 it is the contrast-model posterior of
`../API_CARDS.md` "Common definitions", so Lemmas X, X′ apply to it given X^r. For a draw (S, θ, v): b_j = θ_j/ŝ_j (0 off S
and on dropped columns), â = ȳ^r − x̄ᵀb, Δ(x) = (â + xᵀb) − (α* + xᵀβ*) = a + uᵀx with a := â − α* and u := b − β*, and μ̂ = X_Sθ.
The support of u is contained in S ∪ supp β*, so |supp u| ≤ |S| + s. Constants of Lemma X: c_X = ½, C_X, C′_X = 32, M₀, n₀
(depending on (s, A, σ², M, M′, c_D, κ₀)); of Lemma X′: c = ½, C_{X′}, M₀′, n₀′ (depending on (s, A, σ², M, M′, κ₀)); C_m is the
constant of `X.md` §0 with m_n(t) + s₀ ≤ C_m t. Throughout t ≥ 16 and log n ≤ t (both hold for t ≥ M₀ log n, M₀ ≥ 16, n ≥ 3).

## D.1 The deterministic sparsity levels and the transfer event
For fixed n and t put
  d₁ := min{p_raw, 2s + ⌈32t/log n⌉},   d₂ := min{p_raw, s + ⌈C_m t⌉}.
Both are deterministic. Let n_T be such that for n ≥ n_T and every t ≤ n^{1−κ₀}: 2s + ⌈32t/log n⌉ ≤ n − 1 and s + ⌈C_m t⌉ ≤ n − 1
(possible since t ≤ n^{1−κ₀} = o(n)); then 1 ≤ d_i ≤ min(p_raw, n − 1) (d_i ≥ 1 because p_raw ≥ 2 on 𝒟_n ≠ ∅ and the other
terms are ≥ 1), which is the range of Lemma T. Let 𝒯_{i,t}, i = 1, 2, be the event of Lemma T for d = d_i and δ = e^{−t}:
it depends on X^r only, P*(𝒯_{i,t}ᶜ) ≤ e^{−t}, and on it, for all a ∈ ℝ, all u with |supp u| ≤ d_i and c = 4σ²:
  E_x min{1, (a + uᵀx)²/(4σ²)} ≤ 2n⁻¹Σ_i min{1, (a + uᵀx_i)²/(4σ²)} + η²_n(d_i, e^{−t}).
*Bounds on the remainders.* η²_n(d, e^{−t}) = (4/n)[d log(ep_raw/d) + 2(d + 1) log(2en/(d + 1)) + log 4 + t]. Using
log(ep_raw/d) ≤ 1 + A log n ≤ (A + 1) log n, log(2en/(d + 1)) ≤ log(2e) + log n ≤ 3 log n (n ≥ 3), log 4 ≤ t:
  η²_n(d, e^{−t}) ≤ (4/n)[(A + 7) d log n + 6 log n + 2t].
For d₁ (in D.4, where t ≥ M₀ log n and M₀ ≥ (A + 1)s ≥ 2s): d₁ log n ≤ 2s log n + log n + 32t ≤ t + t + 32t = 34t (2s log n ≤ 2st/M₀ ≤ t).
Hence **η²_n(d₁, e^{−t}) ≤ C_T t/n**, **C_T := 4[34(A + 7) + 8]**, which does not depend on s [v0.2; v0.1 had (2s + 33)].
For d₂: d₂ ≤ s + 1 + C_m t ≤ (s + 1 + C_m)t. Hence **η²_n(d₂, e^{−t}) ≤ C_T′ t log n/n ≤ C_T′ tℓ_n/n**, C_T′ := 4[(A + 7)(s + 1 + C_m) + 8]
(ℓ_n = log(p_raw ∨ n) ≥ log n).

## D.2 The intercept event
𝓘_t := {ε̄² ≤ 2σ²t/n}. Since √n ε̄/σ ~ N(0, 1): P*(𝓘_tᶜ) = P(|N(0, 1)| > √(2t)) ≤ 2e^{−t}. (Lemma X controls only e = Uᵀε; the
plug-in intercept involves ε̄, which the contrast posterior does not see.)

## D.3 The pointwise bound on the Hellinger distance
Let (S, θ, v) be any triple with v > 0 and |supp u| ≤ d_i. By Lemma H and its in-sample identity
(n⁻¹Σ_iΔ_i² = ε̄² + ‖μ̂ − μ‖²/n), on 𝒯_{i,t} (note |supp u| ≤ min{p_raw, |S| + s} always):
  d_H²(f_{S,θ,v}, f*) ≤ (v/σ² − 1)² + E_x min{1, Δ(x)²/(4σ²)}
       ≤ (v/σ² − 1)² + 2n⁻¹Σ_i min{1, Δ_i²/(4σ²)} + η²_n(d_i, e^{−t})
       ≤ (v/σ² − 1)² + (ε̄² + ‖μ̂ − μ‖²/n)/(2σ²) + η²_n(d_i, e^{−t}).                                   (D.3)

## D.4 Proof of (1.1) (Theorem DIST-1)
Let n ≥ max(n₀, n_T), M₀ log n ≤ t ≤ n^{1−κ₀}, and let G_t be the X^r-measurable event 𝒟_n ∩ (E; M) ∩ (C; M′) ∩ (ND; c_D, m_n(t)).
Put d_t := s₀ + ⌈32t/log n⌉ and Bad_X := {‖μ̂ − μ‖² > C_Xσ²t} ∪ {|v/σ² − 1| > C_X√(t/n)} ∪ {|S| > d_t}.
*Step 1 (Lemma X given the design).* On G_t the hypotheses of Lemma X hold for the retained design (p ≥ 2, p ≤ p_raw ≤ n^A,
s₀ ≤ s, s₀ ≤ K as n ≥ 2s). Lemma X's constants do not depend on the design, so with 𝓗_t := {Π(Bad_X | D_n) ≤ e^{−t/2}}:
P*(𝓗_tᶜ | X^r) ≤ 2e^{−t/2} on G_t, hence P*(G_t ∩ 𝓗_tᶜ) ≤ 2e^{−t/2} (ε is independent of X^r).
*Step 2 (inclusion of bad sets).* Let C′ := 33 and C := (C_X² + C_X/2 + 1 + C_T)^{1/2}. On 𝒯_{1,t} ∩ 𝓘_t, every triple outside Bad_X
satisfies: (a) |S| ≤ d_t ≤ s₀ + 32t/log n + 1 ≤ s₀ + 33t/log n, since t/log n ≥ M₀ ≥ 1; (b) |S| + s ≤ s₀ + s + ⌈32t/log n⌉ ≤
2s + ⌈32t/log n⌉, so |supp u| ≤ d₁ and (D.3) applies with i = 1:
  d_H² ≤ C_X²t/n + (2σ²t/n + C_Xσ²t/n)/(2σ²) + C_T t/n = (C_X² + 1 + C_X/2 + C_T)t/n = C²t/n.
So {d_H(f, f*) > C√(t/n)} ∪ {|S| > s₀ + C′t/log n} ⊆ Bad_X on 𝒯_{1,t} ∩ 𝓘_t.
*Step 3 (probability).* On G_t ∩ 𝒯_{1,t} ∩ 𝓘_t ∩ 𝓗_t: Π(d_H > C√(t/n) or |S| > s₀ + C′t/log n | D_n) ≤ Π(Bad_X | D_n) ≤ e^{−t/2}. And
  P*((G_t ∩ 𝒯_{1,t} ∩ 𝓘_t ∩ 𝓗_t)ᶜ) ≤ P*(G_tᶜ) + e^{−t} + 2e^{−t} + 2e^{−t/2} ≤ P*(G_tᶜ) + 3e^{−t/2}
(3e^{−t} ≤ e^{−t/2} for t ≥ 2 log 3). This is (1.1) with **c = ½, C′ = 33**, C as above, and the remainder
P*(G_tᶜ) = P*(𝒟_nᶜ ∪ (E; M)ᶜ ∪ (C; M′)ᶜ ∪ (ND; c_D, m_n(t))ᶜ). No independence between 𝒯_{1,t} and G_t is used. ∎
*Dependence of constants.* c, C, C′, M₀ and max(n₀, n_T) depend only on (s, A, σ², M, M′, c_D, κ₀) and not on the law of the
data: for each such n the bound holds for every law in (RD).
*Dependence on the sparsity [v0.2].* By `X.md` §0 (v0.4), C_X depends on (A, σ², M, M′) only, and so does
C = (C_X² + C_X/2 + 1 + C_T)^{1/2}; c = ½ and C′ = 33 are absolute; and M₀ ≤ 16 + 4(1 + s)(A + 1) + 3(M + M′)/(2σ²). Hence at
t = M₀ log n: ε_n² = C²M₀ log n/n ≤ C²[16 + 4(1 + s)(A + 1) + 3(M + M′)/(2σ²)]·log n/n, with s = s₀^r the raw sparsity (the transfer
step uses the raw support). For fixed (σ², M, M′) this is of order (1 + s₀^r)(A + 1) log n/n, i.e. (1 + s₀^r) log p_raw/n when
p_raw = n^A. (c_D and κ₀ enter only n₀.)
*Consequences (a)–(e) of STATEMENT.* (a), (b): substitute ε_n = C√(t/n) and bound or let the remainder tend to 0. (c): take
t = M₀ log n and use the preceding paragraph. (d): 𝒯_{1,t} has probability ≥ 1 − e^{−t} for every ν_x. (e): on the success event,
d_H²(f̄, f*) ≤ ∫d_H²(f, f*)dΠ ≤ C²t/n + Π(d_H > C√(t/n) | D_n) ≤ C²t/n + e^{−t/2}, by convexity of f ↦ d_H²(f, f*)
(`../work/D_output/P6_DISTC.md`, Lemma P6(c)) and d_H² ≤ 1.

## D.5 Remark on the size constant
Lemma X bounds the mass of {|S| > s₀ + ⌈32t/log n⌉}. The set {|S| > s₀ + 32t/log n} is **larger** when 32t/log n is not an
integer, so (1.1) cannot be stated with C′ = 32; with C′ = 33 the inclusion of Step 2(a) holds. (1.1) asserts the
existence of C′, so its hypotheses and rate are unchanged.

## D.6 Proof of (1.2) (Theorem DIST-2)
Let n ≥ max(n₀′, n_T), M₀′ log n ≤ t ≤ n^{1−κ₀}, G_t′ := 𝒟_n ∩ (E; M) ∩ (C; M′), and
Bad_{X′} := {‖μ̂ − μ‖² > C_{X′}σ²tℓ_n} ∪ {|v/σ² − 1| > C_{X′}√(t/n)} ∪ {|S| > m_n(t)}. As in Step 1, by Lemma X′ (no (ND)):
P*(G_t′ ∩ {Π(Bad_{X′} | D_n) > e^{−t/2}}) ≤ 2e^{−t/2}. On 𝒯_{2,t} ∩ 𝓘_t, a triple outside Bad_{X′} has |S| ≤ m_n(t), so
|S| + s ≤ m_n(t) + s₀ + s ≤ C_m t + s ≤ s + ⌈C_m t⌉ and |supp u| ≤ d₂; (D.3) with i = 2 gives
  d_H² ≤ C_{X′}²t/n + (2σ²t/n + C_{X′}σ²tℓ_n/n)/(2σ²) + C_T′tℓ_n/n ≤ (C_{X′}² + 1 + C_{X′}/2 + C_T′)·tℓ_n/n =: C₂²·tℓ_n/n
(t/n ≤ tℓ_n/n as ℓ_n ≥ log n ≥ 1). So {d_H > C₂√(tℓ_n/n)} ⊆ Bad_{X′} on 𝒯_{2,t} ∩ 𝓘_t, and the probability budget of Step 3
gives (1.2) with c = ½ and remainder P*(𝒟_nᶜ ∪ (E; M)ᶜ ∪ (C; M′)ᶜ). ∎
(The size statement Π(|S| > m_n(t) | D_n) ≤ e^{−t/2} holds on the same event; it is used by the reader version's sentence
without the non-collinearity assumption.)

## D.7 What is used
Lemma X / X′ (fixed design; constants free of the design); Lemma H; Lemma T at a deterministic sparsity level and with
c = 4σ²; the Gaussian law of ε̄; independence of ε and X^r. Not used: any condition on ν_x, any eigenvalue condition,
beta-min, identifiability. The raw dimension p_raw (not p_ret) enters Lemma T; p_ret enters Lemmas X, X′.
