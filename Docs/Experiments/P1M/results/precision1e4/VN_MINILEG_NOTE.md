# V-N mini-leg: cost sketch for the eventual NOTS runs (for the manager → HQ quote)

**Status:** DRAFT sketch, 2026-11-19, v2 after the Opus review of PR #88 (`reviews/PR88_REVIEW_OPUS.md`, ACCEPT-WITH-FIXES: F1 the ratio and the batch count, F6 H = 512, F7 island time). From the Sonnet builder of the V-N engine diff (branch `exp/P1M-VN` off F = `eefcbc4a`, DRAFT PR #88 into `exp/P1M-engine`). Nothing here is submitted or deployed; nothing ran on NOTS. All measurements are on Owls (Xeon Gold 6148, `nice 19`, 4 threads, load ≈ 25). The quote itself is the manager's.

## 1. The 12 held N = 10⁴ precision fits (H1–H3)
Arms: {AR, ARweak, ADJ-OPP} × m ∈ {1, 4} × 2 replicates, R′ = 64, I_max = 3 (LEG_PLAN §4, H1–H3). LEG_PLAN quote: **17.0 core-h per m = 1 fit** (P90 23.5), **41.3 per m = 4 fit** (P90 62.4); 6 + 6 fits → E 349, P90 403.

**Check against a real N = 10⁴ run (Owls, p = 10⁴, n = 200, AR r01 s1, the overlap data; calibrate through the manifest path with `params.N = 10000`, then final islands 1 and 2). The ratio is SAME-MACHINE (reviewer F1; my first figure, 3.7×, divided an Owls N = 10⁴ island by a NOTS N = 2,500 island):**

| | N = 2,500 (Owls, same grid, T = 20, 4 thr; 4 runs) | N = 10⁴ (Owls, 4 thr) | ratio |
|---|---|---|---|
| one final island, wall | 59–79 s, mean **70.7 s** | **270.5 / 274.4 s** (builder: 273 / 277 s; user 1,075 / 1,090 CPU-s) | **3.85×** (range 3.4–4.6; Owls load noise ±15 %): effectively **linear in N** |
| one final island, core-h (4 CPUs billed) | ≈ 0.079 | **≈ 0.30** | |
| calibration (N-independent: H = 512; `calib.bin` sections identical to the N = 2,500 one) | 1.03 core-h (NOTS, 16 CPUs billed) | 0.295 CPU-core-h (4 thr; 285 s wall) | – |
| peak RSS island / calibrate | – | 0.29 GB / 0.76 GB | – |

`quote_model.py` scales only the per-step part by N/2,500 and keeps a fixed island term, i.e. ≈ 3.05× at this grid. **Quote with linear N scaling** (N-factor 1.0 in the model; re-run `quote_model.py` before the commit). Re-pricing the island part of each held class by 3.85/3.05 = **1.26** (one dataset, one T = 20 grid: a single datum, not a fit):

| class | fits | LEG_PLAN E (P90) | re-priced E (P90) |
|---|---|---|---|
| prec N10⁴ m1 I3 | 6 | 17.0 (23.5) | **≈ 21.2** (≈ 29.6) |
| prec N10⁴ m4 I3 | 6 | 41.3 (62.4) | **≈ 51.7** (≈ 78.6) |
| **12 held fits** | 12 | 349 (403) | **≈ 440 (P90 ≈ 510)**, under the 600 cap |

(Slightly conservative: the factor is applied to the island part only, but calibration, ≈ 10 % of a fit at R′ = 64, does not scale.) The LEG_PLAN figure is thus **≈ 26 % low for islands at N = 10⁴**. The m = 4 class re-priced is E ≈ 52 against the old soft line 61.9 (P90 ≈ 79): **soft trips are likely unless the mini-leg commits its own class table (below, §1.2).**

**Batches: 6, not 2** (reviewer F1). 12 fits × (64 islands + setup, calibrate, merge, eval = 68 tasks) = 816 tasks; at ≤ 150 tasks per batch that is **6 batches = 3 waves × 2**, as P1–P4. Re-quote after the first wave (the m = 1 arm, ≈ 130 core-h) if the per-island cost differs.

**Time limits and the driver (reviewer F7, PR task 5).** The driver's `DEFAULT_RES` do not scale with N (islands 0:15 at 16 CPUs for the 10⁴ rung). The engine diff does not touch the driver (V stays byte-identical at default N, no `p1m_driver.py` conflict with PR #86). **The mini-leg plans set `resources.islands` explicitly** (per-fit or plan-level; the driver validates it and refuses > `max_task_hours` = 2 h: dry-run checked: 0:15 default, 0:30 explicit accepted, 3:00 refused). Measured on 4 CPUs: m = 1 island ≈ 4.6 min, m = 4 (92 steps vs 32) ≈ 13–14 min, so **islands 0:30 for m = 1 and 1:00 for m = 4** (LEG_PLAN H1–H3) stand. For the 1M N = 5,000 self-check size the plan-level islands time from 2× the measured 1M N = 2,500 island (cap 2:00).

### 1.1 What the N = 10⁴ arm measures (reviewer F6 / §4)
**The N = 10⁴ arm changes the final islands' N only; the calibration (H = 512, the grid rule) is the same law as at N = 2,500 (D-26): at the same seed the grid and `calib.bin` sections are identical, meta differs only in `N`. c_X is islands-only (R16), consistent with this.** It is a pure island-N contrast; it does not test T's coupling (T's H₀ = ⌈512 N₀/2,500⌉ grows with N). Put this sentence in the mini-leg addendum / PREREG §3.3. Note for the ADOPT rule (r ≤ 1/√c_X): with c_X ≈ 3.85 the bar is r ≤ 0.51 on each of M1–M3 (see R3's resolution figures).

### 1.2 Committed class table for the mini-leg's stops (H-26 Q3 / Q4 form: soft = max(3.0, 1.5 E), hard = max(3.0, 2.5 E); the hard line is never re-fitted)
E per fit from the re-priced §1 (linear N scaling, same-machine ratio); P90 for information.

| class | fits | E | P90 | soft | **hard** |
|---|---|---|---|---|---|
| prec N10⁴ m1 I3 (AR, ARweak, ADJ-OPP × 2 rep) | 6 | 21.2 | 29.6 | 31.8 | **53.0** |
| prec N10⁴ m4 I3 (same) | 6 | 51.7 | 78.6 | 77.6 | **129.3** |
| XB identity fit, AR r01 s1, N = 2,500, R′ = 16 (F′ default-N check) | 1 | 2.5 | 3.0 | 3.7 | **6.2** |
| XB identity fit, ADJ-OPP r01 s1 (optional) | 1 | 2.4 | 2.9 | 3.6 | **6.0** |
| N = 10⁴ canary, m = 1, R′ = 16 (optional) | 1 | 6.0 | 8.0 | 9.0 | **15.0** |

Wave stop: wave actual (billed) > 2 × its quote. **Cumulative stop: 600 core-h = the hard cap** (1.6 × E = 700 would exceed it). Projection ceiling: the hard cap 600 (H1–H3 only; the 4,127 plan figure is the leg's, not this mini-leg's). Soft-trip rule as H-26 Q3: report-and-continue, ≥ 3 soft trips in one wave = STOP; **expected soft trips: 1–2** (m = 4). Arm-identity checks as LEG_PLAN §5.3 with N added: recorded `calib N` must be 10,000 for every H fit (and 2,500 for the XB fits). G-B reading: class mean ≤ 1.5 × the committed class E (Q4 (b)).

## 2. NOTS bit-identity check at default N (new binary F′)
Owls shows branch = F on two overlap V fits (AR r01 s1, ADJ-OPP r01 s1: all 45 files per fit, every scientific field of fit / eval / law / calib / 16 islands / setup / data and sidecars; re-compared with an explicit-provenance-list checker, v2) and equal to the collected NOTS records on every scientific field; the Opus reviewer re-ran AR r01 s1 independently (567/567 sections). The NOTS check closes the sapphirerapids / GCC 14.3 side:
- **A0-style XB re-run of `4-AR-n200-r01-V-s1` with F′** and compare logZ_r, HPM and the 16 island output hashes with the overlap record (LEG_PLAN R7: **≈ 2.5 core-h**; measured 2.46). Optionally also ADJ-OPP r01 s1 (2.4 core-h).
- the freeze reproduction check as for F: one 10⁵ island re-run (`freeze_check_1e5.sh`, ≈ 2 core-h, 48 CPUs; the golden suite runs on Owls for free).
- **≈ 4.5–6.9 core-h total** (reviewer-confirmed). Optionally add one N = 10⁴ canary fit (m = 1, R′ = 16, ≈ 6 core-h) to confirm the NOTS island time before releasing H1–H3.

## 3. Deferred π₀(S₀) item (PREREG / LEG_PLAN Q6, claim C3): what it needs (not built)
The engine has no output of the exact log π₀(S₀) (S₀ = the HPM / the start-mass lattice point). The pieces exist: `StartView::comp(S)` (start_view.h:76) gives the block-product term and `setup.bin` carries `logr`, `size_logmass`, `size_cum`. It would need:
1. **A small read-only reader** (new tool or `smcbvs4 start-mass`): load `setup.bin`, read a model list (the fit's `hpm_S`, or a list of S₀ candidates), return log π₀(S) = log P(|S|) + Σ_b logr_b(code) normalised exactly as `draw_pi0` / `core/cpp/v3_start.h`; **unit test against the core R/C++ values and against the empirical start draws**. About 100–150 lines and one test file; no change to any law output, so no effect on the bit identity (it can ride in the same PR, or a second one, and it only needs the same freeze tag).
2. **Inputs:** `setup.bin` of the 15 A3 fits and their 15 default pairs (LEG_PLAN R15, already kept) and each fit's `fit.bin` (`hpm_S`); data.bin is rebuildable.
3. **Cost:** ≈ 0 core-h (a post-hoc read; seconds per fit on Owls). The only NOTS cost would be re-running fits whose `setup.bin` was not kept.
4. **Open questions for HQ/Theory:** exactly which S₀ (HPM, the truth, or both), and whether to emit π₀ at calibration time (a record field → changes sidecars, so NOT in this diff).
Recommendation: build the reader after the V-N PR is accepted, as its own small PR on top of the same freeze tag; do not couple it to V-N.
