# PROD-L core-hour estimate (billed = allocated CPUs × elapsed; from `ops/PROD_L_SIZING_20261030.md`, scaled to 12,000 repeats per D16/D47.1)

Scope: fitting pieces plus the infrastructure jobs (build, P0a/P0b, truth-lock test, lock, unlock, collect: ≈ 0.06 core-h in the pilot; 0.2 allowed here for the larger P0b and two extra waves). Excludes P5 reruns (none expected; 0 of 28 pilot fits), benchmarks (separate bundle, ≈ 38–41) and local scoring.

| Piece | Units | Layout | Billed CPUs/task | Expected | Conservative | Delay sensitivity |
|---|---|---|---|---|---|---|
| enum20 | 600 | 1 task, 4 threads | 4 | 1.30 | 1.62 | — |
| enum30 | 600 | 24 × 25, 16 threads | 16 | 73.1 | 76.3 | — |
| smc primary | 2,400 | 96 × 25 | 2 | 10.9 | 15.9 | 21.6 |
| smcrep (100 r × 5 m) | 12,000 | 480 × 25 | 2 | **48.4** | **79.4** | **95.0** |
| infrastructure | – | – | 2–4 | 0.2 | 0.2 | 0.2 |
| **Total** | | | | **≈ 134** | **≈ 173** | **≈ 191** |

Formulas (seconds × billed CPUs / 3,600; per-task overhead 5 s; delay scenario 500 s per 28 tasks as in the sizing):
- smcrep expected: (12,000 × 6.35 + 480 × 5 + 480/28 × 500) × 2 / 3,600 = 48.4. Conservative: 11 s/fit in place of 6.35 s = 79.4. Sensitivity (Sol: one excess process delay of ≈ 215.7 s per 28 fits, i.e. the sizing's 19.07 for 2,400 fits scaled): (12,000 × 6.35 + 480 × 5 + 12,000/28 × 215.7) × 2 / 3,600 = 95.0.
- All other rows are the sizing's accepted figures (§3 there). Repeat timing rests on 2 pilot fits per p; revise from the first production evidence (`accounting/core_hours.tsv`).
- Against HQ's expectation (D47: ≈ 95–110 plus ≈ 40 for the extra repeats): the expected 134 sits at the low end of 135–150; the conservative 173 is above it because the 11 s/fit allowance applies to 12,000 repeat fits.

Requested-wall ceilings (charged only if every task ran to its limit; not a forecast): enum20 4 × 1 h = 4; enum30 24 × 16 × 0.75 h = 288; smc 96 × 2 × 5 h = 960; smcrep 480 × 2 × 5 h = 4,800; infrastructure ≈ 6; total ≈ 6,058 billed core-h. P5: 16 is the nominal doubled core allocation (8 h × 2 billed); the wrapper bound is 29,160 s ≈ 16.2 core-hours; the requested-wall ceiling is 18 per unit.

Wall clock (alone, excluding queue): enum30 6 waves × 11.4 min ≈ 70 min; smc 3 × 3.1 min then smcrep 15 × ≈ 3 min ≈ 55 min, in parallel with enum30: ≈ 75 min. With PROD-H (throttles halved): ≈ 2.5 h.
