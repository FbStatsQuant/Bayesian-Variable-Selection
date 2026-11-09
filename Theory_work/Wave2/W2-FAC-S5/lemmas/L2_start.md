# L2 — The start mode is S* = [p] ∖ N₀ (claim (C1)) on block compound symmetry

Status: **PROVED-CHECKED** (Tier 1: lemma checks, mid-point CONTINUE, sweep fixed, council round 2 passed — R09 Sol 8.8, R10 Opus 8.8, all gates PASS); lemma check R02 (Codex Sol high): VERIFIED-WITH-AMENDMENTS, applied.
Falsification numerics: numerics/s4_start.py → S4_out.txt (exact-Gram BCS: S5 and (q, ρ_b, ρ_w) = (3, .2, .6); the FACB
**Python numerical replica** of the partition and start-mode DP, `W2-FAC-B/numerics/bvs_core.py`, whose DP/backtracking ties
are resolved within 10⁻¹² and complete-linkage correlation ties within 10⁻¹⁰ — not the production routine; layouts with
N₀ = ∅ and N₀ ≠ ∅; R06 item 12); FACB
numerics/N1_summary.md (S5 rows: S̃₀ = [p] in all sampled S5 data sets at n = 10⁸).

Setting: STATEMENT §1–2 including (FS-BCS) and (P) (p ≤ ⌊n/2⌋, so K = p); L1 (Υ_n = I). Blocks C_b, |C_b| ≤ 16, any
deterministic partition. N₀ := ⋃{C_b ∖ S₀ : S₀ ⊆ C_b}. The proof is FACB L2 with the CS computations replaced by the
general Schur-complement form of L1.4 and the BCS facts of L1.2.

## L2.1 Increments of the block tables
For U ⊆ C_b, |U| = u ≤ 15, l ∈ C_b ∖ U (L1.4 applied to U ∪ {l} with R = U; ψ_U := 0.02 + Q_U):
  log r_b(U ∪ l) − log r_b(U) = −½[L(U ∪ l) − L(U)] − ν log(1 − n t̃_{U,l}²/(aψ_U)),
  t̃_{U,l} = (z_l − β̃ᵀz_U)/ṽ^{1/2} = ((n − 1)/s)σ_{U,l}/ṽ^{1/2} + (σ√(n − 1)/s)(g_l − β̃ᵀg_U)/ṽ^{1/2},
with σ_{U,l} := (Σθ*)_l − β̃ᵀ(Σθ*)_U, β̃ = Σ̃_UU⁻¹Σ_Ul, ṽ ∈ [d, 1 + 1/a] (ṽ ≥ λ_min(Σ̃) ≥ d).
**Population part.** σ_{U,l} = c(U, l) + O(a⁻¹), where c(U, l) := Cov(x_l, μ | x_U) = Σ_{i∈S₀} ϑ_i(Σ_li − Σ_lUΣ_UU⁻¹Σ_Ui)
(Σ-scale; the O(a⁻¹) is ‖β̃ − β‖·‖(Σθ*)_U‖ ≤ (√u/(ad²))·√u(1 + s₀)‖ϑ‖, L1.4). Terms with i ∈ U vanish, so
c(U, l) = Σ_{i∈S₀∖U}ϑ_i Cov(x_l, x_i | x_U), where Cov(x_l, x_l | x_U) = Var(x_l | x_U) ≥ d and, for i ≠ l,
Cov(x_l, x_i | x_U) > 0 (L1.2(b)).
**Finiteness and (FS-BCS).** Cov(x_l, x_i | x_U) is a function of Σ restricted to U ∪ {l, i} (≤ 17 indices), i.e. of the
incidence pattern "which of these indices share a group" (Σ has entries 1, ρ_w, ρ_b only). Hence c(U, l) ranges over a
finite set of linear forms Σ_{i∈V}κ_iϑ_i (V := S₀ ∖ U, coefficients κ_i > 0 from a finite set fixed by (ρ_b, ρ_w)), and
the set of values {c(U, l)} is finite (it depends on n only through the incidence patterns, of which there are finitely
many). (a) If U ⊇ S₀ then V = ∅ and c(U, l) = 0 ("zero pair"); this needs l null (l ∉ U ⊇ S₀). (b) Otherwise V ≠ ∅;
(FS-BCS) requires c(U, l) ≠ 0. This excludes, for each of the finitely many pairs (pattern, V), the hyperplane
{Σ_{i∈V}κ_iϑ_i = 0} — a proper hyperplane because all κ_i > 0 — so (FS-BCS) is a generic condition on ϑ.
c_FS := min{|c| : c a nonzero value} > 0 is a constant.
**Noise part.** |g_l − β̃ᵀg_U| ≤ (1 + ‖β̃‖₁)G_n ≤ (1 + 16/d)G_n on E1 (‖β̃‖₁ ≤ √u‖β̃‖ ≤ u/d).

## L2.2 Single-flip improvements (on E_n, n ≥ n₀)
Constants (R06 item 11): s²_max := 2[(1 + s₀)‖ϑ‖² + σ²], s²_min := σ²/2; by L3 (c1), s² ∈ [s²_min, s²_max] on E_n for
n ≥ n₀, for every p ≤ n/2 (θ*ᵀΣθ* = ϑᵀΣ_{S₀S₀}ϑ ≤ (1 + s₀)‖ϑ‖² whatever the group incidences).
Let S ∈ Ω, k := |S| ≤ p, b a block, U := S ∩ C_b.
(i) **Positive pair** (l ∈ C_b ∖ U, c(U, l) ≠ 0, k < p).
|t̃_{U,l}| ≥ (n − 1)(c_FS − C/a)/(s√(1 + 1/a)) − σ√(n − 1)(1 + 16/d)G_n^obs/(s√d) ≥ c₁n, c₁ := c_FS/(2s_max), for n ≥ n₀.
With ψ_U ≤ n (Q_U ≤ n − 1) and a ≤ n²: n t̃²/(aψ_U) ≥ c₁² =: c₂ ∈ (0, 1) (c₂ < 1 since Q_{U∪l} > 0).
**Determinant increment** (R02 item 3). For S := U ∪ {l}, the Schur complement gives exactly
L(U ∪ l) − L(U) = log(n + 1) + log[s(1/a)/s(1/a′)], s(t) := 1 + t − Σ_{lU}(Σ_UU + tI)⁻¹Σ_{Ul}, a′ = n − 1
(det(aΣ_SS + I) = a·det(aΣ_UU + I)·s(1/a), likewise with a′, and a/a′ = n + 1); since
s′(t) = 1 + Σ_{lU}(Σ_UU + tI)⁻²Σ_{Ul} > 0 and 1/a < 1/a′, L(U ∪ l) − L(U) ≤ log(n + 1).
Using w(k + 1)/w(k) ≥ 1/(2p) and this bound:
log γ₀(S ∪ l) − log γ₀(S) ≥ −log(2p) − ½log(n + 1) + ν log(1/(1 − c₂)) ≥ (n/2)c₂ − 2 log n > 0.
(ii) **Zero pair** (U ⊇ S₀, l ∈ C_b ∖ U null, hence b is the block containing S₀ and l ∈ N₀). Population part O(n/a) =
O(1/n); by E_S, |t̃_{U,l}| ≤ (σ√(n − 1)/s)·2(20 + L_n)^{1/2}·(1 + o(1)) + O(1/n). Since U ⊇ S₀, Q_U ≥ RSS_U/s² with
RSS_U = ‖e‖² − σ²Φ(U), Φ(U) ≤ ‖g_U‖²/d ≤ 16(G_n^obs)²/d ≤ 16G_n²/d = O(log n), so ψ_U ≥ σ²n/(2s_max²); hence
n t̃²/(aψ_U) ≤ C(20 + L_n)/n and the increment is ≤ −½[L(U ∪ l) − L(U)] + C(21 + L_n) ≤ −½log(n + 1) + 1 + C(21 + L_n)
< −¼log n (by (L1.4.1) with k ≤ 16: L(U ∪ l) − L(U) ≥ log(n + 1) − 32/((n − 1)d); (L1.4.1) holds for any T, here
U ∪ {l}, since its proof only uses the eigenvalue floor d). Equivalently, removing such an l
from S with (S ∩ C_b) ∖ {l} ⊇ S₀ raises log γ₀ by ≥ log[w(k − 1)/w(k)] + ¼log n > 0.

## L2.3 Lemma (C1)
**Lemma L2.** On E_n and for n ≥ n₀: S* is the unique maximiser of γ₀ on Ω. Hence P(S̃₀ = S*, unique) → 1 (L3.1).
*Proof.* Word for word FACB L2.4 (uses only the dichotomy positive pair / zero pair of L2.1 and the two flip bounds of
L2.2): if S ≠ S* and some l ∈ S* ∖ S exists, (S ∩ C_{b(l)}, l) is not a zero pair (l ∉ N₀), so adding l strictly
increases γ₀; otherwise S ⊋ S* contains some l ∈ N₀ with (S ∩ C_b) ∖ {l} ⊇ S₀ (since S₀ ⊆ S* ⊆ S) and removing it
strictly increases γ₀. Ω is finite. ∎
Remarks. (1) Uniqueness makes e4/e4′ irrelevant (FINAL s5, Lemma UM). (2) N₀ and 𝒩* := S* ∖ S₀ are deterministic.
(3) |N₀| ≤ 15; m₀ := |𝒩*| = p − s₀ − |N₀|.
