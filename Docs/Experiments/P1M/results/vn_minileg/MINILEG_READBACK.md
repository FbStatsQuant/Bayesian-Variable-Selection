N OUTCOME: **ADOPT N = 10⁴ at the FROZEN configuration (m 1, I_max 0)** by the pre-declared rule (`precision_freeze_vn.py`, 114f7e78…): r(M1, M2, M3) = 0.5048 / 0.5146 / 0.4794 against the bar 1/√c_X = 0.5164 (measured c_X = 3.7496), HPM identical, every dataset r < 1; **the margin on M2 is 0.0019**. The I_max-3 arm, scored by the registered `precision_freeze.py` verbatim, returns **KEEP** (M3 0.5719 > bar 0.5137). The two configurations disagree: reported as a FINDING (MINILEG_PREREG §3.3); nothing post hoc.

**Checked:** one Opus check (`reviews/MINILEG_CHECK_OPUS.md`) = CONFIRMED-WITH-FIXES (both fixes documentation-only, applied as errata E1/E2 in MINILEG_PREREG.md); all numbers reproduced from the raw records; c_X unambiguous under the prereg wording (every allowed reading gives ADOPT; M2 needs c_X ≥ 3.777 to fail, a 0.7 % margin). Pending HQ acceptance of N* (H-33).

# MINILEG_READBACK: V-N mini-leg verdict read-back (Engineering, Sonnet worker; Fri 2026-11-20)

**Status: pending manager commit.** Exactly as MINILEG_PREREG (exp/P1M 5d8c77e8) declares. No NOTS access by this worker; scratch `~/SMC_Engineering_Department/tmp/20261120-vnverdict/`; outputs and the descriptive tables script are in `results/vn_minileg/readback/` (sha256 in §9). Records: `~/SMC_Engineering_Department/records/vn_minileg/{V0,V1,V2}`, leg baselines `records/precision1e4/{A0,P1,P2,P3,P4}`, T references `records/overlap1e4/W0…W3`. Ops files read: `V0_READBACK.md`, `OPS_VN.md`, `completeness_table.md`, `prior_after_V2.json`.

## 1. Summary for HQ (≤ 10 lines)
1. **N outcome: ADOPT at the frozen configuration; KEEP at I_max 3** (registered script verbatim). Frozen: r = 0.505 / 0.515 / 0.479 (M1 / M2 / M3) vs bar 0.516 (c_X 3.750); I_max 3: 0.470 / 0.467 / **0.572** vs bar 0.514 (c_X 3.790). The ratios are ≈ 1/√4 = 0.5, i.e. N behaves as plain 1/√N scaling, which is exactly the rule's knife-edge (PREREG §3.4): the ADOPT is a thin call (M2 margin 0.0019; with the quote's c_X 3.85 the bar would be 0.5097 and M2 would fail: a sensitivity, **not** used: the rule says c_X measured).
2. **Governing configuration:** the frozen one (PREREG §3.3). If G-B's I_max twin rule reverts 10⁵/1M to I_max 3, that configuration's verdict (KEEP N = 2,500) applies. The disagreement itself is a FINDING for HQ + Theory.
3. **1M consequence, from the pre-declared table (ADOPT default row = S2):** 10⁵ rung at **N = 10⁴** (12 fits, ≈ 1.3k); 1M at **N = 2,500 frozen** for the approved 22-fit replicate set (6.9k) + **ONE N = 10⁴ fit on the rep-1 data** (1,083; re-based 1,061) in place of the N 5,000 self-check + option D at N 2,500. Total with 25 % reserve **17,261** (pre-declared) / **17,122** (re-based on the measured f); envelope 28,300, **closed 2,686.91**. All 22 at N = 10⁴: 34.9k (29.0k without reserve): **does not fit**. Not self-released: HQ accepts N\* at this verdict (S4: 16 fits at N 10⁴, 27.0k; S5: R′ 4 at N 10⁴, 14.0k, needs a D-6 ruling).
4. **Offset N contrast (no pass/fail):** Δ_N (k = 64) = **+0.00062** [−0.00087, +0.00210] frozen; **+0.00089** [−0.00073, +0.00251] I_max 3. H0 (no N dependence) **not excluded**; H-N (finite-N ∝ 1/N: +0.0052 / +0.0045) **excluded**. V − T at N = 10⁴: −0.0063 [−0.0117, −0.0009] (frozen), −0.0051 [−0.0121, +0.0018] (I_max 3). No FINDING from Δ_N.
5. **XB2: F2 = F at R′ 64, I_max 0: bit-identical** (64/64 `logZ_r`, 64/64 island hashes, 72 sidecars 0 differing fields). Pairing identity 12/12 (40 sections equal, grid equal). **Measured f = 3.77** (billed, mean of 12; 3.50–4.15), V0 3.94, wall 3.47; quote assumed 3.85.
6. **r04 (report-only):** the oddity **repeats at I_max 3 (same seed) and at seed 2 (I_max 0)**: σ̂ 1.088 / 1.103 / 1.342, final E2 in all three. By the pre-declared guide: not I_max-specific, not seed-specific: a property of this dataset.
7. **Cost 236.51 core-h** (V0 52.07, V1 67.70, V2 116.75) vs E 248.3 (P90 280): 0.95×; class means 0.95 × the committed E, max 1.09 ×, no soft or hard trip.

## 2. Verification of the registered material (task 1)
| item | check | result |
|---|---|---|
| `precision_freeze_vn.py` | sha256 | `114f7e7847dc9efef111c6888feb2f6616edd24ba18244062332cfba84e4cf73` = MINILEG_PREREG §1 ✓ |
| `vn_offset_contrast.py` | sha256 | `89725c169f8231bc6b6b37c9f20e5a9af88b4cced22f13200dbc599afb3a2655` ✓ |
| `precision_freeze.py` (registered) | sha256 | `7cdd69a11f3aaffa7a6615df639aefbe101042e9d37a8d520999ccbdc6279605` ✓ |
| `precision_offset.py` (registered) | sha256 | `cbbc23012e6900ff7798267cc7325816ad0b8312ec6e26fd09972adc9780d300` ✓ |
| unchanged since the commit | `git diff 5d8c77e8` on the PREREG, PLAN, the four scripts, the tests | empty ✓ |
| self-tests re-run (`python3 -I`) | `tests/test_vn_golden.py` 4 OK (incl. the golden on the leg's real FZ records), `tests/test_vn_offset_contrast.py` 1 OK; the leg's `test_precision_freeze.py` 8 OK, `test_precision_offset.py` 5 OK | **18/18 pass** |
| **defect in the committed PREREG §1 (documentation only)** | the sha256 printed there for `tests/test_vn_offset_contrast.py` is `9ef9b9e73e30f84b9def13e24a34dc690156389d1ed417becedacfcb65073c10d`; the file's actual sha256 is `9ef9b9e73e30f84b9def13e24a34dc690156389d1ed417b8a228a0f2ab9a1331` (MINILEG_PLAN §8 has it right). The file is unchanged since the commit; no rule script is affected | named, not edited |

## 3. Completion, identity, cost
15/15 fits delivered, every stage COMPLETED (`completeness_table.md`); one build `da0cf85b5fe0…` (BUILD_F2) in all 12 N = 10⁴ fits; recorded arm (N, m, I_max, I_used) = plan for 12/12; **pairing identity 12/12**: all 40 `calib.bin` sections except `meta` equal the twin's, `grid` equal (T3 below); X/y sha256 equal to the twins; XB2 bit-identical (T5).
**Cost (ledger `prior_after_V2.json`, 15 fits): 236.51 core-h** = V0 52.07 (quote 50, stop 100) + V1 67.70 (75, 150) + V2 116.75 (125, 250); against E 248.3 (P90 279.7, cap 600): 0.95×. Class means against the committed model: N 10⁴ I_max 0 **18.07 vs 19.06 (0.95×)**, max 20.65 (1.08×); I_max 3 **19.56 vs 20.68 (0.95×)**, max 22.53 (1.09×); soft lines 28.6 / 31.0, hard 47.6 / 51.7 not approached: no soft trip, no hard stop; G-B-type cost criterion (class mean ≤ 1.5×, no fit > 2.5×) met. XB2 6.29 (E 5.71), r04 pair 2.69 + 1.76.

## 4. The N rule (task 2), as computed
Commands (as MINILEG_PREREG §3.2; `R` = the records root; a clean cost directory of 35 per-run `cost_<run_id>.json` links, no `cost_batch.json`):
`python3 -I precision_freeze.py --records R/precision1e4/{A0,P1,P2,P3,P4} R/vn_minileg/{V0,V1,V2} --cost-dir <clean> --out freeze_registered`
`python3 -I precision_freeze_vn.py --records <same> --cost-dir <clean> --baseline 2500,1,0 --knob "N=10000 (m=1,I0):10000,1,0:up" --out freeze_vn_I0`
(and the vn copy with default arguments, which reproduces the registered output on these 20 + 12 fits: `identity`, `decisions`, `detail`, `targets_per_fit` equal ✓).
**Outputs:** frozen configuration: `N=10000 (m=1,I0)` = **ADOPT**, 0 identity failures. Registered script verbatim: **`N=10000 (m=1)` = KEEP**; it also reproduces the FZ knobs (`m=4` KEEP, `I_max=0` ADOPT, `N=10000 (m=4)` NOT_RUN), as it must.
| | frozen (I_max 0): X = (10⁴, 1, 0) vs B = (2,500, 1, 0) | I_max 3: X = (10⁴, 1, 3) vs B = (2,500, 1, 3) |
|---|---|---|
| c_X (mean islands billed X / B) | **3.7496** | 3.7896 |
| bar 1/√c_X | **0.5164** | 0.5137 |
| HPM identical in X ∪ B | yes (all 3 datasets) | yes |
| M1: AR / AR-weak / ADJ-OPP → geometric mean | 0.4968 / 0.5248 / 0.4934 → **0.5048** ≤ bar | 0.4933 / 0.4550 / 0.4637 → **0.4704** ≤ bar |
| M2 | 0.5099 / 0.5856 / 0.4562 → **0.5146** ≤ bar (margin **0.0019**) | 0.4458 / 0.4628 / 0.4924 → **0.4666** ≤ bar |
| M3 | 0.4798 / 0.4807 / 0.4778 → **0.4794** ≤ bar | 0.6296 / 0.5369 / 0.5533 → **0.5719 > bar (fails by 0.058)** |
| every dataset r < 1 | yes (all nine) | yes |
| **rule output** | **ADOPT** | **KEEP** |
Re-derived independently by `vn_verdict_tables.py` (own code): identical ratios and c_X (T2 below). Descriptive facts: all ratios sit in 0.446–0.630; at the frozen configuration M1 and M3 are within 0.04 of 0.5 in every dataset, M2 ranges 0.456–0.586 (the AR-weak dataset's M2 ratio 0.5856 is above the bar by itself; the rule tests the geometric mean). The rule's operating characteristics (PREREG §3.4) gave P(ADOPT) = 0.25–0.46 for a true ratio of 0.50. **Sensitivity (descriptive, not used):** the quote's c_X = 3.85 gives bar 0.5097; M2 0.5146 would then exceed it. The rule specifies the measured c_X.
**Mapping (PREREG §3.3):** N\*(frozen) = 10⁴. N\*(I_max 3) = 2,500. No AND, no veto; the frozen configuration governs the plan; the disagreement is a FINDING (it would say the N effect on the third metric, σ̂ = sd(log Ẑ_r), depends on the grid rule: at I_max 3, M3 improves by only 0.57 against 0.48 at I_max 0) sent to HQ + Theory; the rule outputs are unchanged.
### T1. Per fit: the 12 N = 10^4 fits and their N = 2,500 twins (same seed)
| dataset | I_max | rep | arm | recorded (N, m, I_max, I_used) | T | M1 sd log Z_occ,r | M2 max PIP sd | M3 sigma-hat | sigma-hat robust | islands billed | islands wall s | fit billed | HPM |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| AR | 0 | c1 | N 2,500 (F) | (2500, 1, 0, 0) | 23 | 0.01287 | 0.000444 | 0.02416 | 0.02298 | 5.188 | 94 | 5.55 | [1000, 3000, 5000, 7000, 9000] |
| AR | 0 | c1 | **N 10^4 (F2)** | (10000, 1, 0, 0) | 23 | 0.00687 | 0.000220 | 0.01094 | 0.01240 | 20.030 | 313 | 20.58 | [1000, 3000, 5000, 7000, 9000] |
| AR | 0 | c2 | N 2,500 (F) | (2500, 1, 0, 0) | 23 | 0.01382 | 0.000427 | 0.02348 | 0.02405 | 5.041 | 91 | 5.34 | [1000, 3000, 5000, 7000, 9000] |
| AR | 0 | c2 | **N 10^4 (F2)** | (10000, 1, 0, 0) | 23 | 0.00639 | 0.000224 | 0.01192 | 0.01116 | 18.722 | 294 | 19.23 | [1000, 3000, 5000, 7000, 9000] |
| AR | 3 | c1 | N 2,500 (F) | (2500, 1, 3, 3) | 20 | 0.01276 | 0.000522 | 0.02068 | 0.02304 | 4.840 | 90 | 5.72 | [1000, 3000, 5000, 7000, 9000] |
| AR | 3 | c1 | **N 10^4 (F2)** | (10000, 1, 3, 3) | 20 | 0.00688 | 0.000240 | 0.01341 | 0.01289 | 19.479 | 325 | 20.75 | [1000, 3000, 5000, 7000, 9000] |
| AR | 3 | c2 | N 2,500 (F) | (2500, 1, 3, 3) | 21 | 0.01378 | 0.000438 | 0.02146 | 0.02051 | 5.217 | 88 | 6.14 | [1000, 3000, 5000, 7000, 9000] |
| AR | 3 | c2 | **N 10^4 (F2)** | (10000, 1, 3, 3) | 21 | 0.00621 | 0.000187 | 0.01312 | 0.01150 | 18.254 | 339 | 19.35 | [1000, 3000, 5000, 7000, 9000] |
| ARweak | 0 | c1 | N 2,500 (F) | (2500, 1, 0, 0) | 9 | 0.01183 | 0.000438 | 0.01800 | 0.01544 | 3.807 | 68 | 4.09 | [1000, 3000, 5000, 7000] |
| ARweak | 0 | c1 | **N 10^4 (F2)** | (10000, 1, 0, 0) | 9 | 0.00612 | 0.000277 | 0.00905 | 0.00857 | 13.372 | 235 | 13.79 | [1000, 3000, 5000, 7000] |
| ARweak | 0 | c2 | N 2,500 (F) | (2500, 1, 0, 0) | 10 | 0.01151 | 0.000519 | 0.02108 | 0.02297 | 3.880 | 68 | 4.13 | [1000, 3000, 5000, 7000] |
| ARweak | 0 | c2 | **N 10^4 (F2)** | (10000, 1, 0, 0) | 10 | 0.00613 | 0.000283 | 0.00973 | 0.00867 | 14.956 | 338 | 15.33 | [1000, 3000, 5000, 7000] |
| ARweak | 3 | c1 | N 2,500 (F) | (2500, 1, 3, 3) | 9 | 0.01307 | 0.000461 | 0.01763 | 0.01804 | 3.928 | 74 | 5.01 | [1000, 3000, 5000, 7000] |
| ARweak | 3 | c1 | **N 10^4 (F2)** | (10000, 1, 3, 3) | 9 | 0.00554 | 0.000198 | 0.00874 | 0.00819 | 14.326 | 263 | 15.06 | [1000, 3000, 5000, 7000] |
| ARweak | 3 | c2 | N 2,500 (F) | (2500, 1, 3, 3) | 12 | 0.01267 | 0.000553 | 0.01620 | 0.01435 | 4.364 | 103 | 5.90 | [1000, 3000, 5000, 7000] |
| ARweak | 3 | c2 | **N 10^4 (F2)** | (10000, 1, 3, 3) | 12 | 0.00617 | 0.000272 | 0.00942 | 0.00840 | 16.849 | 293 | 17.61 | [1000, 3000, 5000, 7000] |
| ADJOPP | 0 | c1 | N 2,500 (F) | (2500, 1, 0, 0) | 19 | 0.01546 | 0.000357 | 0.02173 | 0.01901 | 5.186 | 88 | 5.51 | [1000, 1001, 5000, 7000, 9000] |
| ADJOPP | 0 | c1 | **N 10^4 (F2)** | (10000, 1, 0, 0) | 19 | 0.00761 | 0.000161 | 0.01025 | 0.01208 | 20.406 | 632 | 20.65 | [1000, 1001, 5000, 7000, 9000] |
| ADJOPP | 0 | c2 | N 2,500 (F) | (2500, 1, 0, 0) | 17 | 0.01543 | 0.000388 | 0.02515 | 0.02523 | 5.161 | 95 | 5.42 | [1000, 1001, 5000, 7000, 9000] |
| ADJOPP | 0 | c2 | **N 10^4 (F2)** | (10000, 1, 0, 0) | 17 | 0.00764 | 0.000179 | 0.01215 | 0.01114 | 18.486 | 323 | 18.85 | [1000, 1001, 5000, 7000, 9000] |
| ADJOPP | 3 | c1 | N 2,500 (F) | (2500, 1, 3, 3) | 21 | 0.01649 | 0.000362 | 0.02085 | 0.02213 | 5.874 | 103 | 7.24 | [1000, 1001, 5000, 7000, 9000] |
| ADJOPP | 3 | c1 | **N 10^4 (F2)** | (10000, 1, 3, 3) | 21 | 0.00666 | 0.000207 | 0.01150 | 0.01183 | 21.022 | 367 | 22.04 | [1000, 1001, 5000, 7000, 9000] |
| ADJOPP | 3 | c2 | N 2,500 (F) | (2500, 1, 3, 3) | 17 | 0.01424 | 0.000426 | 0.02154 | 0.02032 | 5.172 | 94 | 6.14 | [1000, 1001, 5000, 7000, 9000] |
| ADJOPP | 3 | c2 | **N 10^4 (F2)** | (10000, 1, 3, 3) | 17 | 0.00759 | 0.000182 | 0.01195 | 0.01213 | 21.468 | 358 | 22.53 | [1000, 1001, 5000, 7000, 9000] |

### T2. Independent re-derivation of the rule's inputs (this script's own code; compare freeze.json)
**I_max 0** (N 10^4 vs N 2,500): c_X = mean islands billed(X) / mean islands billed(B) = 3.7496; bar 1/sqrt(c_X) = 0.5164; HPM identical in X u B: True
| metric | AR | AR-weak | ADJ-OPP | geometric mean | <= bar | every dataset < 1 |
|---|---|---|---|---|---|---|
| M1 | 0.4968 | 0.5248 | 0.4934 | **0.5048** | yes (margin +0.0116) | yes |
| M2 | 0.5099 | 0.5856 | 0.4562 | **0.5146** | yes (margin +0.0019) | yes |
| M3 | 0.4798 | 0.4807 | 0.4778 | **0.4794** | yes (margin +0.0370) | yes |
**I_max 3** (N 10^4 vs N 2,500): c_X = mean islands billed(X) / mean islands billed(B) = 3.7896; bar 1/sqrt(c_X) = 0.5137; HPM identical in X u B: True
| metric | AR | AR-weak | ADJ-OPP | geometric mean | <= bar | every dataset < 1 |
|---|---|---|---|---|---|---|
| M1 | 0.4933 | 0.4550 | 0.4637 | **0.4704** | yes (margin +0.0433) | yes |
| M2 | 0.4458 | 0.4628 | 0.4924 | **0.4666** | yes (margin +0.0471) | yes |
| M3 | 0.6296 | 0.5369 | 0.5533 | **0.5719** | **NO** (margin -0.0582) | yes |

### T3. Identity (MINILEG_PREREG section 2)
| fit | recorded arm = plan | pairing: every calib.bin section except `meta` (calib_meta sections) equal to the twin's | grid sha256 equal | X/y sha equal to twin | binary sha | stages |
|---|---|---|---|---|---|---|
| 4-AR-n200-r01-P-N10000-m1-I0-c1-s1 | yes (10000, 1, 0, I_used 0) | 40 sections, 0 differing | yes | yes | da0cf85b5fe0 | COMPLETED |
| 4-AR-n200-r01-P-N10000-m1-I0-c2-s1 | yes (10000, 1, 0, I_used 0) | 40 sections, 0 differing | yes | yes | da0cf85b5fe0 | COMPLETED |
| 4-AR-n200-r01-P-N10000-m1-c1-s1 | yes (10000, 1, 3, I_used 3) | 40 sections, 0 differing | yes | yes | da0cf85b5fe0 | COMPLETED |
| 4-AR-n200-r01-P-N10000-m1-c2-s1 | yes (10000, 1, 3, I_used 3) | 40 sections, 0 differing | yes | yes | da0cf85b5fe0 | COMPLETED |
| 4-ARweak-n200-r01-P-N10000-m1-I0-c1-s1 | yes (10000, 1, 0, I_used 0) | 40 sections, 0 differing | yes | yes | da0cf85b5fe0 | COMPLETED |
| 4-ARweak-n200-r01-P-N10000-m1-I0-c2-s1 | yes (10000, 1, 0, I_used 0) | 40 sections, 0 differing | yes | yes | da0cf85b5fe0 | COMPLETED |
| 4-ARweak-n200-r01-P-N10000-m1-c1-s1 | yes (10000, 1, 3, I_used 3) | 40 sections, 0 differing | yes | yes | da0cf85b5fe0 | COMPLETED |
| 4-ARweak-n200-r01-P-N10000-m1-c2-s1 | yes (10000, 1, 3, I_used 3) | 40 sections, 0 differing | yes | yes | da0cf85b5fe0 | COMPLETED |
| 4-ADJOPP-n200-r01-P-N10000-m1-I0-c1-s1 | yes (10000, 1, 0, I_used 0) | 40 sections, 0 differing | yes | yes | da0cf85b5fe0 | COMPLETED |
| 4-ADJOPP-n200-r01-P-N10000-m1-I0-c2-s1 | yes (10000, 1, 0, I_used 0) | 40 sections, 0 differing | yes | yes | da0cf85b5fe0 | COMPLETED |
| 4-ADJOPP-n200-r01-P-N10000-m1-c1-s1 | yes (10000, 1, 3, I_used 3) | 40 sections, 0 differing | yes | yes | da0cf85b5fe0 | COMPLETED |
| 4-ADJOPP-n200-r01-P-N10000-m1-c2-s1 | yes (10000, 1, 3, I_used 3) | 40 sections, 0 differing | yes | yes | da0cf85b5fe0 | COMPLETED |

all 12: identity OK = True; binary sha of the 12 N 10^4 fits: ['da0cf85b5fe0']


## 5. The 1M consequence: read off the pre-declared table (task 3)
**Outcome = ADOPT (frozen configuration).** MINILEG_PREREG §6, row "ADOPT (default, self-releasable within S2's 17.3k only after HQ accepts N\* at the verdict)":
| | pre-declared | re-based on measured numbers (`vn_budget_rebase.py`: spent 2,686.91, f = 3.768) |
|---|---|---|
| 10⁵ rung | **N = 10⁴, all 12 fits**: 1,326 | 12 × 108.2 = 1,298 |
| 1M | **N = 2,500 frozen (I_max 0)**, 22 fits (20 AR-strong + ADJ-OPP + AR-weak gated): 6,939; **plus ONE N = 10⁴ fit on the rep-1 data**: 1,083 (in place of the N 5,000 self-check, 564); option D at N 2,500: 1,082 | one N 10⁴ fit 1,061; the rest unchanged |
| total with the 25 % reserve (S2) | **17,261** (spent 2,450.40 + 1.25 × 11,848) | **17,122** (spent 2,686.91 + 1.25 × 11,548); 17,187 at the pre-declared f; 17,425 at the measured maximum f 4.15 |
| reported | N = 10⁴ evidence at 10⁴ (12 fits, this read-back), 10⁵ (12), 1M (1 paired fit); the 1M replicate statistics are at N 2,500 and labelled so | |
**Envelope position.** 28,300; closed **2,686.91** = 975.5 (to 11-18 10:05) + 1,010.43 (overlap) + 462.48 (leg) + 1.99 (VN_ID_1) + **236.51** (mini-leg). *The brief's "2,450.40 + 236.51 + 1.99" counts VN_ID_1 twice: 2,450.40 already contains it.* Remaining 25,613.
**What does not fit (pre-declared):** all 22 1M fits at N = 10⁴ (1,061–1,083 each against 315 at N 2,500): **34.9k with the reserve, 28.5k without (re-based; 35.7k / 29.0k pre-declared)**, option D not even included: no. HQ's alternatives, **not self-released**: **S4** N = 10⁴ for 16 fits at 1M (14 AR-strong + ADJ-OPP + AR-weak), no option D, no self-check: 26,984 re-based (27,537 pre-declared at f 3.85; 27,463 re-based at f 3.85; 15 fits at the maximum f 4.15); **S5** R′ 4 at N = 10⁴ (equal island cost): 14,015 re-based; needs a D-6 ruling. **Which configuration runs:** 10⁵ rung: the frozen configuration (m 1, I_max 0) at **N = 10⁴** once HQ accepts N\*; 1M: the frozen configuration at **N = 2,500** with one N = 10⁴ fit; G-B's I_max twin rule (H-30) still decides I_max, and if it reverts to I_max 3 the I_max-3 verdict (KEEP) applies and N stays 2,500 for that configuration. **Gates before any N = 10⁴ run above 10⁴ (pre-declared):** the `--plan-only` memory plan at 10⁵ and 10⁶ for N = 10⁴ (0 core-h), then one 10⁵ N = 10⁴ fit before any 1M fit. Not decided here: S4 / S5, D-6.

## 6. The offset N contrast (task 4): the one pre-declared measurement; no pass/fail
Registered `precision_offset.py` (unedited) on the overlap W0–W3, the leg A0–P4 and the mini-leg V0–V2 (71 run dirs found, 50 V fits used, 10 T datasets), then `vn_offset_contrast.py` on its `offset_per_fit.csv` (the registered CSV's header lacks `src`: read by position, as declared). Reader checks: the overlap cell (ovl, 2,500, 1, 3, k 16) reproduces **−0.00394** [−0.00712, −0.00076], 7/10; s_T = 0.00324; the contrast script's I_max-3 Δ_N equals the registered script's own `N: (10000,1,3) − (2500,1,3) at k=64` (+0.00089 [−0.00073, +0.00251]).
**PN1: Δ_N at k = 64 (paired by dataset; per-dataset values in `vn_offset_contrast.json`)**
| configuration | δ(2,500) | δ(10⁴) | **Δ_N** (se) | 95 % t-CI (df 2) | negative | H0 = 0 | H-N = −0.75 × δ(2,500) | datasets' Δ_N |
|---|---|---|---|---|---|---|---|---|
| frozen (I_max 0) | −0.00690 | −0.00628 | **+0.00062** (0.00034) | −0.00087 … +0.00210 | 0/3 | **not excluded** | **+0.00517: excluded** | see json |
| I_max 3 | −0.00601 | −0.00512 | **+0.00089** (0.00038) | −0.00073 … +0.00251 | 0/3 | **not excluded** | **+0.00451: excluded** | see json |
Reading, as declared (PREREG §5): the interval **contains 0 and excludes the H-N value**: the offset does not move with N at these settings; it is not a finite-N effect of the islands (noise, or an arm difference that N does not change). Resolution as stated in advance: half-width ≈ 0.0015–0.0017 here (t(2)), better than the ≈ 0.006 the independent-seed case would have allowed, consistent with pairing by seed removing the shared grid variability. **No FINDING from Δ_N** (no interval excludes 0). No statement that V is biased is made.
**PN2: R′ span k 4 → 64 with the Jensen prediction (registered `P2_span`):** (10⁴, 1, 0): +0.00002 [+0.00001, +0.00003], Jensen +1.3e-5, slope − Jensen +0.00000 [−0.00001, +0.00001]; (10⁴, 1, 3): +0.00002 [−0.00001, +0.00004], Jensen +1.5e-5, slope − Jensen +0.00000 [−0.00001, +0.00001]. The N = 2,500 cells: frozen +0.00006 (Jensen +5.9e-5), I_max 3 +0.00004 (+4.6e-5). R′ dependence = the Jensen term, at both N.
**PN3: matched-N column (δ against the T tier-0 reference only, T at N = 10⁴, R′ 4; 3 datasets), k = 64:** (10⁴, 1, 0) **−0.00733**; (10⁴, 1, 3) **−0.00617**; for comparison (2,500, 1, 0) −0.00795; (2,500, 1, 3) −0.00706. All-T reference: (10⁴, 1, 0) −0.00628 [−0.01169, −0.00088], (10⁴, 1, 3) −0.00512 [−0.01206, +0.00182]; (2,500, 1, 0) −0.00690 [−0.01198, −0.00182]; (2,500, 1, 3) −0.00601 [−0.01338, +0.00136].
Registered-script note: it **dropped `4-ADJOPP-n200-r04-V-s2`** as ARM_MISMATCH (the run id parses as an overlap V fit, "I_max 3", while its record says I_max 0). That fit belongs to no offset cell (r04 is not a precision dataset): no effect; named for completeness. Knob contrasts of the registered table (m, I_max, N at I_max 3): unchanged from the leg for m and I_max (+0.00010, −0.00089).

## 7. XB2 (F2 = F) and the measured island factor f (task 6)
### T5. XB2 (F2 vs the leg's F record, AR c1 I_max 0, N 2,500, R' 64)
logZ_r (64 values) bit-equal: **True**; HPM equal: True; island output_hash 64/64 equal: **True**; recorded arm (2500, 1, 0, I_used 0); binary da0cf85b vs d0c30b65; fit billed 6.29 vs 5.55 core-h. (The full `xb_check` comparison is in `xb_check_XB2_output.txt`.)

Also from `xb_check_XB2_output.txt` (V0 read-back): 72 sidecars compared, 6,251 provenance keys dropped, **0 differing fields**; `fit.bin` 44 sections and `eval.bin` 4 sections equal. **F2 = F at R′ 64, I_max 0; the pooled F-build baselines are valid** (PREREG §4).
### T4. Measured island factor f = N 10^4 / N 2,500 (same seed, same grid, same T)
| fit pair | T | islands billed 2,500 -> 10^4 | f billed | islands wall (max task) 2,500 -> 10^4 | f wall |
|---|---|---|---|---|---|
| AR I_max 0 c1 | 23 | 5.188 -> 20.030 | 3.86 | 94 -> 313 | 3.33 |
| AR I_max 0 c2 | 23 | 5.041 -> 18.722 | 3.71 | 91 -> 294 | 3.23 |
| AR I_max 3 c1 | 20 | 4.840 -> 19.479 | 4.02 | 90 -> 325 | 3.61 |
| AR I_max 3 c2 | 21 | 5.217 -> 18.254 | 3.50 | 88 -> 339 | 3.85 |
| ARweak I_max 0 c1 | 9 | 3.807 -> 13.372 | 3.51 | 68 -> 235 | 3.46 |
| ARweak I_max 0 c2 | 10 | 3.880 -> 14.956 | 3.85 | 68 -> 338 | 4.97 |
| ARweak I_max 3 c1 | 9 | 3.928 -> 14.326 | 3.65 | 74 -> 263 | 3.55 |
| ARweak I_max 3 c2 | 12 | 4.364 -> 16.849 | 3.86 | 103 -> 293 | 2.84 |
| ADJOPP I_max 0 c1 | 19 | 5.186 -> 20.406 | 3.94 | 88 -> 632 | 7.18 |
| ADJOPP I_max 0 c2 | 17 | 5.161 -> 18.486 | 3.58 | 95 -> 323 | 3.40 |
| ADJOPP I_max 3 c1 | 21 | 5.874 -> 21.022 | 3.58 | 103 -> 367 | 3.56 |
| ADJOPP I_max 3 c2 | 17 | 5.172 -> 21.468 | 4.15 | 94 -> 358 | 3.81 |

mean f billed **3.768** (min 3.50, max 4.15); mean f wall 3.90 (min 2.84, max 7.18); the quote assumed 3.85 (3.2-4.6).

Descriptive: f billed 3.50–4.15 (mean 3.77); the V0 pair means were 3.94 (billed) and 3.47 (wall); one island task of `ADJOPP I_max 0 c1` took 632 s against 88 s (a ×7.2 wall outlier; its billed f is 3.94, a node-speed or load artefact of one task; the rule uses billed cost). The quote's 3.85 (3.2–4.6) held.

## 8. The r04 check (task 5): report-only
### T6. r04 check (report-only): ADJ-OPP n = 200 rep 4, R' 16, N 2,500
| fit | I_max / I_used | island T | sigma-hat = sd(log Z_r) | robust | R_eff/R' | E1 / E2 / E3 | low_empirical_ESS | log Z-hat - log Z_T | HPM = S0 / MPM = S0 | M1 | M2 | occ_inhomog. | fit billed |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| original r04 s1, I_max 0 (F, science S*) | 0 / 0 | 25 | 1.0880 | 1.0034 | 0.423 | False / True / False | False | -0.1227 | True / True | 0.01363 | 0.000549 | False | 1.54 |
| **twin r04 s1, I_max 3 (F2)** | 3 / 3 | 25 | 1.1033 | 1.0096 | 0.429 | False / True / False | False | -0.1082 | True / True | 0.01363 | 0.000549 | False | 2.69 |
| **r04 seed 2, I_max 0 (F2)** | 0 / 0 | 23 | 1.3415 | 0.9407 | 0.213 | False / True / False | True | +0.4541 | True / True | 0.00940 | 0.000488 | False | 1.76 |

**Facts.** All three fits have the final-merge **E2 (sd(log Ẑ_r) > 1)**, σ̂ 1.09–1.34, HPM = MPM = S₀. The I_max-3 twin (same data, same seed, different grid: preliminary → `rebuild_3`, both T = 25) is **not better** than the original (σ̂ 1.103 vs 1.088; log Ẑ − log Z_T −0.108 vs −0.123; R_eff/R′ 0.429 vs 0.423; its M1 and M2 are bit-identical to the original's, 0.013628492… and 0.000549105…, while `logZ_r` differ). The seed-2 I_max-0 fit is also elevated: σ̂ 1.342, R_eff/R′ 0.213, `low_empirical_ESS` True, and log Ẑ is **above** log Z_T (+0.454), unlike the two seed-1 fits (below it).
**Reading, by the pre-declared guide only:** the I_max-3 twin is also elevated → **not I_max-specific**; the seed-2 fit repeats the elevation → **not specific to seed 1**; so it looks like a property of this dataset (ADJ-OPP n = 200, rep 4: two seeds, two grids). One dataset, three fits: no attribution beyond this, no change to any rule; a line to HQ. (The sign of log Ẑ − log Z_T differs between seed 1 and seed 2; a deterministic lower bound below the estimate is not a violation, and with σ̂ > 1 the estimate's noise is of the size of the gap.)

## 9. Files, commands, sha256
`results/vn_minileg/readback/`:
| file | what | sha256 |
|---|---|---|
| `readback/tables.md` | vn_verdict_tables.py output | `c7faf2dad00c85ca85706dfd29c3f836eeeb1d631c3dbd2deb3b8c1589e42570` |
| `readback/tables.json` |  | `a5fafc5482b5fcdd7e1002169ebebe4f5a3165cdc3cd66a1475eef0d781a0f95` |
| `readback/vn_verdict_tables.py` | descriptive tables + independent re-derivation (not registered) | `37a548fa39fd54e36fca2b7b2e58b9e5ab528044418d8737666cbaddab6fe92d` |
| `readback/vn_budget_rebase.py` |  | `d1fa35a33c9db76e908086796c7a981a4c67f3d17e4684e094eb5518f7ba5953` |
| `readback/vn_budget_rebase_output.txt` |  | `22a57cd8f3bdee970982d30dc9e57b898589b9c4df1f6fe17d7245cc9e142150` |
| `readback/outputs/freeze_vn_I0/freeze.json` | precision_freeze_vn.py, frozen configuration | `999b9eb9d7af35df303adac64a10b2e25fc8d5cfb229d5d26b5399113f97b9dd` |
| `readback/outputs/freeze_registered/freeze.json` | registered precision_freeze.py verbatim (I_max 3 and the FZ knobs) | `199faf5b4d85546398284ccf02814b79ebd309a4ac9c225c382dc3e27c995b41` |
| `readback/outputs/freeze_vn_default/freeze.json` | vn copy with default arguments (= registered output) | `e5897184bbb181306eb61693cbab44e00b0f5564a65c652801afdc04fa449262` |
| `readback/outputs/offset/offset.json` | registered precision_offset.py | `16718f26bef64268b91df0de31dc7763cd000d5a5dbaa32e460f0680ae33a833` |
| `readback/outputs/offset/offset_report.md` |  | `8a184f0d516673da68aec1eb616f50d4f31dcdedbcce5ddc8d6e1d582f0bb4f8` |
| `readback/outputs/offset/offset_per_fit.csv` |  | `1edeafb0a96b98dbc502dce8010490c50ae83dfca26085180142b4e85cf1b534` |
| `readback/outputs/contrast/vn_offset_contrast.json` | vn_offset_contrast.py | `224b667c23cac5a16e940bfc158f2c3b5db0e32260133ecb94b1a8c71a2c6683` |
| `readback/outputs/contrast/vn_offset_contrast.md` |  | `8805455388ca49ef4ae50f61909aa139629028d0d1d89a24dd2021c9d1afd2cc` |
Commands to reproduce: §4 (two freeze runs), §6 (`precision_offset.py --records R/overlap1e4/W0 … R/vn_minileg/V2 --out offset`, then `vn_offset_contrast.py --per-fit offset/offset_per_fit.csv --out contrast`), `python3 -I vn_verdict_tables.py --R R --out tables`, `python3 -I vn_budget_rebase.py`.

## 10. Points for a checker
1. **The ADOPT is thin:** M2's geometric mean 0.5146 vs bar 0.5164 (margin 0.0019, 0.4 % of the bar); re-derive from `tables.md` T1/T2 (per-fit M2 and islands billed). With c_X = 3.85 it would be KEEP; the rule uses the measured c_X (3.7496 = mean islands billed(X) / mean islands billed(B), 6 + 6 fits).
2. **Two configurations, two outputs:** frozen ADOPT, I_max 3 KEEP (M3 only). Check that no cross-veto was applied (PREREG §3.3) and that the governing configuration is the frozen one.
3. **Baseline builds:** the N = 2,500 twins are F-build (d0c30b65) fits, the N = 10⁴ fits F2; pooling rests on F2_IDENTITY_CHECK, XB2 (bit-identical) and the pairing identity (12/12): confirm `xb_check_XB2_output.txt` and T3/T5.
4. **c_X uses billed islands core-h** from the per-run cost files; the clean cost directory is 35 symlinks to `records/*/_batch_*/cost/cost_4-*.json` (leg A0–P4 and V0–V2); confirm no `cost_batch.json` is among them (the registered script would raise) and that both scripts read the same numbers (`tables.md` T2 re-derives them).
5. **Offset:** the contrast script reads `offset_per_fit.csv` by position (header defect of the registered script); confirm its I_max-3 Δ_N equals the registered `N:` contrast (+0.00089 [−0.00073, +0.00251]) and the reader check −0.00394.
6. **1M table:** pre-declared numbers are quoted from `vn_budget_output.txt` (sha in MINILEG_PLAN); the re-based column is `vn_budget_rebase.py` (spent 2,686.91; f 3.768). The brief's closed total double counts VN_ID_1.
7. **r04:** M1 and M2 are bit-identical between the original (I_max 0, F) and the I_max-3 twin (F2) although the grids and `logZ_r` differ: a fact I did not explain (the terminal occupancy-based quantities do not move); it does not change the reading, but a checker may want to look.
8. **Documentation defect named:** PREREG §1 prints a wrong sha256 for `test_vn_offset_contrast.py` (§2 above); the registered offset script drops the r04 seed-2 fit by an id-pattern collision (§6). Neither touches a result.
9. **Not done:** no NOTS access; no engine run; no change to any registered file or threshold; no extra analysis beyond what PREREG declares (the c_X = 3.85 sensitivity and the re-based budget are labelled descriptive).
