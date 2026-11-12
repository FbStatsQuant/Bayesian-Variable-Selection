# L8 — Random-design transfer (T3)(a)

Status: **PROVED (by this seat)**. The check record is kept outside this file (the ticket's final checkpoint file and `reviews/`).
Statement proved: `STATEMENT.md` §5.3 (T3)(a). Uses `lemmas/L5_ASM_STARTF.md` (Proposition L5.2 = (T1)(d)) and
`lemmas/L6_COROLLARIES.md` (Lemma L6.0, Corollary L6.0′).

## L8.0 Setting

X^r is a random raw design (n rows). α, β, Q and h are measurable functions of X^r. Conditionally on X^r,
  y^r = α(X^r)1 + X^rβ(X^r) + ε,   ε | X^r ~ N_n(0, σ²I),   σ² > 0 fixed.
Constant raw columns are dropped; p is the number of retained columns; θ* := D_xβ(X^r), S₀ := supp β(X^r) (on the
retained columns), μ = Xθ*. The start π₀ is a measurable function of (X^r, y^r); it depends on y^r only through
Y = Cy^r = Xθ* + Cε (centring removes α), and the partition is a function of X^r. Two special cases: a deterministic β
with ε independent of X^r; Setting R (deterministic θ* on the standardised scale: take β(X^r) := D_x⁻¹θ*).

**Convention off the admissible designs.** The design law is constrained only on the sets 𝒳 below. Where the start,
the lattice or the odds are not defined as in `STATEMENT.md` §1 (no retained column, an invalid response, S₀ ∉ Ω,
S₀ ⊄ Q or |Q| > K), the quantities 1 − π₀(𝓛(Q)) and o₀ are set to 0. This only makes the events B of L8.2 well defined
on the whole design/response space; on admissible designs the usual values are used, and nothing is claimed about a
coded start on invalid inputs.

**Admissible designs at n** (for fixed constants A, M, g_*, s₀ and c_V or (c_m, ε₀)): a realisation x of X^r is
admissible if, with its own (θ*, S₀, Q, h) = (θ*(x), S₀(x), Q(x), h(x)): p ≤ n^A, |S₀| = s₀ < p, S₀ ⊆ Q, |Q| ≤ K, h is a
level vector for Q, ‖μ‖² ≤ Mn, (GF-16) holds, and the visibility condition holds at n. These are the requirements of
Proposition L5.2 on (X, θ*, Q, h).

## L8.1 The conditional law is Setting F

For a measurable set B of pairs (design, response) put f_B(x) := ∫1{(x, α(x)1 + xβ(x) + e) ∈ B}·N_n(0, σ²I)(de). By
Fubini f_B is measurable, and it is a version of P((X^r, y^r) ∈ B | X^r = x), because the conditional law of ε given
X^r is N_n(0, σ²I). For a fixed x, f_B(x) is the probability of B under **Setting F with the fixed design x**, coefficient
vector β(x) and noise N_n(0, σ²I): given x, the objects θ*(x), S₀(x), Q(x), h(x) and the partition are fixed. Nothing
about the response enters θ*, S₀, Q, h.

## L8.2 Proposition (inequality form)

**Proposition L8.2.** Let ε ∈ (0, 1), κ ∈ (0, κ_V), and C, C′, c₀, n₀ = n₀(ε, κ) as in Proposition L5.2. Let n ≥ n₀, let
ϱ̄ ≤ c₀, b̄ ≥ 0, r̄ ≥ 0 be numbers, and let 𝒳 be a measurable set of admissible designs at n such that every x ∈ 𝒳 has
b_n(h(x)) ≤ b̄ and ϱ_n(Q(x); h(x)) ≤ ϱ̄. Then
  (i) P(1 − π₀(𝓛(Q(X^r))) > C·ϱ̄ + n^{−κ}) ≤ ε + b̄ + P(X^r ∉ 𝒳),   𝓛(Q(X^r)) = {T : S₀(X^r) ⊆ T ⊆ Q(X^r)};
  (ii) if Q = S₀ on 𝒳 and n^{−1/2}𝔏⁰_n(h) + n^{−1}𝔏_n(S₀; h)² ≤ r̄ for every x ∈ 𝒳: P(o₀ > C′·r̄ + n^{−κ}) ≤ ε + b̄ + P(X^r ∉ 𝒳),
      o₀ the start odds against S₀(X^r).
The same holds with (ε, C, C′, c₀) replaced by (ε_n, C_n, C′_n, c_{0,n}) of Corollary L6.0′ for n ≥ n**(κ).

*Proof.* (i) Let B := {(x, y) : 1 − π₀(𝓛(Q(x)))(x, y) > Cϱ̄ + n^{−κ}}, a measurable set (with the convention of L8.0 off the
admissible designs). Then
P((X^r, y^r) ∈ B) ≤ P(X^r ∉ 𝒳) + E[1{X^r ∈ 𝒳}·f_B(X^r)]. For x ∈ 𝒳, by L8.1 and Proposition L5.2(i) applied to the fixed
design x (admissible, ϱ_n(Q(x); h(x)) ≤ ϱ̄ ≤ c₀):
f_B(x) ≤ P_x(1 − π₀(𝓛(Q(x))) > C·ϱ_n(Q(x); h(x)) + n^{−κ}) ≤ ε + b_n(h(x)) ≤ ε + b̄. (ii) is the same with L5.2(ii)
(ϱ_n(S₀; h) ≤ ϱ̄ ≤ c₀ is part of the hypothesis on 𝒳). The last sentence: use L6.0′ instead of L5.2. ∎

The constants of L5.2 depend only on (ε, κ) and the fixed constants — not on x, θ*(x), S₀(x), Q(x), h(x). That is all
the proof uses; no union over possible supports is taken.

## L8.3 Theorem (T3)(a)

Hypotheses of (T3)(a): fixed constants; deterministic ϱ̄_n → 0, b̄_n → 0; measurable sets 𝒳_n of admissible designs with
P(X^r ∈ 𝒳_n) → 1, b_n(h) ≤ b̄_n and ϱ_n(Q; h) ≤ ϱ̄_n on 𝒳_n. First take 0 < κ < κ_V and put κ″ := (κ + κ_V)/2.
For ε ∈ (0, 1) and all n ≥ n₀(ε, κ″) with ϱ̄_n ≤ c₀(ε), L8.2(i) gives
P(1 − π₀(𝓛(Q)) > C(ε)ϱ̄_n + n^{−κ″}) ≤ ε + b̄_n + P(X^r ∉ 𝒳_n), whose limsup is ≤ ε. As in `lemmas/L5_ASM_STARTF.md` L5.3(a)
(A_n := (X_n − n^{−κ″})₊ = O_P(ϱ̄_n), B_n := n^{−κ″} = o(n^{−κ})):
  **1 − π₀(𝓛(Q)) = O_P(ϱ̄_n) + o_P(n^{−κ})** under the joint law.
If Q = S₀ on 𝒳_n and n^{−1/2}𝔏⁰_n(h) + n^{−1}𝔏_n(S₀; h)² ≤ r̄_n on 𝒳_n for a deterministic r̄_n ≥ 0, L8.2(ii) gives in the same way
  **o₀ = O_P(r̄_n) + o_P(n^{−κ})**.
For κ ≤ 0, apply the proved result at any κ₀ ∈ (0, κ_V): its o_P(n^{−κ₀}) remainder is also o_P(n^{−κ}); this holds for both
displays. ∎

*Not covered:* supports, coefficients, sets Q or levels h that depend on the response; then the conditional law of
the noise given the targets is not N_n(0, σ²I) and L8.1 fails.
