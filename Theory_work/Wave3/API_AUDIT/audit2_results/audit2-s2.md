# Audit audit2-s2: Theory_work/Wave3/API_AUDIT/audit2/REQ_audit2.md
claims: item1:B4.PROOFS, item1:B4.STATED, item2:B5.S, item2:B6.S, item3:SAMP.LABEL, item3:SAMP.ABSENCE, item4:HEAD.ORDER, item4:HEAD.S, item4:HEAD.H, item4:HEAD.CONC, item5:S.QUOTE, item5:S.MODEL, item5:S.PRIOR, item5:S.DIM, item5:S.LOWER, item5:S.UPPER, item5:S.SIGNAL, item5:S.CONC, item5:S.CORE3
stop_reason: end_turn

## item1:B4.PROOFS — REFUTED (the "needs" clause: a sufficient condition read as the condition)

- **Display and page.** The bound the proof arrives at is on supp p. 6, not p. 5: d²(f*, f) ≥ min{δ_n, β*_t²δ_n/(20σ*²), 1 − √0.8}. The audit's display min{1, β*_t²/(4σ*²+4σ₂²)}·δ_n is not printed. It can be derived from the p. 5 steps, but it still contains the free σ₂, which the proof removes in its "One can show" step.
- **What the proof step needs.** From the printed bound, "d(f*, f) > ε_n" needs β*_t²δ_n ≥ 20σ*²ε_n² eventually, not β*_t bounded away from zero.
- **Counterexample.** Take independent standard normal predictors (p. 955–956). Then E exp{−(x_k+Σb_i x_{j_i})²} = (1+2var)^{−1/2} ≤ 3^{−1/2}, so δ_n is a constant. The p. 6 bound then gives d ≥ ε_n for β*_t = Cε_n → 0.
- **Theorem S.** The need on supp p. 15 is likewise a rate, n·l_n·c² ≻ r̄_n log P_n, as TRACK_B.md:364 itself says. With l_n constant this allows c → 0.
- **Consequence.** "Treated as constants" describes how the proofs are worded. The level their proof steps require is a rate (about ε_n/√δ_n, or √(r̄_n log P_n/(n·l_n))). So "needs β*_t bounded away from zero" (TRACK_B.md:105-106) is false. Our fixed-signal hypotheses (READER 272-273, 670-671) ask more than their proof steps use, not "the same".

## item1:B4.STATED — UNCLEAR

- **What the label depends on.** "Stronger than their statements" and the 1/n example require that Song–Liang's β* may change with n.
- **What the texts show.** Every n-dependent quantity carries a subscript (P_n, r_n, r̄_n, ε_n, l_n, δ_n). β*_j and σ* carry none. Conditions (3) and (4) are written as lim_{n→∞} Σ_{j≤P_n}, which reads as partial sums of one fixed sequence (p. 950). Supp p. 14 uses R*_t/(n−|t|) → 1 almost surely.
- **If β* is a fixed sequence.** A coefficient "of size 1/n" is not an instance of their model. The finitely many nonzero coefficients are constants by the statement itself. The label would then be "same" for our Theorems 2 and 6, and "weaker" for Theorem 1 and Theorem 9 (which allow n-dependent parameters, READER 115, 1035).
- **If β* may depend on n.** The 1/n example is valid. With exchangeable predictors, the screening conclusion of Theorem 3 and (24) both fail.
- **Passage needed.** Their expression (2) or the definition of f*, or any sentence saying whether β* may depend on n.
- **Independent of this.** The unqualified form "their theorems state no condition on the size of the nonzero coefficients" (WRITING_DELTA:17-18; TRACK_B.md:298) is contradicted by Theorem 1. Its condition (8), Δ(r_n) ≺ ε_n, and its preamble (3) do constrain coefficient size (p. 952). TRACK_B.md:101-103 admits this.

## item2:B5.S — REFUTED (quantifier over r̄_n and over our own theorems)

- **Theorem S allows small r̄_n.** It assumes only (12), 1 ≤ r_n ≤ r̄_n < P_n; "r_n ≻ 1" belongs to Theorem 2. Corollary S₁ allows r̄_n ≺ log^{k₁}(n) for any k₁ > 0 (supp p. 16). So |t| + r̄_n may be bounded or ≺ log n.
- **Counterexample.** Take r̄_n = s₀+1, r_n = 1, P_n = n^A. Then (22) speaks only of models with 2s₀+1 columns. Our (A4) covers all sets up to 2(A+1)s₀+2 > 2s₀+1 columns at a fixed level (READER 107-108). Our (A5) covers 3(A+1)(s₀+1) log n columns (READER 109-110), where (22) is silent. So ours is not "stronger only in the fixed level"; it is also on larger sets. "A 1/n-level floor on O(log n) columns and nothing on larger sets" is then additional, not weaker.
- **Inconsistency with the audit.** TRACK_B.md:119-121 makes exactly this r̄_n distinction against Condition 3, then drops it against Theorem S.
- **Our own theorems.** The verdict covers Theorem 2 (A3) and Theorem 6 (A5) (TRACK_B.md:117, AUDIT.md:47). Theorem 2 (A3) is a fixed level on 5(A+1)(s₀+1) log n columns (READER 274-275). Theorem 6 (A5) is a fixed level on Q∪{l} with |Q| up to n^b (READER 682-683). Neither is "bounded sets" nor "only a 1/n-level floor on O(log n) columns".
- **"No upper bound".** This is not a real relaxation on our scale; see item5:S.UPPER.
- **Effect on the label.** In the sub-case r̄_n = s₀+1 with standardised columns, our (A4) implies all of (22)–(23) with l_n = φ₀²/2 and l′_n = 2s₀+1. The comparison is then ordered (ours stronger), not "not ordered".

## item2:B6.S — REFUTED

- **Direction.** "Weaker" requires (22) to imply our (A5). It does so only when |t| + r̄_n ≥ 3(A+1)(s₀+1) log n.
- **Counterexample.** Take r̄_n bounded or r̄_n ≺ log n, allowed by (12) and by Corollary S₁ with k₁ < 1. Take m ≈ log n null columns x_1..x_{m−1} orthogonal and x_m ∝ Σ_{i<m} x_i. Every (|t|+r̄_n)-subset has smallest eigenvalue ≥ n(1−o(1)), so (22)–(23) hold with a constant l_n. But λ_min(X_SᵀX_S) = 0 on a set of m columns, so (A5) fails.
- **Correct label.** B6 against Theorem S is not ordered in set size, just as the audit says against Condition 3 (TRACK_B.md:119-121). "(22) covers every model ζ" (TRACK_B.md:385) is true only for models of exactly |t| + r̄_n columns and their subsets.
- **Consequence.** "Additional on null-only sets holds against Theorem 3 only" is therefore also wrong. It holds against Theorem S whenever r̄_n ≺ log n.

## item3:SAMP.LABEL — REFUTED ("weaker" fails the two-direction check; "not none" stands)

- **Their statements.** Supp p. 10 (15), supp pp. 12-13 after (21), and supp p. 16 with Lemma S₂(ii) hold for every fixed data set with no design hypothesis. They assert convergence of the sampler output to exact posterior quantities (q_j and the mode).
- **Ours.** Theorem 6 needs Gaussian rows and (A3)–(A6) (READER 666-688). It concludes Ŝ = S₀ on events 𝒢_n, not convergence to the posterior. Corollary 9C says "the corollary does not assert" that the list carries posterior mass (READER 1097-1099). It gives nothing on inclusion probabilities.
- **Contradicting case.** Take a design violating visibility (A3) or leakage (A4). Song–Liang's N → ∞ statements apply, and with Theorem S give selection in iterated limit. Ours give nothing.
- **Correct label.** Ours does not imply theirs. The two are not ordered: theirs is weaker in budget (N → ∞ only), broader in data, and about a different object (recovery of the posterior). This applies also to AUDIT.md:71 and TRACK_B.md:389.

## item4:HEAD.S — REFUTED

- **"We ask less: only a 1/n-level floor on O(log n) columns and nothing on larger sets."** This is false whenever |t| + r̄_n ≺ log n, which (12) and Corollary S₁ allow. There our (A4) and (A5) ask more than (22). See item2:B6.S. It is also false for Theorem 2 (A3), a fixed level on O(log n) columns.
- **"We ask less: signals as small as √(log n/n)."** Theorem S as printed (supp p. 13) states no signal condition. Against the theorem we ask more: (A6) and (A3) at READER 106, 111-112. B4 says so itself (TRACK_B.md:101). The "less" is against a proof step (supp p. 15), not a hypothesis.
- **"No upper eigenvalue bound."** There is no difference on standardised columns; see item5:S.UPPER.

## item4:HEAD.H — REFUTED

- **"Add a row law."** Their Hellinger theorems already carry a condition on the law of x. Theorem 1 has "all predictors |x_i| ≤ 1" (p. 952). Theorem 2 has "all the predictors satisfy condition 1" (p. 953), an exponential-moment tail condition.
- **Against Theorem 1 the row condition is not ordered.** Gaussian predictors satisfy our (A3) with L = 1 (READER 1037-1039) and violate |x_i| ≤ 1. A bounded sparse binary predictor with P(x=1) → 0 satisfies theirs and violates our variance-proportional sub-Gaussian bound for any fixed L.
- **"Add the range of p."** They restrict P_n too, through (10), (12)–(13) and Corollary 1. Conditions (12)–(13) (1 ≤ r_n ≺ P_n) and p. 950 (P_n ≻ n^θ) force P_n → ∞. Our (A2), 2 ≤ p_raw ≤ n^A (READER 1036), admits bounded p. So the range is narrower above and wider below.

## item4:HEAD.CONC — REFUTED (stronger in kind, not ordered in rate)

- **Their Theorem 3** (p. 956) concludes π{t∈ξ | D_n} ≥ 1 − exp(−c₁nε_n²) outside a data event of probability < exp(−c₁nε_n²). By (10) and p. 950, nε_n² ≻ r̄_n ln P_n ≳ log n, so both bounds are smaller than any power of n.
- **Ours** give max_j|PIP_j − 1{j∈S₀}| ≤ 1 − π(S₀|y) = O_P(√(log n/n)) and P(HPM=MPM=S₀) ≥ 1 − 4C√(log n/n) (READER 117-122). These do not imply Theorem 3's bound.
- **Hellinger.** Their (15) has exceptional mass and probability exp(−c₁nε_n²). Ours are polynomial, n^{−cM/2} and n^{−cM}, at fixed M (READER 1091-1094). Ours has the smaller radius; theirs has the smaller tail at their radius.
- **Not settled here.** The statement of Theorem 9 itself is not in the material. If M may grow with n, the Hellinger part of this finding falls; the Theorem 3 part does not.

## item5:S.LOWER — REFUTED

- **"Weaker on larger sets"** holds only if |t| + r̄_n exceeds our set sizes.
- **Counterexample.** Take r̄_n = s₀+1, admissible under (12) and condition 2 with r_n = 1 and P_n = n^A. Then (22) concerns 2s₀+1 columns. Ours concern up to 2(A+1)s₀+2 columns at a fixed level and O(log n) columns at g₀. Ours are the larger sets.
- **Effect on the label.** In that case our (A4) gives ch′₁(X_ζᵀX_ζ) ≥ (n−1)φ₀² > n·l_n with l_n = φ₀²/2, and (23) holds since r̄_n log P_n = O(log n) ≺ n. So the lower bounds are ordered (ours stronger), not "not ordered".

## item5:S.UPPER — REFUTED (label should be "same" on the scale of our designs)

- **The upper half of (22) is existential in l′_n.** For columns with ‖x_j‖² = n−1 (STATEMENT.md:20), ch₁(X_ζᵀX_ζ) ≤ tr = |ζ|(n−1) < n·|ζ|. So l′_n := |t| + r̄_n always works.
- **The l′ clauses then follow from (23).** Condition 2's n·l_n ≻ l′_n and condition 1's n·l_n ≻ log l′_n both follow from r̄_n log P_n ≺ n·l_n.
- **Consequence.** No design on our scale satisfies the rest of Theorem S and violates its upper bound. Pervasive factors included: there ch₁ ≈ n|ζ|. "No upper eigenvalue bound" is therefore not a weaker hypothesis here.
- **Caveat.** A difference exists only for raw columns whose scale diverges with n.

AUDIT2 item1:B4.PROOFS VERDICT=REFUTED
AUDIT2 item1:B4.STATED VERDICT=UNCLEAR
AUDIT2 item2:B5.S VERDICT=REFUTED
AUDIT2 item2:B6.S VERDICT=REFUTED
AUDIT2 item3:SAMP.LABEL VERDICT=REFUTED
AUDIT2 item3:SAMP.ABSENCE VERDICT=NO-FINDING
AUDIT2 item4:HEAD.ORDER VERDICT=NO-FINDING
AUDIT2 item4:HEAD.S VERDICT=REFUTED
AUDIT2 item4:HEAD.H VERDICT=REFUTED
AUDIT2 item4:HEAD.CONC VERDICT=REFUTED
AUDIT2 item5:S.QUOTE VERDICT=NO-FINDING
AUDIT2 item5:S.MODEL VERDICT=NO-FINDING
AUDIT2 item5:S.PRIOR VERDICT=NO-FINDING
AUDIT2 item5:S.DIM VERDICT=NO-FINDING
AUDIT2 item5:S.LOWER VERDICT=REFUTED
AUDIT2 item5:S.UPPER VERDICT=REFUTED
AUDIT2 item5:S.SIGNAL VERDICT=NO-FINDING
AUDIT2 item5:S.CONC VERDICT=NO-FINDING
AUDIT2 item5:S.CORE3 VERDICT=NO-FINDING