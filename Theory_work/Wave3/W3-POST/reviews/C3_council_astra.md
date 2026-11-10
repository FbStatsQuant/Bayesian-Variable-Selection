# Council C3 — seat A (OpenAI), final round

Reviewer: gpt-6-astra, high. Date: 2026-11-09. Paths below are relative to `Theory_work/Wave3/W3-POST/`; proof aliases are those in STATEMENT.md. Earlier reviews and dispositions were treated as claims to verify, not evidence of correctness.

**Verdict: PASS for this seat. Uncapped score: 8.8/10. All six gates PASS. Findings: 0 FATAL, 0 MAJOR, 0 MINOR, 2 NIT.** This is one seat's verdict, not a declaration that the two-seat council has passed.

| Gate | Verdict | Reason |
|---|---|---|
| G1 — correctness of every step | PASS | The formal claims in Theorem 1 items 1–7, Corollary 1R, Lemmas 1a/1a′ and Proposition LB follow from the inspected proof steps. No invalidating step or counterexample was found. |
| G2 — hypotheses used = hypotheses stated | PASS | The strong and weak floors are used on their stated ranges; the coefficient/energy restrictions and common random-design constants are preserved. The repaired REPORT now retains LB's feasible-extension domain. |
| G3 — no hidden assumptions | PASS | Contrast Gaussianity, response rescaling, reference-model feasibility, fixed sparsity for concentration, and independence in the random-design transfer are accounted for. Auxiliary comparison models outside the cap are weights, not posterior states. |
| G4 — cited lemmas have adequate status | PASS | The quoted T02/T03 registry statuses and POST status are retained. New lemmas retain “PROVED (by this seat, unchecked)” with separate check records. Conjectures and sketches are not proof inputs. C3 remains pending in the draft report. |
| G5 — constants/rates tracked | PASS | The size-tail normalisation, C′_Λ, determinant factors depending on g₀, beta-min margin, and large-underfit exponent check out. LB establishes the stated lower rate only on its explicit domain; the additional √log n remains conjectural. |
| G6 — fidelity to the method as coded | PASS | Retained-column p, standardisation, K, BB weights, H/A matrices, Q and the IG exponent agree with v3_preprocess.R and v3_score.h in real arithmetic. No sampler or floating-point guarantee is inferred. |

**Independent proof audit**

1. **Lemma 1a.** [P1]'s integrated ridge score, contrast identity, scale-event calculation, endpoint transfer, numerator identity and denominator argument support [T03R] §2. The contrast prior shape is 0.51, so 0.51+(n−1)/2=0.01+n/2. The numerator is integrated at a deterministic endpoint rate; no Gaussian law conditional on the response standard deviation is assumed. Keeping the exact prior ratio R_m cancels the reference prior weight. Restricting the variance integral to an interval of length σ*²/√n produces the √n normalisation. The split at √L and two Markov bounds produce the displayed tail bound. The cutoff substitution is correct, including zero tails. For growing reference size, (1+1/n)^(s₀/2)≤exp(1/4), since s₀≤K≤n/2. The zero extension for negative indices is now explicit.

2. **Lemma 1a′.** In `lemmas/L1a_size_tail.md:27–42`, the variational penalty is θᵀ(G_T+I)θ/n. Substitution of an exact representation gives Q_T^c≤||ε_c||²+ρ with ρ=(||μ||²+||θ||²)/n≤M+M′. This remains true for singular G_T and empty T. The denominator integral needs only that inequality and ρ≥0. Thus EΛ′≤1/√2+1/2+(M+M′)/(2σ*²), with no dependence on a hidden eigenvalue floor. The numerator and denominator random variables need not be independent. Uniformity over the stated class follows from the common constants. The bounded-coefficient consequence correctly retains the energy restriction for growing sparsity.

3. **Theorem 1 item 1.** I checked [T03R] B1–B3 and C1–C10 against [P1]/[P3]. F_w supplies the exact projection ranks and determinant lower bound for anchored unions throughout the logarithmic range. The upper smoother-difference inequality in C4 needs the normalised floor only on S₀. The stronger floor for underfits is used only when |S\\S₀|≤j₀. For larger underfits, C6(a) follows from prior ratios, determinant interlacing and monotonicity of Q, without that stronger floor. The factor (1+1/g₀)^(j/2) remains inside the geometric parameter q_n. The truncated χ² moment and prior multiplicity give EΥ^{>j₀}≤2K_{s₀,j₀}q_n^(j₀+1). Since (j₀+1)/2≥s₀(A+1/2)+1, the large-underfit contribution is O_P(n^−1(log n)^((j₀+1)/2))=o_P(r_n). The strict margin c>c₀ absorbs the factor 1−1/n in the signal lower bound. Tail, supersets and underfits therefore give the asserted rate.

4. **Items 2–4.** These can be re-derived directly without relying on a review verdict. Coordinate errors are at most δ_n; δ_n<min(q,1−q) implies exact threshold selection; δ_n<1/2 gives a unique posterior maximiser; the bounded-functional supremum equals δ_n. Boundedness of δ_n gives expectation convergence, but not an expectation rate. The HPM error bound 2Eδ_n is valid for every tie rule.

5. **Item 5.** Strict-superset control uses G, energy, the truth floor and F_w, without beta-min. Strong-signal recovery applies the small-underfit comparison to each missing strong coordinate and sums over at most fixed s₀ coordinates. Other nonzero coefficients need no lower bound. The size-tail clause follows separately. The specificity mechanism is labelled numerical/sketch evidence and is not used downstream. For E5, the leading proxy coefficient is 0.78, the proxy-plus-one-truth coefficient is 0.30, and models of size at least three have coefficient at most 0.10; the stated 0.48 gap is consistent with the O_P(√log n) remainder.

6. **Item 6 and Corollary 1R.** Conditional Gaussian noise follows from independence of ε and (X,θ*). Common constants and a common beta-min envelope allow the every-deterministic-sequence argument to imply uniform conditional tightness by diagonal contradiction. Adding P(𝒜_n^c) proves joint-law tightness. The support-size clause is now explicit. For Gaussian rows, the entrywise correlation error is O_P(√(log n/n)); multiplying by O(log n) and applying Weyl gives the stated sparse floors. The ψ_n condition makes this error o(ψ_n) and ensures nψ_n→∞. Coefficient upper bounds give energy; lower bounds give beta-min. Raw coefficients are handled on the sample-SD event with θ_lo=b_lo/2 and θ_hi=2b_hi. Removing the lower bound preserves the no-beta-min conclusions, including a design-measurable J_n(c).

7. **Item 7 / Proposition LB.** The prior ratio is (s₀+1)/(2p−1−s₀). The Schur-complement argument gives D_{S₀∪{j}}/D_{S₀}≤n+1, including singular designs, while Q decreases on adding a column. Summing the distinct feasible one-addition models gives δ≥(1−δ)(p−s₀)(s₀+1)/((2p−1−s₀)√(n+1)). The multiplicity factor is at least one for s₀≥1 and p≥s₀+1. This proves LB with precisely its stated domain. REPORT:19–20,68–70,129–132,175 and ASSUMPTION_MAP:123–129 now preserve the essential restriction. In the lemma's “in particular” sentence, s₀+1≤K itself entails s₀<p because K≤p; the standing s₀≥1 remains in force.

**Numerical, literature and status checks**

I inspected the numerical implementation and all supplied output tables. E0–E5 medians/frequencies and the size-tail diagnostic values match the quoted numbers, subject to N1 below. Signals are generated after standardising X. The code uses p=10 and 20 seeds. I independently reran `lb_check.py` and `lb_domain.py` with bytecode writes disabled: 34,920 pairs, minimum ratio **1.012988**, and the p=s₀=2 boundary example gives **6.5453×10^−10 at n=20**. I did not rerun the full E0–E5 suite; their numerical claims were checked against the supplied outputs as requested.

I extracted the three supplied PDFs locally into `reviews/C3_scratch_astra/` and checked the relevant passages. Song–Liang's separate Theorem 1/2 settings, Conditions 1–3, cap comparison and sure-screening discussion agree with the detailed comparison. NH14 Conditions 4.1–4.5 and Theorem 4.1 support the corrected residual-signal/minimum-nonzero-eigenvalue distinction, including the restored ν and κ restrictions. YWJ Assumptions A–D and Theorem 1 support the untruncated D(s*) concentration statement and its p^−1 posterior-error bound. Its faster rate uses a different prior penalty. No certification of the unavailable Song–Liang supplement, NH14 Theorem 4.2, or the YWJ mixing proof is implied.

The citation checker is accurately described as selected range/token/status checks. I read its implementation and saved 53-check, zero-failure result; I did not execute its writes to the unauthorised CITECHECK destinations. The relevant source status strings and separate check records were inspected. No status upgrade was found.

**Earlier findings: independently reconciled**

| Earlier findings | Current disposition |
|---|---|
| C1 A-F1, B-F2 | Corrected YWJ comparison; proved LB replaces unsupported optimality; growing-p √log n attainment remains a conjecture. |
| C1 A-F2/F3, B-N6 | NH and Song–Liang distinctions/qualifications restored and checked against the supplied PDFs. |
| C1 A-F4, B-N2/N3 | Reference-size, coefficient, energy, cap and threshold qualifications restored. |
| C1 A-F5/F6, B-F1/N1 | p≤10, standardised coefficient generation and refreshed numerical quotations verified. |
| C1 A-F7/F8, B-N7 | Design family moved to the bridge; deletion obstructions carry fixed margins and the appropriate remainder. |
| C1 A-F9, B-F3/F4/N4/N5 | Checker scope, p≥2, sketch labels, check records and random J_n(c) clarified. |
| C2 A-F1 | LB domain restored throughout the summary package; boundary failure independently reproduced. |
| C2 A-F2/F3/F4/F5 | NH parameters, E5 remainder, negative-index convention and stale simulation comments corrected. |
| C2 B-F1, N1–N7 | Reviewer-family attribution, item order, random support size, Condition 2 wording, table row, separate check records and boundary-evidence location corrected. The Wainwright reference is expressly marked recalled/not re-read, not represented as a newly verified theorem. |

**Findings and fixes**

**N1 — NIT — numerical maximum should name its scanned range.** `numerics/post_exact.py:206,246`; `ASSUMPTION_MAP.md:16–17`; `lemmas/L1a_size_tail.md:54`. The diagnostic scans t≤m<K, while its heading and summaries write an unqualified “sup_m Θ”. The theoretical lemma quantifies over all integer m. The reported values are valid diagnostics on the scanned range; this does not affect the proved lemma or its cutoff application. **Fix:** label the numerical statistic `max_{t≤m<K} Θ` everywhere, or extend the diagnostic to the remaining nontrivial cutoffs and regenerate the values. This is a scope label, not a failed mathematical gate.

**N2 — NIT — identify the comparator in the report's selection sentence.** `REPORT.md:165`. “Our conclusions are stronger on selection” follows a comparison involving three papers. The detailed Song–Liang paragraph in ASSUMPTION_MAP makes the intended comparison clear, but NH14 and YWJ also prove posterior model concentration. **Fix:** say “Our exact-selection conclusions are stronger than Song–Liang's main-text sure-screening conclusion.” This removes an ambiguous summary without changing any proved result or the detailed literature comparison.

Only this review and the authorised scratch directory were written. No git state changes or delegated work were performed.
