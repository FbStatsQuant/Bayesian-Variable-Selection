# L2 — Key negative lemma: under MR1 the LS0 route fails (claim (P2))

Status: **PROVED (by this seat, unchecked)**; lemma check R03 (Codex Sol xhigh, reviews/R03_L0L1L2_check_sol.md):
VERIFIED-WITH-AMENDMENTS (no-ties event propagated), applied. v2 (R01 item 6: threshold t_n, nonnegative integer caps, [OP] wording). Falsification numerics: N1 (60 data sets), N3
(360 data sets): `lead_swaps` = W and no deletion before move W in every path; numerics/l12_check.py → L12_check.jsonl
(bounds (i), (ii) on 66 size-K sets) and l2_chain.py → L2_chain_summary.txt (each link of (iii) with the actual most
extreme outside null, 48 sets). Limits [R07-9]: the simulated n never reach t_n (all six L1 samples have N_n = 0; none of
the 66 sets has an outside null below −t_n), so (N2) and the threshold event of (iii) are supported analytically only.

Setting: STATEMENT §1–2: G, (CS) (Υ_n = I), (PK), (PB), (θ) with θ̄ > 0; **(TK) is not assumed**. L0 notation; L1's
event E^S_n and Lemma L1. "Swap" = an exchange (j out, l in) of the §6.10 neighbourhood; at |T| = K the feasible
neighbours are the K deletions and the K(p − K) swaps (additions would leave Ω).

## L2.1 The event E^N_n
Fix β ∈ (0, ½). Put t_n := 2 + (log n + 30)^{1/2} (a threshold, not the MR1 cap a_n; R01-6).
* (N1) #{j ∈ [p] : |ξ_j| > 1.5} ≤ 0.14p and Σ_{j∈[p]}|ξ_j| ≤ 0.81p;
* (N2) N_n := #{b ∈ 𝔅 : min_{j∈C_b}ξ_j ≤ −t_n} ≥ n^β.
P(E^N_n) → 1. (N1): Hoeffding for the bounded indicators 1{|ξ_j| > 1.5} (mean 2Φ̄(1.5) = 0.1336) and Bernstein for the
sub-Gaussian |ξ_j| (mean √(2/π) = 0.7979); p → ∞ by (PK). (N2): the block minima of distinct regular blocks are
independent (disjoint coordinates of ξ; 𝔅 is deterministic); each satisfies P(min ≤ −t_n) ≥ Φ̄(t_n) ≥ φ(t_n)/(2t_n)
= n^{−1/2}exp(−17 − 2(log n + 30)^{1/2})/(2t_n√(2π)) =: q_n; |𝔅| ≥ (p − 16(J₀ + s₀))/16 ≥ n/33 for n ≥ n₀ (p > K ≥ (n − 1)/2).
So N_n stochastically dominates Bin(⌈n/33⌉, q_n), whose mean n q_n/33 ≥ n^{1/2 − o(1)} ≫ n^β; Chernoff:
P(Bin < mean/2) ≤ exp(−mean/8) → 0.

## L2.2 Static scan bounds at size K
**Lemma L2.2.** For n ≥ n₀, on E^S_n ∩ E^N_n ∩ 𝒟_n (𝒟_n: no ties among the ξ_j, L1; P(𝒟_n) = 1) [R03-2], for **every** T ∈ Ω with |T| = K:
(i) every deletion has gain G_del(j) ≤ Δ_K ≤ ½log n + log 3 + 1/K + 4/((n − 1)(1 − ρ)) < ½log n + 1.2;
(ii) if S₀ ⊄ T, some swap has gain ≥ c₃n (c₃ = c₃(ρ, ϑ, σ) > 0);
(iii) if S₀ ⊆ T and some null l ∉ T has ξ_l ≤ −t_n, some swap has gain ≥ ½log n + 2.
Consequently, in cases (ii) and (iii) the best scanned neighbour of T is a swap and strictly increases F.

*Proof.* (i) L0.3: G_del(j) = Δ_K − ν log(1 + n(1 + γ_{K−1})t_j²/(αψ_T)) ≤ Δ_K for every j ∈ T (truth or null, any T).
L0.5(a): Δ_K = log[(2p − K)/K] + ½log(n + 1) + δ_{n,K}; p ≤ n − 1 ≤ 2K + 1 gives (2p − K)/K ≤ 3 + 2/K.
(ii) Pick l ∈ S₀ ∖ T and a null j ∈ T (|T| = K > s₀). By L0.3, G_sw(j, l) = −ν log(1 − nV/(αψ_T)) with
V = t_l² − t_j² − γ_K(t_l − t_j)² = (1 − γ_K)(t_l − t_j)² + 2t_j(t_l − t_j). Here t_l − t_j = z_l − z_j =
κ₁(ξ_l − ξ_j) + λ₁θ*_l with |λ₁θ*_l| = (n − 1)(1 − ρ)|ϑ_l|/s ≥ c₄n and |κ₁(ξ_l − ξ_j)| ≤ 2κ₁H̄ = O(√(n log n)), so
c₄n/2 ≤ |t_l − t_j| ≤ C n. And t_j = z_j − γ_KB_T with B_T = Kκ_c + κ₁s_T + λ₁ϑ(T ∩ S₀), so
t_j = κ_cκ/(K + κ) + κ₁(ξ_j − γ_Ks_T) − γ_Kλ₁ϑ(T ∩ S₀); by L1.1 and (N1) (|s_T| ≤ Σ_{[p]}|ξ| ≤ 0.81(2K + 1)),
|t_j| ≤ C + κ₁(H̄ + 1.7) + C ≤ C√n H̄. Hence V ≥ (1 − γ_K)c₄²n²/4 − 2C√nH̄·Cn ≥ c₄²n²/8, and with α ≤ n², ψ_T ≤ n:
nV/(αψ_T) ≥ c₄²/8 ≥ c₅ := min(c₄²/8, ½) ∈ (0, 1) [R09-E3] (the argument of the log is ψ_{T∖j∪l}/ψ_T ∈ (0, 1)). So G_sw ≥ −ν log(1 − c₅) ≥ (n/2)c₅.
(iii) S₀ ⊆ T, so L0.4/L0.6 apply. |x_T| = |s_T − ϱ|/(K + κ) ≤ (0.81(2K + 1) + C_ρ(L_n + 1))/K ≤ 2. The nulls j with
|ξ_j − x_T| > 3.5 have |ξ_j| > 1.5, so by (N1) there are at most 0.14p ≤ 0.14(2K + 1) < K − s₀ of them: some null j ∈ T has
|τ_j| ≤ 3.5. For l: τ_l = ξ_l − x_T ≤ −t_n + 2, so τ_l² ≥ log n + 30, and |τ_l| ≤ H̄ + 2. Then
V_{jl} ≥ (1 − γ_K)τ_l² − 2γ_K|τ_l||τ_j| − (1 + γ_K)τ_j² ≥ log n + 30 − O(log n/K) − 24.6 ≥ log n + 5.
L0.5(c) with RSS_T ≤ ‖e‖² ≤ σ²(n − 1 + n^{2/3}) and s²c_ρ ≤ C gives M_T ≥ ½(1 − 3n^{−1/3}); L0.6:
G_sw(j, l) ≥ M_TV_{jl} ≥ ½(1 − 3n^{−1/3})(log n + 5) ≥ ½log n + 2.
Consequence: at |T| = K the scanned neighbours are deletions and swaps; by (i) and (ii)/(iii) the maximal F among
them is attained only by swaps and exceeds F(T). ∎

## L2.3 The first N_n moves are swaps
**Lemma L2.3.** For n ≥ n₀, on E^S_n ∩ E^N_n ∩ 𝒟_n, let C_0 := S̃₀ (any maximiser of γ₀, L1) and C_0, C_1, … the uncapped
§6.10 path. Then its first N_n moves are swaps; in particular |C_i| = K for i ≤ N_n and m* ≥ N_n.

*Proof.* O* := {regular-block minima with ξ ≤ −t_n}: |O*| = N_n and O* ∩ C_0 = ∅ by L1(d). Induction on i < N_n:
|C_i| = K (L1(a) for i = 0; swaps preserve size). Each move adds at most one variable, so |O* ∖ C_i| ≥ N_n − i ≥ 1.
If S₀ ⊄ C_i apply L2.2(ii), else L2.2(iii) with some l ∈ O* ∖ C_i: the move at C_i exists and is a swap. ∎

## L2.4 Theorem NEG (claim (P2))
**Theorem NEG.** Under G, (CS), (PK), (PB), (θ) (θ̄ ≠ 0) and the LS0 premises (OP-LS0, e4′, complete scans):
(i) P(LS0(a_n) scores S₀) → 0 for the merged cap a_n = ℓ_n + |S̃₀|, and for the legacy cap ℓ_n;
(ii) for every fixed β < ½, P(∃ a ∈ ℤ_{≥0}, a ≤ |S̃₀| − s₀ − 2 + n^β, such that LS0(a) scores S₀) → 0 [R07-11].

*Proof.* On E^S_n ∩ E^N_n ∩ 𝒟_n (n ≥ n₀): by the single-search prefix property (loop rule (L3) of FINAL `s7_impl.tex`,
valid for every nonnegative integer cap), LS0(a) scans exactly C_0, …, C_{min(a, m*)} of the uncapped path and its
scored set is {C_0} ∪ ⋃_{i ≤ min(a, m*)} N(C_i). Let a be a nonnegative integer with a ≤ K − s₀ − 2 + N_n. For i ≤ min(a, m*), the number of deletions
among the first i moves is ≤ max(0, i − N_n) ≤ K − s₀ − 2 (L2.3), and additions only enlarge, so |C_i| ≥ s₀ + 2; every
member of {C_i} ∪ N(C_i) then has ≥ s₀ + 1 elements, so S₀ is not scored. (ii) follows since |S̃₀| = K (L1(a)) and
N_n ≥ n^β. (i): a_n = ℓ_n + K ≤ K − s₀ − 2 + N_n because N_n ≥ n^β ≥ ℓ_n + s₀ + 2 for n ≥ n₀; ℓ_n ≤ a_n. Finally
P(E^S_n ∩ E^N_n ∩ 𝒟_n) → 1 (L1.1, L2.1, P(𝒟_n) = 1). ∎

## L2.5 Remarks (reading)
1. **What this refutes.** The *LS0 route* to reported-model consistency under MR1: [OP]'s upper bound
   D_n ≤ P(LS0(a_n) misses S₀) is asymptotically uninformative (its right side → 1); NEG gives no lower bound on D_n. It is **not** a statement that the full method fails:
   the SMC run and the final local search may still score S₀ (claim (P6), numerics).
2. **Necessary allowance.** (ii) shows that a cap |S̃₀| + o(n^{β}) fails for every β < ½: an additive O(log n) or
   O(polylog) allowance (as in MR1) cannot work on this class; any repair needs a polynomial swap allowance.
3. **No path history, no (TK).** The proof is static (bounds valid at every size-K set) plus counting; it does not
   need the start to contain S₀ nor any control of the centre beyond |x_T| ≤ 2.
4. **Sharpness heuristic (not used).** With M_T ≈ M_W the swap phase lasts while some outside null has
   M_Wτ² > Δ_K ≈ ½log n, i.e. W ≈ p·n^{−1/(4M_W)} up to polylog factors (N3: observed M_W ≈ 0.484–2.723; an observation, separate from the asymptotic bound M_T ≥ ½ − o(1)) [R07-4]; ½ − ε is the exponent
   forced by the crude bound M_T ≥ ½.
