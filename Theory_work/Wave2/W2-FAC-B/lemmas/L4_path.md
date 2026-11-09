# L4 — Key lemma: the LS0 path from S* is a pure backward elimination ending certified at S₀

Status: **PROVED (by this seat, unchecked)**; key-lemma check R04 (Codex Sol xhigh, reviews/R04_L4_check_sol.md):
VERIFIED-WITH-AMENDMENTS, no fatal issue; amendments 1–7 applied (reviews/R04_disposition.md). Falsification numerics: numerics/N3_summary.md (468 exact CS paths,
p ≤ 2·10⁴, n ≤ 10⁸, ρ ∈ {0.3, 0.7, 0.95}, s₀ ∈ {1, 4}, mixed/aligned signs: every run with n ≥ 10⁵ is a pure null
deletion with interval hole ending at S₀; the 10 exceptions are n ≤ 10⁴ with weak truths, where TL fails at finite
n), numerics/N5_raw.jsonl (**exploratory** diagnostic with bulk/end split at m = 20, not the proof's m₁ = ⌈K₁L_n⌉; it
does not test the proof's constants — R04 item 7), numerics/N6_raw.jsonl (direct test of the extended-gap invariant).

Setting: STATEMENT §1–2 (CS, P, θ; FS not needed here), L1 (Υ_n = I), L3 (event E_n, notation). The claim concerns
the **uncapped** §6.10 search started at S* = [p] ∖ N₀; caps enter only in L5.

**Lemma L4.** For n ≥ n₀ (depending on ρ, ϑ, σ, s₀), on E_n ∩ 𝒩𝒟_n, where 𝒩𝒟_n := {|ξ_j| ≠ |ξ_l| for distinct nulls; ξ_j ≠ x_T and |ξ_a − x_T| ≠ |ξ_b − x_T| for every
relevant T and distinct nulls j, a, b} (each excluded equality is a nontrivial linear relation, or a union of two, in
(η, ξ), finitely many per n, so P(𝒩𝒟_n) = 1; R04 item 5): the uncapped search from S* makes exactly m₀ moves; the move at T_i is the deletion
of the null j_i ∈ argmin_{j∈T_i∖S₀}|ξ_j − x_{T_i}| and has positive gain; every addition has gain ≤ −c log n with
c := min{0.29, c_D/2}, c_D = ½ − 1/(s₀ + 1 + (1 − ρ)/ρ) > 0, for n ≥ n₀ (council R09 suggestion 1); every truth deletion and truth-out swap has negative gain; every null-out swap and every other null
deletion has gain strictly below the chosen deletion's gain; T_{m₀} = S₀ and every feasible neighbour of S₀ has
strictly smaller F. (No claim is made about the sign of swap gains relative to F(T); R01 item 1.)

## L4.0 Preliminaries (exact, from L1)

For T with S₀ ⊆ T ⊆ S*, k := |T|, kept nulls K_T := T ∖ S₀, m := |K_T| = k − s₀, outside nulls O_T := (𝒩* ∖ T) ∪ N₀.
κ := α/β = (1 − ρ)/ρ + 1/(ρ(n² − 1)) (so γ_u = 1/(u + κ)), κ_∞ := (1 − ρ)/ρ ≤ κ ≤ κ_∞ + 1 (κ_∞ is unrelated to L1's
common z-component κ_c; R07 item 14).

**(a) Centre.** By L1.4, x_T = γ_k s_T − r_k and r_k = γ_k ϱ with the **k-free** constant
ϱ := [√(n − 1)ρθ̄/(σ√(1 − ρ)) + √(ρ/(1 − ρ)) α η]/β; so x_T = (s_T − ϱ)/(k + κ), |ϱ| ≤ C_ρ(|η| + 1) (c1).
**Drift identity**: for j ∈ T, x_{T∖j} = x_T − (ξ_j − x_T)/(k − 1 + κ) (since x_{T∖j}(k − 1 + κ) = s_T − ξ_j − ϱ
= x_T(k + κ) − ξ_j).
**(b) Gains.** With τ_j := ξ_j − x_T for nulls, τ_j := ξ_j − x_T + λ_θθ*_j for truths (λ_θ := λ₁/κ₁ = √((n − 1)(1 − ρ))/σ,
L1.1, L1.4),
M_T := νnκ₁²/(αψ_T) > 0 and V_{jl} := τ_l² − τ_j² − γ_k(τ_l − τ_j)², L1.3 gives exactly

  G_del(j) = Δ_k − ν log(1 + (1 + γ_{k−1})M_Tτ_j²/ν),  G_add(l) = −Δ_{k+1} − ν log(1 − (1 − γ_{k+1})M_Tτ_l²/ν),
  G_sw(j, l) = −ν log(1 − M_TV_{jl}/ν).

Hence (log(1 + u) ≤ u; −log(1 − u) ≤ u/(1 − u) for 0 ≤ u < 1):
(b1) G_del(j) ≥ Δ_k − (1 + γ_{k−1})M_Tτ_j², and G_del is strictly decreasing in |τ_j|;
(b2) G_add(l) ≤ −Δ_{k+1} + (1 − γ_{k+1})M_Tτ_l²(1 + 2u_l) when u_l := (1 − γ_{k+1})M_Tτ_l²/ν ≤ ½;
(b3) G_sw(j, l) < 0 if V_{jl} < 0, and G_sw(j, l) ≤ M_TV_{jl}(1 + 2M_TV_{jl}/ν) if 0 ≤ M_TV_{jl}/ν ≤ ½.
**(c) Thresholds** (L1.5(a)): Δ_k = log[(2p − k)/k] + ½log(n + 1) + δ_{n,k}, |δ_{n,k}| ≤ 3/((n − 1)(1 − ρ)).
For k ≤ p, Δ_k ≥ ½log(n + 1) − o(1); and with h := H̄²(≤ 2log(2p + 2) + 2L_n), log(2p) ≥ ½h − L_n − 1/p, so
Δ_k ≥ ½h + ½log n − log k − L_n − 2 for 1 ≤ k ≤ p/2 (using (2p − k)/k ≥ p/k).
**(d) The multiplier** (L1.5(b,c)): ¼ ≤ M_T on E_n (RSS_T ≤ ‖e‖², (c1)); and
M_T ≤ (1 + 1/n) n / (2(‖e‖²/σ² − Φ(T))) with Φ(T) ≤ Φ([p]) = gᵀΣ⁻¹g, so by E2 M_T ≤ (1 + 1/n)n/(2r) ≤ 1 + n^{−1/4}
(p ≤ n/2); and, since Σ_TT⁻¹ = (1 − ρ)⁻¹(I − γ′J) with γ′ ≥ 0, Φ(T) ≤ Σ_{j∈T}(ξ_j + √(ρ/(1 − ρ))η)²
≤ 2Σ_{j∈T}ξ_j² + 2kρη²/(1 − ρ). Thus (E1, E2) if Σ_{j∈T}ξ_j² + kL_n² ≤ n/log n then M_T ≤ ½(1 + C_ρ/log n).
**(e) Truth moves (TL).** On E_n, for every T with S₀ ⊆ T ⊆ S*: |x_T| ≤ (|s_T| + |ϱ|)/(k + κ) ≤ H̄ + C L_n, so for a
truth j, |τ_j| ≥ λ_θ|ϑ|_min − L_n − H̄ − CL_n ≥ λ_θ|ϑ|_min/2 =: τ_θ (n ≥ n₀), while every null has |τ_l| ≤ 2H̄ + CL_n
≤ τ_θ/4. Then (1 + γ_{k−1})M_Tτ_j²/ν ≥ ¼τ_θ²/(n/2 + 0.01) ≥ c_θ := (1 − ρ)|ϑ|²_min/(9σ²), so
G_del(j) ≤ Δ_k − ν log(1 + c_θ) ≤ log(2p) + ½log(n + 1) + 1 − (n/2)log(1 + c_θ) < 0; and for a truth-out swap,
V_{jl} ≤ τ_l² + 2γ_k|τ_j||τ_l| − (1 + γ_k)τ_j² ≤ τ_j²(1/16 + 1/2 − 1) < 0, so G_sw < 0. Truths are never added (all are
in T). **So every truth move has negative gain at every T between S₀ and S*.**

## L4.1 Interval structure (deterministic)

Let T_0 := S* and suppose the moves at T_0, …, T_{I−1} are deletions of nulls j_i ∈ argmin_{j∈K_{T_i}}|ξ_j − x_{T_i}|,
m_I ≥ 1. For each i ≤ I put x_i := x_{T_i}, a_i := max{ξ_j : j ∈ K_{T_i}, ξ_j ≤ x_i}, b_i := min{ξ_j : j ∈ K_{T_i},
ξ_j > x_i} (−∞ / +∞ if empty), L_i := x_i − a_i, R_i := b_i − x_i, d_i := min(L_i, R_i) = min_{j∈K}|ξ_j − x_i|.

**Claim L4.1.** For all i ≤ I: (i) 𝒩* ∖ T_i = {j ∈ 𝒩* : a_i < ξ_j < b_i} (the deleted nulls form an interval of the
sorted configuration around x_i); (ii) a side that is empty at T_i stays empty; (iii) if a_i < 0 < b_i then
K_{T_i} = Top₊(N₊) ∪ Top₋(N₋) (the N± nulls of sign ± with the largest |ξ|), N₊ := #{j ∈ K : ξ_j > 0};
(iv) if both sides are nonempty at T_i and T_{i+1}, then with Δ_i := |R_i − L_i| and g_i := the gap between the
deleted point and the next point of K_{T_i} on the same side,
  Δ_{i+1} ≤ max(Δ_i, g_i + 2d_i/(k_i − 1 + κ)).

*Proof.* (i) i = 0: the hole is empty and no point of 𝒩* lies strictly between a_0 and b_0 by definition. Step: the
point of K closest to x_i is a_i or b_i; say b_i is deleted (R_i ≤ L_i; the case a_i is symmetric). By the drift
identity x_{i+1} = x_i − R_i/(k_i − 1 + κ) < x_i < b_i, and x_i − x_{i+1} ≤ L_i/(k_i − 1 + κ) < L_i because
k_i − 1 + κ > 1 (k_i ≥ s₀ + 1 ≥ 2, κ > 0); so a_i < x_{i+1} < x_i. K_{T_i} has no point in (a_i, b_i), hence
a_{i+1} = a_i, b_{i+1} = min{ξ ∈ K_{T_i} : ξ > b_i} and the hole becomes (a_i, b_{i+1}) ∩ 𝒩*. (ii) is immediate from
the same computation. (iii) With a_i < 0 < b_i, K ∩ (0, ∞) = {ξ ≥ b_i} ∩ 𝒩*₊ and K ∩ (−∞, 0) = {ξ ≤ a_i} ∩ 𝒩*₋.
(iv) If b_i is deleted (R_i ≤ L_i): R_{i+1} = g_i + R_i + R_i/(k_i − 1 + κ), L_{i+1} = L_i − R_i/(k_i − 1 + κ), so
R_{i+1} − L_{i+1} = (R_i − L_i) + c with c := g_i + 2R_i/(k_i − 1 + κ) ≥ 0 and R_i − L_i ∈ [−Δ_i, 0]; hence
|R_{i+1} − L_{i+1}| ≤ max(Δ_i, c), and R_i = d_i. Symmetric for a_i. ∎

Also, with D⁺_i := max_{l∈𝒩*∖T_i}|ξ_l − x_i| (−∞ if the hole is empty), (i) gives, when both sides are nonempty,
D⁺_i < max(L_i, R_i) ≤ d_i + Δ_i.

## L4.2 Regime (S): p ≤ n^{1/200}

(This regime contains every bounded-p sequence; no balance or order-statistics argument is used. Regimes are
assigned per n, and n₀ does not depend on the regime, so arbitrary sequences p_n ≤ ⌊n/2⌋ are covered without
subsequences — R02 item 3. The argmin deletion makes L4.1 applicable here too, so the gap invariant holds.)

On E_n every |ξ_j| (j ∈ 𝒩*) is ≤ H̄ with H̄² ≤ 2 log(2n^{1/200} + 2) + 2L_n ≤ (1/90)log n, and |x_T| ≤ H̄ + C L_n;
so every null has τ² ≤ (2H̄ + CL_n)² ≤ (2√((log n)/90) + CL_n)² ≤ 0.1 log n for n ≥ n₀, uniformly in the regime (C fixed,
L_n/√log n → 0; no comparison of L_n with H̄ is needed — R04 item 1; N₀ coordinates obey the same bound by E1). With M_T ≤ 1 + o(1), 1 ± γ ≤ 2, Δ ≥ ½log(n + 1) − o(1):
every null deletion has G_del ≥ 0.29 log n, every addition G_add ≤ −0.29 log n, every null-out swap
G_sw ≤ M_T τ_l² (1 + o) ≤ 0.11 log n (V ≤ τ_l² as γ_k ≥ 0), and truth moves are negative (L4.0(e)). So at every
T ≠ S₀ the best move is a null deletion (the argmin of |τ|), and at S₀ no move improves. ∎(S)

## L4.3 Regime (L), bulk phase (m ≥ m₁)

Throughout L4.3–L4.4, ε_b := ε_bal = 1/50 (L3; renamed from η, which denotes the Gaussian factor — R03 item 4).

**Claim B.** Let i < i* where i* is the first index with m_{i*} < m₁. Suppose the moves at T_0, …, T_{i−1} are argmin
null deletions. Then (B1) both sides of x_i are nonempty; (B2) Δ_i ≤ ε_bH/2; (B3) |x_i| ≤ ε_bH; (B4) the move at T_i is an
argmin null deletion, with G_del ≥ 0.3 log n, all additions ≤ −0.3 log n and all swaps below G_del. (Entry into the
end phase at i* uses only the drift estimate of L4.4, not B1–B3 at i*; R04 item 4.)

*Proof* by induction on i, proving B1, B2, B3, B4 **in this order** at each i (B3 at i uses B2 at i, B2 at i uses B1 at i
and i − 1, B1 at i uses B3 at i − 1).

**i = 0.** x_0 = (s_{S₀} + D_{m₀} − ϱ)/(p − |N₀| + κ) with |D_{m₀}| ≤ H̄√(2m₀x_{m₀}) (E5), so |x_0| ≤ C(L_n + H̄√(m₀ log n))/m₀
→ 0; E6 gives nulls of both signs with |ξ| ≥ H − δ_e > |x_0|, so (B1); Δ_0 ≤ b_0 − a_0 ≤ g_max (c2) ≤ ε_bH/2.

**(B3) at i.** Case A: a_i < 0 < b_i. If x_i > Δ_i/2 then b_i + a_i = (R_i − L_i) + 2x_i > 0, so b_i > |a_i| and
K := K_{T_i} = {ξ ≤ a_i} ∪ {ξ ≥ b_i} ⊆ K⁰ := {j ∈ 𝒩* : |ξ_j| ≥ |a_i|} = Top(J), J := |K⁰|, with K⁰ ∖ K consisting of
positive ξ's; hence s_K ≤ D_J and x_i(k + κ) = s_{S₀} + s_K − ϱ ≤ s_{S₀} − ϱ + |D_J|. In Top(J) the negatives are exactly
the N₋ kept negatives, so by E5 J − 2N₋ = 2P_J − J ≤ 2√(Jx_J/2), whence J ≤ 2N₋ + √(2Jx_J) ≤ 4m + 4x_J. If J ≥ 5m, then (x_u/u is decreasing for u ≥ u₀) x_J/J ≤ x_{5m₁}/(5m₁) < 1/20 for
n ≥ n₀, so J ≤ 4m + J/5, i.e. J ≤ 5m. Hence J ≤ 5m in all cases (R04 item 2).
Therefore x_i ≤ [s₀L_n + C L_n + H̄√(10m x_{5m})]/m ≤ ε_bH, because u ↦ (2 log(5u + 1) + L_n)/u is decreasing for
u ≥ 3, so 10x_{5m}/m ≤ 10(2 log(5m₁ + 1) + L_n)/m₁ ≤ 11/K₁ = 0.11ε_b² for m ≥ m₁ = ⌈K₁L_n⌉ and n ≥ n₀ (H̄ ≤ 1.01H),
and (s₀ + C)L_n/m ≤ ε_bH/10. (This needs 2 log(5K₁L_n + 1) ≤ 0.1L_n, i.e. L_n ≳ 400: the onset n₀ is astronomically
large — admissible under the asymptotic scope rule, and far beyond every simulated n; R09 suggestion 2.) Symmetrically x_i < −Δ_i/2 implies x_i ≥ −ε_bH. Otherwise
|x_i| ≤ Δ_i/2. Case B: a_i ≥ 0 (resp. b_i ≤ 0). Then every negative null is kept (resp. every positive), so
m ≥ m₀/3 (E5), and the hole lies in (a_i, b_i) ⊆ [0, ∞), so s_K ≤ D_{m₀}; with x_i > a_i ≥ 0:
0 < x_i ≤ (CL_n + H̄√(2m₀x_{m₀}))/(m₀/3) ≤ ε_bH. Symmetric for b_i ≤ 0.

**(B2) at i ≥ 1.** By L4.1(iv) and (B1) at i − 1 and i, Δ_i ≤ max(Δ_{i−1}, g_{i−1} + 2d_{i−1}/(k_{i−1} − 1 + κ)) with
g ≤ g_max = O(L_n) (c2) and d_{i−1} ≤ max(|a|, |b|) + |x| ≤ H̄ + ε_bH, k_{i−1} − 1 + κ ≥ m₁: so Δ_i ≤ ε_bH/2 for n ≥ n₀.

**(B1) at i ≥ 1.** Suppose the lower side of T_{i−1} is a single point a and it is deleted (the upper case is
symmetric). The hole of T_{i−1} is (a, b) and contains every other null below b, so a = min_{𝒩*}ξ. If a ≥ 0 all negative
nulls would lie in the hole above a — impossible; so a < 0 and |a| = ζ₋_(1) ≥ H − δ_e (E6). The deletion requires
L ≤ R, i.e. |a| + x ≤ b − x, so b ≥ H − δ_e − 2ε_bH ≥ (1 − 3ε_b)H (B3 at i − 1). The upper side has N₊ = m_{i−1} − 1 ≥ m₁ − 1
points, all ≥ b, so x_{i−1}(k + κ) ≥ N₊(1 − 3ε_b)H − H̄ − CL_n − s₀L_n with k + κ = N₊ + 1 + s₀ + κ, giving
x_{i−1} ≥ (1 − 4ε_b)H > ε_bH for n ≥ n₀ — contradicting (B3) at i − 1. (The inequality b ≥ (1 − 3ε_b)H > 0 already excludes b ≤ 0; R07 item 5.)

**(B4) at i < i*.** Fix T = T_i, m = m_i ≥ m₁, k = m + s₀. Some kept null has |ξ| ≤ ζ_(m) (it has m elements), so
d := d_i ≤ Z_m + ε_bH (E4, B3); every hole null has |τ| ≤ D⁺ ≤ d + Δ ≤ Z_m + 2ε_bH; every l ∈ N₀ has
|τ_l| ≤ L_n + ε_bH. Write Z := Z_m, ε′ := any o(1) term.
*Case (i): m ≤ n/log³ n.* Σ_Tξ² + kL_n² ≤ s₀L_n² + m(H̄² + L_n²) + s₀L_n² ≤ n/log n, so M_T ≤ ½(1 + ε′) (L4.0(d)); also
γ_{k−1} ≤ 1/m₁. Using (u + v)² ≤ (1 + 2ε_b)u² + (1 + 1/(2ε_b))v² (Young with parameter 2ε_b; R04 item 3) and
H² ≤ 2 log(n + 2), with A := log(2m₀/m) + 2L_n:
(1 + γ_{k−1})M_T d² ≤ (1 + ε′)[(1 + 2ε_b)A + (ε_b/2 + ε_b²) log n] ≤ (1 + 2ε_b)A + ε_b log n + o(log n)
(ε_b/2 + ε_b² < ε_b absorbs the o(log n) multiplier and γ corrections for n ≥ n₀).
Since m₀ ≤ p, k ≤ m + s₀ and p ≥ k: log(2m₀/m) ≤ log[(2p − k)/k] + log 2 + log(1 + s₀/m) + log 2. With
log[(2p − k)/k] ≤ log(2p) ≤ log n and (c): G_del ≥ Δ_k − (1 + γ)M d² ≥ ½ log n − 2ε_b log n − 3ε_b log n − O(L_n)
≥ 0.35 log n (ε_b = 1/50). Additions (hole or N₀), using Δ_{k+1} and log(2m₀/m) ≤ log[(2p − k − 1)/(k + 1)] + 3 log 2 +
log(1 + (s₀ + 1)/m) (for k + 1 ≤ p): (1 − γ_{k+1})M τ_l²(1 + 2u_l) ≤ (1 + 4ε_b)A + (ε_b + 4ε_b²)log n + o(log n) ≤ (1 + 4ε_b)[log((2p − k − 1)/(k + 1)) + O(L_n)]
+ 2ε_b log n (Young with parameter 4ε_b),
so G_add ≤ −½log n + 6ε_b log n + O(L_n) < −0.3 log n (u_l = O(log n/n)). Null-out swaps: V_{jl} ≤ τ_l² − τ_j²
≤ (D⁺)² − d² ≤ Δ(2d + Δ) ≤ ε_bH(2Z + 3ε_bH) ≤ ε_b(H² + Z²) + 3ε_b²H² ≤ 5ε_b log n, so G_sw ≤ M V(1 + ε′) ≤ 3ε_b log n
< G_del; swaps with l ∈ N₀ have V ≤ τ_l² ≤ 2L_n² + 2ε_b²H² — smaller. Truth moves < 0 (L4.0(e)).
*Case (ii): m > n/log³ n.* Z² ≤ 2 log(2p log³ n/n) + 4 log log n ≤ 10 log log n (p ≤ n/2); M_T ≤ 1 + ε′, γ ≤ 1/m₁:
(1 + γ)Md² ≤ (1 + ε′)(2Z² + 2ε_b²H²) ≤ 0.01 log n, so G_del ≥ 0.45 log n; additions: τ² ≤ 2Z² + 8ε_b²H² ⇒
G_add ≤ −0.45 log n; swaps: V ≤ ε_bH(2Z + 3ε_bH) ≤ 3ε_b log n ⇒ G_sw ≤ 0.07 log n < G_del.
In both cases the best move is a null deletion, and among null deletions G_del is maximised by the minimiser of |τ|
(b1). ∎(Claim B)

## L4.4 Regime (L), end phase (m < m₁)

Let i_e := i* (so m_{i_e} = m₁ − 1). **Entry bound:** by the drift identity and (B3) at i_e − 1,
|x_{i_e}| ≤ ε_bH + (H̄ + ε_bH)/(m₁ − 2) ≤ 2ε_bH.

**Structure.** For i ≥ i_e: a_i < 0 < b_i unless that side is empty (if a_i ≥ 0 all negative nulls would be kept,
m ≥ m₀/3 > m₁), so by L4.1(iii) K_{T_i} = Top₊(N₊) ∪ Top₋(N₋) with N₊ + N₋ = m < m₁; by E6, E3 every kept null has
|ξ| ∈ [H̄ − 2δ_e, H̄]. Let I_i := N₊ − N₋ and write s_K = I_iH̄ + E_i with |E_i| ≤ 2m₁δ_e. Then

  x_i = (I_iH̄ + E′_i)/(k + κ),  |E′_i| ≤ s₀L_n + C L_n + 2m₁δ_e =: e_n = O(L_n).

Every outside null l has |ξ_l| ≤ H̄. For **retained** nulls τ = ±H̄ − x + O(δ_e), so replacing their exact magnitudes by
H̄ changes τ² by O(H̄δ_e) = O(L_n); outside coordinates are never replaced — they enter only through the envelope
|ξ_l| ≤ H̄ (E-add) and convexity in τ_l (E-swap) (R04 item 6). With B := s_{S₀} − ϱ = O(L_n) = o(H̄),
|x| ≤ (mH̄ + |B|)/(m + s₀ + κ) < H̄ and H̄ − |x| ≫ δ_e for m < m₁, so every retained positive lies above x and every
retained negative below x. One-sided configurations: if a = −∞ and b ≤ 0, every positive null would be retained
(m ≥ m₀/3) — impossible; symmetrically, so a < 0 < b in the extended sense and L4.1(iii) applies after a side empties. Here M_T = ½(1 + ε′) (Σ_Tξ² ≤ m₁H̄² + s₀L_n²),
h := H̄² ≤ 2 log(n + 2) + 2L_n, and k ≤ s₀ + m₁ = O(L_n), so Δ_k = ½h + ½log n − O(L_n) (L4.0(c), also the upper
bound Δ_k ≤ ½h + ½ log(n + 1) + 1). All error terms below are O(H̄ e_n + h ε′ + L_n) = o(log n) uniformly. The bounds below are stated for I_i ≥ 0; the case I_i < 0 is the deterministic sign reversal of ξ **and of the offset
ϱ** in these bounds (reflecting ξ alone does not negate ϱ when θ̄ ≠ 0; R04 item 6).

**Entry imbalance.** |I_{i_e}| ≤ (|x_{i_e}|(k + κ) + e_n)/H̄ ≤ 2ε_b(k + κ) + o(1), i.e. c_I := |I|/(k + κ) ≤ 2ε_b + o(1).

**(E-del) best deletion.** If I ≥ 1, take j kept with ξ_j > 0: τ_j ≤ H̄ − x, and
(1 + γ_{k−1})τ_j² ≤ ((k + κ)/(k − 1 + κ))·h(1 − I/(k + κ))² + o(log n) = h(k + κ − I)²/((k − 1 + κ)(k + κ)) + o
≤ h(k + κ − 1)/(k + κ) + o (as 1 ≤ I ≤ m < k). So G_del ≥ Δ_k − ½h(1 − 1/(k + κ)) − o ≥ ½log n − o(log n).
If I = 0 (then m ≥ 2, k ≥ s₀ + 2): (1 + γ_{k−1})τ_j² ≤ h(k + κ)/(k − 1 + κ) + o, so
G_del ≥ ½log n − ½h/(k − 1 + κ) − o ≥ ½log n − log n/(s₀ + 1 + κ_∞) − o(log n) = c_D log n − o(log n),
c_D := ½ − 1/(s₀ + 1 + κ_∞) > 0 (s₀ ≥ 1, κ_∞ > 0).

**(E-side) the deleted null is on the majority side.** If I ≥ 1: x ≥ (H̄ − e_n)/(k + κ) ≥ H̄/(2(s₀ + m₁ + κ)) ≫ δ_e, and the
closest positive kept point has |τ| ≤ H̄ − x while every negative kept point has |τ| ≥ H̄ − 2δ_e + x > H̄ − x. So the
argmin deletion removes a positive null: I_{i+1} = I_i − 1. If I = 0, |I_{i+1}| = 1. Consequently |I_i| ≤ max(|I_{i_e}|, 1)
for all i ≥ i_e, and whenever |I_i| ≥ 2, c_I(i) = |I_i|/(k_i + κ) ≤ c_I(i_e) ≤ 2ε_b + o (each step lowers |I| and k by one,
and (|I| − 1)/(k − 1 + κ) ≤ |I|/(k + κ) iff |I| ≤ k + κ).

**(E-add) additions fail.** For l outside, |τ_l| ≤ H̄ + |x| ≤ H̄(1 + |I|/(k + κ)) + e_n/(k + κ), so
(1 − γ_{k+1})τ_l² ≤ h(k + κ + |I|)²/((k + κ)(k + κ + 1)) + o, and G_add ≤ −Δ_{k+1} + ½(1 + ε′)·that:
- I = 0 (including T = S₀, m = 0): ≤ h(k + κ)/(k + κ + 1) < h, so G_add ≤ −½log n + o(log n);
- |I| = 1: ≤ h(1 + 1/(k + κ)) + o, k + κ ≥ s₀ + 1 + κ_∞, so G_add ≤ −½log n + log n/(s₀ + 1 + κ_∞) + o = −c_D log n + o;
- |I| ≥ 2: ≤ h(1 + c_I)² + o ≤ h(1 + 6ε_b) + o, so G_add ≤ −½log n + 6ε_b log n + o < −0.3 log n.

**(E-swap) swaps lose.** V_{jl} = (1 − γ_k)τ_l² + 2γ_kτ_jτ_l − (1 + γ_k)τ_j² is convex in τ_l (γ_k < 1), and
τ_l ∈ [−H̄ − x, H̄ − x] for every outside l; so V is at most its value at an endpoint. For j kept on side σ
(τ_j = σH̄ − x + O(δ_e)): at the same-side endpoint τ_l = σH̄ − x, V = O(H̄δ_e); at the opposite endpoint, a direct
expansion gives V = 4σH̄(x − σγ_kH̄) + O(H̄δ_e) = 4γ_k h(σI − 1) + O(H̄e_n). Hence V ≤ 4h(|I| − 1)₊/(k + κ) + o(log n),
G_sw ≤ M V(1 + ε′) ≤ 2h(|I| − 1)₊/(k + κ) + o ≤ 4c_I·log(n + 2)·1{|I| ≥ 2} + o(log n), which is ≤ 8ε_b log n + o when
|I| ≥ 2 (then I ≠ 0 and G_del ≥ ½log n − o) and o(log n) when |I| ≤ 1 (G_del ≥ c_D log n − o). Truth moves < 0.

So for i ≥ i_e with m_i ≥ 1 the move is an argmin null deletion; after m₁ − 1 further moves T = S₀, where every
addition has G_add ≤ −½log n + o(log n) < 0 and every truth move has negative gain: S₀ has no improving feasible
neighbour. ∎(L4)

## L4.5 Remarks

1. For every nonnegative integer cap a, the capped search follows the uncapped path for min(a, m₀) moves and then one
   further scan (single-search prefix property, from the loop rule (L3) of Lemma CAP's setting, FINAL s7 — valid for every
   cap; the integration/monotonicity statement of CAP itself is used only for a ≥ ℓ_n, as in L5). m₀ = |S̃₀ ∖ S₀| on the
   event of L2 (R07 item 7).
2. Ties (exact arithmetic): G_del is strictly monotone in |τ|; on 𝒩𝒟_n no two retained nulls are equidistant from x_T
   and no ξ_j equals x_T, so the chosen deletion is unique and strictly better than every other
   null deletion. All other move types have strictly smaller gain, so the production tie rule is never invoked.
3. What is "path-restricted": NA is **false** on the lattice [S₀, S*] in general (e.g. adding an extreme null to a set
   whose kept nulls are all aligned with it, numerics N1 intermediate n); the proof only uses the sets the path visits:
   interval holes (L4.1), the sign-symmetric bound on D_J for the path's threshold sets (B3), and the end-phase
   imbalance dynamics (E-side).
