# STATEMENT — T14(i) (L-FM, singleton case): first-moment evidence consistency

Source: `Theory_architecture_v3/theorems/T14_LFM_first_moment_evidence.md`, part (i) only. Method: SMC-BVS v3.0, METHODOLOGY_v3.md (SHA-256 93043758058a6d422cca6ca4b6be8f3a9e8149b6f6de2e1bab1ce31c44b8019c). Parts (ii) and (iii) of the file are not part of this run.

Statement analysis outcome: **(a) correct as stated.** No assumption was changed or added. EXP / EXP′ is not needed. No other v3 conjecture is used as a hypothesis (the unbiasedness identity of T12 that the theorem builds on is re-derived inside the proof).

## 1. Setting (from 00_COMMON.md §§1–2 and METHODOLOGY §§6.3, 6.5, 6.6, 6.8, 6.12)

- Ω = {S ⊆ [p] : |S| ≤ K} is a finite set. For S ∈ Ω: γ₀(S) = ϖ(S)∏_b r_b(S ∩ C_b) > 0 (the size prior ϖ and the block tables r_b = BF are strictly positive), d(S) ∈ ℝ, and for real φ, γ_φ(S) = γ₀(S)e^{φ d(S)}, Z̄_φ = Σ_{S∈Ω} γ_φ(S), q_φ = γ_φ/Z̄_φ. Hence q_φ(S) > 0 for every S ∈ Ω. At temperature φ = 0 the bridge is π₀, at φ = 1 it is π, and Z = m(∅)·Z̄_φ evaluated at φ = 1, with m(∅) > 0. (Below, a numerical subscript on q or Z̄ is a stage index; since φ_T = 1, Z = m(∅)Z̄_T and q_T = π.)
- The calibration 𝓒 fixes the grid 0 = φ₀ < φ₁ < … < φ_T = 1 (so T ≥ 1) and the per-island particle count N (= N_e). Write Δ_t = φ_t − φ_{t−1}, q_t = q_{φ_t}, Z̄_t = Z̄_{φ_t}, G_t(S) = e^{Δ_t d(S)} (t = 1, …, T).
- **Final island r** (one island; N ≥ 1 particles), given the data and 𝓒:
  1. ξ₀¹, …, ξ₀ᴺ are iid with law q₀ (exact start).
  2. For t = 1, …, T: (reweighting) particle i gets weight G_t(ξ_{t−1}ⁱ); (multinomial resampling) ζ_t¹, …, ζ_tᴺ are drawn, conditionally on the past, iid from Σ_i G_t(ξ_{t−1}ⁱ)δ_{ξ_{t−1}ⁱ} / Σ_i G_t(ξ_{t−1}ⁱ); (mutation, one round per stage) conditionally on the past and on ζ_t, the ξ_tʲ are independent with ξ_tʲ ~ K_t(ζ_tʲ, ·), where K_t = K_{φ_t} is a Markov kernel on Ω leaving q_t invariant (q_t K_t = q_t).
  3. q̂_t = N⁻¹Σ_i δ_{ξ_tⁱ} (empirical population after stage-t resampling and mutation; q̂₀ = the initial draws).
  4. Island evidence: Ẑ_r = m(∅) Z̄₀ ∏_{t=1}^T q̂_{t−1}(G_t), computed exactly. Pooled evidence: Ẑ = ¼Σ_{r=1}^4 Ẑ_r over the four final islands.
  The burn-in rounds, measured rounds and local search that follow stage T do not enter Ẑ_r.
- **Reference model.** S° ∈ Ω is fixed given 𝓒: a function of the data and 𝓒 only, not of the final-run randomness. Define
  - η_t = 1 − q_t(S°) (t = 0, …, T), ε_* = max_{0≤t≤T} η_t;
  - R_t(S) = G_t(S)/G_t(S°) (t = 1, …, T), so R_t(S°) = 1;
  - A_t = ∏_{v=1}^t q̂_{v−1}(R_v) (A₀ = 1);
  - b_t = q₀(S°)/q_t(S°) (b₀ = 1).

## 2. Hypotheses

- **EX-A:** exact scores, normalisers (Z̄₀ in particular), probabilities and arithmetic.
- **EX-S + CAL:** ideal independent uniform streams; 𝓒 is measurable with respect to calibration streams 0–9 and the data; the final islands use streams 10–13, independent of 𝓒. Consequently, conditionally on (data, 𝓒), each final island evolves exactly as in §1 item 2.
- **Exact start:** the initial particles are exact iid π₀ = q₀ draws.
- **Prescribed resampling and moves:** multinomial resampling after every reweighting; one q_{φ_t}-invariant move round per stage, applied to each particle as in §1 item 2.
- **Successful 𝓒:** the frozen grid exists (no `schedule_limit`); everything below is conditional on (data, 𝓒). E denotes expectation over the final-run randomness given (data, 𝓒).

## 3. Conclusion (to prove)

For every island r and every N ≥ 1 (note ε_* < 1 always, since q_t(S°) > 0):

(i-a) Ẑ_r/Z = A_T/b_T, surely.

(i-b) E|Ẑ_r/Z − 1| ≤ [Σ_{t=1}^T (b_{t−1}η_{t−1} + b_tη_t) + |1 − b_T|]/b_T ≤ (2/(1 − ε_*)) Σ_{t=0}^T η_t.

(i-c) The same two bounds hold for the pooled Ẑ in place of Ẑ_r.

(i-d) Reading of the file's sentence "the endpoint term |1 − b_T| is essential": the middle expression cannot in general be replaced by Σ_{t=1}^T (b_{t−1}η_{t−1} + b_tη_t)/b_T. Precisely: there is an instance of the abstract setting of §1 (finite Ω, positive γ₀, real d, a grid, q_t-invariant kernels K_t, N ≥ 1, S° ∈ Ω) for which E|Ẑ_r/Z − 1| > Σ_{t=1}^T (b_{t−1}η_{t−1} + b_tη_t)/b_T. (This sentence is an informal remark in the theorem file; this is the reading adopted here. It is not claimed that such an instance arises from an actual SMC-BVS data set.)

## 4. Change log

- 2026-10-22, after Astra review round 1 (exposition finding 1): notation only. "q₁ = π, Z = m(∅)Z̄₁" in §1 was rewritten so that a numerical subscript is always a stage index (q_t = q_{φ_t}); the endpoint is written q_T, Z̄_T. No hypothesis or conclusion changed.
