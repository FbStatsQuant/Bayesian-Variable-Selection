# Audit audit2-s1: Theory_work/Wave3/API_AUDIT/audit2/REQ_audit2.md
claims: item1:B4.PROOFS, item1:B4.STATED, item2:B5.S, item2:B6.S, item3:SAMP.LABEL, item3:SAMP.ABSENCE, item4:HEAD.ORDER, item4:HEAD.S, item4:HEAD.H, item4:HEAD.CONC, item5:S.QUOTE, item5:S.MODEL, item5:S.PRIOR, item5:S.DIM, item5:S.LOWER, item5:S.UPPER, item5:S.SIGNAL, item5:S.CONC, item5:S.CORE3
stop_reason: end_turn

## item2:B5.S — REFUTED

**Problem.** This is a quantifier error over r̄_n. Theorem S puts (22) on models of exactly |ζ| = min{|t| + r̄_n, n} columns (supp p. 13). The only condition it places on r̄_n is (12), 1 ≤ r_n ≤ r̄_n < P_n. Unlike Theorem 2 (p. 953) it does not ask r_n ≻ 1, and Corollary S_1 (supp p. 16) allows r̄_n ≺ log^{k₁}(n) for any k₁ > 0. So |t| + r̄_n may be bounded or o(log n). In that regime our floors sit on larger sets than theirs. "Stronger only in asking a fixed level on bounded sets" and "weaker in … a floor of order 1/n on O(log n) columns and nothing on larger sets" are then both false.

**Counterexample E.**
- Take s₀ = |t| = 1, r_n = r̄_n = 1 and V_ξ⁻¹ = X_ξᵀX_ξ/n, so (22) concerns pairs only.
- Take a standardised design with P_n ≤ n^A and all pairwise sample correlations at most ½ in absolute value.
- Among the null columns put x_a, x_b, x_c, x_d mutually orthogonal and x_e = −(x_a + x_b + x_c + x_d)/2. This has norm² n − 1 and correlation −½ with each of the four.
- Theorem S's hypotheses hold. Every pair has eigenvalues (n−1)(1 ± ρ) with |ρ| ≤ ½, so (22) holds with l_n = ¼, l′_n = 2. (23) reads log P_n ≺ n/4. Condition 2 reads n/4 ≻ 2 and log √n ≻ √(log P_n), true since log P_n ≤ A log n.
- Our hypotheses fail. S = {a, b, c, d, e} has λ_min = 0 and |S| = 5, which violates (A4) (READER:107–108, sets up to 2(A+1)s₀+2 ≥ 6 columns) and (A5) (READER:109–110), hence (F_w) (STATEMENT:71–73).

**Consequence.** In this case our eigenvalue hypotheses are strictly stronger, not unordered. For any r̄_n ≤ (2A+1)s₀ + 2, (A4) implies (22)–(23) with l_n = φ₀²/2 and l′_n = s₀ + r̄_n + 1. The upper half of (22) is automatic for columns of norm² n − 1 (STATEMENT:20), since ch₁(X_ζᵀX_ζ) ≤ (n−1)|ζ|. The same failure occurs for r̄_n → ∞ with |t| + r̄_n = o(log n): an exact dependence among m ≤ 3(A+1)(s₀+1) log n null columns can leave every (|t| + r̄_n)-subset well conditioned.

"Not ordered, with ours weaker on larger sets" holds only when |t| + r̄_n exceeds our set sizes. The audit makes exactly this case split for Condition 3 (TRACK_B:119–121) but drops it for Theorem S (TRACK_B:129–132, :299, :384; AUDIT.md:47; WRITING_DELTA:20–22).

## item2:B6.S — REFUTED

**Problem.** "Their floor (22) covers every model of |t| + r̄_n columns … so ours is weaker" assumes those models contain our O(log n)-column sets. That holds only if |t| + r̄_n ≥ 3(A+1)(s₀+1) log n, which Theorem S does not require ((12) only, supp p. 13).

**Counterexample.** In counterexample E above, (22)–(23) and condition 2 hold, yet five null columns are exactly dependent, so Thm 1 (A5) (READER:109–110) fails. Our floor is there an additional condition on null-only sets against Theorem S too. This contradicts "weaker" (TRACK_B:154–156, :300) and "'additional on null-only sets' holds against Thm 3 only" (TRACK_B:385).

AUDIT.md:48 says "all sets". The printed condition is on sets of size min{|t| + r̄_n, n} only.

## item3:SAMP.LABEL — REFUTED

**Problem.** "Weaker" fails the direction check: neither statement implies the other.

- **What Song–Liang assert.** For every data set and with no design condition, as the number of iterations grows: q̂_j → q_j almost surely (supp pp. 12–13, (21)); Ê_f h → E_f h almost surely for any integrable h (supp p. 10, (15)); the sampled best model is a consistent estimate of the MAP model (supp p. 16, Lemma S_2).
- **What ours assert.** Theorem 6 (READER:689–691) says Ŝ = S₀ on events G_n under (A3)–(A6), at the coded budget. It has no statement as iterations grow and none on convergence of sampler estimates to posterior quantities. Corollary 9C says of the list's posterior mass that "the corollary does not assert it" (READER:1097–1099).

**Explicit case.** Take a fixed data set outside G_n, or one whose posterior mode is not S₀. Song–Liang's statements say the output converges to the MAP model and the exact inclusion probabilities; ours say nothing. Against Corollary 9C (AUDIT.md:71), their (15) asserts in the limit exactly what 9C declines to assert.

The correct relation is "not ordered": theirs is an infinite-budget statement for all data, ours a finite-budget statement on G_n under design conditions.

**Citation gap.** The general sampler-output statements (13)–(15) are on supp pp. 9–10. They are missing from the audit's "supp pp. 12–13, 16–17" and from "Lemma S₂ and a citation".

## item4:HEAD.S — REFUTED

1. **Floor on O(log n) columns.** "We ask less elsewhere: … only a 1/n-level floor on O(log n) columns and nothing on larger sets" fails by counterexample E. For |t| + r̄_n below our set sizes (allowed by (12), supp p. 13, and Cor S_1, supp p. 16), that floor is something we ask and Theorem S does not.
2. **Signals.** "We ask less: … signals as small as √(log n/n)" has the wrong direction against the theorem. Theorem S as printed states no signal-size condition (supp p. 13), which is the audit's own B4 label ("stronger than their statements"). A coefficient of size 1/n satisfies Theorem S's hypotheses and violates Thm 1 (A6) (READER:111–112). Against Theorem S we therefore ask more here. "Less" holds only against the implicit setting of its proof (supp p. 15), a qualifier the headline (WRITING_DELTA:9–12) omits.
3. **Upper bound (secondary).** On columns of norm² n − 1 (STATEMENT:20) the upper half of (22) and n·l_n ≻ l′_n follow from the lower half and (23) with l′_n = |t| + r̄_n. "No upper eigenvalue bound" therefore separates the two only on unstandardised X.

## item4:HEAD.CONC — REFUTED

"Our conclusions are stronger" fails the direction check against Song–Liang's stated conclusions.

- **Theorem 3 (p. 956).** It concludes π{t ∈ ξ | D_n} ≥ 1 − exp(−c₁nε_n²), except with probability exp(−c₁nε_n²). Under Theorem 2's conditions ((10) and r_n ≻ 1), nε_n² ≻ r̄_n ln P_n, so for P_n polynomial in n both quantities are o(n^{−K}) for every K. Ours gives 1 − PIP_j ≤ δ_n = O_P(√(log n/n)) and P(HPM = MPM = S₀) ≥ 1 − 4C√(log n/n) (READER:117–122). On sensitivity and on the exceptional probability their conclusion is not implied by ours. Ours is stronger on specificity and exact selection, so the two are not ordered.
- **Theorems 1–2, (15) (pp. 952–953).** Their excluded posterior mass and exceptional probability are exp(−c₁nε_n²). Ours, in the only form given (Cor 9C, READER:1091–1094), are n^{−cM} at radius √(M log n/n). The smaller radius is ours and the smaller probabilities at their radius are theirs, unless the level-M form is uniform in M up to nε_n²/log n. Theorem 9's conclusion is not in the excerpts, so this part cannot be settled here.
- **Theorem S, (24).** See item5:S.CONC: our statement is about a different posterior.

## item5:S.LOWER — REFUTED

Same quantifier error as item2:B5.S (TRACK_B:362). "Weaker on larger sets" presupposes |t| + r̄_n above our set sizes. For r̄_n ≤ (2A+1)s₀ + 2, permitted by (12) (supp p. 13), (A4) (READER:107–108) implies the lower half of (22) and (23) with l_n = φ₀²/2, and counterexample E shows the converse fails. The row is then ordered (ours stronger), and on every set larger than |t| + r̄_n we ask a floor ((A4), (A5)) where Theorem S asks nothing.

## item5:S.CONC — REFUTED (the clause "ours implies (24)")

**Problem.** One posterior is read against another. (24) is a statement about "the posterior probability (7) of the main text" with V_ξ⁻¹ = I or X_ξᵀX_ξ/n (supp p. 13). Its prior is (6): independent inclusion with probability r_n/P_n, truncated at r̄_n (p. 951).

Our rate concerns π of STATEMENT:21–27, which differs in each of these respects:
- the size prior is w(k) = ½/C(2p−1, k);
- the cap is K = min(p, ⌊n/2⌋), which as an r̄_n would violate (23) once P_n → ∞;
- V⁻¹ = (G_S + I)/n;
- the data are standardised and the likelihood is a working one.

Our π is not a posterior covered by Theorem S. So 1 − π(S₀ | y) = O_P(√(log n/n)) implies the ratio statement for our π only, via max_{k≠S₀} π(k)/π(S₀) ≤ δ_n/(1 − δ_n). It does not imply (24) (TRACK_B:365, :24; AUDIT.md:52; WRITING_DELTA:23–25).

**What survives.** Within one posterior, mass on the truth with a rate is a stronger form of conclusion than (24), which has no rate and does not claim π(t | D_n) → 1.

AUDIT2 item1:B4.PROOFS VERDICT=NO-FINDING
AUDIT2 item1:B4.STATED VERDICT=NO-FINDING
AUDIT2 item2:B5.S VERDICT=REFUTED
AUDIT2 item2:B6.S VERDICT=REFUTED
AUDIT2 item3:SAMP.LABEL VERDICT=REFUTED
AUDIT2 item3:SAMP.ABSENCE VERDICT=NO-FINDING
AUDIT2 item4:HEAD.ORDER VERDICT=NO-FINDING
AUDIT2 item4:HEAD.S VERDICT=REFUTED
AUDIT2 item4:HEAD.H VERDICT=NO-FINDING
AUDIT2 item4:HEAD.CONC VERDICT=REFUTED
AUDIT2 item5:S.QUOTE VERDICT=NO-FINDING
AUDIT2 item5:S.MODEL VERDICT=NO-FINDING
AUDIT2 item5:S.PRIOR VERDICT=NO-FINDING
AUDIT2 item5:S.DIM VERDICT=NO-FINDING
AUDIT2 item5:S.LOWER VERDICT=REFUTED
AUDIT2 item5:S.UPPER VERDICT=NO-FINDING
AUDIT2 item5:S.SIGNAL VERDICT=NO-FINDING
AUDIT2 item5:S.CONC VERDICT=REFUTED
AUDIT2 item5:S.CORE3 VERDICT=NO-FINDING