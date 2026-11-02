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

**Theorem A (fixed partition).** Five ingredients, each short:
1. *Lemma X⁺ removes the EXP′ constant.* W1-EXP's remainder R is O(1) (κ_EXP ≈ 100–1,700 nats at study SNR), but its O(1)
   part is ν[a_U/RSS^y_U − a_A/RSS^y_A] with a_S = 0.02 + y'P_Sy/(n+1) + O(1/n) increasing in S and RSS^y decreasing, so it is
   **nonpositive up to O(1/n)**. Upper bounds on start mass off the truth therefore need no EXP′ constant and no chain.
2. *Lemma B′ gives exact Beta laws* for the block statistics X_{U_b*,V} at the reference S₀, for every fixed union of groups
   and every fixed outside conditioning set, with y any function of (X_{S₀}, ε) (so the generator's sample-SD convention is
   exact, not approximate).
3. *Lemma Tr′:* truncated moment E[(1−X)^{−ν}1{X ≤ τ_n}] ≤ (1+o(1))(t_n/2)^{j/2}/Γ(j/2+1) and a truncation event of probability
   → 1 (W3-PXN's Lemma Tr with the crude 2^{e₁} replaced by (1−τ_n)^{−e₁} → 1).
4. *Lemma M:* for D = max_j(j!a_j)^{1/j}, max_j Y_j ≤ λ(1 + Σ_j(Y_j/λ)^j) and the Mittag-Leffler sum give
   E D ≤ 3.8311·C₀·Nξ — **this is where 2^B disappears** (the locked T22(iii) sums over all T ⊆ C_b; W3-PXN summed over j).
5. *Locked T22(i):* 1 − π₀(S₀) ≤ (s₀+1)q/(1−q) + s₀e, with e = O(p√n e^{−νx₁/2}) from Lemma X⁻ and uniform visibility (G4).

**Theorem B (the actual packing).** The crux is a **factorisation across population-independent groups**: inside a realised
block b = K₁ ∪ ⋯ ∪ K_R, the residualised spans of different groups are nearly orthogonal (principal cosines
c_n = O(√(log p/n)) uniformly, (G3)), so by Lemma S the block statistic is at most (1 − Bc_n)^{−1} times the sum of the
per-group statistics, and since all statistics are O(log n/n) on the truncation event the error in the exponent is
O(B²t_n(τ_n + c_n)) → 0. Then a_bj ≤ e^{o(1)}Σ_{j₁+⋯+j_R=j}∏_i a′_{K_i,W_i,j_i}, the multinomial theorem gives
D_b ≤ e^{o(1)}Σ_iD′_{K_i,W_i}, and q ≤ e^{o(1)}Q̄_n where **Q̄_n sums D′_{K,W} over all groups K and all possible truth contexts
W ∈ 𝒲_K(m)** — a fixed, partition-free family with exact Beta laws (Lemma B′ with Γ = K). The packing's dependence on the null
columns never has to be decoupled: the inequality holds for every packing at once. The price is the number of truth contexts
|𝒲(m)|. Lemma P1′ (laminarity of complete linkage w.r.t. groups, then the cut and the packing keep whole groups) gives
P(Q_n(3)) → 1 for S3/S4/S6.

**Proposition B1 (S1).** For independent null columns, every truth context is dominated at once by the column's projection
on span(X_{S₀}, Y), a Beta((s₀+1)/2, ·) variable: rate n^{−1/2}(log n)^{(s₀+1)/2} with no event on the packing.

**Corollaries C1–C3.** δ₁ = O_P(√(log n/n)) from locked T03 by W3-PXN's de-randomisation lemma; Δ_n = max(1 − π₀(S₀), δ₁)
(W2-T26 Lemma 1); T^max = O(log²n); W2-T26 Theorem A and locked T21 do the rest.

## 4. Evidence

__EVIDENCE__

## 5. What fails and why

- **A fixed limit partition for groups of 5 (the task's P_n device).** It does not exist: once each block is a union of whole
  groups, which groups share a block is decided by cross-group sample correlations whose population values are all 0, i.e.
  by noise (Proposition N; §4.2 numerics: two independent designs share almost no co-blocked group pairs). W3-VEXP R3's
  device works only when g ≤ B < 2g (blocks = groups), e.g. groups of 9–16 at B = 16; Theorem A covers that case.
- **Union over candidate blocks / Hölder decoupling** (W3-VEXP's attempts): lose a polynomial factor. Not needed — the
  factorisation inequality is deterministic on a partition-free event.
- **Removing the |𝒲(m)| factor (Conjecture B′).** The realised truth context W(K) is X-measurable while D′_{K,W} depends on y;
  conditioning on X turns D′ into an e^{δ²/(2Δ)}-type leakage functional (W1-EXP's NL_avg route, abandoned by W3-VEXP), and
  the index-1 heavy tail of e^{χ²/2} makes "max over contexts" as large as the sum, so a max-based bound does not help either.
  Numerically the context changes Q̄ by ≤ 4% (§4.1), so I believe the factor is an artefact.
- **S1 constant.** With singleton groups the context count can reach 2^{s₀}; Proposition B1 trades it for (log n)^{(s₀+1)/2}.
  Neither is a usable finite-n constant at s₀ = 14. The realised contexts are small (§4.2).
- **T22(i) as a finite-n certificate.** It is valid in every one of the 1,600 designs, but it is **vacuous at every n ≤ 3,200**
  (§4.1): the deletion quantity e is a maximum over all U ⊆ C_b, including U that contain all of a truth's group mates, where
  the truth's visible gain is θ_j²Var(x_j | mates)/v (Var = 0.19 in S4). That is a finite-n weakness of the locked aggregation
  bound, not of the rate; Proposition F's one-change ceiling and the exact convolution are the finite-n tools.
- **(P1) with T^max.** (T^max + 1)Δ_n < 1 needs Δ_n < 2.5·10⁻⁴, i.e. n ≈ 10¹⁰ at s₀ = 14 (§10's sharp constant). The
  asymptotic statement C2 is true but has no finite-n content; the realised T_n is what matters (§4.5).
- **T_n = O_P(1) in the favourable regime.** I could not prove it. The pilot's first ESS step sees weights e^{d(S)−d(S₀)} whose
  off-truth part (posterior versus block null-addition statistics, (Z_f² − Z_b²)/2) is heavy-tailed, so the realised T_n need
  not settle to 1; the simulations show T_n of order 1–5 at n ∈ [800, 6400] (§4.5). OPEN.

## 6. Needs escalation

1. **Independent check of the three new load-bearing steps:** Lemma X⁺ (sign of the EXP′ remainder; short but everything
   uses it), Lemma M (the Mittag-Leffler aggregation; replaces 2^B), and Theorem B's factorisation (Lemma S + (G3) + the
   multinomial step). The rest is W3-PXN's machinery with sharper constants.
2. **[C1] and the routine perturbation steps** in Lemma G ((G3) Schur-complement Lipschitz bound; (G4) uniform residual
   variances over |T| ≤ B with the generator's sample-SD coefficients): standard, written at proof level but not with every
   constant explicit.
3. **HQ decision (Thm 2(iii), Thm 6):** T22(iii)'s favourable branch can be stated for S3/S4/S6-type iid designs on the
   actual partition with no EXP′/VIS/NL hypothesis and no 2^B (Theorem B + C2). This also discharges W2-T26 Theorem B's
   CONDITIONAL input for these designs. The paper must not claim finite-n relevance: n*_half ≈ 1,050–1,450 for the study's
   s₀ = 14 designs, and (P1) with the realised grid needs n of order 10³–10⁴ (§4.5).
4. **Felipe / method (no change proposed):** the start's dominant finite-n defect in iid designs is the null-addition mass
   (s₀+1)M(p,n)/(2√n), which no signal strength removes and which depends on neither B nor the partition. Only a change of
   the start (e.g. a sharper null-addition penalty in the tables) would move it; that is outside this run.

## 7. Outside scope

- **W3-PXN Theorem P3's constant improves the same way.** Lemmas X⁺ and M apply verbatim to LH-iid (blocks = groups): its
  E[q̃] ≤ 2.3·2^{g+3}gξ_n becomes 3.83(1+o(1))ξ_n, and e^{jκ} disappears. Not rewritten.
- **The locked T22(i) e-quantity is pessimistic at finite n** (proxy-saturated U). A refined aggregation that weights U by its
  start mass would give a usable finite-n certificate; this would be an edit of a locked statement.
- **Sharp first-order law of the start in iid designs** (§10): 1 − π₀(S₀) ≈ 1 − exp(−N_add) with N_add independent of θ, v, B
  and g. The same null-addition mechanism drives δ₁ (posterior null additions), so Δ_n ≈ (s₀+1)√(log p/(πn)) is a floor for
  both endpoints of the bridge in iid designs.
- **Discovery needs much less than favourability.** T38(a)'s route (a) needs only Q_f·π₀(S₀) → ∞; at the study budgets
  that happens at n*_hit ≈ 330–440, a factor ≈ 3 below n*_half.

## 8. Confidence card

__CARD__
