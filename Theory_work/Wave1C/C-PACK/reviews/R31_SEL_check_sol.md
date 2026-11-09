VERDICT: VERIFIED-WITH-AMENDMENTS

Independent adversarial review of Lemma SEL and its application to (C5)(d), based on the current files, not on the earlier reviewers' conclusions. No FATAL or MAJOR mathematical defect found. The deterministic-family reduction closes the selection gap identified in R07. One probability-localization clarification and two notation/scope amendments below make the argument precise. This verdict concerns the stated theoretical extension of the generator and inherits GEN's implementation premises; it does not certify the open N3 premise or finite-n start-mode recovery.

Paths below are relative to the repository root. All citations are to the files as read for this review. Only this review and the requested numerical files were written, all under Theory_work/Wave1C/C-PACK/. No git commands were used.

1. **MINOR — Keep the good-event restriction explicit through the expectation and Markov step.**

   **Location:** Theory_work/Wave1/W1-GEN/lemmas/L6_instances.md:162-169, especially :166-167.

   **Exact text:**

   > Hence on 𝒢_n ∩ 𝒦_n, for every leakage triple, E_{T,l} ≤ (n − 1)ρ²_{T₀,l}/2 + ω_n with

   > (iv) *Average.* max_{T} e^{E_{T,l}} ≤ e^{ω_n} Σ_{T₀∈𝒯₀(l)} e^{(n−1)Q_{T₀,l}/2}, whose expectation is ≤ 2^{75}·O(n^{1/4})
   > by (i); Markov gives P((p − s₀)⁻¹Σ_l max_T e^{E_{T,l}} > n^{3/8}) → 0: NL_avg(1/8). ∎(SEL)

   **What needs repair:** The domination in (iv) holds on the event specified in (iii), not pointwise on the entire design space. The unconditional moment bound is for the fixed-family sum on the right. It is not, without localization, an unconditional moment bound on the selected-block statistic on the left. Reading the preceding event restriction as still in force makes the proof valid, but the displayed Markov conclusion should explicitly add the exceptional-event probability. Also restrict the displayed sum to l ∉ S₀, as in the actual NL_avg definition. Neither independence of the selected T from X nor a conditional Beta moment given 𝒢_n ∩ 𝒦_n is available or necessary.

   **Counterexample status:** No counterexample to the localized argument. The issue is the unstated restriction on the displayed domination, not failure of its high-probability consequence.

   **Concrete replacement for (iv):**

   > Put F_n := 𝒢_n ∩ 𝒦_n ∩ {‖μ‖²/n ≤ M}, A_n^leak := (p−s₀)⁻¹Σ_{l∉S₀} max_T exp(E_{T,l}), and
   > B_n^leak := (p−s₀)⁻¹Σ_{l∉S₀}Σ_{T₀∈𝒯₀(l)} exp((n−1)Q_{T₀,l}/2).
   > On F_n, A_n^leak ≤ exp(ω_n) B_n^leak. Unconditionally, E B_n^leak ≤ C·2^{75}n^{1/4}, with C independent of n,p,l,T₀. Therefore
   > P(A_n^leak > n^{3/8}) ≤ P(F_n^c) + C·2^{75}exp(ω_n)n^{−1/8} → 0.
   > This is NL_avg(1/8). No conditional moment assertion is used.

   The energy event can be absorbed into 𝒢_n eventually for these fixed coefficients, but retaining it matches the final C4 event and avoids an implicit step. The total failure probability is o(1); only the Markov term is necessarily O(n^{−1/8}) unless rates for the other events are also stated.

2. **NIT — State the positive scale convention explicitly, or use absolute values.**

   **Location:** Theory_work/Wave1/W1-GEN/lemmas/L6_instances.md:117, :132; Theory_work/Wave1/W1-GEN/STATEMENT.md:138; compare Scripts/Data_generators/gen_dev_data.R:13.

   **Exact text:**

   > −1.6, 1.4, −1.0, 1.8, −1.2, 0.8, −1.6, 1.4, −1.0) as in the R code) and fixed scale c; iid N(0, Σ_s) rows; σ² = 1;

   > * **(H0), (H2a)** on 𝒢_n as in (b) (φ₀² := 0.05, θ*_min = c·0.8 fixed).

   The code states:

   > SCALES <- c(c100 = 1, c075 = 0.75, c050 = 0.50, c035 = 0.35, c025 = 0.25)

   **What needs repair:** The instance wording does not explicitly say c > 0. For c < 0 the displayed identity for θ*_min, a minimum of absolute coefficients, is false: it equals 0.8|c|. For c = 0 the claimed nondegenerate fourteen-signal model and divergent BM/VIS envelopes disappear. This is a scope clarification rather than a new gap: the actual study scales are positive, and the inherited contract S₀ = supp β, s₀ = 14 already excludes c = 0.

   **Concrete fix:** In both the sequence and (C5)(d), replace the scale phrase with “a fixed scale c > 0 (in particular any of the five study scales)”. Alternatively allow any fixed c ≠ 0 and write θ*_min = 0.8|c|. A scale tending to zero with n is not covered by this proof.

3. **NIT — Embed the fourteen coefficients before multiplying by the p-dimensional covariance.**

   **Location:** Theory_work/Wave1/W1-GEN/lemmas/L6_instances.md:116-118, :138, :170.

   **Exact text:**

   > signal = c·X_std β^pat (R:54-61), so θ* = cβ^pat exactly and μ = X_{S₀}θ* ∈ span X_{S₀} (β_raw X-measurable, (C4)).

   > v̄_y := 1 + 2M on {‖μ‖²/n ≤ M} (an X-event, M := 2c²β^patᵀΣ_sβ^pat + 1; P → 1 by [CONC]). VIS with M_n := 0.05θ*²_min(n − 1)/(v̄_y log n).

   **What needs repair:** β^pat is explicitly a fourteen-entry vector, whereas Σ_s is the p-by-p design covariance and X_std is naturally n-by-p. Those products need a support embedding, or the signal-column submatrices. This is harmless shorthand, but M is a named fixed constant used by C4 and should be well defined.

   **Concrete fix:** Write μ = cX_{S₀}β^pat and M := 2c²(β^pat)ᵀΣ_s[S₀,S₀]β^pat + 1. In all four covered scenarios Σ_s[S₀,S₀] = I₁₄, so this is simply M = 49.28c² + 1. State θ*_{S₀} = cβ^pat and θ*_{S₀^c} = 0. This also makes the use of raw β(X) = D_x^{-1}θ* explicit.

The following line audit records the substantive checks. These are accepted steps, not additional adverse findings.

**Lines 113-125: model, asymptotic scope, and concentration.**

The theoretical extension, p_n → ∞, p_n ≤ n^A, fixed s₀ = 14, fixed support, Gaussian rows, sample standardization, and σ² = 1 are all stated. The finite R generator is correctly distinguished from that extension. The model is not a claim about calling truth(p) outside its supported domain. The two actual layouts are obtained from the exact code

> block <- 1L + step * k
> active <- 5L * (block - 1L) + pos[(k %% 6L) + 1L]

with pos = (3,2,4,1,5,3) and step 7 or 13. They place exactly one truth in each of fourteen distinct groups. In one-based indexing, the supports are:

- step 7: (3,37,74,106,145,178,213,247,284,316,355,388,423,457);
- step 13: (3,67,134,196,265,328,393,457,524,586,655,718,783,847).

The fourteen coefficients in L6 match pattern[(k %% 6L) + 1L] exactly; their squared sum is 24.64. The code's sample SD uses n−1, as required by G. The raw coefficient vector is X-measurable, but θ* on the standardized columns is fixed, which is exactly the extension permitted by C4.

S1 has Σ = I; S3 and S4 have five-column equicorrelation groups at 0.7 and 0.85; S6 has group h correlation 0.4 + 0.1((h−1) mod 6). Between-group correlations are zero in all four cases. The respective minimum population eigenvalues are 1, 0.3, 0.15, and 0.1, so the common 0.1 bound is correct. The S6 matrix construction in the R code gives the same correlation to all entries of a given group.

The event 𝒢_n controls all p² correlation entries. For any fixed maximum matrix order q, its operator-norm error is at most q times the entrywise error. Population eigenvalues are at least 0.1, so inverse and Schur-complement operations on those bounded-size matrices are uniformly stable eventually. This is a deterministic consequence of 𝒢_n, even though the number of possible column subsets grows. For expressions involving μ, first use μ = cX_{S₀}β^pat: only fourteen additional columns are involved. No concentration theorem for a fresh independent “μ column” is being assumed. The dimensions actually needed by SEL fit within these fixed-order bounds.

**Lines 127-132: actual blocks and sparse eigenvalues.**

For S3/S4/S6, the strict within/between absolute-correlation margin forces complete linkage to finish every group before a cross-group merge. Above the group nodes, every node is a union of complete groups. Since B_n ≥ 5 eventually and the size cut stops at nodes of size at most B_n, it cannot split a completed five-column group. Next-fit keeps whole retained clusters. Thus the asserted whole-group property holds for the actual, data-dependent blocks. It does not assert that the blocks equal the groups. S1 needs no such recovery statement.

All blocks have size at most 16; indeed the correlated-scenario blocks are multiples of five and hence at most 15 once the margin holds. Using the looser |T| ≤ 15 is safe. For H0, the shorthand “as in (b)” is valid asymptotically: the final event also enforces the larger sparse-eigenvalue orders. With m♯_n = O(log n) as used in (b), entrywise concentration gives operator error O((log n)^{3/2}/√n) = o(1) at those orders. The constants φ₀² = g₀ = 0.05 are fixed. A normalized eigenvalue floor of 0.05 gives the stated unnormalized SE_w floor eventually, with ample slack.

**Lines 133-138: VIS.**

For an admissible U missing a block truth j, span(X_{U+j}) is nested inside span(X_{U∪U*_b}); the displayed lower bound on g_{b,U} is therefore correct. Population block independence survives conditioning on any fixed set U: it conditions separately within independent groups. Since j is the only truth in its group, the partial signal covariance is θ*_j Var(x_j | X_U), even when U contains columns from several other signal groups. The population conditional variance is at least 0.1.

Uniform correlation concentration on U ∪ S₀ transfers this to the actual standardized signal for every candidate U, not just the selected U. The nonzero fixed θ*_j makes the stated relative approximation legitimate. Eventually the sample gain is at least 0.05(n−1)θ*_j². On the energy event, v_U ≤ 1 + Mn/(n−1) ≤ 1+2M for n ≥ 2. Consequently the displayed deterministic VIS envelope M_n = 0.05θ*²_min(n−1)/((1+2M)log n) tends to infinity and satisfies exactly STATEMENT.md:67-68. No finite-n numerical promise follows from its divergence.

**Lines 139-145: enlarged deterministic family and quantifiers.**

For a leakage index l, the selected T contains every truth in its block. On the whole-group event, if l belongs to a signal group, its group's truth is in that block and hence in T₀. Other null groups contribute only T_x. For S1 use singleton G_l; l is null, so T₀ = T ∩ S₀ and every admissible packing is allowed.

There are at most seventy columns in the signal groups and at most five extra columns in l's own group. Therefore |𝒯₀(l)| ≤ 2^{75}; imposing the size and required-truth restrictions only reduces the count. This is a deterministic list for each l, defined before observing the design or packing. The Beta union bound is over at most 2^{75}p fixed pairs, not over the realized blocks and not over all full sets T. The constant is enormous but independent of n; it does not silently become exponential in p. This argument would fail for growing s₀ or unbounded group sizes, which are outside the stated sequence.

T_x can range over polynomially many candidate subsets because its size is bounded. Crucially, no moment sum over those candidates is used: their effect is bounded simultaneously by the entrywise Gram event. Thus the polynomial count does not multiply the critical n^{1/4} average estimate. This is the substantive repair to R07's gap.

The zero-residual convention at line 145 is necessary and sufficient. When T₀ contains S₀, Q = 0 and the true leakage for its extension T is also zero. Such terms contribute 1 to the fixed-family exponential sum, not an undefined Beta variable. Almost surely for sufficiently large n, a T₀ omitting a truth has positive residual because the relevant Gaussian submatrix has full column rank.

**Lines 146-150: fixed-pair distribution and critical exponential moment.**

For a fixed candidate (T₀,l), regress the *raw* l column on the fixed raw conditioning columns using the population covariance. Because the population covariance is block diagonal, the regression coefficients outside G_l are zero. The Gaussian regression residual w is independent jointly of the conditioning columns. If G_l is a signal group, its truth is among those conditioning columns. All remaining truth columns lie in independent groups. Hence w is independent jointly of (X^r_{T₀}, all raw truth columns), not merely separately independent of some of them.

Sample centering and the positive sample scaling of x_l do not change its residual direction. Conditional on the raw conditioning and truth columns, that direction is uniform on the sphere in E = 1^⊥ ⊖ span(CX^r_{T₀}), of dimension m = n−1−|T₀|. The residual of μ is fixed in E under this conditioning, even though its raw coefficients use the truth columns' sample SDs. Thus

Q_{T₀,l} = ρ²_{T₀,l} has law Beta(1/2,(m−1)/2) = Beta(1/2,(n−2−|T₀|)/2).

This statement is for each fixed candidate, not for a pair conditioned on selection. Selection can depend on w and need not preserve its Beta law.

For t = |T₀| ≤ 15 and m = n−1−t, the moment calculation can be checked directly from the Beta density:

exp((n−1)z/2)(1−z)^{(m−3)/2}
≤ exp((t+3)/2) exp(−(m−3)z²/4).

The normalizing constant is at most √(m/(2π)); integrating z^{−1/2} exp(−(m−3)z²/4) over (0,∞) gives Γ(1/4)/2 · (4/(m−3))^{1/4}. The result is O(n^{1/4}), uniformly in the fixed candidates. The exact n−1 in the exponent is tracked; replacing this critical moment by an O(1) claim would be incorrect. Q = 0 terms satisfy the same upper bound.

**Lines 151-159: perturbation uniformly over packings, T, and l.**

The multivariate partial-correlation identity at line 156 is exact. The vectors a and b contain correlations of residuals after projecting on T₀, and R is the corresponding residual correlation matrix, so the denominator and inverse are correctly placed.

If T₀ contains S₀, the zero case is handled exactly. Otherwise T contains no additional truths beyond T₀, so both T₀ and T omit at least one truth. The small-order Gram floor on S₀ ∪ T yields Λ_T,Λ_{T₀} ≥ 0.05(n−1)θ*²_min: minimize over the coefficients on T, while at least one omitted truth coefficient remains fixed. This also ensures the normalized residual μ correlations are stable.

Every T_x column is from a null group disjoint from G_l and all signal groups. Its population conditional covariance with x_l and with μ given T₀ is zero. Entrywise concentration, bounded |T₀|,|T_x| and fixed signal support therefore give ‖a‖,‖b‖ = O(√(log p/n)) uniformly in every admissible choice. The conditional sample covariance Schur complement has a uniform eigenvalue floor; normalizing its diagonal to obtain R preserves a lower bound of 0.05 since the residual variances are at most the original unit variances. Thus aᵀR^{-1}b, aᵀR^{-1}a and bᵀR^{-1}b are O(log p/n), uniformly. Expanding the denominator away from zero gives exactly

|ρ_{T,l} − ρ_{T₀,l}| ≤ C(log p/n)(1+|ρ_{T₀,l}|).

No independence among the selected variables is used at this step. Correlations within the various groups represented in T_x are allowed and are handled by R^{-1}.

**Lines 160-167: union bound, exponents, NL_C, and NL_avg.**

Use Q = χ₁²/(χ₁²+χ²_{m−1}). On χ²_{m−1} ≥ (m−1)/2 and χ₁² ≤ 4(A+3)log n, for n ≥ 34 and t ≤ 15,

Q ≤ 16(A+3)log n/n.

The failure probability for each pair is at most exp(−(m−1)/16) + 2n^{−2(A+3)}. Union over 2^{75}p ≤ 2^{75}n^A still tends to zero. This justifies 𝒦_n with the stated threshold without an extra selection union bound.

Put d_n = C log p/n and r_n = √(16(A+3)log n/n). The perturbation in (n−1)ρ²/2 is bounded by a constant multiple of n(r_nd_n + d_n²), hence O((log n)^{3/2}/√n) = o(1), using log p ≤ A log n. The displayed ω_n is a safe upper envelope; its extra factors do not miss a factor of n. The threshold for ρ_T² can be enlarged by a factor two eventually because d_n/r_n → 0. Consequently, on the energy event,

δ²_{T,l} = Λ_Tρ_T² ≤ Mn · 32(A+3)log n/n = 32(A+3)M log n.

With σ² = 1 this is the claimed C_L. It is **NL_C**, not the much stronger small-constant NL_η condition. SEL need not establish NL_η, and generally should not be advertised as doing so.

For the average, the fixed-family moment is O(n^{1/4}), whereas the target is n^{3/8}; Markov leaves n^{−1/8}. Since 1/2−1/8 = 3/8, the result is exactly NL_avg(κ) with κ = 1/8. The 2^{75} factor and dependence between different l or T₀ do not affect this exponent. Apply the localized probability calculation in finding 1. No moment calculation for the data-selected pair is needed.

**Lines 168-175: hypotheses consumed by L2/L5.**

After the notation amendments, the final X-event supplies fixed A, M, φ₀² = g₀ = 0.05, C_L = 32(A+3)M, κ = 1/8, ε₀ = 1 and bounded reference size 14. The BM envelope 0.05θ*²_min n/log n and the displayed VIS envelope are deterministic and divergent. The additional sparse-eigenvalue event handles H0; the bounded-order concentration and block argument handle H2a. The gains above give H2b; SEL gives both parts of H2c, on precisely the leakage family in STATEMENT.md:69-74 and L2_centre.md:29-31.

The first branch of E alone bounds E regardless of ε₀; fixing ε₀ = 1 in the final event is therefore consistent with the second branch used by L2. H1/SEP is not needed for C3-fav. One can choose the bounded relevance superset S₀ itself if desired; no separation claim is being smuggled in.

Conditioning on X for L1/L2 makes the actual blocks and their families deterministic. L2's polynomial family size p2^B then concerns Gaussian *response noise*, which remains independent of X under C4 and the generator (raw X drawn first, independent eps drawn at R:57). That conditional argument is distinct from, and compatible with, SEL's unconditional design-residual Beta calculation. The random-design implication is precisely the canonical conditioning argument in L5_assembly.md:66-77. Every deterministic design sequence inside the final event has the same constants and envelopes eventually. This meets C4's quantifier, not merely a pointwise-in-probability version of the hypotheses.

The conclusion about the prescribed start mode follows under the previously named scoring/implementation premises. There is still no quantitative n = 200 guarantee; nor does this prove the actual finite development datasets have the favourable property.

Numerical falsification attempt (local computation, 12 seeds, 97.77 seconds):

Script: Theory_work/Wave1C/C-PACK/numerics/item3_SEL_falsify.py

Output: Theory_work/Wave1C/C-PACK/numerics/item3_SEL_falsify_out.txt

The experiment draws the exact Gaussian covariance law of S1/S3/S4/S6 using independent group factors, centers and sample-standardizes each column, and uses c = σ = 1. It ports complete linkage on 1−|r̂|, smaller-minimum-index child ordering, the actual top-down cap B = min(⌊√n⌋,⌊√p⌋,16), and next-fit packing; it does not replace the selected blocks by deterministic groups. Continuous random distances avoid exact merge ties almost surely. p(n) = 5 ceil(max(1000,n/2)/5), so p = 1000,1000,1600 at n = 200,800,3200, and p ≤ n². The two fixed support layouts are exercised as recorded in the output; layouts alternate across cells, so these are stress-test cells, not repeated samples along one fixed-layout sequence.

For every null l in every actual block, the script exhaustively enumerates all T containing the block's truths. In total it evaluates 68,617,536 leakage triples. A batched Schur-complement calculation obtains δ², Δ_T, both branches of E with A = 2 and ε₀ = 1, and the exact maximum exp(E) for each l. Direct linear solves check empty, full, and intermediate conditioning subsets in each block; the maximum covariance discrepancy is below 1.5×10^{−14}. An additional deterministic six-column check recomputed every admissible exponent directly from the sample vectors and least-squares residuals; the maximum difference between the resulting per-l maxima and the script's maxima was 1.63×10^{−13}. No response noise is needed for this X-only lemma. All nine correlated-scenario draws retain whole groups in their actual blocks.

The exact averaged statistic divided by n^{3/8} was:

| n | S1 | S3 | S4 | S6 |
|---:|---:|---:|---:|---:|
| 200 | 1.033821 | 1.105653 | 15.043955 | 1.362151 |
| 800 | 0.305155 | 0.753086 | 0.972170 | 0.768697 |
| 3200 | 0.181263 | 0.411601 | 0.465565 | 1.176144 |

Five of the twelve draws fail the numerical NL_avg(1/8) inequality at their finite sample size, including S6 at n = 3200. This refutes a finite-n or already-small-failure-probability reading, but not the stated asymptotic lemma: it gives no usable onset or small constant. The raw averages, all seeds/layouts, and all diagnostics are in the output. In particular, the S4/n=200 average is 109.71052 versus threshold about 7.293, and the S6/n=3200 average is 24.260061 versus threshold about 20.627. Neither failure can be dismissed as only a rounding effect.

The maximum induced Q_{T₀,l}·n/log n over these draws is 4.160504, below the stated bound 16(A+3) = 80. This maximum ranges only over T₀ induced by the realized blocks, not the full enlarged family. The maximum δ²/log n ranges from about 38.26 to 105.73; it is below C_L = 8044.8 for c = 1 with the explicit M = 50.28, although that bound is extremely loose. The maximum positive perturbation E_{T,l}−(n−1)Q_{T₀,l}/2 is still between 0.414 and 1.883 across these finite cells. Thus it cannot be replaced by zero in practical finite samples. These observations supply no asymptotic counterexample and no estimate of the claimed failure probabilities from only twelve draws.

Disposition: retain the covered-scenario argument after the three local amendments. Do not revert to a Beta law conditional on selection, discard T_x without the perturbation estimate, assert a uniform O(n^{1/4}) expectation of the selected statistic without localization, or claim NL_η/finite-n start-mode recovery from SEL. The current fixed-family-plus-perturbation proof delivers exactly NL_C and NL_avg(1/8), and the surrounding argument supplies VIS and the remaining C4 hypotheses.

VERDICT: VERIFIED-WITH-AMENDMENTS — FATAL: 0; MAJOR: 0; MINOR: 1; NIT: 2; total: 3 findings.
