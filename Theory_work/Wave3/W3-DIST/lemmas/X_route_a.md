# Lemma X — second, independent route (truncated Occam moments) (W3-DIST, stream A; lead: Claude Fable 5.2)

**Role:** written by the lead before the API attempts arrived; kept as an independent derivation of Lemma X for
comparison. The main proof is `X.md` (fractional-moment route). This file is not on the critical path.

Status: **DRAFT (by this seat, unchecked)**. v0.1, 2026-11-15. Statement: `../STATEMENT.md` §3 (Lemma X, Lemma X′), target
clause TC2–TC4 depend on it. This file proves steps X1, X3, X4 and the assembly; step X2 and Lemmas S, V are inputs
(stream C: `../work/C_size/X12.md`, `S.md`, `V.md`), used exactly in the form (I-X2), (I-S), (I-V) below — when those
files arrive, their statements must match these forms or this file changes.

## 0. Setting, notation, inputs
Fixed design. Notation of `../API_CARDS.md` "Common definitions": N = n − 1, y_c = μ_c + e, e ~ N_N(0, σ²I) (σ := σ*),
G_S, H_S, D_S, M_S, P_S, Q_S := Q^c_S, L_S, a_S := (I − M_S)μ_c, ν = 0.01 + n/2, b = 0.01·s_y², s_y² = ‖y_c‖²/N,
π(S) ∝ w(|S|)D_S^{−1/2}(2b + Q_S)^{−ν} on Ω = {|S| ≤ K}. p ≥ 2, p ≤ n^A, A ≥ 1; s₀ = |S₀| ∈ {0, …, s₀^r}, s₀ ≤ K; ℓ := log n;
κ₀ ∈ (0, 1) fixed. Interfaces: (E; M) ‖μ‖² ≤ nM; (C; M′) ‖θ*‖² ≤ nM′; B := M + M′; (ND; c_D, m). m := m_n(t),
m̄ := min(p, m + s₀). For J ⊆ [p]∖S₀: U_J := S₀ ∪ J, d_J := rank(P_{U_J} − P_{S₀}) ≤ |J|, χ²_J := ‖(P_{U_J} − P_{S₀})e‖²/σ².
τ(k) := C_Akℓ + 6t with C_A := 3A + 5.

**Elementary facts (each with its one-line reason).**
- (F1) D_S = Π_iφ(λ_i(G_S)), φ(λ) := ((n+1)λ + 1)/(λ + 1), increasing, 1 ≤ φ < n + 1 ([P1] `lem:spec`(e)). Hence
  1 ≤ D_S ≤ (n+1)^{|S|}, and for k ∉ S: 1 ≤ D_{S∪{k}}/D_S ≤ n + 1. *Reason for the last:* the eigenvalues λ′₁ ≥ … ≥ λ′_{r+1}
  of G_{S∪{k}} interlace those λ₁ ≥ … ≥ λ_r of G_S (λ′_i ≥ λ_i ≥ λ′_{i+1}), so
  D_{S∪{k}}/D_S = φ(λ′₁)·Π_{i=1}^{r}[φ(λ′_{i+1})/φ(λ_i)] ≤ φ(λ′₁) < n + 1, and = φ(λ′_{r+1})·Π_{i=1}^{r}[φ(λ′_i)/φ(λ_i)] ≥ 1.
- (F2) Q_S = min_φ{‖y_c − X_{c,S}φ‖² + φᵀ(G_S + I)φ/n} ([P1] `lem:slab`). Hence S ⊆ S′ ⇒ Q_{S′} ≤ Q_S (pad φ with zeros), and
  Q_S ≥ ‖(I − P_S)y_c‖².
- (F3) Q_S = ‖e‖² − eᵀM_Se + 2eᵀa_S + L_S, 0 ≤ eᵀM_Se ≤ ‖P_Se‖², ‖a_S‖² ≤ L_S (expand y_cᵀ(I − M_S)y_c; 0 ⪯ M_S ⪯ P_S;
  (I − M_S)² ⪯ I − M_S). L_{S₀} ≤ B (take φ = θ*_{S₀} in (F2) applied to μ_c: L_{S₀} ≤ (‖μ‖² + ‖θ*‖²)/n).
- (F4) Prior ratios. q_k := C(p, k)w(k). Σ_{k≤K}q_k ≤ 1 and 1/w(s₀) = 2C(2p−1, s₀) ≤ 2(2p)^{s₀}. For 0 ≤ k < k′ ≤ p:
  w(k)/w(k′) = C(2p−1, k′)/C(2p−1, k) ≤ (2p)^{k′−k}. For 1 ≤ j ≤ p − s₀:
  [w(s₀+j)/w(s₀)]·C(p − s₀, j) = C(s₀+j, j)·Π_{i=0}^{j−1}(p − s₀ − i)/(2p − 1 − s₀ − i) ≤ (4/3)(j+1)^{s₀}2^{−j}
  (each factor is ≤ ½ when s₀ + i ≥ 1; the factor with s₀ = i = 0 is p/(2p−1) ≤ 2/3; C(s₀+j, j) ≤ (j+1)^{s₀}).
- (F5) Truncated moment. For integers 0 ≤ d ≤ j, j ≥ 1 and τ ≥ j: E[e^{χ²_d/2}1{χ²_d ≤ τ}] ≤ (eτ/j)^{j/2}. *Reason:* for d ≥ 1
  the left side is ∫₀^τ x^{d/2−1}dx/(2^{d/2}Γ(d/2)) = (τ/2)^{d/2}/Γ(d/2 + 1) ≤ (eτ/d)^{d/2} (Γ(x+1) ≥ (x/e)^x); and
  d ↦ (eτ/d)^{d/2} is non-decreasing on (0, τ] (derivative of its logarithm: ½ log(τ/d) ≥ 0), so it is ≤ (eτ/j)^{j/2} as
  d ≤ j ≤ τ. For d = 0 the left side is 1 ≤ (eτ/j)^{j/2}.
- (F6) χ² and Gaussian tails (Laurent–Massart): P(χ²_k ≥ k + 2√(kx) + 2x) ≤ e^{−x}, P(χ²_k ≤ k − 2√(kx)) ≤ e^{−x},
  P(|g| ≥ √(2x)) ≤ 2e^{−x} for g ~ N(0, 1), x > 0.

**Inputs from stream C (to be matched against the delivered files).**
- (I-X2) There is C_X = C_X(C′, C″, s₀^r, A, σ², M, M′) and n₀ such that, on the event 𝓔_t of §1, for every S ∈ Ω with
  |S| ≤ d_t and L_S ≤ C″σ²t:  Π(‖μ̂ − μ‖² > C_Xσ²t or |v/σ² − 1| > C_X√(t/n) | S, y) ≤ e^{−t}.
- (I-S) (Lemma S, corollary for T = S₀.) Under (E; M), (C; M′): for n ≥ n₀ and ℓ ≤ t ≤ n^{1−κ₀}:
  P(π(|S| > m_n(t)) > e^{−t}) ≤ C_Se^{−t}, C_S a constant.
- (I-V) (Lemma V (a) with η = 1, and (c).) For every J ⊆ [p]∖S₀ (U_J need not be in Ω):
  0 ≤ Q_{S₀} − Q_{U_J} ≤ σ²χ²_J + ‖P_{S₀}e‖² + 3B, under (E; M), (C; M′).

## 1. Step X1 — the noise event
𝓔_t is the intersection of:
- (E1) |‖e‖² − Nσ²| ≤ σ²(2√(2Nt) + 4t);
- (E2) ‖P_Te‖² ≤ σ²τ(|T|) for every T ⊆ [p] with 1 ≤ |T| ≤ m̄;
- (E3) χ²_J ≤ τ(|J|) for every J ⊆ [p]∖S₀ with 1 ≤ |J| ≤ min(m, p − s₀);
- (E4) |eᵀa_S| ≤ σ‖a_S‖√(2(A+1)|S|ℓ + 5t) for every S ⊆ [p] with |S| ≤ m (S = ∅ included).

**Claim X1.** For n ≥ 3 and t ≥ 2: P(𝓔_tᶜ) ≤ e^{−t}.
*Proof.* (E1): ‖e‖²/σ² ~ χ²_N; (F6) with x = 2t, both sides: failure ≤ 2e^{−2t} (N + 2√(2Nt) + 4t and N − 2√(2Nt)).
(E2): P_T has rank r ≤ k := |T|, so ‖P_Te‖²/σ² ~ χ²_r ≤_st χ²_k. With x_k := (A+1)kℓ + 2t: k + 2√(kx_k) + 2x_k ≤ 2k + 3x_k ≤
(3A + 5)kℓ + 6t = τ(k) (2√(ab) ≤ a + b; ℓ ≥ 1). There are at most p^k ≤ e^{Akℓ} sets of size k, so the failure probability is
≤ Σ_{k≥1}e^{Akℓ}e^{−x_k} = e^{−2t}Σ_{k≥1}n^{−k} ≤ e^{−2t}. (E3): P_{U_J} − P_{S₀} is a projection of rank d_J ≤ |J| and there are at
most p^k sets J of size k: the same computation gives ≤ e^{−2t}. (E4): eᵀa_S ~ N(0, σ²‖a_S‖²) (a_S deterministic); (F6) with
x_k := (A+1)kℓ + 2t + log 2, 2x_k ≤ 2(A+1)kℓ + 5t (t ≥ 2): failure ≤ Σ_{k≥0}e^{Akℓ}·2e^{−x_k} = e^{−2t}Σ_{k≥0}n^{−k} ≤ 1.5e^{−2t}.
Total ≤ 5.5e^{−2t} ≤ e^{−t} for t ≥ 2. ∎

**Consequences on 𝓔_t** (deterministic; used below). Assume t ≤ n^{1−κ₀} and n ≥ n₁(κ₀, A, s₀^r, σ², M, M′), with n₁ such that
the three displayed "for n ≥ n₁" inequalities hold for every t in [ℓ, n^{1−κ₀}] (possible because t/N ≤ 2n^{−κ₀} and
(m̄ℓ + t)/N ≤ C(s₀^r, A)·n^{−κ₀}ℓ tend to 0 uniformly in t; m̄ ≤ 2s₀ + 1 + (s₀(A+1)ℓ + (s₀+2)ℓ + 3t)/log 2):
- (K1) ‖e‖² ≤ 1.5Nσ², and 2b ≤ 0.02(2‖μ‖² + 2‖e‖²)/N ≤ 0.08(M + σ²) (using n/N ≤ 2);
- (K2) for every U ⊇ S₀ with |U| ≤ m̄: Q_U ≥ ‖(I − P_U)e‖² ≥ σ²N(1 − ε′), ε′ := 2√(2t/N) + (τ(m̄))/N; (F2), μ_c ∈ col X_{c,U},
  (E1), (E2). For n ≥ n₁: ε′ ≤ ½, and ν/(2b + Q_U) ≤ (1 + ε_{n,t})/(2σ²) with
  ε_{n,t} := 2ε′ + 4/N ≤ C_ε(√(t/n) + (ℓ² + tℓ)/n), C_ε = C_ε(s₀^r, A) (as (n/2 + 0.01)/(N(1 − ε′)) ≤ ½(1 + 2/N)(1 + 2ε′) for ε′ ≤ ½);
- (K3) ε_{n,t}·ℓ ≤ C_ε(√(t/n)ℓ + (ℓ³ + tℓ²)/n) ≤ (log 2)/C_A and ε_{n,t} ≤ 1/6 for n ≥ n₁.

## 2. Step X3 — small models with large ridge loss
Constants: C′ ≥ 1 (fixed in §3), c₃ := (7A + 9)(C′ + 1) + 2A + 23, **C″ := 4c₃ + 4**, d_t := s₀ + ⌈C′t/ℓ⌉.
Let 𝔉_t := {S ∈ Ω : |S| ≤ d_t, L_S > C″σ²t}.

**Claim X3.** Assume (E; M), (C; M′), M₀ ≥ max{s₀^r + 1, 2B/σ², 128(A + 2)s₀^r/C″ + 1}, M₀ℓ ≤ t ≤ n^{1−κ₀}, n ≥ n₂ := max(n₁, n₂′) with
n₂′ such that n^{1−κ₀} ≤ 8N/C″ for n ≥ n₂′. Then on 𝓔_t:  π(𝔉_t) ≤ π(S₀)·e^{−C″t/128} ≤ e^{−C″t/128}.
*Proof.* Let S ∈ 𝔉_t, k := |S| ≤ d_t. Since (s₀ + 1)ℓ ≤ t: kℓ ≤ (s₀ + 1)ℓ + C′t ≤ (C′ + 1)t, and s₀ℓ ≤ t.
*Lower bound for Q_S.* By (F3), (E2) (if S ≠ ∅; for S = ∅ the term is 0) and (E4), with 2σ√L√y ≤ L/2 + 2σ²y:
Q_S ≥ ‖e‖² − σ²τ(k) − L_S/2 − 2σ²(2(A+1)kℓ + 5t) + L_S = ‖e‖² + L_S/2 − σ²[(7A + 9)kℓ + 16t].
((E2), (E4) apply because S ∈ Ω and |S| ≤ d_t imply |S| ≤ m: if m = K this is S ∈ Ω; otherwise
d_t ≤ s₀ + 1 + C′t/ℓ ≤ s₀ + 3t/log 2 ≤ m once ℓ ≥ C′, which is put into n₁.)
*Upper bound for Q_{S₀}.* By (F3), dropping −eᵀM_{S₀}e ≤ 0, (E4) for S₀ and 2σ√L√y ≤ L + σ²y:
Q_{S₀} ≤ ‖e‖² + 2L_{S₀} + σ²(2(A+1)s₀ℓ + 5t) ≤ ‖e‖² + 2B + σ²(2A + 7)t.
*Difference.* Δ := Q_S − Q_{S₀} ≥ L_S/2 − σ²t[(7A+9)(C′+1) + 16 + 2A + 7] − 2B ≥ C″σ²t/2 − c₃σ²t − σ²t = σ²t(C″/2 − c₃ − 1) = σ²t·C″/4,
using 2B ≤ σ²t and C″/4 = c₃ + 1.
*Likelihood ratio.* By (K1) and the bound on Q_{S₀}: 2b + Q_{S₀} ≤ 0.08(M + σ²) + 1.5Nσ² + 2B + σ²(2A+7)t ≤ 2Nσ² for n ≥ n₁ (put into n₁).
So x := Δ/(2b + Q_{S₀}) ≥ C″t/(8N), and x ≤ 1 may fail; in all cases log(1 + x) ≥ min(x, 1)/2. Hence
((2b + Q_{S₀})/(2b + Q_S))^ν = (1 + x)^{−ν} ≤ exp(−ν·min(C″t/(8N), 1)/2) ≤ exp(−(N/4)·C″t/(8N)) = e^{−C″t/32},
using ν ≥ N/2 and C″t/(8N) ≤ 1 (n ≥ n₂′).
*Sum.* π(S)/π(S₀) = [w(k)/w(s₀)](D_{S₀}/D_S)^{1/2}(1 + x)^{−ν} ≤ [w(k)/w(s₀)](n+1)^{s₀/2}e^{−C″t/32} by (F1). By (F4),
Σ_{S∈Ω}w(|S|)/w(s₀) = Σ_{k≤K}q_k/w(s₀) ≤ 2(2p)^{s₀}. So
π(𝔉_t)/π(S₀) ≤ 2(2p)^{s₀}(n+1)^{s₀/2}e^{−C″t/32} ≤ exp(log 2 + s₀(A + 2)ℓ − C″t/32) ≤ e^{−C″t/128},
because (2p)^{s₀}(n+1)^{s₀/2} ≤ (2n^A)^{s₀}(2n)^{s₀/2} ≤ e^{s₀(A+2)ℓ} (n ≥ 3 gives 2^{3/2} ≤ n^{3/2}); s₀(A+2)ℓ ≤ s₀(A+2)t/M₀ ≤ C″t/128 by
the third term of M₀; and log 2 ≤ C″t/128 (C″ = 4c₃ + 4 ≥ 4·(16·2 + 25) + 4 > 128, t ≥ 2). So the exponent is
≤ −C″t/32 + 2C″t/128 = −C″t/64 ≤ −C″t/128. ∎
(If s₀ = 0: S₀ = ∅ ∈ Ω, μ = 0, L_∅ = 0, and every step holds with s₀ = 0.)

## 3. Step X4 — models with more than d_t predictors
Split {|S| > d_t} into 𝔏_t := {S ∈ Ω : d_t < |S| ≤ m} and {|S| > m}. The second set is handled by (I-S).
Put j₁ := d_t − s₀ = ⌈C′t/ℓ⌉.

**(a) Reduction to supersets of S₀ (deterministic).** For S ∈ 𝔏_t put J := S∖S₀, j := |J|, U := U_J = S ∪ S₀. Then
j₁ < |S| − s₀ ≤ j ≤ |S| ≤ m and j ≤ p − s₀. Define, for J ⊆ [p]∖S₀ with |J| = j ≥ 1,
  R°(J) := [w(s₀ + j)/w(s₀)]·(D_{S₀}/D_{U_J})^{1/2}·((2b + Q_{S₀})/(2b + Q_{U_J}))^ν
(w(s₀ + j) is defined since s₀ + j ≤ p ≤ 2p − 1; U_J may lie outside Ω — Q, D are defined for every subset of [p]).
By (F2) Q_S ≥ Q_U; by (F1) applied |U| − |S| ≤ s₀ times, D_S ≥ D_U(n+1)^{−s₀}; by (F4), w(|S|) ≤ w(|U|)(2p)^{|U|−|S|} ≤ w(s₀ + j)(2p)^{s₀}
(|U| = s₀ + j). Hence
  π(S)/π(S₀) = [w(|S|)/w(s₀)](D_{S₀}/D_S)^{1/2}((2b + Q_{S₀})/(2b + Q_S))^ν ≤ (2p)^{s₀}(n+1)^{s₀/2}·R°(J).
The map S ↦ J is at most 2^{s₀}-to-one (S = J ∪ (S ∩ S₀)). Therefore
  π(𝔏_t)/π(S₀) ≤ 2^{s₀}(2p)^{s₀}(n+1)^{s₀/2}·Σ_{j=j₁+1}^{min(m, p−s₀)} Σ_{|J|=j} R°(J).                                   (3.1)

**(b) Bound for R°(J) on 𝓔_t.** Let Δ_J := Q_{S₀} − Q_{U_J} ∈ [0, σ²χ²_J + ‖P_{S₀}e‖² + 3B] by (I-V). Then, with
−log(1 − x) ≤ x/(1 − x) for 0 ≤ x < 1 and x = Δ_J/(2b + Q_{S₀}) (so that x/(1 − x) = Δ_J/(2b + Q_{U_J})):
  ((2b + Q_{S₀})/(2b + Q_{U_J}))^ν = (1 − x)^{−ν} ≤ exp(νΔ_J/(2b + Q_{U_J})) ≤ exp((1 + ε_{n,t})Δ_J/(2σ²))
by (K2) (|U_J| ≤ s₀ + m, and |U_J| ≤ p: so |U_J| ≤ m̄). On 𝓔_t, by (E2) for S₀ (if s₀ ≥ 1) and (E3):
‖P_{S₀}e‖² ≤ σ²τ(s₀) ≤ σ²(C_A + 6)t (s₀ℓ ≤ t) and χ²_J ≤ τ(j). With ε_{n,t} ≤ 1/6 ≤ 1 (K3):
  (1 + ε_{n,t})Δ_J/(2σ²) ≤ χ²_J/2 + ε_{n,t}τ(j)/2 + (C_A + 6)t + 3B/σ² ≤ χ²_J/2 + ε_{n,t}C_Ajℓ/2 + (C_A + 7)t + 3B/σ²
(ε_{n,t}·6t/2 ≤ t/2 ≤ t). By (K3), e^{ε_{n,t}C_Aℓ/2} ≤ √2. Hence, on 𝓔_t,
  R°(J) ≤ Φ_t·2^{j/2}·W_J,   Φ_t := exp((C_A + 7)t + 3B/σ²),
  W_J := [w(s₀ + j)/w(s₀)]·(D_{S₀}/D_{U_J})^{1/2}·e^{χ²_J/2}·1{χ²_J ≤ τ(j)}.                                             (3.2)

**(c) Expectation of the truncated sum.** χ²_J ~ χ²_{d_J}, d_J ≤ j, and τ(j) ≥ j. By (F5), E[e^{χ²_J/2}1{χ²_J ≤ τ(j)}] ≤ (eτ(j)/j)^{j/2}.
For j > j₁ ≥ C′t/ℓ: t/j < ℓ/C′, so eτ(j)/j = e(C_Aℓ + 6t/j) ≤ x̄ℓ with x̄ := e(C_A + 6/C′) ≤ e(C_A + 6). The bound does not
depend on J, so it can be taken out of the sum over J; then (ND; c_D, m) (which covers 1 ≤ j ≤ min(m, p − s₀)) and (F4):
  E Σ_{|J|=j}2^{j/2}W_J ≤ 2^{j/2}(x̄ℓ)^{j/2}·[w(s₀+j)/w(s₀)]·C(p − s₀, j)·[c_D(n+1)]^{−j/2} ≤ (4/3)(j+1)^{s₀}·q^j,
  q := [x̄ℓ/(2c_D(n+1))]^{1/2}.
Let n₃ ≥ n₂ be such that for n ≥ n₃: q ≤ ¼ and log(2c_D(n+1)/(x̄ℓ)) ≥ ℓ/2 (both hold for large n since ℓ/n → 0). Then, with
Y_t := Σ_{j=j₁+1}^{min(m, p−s₀)}Σ_{|J|=j}2^{j/2}W_J ≥ 0:
  E Y_t ≤ (4/3)Σ_{j>j₁}(j+1)^{s₀}q^j ≤ (4/3)(j₁ + 2)^{s₀}q^{j₁+1}Σ_{i≥0}(i+1)^{s₀}4^{−i} ≤ K_{s₀}(j₁ + 2)^{s₀}q^{j₁+1},
K_{s₀} := (4/3)Σ_{i≥0}(i+1)^{s₀}4^{−i} < ∞ (using j + 1 = j₁ + 2 + i ≤ (j₁ + 2)(i + 1)). And
  q^{j₁+1} = exp(−(j₁ + 1)·½·log(2c_D(n+1)/(x̄ℓ))) ≤ exp(−(C′t/ℓ)·(ℓ/4)) = e^{−C′t/4},   (j₁ + 2)^{s₀} ≤ (C′t/ℓ + 3)^{s₀} ≤ e^{s₀ℓ}
for n ≥ n₃ (C′t/ℓ + 3 ≤ n: put into n₃; t ≤ n^{1−κ₀}). So E Y_t ≤ K_{s₀}e^{s₀ℓ − C′t/4}.

**(d) Markov.** By (3.1), (3.2), on 𝓔_t: π(𝔏_t) ≤ π(𝔏_t)/π(S₀) ≤ Ψ_tY_t, with
  Ψ_t := 2^{s₀}(2p)^{s₀}(n+1)^{s₀/2}Φ_t ≤ exp(s₀(A + 3)ℓ + (C_A + 7)t + 3B/σ²).
Fix c ∈ (0, 1]. P(𝓔_t ∩ {π(𝔏_t) > e^{−ct}}) ≤ P(Ψ_tY_t > e^{−ct}) ≤ e^{ct}Ψ_tE Y_t ≤ K_{s₀}exp(s₀(A + 4)ℓ + (C_A + 8)t + 3B/σ² − C′t/4).
With **C′ := 4(C_A + 12)** and M₀ ≥ max{s₀^r(A + 4), 3B/σ², log K_{s₀^r}} (so that s₀(A+4)ℓ ≤ t, 3B/σ² ≤ t, log K_{s₀} ≤ t):
the exponent is ≤ (C_A + 11)t − (C_A + 12)t = −t. Hence

**Claim X4.** Under (E; M), (C; M′), (ND; c_D, m_n(t)), for n ≥ n₃ and M₀ℓ ≤ t ≤ n^{1−κ₀}, every c ∈ (0, 1]:
  P(𝓔_t ∩ {π(𝔏_t) > e^{−ct}}) ≤ e^{−t}.   ∎
(The constants c_D enters only through n₃. C′ = 4(C_A + 12) = 12A + 68 depends on A only.)

## 4. Assembly — proof of Lemma X
Constants in order: C_A = 3A + 5; C′ = 4(C_A + 12); c₃, C″ of §2; C_X of (I-X2); M₀ := the maximum of the lower bounds
required in Claims X3, X4 and 2 (it depends on (s₀^r, A, σ², M, M′) only); n₀ := max(n₃, the n₀ of (I-X2) and (I-S));
C := C_X. Let M₀ℓ ≤ t ≤ n^{1−κ₀}, n ≥ n₀, and Bad := {‖μ̂ − μ‖² > Cσ²t} ∪ {|v/σ² − 1| > C√(t/n)} ∪ {|S| > d_t}. Then
  Π(Bad | y) ≤ π(|S| > m) + π(𝔏_t) + π(𝔉_t) + max{Π(Bad′ | S, y) : S ∈ Ω, |S| ≤ d_t, L_S ≤ C″σ²t},
Bad′ the first two events. On the event 𝓗_t := 𝓔_t ∩ {π(|S| > m) ≤ e^{−t}} ∩ {π(𝔏_t) ≤ e^{−t}}: by Claim X3 and (I-X2),
  Π(Bad | y) ≤ e^{−t} + e^{−t} + e^{−C″t/128} + e^{−t} ≤ 4e^{−t} ≤ e^{−t/2}   (C″ ≥ 128; and 4e^{−t} ≤ e^{−t/2} for t ≥ 2 log 4 ≈ 2.78).
And P(𝓗_tᶜ) ≤ e^{−t} + C_Se^{−t} + e^{−t} ≤ 2e^{−t/2} once (2 + C_S)e^{−t/2} ≤ 2, i.e. t ≥ 2 log(1 + C_S/2) (put into M₀).
So Lemma X holds with **c = ½**, C = C_X, C′ = 12A + 68, and one n₀ for the whole range of t. ∎

## 5. Lemma X′ (without (ND))
Take d := m = m_n(t) in place of d_t; then {|S| > d} is handled by (I-S) alone and §3 is not used. Replace t by
t′ := tℓ_n (ℓ_n := log(p_raw ∨ n) ≥ ℓ) in the *thresholds* only: 𝔉′_t := {S ∈ Ω : |S| ≤ m, L_S > C″σ²t′} and the ball
{‖μ̂ − μ‖² ≤ Cσ²t′, |v/σ² − 1| ≤ C√(t/n)}; the event 𝓔_t and all probability levels stay at t.
- X3′: for |S| ≤ m, |S|ℓ ≤ mℓ ≤ C_m t′ with C_m = C_m(s₀^r, A) (m ≤ s₀ + 1 + (s₀(A+2) + 1)ℓ/log 2 + 3t/log 2 and t ≥ ℓ). The proof of
  Claim X3 with (C′ + 1)t replaced by C_m t′, 16t ≤ 16t′, and C″ := 4((7A + 9)C_m + 2A + 23) + 4 gives Δ ≥ C″σ²t′/4 and
  π(𝔉′_t) ≤ e^{−C″t′/128} ≤ e^{−t} on 𝓔_t. It needs C″t′/(8N) ≤ 1 and 2b + Q_{S₀} ≤ 2Nσ²: both hold for n large uniformly in t,
  since t′ ≤ n^{1−κ₀}·Aℓ (ℓ_n ≤ Aℓ as p_raw ≤ n^A) and n^{−κ₀}ℓ → 0; put into n₀.
- X2′: the input (I-X2) is needed in the form: on 𝓔_t, for every S ∈ Ω with |S| ≤ m and L_S ≤ C″σ²t′:
  Π(‖μ̂ − μ‖² > C_Xσ²t′ or |v/σ² − 1| > C_X√(t/n) | S, y) ≤ e^{−t}. (Stream C's X12.md is asked for a general d with d·log p ≤ C‴t;
  here that reads m·log p ≤ C‴t′, with the mean threshold at t′. The variance centre is displaced by O(t′/n) = O(√(t/n)·√(t/n)ℓ_n),
  which is ≤ √(t/n) for n large because √(t/n)·ℓ_n ≤ A n^{−κ₀/2}ℓ → 0.) **This form must be confirmed against X12.md.**
- Assembly as in §4. ∎ (DRAFT; depends on the confirmation above.)

## 6. What is used, and what is not
Used: (E; M) and (C; M′) through B (in (F3), (I-V), (I-S), (K1)); (ND) only in §3(c), on the range 1 ≤ j ≤ min(m_n(t), p − s₀);
p ≤ n^A in the unions of §1 and in n^{s₀(A+…)} bounds; t ≤ n^{1−κ₀} only to make t/N, (m̄ℓ + t)/N and ε_{n,t}ℓ small uniformly
(K1–K3, n₂′, n₃). Not used: any eigenvalue condition on S₀ or elsewhere, beta-min, the size of the nonzero coefficients.
The three factors flagged by the blind read are paid explicitly: exp(‖P_{S₀}e‖²/2σ²) inside Φ_t; the union multiplicity
2^{s₀}(2p)^{s₀}(n+1)^{s₀/2} in Ψ_t; the variance surcharge e^{ε_{n,t}τ(j)/2} as 2^{j/2}·e^{t/2}.
Open points for the line check: (1) the exact forms (I-X2), (I-S), (I-V) against stream C's files; (2) (K2)'s
constant C_ε and the uniformity of n₁ in t; (3) the use of (ND) for j up to min(m, p − s₀) when s₀ + j > K (the sum (3.1)
includes sets U_J outside Ω; (ND) as stated in STATEMENT §0 is on 1 ≤ j ≤ min(m, p − s₀), which covers them).
