# L7 — (C6): boundedness of the relevance set cannot be dropped from the LS0 route

Status: **PROVED (by this seat, unchecked)**, v3 after lemma checks R06 (v1: GAP) and R08 (v2: GAP; its concrete
repair of L7.1 is incorporated here verbatim in substance). v2 note: (Codex Sol: GAP on v1; repairs applied: the
eigenvalue proof, the weakened Proposition L7.1, the noncircular parameter choice, the scope sentence, and a design
change so that the truth is not scored trivially by a block table — see reviews/R06_disposition.md).

Scope: refutes a universal **LS0-discovery** guarantee once the size bounds |𝒱_n| ≤ v̄ and s* ≤ v̄ are both removed,
all other hypotheses kept. It does **not** claim that the full method's D_n fails to vanish (the SMC and other searches
may score S₀), and it does not exclude growth of 𝒱 slower than the cap.

## Design 𝒲

Fix a ∈ (0, 1), θ ≠ 0, σ² = 1, and an integer s₀ ≥ 17 (so S₀ does not fit in one block, B ≤ 16; then no block table
scores S₀, since tables score only subsets of single blocks, SoP 02_method.tex:193-195). For all sufficiently large n
let p = p_n := n − 1, ℓ_n := ⌈log₂(n + p + 1)⌉ = ⌈log₂(2n)⌉, d = d_n := 16(2ℓ_n + 5) (so
d_n ≍ log n and d_n + s₀ ≤ p_n for n large). Let e₀, e₁, …, e_d, e′₁, …, e′_{s₀−1}, f₁, …, f_{p−d−s₀} be an orthonormal
basis of ℝ^p and define unit vectors
  ξ₀ := e₀ (truth with proxies), ξ′_k := e′_k (k = 1..s₀ − 1, further truths),
  ξ_i := (a/√d)e₀ + √(1 − a²/d) e_i (i = 1..d, proxies),  ζ_k := f_k (nulls).
Σ := their Gram matrix. Exact-Gram design X := √(n − 1)QΣ^{1/2}, Q ∈ ℝ^{n×p} orthonormal columns ⊥ 1 (p ≤ n − 1), so
XᵀX = (n − 1)Σ, centred columns of squared norm n − 1. Take the raw design equal to X (unit sample scales).
β: θ on x₀ and on each x′_k; zero elsewhere. S₀ = {0} ∪ {1′, …, (s₀−1)′}, μ = θ(x₀ + Σ_k x′_k).

**(W1) λ_min(Σ) ≥ 1 − a.** Write a coefficient vector as (c₀, b, c′, g) on (ξ₀, ξ_i, ξ′_k, ζ_k) and split
b = βu + b^⊥ with u := d^{−1/2}1, 1ᵀb^⊥ = 0. Then Σ_i b_iξ_i = β[a e₀ + √(1 − a²/d) ē] + √(1 − a²/d)Σ_i b^⊥_i e_i with
ē := d^{−1/2}Σ_i e_i, and the vector's squared norm is
  (c₀ + aβ)² + β²(1 − a²/d) + (1 − a²/d)‖b^⊥‖² + ‖c′‖² + ‖g‖².
On the (c₀, β) plane the Gram matrix is [[1, a], [a, 1 + (d − 1)a²/d]]; subtracting (1 − a)I leaves
[[a, a], [a, a + (d − 1)a²/d]], with nonnegative diagonal and determinant a²(d − 1)a/d ≥ 0, hence PSD. The other
directions have eigenvalues 1 − a²/d ≥ 1 − a and 1. So λ_min(Σ) ≥ 1 − a (also for d = 1). Σ is positive definite. ∎

**(W2) Hypotheses that hold.** φ₀² := 1 − a.
* (H0): R1 (s₀ fixed, p ≤ n − 1 (A = 1), s₀ ≤ K eventually); G; R (‖μ‖² = (n − 1)s₀θ², M = s₀θ²); SE_λ(j₀) and
  SE_w(m♯_n; g₀) at **every** order by (W1) and interlacing (normalized ≥ 1 − a; unnormalized ≥ (n − 1)(1 − a) ≥ g₀
  := 1 − a eventually); BM-∞ (θ fixed). Hence T03♯ applies: π(S₀) → 1 in probability.
* (H1) with 𝒱 := S₀ ∪ {1, …, d}: (H1a) by (W1); (H1b) with ζ_n = 0 (nulls are orthogonal to every column of 𝒱 and to
  μ). **Fails: |𝒱_n| = s₀ + d_n → ∞.**
* (H2), on any actual partition with blocks ≤ B ≤ 16, with S* := S₀ ∪ {proxies not in the block of x₀}:
  (H2a) by (W1). (H2c) with δ = 0 throughout (C_L = 0; NL_avg(κ) with κ = ¼: the average is 1 ≤ n^{1/4}). Block types: (i) x₀'s
  block: T contains all block truths incl. x₀; a residualized proxy is orthogonal to x₀ and to every further truth
  (x_i − (a/√d)x₀ ⊥ μ), a residualized null is orthogonal to μ; (ii) a block with further truths but not x₀: every
  proxy and truth of the block is in U*_b, so leakage indices are nulls, orthogonal to μ; (iii) proxy-only blocks:
  leakage indices are nulls; (iv) null-only blocks: U*_b = ∅ and every residualized null is orthogonal to μ. (H2b): in a block b without x₀ with r proxies, if U contains m of them and misses t of the block's
  truths, then exactly g_{b,U} = θ²(n − 1)[t + f(r) − f(m)] (truths are orthogonal to each other and to the proxies;
  nulls are orthogonal to everything carrying signal); in x₀'s block, a missing x₀ gives g ≥ θ²(n − 1)(1 − a) and a
  missing further truth gives θ²(n − 1); in a block b without x₀, for a set A of m proxies ‖P_Aθx₀‖² = θ²(n − 1)f(m),
  f(m) := m x/(1 + (m − 1)x), x := a²/d (from Σ_{0A} = (a/√d)1, Σ_{AA} = (1 − x)I + x11ᵀ; nulls and the other truths
  are orthogonal to these proxies), and f(m + 1) − f(m) = x(1 − x)/((1 + mx)(1 + (m − 1)x)) ≥ x/2 for m ≤ 16 and
  d ≥ d₀(a); so g_{b,U} ≥ θ²(n − 1)a²/(2d). With v_U ≤ 1 + s₀θ² and d_n ≍ log n, VIS holds with
  M_n := θ²(n − 1)a²/(2d_n(1 + s₀θ²) log n) → ∞. S* ⊆ 𝒱, s* ≤ s₀ + d ≤ K eventually. **Fails: s* ≥ d_n − B + s₀ → ∞.**
So every design hypothesis (H0)–(H2) holds except the two size bounds |𝒱_n| ≤ v̄ and s* ≤ v̄ (the implementation
premises are stipulated contracts, not properties of a design).

## Claims

**Proposition L7.1.** With probability → 1, |S̃₀ ∖ S₀| ≥ ⌈d_n/B⌉ − 1, hence |S̃₀ Δ S₀| ≥ ⌈d_n/B⌉ − 1. More precisely,
P(|S̃₀| < K and some block b containing a proxy and not x₀ has (S̃₀ ∩ C_b) ∖ S₀ = ∅) → 0.

*Proof.* Let 𝔅 := {blocks containing a proxy and not x₀}. The d proxies lie in at least ⌈d/B⌉ blocks, at most one of
which contains x₀, so |𝔅| ≥ ⌈d/B⌉ − 1. Case |S̃₀| = K:
|S̃₀ ∖ S₀| ≥ K − s₀ ≥ ⌈d/B⌉ − 1 for n large (K = ⌊n/2⌋ ≫ d). Case |S̃₀| < K: suppose some b ∈ 𝔅 has (S̃₀ ∩ C_b) ∖ S₀ = ∅, i.e. U := S̃₀ ∩ C_b ⊆ S₀ ∖ {0} (only further truths).
Pick a proxy k ∈ C_b and put S′ := S̃₀ ∪ {k} ∈ Ω. Only block b's factor and the prior change:
log γ₀(S′) − log γ₀(S̃₀) = log[w(q + 1)/w(q)] + log[r_b(U ∪ {k})/r_b(U)] ≥ −log(2p) + log[r_b(U ∪ {k})/r_b(U)]
(q = |S̃₀|; w(q + 1)/w(q) = (q + 1)/(2p − 1 − q) ≥ 1/(2p); capping cancels). Apply L1 to the deterministic family
𝔉_n := {A, A ∪ {k} : A ⊆ S₀ ∖ {0}, k a proxy} (contains ∅; J = s₀; |𝔉_n| ≤ 2^{s₀}(d_n + 1) ≤ C_F n; Gram floor 1
because the further truths are orthonormal and orthogonal to every proxy; auxiliary vectors {r_A} ∪ {r_A − r_{A′}}).
For every such (U, k): (I − P_U)x_k = x_k, so by (E6)/EXP′ and log(1/(1 − x)) ≥ x,
log[r_b(U ∪ {k})/r_b(U)] ≥ −½ log(n + 1) + ν(δ_k + σZ_k)²/RSS_U − 2κ_E, with δ_k := x_kᵀμ/‖x_k‖ = θ√(n − 1)a/√d
(x_k is orthogonal to the further truths) and Z_k := x_kᵀε/(σ‖x_k‖) ~ N(0, 1) — the same for every U. On
{max_{k≤d}|Z_k| ≤ 2√(log n)} (probability ≥ 1 − 2d/n²), δ_k² = θ²(n − 1)a²/d ≫ log n gives (δ_k + σZ_k)² ≥ δ_k²/2,
and RSS_U ≤ ‖Y‖² ≤ C_R n (L1.2) gives ν(δ_k + σZ_k)²/RSS_U ≥ θ²(n − 1)a²/(4C_R d). So, simultaneously for all (U, k),
the gain is ≥ θ²(n − 1)a²/(4C_R d) − log(2p) − ½ log(n + 1) − 2κ_E > 0 for n ≥ n₀ (d log n/n → 0), contradicting
maximality of S̃₀. Hence on the intersection of these events every b ∈ 𝔅 contains a selected element outside S₀ (a
proxy or a null), and |S̃₀ ∖ S₀| ≥ |𝔅| ≥ ⌈d/B⌉ − 1. ∎

**Proposition L7.2.** A local search (M §6.10) from a centre C with at most ℓ moves and one further scan scores only
models within symmetric-difference distance 2(ℓ + 1) of C. *Proof.* A flip changes one membership, a swap two; after
t ≤ ℓ moves the centre is within 2t of C; every scanned model is within 2 of its centre; the emitted centre is C. ∎

**Corollary L7.3.** ⌈d_n/B⌉ − 1 ≥ 2ℓ_n + 4 > 2(ℓ_n + 1) (B ≤ 16). Hence with probability → 1 LS0 (centre S̃₀, cap
ℓ_n) does not score S₀: P(LS0 from S̃₀ misses S₀) → 1, although π(S₀) → 1 and every hypothesis of (C3) other than
the two size bounds holds. ∎

**Remarks.** (1) The obstruction is the move cap ℓ_n = ⌈log₂(n + p + 1)⌉ against at least order d_n/B extras of the
start mode. (With p_n = n − 1 the production run does not take the exact branch eventually: Σ_{k≤K}C(p,k) ≥ 2^{p−1}
while the threshold (5H₀ + 4N₀)p is O(n²), SoP 02_method.tex:162-170; so LS0 is actually executed.) Whether a growing-family version of L3–L4 holds when the cap exceeds the number of extras is **not** established
here (frontier). (2) Because s₀ ≥ 17 > B, no block table scores S₀, so the full method's D_n is not trivially zero; but
the SMC at φ = 1 (target π with π(S₀) → 1) or the final local search may still score S₀: nothing is claimed about the
full method's D_n.
