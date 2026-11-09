# R04 — Cross-family check of L4

**Verdict: VERIFIED-WITH-AMENDMENTS.**

I checked L4 against L1, the explicitly defined event in L3, locked claim (C2), and the local-search/scored-set/tie rules in `02_method.tex:463–495`. I found three false displayed inequalities and some endpoint/nondegeneracy bookkeeping that should be corrected before marking the proof checked. Each admits the explicit repair below without changing the event, hypotheses, or conclusion. I found no fatal obstruction and no asymptotic counterexample to (C2). The existing proof should not be accepted literally unchanged.

Line references below are to the reviewed version of `lemmas/L4_path.md` (201 lines).

## Issues and concrete repairs

1. **Lines 84–85: the small-p inequality `(2H̄ + C L_n)^2 ≤ 9H̄²` is false. Genuine algebra/uniformity error; nonfatal.**

   For bounded p, H̄² = O(L_n), whereas E1 permits the common Gaussian and truth coordinates to have size proportional to L_n. Thus the left side can be of order L_n² and cannot be bounded by a constant times H̄². This is not merely an excessively loose sufficient estimate: E_n permits actual null distances of order L_n.

   For example, take p = 2, s₀ = 1, separate singleton blocks (so N₀ is empty), ρ = 1/2, σ = 1, and a fixed nonzero truth. Set the common Gaussian to 0.9L_n, the truth's ξ to −0.9L_n, and the null's ξ to 1. Then the truth's g-coordinate is zero, ϱ = 0.9L_n + o(1), and at the initial k = 2 state x = −0.6L_n + O(1). The null distance squared is 0.36L_n² + O(L_n), exceeding 9H̄² for large n. Choose r = n − 1 − gᵀΣ⁻¹g; this satisfies E2 for sufficiently large n. E1, E3 and E4 hold, and E5–E7 do not apply in this regime. Small perturbations give the same violation. This breaks the displayed estimate, not the path conclusion.

   **Fix:** retain `|τ| ≤ 2H̄ + C L_n` but bound it directly by

   `(2 sqrt((log n)/90) + C L_n)^2 ≤ 0.1 log n`

   for sufficiently large n. Here C is fixed and L_n/sqrt(log n) → 0, uniformly over the small-p regime. The claimed deletion/addition/swap margins then follow as stated, including bounded p and N₀ coordinates. No comparison of L_n with the actual H̄ is needed.

2. **Line 104: the justification `m ≥ m₁ ≥ 4x_J` is false uniformly in J. Genuine missing count argument; nonfatal.**

   J may be of order p near the initial state. Then x_J is of order log n, whereas m₁ is only 250000 log log n. Increasing n does not make m₁ ≥ 4x_J true. The preceding inequality `J ≤ 4m + 4x_J` is valid, but does not imply the next displayed conclusion by the reason given.

   **Fix:** first observe that x_u/u is decreasing for sufficiently large u. If J ≥ 5m and m ≥ m₁, then, uniformly,

   `x_J/J ≤ x_{5m₁}/(5m₁) < 1/20`.

   Substitution into `J ≤ 4m + 4x_J` gives `J < 4m + J/5`, hence J < 5m, a contradiction. Therefore J < 5m. This establishes the needed count without assuming it or comparing m₁ to x_J. The sign comparison immediately before it is correct: when x > Δ/2, b > |a|, K⁰ contains exactly the retained negatives, and K⁰ minus K consists only of positive coordinates, so s_K ≤ D_J. The negative-x argument is its deterministic sign reversal.

3. **Line 128: the second inequality in the Young-bound chain is false as displayed. Genuine constant error; nonfatal.**

   The intermediate expression has the leading contribution `η(1+η) log n`, not `η log n`. The excess cannot always be absorbed by the displayed extra η times `log(2m₀/m) + 2 log log n`. For example, let p be asymptotic to n/2 and m be asymptotic to n/log³ n. Write t = log n. Then Z² = 10 log t + o(1), and the intermediate expression minus the claimed right side is

   `η² t − 5η log t + o(t) > 0`.

   A direct scalar check at t = 10¹⁰ gives an excess of approximately 3,999,997.7. Consequently this particular chain cannot justify the margin.

   **Fix:** apply Young's inequality with parameter 2η instead. With A := log(2m₀/m) + 2L_n and H² ≤ 2 log(n+2),

   `½(Z + ηH)² ≤ (1+2η)A + (η/2 + η²) log n + o(log n)`.

   Uniformly in this subcase, the multiplier and γ corrections contribute o(log n). Since η/2 + η² < η, they can be absorbed into the available fixed slack to recover the final bound claimed on line 128. Thus its final bound is valid, although the written intermediate chain is not. For additions the analogous parameter 4η gives `(1+4η)A + (η+4η²)log n + o(log n)`, bounded by `(1+4η)A + 2η log n` eventually. These repairs retain the stated 0.35 deletion and −0.3 addition margins. The swap margin also survives.

4. **Lines 92–120: the induction order and its inclusion of i* need correction. Endpoint/presentation issue; nonfatal.**

   B3 at i uses B2 at i; B2 at i uses B1 at i; B1 at i uses B3 at i−1. This is a valid induction in the order **B1, B2, B3, B4**, rather than the written order. More concretely, Claim B includes i = i*, where m_i = m₁−1, but the B3 proof invokes m ≥ m₁. At that same step, line 118 has N₊ = m₁−1, not N₊ ≥ m₁.

   **Fix:** state Claim B for i < i*, and use the drift estimate on lines 144–145 for entry into the end phase. The proof does not require B1–B3 at i*. Alternatively, extend the estimates explicitly to m₁−1 and replace the lower bound in line 118 by m₁−1; the slack suffices. Neither repair changes the argument. The initial state is valid: m₀ grows at least polynomially in regime (L), x₀ → 0 uniformly, and E6 supplies both sides.

5. **Lines 12, 55–69, 194–197: include centre/coordinate equalities in the probability-one exclusions. Nondegeneracy/presentation issue; nonfatal.**

   Distinct ξ coordinates and absence of an a/b distance tie do not themselves exclude ξ_j = x_T. Such a configuration can have a_T = x_T, contradicting the strict gap inequality in locked (C2)(iii). At that point one of the strict drift inequalities in L4.1's proof is also unavailable. L3 also treats absolute order statistics as uniquely ordered, which requires excluding absolute-value ties, rather than only coordinate ties.

   **Fix:** explicitly intersect with the probability-one event `ξ_j ≠ x_T` for every relevant T,j and `|ξ_j| ≠ |ξ_l|` for distinct nulls, in addition to the listed distance ties. Each added equality is a nontrivial linear relation (or a union of two such relations), and there are finitely many per n. With these exclusions, the strict initial/one-sided gap statements match (C2). The deterministic interval identity and empty-side persistence themselves remain valid even for a zero-distance deletion, using weak inequalities where appropriate.

6. **Lines 147–169: make the one-sided end-phase justification and the scope of the magnitude replacement explicit. Presentation issue; nonfatal.**

   With extended endpoints, the desired condition is still a < 0 < b when a = −∞ or b = +∞. For example, a = −∞ and b ≤ 0 would retain every positive original null and therefore force m ≥ m₀/3, impossible in the end phase. The symmetric case is identical. Thus L4.1(iii) really does give the asserted Top± structure after a side empties.

   The phrase on line 154 that replacing magnitudes by H̄ changes *any* τ² by O(H̄δ_e) is too broad: an outside null can have ξ_l near zero, whose replacement by ±H̄ changes its square by order h. The small-error replacement applies to **retained nulls**. Outside coordinates are bounded by the interval [−H̄,H̄]; E-add uses an upper envelope and E-swap uses convexity, so neither calculation requires this false replacement for outside coordinates.

   Also justify the absolute-value estimate in E-side. Put B := s_{S₀}−ϱ = O(L_n). Since |B| = o(H̄),

   `|x| ≤ (mH̄ + |B|)/(m+s₀+κ) < H̄`,

   and `H̄−|x|` is uniformly much larger than δ_e for m < m₁. Consequently each retained positive lies above x and each retained negative below x. The majority-side distance comparison then holds exactly as intended. Replace the assertion of an exact symmetry under ξ ↦ −ξ by a deterministic sign reversal of ξ **and the offset ϱ** in these bounds; reflecting ξ alone does not exactly negate ϱ when the fixed truth sum is nonzero.

7. **Lines 3–7: the cited diagnostics do not test the proof's actual bulk threshold. Evidence-description issue; nonfatal.**

   `n5_invariants.py` passes m₁ = 20, whereas L3 fixes m₁ = ceil(250000 log log n). Its listed p ≤ 20000 runs therefore do not test the theoretical bulk/end split, entry imbalance, or the bulk invariants at that split. The N6 output also contains a finite-n non-pure path with N₀ nonempty (ρ = 0.3, n = 20001, p = 10000, s₀ = 1, seed = 2). This does not contradict an asymptotic theorem; at those dimensions E6 with the specified m₁ is impossible. It should not be used as evidence of a counterexample on E_n.

   **Fix:** label N5 as an exploratory threshold-20 diagnostic and distinguish it from verification of the proof's constants. No new simulation is needed for the analytical repairs above.

## Checks that did not reveal an obstruction

The centre and drift formulas on lines 24–27 follow exactly from L1.4. The deletion/addition/swap gain formulas and the logarithmic inequalities are correct in their stated domains. L4.1's interval induction works with infinite endpoints: deleting the nearest point moves the centre away from the deleted side and cannot cross the other endpoint because k−1+κ > 1. If a side is empty it stays empty. For two finite sides, the asymmetry recurrence is exactly the stated one; the next outward point is consecutive in the original ordered sample, so L3(c2) supplies its gap bound. The hole bound D⁺ < max(L,R) is valid whenever the hole is nonempty; an empty hole simply supplies no candidate additions.

The multiplier bounds correctly use r with residual dimension **n−1−p**. In particular p near n/2 permits M_T near 1, so replacing it globally by 1/2 would be incorrect; L4 does not do that. In the large-m subcase Z² ≤ 10L_n, and the stated 0.01 deletion cost, −0.45 addition margin, and 0.07 swap bound hold eventually. In the smaller-m subcase the energy condition implies the required uniform M_T ≤ 1/2(1+O(1/log n)); issue 3 repairs its one invalid arithmetic chain. N₀ coordinates are controlled by E1: L_n = o(H) uniformly in regime (L), so their addition/swap bounds fit the margins in both subcases. Truth moves satisfy TL: their squared distances are order n, the /9 constant is valid eventually, and γ_k < 1 makes the truth-out swap negative.

For the end phase, e_n = O(L_n), e_n/H̄ = o(1), and the entry bound gives |I|/(k+κ) ≤ 2η+o(1). The majority-side deletion lowers |I| by one, except that a balanced state moves to |I| = 1; for |I| ≥ 2 the ratio cannot increase. The leading deletion cost is

`½h (k+κ−I)² / ((k−1+κ)(k+κ))`,

the addition upper cost is

`½h (k+κ+|I|)² / ((k+κ)(k+κ+1))`,

and the opposite-endpoint swap value is

`4h(σI−1)/(k+κ)`.

All three expansions have the correct signs and constants. The same-side swap endpoint has only the retained-magnitude approximation error. Negative swap values can be dismissed directly; the positive logarithmic upper bound is only needed when V ≥ 0. The one-extra state has |I| = 1; the two-extra balanced state has k−1+κ ≥ s₀+1+κ₀. Thus the critical constant is indeed

`c_D = 1/2 − 1/(s₀+1+κ₀) > 0`.

For s₀ = 1 this equals `(1−ρ)/(2(1+ρ))`. It becomes small as ρ approaches 1, but ρ is fixed and n₀ may depend on it, so the proof needs no uniformity as ρ → 1. At S₀, I = 0, additions have the asserted negative margin and TL handles all truth deletions/swaps, including swaps into N₀. The m₀ = 0 case is already covered by the small-p argument.

The errors are uniform along the path after the amendments. In the end phase, H̄e_n = O(sqrt(log n) L_n) = o(log n), H̄δ_e = O(L_n), hε′ = O(1) using the small-set multiplier bound, and the positive logarithmic Taylor errors are O(log² n/n). In the bulk, γ ≤ 1/m₁ and the multiplier errors tend to zero uniformly in their respective subcases. There is no accumulation over the number of moves: these are simultaneous, statewise bounds. One may take a common addition constant, for example `c = min(0.1, c_D/2)`, after increasing n₀.

The resulting strict move comparisons make the scan's lexicographic tie rule irrelevant on the augmented nondegeneracy event. Every null deletion other than the nearest has strictly smaller gain. The complete frozen-centre scans and final extra scan match the method specification; the certified endpoint and the scored-set cap consequences in (C2) follow.

For independent arithmetic diagnostics I ran inline Python with bytecode writing disabled: it confirmed issue 3's false intermediate bound and checked the leading end-phase deletion/addition/swap comparisons over ρ ∈ {0.01, 0.3, 0.9, 0.99, 0.999999}, s₀ ∈ {1,2,4}, 1 ≤ m ≤ 300, and parity-compatible imbalances satisfying the proved ratio restriction. No violation occurred in that check; its smallest normalized margin was approximately 2.50000125·10⁻⁷, consistent with c_D at s₀ = 1, ρ = 0.999999. These arithmetic checks supplement the algebra and are not a substitute for it. No source files or existing numerical outputs were changed. No git commands were run.

**Fatal issues: none found. Required before acceptance: repair issues 1–5; clarify issues 6–7.**
