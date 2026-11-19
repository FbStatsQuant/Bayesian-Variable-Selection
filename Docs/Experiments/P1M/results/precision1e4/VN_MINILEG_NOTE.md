# V-N mini-leg: cost sketch for the eventual NOTS runs (for the manager → HQ quote)

**Status:** DRAFT sketch, 2026-11-19, from the Sonnet builder of the V-N engine diff (branch `exp/P1M-VN` off F = `eefcbc4a`, DRAFT PR into `exp/P1M-engine`). Nothing here is submitted or deployed; nothing ran on NOTS. All measurements are on Owls (Xeon Gold 6148, `nice 19`, 4 threads, load ≈ 25). The quote itself is the manager's.

## 1. The 12 held N = 10⁴ precision fits (H1–H3)
Arms: {AR, ARweak, ADJ-OPP} × m ∈ {1, 4} × 2 replicates, R′ = 64, I_max = 3 (LEG_PLAN §4, H1–H3). LEG_PLAN quote: **17.0 core-h per m = 1 fit** (P90 23.5), **41.3 per m = 4 fit** (P90 62.4); 6 + 6 fits → E 349, P90 403.

**Check against a real N = 10⁴ run (Owls, p = 10⁴, n = 200, AR r01 s1, the overlap data; calibrate through the manifest path with `params.N = 10000`, then final islands 1 and 2):**

| | N = 2,500 (overlap record, NOTS) | N = 10⁴ (this smoke, Owls, 4 thr) | ratio |
|---|---|---|---|
| one final island, core-h | 0.0813 (measured_V_costs.csv) | **0.300 / 0.303** (user 1,075 / 1,090 CPU-s; 273 / 277 s wall × 4 CPUs) | **3.7×** |
| calibration (N-independent: H = 512; `calib.bin` sections identical to the N = 2,500 one) | 1.03 (16 CPUs billed) | 0.295 CPU-core-h (4 thr; 285 s wall) | – |
| peak RSS island / calibrate | – | 0.29 GB / 0.76 GB | – |

`quote_model.py` scales only the per-step part by N/2,500 and keeps a fixed island term, i.e. ≈ 3.05× for this island; the measurement is **3.7× (nearly linear in N)**. Re-pricing the island part of every held class by 3.7/3.05 = 1.21 (one dataset, one T = 20 grid, so this is a single datum, not a fit):

| class | fits | LEG_PLAN E (P90) | re-priced E | soft / hard stop (committed table) |
|---|---|---|---|---|
| prec N10⁴ m1 I3 | 6 | 17.0 (23.5) | **≈ 20.4** (≈ 28) | 25.5 / 42.5 |
| prec N10⁴ m4 I3 | 6 | 41.3 (62.4) | **≈ 49.8** (≈ 75) | 61.9 / 103.2 |
| **12 held fits** | 12 | 349 (403) | **≈ 421 (≈ 490)** | – |

So the LEG_PLAN figure is **≈ 20 % low for islands at N = 10⁴**; it stays under the soft stop for m = 1, but the m = 4 P90 (≈ 75) is near the soft line (61.9), so expect 1–2 soft trips. Time limits: one m = 1 island ≈ 4.6 min on 4 busy Owls CPUs; an m = 4 island (T × 4: 92 steps vs 32) ≈ 13 min → the held-batch islands limit 0:30 for m = 1 and 1:00 for m = 4 stands (LEG_PLAN H1–H3). Memory is a non-issue (0.3 GB island; merge terminal supports 11 MiB at R′ = 16 → 44 MiB at R′ = 64).
**Suggested quote line: ≈ 420 core-h expected, P90 ≈ 490, hard cap 600; wave 12 fits ≈ 2 batches; re-quote after the first batch (m = 1 arm, ≈ 120 core-h) if the per-island cost differs.** To be re-run through `quote_model.py` with the N-scaling set to ≈ 1 (linear) before committing.

## 2. NOTS bit-identity check at default N (new binary F′)
Owls already shows branch = F on two overlap V fits (AR r01 s1, ADJ-OPP r01 s1; all fit / eval / law / calib / island / setup / data files and sidecars identical outside provenance; and equal to the collected NOTS records on every scientific field). The NOTS check closes the sapphirerapids / GCC 14.3 side:
- **A0-style XB re-run of `4-AR-n200-r01-V-s1` with F′** and compare logZ_r, HPM and the 16 island output hashes with the overlap record (LEG_PLAN R7 priced this at **≈ 2.5 core-h**; measured 2.46). Optionally also ADJ-OPP r01 s1 (2.4 core-h).
- the freeze reproduction check as for F: one 10⁵ island re-run (`freeze_check_1e5.sh`, ≈ 2 core-h, 48 CPUs) and the golden suite (Owls, free).
- **≈ 5–7 core-h total.** Optionally add one N = 10⁴ canary fit (m = 1, R′ = 16, ≈ 6 core-h) to confirm the NOTS island time before releasing H1–H3 (not needed if the first H batch is the pilot).

## 3. Deferred π₀(S₀) item (PREREG / LEG_PLAN Q6, claim C3): what it needs (not built)
The engine has no output of the exact log π₀(S₀) (S₀ = the HPM / the start-mass lattice point). The pieces exist: `StartView::comp(S)` (start_view.h:76) gives the block-product term and `setup.bin` carries `logr`, `size_logmass`, `size_cum`. It would need:
1. **A small read-only reader** (new tool or `smcbvs4 start-mass`): load `setup.bin`, read a model list (the fit's `hpm_S`, or a list of S₀ candidates), return log π₀(S) = log P(|S|) + Σ_b logr_b(code) normalised exactly as `draw_pi0` / `core/cpp/v3_start.h`; **unit test against the core R/C++ values and against the empirical start draws**. About 100–150 lines and one test file; no change to any law output, so no effect on the bit identity (it can ride in the same PR, or a second one, and it only needs the same freeze tag).
2. **Inputs:** `setup.bin` of the 15 A3 fits and their 15 default pairs (LEG_PLAN R15, already kept) and each fit's `fit.bin` (`hpm_S`); data.bin is rebuildable.
3. **Cost:** ≈ 0 core-h (a post-hoc read; seconds per fit on Owls). The only NOTS cost would be re-running fits whose `setup.bin` was not kept.
4. **Open questions for HQ/Theory:** exactly which S₀ (HPM, the truth, or both), and whether to emit π₀ at calibration time (a record field → changes sidecars, so NOT in this diff).
Recommendation: build the reader after the V-N PR is accepted, as its own small PR on top of the same freeze tag; do not couple it to V-N.
