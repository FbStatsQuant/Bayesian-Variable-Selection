# L3 — Key positive lemma: static gain bounds on the lattice above S₀ and the path-length budget (claim (P3))

Status: **PROVED (by this seat, unchecked)**; lemma check R04 (Codex Sol xhigh, reviews/R04_L3_check_sol.md):
VERIFIED-WITH-AMENDMENTS (3 minor, 1 editorial), applied [R04-#]. Falsification numerics: numerics/l3_static.py →
L3_static.jsonl, L3_static_summary.txt (best-deletion gains on random, adversarial and path sets; budget), l3_trend.py →
L3_trend.txt, l3_small.py → L3_small_summary.txt (adversarial small m), N1/N3 (m* vs K); reviewer scratch
reviews/R04_scratch/ (exhaustive pair maximisation of d_T, 9.6·10⁷ pairs; no counterexample).

Setting: G, (CS) (Υ_n = I), (θ) with θ̄ > 0 and every ϑ_r ≠ 0, blocks of size ≤ 16 (any deterministic partition),
and **(PK′)** K + 16s₀ + 1 ≤ p ≤ n − 1 for n ≥ n₀. (Neither (TK) nor (PB) nor the 16/15 condition is used here.)
L0 notation. 𝒯 := {T ∈ Ω : S₀ ⊆ T}; for T ∈ 𝒯: k := |T|, m := k − s₀, R_T := T ∖ S₀ (retained nulls),
x := x_T, τ_j := ξ_j − x for nulls, d_T := min_{j∈R_T}|τ_j| (m ≥ 1). Constants: κ_∞ := (1 − ρ)/ρ,
c_D := ½ − 1/(s₀ + 1 + κ_∞) > 0, m_e := ⌈log² n⌉, h := H̄² = 2 log(2p) + 2L_n.

## L3.1 Events
* (E1) |η| ≤ L_n; max_{j∈[p]}|ξ_j| ≤ H̄; |ξ_j| ≤ L_n for j ∈ S₀; (E2) |‖e‖²/σ² − (n − 1)| ≤ n^{2/3},
  |θ*ᵀg| ≤ L_n(θ*ᵀΣθ*)^{1/2} (as L1.1).
* (E3) tail counts: for every t ∈ ℝ, U₊(t) := #{null j : ξ_j ≥ t} ≤ 2pΦ̄(t) + 5 log n and
  U₋(t) := #{null j : ξ_j ≤ −t} ≤ 2pΦ̄(t) + 5 log n.
* (E4) multiplier floor: RSS_T ≥ c_M σ² n for every T ∈ 𝒯 (c_M > 0 an absolute constant below).
P(E1 ∩ … ∩ E4) → 1. (E3): for a grid t_i = i/n, |t_i| ≤ H̄ + 1, U₊(t_i) ~ Bin(p′, Φ̄(t_i)) (p′ ≤ p nulls) and Bernstein gives
P(Bin ≥ 2p′q + λ) ≤ exp(−3λ/8) (q := Φ̄(t_i)); with λ = 4 log n and O(n√log n) grid points the union → 0. For t between
grid points U₊(t) ≤ U₊(t_i) ≤ 2pΦ̄(t_i) + 4 log n ≤ 2pΦ̄(t) + 2p/n + 4 log n; beyond the grid U₊ = 0 or the bound is trivial.
(E4): RSS_T/σ² = r + (Φ([p]) − Φ(T)) (FACB L1.5(b), ‖e‖² = σ²(Φ([p]) + r)), r ~ χ²_{n−1−p}, and for each fixed T,
Φ([p]) − Φ(T) = ‖(P_X − P_T)e‖²/σ² ~ χ²_{p−|T|}. Since (n − 1 − p) + (p − K) = n − 1 − K ≥ n/2 − 1, for each n either
n − 1 − p ≥ n/5 (then r ≥ n/10 w.p. ≥ 1 − e^{−cn}) or p − K ≥ n/4; in the latter case, by the χ² lower tail
P(χ²_d ≤ cd) ≤ (ce)^{d/2} and a union bound over ≤ 2^p ≤ 2^n sets T with p − |T| ≥ n/4:
P(∃T : Φ([p]) − Φ(T) ≤ c(p − |T|)) ≤ 2^n(ce)^{n/8} → 0 for c := 2^{−9}/e. So c_M := min(1/10, c/4) works.
**Consequences.** (M1) M_T ≤ C_M := 2/c_M for all T ∈ 𝒯 (L0.5(c) upper bound). (M2) If Σ_{j∈T}ξ_j² + kL_n² ≤ n/log n
then M_T ≤ ½(1 + C/log n) (FACB L4.0(d): RSS_T ≥ ‖e‖² − σ²Φ(T), Φ(T) ≤ 2Σ_Tξ² + 2kρη²/(1 − ρ)). (M3) M_T ≥ ½(1 − 3n^{−1/3})
(L2.2(iii)). (X) For T ∈ 𝒯, |x| ≤ (mH̄ + C L_n)/(m + s₀ + κ) ≤ H̄ + CL_n (L0.4: x(k + κ) = Σ_{R_T}ξ + s_{S₀} − ϱ).

## L3.2 The centring identity
For T ∈ 𝒯, Σ_{j∈R_T}τ_j = E_T := x(s₀ + κ) − s_{S₀} + ϱ, and |E_T| ≤ (s₀ + κ_∞ + 1)(H̄ + CL_n) + CL_n =: e_n = O(√log n).
*Proof.* x(k + κ) = s_T − ϱ = Σ_{R_T}ξ + s_{S₀} − ϱ, so Σ_{R_T}(ξ − x) = x(k + κ) − mx − s_{S₀} + ϱ. ∎

## L3.3 Lemma STATIC
**Lemma L3.** For every ε ∈ (0, c_D/2) there is n₀ such that for n ≥ n₀, on E1–E4, for every T ∈ 𝒯:
(a) every truth deletion and every truth-out swap has negative gain (truth additions do not exist);
(b) if T = S₀: every feasible neighbour has strictly smaller F (S₀ is a strict local maximum);
(c) if 1 ≤ m ≤ m_e: the deletion of a null at distance d_T from x has gain ≥ (c_D − ε)log n;
(d) if m > m_e: the deletion of a null at distance d_T from x has gain ≥ (½ − ε)log n.
Moreover (e) for every T ∈ Ω with S₀ ⊄ T and |T| = K, some swap has gain ≥ c₃n, using E1–E2 only [R04-1]: as in L2.2(ii),
for a missing truth l and any null j ∈ T, |t_l − t_j| ≥ c₄n/2 and, with |s_T| ≤ KH̄ (E1),
|t_j| ≤ κ_cκ/(K + κ) + κ₁(H̄ + KH̄/(K + κ)) + γ_Kλ₁Σ|ϑ| = O(√n H̄) uniformly over T; so V ≥ c₄²n²/8 and, with α ≤ n²,
ψ_T ≤ n, G_sw(j, l) ≥ (n/2)min(c₄²/8, ½) =: c₃n. (N1) is not needed.

*Proof.* Throughout, G_del(j) ≥ Δ_k − (1 + γ_{k−1})M_Tτ_j² (L0.6, log(1 + v) ≤ v), and
Δ_k ≥ ½log n + log((2p − k)/k) − 4/((n − 1)(1 − ρ)) ≥ ½log n + log(p/k) − o(1) (k ≤ p).
(a) As FACB L4.0(e), whose proof uses only S₀ ⊆ T, (X), (E1) and M_T ≥ ¼: truths have |τ_j| ≥ λ_θ|ϑ|_min/2 with
λ_θ = √((n − 1)(1 − ρ))/σ, nulls |τ| ≤ 2H̄ + CL_n ≤ λ_θ|ϑ|_min/8; then G_del(truth) ≤ Δ_k − ν log(1 + c_θ) < 0 and
V_{jl} < 0 for every truth-out swap (j truth, l null), so G_sw < 0.
(b) At T = S₀: no null deletions or null-out swaps exist; truth moves are negative by (a); additions:
|x_{S₀}| ≤ CL_n, |τ_l| ≤ H̄ + CL_n, and by L0.6 with u_l := (1 − γ_{s₀+1})M_Tτ_l²/ν = O(log n/n),
G_add(l) ≤ −Δ_{s₀+1} + (1 + 2u_l)M_Tτ_l² ≤ −½log n − ½h + L_n + log 2 + log(s₀ + 1) + o(1) + ½(1 + C/log n)(H̄ + CL_n)²
≤ −½log n + O(L_nH̄) < 0 [R04-2],
using Δ_{s₀+1} ≥ ½log n + log p − log(s₀ + 1) − o(1) and log p = ½h − L_n − log 2.
*Zero or small nearest distance first [R04-3].* If d_T ≤ 1 (including d_T = 0, not excluded by E1–E4), then
G_del ≥ Δ_k − 2M_T ≥ ½log n − 2C_M − o(1) by (M1), which exceeds both bounds (c), (d); so in (c) and (d) below d_T > 1.
(c) Here k ≤ s₀ + m_e, Σ_Tξ² + kL_n² ≤ (s₀ + m_e)(h + L_n²) ≤ n/log n, so M_T ≤ ½(1 + C/log n) (M2). Also
log(p/k) ≥ ½h − L_n − log 2 − log(s₀ + m_e). *Case both sides:* R_T has nulls above and below x. Then
d_T ≤ min(H̄ − x, H̄ + x) ≤ H̄, and k ≥ s₀ + 2, so γ_{k−1} ≤ 1/(s₀ + 1 + κ_∞) and
G_del ≥ ½log n + ½h − O(log log n) − ½(1 + C/log n)(1 + 1/(s₀ + 1 + κ_∞))h ≥ ½log n − h/(2(s₀ + 1 + κ_∞)) − O(log log n)
≥ c_D log n − O(log log n) (h ≤ 2log n + O(L_n), p ≤ n). *Case one side:* all retained nulls above x (the case "below" is
symmetric, with ξ ↦ −ξ, ϱ ↦ −ϱ in the bounds). By L3.2, m d_T ≤ Σ_{R_T}τ_j = E_T, and by (X)
x ≤ (mH̄ + CL_n)/(m + s₀ + κ), so E_T ≤ (s₀ + κ)(mH̄ + CL_n)/(m + s₀ + κ) + CL_n and
d_T ≤ (s₀ + κ)H̄/(m + s₀ + κ) + CL_n. Hence, for m ≥ 1,
(1 + γ_{k−1})d_T² ≤ (s₀ + κ)²h/((m + s₀ − 1 + κ)(m + s₀ + κ)) + O(L_nH̄) ≤ (s₀ + κ)h/(s₀ + κ + 1) + O(L_nH̄),
and, with t := s₀ + κ, G_del ≥ ½log n + ½h − ½(1 + C/log n)[t/(t + 1)]h − O(L_nH̄ + log log n) ≥ ½log n − O(log log n + L_nH̄)
[R04-2]
(note L_nH̄ = O(log log n·√log n) = o(log n)).
(d) Let d := d_T, a := |x| + d. *Step 1 (counting).* Suppose x ≥ 0 (x < 0 is the mirror image with U₋). Split R_T into
R₊ = {ξ_j > x} (so ξ_j ≥ x + d) and R₋ = {ξ_j < x} (ξ_j ≤ x − d). By L3.2,
Σ_{R₋}(x − ξ_j) = Σ_{R₊}(ξ_j − x) − E_T ≤ S₊ + e_n, S₊ := Σ_{null j: ξ_j ≥ x+d}(ξ_j − x) = dU₊(x + d) + ∫_{x+d}^{∞}U₊(t)dt;
each term on the left is ≥ d, so |R₋| ≤ (S₊ + e_n)/d, and |R₊| ≤ U₊(x + d). Hence
  m ≤ 2U₊(a) + d⁻¹∫_a^{H̄}U₊(t)dt + e_n/d   (U₊ = 0 above H̄ by E1).
*Step 2 (d ≤ 1).* Already treated above (zero/small nearest distance).
*Step 3 (d > 1).* Then a ≥ d > 1, and by (E3) and ∫_a^∞Φ̄(t)dt ≤ φ(a) ≤ Φ̄(a)(1 + a²)/a (Mills),
m ≤ pΦ̄(a)(4 + 2(1 + a²)/a) + 10 log n + 5H̄ log n + e_n ≤ pΦ̄(a)(6 + 2a) + 6H̄ log n. Since m > m_e = ⌈log² n⌉ ≫ 12H̄ log n,
m ≤ 2pΦ̄(a)(6 + 2a), so (Φ̄(a) ≤ e^{−a²/2}) a²/2 ≤ log(p/m) + log(12 + 4a), i.e. **log(p/m) ≥ a²/2 − O(log log n)**
(a ≤ |x| + d ≤ 3H̄ + CL_n).
 (d-i) If m ≤ n^{1 − c₀} with c₀ := ε/(8C_M): Σ_Tξ² + kL_n² ≤ (n^{1−c₀} + s₀)(h + L_n²) ≤ n/log n, so M_T ≤ ½(1 + C/log n),
 and log(p/k) ≥ log(p/m) − log(1 + s₀/m) ≥ a²/2 − O(log log n). With a² ≥ d², d² ≤ 9h and γ_{k−1} ≤ 1/(m_e − 1):
 G_del ≥ ½log n + a²/2 − ½(1 + C/log n)(1 + γ_{k−1})d² − O(log log n) ≥ ½log n − O(1) − O(log log n).
 (d-ii) If m > n^{1−c₀}: log(p/m) ≤ c₀log n (p ≤ n), so d² ≤ a² ≤ 2c₀log n + O(log log n), and by (M1)
 (1 + γ_{k−1})M_Td² ≤ 2C_M(2c₀log n + O(log log n)) ≤ (ε/2)log n + o(log n); log((2p − k)/k) ≥ 0 (k ≤ K < p), so
 G_del ≥ ½log n − ε log n for n ≥ n₀. ∎

## L3.4 Lemma BUDGET and the path theorem
**Lemma L3.4.** On the events of L1(a) and L3, for n ≥ n₀(ε): let C_0 := S̃₀ (|S̃₀| = K) and C_0, C_1, …, C_{m*} the uncapped
§6.10 path. Then (i) C_{m*} = S₀; (ii) m* ≤ (1 + 6ε)K + (2/(c_D − ε))(m_e + 1) + A_n, where A_n := #{i : S₀ ⊄ C_i}
≤ (K log n + Cn)/(c₃n) = O(log n) (A_n = 0 if S₀ ⊆ S̃₀).

*Proof.* (Order of the argument: the endpoint (i) first, without any bound on move counts; then the budgets [R06-2].)
*Phase A structure.* While S₀ ⊄ C_i, |C_i| = K and the best move gains ≥ c₃n (L3(e)); since every deletion gains ≤ Δ_K
(L2.2(i), whose proof uses neither (PK) nor (PB) [R09-E1]) and additions are infeasible at size K, the move is a swap, so sizes stay K. *Stays in 𝒯.* Once S₀ ⊆ C_i,
every later centre contains S₀: the chosen move has positive gain, truth-out moves are negative (L3(a)) and truth
additions do not exist. *(i)* Ω is finite and F strictly increases, so the path ends at a centre with no improving
neighbour; by L3(c), (d) no T ∈ 𝒯 ∖ {S₀} is such a centre and by L3(e) no size-K set without S₀ is; sets of size < K
without S₀ are never visited (phase A is at size K). So C_{m*} = S₀, which is a strict local maximum by L3(b); in
particular F(C_i) ≤ F(S₀) for every i. *Phase A count.* The F-increase over phase A is therefore ≤ F(S₀) − F(C_0) ≤
Σ_{k=s₀+1}^{K}Δ_k + ν log(ψ_{C_0}/ψ_{S₀}) ≤ K log n + Cn (ψ_{C_0} ≤ n, ψ_{S₀} ≥ RSS_{S₀}/s² ≥ cn by E2), and each phase-A
move gains ≥ c₃n, giving A_n ≤ (K log n + Cn)/(c₃n) = O(log n).
*(ii)* Let i₁ be the first index with C_{i₁} ∈ 𝒯 and i₂ ≥ i₁ the first index with C_{i₂} ∈ 𝒯 and m(C_{i₂}) ≤ m_e.
Moves i₁ ≤ i < i₂ start at sets with m > m_e and gain ≥ (½ − ε)log n each (L3(d); the chosen move gains at least
the best deletion). Their total gain is ≤ F(C_{i₂}) − F(C_{i₁}) ≤ F(S₀) − F(C_{i₁}) (F increases along the path, which
ends at S₀), and for T ∈ 𝒯
  F(S₀) − F(T) = Σ_{k=s₀+1}^{|T|}Δ_k + ν log(ψ_T/ψ_{S₀}) ≤ Σ_{k=s₀+1}^{|T|}Δ_k   (S₀ ⊆ T ⇒ quad_{S₀} ≤ quad_T ⇒ ψ_{S₀} ≥ ψ_T).
With Σ_{k=1}^{K}log((2p − k)/k) = log C(2p − 1, K) ≤ K(1 + log((2p − 1)/K)) ≤ 2.39K (p ≤ 2K + 1) and ½(L_k − L_{k−1}) ≤
½log(n + 1) + o(1): F(S₀) − F(C_{i₁}) ≤ K(½log n + 2.4). So i₂ − i₁ ≤ K(½log n + 2.4)/((½ − ε)log n) ≤ (1 + 6ε)K for n ≥ n₀.
From i₂ on, the centres need not keep m ≤ m_e (additions are not excluded), but every centre lies in 𝒯 ∖ {S₀} until
the end, so every move gains ≥ (c_D − ε)log n (L3(c), (d); ε < c_D/2), and the total remaining gain is ≤ F(S₀) − F(C_{i₂}) ≤ Σ_{k=s₀+1}^{s₀+m_e}Δ_k ≤ m_e(log(2p) + ½log(n + 1) + 1)
≤ 2(m_e + 1)log n, so at most 2(m_e + 1)/(c_D − ε) moves follow. ∎

**Theorem PATH (claim (P3)).** Under G, (CS), (θ) (θ̄ ≠ 0, ϑ_r ≠ 0), blocks of size ≤ 16, (PK′) and the LS0 premises,
for every fixed δ > 0: P(the uncapped LS0 path from S̃₀ ends at S₀, S₀ is a strict local maximum, and m* ≤ (1 + δ)|S̃₀|) → 1.
Consequently, for every cap a = a(data) ≥ (1 + δ)|S̃₀| (in particular ℓ_n + 2|S̃₀|), P(LS0(a) ends at S₀ as a
certified search endpoint) → 1. *Proof.* L1(a) (|S̃₀| = K; uses only (PK′) and blocks ≤ 16), L3, L3.4 with ε = min(δ/12, c_D/4), and the prefix property (FINAL s7, (L3)). ∎

## L3.5 Remarks
0. **Reading l3_trend [R09-opt3].** The worst large-m ratio (gain/log n ≈ 0.3 at n ≤ 1.3·10⁵, p = n − 1, ρ = 0.8) reflects
   an O(1) deficit (M_Td² ≈ 3 at m ≈ K) divided by log n; it rises with n and is not a counterexample to (d).
1. **Static, not path-restricted.** Unlike FACB L4, no invariant along the path is needed: every set above S₀ has an
   improving deletion with an explicit gain, and the F-budget converts gains into a move count. The price is the
   weaker count (1 + δ)K instead of an exact move count; the exact structure (swap phase, then pure deletion) is
   observed (N1, N3) but not claimed.
2. **Consistency with NEG.** NEG (under (PK), (PB)) gives m* ≥ K − s₀ + n^β; so K − s₀ + n^{1/2−o(1)} ≤ m* ≤ (1 + o(1))K.
3. The constants c_M, C_M are astronomically small/large (union bound over 2^n sets); asymptotic scope.
4. FACB's regime p ≤ n/2 satisfies the hypotheses of L3 except the size of the start (K = p, start S*): the same static
   argument applies to it (not claimed here; a possible independent cross-check of FAC-CS).
