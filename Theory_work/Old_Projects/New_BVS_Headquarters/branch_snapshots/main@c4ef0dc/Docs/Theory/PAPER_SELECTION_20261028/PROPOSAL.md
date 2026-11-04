# HQ proposal: theorems for a JRSS-B / Biometrika paper (2026-10-28)

**Felipe's premise.** Assume every conjecture T01–T36 is provable. Assumptions may be modified, the methodology may get minor tweaks (for example budget sequences indexed by n), and statements may be restated. The target is JRSS-B, or at least Biometrika. The main text should carry 5–10 results, chosen for the highest return on investment.

**Story.** What SMC-BVS reports is consistent, and the reason is that the truth gets *scored*, not that the sampler converges. The reported HPM is the best model ever scored.

## Main-text selection (8)

| Paper # | Conjecture | Role | Proof work left |
|---|---|---|---|
| Thm 1 | T03 (with T02 and T01 as lemmas) | The posterior concentrates on the truth | Restate on the capped space (|S| ≤ K + s0) so the SE premise is not impossible at finite n; s0 fixed |
| Prop 1 | T07 | The HPM is the Bayes rule for exact recovery; no size-only prior can repair a within-size ranking error | None |
| Thm 2 | T22 | The composite start puts provable mass on, or near, the truth; it concentrates in the favourable regime | Finish (iii) |
| Thm 3 | T27 | Masking lower bound: the start gives the truth only about p^-d n^-d/2 mass, so the start alone can fail | Finish |
| Thm 4 | T24 | Terminal repair: from a near-truth particle, the final rounds score the truth with high probability | All |
| Thm 5 | T21 | Composition: P(wrong report) ≤ P(no output) + 2E[posterior mass off the truth] + P(truth never scored) | None (T24 supplies H24) |
| Thm 6 | T26 | Main theorem: the reported HPM, the PIPs and the evidence estimate Ẑ are all consistent under budgets indexed by n | All (it composes the others) |
| Prop 2 | T12 | The evidence estimate is unbiased, and so is Ẑ·PIP, for the frozen run | None |

- **Biometrika cut (5):** Thm 1, Prop 1, Thm 4, Thm 5, Thm 6. T22 and T12 become remarks.
- **Supplement lemmas:** T01, T02, T09, T10, T11, T13, T14, T15, T20, T23.
- **Remarks:** T04, T06, T31, T32, T33, T34.
- **Dropped:** T05, T08, T16, T17, T18, T19, T25, T28, T29, T30, T35, T36.

## Known context

- **Empirical results** (`04_Reports_and_Presentations/STATUS_BRIEFING_20261028/BRIEFING.md` §4):
  - At c = 1, SMC-BVS trails SuSiE, SSL, the horseshoe and SSL-RS by 2–6 points; its misses are mostly the truth plus extra variables.
  - At c = 0.5, SMC-BVS leads clearly, by 11–34 points (paired) over the Bayesian competitors.
  - It is about 85–500× slower than SuSiE and SSL.
- **No current theorem explains the weak-signal advantage** over SuSiE and SSL.
- At n = 200 the asymptotic results are numerically vacuous (INVENTORY §C).
