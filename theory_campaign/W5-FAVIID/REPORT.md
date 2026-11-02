# W5-FAVIID — REPORT: a 2^B-free favourable-regime start rate on iid designs with the actual partition, and (P1)

Run of 2026-11-02, branch `theory/W5-FAVIID`. Proofs: `PROOF.md` (section numbers below refer to it). Scripts: `scripts/`
(fixed seeds in each header). Raw results: `results/*.jsonl`; tables: `results/*.txt`. Every result is a **candidate**,
not reviewed and not adopted. Status words are the protocol's and are never upgraded.

## 1. Headline

__HEADLINE__

## 2. Statements (full text and proofs in PROOF.md)

**Family FAV (PROOF §0).** Rows of X^r iid N(0, Σ_n), Σ_n unit-diagonal and block-diagonal over a deterministic partition
𝒦_n of [p] into groups of size ≤ g ≤ 16, λ_min(Σ_n) ≥ λ₀ > 0; s₀ < p ≤ n^A; fixed S₀ (s₀ fixed) and fixed nonzero β;
y^r = Σ_{k∈S₀}β_k x^r_k/ŝ_k + ε with ŝ_k = 1 or the sample SD (the study generator's convention); ε ~ N(0, σ²I). S1, S3, S4
and S6 are instances (groups of 5, one truth per group; S1 with singleton groups). S2 and S5 are not (not block-diagonal).

| # | Statement | Hypotheses beyond FAV | Status |
|---|---|---|---|
| X⁺ | For U ⊊ A with λ_min(G_A) ≥ φ²(n−1): BF(A)/BF(U) ≤ e^{κ⁺}(n+1)^{−\|A∖U\|/2}(RSS_A/RSS_U)^{−ν}, κ⁺ = O(\|A∖U\|/(φ⁴n) + 1/(φ²RSS^y_U)) — the EXP′ remainder is ≤ O(1/n) *from above*; its O(1) part is nonpositive | none (deterministic) | PROVED |
| X⁻ | matching lower bound with κ⁻ = O(1) (for deletions) | none | PROVED |
| B′ | For any fixed union of groups Γ, any fixed W outside Γ, U = (S₀∩Γ)∪W, V ⊆ Γ∖S₀: X_{U,V} ~ Beta(\|V\|/2, (n−1−\|U\|−\|V\|)/2), independent of (X_U, y); y may be any function of (X_{S₀}, ε) | none | PROVED |
| Tr′ | E[(1−X)^{−ν}1{X ≤ τ}] ≤ (1−τ)^{−e₁}(mτ/2)^{j/2}/Γ(j/2+1); truncation at τ_n = 2(1+ε₀)log max(N_n,n)/n has P → 1 over N_n ≤ Cn^A variables | — | PROVED |
| M | If E[j!a_j] ≤ C₀(Nξ)^j/Γ(j/2+1) for all j, then E max_j(j!a_j)^{1/j} ≤ 3.8311·C₀Nξ (Mittag-Leffler constant; no 2^B, no Σ_j) | — | PROVED |
| S | ‖P_{A₁+⋯+A_r}y‖² ≤ (1−(r−1)c)^{−1}Σ‖P_{A_i}y‖² when pairwise ‖P_{A_i}P_{A_k}‖ ≤ c | — | PROVED |
| G | partition-free good events (SE on sets of size ≤ max(B, 2g+s₀), RSS floor, cross-group angles O(√(log p/n)), uniform visibility, truncation) have P → 1 | [C1] (Gaussian covariance concentration, cited) | PROVED given [C1] |
| **A** | **Fixed partition 𝒫_n (blocks = unions of groups):** on P_n = {v3 blocks = 𝒫_n}, E[q 1_𝒢] ≤ 3.83(1+o(1))ξ_n, ξ_n = √((1+ε₀)log max(2^Bp, n)/(n+1)); e = O(p√n e^{−νx₁/2}); hence **1 − π₀(S₀) = O_P((s₀+1)√(log n/n))** with leading constant 3.83(s₀+1)√((1+ε₀)A) — **no 2^B, no g** (B enters only via log 2^B inside ξ_n and o(1) terms) | [C1], locked T22(i), W1-EXP L1.1–1.2 | PROVED |
| P1′ | If every group has size ≤ B and min within-group \|Σ_jk\| > 0: P(every v3 block is a union of whole groups) → 1; for groups of 5 each block holds ≤ ⌊B/5⌋ groups | [C1] | PROVED given [C1] |
| N | For the study's groups of 5 there is no deterministic limit partition: each fixed pair of groups is co-clustered with probability ≤ (m−1)/(G−1) | exchangeability of the group-level dendrogram (packing step not equivariant) | PROOF SKETCH (+ numerics §4.2) |
| **B** | **Actual, noise-dependent packing:** on Q_n(m) = {blocks are unions of groups; each group's block holds ≤ m−1 other truth-carrying groups}, q ≤ e^{o(1)}Q̄_n with Q̄_n **partition-free**, E Q̄_n ≤ 3.83(1+o(1))\|𝒲(m)\|ξ_n; hence 1_{Q_n(m)}(1 − π₀(S₀)) = O_P(\|𝒲(m)\|(s₀+1)√(log n/n)), \|𝒲(m)\| ≤ Σ_{i<m}C(h₀, i). **For S3/S4/S6, P(Q_n(3)) → 1, so 1 − π₀(S₀) = O_P(√(log n/n)) unconditionally** (constant ×≤106; ×15 while B = 14) | [C1], locked T22(i), W1-EXP L1.1–1.2 | PROVED |
| B′-conj | Theorem B holds without the \|𝒲(m)\| factor | — | CONJECTURE (numerics §4.1: realised truth context changes Q̄ by ≤ 4%) |
| §10 | Sharp first order: 1 − π₀(S₀) ≈ 1 − exp(−N_add), N_add ≈ (s₀+1)(p−s₀)M(p,n)/((2p−s₀−1)√(n+1)), M ≈ 1 + (2/√π)√(log p) — independent of B, g, θ | — | CONJECTURE (PROOF SKETCH of the mechanism; numerics agree to ±15% at n = 3200) |
| F | One-change ceiling π₀(S₀) ≤ [1 + N_add + ΣO^del + ΣO^swp]^{−1} (exact odds, any data) | none | PROVED |
| §11 | Population plug-in thresholds n*_null, n*_del, n*_swp, n*_half, n*_hit as explicit functions of (θ, v, p, s₀, ρ) | — | CONJECTURE (median-level formulas; checked §4.4) |
| C1 | δ₁ = 1 − π(S₀) = O_P(√(log n/n)) on FAV | locked T03, W3-PXN de-randomisation lemma | PROVED (composition) |
| C2 | **Thm 6's (P1) on S3/S4/S6:** Δ_n = O_P(√(log n/n)), (T^max+1)Δ_n = O_P(log^{5/2}n/√n) → 0, so T26(i)–(ii) hold with the actual partition and budgets, without EXP′/VIS/NL | W2-T26 Thm A + Lemma 1 (candidates), idealisations EX-A, EX-S, CAL, START, OUT | PROVED (composition) |
| C3 | **Thm 5(a) (T38(a)) on S3/S4/S6:** liminf P(Ŝ = S₀) ≥ 1 − limsup P(U) | locked T21 route (a), C1, EX-S | PROVED (composition) |

## 3. Proofs (skeleton; details in PROOF.md)

__PROOFS__

## 4. Evidence

__EVIDENCE__

## 5. What fails and why

__FAILS__

## 6. Needs escalation

__ESCALATION__

## 7. Outside scope

__OUTSIDE__

## 8. Confidence card

__CARD__
