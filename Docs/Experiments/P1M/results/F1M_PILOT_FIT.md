# The first 1M fit (P10): 6-AR-n200-r01-V-s1, 2026-11-17 — COMPLETED, HPM = MPM = S₀

AR strong, n = 200, **p = 10⁶**, V mode (N 2,500, R′ = 16, bounded calibration), seed 602020001. Code exp/P1M-engine 2cfaa9e5
(levers 1–3 + m3, offer floor D-29, StartView, 10⁶ memory re-size), island ISA sapphirerapids. Batch F1M_pilot, jobs 2761931
(setup) · 2761932 (calibrate) · 2761933_1–16 (islands) · 2761934 (merge + tail + LS0) · 2761935 (eval + post). All COMPLETED, no
retries. Submitted 07:33 CT, eval ended 10:38 CT: **3 h 04 min**. HQ P9 GO; stop rule 675 not reached.

## Result
- **Selection:** HPM = MPM = S₀ = {100000, 300000, 500000, 700000, 900000}. Plug-in h²(HPM) = h²(MPM) = h²(oracle) = 0.0052197.
  The HPM was first found in the calibration pilot (stage 1, φ = 0.041, Gibbs flip); local search and LS0 did not change it.
- **Predictive / Hellinger (eval, n_test 10,000):** predictive h² HPM = MPM = oracle = 0.0057858; the V-law mixture (T) 0.0060010
  (plug-in 0.0046391, weighted plug-in 0.0106809). log Ẑ = −245.107 (log Ẑ_T −245.388).

## Cost (MEASURED, sacct CPUTimeRAW)
| stage | request | elapsed | billed core-h |
|---|---|---|---|
| setup (gen + prep + setup) | 48 CPUs, 48G | 19:04 | 15.25 |
| calibrate | 96 CPUs, 128G | 1:24:46 | 135.63 |
| 16 final islands | 16 × 96 CPUs, 64G | 8:46–13:12 each | 269.25 |
| merge + tail + LS0 | 32 CPUs, 80G | 31:42 | 16.91 |
| eval + post | 8 CPUs, 16G | 3:01 | 0.40 |
| **total** | | **3:04 wall** | **437.44** (P9 estimate 390–440; H-10 budget 1,188 per fit) |

## Profile
- **Setup:** correlation 780 s, tables, start law 44 s (as P7).
- **Calibration (4,808 s):** the pilot island + **12 diagnostic islands** (3 iterations k1–k3 × 4), each ≈ 300–317 s at N 512:
  bridge 27 rounds ≈ 1,720–1,860 ns·CPU per step, offers 0.034–0.036 per step; burn-in/measured ≈ 760–830 ns·CPU per step;
  M 3.5 → 4.4; mean |S| 5.0 → 6.4; peak RSS 53–55 GB.
- **Final islands** (16 × 96 threads, N 2,500, G 256; O2 cost records via `p1m_stage_cost.py`, which finished after ≈ 1 h on the
  login node: slow but working): 526–792 s each (avg 16.8 core-h); T = 27 bridge rounds + 8 burn-in + 4 measured.
  | kind | ns·CPU per step (range, mean) | M | offers per step | wall s (mean) | compaction s | peak RSS GB |
  |---|---|---|---|---|---|---|
  | bridge (27) | 327–389, **350** | 3.58 | 0.00068 | 246 | 5.2 | 26.2 |
  | burn-in (8) | 440–522, 474 | 4.34 | 0.00021 | 99 | 4.3 | 27.0 |
  | measured (4) | 454–572, 495 | 4.35 | 0.00009 | 52 | 2.2 | 27.1 |
  The offer floor works: bridge offers 0.0007 per step vs 0.035 in the (unfloored) calibration islands (−98%). The bridge cost per
  step (350) is half the P9 estimate (706); the late cost (≈ 480) is close to it (578).
- **Merge:** islands merged in 834 s; tail 1,215 s (final local search 4.0 s, **LS0 3.8 s**); **peak RSS 75.1 GiB of the 80G
  request vs WP3's plan 43.7 GiB** (under-count: see below).

## Gaps found (no effect on the result)
1. **Merge memory under-count** (plan 43.7 GiB, measured 75.1 GiB) and a 20-min merge tail: cause to measure (16 island top stores
   loaded at once + the merged store + mapped setup/island pages counted in RSS are the candidates). Interim: merge request → 128G
   before any further 1M fit; WP4 (merge owner, Sonnet) measures and fixes the plan.
2. **Calibration time** 85 min vs ≈ 55 estimated: the V calibration ran **3 iterations** (12 diagnostic islands), not the 2 (8) the
   estimate assumed from T5; the islands themselves cost what P7 predicted. O3 (parallel leader-store compaction, builder 7) cuts
   the per-island compaction (≈ 38 s of each ≈ 300 s).
3. `p1m_stage_cost.py t5` takes ≈ 1 h on 16 island files at 10⁶ (full-file reads), and `smcbvs4 info --meta` by hand returned invalid_input → builder 7 makes it read the meta section only.
