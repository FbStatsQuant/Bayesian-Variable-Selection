L6 line check — lemmas/DIST12.md sha256 c05fb3f082fcb938

Scope: independent check of the assembly from the stipulated Lemmas H, T, X and X′. I read the brief, DIST12.md, STATEMENT.md only before its Changelog, API_CARDS.md, and X.md §§0, 7, 9. I did not review the proofs of the four input lemmas, follow their external references, or read any other ticket material. All references below are to this permitted packet. No agents or state-changing git commands were used.

Findings

**L6-01 — MAJOR — D.4, lines 65–66; STATEMENT §1, consequence (c), lines 84–85. Quantitative dependence of the best-rate level is not established.**

The instruction “(c): take t = M₀ log n” proves a radius of order √(log n/n) for fixed allowed constants. It does not establish the additional assertion that M₀ is of order (1+s₀^r)(A+1). D.0 imports the constants of X.md §0, which specify, with s=s₀^r and B=M+M′,

    M₀ = max{16, (A+1)s, log C₅},
    C₅ = 4^(s+1) exp(3B/(2σ²)) (8A+4)^(s/2) K_s,
    K_s = Σ_{i≥0}(1+i)^s 2^(−i).

For integer s≥1 the single i=s term gives

    log K_s ≥ s log(1+s) − s log 2.

Consequently the supplied M₀ grows at least as s log s with A and B/σ² fixed. Its stated formula does not have the claimed linear dependence on s. The hypotheses of Lemma X in STATEMENT §3 merely allow arbitrary dependence on the listed constants and supply no smaller level. Nor does this assembly prove a separate rescaling of Lemma X that yields the claimed level while checking the entire t-range and the resulting c, C and C′. This is a gap in the requested consequence, not a counterexample to display (1.1).

There is also an unproved change of sparsity parameter in the same sentence: the deterministic transfer bound uses raw s=s₀^r even when s₀<s. The proved constants therefore depend on raw sparsity. The phrase “of order (1+s₀) log p/n” must not be read as an established uniform dependence on the random retained sparsity. For fixed s this remains an order-in-n description, but that weaker interpretation supplies no such parameter dependence.

Minimal repair: state consequence (c) as “ε_n²=C²M₀ log n/n, with constants depending on the parameters listed in §0; hence ε_n² is of order log n/n for fixed parameters,” and retain raw s₀^r when describing the supported sparsity dependence. Alternatively, supply a separate quantitative argument for the asserted linear level and explain exactly what dependence is hidden in C. The displayed contraction theorem needs no change for this repair.

Verification of the assembly

**D.1.** Both levels use deterministic p_raw, s and t, and the deterministic C_m from X.md §0; neither uses p_ret or s₀. The supplied

    C_m = 2s+1 + [s(A+2)+5]/log 2

indeed bounds m_n(t)+s₀ by C_m t for t≥log n and t≥1: use log(2p)≤(A+1)log n, log(n+1)≤2log n, and the ceiling bound. For a sufficiently large deterministic n_T, chosen for all larger n at t=n^(1−κ₀), both uncapped levels are at most n−1. They are positive whenever p_raw≥1. If p_raw<2 is admitted in (RD), 𝒟_n is empty and the theorem is trivial after the usual extension of the posterior outside its domain; no use of Lemma T at d=0 is necessary. This harmless domain convention should be understood in the displayed probabilities, as already indicated by STATEMENT §0.

Recomputation of the entropy terms gives exactly

    η²_n(d,e^(−t)) ≤ (4/n)[(A+7)d log n + 6log n + 2t].

For d₁, d₁log n≤(2s+33)t, so the stated C_T=4[(A+7)(2s+33)+8] is valid. For d₂, d₂≤(s+1+C_m)t and log n≥1, so the stated C_T′=4[(A+7)(s+1+C_m)+8] bounds η²_n(d₂,e^(−t)) by C_T′t log n/n and hence by C_T′tℓ_n/n. The two “+8” terms account for 6log n and 2t in the respective normalizations. No missing factor was found.

**D.2.** √n ε̄/σ is standard Gaussian, so P*(𝓘_tᶜ)≤2e^(−t) at the given threshold. Lemma X concerns the contrast noise e and contains no bound on ε̄. The separate event is necessary for this plug-in intercept argument. Independence between ε̄ and e is available but unused.

**D.3.** Identify retained indices with their original raw indices. Since b is zero on every dropped column, supp(b−β*)⊆S∪supp β*, including dropped true columns, and its cardinality is at most min(p_raw,|S|+s). With C denoting the centering projection, Δ_i=ε̄+[CX^r(b−β*)]_i=ε̄+(μ̂−μ)_i. Both μ̂ and μ are centered, so the cross term vanishes in the in-sample squared mean. Lemma T is simultaneous in the intercept and direction, and therefore applies to every data-dependent posterior draw on its one design event. At c=4σ² the factor 2 yields precisely the coefficient 1/(2σ²) in (D.3). No population moment is used.

**D.4, Step 1.** Conditioning on X^r makes the retained index map, standardization, X, p, θ*, S₀, s₀, μ, K, m_n(t), and all interfaces deterministic. On G_t they meet the stipulated Lemma X hypotheses. Increase the common deterministic threshold to include n≥2s if necessary; this is allowed and preserves one threshold for the entire range. The stipulated contrast-posterior identification and independence of ε from X^r give the conditional bound and its integral over G_t. Constants are uniform in the retained design and over the finite range 0≤s₀≤s. The posterior kernels and bad-set integrals are measurable on each retained-index stratum: the formulas involve continuous matrix operations with the positive ridge term; the population Hellinger loss is a bounded measurable integral. Lemma T supplies its measurable simultaneous event as an input. A sample-constant response is a conditional probability-zero event under the nondegenerate Gaussian noise and does not add a remainder.

**D.4, Step 2; D.5.** Outside Bad_X, |S|≤s₀+⌈32t/log n⌉. The raw support bound is therefore covered by d₁, and t/log n≥1 gives the claimed size inclusion with C′=33. Formula (D.3), the intercept event, and the checked C_T give C²=C_X²+C_X/2+1+C_T exactly. Both strict bad-set inequalities have the correct direction. The rounding warning in D.5 correctly identifies why this inclusion is unavailable with C′=32 from the stated input alone.

**D.4, Step 3 and uniformity.** A union bound gives

    P*(bad data) ≤ P*(G_tᶜ)+2e^(−t/2)+e^(−t)+2e^(−t)
                 ≤ P*(G_tᶜ)+3e^(−t/2),

because t≥16 implies 3e^(−t)≤e^(−t/2). There is no assumption of independence between the transfer event and G_t, or between these events and the noise success event. The union defining G_tᶜ is exactly the remainder of (1.1). The given uniform thresholds for X and the deterministic transfer threshold can be enlarged once to include n≥3 and n≥2s; every enlargement depends only on the allowed constants. The resulting conclusion is for every fixed n and t in the entire specified range with the same constants and n₀; simultaneous success for all t on a single event is neither used nor claimed. Display (1.1), with c=1/2 and C′=33, is verified.

**Consequences.** Substitute t=nε_n²/C² to obtain the displayed marginal-distance bound on exactly the stated ε_n interval, with the interfaces evaluated at that t. Under the premise in (a) its upper bound is 4e^(−c₁nε_n²), a polynomial at the lower endpoint; (b) follows since nε_n²≥C²M₀log n→∞. These are valid as the asserted exponential form and convergence statement; a literal unit prefactor in a different formulation would require the usual further weakening of the exponent. Consequence (d) follows from the distribution-free transfer event. For (e), concavity of the square root, integrated against f*, gives convexity of d_H² in its first argument. Split the posterior integral into the radius ball and its complement and use d_H²≤1. This proves the bound on the complement of the actual displayed bad-data event, even if an interface fails there. No additional result from the unpermitted file cited on line 68 is needed. The quantitative refinement of (c) is the finding above; its fixed-parameter order in n is verified.

**D.6.** The input constants in X.md §9 have c=1/2 and no dependence on c_D. Its M₀′≥16 ensures all lower-level assumptions used in D.1–D.3. On G_t′ the conditional argument applies exactly as for X. Outside Bad_X′, |S|≤m_n(t), and

    |S|+s ≤ m_n(t)+s₀+s ≤ C_m t+s ≤ s+⌈C_m t⌉,

so the full raw direction is covered by d₂. The variance and intercept terms are at most (C_X′²+1)t/n, the fit term is C_X′tℓ_n/(2n), and the transfer term is C_T′tℓ_n/n. Since ℓ_n≥log n≥1, their sum is bounded by the stated C₂²tℓ_n/n with C₂²=C_X′²+1+C_X′/2+C_T′. The same union bound proves (1.2) with exactly the three-interface remainder and 3e^(−t/2). There is no residual use of (ND) or c_D. The optional size conclusion follows on the same constructed success event.

Adversarial cases

- Atoms and infinite second moments of x cause no extra assumption: the population loss in the transfer and Hellinger bounds is bounded, while every finite sample in ℝ^p has finite coordinates.
- A true column constant in the sample contributes zero to μ but remains in the raw direction b−β*. Its sample contribution is canceled by the plug-in intercept, and its population contribution is covered by Lemma T at raw sparsity s. No step replaces s by s₀ in the transfer level.
- With p_raw≠p_ret or s₀<s₀^r, conditional fixed-design bounds use retained quantities, while the transfer and constants use the deterministic raw quantities. This is valid for both displays.
- When s₀^r=0, both deterministic transfer levels remain positive and the intercept event still supplies the missing mean control. Empty true models and zero signal are allowed by the stipulated inputs.
- At p_raw=2, the event 𝒟_n forces both columns to be retained; d_i≤2. Designs losing either column are covered by the domain remainder. No growing-dimension lower bound is used.
- At the lower t endpoint, t≥16 and t/log n≥1 justify the entropy, rounding and probability absorptions. At the upper endpoint, both deterministic transfer levels are o(n), and the input lemmas have one uniform n₀. No edge-case law in (RD) was found that breaks either displayed inequality, conditional on the four supplied lemmas.

Verdicts

- D.1: VERIFIED.
- D.2: VERIFIED.
- D.3: VERIFIED.
- D.4 / DIST-1: NOT VERIFIED as the full requested package including the quantitative consequence (c); display (1.1) and consequences (a), (b), (d), (e) are VERIFIED. The fixed-parameter √(log n/n) rate in (c) is also VERIFIED.
- D.6 / DIST-2: VERIFIED for display (1.2), its exact remainder and its stated admissible parameter dependencies.

Overall verdict: NOT VERIFIED as written — the two displayed contraction bounds are verified, but the quantitative sparsity dependence asserted in consequence (c) is not established.
