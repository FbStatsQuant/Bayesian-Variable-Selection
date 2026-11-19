# W3 READ-BACK, 10⁴ T-vs-V overlap (Sonnet worker, 2026-11-19; per-wave checks; the rung verdict draft is `OVERLAP_1e4_VERDICT_DRAFT.md`)

## Summary (10 lines)
1. **W3 is clean: 12/12 fits COMPLETED, collected, verified; no stop rule; no T fit escalated (0 of 6).** All 6 AR T fits ran at tier 0, N = 10,000, and are full valid fits. All 40 fits of the rung now exist. Nothing was submitted, cancelled or deleted on NOTS.
2. Collected: 14 units (12 fits + `_batch_OV_W3_{T,V}`) under `records/overlap1e4/W3/`, 2.2 GB, one SHA256SUMS per unit, 0 nested, `sha256sum -c` OK ("collected: 14 units verified, 0 problems"). `/` stays 85 % (70 G, 60 G used), records on NFS 39 %: nothing near 92 %. The manager was sent the one-line "W3 collected" message as soon as the collection verified.
3. W3 billed **256.64 core-h** (T 244.50, V 12.14; sacct CPUTimeRAW/3600) = 52 % of the 490 quote, **below the W2 model's P10 (322)** and far under its E (482). Cumulative W0 + W1 + W2 + W3 = **1,010.43** (monitor 1,010.4). T per fit: AR r02 s1 39.31, s2 41.88; r03 s1 35.82, s2 39.44; r04 s1 **51.49**, s2 36.56 (the six cost 35.8–51.5, as expected; none escalated); V 1.71–2.43 each.
4. **The AR T fits did not escalate:** calibration converged at tier 0 in 8, 12, 11, 12, 11 and 7 rebuilds (cap 14); no tier-1 cost file exists in any W3 fit; `calib.bin.json` tier_final 0, N_final 10,000. AR strong has 1 escalation in 8 T fits (AR r01 s1); the rung has **3 in 20 T fits** (W0 AR s1, W1 IND s2, W1 ARweak s1).
5. Cross-Hellinger (criterion H): d_H(V,T)/d_H(T,f*) = **0.0089, 0.0090 (r02), 0.0113, 0.0118 (r03), 0.0126, 0.0125 (r04)** vs limit 0.10. Same xeval binary as W1/W2 (afef0e46…, from b89cba4d), guard accepted all 6 pairs unpatched. **Self-check B = truth is bit-exact for 12 of 12 W3 fits** (no new 1-ulp miss; the rung has 1 miss in 40, W2 AR r01 T s2).
6. **Registered `compare_overlap.py` (311bbad8…) and `compare_overlap_v2.py` (4f402e51…) agree on every shared cell for W3** (12/12 delivered in both; 0 differing cells; no escalated fit, so ADDENDUM_1 changes nothing). ADDENDUM_2 sha 4985833d… verified.
7. Per-pair criteria (v2, W3): D, PAIR, S1, S2, S3, P, E2, H, C all pass; E1 island-only inside 3 s.e. everywhere (worst r04 s2 1.58). HPM = MPM = {1000, 3000, 5000, 7000, 9000} in all 6 pairs, F_T − F_V ≤ 0.
8. `cross_vt_all.json` (all 20 cells, 10 datasets × 2 seeds) written; **both scripts ran in full mode over W0–W3 with it (Part B, `final/`)**: v2 CLEAN pending review (40/40, every criterion PASS), registered not CLEAN (D 37/40). See the verdict draft.
9. Stop rules, last probe `probe_20261119T082611Z.txt` (`W3_readback/stop_rules_W3_last_probe.txt`): wave 256.6, cumulative 1,010.4, 12 COMPLETED, 3 datasets paired, **no stop rule fired**.
10. Not fixed (ops tools, as before): `bin_version.json` loader error in `collect_nots.sh`; `monitor/cumulative.json` lists W0–W2 only. NOTS clean-up of the W3 run dirs waits for the manager (units are in `records/`; desktop verification is a separate step).

## 1. Collection
`ARMS="T V" nice -n 19 tools/collect_wave.sh W3` (the tool's own ssh / rsync over its one ControlMaster connection; I made no other NOTS call). Log `tmp/20261119-w3readback/collect.log`: OV_W3_T 6 run dirs + 165 batch extras, OV_W3_V 6 + 308; "cost: 6 runs, 244.50 billed core-h" (T), "12.14" (V); "collected: 14 units verified, 0 problems", rc 0. Re-checked by hand: `sha256sum -c` OK in all 14 units, exactly one `SHA256SUMS` per unit (fit units 68–88 files, batch units 178 / 321), no `INCOMPLETE.txt`. **Disk before and after: `/` 70 G, 60 G used, 85 %; records on `yorick:/u/grads/fb31` NFS 4.4 T, 39 %.**
Binary provenance in every record's `binary` block: git_commit eefcbc4a2ab42fdf52ec1e5d318a956bdd07f463 (F), T sha 182c3b62… (portable ISA), V sha 4fecb186… (sapphirerapids); libm self-test pass. All 168 sacct job rows COMPLETED (T limits as deployed: calibrate **05:00:00**, islands 02:00:00, setup 00:15, merge 00:20, eval 00:30). Peak: T calibrate 2,892 s (r04 s1) vs 18,000 s; T islands 380–553 s.
Known flaw (unchanged, ops tool, not fixed): `_batch_OV_W3_{T,V}/bin_version.json` holds a libstdc++ loader error (`CXXABI_1.3.15 not found`), not a version. Observation (unchanged): `eval.bin.json params.seed` is the data seed, not the engine seed, in both arms.

## 2. Per T fit: tier, N_final, cost (`W3_escalation.csv`, `W3_cost_stages.csv`, `W3_sacct_jobs.csv`: 168 job rows, 72 stage rows; same formats as W2)
| fit | tier_final / N_final | rebuilds t0 / t1 | calibrate core-h (wall) | islands at N_final core-h (wall max) | merge + eval | total |
|---|---|---|---|---|---|---|
| AR r02 s1 | 0 / 10,000 | 8 / – | 27.01 (2,026 s) | 12.19 (553 s) | 0.073 | **39.31** |
| AR r02 s2 | 0 / 10,000 | 12 / – | 31.65 (2,374 s) | 10.11 (403 s) | 0.091 | **41.88** |
| AR r03 s1 | 0 / 10,000 | 11 / – | 25.51 (1,913 s) | 10.21 (519 s) | 0.071 | **35.82** |
| AR r03 s2 | 0 / 10,000 | 12 / – | 29.64 (2,223 s) | 9.69 (380 s) | 0.080 | **39.44** |
| AR r04 s1 | 0 / 10,000 | 11 / – | 38.56 (2,892 s) | 12.83 (500 s) | 0.073 | **51.49** |
| AR r04 s2 | 0 / 10,000 | 7 / – | 22.93 (1,720 s) | 13.53 (514 s) | 0.060 | **36.56** |
| V (6 fits) | 0 / 2,500 | 3 each | 0.44–0.94 (99–211 s) | 1.11–1.40 (71–92 s, 16 tasks) | 0.069–0.091 | 1.71 (r03 s2) … 2.43 (r04 s1) |
Setup 0.027–0.033 per fit. **Full and valid (`W3_T_fit_validity.csv`, `w3_t_validity.py`): all 6 T fits** have 4 islands at N = calib N_final = 10,000 (tier 0), calib `cal_status` ok, merge and eval COMPLETED, non-stub `fit.bin` 22.3–22.5 MB, `law.bin` 149–153 MB, `eval.bin` 347 KB, law M = 400,001, R_eff 3.9989–3.9999, `run_manifest calib_N` N_final 10,000 not differing. No `cost_*_t1_*` file in any W3 fit; the tier-1 grid in `settings.tiers` (N 40,000) was configured and never run. Calibrations ran on 6 different nodes. **Did any AR T fit escalate? No (0 of 6).** The two slowest calibrations (r04 s1 2,892 s, r02 s2 / r03 s2 at 12 rebuilds) stayed under the cap.
**Cost by tier, all 20 counted T fits:** tier 0 (17 fits) mean **33.2** (2.3–51.5); tier 1 (3 fits) mean **104.9** (60.7, 110.1, 144.0). T counted total 879.08, V counted 39.85, W0 evidence 91.51 = 1,010.43.
Observation, not an error: AR r03 T s1 and s2 have **bit-identical** `predictive.h2` (0.003702563657549063), `logZ_T`, F and HPM: the two T stores hold the same models, so the store-BMA predictive does not depend on the engine seed; log Ẑ itself differs (−182.7313 vs −182.7320).

## 3. Cross-Hellinger (criterion H)
`~/SMC_Engineering_Department/tmp/20261119-w1readback/xeval_build/smcbvs4_xeval` (sha256 afef0e46…, origin/exp/P1M-engine b89cba4d, merge of #87); `W3_readback/cross/run_cross.sh`: `cross --a <V law.bin> --b <T law.bin> --truth <V truth.json> --data <V data.bin> --data-b <T data.bin> --dataset ID --seed-id s --threads 3` and per fit `--b-truth 1` for the self-check. **No guard bypass, no patched build:** the X/y section-hash guard accepted all 6 pairs. `merge_cross.py` → `W3_readback/cross_vt.json` (3 datasets, 6 cells); `merge_all_cross.py` merges W0–W3 `cross_vt.json` → **`cross_vt_all.json` (10 datasets, 20 cells)**.
| pair | h² (se) | d_H(V,T) | d_H(T,f*) | ratio (limit 0.10) |
|---|---|---|---|---|
| AR r02 s1 | 3.20e-7 (6.9e-8) | 5.66e-4 | 0.06338 | **0.0089** |
| AR r02 s2 | 3.25e-7 (7.5e-8) | 5.70e-4 | 0.06327 | **0.0090** |
| AR r03 s1 | 4.75e-7 (1.5e-7) | 6.89e-4 | 0.06085 | **0.0113** |
| AR r03 s2 | 5.15e-7 (1.9e-7) | 7.17e-4 | 0.06085 | **0.0118** |
| AR r04 s1 | 2.86e-7 (4.8e-8) | 5.35e-4 | 0.04237 | **0.0126** |
| AR r04 s2 | 2.81e-7 (4.6e-8) | 5.31e-4 | 0.04252 | **0.0125** |
**Self-check B = truth** (`selfcheck_bitexact.txt`, `selfcheck.py`): xeval `h2` against `eval.bin.json dist.T.predictive.h2` is **bit-equal in 12 of 12** fits (6 V, 6 T). Across the rung: W0 4/4, W1 12/12, W2 11/12 (AR r01 T s2, 1 ulp), W3 12/12 = **39 of 40**. All 20 cross cells over W0–W3: ratios 0.0034–0.0140, max 0.0140 (ADJ-OPP r02 s2).

## 4. Read-back table, registered vs v2 side by side (`--wave-check --cross-file W3_readback/cross_vt.json --cost-dir …/_batch_OV_W3_{T,V}/cost`; outputs `W3_readback/registered/`, `W3_readback/v2/`)
Hashes verified: `compare_overlap.py` 311bbad886fc61c679ac47d1c30faf8d8897e33681baf5711f1f268472632eea, `compare_overlap_v2.py` 4f402e5127efd4754cf25e4ade6ad799f697ebc28e1c657ff49f93fd2905b5c6, `PREREG_ADDENDUM_2.md` 4985833d479f1de5b9446cafe69b908940af446bc493d479d5394ded904d3230 (all as registered). Both run on the same records, `python3 -I`, rc 0.
**Delivery on W3: registered 12 of 12, v2 12 of 12. The two outputs are identical in every shared column of `wave_check.csv` and `per_fit.csv` (0 differing cells); v2 only adds `tier_final_*` / `N_final_*` (T 0 / 10,000, V 0 / 2,500).**
| pair | HPM T = V (MPM equal) | F_T − F_V | max abs ΔPIP; worst ratio | log Ẑ V (isl s.e.) / T | Δlog Ẑ (V−T); in isl s.e. | log Z_T lb V / T | gap log Ẑ − lb V / T |
|---|---|---|---|---|---|---|---|
| AR r02 s1 | {1000,3000,5000,7000,9000} (yes) | −8.5e-14 | 1.5e-4; 0.015 | −208.1952 (0.0040) / −208.1935 (0.0057) | −0.00174; **0.25** | −208.325277 / −208.325277 | 0.130 / 0.132 |
| AR r02 s2 | same (yes) | −8.5e-14 | 1.4e-4; 0.014 | −208.1858 (0.0069) / −208.1876 (0.0054) | +0.00187; **0.21** | −208.325277 / −208.325277 | 0.140 / 0.138 |
| AR r03 s1 | same (yes) | −5.7e-14 | 1.5e-4; 0.015 | −182.7290 (0.0041) / −182.7313 (0.0025) | +0.00231; **0.48** | −182.863642 / −182.863642 | 0.135 / 0.132 |
| AR r03 s2 | same (yes) | −5.7e-14 | 1.1e-4; 0.011 | −182.7363 (0.0025) / −182.7320 (0.0030) | −0.00430; **1.11** | −182.863642 / −182.863642 | 0.127 / 0.132 |
| AR r04 s1 | same (yes) | −2.8e-14 | 6.2e-5; 0.006 | −212.9449 (0.0054) / −212.9383 (0.0047) | −0.00662; **0.93** | −213.058521 / −213.058521 | 0.114 / 0.120 |
| AR r04 s2 | same (yes) | −2.8e-14 | 5.5e-5; 0.005 | −212.9480 (0.0050) / −212.9309 (0.0096) | −0.01710; **1.58** | −213.058521 / −213.058521 | 0.110 / 0.128 |
| pair | T tier / N | d_H(T,f*) / d_H(V,f*) | plug-in h² HPM = MPM (T = V) | core-h T / V |
|---|---|---|---|---|
| AR r02 s1 | 0 / 10,000 | 0.06337 / 0.06338 | 0.004060 | 39.31 / 1.99 |
| AR r02 s2 | 0 / 10,000 | 0.06326 / 0.06324 | 0.004060 | 41.88 / 2.08 |
| AR r03 s1 | 0 / 10,000 | 0.06085 / 0.06090 | 0.004003 | 35.82 / 1.72 |
| AR r03 s2 | 0 / 10,000 | 0.06085 / 0.06090 | 0.004003 | 39.44 / 1.71 |
| AR r04 s1 | 0 / 10,000 | 0.04237 / 0.04236 | 0.001716 | 51.49 / 2.43 |
| AR r04 s2 | 0 / 10,000 | 0.04252 / 0.04237 | 0.001716 | 36.56 / 2.21 |
X/y sha (truth.json) equal over the four fits of each W3 dataset and different across the datasets. log Z_T (deterministic lower bound) is the same for V and T to 6 decimals in each pair and ≤ log Ẑ in all 12 fits.
**r04 s2 is the largest V − T gap of the rung (−0.0171, 1.58 island s.e.) and it is a tier-0 T fit (7 rebuilds).** Analysis in the verdict draft §3.

## 5. Per-pair criteria status (W3; NOT the verdict)
D 12/12; PAIR PASS; S1 equal 6/6 (all 10 datasets equal over the rung); S2 PASS (ΔF ≤ 0); S3 6/6; S4: no NULL fit in W3, the W1 result stands; P PASS (worst ratio 0.015, max abs ΔPIP 1.5e-4 vs floor 0.01); E1 island-only inside 3 s.e. (worst 1.58); E2 PASS (lb ≤ log Ẑ, gaps 0.110–0.140); H PASS (≤ 0.0126); C PASS (T max 51.49 ≤ 172.5, V max 2.43 ≤ 15).

## 6. Open points for the manager / HQ
- **Escalation did not appear in W3** (0 of 6; the W2 model expected 2.66, P(none) 0.08): AR strong is 1 of 8; the rung 3 of 20 (15 %, exact 95 % interval 3.2–37.9 %).
- The registered script prints **MARGINAL** on the full pooled run (S1 "7/10"), not INCOMPLETE; see the verdict draft §2 for the reading of §4. v2 prints CLEAN. The draft is ready for the Opus review (H-24 (4)).
- Tool flaws unchanged: `bin_version.json` (collect_nots.sh runs `smcbvs4 version` without `env.sh`); `monitor/cumulative.json` lacks W3. Not edited.
- NOTS clean-up of the W3 run dirs waits for the manager's OK and the desktop check.

Files: `results/overlap1e4/W3_readback/` = `W3_escalation.csv`, `W3_cost_stages.csv`, `W3_sacct_jobs.csv`, `w3_readback_tables.py`, `W3_T_fit_validity.csv` + `w3_t_validity.py`, `cross_vt.json`, `cross_vt_all.json` + `merge_all_cross.py`, `cross/` (6 cross + 12 self-check records, `run_cross.sh`), `selfcheck_bitexact.txt` + `selfcheck.py`, `registered/`, `v2/` (`wave_check.csv`, `per_fit.csv`, `stdout.txt`), `stop_rules_W3_last_probe.txt`, `final/{registered,v2}/` (Part B), `cross_w0_recheck/` (the 2 W0 pairs re-run with the PR #87 guard, bit-equal to the bypassed cells), `e1_escalation.py` + `e1_escalation_output.txt` + `e1_escalation_pairs.csv`. Scratch: `SMC_Engineering_Department/tmp/20261119-w3readback/` (collect log). No git state changed; nothing committed; no BNP files touched; nothing in /tmp.
