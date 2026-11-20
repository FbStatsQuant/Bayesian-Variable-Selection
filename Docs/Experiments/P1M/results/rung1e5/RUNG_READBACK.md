OPTION D VERDICT: **D1 PASS, D2 PASS, D3 PASS: all three conditions met (HQ releases)** · RUNG: **CLEAN** (12 of 12 fits delivered, 0 soft / hard trips, all C2 and C3 pass, RG_T6 PASS: the resumed island is bit-identical to the uninterrupted reference)

# RUNG_READBACK: the 10⁵ rung read-back at (F2, N 10⁴, m 1, I_max 0) (Engineering, Sonnet worker; Fri 2026-11-20)

**Status: pending manager commit.** Exactly as RUNG_PLAN (exp/P1M a49be29f) declares; nothing post hoc. No NOTS access by this worker. Scratch `~/SMC_Engineering_Department/tmp/20261120-rungrb/`; outputs in `results/rung1e5/readback/` (sha256 §10). Records: `~/SMC_Engineering_Department/records/rung1e5/RG_{1a,1b,2a,2b,3a,3b,T6}/` (20 units, manager-verified) and `records/gb/{GB_G1a,GB_G2a}` (the two G-B pilots = rung fits 1–2); ledger `staging/rung1e5/prior_after_R3.json` (13 rows, **633.57**), `deploy_rung.log`, `monitor/R{1,2,3}`.

## 1. Summary for HQ (≤ 10 lines)
1. **Option D: D1 PASS** (HPM = S₀ in 5/5 AR fits at n 200 and 3/3 at n 400), **D2 PASS** (mean π̂(S₀) 0.349 at n 200 → 0.546 at n 400, difference **+0.197**, no tolerance; Welch 95 % [0.101, 0.293], cluster bootstrap [0.133, 0.262], reported not gating), **D3 PASS** (re-sized D = 317 after the floor, plan value 1,087; position 12.7–13.5k, ≤ 20.6k with the H-34 seeds and 23.9k at the worst case, of 28.3k). The release is HQ's.
2. **RG_T6 PASS, stated explicitly:** the resumed island is **bit-identical** to the uninterrupted reference: output_hash **0x4e4fd6a2e6135cfb** = the reference = the G-B pilot's own island 1; **11/11 checks** true; **26/26** non-meta sections equal (0 differing). Two real SIGKILLs by PID (second checkpoint generation; mid-write of `island.ckpt.a.tmp.2384528`), resumed from step 22. 10.12 core-h.
3. **Rung CLEAN:** 12 of 12 fits delivered (the G-C bar is ≥ 11), 633.57 core-h against the 824 quote (0.77×); no soft or hard trip, no failed stage; every fit meets M1 ≤ 0.05, M2 ≤ 0.005, evidence within 3 s.e., HPM certified; peak RSS ≤ 40 % of every request; HPM = S₀ (truth) in all 16 fits.
4. **Continuity twins (N 10⁴ vs N 2,500, same data and seeds):** HPM equal and = S₀; Δ log Ẑ −0.004 (−0.4 s.e.) AR, −0.037 (−1.5 s.e.) ADJ-OPP; π̂(S₀) 0.387 vs 0.385 and 0.340 vs 0.327; d_H between the two store laws **0.0010 and 0.0012** (0.014× and 0.009× the distance to the truth). The N effect on π̂(S₀) is small: no flag.
5. **Measured 10⁵ island factor f (N 10⁴ / N 2,500, billed islands, same data, seed, grid): 2.75 (AR), 2.65 (ADJ-OPP), mean 2.70**, not the 3.77 of the 10⁴ mini-leg. A 1M N 10⁴ fit re-sizes from 1,062 to ≈ 774 **if the 10⁵ factor holds at 1M (not measured there)**.
6. **Measured 10⁵ class costs (N 10⁴, I_max 0):** AR n200 **66.2** (n 5), AR n400 **43.1** (n 3), IND n200 **57.0** (n 2), ADJ-OPP n200 **67.8** (n 2); twins at N 2,500: 29.6 / 26.1. Cost follows the stage count T (7–30): islands ≈ 2.0 core-h per (T + 12), R² 0.89 over the 12 N 10⁴ fits.
7. **Envelope:** closed 2,984.56 + 633.57 = **3,618.13**. S2 with rep 1 = (a) (H-42): **12.7–13.5k** (45–48 %); with the 25 % reserve 15.0–16.0k; + the H-34 seeds (19 more, seed 1 = the rep-1 re-run) 18.8–19.5k; worst case 23.9k (84 %).

## 2. Verification of the registered material (task 1)
| item | check | result |
|---|---|---|
| `rung_readback.py` | sha256 | `2c8c883a5f911b7ed4a64def3c926e4ab734b428aea4afb64176497ee94a5aff` = RUNG_PLAN §9; `git diff HEAD` empty ✓ |
| `rung_d123.py` | sha256 | `d80545da6ed5f26b0db87839fc10780428df7c099f747dd577f3bfc645e1c036` ✓ |
| tests | `tests/test_rung_d123.py` (`96bd013a…`), `tests/test_rung_readback.py` (`f8578a61…`) | **7/7 and 4/4 pass** |
| registered G-B scripts | `gb_readback.py` `870a610a…` (continuity report), unedited | ✓ |
| plans deployed | `deploy_rung.log`: 7 COPYBIN lines, all F2 `da0cf85b5fe0…`; one logged **R2 RE-QUOTE** by the manager at the R1 gate (AR n200 4 × 76.4 + AR n400 2 × 46.7 ≈ 399 → quote 420, wave stop 840; the plan's re-quote rule, hard lines unchanged) | ✓ |
| identity | recorded arm (`calib_meta.json`): N 10⁴ / m 1 / I_max 0 for the 10 new fits and the 2 pilots; **N 2,500** / m 1 / I_max 0 for the twins; `rule` bounded, `I_used` 0; F2 sha in every eval; truth X / y sha256 equal inside each twin pair and equal to `staging/rung1e5/rung_refs.json` (AR r01 `2cdfff22…`, ADJ-OPP r01 `231001e2…`) | ✓ (`rung_readback.py`: C4 true in 16/16). The twins' **calibration equality** is checked on the sidecars only (`calib.bin` is not collected): `calib.bin.json` equal except `N_final` and the file hash, island T / L / Hm equal (T 30 / 30, 20 / 20); the RUNG_PLAN §1 section comparison is **not done** here |
| ledger | `prior_after_R3.json` 13 rows | **633.57** ✓ = R1 112.50 + R2 337.03 + R3 184.04 |
| one name collision, harmless | `records/rung1e5/RG_T6/5-AR-n200-r01-V-s1/` is the T6 task's record (no eval record), with the same run id as rung fit 1; both read-back scripts skip it (they require `eval.bin.json`) | named |

## 3. Option D: D1–D3 (adopted verbatim, GB_PLAN §6; H-40 (c)) (task 2)
Command: `python3 -I rung_d123.py --records ~/SMC_Engineering_Department/records/rung1e5 ~/SMC_Engineering_Department/records/gb --out d123` → `readback/rung_d123.json`. Fits that enter: AR-strong `5-AR-n200-r01 … r05-V-s1` (r01 = the G-B pilot) and `5-AR-n400-r01 … r03-V-s1`, each with recorded arm (N 10⁴, m 1, I_max 0); ADJ-OPP, IND, the I_max 3 twins and the continuity twins do **not** enter.
| fit | n | HPM = S₀ | π̂(S₀) = exp(F_S₀ − log Ẑ) | terminal occupancy of the top model |
|---|---|---|---|---|
| AR r01 (G-B pilot) | 200 | yes | 0.3865 | 0.3862 |
| AR r02 | 200 | yes | 0.2865 | 0.2866 |
| AR r03 | 200 | yes | 0.2744 | 0.2747 |
| AR r04 | 200 | yes | 0.4179 | 0.4216 |
| AR r05 | 200 | yes | 0.3774 | 0.3769 |
| **mean, n 200** | | **5 / 5** | **0.3486** | 0.3492 |
| AR n400 r01 | 400 | yes | 0.5511 | 0.5505 |
| AR n400 r02 | 400 | yes | 0.5877 | 0.5861 |
| AR n400 r03 | 400 | yes | 0.4981 | 0.4975 |
| **mean, n 400** | | **3 / 3** | **0.5456** | 0.5447 |
| criterion | rule | value | verdict |
|---|---|---|---|
| **D1** the theorem premise at 10⁵ | P̂(HPM = S₀) ≥ 4/5 at n 200 **and** 3/3 at n 400 | 5/5 and 3/3 | **PASS** |
| **D2** the expected trend | mean π̂(S₀) at n 400 ≥ mean at n 200: **a comparison of means, no tolerance** (5 against 3 datasets) | **+0.1971** (0.5456 − 0.3486) | **PASS** |
| D2 reported, **not gating** | (a) Welch 95 % t-interval (df 5.64); (b) percentile cluster bootstrap (datasets resampled within n level, 10,000 draws, seed 20261120) | (a) **[+0.1009, +0.2933]**; (b) **[+0.1328, +0.2616]** | both exclude 0 |
| **D3** budget | position + D ≤ 28.3k at the re-sized unit cost (§7): closed 3,618.13 + the S2 plan with **rep 1 = (a)** (22 frozen 1M fits at 317, ONE N 10⁴ fit, D, ablations + competitors 1,052) + the conditional 20 seeds | re-sized D = 317 × ρ^(log₂ 5), ρ = 43.08 / 66.18 = 0.651 → 117 → **floored at 317**; plan value 1,087. Position **12,730** (D re-sized) / **13,501** (D 1,087); + 25 % reserve 15,008 / 15,971; + H-34 18,750 / 19,520 (22,532 / 23,495 with the reserve); worst case (f 3.77, D 1,087, seeds, reserve) 23,855 | **PASS** (≤ 28,300 in every case) |
**Option-D verdict: all three conditions met.** Statements HQ should have next to the verdict: (i) D2 compares means with no tolerance; the margin is large here (+0.20) and both intervals exclude 0, but n 200 and n 400 are different datasets (5 against 3) and the intervals are wide in the stated way. (ii) The n 400 fits are **cheaper** than n 200 (43.1 against 66.2), so the pre-declared re-size gives D below the plan: the effect is **stage-count driven** (T 7–8 at n 400 against 12–30 at n 200), a property of these grids, and is **not extrapolated** to 1M; the floor and the plan value 1,087 are both shown, and D3 passes under both. (iii) The trend is measured at N 10⁴ and D runs at N 2,500; the continuity twins (§5) put the N effect on π̂(S₀) at +0.001 and +0.012 at n 200 (no flag); there is **no N 2,500 link at n 400** (stated in advance). (iv) π̂(S₀) at n 200 here (0.27–0.42, mean 0.35) is comparable to the expert's 0.3–0.45 draw (OWNER_SHEET: a p = 10⁶ draw, not a 10⁵ band).

## 4. RG_T6, the forced-kill restart test (task 3): stated EXPLICITLY
`records/rung1e5/RG_T6/5-AR-n200-r01-V-s1/t6.json` (source: the G-B pilot's own `data.bin`, `setup.bin`, `calib.bin` of `GB_G1a`; island 1; F2; 48 CPUs; `--ckpt-every-s 60`; kills 2). **The resumed island is bit-identical to the uninterrupted reference. Nothing differs.**
| item | result |
|---|---|
| **output_hash** (resumed island) | **0x4e4fd6a2e6135cfb** |
| output_hash (uninterrupted reference, same job) | **0x4e4fd6a2e6135cfb** (equal) |
| output_hash of the G-B pilot's own island 1 (`island_1.bin.json`, GB_G1a) = the pre-declared third reference | **0x4e4fd6a2e6135cfb** (equal) |
| `p1m_t6` checks | **11 / 11 true**: `reference_completed`, `kill_1_sigkill`, `kill_1_no_island_file`, `kill_2_sigkill`, `kill_2_no_island_file`, `final_completed`, `resumed`, `status_completed`, `output_hash_equal`, `ckpt_removed`, `sections_equal` |
| sections | **26 / 26** non-meta sections compared (`smcbvs4 info --meta 1` of both files), **0 differing**; `island_isa`, `output_hash`, `status` equal |
| kill 1 | SIGKILL by PID 2384362 **135.07 s** into the process, at the **second checkpoint generation** (`island.ckpt.a` and `.b` both present); return code **−9**; no island file |
| kill 2 | SIGKILL by PID 2384528 **74.35 s** into the **resumed** process, **during a checkpoint write** (`island.ckpt.a.tmp.2384528` present; the two complete generations survived); return code **−9**; no island file |
| final run | resumed **from step 22**, completed in 209.7 s wall (load 7.03 s, checkpoint writes 1.40 s); the checkpoints were removed; the reference took 338.4 s wall (island 328.4 s) |
| cost | **10.12 core-h** (sacct, 1 task), against the quote 11.4 and the class E 12 (soft 18, hard 30: not approached) |
**PASS** by the pre-declared rule (RUNG_PLAN §4: every `p1m_t6` check **and** resumed = reference = 0x4e4fd6a2e6135cfb). This is the G-C item "forced-kill restart at 10⁵" on the campaign engine at the rung configuration (F2, N 10⁴, I_max 0); T6 at N 2,500 on F2 was not repeated (stated in the plan).

## 5. Continuity twins: N 10⁴ vs N 2,500 at 10⁵ (task 4; descriptive, as pre-declared)
Twins `5-AR-n200-r01-VN25-s1` and `5-ADJOPP-n200-r01-VN25-s1` (N 2,500, I_max 0, same data and seeds as the G-B pilots). Registered `gb_readback.py` (`readback/gb_readback_continuity.json`), the cross-evaluator `smcbvs4_xeval` (b89cba4d, sha256 `afef0e46…`, as the 10⁴ leg's partition d_H; `cross --a <N 10⁴ law.bin> --b <N 2,500 law.bin> --truth … --data <pilot data.bin> --data-b <twin data.bin>`, X / y guard passed; `readback/cross/`).
| quantity | AR r01 | ADJ-OPP r01 |
|---|---|---|
| HPM equal; = S₀ | yes; yes ({10000, 30000, 50000, 70000, 90000}) | yes; yes ({10000, 10001, 50000, 70000, 90000}) |
| log Ẑ, N 10⁴ / N 2,500 | −233.2671 / −233.2636 | −244.1310 / −244.0941 |
| **Δ log Ẑ** (N 10⁴ − N 2,500), in combined island s.e. | **−0.0036 (−0.43 s.e.)** | **−0.0369 (−1.47 s.e.)** (twin σ̂ 0.090) |
| log Ẑ − log Z_T (N 10⁴ / N 2,500) | +0.208 / +0.211 | +0.233 / +0.270 |
| **π̂(S₀)** (N 10⁴ / N 2,500); difference | 0.3865 / 0.3852; **+0.0014** | 0.3397 / 0.3274; **+0.0123** |
| sup of null PIP_eq (N 10⁴ / N 2,500); min of active PIP_eq | 0.0166 / 0.0167; 0.99982 / 0.99982 | 0.0917 / 0.0915; 0.99375 / 0.99372 |
| max_j \|ΔPIP_eq\| | **not computed** (needs the `fit.bin` PIP reader; not available here) | not computed |
| M1 / M2 / M3, N 10⁴ | 0.007625 / 0.000272 / 0.01528 | 0.008355 / 0.000806 / 0.04509 |
| M1 / M2 / M3, N 2,500 | 0.01924 / 0.000553 / 0.02963 | 0.01532 / 0.001619 / 0.08998 |
| **r_N** = N 10⁴ / N 2,500 (M1, M2, M3) | **0.396 / 0.493 / 0.516** | **0.545 / 0.497 / 0.501** |
| the mini-leg's reference 1/√c_X at the **measured 10⁵ c_X** (= f) | f 2.747 → 0.603 | f 2.649 → 0.614 |
| **d_H between the two store laws** (xeval `cross`; h² ± s.e.; d_H = √h², the upward-biased point value) | h² 9.94 × 10⁻⁷ ± 1.08 × 10⁻⁷; **d_H 0.00100** | h² 1.49 × 10⁻⁶ ± 4.3 × 10⁻⁷; **d_H 0.00122** |
| d_H of each law to the truth (self-check; N 10⁴ / N 2,500) | 0.07402 / 0.07401 | 0.13305 / 0.13300 |
| ratio d_H(N 10⁴, N 2,500) / d_H(truth) | **0.0135** | **0.0092** |
| measured **island factor f** (billed islands, N 10⁴ pilot / N 2,500 twin; same data, seed, grid; T 30 / 20) | **2.747** (whole fit 2.58; max island wall 447 / 222 s) | **2.649** (whole fit 2.52; 396 / 156 s) |
| twin cost (quote 31.9 / 27.9) | 29.57 | 26.07 |
**Reading (descriptive, no threshold).** The two N settings give the same selection, the same posterior mass on S₀ (differences +0.001 and +0.012), log Ẑ within 1.5 island s.e., and store laws whose Hellinger distance is about 1 % of the distance to the truth (below the 10⁴ leg's H bar of 0.10 by 7× to 11×). The island sd of M1–M3 falls by a factor ≈ 0.4–0.55 at N 10⁴, i.e. at or below the 1/√c_X reference (0.60 / 0.61) in all six ratios: at 10⁵ N 10⁴ costs 2.7× the islands, not 3.77×, and the reference is met with room. The f here is **measured**; the ≈ 2.5 inferred in the G-B read-back from T5 is confirmed.

## 6. Science per fit (task 5)
Full table `readback/science_table.txt`; C1–C5 per fit `readback/rung_readback.md`. All fits R′ 16, F2, recorded arm as planned.
| fit | HPM = S₀ | π̂(S₀) | log Ẑ | σ̂ = sd(log Ẑ_r) | log Ẑ − log Z_T | M1 | M2 | evidence gap (≤ 3 s.e.) |
|---|---|---|---|---|---|---|---|---|
| AR n200 r01 (pilot) | yes | 0.3865 | −233.267 | 0.0153 | +0.208 | 0.00763 | 0.00027 | 0.0022 (0.0128) |
| AR n200 r02 | yes | 0.2865 | −196.284 | 0.0126 | +0.213 | 0.01107 | 0.00124 | 0.0054 (0.0126) |
| AR n200 r03 | yes | 0.2744 | −198.905 | 0.0137 | +0.217 | 0.00868 | 0.00091 | 0.0045 (0.0122) |
| AR n200 r04 | yes | 0.4179 | −218.514 | 0.0133 | +0.188 | 0.00859 | 0.00024 | 0.0049 (0.0119) |
| AR n200 r05 | yes | 0.3774 | −210.102 | 0.0122 | +0.185 | 0.00727 | 0.00053 | 0.0046 (0.0107) |
| AR n400 r01 | yes | 0.5511 | −350.769 | 0.0085 | +0.090 | 0.00647 | 0.000055 | 0.0017 (0.0080) |
| AR n400 r02 | yes | 0.5877 | −357.189 | 0.0068 | +0.082 | 0.00668 | 0.000055 | 0.0024 (0.0071) |
| AR n400 r03 | yes | 0.4981 | −364.309 | 0.0081 | +0.102 | 0.00814 | 0.00024 | 0.0018 (0.0086) |
| IND n200 r01 | yes | 0.4361 | −213.688 | 0.0092 | +0.184 | 0.00818 | 0.00030 | 0.0033 (0.0092) |
| IND n200 r02 | yes | 0.4162 | −207.425 | 0.0138 | +0.183 | 0.00966 | 0.00032 | 0.0024 (0.0126) |
| ADJ-OPP n200 r01 (pilot) | yes | 0.3397 | −244.131 | 0.0451 | +0.233 | 0.00836 | 0.00081 | 0.0044 (0.0344) |
| ADJ-OPP n200 r02 | yes | 0.3157 | −219.889 | 0.0194 | +0.221 | 0.00745 | 0.00114 | 0.0039 (0.0156) |
**C2 (§0-v2.3):** M1 ≤ 0.0111 (target 0.05), M2 ≤ 0.00124 (target 0.005; `target_met` true in every fit), the evidence gap is inside 3 s.e. in every fit (the tightest AR r02: 0.0054 of 0.0126), `local_certified` true, PIP agreement max_j \|PIP_eq − PIP_𝒯\| ≤ 0.020 against bounds 0.09–0.25, M3 ≤ 0.045 (goal 0.5): **PASS in 16 of 16** (the 12 fits above, the 2 I_max 3 G-B twins and the 2 continuity twins). **C5:** final E1–E3, `low_empirical_ESS`, `occ_inhomogeneous` False and sd(log Ẑ_r) > 1 False in all 16; `checks_passed_final` True; calibration E1 / E2 NOT EVALUATED at I_max 0, `grid_unconverged` True and `I_used` 0 (constants). **S₀:** HPM = S₀ and F(HPM) − F(S₀) ≈ 0 in all 16 fits, outcome class "correct". The sup of the null PIP_eq ranges 0.017–0.31 at n 200 (AR r02 0.31, r03 0.21, r04 0.05, r05 0.13, r01 0.017; ADJ-OPP 0.09 and 0.14; IND 0.03 and 0.04) and falls to 0.013–0.048 at n 400. log Ẑ − log Z_T is positive in every fit.

## 7. Cost (task 6): against the quote per wave and class; the measured class costs for the G-C / 1M plan
**Per wave (core-h):**
| wave | content | quote (stop) | measured | ratio |
|---|---|---|---|---|
| R1 | `RG_1a` AR n400 r01 46.74 + `RG_1b` twins 29.57 + 26.07 + `RG_T6` 10.12 | 150 (300) | **112.50** | 0.75 |
| R2 | `RG_2a` AR n200 r02–r05 254.53 + `RG_2b` AR n400 r02–r03 82.50 (manager's R1-gate re-quote 420, stop 840) | 460 (920) | **337.03** | 0.73 (0.80 of the re-quote) |
| R3 | `RG_3a` IND ×2 114.06 + `RG_3b` ADJ-OPP r02 69.97 | 220 (440) | **184.04** | 0.84 |
| **rung** | 10 fits + 2 twins + T6 | **824** (P90 ≈ 1.1k; HQ's 813 excl. T6) | **633.57** | **0.77** |
Cumulative stop 1,400 and the projection ceiling 1,326 (counting the two pilots' 142.04: 775.6 of 1,326) were not approached; **0 soft trips, 0 hard trips, no failed stage**; every fit within its class soft line (the largest ratio: ADJ-OPP r02 1.06× E 66).
**Measured 10⁵ class costs (core-h per fit; stage means; max task wall s):**
| class (N, I_max 0) | n fits | total mean [min–max] | model E (rung table) | setup | calibrate | islands | merge | eval | T | max wall cal / islands / merge |
|---|---|---|---|---|---|---|---|---|---|---|
| AR n200, N 10⁴ | 5 (incl. the pilot) | **66.18** [50.2–76.4] | 76 | 0.45 | 1.57 | 63.40 | 0.70 | 0.06 | 12–30 | 109 / 553 / 172 |
| AR n400, N 10⁴ | 3 | **43.08** [38.3–46.7] | 76 | 0.62 | 1.12 | 40.51 | 0.76 | 0.07 | 7–8 | 69 / 355 / 203 |
| IND n200, N 10⁴ | 2 | **57.03** [50.7–63.4] | 76 | 0.52 | 1.54 | 54.13 | 0.76 | 0.08 | 16 | 93 / 413 / 193 |
| ADJ-OPP n200, N 10⁴ | 2 (incl. the pilot) | **67.81** [65.7–70.0] | 66 | 0.48 | 1.53 | 64.99 | 0.74 | 0.07 | 20–22 | 102 / 433 / 195 |
| twin AR n200, **N 2,500** | 1 | **29.57** | 32 | 0.45 | 1.65 | 26.76 | 0.64 | 0.06 | 30 | 93 / 222 / 144 |
| twin ADJ-OPP n200, **N 2,500** | 1 | **26.07** | 28 | 0.49 | 1.24 | 23.56 | 0.72 | 0.05 | 20 | 70 / 156 / 163 |
| T6 task | 1 | **10.12** | 12 | | | | | | | wall 757 s total |
**What drives cost (for the 1M plan):** islands billed ≈ 1.64 × (T + 12) + 9.0 core-h at N 10⁴ (R² 0.89, 12 fits), i.e. about 2.0 core-h per stage unit, where T is the island stage count of the frozen preliminary grid; n 400 was cheaper than n 200 only because its grids were short (T 7–8). The I_max 0 calibration is 1.1–1.9 core-h per fit (2–3 % of a fit). **Measured island factor f (N 10⁴ / N 2,500) = 2.75 (AR), 2.65 (ADJ-OPP), mean 2.70** (§5): feed 2.7, not 3.77, to the 10⁵ N 10⁴ costs; a 1M N 10⁴ fit is ≈ **774** at f 2.70 (**not measured at 1M**) against 1,062 at f 3.77; the frozen 1M fit at N 2,500 stays 317 (437.44 − 135.63 + 14.96). **Memory:** merge process peak 2.06–2.11 GiB (IND 2.50) in every fit, sacct MaxRSS up to 7.27 GiB (page cache); calibrate ≤ 6.6 GiB, islands ≤ 3.7 GiB, eval ≤ 1.9 GiB; **max 40 % of any request** (calibrate 16 G, islands 12 G, merge 24 G, setup 16 G, eval 16 G). The G-C plan can use these.
**Envelope (closed 3,618.13 = 2,984.56 + 633.57; unit costs as above):**
| scenario | position | +25 % on the unspent items | share of 28.3k |
|---|---|---|---|
| S2 with rep 1 = (a) (22 frozen 1M fits + ONE N 10⁴ fit at f 2.70 + D 317 re-sized + comp 1,052) | **12,730** | 15,008 | 45 % / 53 % |
| same with D at the plan value 1,087 | 13,501 | 15,971 | 48 % / 56 % |
| + H-34, 19 more seeds (seed 1 = the rep-1 re-run), D re-sized | 18,750 | 22,532 | 66 % / 80 % |
| + H-34, D 1,087 | 19,520 | 23,495 | 69 % / 83 % |
| worst case (f 3.77, D 1,087, seeds, reserve) | | **23,855** | 84 % |

## 8. Rung CLEAN: the checklist (RUNG_PLAN §6)
| item | result |
|---|---|
| completion ≥ 11 of 12 rung fits (the two G-B pilots count) | **12 / 12** delivered, recorded arm = plan, one build |
| C1 per fit (class table; soft / hard) | 16 / 16 OK (the twins' G-B I_max 3 fits have no rung model); no trip |
| C2 per fit | 16 / 16 PASS (a miss would have been reported, never an estimator switch) |
| C3 peak RSS < request, 5 stages | 16 / 16 PASS (max 40 %) |
| C4 completion, F2 build | 16 / 16 |
| C5 flags | no final E1–E3 / E2 / low ESS / occ_inhomogeneous; calibration items as constants |
| T6 | PASS (§4) |
| stops (wave 2×, cumulative 1,400, projection 1,326, failures, identity) | none tripped; one logged re-quote (R2, 420) by the plan's own rule |
**CLEAN.** Deviations: none from the registered scripts or thresholds; the manager's R2 re-quote is inside the plan (hard lines unchanged).

## 9. Not done / limits
No NOTS access; no engine run; no change to any registered file; the twins' `calib.bin` section equality not checked (sidecars only); max_j \|ΔPIP_eq\| of the continuity pairs not computed (no `fit.bin` PIP reader here); the 1M island factor is not measured (a 1M N 10⁴ fit is an inference from f at 10⁵); n 400 and IND classes are 3 and 2 fits; the restart **chain** (Slurm `restart`) was not used or tested (T6 tests the checkpoint mechanism it relies on); T6 at N 2,500 on F2 was not repeated; the G-C plan (retention within the desktop cap, the frozen rep 1 as the G-C2 pilot, the parked harder arm) is a separate task.

## 10. Files, commands, sha256
`results/rung1e5/readback/` (not committed) and `tools/rung_readback_budget.py` + `_output.txt`. Commands: `python3 -I rung_d123.py --records records/rung1e5 records/gb --out d123`; `python3 -I rung_readback.py --records records/rung1e5 records/gb --cost-dir <the 16 per-run cost_5-*.json links, no cost_batch.json> --out rb --t6 records/rung1e5/RG_T6/5-AR-n200-r01-V-s1/t6.json` (expected hash default `0x4e4fd6a2e6135cfb`); `python3 -I ../gb/gb_readback.py --records … --cost-dir … --branch pass --out gbstyle`; `cross/run_cross.sh` (xeval, nice 19, 3 threads); `python3 -I tools/rung_readback_budget.py`.
| file | sha256 |
|---|---|
| `tools/rung_readback_budget.py` | `03ec294dc8c4cea6099bcf51240171f9d2289a9702fd06268649f96a1f7a6596` |
| `tools/rung_readback_budget_output.txt` | `434a71e96245c80ec745ec8b30def8388f6eea057415efdfcd1b3fe30e51a544` |
| `readback/rung_d123.json` | `3aa86fb219a09dcecc4e5d347985e0f1f94eb504dbaa7efe76fa775b2ede3ea6` |
| `readback/rung_readback.json` | `a7c7456adf1af7e93c5a95182515ebbdbc65e2316dbace9a10a7157cd80ce4cc` |
| `readback/rung_readback.md` | `8acdd1e274bc5d2137818b6941ffefe9982bf0f0f43a3686f7e3faba9222c77f` |
| `readback/gb_readback_continuity.json` | `5132d5830f4e5d096a3cc41d3169a54c6e8dc299d7293baf2c4bbf9cd64cc800` |
| `readback/stage_table.txt` | `dc08790b48b0dd8b2531f9f58a36022c032558a0c0f975cbe321adb7ea2b4393` |
| `readback/science_table.txt` | `94357a3791130a1d387ff56569209afc3604068d8b022c6e4b911af46cd1ff40` |
| `readback/cross/cross_AR.json` | `50183e2652472079f3933338a09dd2154c58cb909bf75bd5008b1afd0dab4727` |
| `readback/cross/cross_ADJOPP.json` | `eccb7a2a7bf04cd780c483f7f67d52703a186ad9f9472363ca9b6b29a3dcee06` |
| `readback/cross/run_cross.sh` | `04f14c345b28996d89df9b94493688568c22e350ccae9cb5759b9c4274cf73a5` |
## 11. Points for the Opus checker
1. **Re-derive D1 / D2** from the raw eval records: `selection.hpm_eq_S0` and π̂(S₀) = exp(`selection.F_S0` − `evidence.logZ`) for the 8 AR fits (r01 from `records/gb`), the two means, the difference +0.1971, the Welch df and interval, the bootstrap (seed 20261120, 10,000 draws); that no other fit entered; that the script run is the registered one (sha, tests 7/7).
2. **D3:** ρ = 43.08 / 66.18 (AR n400 mean over AR n200 mean, 3 and 5 fits), D = 317 × 5^(log₂ ρ) = 117 floored at 317; the position arithmetic against `tools/rung_readback_budget_output.txt`; that the S2 plan with rep 1 = (a) is 22 frozen fits (the re-run is one of them) and that H-34 adds 19 seeds; that the closed spend is 2,984.56 + 633.57 = 3,618.13.
3. **T6 explicitly:** `t6.json`: 11 checks, `sections` 26 / 0 differing, the three hashes, kill returncodes −9, the kill reasons ("second checkpoint generation"; "checkpoint write in progress (island.ckpt.a.tmp.2384528)"), `resumed_from_step` 22; the pilot's `island_1.bin.json` output_hash; the cost 10.12 from sacct.
4. **Continuity twins:** the pairing: `calib.bin` itself is not in the records (sidecars only), so the section-equality check of RUNG_PLAN §1 could not be made here; what was checked: `calib.bin.json` equal except `N_final` and the file hash (53 keys, 3 differ), island T, L and Hm equal in islands 1, 2 and 16 (T 30 / 30 AR, 20 / 20 ADJ-OPP); `init_hash` differs, as expected when N differs. A section comparison needs the NOTS copy of `calib.bin`; please judge whether this suffices, the f values from the island cost files, the xeval binary identity (`afef0e46…` = the 10⁴ leg's b89cba4d build) and that `--data` / `--data-b` were each fit's own data.bin of the same dataset (guard passed).
5. **Cost:** per-wave sums from the cost files against `prior_after_R3.json` (633.57); per-class means; the regression of islands on T is descriptive and post hoc (12 fits, one dataset per fit).
6. **The f = 2.70 → 774 inference for 1M** is not measured at 1M (read-back §7 says so); the G-C plan must not treat it as a quote.
7. **Name collision** of the T6 record dir with rung fit 1 (§2): confirm no script read the T6 dir as a fit.
8. **Not done:** §9.
