# W3-START — lemma falsification numerics (leg B) — RESULTS

Falsification attempts, **not proofs**; all theorems are asymptotic. Base R only (no compiled core): the scorer in
`lem_common.R` is an independent transcription of the pinned formula; tables and the start are computed by exact
enumeration. Scripts and raw outputs in this folder. Run on 2026-11-11 (local machine, no NOTS).

| lemma | script | output | what was attacked | result |
|---|---|---|---|---|
| L1 (AGG, FLOOR) | `falsify_L1.R 4000 400` (seed 20261111) and `falsify_L1.R 4000 100 7` | `out_L1.txt`, `out_L1_seed7.txt` | random positive tables, random partitions (blocks ≤ 4), p ≤ 11, random K, S₀, Q: (AGG-a) in the form 1 − 1/F, (AGG-b) upper and lower (T₁ ≤ o₀, T₁ ≤ (s₀+1)U, o₀ ≥ c_sΞ, and the prior inequality w(s₀−d+a)/w(s₀) ≥ c_sω for all d ≤ 16, a ≤ 15), (AGG-c), (AGG-d), assembly inequality (e2). Real scorer, 500 data sets incl. duplicate / collinear / near-duplicate columns: one-step ratio ≥ (n+1)^{−1/2} for **all** models, FLOOR for every unsaturated model, T₁ ≥ f_n(s₀) | **0 violations** in 8,000 table cases (about 6,600 (AGG-a) checks, 5,400 upper (AGG-b), 3,600 c_s checks) and 500 data sets (80,000 one-step ratios; smallest ratio·√(n+1) = 1.0125). The table cases have p ≤ 11 and blocks ≤ 4, so the c_s check is run under the sufficient condition s₀ + (largest block) ≤ K, not literally s₀ + 16 ≤ K. Tightness: (AGG-a) bound/actual median 3.4, min 1.01; (AGG-b) upper/actual min 1.00, median 6.5 |
| L2 (TK) | `falsify_L2_L3.R` Part A | `out_L2_L3.txt` | near-twin designs (every second column at distance 1.5 or 0.5 from its neighbour; λ_min(G_U) down to 0.04), n = 60…3840, 400 random sets each: asserted: (E1), (E2) against the realised floor; identities (2.1), (TK-e) (tolerances 1e-10, 1e-8); (f1)–(f3) with the realised ω; R_U in [−κ₁, κ₂] with realised g_* and c_E (tests of the algebra, not of the fixed constants or of the event's probability). Printed as a diagnostic only: max\|ρ_U\| next to ω_n | **0 violations** of the asserted checks. (E1) is attained up to 0.1% (η/(k log(1+1/g)) ≥ −1.000); (E2) ratio ≤ 0.74; max\|ρ\| over all sampled sets used in the comparisons (U and U ∪ {l}; larger of the two twin distances) = 0.61, 0.20, 0.089, 0.040 against ω_n = 3.1, 1.2, 0.55, 0.28 (the bound is loose at these n; ω_n log n → 0 only for much larger n) |
| L3 (Lemma J, (B-L)) | `falsify_L2_L3.R` Parts B, C | `out_L2_L3.txt` | (J0)–(J3) by numerical integration on 240 grid points; step bound L3.3 on small-gain pairs; Monte Carlo of U/(n^{−1/2}𝔏^b) and T₁/((s₀+1)n^{−1/2}𝔏^{b,0}) (60 draws, three designs, one with leaking nulls) | **0 violations**. J/(J0 bound) ≥ 2.78; (J1), (J2) attained (ratio 1.000). Step remainder (exploratory: realised constants, pairs filtered on small mean gain only, n ≥ n₂ not enforced) ≤ 4.4 at n = 60 with g = 0.04 and ≤ 1.2 for n ≥ 960 (bound 2κ_E + 1 ≥ 6). U/(n^{−1/2}𝔏^b): median 0.61–0.72, 90% 1.1–1.2, max 75 in one draw (heavy right tail, as expected at the critical exponential moment: the statement is O_P with a Markov tail) |
| L4 ((B-V2), (B-V1)) | `falsify_L4_L5.R` Part A | `out_L4_L5.txt` | truth with a correlate (ρ = 0.8) in its block, signals √(c log n/n), c = 12, 30, n = 200…3200, 20 draws: the chain of Steps 1–3 of L4.1 with the realised event constants, for every U of the truth blocks | **0 violations** of the chain (slack ≥ 0.67). Realised exponents: largest Ξ term median 1.6–4.2 against c_m/2 = 1.4–4.4; e_n median 0.3–3.0 against (c_V−1−2A)/2 = 0.3–3.5. The worst draws fall below the limit value by up to 1.7: the cross term 2⟨Πμ, Πε⟩ is of relative order (log n)^{−1/2}, so the o(1) in the exponent decays slowly |
| L5 (ASM, START-F) | `falsify_L4_L5.R` Part B | `out_L4_L5.txt` | p = 12, exact enumeration, n = 100…6400, 40 draws: (AGG-b) + (e3) assembly; T₁ ≥ ½(n+1)^{−1/2}; first-order form | **0 violations**. o₀√n median 2.8, 2.3, 2.2, 2.4 (flat: order n^{−1/2}); o₀/T₁ median 1.19, 1.07, 1.03, 1.02 (→ 1) |

Three script errors were found and fixed before the runs recorded above (the first two printed violations):
(1) `falsify_L1.R` drew the extra elements of Q with `sample(x, k)`, which misreads a length-one `x` and produced
duplicate indices in Q (so the lattice mask was wrong); replaced by `sample.int`, with a `stopifnot` on Q.
(2) `falsify_L2_L3.R` computed the realised ω over the sets U only, while (f2) also needs it for U ∪ {l}; ω is now the
maximum over all sets used.
(3) `falsify_L1.R` drew K with `sample(mb:p, 1)`, which misreads the case mb = p and could give K below the largest
block; replaced by `sample.int` with a `stopifnot`. The earlier runs therefore included some cases outside the
block-size hypothesis; the recorded runs do not.
What the scripts do **not** test: the uniform thresholds (n₀, n₂, n₃, n₄), the probability of the toolkit event, blocks
of size 16, Q ≠ S₀ in the visibility chain, or any asymptotic statement.

Not attacked numerically: the uniform constants of (T1)(d) (n₀, c₀, C are far outside any simulable range: c_L = 2^{15}e^{2κ_E+1});
non-default level vectors at finite n (the tail budget of F4 is asymptotic: 2^{16}(log n)^{−2} is below 1 only for
log n > 256).

## Second half (leg C): L6–L11

Script `falsify_L6_L11.R` (seed 20261111; also run with seed 5), output `out_L6_L11.txt`. Asserted checks: **0 violations**.

| lemma | what was attacked | result |
|---|---|---|
| L9 (B-R) | Gaussian rows with a known block-AR(1) covariance, n = 60/200/600, 60 random (l, U₀, V). Asserted identities: J_n(δ_{U,l}, τ_U) = F(g_{U,l}, a_U) (L9.3); the localisation formulas for ρ̂_{U,l} and Δ_U (L9.4); the representation (9.1) of g² through (ξ, d₀, R) built from the **population** regression of W_l on W_D, and the decomposition (I − P_{U₀})CW_l = m + Πe; the Gaussian identity behind L9.5 and its value a^{−1/2}√(2/π)z_n at d₀ = 0, η = 0; the bound Φ_n; (F1), (F2) on a grid | all identities hold to 1e-12 or better; Φ_n and (F2) never violated. Not attacked: the tightness statement itself, the probability of the covariance event, the localisation rates, the count of reference sets, and the size of the thresholds |
| L7 (C2) | orthogonal designs, p = 40, blocks of 4, n = 200/800/3200, 20 draws; one leaking null at level c = 1 + 2A + 1.5 given the truths of its block; one truth at level c = 1 + 2A − 1.2. Asserted: the lower-bound chain of L7.1 with realised constants. Printed: log of the competing model's odds divided by log n | the leaking-null chain holds (the weak-truth chain is not asserted, only its exponents are printed). Leak: median 1.06, 0.56, 0.92 against the limit 0.75; weak truth: 0.58, 0.67, 0.63 against 0.60. The worst draws are lower (0.25 at n = 3200): the fluctuation is of order \|Z\|/√log n |
| L10 (OVL) | p = 12, exact enumeration, one leaking null in Q at level a_l = 2. Asserted: inequality (10.1) (= (AGG-c)). Printed: log m_l/log n | (10.1) held in every draw with U_Q < 1. log m_l/log n: median 0.41, 0.51, 0.52 against the limit (a_l − 1)/2 = 0.5; maxima 1.3–1.8 over 30 draws (the o(1) of the proof is of order max\|Z\|/√log n and decays very slowly) |
| L11 (examples) | F-2 at n = 400, A = 1: the formula Λ_N = cσ² log n·q_k on 200 random sets; Gram floor; (V-m) margins; failure of (V-c); the leak level of a correlate; the lower bound on the default-level J. F-3: the twin Gram matrix. G-2: population partial covariances across groups | all asserted checks hold. F-2: λ_min(BᵀB) = 0.080; (V-m) margins 2.00 and 0.0004 ≥ 0; (V-c) level 0.55 < 3; largest correlate gain 2.40 = 0.4c < 3. Charge of one correlate in ϱ_n, as a power of n: default levels ≥ 2.7, 2.5, 2.3 at n = 10⁴, 10⁶, 10⁹ (diverges; limit 1.9); F4 levels ≤ 1.3, 1.1, 0.9 (limit −0.3): **the F4 bound becomes small only for astronomically large n**, because its o(1) is √(9.6 log log n/log n) |

One script error was found and fixed before the recorded run: the test designs for (C2) and OVL had set the gain
level relative to σ² instead of τ², so the realised level was half the intended one (the observed exponents then
matched the limit for the realised level). A quadrature tolerance in a double-integral check was replaced by an exact
one-dimensional identity.
