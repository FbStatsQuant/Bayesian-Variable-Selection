# Part 3 — The start: Lemma B, P3′ (start mass), P4 (masking), P5 (eligibility). Conclusions (S) and (E)

## 3.1 Lemma B (exact Beta laws of the within-group statistics)

For a group h let U_h° := S° ∩ C_h ({j_h} for a-groups and visible groups, ∅ otherwise). All sets A, U, V, W below are deterministic.
The laws are unconditional (Lemma T(iii)) and the dimension conditions |U| + |W| ≤ n−2 used in the Haar calculation hold for n ≥ n₀
in (i), (i′) and (iii) because g is fixed.

**Lemma B.**
(i) For nonempty V ⊆ C_h ∖ U_h°: X_{h,V} := 1 − RSS_{U_h°∪V}/RSS_{U_h°} ~ Beta(|V|/2, (n−1−|U_h°|−|V|)/2).
(i′) For U with U_h° ⊆ U ⊆ C_h and a neutral l ∈ C_h ∖ U: x_{U,l} := 1 − RSS_{U+l}/RSS_U ~ Beta(½, (n−2−|U|)/2).
(ii) For A ⊇ S° with A ∖ S° neutral and |A| ≤ n − 3, and a neutral l ∉ A: x_{A,l} := 1 − RSS_{A+l}/RSS_A ~ Beta(½, (n−2−|A|)/2).
 (For arbitrary A ⊇ S° with p ≫ n one can have |A| ≥ n−2, where the displayed law is not a distribution; the Haar calculation below
 requires |U| + |W| ≤ n − 2 in general. Statement (ii) is not used anywhere below.)
(iii) The c columns x^r_{j_{b_i}} and y^r are mutually independent, and (n−1)(r̂²_{j_{b_1},y}, …, r̂²_{j_{b_c},y}) →_d independent χ²_1.

*Proof.* In each case of (i)–(ii) the added columns W have population partial covariance 0 with μ given X_U: (F2) for b-groups
with U = ∅ (it covers every subset, including correlated proxies); (F3) and the weak-union property for a-groups with j_a ∈ U;
x_{j_h} ∈ U for visible groups; independence for null groups; the components are independent by (F5). So the population residual
W^r := X^r_W − X^r_UΓ (Γ the population regression matrix) is Gaussian and independent of (X^r_U, y^r).

*Haar step.* Condition on the conditioning columns. After removal of its regression on them, write the raw added submatrix as
GΣ_W^{1/2}, with G an independent n×|W| matrix of iid standard Gaussians and Σ_W the residual covariance, which is positive
definite even when W contains several members of one group. Let Q be an orthonormal basis of E := 1^⊥ ⊖ span X_U, of dimension
m := n − 1 − |U|. Then QᵀC = Qᵀ and QᵀΠ_U^⊥X_W = (QᵀG)Σ_W^{1/2}D_W^{−1}, where D_W is the column scaling; the right factors are
a.s. invertible (D_W may depend on G without affecting this pathwise equality of spans). Conditionally on the conditioning
columns QᵀG is an m×|W| matrix of iid Gaussians, so span(Π_U^⊥X_W) is a Haar |W|-plane in E, and the conditional law does not
depend on the conditioning values. Given (X_U, y), the vector r := Π_U^⊥Y is fixed, so ‖P_{span}r‖²/‖r‖² ~ Beta(|W|/2, (m − |W|)/2),
which needs m − |W| ≥ 1. For (i): W = V, U = U_h°; for (i′): W = {l}, so the second parameter is (m−1)/2 = (n−2−|U|)/2;
for (ii): W = {l}, U = A.

(iii) The c + 1 Gaussian vectors x^r_{j_{b_1}}, …, x^r_{j_{b_c}}, y^r are uncorrelated (F2, F5), hence independent; given y the unit
vectors Cx_{j_b}/‖·‖ are iid uniform on the sphere of 1^⊥, so each r̂²_{j_{b_i},y} ~ Beta(½, (n−2)/2), independently over i, and
(n−1)r̂² →_d χ²_1 jointly. ∎

## 3.2 Theorem P3′ (near-truth start mass on the reference S°, uniformly over the random design)

**Aggregation quantities (group versions on recovered groups).** For a group h and j ≥ 1,
ã_hj := Σ_{V ⊆ C_h∖U_h°, |V|=j} r̃_h(U_h° ∪ V)/r̃_h(U_h°) (zero for unused j), D̃_h := max_{1≤j≤g}(j! ã_hj)^{1/j},
q̃ := (p−s)^{−1} Σ_{h≤G_n} D̃_h, and ẽ := 2p · max{ r̃_h(U)/r̃_h(U + j_h) : h truth-carrying, U ⊆ C_h ∖ {j_h} }.
On 𝒜_n these equal the aggregation quantities q, e of the cited result T22(i-a) on the actual blocks (Lemma T). Only the s
truth-carrying groups have U_h° ≠ ∅ (then U_h° = {j_h}); since S° meets each recovered group in at most one column, the
general 1/a power of the aggregation formula reduces as written.

**Statement.** On LH-iid: q = O_P(√(log n/n)), e = O_P(p√n e^{−c₆n}) (c₆ > 0 fixed), and, on {q < 1},

  1 − π₀(S°) ≤ (s+1)q/(1−q) + s·e;

since P(q < 1) → 1, 1 − π₀(S°) = O_P(√(log n/n)). Explicitly, let
𝒢_n := 𝒜_n ∩ ℰ♯_n ∩ 𝒟_start ∩ {X_{h,V} ≤ τ_{n,A} for all h ≤ G_n and nonempty V ⊆ C_h∖U_h°}, τ_{n,A} = t_{n,A}/n, t_{n,A} = 8(A+1) log n.
Then P(𝒢_nᶜ) ≤ P(𝒜_nᶜ) + P(ℰ♯_nᶜ) + P(𝒟_startᶜ ∩ ℰ♯_n) + P(max X_{h,V} > τ_{n,A}) → 0 (the partition, correlation, Lemma E and Tr-J contributions have the displayed explicit bounds — Theorem R or (R′),
[CONC′], Lemma E, Lemma Tr-J(c) with D = A; the remaining finitely many signal-energy and sample-scale contributions vanish
by Lemma 2.2's SLLN argument), and there are constants C_q (C_q ∝ C_e g e^{2κ_E}√(A+1)) and n₀ with
E[q̃ 1_{𝒢_n}] ≤ C_q √(log n/n), and P(q > x) ≤ C_q√(log n/n)/x + P(𝒢_nᶜ) for every x > 0.

*Proof.* Work with the group versions (Lemma T). Apply Lemma E to 𝔉_start (J = g, D = A, C = 2^{16}) on ℰ♯_n ∩ 𝒟_start.
For V = {l₁,…,l_j} ⊆ C_h ∖ U_h°, telescoping (1.1) along U_h° ⊂ U_h° + l₁ ⊂ … ⊂ U_h° ∪ V gives

  r̃_h(U_h° ∪ V)/r̃_h(U_h°) = (n+1)^{−j/2}(1 − X_{h,V})^{−ν} e^{R_{U°∪V} − R_{U°}} ≤ e^{2κ_E}(n+1)^{−j/2}(1 − X_{h,V})^{−ν},     (3.1)

because the (1 − x) factors multiply to RSS_{U°∪V}/RSS_{U°} = 1 − X_{h,V} and the remainders telescope to a single difference
bounded by 2κ_E.

*Truncation.* The family {X_{h,V}} (nonempty V only) has ≤ G_n 2^g ≤ 2^{16}n^A members, each Beta(j/2, (m−j)/2) with j ≤ g ≤ 16,
u = |U_h°| ≤ 1 (Lemma B(i)); Lemma Tr-J(c) with J = 16, D = A gives P(max X_{h,V} > τ_{n,A}) → 0.

*Moment.* By (3.1), ã_hj 1_{𝒢_n} ≤ e^{2κ_E}(n+1)^{−j/2} Σ_{|V|=j}(1 − X_{h,V})^{−ν}1{X_{h,V} ≤ τ_{n,A}}. By Lemma Tr-J(a) (u ≤ 1, m ≤ n−1,
mτ_{n,A} ≤ t_{n,A}), with C_e := 2^{(1+16+3)/2+0.01} ≤ 2^{10.01}:

  E[ã_hj 1_{𝒢_n}] ≤ e^{2κ_E}(n+1)^{−j/2} C(g, j) C_e (t_{n,A}/2)^{j/2}/Γ(j/2+1).

Since j! C(g, j) ≤ g^j and Γ(j/2+1) ≥ 0.88: E[j! ã_hj 1_{𝒢_n}] ≤ 1.14 C_e (gξ_n)^j with ξ_n := e^{2κ_E}√(t_{n,A}/(2(n+1))) (the factor
e^{2κ_E/j} ≤ e^{2κ_E} is absorbed). Jensen for the concave x ↦ x^{1/j}: E[(j!ã_hj)^{1/j}1_{𝒢_n}] ≤ (1.14C_e)^{1/j}gξ_n ≤ 1.14C_e gξ_n.
As D̃_h = max_j (j!ã_hj)^{1/j} ≤ Σ_{j≤g}(j!ã_hj)^{1/j}: E[D̃_h1_{𝒢_n}] ≤ 1.14C_e g²ξ_n, and q̃ = (p−s)⁻¹Σ_h D̃_h over G_n = p/g
groups gives E[q̃1_{𝒢_n}] ≤ 1.14C_e gξ_n p/(p−s) ≤ 2.3C_e g ξ_n =: C_q√(log n/n)·(1+o(1)). Markov gives the tail (q = q̃ on 𝒜_n).

*Deletion quantity.* The family in ẽ is fixed and finite. By (1.1), log[r̃_h(U + j_h)/r̃_h(U)] ≥ −½ log(n+1) − 2κ_E + ν x_{U,j_h}
(−log(1−x) ≥ x). By the SLLN (finitely many columns), x_{U,j_h} → x^pop(h, U) a.s., the population squared partial correlation of y
and x_{j_h} given X_U, which is positive: for an a-group Cov(x_{j_a}, μ | X_U) = β(1−ψ²)Var(x_{j_a}|X_U) ≠ 0 (the rank-one hub structure
gives E[x_{j_b}|X_{C_a}] = ψx_{j_a}, so Cov(x_{j_a}, y | X_U) = β(1−ψ²)Var(x_{j_a}|X_U); the other signal components and the noise contribute zero covariance), for a visible group β_h Var(x_{j_h}|X_U) ≠ 0, and
Var(x_{j_h}|X_U) ≥ λ₀. With x₀ := ½ min_{h,U} x^pop > 0, w.p. → 1, on ℰ♯_n ∩ 𝒟_start,

  ẽ ≤ 2p√(n+1) e^{2κ_E} e^{−νx₀};  put c₆ := x₀/2

(ν ≥ n/2). Since p ≤ n^A, p√(n+1)e^{−c₆n} = o(√(log n/n)).

*Conclusion.* On 𝒜_n, (q, e) = (q̃, ẽ) (Lemma T). By the tail bound with x = ½, P(q ≥ 1) ≤ 2C_q√(log n/n) + P(𝒢_nᶜ) → 0. The cited result
T22(i-a) (deterministic, for any partition and positive tables and every S° ∈ Ω) gives, on {q < 1}: 1 − π₀(S°) ≤ (s+1)q/(1−q) + se.
On {q ≤ ½} this is ≤ 2(s+1)q + se = O_P(√(log n/n)). ∎

*Remark.* No NL_η, VIS, zero-leakage or exact-Gram hypothesis is used; the Beta law of Lemma B replaces them. The result is an
upper bound; no matching lower bound is claimed (and for slowly growing p the rate √(log p/n) is attainable).

## 3.3 Theorem P4 (masking: π₀(S₀) → 0 at the CL(L) rate)

**P4.** On LH-iid, Mstat_n := log π₀(S₀) + c log p + (c/2) log n →_d Σ_{i=1}^c log((s+i)/2) + ½χ²_c; hence
π₀(S₀) = p^{−c}n^{−c/2}e^{O_P(1)} → 0, and VIS at S₀ fails (the block of j_{b_i} carries no signal given nothing): the family is
genuinely in the masked regime, while π₀(S°) → 1.

*Proof.* On 𝒜_n (Lemma T), the cited result T22(ii-a) (S₀ ∈ Ω eventually) gives
π₀(S₀) = π₀(S°)[w(s+c)/w(s)]∏_{i≤c} r_{b_i}({j_{b_i}}) exactly (S₀ and S° differ only in the b-blocks, where S° is empty).
w(k+1)/w(k) = (k+1)/(2p−1−k) gives log[w(s+c)/w(s)] + c log p → Σ_i log((s+i)/2). For a single column U = {j}: G = n−1, H = n²,
det(G+1) = n, D = n, z = (n−1)r̂_{j,y}, Q = (n−1) − (n−1)²r̂²/n, so

  log r({j}) + ½ log n = −ν log(1 − κ_n r̂²) with κ_n := (n−1)²/(n(n−0.98)) → 1.

By Lemma B(iii), (n−1)r̂²_i →_d independent χ²_1, so −ν log(1 − κ_n r̂_i²) →_d ½χ²_{1,i} jointly (ν/(n−1) → ½, κ_n → 1, and the
Taylor remainder is O_P(1/n)); log π₀(S°) → 0 in probability by P3′; Slutsky, and the transfer from groups to blocks on 𝒜_n
(Lemma T, P(𝒜_nᶜ) → 0). ∎

(On partition recovery, put `V_n := (n−1)Σ_i r̂²_{j_{b_i},y}` and `d_p := Σ_{i=1}^c log[2p/(2p−s−i)] = O(1/p)`. The exact singleton expansion gives `Mstat_n = Σ_i log((s+i)/2) + V_n/2 + log π₀(S°) + d_p + O_P(1/n)`. Consequently its remainder relative to this finite-n statistic is `O_P(√(log n/n) + 1/p)`. All terms beyond `V_n/2` vanish, which suffices for the stated limit law; no rate of convergence to the limiting chi-square law is asserted. [R39 #1: the baseline remark's O_P(√(log n/n)) alone fails for slowly growing p.])

**Conclusion (S).** P3′ and P4 together are (S): 1 − π₀(S°) = O_P(√(log n/n)) with the explicit moment and tail bounds of §3.2, and
the limit law of Mstat_n above.

## 3.4 Theorem P5 (eligibility of the LS0 centre) — conclusion (E)

**P5.** P(S̃₀ = S°) → 1, where S̃₀ = argmax π₀ (exact max-plus convolution, deterministic tie rule). Hence the LS0 centre S̃₀ equals
S° with Φ(S̃₀) = c, S̃₀ ⊆ S₀ with no extras, w.p. → 1.

*Proof.* On {π₀(S°) > ½} no other model has mass ≥ ½, so S° is the unique global maximiser of π₀. Exact max-plus maximisation
and backtracking then return S° (a second optimal configuration would be a second global mode, impossible on this event).
This **bypasses** the tie-DP invariant of the start (registry item OB03, "N3") on this event; it does not prove that invariant.
Premise retained: EX-A, including exact DP arithmetic; floating-point exactness is not established by the probability argument.
Finally P(π₀(S°) > ½) → 1 by P3′. ∎

(In exact arithmetic the DP computes, for each size k, the maximum sum of block log-ratios, then adds the size prior and
maximises over k; backtracking recovers an optimum — implementation: `CODE/cpp/v3_start.h:183-240`.)
