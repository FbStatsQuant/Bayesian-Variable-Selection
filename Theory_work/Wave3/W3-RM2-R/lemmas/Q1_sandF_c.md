# Q1 — Lemma SAND-F-c: the fixed-design sandwich under constant-level visibility (V_b♭) (bridge (Q1); claim W3-RM2-R:SAND-F-c)

Status: **PROVED (by this seat, unchecked)** — 2026-11-16, lead Claude Opus 5.5. Ticket W3-RM2-R; statement:
`../STATEMENT.md` v1.0 §2 ((V♭), (V_b♭)), §4 bridge (Q1).
**This file is a copy** of PARENT `Theory_work/Wave3/W3-RM2/lemmas/L1_sandF_b.md` (claim W3-RM2:SAND-F-b@1.0.0,
"PROVED-CHECKED; council R1, …"; sha256 prefix 4a29eea6b2f2ac38 in `../DEPS.tsv`). **Changed lines are marked [R-#]**;
every unmarked line is the parent's text (with the parent's file references rewritten as PARENT paths, marked [R-0]).
The only mathematical change is Step 2(a) [R-3]: the visibility constant M_n → ∞ is replaced by a fixed M_V > M_V⁰.
PARENT := `Theory_work/Wave3/W3-RM2/`. The only input is PARENT `lemmas/L0_toolkit_b.md` (Lemma Toolkit-b,
W3-RM2:Toolkit-b@1.0.0) for the block family, as in the parent.

## 0. Setting, hypotheses, statement

Setting F and notation of PARENT `lemmas/L0_toolkit_b.md` [R-0] §0. For U ⊆ [p] and l ∉ U with (I − P_U)x_l ≠ 0:
u_{U,l} := (I − P_U)x_l/‖(I − P_U)x_l‖, δ_{U,l} := u_{U,l}ᵀμ, Z_{U,l} := u_{U,l}ᵀε/σ ~ N(0, 1); then
RSS_U − RSS_{U∪{l}} = (u_{U,l}ᵀY)² = (δ_{U,l} + σZ_{U,l})² (u_{U,l} ⊥ 1, so u_{U,l}ᵀCε = u_{U,l}ᵀε) and
Λ_U − Λ_{U∪{l}} = δ²_{U,l}. τ²_U := σ² + Λ_U/(n − 1); U ⊆ U′ ⇒ τ²_{U′} ≤ τ²_U; τ²_U ≥ σ².

Hypotheses (fixed constants A ≥ 1, M > 0, φ₀ ∈ (0, 1], s₀ ≥ 1, η ≥ 0, b > 0 [SW1-1: the range (0, 1] is that of φ₀
only]):
(S0) ‖μ‖² ≤ Mn; p ≤ n^A; S₀ = supp θ*, |S₀| = s₀.
(S1) C₁, …, C_J is a partition of [p] with |C_b| ≤ 16 that is a deterministic function of X; b(j) is the block of j.
(G3a) λ_min(R̂_T) ≥ φ₀² for every nonempty T contained in a block.
(V_b♭) [R-1] δ²_{U,j} ≥ M_V log n for every j ∈ S₀ and U ⊆ C_{b(j)} ∖ {j} and n ≥ n₀, with a fixed
     M_V > M_V⁰ := (σ√(2A) + √((2A + 1)C_R))², C_R := 3(M + σ²) (the constant of PARENT `lemmas/L0_toolkit_b.md:38`).
(L_b) for every l ∉ Q and every U with S₀ ∩ C_{b(l)} ⊆ U ⊆ C_{b(l)} ∖ {l}: δ²_{U,l} ≤ ητ²_U log n.
(Q) Q = Q_n ⊇ S₀ deterministic, |Q| ≤ n^b, |Q| ≤ K, and Q = [p] or K ≥ 2|Q| + 32s₀ + 1 for n ≥ n₀ ((L-feas)).
(B) **b < β(η, A) := ½ − η/2 − √(2Aη)** (this forces η < η_A = (√(2A + 1) − √(2A))² and b < ½).
Objects: Ω := {S ⊆ [p] : |S| ≤ K}, K = min(p, ⌊n/2⌋); r_b(U) := m(U)/m(∅) for U ⊆ C_b;
γ₀(S) := w(|S|)∏_b r_b(S ∩ C_b) on Ω. S̃ denotes **any** maximiser of γ₀ on Ω; k̃ := |S̃|; Ũ_b := S̃ ∩ C_b.

**Lemma SAND-F-c** [R-2]. Under (S0), (S1), (G3a), (V_b♭), (L_b), (Q), (B):
P(S₀ ⊆ S̃ ⊆ Q for every maximiser S̃ of γ₀ on Ω) → 1.

**Lemma B1 (partition-free ⇒ block-relative; elementary).** For any partition with blocks of size ≤ 16:
(FL-16) ⇒ (G3a); (V♭) ⇒ (V_b♭) with the same M_V [R-2]; (L-gain) ⇒ (L_b) with the same η and Q.
*Proof.* A nonempty T inside a block has 1 ≤ |T| ≤ 16. For j ∈ S₀ and U ⊆ C_{b(j)} ∖ {j}: U ⊆ [p] ∖ {j}, |U| ≤ 15
(and u_{U,j} exists by (FL-16) on U ∪ {j}). For l ∉ Q and S₀ ∩ C_{b(l)} ⊆ U ⊆ C_{b(l)} ∖ {l}: U ⊆ [p] ∖ {l}, |U| ≤ 15;
the extra requirement on U only restricts the sets quantified over. ∎
So the [SAND(Q)] part of (C1⁺) follows from the lemma [R-2]: under (T1-F♭) (which contains ‖μ‖² ≤ Mn, p ≤ n^A), (FL-16),
(V♭), (L^b) with b < β(η, A), for the method's partition (a deterministic function of the fixed X).

## 1. Events and two preliminary facts

* 𝓔^blk: the toolkit event of the block family (𝔉_blk, 𝒱𝒱_blk) of PARENT `lemmas/L0_toolkit_b.md` [R-0] §4(i); P(𝓔^blkᶜ) → 0 by (T1), and
  t_n, h_n² = O(log n) there.
* 𝓩 := {Z²_{U,l} ≤ z²_n for all b, U ⊆ C_b, l ∈ C_b ∖ U}, z²_n := 2 log(2^{21}p) + 2 log log n. There are at most
  16·2^{16}p ≤ 2^{20}p such pairs, each Z_{U,l} is standard normal ((G3a) makes u_{U,l} well defined), and
  P(𝓩ᶜ) ≤ 2^{20}p·2 exp(−z²_n/2) = 1/log n.
* For each block b: W_b := max{‖(P_V − P_{V∖N})ε‖²/(σ²|N|) : ∅ ≠ N ⊆ V ⊆ C_b}; C(τ) := #{b : W_b ≥ τ}.

**Fact 1 (tail of W_b).** For τ > 1: P(W_b ≥ τ) ≤ 3^{16}√(eτ)e^{−τ/2}, hence E C(τ) ≤ p·3^{16}√(eτ)e^{−τ/2}.
*Proof.* For fixed (V, N), P_V − P_{V∖N} is a projector of rank d = |N| ((G3a)), so ‖(P_V − P_{V∖N})ε‖²/σ² ~ χ²_d and,
by the Chernoff bound, P(χ²_d ≥ dτ) ≤ (τe^{1−τ})^{d/2} ≤ (τe^{1−τ})^{1/2} (τe^{1−τ} < 1 for τ > 1). There are at most
3^{16} pairs (V, N) in a block (each element is in N, in V ∖ N, or outside V) and at most p blocks. ∎

**Fact 2 (RSS floor in τ-form).** On 𝓔^blk, for n ≥ n₀ and every U ∈ 𝔉_blk:
RSS_U ≥ (n − 1)τ²_U(1 − ω^τ_n), ω^τ_n := h_n/√(n − 1) + (4n^{2/3} + t_n)/(n − 1); and for nested U ⊆ U′ in 𝔉_blk:
ν log(RSS_U/RSS_{U′}) ≤ (1 + ϑ^τ_n)(RSS_U − RSS_{U′})/(2τ²_{U′}), 1 + ϑ^τ_n := (n + 0.02)/((n − 1)(1 − ω^τ_n)).
Here ω^τ_n log n → 0 and ϑ^τ_n log n → 0 (h_n², t_n = O(log n)).
*Proof.* By (0.1) of L0 and the events, RSS_U ≥ Λ_U − 2σh_n√Λ_U + σ²(n − 1) − 4σ²n^{2/3} − σ²t_n. By AM–GM,
2σ√(n − 1)√Λ_U ≤ σ²(n − 1) + Λ_U = (n − 1)τ²_U, so 2σh_n√Λ_U ≤ (h_n/√(n − 1))·(n − 1)τ²_U; also
σ²(n − 1) + Λ_U = (n − 1)τ²_U and σ² ≤ τ²_U. This gives the first display. The second: log u ≤ u − 1 with
u = RSS_U/RSS_{U′}, ν = n/2 + 0.01, and the first display for U′. ∎

**Per-block optimality.** Changing only the block-b part of a maximiser S̃ to U ⊆ C_b gives a set of size
k̃ − |Ũ_b| + |U|; if this is ≤ K, maximality gives

  log r_b(U) + log w(k̃ − |Ũ_b| + |U|) ≤ log r_b(Ũ_b) + log w(k̃).                                         (1.1)

## 2. Step 1: every start-mode maximiser has size ≤ 2k₀, k₀ := |Q| + 16s₀

Call b **good** if S₀ ∩ C_b ⊆ Ũ_b; at most s₀ blocks are not good (each contains a truth outside S̃). For good b put
N_b := Ũ_b ∖ Q. Since S̃ = (S̃ ∩ Q) ∪ ⋃_b(Ũ_b ∖ Q) and a block that is not good contributes at most 16,

  k̃ ≤ |Q| + 16s₀ + Σ_{b good}|N_b| ≤ k₀ + 16·#{b good : N_b ≠ ∅}.                                        (2.1)

*Junk forces a large W_b.* Let b be good with N_b ≠ ∅, d := |N_b| ≤ 16, U := Ũ_b ∖ N_b. Then U ⊇ S₀ ∩ C_b (S₀ ⊆ Q, so
no truth is in N_b). (1.1) with this U (a smaller set, hence feasible) and w(k − 1)/w(k) = (2p − k)/k ≥ p/k̃ for
k ≤ k̃ ≤ p give
  log r_b(Ũ_b) − log r_b(U) ≥ log w(k̃ − d) − log w(k̃) ≥ d log(p/k̃).
On 𝓔^blk, by (E6-tab) and Fact 2 (U ⊆ Ũ_b),
  log r_b(Ũ_b) − log r_b(U) ≤ −½d log(n + 1) + (1 + ϑ^τ_n)(RSS_U − RSS_{Ũ_b})/(2τ²_{Ũ_b}) + 2κ_E.
With Π := P_{Ũ_b} − P_U (a projector, ΠC = Π): RSS_U − RSS_{Ũ_b} = ‖Πμ + Πε‖² ≤ (1 + ε₁)‖Πε‖² + (1 + 1/ε₁)‖Πμ‖² for any
ε₁ > 0. Adding the elements l₁, …, l_d of N_b to U one at a time (U_s := U ∪ {l₁, …, l_s}),
‖Πμ‖² = Λ_U − Λ_{Ũ_b} = Σ_s δ²_{U_{s−1},l_s} ≤ Σ_s ητ²_{U_{s−1}} log n ≤ dητ²_U log n by (L_b) (each U_{s−1} satisfies
S₀ ∩ C_b ⊆ U_{s−1} ⊆ C_b ∖ {l_s}, l_s ∉ Q, and τ²_{U_{s−1}} ≤ τ²_U). Moreover
τ²_{Ũ_b} = τ²_U − ‖Πμ‖²/(n − 1) ≥ τ²_U(1 − ζ_n), ζ_n := 16η log n/(n − 1) → 0, and ‖Πε‖² ≤ σ²dW_b ≤ τ²_U dW_b. Hence, with
1 + ϑ″_n := (1 + ϑ^τ_n)/(1 − ζ_n) (ϑ″_n log n → 0),
  d log(p/k̃) ≤ −½d log(n + 1) + (1 + ϑ″_n)(d/2)[(1 + ε₁)W_b + (1 + 1/ε₁)η log n] + 2κ_E,
and dividing by d/2 ≥ ½:

  W_b ≥ τ_n(k̃),  τ_n(k) := [log(n + 1) + 2 log(p/k) − (1 + ϑ″_n)(1 + 1/ε₁)η log n − 4κ_E]/((1 + ϑ″_n)(1 + ε₁)).   (2.2)

So #{b good : N_b ≠ ∅} ≤ C(τ_n(k̃)); τ_n(·) is decreasing and C(·) is non-increasing.

*Choice of ε₁.* By (B), √(2Aη) + η/2 < ½. [LC1A-2] For η > 0 the minimum over ε₁ > 0 of Aε₁ + (1 + 1/ε₁)η/2 is
√(2Aη) + η/2, attained at ε₁ = √(η/(2A)); for η = 0 the infimum is zero, and any 0 < ε₁ < 1/(2A) suffices. So fix
ε₁ > 0 with Aε₁ + (1 + 1/ε₁)η/2 < ½. Put 1 + ε₂ := (1 + ϑ″_n)(1 + ε₁) and
η₁ := (1 + ϑ″_n)(1 + 1/ε₁)η (both depend on n through ϑ″_n → 0). For n ≥ n₀: ξ := (1 − η₁)/2 − Aε₂ ≥ ξ₀ > 0, ε₂ ≤ 2ε₁ + 1,
and for 1 ≤ k ≤ p
  τ_n(k) ≥ τ̲_n(k) := [(1 − η₁) log n + 2 log(p/k) − 4κ_E]/(1 + ε₂) ≥ 3.
Since τ ↦ √(eτ)e^{−τ/2} is decreasing on [1, ∞) and τ̲_n(k) ≤ log(n + 1) + 2 log p ≤ (2A + 2) log n, Fact 1 gives

  E C(τ_n(k)) ≤ p·3^{16}√(e(2A + 2) log n)·exp(−τ̲_n(k)/2)
             ≤ C₁√(log n)·n^{−(1−η₁)/(2(1+ε₂))}·p^{ε₂/(1+ε₂)}·k^{1/(1+ε₂)},   C₁ := 3^{16}e^{2κ_E}√(e(2A + 2)).           (2.3)

*Ladder.* Put m_i := 2^{i+1}k₀ (i ≥ 0). If k̃ > 2k₀, take i ≥ 0 with m_i < k̃ ≤ m_{i+1}. By (2.1)–(2.2),
16·C(τ_n(k̃)) ≥ k̃ − k₀ > k̃/2 > m_i/2, and C(τ_n(min(m_{i+1}, K))) ≥ C(τ_n(k̃)) (k̃ ≤ min(m_{i+1}, K) ≤ p). The event
{C(τ_n(min(m_{i+1}, K))) > m_i/32} does not depend on the maximiser, so by Markov and (2.3) (min(m_{i+1}, K) ≤ 2m_i):
P(some maximiser has k̃ > 2k₀, 𝓔^blk) ≤ Σ_{i≥0} (32/m_i)·C₁√(log n)·n^{−(1−η₁)/(2(1+ε₂))}·p^{ε₂/(1+ε₂)}·(2m_i)^{1/(1+ε₂)}
  ≤ 64C₁√(log n)·n^{−(1−η₁)/(2(1+ε₂))}·p^{ε₂/(1+ε₂)}·Σ_{i≥0} m_i^{−ε₂/(1+ε₂)}
  ≤ C₂√(log n)·n^{−ξ/(1+ε₂)} → 0,
using p ≤ n^A, m_i ≥ 2^{i+1} (k₀ ≥ 1) and the geometric sum Σ_i 2^{−(i+1)ε₂/(1+ε₂)} ≤ 1/(1 − 2^{−ε₁/(1+ε₁)}) (ε₂ ≥ ε₁).
**The size of Q enters this step only through k₀ ≥ 1** — a larger k₀ makes the bound smaller.
Hence P(k̃ ≤ 2k₀ for every maximiser) → 1.

## 3. Step 2: truths in, junk out

Work on 𝒢_n := 𝓔^blk ∩ 𝓩 ∩ {k̃ ≤ 2k₀ for every maximiser}, n ≥ n₀; P(𝒢_n) → 1. Fix a maximiser S̃.

**(a) Every truth is in S̃.** If Q = [p] and k̃ = K, then K = p (|Q| = p ≤ K ≤ p) and S̃ = [p] ⊇ S₀. Otherwise k̃ < K:
either Q = [p] and k̃ < K, or K ≥ 2|Q| + 32s₀ + 1 > 2k₀ ≥ k̃. Suppose j ∈ S₀ ∖ S̃, j ∈ C_b. Then S̃ ∪ {j} ∈ Ω and, by
(E6-tab) and the prior ratio (k̃ ≤ p − 1),
log γ₀(S̃ ∪ {j}) − log γ₀(S̃) = log[(k̃ + 1)/(2p − 1 − k̃)] − ½ log(n + 1) + ν log(RSS_{Ũ_b}/RSS_{Ũ_b∪{j}}) + (R_{Ũ_b∪{j}} − R_{Ũ_b})
  ≥ −log(2p) − ½ log(n + 1) − 2κ_E + (RSS_{Ũ_b} − RSS_{Ũ_b∪{j}})/(2C_R)
((T4)(b) of L0). [R-3] By (V_b♭) (Ũ_b ⊆ C_b ∖ {j}, |Ũ_b| ≤ 15) and 𝓩: Write δ := δ_{Ũ_b,j}, Z := Z_{Ũ_b,j}; on 𝓩, |Z| ≤ z_n, and |δ| ≥ √(M_V log n) by (V_b♭). Put
z̄_n := √(2A log n) + √(42 log 2 + 2 log log n); then z_n ≤ z̄_n (z²_n = 2 log(2^{21}p) + 2 log log n ≤ 2A log n + 42 log 2 +
2 log log n, p ≤ n^A, √(a + b) ≤ √a + √b). Since M_V > 2Aσ², √(M_V log n) > σz̄_n for n ≥ n₀, and then
  RSS_{Ũ_b} − RSS_{Ũ_b∪{j}} = (δ + σZ)² ≥ (|δ| − σ|Z|)² ≥ (√(M_V log n) − σz̄_n)² = (√M_V − σ√(2A))² log n − e_n,
with 0 ≤ e_n ≤ 2√M_V σ√(log n)·√(42 log 2 + 2 log log n) = O(√(log n · log log n)). Hence
  log γ₀(S̃ ∪ {j}) − log γ₀(S̃) ≥ [(√M_V − σ√(2A))²/(2C_R) − A − ½] log n − log 2 − ½ log 2 − 2κ_E − e_n/(2C_R),
using log(2p) ≤ A log n + log 2 and ½ log(n + 1) ≤ ½ log n + ½ log 2. The bracket is a fixed positive number:
M_V > M_V⁰ means √M_V > σ√(2A) + √((2A + 1)C_R), i.e. (√M_V − σ√(2A))² > (2A + 1)C_R = 2C_R(A + ½). So the right side
is positive for n ≥ n₀ (n₀ depending on A, σ², M, M_V): this contradicts maximality.
So S₀ ⊆ S̃ and every block is good.

**(b) No junk — where the size of Q is paid for.** If Q = [p] there is nothing to prove. Otherwise let l ∈ Ũ_b ∖ Q and
U := Ũ_b ∖ {l}; U ⊇ S₀ ∩ C_b by (a), and S̃ ∖ {l} ∈ Ω. By (E6-tab), the prior ratio w(k̃ − 1)/w(k̃) = (2p − k̃)/k̃ ≥ p/k̃ and
Fact 2 (U ⊆ Ũ_b):
log γ₀(S̃ ∖ {l}) − log γ₀(S̃) = log[(2p − k̃)/k̃] + ½ log(n + 1) − ν log(RSS_U/RSS_{Ũ_b}) + (R_U − R_{Ũ_b})
  ≥ log p − log k̃ + ½ log(n + 1) − 2κ_E − (1 + ϑ^τ_n)(δ_{U,l} + σZ_{U,l})²/(2τ²_{Ũ_b}).
As in Step 1, τ²_{Ũ_b} ≥ τ²_U(1 − ζ_n); by (L_b), 𝓩 and σ ≤ τ_U:
(δ_{U,l} + σZ_{U,l})²/τ²_U ≤ (√(η log n) + z_n)² = η log n + z²_n + 2z_n√(η log n). Write L := log p ≤ A log n;
z²_n = 2L + 42 log 2 + 2 log log n and z_n ≤ √(2L) + √(42 log 2 + 2 log log n). Therefore

log γ₀(S̃ ∖ {l}) − log γ₀(S̃)
  ≥ L − log k̃ + ½ log n − 2κ_E − ½(1 + ϑ″_n)[η log n + 2L + 42 log 2 + 2 log log n + 2√(2Lη log n) + 2√((42 log 2 + 2 log log n)η log n)]
  ≥ [½ − η/2 − √(2Aη)] log n − log k̃ − ϑ″_n(A + 1 + η + √(2Aη)) log n − O(√(log n · log log n))
  = [½ − η/2 − √(2Aη)] log n − log k̃ − o(log n).

On 𝒢_n, k̃ ≤ 2k₀ = 2|Q| + 32s₀ ≤ (2 + 32s₀)n^b, so **log k̃ ≤ b log n + log(2 + 32s₀)** and the right side is at least
[β(η, A) − b] log n − o(log n) > 0 for n ≥ n₀, by (B). This contradicts maximality; so S̃ ⊆ Q.

(a) and (b) hold for every maximiser on 𝒢_n. ∎

## 4. Remarks

0. [R-4] **Visibility enters only here.** (V_b♭) is used in Step 2(a) and nowhere else: Step 1 (the ladder) and Step
   2(b) (junk exclusion) use (G3a), (L_b), (Q), (B) and the toolkit only (check of the parent text: the symbol M_n
   occurs only in (V_b) and Step 2(a)). The constant M_V⁰ ≤ 4Aσ² + 2C_R(2A + 1) ((x + y)² ≤ 2x² + 2y²); both scale like
   σ² under Y ↦ aY (C_R = 3(M + σ²) with M ↦ a²M).
1. **Failure probability.** P(Sand_n(Q)ᶜ) ≤ P(𝓔^blkᶜ) + 1/log n + C₂√(log n)·n^{−ξ/(1+ε₂)}; the term 1/log n comes from
   the choice of z_n and can be made polynomial (replace 2 log log n by 2c log n with a small c > 0: the margin in
   (b) loses (c + √(2cη)) log n, harmless for c small). Not claimed in the statement.
2. **What b < β(η, A) is.** With a start mode of size k̃ ≈ n^b, deleting an outside column gains
   log(p/k̃) + ½ log n in prior and determinant, and loses at most ½(√(η log n) + z_n)² ≈ log p + (η/2 + √(2Aη)) log n in
   fit: the margin is [½ − η/2 − √(2Aη) − b] log n. Nothing else in the proof uses the size of Q: the ladder of Step 1
   improves with |Q|, truth inclusion needs only feasibility. This is a sufficient budget of this argument, not a
   necessity statement.
3. **Relation to the sources.** With |Q| ≤ C log n and σ² in place of τ²_U this is C-GROW:L3; with log|Q| = o(log n)
   it is RM Lemma B2τ. The text above differs from them only in Step 2(b)'s last line and in using
   PARENT `lemmas/L0_toolkit_b.md` [R-0] for the block family.
