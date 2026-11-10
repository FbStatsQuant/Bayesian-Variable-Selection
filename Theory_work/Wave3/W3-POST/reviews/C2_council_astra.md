# Council C2 — seat A (OpenAI)

Reviewer: gpt-6-astra, high. Date: 2026-11-09. Reviewed STATEMENT v1.3 and the package on disk. Earlier verdicts and dispositions were treated as claims to check, not mathematical evidence.

**Verdict: NOT PASSED. Uncapped score: 8.3/10.** The formal results survive this audit. One new report-level overstatement blocks package approval: REPORT drops the essential admissible-extension hypothesis from Proposition LB and states a false universal lower bound. Counts: **0 FATAL, 1 MAJOR, 1 MINOR, 3 NIT**. This is a local repair, not a request to redo the concentration proof.

Paths below are relative to `Theory_work/Wave3/W3-POST/`; source aliases are those in STATEMENT.md.

## Six gates

| Gate | Verdict | Reason |
|---|---|---|
| G1: correctness of every step | FAIL | Formal proofs pass; REPORT's universal LB assertion is false (F1). |
| G2: hypotheses used = hypotheses stated | FAIL | REPORT omits LB's extension condition; the detailed NH14 Condition 4.5 summary also omits its parameter restrictions (F2). |
| G3: no hidden assumptions | FAIL | Reading REPORT alone silently requires a feasible strict superset of the truth for its lower-bound claim. No additional hidden premise was found in the formal statements. |
| G4: cited lemmas have adequate status | PASS | Registry quotations match; POST and the new lemmas retain their unchecked status strings with separate review records. C2 remains pending. Heuristics are not used in the concentration proofs. |
| G5: constants/rates tracked | PASS | Formal constants, cutoff normalisation, superset factors, underfit exponents, and LB's constant check out. The lower-bound scope error is charged to G1–G3. Numerical quotes agree with current outputs. |
| G6: fidelity to the method as coded | PASS | Retained-column p, cap, BB weights, ridge score, standardisation, and IG exponent match the real-arithmetic target. No sampler or floating-point equivalence is inferred. |

The score exceeds 8.0, but the all-gates requirement is not met.

## Independent mathematical audit

**Lemma 1a.** I checked [P1]'s slab integral, contrast transformation, scale event, mixed-endpoint transfer, numerator identity and denominator integral, then [T03R] §2. Contrast dimension n−1 requires IG shape 0.51, preserving exponent 0.01+n/2. The random response scale is handled pointwise by deterministic endpoint bounds; the numerator identity is used only at a data-free rate. Retaining the exact prior ratio R_m cancels the reference prior weight. Integrating over `[σ*², σ*²(1+n^−1/2)]` supplies the √n normalisation. Splitting `c♯ exp(Λ) Θ^(1)` at √L gives exactly the displayed probability bound and C_Λ. Substitution of the cutoff proves the asserted order. Even when s₀ grows, `(1+1/n)^(s₀/2) ≤ exp(1/4)` since s₀≤K. See F4 for a harmless negative-index definition omission.

**Lemma 1a′, line by line.** In `lemmas/L1a_size_tail.md:26–41`, the variational formula has penalty `θᵀ(G_T+I)θ/n`. Substituting the exact representation gives `Q_T^c ≤ ||ε_c||²+ρ`, where `ρ=(||μ||²+||θ||²)/n≤M+M′`. This holds for singular G_T and for T empty. In [P1]'s denominator integral the only needed properties of the replacement term are this upper bound and nonnegativity. Consequently `EΛ′≤1/√2+1/2+(M+M′)/(2σ*²)`. The determinant upper bound needs no floor. The numerator mixture identity and endpoint transfer then give the stated uniform bound, without independence between Λ′ and the numerator variable. The coefficient-bounded consequence retains the necessary energy condition for growing sparsity.

**Theorem 1 item 1.** I checked [T03R] B1–B3 and C1–C10 against the corresponding [P1]/[P3] proof steps. The weak floor gives full rank and the determinant lower bound on large anchored unions; only the truth floor is used for the upper smoother difference in C4. The stronger normalised floor is needed only for small-extra-variable underfits. C6(a) uses monotonicity and determinant interlacing, so does not secretly require the stronger floor on large unions. Auxiliary weights outside Ω are legitimate. The truncated χ² moment gives the factor `(1+1/g₀)^(j/2)` inside q_n; it is not absorbed into a j-independent constant. The large-underfit term is bounded by `n^−1(log n)^((j₀+1)/2)=o(r_n)`, since `(j₀+1)/2≥s₀(A+1/2)+1`. For c>c₀ the factor 1−1/n is absorbed eventually. Tail, supersets, and underfits therefore establish the claimed rate.

**Items 2–4.** Re-derived directly: each coordinate error is at most δ; δ<min(q,1−q) gives exact threshold selection; δ<1/2 gives the unique HPM; the bounded-functional supremum equals δ. Boundedness of δ gives expectation convergence, with no claimed expectation rate. The Markov HPM inequality is correct for any tie rule.

**Item 5.** The strict-superset argument in [T03R] §5/[P1] T02(ii) needs no beta-min and no normalised floor beyond S₀. For strong signals, apply C10 to each missing strong coordinate and sum over at most fixed s₀ coordinates; no lower bound on the other coefficients is used. Size tails are supplied separately. The specificity discussion is explicitly numerical/sketch evidence and is not a premise in any proof. Its leading score coefficients are consistent with the stated mechanism; F3 concerns the remainder notation only.

**Item 6 and Corollary 1R.** The every-deterministic-sequence argument with common constants/envelope yields uniform conditional tightness by a diagonal contradiction. Independence of ε from (X,θ*) supplies the required conditional Gaussian law. For Gaussian rows, entrywise correlation error `O_P(√(log n/n))`, multiplication by O(log n), and Weyl give the stated floors. The LSF(ii) rate makes the error o(ψ_n) and nψ_n diverge. Bounded standardised coefficients give energy; the positive lower bound gives the common BM envelope. For raw slopes, the sample-SD event gives θ_lo=b_lo/2 and θ_hi=2b_hi. Removing only the lower bound preserves floors and energy, so the no-beta-min transfer is valid, including design-measurable J_n(c).

**Item 7 / Proposition LB, every proof step (`lemmas/LB_rate_lower_bound.md:17–29`).**

1. The posterior odds identity cancels all model-independent factors correctly.
2. The prior ratio is `(s₀+1)/(2p−1−s₀)`.
3. Both Schur complements in the displayed determinant ratio are correct. On the common spectral basis, `I−P_H ⪯ I−P_A`; with nonnegative quadratic forms, `(1+(n+1)a)/(1+b)≤n+1` when a≤b. This also works for singular truth Gram matrices.
4. Monotonicity of the smoother gives Q_S≤Q_S₀, so the likelihood factor is at least one.
5. The p−s₀ one-addition models are distinct and feasible precisely under the stated extension condition. Their masses sum to at most δ.
6. The derivative of `(p−s₀)/(2p−1−s₀)` has numerator s₀−1≥0. Its minimum at p=s₀+1 gives `(p−s₀)(s₀+1)/(2p−1−s₀)≥1`.
7. Thus `δ≥(1−δ)/√(n+1)`, giving the claimed deterministic bound. No noise, signal, or eigenvalue assumption is needed. The formal proposition and STATEMENT item 7 are correct; REPORT must preserve their domain.

## Findings and fixes

### F1 — MAJOR — REPORT states LB outside its domain

**Locations:** `REPORT.md:18,66,124–127,170`.

The report says the bound holds deterministically for every data set and design, but omits `1≤s₀<p` and `s₀+1≤K`. Its R1 summary permits p=s₀. The omission is substantive: take p=s₀=2, centred orthogonal columns with G=(n−1)I, and standardised y=(x₁+x₂)/√2. Then D₁=n, D₂=n², Q₂=(n−1)/n, Q₁=(n−1)(1+1/n)/2, Q₀=n−1, with w₀=1/2 and w₁=w₂=1/6. At n=20 these give δ≈6.5453×10⁻¹⁰, whereas the report's bound is ≈0.17913. The analytic formula is checked in `reviews/C2_scratch_astra/check_boundary.py` and its output. The full-support, fixed-dimensional strong-signal setting also permits much faster asymptotic error, so this is not merely a finite-n objection.

**Fix:** append the proposition's domain to every universal LB summary, including the expectation-rate obstruction. Describe sharpness as a worst-case conclusion for a class containing admissible one-addition alternatives, or explicitly restrict to sequences where these alternatives exist eventually. Do not change Proposition LB or STATEMENT item 7; they already include the right hypotheses.

### F2 — MINOR — NH14 Condition 4.5 transcription is incomplete

**Location:** `ASSUMPTION_MAP.md:77–81`.

The displayed eigenvalue inequalities omit the source's restrictions on their parameters: some ν<δ and κ<(K−1)δ/2; the earlier definition of m_n(ν) takes ν>0. These restrictions matter if the paragraph is read as a detailed statement of Condition 4.5. The main corrected comparison—minimum nonzero eigenvalues, singularity allowed, separate residual-signal identifiability—is accurate.

**Evidence:** supplied NH PDF, printed p. 11, Condition 4.5; definition on p. 6. Extracted at `reviews/C2_scratch_astra/nh.txt:238–244,532–540`.

**Fix:** include `for some 0<ν<δ and κ<(K−1)δ/2` before the inequalities, or explicitly mark them as a partial description and point to the full condition.

### F3 — NIT — E5 leading-score display suppresses its stochastic remainder

**Location:** `ASSUMPTION_MAP.md:21`.

The sketch writes the signal-projection score with an `O(|S|)` remainder. A realised log posterior weight relative to the empty model also contains the signal–noise cross term, generally O_P(√log n) here. The same row later correctly mentions these fluctuations, and the sketch is not used as a proved lemma.

**Fix:** say explicitly that these are deterministic leading coefficients, or write the relative log weight as the displayed signal term minus `|S|log n/2 + O_P(√log n)+O(1)` in this fixed-p experiment.

### F4 — NIT — negative m requires the zero-extension convention

**Locations:** `STATEMENT.md:35,44`; `lemmas/L1a_size_tail.md:12–16`.

The tail bound quantifies over every integer m, but the sum starting at k=m+1 does not define q_k for negative k. The registry's formulation already uses k=max(m+1,0). All cutoff applications use nonnegative m, so this does not affect any rate or proof.

**Fix:** start R_m and R_m^T at max(m+1,0), or define q_k=0 outside 0≤k≤K.

### F5 — NIT — two stale simulation comments

**Locations:** `numerics/post_exact.py:140,223`.

The first still says fixed p=12; the actual run uses p=10. The second says the normalised near-singular eigenvalue is of order n^−1; the construction has normalised eigenvalue of order n^−2 (the unnormalised eigenvalue is of order n^−1). Output headings are correct.

**Fix:** update those comments only.

## Numerical, literature, status, and C1 reconciliation

I inspected both numerical scripts and outputs. The signal is now generated after standardising X; p=10 and 20 seeds respect the enumeration/seed limits. Current E0–E5 and L1a quoted medians, frequencies, and maxima match the output. I reran LB with bytecode writes disabled: **34,920 pairs, minimum 1.012988**, reproducing the supplied result exactly (`reviews/C2_scratch_astra/lb_rerun.txt`). No new full E0–E5 run was needed for the requested comparison against saved outputs.

I read the supplied literature PDFs through local text extraction, treating them as source data. Song–Liang's separate Theorem 1/2 settings, predictor-moment qualifications, Condition 3 discussion, cap comparison, and sure-screening/specificity distinction now match printed pp. 952–956. NH14's identifiability and minimum-nonzero-eigenvalue distinction is corrected; F2 records the remaining parameter omission. YWJ's A–D conditions and Theorem 1 substantiate the corrected untruncated concentration comparison and p⁻¹ bound; the comparison is now restricted to a shared dimension regime. Theorem S, NH14 Theorem 4.2, and the YWJ mixing proof are not certified here.

The citation checker now accurately advertises selected range/token/status checks, not semantic completeness. Its saved output says 53 checks, zero failures. I inspected its code and manually checked the registry statuses and relevant review-verdict summaries; I did not execute the checker because it writes outside my permitted destinations. No status upgrade was found.

| C1 findings | Independent C2 disposition |
|---|---|
| A-F1; B-F2: rate/literature overclaims | Growing-p exact-rate attainment is now a conjecture; formal LB supplies the weaker proved obstruction. YWJ correction is supported. New REPORT scope error remains as F1. |
| A-F2: NH14 | Substantive error fixed; parameter-completeness issue remains as F2. |
| A-F3; B-N6: Song–Liang | Fixed in the detailed comparison; theorem settings and qualifications match the source. |
| A-F4; B-N2/N3 | Coefficient, reference-size, cap, and threshold qualifications restored. |
| A-F5/F6; B-F1/N1 | Current numerical values, median labels, standardised coefficients, and p≤10 compliance verified. Stale code comments only: F5. |
| A-F7; B-N7 | Gaussian family moved to a bridge corollary; item 6 is an interface statement. Benchmark multiplier now names its basis. |
| A-F8 | Fixed-margin deletion obstructions and o_P(1) exponent retained; equality cases not claimed. |
| A-F9 | Checker scope description corrected. |
| B-F3 | p≥2 restored. |
| B-F4 | Specificity example explicitly numerical/sketch, with E5 leading coefficients; not used downstream. |
| B-N4/N5 | L1a′ check record added without changing status; random J_n(c) and diagonal transfer explicit. |

**Disposition:** retain the formal results and repair F1 before package approval; also address F2 and the three nits. Only this review and its authorised scratch directory were written. No git state changes or delegated work were performed.
