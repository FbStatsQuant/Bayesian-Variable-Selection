# R03b ("better theorem", gpt-6-astra high; sharpness gate) — disposition

HQ could not be consulted synchronously. Rule applied: adopt a proposal only if (i) it is inside one of the brief's five
items, (ii) its risk is low or medium and the lead re-derived it in full, (iii) it gets its own line check. Everything else
is recorded for HQ.

| rank | proposal | decision | where |
|---|---|---|---|
| 1 | C+: E δ_n = O(r_n) (variance-side window in the denominator integral) | **ADOPTED** (item 3; lead re-derived: Lemma C1 Taylor bound |F″| ≤ 6N on I ⊆ [3/4, 5/4], E′ ≤ 2N event, P(E′ > 2N) ≤ e^{−N/8}) | C_expectation.md v2; STATEMENT v1.2 Claim C |
| 2 | D+: D(b) under (E), (F₀), (OS) only, via the ridge loss L_S; variance at M_n/√n | **ADOPTED** (item 4; lead re-derived D1 floor-free and D3 with E1 at margin c₂ = c₁ + 1) | D_hellinger.md v2; STATEMENT v1.2 D(b) |
| — | ridge-loss form of E1 (implicit in D+) | **ADOPTED** for Claim E: hypothesis (ID^M; c) with L_S ≥ Δ_S (weaker than (ID)) | E_visibility.md v2 |
| 3 | A+.1 exact truncated-moment weights b_J; A+.2 completion costs H_J | recorded (low risk; a strictly weaker sufficient (OS); bookkeeping) | REPORT §open |
| 4 | E+.1 constants c₁ ≈ 54 (probability) / ≈ 60 (expectation) at s₀ = A = 1 | recorded (low–medium; constants are proof artefacts); note R03b's argument that c ≈ 4 cannot be universal at p = n^A (deletion obstruction ≈ 2a_p + 2) | REPORT §open, ASSUMPTION_MAP |
| 5 | B+ optimised, growing reference cost with explicit payment e^{(1/(2σ*²)+ε)L_T} | recorded (low risk; Claim B Remark 7 already flags the payment) | REPORT §open |
| 6 | E-floor+: replace (F₀) by bounded ridge cost L_{S₀} = O(1) (probability conclusions only) | recorded (medium; expectation transfer is false by that route) | REPORT §open |
| 7 | D-transfer: integrated predictive Hellinger under an explicit empirical/population norm interface | recorded (conditional corollary; bridge is extra work) | REPORT §open |
