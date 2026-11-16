# L02 — independent line check

Reviewed against the locked v1.1 statement and the permitted parent sources. No other review, planning, checkpoint, or numerical-result file was read. All line references below refer to the files supplied in the brief.

LEMMA AE_expectation: CORRECT-WITH-FIXES

LEMMA A2C_critical: CORRECT

Findings by tag: C = 0, S = 1, F = 0, E = 0.

The one finding concerns the abstract formulation of the assembly lemma. Its applications supply the missing control, so it does not invalidate Proposition A-E or its corollaries.

## Finding

**S1 — The abstract assembly lemma must control its starting index.**

Location: `Theory_work/Wave3/W3-PSHARP-R/lemmas/AE_expectation.md:45-48`, specifically the assertion at line 48 that the resulting index depends only on `(ϵ, 𝔭)`.

The estimate is assumed only for `n ≥ n₁`, but nothing in the helper lemma's stated hypotheses makes `n₁` a function of `(ϵ, 𝔭)`. Convergence rates for `θ⁺`, `θ⁻`, and `b` cannot control when the assumed estimate begins to hold. Consequently the abstract lemma, with its stated restriction on dependence, is stronger than its assumptions warrant.

For example, take `ϵ = 1/2`, `α = 1/8`, `Λ = L = 1/8`, and `θ⁺ = θ⁻ = θ = b = 1` identically. For an arbitrarily large `n₁`, let `δ_n = 0` before `n₁` and `δ_n = 3/32` thereafter. The assumed inequality holds for every `n ≥ n₁`, and all convergence errors vanish identically. The proposed conclusion requires `E δ_n ≥ 3/64`, which fails before `n₁`. There is therefore no common `n₀` independent of this unrestricted `n₁`.

**Exact fix:** add to line 47: “Assume also that `n₁` depends only on `(ϵ, 𝔭)`.” At the end of the proof set `n₀ := max(n₁, n_rates)`, where `n_rates` is the index after which the two tolerances in line 52 hold. Alternatively, allow dependence on `n₁` in the abstract conclusion and explicitly establish its permitted dependence in each application.

This is a local statement-strength repair. In §4 the preliminary requirements are `n ≥ 3`, `n > (4/ϵ)²`, and `ψ_n ≤ 1`; in §5 one additionally needs `n ≥ 4`, `2 log T ≤ (n−1)/2`, and `ω′_n ≤ 1`. Their common starting indices are controlled by exactly the constants and deterministic sequences allowed in STATEMENT lines 66–68. Thus the proof already contains the bounds needed to apply the repaired helper uniformly.

## AE_expectation: checks and re-derivations

- **Lines 3–12, setting and consumption.** The definitions of odds, `P_n`, and `c_n` agree with the coded posterior and parent Lemma S(4). The assumption `s₀+1 ≤ K` ensures `π(S₀)>0` and makes every one-step superset admissible. The parent statement and proof sources cited here contain the claimed ingredients. Lemma V is in `S_one_step.md:7-15`, while the parent statement's lines 32–44 state Lemma S. The combined citation supplies both.

- **Lines 15–24, Lemma T.** Re-derived the full estimate. Monotonicity gives `δ ≥ Y/(1+Y) ≥ Y−Y²`. Independence of `U_j` from its own event gives the first moment, even when the events depend on other coordinates. The second moment only uses mutual independence of the `U_j`, nonnegativity of the indicators, and `U_j² ≤ T U_j`. The coefficients are exactly `cT L + L²`. Neither mutual independence of the events nor independence of the entire score vector from the event vector is needed.

- **Lines 27–35, truncated means.** The Gaussian integral gives `2√(log T/π)` for every `T ≥ 1`, including zero mean at `T=1`. Re-derived the sphere bounds by integrating the tilted coordinate density over `|t| ≤ √τ`. Parent `A_log_factor.md:30-37` proves the required density estimates for any cutoff satisfying `τ ≤ d/2`; the argument does not require `τ=2 log N` or `N→∞`. Substituting `τ=2 log T` gives precisely the displayed exponents and constants. The requirement `d ≥ 3` is satisfied eventually in the application.

- **Lines 38–43, truncation and (3.1)–(3.2).** From `s₀+1 ≤ p`, the ratio `(2p−1−s₀)/p` belongs to `[1,2)`. Thus `log T = ℓ_n + log(α(2p−1−s₀)/p)` lies in the stated interval. Using `ℓ_n ≥ (log n)/2` gives the lower square-root bound when `n>(4/ϵ)²`. The identities `c_nT=α` and `L_n/Λ^E_n=√(log T/ℓ_n)` are exact. No null-block growth assumption occurs.

- **Lines 45–52, Lemma F.** Apart from S1, the algebra and constants are valid. When `Λ≥1−ϵ`, nonnegativity suffices. Otherwise `Λ<1`, and `ϵ−θα ≥ ϵ/2` because `θ≤2`. The errors are bounded by `4|θ−1|+2(1−b)`, which is at most `6ϵ/16` at the stated tolerances, below the available `ϵ/2`. The repaired lemma proves the desired bound without assuming `Λ→0`.

- **Lines 55–61, orthogonal setup and decoupling.** Parent `A_log_factor.md:53-63` gives the common coefficient and the bound on `V` using only the stated Gaussian truth, energy bounds, and fixed orthogonal witness. These lines do not use `N→∞`. For each fixed `j`, `P_j=C−u_ju_jᵀ` is an orthogonal projection of rank `n−2`. The pair `(u_jᵀε, P_jε)` is jointly Gaussian with zero cross-covariance, so `g_j` is independent of `R_j`, and `R_j` has the claimed chi-square law. This remains true when `R_j` contains other null scores.

- **Lines 62–71, orthogonal comparison.** Chebyshev gives `P(G_jᶜ)≤x⁻²`. The upper bound on `E=g_j²+R_j` is valid with slack because `√(n−2)≤√(n−1)`. Multiplication by `1+0.04/(n−1)` yields the stated `e_n`, since that multiplier is at most `1.02`. On the truncated event, `κ_n≥1−e_n` gives the exponential comparison, also if `1−e_n` is negative. Off the truncated event the right side vanishes. Lemma T therefore applies with exactly the independence it requires and gives line 71.

- **Lines 72–77, orthogonal rates.** The deterministic envelope `ψ_n=√ω_n+(log n)/(2√n)` bounds `log T/√n` and tends to zero. Choosing `x_n=ψ_n^(−1/2)` gives event error `ψ_n` and exponent error bounded by a constant times `ψ_n^(1/2)+ψ_n²+(1+(M+M′)/σ*²)ψ_n/√n`. All preliminary indices and rate bounds depend only on the permitted parameters and the common envelope sequence. This verifies the asserted uniform `n₀` after the S1 clarification.

- **Lines 80–87, spherical scores and event.** Parent lines 75–85 establish that the residual direction is an ε-measurable unit vector in `1^⊥`. Conditional rotation invariance gives the same product distribution for the entire finite score vector for every ε. The conditional-expectation identity in line 84 proves independence of that vector from ε, not merely marginal independence of each score. Parent lines 86–99 give the claimed coefficient bound, event probability, and constant `C₀`. These steps do not use the parent's subsequent `log N` choice of `x`. The rank bound `m≥n/2` follows from `r₀≤s₀≤K−1`.

- **Lines 88–100, spherical comparison and rates.** The positive-part bound handles `κ′_n>1` correctly. Every `U_j` is bounded by `T` and independent of the ε-measurable event `G`, so Lemma T applies with the same event for all coordinates. The two bounds on `θ_n` follow from the integrated sphere density. The envelope for `log T/√n` ensures the cutoff restriction and convergence of both endpoints to one. Since `log T≤log(pn)`, choosing `x_n=(ω′_n)^(−1/2)` makes the exponent and exceptional-event errors vanish with the claimed parameter dependence. Although the displayed lower probability bound can be negative at small `n`, this is harmless and is positive eventually. The required uniform starting index is controlled as described in S1.

- **Lines 103–111, uniformity, conditioning, and limit.** `N_n` enters the proof only through `Λ^E_n`, with all error bounds controlled by the common deterministic sequences. Conditional Gaussian noise and the conditional witness hypotheses permit the same estimate on every point of `𝒜_n`. The nonnegative and negative right-hand-side cases in line 108 correctly justify multiplication by `P(𝒜_n)`. Deterministic `S₀,p,𝒩_n` make `Λ^E_n` deterministic as required. Division by its positive value and then letting `ϵ↓0` proves the limit form, including the random case when `P(𝒜_n)→1`.

- **Lines 114–122, Corollary A1-E.** For the whole orthogonal null block, dimension counting yields `p≤n−1+s₀−r₀≤2n`; hence the extra logarithmic condition is automatic. In the spherical case it is assumed. With fixed `s₀`, these conditions give `ℓ_n/n→0`, so `Λ^E_n→0`. The denominator in the statement is exactly `Λ^E_n`. For diverging `p`, the block factor tends to one. The polynomial choices give `ℓ_n=(a+1/2)log n+O(1)`, including the clipped orthogonal choice at `a=1`. For fixed `p`, the expansion is `ℓ_n=(log n)/2+O(1)` and produces the factor `1/√(2π)`. These prove both stated specializations.

- **Lines 125–132, Corollary A2-E and rank recovery.** Re-derived F1–F3. Parent B1 at `STATEMENT.md:99` is a deterministic, design-free bound under `s₀≤min(K−1,p/2)`; it does not require `N→∞`. Its lower bound for `δ_n` forces `(s₀+1)/√n→0` from `Eδ_n→0`. Combining this with `(log p+log n)/√n→0` recovers the spherical rank condition. The application is valid without assuming that rank condition initially.

- **Lines 133–145, sub-blocks and conclusions.** The one-column increment `Δ_n` tends to zero. Every subfamily inherits the witness structure, and the uniform index from Proposition A-E applies simultaneously to all sub-block sizes because `p` and the common growth envelopes stay fixed. The floor choice of `k*_n`, including its zero case, gives line 140. Thus consistency forces `Λ^E_n→0`. F2 makes this equivalent to the quantity asserted in (i). Applying the limit form after (i) and using `ℓ_n≥(log n)/2` yields the displayed lower multiple of `(s₀+1)r_n`, proving (ii).

- **Lines 148–153, remarks.** The heuristic tail explanation is consistent with the proved truncation argument. The parent assumption-map row 15 concerns the in-probability logarithmic mechanism; its use here is explicitly limited to that mode. The numerical claim is identified as an observation and is not used in the proof. Its referenced numerical files were not read or independently reproduced under this brief.

**Statement match:** after S1's local clarification, the proof establishes exactly Proposition A-E, including its uniform and random-parameter clauses, and Corollaries A1-E and A2-E. No use of the parent weak law or of `N→∞` is needed for these claims.

## A2C_critical: checks and re-derivations

- **Lines 5–15, hypotheses and claim.** These match STATEMENT §3.4. The parent's `N→∞` assumption is retained here. The case `λ=0` is immediate for all four claimed conclusions.

- **Lines 18–20, sizes.** The asymptotic identity cited at parent `A_log_factor.md:121` follows from `N/p→1`, the block factor tending to one, and `log N/log p→1`. Bounded `Λ_n` and diverging `log p` force `s₀=o(√n)`. Both `p−s₀` and `⌊n/2⌋−s₀` diverge, hence their minimum `K−s₀` diverges. Inequality (1.1) is valid and gives `c_nN→0`.

- **Lines 23–32, exact multi-step identities.** At each addition the new column is orthogonal to the current model, so parent Lemma S(1)'s equality case gives determinant ratio exactly `n`. Lemma S(2) gives fit decrease `(x_kᵀy)²/n`, independent of previous null additions. Telescoping proves both multi-step identities. The relation involving the sum of the original one-step `γ_k` follows directly from their common denominator. Positivity of `2b₀+Q` ensures that this sum is strictly below one.

- **Lines 33–40, prior and (2.1).** The ratio of the actual coded binomial priors is the displayed product. Each factor is at least `P_n`, and all denominators remain positive for admissible model sizes. Applying `−log(1−u)≥u` to the sum of the nonnegative `γ_k` gives the product of `V_k`. The admissible supersets indexed by different `J` are distinct, so summing gives (2.1) without overcounting.

- **Lines 43–46, truncation.** The common `κ_n` identity and the event bound are precisely parent lines 53–68. Here `N≤n−1` and `N→∞` hold, so `τ=2 log N` is positive eventually and the cited coefficient-event limit is applicable. The exponential comparison from parent line 46, monotonicity, and homogeneity of `e_j` give the stated lower bound. No independence of `κ_n` and the scores is assumed.

- **Lines 49–52, collision bound.** Re-derived by expanding the ordered product and taking a union bound over equal-coordinate pairs, with all weights nonnegative. Multiple collisions only cause harmless overcounting. The separately specified `j=1` case is `e_1=A`; in line 60 its collision term is understood to be absent, as specified here.

- **Lines 55–58, first moment, weak law, and collisions.** `W_k≤N` gives `B_n≤(c_nN)A_n`. The Gaussian truncated mean and identity (0) give `EA_n=Λ_n` exactly, hence tightness by nonnegativity and Markov. Parent Lemma W with `η=η′=0` gives the exact displayed lower-tail probability. Since `c_nN→0`, `B_n=o_P(1)`.

- **Lines 59–61, polynomial bound and remainder.** Every fixed `J₀` is admissible eventually by the size calculation. The finite sum of collision errors is bounded by the nonnegative infinite series after discarding the exponential discount. The identity `Σ_{j≥2} C(j,2)A^(j−2)/j! = e^A/2` is exact, including at `A=0` with its power-series interpretation. Tightness of `A_n` implies tightness of `e^{A_n}`, so `B_ne^{A_n}/2=o_P(1)`; no exponential-moment bound is needed.

- **Lines 62–65, order of limits.** One may first choose finite `J₀` so that the undiscounted partial exponential series at `λ` exceeds `e^λ−1−η/4`, then choose positive `ϵ` and `ϵ′` sufficiently small by continuity. This gives line 62 with slack. Keeping these choices fixed, `Λ_n→λ>0` ensures `(1−ϵ′)Λ_n≥(1−ϵ′)²λ` eventually. Monotonicity and the remainder bound prove the event inclusion, and all three exceptional probabilities tend to zero. There is no exchange of a growing `J₀` with the probability limit.

- **Lines 66–70, equivalence and expectation.** The reciprocal transformations prove equivalence of the families of statements over all positive tolerances; no claim that an identical tolerance transforms exactly is used. Boundedness of the posterior probability yields the stated expectation inequality, followed by `η′↓0`. This is exactly the expectation consequence in STATEMENT line 100.

- **Lines 73–77, remarks.** The comparisons with the parent's linear-odds bound and design-free B1 critical cap are consistent with the parent statements. The orthogonality restriction is retained. No spherical multi-step result is asserted.

**Statement match:** all hypotheses, the finite critical scale, the all-tolerances probability statements, and both expectation consequences agree with STATEMENT §3.4. No additional growth or independence hypothesis is used.

## Independent numerical checks

I ran small, deterministic-seed Python/NumPy checks directly from standard input. No script or numerical-output file was written, and no supplied numerical file was read. The prescribed temporary directory was created and removed; no temporary artifacts remain.

- **Sphere truncated mean:** 512-node Gauss–Legendre integration for 42 `(d,τ)` combinations, with `d∈{3,4,5,10,30,100,1000}` and cutoffs from `10⁻⁵` to `1` times `d/2`. Every integral lay between the claimed bounds. Minimum `mean/lower` was approximately `1.000253`; minimum `upper/mean` was approximately `1.000756`.
- **Lemma T:** exact enumeration of 72 two-coordinate, two-point iid examples, with each `G_j` depending on the other coordinate. All inequalities held. These deliberately allow dependence between different events and between an event and other scores.
- **Lemma F algebra:** 10,000 sampled choices within its stated endpoint tolerances. All finite algebraic inequalities held. This tests the algebra, not the missing starting-index qualification in S1.
- **Exact coded multi-step ratios:** 90 admissible null supersets across centred orthogonal constructions at `n∈{12,20,50}`, including duplicated true columns so the true block can be rank deficient. Maximum error in the log-determinant identity was `3.6×10⁻¹⁵`; maximum additive-fit error was `2.6×10⁻¹⁴`. Every exact posterior ratio exceeded the proposed lower bound; the smallest ratio to the lower bound was about `1.000000070`.
- **Collision inequality:** 5,000 checks across nonnegative vectors with zero coordinates and degrees 2–6. All inequalities held to floating-point tolerance.

The independence assertions, uniformity, conditional argument, asymptotic rates, and probability limits were checked analytically as described above. The numerical checks are supplementary and do not certify those claims.
