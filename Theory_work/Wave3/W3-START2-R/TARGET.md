# W3-START2-R — TARGET (CP1 evidence: assumption map of the changed hypotheses, parity, boundary numerics)

Statement: `STATEMENT.md` v1.5 (delta over W3-START2 v1.4.1). Better-theorem input: the blind sharpness audit sharp2
(`API_AUDIT/sharp2/TRIAGE.md`, raw `results/f04–f09.md`); no Astra review (RIDER_RULES §3.2).

## 1. Assumption map (changed hypotheses only; unchanged ones: BASE `ASSUMPTION_MAP.md`)

| hypothesis | where it enters | how | necessity reading |
|---|---|---|---|
| (V-cp) δ²_{U,j} ≥ τ²_U(c_V log n + 2 log p), c_V > 1 | VIS-c⁺⁺ (copy of BASE L4.2) → [VIS] → (T1⁺⁺) | each truth-deletion step costs ≤ n^{1/2}·(2p)·e^{−gain/2}; p enters only as log(2p) | **necessary at the constant 1, for every p_n**: (N3⁺⁺) — a truth with gain ≤ τ²(c log n + 2 log p), c < 1, given every V ⊆ S₀ ∖ {j} sends π₀(S₀) → 0. Remaining gap: quantifier (all 15-sets vs subsets of S₀), as in v1.4 |
| (V-mp) with π_n(d, a; Q) | VIS-m⁺⁺ (copy of BASE L4.1, Step 5 exact) | prior-plus-dimension price of U vs T; negative for a > d | necessary at D = {j}, N = ∅ (same as (N3⁺⁺)); the a > d credit is the method's prior, not slack |
| (L-R⁺⁺) \|H_l\| ≤ H̄_n, log H̄_n ≤ κ_H√log n | (B-R⁺⁺)(i): N_ref in the first-moment bound | factor N̄_n ≤ 2^{15}e^{15κ_H√log n}, absorbed by e^{C_R√log n} | a proof device (union over reference sets); not necessary for the conclusion (G-1 with \|H_l\| = s₀ + 1) |
| (L-gain-0) leakage ≤ C₀(n log n)^{−1/2} given U ⊊ S₀ | (B-R⁺⁺)(iii) → leading term of (T3⁺⁺)(b)(iii) | bounded shift d̄√log n of the Gaussian ξ in BASE L9.5; reference sets: the 2^{s₀} proper subsets only | the scale is where the shift stops costing a factor e^{O(√log n)}; with C₀(n log n)^{−1/2} replaced by C_L n^{−1/2}, (i) still gives n^{−1/2}e^{C√log n}. Whether e^{C√log n} is attained at C_L > 0: not claimed (heuristic remark in f09) |
| \|S₀\| ≤ s̄ (TRANSFER) | (T3⁺⁺)(a1) | constants maximised over finitely many s₀ | bookkeeping |
| premises of (C2⁺⁺), (N2⁺⁺), (N3⁺⁺), F4⁺⁺ at c log n + 2 log p, drifting c_n | R2 (copies of BASE L7, L3.5) | one Gaussian variable at a deterministic witness; window (c_n − 1)√log n | limits, not hypotheses of a positive theorem |

## 2. Parity (per changed clause; (a) PROGRAM goals, (b) closest published, (c) best registered result)

| clause | (a) goals: design-agnostic / p ≫ n / method as coded | (b) closest published (as listed in raw verdict f04, `results/f04.md:36`; checked at the citation step) | (c) best registered | verdict |
|---|---|---|---|---|
| (T1⁺⁺) visibility level | matches / matches / matches | beta-min of order τ²(log n + 2 log p) with an identified constant 1; f04 recalls this matches the EBIC penalty with γ = 1 (Chen–Chen 2008), while Yang–Wainwright–Jordan and Castillo–Schmidt-Hieber–van der Vaart leave the constant unspecified | W3-START2:START-F: (1 + 2A) log n of the envelope | **beats (c)** when p ≪ n^A or log p/log n oscillates; **matches (b)**; constant sharp by (N3⁺⁺) |
| (T4⁺⁺) NEC | matches / matches / matches | none closer known | W3-START2:NEC: thresholds 1 + 2Ā vs 1 + 2A̲ | **beats (c)**: one threshold, every p_n; window 1/√log n |
| (T3⁺⁺)(b)(iii) Gaussian-row rate, Q = S₀ | matches / matches (p ≤ n^A) / matches | posterior-mass rates in that literature are prior-driven (p^{−c}-type under p^{−κ\|γ\|} priors, f04 `:18-21`); the coded prior has the n^{−1/2} floor (T0) | W3-START2:START-R C_L = 0: (log n)^{15κ_Q+1/2}/√n | **beats (c)**; **short of the floor by √log n**: the lower bound o₀ ≳ √(log p/n) is not claimed (BASE `:380`; f05 `:58` calls it hard for general designs) — named, not a target |
| (T3⁺⁺)(b)(i) H_l size | matches | — | polylog H_l | beats (c) |
| (T3⁺⁺)(a) TRANSFER | matches | — | deterministic envelopes only | beats (c) (random rate) |
| IF-START⁺⁺ | matches | — | n^{−1/2}e^{C_R√log n} in Gaussian rows | beats (c): √(log n/n) under (iii) |
| MIS⁺⁺ Gaussian instance | matches | — | (GR) assumed | beats (c) in scope (an exact instance); general μ ∉ span X_𝒞: named open item W3-START2R-O1 |

Honest-reading notes (brief item 4): P1 of v1.4 (𝔏^♯ in place of 𝔏⁰) is a rate gain only for p = O(√log n); it is not a
p ≫ n improvement (triage §0). LEAK-0 sharpens the partition-free 𝔏⁰ only (STATEMENT §3.0).

## 3. Boundary numerics (planned; production core via BASE `numerics/start_common.R`, read-only)

| assumption weakened | run | expected observation |
|---|---|---|
| (V-cp), small p | F-1-type orthogonal design, one truth with δ²/τ² = c log n + 2 log p, c ∈ {0.6, 0.9, 1.1, 1.5}, p ∈ {n^{0.3}, n^{0.9}}, n ∈ {200, 800, 3200} | π₀(S₀) high for c > 1 and low for c < 1 **at both p**; the v1.4 level (1 + 2A) log n would put the switch at a different place for p = n^{0.3} |
| (V-mp) a > d credit | F-2 design at A = 0.9: o₀/T₁ vs n | o₀/T₁ → 1 (prediction of EX⁺⁺ for A > 3/4) |
| (L-gain-0) boundary | G-1 (Σ = I) and one null with Cov(W_l, W_j) = C₀/√(n log n) vs C_L/√n, p = 2n | o₀√(n/log n) bounded in the first case; growth in the second is the open question (observational only) |
| (T3⁺⁺)(b)(iii) rate | G-1 at p = 2n, n ∈ {200, …, 3200} | o₀·√(n/log n) stable (v1.4 predicted only the polylog envelope) |
Numerics are observations; no statement cites them unless REPORT says so.
