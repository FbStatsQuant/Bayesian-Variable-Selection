LOCK-WITH-AMENDMENTS

Statement-lock review of STATEMENT.md v1.0, read against the inputs named in L1_brief.md. This is a conditional lock: apply L1-1 and L1-2 before treating the statement as locked. The headline extension is mathematically supported; no new distributional hypothesis or key lemma is needed. I did not read LOG.md or the registry, run git commands, or change any input file. Input statuses are accepted exactly as quoted in the brief, irrespective of historical DRAFT labels in proof files.

## Numbered findings

**L1-1 [C] — K denotes two different quantities, making B3w(i) literally false.** STATEMENT.md:25, 40–42, 56 (also 79 and the references to K in §2). In (A4), K is a fixed tail constant; in the inherited posterior setup K is min(p_ret, floor(n/2)). Thus “s₀ ≤ K” at line 56 reads as a bound on the tail constant, which does not follow: take independent standard Gaussian columns, s₀ = 2, p = 2, and the valid tail constant K = 1. All (A1)–(A4) hold, but 2 ≤ 1 is false. The same collision obscures the meaning of “s₀ > K” at line 25.

Fix: use K_SG ≥ 1 for the fixed sub-Gaussian constant throughout (including ExSG, n₁ and all K⁴ exponents), and define K_cap := min(p_ret, floor(n/2)) explicitly in §0. Use s₀ ≤ K_cap in B3w(i) and s₀ > K_cap in the posterior convention. Read inherited R1 and m♯ with K_cap. State K_SG positive; as written a negative K also satisfies the squared MGF bound, so the remark “K ≥ 1 automatically” needs this sign convention. Choose n₁ ≥ max(3, 2s₀). This is a notation repair, not a sparsity restriction on the intended theorem.

**L1-2 [S] — Distinguish the raw bridge events from the measurable interface events, and state the dimension completion.** STATEMENT.md:47, 55–58 and the intended use at 128–130. The events E₁ and E₂(w_n) are measurable in X^r, but their intersection need not be measurable in (X, θ*), as required by W3-POST item 6. Standardisation discards sample means and column scales; θ* only recovers scales on signal coordinates. In particular, E₁'s scale inequalities for null columns are not generally determined by (X, θ*). The source B3 handles precisely this point in Step 6 and amendment A-2. The present lemma's heading identifies its events with item 6's events without recording that qualification. Also p_ret can be 0 or 1 off E₁ for discrete designs, whereas the consumed theorem uses fixed dimension p ≥ 2.

Fix: retain A_n = E₁ ∩ E₂(w_n) for its stated probability estimate, but add an interface sentence: after a measurable fixed-dimension completion outside {p_ret = p}, there are (X, θ*)-measurable events A'_n containing A_n on which the listed common-constant conditions and common BM envelope hold. Define A'_n by the support, energy, finite Gram-eigenvalue and BM inequalities of the completed pair, as in B3 Step 6; implement the completion of B3 amendment A-2. A deterministic centred standardised n × p matrix with a fixed s₀-supported truth suffices for the completion; the floor conditions need hold only on A'_n. No assumption that the original A_n is (X, θ*)-measurable should be made. Conclusions for actual outputs transfer with error at most P(A_n^c). This needs to be explicit in the assembly proof and at least accurately signposted in B3w; no additional assumption on the row law is needed.

**L1-3 [E] — Finish the off-event convention when every column is removed.** STATEMENT.md:23–26. The removed-true-column and removed-PIP conventions are appropriate and necessary. For finite n, a Rademacher design can have p_ret = 0 with positive probability. The reference to the coded posterior should not leave HPM/MPM or π undefined on that event. Fix: specify the measurable extension π(∅) = 1, HPM = MPM = ∅ when p_ret = 0 (or another explicit extension with the already stipulated δ_n = 1 and removed PIPs = 0). Response constancy has probability zero under the Gaussian noise model. This convention affects no asymptotic conclusion and should not be described as a new property of the implementation if the code rejects that input.

**L1-4 [E] — Keep the correlation normalisation honest about coefficient scale.** STATEMENT.md:20–22 and the delta over NOTATION.md:22–25. Unit diagonal is already an explicit restriction in the recorded reader theorem, so the new statement is faithful. If calling it a reduction from arbitrary positive marginal variances, also transform the coefficients: for D_σ = diag(sd(x_j)), population-standardising X^r replaces β* by D_σβ*. The inherited fixed lower and upper bounds must then apply to |sd(x_j)β*_j|, not to the original raw coefficients without qualification. Fix: add that sentence to remarks if using “without loss of generality”; otherwise the current explicit correlation-matrix assumption is sufficient. No arbitrary covariance generalisation with unchanged raw-slope bounds has been proved here.

**L1-5 [E] — Make the centre-and-scale qualifier precise in the literature comparison.** STATEMENT.md:100–102. The implication to Song–Liang Condition 1 is correct for the population-standardised centred predictors z_j = x_j − m_{n,j} here. It is not a uniform claim about the uncentred x_j with arbitrary m_n. Fix: write “for z = x − m_n (unit marginal variances here)” instead of the potentially ambiguous “standardised predictors”; this is population standardisation, not the random sample-standardised matrix X. Their Condition 1 uses the population predictor law. A proof requiring only single-coordinate (A4) works for every r, including r beyond w_n; see below.

**L1-6 [E] — Reader presentation and explanatory material.** STATEMENT.md:31, 35, 45, 49–50, 64–66. Theorem 2SG's mathematical core is a clean reader statement: four primitive assumptions and one explicit three-part rate display, with no sample-event machinery. Strip the registry-id line from the reader copy; expand (S1), (S2) there unless the shared setup is immediately available. The tail constant needs L1-1's distinct symbol. Add the short “why each assumption” explanations from TARGET.md/inherited reader text when producing READER_DELTA.md. Keep version and changed-line bookkeeping at 49–50 outside the registered mathematical span. ExSG's two explanatory consequences are valid, checked claims (inventory below), so may remain if they are included in its proof; otherwise move them to remarks.

## Answers and mathematical checks

### Theorem 2SG and W3-POST item 6

With K_SG and K_cap distinguished and L1-2 implemented, (A1)–(A4) imply the entire interface. R1 follows from (S1), (S2), fixed s₀ ≥ 1, fixed σ*² > 0, and s₀ ≤ p and floor(n/2) eventually. On E₁ no column is removed, so p_ret = p ≥ 2; the coded prior uses p_ret, which agrees there with the raw p used to compute m♯_n. Outside that event use the completion and transfer just described, not a prior formed using the raw p on the actual retained design.

The truth coefficients are deterministic by §0. The completed pair (X, θ*) is a measurable function of the raw design alone. Hence ε is independent of it, and ε/σ* remains independent with law N(0,I_n). Independence is not lost through θ* = D_xβ*/σ*, because D_x depends on the design alone. Means m_n need no bound: centring eliminates them in all bridge quantities.

B0(a) preserves the model posterior under response translation and positive rescaling. In its unit-noise model the constants in §2 are therefore in the right units. Items 1–3 of W3-POST Theorem 1, transferred by item 6, give exactly line 45; item 4 is available but not needed for these three conclusions. The joint equality HPM = MPM = S₀ follows by combining their two recovery probabilities (or from δ_n < 1/2); the simultaneous PIP bound follows from max_j |PIP_j − 1{j∈S₀}| ≤ δ_n, also valid with the removed-column conventions. No expectation rate or stronger conclusion is implicitly needed.

There is no missing probabilistic assumption after the stated model and the above repairs. The missing implementation details are the measurable interface event and fixed-dimension completion, rather than additional hypotheses on the data-generating distribution.

### B3w constants, window and probability

Write C_w = 5(A+1)(s₀+1), w_n = min(p, floor(C_w log n)). The integer floor exactly matches the quantifier in (A3), (A4); no extra sparse directions are required.

* R1 B1.2 gives s₀+j₀ ≤ (2A+2)s₀+2 < C_w log n for n ≥ 3. Thus every union S₀∪J with |J| ≤ j₀ has size ≤ w_n, after also bounding its size by p.
* R1 B1.3 gives s₀+m♯_n ≤ 3(A+1)(s₀+1)log n < C_w log n for s₀ ≤ K_cap. Thus the same is true for |J| ≤ m♯_n. When w_n = p, use |S₀∪J| ≤ min(p,s₀+|J|), not the generally false inequality s₀+m♯_n ≤ p.
* Since w_n ≤ C_w log n and log(ep/w_n) ≤ 1+A log n, w_n log(ep/w_n) ≤ C_w log n(1+A log n) = O((log n)^2). Choose n₁(s₀,A,K_SG) ≥ max(3,2s₀) such that this is ≤ c₂n/K_SG⁴ for all n ≥ n₁. Such n₁ is finite and independent of φ, b_lo, b_hi and σ*.
* B1 gives 1/2 ≤ ŝ_j² ≤ 2. Thus ||Xθ*||² ≤ 2s₀²b_hi²(n−1)/σ*² ≤ nM_E, with M_E as stated.
* On E₂(w_n), writing Λ = diag(1/ŝ_j), G_T = nΛ_T Σhat_T Λ_T ≥ (n/2)Λ_T Σ_T Λ_T ≥ nφ² I/4 for |T| ≤ w_n. Therefore λ_min(G_T/(n−1)) ≥ φ²/4 = φ₀² and λ_min(G_T) ≥ nφ²/4 ≥ φ²/8 = g₀. The latter also follows by using B2(a) with c_ψ = φ², since the fixed floor implies its weaker floor φ²/n. Both constants are conservative and valid.
* θ*²_min ≥ b_lo²/(2σ*²) on E₁, so θ*²_min nφ₀²/log n ≥ b_lo² nφ²/(8σ*²log n) = M_n → ∞. Here θ* denotes the unit-noise coefficient; one must not divide by σ*² again.
* B1 and B2-core give P(A_n^c) ≤ 4p exp(−n/(576K_SG⁴)) + exp(−10⁻⁵n/K_SG⁴). Since p ≤ n^A and K_SG is fixed, this tends to zero. The constants match exactly. A'_n inherits an upper bound on its failure probability from A_n, rather than being identified with A_n.

Thus the substantive B3w inequalities and threshold dependence are faithful. The false s₀ ≤ K_SG reading and the interface-event identification are the required amendments.

### ExSG

True. With a = Lᵀu, independence gives

E exp(λuᵀ(x−m)) = product_k E exp(λa_kξ_k) ≤ exp(K_SG²λ²||Lᵀu||²/2).

The covariance is LLᵀ by independence, zero means and unit variances. This proves the full-direction assertion, stronger than its sparse restriction. All three K_SG = 1 examples are correct:

* Gaussian: the scalar MGF equals exp(λ²/2).
* Rademacher: cosh λ ≤ exp(λ²/2), by (2k)! ≥ 2^k k! term by term.
* Uniform [−√3,√3]: its MGF is sinh(√3λ)/(√3λ). The coefficients obey 3^k/(2k+1)! ≤ 1/(2^k k!), because (2k+1)!/(2^k k!) = product_{i=1}^k(2i+1) ≥ 3^k. Thus its MGF is ≤ exp(λ²/2), including λ = 0 by continuity.

ExSG guarantees (A4), not (A3) for an arbitrary L; there is no claim otherwise. For strict enlargement beyond Gaussian rows one may take Σ = I and independent Rademacher or uniform coordinates, satisfying (A3) with φ = 1.

### Setting and strength tag

The data model and fixed-noise scale match the recorded reader setup. Naming raw dimension p is a real notation delta over NOTATION.md (where p means retained dimension), but §0 explicitly announces it; retain original column labels for S₀ and PIPs and use p_ret in the prior and cap. This is faithful on the high-probability event and well-defined off it with L1-3's convention. The unit-diagonal assumption matches the recorded reader theorem; see L1-4 for the limits of a WLOG reading.

STRONGER against the recorded reader Theorem 2 is correct after the repairs: every Gaussian row law there satisfies (A4) with K_SG = 1, and there are non-Gaussian admissible laws. A1–A3 are substantively identical and all three conclusions are identical. Nothing in the intended theorem is weaker against that reader statement. A literal identification of K_SG with K_cap would instead introduce an unintended restriction, hence L1-1 is not optional. Compared with W2-APP:POST's more general master, this statement is less general in retaining a fixed floor on all logarithmic-size sets; the vanishing-floor option is correctly disclosed as absent. The master also has additional posterior-summary conclusions not reproduced by this reader-sized claim. These are not weakenings against reader row 1.2.

### §5 literature verification

Both PDFs were accessible. I checked NH14 arXiv v1 printed p.16 (PDF page index 15), including the lemma and its introductory sentence, and Song–Liang printed p.953. The two displayed source quotations, and the additional NH14 introductory quotation, match in wording and mathematical content after ordinary transcription of typeset symbols. Theorem numbering, page references, and Song–Liang's zero-mean unit-variance Gaussian example are accurate. Sources: [NH14 v1](https://arxiv.org/pdf/1405.6545v1) and [Song–Liang, publisher article and PDF access](https://doi.org/10.1111/rssb.12095). I do not reproduce the long quotations here.

The NH14 comparison is accurate for centred isotropic rows with a uniform sub-Gaussian norm: the usual centred MGF/ψ₂ equivalence yields (A4) with a fixed multiple of that norm. Their identity covariance is a special case; the present sparse relative-variance condition admits general correlation matrices subject separately to (A3). This is an assumption comparison, not an assertion that the two papers' Bayesian conclusions coincide.

The Song–Liang implication, with L1-5's centring clarified, holds for all r, using only marginal sub-Gaussianity. For V = r⁻¹ sum_i a_i z_{j_i}, convexity of exp(t²) gives E exp(V²) ≤ r⁻¹ sum_i E exp(a_i² z_{j_i}²). The scalar MGF bound and Gaussian integration give E exp(t z_j²) ≤ (1−2K_SG²t)^(−1/2) when 0 ≤ t < 1/(2K_SG²). Choose fixed δ with 2K_SG²δ² < 1 and M ≥ −(1/2)log(1−2K_SG²δ²). This proves Condition 1 without requiring (A4) on r-sparse directions beyond the stated window.

The converse fails even for centred unit-variance bounded coordinates: let z₁ = R and z₂ = RB, with independent symmetric Rademacher R and P(B = −1) = ε_n → 0. Both coordinates are bounded by 1, so Condition 1 holds uniformly, while z₁−z₂ is zero except for a rare jump ±2 and has variance 4ε_n. Its MGF at its own standard-deviation scale cannot obey a common fixed sub-Gaussian constant. This comparison concerns (A4) alone; this particular example need not satisfy (A3). Allowing unrestricted m_n precludes the same uniform Condition 1 assertion for uncentred raw x.

The statement that no verified BVS precedent with general correlation was found is a report about the lead's search, not a universal mathematical nonexistence claim. I verified the two named positive anchors; I did not independently establish exhaustiveness of that search or check the other negative references, which the brief does not require.

### Inventory of interpretive sentences inside §§1–3

I use the broad reading requested in the brief, including equivalence/application parentheticals, not just sentences containing “hence”.

1. **§1, line 44: “under the joint law of design and noise.” — CHECKED.** This specifies the law of the claimed rates, and follows by item 6 with L1-2's interface construction. It belongs in the mathematical conclusion.
2. **§2 heading, line 47: identification with item 6's events. — AMEND.** The raw events are sufficient bridge events, not necessarily measurable interface events. L1-2 provides the correction.
3. **§2, lines 49–50: “Copy of … with the window changed …; changed lines marked …”. — MOVE OUT / EDIT.** This is provenance and proof-edit bookkeeping. Mathematically this is a restricted adaptation of B3 (other constants, assumptions and delivered clauses are specialised too), not a literal copy with only a renamed window. I checked the underlying source bridge, not an assertion that the future marked proof file exists and matches.
4. **§2, line 53: “computed with p and s₀”, and “in the unit-noise model … (coefficients β*/σ*)”. — CHECKED.** These specify the cutoff and scale convention and may stay; use p = p_ret on the bridge event, and the completion for item 6. B0 supplies the response-scale invariance.
5. **§2, line 56: “no column … is constant … (p_ret = p)”. — CHECKED.** Positive sample variances on E₁ prove the equivalence. The attached support/cap clause needs L1-1's amendment.
6. **§2, lines 57–58: descriptions as (E), (F_λ), (F_w), BM-∞ with a common envelope, and the probability limit. — CHECKED WITH L1-1/L1-2.** These are substantive claims, verified in the calculations above; keep them in scope and prove them. M_n → ∞ is valid since b_lo, φ and σ* are fixed positive constants.
7. **§3, lines 64–65: “so (A4) holds with this K.” — CHECKED.** Full-direction MGF control implies its restriction to the specified sparse directions. Include this sentence in the ExSG proof or move it to remarks.
8. **§3, lines 65–66: “In particular K = 1 …” for Gaussian, Rademacher and uniform coordinates. — CHECKED.** All three scalar inequalities are proved above; include them in ExSG's proof if the sentence remains registered.

The remaining sentences in §§1–3 are hypotheses, definitions, registry metadata or direct mathematical conclusions, not unexamined interpretive riders. Registry metadata should be excluded from reader text. No interpretive claim in these spans needs a new data-generating hypothesis.

### Readability and disposition

The intended Theorem 2SG passes PROGRAM.md's reader-statement standard once K is unambiguous: it uses familiar primitive assumptions, separates bridge machinery into a lemma, and gives explicit rates. The source setup must accompany the abbreviations for the model and method. Keep the short motivation for the new tail assumption in the reader remarks and preserve the explicit distinction between this reader claim and the more general master.

Disposition: apply L1-1 and L1-2 before lock; incorporate L1-3–L1-6 as the indicated convention/editorial clarifications. No expansion of the authorised theorem scope is required.
