# R37 — independent recheck of P-SEL and P-L8

Verdict: **VERIFIED-WITH-AMENDMENTS**.

The substantive repairs are correct. P-SEL.2's positive-scale version works throughout L6(d); its optional signed-scale version needs two further absolute-value edits. One rate-comparison sentence also needs correction. Neither issue invalidates the covered-scenario proof using the positive-scale version. No FATAL or MAJOR finding.

Scope: independently re-derived the affected steps from STATEMENT §2, L2, L6, L8 and [CONC′], and checked the generator's coefficient layout. Existing review verdicts and simulation counts were not used as proof. Original source files and git state were not changed. Only this review and `numerics/R37_constants.py/.txt` were written.

## Numbered findings

1. **MINOR — optional signed-scale repair is incomplete outside the covered scenarios.**
   Location: `Theory_work/Wave1C/C-PACK/patches/P_SEL_L6d.md:19-21`; affected source: `Theory_work/Wave1/W1-GEN/lemmas/L6_instances.md:181,188`.

   The primary choice `c > 0` is correct. If the alternative `c ≠ 0` is adopted, changing only θ*_min to 0.8|c| leaves two false sign-dependent displays in L6(d). For c < 0 the S5 sample covariance converges to 0.24c, which is less than 0.12c, contradicting line 181's asserted lower bound. Line 188's purported positive lower bound also has the wrong sign. The noncoverage conclusions themselves are sign-invariant and remain correct after using absolute values.

   Exact fix: append to P-SEL.2:

   > If the signed-scale alternative c ≠ 0 is used, also replace L6_instances.md:181's covariance assertion by “on 𝒢_n every null-group column satisfies |⟨x_l, μ⟩|/(n − 1) ≥ 0.12|c| eventually”, and replace the lower bound at :188 by “|q| ≥ |c|(1 − Σ_{k<14}|β^pat_k|2^{−32}) > 0”. These additional edits are unnecessary for the c > 0 version.

2. **NIT — weaker rates need not have the same order.**
   Location: `Theory_work/Wave1C/C-PACK/lemmas/I2_LHiid_unconditional.md:76-78`.

   The words “these are the same orders up to A” do not follow from log p ≤ A log n: p may grow as slowly as log n. The replacement is sufficient, but potentially strictly weaker. For complete application to all of L6(d), include the S2 sample-error display at L6:189 as well; its domination argument still works.

   Exact fix: replace the final paragraph of §4 by:

   > **Same replacement for (C5)(d).** Rows are iid N(0, Σ_s), so put 𝒢_n := {max|r̂ − Σ_s| ≤ δ_n} with δ_n = 32√(2(A+1)log n/(n−1)); P(𝒢_nᶜ) ≤ 3n⁻² eventually. Throughout L6(d), replace the concentration-derived √(log p/n) error bounds by O(√(log n/n)), and the concentration-derived log p/n bounds in :159, :163 and :165 by O(log n/n). This also replaces the sample-error term at :189. The new rates may be weaker when p grows slowly, but every required error still vanishes or has the required domination; in particular ω_n = O((log n)^{3/2}/√n) → 0. No equivalence between log p and log n is needed.

## Re-derivation of each patch item

### P-SEL.1 — localized Markov bound: verified

For each fixed null index l, the deterministic family 𝒯₀(l) has at most 2^75 members and each has |T₀| ≤ 15. Regress the raw l-column on the raw T₀-columns using population coefficients. Its Gaussian residual w is independent of X^r_T₀ and all truth columns: different groups are independent, and any truth in l's group is included in T₀. In S1 all columns are independent. The truth-column sample scales are functions of those truth columns, so sample standardization of the mean does not destroy this independence.

Conditionally on the truth columns and T₀-columns, (I−P_T₀)Cw is isotropic in dimension m = n−1−|T₀|. Thus, when Λ_T₀ > 0,

    Q_T₀,l ~ Beta(1/2, (n−2−|T₀|)/2).

For Λ_T₀ = 0 the defined Q = 0 obeys the same upper bounds. With d = |T₀| ≤ 15, the exponential integrand satisfies

    (n−1)z/2 + (m−3)log(1−z)/2
      ≤ (d+3)/2 − (m−3)z²/4.

The Beta normalizer is O(√n), and integrating z^(−1/2)exp(−(m−3)z²/4) gives O(n^(−1/4)). Consequently E exp((n−1)Q/2) ≤ C n^(1/4), uniformly in l, T₀, p and n sufficiently large. Summing the deterministic families and dividing by p−s₀ yields E B_n^leak ≤ C 2^75 n^(1/4). This step requires no independence among the pairs.

The perturbation comparison holds on F_n, so

    P(A_n^leak > n^(3/8))
      ≤ P(F_nᶜ) + P(B_n^leak > e^(−ω_n)n^(3/8))
      ≤ P(F_nᶜ) + C 2^75 e^(ω_n)n^(−1/8) → 0.

This is precisely NL_avg(1/8) on an X-event of probability tending to one. It is not an unconditional moment assertion about A_n^leak, nor a useful finite-n guarantee. The denominator and indices match STATEMENT:72.

### P-SEL.2 — scale: verified for c > 0; signed alternative needs finding 1

For fixed c > 0, θ*_min = 0.8c > 0, the beta-min envelope grows as n/log n, and the VIS envelope diverges. A zero scale contradicts the stated support size; a vanishing sequence is not covered by this fixed-scale proof. All five actual study scales are positive. Allowing a fixed negative scale is mathematically possible with θ*_min = 0.8|c| and finding 1's additional edits.

### P-SEL.3 — coefficient embedding and energy: verified

The generator forms a length-p coefficient vector by placing the fourteen pattern entries at its active positions. Both high-p layouts put one truth in each of fourteen distinct groups. Thus μ = cX_S₀β^pat and θ* restricted to S₀ is cβ^pat, with zero coefficients elsewhere. In the four covered scenarios the truth covariance is I_14, and direct exact arithmetic gives

    Σ_j (β^pat_j)² = 24.64,
    M = 2c²(β^pat)ᵀΣ_s[S₀,S₀]β^pat + 1 = 49.28c² + 1.

Since X is sample-standardized, ‖μ‖²/n converges in probability to 24.64c²; the proposed M therefore gives a high-probability energy event. Embedding the coefficients resolves the original dimension mismatch without changing the mean.

### P-L8.1 — ε₀ and κ compatibility: verified

Use the second branch defining E and v_T ≥ σ². Under NL_η,

    E_T,l ≤ [η/2 + √(2η(A+ε₀))] log n = q log n.

Hence every term, each maximum and their average are at most n^q. NL_C holds with C_L = η, and NL_avg(κ) follows for every fixed 0 < κ ≤ 1/2−q. Equality at this upper endpoint is permitted, since NL_avg uses a non-strict inequality.

For η > 0 the necessary constant condition for this deduction is

    η/2 + √(2η(A+ε₀)) < 1/2,
    equivalently 0 < ε₀ < (1−η)²/(8η) − A.

The assumed η < (√(2A+1)−√(2A))² makes the right-hand side positive. Choose ε₀ once, independently of n, and then choose κ in the displayed range. For η = 0 all leakage δ and E vanish, giving any ε₀ > 0 and 0 < κ ≤ 1/2. For prescribed constants, both the strict q < 1/2 requirement and the displayed κ range must be respected, as the patch states. Numerically, η=0.1 and A=1 permit ε₀ < 0.0125; ε₀=1 fails, whereas ε₀=0.001 permits κ ≤ 0.002562853576.

L8's VIS proof is separately sound: for D = U*_b∖U nonempty, the Schur-complement lower bound gives norm at least √((n−1)φ₀²)‖γ^L_b,D‖ for the large component. Subtracting at most ‖s_b‖ establishes VIS. For a leakage direction, the large component is annihilated and |δ| ≤ ‖s_b‖ establishes NL_η. Empty large supports create no VIS obligation.

### P-L8.2 — W coefficient and disjoint split: verified

For a nine-column block, Σ_C = (3/4)I + (1/4)11ᵀ, with row sum 3. The other truth has correlation vector ε_n 1 with this block, so Σ_C^(-1)(ε_n 1) = (ε_n/3)1. Consequently the active coefficient is exactly θ(1+ε_n/3), and each of the eight off-active coefficients is θε_n/3. The patched split has disjoint supports. More explicitly,

    ‖X_C γ^S‖² = (22/9)(n−1)θ²ε_n²  [signal block],
    ‖X_C γ^S‖² = 12(n−1)θ²ε_n²          [null block].

Both vanish for either ε_n variant in L6(c), while the active squared coefficient times n grows as √n. Thus L8.2(i) and (ii) can hold with a diverging VIS envelope. The direct L6(c) argument is unaffected.

### P-L8.3 — notation: verified

Defining D_b,U = U*_b∖U in both proofs and updating every set-indexed occurrence removes the scalar/set collision. In particular, retain scalar M in (BBM), σ²+2M, and all energy assumptions; do not replace those occurrences. The Schur complement on U∪D_b,U has lower eigenvalue at least (n−1)φ₀² by (H2a). Neither proof requires another assumption.

## Full [CONC′] audit of L6(d)

Set t_n = O(√(log n/n)) deterministically using the explicit δ_n. Fixed-size correlation submatrices have operator error O(t_n). Population eigenvalues are at least 0.1, so their sample eigenvalues are at least 0.05 eventually, uniformly. Inverses, Schur complements and normalized partial correlations therefore have uniformly bounded perturbation constants. Correlations involving μ can be expressed using the fourteen truth columns and their fixed standardized coefficients; when a truth is omitted, the residual variance is bounded below by a fixed positive multiple of θ*_min². The union of the conditioning columns and the truth columns still has bounded size. Hence these correlations also have error O(t_n).

In SEL(ii), every T_x-column belongs to a null group independent of X_T₀, x_l and the truth columns at population level. Therefore a,b = O(t_n) uniformly. The conditional correlation matrix R has a fixed positive eigenvalue floor, giving aᵀR⁻¹b, aᵀR⁻¹a and bᵀR⁻¹b all O(t_n²). The exact recursive identity then implies

    |ρ_T,l − ρ_T₀,l| ≤ C t_n²(1+|ρ_T₀,l|).

The fixed-pair Beta tail union over at most 2^75p indices still gives Q_T₀,l ≤ 16(A+3)log n/n with probability tending to one. Accordingly,

    ω_n = O(n t_n² √(log n/n) + n t_n⁴)
        = O((log n)^(3/2)/√n) → 0.

Moreover ρ_T,l² ≤ 32(A+3)log n/n eventually, so δ_T,l² ≤ 32(A+3)M log n on the energy event, exactly the stated NL_C constant. The replacement introduces no ε₀ restriction here: the first branch of E supplies SEL's bound, so the chosen ε₀=1 remains valid.

The correlated-scenario partition margin is within-group |r̂| ≥ 0.4−δ_n versus cross-group |r̂| ≤ δ_n. It is strict once δ_n < 0.2. Complete linkage finishes groups first; the cut cannot split a size-five group once B ≥ 5, and packing whole clusters preserves whole groups. S1 requires no partition restriction.

VIS errors are o(1) relative to its fixed nonzero coefficients and residual variances. For the larger sparse-eigenvalue family in the X-event, size O(log n) times δ_n is O((log n)^(3/2)/√n)=o(1), so (H0)'s floors also survive. Energy convergence uses only finitely many truth columns. Finally, the S5 covariance error is O(t_n)=o(1), and the S2 lower signal n^(−α/2) dominates t_n since t_n/n^(−α/2)=O(√(log n)/n^((1−α)/2))→0 for α<1. Thus both noncoverage arguments survive the weaker concentration rate, subject to finding 1 if negative scales are allowed.

## Effect on Theorem GEN

No change to the hypotheses or conclusions of the main theorem (C3), its favourable case, or the random-design transfer is needed. P-SEL localizes a proof step and makes the instance's coefficients and constants explicit. The positive-scale wording explicitly restricts the instance to the study's positive-scale convention; it should not be described as preserving a literal prior allowance of every signed c. The signed alternative preserves all nonzero fixed scales after finding 1.

P-L8 makes explicit the admissible choice of auxiliary ε₀ and κ already required by L2:62; it does not justify arbitrary prescribed constants. Neither amendment strengthens GEN to uniform finite-n performance or changes its implementation premises. Apart from the findings above, no further error was found in the audited L6(d)/L8 arguments.

VERIFIED-WITH-AMENDMENTS — FATAL 0 / MAJOR 0 / MINOR 1 / NIT 1.
