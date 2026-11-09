# L5 — Lemma VN: visible nulls force large start modes (route obstruction)

Status: **PROVED (by this seat, unchecked)**. Check record: R04 (Codex gpt-6.1-sol high, `reviews/R04_L5_check_sol.md`):
VERIFIED-WITH-AMENDMENTS (1 MAJOR, 1 MINOR — growth qualifications in V4 and §L5.3), applied [R04-#]; core lemma,
corollary and the four population computations verified (scratch numerics R04_scratch/).
Falsification numerics: `numerics/n3_*` (start modes on STAR, growing blocks, equicorrelation); summary
`numerics/NUMERICS_LOC_VN.md`.

**What this is and is not.** VN is a statement about the start mode γ₀ (the product-of-block-tables start law) and
therefore about the *proof routes* of GEN (bounded centre S̃₀ = S*) and GROW/LOC (sandwich S₀ ⊆ S̃₀ ⊆ Q with
|Q| = O(log n)). It says nothing about whether LS0 or the full method reaches S₀ from a large start mode.

## L5.0 Setting and statement
Random design as STATEMENT §1 (raw rows iid N(m, Σ_n), Σ_n unit-diagonal, p ≤ n^A, fixed s₀, |θ*_j| ∈ [θ_lo, θ_hi],
Y = Xθ* + Cε, ε independent of the design), and
* (F16) λ_min(Σ_{n,S}) ≥ c > 0 for every S with |S| ≤ 16 + s₀ (fixed c).
Population response (a single population row): Y° := Σ_{k∈S₀}θ*_kW_k + σξ, ξ ~ N(0, 1) independent of W
(STATEMENT writes V for Y°). For a deterministic null set
𝒩_n ⊆ [p] ∖ S₀ define the **visible-null floor**
* VNF(κ_n): Corr(W_l, Y° | W_U)² ≥ κ_n for every l ∈ 𝒩_n and every U ⊆ [p] ∖ (S₀ ∪ {l}) with |U| ≤ 15,
with nκ_n/log n → ∞.

**Lemma VN.** Under (F16) and VNF(κ_n), for any X-measurable partition with blocks of size ≤ 16, with probability
→ 1 (joint law) every maximiser S̃ of γ₀ on Ω satisfies
  |S̃| = K  or  S̃ ⊇ 𝒩_n ∖ ⋃{C_b : C_b ∩ S₀ ≠ ∅};
in particular |S̃ ∖ S₀| ≥ min(K − s₀, |𝒩_n| − 15s₀).

**Corollary VN-routes.** (i) If |𝒩_n| → ∞, then for every fixed v̄: P(|S̃₀| ≤ v̄) → 0. Hence there are no X-measurable
S*_n with |S*_n| ≤ v̄ such that GEN's (H2) holds with fixed constants on design events of probability → 1: otherwise
GEN (C1) along every deterministic sequence in those events plus the diagonal argument (GEN L5.3) would give
P(S̃₀ = S*_n) → 1. The GEN route ((C3), (C3-fav), (C4)) is unavailable. (ii) If min(K, |𝒩_n|)/log n → ∞, then
for every C_Q and every deterministic Q_n with |Q_n| ≤ C_Q log n: P(S̃₀ ⊆ Q_n) → 0. Hence GROW's (G1) + (G3) cannot hold
with fixed constants on design events of probability → 1 (GROW (C3) would give P(S̃ ⊆ Q) → 1 by the same diagonal
argument), and no sandwich with an O(log n) relevance set — the mechanism of GROW and of Theorem LOC — exists.

## L5.1 Proof
*Regularity.* Every set of the form {l} ∪ U ∪ S₀ with |U| ≤ 15 has size ≤ 16 + s₀. The argument of [L6] L6.2
(GROW `lemmas/L6_random_AR1.md`; entrywise event for the raw centred columns and the noise column, ħ_n = C_A√(log n/n);
bounded-dimension perturbation of conditional covariances with conditional variances ≥ c by (F16) and residual
variance of Y° ≥ σ²; coefficients θ*_k/t_k within O(ħ_n) of θ*_k) uses only Gaussianity, unit variances and these
floors; it gives an event A_cov, P(A_cov) → 1, on which, uniformly over l ∈ [p] and U ⊆ [p] ∖ (S₀ ∪ {l}), |U| ≤ 15,
the sample partial correlation ρ̂_{U,l} of x_l and Y given X_U satisfies |ρ̂_{U,l} − Corr(W_l, Y° | W_U)| ≤ C ħ_n.
On A_cov and VNF, h_{U,l} := n ρ̂²_{U,l} ≥ n(√κ_n − Cħ_n)² ≥ nκ_n/2 for n ≥ n₀ (ħ_n = o(√κ_n) because
nκ_n/log n → ∞). Also the L0 events for the family of all subsets of [p] of size ≤ 16 hold w.p. → 1 ([L6] §1,
"A_score"; Gram floors from (F16) and the entrywise event; energy ‖μ‖² ≤ s₀²θ_hi²n).
*Block-table increment.* By GROW L0.2(c) (block-table form) and RSS_{U∪{l}}/RSS_U = 1 − h_{U,l}/n:
  log r_b(U ∪ {l}) − log r_b(U) = −½ log(n + 1) − ν log(1 − h_{U,l}/n) + (R_{U∪l} − R_U)
                                ≥ −½ log(n + 1) + h_{U,l}/2 − 2κ_E,
using −log(1 − x) ≥ x and ν ≥ n/2.
*Maximisers.* Fix any maximiser S̃, k := |S̃| < K, and suppose l ∈ 𝒩_n ∖ S̃ lies in a block C_b with C_b ∩ S₀ = ∅.
Put U := S̃ ∩ C_b (|U| ≤ 15, U ∩ S₀ = ∅, l ∉ U). S̃ ∪ {l} ∈ Ω and
  log γ₀(S̃ ∪ {l}) − log γ₀(S̃) = log[(k + 1)/(2p − 1 − k)] + log r_b(U ∪ {l}) − log r_b(U)
                               ≥ −log(2p) − ½ log(n + 1) − 2κ_E + nκ_n/4 > 0
for n ≥ n₀ (log p ≤ A log n, nκ_n/log n → ∞), contradicting maximality. The bound holds simultaneously for all
maximisers and all such l on the stated events (no union over maximisers). Since at most s₀ blocks meet S₀ and each
has ≤ 16 elements, |⋃{C_b : C_b ∩ S₀ ≠ ∅} ∖ S₀| ≤ 15s₀, giving the count. ∎
*Corollary.* (i) |S̃₀| ≥ min(K − s₀, |𝒩_n| − 15s₀) → ∞ (K ≥ min(p, ⌊n/2⌋) → ∞ when p → ∞; if p is bounded, |𝒩_n| is
bounded). (ii) |S̃₀ ∖ S₀| ≥ min(K − s₀, |𝒩_n| − 15s₀) > C_Q log n eventually. The contrapositive arguments are as stated
(GEN (C1) and GROW (C3) are proved theorems; their fixed-design conclusions transfer along deterministic sequences;
a common-constants violation along a subsequence gives a contradiction). ∎

## L5.2 Applications (each verifies VNF with explicit κ)

**(V1) STAR (bounded spectrum, non-local).** s₀ = 1, S₀ = {1}, θ*₁ = θ; leaves 𝓛_n, |𝓛_n| = m_n; Σ = I + r_n(e₁1ᵀ_𝓛 + 1_𝓛e₁ᵀ),
r_n := 1/(2√m_n). Spectrum: {1 ± r_n√m_n} ∪ {1} = {½, 1, 3/2}: Σ has spectrum in [½, 3/2] for all n, so (F16) and
L1_POST hold. For a leaf l and U ⊆ [p] ∖ {1, l}: Σ_{lU} = 0 (leaves are mutually uncorrelated and uncorrelated with
non-leaves other than W₁), so Cov(W_l, W₁ | W_U) = r_n, Var(W_l | W_U) = 1, Var(Y° | W_U) ≤ θ² + σ²; hence
Corr(W_l, Y° | W_U)² ≥ θ²r_n²/(θ² + σ²) = θ²/(4m_n(θ² + σ²)) =: κ_n. VNF holds iff m_n = o(n/log n). With
m_n = ⌊n^{1/3}⌋: |S̃₀ ∖ S₀| ≥ min(K − 1, m_n − 15) ≫ log n, so neither the GEN nor the GROW/LOC route applies,
although the design has condition number 3. STAR ∉ LOC for any fixed (K, a) once m_n/log m_n → ∞: |Σ_{1l}| = r_n ≤
Ke^{−a d(1,l)} forces d(1, l) ≤ a⁻¹ log(2K√m_n), and at most 2a⁻¹log(2K√m_n) + 1 = O(log m_n) < m_n positions qualify.
PTV holds: for U ∌ 1, |Cov(W₁, θW₁ | W_U)| = |θ| Var(W₁ | W_U) ≥ |θ|/2 (Var(W₁ | W_U) ≥ λ_min(Σ) = ½).

**(V2) Equicorrelated blocks of growing size.** Blocks G of size g_n (consecutive), within-correlation ρ ∈ (0, 1)
fixed, independent blocks; ≤ one truth per block. Spectrum: λ_min = 1 − ρ, so (F16) and L1_POST hold (λ_max = 1 + (g_n − 1)ρ
→ ∞ is irrelevant). For a truth j, 𝒩_n := G(j) ∖ {j} (over all truths: s₀(g_n − 1) nulls). For l ∈ G(j) ∖ {j} and
U ⊆ [p] ∖ (S₀ ∪ {l}), |U| ≤ 15, with u := |U ∩ G(j)|: by the equicorrelated Schur complement,
Cov(W_l, W_j | W_U) = ρ − ρ²u/(1 + (u − 1)ρ) = ρ(1 − ρ)/(1 + (u − 1)ρ) ≥ ρ(1 − ρ)/(1 + 14ρ); members of U in other blocks
and other truths are independent of (W_l, W_j, W_{U∩G(j)}). So Cov(W_l, Y° | W_U) = θ*_j ρ(1 − ρ)/(1 + (u − 1)ρ),
Var(W_l | W_U) ≤ 1, Var(Y° | W_U) ≤ s₀θ_hi² + σ²:
  κ := θ_lo²ρ²(1 − ρ)²/[(1 + 14ρ)²(s₀θ_hi² + σ²)] > 0 fixed.
Hence |S̃₀ ∖ S₀| ≥ min(K − s₀, s₀(g_n − 1) − 15s₀): g_n → ∞ excludes the GEN route; g_n/log n → ∞ excludes the
GROW/LOC sandwich. (g_n = O(log n): not decided here.)

**(V3) Equicorrelation with a nonzero common signal.** Σ = (1 − ρ)I + ρ11ᵀ, ρ ∈ (0, 1) fixed, and Σ_kθ*_k =: θ̄ with
|θ̄| ≥ θ̄₀ > 0 fixed. (F16) with c = 1 − ρ. 𝒩_n := [p] ∖ S₀. For l ∉ S₀ and U ⊆ [p] ∖ (S₀ ∪ {l}), |U| = u ≤ 15, every
truth k satisfies Cov(W_l, W_k | W_U) = ρ(1 − ρ)/(1 + (u − 1)ρ) (same Schur complement), so
Cov(W_l, Y° | W_U) = θ̄ρ(1 − ρ)/(1 + (u − 1)ρ) and κ := θ̄₀²ρ²(1 − ρ)²/[(1 + 14ρ)²(θ*ᵀΣ_{S₀}θ* + σ²)] (θ*ᵀΣ_{S₀}θ* ≤ s₀²θ_hi²).
Hence |S̃₀ ∖ S₀| ≥ min(K − s₀, p − 16s₀): the start mode is asymptotically saturated or contains all but O(1) nulls.
If θ̄ = 0 the floor is 0 for every null (exchangeability) and VN gives nothing (remark only; no claim).

**(V4) One-factor models.** Σ = bbᵀ + Ψ unit-diagonal, Ψ = diag(ψ_j), ψ_j ≥ ψ₀ > 0, |b_j| ≤ 1. With f the factor,
for l, k distinct and U ∌ l, k: Cov(W_l, W_k | W_U) = b_lb_k Var(f | W_U) and Var(f | W_U) = (1 + Σ_{u∈U}b_u²/ψ_u)⁻¹
≥ (1 + 15/ψ₀)⁻¹ for |U| ≤ 15. If |bᵀ_{S₀}θ*| ≥ β₀ > 0 and 𝒩_n := {l ∉ S₀ : |b_l| ≥ b₀} for a fixed b₀ > 0, then VNF holds
with κ := b₀²β₀²(1 + 15/ψ₀)⁻²/(θ*ᵀΣ_{S₀}θ* + σ²) (Var(W_l | W_U) ≤ 1). (F16): λ_min(Σ) ≥ ψ₀. [R04-1] A pervasive loaded set excludes
the GEN route if |𝒩_n| → ∞, and excludes the GROW/LOC sandwich if min(K, |𝒩_n|)/log n → ∞, provided the displayed
exposure and signal floors hold. (R04 example: p_n ≍ √(log n), ρ = ½, s₀ = 1 satisfies VNF with |𝒩_n| → ∞, yet GROW
applies with Q = [p_n]; only the GEN route is excluded there.)

## L5.3 Reading (necessary vs proof limitation)
[R04-2] VN gives |S̃₀ ∖ S₀| ≥ min(K − s₀, |𝒩_n| − 15s₀) with |𝒩_n| = m_n (V1), s₀(g_n − 1) (V2), p − s₀ (V3), the
loaded null set (V4). In each application separately: the GEN route ("S̃₀ bounded") is impossible when |𝒩_n| → ∞, and
the GROW/LOC route ("S̃₀ inside an O(log n) lattice") is impossible when min(K, |𝒩_n|)/log n → ∞ (V1 with
m_n = ⌊n^{1/3}⌋: both; V2: GEN iff-direction g_n → ∞, GROW/LOC when g_n/log n → ∞; V3/V4: GEN when p → ∞ (resp.
|𝒩_n| → ∞), GROW/LOC when min(K, |𝒩_n|)/log n → ∞). Where these hold the obstruction is **necessary for these
routes**. It is **not** shown that the method
fails: LS0's shipped cap ℓ_n + |S̃₀| permits |S̃₀ ∖ S₀| deletions, and whether the deletion path reaches S₀ is a
separate question (FAC tickets for (V3)/(V4); open for (V1), (V2)). The numerics in `numerics/n3_*` report what the
ported start mode and LS0 do at moderate n — observations, not proof.
