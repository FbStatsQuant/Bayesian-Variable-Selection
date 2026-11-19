# ADDENDUM_1_BOUNDARY: one boundary-regime V-vs-T check (wave B1) inside the precision + 10⁴-science leg

**Status: COMMITTED by the Engineering manager (2026-11-19) before any B1 run; GO (expected quote 115 ≤ 120, HQ_DECISIONS 09e24da1 / DECISIONS H-27).** Generator and quote scripts copied to `B1/`. Owner-approved add-on (HQ_DECISIONS 09e24da1; owner: "cheap, and no overthinking"). Author: Sonnet design worker, 2026-11-19. Descriptive only; no new pass/fail, no change to any registered script, threshold or table.

## Why, and what
In the 10⁴ T-vs-V overlap every AR-weak fit (n = 200, β_min·√n ≈ 5.1) recovered S₀, so V vs T was never tested on a spread-out posterior. One check: **AR-weak, p = 10⁴, n = 100 (β_min·√n ≈ 3.6), ONE dataset, V and T × 2 seeds = 4 fits.**

| item | value |
|---|---|
| wave / batches | **B1**: `PL_B1_1` (V, 2 fits, 40 tasks), `PL_B1_2` (T, 2 fits, 16 tasks) |
| dataset | `4-ARweak-n100-r91`: data seed **403010091** (R 4, D 3, n/100 = 1, **rep 91**; MANIFEST_CELLS §1 rule) |
| seeds | s1 = 403010091, s2 = 403010191 (data seed + 100); V and T share (data seed, engine seed), as in the overlap |
| run ids | `4-ARweak-n100-r91-{V,T}-s{1,2}` |
| collision check | seeds 403010091 / 403010191 and rep 91 are absent from every fit of the generator (overlap 40, precision 24 + 6, science 156; science AR-weak n = 100 uses reps 1–20): asserted in `make_waves_b1.py`. Rep 91 is **reserved for B1** |

## Settings (identical to the overlap)
- **V:** V-1M class A (island_isa sapphirerapids), N 2,500, R′ 16, bounded calibration, default m = 1, I_max = 3 whatever the leg's precision freeze says (like the A0 canaries; the overlap's configuration is what B1 tests). Shapes = the leg's s100 class. The leg's V build **d0c30b65…** is copied (COPYBIN), no V rebuild.
- **T:** law mode, N 10⁴, R′ 4, coded calibration with escalation (tier k → N = 10⁴·4ᵏ). Shapes = overlap W3: calibrate 48 CPU 16 G **5:00** (`max_task_hours` 5.0), islands 24 CPU **2:00**, merge 0:20, eval 0:30.
- **One T build** (H-25): the leg has none; T is built ONCE at F (default ISA) and recorded in `deploy_leg.log` as a `BUILD_T` line (sha256, F, libm). No rebuild.
- Plans: `~/SMC_Engineering_Department/tmp/20261119-b1/B1/plans/` (`make_waves_b1.py` sha `f19e540e…`); driver `--strict` clean, no warnings. Plan sha256: `PL_B1_1` `9a1235ab…`, `PL_B1_2` `ab30848d…`. Worst (limit sum, a ledger figure, not an estimate): V 93.4, T 881.4.

## Scoring (descriptive)
`compare_overlap_v2.py` (sha **4f402e51…**, unchanged) with `--wave-check` on the 4 records (+ `--cross-file` for d_H(V, T); the script labels the dataset `4-ARweak-n200-r91`, cosmetic, use that key). Report per fit and per seed pair: HPM = S₀? / HPM equal V vs T, F_hpm, log Ẑ (V − T, s.e.), PIP differences, d_H(V, T) vs d_H(T, f*), tier_final / N_final, core-h; plus how spread the posterior is (HPM mass, max island PIP sd). **No outcome class, no criterion verdict, no effect on the leg's gates.** The registered script's output is shown beside it, as in every overlap read-back.

## Offset cell
One more cell of the leg's pre-declared offset measurement (PREREG §4): **cell (N 2,500, m 1, I_max 3, k = 16, src = `bnd`)**, δ_B1 = mean over the 2 seeds of [log Ẑ_V − log Ẑ_T] on this one dataset, with its seed spread and island s.e., in units of s_T (0.00324). One dataset has no dataset-level interval; it is printed as a point, not tested. **No offset-vs-p** is drawn from it. Computed by hand from `wave_check.csv`; `precision_offset.py` is not changed.

## Quote (core-h; unmeasured n = 100 priced from the 20 T + 20 V overlap fits)
Model `quote_b1.py` (sha `ac1e58ae…`, 20,000 draws, output `quote_b1_output.txt`). T tier-0 costs: 75 % of fits drawn from the AR/ADJ/IND tier-0 fits (35.8–51.5; a spread posterior should not look like the cheap AR-weak n = 200 fits, 7.7–23.2); escalation probability per dataset ~ Beta, mean 0.35 (observed 3/20 = 0.15), tier 2 with 10 % given escalation; n = 100 factor 0.85 (planning 0.7; unmeasured for T).

| | E | P50 | P90 | P99 |
|---|---|---|---|---|
| T × 2 | 110.7 | 92.5 | 201 | 347 |
| V × 2 | 3.8 | 3.7 | 4.6 | 5.5 |
| **B1 (4 fits)** | **114.5 ≈ 115** | 96 | **205** | 351 |

Gate (expected quote ≤ 120): **GO**, with a thin margin and a wide spread: P(total > 120) ≈ 0.36, P(a T fit > 172.5) ≈ 0.05. Sensitivity of E: n factor 0.7 → 95, 1.0 → 134; escalation mean 0.17 → 90; all-hard tier-0 and mean 0.5 → 143 (`tmp/20261119-b1/sensitivity_b1.txt`; the n = 100 T cost is the unknown). The leg's measured-basis quote is unchanged (E 592); B1 adds ≈ 115.

## Stops
- **V per fit:** soft 1.5× / hard 2.5× of class `ARweak n100` in the committed table (E 1.36: soft 3.0 floor, hard 3.4), HQ Q3: soft = report-and-continue, hard = STOP.
- **T per fit:** report-and-continue above **172.5** core-h (PREREG_ADDENDUM_2 style: the fit is not cancelled; recorded as cost-criterion FAIL for that fit, nothing else changes). Still STOP: a T calibrate TIMEOUT (5:00), any non-infrastructure failure, > 2 failed fits, admission refusal, X/y mismatch across the 4 fits.
- **Wave:** actual > 2 × quote = **230** core-h.
- **Cumulative:** B1 counts inside the leg's cumulative stop (baseline 1,000; 1,600 / 900 if m = 4 / I_max = 0 is frozen): leg actual = 592 (E) + 115 ≈ 707.
- Build identity: V = the leg's d0c30b65…; T = its own single `BUILD_T`.

## Monitor tooling (not edited here; proposal for the manager)
`stop_rules_prec.py` covers the V fits (class `ARweak n100` is in the pinned table; RID accepts rep 91) but **not the T fits**: `klass()` returns None → false STOP; arm identity expects rule `bounded` and the plan N (T is `coded`, N = 10⁴·4ᵏ); build identity compares every batch with the leg's V build. Minimal change, `TABLE` / `TABLE_SHA256` untouched: (1) a T branch before the table lookup: report-only above 172.5, no soft/hard line; (2) T arm identity: rule `coded`, N ∈ {10⁴·4ᵏ}, skip refine_m / I_max; (3) batches with plan mode `law` compare to the `BUILD_T` line; (4) `QUOTE["B1"] = 115` (or `QUOTE=115`); (5) projection: T mean 44 for T fits left. `deploy_wave.sh` / `presubmit_check.sh` also assume V (sapphirerapids, one BUILD line, MASTER_BATCH PL_A0_1): `PL_B1_2` needs a T build mode that logs `BUILD_T`, and presubmit must skip the ISA test for it.
