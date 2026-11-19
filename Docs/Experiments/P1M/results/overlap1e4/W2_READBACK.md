# W2 READ-BACK, 10⁴ T-vs-V overlap (Sonnet worker, 2026-11-19; per-wave checks only, NOT the rung verdict)

## Summary (10 lines)
1. **NOT CLEAN, one item, and it is a 1-ulp difference.** The xeval self-check (B = truth) is bit-exact for **11 of 12** fits; **AR r01 T s2** differs from the engine's `predictive.h2` by 1.1e-16 (= 2⁻⁵³, the last bit of `1 − X`; 1.5e-14 relative), identical at 1, 3 and 8 threads (§4). The brief said "must be bit-exact for all 12", so I report it as not met; the cross value of that pair (h² 4.1e-7, s.e. 1.2e-7) is unaffected in any way that matters. Everything else is clean: 12/12 fits COMPLETED, all T fits full and valid, no stop rule, nothing submitted, cancelled or deleted.
2. Collected: 14 units (12 fits + `_batch_OV_W2_{T,V}`) under `records/overlap1e4/W2/`, 2.1 GB, one SHA256SUMS each, 0 nested, `sha256sum -c` OK, 0 problems ("collected: 14 units verified, 0 problems"). `/` stays 85 % (checked before and after), records on NFS at 39 %. Nothing on NOTS beyond the collect tool's own calls over its one connection.
3. W2 billed **221.15 core-h** (T 207.09, V 14.06; sacct) = 46 % of the 480 quote. Cumulative W0 + W1 + W2 = **753.79** (monitor 753.8). **No T fit escalated: 0 of 6** (all tier 0, N 10⁴). T per fit: ARweak r02 s1 23.16, s2 7.66; ADJ-OPP r01 s2 36.73, r02 s1 47.41, r02 s2 43.13; **AR r01 s2 49.01**; V 1.76–2.91 each.
4. **HQ's question, AR r01 s2 (49.01, ~43-min calibrate): yes, tier 0, the non-escalation case.** It needed **12 tier-0 rebuilds** (cap ℓ = 14) and **converged**: `calib.bin.json` tier_final 0, N_final 10,000, cal_status ok, no tier-1 cost files. Calibrate 2,558 s (34.11 core-h), islands 14.82, merge + eval 0.05. W0's AR r01 s1 (same dataset, other engine seed) hit the cap at 14 and escalated: 110.12.
5. All 6 T fits are **full valid fits**: 4 islands each at N = calib N_final = 10,000, merge and eval COMPLETED, non-stub `fit.bin` 19.5–23.3 MB, `law.bin` 104–168 MB, `eval.bin` 347 KB, law M = 400,001, R_eff 3.9975–3.9998 (`W2_T_fit_validity.csv`). Escalations to date: **3 of 14 T fits** (W0 AR s1; W1 IND s2, ARweak s1); none in W2.
6. Criterion H: d_H(V,T)/d_H(T,f*) = **0.0119 (ADJ r01 s2), 0.0133, 0.0140 (ADJ r02 s1, s2), 0.0075 (AR r01 s2), 0.0034, 0.0037 (ARweak r02)** vs limit 0.10. Guard accepted all 6 pairs, unpatched, same binary as W1 (afef0e46…, built from b89cba4d).
7. **Registered `compare_overlap.py` (311bbad8… verified) and `compare_overlap_v2.py` (4f402e51…) agree on every cell for W2** (12/12 delivered in both; no T fit escalated, so ADDENDUM 1 changes nothing here). ADDENDUM_2 sha 4985833d… verified. Pooled over W0 + W1 + W2 (28 fits read): **v2 28/28 delivered, registered 25/28** (the 3 escalated T fits are "not delivered").
8. Per-pair criteria (v2): D, PAIR, S1, S2, S3, P, E2, H, C all pass; E1 island-only inside 3 s.e. everywhere (worst W2 0.58, ADJ r02 s1). **First seed-pooled values (scripts' own multi-root mode, W0 + W1 + W2): AR r01 E1 V − T = −0.00964 (se_comb 0.00588, ratio 1.64), ADJ-OPP r01 −0.00072 (0.00850, ratio 0.09); S1 HPM equal in both seeds of both.** E1 sign: V − T negative in 11 of 14 pairs; mean −0.0115 where T escalated (3 pairs, all negative) vs −0.0017 where it did not (§5).
9. W2 came in **below the W1 model's P10** (221 vs E 400, P10 250; P(W2 ≤ 221) = 0.054; 0 of 6 escalated vs 2.8 expected, P = 0.044). Re-projection (Opus model, W2 added, W3 at 5:00): **W3 E 482 (P10 / P50 / P90 322 / 473 / 648); rung E 1,235 (1,076 / 1,226 / 1,402); P(> 1.6k) 0.009, P(> 2.1k) < 0.0001, P(> 2.5k) ≈ 0; P(any W3 T fit > 172.5) 0.118.** AR P(escalate) posterior 0.44 (P10–P90 0.23–0.67; was 0.67); a plain Beta update of the old prior with 1 of 2 gives 0.73.
10. **Material move vs REPROJECTION_W1: yes, downward** (rung E −19 %, P90 −24 %; W3 E −20 %; the P90 now sits under 1.6k, previously above). **Recommended W3 QUOTE: 490** (E(W3) 482 is outside the 580–700 band; stop > 980). `stop_rules.py` on the last probe: **no stop rule fired** (wave 221.2, cumulative 753.8, 4 datasets paired).

## 1. Collection
`ARMS="T V" nice -n 19 tools/collect_wave.sh W2` (the tool's own ssh / rsync calls over its one ControlMaster connection; I made no other NOTS call and did not poll). Log `tmp/20261119-w2readback/collect.log`: OV_W2_T 6 run dirs + 165 batch extras, OV_W2_V 6 + 308; "cost: 6 runs, 207.09 billed core-h" (T), "14.06" (V); "collected: 14 units verified, 0 problems", rc 0. Re-checked by hand: `sha256sum -c` OK in all 14 units, exactly one `SHA256SUMS` per unit (fit units 44–88 files, batch units 178 / 321), no `INCOMPLETE.txt`. **Disk before: `/` 70 G, 60 G used, 85 %; records on `yorick:/u/grads/fb31` NFS 4.4 T, 39 %. After: unchanged** (copy goes to NFS only; 2.1 GB). Neither is near 92 %.
Binary provenance in every record's `binary` block: git_commit eefcbc4a2ab42fdf52ec1e5d318a956bdd07f463, T sha f90aa3f6… (portable ISA), V sha 1e375b74… (sapphirerapids); libm self-test pass. All 168 sacct job rows are COMPLETED (no refused attempts, no OUTCOME or resource-limit records).
Known flaw (unchanged, ops tool, not fixed): `_batch_OV_W2_{T,V}/bin_version.json` holds a libstdc++ loader error (`CXXABI_1.3.15 not found`), not a version (`collect_nots.sh` runs `smcbvs4 version` without `env.sh`). Observation (unchanged): `eval.bin.json` `params.seed` is the **data seed** (e.g. 402020001 for AR r01 s2; s2 island seed = data seed + 100), not the engine seed; both arms agree, no effect on the checks.

## 2. Per T fit: tier, N_final, cost (`W2_readback/W2_escalation.csv`, `W2_cost_stages.csv`, `W2_sacct_jobs.csv`: 168 job rows, 72 stage rows; same formats as W1)
| fit | tier_final / N_final | rebuilds t0 / t1 | calibrate core-h (wall) | islands at N_final core-h (wall max) | merge + eval | total |
|---|---|---|---|---|---|---|
| ARweak r02 s1 | 0 / 10,000 | 10 / – | 16.56 (1,242 s) | 6.52 (262 s) | 0.049 | **23.16** |
| ARweak r02 s2 | 0 / 10,000 | 1 / – | 1.65 (124 s) | 5.92 (236 s) | 0.058 | **7.66** |
| ADJ-OPP r01 s2 | 0 / 10,000 | 9 / – | 25.24 (1,893 s) | 11.40 (453 s) | 0.056 | **36.73** |
| ADJ-OPP r02 s1 | 0 / 10,000 | 12 / – | 33.33 (2,500 s) | 13.99 (546 s) | 0.053 | **47.41** |
| ADJ-OPP r02 s2 | 0 / 10,000 | 10 / – | 30.47 (2,285 s) | 12.57 (504 s) | 0.053 | **43.13** |
| **AR r01 s2** | **0 / 10,000** | **12 / –** | **34.11 (2,558 s)** | **14.82 (558 s)** | 0.049 | **49.01** |
| V (6 fits) | 0 / 2,500 | 3 each | 0.58–1.10 (130–247 s) | 1.07–1.75 (73–111 s, 16 tasks) | 0.08–0.09 | 1.76 (ARweak s2) … 2.91 (ADJ r02 s2) |
Setup is 0.027–0.036 per fit. tier_final / N_final from `calib.bin.json`; rebuild counts from the `cost_diag_t0_k*` files (no `cost_*_t1_*` file exists in any W2 fit); every island json carries N = 10,000 and tier 0. Peak limits: T calibrate max 2,558 s vs 3:00 = 10,800 s; T islands max 558 s vs 2:00. Nodes: calibrations ran on 6 different nodes; per-rebuild wall 204–223 s (ADJ), 210 s (AR r01 s2, W0 s1 was 246 s T2 / 213 s evidence), 121 s (ARweak) (`reproj/rebuild_times_output.csv`).
**Cost by tier, all 14 counted T fits:** tier 0 (11 fits) **mean 29.1** (fast regime 2.3–7.7; slow regime 23–51, scaling with the rebuild count: 9 → 36.7, 10 → 23.2 / 43.1, 11 → 50.5, 12 → 47.4 / 48.3 / 49.0); tier 1 (3 fits) **mean 104.9** (unchanged). Slow-regime K0 so far: **9, 10, 10, 11, 12, 12, 12 converged and three at the cap (14+)**; nothing yet in 2–8. T counted total 634.58, V counted 27.71, W0 evidence 91.51 = 753.80.

## 3. HQ question: AR r01 s2 (49.01 core-h, ~43-min calibrate)
- **It is tier 0, and it did not escalate.** `calib.bin.json`: status completed, cal_status ok, **tier_final 0, N_final 10,000**, engine `seconds` 2,549 (sacct 2,558 s = 42.6 min on bb5u21c1). The tier-1 grid in `settings.tiers` (H 8192, N 40,000) was configured but never run: no tier-1 pilot / diag files, `run_manifest.calib_N` = {N_plan 10,000, N_final 10,000, differs false}.
- **Tier-0 rebuild count 12 (cap ℓ = 14), converged at rebuild 12** (cost files `cost_diag_t0_k1…k12_r1..r4`; 12 × ≈ 210 s = 2,507 s plus the pilot ≈ 60 s, the calibrate total). Escalation needs the cap (grid_unconverged) or another trigger; neither fired. The grid became identical two rebuilds short of the cap.
- **Against W0's AR r01 s1 (110.12):** same dataset (same X/y; X_y sha equal), other engine seed. s1 used all 14 tier-0 rebuilds (≈ 246 s each on the T2 node), did not converge, escalated to tier 1 (1 rebuild, 835 s) and ran its islands at N 40,000 (49.21). s2: no tier 1, islands at N 10⁴ (14.82). Cost 49.01 = 34.11 + 14.82 + 0.05 + 0.03 setup, against 110.12.
- **Full valid fit:** 4 islands COMPLETED at N 10,000 (seed 402020101, wall 550–558 s), merge and eval COMPLETED, `fit.bin` 22,389,184 B, `law.bin` 150,536,448 B, M 400,001, R_eff 3.9993, eval completed; HPM {1000, 3000, 5000, 7000, 9000} (same as V and as s1).
- So AR is **1 escalation of 2** (s1 yes, s2 no), the first sign that AR is not certain to escalate; the tier-0 K0 of 12 is close to the cap, so a second AR seed escalating on W3 data is entirely plausible (§7).

## 4. Cross-Hellinger (criterion H)
The W1 xeval binary `~/SMC_Engineering_Department/tmp/20261119-w1readback/xeval_build/smcbvs4_xeval` (sha256 afef0e46…) was built from **origin/exp/P1M-engine b89cba4d** (the brief's "b89cba4d or later"), so I did not rebuild; `W2_readback/cross/run_cross.sh`: `cross --a <V law.bin> --b <T law.bin> --truth <V truth.json> --data <V data.bin> --data-b <T data.bin> --dataset ID --seed-id s --threads 3` and, per fit, `--b-truth 1` for the self-check. **No guard bypass, no patched build**: the X/y section-hash guard accepted all 6 pairs. `merge_cross.py` (from the b89cba4d tree) → `W2_readback/cross_vt.json` (4 datasets, 6 cells).
| pair | h² (se) | d_H(V,T) | d_H(T,f*) | ratio (limit 0.10) |
|---|---|---|---|---|
| ADJ-OPP r01 s2 | 4.73e-7 (1.3e-7) | 6.87e-4 | 0.05797 | **0.0119** |
| ADJ-OPP r02 s1 | 1.18e-6 (6.0e-7) | 1.085e-3 | 0.08163 | **0.0133** |
| ADJ-OPP r02 s2 | 1.31e-6 (8.3e-7) | 1.143e-3 | 0.08168 | **0.0140** |
| AR r01 s2 (T tier 0) | 4.13e-7 (1.2e-7) | 6.42e-4 | 0.08571 | **0.0075** |
| ARweak r02 s1 | 4.04e-7 (1.3e-7) | 6.35e-4 | 0.18804 | **0.0034** |
| ARweak r02 s2 | 4.92e-7 (1.2e-7) | 7.01e-4 | 0.18797 | **0.0037** |
Max 0.0140 (ADJ r02 s2); the earlier waves gave 0.0034–0.0136. **Self-check B = truth** (`selfcheck_bitexact.txt`): xeval `h2` against the engine's `eval.bin.json dist.T.predictive.h2` is **bit-equal in 11 of 12 fits** (all 6 V fits, 5 of 6 T fits). **Not bit-equal: 4-AR-n200-r01-T-s2**, xeval 0.007346601991972235 against engine 0.007346601991972124, difference **1.1102e-16 = 2⁻⁵³ (the last bit of `1 − X` with X ≈ 0.9927), relative 1.5e-14**. I re-ran that self-check at 1, 3 and 8 threads (`tmp/…/selfchk_diag`): xeval gives exactly 0.007346601991972235 every time, so it is deterministic and not thread-order noise; the engine's own eval used 8 threads on NOTS (g++ 14.3 binary) while xeval was built on Owls (g++ 11.5), a libm / compiler rounding difference is the likely cause but I have not tested that. The other 11 fits, and all 12 in W1, agree to the last bit with the same xeval binary. No effect on any criterion value; I did not patch or work around it. The manager decides whether a 1-ulp miss counts against "bit-exact".

## 5. Read-back table, registered vs v2 side by side (`--wave-check --cross-file W2_readback/cross_vt.json --cost-dir …/_batch_OV_W2_{T,V}/cost`; outputs `W2_readback/registered/`, `W2_readback/v2/`)
Hashes verified: `compare_overlap.py` 311bbad886fc61c679ac47d1c30faf8d8897e33681baf5711f1f268472632eea (registered), `compare_overlap_v2.py` 4f402e5127efd4754cf25e4ade6ad799f697ebc28e1c657ff49f93fd2905b5c6, `PREREG_ADDENDUM_2.md` 4985833d479f1de5b9446cafe69b908940af446bc493d479d5394ded904d3230. Both run on the same records, `python3 -I`, rc 0.
**Delivery on W2: registered 12 of 12 (T 6/6, V 6/6), v2 12 of 12. The two outputs are identical in every shared column (0 differing cells); v2 only adds `tier_final_*` / `N_final_*` (all 0 / 10,000 for T, 0 / 2,500 for V).** With W0 and W1 pooled (§5b): registered 25 of 28 fits read, v2 28 of 28; the 3 undelivered fits are the 3 escalated T fits.
| pair | HPM T = V (MPM equal) | F_T − F_V | max abs ΔPIP; worst ratio | log Ẑ V (isl s.e.) / T | Δlog Ẑ (V−T); isl s.e. | log Z_T lb V / T | gap log Ẑ − lb V / T |
|---|---|---|---|---|---|---|---|
| ADJ r01 s2 | {1000,1001,5000,7000,9000} (yes) | −1.1e-13 | 1.5e-4; 0.015 | −220.0662 (0.0041) / −220.0654 (0.0098) | −0.00074; **0.07** | −220.223432 / −220.223430 | 0.157 / 0.158 |
| ADJ r02 s1 | same (yes) | −2.8e-14 | 2.5e-4; 0.025 | −241.8170 (0.0112) / −241.8080 (0.0108) | −0.00895; **0.58** | −242.023959 / −242.023956 | 0.207 / 0.216 |
| ADJ r02 s2 | same (yes) | −2.8e-14 | 9.6e-4; 0.096 | −241.8124 (0.0055) / −241.8148 (0.0145) | +0.00243; **0.16** | −242.023960 / −242.023957 | 0.212 / 0.209 |
| AR r01 s2 | {1000,3000,5000,7000,9000} (yes) | 0 | 2.4e-4; 0.024 | −177.2514 (0.0060) / −177.2474 (0.0079) | −0.00406; **0.41** | −177.378442 / −177.378441 | 0.127 / 0.131 |
| ARweak r02 s1 | {1000,3000,5000} (yes) | 0 | 2.0e-4; 0.020 | −274.6062 (0.0035) / −274.6080 (0.0041) | +0.00175; **0.33** | −274.702257 / −274.702256 | 0.096 / 0.094 |
| ARweak r02 s2 | same (yes) | 0 | 1.7e-4; 0.017 | −274.6089 (0.0049) / −274.6073 (0.0059) | −0.00165; **0.22** | −274.702258 / −274.702257 | 0.093 / 0.095 |
| pair | T tier / N | d_H(T,f*) / d_H(V,f*) | plug-in h² HPM = MPM (T = V) | predictive h² T / V (oracle) | core-h T / V |
|---|---|---|---|---|---|
| ADJ r01 s2 | 0 / 10,000 | 0.05797 / 0.05787 | 0.003126 | 0.003360 / 0.003349 (0.003251) | 36.73 / 2.27 |
| ADJ r02 s1 | 0 / 10,000 | 0.08163 / 0.08169 | 0.003960 | 0.006664 / 0.006673 (0.003837) | 47.41 / 2.82 |
| ADJ r02 s2 | 0 / 10,000 | 0.08168 / 0.08154 | 0.003960 | 0.006671 / 0.006649 | 43.13 / 2.91 |
| AR r01 s2 | 0 / 10,000 | 0.08571 / 0.08584 | 0.008187 | 0.007347 / 0.007369 (0.007281) | 49.01 / 2.22 |
| ARweak r02 s1 | 0 / 10,000 | 0.18804 / 0.18792 | 0.038840 | 0.035359 / 0.035314 (0.006383) | 23.16 / 2.08 |
| ARweak r02 s2 | 0 / 10,000 | 0.18797 / 0.18798 | 0.038840 | 0.035334 / 0.035337 | 7.66 / 1.76 |
X/y sha (truth.json) equal over the four fits of each dataset and different across the datasets.

### 5b. Seed-pooled E1 and S1 where both seeds now exist (the scripts' own multi-root mode: `--records records/W0 records/W1 records/W2`, NOT `--wave-check`; outputs `W2_readback/pooled/{registered,v2}_{wave,full}/`; cross file `cross_vt_pooled_W0W1W2.json`, 14 cells; cost dirs W0 T2 / V2 + W1 + W2)
The scripts accept several record roots, so no change was needed. In W0 the evidence runs and the rebuilds share run ids; the scripts keep the newest eval record, which is the T2 / V2 rebuild. Result per dataset (V − T on log Ẑ pooled over the two seeds, `logZ_diff_VminusT`; `se_comb` = the script's seed-pooled yardstick; ratio = |diff| / se_comb):
| dataset | seeds (T tier s1 / s2) | **E1 V − T pooled** | se_comb | ratio | s1 diff / s2 diff | S1 HPM equal (s1, s2) |
|---|---|---|---|---|---|---|
| **AR r01** (s1 W0, s2 W2) | 1 / 0 | **−0.00964** | 0.00588 | **1.64** | −0.01521 / −0.00406 | yes, yes |
| **ADJ-OPP r01** (s1 W0, s2 W2) | 0 / 0 | **−0.00072** | 0.00850 | **0.09** | −0.00070 / −0.00074 | yes, yes |
| ARweak r01 | 1 / 0 | −0.00684 | 0.00547 | 1.25 | −0.00792 / −0.00575 | yes, yes |
| ARweak r02 | 0 / 0 | +0.00005 | 0.00561 | 0.01 | +0.00175 / −0.00165 | yes, yes |
| ADJ-OPP r02 | 0 / 0 | −0.00326 | 0.01096 | 0.30 | −0.00895 / +0.00243 | yes, yes |
| IND r01 | 0 / 1 | −0.00638 | 0.00492 | 1.30 | −0.00137 / −0.01138 | yes, yes |
| NULL r01 | 0 / 0 | +0.00018 | 0.00480 | 0.04 | +0.00040 / −0.00003 | yes, yes |
Pooled yardstick (v2, 7 of 10 datasets have both seeds): s_V = 0.00612 (df 7), s_T = 0.002943 (df 7) (W1 had 0.0046 / 0.0008 on 3 datasets). The registered E1 still needs 10 datasets, so **E1 is NOT_EVALUATED as registered and these ratios are provisional**; 0 of 7 above 3. **Registered script, pooled: AR r01, ARweak r01 and IND r01 are not evaluable** (their escalated T fit is "not delivered"): 4 of 7 datasets evaluated, s_T on df 4 = 0.002636. The other 4 datasets are identical in both outputs.
Pooled script verdicts (partial data, so the outcome label is meaningless as a verdict): v2 "MARGINAL, criteria failed S1", D 28 / 40 delivered, **S1 "FAIL" = "7/10 datasets equal (7 evaluable, 0 real mismatching datasets)"**, i.e. not all 10 datasets evaluable, not a mismatch; registered: D 25 / 40 with 3 failed / invalid, S1 4 / 10. PAIR PASS, S2 PASS, S4 PASS (4 NULL fits), C PASS (0 over, 0 without a cost record).
**E1 sign / tier pattern (descriptive, island-only, nothing tested):** over the 14 V–T pairs read, V − T is negative in 11. **T escalated (N 40,000), 3 pairs: −0.0152 (AR s1), −0.0079 (ARweak r01 s1), −0.0114 (IND s2): all negative, mean −0.0115, 1.3–2.4 island s.e. T tier 0 (N 10⁴), 11 pairs: mean −0.0017**, 8 negative, from −0.0090 (ADJ r02 s1) to +0.0024. AR r01 s2 at tier 0 is −0.0041 (0.41 s.e.), so the AR sign persists at tier 0 but at a quarter of the escalated size. The particle-count reading from W1 (V 16 × 2,500 = 40,000, T tier 0 4 × 10⁴ = 40,000, T tier 1 160,000) still fits; W2 added 11 pairs of tier-0 T, and the tier-0 mean is small and noisy. A hypothesis for the analysis, not a result: report s_T by tier.

## 6. Per-pair criteria status (W2 = 3 datasets with a new seed, 2 new datasets; NOT a verdict)
| crit | status at W2 (v2 script; registered identical on W2) |
|---|---|
| D 40/40 | W2: 12 of 12 delivered. To date 28 of 40 fits read (W0 4 + W1 12 + W2 12): **v2 28 delivered, registered 25 (3 escalated T fits "not delivered")** |
| PAIR | PASS (X/y sha equal T = V and seed 1 = seed 2 within each of the 4 W2 datasets; pooled, ADJ r01 and AR r01 equal across W0 and W2) |
| S1 HPM | equal in 6 / 6 W2 pairs; both seeds equal in all 7 datasets that have two seeds (§5b) |
| S2 T never higher F | PASS (ΔF ≤ 0, min −1.1e-13) |
| S3 MPM | PASS 6/6 (14/14 pooled under v2) |
| S4 NULL | no NULL fit in W2; the W1 result stands (n_null_gt_0.5 = 0 in 4 of 4) |
| P PIP | PASS: worst ratio 0.096 (ADJ r02 s2), max abs ΔPIP 9.6e-4 vs floor 0.01 |
| E1 log Ẑ | island-only inside 3 s.e. in all 6 W2 pairs (worst 0.58); pooled over all 14 pairs worst 2.41 (AR s1, W0); as registered not evaluable (10 datasets needed) |
| E2 lower bound | PASS: lb ≤ log Ẑ in all 12 W2 fits (gaps 0.093–0.216) |
| H | PASS (ratio ≤ 0.0140 vs 0.10); the xeval self-check misses bit-exactness on 1 of 12 fits (§4) |
| C cost per fit | PASS: T max 49.01 ≤ 172.5, V max 2.91 ≤ 15; no T fit near the ADDENDUM_2 report line |

## 7. Re-projection for W3 and the rung (Opus model re-run, W2 added; `W2_readback/reproj/`)
**What I changed (data only; the model is the one in REPROJECTION_W1 §2, not redesigned):** the 6 W2 T fits added as observations (ARweak r02: K0 10 slow, K0 1 fast; ADJ r01 s2 K0 9, r02 s1 12, r02 s2 10: slow, converged; AR r01 s2 K0 12 slow, converged; 6 more converged fits without a non-cap trigger → 11); SPENT = 254.74 + 277.90 + 221.15 = **753.79**; only the 6 W3 AR T fits (r02, r03, r04 × s1, s2) and their 6 V remain, **all on new datasets**; the W3 T calibrate limit is **5:00** (HQ, ADDENDUM_2), so a TIMEOUT needs > 18,000 s and is essentially impossible (P 0.0005); constants refreshed from the W2 measurements (tier-0 rebuild s: AR 223 (was 230), ADJ 209, ARweak 132; islands at N 10⁴: AR 14.82 measured (was 12.3), ADJ 12.6, ARweak 6.5). Tier-1 observations are unchanged (3: k1 = 1, 1, 3), so the tier-1 tail (φ) is as uncertain as before. Script `reproj/reproj_w2.py` → `reproj_w2_output.txt` (3·10⁵ posterior draws from 1.5 M prior draws, seed fixed, ESS 4,693 — smaller than W1's 29 k because the data now pull harder on the prior; `envs/ci-py313`, `python -I`, 78 s). Sanity: the same code with the W1 observations only gives W3 573 at 5:00, against 578 in REPROJECTION_W1 §5.
| quantity (base: W3 at 5:00) | E | P10 | P50 | P90 |
|---|---|---|---|---|
| **W3** (6 AR T + 6 V) | **482** | 322 | 473 | 648 |
| **rung total** (753.79 spent + W3) | **1,235** | 1,076 | 1,226 | 1,402 |
| rung, counted-only basis (W0 163.24) | 1,144 | 985 | 1,135 | 1,310 |
W3 P5 / P95 / P99: 288 / 704 / 840. Rung P95 1,458, P99 1,594.
| threshold | probability |
|---|---|
| **P(cumulative > 1.6k)** | **0.009** (the stop would need W3 > 846) |
| **P(> 2.1k)** | **< 0.0001** (W3 > 1,346; 2·10⁻⁵ in 3·10⁵ draws) |
| **P(> 2.5k)** | ≈ 0 (0 of 3·10⁵; W3 > 1,746) |
| P(> 1.8k) / P(> 2.0k) | 0.001 / 0.0001 |
| **P(any W3 T fit > 172.5)** | **0.118** (each AR fit 0.0235; includes P(TIMEOUT) 0.0005). Report-and-continue under ADDENDUM_2; a breach is C = FAIL for that fit, outcome at best MARGINAL |
| P(escalation) per W3 AR fit | **0.44** (posterior; P10–P90 0.23–0.67). Escalations in the 6 W3 fits: E 2.66 (P10–P90 1–5; P(all 6) 0.03, P(none) 0.08); **≈ 5.7 of 20 over the rung** (3 seen + 2.7) |
**AR P(escalate) posterior now that AR has 1 escalation of 2:** the model's 0.44 (was 0.67, P10–P90 0.41–0.91). It is lower than the naive count because the hierarchy also uses the 12 non-AR observations: ADJ-OPP slow fits converged at 9, 10, 10, 12 (never the cap), ARweak 1 slow converged + 2 fast, and AR's own non-escalation sat at K0 = 12 of 14. For comparison, the plain Beta(3.4, 0.6) prior (mean 0.85, ESS 4, as in the W1 Sonnet model) updated with 1 / 2 gives 0.73; these two estimates bracket the plausible range, and the sensitivity table maps them to W3 ≈ 480 (0.44) and ≈ 600 (0.73; between the 0.62 and 0.76 rows).
**Sensitivity (the same three assumptions as REPROJECTION_W1 §5):**
| assumption | E W3 | E rung | P90 rung | P > 1.6k | P > 2.1k | P(any W3 T > 172.5) | P(TIMEOUT) |
|---|---|---|---|---|---|---|---|
| **base** (5:00, AR esc 0.44, φ̄ 0.03) | **482** | **1,235** | 1,402 | 0.009 | 0.0000 | 0.118 | 0.0005 |
| W3 at 3:00 (counterfactual; W1 model basis) | 498 | 1,252 | 1,442 | 0.037 | 0.0018 | 0.119 | 0.0895 |
| **(1) tier-1 tail** φ = 0 | 471 | 1,225 | 1,380 | 0.004 | 0 | 0.053 | 0.0001 |
| φ prior Beta(0.5, 3.5) | 495 | 1,248 | 1,432 | 0.018 | 0.0001 | 0.193 | 0.0010 |
| φ prior Beta(1, 3) | 517 | 1,271 | 1,483 | 0.038 | 0.0003 | 0.313 | 0.0020 |
| **(2) AR P(esc)** 0.32 (no shift, π_AR Beta(1, 3)) | 413 | 1,167 | 1,335 | 0.004 | 0 | 0.087 | 0.0003 |
| AR P(esc) 0.62 (shift +0.35) | 568 | 1,322 | 1,479 | 0.025 | 0.0001 | 0.159 | 0.0008 |
| AR P(esc) 0.76 ("certain", F16) | 629 | 1,382 | 1,531 | 0.048 | 0.0002 | 0.186 | 0.0011 |
| 5:00 + φ prior Beta(1, 3) | 511 | 1,265 | 1,479 | 0.036 | 0.0002 | 0.304 | 0.0019 |
Minor ones (slow-K centre prior 7 / 14, ε = 0, dataset latent, dataset cost factor sd 0.15) move E(W3) by −9 … +6. **The one thing that sets the level is the AR escalation probability (E W3 413–629); the one that sets P(any > 172.5) is the tier-1 tail (0.05–0.31).** Neither can be narrowed with the data so far (2 AR fits, 3 tier-1 fits).
**Recommended W3 QUOTE: 490** (E(W3) 482 rounded up to 10). REPROJECTION_W1 said to keep 640 unless E(W3) falls outside 580–700; it falls outside (482; even the "AR certain" row, 629, lies inside the old band). At 490 the wave stop (2 × quote) is **> 980**, P(W3 > 980) ≈ 0.002 (0.0017 for a quote of 500). P(W3 > quote) is 0.42 at 500, 0.21 at 580, 0.11 at 640; if the manager prefers to keep the quote close to the old 640 (to leave room for the AR uncertainty above), the stop stays at 1,280 and nothing changes in the stop logic. I would use 490, since the quote is the expected cost and the stop is 2 ×. The W3 T plan cap (5:00 limit, 6 × ≈ 441 = 2,644) is a ceiling, not an expectation, and does not need to change.
**Option A (cumulative 1.6k → 2.1k, HQ to confirm at this read-back):** with 753.8 spent the 1.6k stop would fire with P 0.009 (0.048 at the "AR certain" row), and 2.1k is unreachable in the model (P < 0.0001), so Option A is harmless but no longer protects anything; the numbers support either choice.
**Did the numbers move materially vs REPROJECTION_W1 (rung E 1,534, P90 1,853; W3 E 602)? Yes, downward, on every measure.** Rung E 1,235: **−299 (−19 %)**; P90 1,402: **−451 (−24 %)**; W3 E 482: **−120 (−20 %; −17 % against REPROJECTION_W1's 5:00 variant, 578)**. The old P90 (1,853) sat above 1.6k; the new P90 (1,402) is below it, i.e. a crossing of the 1.6k line at P90 (the 1.6k probability fell from 0.34 to 0.009). 2.1k: P(> 2.1k) 0.037 → < 0.0001, P(> 2.5k) 0.008 → ≈ 0; the 2.1k line was not crossed at P90 before or now. The change came from the observations, not the constants: refreshing the constants moved W3 from 578 to 573; adding W2 moved it to 482. **The W1 model scored W2 poorly: actual 221 against E 400 (P10 250, P90 557); P(W2 ≤ 221) = 0.054, P(0 of 6 escalate) = 0.044 (`reproj/w2_pit_check_output.txt`).** Expected escalations in the 6 fits were 2.8, observed 0; actual T costs 7.7–49.0 against expected 40–98. A model that over-predicted the escalation rate by this much is a reason to treat the 0.44 as an estimate with a wide band (0.23–0.67), not a point.
**Stop rules, last probe `probe_20261119T064237Z.txt`:** `stop_rules.py … --wave W2 --plans F_eefcbc4a/scripts --quote 480 --prior monitor/cumulative.json` (output `W2_readback/stop_rules_W2_last_probe.txt`) → "wave actual 221.2 (quote 480) | cumulative overlap 753.8 | projection 1038 [T mean 45.3 (14 completed attempts); V mean 2.0 (14 completed attempts)] … datasets with X/y hash seen: 4 (all paired: True) **VERDICT: no stop rule fired**", rc 0. All 12 fits COMPLETED; per-fit max T 49.01 (< 172.5), V max 2.91 (< 15). The monitor's projection (1,038) is the mean cost per completed attempt times the fits left and ignores the escalation weighting; it is not comparable with the table above.

## 8. Open points for the manager / HQ
- **Self-check, 1 of 12 not bit-exact (§4):** AR r01 T s2, 1 ulp of `1 − X`, deterministic in xeval, no effect on H or any other value. Decide whether that clears "bit-exact"; if not, a rebuild of xeval with the NOTS compiler / libm would be the test (I did not do it).
- **AR P(escalate) is 0.44 (this model) to 0.73 (plain Beta update)** (§7); W3 will be the first data of AR beyond r01. The W3 quote of 490 rests on 0.44; at 0.73 the expected W3 is ≈ 600.
- **Registered script vs v2 (H-21):** both outputs are in this read-back as ordered; for W2 they are identical. The difference (N check on escalated T fits) sits in W0 and W1, and only shows in pooled runs (25 vs 28 delivered).
- **Option A / Option "5:00 for W3":** both are in force per HQ 5b26e388; the numbers in §7 assume the 5:00 limit (P(TIMEOUT) 0.0005 at 5:00 against 0.09 at 3:00).
- Tool flaws, unchanged: `bin_version.json` loader error in `collect_nots.sh`; `monitor/cumulative.json` still lists only W0 + W1 (532.64; the stop-rule run uses it as the prior and adds the live wave: 532.6 + 221.2 = 753.8). Not edited here.
- NOTS clean-up of the W2 run dirs waits for the manager's OK (units are in `records/`; desktop verification is a separate step). Nothing was submitted, cancelled or deleted.

Files: `results/overlap1e4/W2_readback/` = `W2_escalation.csv`, `W2_cost_stages.csv`, `W2_sacct_jobs.csv`, `w2_readback_tables.py`, `W2_T_fit_validity.csv` + `w2_t_validity.py`, `cross_vt.json`, `cross_vt_pooled_W0W1W2.json`, `cross/` (6 cross + 12 self-check records, `run_cross.sh`), `selfcheck_bitexact.txt`, `registered/`, `v2/` (`wave_check.csv`, `per_fit.csv`, `stdout.txt`), `pooled/{registered,v2}_{wave,full}/` (`wave_check.csv` or `per_dataset.csv`, `per_fit.csv`, `verdict.json`, `verdict.md`, `stdout.txt`), `reproj/` (`reproj_w2.py` + `reproj_w2_output.txt`, `rebuild_times.py` + `rebuild_times_output.csv` now W0–W2, `w2_pit_check.py` + `w2_pit_check_output.txt`), `w2_projection_W1_sonnet_ref.py` (the Sonnet W1 script, copied for reference, not re-run), `stop_rules_W2_last_probe.txt`. Scratch: `SMC_Engineering_Department/tmp/20261119-w2readback/` (collect log, cross scratch, `selfchk_diag/`, `pool_test/`). No git state changed; nothing committed; no BNP files touched; nothing in /tmp.
