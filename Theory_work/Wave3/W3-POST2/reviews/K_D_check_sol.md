# Cross-family line-by-line check of Claim D

**Verdict: VERIFIED-WITH-AMENDMENTS.**

Reviewed `lemmas/D_hellinger.md` against STATEMENT v1.1 and the specified source snapshots. No counterexample to D(a) or D(b) was found. D(a) is verified. D(b)'s argument is valid after making the stronger projection-noise event explicit; as written, its claimed deterministic bounds on the named event are not justified. The correction uses an already proved Gaussian union bound and adds no design or beta-min assumption. The comparison remark needs a qualification of its quoted rate.

Locations below are relative to `Theory_work/Wave3/W3-POST2/` unless a source alias is given. [P1], [P3], [T03R], [W3P] refer to the exact files specified in the review brief. No proof or statement files were edited.

## Numbered findings

1. **MAJOR — A stronger event than the defined (G2) is used in D(b).**

   **Location:** `lemmas/D_hellinger.md:60–68`, especially line 62; event imported by `STATEMENT.md:17–19` from [P3] §`sec:good`.

   Line 62 asserts that (G2) gives
   
   `‖P_S e‖² ≤ σ*² C_A |S| log n`.
   
   However, the actual definition of (G2) in [P3] `PROOF_v2.tex:177` only requires
   
   `‖P_T e‖² ≤ σ*² C_A (m_n+s₀) log n`
   
   simultaneously for `1 ≤ |T| ≤ m_n+s₀`. [T03R] (C2), lines 174, and A's event definition do not explicitly replace this clause by the sharper one. The difference matters: the defined cutoff is O(log n), so substituting its stated bound gives an O((log n)²) fitting-error bound, insufficient for lines 63 and 70–73. The same stronger bound is used for the projection subtraction in line 66. Thus the displayed constants are not established on precisely the event named at lines 60 and 74–75.

   **Proposed fix:** Introduce explicitly the stronger event
   
   `G2* = {‖P_T e‖² ≤ σ*² C_A |T| log n for every nonempty T with |T| ≤ m♯_n+s₀}`.
   
   [P3] `PROOF_v2.tex:190` proves exactly this event with exceptional probability at most `1/n`: for size k take `x_k=k(log p+1)+log n`, sum `e^(−k)/n`, and use `2k+3x_k ≤ C_A k log n`. Replace (G2) by G2* in the event used locally in D(b). Because G2* implies the original (G2), all preceding comparisons remain available, and the total exceptional probability remains `6/n` when this replacement is made in the original probability accounting. Alternatively intersect with G2* as an extra event and change the displayed bound to `7/n`. The former repair preserves all stated constants and rates. No new hypothesis is needed.

2. **MINOR — The primed assembly lemma is attributed to a file that has only its unprimed predecessor.**

   **Location:** `lemmas/D_hellinger.md:53–56`.

   The text says `[T03R] (C8′)`. That file has (C8), at `PROOF.md:194–197`, with Υ rather than Υ′ and with the older eigenvalue-based superset estimates. Under the present (OS) assumptions, it is the primed replacement in `lemmas/A_occam.md:74–76`, using (C5′), that is needed. [T03R] (C8) alone does not establish the asserted rate under (OS).

   **Proposed fix:** Cite `A_occam.md (C8′), replacing [T03R] (C8)` at both uses. E's assembly at `lemmas/E_visibility.md:50–54` also spells out the same primed argument. Define `max ∅ := 0` when introducing κ, as [P3] line 317 does, to cover an empty bounded-excess part of U_far.

3. **MINOR — Qualify the Song–Liang corollary rate and identify the normalization.**

   **Location:** `lemmas/D_hellinger.md:78–80`.

   The central comparison is faithful: the PDF's Theorem 1 (printed p. 952) defines an integrated distance against the design law and gives the displayed exponential posterior-tail/probability bound; Theorem 2 (printed p. 953) gives the analogous result under Condition 1, strict sparsity, and its other hypotheses. But the first rate in Corollary 1 is conditional on its logarithmic model-size branch. On printed p. **954**, the corollary assumes `P_n < exp(C n^α)`, covariance-eigenvalue envelopes, strict sparsity, and chooses `r_n < r̄_n ≺ log^k n` for that branch. It also gives a different polynomial-size branch. The symbol ξ used in D's quotation is not identified with the paper's α. Moreover, the paper uses `d²=∫(√f−√f*)²`, whereas D uses `H²=1−∫√(ff*)`; their squared distances differ by a factor of two when compared under the same averaging/integration convention.

   **Proposed fix:** Write: “Under the logarithmic model-size branch and the hypotheses of SL Corollary 1 (printed p. 954), with `P_n < exp(C n^ξ)`, one can take `ε_n=O(n^{−(1−ξ)/2}(log n)^{k/2})`. SL's distance uses `d²=2H²`.” Keep the existing fixed-design/in-sample versus integrated-design distinction. The normalization has no effect on rates; this is a qualification of the comparison, not a defect in D0 or D(a)/(b).

4. **NIT — An unexplained additive term in the Q bound is harmless but should be removed.**

   **Location:** `lemmas/D_hellinger.md:66`.

   The term `+2 log n` is not required by the named (G1), which already states `|‖e‖²−Nσ*²| ≤ 3σ*²√(N log n)` ([P3] line 176). If intended to come from the raw chi-square inequality, that inequality's extra term is `2σ*² log n`, and its leading square-root constant is 2 before absorption into 3 ([P3] line 188). As a gratuitous positive addition the term printed here does not invalidate the upper bound, and it is still absorbed eventually for fixed positive σ*².

   **Proposed fix:** Delete `+2 log n` and use (G1) exactly as stated. No downstream constant needs changing.

## Verification record by attack point

### Parameter posterior and geometry (lines 7–10)

Verified exactly, not merely at the model-marginal level. [P1] `thm:T01i`, `PROOF_v3.tex:173–208`, explicitly proves equality of the **joint transformed posterior** and Π_b, with `b=b₀s_y²`, including the Jacobian and the change from the n-dimensional working likelihood to the contrast model with IG prior shape 0.51. It states both conditionals at line 178. `prop:closed`, lines 155–170, independently provides the normal and IG conditionals. There is no missing extra half-degree-of-freedom correction: `ν=0.01+n/2` is correct.

Since the fitted mean and truth here are centered, `X_S=UX_{c,S}`, `μ=Uμ_c`, and `UᵀU=I_N`; consequently the norm identity in line 10 is correct. It would not describe an unknown uncentered intercept, but D explicitly restricts the target to the centered mean. No out-of-sample assertion follows or is used.

### Lemma D0 (lines 11–16)

Every formula and inequality is correct for `v,w>0` under D's stated Hellinger normalization. The affinity is `(2√(vw)/(v+w))^{1/2} exp(−(a−b)²/[4(v+w)])`. Both A and B lie in [0,1]. The decomposition of `1−AB`, the bound `1−e^(−t)≤t`, and all three inequalities for `1−A` hold. Averaging gives the displayed `1/(4nσ*²)` constant without an independence assumption across the centered observations: this is a distance between one-observation laws averaged over design points, not a product-law calculation.

### Lemma D1 (lines 19–30)

Verified under the ambient energy hypothesis (E), which supplies `‖μ‖²≤nM` in part (b). If D1 is meant to stand alone, explicitly repeat (E) in its statement.

- (a) Posterior covariance gives `v tr(M_S)`, not `v tr(M_S²)`. [P3] `lem:smoother`(a),(b), lines 94–108, establishes the common eigenvectors and `0⪯M_S⪯P_S`; the trace bound follows.
- (b) The three-term decomposition is exact. The spectral estimate `1−h(λ)≤2/(n+1)` follows for `λ≥1`; hence the squared shrinkage contribution is at most `4nM/(n+1)²≤4M/n`. Multiplication by 3 gives `12M/n`. The empty model satisfies the inequality as well.
- (c) The IG moments are correct for `ν>2`; all asymptotic uses allow n sufficiently large.
- (d) [P1] `lem:spec`(b),(c), lines 90–110, gives precisely the residual lower bound and the upper remainder with `γ≤2/(n+1)`. For S empty the result is equality before adding the nonnegative remainder.

### D(a) (lines 33–46)

Verified. (F₀) gives full rank s₀, so `‖P_{S₀}e‖²/σ*²` has the claimed chi-square law and the residual has `N−s₀` degrees of freedom. [P1] `lem:den`, first proof paragraph at lines 337–338, gives the residual-plus-shrinkage bound; [P1] `thm:T01iii`, lines 234–250, implies `s_y²=O_P(1)` under (E). Thus

`Q^c_{S₀}=Nσ*²+O_P(√n)`, `b=O_P(1)`,

`E[v|S₀,y]=(Q^c_{S₀}+2b)/(n−1.98)=σ*²+O_P(n^{−1/2})`.

The exact variance is `(Ev)²/(n/2−1.99)`, at most `4(Ev)²/n` eventually. Chebyshev must be applied around Ev with the random centering error handled using `√n(Ev−σ*²)=O_P(1)`; this justifies the claimed convergence for every diverging M_n. No unjustified fixed-centering Chebyshev step is necessary. The coefficient implication is valid after zero-padding on S=S₀, with `N/n≥1/2`. The final D0 event inclusions and constants are correct.

### D(b): partition and far-underfit mass (lines 49–59)

Verified after correcting finding 2's citation. Every nontruth model is a large model, a strict superset, or an underfit; the latter is near or far according to the displayed alternatives. The cutoff observation can be justified directly: for any fixed integer B, uniformly when `K>B`, `R_B≥q_{B+1}/w(s₀)` is bounded below by a positive constant depending only on B,s₀ (the fixed-index BB size ratios are bounded below for p≥B+1 and `w(s₀)≤1/2`). It cannot meet the vanishing cutoff threshold. Thus eventually either `m♯_n≥B` or the cap has already been reached; take `B=s₀+j₀−1`.

Tail control is [T03R] T02(i♯), lines 79–85; it uses only (E),(F₀),G here. Strict-superset control is A's 5(a), lines 82–83; it uses (OS),(E),(F₀),G and does not use beta-min.

For the bounded-excess part of U_far, its definition itself supplies `Δ_S≥L*σ*² log n`. [T03R] (B2), lines 140–143, supplies the floors for S and S′; (C3), line 176, supplies the restricted denominator bound; (C6)(b), line 190, supplies the sharp comparison. [P3] `lem:signalgain`, lines 303–311, uses these and (G4), not beta-min. The only beta-min use in the original Step 1, lines 342–348, is to *derive* the discrepancy lower bound, which is already supplied here. With `L*≥4C_*` and `L*/32≥s₀(A+1)+2`, its exponent is at most `ρ_n−2 log n`. For large excess, (C6)(a) is unconditional. The primed (C8′) and (OS) therefore give `π(U_far)=O_P(n^{−2}+r_n)` without (F_w), (ID), or beta-min. No hidden beta-min dependency was found.

### D(b): uniform bounds and constants (lines 58–75)

After finding 1's event repair, the remaining calculation is verified. (F_λ) and interlacing give the floor on all near models, which have bounded size. E's cross-term event at `E_visibility.md:13–23` applies to every underfit in the near family; for S₀ the cross term is identically zero. Its counting and `x_n≤C_x log n` are correct and give exceptional probability at most 1/n.

In the Q bound, the substantive terms are respectively the (G1) norm fluctuation, projection subtraction bounded on G2*, twice the cross term, discrepancy, and D1(d)'s remainder bounded by `8(M+σ*²)`. All except the leading square-root fluctuation are O(log n) uniformly with fixed constants, so they fit within the additional `σ*²√(N log n)` for n sufficiently large. Finding 4's extra term does not change this fact.

Writing `a_S=E[v|S,y]` gives the exact identity

`a_S−σ*²=[Q^c_S−Nσ*²+2b+0.98σ*²]/(n−1.98)`.

Consequently the uniform constant 5 in line 68 follows from the constant 4 for Q, and `a_S/σ*²→1` uniformly on the repaired event. The exact variance `a_S²/(n/2−1.99)` is then at most `4σ*⁴/n` eventually (its leading constant is 2). There is ample slack; replacing the earlier variance bound by `4a_S²/n` and then merely using `a_S≤2σ*²` would be too crude to recover the printed 4, but the exact formula does recover it.

Put `B=σ*²[C_A(s₀+j₀)+L*]`. Then `m_n^{fit}=3B log n+12M/n` and the chosen `C_H≥12B+1` gives `2m_n^{fit}≤C_H log n/2` eventually, since `24M/n≤(log n)/2`. Also `C_H≥6` leaves a unit standard-deviation-scale gap beyond the centering bound 5. Chebyshev gives `4/log n`; Markov with `Ev≤2σ*²` gives exactly the last constant on line 73. Summing the two conditional tails, rather than taking their maximum separately, is still O(1/log n). Finally D0 gives precisely `C_H′=C_H²+C_H/(4σ*²)` off Bad_b. The threshold n₀ can absorb all fixed constants, including M and φ₀; C_OS affects only the vanishing mass outside the retained family, not C_H.

### Remarks and source fidelity

[W3P] §0 confirms all data conventions and the working posterior; §2 R1 fixes s₀ and σ*², and item 6 provides the stated random-design interface. These are consistent with the uses in D. The SL PDF was read via local `pdftotext -layout` extraction, saved only in the allowed scratch directory. Its Theorems 1–2 support the qualitative comparison, subject to finding 3. The N7 tables in `numerics/post2_checks_out.txt:88–107` support the reported finite-grid weak-signal mean-loss behavior and approximately constant oracle Hellinger upper-bound diagnostic. They are numerical evidence, not an analytic minimax lower bound; D's wording explicitly identifies them as numerics. The final restriction excluding expectations of unbounded losses is appropriate.
