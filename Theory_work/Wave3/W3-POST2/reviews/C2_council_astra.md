## (a) My C1 findings

| my C1 finding | resolved | file:line | note |
|---|---|---|---|
| 1 — scope flag omits the effect on item 5 | yes | REPORT.md:23–33; lemmas/E_visibility.md:3 | The flag now lists all three effects of the two ranked proposals, expressly including E's ID → ID^M weakening. It says “No other ranked proposal” and retains the disclosure that prior HQ approval was not obtained. The budget decision is expressly reserved to HQ; this review does not purport to grant that authorization. |
| 2 — N4/N2 sharpness wording exceeds the numerical evidence | yes | REPORT.md:149–150,157–158,193; ASSUMPTION_MAP.md:14,27–28; lemmas/A_occam.md:33–34 | N4 now reports the coefficient scale, achieved margins 3.67–3.99 log n and observed ratios 0.75–1.18, without claiming a smaller universal constant. N2's example is consistently qualified as finite-n evidence without an asymptotic proof, including the two L2 propagation repairs. |
| 3 — stale citation-check count | yes | REPORT.md:180; reviews/CITECHECK.txt:1 | The report uses the saved-output pointer and “0 failures at close”; the output says 136 checks, 0 failures. The obsolete count is no longer asserted. |

## (b) Does the diff break anything?

**No. The repaired D(b) and its listed dependents are correct on this manifest.** This is seat A's R2 diff review, under PROTOCOL_v4 §5 and H1–H5, of manifest `96fd83cf3564e3f4a0ff5b98295c79a55868d9192e6987e9d40e936e5ad9541a`. Before examination, `python -I Theory_work/Wave3/tools/manifest.py verify Theory_work/Wave3/W3-POST2 Theory_work/Wave3/W3-POST2/reviews/MANIFEST_C2.txt` printed `verify: OK` with that digest.

I read the C1 review, its disposition, C2_DIFF (its §1 first), C2_diff.patch and C2_DEPENDENTS in the prescribed order. L1 is the supplied located reconstruction, not an exact historical byte diff; L2 is the supplied exact patch. Both are included in this review. I checked the changed and listed dependent passages against the frozen sources. The PC1/PC2 reviews embedded in the patch were records, not mathematical premises. Unchanged claims retain the C1 acceptance subject to these dependent checks. Paths below are relative to the ticket unless a source alias is used; source aliases have the exact manifest meanings.

### 1. D3 cutoff chain — correct

At `lemmas/D_hellinger.md:50–55`, S in the bounded-excess underfit family satisfies |S∩S₀| ≤ s₀−1 and |S∖S₀| ≤ j₀, hence |S| ≤ s₀+j₀−1. Separately, S∈Ω gives |S|≤K by [W3P]:21. Combining the two bounds gives exactly

`|S| ≤ min(s₀+j₀−1,K) ≤ min(s₀+j₀,K) ≤ m♯_n`.

The last inequality is E0 with the fixed integer B=s₀+j₀; `STATEMENT.md:21` makes this a function of s₀,A only. The middle comparison is monotonicity of min, not the false assertion s₀+j₀−1≤K. Thus the repair covers K<s₀+j₀−1, K=s₀, p=s₀, the empty underfit and fixed small p. For example, p=K=2, s₀=A=1 gives j₀=4 and the repaired bound |S|≤2≤2=m♯_n eventually. No additional growth assumption on p is used.

### 2. Lemma E0 and both applications — correct

At `lemmas/E_visibility.md:15–20`, for s₀≤m<min(B,K), the term q_{m+1}/w(s₀) is present in R_m. [T03R]:22,32 supplies exactly the product written there. Every factor has positive denominator. If p≥2B, i<B implies ρ_i≥(p−B)/(2p)≥1/4; if p<2B, ρ_i≥1/(2p)≥1/(4B). There are m−s₀+1≤B factors and C(p,s₀)≥1. Consequently R_m≥(4B)^(−B), uniformly over the admissible p.

[W3P]:36–38 defines the cutoff using the threshold n^(−(s₀+2)/2). Taking an integer n₀ strictly larger than (4B)^(2B/(s₀+2)) excludes every such m. If K<B, all m<K are excluded and m♯_n=K since R_K=0; if K=s₀, the cutoff domain gives the conclusion immediately. The inherited R1 restriction s₀≤K is maintained. This proof is uniform even when p does not grow.

The application with B=j₀ at `lemmas/E_visibility.md:46` is valid: j₀≥s₀+1, and |J′|≤j₀ and |J′|≤|S|≤K. It places the increment within G3′; J′=∅ is explicitly zero. The application with B=s₀+j₀ at `lemmas/D_hellinger.md:54–55` meets the same hypotheses and places each near model below the cutoff. Neither invocation introduces a parameter into the leading constants beyond s₀,A.

### 3. D3 outside-family mass — correct

At `lemmas/D_hellinger.md:52–59`, the three sets cover Ω∖𝒮_n. The tail has mass O_P(n^(−1/2)) by [T03R]:79–85; strict supersets have mass O_P(r_n) by the accepted A1 5(a), using only (E),(F₀),(OS).

A far underfit with |S∖S₀|≤j₀ has L_S≥c₂σ*²log n by exclusion from the near family. E1(b), at c₂=c₁+1, therefore bounds its completion ratio by n^(−2), without imposing ID on any near model. For larger excess, [T03R]:187–189 gives the unconditional crude ratio. The E2 multiplicity count applies to this restricted collection: each completion has fewer than 2^s₀ preimages, and its excess is at most m♯_n. The two OS sums pay the respective completion sums. Algebraic comparison unions need not belong to Ω. Therefore the displayed O_P(n^(−2)+r_n) far mass and O_P(r_n) discarded mass follow.

### 4. D3 uniform conditional bounds and constants — correct

At `lemmas/D_hellinger.md:60–65`, every retained model has bounded size and L_S≤c₂σ*²log n eventually. For S₀ this uses its bounded ridge loss; for near underfits it is their defining inequality. The repaired cutoff and m♯_n≥s₀ put all relevant projections in G2*. The per-size bound is justified by [P3]:190 using rank≤size, including singular competitors; the empty projection is zero. E1(a)'s union bound covers the near family. For S₀, a₀ is in col X_{c,S₀}, so the separate projection argument at :61–62 supplies the cross-term bound. The event complement has probability at most 5/n. The displayed fitted-mean and Q residual bounds follow simultaneously, without a floor away from S₀.

At :66–71, the inverse-gamma mean identity has denominator n−1.98. Subtracting σ*² and writing N=n−1 leaves the stated +0.98σ*² term. The bounded 2b contribution and the denominator correction are eventually absorbed into the second term at :68. The deterministic good-event bound makes the means at most 5σ*²/4; the exact inverse-gamma variance is then at most 4σ*⁴/n for large n. Crucially, the leading fluctuation ‖e‖²−Nσ*² is one common O_P(√n) variable. Thus the uniform mean error is O_P(n^(−1/2)), despite the weaker deterministic √(log n/n) envelope used to bound the variance. There is no growing-family union bound that would lose the parametric rate.

At :72–79,

`C_H = 8σ*²[C_A(s₀+j₀)+c₂]+1`

depends only on s₀,A,σ*². Splitting squared fitted-mean error into twice the fitted bias and twice the posterior displacement leaves the stated C_H log n/4 displacement threshold. Its posterior expectation is bounded by 2σ*²(s₀+j₀), giving :74–75. Conditional Chebyshev gives 16/M_n² at :73. Uniform tightness of the posterior means, the vanishing good-event exception and the discarded mass prove :76–77 for every M_n→∞. D0 with M_n=√log n yields precisely C′_H=1+C_H/(4σ*²) at :78–79. Other fixed constants can affect onset and auxiliary probability bounds, but do not enter C_H or C′_H. The exclusions listed at :80–81 are supported.

### 5. D(b) statement and all listed uses — correct

`STATEMENT.md:112–116` has exactly D3's assumptions, the same parameter dependence for C_H, every-diverging-M_n variance conclusion, the same fixed C′_H and convergence in sampling probability of posterior mass. It does not assert an expectation rate for that posterior probability. The random-design interface at :117 retains common constants and noise independence, as in [W3P]:95–99; the cutoff repair adds no design-dependent onset.

The copies and uses at `REPORT.md:94–100,240–244`, `ASSUMPTION_MAP.md:13,16,38,45–46`, and `lemmas/D_hellinger.md:94–101` are consistent with these conclusions and assumptions. Their log n/n rate is the squared-distance rate in the stated posterior-contraction setting. The sharpness remarks at `ASSUMPTION_MAP.md:59–61`, `REPORT.md:161–162,191` and D:96–101 explicitly refrain from claiming a proved lower bound. The registry's D and D.D(b) rows point to the same statement and premises; the diff does not break the bundle or its clause.

### 6. Intercept extension, including the same constants — correct

At `lemmas/D_hellinger.md:84–88`, [W3P]:31 gives raw fitted-minus-true mean ε̄1+(μ̂−μ). Centering makes the summands orthogonal, so its squared norm is nε̄²+‖μ̂−μ‖². Applying D0's inequality proves exactly the additional term ε̄²/(4σ*²) in the squared-distance upper bound. Gaussian noise gives nε̄²/σ*²∼χ²₁.

For D(a), use its conclusions with smaller fixed multiples of the diverging thresholds; the added sampling-tight term in n times squared distance is negligible compared with M_n². This proves the same M_n/√n Hellinger conclusion. The parameter clauses are unchanged.

For D(b), preservation of the fixed C′_H follows from slack already available in :73–77: choose M_n=√(log n/2). Outside posterior mass tending to zero, the squared variance term is at most log n/(2n), and the centered mean term is at most C_H log n/(4nσ*²). With sampling probability tending to one, ε̄²/(4σ*²)≤log n/(2n). Their sum is at most the original C′_H log n/n. Thus no enlargement of C_H or C′_H is needed. This is a consequence of the written every-M_n bound, not an assumption that adding a positive term to an exhausted bound is harmless. It supports `STATEMENT.md:117–119` and `REPORT.md:95–96` as well.

### 7. Claim B relation — correct

At `STATEMENT.md:79–80`, `lemmas/B_tail_approx.md:45–48` and `REPORT.md:119,228`, exact reference means r=0. The refined exact-reference proof removes the Gaussian cross-term payment and gives 1/√2+1/2+B/(2σ*²), rather than merely substituting into the larger generic C″_Λ.

For T=S₀, (E),(F₀) imply ‖θ*‖²/n≤M/((n−1)φ₀²)≤M/(2φ₀²) for n≥3. Hence B≤M+M/(2φ₀²), and the refined constant is at most [W3P]:48's C_Λ. For empty truth the actual exact-reference cost is zero, giving its indicator-free base constant. The determinant bound in [P1]:97 gives Θ♯=√D_{S₀}(n+1)^(−s₀/2)Θ″≤Θ″; if R_m=0 both tail normalizations are zero. The same comparison with T arbitrary gives Lemma 1a′ and its exact constant. Both implications, not just their rates, are justified. The revised B Remark 4 citation at :54 also matches the explicit geometric tail calculation in [P1]:128.

### 8. E1(b), E2, C case (iii), and E3.1 — correct

At `lemmas/E_visibility.md:26–54`, the union count and normal tail prove E1(a) without independence among models. The smoother inequalities in [P1]:93–96 give the residual lower bound; only the true-model floor enters R_n and B′. The now-justified G3′ invocation at :46 bounds the increment. For λ≥c>c₁, φ(λ)=λ−2√(2C_xλ)−C_Aj₀ is increasing, and the stated c₁ makes φ(c₁)=(2/log 2)[s₀(A+1)+2]. Strict inequality supplies fixed slack to absorb the vanishing remainder in both exponent cases. Thus the n^(−2) ratio follows.

E2 at :56–70 consumes exactly this ratio and the OS sums; its restricted-coordinate and random-design consequences retain their stated hypotheses. `STATEMENT.md:128–133` matches this assembly. At `lemmas/C_expectation.md:52,54`, κ̄_n=n^(−2) and the extra 1/n exceptional probability remain valid, so taking expectations of the nonnegative truncated sums at :49–53 gives the case-(iii) bound in `STATEMENT.md:85–94`. No expectation conclusion is inferred from O_P alone.

For E3.1 at E:76–78, [P3]:146–151 gives Δ_S≥Nφ₀²‖θ*_{S₀∖S}‖², and BM(c) gives the factor c(1−1/n). Ridge loss dominates Δ_S. Choose a fixed c₁<c′<c and take n≥c/(c−c′), exactly as `STATEMENT.md:135–136` specifies. Claim E then applies with fixed margin c′; this validates the stated containment without applying a fixed-c theorem to an uncontrolled moving constant.

### 9. c₀<c₁ numerical grid — correct as a grid observation

`STATEMENT.md:136` and `REPORT.md:122` explicitly identify a numerical check. Using c₁ from :130, j₀ from :21, and C_*=2s₀+3[Aj₀+s₀+log(j₀+1)+1] from [P3]:194 in [W3P]:75's c₀, I checked s₀=1,…,20 and A=1,1.001,…,10. All 180,020 ratios exceed one; the minimum is 1.2277505771641137 at s₀=1,A=10, rounding to 1.23. Integer arithmetic computed the ceiling in j₀ to avoid grid-boundary rounding errors. This confirms the reported observation, not a theorem for continuous A or all parameter values. The conditional coexistence statement does not need such a universal comparison.

### 10. Remaining W/R edits — correct within this diff's scope

The numbering/version pointers, per-file check records, relation labels, registry blocks and council record preserve the mathematical scopes and literal author statuses checked in C1. `REPORT.md:55–56` correctly limits the “rank loss costs nothing” statement to the chi-square component. N5's revised header in `numerics/post2_checks.py:263` and output :58,66 describes Claim C's proved upper bound. The exponent rename in `ASSUMPTION_MAP.md:44` and D:91–92 is consistent with the C1-checked comparison. The N2/N4 and predictive-scale qualifications are resolved as detailed above. No proof uses these empirical remarks. No new editorial finding is raised.

Independent finite checks are saved in `reviews/C2_scratch_astra/check.py` and `check_out.txt`, executed with `python -I`: 1,590,302 feasible cutoff cardinality tuples and 30,655 exact rational E0 product/lower-bound instances passed, as did the grid above. These supplement the analytic proofs and do not establish asymptotic claims by enumeration. Only this review and its allowed scratch files were written; no git operations or subagents were used.

## Findings

No C/S/F findings. All three numbered C1 findings are resolved. No new E findings.

## Gates

- G1 — PASS: Every changed mathematical step and listed dependent inference checked above is correct, including the repaired cutoff and intercept extension.
- G2 — PASS: Used hypotheses match the statements; E0 uses inherited s₀≤K, and D(b) does not require global ID, beta-min or a floor away from S₀.
- G3 — PASS: Fixed small p, cap endpoints, empty/singular competitors, algebraic comparison unions and random-design common-constant requirements are covered without hidden assumptions.
- G4 — PASS: Frozen inherited sources supply the consumed results; literal statuses and the C1 acceptance basis are preserved, and no PC1/PC2 conclusion is used as a proof premise.
- G5 — PASS: C_H and C′_H have exactly their stated dependence; the parametric variance rate, fixed Hellinger threshold, exact-reference constants and qualified grid observation all check.
- G6 — PASS: The diff preserves the coded real-arithmetic posterior target; the intercept extension uses the specified plug-in intercept and original response scale, without adding a sampler or out-of-sample claim.

## (c) Per-claim decisions

ACCEPT here means the C1 acceptance stands and the reviewed diff and its dependents do not break the claim on this manifest; it is not a fresh full review of unchanged text. The score reflects C/S/F only.

| id | decision |
|---|---|
| W3-POST2:A0 | ACCEPT |
| W3-POST2:A1 | ACCEPT |
| W3-POST2:A2 | ACCEPT |
| W3-POST2:B | ACCEPT |
| W3-POST2:C | ACCEPT |
| W3-POST2:D | ACCEPT |
| W3-POST2:D.D(a) | ACCEPT |
| W3-POST2:D.D(b) | ACCEPT |
| W3-POST2:E | ACCEPT |
| W3-POST2:E3.1 | ACCEPT |

COUNCIL-VERDICT round=R2 manifest=96fd83cf3564e3f4a0ff5b98295c79a55868d9192e6987e9d40e936e5ad9541a seat=A score=10.0 gates=PASS
