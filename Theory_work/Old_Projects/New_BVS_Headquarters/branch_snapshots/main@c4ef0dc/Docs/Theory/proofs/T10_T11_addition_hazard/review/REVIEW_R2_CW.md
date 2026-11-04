# Review round 2 — CW reviewer (Claude Work, Opus 5.5 xhigh, same native agent resumed via SendMessage)
Packet: %TEMP%/T10_review/CW_round2 (STATEMENT.md v3, PROOF_v4.tex/.pdf, CLAIMS_OF_FATAL_FLAWS.md, MY_ROUND1_REPORT.md, REPORT_FORMAT.md).
Verdict: **VERIFIED**. All round-1 findings F1–F9 resolved. New findings N1–N3, all exposition (non-blocking):
- N1 (Remark 6(a)): "runs no SMC round" slightly beyond the quoted exact-branch rule ("precedes block/Gram construction and scores every feasible model"); the example still satisfies the (ii-neg) reading (B = 1 forces singleton blocks, explicit neighbour rule). Not a proof gap.
- N2 (§5 model of a run): EX-S has several streams; the consumption-ordered sequence of draws is i.i.d. uniform, so the stopping-time argument goes through unchanged.
- N3 (§5 conditional-form illustration): conditions on 𝓖 ⊇ σ(𝓒) rather than σ(𝓒); indexing final-run steps from their own start, the general result applies with 𝓖 = σ(data, 𝓒) directly. Illustration is marked not used; the formal clause is proved.
Also checked: in the (iv-c) regime the SMC branch, not the exact branch, is taken (Σ_{k≤⌊n/2⌋}C(n,k) ≥ 2^{n−1} ≫ (5H₀+4N₀)n), so a final run exists.

(The full verbatim reply is reproduced below.)

---

I checked the revised proof (PROOF_v4) against STATEMENT.md v3 and the verdict is now **verified**. The only blocking issue from round 1 (F1, the budget formulas) is closed, because STATEMENT.md v3 now quotes them and the proof's arithmetic checks out against that quote. All nine round-1 findings are resolved. The second pass found three new points, all presentation-only and none blocking. The compiled PDF (8 pages) matches the LaTeX source, and every check was done by hand.

# Review report, round 2: T10 (old T11), PROOF_v4 against STATEMENT.md v3

## Part 1: status of the round-1 findings

| Finding | Status | Reason |
|---|---|---|
| **F1** (gap: budget formulas behind (iv-c) not in packet) | **Resolved** | STATEMENT.md v3 (line 25) now quotes the budget block, the final-run structure and the exact-branch rule. I checked the proof's §6 (iv-c) (tex 209–219) against that quote; details are under "Conclusions checked". |
| **F2** (admissibility and scaling of the example) | **Resolved** | STATEMENT.md v3 line 9 now gives the data conditions and the scaling rule. The example meets them: n ≥ 400 ≥ 3; columns are centred with ‖x_j‖² = n−1 > 0, so none is constant; y is non-constant; the sample SD with divisor n−1 is 1, so D_x = I and s_y = 1. The standardisation therefore leaves the data unchanged. Remark 6(a) on the exact branch is now sourced (see new point N1). |
| **F3** (comparison chain "β replaced by 0") | **Resolved** | The comparison kernels are now defined directly (tex 125); each is a valid Markov kernel. The total-variation bounds still hold: < β for the Gibbs steps, 0 for U and N, at most β for I. Line 100 now uses 2β+β² ≤ β(3+2β+β²), which is true for all β ≥ 0. |
| **F4** (independence of the next random draw from the past) | **Resolved** | The proof now states that the number of draws consumed before step u is a stopping time and invokes the strong Markov property (tex 179). That justifies (7). The proof says "the stream" in the singular while EX-S has several streams; this is trivial (new point N2). |
| **F5** (conditional form; random index set) | **Resolved** | 𝓘 may now be random, under three stated conditions. I re-derived the computation (details under "Conclusions checked"); it is correct. The "with 𝓖 trivial" clause gives STATEMENT's display. One small residual point on the illustration is new point N3. |
| **F6** ((iv-d) "no other kernel leaves Ω") | **Resolved** | A reason is now given (tex 221). Both swaps keep the size \|S\|. Independence proposals come from π₀, which is zero outside Ω. The Gibbs denominator is at least γ_φ(S) > 0 by T22 Lemma 1. |
| **F7** (positivity in part (i)) | **Resolved** | T22 Lemma 1 is now cited exactly where the proof divides and takes real powers (tex 53). Positivity of ϖ on Ω follows from γ₀ > 0 and ∏r_b > 0. |
| **F8** (side remarks on what T22 needs) | **Resolved** | Remark 1 now rests only on the in-text sketch and is marked unused. "Hypothesis use" now says "every admissible data set". The sentence on line 47 about T22's theorem is kept; it matches the cited statements, which carry no extra hypotheses, and is not used. |
| **F9** (Remark 6(c) numbers) | **Resolved** | The terminal value is now derived in the remark from T09(ii) reversibility, as cited in STATEMENT v3 (details under "Conclusions checked"). The visit figure 0.01978 is still unchecked by me, but it is clearly marked as corroboration and not used. |

## Part 2: findings on PROOF_v4

**N1**
- **Location:** Remark 6(a), tex 174; and how it relates to the (ii-neg) reading in STATEMENT.md line 44.
- **Severity:** exposition.
- **Claim:**
  - "Runs no SMC round" goes slightly beyond the quoted rule. The rule says only that the exact branch "precedes block/Gram construction and scores every feasible model".
  - The (ii-neg) reading asks for data "with the blocks and neighbour graph computed by the method". For p = 2, production never builds blocks, because the exact branch comes first.
- **Evidence:**
  - The example still satisfies the reading as written. "Admissible data" is defined by the line 9 conditions, which p = 2 meets.
  - With B = min(⌊√n⌋, ⌊√2⌋, 16) = 1, any block partition has to be singletons.
  - The neighbour rule is explicit and gives N(1) = {2}, N(2) = {1}.
  - So the round kernel is fully determined. The remark is open that the failure is not shown in the regime where SMC rounds actually run.
  - This is not a proof gap. A counterexample in that regime would need p ≳ 18 under the quoted threshold, and requiring one would be a change to the statement.

**N2**
- **Location:** §5, "Model of a run", tex 179: "Under EX-S the stream is i.i.d. uniform".
- **Severity:** exposition.
- **Claim:** EX-S has several independent streams; the proof writes one.
- **Evidence:**
  - Take the draws in the order they are consumed.
  - Each new draw comes from a position not yet read, and the past decides which position. So it is uniform and independent of the draws already read.
  - Hence the consumption-ordered sequence is i.i.d. uniform, and the stopping-time argument goes through unchanged.

**N3**
- **Location:** §5, "Conditional form", the illustration (tex 197).
- **Severity:** exposition.
- **Claim:** The illustration conditions on 𝓖 ⊇ σ(𝓒), the data plus all draws before the final run. STATEMENT's "e.g." conditions on 𝓒 itself.
- **Evidence:**
  - Index the final run's steps from its own start. Then {u ∈ 𝓘} and φ_u depend only on 𝓒, since the grid is frozen and φ = 1 for burn-in and measured rounds.
  - The general result then applies with 𝓖 = σ(data, 𝓒) directly; alternatively, take one more conditional expectation from the larger 𝓖.
  - The three conditions hold for the illustration, using the standard fact that for B ∈ 𝓕_τ, B ∩ {τ ≤ τ_u} ∈ 𝓕_{τ_u}.
  - The illustration is marked "not used". The formal clause (non-random φ_u gives the middle term) is proved.

## Conclusions checked (round 2)

- **(i):** proved, as in round 1. The only change is the positivity citation.
- **(ii) and its "event" sentence:** unchanged and proved. The set of qualifying label orders has a!(m−a)! members. Part (i) bounds each addition step. The events for different orders are disjoint.
- **(ii-neg):** proved.
  - Re-checked the scores: G_T = (n−1)I, H_T = n²I, D_T = n^t, BF = β^t, d ≡ 0.
  - Re-checked the kernels and h₁ = β/(β+√(1+β²)).
  - Re-checked the coupling lemma and the label counts 30/120 and 16/120.
  - Union bound: (23/60)β + (31/3)β².
  - f(1/20) = 0.9·(1+√401)/20 ≈ 0.9461 < 1.
- **(iii-a) and (iii-b):** proved, including the new conditional form.
  - Conditional form: since B ∩ {u∈𝓘} ∩ A_u ∈ 𝓕_{u⁻}, part (iii-a) gives E[1_B I_u 1_{A_u} 1{X_u = S+j}] = E[1_B I_u 1_{A_u} o_j].
  - I_u·o_j(S,φ_u) = I_u·o_j(S, φ_u I_u) depends only on 𝓖, by continuity in φ.
  - The tower property and conditional monotone convergence then give the display.
- **(iv-a) and the supplementary ratio:** proved.
  - Case bounds β²/3, β² and (4/3)β².
  - Ratio bound (20/3)β(β+√(1+β²)) ≈ 0.3504 < 1 at β = 1/20; it increases in β and tends to 0.
  - Remark 6(c) confirms the bound: X₅ ~ π₀ exactly, so P(X₅ = ab) = π₀(ab) = 1/1241 ≈ 8.06·10⁻⁴ at n = 400.
    - In the example q_φ = π₀ because d ≡ 0.
    - Reversibility implies invariance, and step I outputs an exact draw from π₀.
    - The label order σ is independent of the draws, so given σ the law π₀ is preserved after step I.
- **(iv-b):** unchanged and proved.
- **(iv-c):** proved under STATEMENT v3's quoted budgets. The quote matches the lead's answer in CLAIMS_OF_FATAL_FLAWS.md.
  - Particles and rounds: 4 islands × N_e = 4N_e particles, and T + L + 4 rounds per particle.
  - Budget bounds:
    - T ≤ T_e follows from Q_f ≤ 4N_e(T_e+L+5).
    - N_e = 4^e·max(2500, n, n) = 4^e n ≤ 4n.
    - ℓ = ⌈log₂(2n+1)⌉ and T_e ≤ 4(1000+ℓ²).
    - L ≤ ℓ+4.
  - Total: R ≤ 16n(4008+4ℓ²+ℓ). Hence (1) is at most 16(k+1)n^{−3/2}(…) → 0 and (2) is at most 16(k+1)n^{−1/2}(…) → 0.
  - In this regime the SMC branch, not the exact branch, is taken: Σ_{k≤⌊n/2⌋} C(n,k) ≥ 2^{n−1}, far above (5H₀+4N₀)n ≈ 5n². So a final run exists.
- **(iv-d):** proved.

## Files reviewed
- `<PC_TEMP_PATH>`
- `<PC_TEMP_PATH>`
- `<PC_TEMP_PATH>`
- `<PC_TEMP_PATH>`
- `<PC_TEMP_PATH>`
- `<PC_TEMP_PATH>`

**VERDICT: verified**
