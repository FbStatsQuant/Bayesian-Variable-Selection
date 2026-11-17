# R1 council review — Sol

Reviewed manifest de19cf54f91f81defa8bc75a5b174e01a697ea75c3984f70106efaa23a39b768. All 28 listed file hashes match. The three registered claims are supported by their proofs, but the package fails because the report/card and reader proposal overstate the Song–Liang implication.

| id | decision |
|---|---|
| W3-D3:Thm2SG | ACCEPT |
| W3-D3:B3w | ACCEPT |
| W3-D3:ExSG | ACCEPT |

## Findings

**S1 — missing centring qualifier; also unfaithful to STATEMENT (F).** [REPORT.md:35](/home/fb31/BVS-wt/W3-D3/Theory_work/Wave3/W3-D3/REPORT.md:35), continued at line 36, says the displayed assumption “implies Song and Liang's Condition 1.” The same omission occurs at REPORT.md:23–24 and [READER_DELTA.md:34](/home/fb31/BVS-wt/W3-D3/Theory_work/Wave3/W3-D3/READER_DELTA.md:34), continued at line 35. [STATEMENT.md:117](/home/fb31/BVS-wt/W3-D3/Theory_work/Wave3/W3-D3/STATEMENT.md:117) explicitly restricts this implication to z = x − m_n; lines 124–129 explain why. The proposed card discusses x with unrestricted mean m_n and drops that essential restriction.

Counterexample: take p = 2, A = 1, s₀ = 1, β* = (1,0), σ* = 1, and x = (n,n) + (R₁,R₂), where R₁,R₂ are independent Rademacher variables. This satisfies all of (A1)–(A4), with Σ_n = I₂, φ = L = 1. But Condition 1 as quoted in STATEMENT, applied to r = 1 and a₁ = δ for any fixed δ > 0, requires a uniform bound on E exp(δ²x₁²). For n > 1 this expectation is at least exp(δ²(n−1)²), which diverges. Thus no fixed M,δ > 0 work for the raw predictors.

Repair every affected sentence to say “implies Song and Liang's Condition 1 for the centred predictors z = x − m_n.” This changes no theorem hypothesis or registered conclusion. It restores the precise qualification already present in STATEMENT. There are no other C, S or F findings.

## Proof checks

- **Window and probability threshold.** B3w Step 0 correctly uses R1 B1.2 and B1.3, with p_ret = p and s₀ ≤ K_cap where needed. Integer sizes below W̄_n lie below q_n = floor(W̄_n); actual sets also lie below p. B2-core permits q_n > p through q′ = min(q_n,p). The inequality q′ log(ep/q′) ≤ W̄_n(1 + A log n) establishes its size condition for the stated n₁(s₀,A,L). This threshold is independent of φ and the signal bounds. B1's marginal hypothesis follows from (A4), since Σ_jj = 1. The stated c₁, c₂ and union bound follow.
- **Constants after B0.** The unit-noise coefficients are β*/σ*. B1 gives M_E = 2s₀²b_hi²/σ*². The Gram identity and sample-scale bound give λ_min(G_T) ≥ nφ²/4, hence F_λ with φ₀² = φ²/4. B2(a), with c_ψ = φ², gives F_w with g₀ = φ²/8. The lower sample-scale bound gives θ̃*²_min ≥ b_lo²/(2σ*²), hence precisely the stated deterministic envelope M_n → ∞.
- **Completion and interface.** For n ≥ n₁ ≥ 3 a centred, standardised deterministic completion exists even when p > n. Its columns need not be linearly independent. Choosing supp θ⁰ = S₀ makes supp θ° = S₀ everywhere. The completion is Borel in the raw design and independent of the noise. The finite norm/eigenvalue/coefficient conditions defining 𝒜′_n are measurable in the completed pair; raw event measurability in that pair is unnecessary. The inclusion 𝒜_n ⊆ 𝒜′_n ∩ {p_ret = p} supplies its probability. All R1 and item 6 hypotheses hold, including deterministic dimension, eventual cap, common constants, fixed unit noise variance and the common beta-min envelope.
- **Actual outputs.** ASSEMBLY Steps 3–4 construct the appropriate centred response and correctly transfer tightness and selection by adding P(p_ret ≠ p). This probability need only tend to zero, even for the O_P(r_n) conclusions. STATEMENT §0 explicitly defines outputs on removed-column outcomes, including p_ret = 0; these conventions cause no gap. The same measurable HPM selection can be used on agreeing data.
- **ExSG.** Independence gives the product MGF for Bᵀu and covariance BBᵀ. The Gaussian, Rademacher and uniform scalar inequalities hold with L = 1. The factorial inequality for the uniform example is correct. The in-place Hoeffding argument gives ψ″ ≤ 1/4 and ψ(h) ≤ h²/8 for either sign of h, establishing L = K for an interval of length 2K.
- **Gaussian bridge coverage.** L1_POST's sample-scale tails, sparse sample floors, absence of constant columns and joint-law transfer are all replaced or covered. B3w uses its own checked window, rather than silently importing B3's slightly larger one. No Gaussian predictor step remains unaccounted for; Gaussian noise remains explicitly assumed.

## Interpretive sentences within the registered spans

Locations below refer to [STATEMENT.md](/home/fb31/BVS-wt/W3-D3/Theory_work/Wave3/W3-D3/STATEMENT.md).

| location | sentence or implication | verdict |
|---|---|---|
| §1, lines 56–57 | “Then, under the joint law …” followed by the three conclusions | checked — ASSEMBLY applies item 6 and transfers outputs |
| §2, lines 74–75 | “Then supp θ° = S₀ on every outcome” | checked — completion fixes the support off the retention event |
| §2, line 75 | “(X°, θ°) is a Borel function of the raw design, hence independent of ε” | checked — (S1) gives the requisite independence |
| §2, line 77 | “Then 𝒜′_n is (X°, θ°)-measurable and 𝒜_n ⊆ 𝒜′_n ∩ {p_ret = p}” | checked — finite inequalities and B3w Steps 2–6 |
| §2, lines 77–79 | “Moreover … the hypotheses of … item 6 hold … in regime R1 …” | checked — includes the explicit probability argument and common envelope |
| §3, line 86 | “In particular (A4) holds with this L” | checked — the all-direction inequality implies its sparse restriction |

There are no other “hence,” “so,” “in particular,” “this means,” “reading” or “interpretation” sentences in these spans. None must move out.

## Consistency, scope and evidence

The lemma statements agree with STATEMENT §§1–3, and their uses stay within scope. REPORT's registry blocks match the registered claims and retain unchecked local proof statuses; consumed statuses match the quotations supplied in the brief. The conditional part of DIST:B3 is not used. The STRONGER tag is correct against the recorded reader theorem, with the master comparison explicitly qualified. The changelog distinguishes the strengthened companion claims and the specialised completion correctly. The named open directions remain outside the registered spans.

The mathematics of STATEMENT §5 is sound with its centring qualifier: marginal sub-Gaussianity and Jensen give the quoted Condition 1 for centred predictors, for every r. For example, choose δ = 1/(2L); the marginal square-exponential moments are at most √2, and convexity bounds the corresponding moment of any average by the average of these moments. The bounded-mixture backup follows from ExSG and does not dispense with (A3). S1 is a loss of this qualification in downstream prose.

All ten DEPS span hashes reproduce both sha and checked_sha. I did not inspect the earlier reviews named in checked_by: the brief expressly prohibits reading them. Thus I verified current spans and dependency scopes, but cannot independently attest those historical review dispositions. I read the permitted CITECHECK record; I did not run its writer or the DEPS writer. N1 and N2 were rerun without file output and reproduced the frozen outputs: 1,966 window cases with zero violations, and all fifteen exact-posterior sanity rows. Numerics remain sanity checks, not proof. No scratch files were created and no git state was changed.

Better-theorem proposals: none requested for acceptance; the already identified smaller window and split floor remain outside this review's target.

## Six gates and score

- **correct: PASS** — the three registered claims and their proof steps check out.
- **strength: FAIL** — S1 adds an unqualified raw-predictor implication beyond STATEMENT.
- **faithful: FAIL** — the report/card and reader proposal lose STATEMENT's explicit centring qualifier.
- **statuses: PASS** — supplied consumed statuses and local unchecked statuses are represented consistently.
- **sweep: FAIL** — the required report/card sweep detects S1; historical review-file inspection was prohibited.
- **reader: FAIL** — the proposed reader material contains the false unqualified implication.

Score: **8.5/10.0**, reflecting S1/F only. The registered mathematics is acceptable; package acceptance requires the prose repair above.

COUNCIL-VERDICT round=R1 manifest=de19cf54f91f81defa8bc75a5b174e01a697ea75c3984f70106efaa23a39b768 seat=sol score=8.5 gates=FAIL
