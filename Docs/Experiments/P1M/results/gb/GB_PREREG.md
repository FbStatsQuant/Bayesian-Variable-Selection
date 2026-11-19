# GB_PREREG: pre-declarations for gate G-B: the I_max rule applied to the 10⁵ pair, the registered G-B criteria, operating characteristics, disclosures (Engineering, Sonnet plan writer; Thu 2026-11-19)

**Status: DRAFT; finalised after the V-N mini-leg verdict (H-33).** Written before any 10⁵ fit of this gate exists. Companion: `GB_PLAN.md` (spec, run sheet, quotes). It applies HQ's ruling H-30 (1): the **same registered I_max rule** (PREREG `results/precision1e4/PREREG.md` §3.2, script `precision_freeze.py` sha256 `7cdd69a11f3aaffa7a6615df639aefbe101042e9d37a8d520999ccbdc6279605`) is applied to the 10⁵ pair and pre-declared BEFORE it runs. No threshold below is new: every number is copied from the registered rule, H-26 Q4 or ENGINEERING_SPEC §0-v2.3. At finalisation the manager commits this file with the sha256 of `gb_imax_rule.py` and `gb_readback.py` **before the pilot is submitted**; any later change is a logged deviation (§8) with the date and the new sha256.

## 1. What is registered (placeholders until finalisation)
| item | value |
|---|---|
| engine | F2: tag `p1m-freeze-F2`, e993ece226b355058e26400f05f9faad6daf16ca; binary sha256 `da0cf85b5fe014973d15674f0da8e8c12dfdaf465a5e06aa0216b294601f231a`; NOTS default-N identity PASS (`results/vn_minileg/F2_IDENTITY_CHECK.md`). Every sidecar's `binary.sha256` of the pair must equal it |
| rule script | `results/gb/gb_imax_rule.py`, sha256 **TO BE RECORDED** (stdlib, `python3 -I`, deterministic; `fit_metrics` copied verbatim from the registered `precision_freeze.py`; reads the two eval records only) |
| read-back script | `results/gb/gb_readback.py`, sha256 **TO BE RECORDED** (cost, stage table, §5 criteria, C7 items) |
| self-tests | synthetic records only: PASS, FAIL on each metric, FAIL on HPM, n = 1 and n = 2 forms, zero denominator → NOT_EVALUATED, arm mismatch → INCOMPLETE; sha256 TO BE RECORDED |
| configuration | frozen: `refine_m 1`, `N = N*` (2,500 or 10⁴, the mini-leg's), R′ 16, bounded calibration, resampling off ("not tested"), class A, `island_isa sapphirerapids`. The pair differs **only in `I_max`** (0 vs 3) |
| evaluator | the engine `eval` command of F2 with the overlap's parameters (n_x 4,000, n_gh 64, n_draws 10⁴, n_test 10⁴, rel_cut 1e-12, top_k 1,000, tail_r 1,000, tail_groups 8, block_rows 500); eval seed = the dataset's data seed |

## 2. THE rule applied to the pair (exactly what `gb_imax_rule.py` computes)
**Fits and data.** Dataset A = `5-AR-n200-r01` (data seed 502020001, engine seed 502020001). Pilot = I_max 0 (`…-V-s1`), twin = I_max 3 (`…-VI3-s1`). **Optional dataset B** (if HQ approves design B, `GB_PLAN` §3) = `5-ADJOPP-n200-r01` (data seed 505020001, engine seed 505020001), same two arms. One seed per arm, **the same seed in both arms of a dataset**; no second seed, no R′ change.

**Quantities (PREREG §3.1, with the §8 erratum).** Per fit: M1 = `fit.meta.occ[M = 1000].sd_log_Z_occ_r`; M2 = `pip.island_spread.max_sd`; M3 = `evidence.sigma_hat` = **sd(log Ẑ_r)** over the 16 final islands (not sd(Ẑ_r / Ẑ)); HPM = `selection.hpm`. Per dataset d and metric k: **r_{k,d} = M_k(I_max 0 fit) / M_k(I_max 3 fit)** (the registered rule's "mean over the replicates" is the single fit).

**Rule.** Let r_k = the geometric mean over the datasets present of r_{k,d} (one dataset: r_k = r_{k,A}). **I_max = 0 PASSES iff, for each k ∈ {1, 2, 3}: r_k ≤ 1.15, AND r_{k,d} ≤ 1.30 for every dataset d, AND `selection.hpm` is identical in the I_max 0 and I_max 3 fit of every dataset.** Otherwise FAIL.
- **n = 1 dataset (design A, approved):** the two bars apply to the same number, so **the binding condition is r_k ≤ 1.15** (the 1.30 clause cannot bind when 1.15 holds). Stated so nobody reads the 1.30 as a margin for the pair.
- **n = 2 datasets (design B):** the rule is the registered one with 2 datasets × 1 replicate: the geometric mean ≤ 1.15 **and** each dataset ≤ 1.30.
- **Not used by the rule:** Δ log Ẑ, E1–E3, `grid_fallback`, cost. They are reported beside it (§4 table). `grid_fallback` True in either fit does not change the outcome; it is flagged to HQ at the read-back (no default action).

**Edge cases, fixed now.**
| case | outcome |
|---|---|
| a field missing, or a denominator = 0 or non-finite | **NOT EVALUATED** → HQ (no default) |
| a fit not delivered after one infrastructure rerun, or an identity failure (recorded arm ≠ plan, rule ≠ bounded, `I_used` > `I_max`, no calibration record) | **INCOMPLETE** → HQ (rerun or hold); never scored |
| both M_k below any floor | **no floor**: the registered rule has none; the target margins (§5 C2) are printed beside the ratios |
| the I_max 0 fit installs the pilot-schedule fallback (`grid_fallback`) | scored as is; flagged |
**Consequence (H-30 (1)):** PASS → the 10⁵ rung and the 1M fits run at I_max = 0. FAIL → **both use I_max = 3**; the 10⁴ science stands as run (I_max 0, N 2,500, m 1) and is **reported per configuration**. No post-hoc override either way (the FZ precedent). The pilot is rung fit 1 on PASS; the twin is rung fit 1 on FAIL.

## 3. What one pair can and cannot decide: operating characteristics (assumptions labelled)
**Inputs, all from 10⁴ data (the only data that exist):** the 14 same-seed pairs of the precision leg (the `VF` fit, I_max 0, against the overlap V fit, I_max 3, same data, same engine seed, R′ = 16, N 2,500, m 1; `tools/pair_ratios.py`, output `tools/pair_ratios_output.txt`).
| metric | r over the 14 pairs | note |
|---|---|---|
| M1 | **0.999–1.001 in 14/14** (gmean 1.000) | the arms' island occupancy spreads were identical to ≥ 3 digits; cause not examined |
| M2 | **0.999–1.001 in 14/14** | same |
| M3 | 13 non-NULL pairs: 0.85–1.37, gmean 1.022, **sd(log r) 0.123**, **12/13 ≤ 1.15** (the NULL pair, σ̂ = 0.001, is 1.000; 13/14 overall); the exceedance is AR r04 s2 (1.373) | the only discriminating metric at 10⁴ |
| HPM | identical in 14/14 | |
For comparison the registered study at R′ = 64, 3 datasets × 2 replicates, different seeds per arm: r(M1) 0.971, r(M2) 0.932, r(M3) 1.130.
**Resulting characteristics (model: ln r_3 ~ N(ln ρ, 0.123²), M1 and M2 treated as deterministic ≈ 1; an assumption, not a result at 10⁵):**
| true ratio ρ of M3 | P(pair PASSES), design A (n = 1, r_3 ≤ 1.15) | P(PASSES), design B (n = 2: gmean ≤ 1.15 and each ≤ 1.30) |
|---|---|---|
| 1.00 | 0.87 | 0.93 |
| 1.13 (the 10⁴ R′ = 64 estimate) | 0.56 | 0.55 |
| 1.30 | 0.16 | 0.07 |
| 1.50 | 0.02 | 0.00 |
**Reading.** (i) One pair is a **coarse test**: P(pass) is about 0.9 if I_max = 0 is truly equivalent and about 0.6 at the registered study's own point estimate (1.13), so a PASS is weak evidence of non-inferiority and a FAIL is weak evidence of inferiority. (ii) The registered point-estimate ADOPT at 10⁴ itself sat ≈ 0.5 s.e. inside the margin (FZ addendum §2); the 10⁵ pair inherits that. (iii) The pair is **paired by seed** (same data, same position-addressed random numbers); that is what makes M1 and M2 near-deterministic at 10⁴ and the M3 ratio sd 0.12 rather than the 0.10–0.27 per-fit figures of PREREG §3.2 (different seeds). (iv) **At 10⁵ the M1 / M2 ratios may stop being ≈ 1** (the coded rule's grid kept changing for 13–15 rebuilds at p ≥ 5k, FZ addendum §3; the preliminary grid may degrade faster with p): that is exactly what the pair can detect. (v) **Cost asymmetry:** a false FAIL costs ≈ 9.5 per 10⁵ fit and ≈ 121 per 1M fit (≈ 2.5k over 20 replicates, ≈ 9 % of 28.3k); a false PASS costs a σ̂ ≈ 13 % wider at 1M with M1 and M2 unaffected at 10⁴. Both are affordable, which is the reason a coarse test is accepted. (vi) **Design A cannot cover the design that matters most** (ADJ-OPP: the one σ̂ = 1.09 outlier at I_max 0, r04 s1, has no I_max 3 twin); design B adds it for ≈ +49.
**Not asked of this pair:** a second seed, R′ = 64, a third dataset (`GB_PLAN` §3 prices them: +70, +172, +≈ 49 each).

## 4. Decision table (registered)
| outcome | rung and 1M | 10⁴ science | what the pair's fits are |
|---|---|---|---|
| PASS | I_max 0 (frozen) | stands | pilot = rung fit 1; twin reported |
| FAIL | I_max 3 | stands, reported per configuration | twin = rung fit 1; pilot reported; G-B cost / precision / memory move to the twin |
| NOT EVALUATED / INCOMPLETE | HQ decides (rerun or hold) | stands | none is a rung fit until HQ rules |
Reported with the verdict, never part of it: r_k with the n; M1–M3 of both fits against §0-v2.3; Δ log Ẑ (I_max 0 − I_max 3) in units of the island s.e.; stage counts T and wall of each grid; calibration core-h saved; final-merge E1–E3, `low_empirical_ESS`, `checks_passed_final`, sd(log Ẑ_r) > 1; `occ_inhomogeneous`; calibration E1 / E2 as **NOT EVALUATED** and `grid_unconverged` / `I_used` / `checks_passed_calibration` as the I_max-0 constants outside any quality aggregate (CAMPAIGN_FREEZE_ADDENDUM §2 and errata); whether the twin reproduces T5's island hashes (informational).

## 5. The G-B criteria, registered (ENGINEERING_SPEC §0-v2.6 G-B; EXPERIMENT_PLAN G-B; H-26 Q4)
Evaluated on the **winning configuration's fit** (the pilot on PASS, the twin on FAIL); both are reported.
| # | criterion | registered pass condition |
|---|---|---|
| C1 cost | ≤ 1.5× model, with the Q4 guard | fit billed core-h (sacct CPUTimeRAW, all stages) ≤ 1.5 × the committed class model, **model = the committed table, never re-fitted**: N* 2,500: pilot E **31** (46.5; hard 77.5), twin E **40** (60; hard 100); N* 10⁴: pilot **110** (165; 275), twin **120** (180; 300). A class of one fit: the class mean is the fit, and the 2.5× guard is the STOP line. Beside it, not a criterion: the ratio to the manifest planning value 96 |
| C2 precision | §0-v2.3, at R′ = 16 | **M1 ≤ 0.05; M2 ≤ 0.005 (engine `target_met` True); \|log Ẑ − log Ẑ_occ(M = 1,000)\| ≤ 3 √(se_Z² + se_occ²) (se = sd over islands / √16); HPM certified by the final local search (`local_certified`)**; and max_j \|PIP_eq − PIP_𝒯\| ≤ 0.01 + (1 − π̂(𝒯)) if the field exists (not verified). Reported, not gating: M3 ≤ 0.5 (goal); `occ_inhomogeneous` (flag only); "same best model in 16 of 16 islands" **not computable** (no per-island HPM; PREREG §3.1) |
| C3 memory | < request | MaxRSS < the stage's request in **each** of setup 16 G, calibrate 16 G, islands 8 G, merge 24 G, eval 16 G (advisory > 80 %); peak < 50 % of a node recorded |
| C4 completion | delivered | both fits delivered, one binary sha256 = F2's, arm identity verified, `logZ_r` length 16 and finite |
| C5 E2 recorded | EXPERIMENT_PLAN G-B | reported per §4 |
| C6 I_max rule | §2 | PASS or FAIL recorded |
**G-B passes iff C1–C4 pass (after a memory resize, if any) and C6 is PASS or FAIL.**
**Misses (registered, no discretion):** C1 in (1.5×, 2.5×]: G-B cost FAIL, the rung and the 1M block re-quoted from the measured fit, HQ releases; > 2.5×: STOP. C2: G-B precision FAIL, rung not auto-released, HQ gets the priced options (accept as a reported miss; R′ 32 for the rung ≈ +28 per fit; hold); **never an estimator switch** (§0-v2.3). C3: re-size the request to 1.3 × the measured peak, rerun the stage, re-evaluate ("PASS after resize"). C4: one infrastructure rerun, then INCOMPLETE → HQ. The pilot's HPM ≠ S₀ ({10000, 30000, 50000, 70000, 90000}) is a flag to HQ, not a criterion.

## 6. Disclosures
- **What I looked at on real data before registering.** (i) The F2 identity record and the T5 / 1M pilot cost records (documents). (ii) **The 14 same-seed I_max 0 / I_max 3 pairs of the 10⁴ leg:** M1, M2, M3 and HPM from their eval records, to price the pair's resolution (`tools/pair_ratios_output.txt`, §3). They are 10⁴ fits already read by the leg (FZ, LEG_READBACK); nothing at 10⁵ exists for this gate; no threshold was tuned on them. (iii) No 10⁵ I_max 0 fit and no 10⁵ pair exists.
- **Limits.** The §3 characteristics assume a log-normal M3 ratio with sd 0.123 estimated from 13 pairs, M1 and M2 ≈ 1, and that 10⁵ behaves like 10⁴ in its noise (untested). The 14 pairs are at n = 200, p = 10⁴, single seed each, designs AR (8), AR-weak (2), ADJ-OPP (2), IND (1), NULL (1).
- **Fields not verified at F2 / 10⁵:** PIP_𝒯 agreement field; `local_certified` name; π̂(S₀); `calib_meta.json` content at 10⁵ (the leg's collection plan produced it at 10⁴).
- **Choices I fixed that HQ or the reviewer may overrule before the commit** (each a line in a script constant or a table cell): the 1.15 / 1.30 are the registered values, unchanged; design B (ADJ-OPP) is **a request**; the merge request 24 G; the islands limit 0:20 / 0:45; the class models 31 / 40 (110 / 120 at N* 10⁴); NOT EVALUATED / INCOMPLETE → HQ with no default.
- **Mini-leg interplay.** If N* = 10⁴ is adopted, the frozen combination (N 10⁴, I_max 0) was run only in this pair, and at 10⁵ (the mini-leg's N = 10⁴ arms are I_max 3 at p = 10⁴). The 10⁴ science (N 2,500, I_max 0) stands as run.

## 7. Carry rules from the leg (L-8, L-12, errata)
Scripts registered **before the pilot is submitted** (stronger than "before the first read"); `law.bin` and `data.bin` kept for both fits from the start (L-12); the registered `precision_freeze.py` is not edited and not used (its regex and its `cost_batch.json` glob are the leg's); M3 is sd(log Ẑ_r); E1 / E2 calibration triggers are NOT EVALUATED at I_max 0, the final-merge flags are reported as frequencies.

## 8. Deviation log
None yet. A change to any threshold, rule, field choice or script after the shas of §1 are committed is a logged deviation with the reason, the date and the new sha256.
