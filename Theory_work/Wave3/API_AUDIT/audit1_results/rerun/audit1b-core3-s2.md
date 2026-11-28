# Audit audit1b-core3-s2: Theory_work/Wave3/API_AUDIT/audit1b/REQ_core3.md
claims: core3:B7.SL, core3:B1.SL, core3:B2.SL, core3:B7.IO, core3:A2.SL, core3:A2.IO, core3:B8.SL, core3:B8.LEMMA, core3:B8.IO, core3:B9.SL, core3:B9.IO, core3:B5.SL, core3:B10-FL.SL, core3:A5.IO, core3:A6.SL, core3:A6.IO, core3:SCOPE.IO
stop_reason: end_turn

## core3:B7.SL

**Problem.** "Gaussian rows … stronger than Condition 1 (implies it)" fails for the row law Theorem 6 actually allows.

- Theorem 6 takes rows N_p(m_n, Σ_n) with an unrestricted mean m_n (`READER_VERSIONS.md:666`; `W3-RM/STATEMENT.md:41-42`).
- Condition 1 (SL p. 953) is a raw-moment bound with constants M, δ fixed in n. SL's own Gaussian case is "a Gaussian process with zero mean and var(x_i) = 1".
- Counterexample: Σ_n = I, m_n = n·1 (any unbounded mean works). Take r = 1, a = δ. Then E exp{(δx_j)²} = (1−2δ²)^(−1/2) · exp{δ²n²/(1−2δ²)} → ∞, so no fixed M exists.
- This sequence is inside Theorem 6 (the model has an intercept α and X is centred) and outside Condition 1. The implication holds only for centred rows or bounded means, which the verdict does not state.

The first half of `TRACK_B.md:140` ("Thm 9 (A3) … implies it") cannot be checked: the text of Thm 9 (A3) is not among the excerpts.

## core3:B2.SL

**Unclear.** The lower-range half is confirmed by SL p. 950 ("P_n ≻ n^θ for some θ > 0") against (S2), `READER_VERSIONS.md:29`. The upper-range half rests on "Corollary 1, p. 954, P_n < exp(Cn^α), α ∈ (0,1)", which is not among the excerpts.

**Passage needed:** SL Corollary 1, p. 954, with its hypotheses.

## core3:A2.SL

**Problem.** `AUDIT.md:77` equates (A2) with SL's (4), but (A2) is strictly stronger.

- (A2) is two requirements: s₀ fixed, and θ_lo ≤ |θ*_j| ≤ θ_hi on S₀ (`READER_VERSIONS.md:670-671`).
- SL (4), p. 950, bounds only the number of nonzero β*_j. It says nothing about their size.
- Counterexample: a fixed finite support with β*_j = 1/n (or β*_j = n) satisfies (4) and violates (A2).
- By the audit's own reading (`TRACK_B.md:89-92`), SL state no upper bound under (4) and no beta-min in Theorem 3. So on the signal part our assumption is stronger on both sides, not "same" and not merely "comparable".

Two supporting claims are also not checkable from the excerpts: "(4) used by Theorems 2–3; Theorem 1 alone allows (3)" and "Theorem 3 states no beta-min". Theorem 3 (p. 956) imports "all the conditions of theorem 2", and neither Theorem 1 (p. 952) nor Theorem 2 is given.

## core3:B8.IO

**Problem.** "P6: fac2, s5 unclear" (`TRACK_B.md:251`) is contradicted by explicit computation. Both satisfy (A3) with a fixed margin.

The P6 truth has aligned signs: β = (1.4, 1.0, 1.8, 1.2) repeated, all positive (`W3-P6/DESIGN.md:16`). So visibility holds whenever all conditional covariances between columns outside U are nonnegative, because then

Cov(W_j, Wᵀθ* | W_U) = θ_j·Var(W_j | W_U) + Σ_{k∈S₀∖(U∪j)} θ_k·Cov(W_j, W_k | W_U) ≥ θ_j·λ_min(Σ).

**fac2** (`DESIGN.md:14`). Loadings are b_j = (√.35, ±√.25), idiosyncratic variance .40. Let U contain m₁ even and m₂ odd columns, M = m₁ + m₂, D = m₁ − m₂.

- The factor posterior precision is [[1+.875M, D√.0875/.4], [D√.0875/.4, 1+.625M]], with determinant det > 0.
- Opposite parity, j, k ∉ U: Cov(W_j, W_k | W_U) = [.35(1+.625M) − .25(1+.875M)]/det = .10/det > 0.
- Same parity: Cov = [.6 + .875·m_opp]/det > 0, where m_opp is the number of U-columns of the other parity.
- Var(W_j | W_U) ≥ .40.
- Hence |Cov(W_j, Wᵀθ* | W_U)| ≥ 1.0 × 0.40 for every |U| ≤ 15 (indeed every U). Inside.

**s5** (`DESIGN.md:15`). Σ = .3J + .4H + .3I.

- With A = .3I + .4H, A⁻¹ = (1/.3)(I − (.4/2.3)H), which has negative within-block off-diagonals.
- Σ⁻¹ = A⁻¹ − κJ with κ > 0 (Sherman–Morrison, A⁻¹1 = .4348·1).
- All off-diagonals of Σ⁻¹ are negative, so Σ⁻¹ is an M-matrix and every conditional covariance is ≥ 0.
- Var(W_j | W_U) ≥ λ_min(Σ) = .3.
- Hence |Cov(W_j, Wᵀθ* | W_U)| ≥ 1.0 × 0.3 for every U. Inside.

This is the same aligned-sign argument that gives "cs in". It also agrees with `RESULTS.md:63-64` ("Clustered aligned truths in factor designs are inside").

The other cells of the row are not contradicted. Study S5 has mixed signs and a very small margin: for θ_j = −1.0 with U = the six other negative truths the value is +0.0056, so "unclear" is defensible. For 1M FAC the coefficient signs are not in the excerpt.

## core3:B5.SL

**Unclear.** One of the three comparisons is confirmed and two cannot be settled.

- "Fixed level against vanishing" is confirmed: δ_n ≤ 1 and δ_n ≻ ε_n² force ε_n → 0, and the Gaussian form on pp. 955–956 needs only var ≻ ε_n².
- "On smaller sets" compares |S| ≤ 5(A+1)(s₀+1) log n (`READER_VERSIONS.md:682-683`) with Condition 3's r̄_n + 1 predictors. No excerpt defines r̄_n or gives its growth. If r̄_n = O(log n) the comparison reverses.
- "For a stronger conclusion" is open because p. 956 says "Theorem S in the on-line supplementary material establishes the consistency of MAP models". Its hypotheses are not given.

**Passages needed:** SL's definition and rate of r̄_n (and ε_n) in the conditions of Theorem 2, and the statement of Theorem S.

## core3:B10-FL.SL

**Problem.** The absence claim ("none", `AUDIT.md:80` second part; `TRACK_B.md:199`) is contradicted by the SL texts supplied. This is the most contestable of my findings, since "counterpart" can be read by role rather than by mathematical content.

- The second part of (A5) is a population eigenvalue floor λ_min(Σ_{Q∪{l}}) ≥ c. It is the same kind of object as the first part, which the audit itself calls "comparable to Condition 3".
- It implies Var(W_l | W_Q) ≥ c, i.e. no linear combination of the columns of Q mimics column l. That is the content of Condition 3 (p. 955) for index sets drawn from Q ∪ {l}.
- SL's sufficient forms are eigenvalue floors "for any choice of x̃" and for the whole vector: "all predictors are identifiable if ch′₁{var(x)} ≻ ε_n²" (pp. 955–956).
- Corollary 2 (p. 957) requires no exact multicollinearity in the designated subset x_s.
- Stage 2 (p. 959, step (c)) applies the Section 2 theory to the merged set S̃, which is SL's analogue of Q.
- The verdict's own rider ("implied by B5's global floor") concedes the link: a global floor implies it by itself as a principal-submatrix bound, and SL state a global floor at vanishing level.

So the correct relation is the same as for the first part (comparable: fixed against vanishing level, different set family), not "none". That the condition serves the search does not remove the counterpart.

AUDIT1 core3:B7.SL VERDICT=REFUTED
AUDIT1 core3:B1.SL VERDICT=NO-FINDING
AUDIT1 core3:B2.SL VERDICT=UNCLEAR
AUDIT1 core3:B7.IO VERDICT=NO-FINDING
AUDIT1 core3:A2.SL VERDICT=REFUTED
AUDIT1 core3:A2.IO VERDICT=NO-FINDING
AUDIT1 core3:B8.SL VERDICT=NO-FINDING
AUDIT1 core3:B8.LEMMA VERDICT=NO-FINDING
AUDIT1 core3:B8.IO VERDICT=REFUTED
AUDIT1 core3:B9.SL VERDICT=NO-FINDING
AUDIT1 core3:B9.IO VERDICT=NO-FINDING
AUDIT1 core3:B5.SL VERDICT=UNCLEAR
AUDIT1 core3:B10-FL.SL VERDICT=REFUTED
AUDIT1 core3:A5.IO VERDICT=NO-FINDING
AUDIT1 core3:A6.SL VERDICT=NO-FINDING
AUDIT1 core3:A6.IO VERDICT=NO-FINDING
AUDIT1 core3:SCOPE.IO VERDICT=NO-FINDING