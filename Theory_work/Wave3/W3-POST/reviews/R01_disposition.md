# R01 disposition (lead) — reviewer: gpt-6-astra high, `R01_recheck_astra.md`

Verdicts received: T02(i♯)/E1/E2 VERIFIED; Lemma B VERIFIED; T02(ii♯) VERIFIED; T03♯ VERIFIED; [P1]/[P3] load-bearing
steps VERIFIED; L1_POST VERIFIED; SL0/SL1/SL1′ VERIFIED; L1a′ VERIFIED-WITH-AMENDMENTS; STATEMENT fidelity
VERIFIED-WITH-AMENDMENTS. 0 FATAL / 0 MAJOR / 4 MINOR. All four applied (STATEMENT v1.1; L1a_size_tail.md remarks).

| # | Finding | Action |
|---|---|---|
| R01-1 | E2(ii) cutoff display transcribed without ω ≥ 0, s₀ ≥ 1, s₀ ≤ K; false for ω = −100 | FIXED: STATEMENT §0 restores the restrictions, integer minimisation, s₀ ≤ K. Theorem 1 uses ω = ½ log n: unaffected. |
| R01-2 | L1a′ Remark 2 asserted ridge bias ≍ L²/n; false (bias ≤ ‖μ‖²; exact formula 2L²g(g+1)/((n+1)g+1)) | FIXED: Remark 2 rewritten with R01's exact formula; necessity of the coefficient bound now stated as OPEN, with numerics L1a′(e) (no failure observed). |
| R01-3 | Remark 5 constant missing +1/log 2; order claim lacked its regime | FIXED: constant [(A + ½)t + 1]/log 2, fixed t ≥ 1, p ≍ n^A; Proposition D stated as worst-case necessity only. |
| R01-4 | Positivity of φ₀, g₀, φ, b_lo/θ_lo not explicit; retained p; s_y > 0; working likelihood; real-arithmetic target | FIXED: all added to STATEMENT §0, §2 hypotheses and item 6 (with the raw-design event of [POST] lines 12-18). |
