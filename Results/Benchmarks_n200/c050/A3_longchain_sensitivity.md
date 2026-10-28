# A3 (8× chain, flagged fits): long-chain sensitivity (PREREG_c050 R6)

Reported beside A3, never substituted. Long chains: 8x the production budget, same seeds and settings otherwise (engineers' runs).
Fits: 38 at c = 0.5, 32 at c = 1 (exactly the production fits with an ESS flag). Scoring problems: 0.
The `implied` columns are a sensitivity only: production fit replaced by its 8x fit for the ESS-flagged fits; never substituted for A3.

| scale | rule | p | scenario | flagged fits | still flagged at 8x | exact prod | exact 8x | gained | lost | supports changed | TP prod / 8x | FP prod / 8x | all-fits exact prod | implied all-fits exact (sensitivity) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| c100 | ci95 | 500 | pooled | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 / 0 | 0 / 0 | 574/600 | 574/600 |
| c100 | ci95 | 1000 | 1 | 26 | 1 | 20 | 22 | 2 | 0 | 2 | 364 / 364 | 10 / 8 | 91/100 | 93/100 |
| c100 | ci95 | 1000 | 2 | 5 | 0 | 4 | 4 | 0 | 0 | 0 | 70 / 70 | 1 / 1 | 95/100 | 95/100 |
| c100 | ci95 | 1000 | 6 | 1 | 0 | 1 | 1 | 0 | 0 | 0 | 14 / 14 | 0 / 0 | 100/100 | 100/100 |
| c100 | ci95 | 1000 | pooled | 32 | 1 | 25 | 27 | 2 | 0 | 2 | 448 / 448 | 11 / 9 | 575/600 | 577/600 |
| c100 | km2 | 500 | pooled | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 / 0 | 0 / 0 | 511/600 | 511/600 |
| c100 | km2 | 1000 | 1 | 26 | 1 | 24 | 24 | 0 | 0 | 0 | 362 / 362 | 0 / 0 | 90/100 | 90/100 |
| c100 | km2 | 1000 | 2 | 5 | 0 | 3 | 3 | 0 | 0 | 0 | 68 / 68 | 0 / 0 | 90/100 | 90/100 |
| c100 | km2 | 1000 | 6 | 1 | 0 | 1 | 1 | 0 | 0 | 0 | 14 / 14 | 0 / 0 | 84/100 | 84/100 |
| c100 | km2 | 1000 | pooled | 32 | 1 | 28 | 28 | 0 | 0 | 0 | 444 / 444 | 0 / 0 | 522/600 | 522/600 |
| c050 | ci95 | 500 | pooled | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 / 0 | 0 / 0 | 185/600 | 185/600 |
| c050 | ci95 | 1000 | 1 | 30 | 2 | 15 | 17 | 2 | 0 | 3 | 412 / 412 | 11 / 10 | 60/100 | 62/100 |
| c050 | ci95 | 1000 | 2 | 6 | 0 | 1 | 2 | 1 | 0 | 1 | 79 / 80 | 3 / 3 | 50/100 | 51/100 |
| c050 | ci95 | 1000 | 3 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 11 / 11 | 0 / 0 | 11/100 | 11/100 |
| c050 | ci95 | 1000 | 6 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 12 / 12 | 0 / 0 | 4/100 | 4/100 |
| c050 | ci95 | 1000 | pooled | 38 | 2 | 16 | 19 | 3 | 0 | 4 | 514 / 515 | 14 / 13 | 136/600 | 139/600 |
| c050 | km2 | 500 | pooled | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 / 0 | 0 / 0 | 139/600 | 139/600 |
| c050 | km2 | 1000 | 1 | 30 | 2 | 12 | 12 | 0 | 0 | 1 | 398 / 397 | 0 / 0 | 43/100 | 43/100 |
| c050 | km2 | 1000 | 2 | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 76 / 76 | 1 / 1 | 36/100 | 36/100 |
| c050 | km2 | 1000 | 3 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 11 / 11 | 0 / 0 | 20/100 | 20/100 |
| c050 | km2 | 1000 | 6 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 12 / 12 | 0 / 0 | 12/100 | 12/100 |
| c050 | km2 | 1000 | pooled | 38 | 2 | 12 | 12 | 0 | 0 | 1 | 497 / 496 | 1 / 1 | 128/600 | 128/600 |

Per-fit rows: A3_longchain_per_case.csv. Provisional (G5).
