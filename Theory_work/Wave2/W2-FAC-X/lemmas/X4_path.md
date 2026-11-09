# X4 — Key lemma: under iid CS rows the LS0 path from S* is a pure null deletion with band-controlled holes, ending
certified at S₀ (claim (C2))

Status: **PROVED (by this seat, unchecked)**; key-lemma check R04 (Codex Sol xhigh, reviews/R04_X4_check_sol.md):
VERIFIED-WITH-AMENDMENTS, no FATAL/MAJOR; MINOR items 1–7 applied (reviews/R04_disposition.md). Falsification numerics: numerics/N1X_summary.md (121/121 iid-row paths
from [p] are pure null deletions ending at S₀; band width ≈ 1.3–1.5·δ̂, δ̂ ≈ 2–3·√(k log p/n)); numerics/N3X_out.txt
(X3 under adversarial ϖ-approximate rules).

Setting: STATEMENT §1–2 (FS not needed), X1 (representation, gains), X2 (event 𝔈_n, Proposition X2), X3
(deterministic soft gap). FACB = `Theory_work/Wave2/W2-FAC-B/lemmas/`. The claim concerns the uncapped §6.10 search
started at S* = [p] ∖ N₀, N₀ the (X-measurable, random) set of nulls sharing the method's block with all truths,
|N₀| ≤ 15. We prove the claim **simultaneously for every 𝔫 ⊆ 𝒩_all with |𝔫| ≤ 15** in place of N₀ (so the dependence of
the partition on the data is irrelevant): all events below are defined on 𝒩_all = [p] ∖ S₀.

## X4.0 Constants, regimes and the event

A₁ ∈ (0, ½) with p ≤ n^{A₁} for n ≥ n₀. ε_b := min{1/50, (½ − A₁)/5}; K₁ := 100/ε_b²; m₁ := ⌈K₁L_n⌉; ε′ := ε_b/100;
H := √(2 log(2m_all + 2)), m_all := p − s₀, H̄² := H² + 2L_n; δ_e := 2 log(25(m₁ + 32)H)/H; g_max := 16L_n + δ_e;
ϖ := ϖ_n := 6C_X H̄√(p log n/n) + n^{−1/3} (C_X from X2); w := 4.3ϖ. Regimes per n as FACB: (S) p ≤ n^{1/200},
(L) p > n^{1/200}. κ′ := s₀ + κ, κ_∞ := (1 − ρ)/ρ.

**The event 𝔊_n := 𝔈_n ∩ E′_n ∩ D7 ∩ D8**, where 𝔈_n is X2.1 with D6 for the widths w and 9ϖ, and:
* **E′_n** = FACB L3's E3–E7 for the sample 𝒩_all (in place of 𝒩*), with E6 for the (m₁ + 16)-th order statistics
  (ζ±_(m₁+16) ≥ H − δ_e) and E7 strengthened to "every interval of length L_n/2 in [0, H − δ_e] contains ≥ 16 values
  |ξ_j| of each sign"; E1 replaced by D3/D4 (|η|, |ξ_j| (j ∈ S₀) ≤ √(2L_n) ≤ H̄; no condition on N₀); E2 is replaced by D3 and X1.4. Probability → 1 by
  FACB L3.1's proofs (E6: Bin(m_all, Φ̄(t₀)) with mean 2(m₁ + 16) — same Chernoff bound; E7: the cell count is
  Bin with mean ≥ L_n(m₁ + 16)/2, and P(Bin < 16) ≤ e^{−mean/8} for mean ≥ 64).
* **D7 (tail ratio)** for every t ∈ [0, H̄ + 1] and σ ∈ {+, −}:
  #{l ∈ 𝒩_all : σξ_l ∈ [t, t + 9ϖ)} ≤ ε′·#{l ∈ 𝒩_all : σξ_l ≥ t + 9ϖ} + T₀, with T₀ := ⌈8/c_w⌉ + 1, c_w := (½ − A₁)/4.
* **D8 (spacings)** (L): with y_n := Φ̄⁻¹((4m₁ + 2)/m_all), for each σ ∈ {+, −}: #{l ∈ 𝒩_all : σξ_l ≥ y_n} ≥ 2m₁ + 1,
  and any two distinct nulls l, l′ with σξ_l, σξ_{l′} ≥ y_n satisfy |ξ_l − ξ_{l′}| > c₁ϖ, c₁ := 9 + 8/κ_∞ (so the 2m₁ + 1
  largest values of σξ are c₁ϖ-separated); (S): any two distinct null values ξ_l differ by > c₁ϖ.

**Lemma X4.0.** P(𝔊_n) → 1.
*Proof.* 𝔈_n, E′_n: X2.1 and the remark above. D7: let q(t) := P(σξ ∈ [t, t + 10ϖ)) ≤ 10ϖφ(t) and
F(t) := Φ̄(t + 10ϖ); grid t_r := rϖ ∩ [0, H̄ + 1] (≤ 2H̄/ϖ + 2 ≤ n points); every [t, t + 9ϖ) lies in some
[t_r, t_r + 10ϖ), and {σξ ≥ t + 9ϖ} ⊇ {σξ ≥ t_r + 10ϖ}. For a grid point put μ := m_all F(t_r) (the mean
tail count; R04 item 1). Hazard bound: φ(u)/Φ̄(u) ≤ u + 1 for u ≥ 0, hence Φ̄(t)/Φ̄(t + h) ≤ e^{h(t + h + 1)} and, with
h = 10ϖ, m_all q(t_r) ≤ 10ϖ·m_all φ(t_r) ≤ 10ϖ(1 + t_r)e^{h(t_r + h + 1)}μ ≤ 20ϖ(2 + H̄)μ for n ≥ n₀ (ϖH̄ → 0).
If μ ≥ log³n: #{σξ ≥ t_r + 10ϖ} ≥ μ/2 except with probability e^{−μ/8} ≤ e^{−log³n/8}, and the window count is
≤ e²m_all q + 3 log n + 1 (as D6, failure ≤ n^{−3}) ≤ ε′μ/2 for n ≥ n₀ (ϖH̄ → 0, log n/log³n → 0). If μ < log³n:
m_all q ≤ 20ϖ(2 + H̄)log³n ≤ n^{−c_w} for n ≥ n₀ (ϖ ≤ n^{−(½−A₁)/2+o(1)}), so P(window ≥ T₀) ≤ (e·m_all q)^{T₀} ≤ n^{−c_wT₀/2}
≤ n^{−4}. Union over ≤ 3n(H̄ + 1) grid points and two signs → 0; m_all = 0 is trivial. D8 (L): #{σξ ≥ y_n} ~ Bin(m_all, (4m₁ + 2)/m_all) has mean 4m₁ + 2, so it is ≥ 2m₁ + 1 except with
probability ≤ e^{−(4m₁+2)/8} → 0 (Chernoff). For the separation, with t := c₁ϖ and y := y_n (y ≤ H̄ eventually),
P(∃ l ≠ l′ : σξ_l, σξ_{l′} ≥ y, |ξ_l − ξ_{l′}| ≤ t) ≤ m_all²·Φ̄(y)·2tφ(y − t) ≤ 2t e^{tH̄}·m_all²Φ̄(y)φ(y) and, by
φ(y) ≤ 2(1 + y)Φ̄(y), this is ≤ 4t e^{tH̄}(1 + H̄)(4m₁ + 2)² → 0 (t = c₁ϖ ≤ n^{−c}, m₁, H̄ = n^{o(1)}). (S): P ≤ p²c₁ϖ·(2π)^{−1/2} ≤ n^{1/100}c₁ϖ → 0.
**Nondegeneracy (R04 item 2).** ND_n := {the null ξ's are distinct; ξ_l ≠ x_T for every null l and every S₀ ⊆ T ⊆ [p]}:
for fixed n finitely many nontrivial linear relations in (ξ, η) given φ, so P(ND_n) = 1. **𝔊_n is redefined as
𝔈_n ∩ E′_n ∩ D7 ∩ D8 ∩ ND_n**; one event serves every 𝔫. (Without ND_n the deterministic statements fail on a null set,
e.g. a null coordinate equal to x_0.) At K = ∅ the extended endpoints a = −∞, b = +∞ are used directly. ∎

Standing consequences on 𝔊_n (n ≥ n₀): those of X2.1 (λ_min(G_T) ≥ c₀(n − 1), q_T ≤ 1/10, |x_T| ≤ C_ρH̄ (C_ρ = 1 + ℓ), κ ∈ [κ_∞/2,
2κ_∞]); FACB L3 (c2) for 𝒩* = 𝒩_all ∖ 𝔫 (removing ≤ 15 points merges ≤ 16 consecutive gaps, hence g_max = 16L_n + δ_e;
E7 gives ≥ 1 point of 𝒩* per cell); E5 transfers to 𝒩* with errors ≤ 15H̄ in D_j and ≤ 15 in P_j; and m₀ = |𝒩*| ∈
[m_all − 15, m_all], m₀± ≥ m₀/3 − 15.

## X4.1 The gain-ordering slack (from X1.4)

On 𝔊_n, for every T ⊇ S₀ with k ≥ s₀ + 1 and nulls j, j′ ∈ T: if G_del(j; T) ≥ G_del(j′; T) and |τ̂_j|, |τ̂_{j′}| ≤ 3H̄,
then |τ̂_j(T)| ≤ |τ̂_{j′}(T)| + C_g n^{−1/2}, with C_g := 2C₁^{1/2} (R14 item 4).
*Proof.* With u_j := (1 + γ_{k−1})M_T(1 + ε^d_j)τ̂_j²/ν + r_j/ψ_T (X1.4 (g3)), G_del(j) ≥ G_del(j′) gives
ν log((1 + u_j)/(1 + u_{j′})) ≤ ½(e¹_{j′} − e¹_j) ≤ 3/(c₀n), so u_j ≤ u_{j′} + 7(1 + u_j)/(c₀νn); multiply by
ν/((1 + γ_{k−1})M_T) ≤ 4ν (M_T ≥ ¼; 1 + u_j ≤ 2): with ε^d_j ≥ 0, ε^d_{j′} ≤ 2ω_{j′}² = 2τ̂_{j′}²/(N(1 − γ_k)) ≤ Cτ̂_{j′}²/n
and |νr/ψ| ≤ Cn^{−3/2}(1 + τ̂²) (X1.4 (g3)),
  τ̂_j² ≤ τ̂_{j′}² + E,  E := C₁/n + C₁|τ̂_{j′}|⁴/n
(the determinant errors give C/n, the ε^d term C|τ̂_{j′}|⁴/n, the ridge terms are smaller; R02 item 4). With a := |τ̂_{j′}|
and √(x + y) ≤ √x + y/(2√x) applied to x := a² + C₁/n ≥ a², y := C₁a⁴/n:
|τ̂_j| ≤ a + √(C₁/n) + C₁a³/n ≤ |τ̂_{j′}| + C₁^{1/2}n^{−1/2}(1 + 27C₁^{1/2}H̄³n^{−1/2}) ≤ |τ̂_{j′}| + 2C₁^{1/2}n^{−1/2} = |τ̂_{j′}| + C_g n^{−1/2},
since 27C₁^{1/2}H̄³n^{−1/2} ≤ 1 for n ≥ n₀. ∎

**Corollary X4.1 (rule R_ϖ).** If moreover T is (a, b; w)-structured with exceptional set 𝔫 (|𝔫| ≤ 15) and #Band ≤
2(2e²pw + 3 log n + 1), then the best deletion j° := argmax_{j∈T∖S₀}G_del(j; T) satisfies
|ξ_{j°} − x_T| ≤ min_{j∈T∖S₀}|ξ_j − x_T| + 2ϖ.
*Proof.* Proposition X2 with this band count: |δ_j(T)| ≤ C_X·3H̄[√(p log n/n) + (4e²p·4.3ϖ + 6 log n + 19)√(log n/n)]
≤ ϖ/2 + 52e²C_X H̄p√(log n/n)·ϖ + C H̄(log n)^{3/2}/√n ≤ ϖ/2 + ϖ/8 + n^{−1/3}/8 for n ≥ n₀, **because
p H̄√(log n/n) → 0 (A₁ < ½)**. With j_c the kept null closest to x_T, X4.1 gives
max_j|δ_j(T)| ≤ ¾ϖ (n^{−1/3} ≤ ϖ), so |ξ_{j°} − x_T| ≤ |τ̂_{j°}| + ¾ϖ ≤ |τ̂_{j_c}| + C_gn^{−1/2} + ¾ϖ ≤ |ξ_{j_c} − x_T| + (3/2)ϖ
+ C_g n^{−1/2} ≤ d_T + 2ϖ (C_g n^{−1/2} ≤ n^{−1/3}/2 ≤ ϖ/2 for n ≥ n₀). The envelope (R04 item 3): with d := N/φ² ∈ [½, 2] (D3), κ = d/ℓ² and ϱ = dη/ℓ, so for k ≥ 1
|x_T|/H̄ ≤ (kℓ² + dℓ)/(kℓ² + d) ≤ 3/2 (since (kℓ² + d)/2 − d(ℓ − 1) = kℓ²/2 − dℓ + 3d/2 > 0, a quadratic in ℓ with discriminant
d² − 3kd = d(d − 3k) < 0 for d ≤ 2, k ≥ 1; |Σ_Tξ| ≤ kH̄, |η| ≤ H̄). Hence H̄ + |x_T| ≤ 2.5H̄ (so Proposition X2's factor is ≤ 2.5H̄ ≤ 3H̄, as used
above) and |ξ_j − x_T| ≤ 2.5H̄ ≤ 3H̄ − 1 eventually, giving the bound |τ̂| ≤ 3H̄ needed in X4.1. ∎

## X4.2 The induction

**Lemma X4.** For n ≥ n₀ (depending on ρ, ϑ, σ, s₀, A₁), on 𝔊_n, for every 𝔫 ⊆ 𝒩_all with |𝔫| ≤ 15 and start
S* := [p] ∖ 𝔫: the uncapped search from S* makes exactly m₀ := |S* ∖ S₀| moves; the move at T_i is the deletion of the
best-deletion null j°_i, which satisfies rule (R_ϖ) and has positive gain; every addition has gain ≤ −c log n,
c := min{0.29, c_D/2, 0.6(½ − A₁)}, c_D := ½ − 1/(s₀ + 1 + κ_∞); every truth deletion and truth-out swap has negative
gain; every null-out swap has gain strictly below G_del(j°_i); every T_i satisfies
𝒩* ∩ (a_i, b_i) ⊆ 𝒩* ∖ T_i ⊆ 𝒩* ∩ (a_i − w, b_i + w); T_{m₀} = S₀ and every feasible neighbour of S₀ has strictly
smaller F.

*Proof structure.* Induction on i with hypothesis 𝓗(i): the moves at T_0, …, T_{i−1} are best deletions of nulls of
𝒩* satisfying (R_ϖ). Given 𝓗(i): X3 applies to the kept sequence K_0 = 𝒩*, …, K_i (with B = Σ_{S₀}ξ − ϱ, κ′ = s₀ + κ,
x = x_T), giving the band structure of T_i (§X4.3–X4.5 check X3's hypotheses); Corollary X4.1 then gives (R_ϖ) for j°_i;
§X4.3–X4.6 show that j°_i's deletion is the best move with the stated margins. So 𝓗(i + 1). Truth moves: §X4.6 (uniform
over all T ⊇ S₀).

**Dependency table (R02 suggestion 2; no step uses a future move).**
| at step i, from | gives | used for |
|---|---|---|
| 𝓗(i) = (R_ϖ) at steps 0, …, i − 1 (a prefix) | X3 prefix form: band structure (4.1) of T_i | X2 at T_i, T_i ∖ j, T_i ∪ l, T_i ∖ j ∪ l |
| (4.1) + D6 | #Band ≤ 2(2e²pw + 3 log n + 1) | Corollary X4.1: (R_ϖ) for the best deletion at T_i |
| (4.1) + D7 + E5 | band counts ≤ ε′(m + 15) + T₀ | B3(i) |
| B3(i − 1), X3 (vii)/(v) | B1(i) | B2(i) |
| B1(i), B1(i − 1), (4.1) | B2(i) | B3(i) |
| B3(i), X2, X1.4 | B4(i): best move = best deletion, margins | 𝓗(i + 1) |
| end phase: (4.1) at i_e + D7 + D8 | exact top sets, propagated by (a)–(c) of X4.5 | FACB L4.4 with τ̂ |

## X4.3 Regime (S)

On D8(S) all distinct null values differ by > c₁ϖ, and in X3 a crossing at step i forces
d_i < 2ϖ/(|K_i| − 2 + κ′) ≤ 2ϖ/(κ′ − 1) ≤ 4ϖ/κ_∞ and ω_i ≤ 2d_i + 2ϖ < c₁ϖ (X3 (iii), general-|K| form:
|K_i| − 2 + κ′ ≥ κ′ − 1 ≥ κ_∞/2 > 0). Since ω_i ≥ min spacing > c₁ϖ whenever both sides are nonempty (and no crossing is
possible on an empty side), no step is a crossing; by X3 (iv), (ii) and the spacing, every deletion is of an edge point
a_i or b_i and the hole is exactly 𝒩* ∩ (a_i, b_i) (X3 (ix)). Then FACB L4.2 applies with τ replaced by τ̂ = τ + δ,
|δ| ≤ ϖ (X2 with #Band = 0): every null has τ̂² ≤ (2H̄ + ℓ√(2L_n) + ϖ)² ≤ 0.1 log n (|x_T| ≤ H̄ + ℓ√(2L_n) by X2.1; H̄² ≤ (1/90)log n + 2L_n in
regime (S)); with X1.4 (g3)–(g5) and M ≤ ½(1 + C/n):
every null deletion has gain ≥ 0.29 log n, every addition ≤ −0.29 log n, every null-out swap
G_sw ≤ M V̂(1 + o) + O(1/n) ≤ (τ_l² + o(1))(½ + o) ≤ 0.11 log n. Truth moves: §X4.6. ∎(S)

## X4.4 Regime (L), bulk (m_i ≥ m₁): FACB Claim B with perturbations

Claim B′ (for i < i*, i* := first index with m_{i*} < m₁): (B1) both sides of x_i nonempty; (B2) Δ_i := |R_i − L_i| ≤
ε_bH/2; (B3) |x_i| ≤ ε_bH; (B4) the best move at T_i is the deletion j°_i, G_del(j°_i) ≥ 0.3 log n, every addition
≤ −0.7(½ − A₁)log n, every null-out swap < G_del(j°_i). Proved in FACB's order (B1, B2, B3, B4 at each i), using 𝓗(i).

**X3 applied to the established prefix (R02 item 1).** Under 𝓗(i) the steps 0, …, i − 1 form a prefix of length I := i
satisfying (R_ϖ), with |K_{i′}| = m_{i′} ≥ m₁ ≥ 3 for i′ < i ≤ i*. Q := max #(points of 𝒩* in an interval of length 9ϖ)
≤ 18e²pϖ + 3 log n + 1 (D6), and 4Qϖ/(m₀ − Q − 1 + κ′) ≤ ϖ/10 for n ≥ n₀ (Q/m₀ → 0: ϖp/m₀ ≤ 2ϖ → 0 and
log n/m₀ ≤ 2n^{−1/200}log n → 0). X3 (vii)–(viii) in prefix form (no future step is used) give, for T_i:
  𝒩* ∩ (a_i, b_i) ⊆ D_i ⊆ 𝒩* ∩ (a_i − w, b_i + w),  w = 4.3ϖ,                                         (4.1)
T_i is (a_i, b_i; w)-structured with exceptional set 𝔫, and #Band(a_i, b_i; w) ≤ 2(2e²pw + 3 log n + 1) (D6), so
Corollary X4.1 gives (R_ϖ) for j°_i.

**Band counts relative to m (from D7).** If a_i > −∞, every null of 𝒩* below a_i − w is kept (4.1), so
#(Band near a_i) ≤ #{l ∈ 𝒩_all : −ξ_l ∈ [|a_i|, |a_i| + w)} ≤ ε′(N₋ + 15) + T₀ when a_i < 0 (D7 with t = |a_i|; the kept
endpoint a_i itself is counted; the comparison tail {−ξ ≥ |a_i| + 9ϖ} consists of kept negatives and ≤ 15 points of 𝔫 —
R07 item 1), and symmetrically #(Band near b_i) ≤ #{l : ξ_l ∈ [b_i, b_i + w)} ≤ ε′(N₊ + 15) + T₀ when b_i > 0. (Window
[t, t + 9ϖ) ⊇ [t, t + w).)

**i = 0.** x_0 = (Σ_{S₀}ξ + Σ_{𝒩*}ξ − ϱ)/(m₀ + κ′) with |Σ_{𝒩*}ξ| ≤ H̄√(2m_all x_{m_all}) + 15H̄ (E5 for 𝒩_all), so
|x_0| → 0; E6 gives kept nulls of both signs with |ξ| ≥ H − δ_e > |x_0| (B1); Δ_0 ≤ ω_0 ≤ g_max ≤ ε_bH/2 (B2).

**(B3) at i.** *Case A: a_i < 0 < b_i.* If x_i > Δ_i/2 + ϖ: then b_i + a_i = (R_i − L_i) + 2x_i > 0, so b_i > |a_i|. Every
kept null lies in (−∞, a_i] ∪ [b_i, ∞). Let J″ := #{l ∈ 𝒩_all : |ξ_l| ≥ |a_i|} and K⁰ := {l ∈ 𝒩* : |ξ_l| ≥ |a_i|} ⊇ K_i.
K⁰ ∖ K_i consists of (α) positives in [|a_i|, ∞) (removing them lowers the sum) and (ϖ) deleted negatives in
(a_i − w, a_i] (band). Hence
  s_{K_i} ≤ s_{K⁰} + #(ϖ)·(|a_i| + w) ≤ |D^{all}_{J″}| + 15H̄ + (ε′(m_i + 15) + T₀)(H̄ + w).
Size of J″: the negatives in Top_{all}(J″) are the kept negatives (N₋ ≤ m_i), the band negatives of (ϖ) and ≤ 15 points
of 𝔫; by E5 (all-null version), J″/2 − √(J″x_{J″}/2) ≤ N₋ + ε′(m_i + 15) + T₀ + 15, so
J″ ≤ 2.1m_i + C₀ + √(2J″x_{J″}) (C₀ := 2T₀ + 31). If J″ ≥ 5m_i then x_{J″}/J″ ≤ x_{5m₁}/(5m₁) ≤ 1/50 (n ≥ n₀), so
√(2J″x_{J″}) ≤ J″/5 and J″ ≤ (5/4)(2.1m_i + C₀) < 5m_i — contradiction; so J″ ≤ 5m_i. Therefore, with
k_i + κ ≥ m_i and |D^{all}_{J″}| ≤ H̄√(2J″x_{J″}) ≤ H̄√(10 m_i x_{5m_i}):
  x_i ≤ [s₀L_n + C L_n + 15H̄ + 1.1T₀H̄]/m_i + H̄√(10x_{5m_i}/m_i) + 1.1ε′H̄(1 + 15/m_i)
     ≤ ε_bH/10 + 0.34ε_bH̄ + ε_bH̄/50 ≤ ε_bH
(FACB's computation 10x_{5m}/m ≤ 11/K₁ = 0.11ε_b² for m ≥ m₁; (15 + 1.1T₀)/m₁ → 0; H̄ ≤ 1.01H). Symmetrically
x_i < −Δ_i/2 − ϖ implies x_i ≥ −ε_bH. Otherwise |x_i| ≤ Δ_i/2 + ϖ ≤ ε_bH/4 + ϖ.
*Case B: a_i ≥ 0* (resp. b_i ≤ 0). By (4.1) every null of 𝒩* below −w is kept, so m_i ≥ m₀/3 − 15 − (2e²pw + 3 log n + 1)
≥ m₀/4; and D_i ⊆ (a_i − w, ∞) ⊆ (−w, ∞), so s_{D_i} ≥ −w·#(𝒩* ∩ (−w, 0)) ≥ −w(2e²pw + 3 log n + 1) ≥ −1 (D6; w·count ≤ Cpw² + Cw log n = o(1) since
w = O(H̄√(p log n/n) + n^{−1/3}) and p ≤ n^{A₁}, A₁ < ½ — R06 item 3) and
s_{K_i} = s_{𝒩*} − s_{D_i} ≤ H̄√(2m_all x_{m_all}) + 15H̄ + 1. With x_i > a_i ≥ 0:
0 < x_i ≤ (C L_n + H̄√(2m_allx_{m_all}) + 15H̄ + 1)/(m₀/4) ≤ ε_bH. Symmetric for b_i ≤ 0.

**(B2) at i ≥ 1.** If i ≤ i₀ (X3's initial phase): by X3 (vii) every deleted null lies in [x_0 − 4.1ϖ, x_0 + 4.1ϖ] and
|x_i − x_0| ≤ ϖ/10; the nearest points of 𝒩* outside that window (on each side) are kept and within g_max of it ((c2):
consecutive gaps of 𝒩* near 0, including the gap across 0, are ≤ g_max), so L_i, R_i ≤ 4.3ϖ + g_max and
Δ_i ≤ max(L_i, R_i) ≤ ε_bH/2. If i > i₀, step i − 1 ≥ i₀ is not a crossing (X3 (v)).
Say the deleted null ξ_{j} lies above x_{i−1} (else symmetric). By (R_ϖ) and X3 (ii): R_{i−1} ≤ ξ_j − x_{i−1} ≤ d_{i−1}
+ 2ϖ ≤ L_{i−1} + 2ϖ, so R_{i−1} − L_{i−1} ∈ [−Δ_{i−1}, 2ϖ]. With h := (ξ_j − x_{i−1})/(k_{i−1} − 1 + κ) ∈
(0, (d_{i−1} + 2ϖ)/(m₁ − 1)]: a_i = a_{i−1}, L_i = L_{i−1} − h, and b_i ≥ b_{i−1} with b_i − b_{i−1} ≤ w + g_max (if
the point at b_{i−1} was deleted, the next kept point above is at most the next point of 𝒩* above b_{i−1} + w, by (4.1)
and (c2)); R_i = R_{i−1} + h + (b_i − b_{i−1}). Hence R_i − L_i ∈ [R_{i−1} − L_{i−1}, R_{i−1} − L_{i−1} + 2h + w + g_max] and
  Δ_i ≤ max(Δ_{i−1}, 2ϖ + w + g_max + 2(d_{i−1} + 2ϖ)/(m₁ − 1)) ≤ ε_bH/2
(d_{i−1} ≤ H̄ + |x_{i−1}| ≤ C_ρH̄ + H̄; g_max = O(L_n); ϖ, w → 0).

**(B1) at i ≥ 1.** (R02 item 1.) *Narrow phase, i ≤ M (X3 (vii)):* every deleted null lies in [x_0 − 4.1ϖ, x_0 + 4.1ϖ]
and |x_i − x_0| ≤ ϖ/10, |x_0| → 0; by E6 there are kept nulls of both signs with |ξ| ≥ H − δ_e > |x_i| + 5ϖ, so both sides of
x_i are nonempty. *Wide phase, i > M:* step i − 1 ≥ i₀ is not a crossing (X3 (v)), so a side of T_i is empty only if it was
empty at T_{i−1} (impossible by B1 at i − 1) or its single point was the deleted one; suppose the lower side of T_{i−1} is
the single point a := a_{i−1} and it is deleted (the upper case is symmetric). All other nulls of 𝒩* below x_{i−1} are
deleted, so by (4.1) they lie above a − w: a ≤ min_{𝒩*}ξ + w. If a ≥ 0, every negative of 𝒩* (≥ m₀/3 − 15 of them) is
below x_{i−1} and ≠ a, hence deleted, hence in (a − w, 0) ⊆ (−w, 0) — impossible (D6: a window of length w holds
≤ 2e²pw + 3 log n + 1 ≪ m₀ nulls).
So a < 0 and |a| ≥ ζ₋_(1)(𝒩*) − w ≥ H − δ_e − w (E6). (R_ϖ) requires L_{i−1} ≤ R_{i−1} + 2ϖ (deleting a lower point:
L ≤ d + 2ϖ ≤ R + 2ϖ), i.e. |a| + x_{i−1} ≤ b − x_{i−1} + 2ϖ, so b ≥ H − δ_e − w − 2ε_bH − 2ϖ ≥ (1 − 3ε_b)H by (B3) at
i − 1. The upper side has N₊ = m_{i−1} − 1 ≥ m₁ − 1 kept points, all ≥ b, so
x_{i−1}(k + κ) ≥ N₊(1 − 3ε_b)H − H̄ − CL_n − s₀L_n with k + κ = N₊ + 1 + s₀ + κ, giving x_{i−1} ≥ (1 − 4ε_b)H > ε_bH,
contradicting (B3) at i − 1.

**(B4) at i < i*.** Fix T = T_i, m = m_i ≥ m₁, k = m + s₀. Some kept null has |ξ| ≤ ζ_(m)(𝒩*) ≤ Z_m (E4 for 𝒩_all;
removing points lowers order statistics), so d := d_T ≤ Z_m + ε_bH (B3).
*Best deletion.* With j_c the closest kept null, G_del(j°) ≥ G_del(j_c) ≥ Δ_k − 3/(c₀n) − (1 + γ_{k−1})M_T(1 + ε^d)(d + ϖ)²
− o(1) (X1.4 (g3), log(1 + u) ≤ u), and M_T ≤ ½(1 + C/n), γ_{k−1} ≤ 1/m₁, (d + ϖ)² ≤ d² + 3ϖH̄. FACB (B4) case (i)'s
computation (p ≤ n/log³n always here) then gives G_del(j°) ≥ 0.35 log n.
*Additions* (any null l ∉ T, including N and hole points): by X1.4 (g4) and X2 at T ∪ l (Corollary X2):
(1 + γ_k)(1 + ε^d)τ̂_l(T ∪ l)² ≤ (1 − γ_{k+1})(|ξ_l − x_T| + 2ϖ)²(1 + C H̄²/n) ≤ H̄²(1 + 2.2ε_b) for n ≥ n₀
(τ̂_l(T ∪ l) = (1 − γ_{k+1})(ξ_l − x_T) + δ and (1 + γ_k)(1 − γ_{k+1})² = 1 − γ_{k+1}, so the δ-term enters as
|δ|/(1 − γ_{k+1}) ≤ 2|δ| ≤ 2ϖ since γ_{k+1} ≤ ½ — R02 item 4; |ξ_l| ≤ H̄,
|x_T| ≤ ε_bH), and M_{T∪l} ≤ ½(1 + C/n). With Δ_{k+1} = log((2p − k − 1)/(k + 1)) + ½log(n + 1), ½H̄² = log(2m_all + 2) + L_n
and k + 1 ≤ p:
  G_add(l; T) ≤ log((k + 1)(2p + 2)/(2p − k − 1)) + 2.2ε_b log(2p + 2) + O(L_n) − ½log n
             ≤ (A₁(1 + 2.2ε_b) − ½)log n + O(L_n) ≤ −0.7(½ − A₁)log n
(2p − k − 1 ≥ p − 1; ε_b ≤ (½ − A₁)/5 gives 2.2ε_bA₁ ≤ 0.22(½ − A₁)).
**Remark (R14 item 1).** The binding margin of the uniform-in-𝔫 claim is this bulk addition bound (and its use at T ∖ j for
swaps), whose margin is ½log n − log(2p + 2) − O(L_n) up to the ε_b terms; adversarial 𝔫 (the 15 largest positive ξ excluded
and offered back as additions) is the worst case. Numerically (reviews/R14_scratch/adv_n0_out.txt, adv_fail_out.txt):
23/24 adversarial-𝔫 paths clean at n ∈ {10⁵, 10⁶}; the single failure (n = 10⁵, p = 180) occurs where this margin is still
negative (½log n = 5.76 < log(2p + 2) + L_n = 8.34) and disappears at n ∈ {10⁷, 10⁹} (8/8 clean) — a finite-n effect, consistent
with the asymptotic claim.
*Null-out swaps* (j ∈ T null, l ∉ T null): G_sw(j, l) = G_del(j; T) + G_add(l; T ∖ j) ≤ G_del(j°; T) + G_add(l; T ∖ j), and
the addition bound holds at T ∖ j (R04 item 4: T ∖ j has exceptional set 𝔫 ∪ {j} (size ≤ 16) and its addition
statistic is taken at T ∖ j ∪ l (size ≤ 17); the absorption calculation of Corollary X4.1 with #Band + 17 unchanged
gives |δ| ≤ ϖ there; |x_{T∖j}| ≤ |x_T| + 3H̄/(m₁ − 1) ≤ 1.01ε_bH, so the squared envelope is H̄²(1 + 2.3ε_b) and
2.3ε_bA₁ ≤ 0.23(½ − A₁)): G_sw(j, l) ≤ G_del(j°) − 0.6(½ − A₁)log n < G_del(j°).
*Truth moves:* negative (§X4.6). Hence the best move is the deletion j°, which satisfies (R_ϖ) (Corollary X4.1). ∎(B′)

## X4.5 Regime (L), end phase (m_i < m₁)

Let i_e := i*. **Entry:** |x_{i_e}| ≤ ε_bH + (H̄ + ε_bH)/(m₁ − 2) ≤ 2ε_bH (drift identity and (B3) at i_e − 1).

**Exact structure from i_e on.** At i_e, (4.1) holds (X3 (viii) with I = i_e) and a_{i_e} < 0 < b_{i_e} (B1 also holds at i = i* by the same wide-phase argument, since N₊ ≥ m₁ − 1 there — R20 item 5;
one-sided states are in any case covered by the sign/separation invariant below; Case B is
impossible: it forces m ≥ m₀/4 > m₁). Kept positives include every positive of 𝒩* ≥ b + w, so
#{l ∈ 𝒩* : ξ_l ≥ b + w} ≤ m < m₁; by D7, #{l ∈ 𝒩_all : ξ_l ∈ [b, b + w)} ≤ ε′(m₁ + 15) + T₀; so #{l ∈ 𝒩_all : ξ_l > b} ≤ m₁ + ε′(m₁ + 15) + T₀ + 15 ≤ 2m₁, i.e. b is among the 2m₁ + 1 largest positive values
of 𝒩_all, and by D8 no other null lies in [b, b + c₁ϖ] ⊇ [b, b + w); so no deleted null lies in [b, b + w), and
likewise at a. Hence D_{i_e} = 𝒩* ∩ (a, b) exactly, and K_{i_e} =
Top₊(N₊) ∪ Top₋(N₋) (FACB L4.1(iii)). Induction for i ≥ i_e (R02 item 4): suppose D_i = 𝒩* ∩ (a_i, b_i) and every kept null has
|ξ| ∈ [H − δ_e, H̄] (true at i_e by the above, E6 and E3: the kept nulls are the top N₊ positives and top N₋ negatives
of 𝒩*, N± < m₁, and E6 gives ζ±_(m₁)(𝒩*) ≥ H − δ_e). (a) *No crossing at step i.* A crossing needs both sides nonempty
(X3 (iii)); then ω_i = b_i − a_i ≥ 2(H − δ_e) > c₁ϖ ≥ c(κ′)ϖ (κ′ − 1 ≥ κ_∞/2), contradicting X3 (iii) (whose general-|K|
form needs only |K_i| ≥ 1). If a side is empty, say the lower one, the deleted null lies above x_i, x_{i+1} < x_i, and no
kept point lies below x_i, so there is no crossing and the lower side stays empty (X3 (iv)). (b) *Edge deletion.* By X3 (ii)
the deleted null ξ_j lies in [b_i, b_i + 2ϖ] (or [a_i − 2ϖ, a_i]); b_i is among the 2m₁ + 1 largest positive values of
𝒩_all (#{𝒩_all ∋ l : ξ_l > b_i} ≤ N₊ + 15 ≤ 2m₁, all positives of 𝒩* above b_i being kept), so by D8 the only null in
[b_i, b_i + c₁ϖ] is b_i itself: j is the edge point. (c) By (a), (b) and X3 (iv), D_{i+1} = 𝒩* ∩ (a_{i+1}, b_{i+1}) and the
kept set is again Top₊(N₊′) ∪ Top₋(N₋′) ⊆ the previous kept set, with magnitudes in [H − δ_e, H̄]. (FACB L4.1(i)–(iii) are
thereby re-proved for the approximate rule in this phase rather than imported.)

**Sign/separation invariant (R06 item 2).** With B := Σ_{S₀}ξ − ϱ = O(L_n) and m := |K_i| < m₁ (|ξ| ≤ H̄ for kept
nulls): |x_i| ≤ (mH̄ + |B|)/(m + s₀ + κ) and H̄ − |x_i| ≥ ((s₀ + κ)H̄ − |B|)/(m + s₀ + κ) ≫ δ_e + ϖ (as H̄/m₁ ≫ δ_e + ϖ);
since kept nulls have |ξ| ≥ H − δ_e ≥ H̄ − 2δ_e, every kept positive lies above x_i and every kept negative below x_i,
also in one-sided configurations. This is the invariant FACB L4.4 uses to identify K_i with Top₊(N₊) ∪ Top₋(N₋).

**Order of the argument at an end-phase step (R04 item 5).** At an established state T_i with exact hole (so it is
(a_i, b_i; 0)-structured, #Band = 0), Proposition X2 and Corollary X4.1 give (R_ϖ) for the best-deletion candidate j°;
(a)–(c) above are applied to the hypothetical deletion of j° (not assuming it is the chosen move); the comparisons
below then show it is the best move, so it is the actual move and (c) propagates. FACB's notation is used: I := N₊ − N₋,
h := H̄², s_K = IH̄ + E with |E + B| ≤ e_n = O(L_n), and H̄/m₁ ≫ δ_e + ϖ; κ = κ_∞(1 + O(n^{−1/3})) by D3, which is what
preserves FACB's constant c_D.

FACB L4.4 then applies verbatim with τ replaced by τ̂ = τ + δ, |δ| ≤ ϖ (X2 with #Band = 0 and E = 𝔫, or 𝔫 ∪ {j, l}
for swap statistics), M_T ≤ ½(1 + C/n) in place of ½(1 + ε′), and the j-dependent errors of X1.4. Every FACB L4.4 bound
has a margin of order log n (or at least (H̄ − x)·x ≫ ϖ for (E-side)), while the replacements change the relevant
quadratic quantities by O(ϖH̄ + ϖ² + H̄⁶/n + 1/n) = o(1) (the H̄⁶/n from (g5)'s CH̄⁴max ω², ω² = O(H̄²/n)):
* **(E-del)** G_del(j°) ≥ G_del(j_c) ≥ ½log n − o(log n) if I ≠ 0, ≥ c_D log n − o(log n) if I = 0.
* **(E-side)** If I ≥ 1 then x ≥ (H̄ − e_n)/(k + κ) ≥ H̄/(2(s₀ + m₁ + κ)); the closest positive kept point has
  |τ| ≤ H̄ − x and every negative kept point has |τ| ≥ H̄ − 2δ_e + x > H̄ − x + 2ϖ; by (R_ϖ) the deleted null is positive,
  i.e. (exact structure) the smallest kept positive: I_{i+1} = I_i − 1. If I = 0, |I_{i+1}| = 1. FACB's consequences
  (|I_i| ≤ max(|I_{i_e}|, 1), c_I(i) ≤ 2ε_b + o when |I_i| ≥ 2) follow unchanged.
* **(E-add)** (g4): (1 + γ_k)(1 + ε^d)τ̂_l(T ∪ l)² ≤ (1 − γ_{k+1})(|ξ_l − x_T| + 2ϖ)² + o(1) (same factor argument), the quantity FACB bounds by
  h(k + κ + |I|)²/((k + κ)(k + κ + 1)) + o; so G_add ≤ −½log n + o(log n) (I = 0, incl. T = S₀), ≤ −c_D log n + o(log n)
  (|I| = 1), < −0.3 log n (|I| ≥ 2).
* **(E-swap)** (g5): G_sw = O(1/n) − ν log(1 − M_TV̂/ν) with |V̂ − V| = o(1) (X1.4 (g5); X2 at T and T ∖ j ∪ l);
  FACB's bound V ≤ 4h(|I| − 1)₊/(k + κ) + o(log n) for all kept j, outside l gives G_sw ≤ 8ε_b log n + o when |I| ≥ 2 and
  o(log n) when |I| ≤ 1 (if V̂ ≤ 0 then G_sw ≤ O(1/n)), both strictly below G_del(j°).
* Truth moves negative (§X4.6).
**Audit table (R09 recommendation 4): FACB L4.4 bounds reused, their margins, and the perturbation they absorb.**
| bound | FACB margin | replacement error here |
|---|---|---|
| (E-del) best deletion | ≥ ½log n − o (I ≠ 0); ≥ c_D log n − o (I = 0) | (|τ| + ϖ)² − τ² ≤ 3ϖH̄ + ϖ² = o(1); M ≤ ½(1 + C/n); e¹, ε^d, r = O(H̄²/n) |
| (E-side) majority side | gap 2x − 2δ_e ≥ H̄/(s₀ + m₁ + κ) − 2δ_e ≫ 2ϖ | rule slack 2ϖ (R_ϖ) |
| (E-add) additions | −½log n, −c_D log n, < −0.3 log n by |I| | |δ|/(1 − γ) ≤ 2ϖ inside the square: O(ϖH̄) = o(1) |
| (E-swap) swaps | ≤ 8ε_b log n + o vs G_del ≥ (½ − o(1))log n when |I| ≥ 2; o(log n) vs G_del ≥ (c_D − o(1))log n when |I| ≤ 1 (R13 item 1) | |V̂ − V| = O(ϖH̄ + ϖ² + H̄⁶/n + 1/n) = o(1) |
All four margins are of order log n (or ≫ ϖ for (E-side)); all errors are o(1).

So for i ≥ i_e with m_i ≥ 1 the best move is the edge deletion j°_i; after m_{i_e} (≤ m₁ − 1) further moves (total exactly m₀(𝔫), (C2)(iv); R20 item 3) T = S₀, where every
addition has G_add ≤ −½log n + o(log n), every truth deletion and truth-out swap is negative, and there are no null-out
swaps (S₀ has no nulls): S₀ has no improving feasible neighbour. ∎(L)

## X4.6 Truth moves (uniform over all T ⊇ S₀)

Let S₀ ⊆ T, j ∈ S₀, and T′ = T ∖ j or T′ = T ∖ j ∪ l (l ∉ T). Let U := T′ ∪ {j} (= T or T ∪ l) and r := (I − P_{T′})g_j.
Then RSS_{T′} − RSS_U = (rᵀY)²/‖r‖² with rᵀY = β_j‖r‖² + rᵀe (μ − β_jg_j ∈ span X_{T′}). On 𝔊_n: ‖r‖² ≥ λ_min(G^r_U) ≥
(1 − ρ)N/2 (N = n − 3), and |rᵀe|/‖r‖ ≤ ‖P_Ue‖ = ‖e‖(q_U/(1 + q_U))^{1/2} ≤ C√p H̄ (q_U ≤ 2p(1 + ℓ)²H̄²/N, X2.1; R04 item 6). So
RSS_{T′} − RSS_U ≥ (|ϑ|_min√((1 − ρ)N/2) − C√p H̄)² ≥ c_θ n (|β_j| ≥ |ϑ|_min: sign-corrected raw coefficients are
the fixed ϑ; p ≤ n^{A₁}, A₁ < 1). Also RSS_T − RSS_U ≤ ‖P_Ue‖² ≤ Cp H̄² (U ⊇ T, both ⊇ S₀ — for U = T ∪ l). Hence
RSS_{T′} − RSS_T ≥ c_θ n/2. Write Q_{T′} − Q_T = (Q_{T′} − Q_U) − (Q_T − Q_U) (R04 item 6): the first difference is the
ridge partial statistic of truth j at U (U ⊇ S₀, so X1.4 (g2)'s ridge/OLS comparison applies — its coefficient bound
‖b(0)‖ ≤ 1/√c₀ holds for any T, see X5.2 — while the ω² identification is not used for a truth); the second is the
null statistic of l at U (zero for a deletion). Both carry the exact factor n/(n + 1) and have OLS values O(n)
(yᵀy = n − 1), so Q_{T′} − Q_T = [n/(n + 1)](RSS_{T′} − RSS_T)/s² + O(n^{−1/2}) ≥ c′n (s² ∈ [s_min², s_max²], X2.1), and ψ_T ≤ n; the size terms are
≤ log(2p) + ½log(n + 1) + 1 (deletion) or O(1/n) (swap). So the gain is ≤ log(2p) + log n − (n/2)log(1 + c′) < 0. Truths are
never added (S₀ ⊆ T). ∎

## X4.7 Consequences (claim (C2) of STATEMENT v3)

(i)–(iv) of (C2) are Lemma X4 with 𝔫 := N₀ (allowed since the lemma holds simultaneously for all |𝔫| ≤ 15), on 𝔊_n
with P(𝔊_n) → 1 (Lemma X4.0). Caps: for every nonnegative integer cap a the capped search follows the uncapped path for
min(a, m₀) moves and then one further scan (single-search prefix property, FACB L4.5 remark 1); a_n = ℓ_n + |S̃₀| ≥ m₀
on the start event of X5, so LS0 ends at S₀ as a certified search endpoint; with the legacy cap ℓ_n and m₀ ≥ ℓ_n + 2 every
model LS0 scores has ≥ |S*| − ℓ_n − 1 > s₀ elements (FACB L5.2). Ties: the claims are margin statements; the
production tie rule picks among maximisers, and every maximiser is a null deletion satisfying (R_ϖ), which is all that
the induction uses (nondegeneracy only through ND_n, an intersected condition of 𝔊_n, so 𝔊_n ⊆ ND_n; R04 item 2).

**Uniformity in p_n.** As FACB: regimes are assigned per n; n₀ depends only on (ρ, ϑ, σ, s₀, A₁).
