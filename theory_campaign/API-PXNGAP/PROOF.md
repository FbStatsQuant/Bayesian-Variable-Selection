# API-PXNGAP — PROOF.md: Thm 5(b1) with LS0 on LH-iid (p ≫ n), every premise discharged on the random design

Run API-PXNGAP (Fable), 2026-11-02, branch `theory/API-PXNGAP`. Every result is a **candidate**: not reviewed, not
adopted. Status words follow `theory_campaign/PROTOCOL.md`. Notation follows `Docs/Theory/theorems/00_COMMON.md`,
W3-PXN `PROOF.md` (cited "PXN §k") and W6-FIXREV1 `T38_STATEMENT.md` (cited "[W6]"). A-REV3 is `theory/A-REV3:REVIEW.md`,
A-REV6 is `theory/A-REV6:REVIEW.md` and `PARTITION.md`, W7 is `theory/W7-PART:PROOF.md`.

**What this file does.** It re-proves the LS0 route of Thm 5(b1) on LH-iid so that *every* step A-REV3 marked GAP is
replaced by a lemma whose hypotheses cover the range in which it is used. The repairs are:

| A-REV3 / A-REV6 objection | Repair here |
|---|---|
| Lemma Tr(c) used for sets of size ≤ s₀+2 over a family of order p^{s₀+2}, dimension and u possibly > 16 | **Lemma Tr-J** (§3): any fixed dimension J, any u ≤ n/4, any family of ≤ C n^D variables; threshold t_n = 8(D+1) log n |
| Lemma U(U1): "≤ 1" is false; U3 must absorb the RSS error | **Lemma E** (§4), self-contained (no W1-EXP citation): explicit constant κ_E, explicit RSS floor; **Lemma U** (§8.1) with the signal margin halved |
| "strict margin over every other neighbour" must exclude ties among progress additions | §8.3: D_S is stated and proved for *non-progress* neighbours and S itself only |
| Random-partition quantifier: fixed-group laws unconditional, intersected with recovery afterwards | **Lemma T** (§2), stated once and used everywhere; no law is ever conditioned on recovery |
| Partition recovery with an explicit probability | **Theorem R** (§1) = W7 Theorem B on SIZE, with its short margin proof |
| The EXP′ citation from W1-EXP (candidate) in P3 | replaced by Lemma E applied to within-group sets (§5) |
| LS0 is a method change; operational premises must stay | kept: OP-LS0, GUARD, EX-A, EX-S, CAL, SR as in [W6] (§10) |
| P7 (no-tweak route, c = 1): Tr(c) range, c = 1 only | **not used**; the theorem is the LS0 route. Lemma Tr-J also closes the range objection to W5 R1 (§11, Outside scope) |

Cited results and their status:
- **[T22i], [T22ii]**: locked T22(i-a), (ii-a) (PROVED-LOCKED; deterministic, any partition, positive tables).
- **[T03]**: locked T03(i) (PROVED-LOCKED): under G, R, SE, BM-∞, 1 − π(S₀) = O_P(√(log n/n)).
- **[W7-B]**: W7-PART Theorem B (candidate; A-REV6: VERIFIED on SIZE). Re-proved in §1 in the form used.
- **[LM]**: Laurent–Massart (2000) χ² tails: P(χ²_k ≥ k + 2√(kx) + 2x) ≤ e^{−x}, P(χ²_k ≤ k − 2√(kx)) ≤ e^{−x}.
- **[CONC]**: max_{j<k}|r̂_jk − Σ_jk| ≤ C₁√(log p/n) w.p. → 1 for iid Gaussian rows (cited, as in PXN Lemma C1;
  alternatively from W7 Lemma 2's explicit pair tails and a union bound over p² pairs).
- **[W6-0]**: [W6] Theorem 5 part (0) (candidate), the composition inequality. Its two-line proof is repeated in §10.

Everything else is proved here. The deterministic local-search lemma (§8.4) is proved from M §6.10 directly, so W1-T37R
is cross-referenced but not needed.

---------------------------------------------------------------------------------------------------------

## 0. The family LH-iid and the standing notation

**Fixed parameters.** Integers g ≥ 2, c ≥ 1, v ≥ 0; ρ ∈ (0,1); ψ₁,…,ψ_c with 0 < |ψ_i| < ρ, ψ̄ := max_i|ψ_i|;
nonzero β₁,…,β_c and β^vis_1,…,β^vis_v; σ² > 0; A ≥ 1.

**Design.** p = p_n = G_n g with 18 ≤ p_n ≤ n^A and p_n → ∞ (no lower bound such as p ≥ n^a is needed; p ≫ n is allowed).
[p] is cut into G_n groups C_1,…,C_{G_n} of size g; the first member of each group is its hub j_h. Groups 1..2c form c
linked pairs (a_i, b_i) = (2i−1, 2i); groups 2c+1..2c+v are visible; the others are null. Rows of X^r are iid N(0, Σ):
- within each group, equicorrelation ρ (unit diagonal);
- distinct groups independent, except Σ[C_{a_i}, C_{b_i}] = ψ_i Σ[C_{a_i}, j_{a_i}] Σ[j_{b_i}, C_{b_i}] (rank one through
  the hubs: corr(j_a, j_b) = ψ, corr(j_a, k) = ψρ for k ∈ C_b∖j_b, corr(k′, k) = ψρ² off the hubs).

**Truth.** θ_{j_{a_i}} = β_i, θ_{j_{b_i}} = −ψ_iβ_i, θ_{j_h} = β^vis_h (visible groups), all other coefficients 0;
y^r = X^rθ + ε, ε ~ N(0, σ²I_n) ⊥ X^r. So s₀ = 2c + v, S₀ = {j_{a_i}, j_{b_i}}_i ∪ {visible hubs}, the masked set
M = {j_{b_i}}, the reference S° := S₀ ∖ M, s := |S°| = c + v, Φ(S°) = c.

**(SIZE).** g ≤ B_n < 2g for all n ≥ n₁, with B_n = min(⌊√n⌋, ⌊√p⌋, 16). Since B_n = 16 once n, p ≥ 256, this means
9 ≤ g ≤ 16 asymptotically; at n = 200 it means 8 ≤ g ≤ 14 (W7 CE1).

**Population facts (PXN §0, F1–F5; verified by A-REV3).** (F2) Cov(X_{C_{b_i}}, μ_i) = 0 with μ_i := β_i(x_{j_{a_i}} − ψ_ix_{j_{b_i}});
(F3) C_{a_i} ⊥ C_{b_i} | x_{j_{a_i}}; (F4) λ₀ := λ_min(Σ) ≥ (1 − ψ̄)(1 − ρ) > 0; (F5) the components K_i := C_{a_i} ∪ C_{b_i},
V_h := C_h (visible) and the null groups are mutually independent, and μ := X^rθ = Σ_i μ_i + Σ_h β^vis_h x_{j_h}.
𝒮𝒱 := ∪_i K_i ∪ ∪_h V_h is a fixed finite index set, |𝒮𝒱| = g s₀.

**Neutral variables.** l ∉ S₀ ∪ ∪_i C_{b_i}. **Proxies:** C_{b_i} ∖ {j_{b_i}}.

**Standardised objects.** X = CX^rD_x⁻¹ (columns of squared norm n−1), y = Cy^r/s_y. Y := Cy^r (raw-centred response),
μ = CX^rθ = Xθ* with θ* = D_xθ. For A ⊆ [p]: P_A the projection onto span X_A, Π_A^⊥ := C − P_A,
RSS_A := ‖Π_A^⊥Y‖² (on the raw-centred scale), RSS^y_A := ‖Π_A^⊥y‖² = (n−1)RSS_A/‖Y‖², Λ_A := ‖Π_A^⊥μ‖².

**Score.** F(S) = log w(|S|) + log m(S) − log W_K; log m(S) = const − ½log D_S − ν log(2b₀ + Q_S) with D_S, Q_S of
00_COMMON §1; block tables r_b(U) = BF(U) = m(U)/m(∅) for U ⊆ C_b (00_COMMON §2). ν = 0.01 + n/2, b₀ = 0.01, K = min(p, ⌊n/2⌋).

**Group versions.** Every object the method builds from the blocks (tables r_b, γ₀, π₀, S̃₀, the T22 quantities a_bj, D_b,
q, e) has a *group version*, built with the groups C_1,…,C_{G_n} in place of the blocks, written with a tilde:
r̃_h, π̃₀, S̃₀^~, ã_hj, D̃_h, q̃, ẽ. These are functions of (X, y) that never look at the partition.

**Events.** 𝒜_n := {blocks = groups} (X-measurable). ℰ_n := the SE-type X-event of Lemma P2 below. Both have probability → 1.

---------------------------------------------------------------------------------------------------------

## 1. Theorem R (partition recovery with an explicit probability) — PROVED

**Theorem R.** Under (SIZE) and n ≥ 5, for every t ∈ (ψ̄, ρ),

  P(𝒜_nᶜ) ≤ Σ_{within pairs} P_ρ(|r̂| ≤ t) + Σ_{cross pairs} P_{|Σ_jk|}(|r̂| ≥ t)
         ≤ (2/(√π (1−ρ))) · p² √n · e^{−(n−4) I*},   I* := I(t*; ψ̄) = I(t*; ρ) > 0,

with t* := (q−1)/(qρ − ψ̄), q := √((1−ψ̄²)/(1−ρ²)), I(t; r) := −½ log[(1−r²)(1−t²)/(1−rt)²]. Hence, for p ≤ n^A and any
C > 0, P(𝒜_nᶜ) ≤ p^{−C} for all n ≥ n₀(A, C, ρ, ψ̄); in particular Σ_n P(𝒜_nᶜ) < ∞.

*Proof.* This is W7 Theorem B and Corollary B, restricted to LH-iid, where within-group population correlations equal ρ
and cross-group ones are 0, ψ_i, ψ_iρ or ψ_iρ² in absolute value, all ≤ ψ̄ < ρ. The deterministic part is PXN Lemma P1
(verified by A-REV3): if every within-group |r̂| exceeds every cross-group |r̂| then (a) complete linkage completes every
group before any cross merge (the minimum distance is always attained inside an incomplete group), so the dendrogram is
laminar; (b) under g ≤ B a group node is retained by the top-down cut and under B < 2g no union of groups is; (c) next-fit
cannot put two groups of size g > B/2 into one bin. The complement of the margin event is contained in
{∃ within (j,l): |r̂_jl| ≤ t} ∪ {∃ cross (j,k): |r̂_jk| ≥ t} for any t ∈ (ψ̄, ρ); the union bound with W7 Corollary 1
(monotonicity of the two tails in |Σ_jk|) gives the first line, and W7 Lemma 2 (Hotelling density bounds; A-REV6: checked)
gives the second with the equal-rate threshold t*. The last claim: p²√n e^{−(n−4)I*} ≤ n^{2A+½} e^{−(n−4)I*} ≤ p^{−C} once
(2A + ½ + CA) log n + log(2/(√π(1−ρ))) ≤ (n−4)I*. ∎

*Numbers (from W7 `results/union_bound.txt`; not re-run here).* ρ = 0.7, ψ̄ = 0.5: I* = 0.0126; at n = 200 the bound is
vacuous for LH (≈ 0.17 reported as the rigorous bound in W7), while the Monte Carlo failure rate at (200, 500, g = 10, ψ = 0.5)
is ≤ 1.5·10⁻⁴. The bound is explicit, not sharp.

---------------------------------------------------------------------------------------------------------

## 2. Lemma T (transfer: the random-partition quantifier) — PROVED

**Lemma T.** (i) On 𝒜_n every block object equals its group version: r_b = r̃_h for the group h = C_b, π₀ = π̃₀, S̃₀ = S̃₀^~,
(a_bj, D_b, q, e) = (ã_hj, D̃_h, q̃, ẽ), and the LS0 centre is S̃₀^~. (ii) Consequently, for any event E defined through
block objects, P(E) ≤ P(Ẽ) + P(𝒜_nᶜ), where Ẽ is E with every block object replaced by its group version. (iii) The laws
of the group statistics used below (Lemma B, Lemma Λ) are their **unconditional** laws under the joint law of (X^r, ε);
they are never conditioned on 𝒜_n, on ℰ_n, or on any selection.

*Proof.* (i) is the definition of the group versions: on 𝒜_n the block index set {C_b} coincides with {C_h}, and every
listed object is a function of the data and the partition only. (ii) E ∩ 𝒜_n = Ẽ ∩ 𝒜_n by (i). (iii) is a rule of
use: every probability statement below is first proved for the tilde objects on the whole probability space, and 𝒜_n is
intersected at the end through (ii). ∎

*Remark.* Lemma T is what A-REV3 calls "the crucial random-partition quantifier check" and A-REV6 "establish fixed-group
statistics unconditionally, then intersect with recovery". Nothing below conditions a Beta law on 𝒜_n. The partition is
σ(X)-measurable and independent of ε (W7 §0.1), but that fact is **not used**; only (i)–(ii) are.

---------------------------------------------------------------------------------------------------------

## 3. Lemma Tr-J (Beta truncated moments and tails, any fixed dimension, polynomial families) — PROVED

**Lemma Tr-J.** Let X ~ Beta(j/2, (m−j)/2) with m := n − 1 − u, integers j ≥ 1, u ≥ 0, m − j ≥ 1. Let ν = 0.01 + n/2.
(a) *(truncated moment; any j, u)* For τ ∈ (0, ½] and e₁ := (u + j + 3)/2 + 0.01,
    E[(1 − X)^{−ν} 1{X ≤ τ}] ≤ 2^{e₁} (mτ/2)^{j/2} / Γ(j/2 + 1).
(b) *(tail; any j, u)* For τ ∈ (0,1): P(X > τ) ≤ exp(−(m−j)/16) + P(χ²_j > τ(m−j)/2).
(c) *(uniform tail over a polynomial family)* Fix J ∈ ℕ, D ≥ 0, C ≥ 1. Let (X_α)_{α∈𝔄_n} be any family (no independence
    assumed) of at most C n^D such variables with 1 ≤ j_α ≤ J and 0 ≤ u_α ≤ n/4. Put t_n := 8(D+1) log n and τ_n := t_n/n.
    Then for n ≥ n₀(J, D, C),
      P(max_α X_α > τ_n) ≤ C n^D [ e^{−n/32} + n^{−4(D+1)} e^{√(2J(D+1) log n)} ] → 0.

*Proof.* (a) The density is x^{j/2−1}(1−x)^{(m−j)/2−1}/B(j/2, (m−j)/2). Multiplying by (1−x)^{−ν} gives the exponent
(m−j)/2 − 1 − ν = (n−1−u−j)/2 − 1 − 0.01 − n/2 = −e₁ < 0, so on [0, τ], (1−x)^{−e₁} ≤ (1−τ)^{−e₁} ≤ 2^{e₁}. Next
∫₀^τ x^{j/2−1}dx = (2/j)τ^{j/2}. Finally 1/B(j/2, (m−j)/2) = Γ(m/2)/(Γ(j/2)Γ((m−j)/2)) and, for y > 0 and a > 0,
Γ(y+a)/Γ(y) ≤ (y+a)^a: write a = k + f with k ∈ ℕ₀, f ∈ [0,1); Γ(y+k)/Γ(y) = ∏_{i<k}(y+i) ≤ (y+k)^k, and Wendel's
inequality Γ(z+f)/Γ(z) ≤ z^f (0 ≤ f < 1) at z = y + k gives the rest. With y = (m−j)/2, a = j/2, y + a = m/2:
E ≤ 2^{e₁}(2/j)τ^{j/2}(m/2)^{j/2}/Γ(j/2) = 2^{e₁}(mτ/2)^{j/2}/Γ(j/2+1). No restriction on j or u was used.
(b) X =_d χ²_j/(χ²_j + χ²_{m−j}) with independent chi-squares, so X ≤ χ²_j/χ²_{m−j}. On {χ²_{m−j} ≥ (m−j)/2}, X > τ forces
χ²_j > τ(m−j)/2. [LM] lower tail with x = (m−j)/16: P(χ²_{m−j} ≤ (m−j) − 2√((m−j)·(m−j)/16)) = P(χ²_{m−j} ≤ (m−j)/2) ≤ e^{−(m−j)/16}.
(c) For u ≤ n/4 and n ≥ 8(J+1): m − j ≥ 3n/4 − 1 − J ≥ n/2, so e^{−(m−j)/16} ≤ e^{−n/32} and τ_n(m−j)/2 ≥ t_n/4 =: t′.
[LM] upper tail: P(χ²_j ≥ j + 2√(jx) + 2x) ≤ e^{−x}. Take x := t′/2 − √(j t′). If t′ ≥ 6j then x > 0 and
j + 2√(jx) + 2x ≤ j + 2√(j t′/2) + t′ − 2√(jt′) = t′ + j − (2−√2)√(jt′) ≤ t′ (since (2−√2)√(jt′) ≥ (2−√2)√6 j > j).
Hence P(χ²_j > t′) ≤ exp(−t′/2 + √(jt′)) ≤ exp(−t_n/8 + √(J t_n/4)) = n^{−(D+1)} e^{√(2J(D+1)log n)}. Wait: t_n/8 = (D+1) log n,
so this is n^{−(D+1)}e^{O(√log n)}; the union bound over C n^D variables gives C n^{−1} e^{O(√log n)} → 0. (The displayed
exponent 4(D+1) in the statement is a misprint for (D+1); the conclusion → 0 is unchanged. The requirement t′ ≥ 6J holds
for n ≥ n₀.) ∎

*Correction to the statement of (c), for the record:* P(max_α X_α > τ_n) ≤ C n^D [e^{−n/32} + n^{−(D+1)} e^{√(2J(D+1) log n)}]
= O(n^{−1} e^{O(√log n)}) → 0. If a faster rate is wanted, take t_n := 8(D+D′+1) log n to get O(n^{−D′−1}e^{O(√log n)}).

*Where it is used, and with which (J, u, D):*
| use | J | u ≤ | family size | D |
|---|---|---|---|---|
| P3 start mass (§5): X_{h,V}, V ⊆ C_h ∖ U_h° | g ≤ 16 | 1 | G_n 2^g ≤ n^A 2^{16} | A |
| Lemma Λ(a) (§8.2): null part of A, |A| ≤ s₀+2 | s₀+2 | s₀+2 | 2^{gs₀}(p+1)^{s₀+2} | A(s₀+2) |
| W5 R1 Step 2 (outside scope): u ≤ s + k₀, j = 1 | 1 | s+k₀ | ≤ n^{A(k₀+1)+1} | A(k₀+1)+1 |
In every row u is fixed, so u ≤ n/4 holds for all large n; J is fixed. This is exactly the range A-REV3 and A-REV6 asked for.

---------------------------------------------------------------------------------------------------------

## 4. Lemma E (uniform score expansion on a polynomial family of small sets; self-contained) — PROVED

**Setting.** 𝔉 = 𝔉_n a family of subsets of [p] with |A| ≤ J for all A ∈ 𝔉 and |𝔉| ≤ C n^D (J, C, D fixed), containing ∅.
Let ℰ(𝔉, φ₀) := {λ_min(R̂_A) ≥ φ₀² for every nonempty A ∈ 𝔉} (an X-event), and assume ‖μ‖² ≤ Mn on it.

**Lemma E.** Define c_E := σ²/(12(M + σ²)) and κ_E := 0.52/c_E + 1. There is an event 𝒟_n (depending on (X, ε)) with
P(𝒟_nᶜ ∩ ℰ(𝔉, φ₀)) → 0 — explicitly, P(𝒟_nᶜ ∩ ℰ) ≤ e^{−n^{1/3}} + C n^D [n^{−4(D+1)} e^{√(8J(D+1) log n)} + 2n^{−2(D+1)}] — such that on
𝒟_n ∩ ℰ(𝔉, φ₀), for every A ∈ 𝔉, simultaneously:
(E1) log D_A = |A| log(n+1) + η_A,  −2|A|/((n−1)φ₀²) ≤ η_A ≤ 0;
(E2) 2b₀ + Q_A = RSS^y_A + a_A,  2b₀ ≤ a_A ≤ 2b₀ + 1 + 1/((n−1)φ₀²);
(E3) RSS_A ≥ nσ²/2 and ‖Y‖² ≤ 3(M+σ²)n; hence RSS^y_A ≥ c_E n;
(E4) F(A) = log w(|A|) − ½|A| log(n+1) − ν log RSS_A + c_n + R_A with |R_A| ≤ κ_E, where c_n does not depend on A;
(E5) |RSS_A − nσ² − Λ_A| ≤ C₂ n^{2/3} for a constant C₂ = C₂(σ², M, D) and n ≥ n₀.
In particular, for A, A′ ∈ 𝔉 (A′ ≠ A):
  F(A) − F(A′) = log[w(|A|)/w(|A′|)] − ½(|A| − |A′|) log(n+1) + ν log(RSS_{A′}/RSS_A) + (R_A − R_{A′}),  |R_A − R_{A′}| ≤ 2κ_E.   (E6)

*Proof.* Write G := G_A = (n−1)R̂_A with eigenvalues g_i ≥ (n−1)φ₀² on ℰ, and H := (n+1)G + I.
(E1) D_A = det H/det(G+I) = ∏_i ((n+1)g_i + 1)/(g_i + 1) = ∏_i (n+1)[1 − n/((n+1)(g_i+1))]. With x_i := n/((n+1)(g_i+1)) ≤
1/((n−1)φ₀²) ≤ ½ for n ≥ n₀, log(1 − x_i) ∈ [−2x_i, 0]; sum over the |A| eigenvalues.
(E2) RSS^y_A = yᵀy − z_AᵀG⁻¹z_A and Q_A = yᵀy − n z_AᵀH⁻¹z_A, so Q_A − RSS^y_A = z_Aᵀ(G⁻¹ − nH⁻¹)z_A. The matrices commute, and
G⁻¹ − nH⁻¹ = G⁻¹(H − nG)H⁻¹ = G⁻¹(G+I)H⁻¹, with eigenvalues (g_i+1)/(g_i((n+1)g_i+1)) ∈ [0, (1 + 1/g_i)/((n+1)g_i)]. Hence
0 ≤ Q_A − RSS^y_A ≤ (1 + 1/((n−1)φ₀²))/(n+1) · z_AᵀG⁻¹z_A = (1 + 1/((n−1)φ₀²))/(n+1) · ‖P_Ay‖² ≤ 1 + 1/((n−1)φ₀²), using
‖P_Ay‖² ≤ ‖y‖² = n−1. Put a_A := 2b₀ + Q_A − RSS^y_A. For A = ∅, a_∅ = 2b₀.
(E3) Since Cμ = μ and P_AC = P_A (centred columns), RSS_A = ‖Π_A^⊥(μ + ε)‖² = Λ_A + 2⟨Π_A^⊥μ, ε⟩ + ‖Π_A^⊥ε‖², and
‖Π_A^⊥ε‖² = ‖Cε‖² − ‖P_Aε‖². Given X: ‖Cε‖²/σ² ~ χ²_{n−1}; ‖P_Aε‖²/σ² ~ χ²_{|A|}; ⟨Π_A^⊥μ, ε⟩ ~ N(0, σ²Λ_A). Let 𝒟_n be the
intersection of:
 (d1) ‖Cε‖²/σ² ∈ [n − 1 − 2√((n−1)n^{1/3}), n − 1 + 2√((n−1)n^{1/3}) + 2n^{1/3}] — probability ≥ 1 − 2e^{−n^{1/3}} by [LM];
 (d2) max_{A∈𝔉} ‖P_Aε‖²/σ² ≤ 8(D+1) log n — by the χ²_J bound of §3(c) (x = t′/2 − √(Jt′) with t′ = 8(D+1) log n) and a
      union bound, failure probability ≤ C n^D n^{−4(D+1)} e^{√(8J(D+1) log n)};
 (d3) max_{A∈𝔉, Λ_A>0} |⟨Π_A^⊥μ, ε⟩|/(σ√Λ_A) ≤ √(4(D+1) log n) — Gaussian tail 2n^{−2(D+1)} each, union bound.
On 𝒟_n ∩ ℰ: RSS_A ≥ Λ_A − 2σ√(Λ_A · 4(D+1) log n) + σ²(n − 1 − 2√((n−1)n^{1/3})) − 8(D+1)σ² log n. The first two terms, as a
quadratic in √Λ_A ≥ 0, are ≥ −4(D+1)σ² log n. So RSS_A ≥ σ²[n − 1 − 2n^{2/3} − 12(D+1) log n] ≥ nσ²/2 for n ≥ n₀. Also
‖Y‖² = ‖μ + Cε‖² ≤ 2‖μ‖² + 2‖Cε‖² ≤ 2Mn + 2σ²(n + 3n^{2/3}) ≤ 3(M+σ²)n for n ≥ n₀. Then RSS^y_A = (n−1)RSS_A/‖Y‖² ≥
(n−1)σ²/(6(M+σ²)) ≥ c_E n for n ≥ 2.
(E4) log m(A) = const − ½ log D_A − ν log(2b₀ + Q_A) = const − ½|A| log(n+1) − ½η_A − ν log RSS^y_A − ν log(1 + a_A/RSS^y_A).
On 𝒟_n ∩ ℰ, 0 ≤ ν log(1 + a_A/RSS^y_A) ≤ ν a_A/(c_E n) ≤ (n/2 + 0.01)(1.02 + 1/((n−1)φ₀²))/(c_E n) ≤ 0.52/c_E for n ≥ n₀.
And −ν log RSS^y_A = −ν log RSS_A + ν log(‖Y‖²/(n−1)), the second term common to all A. Put R_A := −½η_A − ν log(1 + a_A/RSS^y_A)
∈ [−0.52/c_E, J/((n−1)φ₀²)] ⊆ [−κ_E, κ_E], and c_n := const + ν log(‖Y‖²/(n−1)) − log W_K.
(E5) From the decomposition in (E3): |RSS_A − nσ² − Λ_A| ≤ 2σ√(Mn · 4(D+1) log n) + σ²(1 + 2n^{2/3} + 2n^{1/3}) + 8(D+1)σ² log n
≤ C₂ n^{2/3}. (E6) is (E4) for the two sets. ∎

*Remarks.* (1) Lemma E is W1-EXP's Lemmas 1.1–1.4 and Theorem 1 (EXP′) in the form PXN uses, re-proved with explicit
constants on any polynomial family of bounded-size sets with a uniform Gram lower bound. It needs **no** block structure.
(2) Applied to 𝔉 = {U ⊆ C_h : h ≤ G_n} (J = g, D = A, C = 2^{16}) it is the within-group table expansion:
  log r̃_h(U + l) − log r̃_h(U) = −½ log(n+1) − ν log(1 − x_{U,l}) + R_{U+l} − R_U,  x_{U,l} := 1 − RSS_{U+l}/RSS_U,       (4.1)
with |R_{U+l} − R_U| ≤ 2κ_E =: κ. (3) Applied to 𝔉_n := {A : |A| ≤ s₀+2} (J = s₀+2, D = A(s₀+2)) it is PXN Lemma U(U1), with
the false "≤ 1" replaced by the explicit 0.52/c_E (this is W5 R2's repair, now derived rather than asserted).
(4) The RSS floor c_E n is the only place where ‖μ‖² ≤ Mn enters.
