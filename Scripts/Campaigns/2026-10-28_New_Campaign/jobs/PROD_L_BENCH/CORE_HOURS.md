# PROD-L benchmark wave: core-hour estimate (billed = allocated CPUs × elapsed; 1-CPU tasks bill 2)

Source: the accepted pilot's benchmark timings (`ops/PROD_L_SIZING_20261030.md` §2–§3; 24 cases × 8 methods, R 4.5.2, Sapphire Rapids): mean case wall 28.54 s (all 8 methods; per method F1 5.3, F2 3.2, F3 2.2, F4 1.0, F5 2.8, A1 3.8, A2 1.0, A3 9.3 s), p90 30.25 s, peak RSS 256 MiB.

| Item | Formula | Billed core-h |
|---|---|---|
| Expected | (2,400 × 28.54 s + 96 tasks × 5 s) × 2 / 3,600 | **38.3** |
| Conservative (p90 case wall) | (2,400 × 30.25 s + 96 × 5 s) × 2 / 3,600 | **40.6** |
| F3 sensitivity (D42: F3 now fits a CV-lasso pilot, ≈ F1's 5.3 s per case, measured before with the ridge pilot) | + 2,400 × 5.3 s × 2 / 3,600 | **≈ 45.4** |
| Doubled-time retries | ≤ 2 × (1,200 + 60) s × (cases retried) / 3,600 | ≈ 0.7 per retried case at most |
| Requested-wall ceiling (not a forecast) | 96 tasks × 1 h × 2 | 192 (+ retries 1 h × 2 per retry task) |

Notes. The pilot ran one Rscript per method (8 R start-ups per case); production runs one call per case (`--methods all`), so its per-case overhead is lower than the pilot's sum, which makes the estimates above conservative on that term. Infrastructure jobs (verify, collect) add ≈ 0.05. Laptop timings from the live local run are NOT used for sizing (different platform; charter rule 6). Revise from `accounting/core_hours.tsv` after the main wave.

Wall clock (alone, excluding queue): 96 tasks at `%32` → 3 waves × ≈ 12 min ≈ 40 min; at `%16` (with PROD-H) ≈ 75 min.
