# Empirical summary: 2,400 SMC-BVS v3 fits (scored 2026-10-28; provisional, before external review)

Source: `<PC_NB_ARCHIVE>\smcbvs_v3_deploy_20261022\F_analysis\` (score_p0500_20261028T1404Z, score_p1000_20261028T1404Z, HEADLINE_TABLES.md). An independent recount matches 48/48 SMC cells.

Exact recovery of the true 14-variable model, counted out of 100 per scenario (S1–S6), with the total out of 600:

| | p500 S1–S6 | total | p1000 S1–S6 | total |
|---|---|---|---|---|
| c=1, SMC-BVS HPM | 95 96 94 91 89 94 | 559 | 95 95 97 93 84 96 | 560 |
| c=1, SMC-BVS PIP>0.5 | 92 97 93 93 90 94 | 559 | 94 95 97 94 85 96 | 561 |
| c=1, SuSiE | 99 98 97 95 98 98 | 585 | 100 96 98 95 94 99 | 582 |
| c=1, spike-and-slab LASSO | 99 99 97 84 93 97 | 569 | 100 96 98 92 97 99 | 582 |
| c=1, horseshoe | 92 98 100 87 98 99 | 574 | 91 95 100 91 98 100 | 575 |
| c=0.5, SMC-BVS HPM | 79 84 64 25 59 59 | 370 | 71 75 67 35 31 61 | 340 |
| c=0.5, SMC-BVS PIP>0.5 | 74 83 63 18 53 47 | 338 | 70 76 63 24 32 56 | 321 |
| c=0.5, spike-and-slab LASSO (best benchmark) | 80 84 53 9 42 35 | 303 | 67 64 43 15 28 38 | 255 |

SMC-BVS HPM error types, pooled per p (exact / extra only / missed only / mixed / failed), with mean FP and FN:
- c=1, p500: 559 / 36 / 0 / 4 / 1. FP 0.07, FN 0.01.
- c=1, p1000: 560 / 34 / 0 / 3 / 3. FP 0.07, FN 0.01.
- c=0.5, p500: 370 / 50 / 49 / 131 / 0. FP 0.39, FN 0.40.
- c=0.5, p1000: 340 / 47 / 84 / 127 / 2. FP 0.39, FN 0.49.
- For comparison at c=0.5: SuSiE FN 2.6–2.7; horseshoe FN 1.75–1.98.

**The diagnostic flag versus recovery.** At c=1, flagged fits were exact 34/34 (p500) and 48/56 (p1000); unflagged fits 525/566 and 512/544. The flag does not predict wrong answers.

**Failures and escalation.** 6 fits failed with `resource_limit`, all in S5. 208 fits escalated (4× particles and stages).

**Runtime per fit.** The median is 486–522 s at p500 and 1,337–1,405 s at p1000. SuSiE takes seconds and horseshoe takes 5–11 min.
