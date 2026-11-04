# W5-VPGD — the constant in (★): a sharpening, a better lower-bound family, and what is intrinsic

Notation: W3-PGD PROOF §0–§3. λ := log p ≤ A log n. c_* = ½ log n + log p − O(1) is the one-step superset
penalty, so in units of log p the penalty per extra is κ := 1 + 1/(2A) (asymptotically). For a null l and
T ⊆ S₀ᶜ∖{l}, Z_{S₀∪T,l} is the standardised noise along the residual of x_l on X_{S₀∪T}. LD♭(d; B′, ρ*) is as in
W3-PGD §3. **New symbols:** for k ≥ 0,

  ρ*_k := sup over nulls l and T ⊆ S₀ᶜ∖{l} with |T| ≤ k of ρ(l, T∖𝔑(l) | S₀ ∪ (T ∩ 𝔑(l)))   (so ρ*_d is W3's ρ*),
  τ_k := (1 + ρ*_k √k)/√(1 − ρ*_k²)   (τ_0 = 1; W3's τ is τ_d).

Everything below is a **candidate**; statuses are the protocol's.

---------------------------------------------------------------------------------------------------------

## 1. Where the slack in (★) comes from

W3-PGD's Lemma S needs, at every superset state S = S₀ ∪ P (1 ≤ |P| ≤ d), three noise events:
(α) F(S − e₀) > F(S), statistic Z_{S₀∪(P−e₀), e₀}, so |T| = |P| − 1 ≤ d − 1;
(γ) F(S − e′) > F(S − e′ + l), statistic Z_{S₀∪(P−e′), l}, so |T| ≤ d − 1;
(β) F(S − e₀) > F(S + l), statistic ½(Z²_{S₀∪(P−e₀),e₀} + Z²_{S₀∪P,l}), one |T| ≤ d − 1 and one |T| ≤ d term,
against a **double** penalty 2c_*.
W3's (★) bounds every statistic by the |T| ≤ d worst case τ_d and asks τ_d² < κ for all three. Two things are lost:
1. (α) and (γ) only involve |T| ≤ d − 1, and (β) has twice the penalty budget. This loss is removable (§2).
2. The local/far inequality |Z_{S₀∪T,l}| ≤ (|Z_{A,l}| + ρ‖P_Ṽe‖/σ)/√(1−ρ²) treats the local statistic and the far noise
   as if both could be extreme with opposite signs. They are positively correlated (Corr(Z_{A,l}, ⟨v̂, e⟩/σ) = ρ, with
   v̂ the unit vector along P_Ṽx̌_l), so this costs something. §4 shows the cost is second order in ρ: it is intrinsic to
   the method, but it does not change the leading constant.
3. The comparison family. C-LD (one equicorrelated block of all nulls) is **not** the extremal design. The common
   factor is then a single N(0,1) and cannot help. With many large groups, the best group's factor is itself extreme,
   and the threshold drops from r > 1/(2A) to r > 1/(4A − 1) (Prop. G, §3). The "factor 3–4" in W3-PGD compares (★) with
   the wrong family.

---------------------------------------------------------------------------------------------------------

## 2. Proposition S′ (sharpened superset lemma). Status: PROVED (candidate)

**Statement.** Assume G, R, SE_λ(d+1), BM-∞, d ≥ 2, and LD♭(d; B′, ρ*) with B′ fixed, and let ρ*_{d−1} ≤ ρ*_d be as
above. Suppose

 (★′a) (τ_{d−1}² − 1)·A < ½, and
 (★′b) (τ_{d−1}² + τ_d² − 2)·A < 1, **or** the counting condition (|𝒟| + 1)^d ≤ p·n^{1−ε} for a fixed ε > 0.

Then the conclusion of W3-PGD Lemma S holds: w.p. → 1, (L) holds and D_S holds at every S = S₀ ∪ P, P ⊆ 𝒟,
1 ≤ |P| ≤ d. Consequently Theorem W holds with (H3) replaced by (★′a) ∧ (★′b) under LD♭.

(★) ⇒ (★′): τ_k is increasing in ρ*_k and in k, and ρ*_{d−1} ≤ ρ*_d, so τ_{d−1} ≤ τ_d. Then (★) gives
(τ_{d−1}² − 1)A ≤ (τ_d² − 1)A < ½ and (τ_{d−1}² + τ_d² − 2)A < 1. So (★′) is a strictly weaker hypothesis.

**Proof.** (T) and (L′) are unchanged (W3-PGD Lemma S; they use no LD). Fix the events of W3's (H3) proof, but with
two maximal statistics:

  V_k := max ‖P_{Ṽ(L,F)}e‖/σ over disjoint null sets L, F with |L| + |F| ≤ k (subspaces of dimension ≤ |F| ≤ k),
  Z^loc := max |Z_{S₀∪L,l}| over nulls l and L ⊆ 𝔑(l), |L| ≤ d.

By Lemma Q, w.p. ≥ 1 − 3e^{−ω_n}: (Z^loc)² ≤ 2λ + 2B′ log 2 + 2ω_n and V_k² ≤ 2kλ + o(log n) for k = d − 1, d (there
are ≤ (2p+1)^k subspaces of dimension ≤ k; t = k log(2p+1) + ω_n in Laurent–Massart). By Lemma LD and monotonicity of
(a + ρb)/√(1−ρ²) in ρ, every Z_{S₀∪T,l} with |T| ≤ k satisfies

  ½ Z²_{S₀∪T,l} ≤ ½(Z^loc + ρ*_k V_k)²/(1 − ρ*_k²) ≤ τ_k² λ + o(log n)    (k = d−1, d),

uniformly in (T, l), because |F| ≤ |T| ≤ k and ρ(l, F | A) ≤ ρ*_k.
(α), (γ): the statistics have |T| ≤ d − 1, and Lemma U gives
  F(bigger) − F(smaller) ≤ τ_{d−1}²λ − c_* + o(log n) = (τ_{d−1}² − 1)λ − ½ log n + o(log n)
                        ≤ [(τ_{d−1}² − 1)A − ½] log n + o(log n) → −∞    by (★′a).
(β), LD branch: W(S + l | S − e₀) = Z²_{S−e₀,e₀} + Z²_{S,l}, with |T| = |P| − 1 ≤ d − 1 and |T| = |P| ≤ d. Lemma U with
two steps of penalty gives
  F(S + l) − F(S − e₀) ≤ (τ_{d−1}² + τ_d²)λ − 2c_* + o(log n) = [(τ_{d−1}² + τ_d² − 2)λ − log n] + o(log n) → −∞    by (★′b).
(β), counting branch: W(S + l | S − e₀) is χ²₂ (tail e^{−x/2}) over ≤ (|𝒟|+1)^d p pairs (P, l), so w.p. ≥ 1 − e^{−ω_n}
½W ≤ d log(|𝒟|+1) + λ + ω_n, and F(S + l) − F(S − e₀) ≤ d log(|𝒟|+1) + λ + ω_n − 2c_* + O(1)
≤ d log(|𝒟|+1) − λ − log n + ω_n + O(1) ≤ −ε log n + ω_n + O(1) → −∞.
All thresholds are O(log n), so Lemma U applies. The case log p = o(log n) is trivial as in W3. ∎

**Remark (d = 1).** For d = 1, (★′a) is empty (τ_0 = 1) and the counting branch of (★′b) reads (|𝒟| + 1) ≤ p·n^{1−ε},
which always holds. So Prop. S′ contains W3's (H1). It also contains (H2), whose (β) step is the counting branch.

---------------------------------------------------------------------------------------------------------

## 3. Proposition G (grouped equicorrelated nulls). Status: COUNTEREXAMPLE (explicit construction + proof)

**Construction (A = 1, exact Gram).** N = n − 1. Fix r ∈ (0, 1) and β ∈ (0, 1). Let k := ⌊N^β⌋ and
G := ⌊(N − 1)/(k + 1)⌋. Take orthonormal v₀, f_1, …, f_G, h_{g,i} (g ≤ G, i ≤ k) in ℝ^N (1 + G + Gk ≤ N). Truth
x₁ = √N v₀ (s₀ = 1, θ₁ = θ ≠ 0 fixed). Nulls x_{g,i} = √N(√r f_g + √(1−r) h_{g,i}). So p = 1 + Gk, with N/2 ≤ p ≤ N
for large N, i.e. A = 1.

**Hypotheses that hold.** G; R (p ≤ n); SE_λ(j) for every j with φ₀² = 1 − r; BM-∞ (θ fixed); PGD(1) and
GERC (ERC ≡ 0), because every null is orthogonal to x₁; TRC vacuous. For any fixed B′ and any neighbour map,
ρ*_k = r√(k/(1 + (k−1)r)) for k ≥ 1 (groups have size → ∞, so a fixed list cannot absorb the k mates). In particular
ρ*_1 = r.

**Claim.** If (1 + 3r)/(1 + r) > 3/2, i.e. **r > 1/3**, then with β = β* := (1+r)²/(1+3r) ∈ (0,1),
P₀(TD′_P(R_{0,2}) fails) → 1. (C-LD needs r > 1/2.) More generally, for d ≥ 2 and B the d − 1 most negative members of
the best group, the same argument gives failure of TD′_P(R_{0,d}) as soon as
  t²_{d−1}(r) := [√r(1 − (d−1)γ)]²/v + [√(1−r)(1 + (d−1)γ)]²/v > 3/2,   γ = r/(1 + (d−2)r), v = 1 − (d−1)γr,
i.e. r > 0.153 for d = 3 and r > 0.100 for d = 4 (`results/star_thresholds.txt`).

**Proof (d = 2).** Put F_g := ⟨f_g, e⟩/σ and H_{g,i} := ⟨h_{g,i}, e⟩/σ, all iid N(0,1). Then
Z_{S₀,(g,i)} = √r F_g + √(1−r) H_{g,i}. For b, l in the same group, the residual of x̂_l on {x₁, x̂_b} is x̂_l − r x̂_b, and

  t := Z_{S₀+b, l} = (Z_l − rZ_b)/√(1−r²) = c_F F_g + (H_l − rH_b)/√(1+r),   c_F := √(r(1−r)/(1+r)).

Let g* := argmax_g F_g, l := argmax_i H_{g*,i}, b := argmin_i H_{g*,i}. The H's are independent of the F's, so by the
standard maxima of iid normals (as in the C-LD proof), w.p. → 1:
F_{g*} ≥ √(2 log G) − ω_n/√(log G), H_l ≥ √(2 log k) − ω_n/√(log k), H_b ≤ −√(2 log k) + ω_n/√(log k).
With log G = (1−β) log N + O(1) and log k = β log N + O(1),

  t ≥ [c_F √(1−β) + √(1+r) √β] √(2 log N) − O(ω_n),

because (H_l − rH_b)/√(1+r) ≥ (1 + r)√(2 log k)/√(1+r) − O(ω_n/√log k). By Cauchy–Schwarz the bracket is maximal at
β = β*, where it equals √(c_F² + 1 + r) = √((1+3r)/(1+r)). So t² ≥ ((1+3r)/(1+r))·2 log N − O(ω_n √log N).

Let a := argmin |Z_{S₀,x}| over nulls x outside group g* (w.p. → 1 |Z_{S₀,a}| ≤ 1), and S := S₀ ∪ {a, b} ∈ R_{0,2}.
The swap a → l (null → null, neutral) gives S − a + l = S₀ + b + l. By the lower direction of Lemma R
(RSS_{S₀+b+l} = RSS_{S₀+b} − σ²t², −ν log(1−x) ≥ νx, ν ≥ N/2, RSS_{S₀+b} ≤ ‖e‖² ≤ Nσ²(1 + δ_n)):

  F(S₀+b+l) − F(S₀+b) ≥ ½t²/(1+δ_n) − c_{s₀+1} − 2C₀ ≥ [(1+3r)/(1+r) − 3/2] log N − o(log N) → +∞,

using c_{s₀+1} = ½ log(n+1) + log((2p−3)/3) = (3/2) log N + O(1) (p ≍ N). Also, by Lemma U for S₀ ⊆ S₀ + a and the lower
direction of Lemma R for S₀ ⊆ S₀ + b,
  F(S₀+a) − F(S₀+b) ≤ ½Z²_{S₀,a}(1+δ′_n) + 4C₀ + 1 = O(1).
Hence F(S − a + l) > max{F(S − a), F(S − b)} = max{F(S₀+b), F(S₀+a)} w.p. → 1. Both progress neighbours of S (the two
deletions) lose to a non-progress neighbour, so D_S fails and TD′_P(R_{0,2}) fails. |S| = 3 ≤ K. ∎

For d ≥ 3 replace b by the set B of the d − 1 smallest H's in g* (each ≤ −√(2 log k) + o(√log k)), use
Z_{S₀∪B,l} = (Z_l − γΣ_{b∈B}Z_b)/√v, take S := S₀ ∪ B ∪ {a} and the swap a → l. The extra comparisons F(S − e) for e ∈ B
are F(S₀ ∪ (B−e) ∪ a) ≤ F(S₀ ∪ B) + O(1) (swap a tiny-Z orthogonal null for e). Status for d ≥ 3: PROOF SKETCH (the
order-statistics step for d − 1 simultaneous minima is standard but not written out).

**Is the configuration optimal within the family?** A large-deviation counting relaxation (`scripts/star_thresholds.py`,
`t2_relaxed`, heuristic) returns the same value (1+3r)/(1+r) to 4 decimals for d = 2. So within this family the bound is
the right one. Whether another family does worse is OPEN.

**The (β) comparator is not the failure mode here.** The same relaxation for the (β) event gives a rate of at most 2.30
(failure needs > 3) for every r ≤ 0.8 (`scripts/beta_rate.py`, `results/beta_rate.txt`). In this family the binding
failure is the (γ)-type swap.

---------------------------------------------------------------------------------------------------------

## 4. Comparison, and what is intrinsic

Thresholds in r for the grouped family at A = 1 (d = 2; `results/star_thresholds.txt`):

| condition | certifies r < | fails for r > |
|---|---|---|
| W3's (★) (ρ*_2 = r√(2/(1+r))) | 0.111 | — |
| (★′a) alone | 0.200 | — |
| (★′) = (★′a) ∧ (★′b) | 0.143 | — |
| C-LD (one block) | — | 0.500 |
| **Prop. G (grouped)** | — | **0.333** |

So the gap between what is proved and what is known to fail, at A = 1 and d = 2, goes from 0.5/0.111 = 4.5 (W3's
comparison) to 0.333/0.143 = 2.3. If (β) can be removed (see the CONJECTURE below), it is 0.333/0.2 = 1.67.

**Intrinsic part (PROVED as a computation).** For the (α)/(γ) statistic with |T| = d − 1, the local/far bound is
τ_{d−1}² = 1 + 2(d−1)r + O(r²) on this family, and the configuration of Prop. G achieves
t²_{d−1}(r) = 1 + 2(d−1)r + O(r²). The slopes agree (2.000, 4.000, 6.000 for d = 2, 3, 4 numerically). For d = 2 exactly:
bound (1+r)/(1−r), achieved (1+3r)/(1+r); the excesses are 2r/(1−r) and 2r/(1+r), ratio (1+r)/(1−r).
The remaining loss is the positive correlation ρ between the local statistic and the far noise direction, which the
local/far inequality ignores. It is **intrinsic to the local/far decomposition** (the inequality is used with only the
scalars ρ*_k, d and A), and it is **second order**: the certified and failing thresholds of (★′a) are 1/(4A+1) and
1/(4A−1) for d = 2, so their ratio → 1 as A → ∞ (1.67, 1.29, 1.13, 1.06 at A = 1, 2, 4, 8). Caveat: for A > 1 the
grouped family needs p > n, which an exact orthonormal construction cannot give; the A > 1 column is a formula
comparison (CONJECTURE that a random-design version fails at the same r), not a proved counterexample.

**CONJECTURE (β-removal).** Under LD♭, (★′a) alone suffices for Lemma S. Evidence: in the grouped family the (β) rate
stays ≤ 2.3 < 3 at A = 1 (heuristic relaxation). The obstacle is that the local/far method bounds the two summands of
the (β) statistic by their separate worst cases.

**Answer to the task's question.** (★) can be sharpened, and the sharpening is proved (Prop. S′). The remaining gap to
the best known failing family is 2.3× at A = 1, d = 2. Within it, the factor (1+r)/(1−r) vs (1+3r)/(1+r) on the
(α)/(γ) statistic is intrinsic to the local/far decomposition but vanishes to first order. The rest sits in the (β)
step and is probably an artefact (CONJECTURE). The "factor 3–4 from C-LD" in W3-PGD overstated the gap: C-LD is not
extremal (Prop. G fails at 1/3, not 1/2). It also understated how loose (★) itself is (4.5× against C-LD at A = 1).
