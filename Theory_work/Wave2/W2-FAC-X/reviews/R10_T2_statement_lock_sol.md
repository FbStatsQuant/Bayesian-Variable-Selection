# R10 — Target-2 statement lock, adversarial review

Verdict: **LOCK-WITH-CHANGES**. The v1 statement must not be marked locked until required changes 1–4 below are incorporated. This is a statement/proof-map viability review, not a line-by-line verification or an upgrade of any draft lemma's status.

Reviewed: `STATEMENT_T2.md` v1; `T2/{STATEMENT_T2.md,L4r_path.md,NOTES.md}`; lemmas X7–X10; relevant X1–X5 representation, perturbation, start and path arguments; FAC-B's statement and start argument; both supplied numerical summaries; Wave-2 and its two ancestor protocols. Paths below are relative to `Theory_work/Wave2/W2-FAC-X/` unless explicitly prefixed. Only this review file was written. No new numerical experiment is claimed; the falsification below is analytic.

## Required changes

1. **Correct the coordinates and the population meaning of (FS-G).** `STATEMENT_T2.md:30–35` combines the sign-corrected vector ϑ with the signed covariance Σ_n. These are different coordinate systems. Define Σ⁰_n := Υ_nΣ_nΥ_n and formulate the condition as

   c⁰_n(U,l) := (Σ⁰_nϑ)_l − Σ⁰_{n,lU}(Σ⁰_{n,UU})⁻¹(Σ⁰_nϑ)_U,
   with |c⁰_n(U,l)| ≥ c_FS for every nonzero pair. Alternatively use Σ_n with the uncorrected coefficient vector Υ_nϑ. The actual partial covariance in the original coordinates is Υ_{n,ll}c⁰_n(U,l), so its absolute value agrees with the corrected formulation.

   This matters substantively: take unsigned CS with ρ=1/2, two truths, corrected coefficients (1,−2), and flip the second truth's column. The true marginal signal at the first truth is 1+(1/2)(−2)=0, whereas the displayed signed-Σ-times-ϑ expression gives 1+(−1/2)(−2)=2. Indeed the displayed condition tests, after sign correction, the fictitious positive truth vector (1,2); its nonzero pairs are uniformly separated from zero for |U|≤15. Thus the current condition can pass while the non-masking dichotomy used by X8 fails. This is a counterexample to the asserted identification of the hypothesis, without assuming any particular production partition. X8's opening “Υ_n=I” is justified only after this hypothesis is made invariant under that change of coordinates.

   Also define this as a population regression functional. In (R), use a single raw population row and its linear signal with raw coefficients β; in (G), use the population/reference Gram functional with coefficient θ*. Do not identify it literally with the covariance of a random standardized sample column and the n-vector μ. Retain a single c_FS>0 independent of n, U and l, at least for all sufficiently large n. Pointwise nonzero covariances for each n would not suffice when the loadings approach a masking configuration.

2. **State the actual FAC-NCS conclusion, reference variables, and replacement hypotheses.** `STATEMENT_T2.md:51–53` imports (C1)–(C4), including the numerical band width in (C2), without the essential replacement in `lemmas/X7_near_cs_loadings.md:16–17`. Put that replacement into the locked statement:

   Δ_n := max_j|λ_j−λ̄|;
   ϖ′_n = ϖ_n + C₇H̄_nΔ_n for (R), and
   ϖ′_n = C₇H̄_nΔ_n + n^(−1/3) for (G).

   Every occurrence of ϖ_n in the imported deletion tolerance and band/path conclusion must mean ϖ′_n. Define the CS reference x_T using λ̄ and the appropriate (G)/(R) κ and ϱ from X7, rather than the general-loading X_T. The additional Δ_n term can dominate the original rate for arbitrarily small c₂; X7 does not establish the original width. I am not asserting a counterexample to the corrected-width corollary.

   Say explicitly that the corollary assumes the corresponding design model, (θ), the implementation/delivery premises as appropriate, the near-equality condition, (P-½), and limiting-CS (FS), **in place of** (P-S) and (FS-G). As written, “moreover” is ambiguous about retaining the theorem's smaller exponent restriction. For (G), the fixed coefficient assumption must be on θ*, not the raw β assumption of Target 1. This should be a standalone corollary specification, not an unqualified invocation of an iid-only theorem.

3. **Repair the X7 transfer for unrestricted c₂>0 before using it to lock FAC-NCS.** The assertion that X4 uses its error scale only through polynomial decay and that X4 transfers unchanged (`lemmas/X7_near_cs_loadings.md:42–47`) is false. There are at least these concrete rate dependencies:

   (a) X4's small regime is p≤n^(1/200), and D8(S) requires every pair of distinct null ξ's to be separated by c₁ϖ (`lemmas/X4_path.md:30–32,46`). Polynomial decay alone does not imply p²ϖ→0. For an admissible loading sequence λ_j=λ̄+n^(−0.001), p=⌊n^0.004⌋, and fixed s₀, the proposed replacement width has order H̄_n n^(−0.001). Hence p²ϖ′ diverges. In a fixed interval where the Gaussian density is bounded above and below, let Z count pairs at distance at most c₁ϖ′. Then E Z has order p²ϖ′→∞ and Var Z is O(p²ϖ′+p³(ϖ′)²); the second-moment bound gives P(Z=0)→0. D8(S) therefore has probability tending to zero, not one. This construction can use positive truth coefficients satisfying (FS), and applies to both design models' ξ representation. It falsifies the proposed high-probability proof event, not consistency itself.

   (b) D7's sparse-tail union bound fixes c_w=(1/2−A₁)/4 and T₀ from that exponent (`lemmas/X4_path.md:28–29,41–43`). Its rate argument must be redone using a decay exponent for ϖ′ that also accounts for c₂.

   (c) X4's bulk B3, Case B, uses p w²+w log n=o(1) to bound the deleted negative sum below by −1. With w=4.3ϖ′ this need not hold: p≈n^0.4 and Δ_n=n^(−0.01) already violate it. After division by m≈p a weaker estimate might suffice, but the displayed argument is not unchanged.

   A viable repair may choose the small/large cutoff using a proven decay exponent for ϖ′, rechoose D7's constants, and carry the weaker Case-B error through the normalized centre inequality. Another possibility is to use the uniform path result for the problematic small regime and separately establish the desired band structure there. Spell out and justify the chosen repair; do not silently strengthen c₂>0. If it cannot be supplied, narrow or defer FAC-NCS rather than treating X7 as a completed transfer. Ordinary lemma checks can follow, but a known event of probability tending to zero cannot be deferred as a minor line-check issue.

4. **Bind A₁ and the asymptotic quantifiers in (G2).** `STATEMENT_T2.md:36,45` uses A₁ in the constant without defining it. Select any fixed

   limsup_n log p_n/log n < A₁ < A_S,

   so p_n≤n^A₁ eventually. The constants bounding loading dispersion are fixed across the sequence; λ^(n) and the support may vary as declared. State that the probability-one-limit event is simultaneous over all T for the given deterministic triangular array, while n₀ may depend on the fixed coefficient vector, σ, the compact loading bounds and A₁. No simultaneous coupling over every possible loading array is being asserted. Keep the positive logarithmic margin distinct from the truth-move constant, which also depends on the signal and noise parameters.

## Assessment of the requested break points

**Right target and faithful method.** The deliverable remains an asymptotic discovery/reported-model consistency and delivery theorem for the merged score, BB prior, actual block start and MR1 search cap. The proposed smaller range and uniform-over-T path claim change the theorem's coverage, not the algorithm. X10 uses the actual start and the single-search prefix property; it does not infer unconditional delivery merely from D_n→0. I found no need for a method change in this review.

**Start hypothesis after change 1.** The corrected uniform population condition is strong enough for the X5/X8 route: all conditioning sets have at most 15 members, and U∪{l}∪S₀ has bounded size because s₀ is fixed. The eigenvalue floor 1−λ_hi² controls the inverse in the regression functional uniformly. Thus entrywise sample-correlation and support-scale errors are uniformly o(1), even for n-varying loadings. Exact zero pairs remain exactly zero because the signal belongs to span(X_U). For random blocks the zero-pair noise bounds must remain conditional on the raw design, as in X5; no independence of N₀ from ξ is available or needed. This reasoning does not rescue the mixed-coordinate condition currently printed.

**Uniform exact-Gram path and A_S.** I tried adversarial same-sign kept tails and opposite-sign excluded extremes, as well as a single high-loading kept null. I did not obtain a counterexample inside the declared strict range. L4r.2(a)'s weighted residual identity supplies a good deletion without requiring per-class balance. L4r.2(b)'s top-square bound is genuinely uniform over all subsets. The resulting leading margins in L4r.3 are

    deletion: 1/2 − A₁ max(1,γ̄),
    addition: 1/2 − A₁((1+R)²−1).

Both are positive under the stated bound. Telescoping at T∖{j}, which still contains S₀ for a null deletion, makes the uniform no-addition bound sufficient for every null-out swap. The full model has no feasible additions; the truth set has no null deletions. Neither boundary needs an extra hypothesis. These are viability observations, not a declaration that L4r-S is lemma-checked.

**Iid transfer.** X9's operator-norm route avoids conditioning a Gaussian row on a path-dependent set. Principal-submatrix norm bounds and a bound on the full vector norm apply to every T simultaneously. Its stated error is

    C[p/√n + √(p log n/n) + √(log n/n)]H̄_n.

The p/√n term is affordable because R≥1 implies A_S≤1/6<1/2. In particular δ̄_n H̄_n→0, so squaring the reference statistic produces o(1) errors, smaller than the positive log n margins. I found no dependence counterexample here. Do not simplify this to C(p/√n)H̄_n uniformly for bounded or very slowly growing p: the other terms cannot then be absorbed into that expression with a fixed constant. X9's full displayed bound should be retained.

**Frontier.** Section 4 correctly refrains from asserting failure of the algorithm. Its examples support failed proof invariants and observed positive additions at non-path sets, not an asymptotic necessity theorem for every loading array. The phrase “stops near A_S” needs that distinction. The supplied N2X summary describes 32 iid paths and 32 reference-mode paths; the latter are not the same exact-Gram model as T2's 366 paths. “430 simulated data sets” is an aggregate diagnostic count, not 430 independent exact-Gram validations or a proof about the asymptotic frontier.

## Optional suggestions

1. Simplify or explain the exponent. Since s₀≥1,

       γ̄ = R²ℓ_lo²/(1+s₀ℓ_lo²) < R²,
       max(1,γ̄) < R²+2R = (1+R)²−1.

   Consequently the addition restriction always determines A_S: A_S=1/[2(R²+2R)]. Keeping both terms is useful for the proof map, but readers should not mistake the deletion restriction for an independently active bottleneck. Bounds chosen wider than the realized loading range give a correspondingly conservative theorem.

2. Make the frontier explicitly asymptotic or label its current support as finite numerical evidence only. A useful analytic obstruction to investigate is two loading classes of positive limiting proportions, keeping m=⌈(log p)²⌉ largest positive low-loading nulls and adding the most negative high-loading null. For p=n^a, the reference centre has ℓ_lo X_T≈√(2 log p), the addition residual is approximately −(1+R)√(2 log p), and the prior cost is log p+(1/2)log n+o(log n). This suggests gain [(R²+2R)a−1/2]log n+o(log n), matching the sufficient threshold for a worst-case class configuration. Establish the order-statistic and score approximations before claiming sharpness; the existing finite examples at exponents 0.33 or 0.155 do not themselves do that.

3. X8 states its own lemma for p≤n/2, beyond what FAC-GL needs. The cited D1 bound r_n=3√(p/N)+3√(2 log n/N) does not give the advertised ψ_lo/5 global sample-correlation eigenvalue floor throughout that larger range. Either restrict X8 to the polynomial range used here, use only bounded-size submatrix floors in its proof, or supply an appropriate separate sample-Gram eigenvalue argument with revised constants. This does not force a narrower FAC-GL range.

Required disposition: apply 1, 2 and 4 to the statement; resolve 3 in the proof map or withdraw/narrow the affected corollary. No counterexample to the corrected FAC-GL uniform path claim within A_S was established. FAC-NCS as printed and its claimed unchanged X4 transfer are not ready for lock.
