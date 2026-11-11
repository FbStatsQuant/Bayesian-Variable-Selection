# W3-START — lemma falsification numerics (leg B) — RESULTS

Falsification attempts, **not proofs**; all theorems are asymptotic. Base R only (no compiled core): the scorer in
`lem_common.R` is an independent transcription of the pinned formula; tables and the start are computed by exact
enumeration. Scripts and raw outputs in this folder. Run on 2026-11-11 (local machine, no NOTS).

| lemma | script | output | what was attacked | result |
|---|---|---|---|---|
| L1 (AGG, FLOOR) | `falsify_L1.R 4000 400` (seed 20261111) and `falsify_L1.R 4000 100 7` | `out_L1.txt`, `out_L1_seed7.txt` | random positive tables, random partitions (blocks ≤ 4), p ≤ 11, random K, S₀, Q: (AGG-a) in the form 1 − 1/F, (AGG-b) upper and lower (T₁ ≤ o₀, T₁ ≤ (s₀+1)U, o₀ ≥ c_sΞ, and the prior inequality w(s₀−d+a)/w(s₀) ≥ c_sω for all d ≤ 16, a ≤ 15), (AGG-c), (AGG-d), assembly inequality (e2). Real scorer, 500 data sets incl. duplicate / collinear / near-duplicate columns: one-step ratio ≥ (n+1)^{−1/2} for **all** models, FLOOR for every unsaturated model, T₁ ≥ f_n(s₀) | **0 violations** in 8,000 table cases (about 6,600 (AGG-a) checks, 5,400 upper (AGG-b), 3,600 c_s checks) and 500 data sets (80,000 one-step ratios; smallest ratio·√(n+1) = 1.0125). The table cases have p ≤ 11 and blocks ≤ 4, so the c_s check is run under the sufficient condition s₀ + (largest block) ≤ K, not literally s₀ + 16 ≤ K. Tightness: (AGG-a) bound/actual median 3.4, min 1.01; (AGG-b) upper/actual min 1.00, median 6.5 |
| L2 (TK) | `falsify_L2_L3.R` Part A | `out_L2_L3.txt` | near-twin designs (every second column at distance 1.5 or 0.5 from its neighbour; λ_min(G_U) down to 0.04), n = 60…3840, 400 random sets each: asserted: (E1), (E2) against the realised floor; identities (2.1), (TK-e) (tolerances 1e-10, 1e-8); (f1)–(f3) with the realised ω; R_U in [−κ₁, κ₂] with realised g_* and c_E (tests of the algebra, not of the fixed constants or of the event's probability). Printed as a diagnostic only: max\|ρ_U\| next to ω_n | **0 violations** of the asserted checks. (E1) is attained up to 0.1% (η/(k log(1+1/g)) ≥ −1.000); (E2) ratio ≤ 0.74; max\|ρ_U\| = 0.26, 0.09, 0.09, 0.04 against ω_n = 3.1, 1.2, 0.55, 0.28 (the bound is loose at these n; ω_n log n → 0 only for much larger n) |
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
