# GB_PREREG: pre-declarations for gate G-B (final): the I_max rule on the two 10⁵ pairs at N* = 10⁴, the registered criteria, the continuity-twin report, operating characteristics, disclosures (Engineering, Sonnet plan writer; Fri 2026-11-20)

**Status: FINAL; pending manager commit** (HQ H-38 applied). Written before any 10⁵ fit of this gate exists. Companion: `GB_PLAN.md` (fits, run sheet, quotes, stops). It applies HQ's H-30 (1) / H-38 (2): the **same registered I_max rule** (PREREG `results/precision1e4/PREREG.md` §3.2) is pre-declared for the 10⁵ set BEFORE it runs. No threshold below is new: every number is copied from the registered rule, H-26 Q4 or ENGINEERING_SPEC §0-v2.3. The manager commits this file with the sha256 of the scripts in §1 **before the pilot set is submitted**; any later change is a logged deviation (§9) with the reason, the date and the new sha256.

## 1. What is registered
| item | value |
|---|---|
| registered rule (unedited) | `results/precision1e4/precision_freeze.py` sha256 `7cdd69a11f3aaffa7a6615df639aefbe101042e9d37a8d520999ccbdc6279605` (the "I_max = 0" block); its mini-leg copy `results/vn_minileg/precision_freeze_vn.py` sha256 `114f7e7847dc9efef111c6888feb2f6616edd24ba18244062332cfba84e4cf73` (`--baseline`, `--knob`) |
| **script that scores the 10⁵ set** | **`results/gb/gb_imax_rule.py`, sha256 `76927ae2faadc095e9353050eae3ef626ad439d88b92a7bf7cb9f313dab91012`** (stdlib, `python3 -I`, deterministic). **Why not the registered files:** both have the precision leg's run-id regex (`4-<design>-n200-r01-P-…`), so a 10⁵ id (`5-…-V-s1`) is never found; and both score a cell only if it has **exactly 2 replicates** (`val()` returns None otherwise → NOT_EVALUATED), while a G-B arm has one fit per dataset. **The copy differs in exactly three places:** (1) run ids (`--ids gb`: `5-<AR\|ADJOPP>-n200-r01-(V\|VI3)-s1`; `--ids precision` for the golden), (2) `--reps R` (default 1; registered 2), (3) only the I_max rule is computed (no cost ratio, no N or m knob) and the final-merge flags are reported beside it. `fit_metrics`, `recorded_arm`, the thresholds 1.15 / 1.30 and the HPM test are verbatim |
| self-test | `results/gb/tests/test_gb_imax_rule.py` sha256 `7c85ebfab0145fb9140ee8887b725190bf40220a4bc9bed9bf070c5bfdd19018`: **7 of 7 pass**, including the **golden on the leg's REAL FZ records** (`--ids precision --N 2500 --reps 2` reproduces `fz/freeze.json` decisions["I_max=0"] = ADOPT → PASS and every ratio to 12 places: r = 0.97150 / 0.93169 / 1.13031) and synthetic PASS, FAIL on each metric, FAIL on HPM, the n = 1 and n = 2 forms, NOT_EVALUATED (zero denominator, missing arm), INCOMPLETE (arm mismatch, no calibration record) |
| read-back script | `results/gb/gb_readback.py` (tables, §5 criteria, §6 report): **to be written and its sha256 recorded before the first submit** |
| engine | F2: tag `p1m-freeze-F2`, e993ece226b355058e26400f05f9faad6daf16ca; binary sha256 `da0cf85b5fe014973d15674f0da8e8c12dfdaf465a5e06aa0216b294601f231a`; NOTS identity PASS and XB2 bit-identical. Every sidecar's `binary.sha256` must equal it |
| configuration | m 1, **N = 10⁴** (N\*), R′ 16, bounded calibration, resampling off ("not tested"), class A, `island_isa sapphirerapids`. A pair differs **only in `I_max`** (0 vs 3), same data seed, same engine seed |
| evaluator | the engine `eval` command of F2 with the overlap's parameters (n_x 4,000, n_gh 64, n_draws 10⁴, n_test 10⁴, rel_cut 1e-12, top_k 1,000, tail_r 1,000, tail_groups 8, block_rows 500); eval seed = the dataset's data seed |

## 2. THE rule on the two pairs
**Fits.** Dataset A = `5-AR-n200-r01` (data seed = engine seed 502020001); dataset B = `5-ADJOPP-n200-r01` (505020001). Per dataset: `…-V-s1` (I_max 0, the frozen fit) and `…-VI3-s1` (I_max 3). Four fits, R′ 16, N 10⁴ (recorded N must be 10,000).
**Quantities** (PREREG §3.1 with the §8 erratum): M1 = `fit.meta.occ[M = 1000].sd_log_Z_occ_r`; M2 = `pip.island_spread.max_sd`; M3 = `evidence.sigma_hat` = **sd(log Ẑ_r)** over the 16 final islands; HPM = `selection.hpm`. Per dataset d and metric k: **r_{k,d} = M_k(I_max 0 fit) / M_k(I_max 3 fit)** (the registered "mean over replicates" is the single fit).
**Rule (the registered one, for 2 datasets × 1 replicate).** Let r_k = the geometric mean over the two datasets. **I_max = 0 PASSES iff, for each k ∈ {1, 2, 3}: r_k ≤ 1.15, AND r_{k,d} ≤ 1.30 for each dataset d, AND `selection.hpm` is identical in all four fits (within a dataset: the I_max 0 and I_max 3 fit).** Otherwise FAIL. (One dataset alone would collapse the two bars to 1.15; with two they are the registered pair of bars.)
**Not used by the rule, reported beside it:** Δ log Ẑ, E1–E3, `grid_fallback`, cost. `grid_fallback` True in either fit does not change the outcome and is flagged to HQ.
| case | outcome |
|---|---|
| a field missing, or a denominator = 0 or non-finite, or an arm fit missing | **NOT EVALUATED** → HQ, no default |
| a fit undelivered after one infrastructure rerun, or an identity failure (recorded arm ≠ plan, rule ≠ bounded, `I_used` > `I_max`, no calibration record) | **INCOMPLETE** → HQ (rerun or hold); never scored |
| both M_k tiny | **no floor** (the registered rule has none); the §5 target margins are printed beside the ratios |
**Consequence (H-30, H-38, MINILEG_PREREG §3.3).** **PASS** → the 10⁵ rung and the 1M fits run at I_max 0 (rung at N 10⁴; 1M replicates at N 2,500 + ONE N 10⁴ fit, S2). **FAIL** → **I_max 3 and N 2,500** (the mini-leg's I_max-3 verdict for N is KEEP: "the I_max-3 result is what is used if the G-B rule reverts 10⁵/1M to I_max 3"); the 10⁴ science stands as run (I_max 0, N 2,500, m 1) and is **reported per configuration**. No post-hoc override either way (the FZ precedent).

## 3. What two pairs can and cannot decide (assumptions labelled)
**Inputs, all from 10⁴ data (the only data that exist), listed in §7:**
| source | what | result |
|---|---|---|
| 14 same-seed pairs of the precision leg (`VF` I_max 0 vs the overlap I_max 3 fit; same data, same engine seed; R′ 16; **N 2,500**; `tools/pair_ratios_output.txt`) | single-pair ratios | **M1 and M2: 0.999–1.001 in 14/14**; M3 (13 non-NULL pairs): 0.85–1.37, gmean 1.022, **sd(log r) 0.123**, **12/13 ≤ 1.15** (the exceedance: AR r04 s2, 1.373); HPM identical 14/14 |
| the registered study at R′ 64, N 2,500, 3 datasets × 2 replicates, different seeds per arm | the registered ADOPT | r = 0.971 / 0.932 / 1.130 |
| **the same rule at N 10⁴, R′ 64** (V0–V2, 6 + 6 fits at I_max 0 / 3, different seeds per arm; `gb_imax_rule.py --ids precision --N 10000 --reps 2`, `tools/imax_at_N1e4_output.txt`) | the rule applied to the cells that now exist | **PASS**: r = 1.043 / 1.027 / 0.948; per dataset ≤ 1.193 (M2, AR-weak), HPM identical. Descriptive; **no decision rests on it** |
**Characteristics of the 2-pair rule** (model: ln r_3 ~ N(ln ρ, 0.123²) independently in the two datasets, M1 and M2 ≈ 1; an assumption, **and 0.123 is the N 2,500 value: the N 10⁴ noise is unknown**):
| true ratio ρ of M3 | P(PASS) |
|---|---|
| 1.00 | 0.93 |
| 1.13 (the registered study's estimate) | 0.55 |
| 1.30 | 0.07 |
| 1.50 | 0.00 |
**Reading, stated plainly.**
- (i) The two pairs **can** detect: HPM differing, an M3 ratio far above 1.15 in either dataset, M1 or M2 leaving ≈ 1 (they were identical at 10⁴; if they separate at 10⁵ that is a structural change), a grid-construction failure at I_max 0, a final-merge E2. They cover **two designs** (AR-strong and ADJ-OPP; not AR-weak or IND).
- (ii) They **cannot** show non-inferiority within 15 %: P(PASS) is ≈ 0.9 if I_max 0 is truly equivalent and ≈ 0.55 at the registered study's own point estimate, so a PASS is weak evidence of non-inferiority and a FAIL is weak evidence of inferiority. The registered ADOPT at 10⁴ itself sat ≈ 0.5 s.e. inside its margin (FZ addendum §2); the 10⁵ set inherits that.
- (iii) The pairs are paired by seed (same position-addressed random numbers); that is why M1 and M2 were near-deterministic and the M3 ratio sd is 0.123 rather than the 0.10–0.27 per-fit noise of different-seed arms (PREREG §3.2). Cause of the identical M1 / M2 not examined (the check's reading: they are occupancy-based and the same seed visits the same top sets).
- (iv) **ADJ-OPP r01 is not r04.** The mini-leg found the r04 σ̂ oddity to be a property of that dataset (it repeats at I_max 3 and at seed 2); r01 is not expected to show it, so the set does not test that tail.
- (v) **Cost asymmetry:** a false FAIL costs ≈ 9.5 per 10⁵ fit and ≈ 121 per 1M fit (≈ 2.5k over 20 replicates) and moves N back to 2,500; a false PASS costs a σ̂ ≈ 13 % wider at 1M with M1 and M2 unaffected at 10⁴. Both are affordable; a coarse test is accepted.
- (vi) **Fragility chain, stated:** the N\* = 10⁴ ADOPT (margin 0.0019) and the I_max 0 ADOPT are each within noise, and the I_max-3 arm said KEEP. A FAIL here sends the campaign to (2,500, I_max 3), the configuration the N rule's KEEP governs.

## 4. Decision table (registered)
| outcome | rung and 1M | 10⁴ science | what the four fits are | continuity twins |
|---|---|---|---|---|
| PASS | I_max 0; rung 12 fits at N 10⁴ | stands | the two I_max 0 pilots are rung fits AR r01 and ADJ-OPP r01; the I_max 3 twins are reported | run with the rung (§6) |
| FAIL | I_max 3, N 2,500; rung 12 fits at (2,500, 3), first fit = the C1–C3 confirmation fit | stands, reported per configuration | reported only; none is a rung fit | dropped |
| NOT EVALUATED / INCOMPLETE | HQ decides (rerun or hold) | stands | none is a rung fit until HQ rules | held |
Reported with the verdict, never part of it: r_{k,d}; M1–M3 of all four fits against §0-v2.3; Δ log Ẑ (I_max 0 − I_max 3) in island s.e.; stage counts T and wall per grid; calibration core-h saved; final-merge E1–E3, `low_empirical_ESS`, `checks_passed_final`, sd(log Ẑ_r) > 1; `occ_inhomogeneous`; calibration E1 / E2 as **NOT EVALUATED**, and `grid_unconverged` / `I_used` / `checks_passed_calibration` as the I_max-0 constants outside any quality aggregate (CAMPAIGN_FREEZE_ADDENDUM §2 and errata); the measured **f at 10⁵** if the continuity twins run.

## 5. The G-B criteria, registered (ENGINEERING_SPEC §0-v2.6 G-B; EXPERIMENT_PLAN G-B; H-26 Q4)
Judged on the **winning configuration's fit** (PASS: the I_max 0 pilots; FAIL: the rung's confirmation fit at (N 2,500, I_max 3), which is evaluated before the other 11 rung fits are released). All four pair fits are reported either way.
| # | criterion | registered pass condition |
|---|---|---|
| C1 cost | ≤ 1.5× model, Q4 guard | fit billed core-h (sacct CPUTimeRAW, all stages) ≤ 1.5 × the committed class model (**the committed table, never re-fitted**): AR pilot E 108 → **162** (hard 270), ADJ-OPP pilot E 133 → **200** (hard 333), twins 118 → 177 (295) and 142 → 213 (355) informational; FAIL-branch confirmation fit E 40 → 60 (hard 100). A class of one fit: the class mean is the fit and **the 2.5× guard is the STOP line**. Beside it, not a criterion: the ratio to the manifest planning value (96 at N 2,500) |
| C2 precision | §0-v2.3 at R′ 16 | **M1 ≤ 0.05; M2 ≤ 0.005 (engine `target_met`); \|log Ẑ − log Ẑ_occ(M = 1,000)\| ≤ 3√(se_Z² + se_occ²) (se = island sd / √16); HPM certified by the final local search (`local_certified`)**; max_j \|PIP_eq − PIP_𝒯\| ≤ 0.01 + (1 − π̂(𝒯)) if the field exists (not verified). Reported, not gating: M3 ≤ 0.5 (goal), `occ_inhomogeneous`; "same best model in 16 of 16 islands" **not computable** (no per-island HPM) |
| C3 memory | < request | MaxRSS < the stage's request in **each** of setup 16 G, calibrate 16 G, islands 12 G, merge 24 G, eval 16 G (advisory > 80 %); peak < 50 % of a node recorded |
| C4 completion | delivered | all four fits delivered, one sha256 = F2's, arm identity verified, `logZ_r` of length 16 and finite |
| C5 E2 recorded | EXPERIMENT_PLAN G-B | reported per §4 |
| C6 I_max rule | §2 | PASS or FAIL recorded |
**G-B passes iff C1–C4 pass (after a memory resize, if any) and C6 is PASS or FAIL.**
**Misses (registered, no discretion):** C1 in (1.5×, 2.5×]: G-B cost FAIL, the rung and 1M re-quoted from the measured fit, HQ releases; > 2.5×: STOP. C2: G-B precision FAIL, rung not auto-released, HQ gets priced options (accept as a reported miss; R′ 32 ≈ +106 per fit at N 10⁴; hold); **never an estimator switch** (§0-v2.3). C3: re-size to 1.3 × the measured peak, rerun the stage, re-evaluate ("PASS after resize"). C4: one infrastructure rerun, then INCOMPLETE → HQ. A pilot HPM ≠ S₀ is a flag to HQ, not a criterion.

## 6. The continuity twins: what is reported (HQ H-38 (1); report-only, no threshold, no pass/fail)
**Fits.** Two at 10⁵, **N 2,500, I_max 0**, F2: `5-AR-n200-r01-VN25-s1` and `5-ADJOPP-n200-r01-VN25-s1`, the **same data and seeds as the two N 10⁴ pilots (rung fits AR r01 and ADJ-OPP r01)**; same shapes as the pilots (islands limit 0:20); ≈ 67 core-h. They run **with the rung, only after the G-B verdict is PASS**; on FAIL they are dropped (the rung is then at N 2,500). Calibration is identical by pairing (N-independent, H = 512): verified by `calib.bin` section equality (all but `meta`), as the mini-leg's pairing identity.
**Reported, per pair (N 10⁴ vs N 2,500):** HPM equality and HPM = S₀; max_j |ΔPIP_eq| and the change of the active-PIP minimum and the null-PIP supremum; Δ log Ẑ (N 10⁴ − N 2,500) in units of the island s.e.; log Ẑ − log Z_T for both; M1–M3 ratios r_N (N 10⁴ / N 2,500) beside the mini-leg's reference 1/√c_X evaluated at the **measured 10⁵ c_X** (a reference, not a bar); the measured **f at 10⁵** (billed islands ratio) against 3.77; π̂(S₀) at both N; d_H between the two store laws **if** `law.bin`, `data.bin` and the cross-evaluator build exist at 10⁵ (not verified; otherwise "not computed"); stage costs and wall. Stated limits: two datasets, one seed pair each; the I_max of the twins is the verdict's (0).

## 7. Disclosures
- **What I looked at on real data before registering.** (i) The F2 identity record, the T5 and 1M pilot cost records, the mini-leg read-back and its Opus check (documents). (ii) **The 14 same-seed I_max 0 / I_max 3 pairs of the 10⁴ leg** (M1–M3, HPM from eval records; `tools/pair_ratios_output.txt`), to price the pair's resolution; read in the 11-19 draft, before this file's rule was fixed; no threshold was tuned on them. (iii) **The registered I_max rule applied to the 12 mini-leg fits at N 10⁴** (`tools/imax_at_N1e4_output.txt`; new here, from records the mini-leg read-back already tabulates in its T1); descriptive. (iv) Nothing at 10⁵ exists for this gate: no I_max 0 fit, no pair, no N 10⁴ fit.
- **Limits.** The §3 characteristics assume a log-normal M3 ratio with sd 0.123 (13 pairs at N 2,500, p 10⁴, n 200, one seed each: AR 8, AR-weak 2, ADJ-OPP 2, IND 1), M1 and M2 ≈ 1, and that 10⁵ at N 10⁴ behaves like 10⁴ at N 2,500 in its noise: **untested**.
- **Fields not verified at F2 / 10⁵:** the PIP_𝒯 agreement field; `local_certified`; π̂(S₀); `calib_meta.json` content at 10⁵ (the leg produced it at 10⁴).
- **Choices fixed here that HQ or a reviewer may overrule before the commit** (each a table cell or one script constant): the rule is the registered one with 2 datasets × 1 replicate; the continuity pairs are AR r01 and ADJ-OPP r01 (any two rung fits would do; these two are the I_max-pair datasets); the committed class models (108 / 118 / 133 / 142; 30 / 37; 40 for the FAIL confirmation fit); merge request 24 G and islands request 12 G; islands limits 0:45 (AR), 1:00 (ADJ-OPP); NOT EVALUATED / INCOMPLETE → HQ with no default; on FAIL, N = 2,500 (MINILEG_PREREG §3.3).
- **Mini-leg interplay.** (N 10⁴, I_max 0) was run at 10⁴ (6 fits) and is the configuration the pilots test at 10⁵; (N 10⁴, I_max 3) was run at 10⁴ and said KEEP N 2,500; the continuity twins (N 2,500, I_max 0) are the only 10⁵ link between the N 2,500 thread and the N 10⁴ thread.

## 8. Carry rules (L-8, L-12, errata, the mini-leg's F2)
Scripts registered **before the pilot set is submitted**; `law.bin` and `data.bin` kept for all four fits from the start; the registered `precision_freeze.py` / `precision_freeze_vn.py` are not edited and not used on 10⁵ ids; ids of report-only fits stay **outside the registered patterns** (the mini-leg's r04 collision): the continuity twins carry the arm tag `VN25`; M3 is sd(log Ẑ_r); calibration E1 / E2 are NOT EVALUATED at I_max 0 and the final-merge flags are reported as frequencies.

## 9. Deviation log
None yet. A change to any threshold, rule, field choice or script after the shas of §1 are committed is a logged deviation with the reason, the date and the new sha256.
