<!-- Proof check PC1 (Opus 5.5, Claude Work, read-only), 2026-11-03; commissioned by the chair. Filed verbatim. Scripts in 2026-11-03_PC1_scripts/. -->
# PC1 — proof check for the MEET-v31 chair

Read-only. I edited, committed and pushed nothing, and started no subagents or jobs. The scripts are in `/tmp/claude-71711/-home-fb31--t3-worktrees-Bayesian-Variable-Selection-theory-MEET-v31/14bcdd62-deb0-4c36-99c9-68518a64c746/scratchpad/pc1/`. They use fixed seeds 20261103–20261106 and exact enumeration at p ≤ 12. Status words follow `PROTOCOL.md`, and every PROVED below is a **candidate**.

---

## Claim 1 — analytic upper bound on Z (Seat C, R1_C §4 item 4)

**Verdict: PROVED.** It holds for the spec's m(S) exactly as written. The amendment is only about wording: the bound needs no centring or standardisation of y.

**Spec check (METHODOLOGY_v3 §5; 00_COMMON §1).**
- There is no intercept, and y is centred and standardised, so yᵀy = n − 1.
- H_S = (n+1)G_S + I_k and Q_S = yᵀy − n z_Sᵀ H_S⁻¹ z_S.
- log m(S) = log C_n − ½[log det H_S − log det(G_S + I_k)] − ν log(2b₀ + Q_S), with ν = a₀ + n/2.
- 00_COMMON defines D_S = det H_S / det(G_S + I) and writes m(S) = C_n D_S^{−1/2}(2b₀+Q_S)^{−ν}. This is exactly C's form. The "g/(g+1)" factor is not a separate factor; it appears through H_S = (g+1)G_S + I with g = n.

**Proof.**
1. G_S ⪰ 0 has eigenvalues λ_i ≥ 0. H_S and G_S + I are polynomials in G_S, so they share its eigenvectors. Hence D_S = ∏_i ((n+1)λ_i + 1)/(λ_i + 1) ≥ 1, with each factor ≥ 1.
2. Q_S = yᵀ(I − nX_S H_S⁻¹ X_Sᵀ)y. The nonzero eigenvalues of X_S H_S⁻¹ X_Sᵀ equal those of H_S^{−1/2} G_S H_S^{−1/2}, which are λ_i/((n+1)λ_i + 1) < 1/(n+1). So the matrix I − nX_S H_S⁻¹ X_Sᵀ ⪰ (1/(n+1)) I, which gives Q_S ≥ yᵀy/(n+1). This holds for every y. For S = ∅, Q = yᵀy.
3. Therefore m(S) ≤ C_n(2b₀ + yᵀy/(n+1))^{−ν} for every S ∈ Ω.
4. Σ_Ω ϖ = 1, because ϖ is normalised by W_K. So Z ≤ C_n(2b₀ + yᵀy/(n+1))^{−ν}. On the spec's scale this is C_n(0.02 + (n−1)/(n+1))^{−ν}. ∎

The spec's remark "With y standardised, Q_S ≥ yᵀy/(n+1)" is true, but the qualifier is not needed.

**Looseness.** Z/m(∅) ≤ [(2b₀ + yᵀy)/(2b₀ + yᵀy/(n+1))]^ν ≈ (n+1)^ν. At n = 200 that is about 530 nats. So C's own description, "may be extremely loose", is accurate.

**Numerical check (`c1_bound.py`).** Exact enumeration with the spec's standardisation:

| case | n | p | K | log Z | log bound | min Q_S | yᵀy/(n+1) |
|---|---|---|---|---|---|---|---|
| independent | 20 | 10 | 10 | −22.24 | −2.48 | 1.399 | 0.905 |
| correlated | 30 | 12 | 12 | −37.66 | 4.09 | 5.784 | 0.935 |
| p > n | 8 | 12 | 4 | −13.81 | −6.51 | 0.882 | 0.778 |
| strong signal | 15 | 10 | 7 | −16.63 | −4.84 | 0.957 | 0.875 |

In every case min log D_S = 0 (attained at ∅). A raw, uncentred y also satisfies the bound. No violations.

---

## Claim 2 — L = max{Z_𝒯, 0.05Ẑ} has coverage ≥ 95% (R1_C §4 item 5; output-event version, item 8)

**Verdict: PROVED** for the potential run. The output-event version is **CORRECT WITH AMENDMENT**: it needs hypotheses stated explicitly.

**Potential-run statement.** Assume:
- EX-A (exact arithmetic);
- the reported Ẑ ≥ 0 with E[Ẑ | 𝓒] ≤ Z (unbiasedness, T12 and P6/P7, gives equality);
- 𝒯 is a set of distinct feasible models;
- Z_𝒯 := Σ_{S∈𝒯} ϖ(S)m(S), using the same W_K and the same m.

Then P(L > Z | 𝓒) ≤ 0.05.

**Proof.**
1. Z_𝒯 ≤ Z on every outcome, since the summands are distinct, nonnegative terms of Z.
2. So {L > Z} = {Z_𝒯 > Z} ∪ {0.05Ẑ > Z} = {0.05Ẑ > Z}. The two events are equal, not just nested.
3. By Markov, P(Ẑ > 20Z | 𝓒) ≤ E[Ẑ | 𝓒]/(20Z) ≤ 0.05, using Z > 0.
4. Average over 𝓒. ∎

Two notes:
- Adding Z_𝒯 leaves the coverage probability unchanged and raises L pointwise.
- Distinctness matters: a store that holds duplicates and sums them could exceed Z. Lemma S guarantees distinct pairs.

**Output-event version: amended statement.** P(𝒪 ∩ {L > Z}) ≤ 0.05·P(SMC ∩ 𝒜) ≤ 0.05. This needs:
- (i) Lemma RO / GUARD: on 𝒪 the reported Ẑ, 𝒯 and Z_𝒯 equal the potential run's.
- (ii) On the SMC part of 𝒪 the calibration succeeded (𝒜), and E[Ẑ̄ | 𝓒] ≤ Z for every successful 𝓒.
- (iii) CAL and EX-S: the final streams are independent of 𝓒.
- (iv) On the exact branch Ẑ = Z, so there is no exceedance.

Proof: by (i), 𝒪 ∩ {L > Z} ⊆ SMC ∩ 𝒜 ∩ {0.05Ẑ̄ > Z}. Condition on 𝓒 and apply the potential-run bound. C's sketch, "Markov coverage and event inclusion", is right, but premise (i) has to be named because it is where the guard enters.

As C says, the result is **not** P(L > Z | 𝒪) ≤ 0.05.

The floating-point version of "Z_𝒯 ≤ Z deterministically" is not covered. It is OPEN (C item 8 agrees).

**Numerical check (`c24_twostate.py`, exact rationals).** Setup: two states, π₀(a) = 0.01, π(a) = 0.99, one particle, one stage. Results: E W = 1, P(0.05Ẑ > Z) = 0.01, and with 𝒯 = {x}, P(L > Z) = 0.01 ≤ 0.05.

---

## Claim 3 — finite-R bound for the self-normalised μ̂ (R1_C item 7)

**Verdict: PROVED** as stated. One hypothesis is implicit and needs to be written in: W_r ≥ 0. It holds here, since W_r = Ẑ_r/Z.

**Statement.** Conditional on 𝓒, let (W_r, H_r) for r = 1, …, R be iid. Pairwise uncorrelated is enough. Assume:
- W_r ≥ 0 and 0 ≤ H_r ≤ 1;
- E W_r = 1, E[W_r H_r] = μ, and M = E W_r² < ∞.

Then P(|μ̂ − μ| > ε) ≤ min{1, 4(M−1)/R + 4M/(Rε²)}. Here μ̂ = ΣW_rH_r/ΣW_r, and an arbitrary value of μ̂ when ΣW_r = 0 is allowed.

**Proof (each step checked).**
1. μ ∈ [0, 1], because 0 ≤ W_r H_r ≤ W_r. So |H_r − μ| ≤ 1.
2. Let Y_r = W_r(H_r − μ). Then E Y_r = μ − μ·1 = 0, and E Y_r² = E[W_r²(H_r − μ)²] ≤ E W_r² = M. The tighter bound is ≤ M·max(μ, 1−μ)².
3. Event {W̄ < ½}: it is contained in {|W̄ − 1| ≥ ½}. Var W̄ = (M − 1)/R, so Chebyshev gives probability ≤ 4(M − 1)/R. This event includes ΣW_r = 0, so the convention for μ̂ there does not matter.
4. On {W̄ ≥ ½}: W̄ > 0, so μ̂ − μ = Ȳ/W̄. Then |μ̂ − μ| > ε implies |Ȳ| > εW̄ ≥ ε/2. Chebyshev gives P(|Ȳ| > ε/2) ≤ 4 Var Ȳ/ε² = 4E Y²/(Rε²) ≤ 4M/(Rε²).
5. A union bound finishes the proof, and min{1, ·} is trivial. ∎

C's sketch, "Two applications of Chebyshev and a union bound", is complete once steps 1–2 are written out.

What is assumed rather than proved is the identity E[W_r H_r] = π(h) for the measured-round estimator. C correctly leaves that as a PROOF SKETCH, and this bound does not cover it.

**Numerical check (`c3_cheb.py`).** Setup: W lognormal with mean 1, M = e^{s²}, and H | W ~ Bernoulli(1/(1+W)), so H depends on W. Empirical E Y² is between 0.27 and 1.24, always ≤ M. In every non-vacuous configuration, the empirical probability is below the bound (R = 2000, ε = 0.1: empirical 0.000 versus bound 0.257). The bound is valid but loose.

---

## Claim 4 — "THM-SYNTH A2's 'can only fail downward' is literally false" (R1_C item 7)

**Verdict: PROVED (C's COUNTEREXAMPLE is valid).** It applies to A2's plain-language sentence and to its table row as written. It does not apply to A2's formal statement (iii).

**A2's exact wording** (`origin/theory/THM-SYNTH:…/THEOREM_LIST.md`):
- Table row, line 26: "masked regime: Ẑ errs only downward, by the log-odds overshoot of a late crossing".
- §A2 "(ii) Plainly", line 236: "in the masked regime it can only fail *downward*, by an amount the run can partly certify."
- Formal (iii), "Masked regime, lower tail": P(W > (T/η)[π₀(Aᶜ)/π₀(x_m)]e^{−φ_{τ_A}D_A}) ≤ η + Nπ₀(A), and "on a frozen path log W = (a+Λ)(φ*−φ_τ) + O(1): Ẑ underestimates…".

(iii) is a high-probability statement plus a statement conditional on a path. It does not assert P(W > 1) = 0, so the counterexample does not refute (iii). C's quote matches the "Plainly" sentence word for word, so it is not a paraphrase.

**Proof that the literal sentence is false.**
1. Suppose Ẑ ≤ Z almost surely and E[Ẑ | 𝓒] = Z.
2. Then Z − Ẑ ≥ 0 with mean 0, so Ẑ = Z almost surely.
3. A2(iii) says that in the masked regime P(Ẑ < Z | 𝓒) > 0, and in fact close to 1.
4. Hence P(Ẑ > Z | 𝓒) > 0. More precisely, E[(W−1)⁺ | 𝓒] = E[(1−W)⁺ | 𝓒], so the rare upward excursions carry all the missing mass. Nonnegativity is not even needed. ∎

**Explicit instance (`c24_twostate.py`).** π₀(a) = 0.01, π(a) = 0.99, one particle (the masked start). W = 99 with probability 0.01, and W = 0.0101 with probability 0.99. E W = 1, and E(W−1)⁺ = E(1−W)⁺ = 0.98. Ẑ overestimates by a factor of 99 with probability 0.01.

**Corrected wording.**
> "In the masked regime Ẑ underestimates Z with high probability: P(W_r > t_*) ≤ η + Nπ₀(A) with t_* = (T/η)[π₀(Aᶜ)/π₀(x_m)]e^{−φ_{τ_A}D_A}. Because E[W_r | 𝓒] = 1, the complementary rare event carries compensating overestimates of the same total mean, E[(W_r−1)⁺] = E[(1−W_r)⁺], which can be large when they occur. Markov caps them: P(Ẑ > 20Z) ≤ 0.05. The run certificate Ẑ < Z_𝒯 detects underestimation only."

Line 26 should change the same way, for example: "errs downward with high probability; upward errors are rare and large (mean-compensating)".

---

## Claim 5 — HPM and top-store MPM thresholds (Seat B, R1_B §2.2)

**(a) HPM: PROVED.**

Statement: under EX-A, if S₀ ∈ 𝒮 and δ₁ < ½, then Ŝ = S₀.

Proof: for every S ≠ S₀, π(S) ≤ δ₁ < ½ < π(S₀). So F(S₀) > F(S) strictly, S₀ is the strict ≻-maximum over 𝒮 ∋ S₀, and the tie rule is never used.

½ is sharp. With δ₁ = ½, take an abstract posterior with π(S₀) = π(S₁) = ½ and |S₁| < |S₀| (for example S₁ = ∅). The tie rule (smallest size) then returns S₁ ≠ S₀. For δ₁ > ½, any posterior with π(S₁) > π(S₀) fails.

**(b) Top-store MPM: FALSE as "needs δ₁ < ⅓"; CORRECT WITH AMENDMENT, and the threshold is ½.**

What B gets right: the individual bounds PIP^𝒯_j ≥ 1 − δ₁ (j ∈ S₀) and PIP^𝒯_j ≤ δ₁Z/Z_𝒯 ≤ δ₁/(1−δ₁) (j ∉ S₀) are true. So δ₁ < ⅓ is sufficient. It is neither necessary nor sharp, because B bounds the numerator and the denominator separately even though they are coupled.

**Amended statement (PROVED).** If S₀ ∈ 𝒯, then PIP^𝒯_j ≥ 1 − δ₁ for j ∈ S₀ and PIP^𝒯_j ≤ δ₁ for j ∉ S₀. Hence δ₁ < ½ implies MPM^𝒯 = S₀.

Proof:
1. Let a = π(S₀)Z = (1−δ₁)Z and let x = the 𝒯-mass outside S₀. Then x ≤ δ₁Z and Z_𝒯 = a + x.
2. For j ∈ S₀: PIP^𝒯_j ≥ a/(a + x) ≥ (1−δ₁)/(1−δ₁+δ₁) = 1 − δ₁.
3. For j ∉ S₀: PIP^𝒯_j ≤ x/(a + x). This is increasing in x, so it is ≤ δ₁Z/((1−δ₁)Z + δ₁Z) = δ₁. ∎

The same proof with 𝒯 = Ω gives MPM = S₀ when δ₁ < ½. ½ is sharp: with π(S₀) = π(S₀∖{i}) = ½ and 𝒯 = Ω, PIP_i = ½, which is not > ½, so the MPM is S₀∖{i}.

**Counterexample to "needs ⅓" (`c5_mpm.py`).** Real m(S) with n = 30, p = 8, s₀ = 1, δ₁ = 0.3393 ∈ [⅓, ½). There MPM^𝒯 = S₀, and the largest PIP^𝒯 outside S₀ is 0.144. In 2,400 random stores 𝒯 ∋ S₀ (including top-(4p+1) stores), there were 0 violations of the amended bounds.

**Consequence for B's argument.** "The HPM's certificate is the weakest-hypothesis one" does not hold. Both rules need δ₁ < ½. In fact the hypotheses coincide: if S₀ ∈ 𝒮 and δ₁ < ½, then S₀ is the F-maximum of 𝒮. It is therefore in 𝒯 = top_{40p+1}(𝒮) (Lemma S, plus "every scored model is offered", Prop W(b)). So under δ₁ < ½, S₀ ∈ 𝒮 ⇔ S₀ ∈ 𝒯, and the HPM and MPM^𝒯 certificates are equivalent. B's conclusion that neither bites at n = 200 (δ₁ > 0.63) is unaffected.

---

## Claim 6 — Cor W-R and the extra local search (dispute D3a)

**Cor W-R as written (with its caveat): PROVED.** Islands 1–4 are bitwise unchanged; the pre-search scored set is nested; the pre-search HPM is ⪰ the R = 4 one. With the extra search from the R = 4 centre c₄, the post-search scored set is nested: 𝒮⁺(R′) ⊇ 𝒮⁺(4). The reason is that the local-search path is a deterministic function of (centre, ℓ, scores) with no RNG (Prop W(b) proof). So HPM(R′) ⪰ HPM(4) holds exactly.

There is one small amendment. "Flags computed on islands 1–4 are identical" holds for E1, E2 and low_ESS. It does not hold for E3 or local_certified, because they depend on the final search's centre. They match only if they are evaluated on the search from c₄.

**Monotonicity without the extra search: FALSE. COUNTEREXAMPLE (`c6_ls.py`, `c6b_ls_downsets.py`).**

Setup: the spec's m(S), the production local search (flips and swaps, centre frozen during each scan, best strict ≻-improvement, ≤ ℓ moves then one more scan, every evaluated model updates the best), seed 20261106. Data: n = 29, p = 8, K = 8, ℓ = 6, with y = x₀ + x₁ + noise and x₂ ≈ x₀ + x₁ (a proxy).

Under flips and swaps there are exactly two local maxima:
- {2}, with F = −34.843 (the proxy);
- {0,1} = S₀ = S†, with F = −31.512.

The two runs:
- **R = 4 run.** Pre-search HPM c₄ = {0,1,2,3}, F = −35.789. The search path is {0,1,2,3} → {0,1,3} → {0,1}, so the post-search HPM is {0,1} = S₀.
- **R′ run.** An extra island scores {2}, so c′ = {2}, with F = −34.843 and c′ ≻ c₄. {2} is a local maximum, so the search stops immediately and certifies it. {0,1} is not a flip or swap neighbour of {2}. The post-search HPM is {2} ≠ S₀.

The counterexample survives the most generous nesting: the scored sets can be taken to be the whole down-sets {S ⪯ c₄} ⊂ {S ⪯ c′}. In that design, 3,813 of 32,640 ordered pairs (c₄ ≺ c′) give HPM(R′) ≺ HPM(4). Adding the search from c₄ restores {0,1}.

This shows the deterministic implication "pre-search sets nested ⇒ post-search HPM monotone" is false. I did not prove that the actual SMC realises these particular scored sets with positive probability. It is plausible, given full-support π₀ proposals, but it is CANNOT DECIDE here. The same configuration also gives S₀ ∈ 𝒮⁺(4) but S₀ ∉ 𝒮⁺(R′), so the post-search scored set is not nested either.

**Which THM-SYNTH claims need what.**

| Claim | What it needs about R′ |
|---|---|
| V1, V3, A1, A2, A4, D1–D3, R1, R2, R6, R7 | Neither. These are evidence, PIP, cost and posterior statements, with no scored-set content across R′. |
| V2 / Cor W-R | Only pre-search nesting, which is what it states (line 104: "pre-local-search HPM ⪰"). |
| R4: T21(C1), T38(0), (0_H), N200, Lemma RO | A bound for each run, applied to the R′ run with its own 𝒮⁺(R′), D_n(R′) and Π(X). There is no comparison across R′. These hold for any R′ declared before final randomness. |
| R5 routes (a) iid draws, (b1)/(b1-LH) LS0 from S̃₀, (b1′) pilot, (b2-LH) populations | S₀ enters through route sets in the pre-search set or LS0, and these do not depend on the final search's centre. So the bound proved for each route at R = 4 carries over to R′ by **scored-set nesting** alone. |
| R5(c) cost | Scales with R′. This is not a monotonicity question. |
| R3 (Theorem A) | Deterministic, from any centre in Lat(S°). It is used through LS0, whose centre does not depend on R′. |
| A3, C1(d) | A bound for each run (S₀ ∈ 𝒯 of that run). |

No listed theorem asserts that the post-search HPM(R′) is ⪰ HPM(4), D_n(R′) ≤ D_n(4), or "stacking never worsens the reported HPM".

**Conclusion on D3a.** Seat A's factual claim, that no theorem in the list uses HPM monotonicity in R′, is correct. The extra local search is **not needed for any listed theorem**. Seats B and C are correct that greedy search is not monotone (counterexample above).

The extra search is needed only if v3.1's spec or paper asserts one of these:
- (i) the reported HPM is monotone in R′, or "stacking never worsens Ŝ";
- (ii) D_n(R′) ≤ D_n(4), or P(𝒪 ∩ {Ŝ⁺(R′) ≠ S₀}) ≤ the R = 4 value;
- (iii) study measurements taken from R = 4 post-search scored sets (for example N200's "0/2,394 S₀ ∉ 𝒮") carry over to R′ > 4 fits.

Its cost is ≤ ℓ + 1 deterministic scans. So this is a spec choice, not a requirement of the theorems.

---

## Not checked

- D2 (the O-CERT card) is named in the brief's table rows but is not among the six claims, so I did not check it.
- MASKZPIP P3/C1 and Prop P were consulted only through their statements as quoted in THM-SYNTH.

## Summary

| # | Claim | Verdict |
|---|---|---|
| 1 | Z ≤ C_n(2b₀ + yᵀy/(n+1))^{−ν} (C) | **PROVED** for the spec's m. Holds for any y; very loose (≈ ν log(n+1) nats). Enumeration: 4/4 designs pass. |
| 2 | P(max{Z_𝒯, 0.05Ẑ} > Z) ≤ 0.05; output-event form (C) | **PROVED** (the two events are equal). Output form **CORRECT WITH AMENDMENT**: needs Lemma RO/GUARD, successful 𝓒, CAL, EX-A, distinct stores. |
| 3 | P(\|μ̂−μ\| > ε) ≤ min{1, 4(M−1)/R + 4M/(Rε²)} (C) | **PROVED**. Add W_r ≥ 0. The identity E[W_r ĥ_r] = π(h) is still a premise. |
| 4 | A2 "can only fail downward" literally false (C) | **PROVED** (COUNTEREXAMPLE valid against the "Plainly" sentence and the table row, not against formal (iii)). Corrected wording given. |
| 5 | HPM = S₀ if δ₁ < ½; MPM^𝒯 = S₀ needs δ₁ < ⅓ (B) | (a) **PROVED**, ½ sharp. (b) **FALSE** as "needs ⅓" (counterexample δ₁ = 0.339). Amended: PIP^𝒯_j ≤ δ₁ off S₀, so δ₁ < ½ suffices and is sharp; the two certificates are then equivalent. |
| 6 | Post-search HPM monotone in R′ without the extra local search (D3a) | **FALSE** (COUNTEREXAMPLE: R = 4 returns S₀ = {0,1}, R′ returns {2}). Cor W-R with its caveat **PROVED**. No listed theorem needs the extra search; it matters only for monotonicity or transfer claims. |
