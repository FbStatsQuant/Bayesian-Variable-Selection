# Stage B — Opus 5.5 (xhigh) review, round 1, 2026-10-22

Launched with T3 delegate_task on Claude Personal (provider claudeAgent, claude-opus-5-5, effort xhigh), clientRequestId T14i-stageB-opus-personal-r1. Packet: STATEMENT.md, PROOF.tex/PROOF.pdf (= proof/PROOF_v2), REPORT_FORMAT.md. Reviewer scratch (its numerical check script): <PC_TEMP_PATH> Reply copied verbatim from the task result below.

---

I found no fatal errors and no gaps. Every equality and inequality checks out by hand, and the proof proves exactly the statement under its hypotheses, with nothing extra assumed. Small exact-enumeration checks agree to rounding error.

**Step-by-step check**

- **Setting vs. STATEMENT §1–2.** The bridge, grid, island (exact start; multinomial resampling with weights G_t(ξ_{t−1}^i); one q_t-invariant move per stage), Ẑ_r, Ẑ, S°, η_t, ε_*, R_t, A_t and b_t all match the statement. Nothing beyond EX-A, EX-S+CAL, exact start, the prescribed resampling and moves, and a successful 𝓒 is used.
- **Lemma 2 (change of temperature).** q_{t−1}(S)G_t(S) = γ₀(S)e^{φ_{t−1}d}e^{Δ_t d}/Z̄_{t−1} = (Z̄_t/Z̄_{t−1})q_t(S). Correct.
- **Lemma 3 (ratio of the b's).** b_t/b_{t−1} = q_{t−1}(S°)/q_t(S°). Lemma 2 with h = 1_{S°}, divided by G_t(S°)q_t(S°) > 0, gives the stated ratio. It also holds at t = 1, since b₀ = 1 = q₀(S°)/q₀(S°). Correct.
- **Lemma 4 (one stage in conditional mean).** E[f(ξ_t^j) | F_{t−1}, ζ_t] = K_t f(ζ_t^j), and ζ_t^j ~ μ_t given F_{t−1}. The tower property gives μ_t(K_t f) = q̂_{t−1}(G_t K_t f)/q̂_{t−1}(G_t), and the denominator is positive because G_t > 0. Ω is finite, so everything is bounded. Correct.
- **Proposition 5.** The base case t = 0 is immediate. In the induction step:
  - A_t is F_{t−1}-measurable (A_{t−1} is F_{t−2}-measurable and q̂_{t−1} is F_{t−1}-measurable) and bounded, so it can be pulled out of the conditional expectation.
  - q̂_{t−1}(R_t)/q̂_{t−1}(G_t) = 1/G_t(S°), and q̂_{t−1}(G_t K_t f)/G_t(S°) = q̂_{t−1}(R_t·K_t f).
  - The induction hypothesis applies to the function R_t·K_t f. Lemma 2 with h = K_t f, then q_t K_t = q_t, then Lemma 3 give b_t q_t(f).

  Every step is correct. The range 0 ≤ t ≤ T−1 is exactly what the later steps need.
- **(i-a).** Writing G_t = G_t(S°)R_t gives ∏_t G_t(S°) = e^{d(S°)(φ_T−φ₀)} = e^{d(S°)}, so Ẑ_r/Z = (Z̄₀/Z̄_T)e^{d(S°)}A_T. Also q_T(S°)/q₀(S°) = e^{d(S°)}Z̄₀/Z̄_T, so Ẑ_r/Z = A_T/b_T. This is purely algebraic, so it holds surely. Correct.
- **Increment bound (1).**
  - q̂ is a probability measure and R_t(S°) = 1, so q̂(R_t) − 1 = q̂((R_t − 1)1_{Ω∖S°}).
  - Since R_t > 0, |R_t − 1| ≤ R_t + 1.
  - Then |A_t − A_{t−1}| = A_{t−1}|q̂_{t−1}(R_t) − 1|.
  - Proposition 5 at t−1, applied to the two functions R_t 1_{Ω∖S°} and 1_{Ω∖S°}, gives b_{t−1}q_{t−1}(R_t 1_{Ω∖S°}) + b_{t−1}η_{t−1}.
  - By Lemmas 2 and 3, the first term equals b_t η_t.

  Correct.
- **(i-b), first inequality.** (A_T − 1)/b_T + (1 − b_T)/b_T = A_T/b_T − 1. The telescoping triangle inequality and (1) then give the bound. Correct.
- **(i-b), second inequality.**
  - For each s, b_s/b_T = q_T(S°)/q_s(S°) ≤ 1/(1 − η_s) ≤ 1/(1 − ε_*).
  - Σ_{t=1}^T (η_{t−1} + η_t) = 2Σ_{t=0}^T η_t − η₀ − η_T.
  - The endpoint term: |1 − b_T|/b_T = |q_T(S°) − q₀(S°)|/q₀(S°) = |η₀ − η_T|/(1 − η₀) ≤ (η₀ + η_T)/(1 − ε_*), since both η's lie in [0, 1).
  - The two pieces add to exactly 2(1 − ε_*)^{-1}Σ_t η_t.

  Correct.
- **(i-c).** Ẑ/Z − 1 = ¼Σ_r(Ẑ_r/Z − 1), so the triangle inequality bounds it by the average of the island errors. Both right-hand sides depend only on (γ₀, d, grid, S°), which 𝓒 fixes, so they are the same for every island. No independence between islands is needed. Correct.
- **(i-d).** The instance is Ω = {S°, x} with a = 0.01, c = 0.1.
  - Z̄₀ = 1, γ₁ = (0.99, 0.11), Z̄₁ = 1.1, q₁ = (0.9, 0.1).
  - With N = 1, Ẑ_r/Z = q₁(ξ)/q₀(ξ), so E|Ẑ_r/Z − 1| = Σ_y |q₁(y) − q₀(y)| = 0.18.
  - η₀ = 0.01, η₁ = 0.1 and b₁ = 0.99/0.9 = 1.1, so the bound without the endpoint term is 0.12/1.1 = 0.10909… < 0.18. The inequality is strict, as (i-d) requires.
  - The full middle expression is 0.2 and the right-hand side is 0.2444… Both are ≥ 0.18, as they must be.
  - The identity kernel is a Markov kernel that leaves q₁ invariant, and the statement's (i-d) explicitly allows an abstract finite Ω. Correct.
- **PDF vs. TeX.** The PDF text (extracted with pdftotext) has the same structure and content as PROOF.tex (version 2). The only difference is that Theorem, Lemma, Proposition and Remark share one counter, which makes "Lemma 2" in the PDF the first lemma.

**Numerical check** (exact enumeration, one seed, script `review_B_opus_scratch/check.py`)

I ran 84 random instances with |Ω| ∈ {2, 3, 4}, T ∈ {1, …, 4}, N ∈ {1, 2}, both reversible Metropolis–Hastings kernels and non-reversible invariant kernels, and a random S°:

- **Proposition 5:** the largest value of |E[A_t q̂_t(f)] − b_t q_t(f)| was 8.8e-13.
- **Unbiasedness:** the largest value of |E A_T − b_T| was 6.4e-12.
- **Bounds:** (i-a), the increment bound (1) and both inequalities of (i-b) held in every instance.
- **Endpoint term:** in 6 instances the error exceeded the bound with the endpoint term dropped, which independently supports (i-d).
- **(i-d) instance:** reproduced as E = 0.18, bound without endpoint 0.10909, full middle 0.2, right-hand side 0.2444.

**Findings**

1. **Location:** §1 item (b) and the proof of Lemma 4.
   **Severity:** exposition.
   **Claim:** the statement gives the resampling and move laws "conditionally on the past". The proof conditions on the smaller σ-field F_{t−1} = σ(ξ₀, ζ₁, …, ξ_{t−1}) without saying why that is allowed.
   **Evidence:** the reduction is valid, because μ_t is F_{t−1}-measurable and the move law depends only on ζ_t^j. So conditioning on any larger past and then applying the tower property gives the same conditional laws. This is a one-line justification, not a gap.

2. **Location:** §4 (i-c).
   **Severity:** exposition.
   **Claim:** the proof says the islands "share the grid, the kernels, N and S°". Only the grid, γ₀, d and S° are actually needed.
   **Evidence:** M and 2(1−ε_*)^{-1}Σ_t η_t depend only on (q_t)_t and S°, and 𝓒 fixes the grid and S°. The extra claims about kernels and N are true under the statement (K_t = K_{φ_t}, and N is the per-island count fixed by 𝓒) but are not used.

3. **Location:** Remark 6.
   **Severity:** exposition.
   **Claim:** it cites T12(i) (E[Ẑ_{r,t} q̂_t(f)] = Z_t q_t(f)), which is not in the packet, so I cannot check it against its source.
   **Evidence:** the remark is not used anywhere in the argument. I checked the stated rewrite: with b_t = Z̄_t/(Z̄₀e^{φ_t d(S°)}), the expression m(∅)Z̄₀e^{φ_t d(S°)}·b_t q_t(f) equals Z_t q_t(f). What T12(i) itself says remains unverified.

VERDICT: verified
