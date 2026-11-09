# L3 — Centre sandwich: S₀ ⊆ S̃ ⊆ Q for every start-mode maximiser (claim (C3))

Status: **PROVED (by this seat, unchecked)**; key-lemma check R02 (Codex Sol xhigh): **VERIFIED** (no amendments;
reviews/R02_L3_check_sol.md). Remark (from R02 item 9): in the branch Q = [p] (then p = O(log n)) the start mode can
have size close to K = p; the sandwich still holds.
Hypotheses: G; ‖μ‖² ≤ Mn; p ≤ n^A; blocks C_b with |C_b| ≤ B ≤ 16 (the method's actual partition, deterministic under
G); (G1) Q = S₀ ∪ 𝒫_n with |Q| ≤ C_Q log n, and **either** Q = [p] **or** K ≥ 2|Q| + 32s₀ + 1 for n ≥ n₀;
(G3a) within-block SE; (G3b) TV with M_n → ∞; (G3c) NEG(η) with η < η_A := (√(2A + 1) − √(2A))².
Objects: γ₀(S) = w(|S|)∏_b r_b(S ∩ C_b) on Ω = {|S| ≤ K}, r_b(U) = m(U)/m(∅); S̃ denotes **any** maximiser of γ₀
on Ω; k̃ := |S̃|; Ũ_b := S̃ ∩ C_b. For U ⊆ C_b, l ∈ C_b ∖ U: δ_{U,l} = u_{U,l}ᵀμ, Z_{U,l} = u_{U,l}ᵀε/σ, and
RSS_U − RSS_{U∪{l}} = (δ_{U,l} + σZ_{U,l})² (u_{U,l} ⊥ 1). Notation L0.

**Lemma L3.** P(S₀ ⊆ S̃ ⊆ Q for every maximiser S̃ of γ₀ on Ω) → 1.

## L3.0 Events

* 𝓔^blk: the events 𝒟₁ ∩ 𝒟₂ ∩ 𝒟₃ of [GEN-L1] for 𝔉_blk := {U : U ⊆ C_b for some b} (|U| ≤ 16, |𝔉_blk| ≤ 2^{16}p,
  Gram floor by (G3a)), 𝒱𝒱 := {r_U, r_U − r_{U′} : U, U′ ∈ 𝔉_blk}; P → 1 ([GEN-L1] L1.1). On it, for n ≥ n₀:
  L0.2(a)–(c) and [GEN-L1] L1.4(b) hold on 𝔉_blk.
* 𝓩 := {Z²_{U,l} ≤ z²_n for all b, U ⊆ C_b, l ∈ C_b ∖ U}, z²_n := 2 log(2^{21}p) + 2 log log n. At most 2^{20}p
  (≥ 16·2^{16}p) standard normals: P(𝓩ᶜ) ≤ 2^{20}p·2 exp(−log(2^{21}p) − log log n) = 1/log n.
* For each block b: W_b := max{‖(P_V − P_{V∖N})ε‖²/(σ²|N|) : ∅ ≠ N ⊆ V ⊆ C_b}; count C(τ) := #{b : W_b ≥ τ}.

**Tail of W_b.** For fixed (V, N), P_V − P_{V∖N} has rank d = |N| (G3a), so ‖·‖²/σ² ~ χ²_d. Chernoff:
P(χ²_d ≥ dτ) ≤ (τe^{1−τ})^{d/2} ≤ (τe^{1−τ})^{1/2} = √(eτ)e^{−τ/2} for τ > 1 (τe^{1−τ} < 1). There are ≤ 3^{16} pairs
(V, N) per block, hence P(W_b ≥ τ) ≤ 3^{16}√(eτ)e^{−τ/2} and E C(τ) ≤ p·3^{16}√(eτ)e^{−τ/2} (at most p blocks).

## L3.1 Per-block optimality

Since only the factor of block b and the prior change, for every U ⊆ C_b with k̃ − |Ũ_b| + |U| ≤ K:

  log r_b(U) + log w(k̃ − |Ũ_b| + |U|) ≤ log r_b(Ũ_b) + log w(k̃).                                         (3.1)

## L3.2 Step 1: the start mode is small

Call b **good** if S₀ ∩ C_b ⊆ Ũ_b; at most s₀ blocks are not good. For good b put N_b := Ũ_b ∖ Q (junk). Then

  k̃ ≤ |Q| + s₀B + Σ_{b good} |N_b| ≤ k₀ + B·#{b good : N_b ≠ ∅},  k₀ := |Q| + 16s₀.                       (3.2)

*Junk forces a large W_b.* Let b be good with N_b ≠ ∅ and U := Ũ_b ∖ N_b ⊇ S₀ ∩ C_b. (3.1) with this U (smaller,
hence feasible) and w(k − 1)/w(k) = (2p − k)/k ≥ p/k for k ≤ p (k̃ ≤ K ≤ p) give
log r_b(Ũ_b) − log r_b(U) ≥ log w(k̃ − |N_b|) − log w(k̃) ≥ |N_b| log(p/k̃).
On 𝓔^blk, by L0.2(c) and the second display of L0.2(b),
log r_b(Ũ_b) − log r_b(U) ≤ −½|N_b| log(n + 1) + (1 + ϑ_n)(RSS_U − RSS_{Ũ_b})/(2σ²) + 2κ_E.
With Π := P_{Ũ_b} − P_U (ΠC = Π): RSS_U − RSS_{Ũ_b} = ‖Πμ + Πε‖² ≤ (1 + ε₁)‖Πε‖² + (1 + 1/ε₁)‖Πμ‖² for any ε₁ > 0,
and, adding the elements l₁, …, l_d of N_b to U one at a time (U_s := U ∪ {l₁, …, l_s}),
‖Πμ‖² = Σ_s δ²_{U_{s−1},l_s} ≤ |N_b|ησ² log n by NEG (each U_{s−1} ⊇ S₀ ∩ C_b, l_s ∉ Q). Since
‖Πε‖²/σ² ≤ |N_b|W_b and |N_b| ≥ 1, combining:

  W_b ≥ τ_n(k̃),  τ_n(k) := [log(n + 1) + 2 log(p/k) − (1 + ϑ_n)(1 + 1/ε₁)η log n − 4κ_E] / ((1 + ϑ_n)(1 + ε₁)).   (3.3)

So #{b good : N_b ≠ ∅} ≤ C(τ_n(k̃)), and τ_n(k) is decreasing in k.

*Choice of ε₁.* Since η < η_A, there is ε₁ > 0 with Aε₁ + (1 + 1/ε₁)η/2 < ½ (the minimum over ε₁ > 0 of the left
side is √(2Aη) + η/2, and √(2Aη) + η/2 < ½ ⇔ √η < √(2A + 1) − √(2A); for η = 0 take ε₁ < 1/(2A)). Fix it, and
n₀ so large that, with 1 + ε₂ := (1 + ϑ_n)(1 + ε₁) and η₁ := (1 + ϑ_n)(1 + 1/ε₁)η, ξ := (1 − η₁)/2 − Aε₂ ≥ ξ₀ > 0
for n ≥ n₀ (possible as ϑ_n → 0). Then τ_n(k) ≥ [(1 − η₁) log n + 2 log(p/k) − 4κ_E]/(1 + ε₂) ≥ 3 for k ≤ p, n ≥ n₀, and

  E C(τ_n(k)) ≤ p 3^{16}√(e(2A + 2) log n) e^{2κ_E} n^{−(1−η₁)/(2(1+ε₂))}(k/p)^{1/(1+ε₂)}
             = C₁√(log n) n^{−(1−η₁)/(2(1+ε₂))} p^{ε₂/(1+ε₂)} k^{1/(1+ε₂)}                                        (3.4)

(τ_n(k) ≤ log(n + 1) + 2 log p ≤ (2A + 2) log n; C₁ := 3^{16}e^{2κ_E}√(e(2A + 2))).

*Ladder.* Put m_i := 2^{i+1}k₀ (i ≥ 0). If k̃ > 2k₀, take i with m_i < k̃ ≤ m_{i+1}; by (3.2)–(3.3),
B·C(τ_n(k̃)) ≥ k̃ − k₀ > k̃/2 > m_i/2, and C(τ_n(min(m_{i+1}, K))) ≥ C(τ_n(k̃)) (k̃ ≤ min(m_{i+1}, K), τ_n decreasing, C
non-increasing). Markov and (3.4):
P(k̃ > 2k₀, 𝓔^blk) ≤ Σ_{i≥0} (2B/m_i) E C(τ_n(min(m_{i+1}, K)))
  ≤ Σ_{i≥0} 2B C₁√(log n) n^{−(1−η₁)/(2(1+ε₂))} p^{ε₂/(1+ε₂)} (2m_i)^{1/(1+ε₂)}/m_i
  ≤ 4B C₁√(log n) n^{−(1−η₁)/(2(1+ε₂))} p^{ε₂/(1+ε₂)} Σ_{i≥0} 2^{−iε₂/(1+ε₂)}
  ≤ C₂ √(log n) n^{−ξ/(1+ε₂)} → 0      (p ≤ n^A; k₀ ≥ 1; the geometric sum is ≤ 1/(1 − 2^{−ε₂/(1+ε₂)})).
(The event "for every maximiser" is covered: the bound (3.2)–(3.3) holds for each maximiser, and the event
{C(τ_n(min(m_{i+1}, K))) > m_i/(2B)} does not depend on the maximiser.) Hence P(k̃ ≤ 2k₀ for every maximiser) → 1.

## L3.3 Step 2: truths in, junk out

Work on 𝒢_n := 𝓔^blk ∩ 𝓩 ∩ {k̃ ≤ 2k₀ for every maximiser}, n ≥ n₀ (P(𝒢_n) → 1).

*(a) Every truth is in S̃.* If Q = [p] and k̃ = K, then K = p (|Q| ≤ K) and S̃ = [p] ⊇ S₀. Otherwise k̃ < K (in the
second case of (G1), k̃ ≤ 2k₀ = 2|Q| + 32s₀ < K). Suppose j ∈ S₀ ∖ S̃, j ∈ C_b. S̃ ∪ {j} ∈ Ω and
log γ₀(S̃ ∪ {j}) − log γ₀(S̃) = log[(k̃ + 1)/(2p − 1 − k̃)] + log r_b(Ũ_b ∪ {j}) − log r_b(Ũ_b)
  ≥ −log(2p) − ½ log(n + 1) − 2κ_E + (RSS_{Ũ_b} − RSS_{Ũ_b∪{j}})/(2C_R)
(L0.2(c); [GEN-L1] L1.4(b), nested sets). By TV and 𝓩, RSS_{Ũ_b} − RSS_{Ũ_b∪{j}} = (δ + σZ)² ≥ δ²/2 − σ²Z²
≥ ½M_n log n − σ²z²_n. Since M_n → ∞ and z²_n ≤ 2(A + 1) log n for n ≥ n₀, the right side is positive for n ≥ n₀,
contradicting maximality. So S₀ ⊆ S̃ and every block is good.

*(b) No junk.* If Q = [p] there is nothing to prove. Otherwise let l ∈ Ũ_b ∖ Q. S̃ ∖ {l} ∈ Ω and, by L0.2(b),(c),
log γ₀(S̃ ∖ {l}) − log γ₀(S̃) = log[(2p − k̃)/k̃] + ½ log(n + 1) − ν log(RSS_{Ũ_b∖{l}}/RSS_{Ũ_b}) + (R − R′)
  ≥ log p − log k̃ + ½ log(n + 1) − 2κ_E − (1 + ϑ_n)(δ_{Ũ_b∖{l},l} + σZ)²/(2σ²).
By NEG (Ũ_b ∖ {l} ⊇ S₀ ∩ C_b) and 𝓩: (δ + σZ)²/σ² ≤ (√(η log n) + z_n)² ≤ η log n + z²_n + 2z_n√(η log n). Write
L := log p ≤ A log n and z²_n ≤ 2L + c₃ log log n (c₃ fixed, n ≥ n₀). Then the right side is at least
  ½ log n − ½η log n − √(2ηL log n) − ϑ_n(L + log n) − O(√(log n log log n)) − log k̃ − 2κ_E
  ≥ [½ − η/2 − √(2Aη)] log n − o(log n) > 0   for n ≥ n₀,
because ½ − η/2 − √(2Aη) > 0 ⇔ η < η_A and log k̃ = O(log log n). Contradiction; so S̃ ⊆ Q. ∎

**Remarks.** (1) Step 1 is what excludes a huge start mode (e.g. |S̃| ≈ K made of noise-fitting nulls): a junk
element costs ½ log n + log(p/k̃) − (NEG + noise) and noise can pay for many junk elements only in few blocks
(Markov count over blocks; no independence between blocks is used). (2) The same constant η_A as in GEN's NL_η
appears in both steps. (3) Masked truths are excluded by TV (they would sit outside S̃); GEN handles them for a
bounded relevance set.
