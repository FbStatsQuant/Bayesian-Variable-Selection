I_max OUTCOME: **PASS** (the registered rule on both pairs; I_max 0 stands, 10⁵ and 1M at I_max 0, N 10⁴, S2) · G-B VERDICT: **PASS** (C1–C4 pass, C6 PASS; 4/4 fits, 297.65 core-h against the 501 quote, 0 trips)

# GB_READBACK: the G-B pilot set read-back (Engineering, Sonnet worker; Fri 2026-11-20)

**Status: final; Opus-checked (`reviews/GB_CHECK_OPUS.md`: CONFIRMED-WITH-FIXES; F1–F5 applied here, reporting only: no verdict, consequence or total changes); ready for manager commit.** Exactly as GB_PREREG (exp/P1M 26ef4abc) declares; nothing post hoc. No NOTS access by this worker. Scratch `~/SMC_Engineering_Department/tmp/20261120-gbrb/`; outputs in `results/gb/readback/` (sha256 §9). Records: `~/SMC_Engineering_Department/records/gb/{GB_G1a,GB_G1b,GB_G2a,GB_G2b}/` (4 units, `sha256sum -c` OK: 77 / 89 / 77 / 89 files), ledger `staging/gb/prior_after_G2.json`, monitor `staging/gb/monitor/G{1,2}/`.

## 1. Summary for HQ (≤ 10 lines)
1. **I_max rule: PASS** (`gb_imax_rule.py`, 2 datasets × 1 replicate, N 10⁴): geometric mean r = **1.0066 / 0.9272 / 0.9038** (M1 / M2 / M3) against 1.15; per dataset 0.89–1.01 against 1.30; HPM identical in both pairs. **Consequence (H-30, H-38): the 10⁵ rung and the 1M fits run at I_max 0, N 10⁴ rung / S2.**
2. **Low power, restated:** the two pairs detect only a GROSS I_max failure (P(pass) 0.93 / 0.55 / 0.07 at true ratio 1.00 / 1.13 / 1.30; HQ noted this in H-39). A PASS shows no gross failure at 10⁵ on AR-strong and ADJ-OPP; it does not show non-inferiority within 15 %.
3. **G-B: PASS.** C1 cost 76.4 (AR pilot, model 108, 0.71×) and 65.7 (ADJ-OPP pilot, model 133, 0.49×), no soft or hard trip. C2 precision: M1 0.0076 / 0.0084 (≤ 0.05), M2 0.00027 / 0.00081 (≤ 0.005), evidence gap 0.0022 / 0.0044 inside 3 s.e. (0.0128 / 0.0344), HPM certified. C3 memory: sacct peak RSS ≤ 36 % of every request (pilots; ≤ 41 % for the twins); the merge process itself peaked at 2.06 GiB (0.49× the plan). C4 all four fits delivered, one build F2.
4. **Science:** HPM = S₀ in all four fits (AR r01 = T5's {10000, 30000, 50000, 70000, 90000}); π̂(S₀) 0.387 (AR) and 0.340 (ADJ-OPP), comparable to the expert's 0.3–0.45 draw (OWNER_SHEET; a p = 10⁶ draw, not a 10⁵ band); log Ẑ V vs twin differs by 0.7 and 0.3 island s.e.; log Ẑ = −233.267, as T5 (−233.27).
5. **The island cost factor at 10⁵ is ≈ 2.5, not 3.77:** islands 71.1 core-h at N 10⁴ against T5's 28.1 at N 2,500 (same data, seed, I_max 3, T 30). The quote (islands 105.9) was conservative; the fits cost 59 % of it. The 11-18 freeze check (one 10⁵ island on F with T5's inputs: output bit-identical to T5's, 1.51 core-h, 1:53, inside T5's 112–153 s) and F2 = F at default N (VN_ID_1) put the N 2,500 island at ≈ 1.5–1.76, so **f ∈ ≈ [2.5, 2.9]** (an inference); the continuity twins measure it directly.
6. **Rung quote at (N 10⁴, I_max 0):** 12 fits ≈ **895**, the remaining 10 after the two pilots ≈ **753** (P90 ≈ 1.1k), against the 1,360 / 1,119 quote; continuity twins ≈ **60**. **Envelope:** closed 2,686.91 + 297.65 = **2,984.56** of 28,300.
7. **For HQ's ruling at G-B:** option D wording D1–D3 verbatim, with the D2 no-tolerance note (§7), 1M rep-1 options (a) / (b) / (c) with the recommendation (b) and its pairing dependency on H-34 (§7), the envelope table (§7). All four fits are I_max 0 / I_max 3 pairs at the same T (30 / 30 and 20 / 20); the calibration saving of I_max 0 is 9.5 (AR) and 6.6 (ADJ-OPP) core-h per 10⁵ fit.

## 2. Verification of the registered material (task 1)
| item | check | result |
|---|---|---|
| `gb_imax_rule.py` | sha256 | `76927ae2faadc095e9353050eae3ef626ad439d88b92a7bf7cb9f313dab91012` = GB_PREREG §1; `git diff HEAD` empty ✓ |
| `gb_readback.py` | sha256 | `870a610adb8663c02d431126ae14bfc63f5ea256093ea2ab2e1699a23d6d1589` = GB_PLAN §2.5; unchanged ✓ |
| tests | `tests/test_gb_imax_rule.py` (`7c85ebfa…`), `tests/test_gb_readback.py` (`b131ca93…`) | **7/7 and 7/7 pass** (the rule's golden on the leg's real FZ records included) |
| plans deployed | `staging/gb/plans/GB_G*.json` sha256 | `51af3e68…`, `b5d8438b…`, `98c7d2e8…`, `5d4b9e30…` = GB_PLAN §2.5 ✓; four `COPYBIN` lines in `deploy_gb.log`, all `da0cf85b…` (the one F2 build) |
| records | `sha256sum -c SHA256SUMS` in each unit | 4/4 OK |
| identity | recorded arm (`calib_meta.json`) = plan; `binary.sha256` = F2 in every eval; X / y sha256 equal inside each pair | AR: N 10⁴, m 1, I_max 0 / 3, `I_used` 0 / 3, rule bounded; ADJ-OPP likewise; truth `X_sha256` AR `2cdfff22…`, ADJ-OPP `231001e2…` in both fits of the pair ✓ |
| ledger | sum of `prior_after_G2.json` | 76.39 + 83.11 + 65.65 + 72.50 = **297.65** ✓ |
| stops | monitor G1 / G2, cost vs the committed table | 0 soft trips, 0 hard trips, no failed stage (all 80 tasks COMPLETED) |

## 3. The registered I_max rule on the two pairs (task 2)
Commands: `python3 -I gb_imax_rule.py --records ~/SMC_Engineering_Department/records/gb --N 10000 --out rule` → `readback/gb_imax.json`, `readback/rule_stdout.txt`. Form: **2 datasets × 1 replicate, the registered two bars**.
| metric | AR r01 (I_max 0 / 3) | ADJ-OPP r01 (I_max 0 / 3) | r per dataset AR / ADJ-OPP | **geometric mean r** | ≤ 1.15 | each ≤ 1.30 |
|---|---|---|---|---|---|---|
| M1 `sd_log_Z_occ_r` (M = 1,000) | 0.007625 / 0.007616 | 0.008355 / 0.008255 | 1.0011 / 1.0120 | **1.0066** | yes | yes |
| M2 `max_sd` of PIP over islands | 0.000272 / 0.000283 | 0.000806 / 0.000902 | 0.9624 / 0.8933 | **0.9272** | yes | yes |
| M3 `sigma_hat` = sd(log Ẑ_r) | 0.015278 / 0.016664 | 0.045090 / 0.050605 | 0.9168 / 0.8910 | **0.9038** | yes | yes |
| HPM identical in both fits | yes ({10000, 30000, 50000, 70000, 90000}) | yes ({10000, 10001, 50000, 70000, 90000}) | | | **yes** | |
**Outcome (as computed): PASS.** Pre-declared consequence (GB_PREREG §2, §4): **PASS → the 10⁵ rung and the 1M fits run at I_max 0; rung at N 10⁴; 1M replicates at N 2,500 + ONE N 10⁴ fit; the 10⁴ science stands.** FAIL would have meant I_max 3 AND N 2,500 (not triggered).
**What it can and cannot say (GB_PREREG §3, restated).** The two pairs detect only a gross I_max failure: HPM differing, an M3 ratio far above 1.15 in either dataset, M1 / M2 leaving ≈ 1, a grid-construction failure, a final E2. None occurred: `grid_fallback` empty, `grid_unconverged` True in all four (bounded stop, I_used = I_max in the twins; H-30 (3)), no final E1–E3, no E2, R_eff/R′ ≥ 0.997, island T equal between arms (30 / 30 AR, 20 / 20 ADJ-OPP). Under the registered model (ln r₃ ~ N(ln ρ, 0.123²), N 2,500 noise) P(pass) is 0.93 / 0.55 / 0.07 at ρ = 1.00 / 1.13 / 1.30, so a PASS is weak evidence of non-inferiority within 15 %; two designs (AR-strong, ADJ-OPP) are covered, not AR-weak or IND; the noise at N 10⁴ is unknown. *(Descriptive, under that same model, not a decision input: the observed M3 geometric mean 0.904 sits about 2.8 s.d. below the 1.15 bar; the model is assumed, not shown at 10⁵.)* As at 10⁴, the arms are close: M1 ≈ 1.00–1.01; M2 and M3 are 4–11 % **lower** at I_max 0.

## 4. G-B criteria on the pilots (I_max 0 fits; the rule selected I_max 0) (task 3)
`gb_readback.py --records records/gb --cost-dir <the 4 per-run cost files> --rule rule/gb_imax.json --branch pass` → `readback/gb_readback.json`, `gb_readback.md`: **G-B PASS; C6 PASS.**
| # | criterion (GB_PREREG §5) | AR pilot `5-AR-n200-r01-V-s1` | ADJ-OPP pilot `5-ADJOPP-n200-r01-V-s1` | verdict |
|---|---|---|---|---|
| **C1 cost** ≤ 1.5× the committed model, guard 2.5× | 76.39 core-h; E 108; **0.71×** (soft 162, hard 270) | 65.65; E 133; **0.49×** (soft 200, hard 333) | **PASS** (class of one fit: the 2.5× guard is the STOP line, not approached). Twins informational: 83.11 (E 118, 0.70×), 72.50 (E 142, 0.51×) |
| **C2** M1 ≤ 0.05 | 0.007625 | 0.008355 | PASS (6.6× / 6.0× margin) |
| M2 ≤ 0.005 (`target_met`) | 0.000272 (True) | 0.000806 (True) | PASS (18× / 6.2×) |
| evidence within 3 s.e. | \|log Ẑ − log Ẑ_occ\| 0.0022 ≤ 0.0128 | 0.0044 ≤ 0.0344 | PASS |
| HPM certified (`local_certified`) | True (by both) | True | PASS |
| PIP agreement | max\|PIP_eq − PIP_𝒯\| 0.0028 ≤ 0.198 (`eq_T_target_met` True) | 0.0128 ≤ 0.218 (True) | PASS |
| reported, not gating: M3 ≤ 0.5 | 0.0153 | 0.0451 | met; `occ_inhomogeneous` False; E1–E3 False; sd(log Ẑ_r) > 1 False; `checks_passed_final` True |
| **C3 memory** MaxRSS < request, every stage | max 35.9 % (calibrate 5.74 of 16 GiB) | max 34.7 % (calibrate 5.55 of 16 GiB) | **PASS** (table below) |
| **C4 completion** | delivered, F2 `da0cf85b…`, arm identity, `logZ_r` length 16 | same | PASS |
| **C5 E2 recorded** | final-merge E1 / E2 / E3 all False; calibration E1 / E2 **NOT EVALUATED at I_max 0**; `grid_unconverged` True, `I_used` 0 (constants) | same | recorded |
| **C6 rule** | PASS (§3) | | recorded |
**G-B passes.** No §5 miss occurred; no resize of any request is needed.
### Peak RSS per stage against the request (GiB; sacct MaxRSS from the cost files)
| stage (request) | AR pilot | ADJ-OPP pilot | AR twin | ADJ-OPP twin | plan (GB_PLAN §2.6, AR) |
|---|---|---|---|---|---|
| setup (16 G) | 2.50 (15.6 %) | 2.50 (15.6 %) | 2.51 | 2.50 | measured 1.43 on Owls (8 threads) |
| calibrate (16 G) | 5.74 (35.9 %) | 5.55 (34.7 %) | 6.44 (40.3 %) | 6.64 (41.5 %) | 8.33 (over-count; T5 8–11 GB) |
| islands (12 G) | 3.54 (29.5 %) | 3.70 (30.8 %) | 3.53 | 3.61 | 3.53 (AR pilot 3.535: exact) |
| merge (24 G), sacct MaxRSS (**includes page cache**) | 4.97 (20.7 %) | 6.86 (28.6 %) | 4.83 | 6.87 | 4.22; engine's own `sacct_upper` 7.77 / 7.85 |
| **merge process peak** (`fit.bin.json` `peak_rss_kb`, anonymous + mapped as the process saw it) | **2.07 (8.6 %)** | **2.06 (8.6 %)** | 2.07 | 2.06 | 4.22 (**0.49×**) |
| eval (16 G) | 1.67 (10.4 %) | 1.72 (10.8 %) | 1.82 | 1.88 | not planned |
**Merge, read correctly (Opus F1).** The merge's own process peak is **2.06–2.07 GiB in all four fits** (0.49× the 4.22 GiB plan: the plan bounds the real process at 10⁵). The higher sacct MaxRSS (4.83–6.87 GiB; AR vs ADJ-OPP differ only there) counts **file pages (page cache)**, the effect MERGE_MEM.md finding 1 showed for the 1M's 75.1 GiB; it is not a plan under-count, and my earlier "1.63× the plan, inside the 1M's 1.72 band" reading is withdrawn. **No 1M sizing risk follows from G-B**; the 1M merge request stays at 128G until a 1M `peak_rss_kb` is read. All requests unchanged.

## 5. Also reported (task 4)
**Selection and evidence (all R′ 16, N 10⁴, F2):**
| quantity | AR I_max 0 | AR I_max 3 | ADJ-OPP I_max 0 | ADJ-OPP I_max 3 |
|---|---|---|---|---|
| HPM; = S₀ (truth) | {10000, 30000, 50000, 70000, 90000}; **True** (T5: same) | same; True | {10000, 10001, 50000, 70000, 90000}; **True** | same; True |
| F(HPM) − F(S₀); outcome class; S₀ store rank | 0; correct; 0 | 0; correct; 0 | 1.1e−13; correct; 0 | same |
| **π̂(S₀)** = exp(F_S₀ − log Ẑ) (terminal occupancy of the top model) | **0.3865** (0.3862) | 0.3849 (0.3862) | **0.3397** (0.3403) | 0.3412 (0.3404) |
| log Ẑ | −233.2672 | −233.2630 | −244.1310 | −244.1354 |
| log Ẑ − log Z_T (deterministic bound) | +0.208 | +0.212 | +0.233 | +0.228 |
| σ̂ = sd(log Ẑ_r); R_eff/R′ | 0.0153; 0.9998 | 0.0167; 0.9997 | 0.0451; 0.9981 | 0.0506; 0.9974 |
| sup_{j∉S₀} PIP_eq; min_{j∈S₀} PIP_eq | 0.0166; 0.9998 | 0.0166; 0.9998 | 0.0917; 0.9937 | 0.0917; 0.9937 |
| island T (stages) | 30 | 30 | 20 | 20 |
**log Ẑ, V vs twin:** AR −0.0042 (0.74 combined island s.e. 0.0057), ADJ-OPP +0.0045 (0.26 of 0.0169): no difference beyond noise; T5 (N 2,500, I_max 3): −233.27. ADJ-OPP carries more null PIP mass (sup 0.092) than AR (0.017) with both HPM = S₀.
**Cost and wall per stage against T5 (AR r01; T5 = N 2,500, I_max 3, pre-freeze code, quote basis):**
| stage | T5 N 2,500 I_max 3 | G-B AR twin N 10⁴ I_max 3 | G-B AR pilot N 10⁴ I_max 0 | G-B ADJ-OPP pilot (I_max 0) |
|---|---|---|---|---|
| setup | 0.41 / 0:46 | 0.42 / 47 s | 0.53 / 60 s | 0.51 / 57 s |
| calibrate | 10.56 / 9:54 | 10.99 / 618 s (the same grid work: N-independent) | **1.51** / 85 s | **1.81** / 102 s (twin 8.46 / 476 s) |
| islands (16) | 28.10 / 112–153 s each | 71.12 / ≤ 414 s | 73.51 / ≤ 447 s | 62.40 / ≤ 396 s |
| merge (+ tail, LS0) | 0.74 / 2:47 | 0.49 / 111 s | 0.76 / 172 s | 0.87 / 195 s |
| eval + post | 0.07 / 0:30 | 0.09 / 41 s | 0.07 / 32 s | 0.07 / 30 s |
| **fit total** | 42.18 (39.9 w/o isa_check) | 83.11 | **76.39** | **65.65** |
The I_max 0 calibration costs 14 % (AR) and 21 % (ADJ-OPP) of the I_max 3 calibration, not the 10 % assumed; the saving per fit is 9.5 and 6.6. **Quote against measured:** the four fits cost 297.65 of the 501 quote (59 %): the islands came in at 73.5 / 71.1 for AR against the 105.9 quoted (f ≈ 2.5 instead of 3.77), and ADJ-OPP (T = 20) is cheaper than AR (T = 30), not 1.23× dearer.

## 6. Pre-declared reporting items (GB_PREREG §4)
Calibration E1 / E2 reported NOT EVALUATED at I_max 0; `grid_unconverged` True, `I_used` 0 / 3, `grid_fallback` empty in all four (constants, outside any quality aggregate); final-merge flags E1–E3, `low_empirical_ESS` False, `checks_passed_final` True in all four; sd(log Ẑ_r) > 1 False; island T equal between arms. The continuity twins were **not run** (they run with the rung); the measured f at 10⁵ is therefore inferred only from T5 (§1.5).

## 7. For HQ's ruling at G-B (task 5)
**(i) 10⁵ rung quote at the selected configuration (N 10⁴, I_max 0), re-based on the measured costs** (`tools/gb_readback_budget_output.txt`): AR n200 unit 76.4, ADJ-OPP 65.7; 12 fits ≈ **895**, **10 remaining ≈ 753 (P90 ≈ 1.1k)** after the two pilots (the rung fits AR r01 and ADJ-OPP r01); n = 400 at 1.0× (unmeasured at 10⁵; at the plan's 1.6× the remaining 10 would be ≈ +138, ≈ 891, inside the P90 1.1k; **the rung's first batch (AR n400 ×1) re-quotes the rest**), IND = 1.0× AR (**a change from the plan's 1.05×, −8**; assumption). **Continuity twins** (2 fits, N 2,500, I_max 0, same data and seeds): ≈ **60** (estimate from the I_max 0 stage costs with f 2.5: the **conservative** figure, ≈ 52 at f 2.9, and f 3.77 would under-quote them at ≈ 42); they run with the rung. **The rung quote does not use f** (it is the measured N 10⁴ unit costs). Rung data seeds, ids and the order as GB_PLAN §6.
**(ii) Option D (restated VERBATIM from GB_PLAN §6; HQ rules):** **Option D (H-1; HQ rules at G-B): proposed gate wording.** AR-strong n = 1,000 at 1M, N 2,500, I_max per the verdict (≈ 1,087), is released iff **all** hold on the 10⁵ rung (AR-strong, n 200 × 5 and n 400 × 3, in the winning configuration): **(D1)** the theorem premise holds at 10⁵: P̂(HPM = S₀) ≥ 4/5 at n 200 and 3/3 at n 400; **(D2)** the expected trend: the mean over datasets of **π̂(S₀)** (**field verified**: π̂(S₀) = exp(`selection.F_S0` − `evidence.logZ`), the estimated posterior probability of S₀, with the terminal occupancy `fit.meta.occ[M = 1].occ` beside it (S₀'s when HPM = S₀) and the store-law omitted mass reported) at n 400 is ≥ the mean at n 200 (OWNER_SHEET's expected band: 0.3–0.45 at n 200, rising; reported with the dataset-clustered interval, **not a significance test**: 5 against 3 datasets); **(D3)** the budget check: position + D ≤ 28.3k at the re-sized unit cost. Reported beside it, with **no numeric threshold and a flag to HQ if the N effect looks large**: the continuity twins' π̂(S₀) at N 2,500 against N 10⁴ (the trend is measured at N 10⁴, D runs at N 2,500). π₀(S₀) is a different, deferred quantity. *First evidence at n = 200, 10⁵ (two datasets):* π̂(S₀) 0.387 (AR), 0.340 (ADJ-OPP), HPM = S₀ in both; comparable to the expert's 0.3–0.45 draw (OWNER_SHEET: a p = 10⁶ draw, not a 10⁵ band).
**Notes for HQ on D2 (Opus F2):** (1) **D2 is a comparison of means with no tolerance** (5 datasets at n 200 against 3 at n 400); the clustered interval is reported but does not gate, so with a small true rise D2 is close to a coin flip; HQ should rule on it knowingly. (2) **D1 and D2 can be judged only at the rung read-back** (8 AR fits): G-B fixes the wording, not the release. (3) The continuity twins cover n = 200 only: there is no N 2,500 link at n = 400.
**(iii) 1M rep 1** (`6-AR-n200-r01-V-s1`, 437.44, pre-F2, I_max 3 with 3 rebuilds, N 2,500): **(a)** re-run frozen ≈ **317** (P90 ≈ 360; I_max 0 saves ≈ 121); **(b)** report as a separate configuration, **0**; (c) a 21st replicate ≈ 317. **Recommendation: (b)**, decided by HQ now that the rule PASSED: under PASS the MANIFEST §1 pilot rule (fresh replicate 1 when the frozen configuration changed) makes (b) a departure that needs HQ's explicit ruling; (b) leaves 19 of 20 replicates on-rule (21 frozen fits with ADJ-OPP and AR-weak); **(b) leaves the ONE N 10⁴ 1M fit on the rep-1 data without a same-seed N 2,500 I_max 0 partner unless the conditional H-34 seeds run (H-34 is released only after the first 1M replicates are clean); otherwise (a), +317 = 1.1 %, is the paired route, or HQ accepts an unpaired N 10⁴ fit**; with H-34's 20-seed block released on the rep-1 data, its seed 1 is the frozen re-run, so (a) then costs nothing extra; the N 10⁴ 1M fit on the rep-1 data (S2) wants a same-seed N 2,500 I_max 0 partner, which only (a) or the seed block supplies (the seed block is conditional, see above). The FAIL branch (rep 1 kept as an I_max 3 fit) is moot.
**(iv) Envelope** (28,300; closed 2,686.91 + **297.65** = **2,984.56**; unit costs 1M: 317 at N 2,500 I_max 0, 1,062 for the ONE N 10⁴ fit at f 3.77 — about **730 at f 2.5 and 840 at f 2.9 if the 10⁵ factor held at 1M, not measured there; 1,062 is kept** (higher f is the conservative side for this fit); D 1,087; ablations + competitors 1,052):
| scenario | position (no reserve) | +25 % on the unspent 1M items | share of 28.3k |
|---|---|---|---|
| after the rung and the twins (753 + 60) | 3,798 | | 13 % |
| S2, (b): 21 frozen 1M fits + ONE N 10⁴ + D + comp | **13,651** | 16,115 | 48 % / 57 % |
| S2, (a) / (c): 22 frozen fits | 13,968 | 16,511 | 49 % / 58 % |
| + H-34 20 seeds (6,335; (a) = (b)) | **19,986** | **24,034** | **71 % / 85 %** |
**Sensitivity (Opus F4).** The 1M frozen unit 317 takes the I_max 0 calibration as P7's pilot island (14.96). G-B measured the I_max 0 calibration at 14 % (AR) and 21 % (ADJ-OPP) of the I_max 3 calibration; applied to rep 1's 135.63 that is 19–29 per fit, **+4 to +14 per 1M fit**: ≈ **+80 to +310 on S2** (22 fits incl. the N 10⁴ one) and **+75 to +280 more with H-34**; the saving per fit becomes ≈ 107–117, not 121. Worst case H-34 with reserve ≈ **24.8k (87.5 %)**; every scenario still fits 28.3k; no decision changes.
The G-B result lowered the position by 203 against the quote (501 → 297.65) and the rung quote by about 366 (1,119 → 753 for the remaining 10 fits); nothing is released by this read-back (HQ rules).

## 8. Files, commands, sha256
`results/gb/readback/` (not committed): `gb_imax.json` `03e701abfeb379c9…`, `rule_stdout.txt` `d96ab3ae3b58680d…`, `gb_readback.json` `a38ad8f93cddd4db…`, `gb_readback.md` `a589ae290a48afb4…`; `tools/gb_readback_budget.py` + `_output.txt` (the §7 arithmetic). Commands: §3 (rule), §4 (`python3 -I gb_readback.py --records R --cost-dir <dir of the four cost_5-*.json links> --rule rule/gb_imax.json --branch pass --out readback`, no `cost_batch.json` in the directory), `python3 -I tools/gb_readback_budget.py`.

## 9. Points for the Opus checker
1. **Re-derive the rule** from the raw eval records (M1 = `fit.meta.occ[M = 1000].sd_log_Z_occ_r`, M2 = `pip.island_spread.max_sd`, M3 = `evidence.sigma_hat`): the 12 ratios of §3, the two geometric means, the HPM identity, and that the script run is the registered one (sha, tests).
2. **Identity:** recorded arm and N 10⁴ in all four `calib_meta.json`, `I_used` 0 / 3, F2 sha in every sidecar, X / y equal inside the pairs, the four plan shas against `presubmit/plans.sha256`.
3. **Cost and RSS** from the cost files against `prior_after_G2.json` and the sacct dumps (297.65; per-stage MaxRSS); that the cost directory held only the four per-run files; the C1 models used are the committed ones (108 / 133, twins 118 / 142).
4. **The f inference** (§1.5, §5) compares the AR twin with T5's record: same data, seed, I_max 3 and T 30, N differs; T5 ran pre-freeze code (04d8d2b5), but the 11-18 freeze check reproduced T5's island on F bit for bit (1.51 core-h) and F2 = F at default N, which bounds f at ≈ [2.5, 2.9]. It is an inference, not a measurement (the continuity twins measure it); it enters no criterion, and the rung quote does not use it.
5. **The descriptive sentence in §3** (0.904 about 2.8 s.d. below the bar) uses the PREREG §3 model with the N 2,500 sd; check that it is labelled descriptive and not read as a decision.
6. **Merge RSS** (§4, F1): the process peak (`peak_rss_kb`, 2.06–2.07 GiB, 0.49× plan) against sacct MaxRSS (4.83–6.87 GiB, page cache); the 1M merge policy (128G until a 1M `peak_rss_kb` is read) is unchanged.
7. **π̂(S₀) definition:** exp(F_S₀ − log Ẑ) (log Ẑ, the estimate), not the store-renormalised exp(F_S₀ − log Z_T); the two differ by exp(0.2) (≈ 1.23×): confirm the choice against the option-D wording (GB_PLAN §6) and that the terminal occupancy (0.386 / 0.340) agrees with it.
8. **Not done:** no NOTS access; no engine run; no change to any registered file or threshold; the continuity twins and the rung are not run; no π₀(S₀); no d_H between pair fits (the `law.bin` / `data.bin` are kept for it).
