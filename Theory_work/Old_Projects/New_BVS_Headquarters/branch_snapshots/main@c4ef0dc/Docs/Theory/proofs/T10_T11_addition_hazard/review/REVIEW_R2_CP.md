# Review round 2 — CP reviewer (Claude Personal, Opus 5.5 xhigh, T3 delegate_task, clientRequestId T10-review-CP-round2)
Packet: %TEMP%/T10_review/CP_round2 (STATEMENT.md v3, PROOF_v4.tex/.pdf, CLAIMS_OF_FATAL_FLAWS.md, MY_ROUND1_REPORT.md, REPORT_FORMAT.md). Reply saved verbatim.

---

# T10 (old T11): round 2 review of PROOF_v4 against STATEMENT.md v3

I read only the packet folder. The text extracted from the PDF matches PROOF_v4.tex, and I checked page 7 visually. I wrote no files and ran no code; all checks below are by hand.

The revision closes the round-1 gap, and all seven round-1 findings are resolved. I found no fatal error and no gap in PROOF_v4. Three new findings remain, all exposition, and none affects a conclusion.

## Part 1: Round-1 findings

**Finding 1 (gap; budget formulas in (iv-c)): resolved.**
- STATEMENT.md v3 now quotes the 00_COMMON §2 budget block verbatim: N₀, H₀, ℓ = ⌈log₂(n+p+1)⌉, T₀, (N_e, H_e, T_e) = 4^e(N₀, H₀, T₀), L, Q_f and its bounds. It also quotes the final-run structure.
- I re-derived (iv-c) from these quotations alone:
  - **Particle-rounds.** There are 4N_e particles and T+L+4 rounds per particle (T one-round stages, L burn-in rounds, 4 measured rounds). This agrees with Q_f = 4N_e(T+L+5): one initial π₀ draw plus one independence proposal per round.
  - **T ≤ T_e.** This follows from the quoted bound Q_f ≤ 4N_e(T_e+L+5), since N_e > 0.
  - **N_e.** With p = n ≥ 2500, N_e = 4^e·n ≤ 4n.
  - **T_e.** ℓ = ⌈log₂(2n+1)⌉, so T_e ≤ 4(1000+ℓ²).
  - **L.** ⌈log₂(n+1)⌉ ≤ ℓ, so L ≤ max(4, ℓ) ≤ ℓ+4.
  - **R.** R ≤ 16n(4008+4ℓ²+ℓ). With h_k ≤ (k+1)n^{−3/2} and h_k/m ≤ (k+1)n^{−5/2}, both limits hold.
- The round-1 concern (N_e growing like n²) is excluded by the quoted N₀ = max(2500, n, p).

**Finding 2 (admissibility and scaling): resolved.**
- §1's data conditions and standardisation are now quoted. The example now checks them:
  - the raw columns are centred and non-zero, so they are non-constant;
  - with the divisor n−1 implied by "‖x_j‖² = n−1", D_x = I and s_y = 1;
  - so X = X^r and y = y^r.

**Finding 3 (exact branch): resolved.**
- Remark 6(a) now says plainly that the example does not exhibit the failure where production SMC rounds run.
- It cites the quoted rule: Σ_{k≤2} C(2,k) = 4 ≤ (5H₀+4N₀)·2.
- One small residue is listed as N3 below.

**Finding 4 (conditional form): resolved.**
- Conditional monotone convergence is now named.
- The index set 𝓘 may now be random, with three stated measurability conditions. I checked the derivation:
  - B∩{u∈𝓘}∩A_u ∈ 𝓕_{u⁻} gives the first equality;
  - the 𝒢-measurability of I_u·o_j(S, φ_u) = I_u·o_j(S, φ_u I_u) gives the second.
- The final-run example is now labelled an illustration and carries no weight. A minor residue is listed as N1.

**Finding 5 ((iv-d) one-line reason): resolved.**
- Both swaps propose sets of size |S|.
- π₀ is supported on Ω.
- The Gibbs denominator is at least γ_φ(S) > 0, by T22 Lemma 1.

**Finding 6 (side remarks on T22): resolved.**
- Remark 1 now rests explicitly on the sketch in §1 and is marked as not used.
- §1's sentence "use none of the hypotheses of T22's theorem" agrees with STATEMENT.md, which cites the three lemmas unconditionally.

**Finding 7 (Remark 6(c) figures): resolved, and both figures are now verified.**
- **Terminal occupancy.** The new invariance argument (d ≡ 0, so q_φ = π₀; T09(ii) reversibility; I outputs an exact π₀ draw; σ is independent of the draws) gives X₅ ~ π₀ exactly, so the terminal figure is π₀(ab) = 8.058·10⁻⁴.
- **Visit probability 0.01978**, which I left unchecked in round 1, I have now computed by hand.
  - Split each order σ at I. Let f be the visit probability from a over the labels before I, and g the visit probability from a fresh π₀ draw over the labels after I. Then P(visit) = (1/120)·Σ_σ [f(pre) + (1−f(pre))·g(post)].
  - With p₀ = β/(3+β) and p₁ = β/(1+β), Σ_σ f(pre) = 46p₁ + 14p₀p₁ − 6p₁². Its leading term reproduces Lemma 3's 46/120.
  - At β = 1/20: Σ f = 2.18780 and Σ(1−f)g = 0.18586. The g sum by number of labels before I (4, 3, 2, 1, 0) is 0.018727, 0.027793, 0.037080, 0.046371, 0.055883.
  - The total is 2.37366/120 = 0.019780, which matches the remark.

## Part 2: Full re-review of PROOF_v4

What I re-checked by hand:

- **Part (i).**
  - Display (3): γ₀e^d = ϖ·BF.
  - Only block b changes when j is added.
  - Lemma 2 applies with T = U and with T = S, and the exponents 1−φ and φ are nonnegative.
  - o_j = a_j/(1+a_j) is increasing in a_j.
  - The π₀ clause is the same bound at φ = 0.
  - The sketch is correct:
    - the ridge minimum equals Q_T;
    - the determinant ratio is (1+(n+1)ξ)/(1+ζ) ≤ n+1, because ξ ≤ ζ.
- **Part (ii).**
  - Path law (4).
  - a!(m−a)! orders.
  - |S_{i−1}| < K at every step.
  - Disjoint summation over orders.
  - The a = 0 case.
- **Example.**
  - Scores: G_T = (n−1)I, z_T = 0, H_T = n²I, D_T = n^t, BF = β^t, d ≡ 0.
  - Method objects: B = 1, N(1) = {2}, N(2) = {1}, m = 5, w = (½, ⅙, ⅙).
  - π₀(ab) ≤ β²/3 and 1−π₀(∅) ≤ β.
  - All five kernels.
  - h₁ = β/(β+√(1+β²)).
- **Coupling and counting.**
  - Lemma 2's hybrid argument.
  - Total-variation distances: o < β for the Gibbs steps, 0 for U and N, at most β for I.
  - The comparison chain is now defined directly.
  - Lemma 3's counts, 30/120 and 16/120.
- **Propositions 4 and 5.**
  - Proposition 4: the first-visit decomposition, the constants 23/60·β + 31/3·β², and f(1/20) ≈ 0.946 < 1.
  - Proposition 5: the three cases on the position of I, each bounded by at most (4/3)β², and the ratio ≈ 0.350 < 1.
- **Part (iii).**
  - The new stopping-time / strong-Markov sentence: the consumed count is a stopping time, 𝓕_{u⁻} is the stopped σ-field, and the next variates are i.i.d. uniform and independent of 𝓕_{u⁻}.
  - Display (7).
  - Measurability via continuity of φ ↦ o_j.
  - Tonelli's theorem and the tower property.
  - With 𝒢 trivial and non-random φ_u, the reading's displayed equality follows.
- **(iv-b).**
  - p ≤ 2p−k−i−1 ≤ 2p.
  - h ≥ r/2.
  - m ≤ 4p and C(m, a) ≤ m^a/a!.
  - 16p²√(n+1) ≤ 16√2·n^{2A+1/2}.
- **(iv-c).** As in Finding 1.
- **(iv-d).** As in Finding 5.

### New findings

**N1**
- **Location:** §5, "Conditional form", Illustration.
- **Severity:** exposition.
- **Claim:** The statement's example says "all probabilities then conditional on 𝒞". The illustration instead conditions on 𝒢 ⊇ σ(𝒞), using global step indices.
- **Evidence:** Getting the version conditional on 𝒞 needs one more step: re-index the final-run steps locally, so that the index set and each φ_u are σ(𝒞)-measurable, then apply the tower property from 𝒢 down to σ(𝒞). The proof's phrase "enumerated stage by stage, particle by particle and position by position" points at that re-indexing but does not carry it out. This does not affect any conclusion: the main claim (non-random φ_u) is proved with 𝒢 trivial, and the statement gives the final run only as an "e.g.".

**N2**
- **Location:** §5, "Model of a run" and "Conditional form".
- **Severity:** exposition.
- **Claim:** For u beyond the last step, the proof sets only λ_u = none and leaves φ_u undefined. The conditional form nevertheless needs I_u·o_j(S, φ_u) to be defined and 𝒢-measurable for every u.
- **Evidence:** A convention (for example φ_u := 0 off the executed steps) or restricting 𝓘 to executed steps fixes this. On A_u, φ_u is always defined, so (iii-a) and (iii-b) are unaffected.

**N3**
- **Location:** Remark 6(a).
- **Severity:** exposition.
- **Claim:** "Runs no SMC round" goes slightly beyond the quoted rule.
- **Evidence:** STATEMENT.md quotes only that the exact branch "precedes block/Gram construction and scores every feasible model". The remark is not used in any proof.

I found no fatal or gap finding. PROOF_v4 establishes every conclusion of STATEMENT.md v3 — (i), (ii), (ii-neg), (iii-a), (iii-b), (iv-a) to (iv-d), and the supplementary ratio — under EX-A and EX-S and the cited statements of T09(ii) and T22 Lemmas 1–3.

**VERDICT: verified**
