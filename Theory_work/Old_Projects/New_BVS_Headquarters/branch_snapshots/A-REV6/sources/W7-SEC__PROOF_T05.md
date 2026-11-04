# T05 — Orthogonal threshold and the benchmark gap: statements and proofs (W7-SEC)

Run W7-SEC, 2026-11-02. **Candidate proofs, not reviewed, not adopted.** Notation: `00_COMMON.md`, `T05_A4_orthogonal_threshold.md`.
Status per item is given at its heading.

## 0. Setting and new symbols

**Hypotheses.** G (fixed design, ε ~ N_n(0, σ*²I), σ*² > 0) and ORTH-design: XᵀX = (n−1)I_p (so p ≤ n − 1), columns
centred. S₀ = supp θ*, 1 ≤ s₀ := |S₀| < p, s₀ ≤ K = min(p, ⌊n/2⌋), n ≥ 3. Equal magnitudes and b_n²/σ*² bounded
are used **only** where stated (Theorem T05-L, case c = +∞). No beta-min, no SE.

**New symbols** (all defined from ε and θ*; P₀ is over ε):
- e_j := x_j/√(n−1), j ∈ [p] (orthonormal, ⊥ 1). Complete them to an orthonormal basis e_1..e_p, f_1..f_{n−1−p} of 1^⊥.
- ξ_j := e_jᵀε/σ*, η_i := f_iᵀε/σ*. λ_j := (n−1)θ*_j²/σ*², and T_j := √(n−1)θ*_j/σ* + ξ_j (so T_j ~ N(±√λ_j, 1)).
- R′ := Σ_i η_i² (R′ ≡ 0 if p = n − 1); Ξ := R′ + Σ_{j∉S₀}ξ_j²; d := n − 1 − s₀; M := p − s₀ ≥ 1.
- V_S := R′ + Σ_{j∉S}T_j² + n⁻¹Σ_{j∈S}T_j²; V_tot := V_∅ = R′ + Σ_jT_j²; c_n := 0.02·V_tot/(n−1).
- τ := τ_n = log n + 2 log((2p − s₀)/s₀) (as in the theorem file); τ^{(i)} := log n + 2 log((2p−1−i)/(i+1)), so τ^{(s₀−1)} = τ.
- ν′ := 2ν(1 − 1/n) = (n−1)(n+0.02)/n.
- Global HPM S† (00_COMMON §1). Known-size selector Ŝ_or := the s₀ indices with the largest |z_j|.

Facts used without proof (standard): (F1) Laurent–Massart: for X ~ χ²_D and x > 0, P(X ≤ D − 2√(Dx)) ≤ e^{−x} and
P(X ≥ D + 2√(Dx) + 2x) ≤ e^{−x}. (F2) 2Φ̄(s) ≤ e^{−s²/2} for s ≥ 0 (log 2Φ̄ has derivative −φ/Φ̄ ≤ −s by the
Mills ratio). (F3) Hoeffding's inequality for sums of independent [0, q]-valued variables. (F4) C(M, i) ≤ (eM/i)^i.

---

## 1. Lemma T05-R (exact representation). **PROVED.**

Under G and ORTH-design:
(a) ξ_1, …, ξ_p, η_1, …, η_{n−1−p} are iid N(0,1); hence (ξ_j)_{j∈S₀}, (ξ_j)_{j∉S₀} and R′ ~ χ²_{n−1−p} are
independent, and Ξ ~ χ²_d is independent of (ξ_j)_{j∈S₀}.
(b) D_S = n^{|S|} and Q_S = (n−1)V_S/V_tot for every S ∈ Ω.
(c) F(S) = κ + log ϖ(|S|) − (|S|/2) log n − ν log(c_n + V_S), where κ := log C_n + ν log(V_tot/(n−1)) does not depend on S.
(d) The exact addition log-odds of T05(i) hold: for S of size k < K and j ∉ S,
F(S+j) − F(S) = log[(k+1)/(2p−k−1)] − ½ log n + ν log[(0.02+Q_S)/(0.02+Q_S−z_j²/n)].

*Proof.* (a) (e, f) is an orthonormal family and ε ~ N(0, σ*²I), so the coordinates are iid N(0,1). (b) G_S = (n−1)I_k,
so H_S = ((n+1)(n−1)+1)I = n²I and G_S + I = nI; D_S = n^{2k}/n^k = n^k, and Q_S = yᵀy − n·n⁻²Σ_S z_j². By the model and
00_COMMON §1, Cy^r = Xθ* + Cε (C1 = 0, CX^rβ* = Xθ*). Since e_j, f_i ∈ 1^⊥, e_jᵀC = e_jᵀ and f_iᵀC = f_iᵀ, so
e_jᵀCy^r = (n−1)θ*_j/√(n−1) + e_jᵀε = σ*T_j and f_iᵀCy^r = σ*η_i (f_i ⊥ col X). Hence ‖Cy^r‖² = σ*²V_tot,
s_y² = σ*²V_tot/(n−1), yᵀy = n − 1 and z_j = x_jᵀy = √(n−1)σ*T_j/s_y, so z_j²/n = (n−1)²T_j²/(nV_tot). Therefore
Q_S = (n−1) − (n−1)²Σ_S T_j²/(nV_tot) = ((n−1)/V_tot)[V_tot − (1 − 1/n)Σ_S T_j²] = (n−1)V_S/V_tot.
(c) 0.02 + Q_S = ((n−1)/V_tot)(c_n + V_S); substitute in F = log ϖ + log C_n − ½ log D_S − ν log(2b₀ + Q_S).
(d) w(k+1)/w(k) = C(2p−1,k)/C(2p−1,k+1) = (k+1)/(2p−1−k) and D_{S+j}/D_S = n. ∎ (V_tot > 0 a.s.)

**Corollary T05-R1 (top-k structure). PROVED.** Since V_S = V_tot − (1 − 1/n)Σ_{j∈S}T_j², for each k the maximum of F
over {|S| = k} is attained exactly at the k-subsets with the largest T_j² (a.s. unique). Write top_k for it and
g(k) := F(top_k). Then S† = top_{k̂}, k̂ = the smallest maximiser of g; and **S† = S₀ ⇔ top_{s₀} = S₀ and g(s₀) > g(k)
for all k ≠ s₀** (up to a P₀-null set of ties). (Checked by enumeration: `results/t05_representation_check.txt`.)

---

## 2. Theorem T05-U (finite-n failure bound for the global HPM). **PROVED.**

Under G and ORTH-design (magnitudes arbitrary), for every δ ∈ (0, 1),

  P₀(S† = S₀) ≤ e^{−dδ²/4} + ∏_{j∈S₀} [Φ(√λ_j − t_δ) + Φ̄(√λ_j + t_δ)],   t_δ := √((1−δ)·d·τ/ν′).      (U)

In particular P₀(S† = S₀) ≤ e^{−dδ²/4} + 2Φ(√λ_min − t_δ) (keep one factor; Φ̄(√λ + t) ≤ Φ(√λ − t)).

*Proof.* Fix j ∈ S₀; S₀∖j is feasible. By Lemma T05-R(c), with a := (1 − 1/n)T_j² and V_{S₀∖j} = V_{S₀} + a,
F(S₀) − F(S₀∖j) = log[ϖ(s₀)/ϖ(s₀−1)] − ½ log n + ν log(1 + a/(c_n + V_{S₀})). The prior ratio is s₀/(2p − s₀), so the
first two terms equal −τ/2. Since log(1+x) ≤ x and c_n + V_{S₀} ≥ V_{S₀} ≥ Ξ (drop c_n and n⁻¹Σ_{S₀}T²),
F(S₀) − F(S₀∖j) ≤ ½[ν′T_j²/Ξ − τ]. If S† = S₀ then F(S₀) ≥ F(S₀∖j) for every j ∈ S₀, hence T_j² ≥ τΞ/ν′ for all
j ∈ S₀. On {Ξ ≥ (1−δ)d} this gives T_j² ≥ t_δ² for all j ∈ S₀; these events are independent (Lemma T05-R(a)) with
P(T_j² ≥ t²) = Φ(√λ_j − t) + Φ̄(√λ_j + t). Finally P(Ξ < (1−δ)d) ≤ e^{−dδ²/4} by (F1) with x = dδ²/4. ∎

**Corollary T05-U∞ (failure half of (ii), and the v3 half of (iii)). PROVED.** If √τ_n − √λ_{j₀,n} → ∞ for some j₀ ∈ S₀
(in particular, equal magnitudes with √λ_n − √τ_n → −∞), then P₀(S† = S₀) → 0. More generally, with equal magnitudes
and √λ_n − √τ_n → c ∈ [−∞, ∞), limsup P₀(S† = S₀) ≤ Φ(c)^{s₀}.
*Proof.* Take δ = δ_n = n^{−1/3}: dδ² → ∞ and t_δ = √τ·√((1−δ)d/ν′) = √τ(1 − O(n^{−1/3})) = √τ − o(1), because
τ ≤ log n + 2 log(2n) = O(log n). So Φ(√λ − t_δ) → Φ(c) and Φ̄(√λ + t_δ) ≤ Φ̄(t_δ) → 0. ∎

**Corollary T05-Ŝ (the reported HPM). PROVED (given the code reading of `local_search`, `v3_engine.h:378–418`).**
On the SMC branch, P(Ŝ = S₀ is reported) ≤ (U) + P(the final local search ends with local_limit). On the exact
branch Ŝ = S†.
*Proof.* Suppose the final local search ends with termination "no_improvement" at centre C*. Its centres have strictly
increasing F, its first centre is the HPM of everything scored before it, and every model it scans has F ≤ F(next
centre); so every scored model has F ≤ F(C*). Under ORTH-G distinct models have a.s. distinct F (F is a non-constant
analytic function of the continuous T's on each pair), so Ŝ = C*. Certification means F(C*) ≥ F of every flip of C*,
in particular F(S₀) ≥ F(S₀∖j) for all j if C* = S₀ — the necessary condition used in the proof of (U). ∎

---

## 3. Theorem T05-L (success half of (ii)). **PROVED as a limit statement**; the explicit constants are crude.

Assume G, ORTH-design, equal magnitudes |θ*_j| = b_n on S₀, b_n²/σ*² bounded, and √λ_n − √τ_n → c ∈ (−∞, ∞]. Then
liminf P₀(S† = S₀) ≥ Φ(c)^{s₀}. With Corollary T05-U∞ this proves **T05(ii)**: P₀(S† = S₀) → Φ(c)^{s₀} for every
c ∈ [−∞, ∞] (the case c = −∞ being U∞).

**Events and parameters.** δ := n^{−1/3}; h := √(2 log n); a := log log n; ε := 0.008; β₀ := μ_q − q/2 − 0.02 = 0.05133,
where q = 0.45494 is the median of χ²₁ and μ_q = E min(χ²₁, q) = 0.29879 (`results/t05_constants.txt`).
Write ζ_1, …, ζ_d for the d iid χ²₁ summands of Ξ (the η_i² and the null ξ_j²), ξ²_{(1)} ≥ … ≥ ξ²_{(M)} for the
ordered null squares and W_m := Σ_{i≤m}ξ²_{(i)}.
- E_Ξ := {(1−δ)d ≤ Ξ ≤ (1+δ)d}. P(E_Ξ^c) ≤ e^{−dδ²/4} + e^{−dδ²/16} (F1; for the upper tail take x = dδ²/16, then
  2√(dx) + 2x ≤ dδ).
- E_S := {|ξ_j| ≤ h ∀j ∈ S₀}. P(E_S^c) ≤ s₀/n (F2).
- E_O := {ξ²_{(i)} ≤ 2 log(eM/i) + 2(a + 2 log i)/i for all 1 ≤ i ≤ M}. P(E_O^c) ≤ Σ_i C(M,i)e^{−t_i i/2} ≤ Σ_i e^{−a}/i²
  ≤ 1.65/log n (F2, F4).
- E_B := {for every 0 ≤ m ≤ d/2, the sum of the d − m smallest ζ's is ≥ β₀d}. Proof of the bound: that sum is
  ≥ Σ_i min(ζ_i, q) − mq ≥ Σ_i min(ζ_i, q) − dq/2, and by (F3) P(Σ_i min(ζ_i,q) < d(μ_q − 0.02)) ≤ exp(−2d(0.02)²/q²)
  = e^{−0.003865d}.
- 𝒮 := {|T_j| > t⁺ ∀j ∈ S₀}, t⁺² := (τ + C₀)·V⁺·n(n−0.98)/((n−1)²(n+0.02)), C₀ := 2 log(2s₀),
  V⁺ := (1+δ)d + s₀(√λ_n + h)².

On E_O, W_m ≤ 2m log(e²M/m) + r_m with r_m := 2(a + 2 log m)(1 + log m) (Σ_{i≤m}log(eM/i) ≤ m log(e²M/m) and
Σ_{i≤m}1/i ≤ 1 + log m). Note M ≤ d, and every m = k − s₀ with k ≤ K satisfies m ≤ d/2 (since 2⌊n/2⌋ ≤ n − 1 + s₀).

**Deterministic step.** On E := E_Ξ ∩ E_S ∩ E_O ∩ E_B ∩ 𝒮 and for n ≥ n₀ (conditions N1, C1, C2 below), S† = S₀.
(A) *top_{s₀} = S₀.* On 𝒮, T_j² > t⁺² ≥ τ for j ∈ S₀ [for n ≥ n₀]; on E_O the largest null square is ≤ 2 log(eM) + 2a,
and τ − 2 log(eM) ≥ log n − 2 − 2 log s₀ (because 2p − s₀ ≥ M). (N1): log n > 2 + 2 log s₀ + 2a.
(B) *k < s₀.* For i < s₀ the step top_i → top_{i+1} adds a signal; with A := c_n + V_{top_i} ≤ c_n + V_tot =
V_tot(1 + 0.02/(n−1)) and log(A/(A − x)) ≥ x/A,
g(i+1) − g(i) ≥ ½[ρT²_{(i+1)} − τ^{(i)}], ρ := (n−1)²(n+0.02)/(n(n−0.98)V_tot).
On E_Ξ ∩ E_S, V_tot ≤ V⁺, and τ^{(i)} ≤ τ + C₀ (since (2p−1)/(2p−s₀) ≤ 2). So on 𝒮 every such increment is > 0.
(C) *k > s₀ (all increments negative).* For s₀ ≤ k < K the step adds the m-th largest null, m = k + 1 − s₀:
g(k+1) − g(k) ≤ −log[(2p−1−k)/(k+1)] − ½ log n + ν ξ²_{(m)}/(Ξ − W_m),
because c_n + V_{top_{k+1}} ≥ Ξ − W_m. Also log[(2p−1−k)/(k+1)] ≥ log(p/(s₀+m)) ≥ 0 (k ≤ p − 1).
  (C1) m ≤ εd: Ξ − W_m ≥ (1−δ)d − W̄, W̄ := 2εd log(e²/ε) + r_{⌊εd⌋}; with θ_n := (n+0.02)/((1−δ)d − W̄) and
  log(eM/m) ≤ 1 + log(p/m), log(p/(s₀+m)) ≥ log(p/m) − log(1+s₀), 2 log m/m ≤ 2/e, log(p/m) ≤ log n, the increment is
  < 0 if max(θ_n − 1, 0)·log n + θ_n(1 + a + 2/e) + log(1 + s₀) < ½ log n. Here θ_n → 1/(1 − 2ε log(e²/ε)) = 1.1227.
  (C2) m > εd: Ξ − W_m ≥ β₀d (E_B) and ξ²_{(m)} ≤ 2 log(e/ε) + 2(a + 2 log n)/(εd); the increment is < 0 if
  (n/2 + 0.01)·[2 log(e/ε) + 2(a + 2 log n)/(εd)]/(β₀d) < ½ log n.
N1, C1, C2 are explicit and hold for all large n, since their left sides grow like log log n or stay bounded.
By Corollary T05-R1, (A)–(C) give S† = S₀ (strictly, so the tie rule is irrelevant).

**Probability step.** P₀(S† = S₀) ≥ P(𝒮) − P(E_Ξ^c) − P(E_S^c) − P(E_O^c) − P(E_B^c) for n ≥ n₀, and
P(𝒮) = ∏_{j∈S₀}P(|±√λ_n + ξ| > t⁺) ≥ Φ(√λ_n − t⁺)^{s₀} (t⁺ is deterministic). The four error terms → 0.
It remains to show liminf Φ(√λ_n − t⁺) ≥ Φ(c):
- if λ_n ≤ (log n)²: V⁺/(n−1) = 1 + O(n^{−1/3}) + O(log²n/n), so t⁺ = √(τ + C₀)(1 + O(n^{−1/3})) = √τ + o(1)
  (τ = O(log n)); hence √λ_n − t⁺ → c;
- if λ_n > (log n)² (only possible when c = +∞): b_n²/σ*² ≤ B̄ gives λ_n ≤ (n−1)B̄, so V⁺/(n−1) ≤ C(B̄, s₀) and
  t⁺ ≤ C′√τ = O(√log n) = o(√λ_n); hence √λ_n − t⁺ → ∞. ∎

**Honesty note on constants.** Every constant above is explicit, but the n₀ they imply is useless: on a grid,
N1, C1 and C2 first hold at **log n ≈ 227** for s₀ ∈ {1, 2, 5, 14} (`scripts/t05_constants.py`). The slack is in
(C2) (bottom-sum constant β₀ ≈ 0.05 and the crude quantile bound). The Monte Carlo through Lemma T05-R
(`results/t05_mc.txt`) shows the limit Φ(c)^{s₀} is already accurate to MC error at n = 10³. A sharper n₀ would need a
DKW-type uniform control of null order statistics; not pursued (the remark only needs §2 and §4).

---

## 4. Proposition T05-O (the known-size selector) and Theorem T05-G (the gap). **PROVED.**

**Proposition T05-O.** Under G and ORTH-design, for every x > 0,
  P₀(Ŝ_or ≠ S₀) ≤ e^{−x} + Σ_{j∈S₀} Φ(√(2 log M + 2x) − √λ_j).
*Proof.* |z_j| ∝ |T_j| with a common positive factor (Lemma T05-R), so Ŝ_or = S₀ iff min_{S₀}|T_j| > max_{j∉S₀}|ξ_j|.
With t := √(2 log M + 2x): P(max_{j∉S₀}|ξ_j| ≥ t) ≤ M·2Φ̄(t) ≤ Me^{−t²/2} = e^{−x} (F2), and
P(|T_j| ≤ t) ≤ P(ξ_j ≤ t − √λ_j) = Φ(t − √λ_j). ∎ (Knowledge of σ* is not used: the selector is scale-free.)

**Corollary.** If ω_n := √λ_min − √(2 log M) → ∞ then P₀(Ŝ_or = S₀) → 1: take x = ω_n²/8, so that
√(2 log M + 2x) ≤ √(2 log M) + ω_n/2 and the bound is ≤ e^{−ω_n²/8} + s₀Φ(−ω_n/2).

**Theorem T05-G (= T05(iii)).** Under G, ORTH-design and equal magnitudes, every sequence with
√λ_n − √(2 log M_n) → ∞ and √τ_n − √λ_n → ∞ has P₀(Ŝ_or = S₀) → 1 and P₀(S† = S₀) → 0 (Prop T05-O, Cor T05-U∞;
for the reported HPM, also P(Ŝ = S₀) → 0 whenever P(final local_limit) → 0, Cor T05-Ŝ). Such sequences exist
whenever log n → ∞, because τ_n − 2 log M_n = log n + 2 log((2p − s₀)/(p − s₀)) − 2 log s₀ ≥ log n − 2 log s₀,
so √τ_n − √(2 log M_n) ≥ (log n − 2 log s₀)/(2√τ_n) → ∞ (τ_n ≤ 3 log n + 2 log 2); take √λ_n halfway. E.g. p ≍ n^a,
λ_n = (1−ε)τ_n with 0 < ε < 1/(1+2a).
At p = n^a (a > 0), √τ_n − √(2 log M_n) = [√(1+2a) − √(2a)]√log n + o(1) (`results/t05_mc.txt` part C). **PROVED.**

**Wording correction for the paper remark (important).** The gap is **additive on the amplitude scale √λ**
(equivalently b_n√(n−1)/σ*): about [√(1+2a) − √(2a)]√log n standard errors. On the energy scale λ, or for the minimal
detectable |b_n|, it is a **constant factor**: the HPM needs λ ≳ (1+2a) log n and the oracle λ ≳ 2a log n, a ratio
(1+2a)/(2a) (= 2 at a = ½, 1.5 at a = 1). Both thresholds scale as √(log n / n) in b_n. So "loses a √log n factor" is
wrong if read multiplicatively; it is right only as "an additive √log n in standardised amplitude". The
multiplicative loss is unbounded only when log p = o(log n) (e.g. p fixed: oracle needs λ → ∞, HPM needs λ > log n).

## 5. Reading of the numbers (`results/t05_mc.txt`)

- Threshold: at n = 10³…10⁹, p = ⌈√n⌉, s₀ = 2, c ∈ {−1, 0, 1}: P(S† = S₀) = 0.029/0.238/0.704 (n = 10³) and
  0.025/0.253/0.697 (n = 10⁹), against Φ(c)² = 0.025/0.250/0.708. The bound (U) is 0.061/0.375/0.815 at n = 10³ and
  0.0253/0.2504/0.7083 at n = 10⁹ — it is asymptotically tight.
- Gap at a = ½, λ = 0.7τ: the oracle succeeds 61% → 74% as n goes 10³ → 10⁹; the HPM succeeds 8.0% → 2.0%. The gap
  in amplitude units grows only from 0.6 to 1.05 over six decades of n: the √log n growth is real but very slow.
- Proposition T05-O's explicit bound is loose at small n (its guaranteed success is 0 at n = 10³ and 0.19 at 10⁹,
  vs MC 0.61 and 0.74). It is only used for the limit.
- ORTH forces p ≤ n − 1, so none of this is the n = 200, p ∈ {500, 1000} study design.
