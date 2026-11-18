# case2 · gpt-6.1-sol (codex, reasoningEffort high), SCORED run

Wrapper: chunks of 120 lines; no other file. Run about 19:16 to 19:19 CT (wall ≈ 3–4 min). Full reply: T3 child thread "SOL62 A/B case2 · gpt-6.1-sol". Header line correct.

**Verdict line:** `COUNCIL-VERDICT round=R1 manifest=6f8c05aa… seat=sol score=8.0 gates=FAIL`. Claim decisions: Thm2X **NOT-EXAMINED**, Cor2X **NOT-EXAMINED**. The rubric expects ACCEPT for both, and the stored 6.1 original ACCEPTed both (9.2, gates=FAIL). The model gives missing sources as its reason.

**Findings:**
- **F1 (F):** `log_comb` lgamma cancellation at p → 10¹⁵. It gives log_comb(2·10¹⁵−1, 1) = 40 vs 35.2319, and m♯ = 95 vs 76 (stable recurrence given). "Exact" is unsupported. **Known answer: CAUGHT, with the bonus recomputation.**
- **F2 (F):** TARGET.md:26 states "P(HPM ≠ S₀) = 0 at n = 1600", but this is 0 errors in 300 Monte Carlo replications, not a probability. **Verified real** (PROMPT line 307 vs line 492). This minor faithfulness point is not in the known answer.
- **Analytic checks:** all pass (cutoff bound k_n ≤ 3(A+1)(s₀+1) log n, Markov, energy/beta-min). There is no false C/S finding.
- **Interpretive-sentence inventory:** complete for the supplied spans.
- **Sweep and unverifiable sources:** marked "not supplied" (correct).
- **Gates:** correct FAIL · strength FAIL · faithful FAIL · statuses PASS · sweep FAIL · reader FAIL. Several of these FAILs come from missing sources rather than defects.
- **Better-theorem proposal:** the liminf threshold instead of ρ_n → ∞. Offered as a proposal, not a finding.

**Score.**
- Known answer: caught (bonus: 76 vs 95).
- New: 1 verified real minor (F2).
- False: 0.
- Nitpick: 0.
- Fidelity: weaker. It returned NOT-EXAMINED instead of a decision, and turned missing inputs into gate FAILs. This is the same pattern as its case 1 run.
