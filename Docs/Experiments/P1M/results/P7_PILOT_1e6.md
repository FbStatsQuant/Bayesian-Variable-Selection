# P7: the 10⁶ calibration pilot (H-11 gate (2)), 2026-11-17 — COMPLETED

Cell `6-AR-n200-r01-V-s1` (AR strong, n = 200, p = 10⁶), production setup (WP2 `setup` + D-31 + StartView), then the pilot
island alone (`v4_pilot_island` = the first island of `calibrate --mode V`, calibration ledger held). Code exp/P1M-engine
2cfaa9e5 (levers 1–3 + m3, offer floor, StartView, 10⁶ re-size), island ISA sapphirerapids. Jobs 2761787 (setup, 48 CPUs) and
2761788 (pilot, 96 CPUs), both COMPLETED. **Billed 30.17 core-h** (setup 15.21 + pilot 14.96; expected 25–50, worst 144).

## Setup at 10⁶ (MEASURED, 48 threads)
- Wall 19:01; correlation **789 s** (dominant), tables 172 s, start law 44 s, partition 3.7 s; J = 74,734 blocks, B = 14.
- setup.bin 10.14 GB; peak RSS 13.5 GB (accounted 20.3 GB); sacct MaxRSS 23.7 GB.
- 15.2 core-h per dataset (shared by every fit on that dataset).

## Pilot island (N 512, G 256, 96 threads, label-major, class A) — per-stage cost record (O2)
T = 20 bridge stages, 8 burn-in, 4 measured (34 rows with init/exit). Island 314.8 s (+ inputs 223 s); peak RSS 48.7 GB.
| kind | rounds | wall s | M | mean \|S\| | flips/step | active cols/pass | offers/step | compaction s | ns·CPU per step |
|---|---|---|---|---|---|---|---|---|---|
| bridge | 20 | 259.7 | 3.64 | 5.08 | 0.78 | 81 | 0.046 | 39.8 | 2,435 |
| burn-in | 8 | 36.1 | 4.20 | 6.34 | 0.95 | 128 | 0.0030 | 4.8 | 847 |
| measured | 4 | 18.4 | 4.53 | 6.45 | 0.99 | 144 | 0.0008 | 2.2 | 861 |
- First bridge stage (φ = 0.041): 70 s, 13,138 ns·CPU per step (offers 0.23 per step, 9 compactions); by φ ≈ 0.5 it is ≈ 1,000–1,600.
- Late rounds: ≈ 219–224 ns·CPU **per pair** at M ≈ 4.4–4.6 (round 32: products 27 ns/pair, phase A 67, phase B 0.9 s); store
  check 0.14 s at exit only (O1); Gram-row reuse 63% (K3).

## Against the R1 model's anchors (results/R1_RESIZE.md)
- **Late M** 4.4–4.6 (anchor 3.9; G0 5.5): above the low anchor, inside the G0 bracket.
- **Offers per bridge step** 0.046 (bracket 0.01–0.10): mid-bracket, before the offer floor (calibration islands never floor).
- **ns·CPU per pair, late:** 219–224 at N = 512 against the anchor ≈ 116 at N = 2,500. The per-pair cost at N = 512 is not
  comparable 1:1: the T5 run at 10⁵ measured final islands (N 2,500) at 0.68× the late and 0.29× the bridge per-step cost of
  its N = 512 diagnostic islands. Applied below.

## P9 re-size (ESTIMATE from MEASURED P7 + T5 numbers; method and assumptions stated)
| component | basis | core-h |
|---|---|---|
| setup | MEASURED (P7) | 15 |
| calibration | 9 islands of N 512 (pilot + 8 diagnostic, as T5's V calibration) × 8.9 core-h (P7 island) + 6 (inputs) | ≈ 86 |
| 16 final islands | per round 2.5·10⁹ steps; bridge 2,435 × 0.29 ≈ 706 ns·CPU/step, late 850 × 0.68 ≈ 578; 20–30 bridge rounds + 12 late | ≈ 273–312 |
| merge + tail + LS0 | T5: 0.7 core-h at 10⁵; 10⁶ ≈ 10× | ≈ 10–16 |
| eval + post | | ≈ 5–8 |
| **per 1M fit** | | **≈ 390–440** (high bracket × 1.5 ≈ 660) |
- f = fit / 1,188 ≈ 0.33–0.37 (high 0.56) → campaign ≈ 27,608 + 15,293·(f − 1) ≈ **17.9k–18.3k** (high ≈ 20.9k), under 28.3k.
- The offer floor (O6, merged) lowers the final islands' bridge offers further; not credited here.
- Final-island wall ≈ 17–20 core-h / 96 CPUs ≈ 11–13 min, far inside the 2 h task limit. Calibration ≈ 50–55 min on 96 CPUs.
- Risks: the 0.29 / 0.68 N-scaling factors come from 10⁵; the final schedule's T at 10⁶ is not yet known (20–30 assumed);
  first-stage cost dominates the bridge.
