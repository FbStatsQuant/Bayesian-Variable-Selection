G-C2 PILOT VERDICT: **PASS** (C1 345.64 ≤ 489; C2 targets met; C3 memory on the process basis; C4 delivered; identity gate PASS; no kill-rule trip) · the frozen rep-1 re-run reproduces the 11-17 selection at a **21 % lower cost** (345.64 vs 437.44 core-h)

# GC_P_READBACK: the G-C2 pilot read-back, `6-AR-n200-r01-V-s1` at (F2, N 2,500, m 1, I_max 0) (Engineering, Sonnet worker; Fri 2026-11-20)

**Status: ready for Opus check; pending manager commit.** Exactly as GC_PREREG (§3 identity gate, §4 pilot criteria and kill rule, §5 class table) and GC_PLAN §2 declare; the registered scripts ran **unedited**. No NOTS access by this worker; the jobs were not touched. Scratch `~/SMC_Engineering_Department/tmp/20261120-gcprb/`; outputs in `results/gc1m/readback/` (sha256 §11). Inputs: `records/gc1m/GC_P/{6-AR-n200-r01-V-s1,_batch_GC_P}` (sha-verified by ops), `staging/gc1m/prior_after_P.json` (345.64), the batch `cost/` and `sacct_dump.txt`, the monitor's last probe `monitor/P/probe_20261120T173504Z.txt` (20/20 tasks COMPLETED, no flag), `OPS_GC.md`; the 11-17 reference `records/F1M_pilot/` (+ `records/fitbin_1117/` for its `fit.bin`).

## 1. Summary for HQ (≤ 10 lines)
1. **G-C2 pilot: PASS.** **C1** 345.64 core-h = 1.06× the model 326 (≤ 489; hard 815; quote 325; P90 ≈ 360 not exceeded). **C2** M1 0.01707 (≤ 0.05), M2 0.00312 (≤ 0.005), evidence gap 0.0153 inside 3 s.e. (0.0248), HPM certified, PIP agreement 0.0187 (≤ 0.2526). **C3** (process basis) merge process peak 20.9 GiB of 128 G, setup 13.2 of 48 G, every stage COMPLETED; sacct ≤ 59 % of any request. **C4** delivered, F2 `da0cf85b…`, arm (N 2,500, m 1, I_max 0, `I_used` 0, bounded).
2. **Identity gate: PASS** (`gc_identity.py`): X / y content hashes, generator, spec, S₀, β equal; setup counts equal (J 74,734, C 874,393,600, B 14); the pilot island's **state counters equal in 34 of 34 rows**; the five kernel-structure counters differ in 32 rows (rolling admission, by design) and the whole-file raw hash differs (both reported only); island stage count T = 27 (as expected). **Kill rules: none tripped** (calibrate 16.24 ≤ 48; the slowest island 1,097 s ≤ 1,584 s; the fit 345.64 ≤ 815).
3. **Science:** HPM = MPM = S₀ = {100000, 300000, 500000, 700000, 900000}, F(HPM) = F(S₀), outcome "correct"; **π̂(S₀) 0.3203**; the five true PIPs ≥ 0.99999982 (PIP_eq) / ≥ 0.99999989 (PIP_T); max null PIP **0.106** (eq) / **0.088** (T) at column 398,205; null PIPs above 0.5: 0 / 0 / 0, above 0.1: 1 / 0 / 1 (eq / T / Z). log Ẑ **−245.110**, log Ẑ_occ −245.095, log Z_T −245.388; σ̂ = sd(log Ẑ_r) **0.0283**; no E1–E3, no E2.
4. **The 1M I_max 3 / 0 pair (descriptive; one seed):** the same selection, log Ẑ within **0.3 combined island s.e.** (−245.1099 vs −245.1065), π̂(S₀) 0.3203 vs 0.3192, M1 / M2 / M3 0.01707 / 0.00312 / 0.0283 against 0.01710 / 0.00290 / 0.0323; cost 345.64 vs 437.44, the calibration 16.24 instead of 135.63 (saving 119.4).
5. **Islands came in dearer than the model:** 302.93 core-h (mean 18.93 per island, elapsed 584–1,097 s, mean 710 s) against 269.25 (16.8) in the 11-17 fit and the model: +12.5 %, cause not examined; the fit still lands at 1.06×. **Consequence for W1 (stated, not applied):** a class-mean re-fit from this one fit gives a unit ≈ 346, soft line 518 (hard 815 stays), a pair quote ≈ 691 (wave stop ≈ 1,380), W1 ≈ 705; the S2 block ≈ 10.6k instead of 10.1k (position 14.2k, 50 %).
6. **log Z_T gap (HQ asked):** log Ẑ − log Z_T = +0.278, i.e. the store holds e^{−0.278} ≈ **76 %** of the posterior mass; the 11-17 fit has +0.281; §7.
7. **Next steps (stated, not started):** option D on HQ's G-C2 ruling (alone, before W1); the 1M literal two-thread-count hash check (HQ H-45 (d), ≈ 20 core-h, report-only); W1 on the ruling.

## 2. Verification of the registered material
| item | check | result |
|---|---|---|
| `gc_identity.py` | sha256 | `6842354256c47a49…` = GC_PLAN §12 ✓ (run unedited) |
| `gc_readback.py` | sha256 | `63767ad3312ef580…` ✓ (run unedited) |
| tests | `tests/test_gc_identity.py` (`eb5c3f7d…`), `tests/test_gc_readback.py` (`c5ebaf07…`) | identity **8 / 8 OK**; readback **7 of 8 OK, 1 FAIL** (below) |
| **the one test failure, reported, not patched** | `test_real_11_17_record_parse` scans the whole `records/` root for run id `6-AR-n200-r01-V-s1`; **the pilot's record now has the same run id as the 11-17 record**, the scan picks the pilot, and the test's 11-17 constants (M1 0.0171029…) no longer match (it reads 0.0170710…, the pilot). Not a script defect; the readback script's own results below are unaffected (I ran it on `records/gc1m/GC_P` alone, and separately on `records/F1M_pilot`). A one-line fix in the test (point it at `records/F1M_pilot`) is the manager's call | named |
| plan / build | `GC_P.json` `20d81283…` = the committed plan; `deploy_gc.log` one COPYBIN, sha `da0cf85b…` (`OPS_GC.md`) | ✓ |
| records | one SHA256SUMS per unit, ops verified 2 units 0 failures; the read-back reads the eval / fit sidecars and `fit.bin` (section hashes verified by the reader) | ✓ |
| ledger | `prior_after_P.json` 345.64; my sum of the sacct dump: 12.320 + 16.240 + 302.933 + 13.920 + 0.222 = **345.635** | ✓ |
| one figure differs from the quick numbers | islands 302.93 (sacct dump and the cost file) against 303.04 in the brief; the total 345.64 agrees; the per-island mean is 18.93 (18.94 at 303.04) | named |

## 3. The G-C2 pilot verdict (GC_PREREG §4)
Command: `python3 -I gc_readback.py --records records/gc1m/GC_P --cost-dir <the one per-run cost file> --out readback --identity readback/gc_identity.json` → `readback/gc_readback.json`, `.md`: **"G-C2": "PASS"**.
| # | criterion | registered condition | measured | verdict |
|---|---|---|---|---|
| **C1** cost | ≤ 1.5× model; the Q4 guard 2.5× | billed ≤ **489** (E 326); STOP > **815** | **345.64** (ratio **1.060**) | **PASS** |
| **C2** M1 | ≤ 0.05 | `fit.meta.occ[M 1,000].sd_log_Z_occ_r` | **0.017071** (2.9× margin) | PASS |
| M2 | ≤ 0.005 (`target_met`) | `pip.island_spread.max_sd` | **0.003118** (62 % of the bar; `target_met` true) | PASS |
| evidence | \|log Ẑ − log Ẑ_occ\| ≤ 3√(se_Z² + se_occ²) | | **0.01532** ≤ **0.02479** (62 % of the bound) | PASS |
| HPM certified | `local_certified` | True, certified by both (the final local search and LS0) | PASS |
| PIP agreement | max_j \|PIP_eq − PIP_𝒯\| ≤ 0.01 + (1 − π̂(𝒯)) | **0.01869** ≤ **0.2526** (`eq_T_target_met` true) | PASS |
| reported, not gating | M3 = σ̂ = sd(log Ẑ_r) ≤ 0.5 (goal) | **0.02830**; robust 0.02570; R_eff / R′ 0.9992 | met |
| **C3** memory (process basis) | no OOM; merge `peak_rss_kb` < 128 G; setup peak < 48 G | merge process **20.88 GiB**, setup process **13.25 GiB**; all 5 stage groups COMPLETED; sacct at most **58.5 %** of any request (§5) | **PASS** |
| **C4** completion | delivered, F2, arm | 5 stage groups COMPLETED, `logZ_r` length 16 and finite, `binary.sha256` = `da0cf85b…`, recorded arm (2,500, 1, 0, `I_used` 0, bounded) | **PASS** |
| **identity** | §3 gate | I1 PASS, I2 PASS, I3 PASS (§3.1) | **PASS** |
| **kill rule** | K1 / K2 / K3 | calibrate 16.24 core-h, 609 s (K1 48 / 30 min); slowest island 1,097 s (K2 1,584 s); fit 345.64 (K3 815) | **no trip** |
**G-C2: PASS.** (Final flags: E1 / E2 / E3 False, `low_empirical_ESS` False, `occ_inhomogeneous` False, `checks_passed_final` True; calibration E1 / E2 NOT EVALUATED and `grid_unconverged` / `I_used` constants at I_max 0.) HPM vs S₀ is reported in §6 (HPM = S₀).
### 3.1 The identity gate (`gc_identity.py`, GC_PREREG §3) against the 11-17 fit
`python3 -I gc_identity.py --old records/F1M_pilot --new records/gc1m/GC_P/6-AR-n200-r01-V-s1 --out readback` → `readback/gc_identity.json`: **IDENTITY PASS**.
| check | result |
|---|---|
| **I1 data** | `X_sha256` `5174f8b3…`, `y_sha256` `9b0c866c…`, generator `smcbvs4.gen/1`, spec (AR, ρ 0.6, b 20, s₀ 5, a 1, σ 1, seed 602020001), S₀ {100000, 300000, 500000, 700000, 900000}, β (1, −0.8, 0.9, −0.7, 0.6), σ and the run params (design, signal, p, n, data_seed, seed, Rp) **equal**. Reported, not gated: the whole-file `raw_content_sha256` **differs** (`2e8550be…` vs `52c89267…`; it embeds the binary's provenance) |
| **I2 setup** | B 14, B_blocks 14, C 874,393,600, J 74,734, mode_size 2, n 200, p 10⁶, partition truncated, file_mode V: **equal** |
| **I3 pilot island** (`cost_pilot_t0_k0_r0.jsonl`) | header equal; **34 of 34 rows equal on the state counters** (M, mean_S, phi, sweeps, particle_rounds, store_size, store_mean_k, slow_supports, kind, step, segment): 0 differences |
| reported, not gated | kernel-structure counters differ in 32 rows (passes up to 45 %, act_cols up to 4.9 %, pairs and supports up to 1.9 %: the rolling-admission kernel, by design); accounting counters differ in 32 rows (flips ≤ 1.3 %, offers ≤ 6.6 %, duplicates dropped ≤ 28 % of a small number; merges 0 rows) |
| I4 (reported) | new final-island T = **27** (expected 27); arms I_max 3 → 0, `I_used` 0, N 2,500; binaries `2197fd5b…` → `da0cf85b…` |
Same data, setup and pilot-island trajectory as the 11-17 fit at 1M; the final-island stage runs on a different grid (rebuild_3 vs the preliminary one) and build, as GC_PLAN §2.3 states.

## 4. Stage costs and walls against the model; the class-mean re-fit consequence
| stage | model E | **measured billed** | elapsed (max task) | 11-17 fit (I_max 3, `2cfaa9e5`) billed / elapsed | note |
|---|---|---|---|---|---|
| setup (48 CPU) | 15.25 | **12.32** | 924 s (15.4 min) | 15.25 / 1,144 s | below the model |
| calibrate (96 CPU) | **24** | **16.24** | 609 s (10.2 min) | 135.63 / 5,086 s | the I_max 0 saving **119.4** (the 11-17 12 diagnostic islands are gone); below the 24 model and the 12–15 min expectation; K1 line 48 |
| islands (16 × 96 CPU) | 269.25 (16.8 per island) | **302.93** (18.93 per island) | min **584** / mean **710** / max **1,097** s | 269.25 / 526–792 s | **+12.5 %**; 16 of 16 COMPLETED; the one slowest island 29.25 core-h (1.74× the model per island, below K2) |
| merge (32 CPU) | 17 | **13.92** | 1,566 s (26.1 min) | 16.91 / 1,902 s | below |
| eval (8 CPU) | 0.4 | **0.22** | 100 s | 0.40 / 181 s | below |
| **fit** | **326** | **345.64** | submit → eval 79 min (queue included) | 437.44 / 3 h 04 min | ratio 1.060; **−91.8 core-h (−21 %)** against the 11-17 fit |
**Reading.** Every stage except the islands is below its model; the islands cost 12.5 % more than the 11-17 islands (mean elapsed 710 s against ≈ 630 s) with the same stage count T = 27, so the extra is per-step cost or node mix, **not examined here** (the elapsed range 584–1,097 s is wider than the 11-17 526–792 s; K2's 1,584 s was not approached). The fit is inside the committed lines (soft 489, hard 815) and P90 360.
**Class-mean re-fit consequence for W1 (STATED, NOT APPLIED; GC_PREREG §5: a re-fit moves the soft line and the next quote only, never the hard line).** From this one fit: unit ≈ **346** (× 1.060 of the model), ADJ-OPP ≈ 359; soft line 1.5 × 346 = **518** (the hard line stays 815); the next pair ≈ **691** (wave stop 2× ≈ 1,380 instead of 650 / 1,300), W1 (AR r02 + ADJ-OPP r01) ≈ **705** (1,410 instead of 665 / 1,330); the N 10⁴ fit ≈ 860 (islands 302.93 × 2.70 + 42.7; 783 in the plan); option D unchanged at 1,087. Envelope (`readback/refit_sensitivity.txt`): S2 block ≈ **10,617** against 10,107, position **14,235** (50.3 %), 16,889 with the 25 % reserve (59.7 %); with the seeds 20,802 (73.5 %), 25,098 (88.7 %) with the reserve: all ≤ 28,300. Whether to re-fit after one fit or after W1 (the plan says after the pilot and W1) is the manager's call.

## 5. Memory on the process basis (GC_PREREG §4 C3)
| stage (request) | **process peak** (where recorded) | sacct MaxRSS (includes page cache) | % of request (sacct) | plan / 11-17 |
|---|---|---|---|---|
| setup (48 G) | **13.25 GiB** (`setup.bin.json` `peak_rss_mb`) | 22.63 GiB | 47 % | 13.5 GB process, 23.7 sacct (P7) |
| calibrate (128 G) | not recorded | 48.50 GiB | 38 % | pilot island peaked 48.7 GB (P7); no diagnostic islands |
| islands (64 G) | not recorded | 37.47 GiB | 58.5 % | plan 33.8 GiB; 11-17 measured 26–27 GB (sacct now adds mapped input pages) |
| merge (128 G) | **20.88 GiB** (`fit.bin.json` `peak_rss_kb`) | 68.37 GiB | 53 % | MERGE_MEM plan 26.2 GiB (the process is **0.80×** the plan); 11-17 sacct 75.1 GiB at an 80 G request |
| eval (16 G) | not recorded | 3.54 GiB | 22 % | |
**Verdict: PASS.** No OOM; both recorded process peaks are well below their requests. The merge **process** peak, 20.88 GiB, is the number MERGE_MEM said would set the later merge request: **the 128 G request has 6× headroom, and the 48 G fallback (90 % budget 43.2 GiB) would hold 2.07× the measured peak**; whether the later fits (and option D, plan 58.0 GiB) move to 48 G / 64 G is the manager's call, not applied here. sacct counts page cache (68.4 GiB at the merge for a 20.9 GiB process).

## 6. Science
**Selection (all from `eval.bin.json` and `fit.bin`, section hashes verified by the registered reader `compare_overlap_v2.read_sections`; `readback/pip_pilot.json`):**
| quantity | pilot (F2, I_max 0) | 11-17 fit (I_max 3) |
|---|---|---|
| HPM | {100000, 300000, 500000, 700000, 900000} = S₀ | the same |
| MPM | = S₀ | = S₀ |
| F(HPM) − F(S₀); S₀ store rank; outcome class | 0; 0; "correct" | 0; 0; "correct" |
| **π̂(S₀)** = exp(F_S₀ − log Ẑ) (terminal occupancy of the top model) | **0.3203** (0.3174) | 0.3192 (0.3174) |
| store-renormalised exp(F_S₀ − log Z_T) | 0.4229 | 0.4229 |
**The five true PIPs (PIP_eq = the primary equal-weight RB PIP; PIP_T = the store-renormalised one, unclipped):**
| j (original column) | PIP_eq | 1 − PIP_eq | PIP_T |
|---|---|---|---|
| 100000 | 0.9999999999999987 | 1.3 × 10⁻¹⁵ | 1.0000000000000109 |
| 300000 | 0.9999999997997181 | 2.0 × 10⁻¹⁰ | 1.0000000000000109 |
| 500000 | 0.9999999999851821 | 1.5 × 10⁻¹¹ | 1.0000000000000109 |
| 700000 | 0.9999999993223183 | 6.8 × 10⁻¹⁰ | 0.9999999975746624 |
| 900000 | 0.9999998224317759 | 1.8 × 10⁻⁷ | 0.9999998862095665 |
| **min over the true variables** | **0.99999982** | | **0.99999989** |
**Null variables (the 999,995 columns outside S₀):**
| estimator | max null PIP (column) | null PIPs > 0.5 | null PIPs > 0.1 | Σ PIP | Brier |
|---|---|---|---|---|---|
| PIP_eq | **0.10640** (398,205) | 0 | **1** | 6.3729 | 1.68 × 10⁻⁸ |
| PIP_T | **0.08771** (398,205) | 0 | 0 | 5.7833 | 1.10 × 10⁻⁸ |
| PIP_Z (island-weighted) | 0.10639 (398,205) | 0 | 1 | | 1.68 × 10⁻⁸ |
The 11-17 fit: PIP_eq max null 0.10652 (398,205), PIP_T 0.08773, the same counts (0 / 0 / 0 above 0.5; 1 / 0 / 1 above 0.1); true PIPs equal to 9 digits where listed. The single null column 398,205 is the same in both fits (a near-neighbour candidate of S₀ that holds ≈ 10 % of the mass).
**Evidence and precision:** log Ẑ **−245.1099**; log Ẑ_occ (M = 1,000) −245.0946; log Z_T −245.3878; σ̂ = sd(log Ẑ_r) **0.02830** (robust 0.02570), max − median 0.0579, max weight 0.0662, R_eff / R′ 0.9992; M1 0.017071, M2 0.003118, M3 = σ̂. Predictive: plug-in h² of the HPM = MPM = the oracle's 0.0052197; the store-law predictive h² 0.0059988 (1.037× the oracle's); store size 40,000,001, omitted law mass 0.102.

## 7. The log Z_T gap (HQ asked)
**What Z_T is:** the deterministic **store-sum lower bound** of the same fit: Z_T = Σ over the models held in the top store (here 40,000,001, the cap 40p + 1) of e^{F(model)}, so log Z_T ≤ log Z always (no estimator noise). **The gap:** log Ẑ − log Z_T = **+0.2779**, i.e. Z_T / Ẑ = π̂(𝒯) = e^{−0.278} = **0.757**: the store holds about **76 %** of the posterior mass (the SMC estimate Ẑ), the rest, ≈ 24 %, sits in models outside the top 40 M. Against log Ẑ_occ (the top-M occupancy evidence) the gap is +0.293 (74.6 %). **Not a discrepancy and not a defect:** it is a lower bound by construction. **Comparison:** the 11-17 fit has +0.2812 (75.5 %); at 10⁵ the gaps are +0.185 to +0.233 at n 200 (AR r01 +0.208; ADJ-OPP +0.233 and +0.221; IND +0.184 and +0.183) and +0.082 to +0.102 at n 400 (the store holds ≈ 82–83 % at n 200 and ≈ 90–92 % at n 400): the unstored mass grows with p at fixed n = 200 (the posterior spreads over more near-S₀ models) and shrinks with n. **Where it matters:** C2 does **not** use log Z_T: the evidence criterion is |log Ẑ − log Ẑ_occ| ≤ 3 s.e. (0.0153 of 0.0248), and the PIP agreement bound already allows for it: max_j |PIP_eq − PIP_T| ≤ 0.01 + (1 − π̂(𝒯)) = 0.2526 (measured 0.0187). It is visible in the PIPs: PIP_T, normalised over the stored models only, gives a smaller null maximum (0.088) and a smaller Σ PIP (5.78 against 6.37) than PIP_eq (0.106, 6.37).

## 8. The 1M I_max 3 / 0 pair against the 11-17 fit (descriptive; GC_PLAN §2.3 wording)
**Same data, seed, setup and calibration-pilot trajectory (the identity gate); differing in the final-island grid (rebuild_3 vs the preliminary one) and in the build (`2cfaa9e5` vs F2). One seed, one dataset: a grid contrast, not a validation of the I_max rule at 1M.**
| quantity | 11-17 (I_max 3) | pilot (I_max 0) | difference |
|---|---|---|---|
| HPM / MPM = S₀ | yes / yes | yes / yes | identical |
| log Ẑ | −245.1065 | −245.1099 | −0.0034 = **−0.32** combined island s.e. (σ̂ 0.0323 and 0.0283, R′ 16) |
| log Ẑ_occ (M 1,000); log Z_T | −245.0945; −245.3877 | −245.0946; −245.3878 | −0.0001; −0.0001 |
| log Ẑ − log Z_T | +0.2812 | +0.2779 | −0.0033 |
| π̂(S₀) | 0.3192 | 0.3203 | +0.0011 |
| M1 / M2 / M3 (σ̂) | 0.017103 / 0.002905 / 0.03232 | 0.017071 / 0.003118 / 0.02830 | ratios I_max 0 / I_max 3: 0.998 / 1.073 / 0.876 |
| R_eff / R′; max − median log Ẑ_r | 0.9990; 0.0476 | 0.9992; 0.0579 | |
| max null PIP_eq / PIP_T | 0.10652 / 0.08773 | 0.10640 / 0.08771 | |
| final flags | none | none | |
| island stage count T | 27 | 27 | equal |
| **cost (core-h)**: setup / calibrate / islands / merge / eval / **total** | 15.25 / 135.63 / 269.25 / 16.91 / 0.40 / **437.44** | 12.32 / 16.24 / 302.93 / 13.92 / 0.22 / **345.64** | calibration −119.4; islands +33.7; **total −91.8 (−21 %)** |
| wall (queue excluded) | 3 h 04 min | ≈ 79 min submit → eval end (queue included) | |
| merge memory | sacct 75.1 GiB at an 80 G request (process not recorded) | process 20.9 GiB (sacct 68.4 GiB at 128 G) | |
The three I_max 0 / I_max 3 ratios (0.998, 1.073, 0.876) are inside the registered rule's bars (1.15 / 1.30) **as a description of this one pair**, the same picture as the 10⁴ and 10⁵ pairs (low power; no new decision rests on it).

## 9. Next steps (stated, not started)
1. **HQ's G-C2 ruling** on this read-back (after the Opus check). On a PASS it releases W1 and starts **option D** (released by H-44; alone, before W1; the sizes-only plan gate is done; D's requests: setup 64 G, eval 32 G; quote ≈ 1,087, kept until measured).
2. **The 1M literal two-thread-count hash check (HQ H-45 (d)):** one pilot island re-run at a second thread count (48 against the pilot's 96) compared bit for bit, ≈ 20 core-h, report-only, any time after the pilot; needs the pilot's `data.bin`, `setup.bin` and `calib.bin`, which are on the desktop path (pilot exception: islands and `calib.bin` kept until the block read-back). Output hash to compare: the pilot's `island_1.bin.json`.
3. **W1** (AR r02 + ADJ-OPP r01; committed quote 665, stop 1,330; the §4 re-fit is the manager's call) on the ruling; the `gc_seeds.py` registration after W2's read-back, its sha frozen before any seed-block fit is submitted (H-45 (b)).

## 10. Not done / limits
No NOTS access; no engine run; no change to any registered file or threshold; the per-island HPM ("same best model in 16 of 16 islands") is not computable; the cause of the 12.5 % island excess is not examined; the one failing readback test is named (§2) and not patched; the per-variable PIP read used a one-off descriptive script `readback/pip_read.py` (it imports the registered reader unedited; not registered; its sha is in §11); one dataset, one seed.

## 11. Files, commands, sha256
`results/gc1m/readback/` (not committed): `gc_identity.json`, `gc_identity_stdout.txt`, `gc_readback.json`, `gc_readback.md`, `gc_readback_stdout.txt`, `pip_read.py`, `pip_pilot.json`, `pip_old.json`, `refit_sensitivity.txt`.
| file | sha256 (first 16) |
|---|---|
| `gc_identity.json` | `6a1211f4559f181e…` |
| `gc_identity_stdout.txt` | `840286d743f1b44d…` |
| `gc_readback.json` | `172680f75e9966ff…` |
| `gc_readback.md` | `4ee1a01e8bf95bc8…` |
| `gc_readback_stdout.txt` | `34a3caa68362e4e1…` |
| `pip_read.py` | `0a93d61a827d580b…` |
| `pip_pilot.json` | `bf4387a3403d6d7c…` |
| `pip_old.json` | `c3602d1b57a6dd7b…` |
| `refit_sensitivity.txt` | `9b66d789c42d5b4e…` |
Commands: `python3 -I gc_identity.py --old ~/SMC_Engineering_Department/records/F1M_pilot --new ~/SMC_Engineering_Department/records/gc1m/GC_P/6-AR-n200-r01-V-s1 --out readback`; `python3 -I gc_readback.py --records ~/SMC_Engineering_Department/records/gc1m/GC_P --cost-dir <the per-run cost link> --out readback --identity readback/gc_identity.json`; `python3 -I readback/pip_read.py <fit.bin> <truth.json> <out.json>` (the 11-17 `fit.bin` is `records/fitbin_1117/F1M_pilot_6-AR-n200-r01-V-s1.fit.bin`).

## 12. Points for the Opus checker
1. **Re-derive the verdict** from the raw records: C1 345.64 against the committed lines (326 / 489 / 815) and the sacct dump (the five stage sums); C2 from `eval.bin.json` (M1, M2, the evidence gap and bound, `local_certified`, `eq_T_target_met`); C3 on the process basis (`peak_rss_kb`, `peak_rss_mb`, the COMPLETED states); C4; the kill rules (K1 calibrate 16.24, K2 slowest island 1,097 s, K3).
2. **The identity gate:** re-run `gc_identity.py` against `records/F1M_pilot`; check the three gated groups and that the kernel counters (32 rows) and the raw hash differ as expected; check T = 27.
3. **The brief's islands figure** (303.04) against 302.93 here (sacct dump, cost file): the per-island mean 18.93 and the +12.5 % over the model; whether the excess merits a look before W1.
4. **The PIP table:** the original-column mapping (`orig` section, 1-based; the 11-17 `fit.bin` has no `orig` and keeps all columns: I first read it 0-based and corrected it), the section hashes verified, the null maximum at column 398,205 for both fits.
5. **§7 (the Z_T gap):** that Z_T is the store-sum bound (π̂(𝒯) = 0.7574 in `store.pi_T_hat`), the 10⁵ gap figures (RUNG_READBACK §6, G-B), and the statement that no criterion uses log Z_T.
6. **The class-mean re-fit** (§4) is arithmetic only and not applied; the re-fit timing (after the pilot vs after W1) is the manager's call.
7. **The failing test** (§2): name collision of the run id; confirm the script's results are unaffected.
8. **Not done:** §10.
