MANIFEST 053bc169c5da3c032943e217e7bd5ddb76d4268ba821b09579be126d9961a155

Verdict: VERIFIED — lemmas/L6_COROLLARIES.md
Verdict: VERIFIED — lemmas/L7_NEC.md
Verdict: VERIFIED-WITH-AMENDMENTS — lemmas/L8_TRANSFER.md

## Findings

1. **MINOR — lemmas/L8_TRANSFER.md:51–54.** The statement allows every κ < κ_V, but the proof fixes κ″ = (κ + κ_V)/2 and applies L8.2, which requires a positive exponent. For κ ≤ −κ_V this application is unavailable. The asserted conclusion remains true. **Exact repair:** begin L8.3 with “First take 0 < κ < κ_V”; after the proof add “For κ ≤ 0, apply the proved result at any κ₀ ∈ (0, κ_V); its o_P(n^{−κ₀}) remainder is also o_P(n^{−κ}).” Apply this observation to both displays. No change to STATEMENT.md is necessary.

2. **MINOR — numerics/lemmas/falsify_L6_L11.R:10–11, 97–104.** The comments describe the inequality chains for both (C2)(i) and (ii) as asserted. Only the leaking-null chain is asserted: line 100 compares against (f1) using the *realised* RSS envelope and the *exact realised* score remainder Rdiff. The weak-truth branch computes competing odds and prints exponents, without asserting the (f3) chain. Neither branch verifies the uniform remainder constant, the uniform toolkit event probability, or the asymptotic probability statement. RESULTS_LEMMAS.md:37 more accurately describes this limitation. **Exact repair:** change the script comments to “Assert the leaking-null (f1) chain with realised RSS envelope and exact score remainder; print competing-odds exponents for both cases. The weak-truth (f3) chain and uniform constants are not asserted.” This is a numerical-test description amendment; it does not affect the L7 proof or STATEMENT.md.

No false displayed inequality or substantive gap was found in the assigned proofs. The L7 verdict concerns the mathematical lemma; finding 2 concerns its accompanying numerical-test description.

## Checks performed

### Frozen inputs and scope

Read the brief first. The permitted manifest verifier returned `verify: OK` with the digest above. Read all lines of L6, L7 and L8, the relevant locked STATEMENT.md definitions and claims, L5 in full, the cited toolkit and leakage results in L2/L3, the cited L4 propositions and their uniformity statements, and the relevant L1 prior/floor statements. Read the numerical script and its results description. No other reviewer report, LOG, CHECKPOINT, or registry claim was read or consumed. Earlier lemma results are accepted as permitted; their statements were checked against their uses here.

### L6.0 and L6.0′

Re-derived the dependence on ε directly from L5.2: its deterministic thresholds n₂, n₃/n₄ and the two visibility smallness requirements do not depend on ε. The only additional ε-dependent threshold is

`2 exp(−n^{1/3}) + 2/n + 1/log n ≤ ε/2`.

The Markov steps use ε through λ = 4c_L/ε, and the restriction ϱ ≤ c₀(ε) enforces the needed smallness; these alter the constants/admissible inputs, not the deterministic threshold otherwise. In particular c₀ ≤ 1, the L3 small-gain envelope applies uniformly, and the L4 constant-level branch needs c_QU_Q ≤ 1, supplied by the same event. No additional ε-dependent threshold is hidden in those citations.

For ε_n = 4/log n, substitution gives λ_n = c_L log n, c_{0,n} = 1/(64s₀′c_L log n), C_n = 43s₀′c_L log n, and precisely the displayed C′_n. The probability budget is valid once 2 exp(−n^{1/3}) + 2/n ≤ 1/log n and log n > 4. Here C_n = O(log n), C′_n = O((log n)²). The joint statement that both are O((log n)²) is also correct. L5.2's coefficient 43 safely exceeds (8/3)16 = 128/3. Its use of the sum of the two coefficients as C′ is conservative and valid.

### L6.1 / F1

From J2, d²/t² ≤ η log n and σ/t ≤ 1 give the cross term at most √(η log n) z̄_n. Since A > 0, z̄_n/√log n → √(2A); the logarithm of the prefactor is o(log n). This proves the claimed exponent η/2 + √(2Aη) + o(1), uniformly in the design. Solving κ_L > 0 gives exactly η < (√(2A+1) − √(2A))².

Let d = κ_L − κ₁ > 0. The assumed factor (|Q|+1)n^{−κ₁} is eventually bounded, so ϱ ≤ n^{−d+o(1)}; thus ϱ tends to zero polynomially and is eventually below c_{0,n}, even if that assumed factor itself tends to zero arbitrarily slowly. The default budget tends to zero. The final probability display follows by using a positive κ₃ strictly between κ and κ_V, absorbing C_n by n^{κ_L−κ+o(1)}, and bounding n^{−κ₃} ≤ n^{−κ}. Nonpositive κ make the lattice conclusion trivial. All hypotheses and the displayed rate match F1 in STATEMENT.md:262–265.

For η = 0, the exact integral comparison J_n(0,τ_U) ≤ J_n(0,σ) = √(2/π)z_n gives the stronger square-root logarithmic rate. The growing-Q condition in F1 ensures (AL); L5.3(a) then supplies the asserted O_P plus o_P form, without a logarithmic high-probability penalty.

### L6.2 / F2

For an arbitrary proper U ⊂ S₀, write W = S₀ \ U. The Schur-complement quadratic form is

`aᵀ𝒮a = min_b (b,a)ᵀR̂_{S₀}(b,a) ≥ φ₀² ||a||²`.

This also covers U = ∅ by taking 𝒮 = R̂_{S₀}. Consequently Δ_U ≥ φ₀²||θ*_W||² ≥ φ₀²θ_lo². This uses F2's floor on the **entire** truth Gram matrix, not GF-16; it remains valid when s₀ > 16. It is exactly the stronger floor explicitly assumed by F2.

J1 uses τ_U² − σ² = Δ_U, so its prefactor is bounded by C_F = √(1+σ²/(φ₀²θ_lo²)); its exponent is at most η′ log n/2. Averaging over at most p nulls gives C_F n^{η′/2}. The additional 15√(2/π)z̄_n/p is handled by p/√log n → ∞, making its contribution o(n^{−1/2}). The separate hypothesis n^{−1/2}𝔏_n(S₀)² → 0 both gives (AL), via the identity on line 56, and makes the quadratic odds contribution o(n^{−1/2}). These are distinct uses; neither can be silently dropped from this argument.

L5.3(b) now gives the advertised n^{−(1−η′)/2} rate plus visibility remainder. When η′ = 0 and κ_V > 1/2, choose κ strictly above 1/2 to absorb that remainder. L1's deterministic floor supplies the matching lower bound, since eventually s₀ < K. Thus the exact-order assertion agrees with STATEMENT.md:266–269, including its κ_V > 1/2 qualification.

### L6.3 / F3 and L6.4 / F4

For large n, 2log(2^{21}) + 2log log n ≤ log n, hence z̄_n² ≤ (2A+1)log n. The J2 exponent is bounded by C₀/2 + √(C₀(2A+1))√log n. The prefactor is eventually at most exp(√log n). This yields C₃ = √(C₀(2A+1))+1. Applying the hypothesis with C₁ = C₃+1 supplies enough decay for ϱ ≤ c_{0,n}; it is stronger than merely ϱ → 0. The additional unit in C₂ = √(C₀(2A+1))+2 absorbs 43s₀′c_L log n eventually. C₂ depends only on C₀,A, while the eventual threshold may depend on the other fixed constants. For κ ≤ 0 the lattice probability assertion is immediate; for positive κ it follows directly from L6.0′.

For F4, checked all of L3.5's arithmetic: h ≥ 1 for n ≥ 4; exp(−min(z_n²,4log log n)/2) is the maximum of the two stated tails; bounded |I_n| makes their sum vanish. J2 at the reduced levels gives n^{c/2+o(1)}. Dividing by p and √n and using log p/log n ≥ A̲−o(1) gives exactly the exponent −(1+2A̲−c)/2. The κ₁ slack proves (AL); no separate assertion that the default functional vanishes is needed. This permits all parts of T1 with the selected levels. The default-level charge threshold follows by solving (c−1)/2+√(2Ac)−A < 0, producing the displayed (√(4A+1)−√(2A))². This is an upper-bound threshold, as the statement correctly says.

### L7.1 / (C2)(i)

Since p > s₀ and n ≥ 2s₀+2 eventually, K ≥ s₀+1 and S₀ ∪ {l} is feasible. L1(P1) gives the exact prior ratio (s₀+1)/(2p−1−s₀), which is at least 1/(2p). The witness is deterministic in Setting F, because the partition and mean are fixed. A single Gaussian variable suffices; its squared-tail event has complement at most 2/log n, independently of the toolkit event.

TK-d plus f1 gives the asserted lower bound for any gain size. This use does not require the gain divided by RSS to be small. The squared-sum lower bound, σ² ≤ τ_U² and the event bound give the displayed loss 2log log n/ε₁. Replacing ω_n by ω̄_n decreases the lower bound. The additional negative logarithmic term on line 24 safely drops its factor 1/(1+ω̄_n). The correction log(n+1)−log n ≤ log(5/4) holds for n ≥ 4. From the limsup, log(2p) ≤ (Ā+ϵ)log n eventually. The ε₁ loss is at most ϵ/2 in the exponent; the remaining loss is o(1). With 3ϵ = (c−1−2Ā)/2−κ′ there is the claimed positive slack. No upper bound on δ², visibility, or (AL) was used.

### L7.2 / (C2)(ii)

Here s₀ ≥ 1 and deletion is feasible. L1(P2) gives (2p−s₀)/s₀, at least p/s₀. The single-variable Gaussian event is again sufficient. The squared-sum upper bound gives exactly G_n in the proof. TK-a then yields x ≤ G_n/((n−1)(1−ω̄_n)) = O(log n/n), allowing f3; unlike part (i), this linearisation needs and has the small-gain assumption. The factors ϑ̄_n and x̄_n introduce only o(log n) error (indeed ϑ̄_nG_n → 0). The constant −log s₀ is absorbed into that error.

The liminf supplies log p ≥ (A̲−ϵ)log n eventually. Since ε₁c ≤ ϵ, the exponent is at least (1+2A̲−c)/2−3ϵ/2−o(1), strictly above κ′. The same noise is allowed in the toolkit event and the single-variable event: only a union bound is used. Neither part introduces a visibility or leakage hypothesis. The quantitative version of [TK] consumed here is the one explicitly stipulated in STATEMENT.md:181–185; L7's use of GF-16 to obtain it is consistent with that convention.

### L7.3 / N1–N3, non-vacuity and sharpness

N1 invokes the deterministic floor and F2's **qualified exact-order clause** (κ_V > 1/2), as L7:54 explicitly records. The shorter reference in STATEMENT.md:306 should be read as that F2 clause, not as dispensing with its qualification.

For N2, U*_{b(l)} has size at most 15 because l is a null in the same block, so C2(i) applies. If s₀ ≤ 15, V = S₀ makes δ = 0, proving emptiness of the premise. I independently checked that the premise really is non-empty for every fixed s = s₀ ≥ 16:

Take p = s+1, σ² = 1, centred orthonormal vectors e₀,e₁,…,e_s, N = n−1, θ*_j = 1 on the s truths, x_j = √N e_j, and one null

`x_l = √N [r_n Σ_{j=1}^s e_j + √(1−s r_n²)e₀]`, with `r_n² = 6 log n/N`.

For sufficiently large n this is well defined and has the required column norms. Its mean energy is sN ≤ sn; Ā = A̲ = 0, while p ≤ n^A for any fixed A > 0 eventually. Every 16-column correlation Gram has minimum eigenvalue at least 1−√(15r_n²), so GF-16 holds with a common positive constant eventually. For V ⊆ S₀ of size k ≤ 15, set m = s−k ≥ 1. Direct projection gives

`δ²_{V,l}/(τ_V² log n) = 6m²/[(1−kr_n²)(1+m)] ≥ 3`.

Thus the N2 hypothesis holds with the fixed c = 2 > 1+2Ā. This construction obeys Setting F and (E), rather than just specifying abstract gains.

For N3 the block-relative conditioning set is among the quantified truth subsets, giving C2(ii). In the stated orthogonal-truth example, choose 0 < c′ < c: δ²_{V,j} = c′σ²log n and τ_V² ≥ σ² for all such V, so the claimed inequality holds. Other truths can also be omitted by taking s₀ = 1. The example is valid; it is not an example for c = 0, which is not required by the non-emptiness assertion.

The sharpness interpretation is sound. For example, make every null orthogonal to one weak truth (s₀ = 1) with Nθ_j² = dσ²log n, where a proposed lower visibility constant t satisfies t < d < 1+2A. Then the null gains vanish and the true gain divided by τ²log n tends to d. The modified V-c requirement holds eventually, but N3 forces failure when log p/log n → A. For V-m choose a sufficiently small positive c_m so t+c_m < d; with one truth, all substituting-null gains are zero and every modified margin instance holds eventually. For polynomial p larger than n, polynomially many null unit vectors in the orthogonal complement can have every 16-column Gram bounded below (e.g. by the usual finite-pair inner-product concentration and a union bound); full-column orthogonality is unnecessary. This sharpness argument imports no registry premise.

### L8 / transfer and statement comparison

The design and response are finite-dimensional measurable objects. Centring, dropping constant columns, standardising retained columns, support selection for a measurable β, finite table sums, and the deterministic partition define measurable functions, with fixed conventions for ties. Given X^r = x, α, β, θ*, S₀, Q, h and the partition are fixed. Integrating the Gaussian kernel as in L8.1 is therefore a measurable version of the conditional probability. No response information may enter those targets. Conditional noise is exactly Setting F's noise; no union bound over possible supports or coefficient values is needed.

For x in 𝒳, the event at threshold Cϱ̄ is contained in the event at threshold Cϱ(x), because C ≥ 0 and ϱ(x) ≤ ϱ̄. Hence its conditional probability is ≤ ε+b_n(h(x)) ≤ ε+b̄. Splitting off X^r ∉ 𝒳 proves P(B) ≤ P(X^r ∉ 𝒳)+ε+b̄, without independence of B and 𝒳. The odds version uses the same direction of threshold inclusion and still needs ϱ ≤ c₀; L8.2 explicitly retains this requirement. The L6.0′ version follows by the same conditional argument.

The constants and thresholds in L5.2 depend on the fixed bounds, ε and κ only. κ_E is controlled by (g_*,M,σ²); the event envelopes use (n,A); the truth-block event depends on s₀ rather than the identity of the support. These facts justify the claimed design uniformity. The tail budget and leakage functional may vary with x, because they are bounded on 𝒳 before integration.

For positive κ, apply the inequality at κ″ strictly between κ and κ_V. For each fixed ε the deterministic envelope is eventually below c₀(ε), and b̄_n+P(X^r∉𝒳_n) tends to zero. Thus (X_n−n^{−κ″})₊ = O_P(ϱ̄_n), and n^{−κ″} = o(n^{−κ}); the same proof works for the odds and r̄_n without requiring r̄_n → 0. Finding 1 fills in the remaining exponents. These are exactly the quantifiers, target definitions, hypotheses and rates of STATEMENT.md:284–295. Both deterministic β with independent noise and Setting R with β(x)=D_x(x)^{-1}θ* have the claimed conditional law. No assertion about the Gaussian-row sufficient conditions of T3(b) is needed here.

As usual these are random variables for valid scored inputs. If the arbitrary raw-design law admits invalid inputs outside 𝒳_n (e.g. no retained columns), assign arbitrary measurable values to the displayed statistics there; their probability tends to zero and the same inequalities charge that event to P(X^r∉𝒳_n). This conventional extension makes no claim about running the algorithm on invalid inputs.

### Numerical checks actually run

1. Ran the permitted manifest verification: OK.
2. Re-ran `Rscript --vanilla Theory_work/Wave3/W3-START/numerics/lemmas/falsify_L6_L11.R 113` read-only. Exit status 0; `TOTAL VIOLATIONS: 0`. In Part B the leaking-null median competing-odds exponents were 0.78, 0.68, 0.85 for n = 200,800,3200 (printed target 0.75); weak-truth medians were 0.77,0.62,0.59 (printed target 0.60). Negative minima occurred at these finite n; this does not falsify an asymptotic probability assertion. Moreover p = 40 is fixed while c is recalibrated with log(40)/log n, so the printed targets describe that finite-n calibration, not a literal fixed-c asymptotic experiment. See finding 2 on the asserted checks.
3. Ran an independent inline base-R check, seed 113, with no script or output file written. For 300 random positive-definite correlation matrices with s = 2,16,17,24,40, random proper U, the Schur-complement minimum eigenvalue never fell below the full Gram minimum (tolerance 1e−10).
4. Numerically integrated J for 24 F2 parameter combinations: Δ = .01,.2,1,10; η′ = 0,.2,.9; n = 100,10^6. The ratio to √(1+1/Δ)n^{η′/2} never exceeded 1 (maximum rounded to 1). This tests the prefactor as well as the exponent.
5. Evaluated the independent N2 construction above for s = 16,17,32, n = 10^4,10^6,10^9 and every k = 0,…,15. The smallest normalised gain was greater than 3, and the common normalised GF-16 lower bound ranged from .712074 to .998634. No violation.
6. Independently tested the scalar f1/f3 inequalities over n = 100,10^4,10^8, RSS relative errors at −ω,0,+ω with ω = 0,.1,.49, and explained-RSS fractions from 0 through 1−10^{−12}. For f3 retained fractions ≤ 1/2. Maximum relative excess over either asserted bound was 0. This specifically exercises f1 near total explained energy and f3 at its allowed endpoint.

R emitted locale-setting startup warnings; the runs completed and all numerical checks above executed. The computations are falsification attempts, not evidence for uniform asymptotic thresholds.

## Not checked

- Proofs of L1–L5 beyond the dependency statements and the explicit L5.2 ε-dependence required by the brief; these results were accepted where cited.
- Independent correctness of the pinned implementation, binary64 behaviour, or computational tie handling beyond the assumed measurable mathematical partition and EX-A.
- Proofs of L9–L11, T3(b), consumer tickets, registry entries or externally certified claims. Incidental L9–L11 numerical output from the permitted script is not a verification of those proofs.
- Simulation of the uniform thresholds n₀,n₂,n₃,n₄ or of the very large constants c_L,C,C′. No finite simulation establishes their eventual probability guarantees.

Verdict: VERIFIED — lemmas/L6_COROLLARIES.md
Verdict: VERIFIED — lemmas/L7_NEC.md
Verdict: VERIFIED-WITH-AMENDMENTS — lemmas/L8_TRANSFER.md
