# LEG_READBACK: precision study (Sol F6) + 10⁴ science leg: closing read-back, PREREG §5 / §6.3 (Engineering, Sonnet worker; Thu 2026-11-19 evening)

**Status: REVISED after the Opus leg review (`reviews/LEG_REVIEW_OPUS.md`, ACCEPT-WITH-FIXES, G-A closes): F1–F18 applied (dated 2026-11-19, later the same evening); not committed (the manager commits).** Descriptive only: no outcome class, no criterion verdict beyond what the registered files define; this worker made no NOTS access (the `law.bin` / `data.bin` of the 14 `VF` units were fetched afterwards by ops, §4, §7 L-12); the only registered / committed files touched are the appended, dated errata lines of `PREREG.md` §8 and `CAMPAIGN_FREEZE_ADDENDUM.md` ("Errata after the leg"), ordered by the manager. Supporting scripts, outputs and their sha256 are in `results/precision1e4/leg_readback/`; scratch was `~/SMC_Engineering_Department/tmp/20261119-legrb/`. Records: `~/SMC_Engineering_Department/records/precision1e4/{A0,P1…P4,B1,S1…S10}`; overlap: `records/overlap1e4/W0…W3`. All fits read here ran on the leg's one V build `d0c30b65…`; the 2 B1 T fits on `09249230…`.

## 1. Summary for HQ (≤ 12 lines)
1. **No newly failed criterion. G-A closes** (Opus review ACCEPT-WITH-FIXES). **ADDENDUM_2_VF is CLEAN:** the 14 `VF` fits (I_max = 0) pass every overlap v2 criterion that V at I_max = 3 passed, **including the Hellinger criterion H: 14/14, d_H(VF, T) / d_H(T, f\*) 0.0034–0.0136 against 0.10** (I_max 3: max 0.0136); the registered scorer returns **CLEAN, 11/11 PASS** on the 40-fit mixed set with the cross file. Scope: 14 pairs, p = 10⁴, n = 200. §4.
2. **G-A:** precision COMPLETE (§3.3: 18/18 delivered, 0 identity failures, XB bit-equal, FZ_CHECK_OPUS counted as the ACCEPT, HQ 5a44e163); **science 170/170 = 100 %** (156/156 new + 14/14 `VF`; ≥ 95 % needed); nothing to list as a failure. §2.
3. **Frozen configuration:** N 2,500 (provisional), m 1, I_max 0, resampling off ("not tested"), π₀(S₀) deferred; `CAMPAIGN_FREEZE_ADDENDUM.md` sha256 **`0b9890835ff36e4c…0f201491`** (exp/P1M e627b547), binary **`d0c30b65103e308e…`** (git F `eefcbc4a…`, one build: all 192 V fits; the 2 B1 T fits `09249230…`); all 170 science records show the recorded arm (2,500, 1, 0, I_used 0, bounded).
4. **VF vs T (14 pairs, R′ = 16):** HPM equal 14/14, MPM equal 14/14, T never higher F, NULL clean, PIP worst ratio 0.0379 (I_max 3: 0.0381), log Ẑ worst 1.38 of 3 combined s.e. (I_max 3: 1.76), E2 and C pass; I_max = 0 V agrees with T as I_max = 3 V did, and the 14 `VF` fits cost 33 % less than their I_max = 3 twins (1.35 vs 2.02 core-h; FZ estimated 39 %).
5. **Science, per design and n (§3):** P(HPM = S₀) AR-strong 0.50 (n 100) → 1.00 (n ≥ 200); AR-weak 0.00 / 0.50 / 1.00 / 0.90 (n 100 / 200 / 400 / 800); IND 0.8 / 1.0 / 0.8; BLK and ADJ-OPP 1.00; NULL: HPM empty 5/5, no null PIP > 0.5. 112 of 150 non-NULL fits recover S₀; all 38 misses are posterior-mode misses (34 are subsets of S₀, 4 contain one variable outside S₀). **At n ≥ 400 the store-BMA / oracle d_H² ratio is 1.02–1.04 in AR-strong, BLK and ADJ-OPP; it stays above 1 where HPM misses remain: AR-weak 1.40 / 1.58 (n 400 / 800), IND n 400 1.26 (the r01 fit with one extra variable).**
6. **Flags for HQ (not criteria):** (a) **`4-ADJOPP-n200-r04-V-s1`: σ̂ = sd(log Ẑ_r) 1.09, R_eff/R′ 0.42, the one final-merge E2 of the leg, log Ẑ 0.123 BELOW the deterministic lower bound log Z_T (the only fit of 155 with log Ẑ < log Z_T), selection intact (HPM = MPM = S₀); no I_max = 3 twin, so not attributable; no bearing on the freeze; optional attribution check ≈ 3–4 core-h (§3.4).** (b) §0-v2.3 targets at the production R′ = 16 (report-only): M1 0 misses, **M2 14/155 above 0.005 (13 at n = 100)**, M3 1/155 above 0.5 (the same ADJ-OPP fit); this corrects the freeze addendum's "every fit meets the targets", which covers the R′ = 64 precision fits only. low_empirical_ESS 6. A3: 15/15 HPM identical, max |ΔPIP| 2.5 × 10⁻⁴ (second-seed spread 8.7 × 10⁻⁴); second seed 10/10.
7. **Offset, final (§5):** δ(ovl, k = 16) = −0.00394 reproduced; leg cells at k = 64: −0.0060 (m1·I3), −0.0059 (m4·I3), −0.0069 (m1·I0), half-widths 0.005–0.007 (3 datasets); R′ span = Jensen term; contrasts m +0.0001 [−0.0018, +0.0020], I_max −0.0009 [−0.0040, +0.0022]; **no FINDING**; N contrast not computable; `vf` row (10 datasets) −0.0030 [−0.0061, +0.0001]; B1 point −0.0004.
8. **Cost:** leg **462.48 core-h** (ledger; 462.46 unrounded; VN_ID_1 1.99 separate) = 11.2 % of the plan 4,127 and 0.75 × the committed released-scope quote at the frozen setting (505 + B1 115). **G-B cost criterion PASS in all 21 classes** (class mean ≤ 1.5 × model, no fit above 1.5 × model, largest single 1.36 ×). §6.
9. **n-scaling:** n = 400 and n = 800 cost less than or about the same as n = 200 (AR-strong 0.77 × / 1.02 ×, AR-weak 0.84 × / 0.85 ×, IND 0.73 ×, ADJ-OPP 0.77 ×), against the model's 1.6 × / 2.8 × — **except BLK n = 400, 1.31 ×**; cost follows the frozen grid length T, not n.
10. **G-B readiness (§8):** the 10⁵ pilot on F2 (`p1m-freeze-F2` e993ece2, binary da0cf85b, identity PASS), the I_max = 3 twin with the registered rule pre-declared, 1M rep 1 options (a) / (b) (recommendation: (b) now, decide after the 10⁵ twin; (b) leaves 19 of the 20 approved replicates in the frozen configuration), the V-N mini-leg; plus 6 items the G-B plan must settle.
11. **Deviations and errata (§7):** the science analysis script was **not registered before this first science read-back** (PREREG §8 entry; moderate procedural breach, no gate touched); the VF scoring was late and 14 units were amended with `law.bin` / `data.bin` (PREREG §8 entries); the E1 / E2 final-merge wording and the σ̂ = sd(log Ẑ_r) label are corrected in PREREG §8 and the freeze addendum (errata, 2026-11-19).

## 2. G-A closing (PREREG §6.3)

| G-A condition | status | evidence |
|---|---|---|
| **Precision study COMPLETE** (§3.3) | **MET** | 18/18 released precision fits delivered (D), arm identity verified from `calib_meta.json` (0 failures), canary A0 clean incl. the XB bit check (16/16 `logZ_r`, HPM, 16/16 island output hashes equal to the overlap records), both registered scripts run with shas verified (`precision_freeze.py` `7cdd69a11f3a…6279605`, `precision_offset.py` `cbbc23012e69…d300`; re-verified here, HEAD blobs equal), independent review `reviews/FZ_CHECK_OPUS.md` CONFIRMED-WITH-FIXES (counted as the ACCEPT, CAMPAIGN_FREEZE_ADDENDUM header), FZ accepted by HQ 5a44e163 (H-30). Rule output: m = 4 KEEP m = 1, I_max = 0 ADOPT, N = 10⁴ NOT RUN, resampling not testable. |
| **Science completion ≥ 95 %** (§2) | **MET: 170/170 = 100 %** | 156/156 new fits (≥ 149 needed) + 14/14 `VF`; leg 194/194 (A0 4, P1–P4 16, B1 4, S1–S10 170); `LEG_COMPLETENESS_output.txt`. Delivered = unit present, one `SHA256SUMS` and `sha256sum -c` OK, `fit.bin`, `eval.bin.json` status and fit_status completed, every stage COMPLETED, `evidence.logZ_r` of length R′ and finite. No non-delivery, no rerun. Re-checked here from the eval records: 170/170 completed, recorded arm (N 2,500, m 1, I_max 0, I_used 0, rule bounded) in 170/170, one `binary.sha256` in 170/170. |
| **Frozen configuration recorded by hash** | **MET** | see below |

| item | value |
|---|---|
| frozen configuration | N 2,500 **provisional** (default D-1, not evidence), m 1, I_max 0, resampling OFF "not tested", π₀(S₀) deferred (HQ Q6) |
| `CAMPAIGN_FREEZE_ADDENDUM.md` sha256, as committed | **`0b9890835ff36e4cfbd3b05e49d6a6440be7a5a5c7c0cf46a9dcdd390f201491`** (blob committed in exp/P1M **e627b547**, unchanged at HEAD (HEAD itself is now an auto-snapshot); also in LOG 11-19 10:30 CST) |
| `ADDENDUM_2_VF.md` / `PREREG.md` as committed | `8c70fc53700cbb1c5f370b59506478b82d9b87ba1bf96a89ff7c084bf63eaa31` / `3f2daf76c367e33cf0d2f00c2c4d7d00a1a072044dbd30e5d17611fe03ca6c9f` |
| V binary (the leg's ONE build) | sha256 **`d0c30b65103e308eb12c0665727c248f9ef0d9afe28f115dc9da6614a981b378`**, git **F = `eefcbc4a2ab42fdf52ec1e5d318a956bdd07f463`** (tag `method-v3.1.1-listpip`), ISA sapphirerapids, `deploy_leg.log` BUILD line 2026-11-19T10:05:47Z; in all 192 V fits (A0 4, P1–P4 16, B1 V 2, S1–S10 170), 0 deviations |
| T binary (B1 only) | `09249230f052860fbf04960e5a224cd6e4987b461de91eafa28cf97ec12cbc21`, git F, ISA portable (`BUILD_T`); the 2 B1 T fits |
| science plan | `waves_freeze_i0.json` sha256 `2837a507b95713713d7b660fe605d94f9a3a3ae4c0a9c0d5b2fc4b15240f7964` (I_max = 0 scenario, S1–S10; `LEG_PLAN.md` §10) |
| validity scope of I_max = 0 (as in the addendum, unchanged) | p = 10⁴; precision n = 200, 3 datasets, R′ = 64; carry-over 14 VF pairs (§4); science n = 100–800 (this file). Extrapolation to 10⁵ and 1M is not shown: G-B. |

**G-A is met on the records.** It closes when the Opus review of this read-back (PREREG §6.3) accepts it and HQ rules. Not closed by G-A (carried): N = 10⁴ (V-N mini-leg), resampling, π₀(S₀), the m × I_max interaction.

## 3. The 10⁴ science, per PREREG §5 (descriptive; no pass/fail except completion)
**Conventions.** Cells = design × n; science fits = tags `V` / `VF` (155 fits, all at the frozen configuration; `VF` = the 14 overlap fits re-run at I_max 0); the 15 `A3` / `A3F` exact-partition fits are analysed only in the A3 block. The **dataset** is the unit (the two engine seeds of AR n = 200 are averaged within a dataset first). Continuous quantities: mean over datasets and its 95 % t interval (df = datasets − 1; **not clipped, so intervals for counts, proportions and PIPs can leave [0, 1]**; IND / BLK / ADJ-OPP cells have 5 datasets). Proportions: dataset-level fractions averaged, Wilson 95 % interval with n = number of datasets (fractional successes at AR n = 200). The slope of log d_H² on log n: OLS on log of the dataset-mean per n, percentile interval of a dataset bootstrap within each n (B 4,000, seed 20261119). The PIP reliability curve is a **repeated-sampling diagnostic under a fixed truth** (MANIFEST_CELLS §4), pooled over fits, with dataset-cluster bootstrap intervals. The analysis script is `leg_readback/scripts/science.py` (stdlib + numpy / scipy; **not registered in advance: §7 L-8**); full generated tables: `leg_readback/science/science_tables.md`, `science_per_fit.csv`, `science_summary.json`; post-read extras `science_extras*.md`.
Inventory (155 fits): AR-strong n 100 / 200 / 400 / 800 = 10 / 20 (10 datasets × seeds 1, 2) / 10 / 10; AR-weak 20 / 20 / 10 / 10; IND 5 / 5 / 5; BLK 5 / 5 / 5; ADJ-OPP – / 5 / 5; NULL – / 5 / –.

### 3.1 C2 reported model = S₀

| design | n | P(HPM = S0) | outcome classes (fits) | mean Hamming HPM | HPM TP / FP / FN (mean per fit) | P(MPM = S0) | MPM TP / FP (mean) | HPM phase (fits) |
|---|---|---|---|---|---|---|---|---|
| AR-strong | 100 | 0.50 [0.24, 0.76] (5/10 fits; 10 ds) | correct 5, posterior 5 | 0.70 [2.1e-02, 1.38] | 4.30 / 0.00 / 0.70 | 0.60 [0.31, 0.83] (6/10 fits; 10 ds) | 4.40 / 0.00 | final_bridge 3, pilot 7 |
| AR-strong | 200 | 1.00 [0.72, 1.00] (20/20 fits; 10 ds) | correct 20 | 0.00 [0.00, 0.00] | 5.00 / 0.00 / 0.00 | 1.00 [0.72, 1.00] (20/20 fits; 10 ds) | 5.00 / 0.00 | final_bridge 14, pilot 6 |
| AR-strong | 400 | 1.00 [0.72, 1.00] (10/10 fits; 10 ds) | correct 10 | 0.00 [0.00, 0.00] | 5.00 / 0.00 / 0.00 | 1.00 [0.72, 1.00] (10/10 fits; 10 ds) | 5.00 / 0.00 | pilot 10 |
| AR-strong | 800 | 1.00 [0.72, 1.00] (10/10 fits; 10 ds) | correct 10 | 0.00 [0.00, 0.00] | 5.00 / 0.00 / 0.00 | 1.00 [0.72, 1.00] (10/10 fits; 10 ds) | 5.00 / 0.00 | pilot 10 |
| AR-weak | 100 | 0.00 [0.00, 0.16] (0/20 fits; 20 ds) | posterior 20 | 4.55 [4.23, 4.87] | 0.45 / 0.00 / 4.55 | 0.00 [0.00, 0.16] (0/20 fits; 20 ds) | 0.65 / 0.00 | final_bridge 2, pilot 2, table 16 |
| AR-weak | 200 | 0.50 [0.30, 0.70] (10/20 fits; 20 ds) | correct 10, posterior 10 | 0.80 [0.35, 1.25] | 4.25 / 0.05 / 0.75 | 0.50 [0.30, 0.70] (10/20 fits; 20 ds) | 4.35 / 0.05 | final_bridge 8, pilot 12 |
| AR-weak | 400 | 1.00 [0.72, 1.00] (10/10 fits; 10 ds) | correct 10 | 0.00 [0.00, 0.00] | 5.00 / 0.00 / 0.00 | 1.00 [0.72, 1.00] (10/10 fits; 10 ds) | 5.00 / 0.00 | final_bridge 5, pilot 5 |
| AR-weak | 800 | 0.90 [0.60, 0.98] (9/10 fits; 10 ds) | correct 9, posterior 1 | 0.10 [-0.13, 0.33] | 5.00 / 0.10 / 0.00 | 0.90 [0.60, 0.98] (9/10 fits; 10 ds) | 5.00 / 0.10 | final_bridge 1, pilot 9 |
| IND | 100 | 0.80 [0.38, 0.96] (4/5 fits; 5 ds) | correct 4, posterior 1 | 0.60 [-1.07, 2.27] | 4.60 / 0.20 / 0.40 | 0.80 [0.38, 0.96] (4/5 fits; 5 ds) | 4.80 / 0.20 | final_bridge 1, pilot 4 |
| IND | 200 | 1.00 [0.57, 1.00] (5/5 fits; 5 ds) | correct 5 | 0.00 [0.00, 0.00] | 5.00 / 0.00 / 0.00 | 1.00 [0.57, 1.00] (5/5 fits; 5 ds) | 5.00 / 0.00 | final_bridge 5 |
| IND | 400 | 0.80 [0.38, 0.96] (4/5 fits; 5 ds) | correct 4, posterior 1 | 0.20 [-0.36, 0.76] | 5.00 / 0.20 / 0.00 | 0.80 [0.38, 0.96] (4/5 fits; 5 ds) | 5.00 / 0.20 | final_bridge 1, pilot 4 |
| BLK | 100 | 1.00 [0.57, 1.00] (5/5 fits; 5 ds) | correct 5 | 0.00 [0.00, 0.00] | 5.00 / 0.00 / 0.00 | 0.80 [0.38, 0.96] (4/5 fits; 5 ds) | 5.00 / 0.20 | final_bridge 2, pilot 3 |
| BLK | 200 | 1.00 [0.57, 1.00] (5/5 fits; 5 ds) | correct 5 | 0.00 [0.00, 0.00] | 5.00 / 0.00 / 0.00 | 1.00 [0.57, 1.00] (5/5 fits; 5 ds) | 5.00 / 0.00 | final_bridge 3, pilot 2 |
| BLK | 400 | 1.00 [0.57, 1.00] (5/5 fits; 5 ds) | correct 5 | 0.00 [0.00, 0.00] | 5.00 / 0.00 / 0.00 | 1.00 [0.57, 1.00] (5/5 fits; 5 ds) | 5.00 / 0.00 | pilot 5 |
| ADJ-OPP | 200 | 1.00 [0.57, 1.00] (5/5 fits; 5 ds) | correct 5 | 0.00 [0.00, 0.00] | 5.00 / 0.00 / 0.00 | 1.00 [0.57, 1.00] (5/5 fits; 5 ds) | 5.00 / 0.00 | final_bridge 4, pilot 1 |
| ADJ-OPP | 400 | 1.00 [0.57, 1.00] (5/5 fits; 5 ds) | correct 5 | 0.00 [0.00, 0.00] | 5.00 / 0.00 / 0.00 | 1.00 [0.57, 1.00] (5/5 fits; 5 ds) | 5.00 / 0.00 | pilot 5 |
| NULL | 200 | 1.00 [0.57, 1.00] (5/5 fits; 5 ds) | correct 5 | 0.00 [0.00, 0.00] | 0.00 / 0.00 / 0.00 | 1.00 [0.57, 1.00] (5/5 fits; 5 ds) | 0.00 / 0.00 | table 5 |

Misses: **38 of the 150 non-NULL fits have HPM ≠ S₀** (AR-strong n 100: 5; AR-weak n 100: 20, n 200: 10, n 800: 1; IND n 100: 1, n 400: 1). Every one has outcome class `posterior` (F(HPM) > F(S₀): the posterior mode itself is not S₀; the search class never occurs). **34 are strict subsets of S₀ (false negatives only: AR-weak n 100 has |HPM| = 0 in 13 of 20 and S₀ is not even in the store in 11)**; **4 contain one variable outside S₀** (AR-weak n 200 r06, AR-weak n 800 r01 and IND n 400 r01 hold all of S₀ plus one: |HPM| 6, TP 5, FP 1; IND n 100 r03 holds 3 of the 5 plus one). The per-fit list is in `science_tables.md` (S1). **At n ≥ 200, 98 of 110 non-NULL fits recover S₀**; the 12 misses are AR-weak n 200 (10 of 20 fits), AR-weak n 800 (1 of 10) and IND n 400 (1 of 5); AR-strong (40/40), BLK, ADJ-OPP and AR-weak n 400 are all S₀. NULL: HPM is the empty model in 5 of 5.

### 3.2 C4 PIP consistency

| design | n | sup null PIP (eq) | min PIP over S0 (eq) | sup null (Z) | min over S0 (Z) | Brier (eq) | #null PIP > 0.1 (mean per fit; fits with >= 1) | #null PIP > 0.5 (fits with >= 1) | max abs(PIP_Z - PIP_eq) (max) |
|---|---|---|---|---|---|---|---|---|---|
| AR-strong | 100 | 0.172 [0.076, 0.267] | 0.561 [0.250, 0.872] | 0.172 [0.076, 0.268] | 0.561 [0.250, 0.872] | 5.813e-05 [6.706e-06, 1.095e-04] | 1.20; 6/10 | 0/10 | 3.4e-04 |
| AR-strong | 200 | 0.124 [0.032, 0.217] | 1.000 [1.000, 1.000] | 0.124 [0.032, 0.217] | 1.000 [1.000, 1.000] | 4.110e-06 [-8.717e-07, 9.092e-06] | 0.60; 8/20 | 0/20 | 2.8e-05 |
| AR-strong | 400 | 0.055 [0.021, 0.090] | 1.000 [1.000, 1.000] | 0.055 [0.021, 0.090] | 1.000 [1.000, 1.000] | 7.344e-07 [1.316e-07, 1.337e-06] | 0.20; 2/10 | 0/10 | 9.7e-06 |
| AR-strong | 800 | 0.050 [0.021, 0.080] | 1.000 [1.000, 1.000] | 0.050 [0.021, 0.080] | 1.000 [1.000, 1.000] | 4.831e-07 [2.255e-09, 9.639e-07] | 0.10; 1/10 | 0/10 | 2.6e-06 |
| AR-weak | 100 | 0.117 [0.059, 0.174] | 2.2e-03 [-2.3e-04, 4.6e-03] | 0.117 [0.059, 0.174] | 2.2e-03 [-2.3e-04, 4.6e-03] | 4.029e-04 [3.557e-04, 4.500e-04] | 0.40; 7/20 | 0/20 | 3.2e-04 |
| AR-weak | 200 | 0.151 [0.065, 0.237] | 0.560 [0.374, 0.745] | 0.151 [0.065, 0.237] | 0.560 [0.374, 0.745] | 5.834e-05 [2.452e-05, 9.215e-05] | 0.45; 8/20 | 1/20 | 3.0e-05 |
| AR-weak | 400 | 0.090 [3.6e-03, 0.177] | 0.966 [0.894, 1.038] | 0.090 [3.6e-03, 0.177] | 0.966 [0.894, 1.038] | 3.844e-06 [-6.309e-07, 8.318e-06] | 0.40; 3/10 | 0/10 | 2.9e-05 |
| AR-weak | 800 | 0.123 [-0.073, 0.319] | 1.000 [1.000, 1.000] | 0.123 [-0.073, 0.319] | 1.000 [1.000, 1.000] | 8.326e-06 [-9.807e-06, 2.646e-05] | 0.20; 2/10 | 1/10 | 6.2e-06 |
| IND | 100 | 0.302 [-0.103, 0.708] | 0.748 [0.221, 1.276] | 0.302 [-0.103, 0.708] | 0.748 [0.221, 1.276] | 4.690e-05 [-5.400e-05, 1.478e-04] | 1.00; 3/5 | 1/5 | 1.3e-04 |
| IND | 200 | 0.095 [-8.7e-03, 0.199] | 1.000 [1.000, 1.000] | 0.095 [-8.7e-03, 0.199] | 1.000 [1.000, 1.000] | 1.992e-06 [-1.349e-06, 5.332e-06] | 0.20; 1/5 | 0/5 | 1.4e-05 |
| IND | 400 | 0.307 [-0.119, 0.733] | 1.000 [1.000, 1.000] | 0.307 [-0.119, 0.733] | 1.000 [1.000, 1.000] | 1.902e-05 [-2.089e-05, 5.894e-05] | 0.60; 3/5 | 1/5 | 3.2e-06 |
| BLK | 100 | 0.159 [-0.084, 0.402] | 0.960 [0.918, 1.002] | 0.159 [-0.084, 0.402] | 0.960 [0.918, 1.002] | 1.117e-05 [-1.553e-05, 3.786e-05] | 1.00; 2/5 | 1/5 | 2.8e-04 |
| BLK | 200 | 0.034 [0.021, 0.048] | 1.000 [1.000, 1.000] | 0.034 [0.021, 0.048] | 1.000 [1.000, 1.000] | 4.287e-07 [1.209e-07, 7.366e-07] | 0.00; 0/5 | 0/5 | 4.0e-06 |
| BLK | 400 | 0.089 [0.013, 0.165] | 1.000 [1.000, 1.000] | 0.089 [0.013, 0.165] | 1.000 [1.000, 1.000] | 1.307e-06 [-3.149e-08, 2.645e-06] | 0.60; 3/5 | 0/5 | 5.8e-06 |
| ADJ-OPP | 200 | 0.131 [-0.064, 0.327] | 1.000 [0.999, 1.000] | 0.131 [-0.064, 0.327] | 1.000 [0.999, 1.000] | 4.306e-06 [-5.173e-06, 1.379e-05] | 0.40; 2/5 | 0/5 | 1.5e-04 |
| ADJ-OPP | 400 | 0.049 [0.015, 0.084] | 1.000 [1.000, 1.000] | 0.049 [0.015, 0.084] | 1.000 [1.000, 1.000] | 5.068e-07 [-1.150e-07, 1.129e-06] | 0.00; 0/5 | 0/5 | 5.2e-06 |
| NULL | 200 | 0.011 [6.8e-03, 0.015] | n/a (S0 empty) | 0.011 [6.8e-03, 0.015] | n/a | 2.739e-08 [2.583e-09, 5.219e-08] | 0.00; 0/5 | 0/5 | 6.6e-08 |

Active-variable detection (equal-weight PIP): minimum PIP over S₀ is > 0.5 in 6/10 AR-strong n 100 fits, 20/20 at n 200, 10/10 at n 400 and 800; AR-weak 0/20, 11/20, 10/10, 10/10 (> 0.9 in 0, 6, 9, 10); IND n 100 4/5, BLK n 100 5/5, all other cells all fits. **A null variable with PIP > 0.5 occurs in 5 non-NULL fits** (AR-weak n 200 r06, AR-weak n 800 r01, BLK n 100 r03, IND n 100 r03, IND n 400 r01; one variable each) and in **0 of 5 NULL fits** (largest null PIP 0.0157). PIP_Z and PIP_eq agree to ≤ 3.4 × 10⁻⁴ everywhere (`max |PIP_Z − PIP_eq|` column).

**PIP reliability curve, AR-weak arm** (60 datasets, 60 fits; bins of 0.05; observed = share of the pooled variables that are active; cluster interval = dataset bootstrap; last column = observed by n):

| bin | variables n (all AR-weak fits) | mean PIP (predicted frequency) | observed frequency of S0 | 95% dataset-cluster bootstrap | n_true (active) | datasets with >= 1 variable | observed by n (100 / 200 / 400 / 800) |
|---|---|---|---|---|---|---|---|
| 0.00-0.05 | 599722 | 0.0001 | 0.0001 | [7.84e-05, 1.70e-04] | 74 | 60 | 0.000 (70/199954) / 0.000 (4/199879) / 0.000 (0/99942) / 0.000 (0/99947) |
| 0.05-0.10 | 33 | 0.0708 | 0.1212 | [0.0294, 0.2353] | 4 | 23 | 0.333 (4/12) / 0.000 (0/16) / 0.000 (0/4) / 0.000 (0/1) |
| 0.10-0.15 | 14 | 0.1230 | 0.5000 | [0.2143, 0.8000] | 7 | 13 | 0.600 (3/5) / 0.667 (4/6) / 0.000 (0/2) / 0.000 (0/1) |
| 0.15-0.20 | 6 | 0.1727 | 0.1667 | [0.0000, 0.5000] | 1 | 6 | 0.500 (1/2) / 0.000 (0/3) / 0.000 (0/1) / - (0/0) |
| 0.20-0.25 | 5 | 0.2320 | 1.0000 | [1.0000, 1.0000] | 5 | 5 | 1.000 (2/2) / 1.000 (3/3) / - (0/0) / - (0/0) |
| 0.25-0.30 | 3 | 0.2595 | 0.3333 | [0.0000, 1.0000] | 1 | 3 | 0.333 (1/3) / - (0/0) / - (0/0) / - (0/0) |
| 0.30-0.35 | 4 | 0.3157 | 0.5000 | [0.0000, 1.0000] | 2 | 4 | 0.333 (1/3) / 1.000 (1/1) / - (0/0) / - (0/0) |
| 0.35-0.40 | 5 | 0.3866 | 0.2000 | [0.0000, 0.6667] | 1 | 5 | 0.500 (1/2) / 0.000 (0/3) / - (0/0) / - (0/0) |
| 0.40-0.45 | 4 | 0.4032 | 0.7500 | [0.0000, 1.0000] | 3 | 4 | 1.000 (2/2) / 1.000 (1/1) / 0.000 (0/1) / - (0/0) |
| 0.45-0.50 | 2 | 0.4801 | 1.0000 | [1.0000, 1.0000] | 2 | 2 | 1.000 (2/2) / - (0/0) / - (0/0) / - (0/0) |
| 0.50-0.55 | 1 | 0.5306 | 1.0000 | [1.0000, 1.0000] | 1 | 1 | 1.000 (1/1) / - (0/0) / - (0/0) / - (0/0) |
| 0.55-0.60 | 5 | 0.5682 | 1.0000 | [1.0000, 1.0000] | 5 | 4 | 1.000 (2/2) / 1.000 (3/3) / - (0/0) / - (0/0) |
| 0.65-0.70 | 1 | 0.6801 | 1.0000 | [1.0000, 1.0000] | 1 | 1 | - (0/0) / - (0/0) / 1.000 (1/1) / - (0/0) |
| 0.70-0.75 | 4 | 0.7297 | 0.7500 | [0.0000, 1.0000] | 3 | 4 | 1.000 (1/1) / 0.667 (2/3) / - (0/0) / - (0/0) |
| 0.75-0.80 | 2 | 0.7762 | 1.0000 | [1.0000, 1.0000] | 2 | 2 | 1.000 (1/1) / 1.000 (1/1) / - (0/0) / - (0/0) |
| 0.80-0.85 | 2 | 0.8289 | 1.0000 | [1.0000, 1.0000] | 2 | 2 | - (0/0) / 1.000 (1/1) / 1.000 (1/1) / - (0/0) |
| 0.85-0.90 | 4 | 0.8900 | 0.7500 | [0.0000, 1.0000] | 3 | 4 | 1.000 (2/2) / 1.000 (1/1) / - (0/0) / 0.000 (0/1) |
| 0.90-0.95 | 6 | 0.9429 | 1.0000 | [1.0000, 1.0000] | 6 | 5 | - (0/0) / 1.000 (6/6) / - (0/0) / - (0/0) |
| 0.95-1.00 | 177 | 0.9973 | 1.0000 | [1.0000, 1.0000] | 177 | 46 | 1.000 (6/6) / 1.000 (73/73) / 1.000 (48/48) / 1.000 (50/50) |

Reading (descriptive): the top bin (PIP ≥ 0.95) holds 177 variables, all active (predicted 0.997); the bottom bin (PIP < 0.05; 599,722 variables) holds 74 actives (**observed 1.2 × 10⁻⁴ [0.8 × 10⁻⁴, 1.7 × 10⁻⁴] against a mean PIP of 5.7 × 10⁻⁵**; 70 of the 74 are at n = 100, where the HPM is mostly empty); the 101 variables with PIP in [0.05, 0.95) contain 49 actives where the summed PIP predicts 32.2 (n 100: 24 vs 11.6; n 200: 23 vs 17.0; n 400: 2 vs 2.6; n 800: 0 vs 1.1). The mid-range bins are sparse (1–14 variables), so each has a wide interval. Under a fixed truth this is a repeated-sampling statement, not a calibration of any single posterior.

### 3.3 C5 distribution

| design | n | d_H^2 HPM plug-in | d_H^2 MPM plug-in | d_H^2 store-BMA predictive | oracle d_H^2 (known-S0 fit) | ratio to oracle (BMA / oracle) | n d_H^2 (BMA) | n d_H^2 / (s0 log p) (BMA) | post. median d_H | test MSE - oracle | mlpd - oracle |
|---|---|---|---|---|---|---|---|---|---|---|---|
| AR-strong | 100 | 0.0364 [0.0093, 0.0635] | 0.0324 [0.0050, 0.0598] | 0.0314 [0.0103, 0.0525] | 0.0092 [0.0069, 0.0115] | 4.399 [0.175, 8.622] | 3.143 [1.032, 5.254] | 0.0682 [0.0224, 0.1141] | 0.2117 [0.1628, 0.2605] | 0.2180 [-0.0308, 0.4667] | -0.0789 [-0.1552, -0.0026] |
| AR-strong | 200 | 0.0043 [0.0029, 0.0056] | 0.0043 [0.0029, 0.0056] | 0.0048 [0.0037, 0.0059] | 0.0042 [0.0030, 0.0055] | 1.191 [0.936, 1.446] | 0.956 [0.733, 1.179] | 0.0208 [0.0159, 0.0256] | 0.1038 [0.0942, 0.1135] | 0.0038 [-0.0010, 0.0087] | -0.0020 [-0.0046, 6.28e-04] |
| AR-strong | 400 | 0.0015 [8.90e-04, 0.0020] | 0.0015 [8.90e-04, 0.0020] | 0.0015 [9.59e-04, 0.0021] | 0.0015 [9.11e-04, 0.0021] | 1.036 [0.991, 1.082] | 0.610 [0.384, 0.837] | 0.0133 [0.0083, 0.0182] | 0.0616 [0.0565, 0.0668] | 5.96e-04 [-1.97e-04, 0.0014] | -3.14e-04 [-7.28e-04, 9.94e-05] |
| AR-strong | 800 | 0.0011 [6.27e-04, 0.0016] | 0.0011 [6.27e-04, 0.0016] | 0.0011 [6.43e-04, 0.0015] | 0.0011 [6.27e-04, 0.0015] | 1.020 [0.996, 1.044] | 0.877 [0.514, 1.240] | 0.0190 [0.0112, 0.0269] | 0.0463 [0.0412, 0.0514] | -1.21e-05 [-4.29e-04, 4.05e-04] | 1.13e-05 [-1.95e-04, 2.18e-04] |
| AR-weak | 100 | 0.1055 [0.0971, 0.1139] | 0.1002 [0.0892, 0.1112] | 0.0933 [0.0822, 0.1044] | 0.0082 [0.0066, 0.0098] | 14.256 [9.958, 18.554] | 9.331 [8.221, 10.440] | 0.2026 [0.1785, 0.2267] | 0.3225 [0.3105, 0.3344] | 0.8639 [0.7410, 0.9869] | -0.2902 [-0.3256, -0.2547] |
| AR-weak | 200 | 0.0183 [0.0100, 0.0265] | 0.0164 [0.0089, 0.0238] | 0.0152 [0.0087, 0.0217] | 0.0046 [0.0034, 0.0059] | 3.496 [2.185, 4.807] | 3.039 [1.738, 4.340] | 0.0660 [0.0377, 0.0942] | 0.1463 [0.1248, 0.1678] | 0.0907 [0.0341, 0.1474] | -0.0393 [-0.0622, -0.0165] |
| AR-weak | 400 | 0.0024 [9.96e-04, 0.0037] | 0.0024 [9.96e-04, 0.0037] | 0.0031 [0.0011, 0.0051] | 0.0024 [0.0010, 0.0038] | 1.395 [0.794, 1.995] | 1.240 [0.433, 2.047] | 0.0269 [0.0094, 0.0445] | 0.0718 [0.0600, 0.0836] | 0.0058 [-0.0030, 0.0145] | -0.0026 [-0.0067, 0.0014] |
| AR-weak | 800 | 0.0013 [1.84e-04, 0.0023] | 0.0013 [1.84e-04, 0.0023] | 0.0011 [3.38e-04, 0.0020] | 7.82e-04 [5.14e-04, 0.0011] | 1.582 [0.295, 2.868] | 0.918 [0.270, 1.565] | 0.0199 [0.0059, 0.0340] | 0.0462 [0.0372, 0.0552] | 0.0022 [-0.0029, 0.0074] | -0.0014 [-0.0045, 0.0018] |
| IND | 100 | 0.0309 [-0.0341, 0.0959] | 0.0234 [-0.0209, 0.0678] | 0.0244 [-0.0168, 0.0656] | 0.0087 [0.0025, 0.0149] | 2.292 [-0.353, 4.937] | 2.440 [-1.684, 6.563] | 0.0530 [-0.0366, 0.1425] | 0.1977 [0.0865, 0.3089] | 0.1486 [-0.2192, 0.5164] | -0.0691 [-0.2377, 0.0996] |
| IND | 200 | 0.0052 [0.0019, 0.0086] | 0.0052 [0.0019, 0.0086] | 0.0052 [0.0023, 0.0080] | 0.0050 [0.0020, 0.0080] | 1.044 [0.950, 1.137] | 1.032 [0.467, 1.598] | 0.0224 [0.0101, 0.0347] | 0.1049 [0.0924, 0.1174] | 0.0013 [-4.56e-04, 0.0030] | -4.27e-04 [-0.0014, 5.72e-04] |
| IND | 400 | 0.0046 [-0.0019, 0.0112] | 0.0046 [-0.0019, 0.0112] | 0.0042 [-5.07e-04, 0.0089] | 0.0030 [8.13e-04, 0.0052] | 1.255 [0.850, 1.660] | 1.677 [-0.203, 3.557] | 0.0364 [-0.0044, 0.0772] | 0.0826 [0.0518, 0.1135] | 0.0088 [-0.0102, 0.0279] | -0.0054 [-0.0172, 0.0065] |
| BLK | 100 | 0.0067 [0.0039, 0.0096] | 0.0124 [-7.71e-04, 0.0256] | 0.0095 [0.0049, 0.0142] | 0.0064 [0.0041, 0.0087] | 1.752 [0.023, 3.480] | 0.953 [0.489, 1.416] | 0.0207 [0.0106, 0.0308] | 0.1569 [0.1142, 0.1996] | 0.0253 [-0.0183, 0.0688] | -0.0105 [-0.0309, 0.0099] |
| BLK | 200 | 0.0076 [0.0050, 0.0101] | 0.0076 [0.0050, 0.0101] | 0.0079 [0.0051, 0.0107] | 0.0078 [0.0051, 0.0105] | 1.007 [0.995, 1.019] | 1.578 [1.014, 2.141] | 0.0343 [0.0220, 0.0465] | 0.1129 [0.0996, 0.1263] | 5.89e-04 [-5.47e-04, 0.0017] | -3.16e-04 [-0.0010, 3.90e-04] |
| BLK | 400 | 0.0042 [0.0031, 0.0053] | 0.0042 [0.0031, 0.0053] | 0.0043 [0.0034, 0.0052] | 0.0042 [0.0032, 0.0052] | 1.020 [0.980, 1.061] | 1.708 [1.346, 2.070] | 0.0371 [0.0292, 0.0449] | 0.0823 [0.0752, 0.0895] | 0.0011 [-4.06e-04, 0.0026] | -5.13e-04 [-0.0011, 9.48e-05] |
| ADJ-OPP | 200 | 0.0053 [0.0030, 0.0076] | 0.0053 [0.0030, 0.0076] | 0.0060 [0.0039, 0.0082] | 0.0054 [0.0030, 0.0078] | 1.158 [0.756, 1.560] | 1.207 [0.778, 1.635] | 0.0262 [0.0169, 0.0355] | 0.1079 [0.0907, 0.1251] | 0.0046 [-0.0075, 0.0166] | -0.0023 [-0.0082, 0.0035] |
| ADJ-OPP | 400 | 0.0032 [0.0012, 0.0051] | 0.0032 [0.0012, 0.0051] | 0.0032 [0.0014, 0.0050] | 0.0032 [0.0014, 0.0050] | 1.026 [0.986, 1.067] | 1.289 [0.566, 2.013] | 0.0280 [0.0123, 0.0437] | 0.0742 [0.0614, 0.0871] | 9.50e-04 [2.13e-04, 0.0017] | -4.41e-04 [-7.64e-04, -1.18e-04] |
| NULL | 200 | 5.38e-04 [2.93e-04, 7.83e-04] | 5.38e-04 [2.93e-04, 7.83e-04] | 5.40e-04 [2.94e-04, 7.87e-04] | 5.40e-04 [2.97e-04, 7.83e-04] | 0.998 [0.980, 1.015] | 0.108 [0.059, 0.157] | n/a (s0 = 0) | 0.0289 [0.0250, 0.0328] | 6.18e-05 [-7.12e-05, 1.95e-04] | -3.19e-05 [-1.32e-04, 6.81e-05] |

d_H² = Hellinger² to the true predictive (`dist.*.plugin.h2`, closed form; store-BMA predictive from `dist.T.predictive.h2`, 4,000 x draws × 64 GH nodes, top-K 1,000 + stratified tail sample: relative s.e. ≤ 2.3 %, `h2_se_tail` ≤ 1.6 × 10⁻⁴; **omitted store mass and dropped mass are 0 in all 155 fits**, so no distance carries an omitted-mass correction). The oracle column is the engine's fit with S₀ known. Test MSE and mean log predictive density are on 10⁴ fresh rows, shown as differences from the oracle.

Posterior quantiles of d_H (store-BMA law; mean over datasets):

| design | n | post. d_H q05 | q50 | q95 (mean over datasets) | true d_H of the BMA = sqrt(d_H^2 BMA) |
|---|---|---|---|---|---|
| AR-strong | 100 | 0.1293 | 0.2117 | 0.3216 | 0.1639 |
| AR-strong | 200 | 0.0619 | 0.1038 | 0.1680 | 0.0682 |
| AR-strong | 400 | 0.0365 | 0.0616 | 0.1014 | 0.0380 |
| AR-strong | 800 | 0.0279 | 0.0463 | 0.0732 | 0.0318 |
| AR-weak | 100 | 0.2813 | 0.3225 | 0.3597 | 0.3028 |
| AR-weak | 200 | 0.0887 | 0.1463 | 0.2106 | 0.1124 |
| AR-weak | 400 | 0.0420 | 0.0718 | 0.1180 | 0.0514 |
| AR-weak | 800 | 0.0278 | 0.0462 | 0.0712 | 0.0313 |
| IND | 100 | 0.1184 | 0.1977 | 0.3060 | 0.1328 |
| IND | 200 | 0.0638 | 0.1049 | 0.1669 | 0.0705 |
| IND | 400 | 0.0512 | 0.0826 | 0.1232 | 0.0609 |
| BLK | 100 | 0.0835 | 0.1569 | 0.2830 | 0.0962 |
| BLK | 200 | 0.0737 | 0.1129 | 0.1649 | 0.0882 |
| BLK | 400 | 0.0534 | 0.0823 | 0.1217 | 0.0651 |
| ADJ-OPP | 200 | 0.0674 | 0.1079 | 0.1717 | 0.0769 |
| ADJ-OPP | 400 | 0.0468 | 0.0742 | 0.1122 | 0.0554 |
| NULL | 200 | 0.0133 | 0.0289 | 0.0841 | 0.0228 |

Fitted slope of log d_H² on log n:

| design | n values (datasets) | slope, store-BMA predictive d_H^2 | slope, HPM plug-in d_H^2 | slope, oracle d_H^2 |
|---|---|---|---|---|
| AR-strong | 100 (10), 200 (10), 400 (10), 800 (10) | -1.62 [-1.89, -1.32] | -1.67 [-1.95, -1.32] | -1.08 [-1.28, -0.90] |
| AR-weak | 100 (20), 200 (20), 400 (10), 800 (10) | -2.13 [-2.42, -1.88] | -2.21 [-2.53, -1.94] | -1.11 [-1.29, -0.96] |
| IND | 100 (5), 200 (5), 400 (5) | -1.27 [-2.10, -0.15] | -1.37 [-2.38, 0.14] | -0.76 [-1.19, -0.22] |
| BLK | 100 (5), 200 (5), 400 (5) | -0.58 [-0.81, -0.31] | -0.34 [-0.55, -0.05] | -0.31 [-0.50, -0.09] |
| ADJ-OPP | 200 (5), 400 (5) | -0.90 [-1.63, -0.33] | -0.74 [-1.56, -0.10] | -0.78 [-1.52, -0.14] |

**BMA / oracle ratio at n ≥ 400:** 1.02–1.04 in AR-strong (1.04 / 1.02), BLK (1.02) and ADJ-OPP (1.03); above 1 where HPM misses remain: AR-weak 1.40 (n 400) / 1.58 (n 800, interval [0.30, 2.87]) and IND n 400 1.26 [0.85, 1.66] (the r01 fit with one extra variable). (Descriptive: the oracle's own slope is −1.1 for the two AR designs; the BMA slopes steeper than −1 for AR-strong and AR-weak reflect the n = 100 → 200 step, where the fits move from missing active variables to recovering S₀. BLK's oracle slope is −0.31 on 5 datasets per n. No exponent is claimed.)

### 3.4 C7 evidence / merge

| design | n | log Z-hat (mean; range) | σ̂ = sd(log Ẑ_r) (mean [CI]; max) | robust σ̂ (mean) | max - median of log Z_r (mean; max) | R_eff / R' (min) | log Z-hat - log Z_T (mean; max) | omitted store mass (max) | island PIP sd, max (max) | sd of log Z-hat_occ(1000) over islands (max) |
|---|---|---|---|---|---|---|---|---|---|---|
| AR-strong | 100 | -130.5 (-137.2 to -117.7) | 0.0894 [-0.0037, 0.1826]; 0.4579 | 0.0740 | 0.185; 1.090 | 0.773 | 0.2965; 0.4343 | 0 | 0.01058 | 0.0247 |
| AR-strong | 200 | -199.7 (-212.9 to -177.2) | 0.0216 [0.0186, 0.0247]; 0.0277 | 0.0208 | 0.039; 0.076 | 0.999 | 0.1395; 0.2339 | 0 | 0.00374 | 0.0205 |
| AR-strong | 400 | -347.4 (-368.5 to -334.7) | 0.0182 [0.0139, 0.0224]; 0.0310 | 0.0170 | 0.034; 0.050 | 0.999 | 0.0689; 0.0956 | 0 | 0.00089 | 0.0143 |
| AR-strong | 800 | -623.1 (-671.1 to -568.6) | 0.0213 [0.0167, 0.0258]; 0.0316 | 0.0192 | 0.041; 0.058 | 0.999 | 0.0324; 0.0489 | 0 | 0.00044 | 0.0109 |
| AR-weak | 100 | -145.8 (-147.6 to -140.3) | 0.0187 [0.0102, 0.0271]; 0.0780 | 0.0169 | 0.032; 0.101 | 0.995 | 0.0645; 0.1728 | 0 | 0.00905 | 0.0217 |
| AR-weak | 200 | -264.7 (-282.4 to -241.4) | 0.0267 [0.0228, 0.0305]; 0.0407 | 0.0265 | 0.050; 0.078 | 0.999 | 0.1362; 0.1904 | 0 | 0.00502 | 0.0221 |
| AR-weak | 400 | -485.9 (-511.2 to -467.8) | 0.0178 [0.0151, 0.0206]; 0.0233 | 0.0146 | 0.042; 0.067 | 0.999 | 0.0653; 0.0851 | 0 | 0.00228 | 0.0160 |
| AR-weak | 800 | -888.7 (-920.2 to -861.4) | 0.0161 [0.0114, 0.0208]; 0.0258 | 0.0152 | 0.027; 0.053 | 0.999 | 0.0343; 0.0474 | 0 | 0.00077 | 0.0112 |
| IND | 100 | -128.6 (-141.1 to -114.3) | 0.0806 [-0.0291, 0.1903]; 0.2373 | 0.0611 | 0.208; 0.794 | 0.914 | 0.3526; 0.4867 | 0 | 0.00591 | 0.0252 |
| IND | 200 | -191.7 (-210.4 to -175.8) | 0.0237 [0.0170, 0.0304]; 0.0310 | 0.0229 | 0.041; 0.058 | 0.999 | 0.1422; 0.1621 | 0 | 0.00212 | 0.0148 |
| IND | 400 | -340.1 (-352.3 to -326.5) | 0.0173 [0.0112, 0.0235]; 0.0236 | 0.0147 | 0.032; 0.042 | 0.999 | 0.0698; 0.0839 | 0 | 0.00116 | 0.0140 |
| BLK | 100 | -126.4 (-135.3 to -116.2) | 0.0739 [0.0352, 0.1125]; 0.1108 | 0.0733 | 0.124; 0.171 | 0.989 | 0.3232; 0.4923 | 0 | 0.00780 | 0.0203 |
| BLK | 200 | -208.1 (-222.2 to -169.7) | 0.0262 [0.0180, 0.0343]; 0.0376 | 0.0220 | 0.052; 0.076 | 0.999 | 0.1343; 0.1614 | 0 | 0.00072 | 0.0157 |
| BLK | 400 | -357.5 (-391.7 to -334.6) | 0.0296 [0.0193, 0.0400]; 0.0384 | 0.0286 | 0.043; 0.063 | 0.999 | 0.0664; 0.0917 | 0 | 0.00090 | 0.0142 |
| ADJ-OPP | 200 | -229.0 (-241.8 to -220.1) | 0.2381 [-0.3520, 0.8281]; 1.0880 | 0.2215 | 0.431; 1.964 | 0.423 | 0.1008; 0.2053 | 0 | 0.00341 | 0.0161 |
| ADJ-OPP | 400 | -401.3 (-427.8 to -376.4) | 0.0201 [0.0124, 0.0278]; 0.0283 | 0.0213 | 0.036; 0.070 | 0.999 | 0.0639; 0.0785 | 0 | 0.00052 | 0.0127 |
| NULL | 200 | -289.9 (-289.9 to -289.9) | 0.0014 [6.91e-04, 0.0021]; 0.0023 | 0.0012 | 0.003; 0.005 | 1.000 | 0.0075; 0.0086 | 0 | 0.00014 | 0.0052 |

Evidence and merge checks, 155 fits at I_max = 0:
- **σ̂ label (review F5):** σ̂ in the C7 table and everywhere in this file is `evidence.sigma_hat` = **sd(log Ẑ_r)** over the islands, not sd(Ẑ_r / Ẑ) as PREREG §3.1 words M3 (erratum in PREREG §8); for r04 the two are 1.088 and 1.205.
- **Calibration flags are constants, reported as constants and kept out of any quality aggregate** (PREREG §7 last bullet; CAMPAIGN_FREEZE_ADDENDUM §2): `grid_unconverged` True 155/155, `checks_passed_calibration` False 155/155, `I_used` 0 155/155, `escalated` 0, the only calibration trigger fired is `grid_unconverged` (155). **The calibration's E1 and E2 are NOT EVALUATED at I_max = 0** (never 0 %).
- **Correction to the wording (L-10; now an erratum in PREREG §8 and the freeze addendum):** the eval record's `fit.meta.flags.{E1, E2, E3, low_empirical_ESS, checks_passed_final}` are **final-merge checks** computed at every I_max (`include/v4/merge.h:473-487` at F, confirmed by the Opus review: E1 = an island found a model better than the HPM by more than 1; **E2 = sd(log Ẑ_r) > 1**; E3 = local search improved the HPM; low ESS = a final-island ESS < N/2). Frequencies: **E1 0, E2 1, E3 0, low_empirical_ESS 6, occ_inhomogeneous 0, local_limit 0, final_local_limit 0, near_tie_truncated 0, ls0_hpm_changed 0, ls0_improved 0; checks_passed_final 148/155.** The six low-ESS fits: AR-weak n 100 r05, r06, r11, IND n 100 r02, r04, AR-strong n 800 r02 (`science_extras.md` X1).
- **FLAG for HQ: `4-ADJOPP-n200-r04-V-s1` (the one E2).** sd(log Ẑ_r) = σ̂ = 1.088 (robust 1.003), R_eff/R′ 0.423, max − median of log Ẑ_r +1.96, **log Ẑ = −227.811 against the deterministic lower bound log Z_T = −227.688: log Ẑ − log Z_T = −0.123, the only negative value of 155 (the SMC estimate sits below a known lower bound on Z)**; the 16 log Ẑ_r run from 2.07 below to 1.96 above their median (five islands at least 0.8 below it; max weight 0.32), i.e. some islands under-sample posterior mass and a few carry the mean. **Selection is intact:** HPM = MPM = S₀, F(HPM) = F(S₀), M1 0.0136, M2 0.00055, `occ_inhomogeneous` False, 1.54 core-h. It is the only fit of the leg with σ̂ > 0.46 and no other n = 200 fit exceeds 0.1; the 20 overlap V fits (I_max 3) and the 18 precision fits all stay ≤ 0.1; with 1 of 155 against 0 of 38 **no attribution to I_max = 0 is possible** (no I_max = 3 run of r04). **No bearing on the freeze** (the registered rule's output; H-30 "no post-hoc override"; §0-v2.3 targets never switch estimators); it concerns the precision of log Ẑ, not selection. **Optional attribution check, ≈ 3–4 core-h, HQ's call:** an I_max = 3 twin of r04 s1 (same data and engine seed, ≈ 2.2 core-h) plus an I_max = 0 seed-2 fit (≈ 1.5), folded into the next NOTS batch (V-N mini-leg or the G-B pilot batch), no wave of its own; it would say whether the heavy-tailed island spread follows the grid (I_max) or the seed.
- **§0-v2.3 targets at the production R′ = 16** (counted from the records and cross-checked by the review against the engine's own `pip.island_spread.target_met`, False in exactly these 14; reported per fit, **report-only: never switching an estimator**): M1 (sd of log Ẑ_occ(1000) ≤ 0.05) **0 misses** (max 0.025); **M2 (island PIP max sd ≤ 0.005): 14 of 155 fits above** (AR-strong n 100 r01, r04, r05; AR-weak n 100 r04, r06, r07, r12, r20; BLK n 100 r03, r05; IND n 100 r01, r03, r05; AR-weak n 200 r03 by 2 × 10⁻⁵): **13 at n = 100**, none at n ≥ 400; M3 (σ̂ goal ≤ 0.5) **1 miss** (the ADJ-OPP fit above; next largest 0.458, `4-AR-n100-r07-V-s1`). Median σ̂ by n: 0.035 / 0.024 / 0.017 / 0.020. **Scope correction (review F10):** the freeze addendum's "at 10⁴ every fit meets the §0-v2.3 targets by 3–54 ×" covers the 18 precision fits at R′ = 64, n = 200 only; the I_max decision used M2 only there. (Errata line in the addendum.)
- **log Ẑ − log Z_T** (the deterministic store lower bound) is positive in 154 of 155 fits; **it is negative in one: `4-ADJOPP-n200-r04-V-s1`, −0.123 (the flag above).** Cell means ≈ 0.30–0.35 at n = 100 (AR-weak 0.06, where the HPM is mostly empty), 0.10–0.14 at n = 200 (NULL 0.008), 0.064–0.070 at n = 400, 0.032–0.034 at n = 800; the omitted store mass is 0, so the positive gap is posterior mass outside the store, not truncation. Per-cell minimum, maximum and count below 0 (`science_extras3.md`):

| design | n | log Z-hat - log Z_T: mean | min | max | fits < 0 |
|---|---|---|---|---|---|
| AR-strong | 100 | 0.2965 | 0.1105 | 0.4343 | 0 |
| AR-strong | 200 | 0.1395 | 0.1078 | 0.2339 | 0 |
| AR-strong | 400 | 0.0689 | 0.0550 | 0.0956 | 0 |
| AR-strong | 800 | 0.0324 | 0.0229 | 0.0489 | 0 |
| AR-weak | 100 | 0.0645 | 0.0175 | 0.1728 | 0 |
| AR-weak | 200 | 0.1362 | 0.0535 | 0.1904 | 0 |
| AR-weak | 400 | 0.0653 | 0.0562 | 0.0851 | 0 |
| AR-weak | 800 | 0.0343 | 0.0245 | 0.0474 | 0 |
| IND | 100 | 0.3526 | 0.2721 | 0.4867 | 0 |
| IND | 200 | 0.1422 | 0.1230 | 0.1621 | 0 |
| IND | 400 | 0.0698 | 0.0551 | 0.0839 | 0 |
| BLK | 100 | 0.3232 | 0.2401 | 0.4923 | 0 |
| BLK | 200 | 0.1343 | 0.1137 | 0.1614 | 0 |
| BLK | 400 | 0.0664 | 0.0560 | 0.0917 | 0 |
| ADJ-OPP | 200 | 0.1008 | -0.1227 | 0.2053 | 1 |
| ADJ-OPP | 400 | 0.0639 | 0.0551 | 0.0785 | 0 |
| NULL | 200 | 0.0075 | 0.0068 | 0.0086 | 0 |

- Island stage count T of the frozen preliminary grid: mean 14.4 (n 100 13.9, 200 15.4, 400 12.8, 800 15.4).

### 3.5 A3: exact partition vs the default, 15 pairs (AR 10, BLK 5; paired by dataset, engine seed 1)

| pair (dataset) | default tag | HPM equal | HPM = S0 (A3 / default) | F(HPM) A3 - default | max abs(PIP_A3 - PIP_default) | log Z-hat A3 - default | island s.e. of the difference | d_H^2 BMA A3 / default | core-h A3 / default |
|---|---|---|---|---|---|---|---|---|---|
| AR-strong n200 r01 | VF | True | True / True | +0.00e+00 | 1.32e-06 | +0.00291 | 0.00910 | 0.00737 / 0.00737 | 2.18 / 1.43 |
| AR-strong n200 r02 | VF | True | True / True | +0.00e+00 | 7.90e-06 | +0.00273 | 0.00642 | 0.00402 / 0.00402 | 1.51 / 1.62 |
| AR-strong n200 r03 | VF | True | True / True | +0.00e+00 | 3.35e-05 | -0.00801 | 0.00664 | 0.00371 / 0.00371 | 1.11 / 1.22 |
| AR-strong n200 r04 | VF | True | True / True | +0.00e+00 | 9.14e-07 | -0.00336 | 0.00692 | 0.00180 / 0.00180 | 1.64 / 1.57 |
| AR-strong n200 r05 | V | True | True / True | +0.00e+00 | 1.27e-05 | +0.00352 | 0.01056 | 0.00434 / 0.00434 | 1.68 / 1.51 |
| AR-strong n200 r06 | V | True | True / True | +2.84e-14 | 7.92e-05 | -0.00037 | 0.00584 | 0.00674 / 0.00674 | 1.24 / 1.14 |
| AR-strong n200 r07 | V | True | True / True | +0.00e+00 | 5.82e-05 | +0.00807 | 0.00715 | 0.00466 / 0.00466 | 1.85 / 1.22 |
| AR-strong n200 r08 | V | True | True / True | +0.00e+00 | 2.50e-04 | +0.00481 | 0.00931 | 0.00542 / 0.00540 | 2.27 / 2.30 |
| AR-strong n200 r09 | V | True | True / True | +0.00e+00 | 1.80e-04 | +0.00290 | 0.00764 | 0.00503 / 0.00504 | 1.38 / 1.33 |
| AR-strong n200 r10 | V | True | True / True | +0.00e+00 | 3.75e-06 | -0.00521 | 0.00577 | 0.00471 / 0.00471 | 1.48 / 1.24 |
| BLK n200 r01 | V | True | True / True | +0.00e+00 | 1.16e-05 | -0.00481 | 0.00851 | 0.01174 / 0.01173 | 3.21 / 1.72 |
| BLK n200 r02 | V | True | True / True | +0.00e+00 | 3.00e-07 | -0.01572 | 0.01300 | 0.00669 / 0.00669 | 2.52 / 2.41 |
| BLK n200 r03 | V | True | True / True | +0.00e+00 | 1.03e-05 | +0.00684 | 0.00861 | 0.00771 / 0.00770 | 1.49 / 1.26 |
| BLK n200 r04 | V | True | True / True | +0.00e+00 | 7.67e-07 | -0.00718 | 0.00963 | 0.00745 / 0.00745 | 2.19 / 1.82 |
| BLK n200 r05 | V | True | True / True | +0.00e+00 | 5.30e-06 | -0.01172 | 0.00876 | 0.00586 / 0.00586 | 1.54 / 1.63 |

Summary: 15 pairs, HPM identical in 15, HPM = S0 in 15 (A3) / 15 (default); max over pairs and variables of abs(dPIP) = 2.50e-04; dlogZ (A3 - default) mean -0.00164 [-0.00554, 0.00226], largest abs 0.01572, largest abs in island s.e. of the difference 1.34; cost A3 1.82 [1.51, 2.13] vs default 1.56 [1.35, 1.77] core-h; pi_0(S0) NOT AVAILABLE (B4, HQ Q6); d_H between the two partitions' predictives NOT COMPUTABLE (the default-partition fits have no law.bin: law.bin was kept for the precision and A3 fits only).
Yardstick: the second-seed block below (AR-strong): max |ΔPIP| 8.7 × 10⁻⁴ (A3: 2.5 × 10⁻⁴), rms seed-to-seed difference of log Ẑ 0.0141 (A3 − default: rms 0.0070, largest 0.0157 against 0.0259). **The A3 pairs are closer than the seed-to-seed spread on every outcome reported**; both fits of a pair use the same engine seed, so this is a partition effect with the seed fixed. Not available: π₀(S₀) (B4 / HQ Q6, deferred); **d_H between the two partitions' predictives: computed for the 4 pairs whose default fit is a `VF` unit (AR r01–r04), which now hold `law.bin` and `data.bin`** (table below); **not computable for the other 11 pairs** (their default-partition fits have no `law.bin`; law was kept for the precision and A3 fits only). d_H² to the truth is equal to 3–4 significant digits in every pair.

**Partition d_H, 4 of 15 pairs** (`smcbvs4_xeval` b89cba4d sha `afef0e46…`, `cross --a <A3 law.bin> --b <VF law.bin> --truth … --data <VF data.bin> --data-b <VF data.bin>`: the A3 units hold no `data.bin`, the VF `data.bin` is the same dataset (X / y sha256 equal, guard passed); h2 is of the size of its own s.e., so d_H = √h2 is the upward-biased point value; files `leg_readback/a3_cross/`; script `science_extras3.py`):

|---|---|---|---|---|---|
| pair | d_H(A3F, VF) | h2 (s.e.) | d_H(VF, f*) | ratio |
|---|---|---|---|---|
| AR n200 r01 | 6.294e-04 | 3.96e-07 (1.2e-07) | 0.0858 | 0.0073 |
| AR n200 r02 | 5.716e-04 | 3.27e-07 (7.4e-08) | 0.0634 | 0.0090 |
| AR n200 r03 | 6.960e-04 | 4.84e-07 (1.8e-07) | 0.0609 | 0.0114 |
| AR n200 r04 | 5.193e-04 | 2.70e-07 (6.2e-08) | 0.0424 | 0.0122 |

The A3 − default distances (5–7 × 10⁻⁴) are of the size of the `VF` − T distances of §4 (5–8 × 10⁻⁴) and 0.7–1.2 % of d_H(VF, f\*). **Not available: π₀(S₀)** (B4 / HQ Q6).

### 3.6 Second seed: AR-strong n = 200, seeds 1 and 2 on 10 datasets

| dataset | HPM equal | HPM = S0 (s1 / s2) | max abs(PIP_s1 - PIP_s2) | log Z-hat s1 - s2 | d_H^2 BMA s1 / s2 |
|---|---|---|---|---|---|
| AR n200 r01 | True | True / True | 2.89e-04 | -0.02161 | 0.00737 / 0.00737 |
| AR n200 r02 | True | True / True | 4.37e-05 | -0.00718 | 0.00402 / 0.00400 |
| AR n200 r03 | True | True / True | 1.14e-04 | +0.00704 | 0.00371 / 0.00371 |
| AR n200 r04 | True | True / True | 6.36e-05 | -0.00020 | 0.00180 / 0.00180 |
| AR n200 r05 | True | True / True | 6.51e-04 | -0.01629 | 0.00434 / 0.00434 |
| AR n200 r06 | True | True / True | 2.04e-04 | +0.00920 | 0.00674 / 0.00675 |
| AR n200 r07 | True | True / True | 4.79e-04 | -0.01447 | 0.00466 / 0.00466 |
| AR n200 r08 | True | True / True | 5.72e-04 | -0.02593 | 0.00540 / 0.00542 |
| AR n200 r09 | True | True / True | 8.67e-04 | -0.01021 | 0.00504 / 0.00504 |
| AR n200 r10 | True | True / True | 1.55e-04 | -0.00937 | 0.00471 / 0.00471 |

Summary: HPM equal in 10/10 datasets; max abs(dPIP) 8.67e-04 (median 2.47e-04); seed-to-seed sd of log Z-hat (pooled, sqrt(mean d^2 / 2)) = 0.00998; largest abs(dlogZ) 0.02593; seed-to-seed d_H^2 difference: mean abs 7.93e-06.

### 3.7 NULL control (n = 200)

| run | n_null PIP > 0.5 | n_null PIP > 0.1 | sup PIP (eq) | HPM size | outcome | log Z-hat | sigma-hat |
|---|---|---|---|---|---|---|---|
| 4-NULL-n200-r01-VF-s1 | 0 | 0 | 0.0080 | 0 | correct | -289.896 | 0.0010 |
| 4-NULL-n200-r02-V-s1 | 0 | 0 | 0.0126 | 0 | correct | -289.881 | 0.0014 |
| 4-NULL-n200-r03-V-s1 | 0 | 0 | 0.0081 | 0 | correct | -289.900 | 0.0009 |
| 4-NULL-n200-r04-V-s1 | 0 | 0 | 0.0098 | 0 | correct | -289.872 | 0.0014 |
| 4-NULL-n200-r05-V-s1 | 0 | 0 | 0.0157 | 0 | correct | -289.854 | 0.0023 |

`n_null_gt_0.5 = 0` in 5 of 5 NULL fits (no violation to state); HPM empty in 5 of 5.

### 3.8 n-trend (the same numbers, one line per design)

| design | n | P(HPM = S0) | min PIP over S0 (mean) | sup null PIP (mean) | d_H^2 BMA (mean) | n d_H^2 / (s0 log p) | sigma-hat (mean) |
|---|---|---|---|---|---|---|---|
| AR-strong | 100 | 0.50 | 0.561 | 0.172 | 0.0314 | 0.068 | 0.0894 |
| AR-strong | 200 | 1.00 | 1.000 | 0.124 | 0.0048 | 0.021 | 0.0216 |
| AR-strong | 400 | 1.00 | 1.000 | 0.055 | 0.0015 | 0.013 | 0.0182 |
| AR-strong | 800 | 1.00 | 1.000 | 0.050 | 0.0011 | 0.019 | 0.0213 |
| AR-weak | 100 | 0.00 | 2.2e-03 | 0.117 | 0.0933 | 0.203 | 0.0187 |
| AR-weak | 200 | 0.50 | 0.560 | 0.151 | 0.0152 | 0.066 | 0.0267 |
| AR-weak | 400 | 1.00 | 0.966 | 0.090 | 0.0031 | 0.027 | 0.0178 |
| AR-weak | 800 | 0.90 | 1.000 | 0.123 | 0.0011 | 0.020 | 0.0161 |
| IND | 100 | 0.80 | 0.748 | 0.302 | 0.0244 | 0.053 | 0.0806 |
| IND | 200 | 1.00 | 1.000 | 0.095 | 0.0052 | 0.022 | 0.0237 |
| IND | 400 | 0.80 | 1.000 | 0.307 | 0.0042 | 0.036 | 0.0173 |
| BLK | 100 | 1.00 | 0.960 | 0.159 | 0.0095 | 0.021 | 0.0739 |
| BLK | 200 | 1.00 | 1.000 | 0.034 | 0.0079 | 0.034 | 0.0262 |
| BLK | 400 | 1.00 | 1.000 | 0.089 | 0.0043 | 0.037 | 0.0296 |
| ADJ-OPP | 200 | 1.00 | 1.000 | 0.131 | 0.0060 | 0.026 | 0.2381 |
| ADJ-OPP | 400 | 1.00 | 1.000 | 0.049 | 0.0032 | 0.028 | 0.0201 |
| NULL | 200 | 1.00 | n/a | 0.011 | 5.40e-04 | n/a | 0.0014 |

### 3.9 What §5 asks for that the records cannot give
- **π₀(S₀) and claim C3** (A3 column): no command or field at F (B4; HQ Q6 deferred); the `setup.bin` of the A3 pairs is kept for a later reader.
- **d_H between the exact and default partitions:** computed for 4 of 15 pairs (§3.5); the other 11 default-partition fits have no `law.bin` / `data.bin`. (**V − T Hellinger for `VF` is now available: §4.**)
- **"Same best model in 16 of 16 islands"**: no per-island HPM in the collected records (PREREG §3.1); `occ_inhomogeneous` (0/155) and the M = 1 occupancy are reported instead.
- **Calibration-stage E1 / E2** at I_max = 0: not evaluated by construction (reported as such, §3.4); no rebuild index or `I_used` frequency exists (constant 0).
- Everything else listed in §5 (C2, C4 with the reliability curve, C5 incl. the slope and posterior quantiles, C7, A3, second seed, null, cost, G-B inputs) is reported above or in §6.

## 4. ADDENDUM_2_VF: the 14 `VF` fits (I_max = 0) against the existing overlap T fits
**Result: no newly failed criterion; the VF carry-over is CLEAN.** Every v2 criterion that the overlap's V (I_max = 3) passed is passed by the 14 `VF` fits, **including H (14/14)**; the registered scorer, run in full mode on the 40-fit mixed set with the merged cross file, returns **CLEAN, 11/11 PASS**. I_max = 0 V agrees with T as I_max = 3 V did, on these 14 pairs, p = 10⁴, n = 200, single-seed pairs: this is **not** a statement that I_max = 0 is validated beyond them (ADDENDUM_2_VF "Reading"). `VF` and its I_max-3 twin share data and engine seed and differ only in the temperature grid, so the near-equality is a direct measurement of the grid change; it says nothing about rare heavy-tailed island spreads, which these 14 pairs did not contain (the one such case is the un-twinned ADJ-OPP r04, §3.4).
**Provenance (declared in ADDENDUM_2_VF before S1).**

| item | value |
|---|---|
| scorer | `results/overlap1e4/compare_overlap_v2.py` sha256 `4f402e5127efd4754cf25e4ade6ad799f697ebc28e1c657ff49f93fd2905b5c6`, unchanged (verified before and after) |
| VF wrapper (thin input builder: mirrors each `VF` run dir as a real dir of symlinks and rewrites `run_manifest.json` `run_id` `VF` → `V`; T fits mirrored as they are) | `leg_readback/scripts/vf_wrapper.py` sha256 **`f64cc97e3f8ba0744105559200f2eb1efa961f4101f8097adf415711b54e545a`**, recorded 2026-11-19T22:31:31Z in `vf_wrapper.sha256.v2` **before any scored output was read** (v1 logged 22:31:13Z). v1 (`8f891a923b78e58915e4415ee574181e2c19ed5f5cba742eebee9cf8eba83965`) symlinked the T run dirs themselves, which `os.walk` in the scorer does not descend into: its only output was 14 rows of `T: False`, every scored column NA; fixed (mirror as real dirs) before any scored value was seen. **v1's output was not kept; "no scored value" rests on the scorer's code path (`compare_overlap_v2.py:752-765`: with no T run found a `wave_check` row carries only the V side's `reasons`, `core_h`, `tier`, `flags`), which the Opus review confirmed.** Logged: §7 L-9. |
| invocations | (a) `--wave-check --records vf_pairs --cost-dir …` (the addendum's mode: per-(dataset, seed) pair table, island-only s.e., no verdict) **without** a cross file (first pass, no `law.bin` yet) and **with** `--cross-file cross_vf.json` (`vf/vf_pairs_cross/`); (b) the same on `v3_pairs` (the overlap's own V fits, I_max = 3) with `--cross-file W3_readback/cross_vt_all.json`; (c) **full verdict mode** on `v3_pairs` (reproduces the overlap result: **CLEAN, 11/11 criteria PASS**: toolchain check) and on `mixed40` = 20 T + the 14 `VF` + the 6 overlap V fits that have no `VF` twin (they stay as the I_max = 3 record, ADDENDUM_2_VF): first without cross values (INCOMPLETE solely because H was NOT_EVALUATED: `vf/mixed_full/`), then with `vf/cross_mixed40.json` = the 14 `VF` seeds from `cross_vf.json` + the 6 un-twinned seeds from the overlap cross file (input plumbing only): **CLEAN 11/11** (`vf/mixed_full_cross/`). The Opus review re-ran the mixed-set scorer independently and obtained the same. Outputs: `leg_readback/vf/{vf_pairs,vf_pairs_cross,v3_pairs,v3_full,mixed_full,mixed_full_cross}/`. |

**Per criterion** (dataset-level, full mode; the I_max = 3 column is the overlap's 40 fits re-scored by the same script):

| v2 criterion | overlap V, I_max = 3 (10 datasets) | `mixed40`: 14 `VF` + 6 I_max-3 fits (10 datasets) |
|---|---|---|
| D delivered; PAIR (X/y sha equal across fits of a dataset) | 40/40; PASS | 40/40; PASS |
| S1 HPM(V) = HPM(T), ≥ 9/10 datasets | 10/10 | **10/10** (14/14 `VF` pairs) |
| S2 T never reports a higher F | PASS (0 pairs) | **PASS (0 pairs)** |
| S3 MPM(V) = MPM(T) | PASS (0 of 20) | **PASS (0 of 20; 14/14 `VF` pairs)** |
| S4 NULL: no PIP > 0.5 | PASS | **PASS** (`VF` NULL r01 s1: `n_null_gt_0.5` 0) |
| P max_j abs(PIP_V − PIP_T) ≤ max(0.01, 3 s.e.) | PASS; worst ratio 0.0381 (ADJ-OPP r02) | **PASS; worst 0.0379** (ADJ-OPP r02) |
| E1 abs(log Ẑ_V − log Ẑ_T) ≤ 3 combined s.e. | PASS; worst ratio **1.761** (AR r04); s_V 0.00582 | **PASS; worst 1.382** (AR r01; AR r04 1.184); s_V 0.00607 (s_T 0.00324) |
| E2 log Z_T lower bound consistent | PASS | **PASS** |
| **H** Hellinger d_H(V, T) ≤ 10 % of d_H(T, f\*) | PASS; 10/10 with a cross value; worst ratio 0.0136 | **PASS, 10/10 with a cross value; the 14 `VF` pairs 0.0034–0.0136** (ADJ-OPP r02 s1 worst; dataset-level worst 0.0138; NULL r01 0.0034): d_H(VF, T) 0.9 × 10⁻⁴ – 1.1 × 10⁻³ against d_H(T, f\*) 0.026–0.19; `cross_vf.md` |
| C cost ≤ 1.5 × model (V 15.0) | PASS | **PASS** (largest `VF` fit 1.62 core-h) |

The scorer's outcome on `mixed40` with the merged cross file is **CLEAN (11/11 PASS)**; without cross values (the first pass) it was INCOMPLETE solely because H was NOT_EVALUATED. No criterion FAILED at any stage.
**How H was completed (late; §7 L-12):** the xeval `cross` command needs `law.bin` and `data.bin` of both fits, and the science units kept neither (LEG_PLAN §6.5). After the first draft of this read-back ops fetched them for the 14 `VF` units from NOTS scratch, verified their content hashes against the fit's own `law.bin.json` / `data.bin.json` (28/28), rewrote `SHA256SUMS` (old kept as `.prev`, `sha256sum -c` OK) and ran `smcbvs4_xeval` (b89cba4d, sha256 `afef0e463216edca…`, the overlap's tool, data-identity guard passed in all 14) with 14 self-checks of the VF laws and 14 of the T laws that agree with the engine's own d_H(T, f\*) to ≤ 1 × 10⁻⁹ relative (`leg_readback/cross_vf.{json,md}`, `cross_vf_raw/`, `vf_cross.sh`, `vf_merge_units.log`). The Opus review re-ran three pairs (ADJ-OPP r02 s1, AR r01 s1, NULL r01 s1): bit-identical h².
**Pair table** (`--wave-check`; V − T = log Ẑ difference with the pair's island s.e. in parentheses; V3 = the same fit at I_max 3; "tri" = triangle lower bound on d_H(V, T); dH_VT V3 / dH_T = the overlap's cross ratio; tier T = T's final tier / N):
```
pair | HPMeq VF/V3 | MPMeq | T>F | dlogZ VF (se) | dlogZ V3 (se) | pip ratio VF/V3 | dH_T | dH_V* VF/V3 | triangle VF/V3 | dH_VT/dH_T VF (cross) | dH_VT/dH_T V3 | coreh VF/V3 | tierT
ADJOPP-r01 s1 | True/True | True/True | False/False | +0.00105 (0.08) | -0.00070 (0.06) | 0.01473/0.01475 | 0.05799 | 0.05789/0.05787 | 9.956e-05/0.0001181 | 0.0126 | 0.01255 | 1.57/2.24 | 0/10000
ADJOPP-r02 s1 | True/True | True/True | False/False | -0.01064 (0.74) | -0.00895 (0.58) | 0.02569/0.02498 | 0.08163 | 0.08162/0.08169 | 1.422e-05/5.102e-05 | 0.01365 | 0.01329 | 1.61/2.82 | 0/10000
AR-r01 s1 | True/True | True/True | False/False | -0.01540 (2.25) | -0.01521 (2.41) | 0.008853/0.008853 | 0.08584 | 0.08583/0.08581 | 1.129e-05/2.701e-05 | 0.006915 | 0.00715 | 1.43/2.23 | 1/40000
AR-r01 s2 | True/True | True/True | False/False | -0.00165 (0.16) | -0.00406 (0.41) | 0.0239/0.02385 | 0.08571 | 0.08585/0.08584 | 0.0001328/0.0001307 | 0.007353 | 0.007494 | 1.48/2.22 | 0/10000
AR-r02 s1 | True/True | True/True | False/False | +0.00200 (0.29) | -0.00174 (0.25) | 0.01513/0.01513 | 0.06338 | 0.06337/0.06338 | 6.558e-06/4.607e-06 | 0.009162 | 0.008929 | 1.62/1.99 | 0/10000
AR-r02 s2 | True/True | True/True | False/False | +0.00333 (0.39) | +0.00187 (0.21) | 0.01439/0.01439 | 0.06327 | 0.06324/0.06325 | 2.661e-05/2.414e-05 | 0.009259 | 0.009009 | 1.26/2.08 | 0/10000
AR-r03 s1 | True/True | True/True | False/False | +0.00214 (0.42) | +0.00231 (0.48) | 0.01519/0.0152 | 0.06085 | 0.06091/0.0609 | 5.754e-05/5.449e-05 | 0.01234 | 0.01132 | 1.22/1.72 | 0/10000
AR-r03 s2 | True/True | True/True | False/False | -0.00421 (1.03) | -0.00430 (1.11) | 0.01055/0.01055 | 0.06085 | 0.06088/0.0609 | 3.498e-05/5.196e-05 | 0.01104 | 0.01179 | 1.2/1.71 | 0/10000
AR-r04 s1 | True/True | True/True | False/False | -0.00451 (0.65) | -0.00662 (0.93) | 0.006186/0.006186 | 0.04237 | 0.0424/0.04236 | 3.743e-05/2.035e-06 | 0.01231 | 0.01262 | 1.57/2.43 | 0/10000
AR-r04 s2 | True/True | True/True | False/False | -0.01169 (0.99) | -0.01710 (1.58) | 0.005465/0.005465 | 0.04252 | 0.04243/0.04237 | 9.465e-05/0.0001564 | 0.01254 | 0.01248 | 1.42/2.21 | 0/10000
ARweak-r01 s1 | True/True | True/True | False/False | -0.00834 (1.40) | -0.00792 (1.31) | 0.02081/0.02081 | 0.1357 | 0.1356/0.1358 | 4.07e-05/0.0001197 | 0.005572 | 0.005517 | 1.28/1.62 | 1/40000
ARweak-r02 s1 | True/True | True/True | False/False | +0.00110 (0.21) | +0.00175 (0.33) | 0.02004/0.02004 | 0.188 | 0.188/0.1879 | 6.775e-05/0.0001194 | 0.003805 | 0.003379 | 1.19/2.08 | 0/10000
IND-r01 s1 | True/True | True/True | False/False | -0.00147 (0.23) | -0.00137 (0.21) | 0.1264/0.1264 | 0.06759 | 0.06755/0.06757 | 3.286e-05/1.548e-05 | 0.01317 | 0.0122 | 1.61/2.4 | 0/10000
NULL-r01 s1 | True/True | True/True | False/False | +0.00040 (1.10) | +0.00040 (1.10) | 0.001808/0.001808 | 0.02579 | 0.02579/0.02579 | 1.735e-07/1.592e-07 | 0.003407 | 0.003464 | 0.445/0.5 | 0/10000
```
Reading of the pair table (single-seed pairs are single pairs): every `VF` pair has HPM and MPM equal to T and |F(HPM)_V − F(HPM)_T| ≤ 1.1 × 10⁻¹³ (the same bound holds at I_max 3); `VF` log Ẑ differences to T are of the same size and sign pattern as their I_max-3 twins (the largest, AR r01 s1: −0.0154 = 2.25 island s.e. at I_max 0, −0.0152 = 2.41 at I_max 3, against a T fit at tier 1, N 40,000; the AR r04 s2 pair −0.0117 vs −0.0171). Per-fit `VF` − I_max-3 log Ẑ: mean +0.00098, sd 0.0019, range −0.0017 to +0.0054 over the 14 fits (`vf/vf_offset.json`), smaller than the pooled seed-to-seed sd of V (0.0058). The `vf` row of the offset surface is in §5.

## 5. Offset, final (PREREG §4: ONE measurement; no pass/fail)
**Run:** `precision_offset.py` (sha256 `cbbc23012e6900ff7798267cc7325816ad0b8312ec6e26fd09972adc9780d300`, verified, unchanged) on `records/overlap1e4/{W0,W1,W2,W3}` + `records/precision1e4/{A0,P1,P2,P3,P4}`: 58 fits found, 38 V fits used (10 datasets with a T reference), 0 dropped, 2 duplicates resolved (the W0 rebuild dirs `.T2` / `.V2`; newest eval wins, as in the overlap verdict); output in `leg_readback/offset/`. **`offset_report.md` and `offset_per_fit.csv` are byte-identical to the FZ outputs, `offset.json` equal apart from the record paths:** no record of the registered run-id pattern has been added since FZ (the science `V` ids at n = 200 are `VF` or have no T reference; the B1 ids and `VF` ids are outside the registered pattern). The additions are by hand (below). s_T = 0.00324 (10 df); s_rep(k = 64) = 0.00247 (9 dataset-cells).
**Surface** δ(N, m, I_max, k) = mean over datasets of [V block-mean log Ẑ − T reference]:

| src | N | m | I_max | k | datasets | fits | delta | se (clustered) | 95% t-CI | neg | delta / s_T | delta (T tier-0 ref only; datasets) | Jensen mean | occ offset |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| prec | 2500 | 1 | 0 | 4 | 3 | 6 | -0.00696 | 0.00118 | -0.01206 .. -0.00186 | 3/3 | -2.15 | -0.00801 (3) | -6.3e-05 | - |
| prec | 2500 | 1 | 0 | 8 | 3 | 6 | -0.00692 | 0.00118 | -0.01202 .. -0.00183 | 3/3 | -2.13 | -0.00797 (3) | -3.1e-05 | - |
| prec | 2500 | 1 | 0 | 16 | 3 | 6 | -0.00691 | 0.00118 | -0.01199 .. -0.00182 | 3/3 | -2.13 | -0.00796 (3) | -1.6e-05 | - |
| prec | 2500 | 1 | 0 | 32 | 3 | 6 | -0.00690 | 0.00118 | -0.01198 .. -0.00182 | 3/3 | -2.13 | -0.00795 (3) | -7.8e-06 | - |
| prec | 2500 | 1 | 0 | 64 | 3 | 6 | -0.00690 | 0.00118 | -0.01198 .. -0.00182 | 3/3 | -2.13 | -0.00795 (3) | -3.9e-06 | +0.00058 |
| ovl | 2500 | 1 | 3 | 4 | 10 | 20 | -0.00397 | 0.00141 | -0.00716 .. -0.00079 | 7/10 | -1.22 | -0.00435 (10) | -5.9e-05 | - |
| ovl | 2500 | 1 | 3 | 8 | 10 | 20 | -0.00395 | 0.00141 | -0.00714 .. -0.00077 | 7/10 | -1.22 | -0.00433 (10) | -2.9e-05 | - |
| ovl | 2500 | 1 | 3 | 16 | 10 | 20 | -0.00394 | 0.00141 | -0.00712 .. -0.00076 | 7/10 | -1.21 | -0.00431 (10) | -1.5e-05 | +0.00029 |
| prec | 2500 | 1 | 3 | 4 | 3 | 6 | -0.00605 | 0.00171 | -0.01341 .. +0.00130 | 3/3 | -1.87 | -0.00710 (3) | -4.9e-05 | - |
| prec | 2500 | 1 | 3 | 8 | 3 | 6 | -0.00603 | 0.00171 | -0.01339 .. +0.00133 | 3/3 | -1.86 | -0.00708 (3) | -2.5e-05 | - |
| prec | 2500 | 1 | 3 | 16 | 3 | 6 | -0.00602 | 0.00171 | -0.01339 .. +0.00135 | 3/3 | -1.85 | -0.00707 (3) | -1.2e-05 | - |
| prec | 2500 | 1 | 3 | 32 | 3 | 6 | -0.00601 | 0.00171 | -0.01338 .. +0.00135 | 3/3 | -1.85 | -0.00706 (3) | -6.2e-06 | - |
| prec | 2500 | 1 | 3 | 64 | 3 | 6 | -0.00601 | 0.00171 | -0.01338 .. +0.00136 | 3/3 | -1.85 | -0.00706 (3) | -3.1e-06 | -0.00029 |
| prec | 2500 | 4 | 3 | 4 | 3 | 6 | -0.00592 | 0.00140 | -0.01195 .. +0.00011 | 3/3 | -1.82 | -0.00697 (3) | -1.4e-05 | - |
| prec | 2500 | 4 | 3 | 8 | 3 | 6 | -0.00591 | 0.00140 | -0.01195 .. +0.00013 | 3/3 | -1.82 | -0.00696 (3) | -7.2e-06 | - |
| prec | 2500 | 4 | 3 | 16 | 3 | 6 | -0.00591 | 0.00140 | -0.01194 .. +0.00012 | 3/3 | -1.82 | -0.00696 (3) | -3.6e-06 | - |
| prec | 2500 | 4 | 3 | 32 | 3 | 6 | -0.00591 | 0.00140 | -0.01194 .. +0.00013 | 3/3 | -1.82 | -0.00696 (3) | -1.8e-06 | - |
| prec | 2500 | 4 | 3 | 64 | 3 | 6 | -0.00591 | 0.00140 | -0.01194 .. +0.00013 | 3/3 | -1.82 | -0.00696 (3) | -8.9e-07 | -0.00059 |

**Contrasts read under §4.4** (T reference cancels; P2 spans and the knob contrasts; the 14 R′ steps are descriptive and not read; multiplicity: 4 P2_span, 14 R_step, 2 knob):

| contrast | kind | datasets | mean | se (clustered) | 95% t-CI | neg | Jensen pred. | slope - Jensen (95% CI) |
|---|---|---|---|---|---|---|---|---|
| R' SPAN (2500, 1, 0, 'prec') k 4 -> 64 | P2_span | 3 | +0.00006 | 0.00000 | +0.00004 .. +0.00008 | 0/3 | +5.9e-05 | +0.00000 (-0.00001 .. +0.00002) |
| R' SPAN (2500, 1, 3, 'ovl') k 4 -> 16 | P2_span | 10 | +0.00003 | 0.00001 | +0.00002 .. +0.00005 | 0/10 | +4.4e-05 | -0.00001 (-0.00002 .. +0.00000) |
| R' SPAN (2500, 1, 3, 'prec') k 4 -> 64 | P2_span | 3 | +0.00004 | 0.00000 | +0.00002 .. +0.00006 | 0/3 | +4.6e-05 | -0.00000 (-0.00003 .. +0.00002) |
| R' SPAN (2500, 4, 3, 'prec') k 4 -> 64 | P2_span | 3 | +0.00001 | 0.00000 | +0.00001 .. +0.00002 | 0/3 | +1.3e-05 | -0.00000 (-0.00001 .. +0.00001) |
| m: (2500,4,3) - (2500,1,3) at k=64 | knob | 3 | +0.00010 | 0.00045 | -0.00183 .. +0.00204 | 1/3 | - | - |
| I_max: (2500,1,0) - (2500,1,3) at k=64 | knob | 3 | -0.00089 | 0.00072 | -0.00398 .. +0.00220 | 2/3 | - | - |

**Declared headline lines (§4.3).** **P1** δ(ovl, 2,500, 1, 3, k = 16) = **−0.00394** [−0.00712, −0.00076], 7/10 negative, −1.21 s_T: reproduced. **P2** (R′ span with the Jensen prediction): overlap k 4 → 16: +3.5 × 10⁻⁵ vs Jensen +4.4 × 10⁻⁵, slope − Jensen −0.9 × 10⁻⁵ (−2.2 × 10⁻⁵, +0.3 × 10⁻⁵); leg k 4 → 64: m1·I3 +4.3 × 10⁻⁵ vs +4.6 × 10⁻⁵, m4·I3 +1.3 × 10⁻⁵ vs +1.3 × 10⁻⁵, **m1·I0 +6.0 × 10⁻⁵ vs +5.9 × 10⁻⁵**: **all four intervals of slope − Jensen contain 0**. **P3** m: **+0.00010** [−0.00183, +0.00204]; I_max: **−0.00089** [−0.00398, +0.00220]; **N: not computable** (the 12 N = 10⁴ fits are held, B2 / HQ Q1; the V-N mini-leg supplies it). No contrast interval excludes 0: **no FINDING** (§3.3 / §4.4).
**Reading allowed by §4.4:** δ is the same at k = 4 and k = 64 within the Jensen term and the studied knob contrasts include 0, so the offset is **not** an R′, grid, calibration or (m, I_max) effect at these settings; it is either noise or a difference between the V and T arms that none of the studied knobs changes. **N was not tested** (R9). No statement "V is biased low" follows from δ alone (§4.4 last bullet). For completeness, without reading: the three leg cells at k = 64 are all negative (3/3 datasets), −0.00601 (m1·I3), −0.00591 (m4·I3), −0.00690 (m1·I0), half-widths 0.0074 / 0.0060 / 0.0051; the I_max = 0 cell's t interval, [−0.01198, −0.00182], excludes 0 (df = 2; not one of the §4.3 headline lines); against the T tier-0 reference the three are −0.0071 / −0.0070 / −0.0080. The §4.5 resolution applies: a 3-dataset cell cannot resolve an offset of the overlap's size (−0.0039), the realised half-widths (0.005–0.007) match the predicted ≈ 0.0076, and the R′ slope and knob contrasts do not carry the T noise.
**Additions by hand** (`leg_readback/scripts/vf_offset.py`, sha256 `6ac532b7ff847c191c00bca87d22894347665f0a9a5ac71bbef5f55e310372d5`, importing the registered reader unchanged; not part of the registered surface, not read):

| row | δ (k = 16) | 95 % t-CI | negative | per-dataset values |
|---|---|---|---|---|
| **`vf`**: the 14 `VF` fits, 10 datasets, (2,500, 1, 0), R′ = 16 | **−0.00300** (−0.92 s_T; k = 4: −0.00304; Jensen −1.6 × 10⁻⁵) | [−0.00609, +0.00009] | 7/10 | ADJ-OPP r01 −0.0004, r02 −0.0072; AR r01 −0.0085, r02 +0.0027, r03 −0.0010, r04 −0.0081; AR-weak r01 −0.0076, r02 +0.0008; IND −0.0009; NULL +0.0003 |
| the same 14 fits at I_max = 3 (the overlap twins) | −0.00363 | [−0.00693, −0.00033] | 7/10 | |
| `vf` − I_max 3 twin, paired by dataset (descriptive) | +0.00063 | [−0.00055, +0.00182] | 5/10 | |
| **B1 point** (AR-weak p = 10⁴, n = 100, one dataset; V − T, 2 seeds; both T fits tier 1, N 40,000) | **−0.00042** (−0.13 s_T) | none (one dataset) | seeds +0.00197 / −0.00282 (spread 0.00339 = 1.05 s_T) | |

The `vf` row uses the same T reference as the overlap cell; for 6 of the 10 datasets it rests on a single `VF` fit. Recorded arm of the 14 `VF` fits verified in the script (N 2,500, m 1, I_max 0, I_used 0, rule bounded).

## 6. Cost
**Leg ledger:** `prior_after_S10.json` = **462.48 core-h** for 194 fits (2-decimal rounding per fit; 462.46 unrounded from the per-fit `cost_<run>.json`), `VN_ID_1` (F2 identity check, 1.99) separate: leg + VN_ID_1 = 464.47. Split: A0 24.83 + P1–P4 120.85 (= precision 145.68 incl. the A3 canary and XB) + B1 82.35 + S1–S10 234.43. **Against the plan figure 4,127 (MANIFEST_CELLS v0.4): 11.2 %.** Against the committed quote of the scope actually run: 505.1 (released scope at I_max = 0, `quote_output_freeze_i0.txt`) + B1 115 = 620 → **0.75 ×** (measured-calibration variant 460.5 + 115). Cumulative stop 900 never approached; **no soft or hard per-fit trip in the leg** (every wave clean).
**Per wave** (billed vs quote; wave stop = 2 × quote):

| wave | fits | actual | quote | ratio | note |
|---|---|---|---|---|---|
| A0 / P1 / P2 / P3 / P4 | 4 each | 24.83 / 30.25 / 30.97 / 21.60 / 38.04 | 25 / 30 / 30 / 25 / 45 | 0.99 / 1.01 / 1.03 / 0.86 / 0.85 | |
| B1 | 4 | 82.35 | 115 | 0.72 | T 36.63 / 44.21 vs report line 172.5 |
| S1 / S2 / S3 / S4 | 28 / 28 / 4 / 15 | 40.63 / 41.86 / 1.76 / 27.30 | 50 / 40 / 5 / 35 | 0.81 / 1.05 / 0.35 / 0.78 | |
| S5 / S6 | 28 / 12 | 30.32 / 19.02 | 30 / 15 | 1.01 / **1.27** | S6 above its quote, inside its stop (30) |
| **S7** (n = 400 pilot) | 7 | 7.42 | 20 | 0.37 | gate: re-quotes S8 |
| **S8** | 28 | 38.70 | **45 (re-quoted; committed 70)** | 0.86 | |
| **S9** (n = 800 pilot) | 7 | 10.32 | 35 | 0.29 | gate: re-quotes S10 |
| **S10** | 13 | 17.10 | **25 (re-quoted; committed 55)** | 0.68 | |

**The S8 / S10 re-quotes** (manager, pilot gates; `OPS_PREC.md`): after S7 (n = 400: ADJ-OPP 1.13, AR 0.88 core-h per fit, 0.24 × the committed class E) the n = 400 classes were set conservatively to the measured **n = 200** means (AR 1.52, AR-weak 1.47, BLK 1.77, IND 1.47) → E ≈ 43, **S8 quote 45 (stop 90)**; after S9 (AR n = 800 mean 1.47, 0.21 × E) S10 was quoted at 3 × 1.47 + 10 × 1.67 ≈ 21 → **25 (stop 50)**. Hard per-fit lines stayed pinned to the committed table (sha256 `c0fcd139db0a…`); only the soft line of `prec N2500 m4 I3` was moved (18.5 → 21.0, manager F2, before P4). The measured S8 actual (38.7) fell below the re-quote; in S8 the BLK fits (1.88–2.91 core-h, mean 2.32) were the one class above the n = 200 mean it used.
**Per class vs the committed class model, and the G-B cost criterion** (HQ Q4: class mean ≤ 1.5 × model **and** no single fit > 2.5 × model; every fit above 1.5 × listed; "model" = the committed table, never re-fitted; fits of all 194 incl. B1 V, A0 canaries and the 14 `VF`):

| class | fits | mean | max | E | mean/E | max/E | class mean <= 1.5E | no fit > 2.5E | fits > 1.5E |
|---|---|---|---|---|---|---|---|---|---|
| A3 n200 | 16 | 1.87 | 3.21 | 2.76 | 0.68 | 1.16 | yes | yes | 0 |
| ADJOPP n200 | 5 | 1.46 | 1.61 | 2.69 | 0.54 | 0.60 | yes | yes | 0 |
| ADJOPP n400 | 5 | 1.13 | 1.42 | 4.62 | 0.24 | 0.31 | yes | yes | 0 |
| AR n100 | 10 | 1.67 | 2.07 | 1.55 | 1.08 | 1.33 | yes | yes | 0 |
| AR n200 | 21 | 1.52 | 2.64 | 2.18 | 0.70 | 1.21 | yes | yes | 0 |
| AR n400 | 10 | 1.12 | 1.53 | 3.64 | 0.31 | 0.42 | yes | yes | 0 |
| AR n800 | 10 | 1.49 | 2.06 | 6.94 | 0.21 | 0.30 | yes | yes | 0 |
| ARweak n100 | 22 | 0.76 | 1.28 | 1.36 | 0.56 | 0.94 | yes | yes | 0 |
| ARweak n200 | 20 | 1.47 | 1.96 | 1.87 | 0.78 | 1.05 | yes | yes | 0 |
| ARweak n400 | 10 | 1.23 | 1.67 | 3.05 | 0.40 | 0.55 | yes | yes | 0 |
| ARweak n800 | 10 | 1.25 | 1.54 | 5.67 | 0.22 | 0.27 | yes | yes | 0 |
| BLK n100 | 5 | 1.74 | 2.05 | 1.58 | 1.10 | 1.30 | yes | yes | 0 |
| BLK n200 | 5 | 1.77 | 2.41 | 2.22 | 0.80 | 1.09 | yes | yes | 0 |
| BLK n400 | 5 | 2.32 | 2.91 | 3.72 | 0.62 | 0.78 | yes | yes | 0 |
| IND n100 | 5 | 1.73 | 2.20 | 1.62 | 1.07 | 1.36 | yes | yes | 0 |
| IND n200 | 5 | 1.47 | 1.61 | 2.30 | 0.64 | 0.70 | yes | yes | 0 |
| IND n400 | 5 | 1.07 | 1.26 | 3.89 | 0.27 | 0.33 | yes | yes | 0 |
| NULL n200 | 5 | 0.44 | 0.50 | 0.51 | 0.87 | 0.97 | yes | yes | 0 |
| T law | 2 | 40.42 | 44.21 | (no class: T fits, report line 172.5) | - | - | - | - | - |
| prec N2500 m1 I0 | 6 | 5.00 | 5.55 | 5.76 | 0.87 | 0.96 | yes | yes | 0 |
| prec N2500 m1 I3 | 6 | 6.02 | 7.24 | 6.28 | 0.96 | 1.15 | yes | yes | 0 |
| prec N2500 m4 I3 | 6 | 12.37 | 14.01 | 12.36 | 1.00 | 1.13 | yes | yes | 0 |

**G-B cost criterion: PASS in every one of the 21 model classes; 0 fits above 1.5 × and none above 2.5 × their committed model** (largest single fit: IND n 100 at 1.36 ×, AR n 100 1.33 ×, BLK n 100 1.30 ×; largest class mean: BLK n 100 1.10 ×, AR n 100 1.08 ×, IND n 100 1.07 ×). The review's own recomputation differs only in the 2nd decimal (AR n 100 max / E 1.34 vs 1.33; IND n 400 mean / E 1.06 vs 1.07; largest single fit 1.358 ×, IND n 100 r05), immaterial. The 2 B1 T fits are outside the table (36.6 / 44.2 core-h, report line 172.5). Caveat: the science classes' committed E is the baseline (I_max 3) table; at I_max = 0 the fits are far under it (mean / E 0.21–0.62 at n ≥ 400: AR-strong 0.31 / 0.21, AR-weak 0.40 / 0.22, IND 0.27, ADJ-OPP 0.24, BLK 0.62); this criterion, as registered, is checked against that table.
**n-scaling (the planning model assumed per-step cost × nf(n) = 0.7 / 1.0 / 1.6 / 2.8 for n = 100 / 200 / 400 / 800):**

| design | n=100 | n=200 | n=400 | n=800 | ratio 100/200 | ratio 400/200 | ratio 800/200 | mean island T (100/200/400/800) | mean islands core-h (100/200/400/800) |
|---|---|---|---|---|---|---|---|---|---|
| AR-strong | 1.67 | 1.46 | 1.12 | 1.49 | 1.14 | 0.77 | 1.02 | 22.10/15.40/9.30/19.80 | 1.47/1.27/0.91/1.21 |
| AR-weak | 0.77 | 1.47 | 1.23 | 1.25 | 0.52 | 0.84 | 0.85 | 4.90/16.15/10.50/11.10 | 0.61/1.27/0.99/1.02 |
| IND | 1.73 | 1.47 | 1.07 | - | 1.18 | 0.73 | - | 23.00/17.20/8.20/- | 1.52/1.22/0.82/- |
| BLK | 1.74 | 1.77 | 2.32 | - | 0.98 | 1.31 | - | 24.20/23.60/30.20/- | 1.52/1.56/2.05/- |
| ADJ-OPP | - | 1.46 | 1.13 | - | - | 0.77 | - | -/17.00/11.60/- | -/1.28/0.92/- |
| NULL | - | 0.44 | - | - | - | - | - | -/1.00/-/- | -/0.32/-/- |

- **n = 400 and n = 800 are cheaper than or equal to n = 200** in AR-strong (0.77 × / 1.02 ×), AR-weak (0.84 × / 0.85 ×), IND (0.73 × at 400), ADJ-OPP (0.77 × at 400): against the model's 1.6 × / 2.8 ×. **Exception: BLK n = 400 costs 1.31 × its n = 200 mean (all 5 fits above it; island T 30 vs 24 stages)**, still below 1.6 ×. n = 100 is not cheaper than n = 200 for AR-strong (1.14 ×), IND (1.18 ×), BLK (0.98 ×) against the model's 0.7 ×, only for AR-weak (0.52 ×: the grid has ~5 stages when nothing is detected).
- **Cause (descriptive regression on the 150 non-NULL science fits, not a registered analysis):** islands core-h = −0.028 + 0.0440 × (T + 12), R² 0.80, where T = island stage count of the frozen preliminary grid; adding n / 200 as a regressor gives a coefficient of −0.010 (≈ 0). Per island per stage the cost is flat in n (2.4 / 2.8 / 2.7 / 2.6 × 10⁻³ core-h for n = 100 / 200 / 400 / 800), and T did not grow with n (mean 22 / 15 / 9 / 20 for AR-strong). The planning model's per-step n-scaling is not seen at p = 10⁴ in n = 100–800; the 10⁵ / 1M re-size should consider T rather than nf(n) (post hoc, at p = 10⁴; T at 10⁵ is unknown).
**Stage split, wall and memory** (science V fits by n; requests: setup 8 G, calibrate 8 G, islands 4 G, merge 4 G, eval 8 G; time limits 15 / 45 / 45 / 15 / 20 min):

| n | fits | setup | calibrate | islands | merge | eval | max wall s cal / isl / merge | max RSS MB (setup / cal / isl / merge / eval) |
|---|---|---|---|---|---|---|---|---|
| 100 | 40 | 0.020 | 0.083 | 1.048 | 0.054 | 0.028 | 29 / 145 / 40 | 167 / 583 / 344 / 705 / 857 |
| 200 | 60 | 0.028 | 0.087 | 1.211 | 0.049 | 0.029 | 33 / 165 / 43 | 359 / 801 / 432 / 869 / 774 |
| 400 | 35 | 0.047 | 0.090 | 1.082 | 0.061 | 0.038 | 35 / 168 / 40 | 383 / 812 / 456 / 888 / 760 |
| 800 | 20 | 0.060 | 0.089 | 1.116 | 0.064 | 0.041 | 32 / 117 / 43 | 389 / 856 / 494 / 856 / 766 |

Peak RSS is 0.89 GB against the 4 G request of the merge (22 %); the longest wall of any stage is 168 s (islands). A3 (exact partition) setup: mean 0.036 core-h, ≤ 19 s, peak 0.87 GB.
**I_max = 0 saving, measured at the production R′ = 16:** the 14 `VF` fits cost 1.35 core-h mean against 2.02 for their I_max = 3 twins (−33 %; the 13 non-NULL pairs −34 %); FZ's estimate was −39 % (R′ = 64 stage costs extrapolated).

## 7. Tooling notes and deviations (one line each; ids L-n)

| id | line |
|---|---|
| **L-1** | **A0 throttle false alarm** (monitor STOP at the A0 probe 10:17:15Z): pending reason `JobArrayTaskLimit` on `2791240_[9-16%8]` was our own `%8` array throttle, not a cluster limit; nothing cancelled; `stop_rules_prec.py` narrowed (`JobArrayTaskLimit` with `%k` → INFO, without `%k` still STOP; 26/26 tests; backup `.bak_20261119`). |
| **L-2** | **P1 monitor miss and the WAVE STATE fix:** the Haiku monitor missed the end of P1 (≈ 11:46Z) and kept probing ≈ 2.7 h (≈ 8 extra NOTS probes) until the manager deleted schedule 87b0cd35; fix: every probe verdict prints `WAVE STATE: RUNNING|ENDED` (ENDED = no squeue row, every sacct row terminal, every submitted job seen), and the prompt says to stop on ENDED. |
| **L-3** | **S2 monitoring gap:** the S2 job-id hand-off to the monitor was never sent, so S2 ran unmonitored ≈ 1.5 h (it ended clean at 18:26Z, first probe); fix: ops sends the monitor a `START <wave>` line after each wave's last batch (worked for S3–S10). |
| **L-4** | **Freeze-script `cost_batch` defect:** registered `precision_freeze.py` globs `cost_*.json`, which also matches the per-batch `cost_batch.json` (no `stages`) → `KeyError: 'stages'` (`:99`); run on a directory of per-run cost files only, output identical to the Opus check's; registered file not edited (PREREG §8, FZ_CHECK_OPUS F2); the V-N mini-leg needs the same clean cost dir. |
| **L-5** | **1-ulp xeval self-checks:** overlap W2 AR r01 T s2 differed by 1 ulp (2⁻⁵³ of 1 − X; deterministic; W3 12/12 bit-exact); B1: 2 of 4 self-checks (V s1, T s1) 1.1 × 10⁻¹⁶ off; not material (cross-Hellinger values are 10⁻⁷-scale); cause untested (g++ 11.5 Owls vs 14.3 NOTS libm / rounding is the working hypothesis). |
| **L-6** | **`starts.jsonl` / `ends.jsonl` losses:** non-atomic `printf >>` from many nodes on shared scratch: A0 `PL_A0_1` has ≈ 25 of 136 start records lost (111 `"stage"` tokens; 1 glued line, 2 fragments), `ends.jsonl` 135/136; expected in every 136-task batch; `submissions.jsonl` is intact; cost and records come from sacct + `p1m_cost.py`, never from these files (a per-task record file would be a later driver PR). |
| **L-7** | **Builds:** the overlap rebuilt 4 times per arm (verdict deviation 7; W0 V `dd5af0cd` vs the doc's `ba569a33` was a doc slip, A0 check F7); **this leg built the V arm once (`d0c30b65`, A0) and the T arm once (`09249230`, B1)**, every later batch a `cp -p` + sha256 check (`COPYBIN`); the XB check (A0) showed the leg build bit-equal to both W0 overlap builds on `4-AR-n200-r01-V-s1`; 194/194 units carry exactly one sha256; the "14 reused fits exempt by their shas" rule was never used (they were re-run as `VF`). |
| **L-8** | **Science analysis script not registered before the first science read-back (PREREG §5 required a short addendum with script, sha256 and self-test before S1's read-back). A moderate procedural breach; it touches no gate** (the only §5 gate quantity, completion, was re-derived independently by the review). No such addendum exists; the per-wave read-backs were completion, cost and identity only. **Sha chain** (`leg_readback/science_script.sha256`, recorded before each run): `science.py` `9a2cc1cb772a…` → `3b3b1254c67f…` → **`7c5c7feeee09733ea4e88fc134b55ae680c581aa6b23609718182d411e3acf78`** (two crash fixes, no output written); helper self-test 16/16 on synthetic data (`science/test_science_helpers_output.txt`); reader hand-checked on 3 fits. **Qualification of "no science value had been read":** the VF scorer outputs (V − T and log Ẑ values for 14 of the 155 science fits, no C2–C5 quantity) existed at 16:32 CST and the `vf_offset` / `costs` outputs at 16:33, before the sha was recorded at 16:37; the sha file is self-attested (rewritten when the extras were appended). Post-read additions, logged as such: `science_extras.py` `390383e4…`, `science_extras2.py` `570aa665…`, `science_extras3.py` `eb01236d…`; `vf_offset.py` and `costs.py` have post-hoc shas. The script has no threshold and no pass/fail. **Carry rule for G-B: register the analysis script before the first read.** Entered in PREREG §8 (2026-11-19). |
| **L-9** | **VF wrapper revision** (§4: v1 → v2, no scored value read; v1's output not kept, cleanliness rests on the scorer's code path, review-confirmed); **ADJ-OPP n200 r04 E2 flag** has no I_max = 3 twin (§3.4); **`vf_offset.py`** (sha above) and **`costs.py`** (`cf179b90…`) were run before their sha was written to the log (their sha256 are in `science_script.sha256`, post hoc). |
| **L-10** | **E1 / E2 wording at I_max = 0** (PREREG §7 last bullet; CAMPAIGN_FREEZE_ADDENDUM §2): "E1 and E2 are not evaluated" is true of the **calibration** triggers only (`calib.h:221-246`, rebuild loop, `cap = I_max`); the eval record's final-merge E1–E3 are computed at every I_max (`merge.h:473-487` at F, confirmed in the source by the review) and E2 fired once (§3.4). **Erratum entered in PREREG §8 and in the addendum's "Errata after the leg" (2026-11-19).** My `science.py` stdout contains one sentence to the contrary (S4 flag paragraph, "must be read as not evaluated when False"): wrong for the final flags; annotated in `science/science_tables.md` and `science/stdout.txt` (review F16). **M3 / σ̂ label:** `evidence.sigma_hat` = sd(log Ẑ_r), not sd(Ẑ_r / Ẑ) (PREREG §3.1 wording; same erratum, review F5). |
| **L-11** | **Ledger rounding:** `prior_after_S10.json` rounds each fit to 2 decimals: 462.48 vs 462.46 from the unrounded cost files. **S6 above its quote** (19.0 vs 15; stop 30) and **S2** (41.86 vs 40) are inside their stops. **Other ops events** (no effect on any record): S2 first deploy refused ("already submitted": a transient ssh failure; nothing submitted; guard hardened to EXISTS / FRESH / unreadable, fail-closed); S5 first deploy refused on an expired ssh ControlMaster, retry ok; NOTS home +502 MB at S6 (not from the leg; guard 7,900); `LEG_PLAN.md` §10 corrections (S10 wording, stale totals) are appended, the committed text unchanged. |
| **L-12** | **ADDENDUM_2_VF timing and the amendment of 14 record units (review F7; PREREG §8, 2026-11-19):** the addendum placed the VF scoring "at the read-back of the wave that holds the VF fits (S1 / S2)"; it ran only at the leg read-back. Criterion H became possible only after `law.bin` and `data.bin` were fetched from NOTS scratch for the 14 `VF` units (the collection plan kept `law.bin` only for `-P-` and A3 fits and no `data.bin`, although the addendum pre-declared `--cross-file`); the 14 units were amended after collection: content hashes checked against the fit's own `law.bin.json` / `data.bin.json` (28/28), `SHA256SUMS` rewritten with the old file kept as `SHA256SUMS.prev`, `sha256sum -c` OK (`vf_merge_units.log`; the review's reader confirms all 194 units). Nothing failed, so the addendum's "report to HQ at once" clause was never triggered. **The desktop offload copy of the 14 units needs a re-sync** (OPS_PREC heads-up). |

## 8. G-B readiness: what the G-B plan must contain (H-30, H-31; a list; the plan is a later task)
1. **10⁵ pilot on F2.** Engine F2 = merge **e993ece226b355058e26400f05f9faad6daf16ca**, tag **`p1m-freeze-F2`** (object ab0e3e6c), V binary sha256 prefix **`da0cf85b…`** (`BUILD_F2`, NOTS, once; `staging/vn_minileg/deploy_F2.log`); **default-N identity check PASS** (`VN_ID_1`, AR r01 s1 vs the overlap W0 V2 record: `logZ_r` 16/16, HPM, island hashes 16/16, 24 sidecars, fit / eval sections; `results/vn_minileg/F2_IDENTITY_CHECK.md`). The pilot runs in the frozen configuration (m 1, **I_max 0**, N 2,500), reports M1–M3 against §0-v2.3 and the C7 items of §3.4, and needs its **own committed class model for 10⁵** (the registered class table stops at p = 10⁴; T5 measured 42 core-h at m 1, I_max 3).
2. **The I_max = 3 twin of the pilot (≈ 42 core-h, approved H-30 (1)) with the SAME registered I_max rule pre-declared BEFORE it runs** (PREREG §3.2: non-inferiority r ≤ 1.15 on each of M1, M2, M3 and ≤ 1.30 per dataset, HPM identical; if I_max = 0 fails at 10⁵, 10⁵ and 1M use I_max = 3; the 10⁴ science stands as run, reported per configuration). The plan must say how a rule written for 3 datasets × 2 replicates reads on **one pair** (no replicate: the PREREG's own resolution figures give a per-fit sd of the log metric 0.10–0.27, so a single ratio is a coarse test), whether 2 seeds per arm are drawn, and which "dataset" count the 1.30 per-dataset clause uses.
3. **1M rep 1 options** (rep 1 = the 11-17 fit, V calibration with 3 rebuilds, not in the frozen configuration): **(a)** re-run rep 1 frozen (≈ 440 core-h; the calibration saving ≈ 120 per 1M fit offsets part of it); **(b)** report it as a separate configuration (cost 0 now). **Recommendation (worker's, endorsed with two corrections by the Opus review, for the manager and HQ): (b) now, and decide between (a), a 21st replicate and accepting 19 after the 10⁵ I_max twin is read.** Reasons: I_max = 0 at p ≫ 10⁴ is untested (the coded rule's grid kept changing for 13–15 rebuilds at p ≥ 5k: addendum §3), so (a) may spend ≈ 440 on a configuration the 10⁵ twin rejects, while under (b) rep 1 is already in-configuration if 1M ends up at I_max = 3. **Corrections:** (1) rep 1 is **one fit with one seed, on a pre-F2 build (the 11-17 pilot) whereas H-31 makes F2 the 1M engine, and with no same-seed I_max = 0 partner**; it could serve as an I_max = 3 arm of a 1M I_max comparison only with an F2 identity statement at 1M and a paired I_max = 0 fit — it is not "exactly" that arm; (2) HQ approved **20** AR-strong 1M replicates (H-14): **under (b) only 19 are in the frozen configuration** unless a 21st is run (≈ 440), so (b) defers the cost rather than removing it, unless HQ accepts 19.
4. **V-N mini-leg** (approved H-28; ≈ 440 core-h, P90 ≈ 510, plus the NOTS identity check 5–7; its three conditions are met: Sol 6.2 ACCEPT-WITH-FIXES with the fixes adopted (H-29), tag `p1m-freeze-F2` (H-31), identity PASS), scheduled **after** the current leg's precision waves (done). It still needs its own committed class table, stops and quote (`VN_MINILEG_NOTE.md` §1.2: E 21.2 / 51.7, hard 53.0 / 129.3, cumulative stop 600), runs `precision_freeze.py` on a **clean per-run cost dir** (L-4) and the offset's N contrast (`precision_offset.py`'s run-id pattern must accept the `N10000` ids; its `P(N, m, I)` contrast is built for I_max = 3), and its 12 arms were designed at **I_max = 3** against the baseline B: say whether they stay at I_max 3 or move to the frozen I_max 0. The F2 arms and the F baseline fits are different builds (identity PASS supports pooling; the plan should say so).
5. **Items from this read-back the G-B plan should not lose:** (i) report calibration E1 / E2 as NOT EVALUATED and the constants of §3.4 at I_max = 0, and the final-merge E1–E3 and σ̂ / sd(log Ẑ_r) > 1 (the E2 analogue) as the quality items (one ADJ-OPP E2 at 10⁴); (ii) the n = 100 M2 misses and the ADJ-OPP σ̂ outlier are reasons not to read the §0-v2.3 targets as met at R′ = 16 outside n ≥ 200 (the freeze addendum's "every fit meets the targets" covers R′ = 64 only; erratum entered); the optional ≈ 3–4 core-h attribution pair for r04 (§3.4) can ride in the V-N or G-B batch; (iii) register the analysis script **before** the first read (L-8); (iv) ADDENDUM_2_VF is closed (CLEAN incl. H, §4), but the 14 units were amended after collection (L-12): keep `law.bin` / `data.bin` in the collection list of any later carry-over check; (v) size 10⁵ / 1M from the stage count T, not nf(n) (§6); (vi) N, resampling and π₀(S₀) stay open.

## 9. Points for the Opus reviewer
1. **Review status.** The Opus review (`reviews/LEG_REVIEW_OPUS.md`) accepted with fixes F1–F18; this revision applies all of them (F1: the VF section is CLEAN, H 14/14, scorer CLEAN 11/11; F2: log Ẑ − log Z_T negative in 1/155; F3: BMA / oracle ratio statement; F4–F18 as listed in the review §8: the σ̂ label, the targets scope, partition d_H for 4/15 pairs, the 1M rep 1 wording, the L-8 qualification, L-12, the nits). The points below are the original reviewer questions, kept for the record; those answered by the review are marked in §7 (L-8, L-9, L-10, L-12).
2. **Mixed 40-fit set.** The full-mode `mixed40` verdict combines 14 `VF` with 6 I_max-3 V fits (ADDENDUM_2_VF's rule); 6 of the 10 datasets have one `VF` seed and one I_max-3 seed. Per-pair statements rest on `--wave-check`. Please check that the E1 / P figures I quote come from the right file (`vf/mixed_full/per_dataset.csv`, `vf/v3_full/per_dataset.csv`).
3. **Wrapper.** v1 → v2 (§4, L-9); please confirm no scored value was seen before the v2 sha was recorded (`vf_wrapper.sha256.v2`: timestamp, text), and that the renamed `run_manifest.json` is the only change to the VF inputs (the scorer takes `run_id` from the manifest).
4. **Unregistered science script (L-8).** Please check `science.py` against §5 (what is reported, what is not), the clustering (dataset = unit; AR n = 200 seeds averaged), the Wilson-with-fractional-successes convention, the unclipped t intervals, and the slope bootstrap; the helper self-test is synthetic only.
5. **E1 / E2 at I_max = 0 (L-10).** I read `merge.h:470-487` (worktree `~/SMC_Engineering_Department/tmp/20261119-precplan/wt_b89cba4d`, = b89cba4d, F's `src` unchanged) to conclude that the eval-record E1–E3 are final-merge checks and so evaluated at I_max = 0, contradicting the plain reading of the addendum's "E1 / E2 not evaluated". Please confirm, and say whether PREREG §7 / the addendum need an erratum before the 10⁵ read-back.
6. **ADJ-OPP n200 r04** (σ̂ 1.088, final E2, R_eff/R′ 0.42, log Ẑ 0.123 below log Z_T, HPM = S₀): one fit in 155, no I_max = 3 run of this dataset; described in §3.4 with the optional ≈ 3–4 core-h attribution check; the review: not attributable, no bearing on the freeze, a flag for HQ.
7. **M2 (island PIP max sd) 14/155 above 0.005, 13 at n = 100:** I counted them against the §0-v2.3 value; the engine's own `target_met` flag was not tabulated. R′ = 16 is the production size; the precision study (R′ = 64) never saw these cells.
8. **n-scaling claim.** The brief's "n = 400 and 800 cheaper than or equal to n = 200" holds in four designs and fails for BLK n = 400 (1.31 ×); the T-based explanation (R² 0.80) is a post hoc regression, flagged as such.
9. **Offset.** The registered script was run once on all it covers (output identical to FZ); `vf` and B1 rows are by hand with the registered reader's functions. The I_max = 0 cell's interval excludes 0 (df 2); I made no reading beyond §4.4. Check §5 against `offset_report.md` (a table copy, unedited) and the two hand rows against `vf_offset.json`.
10. **Cost.** The G-B cost check uses the committed (I_max 3, baseline) class table for I_max = 0 science fits; class assignment is `stop_rules_prec.klass` (imported, unchanged): A3 n 200 holds 16 fits (15 S4 + the A0 canary), AR n 200 holds 21 (20 + XB), ARweak n 100 holds 22 (20 + 2 B1 V fits). Ledger 462.48 vs 462.46 (L-11).
11. **G-B list (§8).** The 1M rep 1 recommendation (b) is mine, not the manager's; items 2, 4 and 5 are open questions I flagged, not decisions.
12. **Not done:** no NOTS access by this worker; no engine run by this worker except the 4 A3-pair xeval `cross` runs (§3.5); no co-reading of the 38 HPM misses beyond the counts (per-fit list in `science_tables.md`); no inference from δ, from the slopes or from the reliability curve.
