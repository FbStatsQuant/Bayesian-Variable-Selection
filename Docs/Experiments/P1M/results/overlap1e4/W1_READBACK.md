# W1 READ-BACK, 10⁴ T-vs-V overlap (Sonnet worker, 2026-11-19; per-wave checks only, NOT the rung verdict)

## Summary (10 lines)
1. **CLEAN (per-wave read-back; no stop rule, nothing invalid).** 12/12 W1 fits COMPLETED, collected, verified; all per-pair criteria pass under v2; no stop rule on the last probe. Two things to look at, neither is a failure: IND-T-s2 cost 143.96 (cap 172) and the registered script marks 2 escalated T fits "not delivered" (expected, ADDENDUM 1).
2. Collected: 14 units (12 fits + `_batch_OV_W1_{T,V}`) under `records/overlap1e4/W1/`, 1.8 GB, one SHA256SUMS each, 0 nested, `sha256sum -c` OK, 0 problems. `/` stays 85 % (records are on NFS, 39 %). Nothing submitted, cancelled or deleted on NOTS.
3. W1 billed **277.90 core-h** (T 269.09, V 8.81; sacct CPUTimeRAW/3600) = 62 % of the 450 quote. Cumulative W0 + W1 = **532.64** (254.74 + 277.90). Per T fit: IND s1 50.53 (tier 0, N 10⁴), **IND s2 143.96 (tier 1, N 40,000)**, NULL s1/s2 2.30 / 2.29 (tier 0), ARweak s1 60.72 (tier 1, N 40,000), **ARweak s2 9.28 (tier 0, N 10⁴)**; V 0.49–2.40 each.
4. **IND s2 = escalation, not an anomaly:** tier 0 ran all 14 rebuilds (≈ 259 s each, no convergence; 49.8 core-h), tier 1 needed 3 rebuilds (≈ 930 s each, 39.8), islands at N 40,000 cost 54.30. The 6,717 s calibrate = 3,732 s tier 0 + 2,985 s tier 1. Cap 172 is crossed at ≥ 6 tier-1 rebuilds (IND needed 3). Exposed in W2/W3: AR-strong (crossed at ≥ 7), not ADJ-OPP (≥ 8). Numbers in §3.
5. **ARweak s2 is a full, valid T fit** (not a short-circuit): calibration converged at the first rebuild at tier 0 (147 s), 4 islands N 10,000 = calib N_final, all COMPLETED, merge + eval COMPLETED, `fit.bin` 20.8 MB / `law.bin` 124 MB, eval completed, law M 400,001, R_eff 3.9995. The same dataset's s1 needed 14 rebuilds and escalated. NULL T fits (2.3 each): valid too.
6. Cross-Hellinger (criterion H): `smcbvs4_xeval` from b89cba4d, **guard accepted all 6 pairs unpatched**; self-check B = truth reproduces the engine `predictive.h2` bit-exactly for 12/12 fits. d_H(V,T)/d_H(T,f*) = **0.0055, 0.0056 (ARweak), 0.0122, 0.0136 (IND), 0.0035, 0.0034 (NULL)** vs limit 0.10.
7. **Registered `compare_overlap.py` (sha 311bbad8… verified): 10/12 fits delivered**; it marks IND-T-s2 and ARweak-T-s1 "not delivered (N = 40000, pre-registered 10000)", so those 2 pairs are empty. **`compare_overlap_v2.py` (4f402e51…): 12/12 delivered**; the 4 other pairs are identical in both.
8. Per-pair criteria (v2): D, PAIR, S1, S2, S3, **S4 (NULL: n_null_gt_0.5 = 0 in all 4 fits, HPM = MPM = ∅)**, P, E2, H, C all pass; E1 island-only inside 3 s.e. everywhere (worst IND s2 1.61, ARweak s1 1.31). E1 is still not evaluable as registered.
9. **E1 watch:** V − T is negative in 8 of 9 pairs seen so far and clearly larger where T escalated to N 40,000 (−0.0152 AR, −0.0079 ARweak s1, −0.0114 IND s2) than where it did not (−0.0058 … +0.0004). Descriptive only (§5).
10. Re-projection: expected rung **1,614 (P10–P90 1,460–1,763)** vs REPROJECTION_W0 1,816 (1,613–2,021): **moved materially (−11 %, P90 −13 %), downward; no 2.1k crossing (P > 2.1k 0.002)**, P(> 1.6k) 0.56 (was 0.91). Escalations: 3 of 8 T fits so far; ≈ 7.9 of the remaining 12 expected (≈ 10.9 of 20, as before). W3 is still the wave that decides the 1.6k line.

## 1. Collection
`ARMS="T V" nice -n 19 tools/collect_wave.sh W1` (NOTS: the tool's own ssh / rsync calls over its one ControlMaster connection; I made no other NOTS call). Units: `<run_id>` for the 12 fits (no suffix, one batch per arm) + `_batch_OV_W1_T`, `_batch_OV_W1_V`; log `tmp/20261119-w1readback/collect.log` ("collected: 14 units verified, 0 problems"). Re-checked by hand: `sha256sum -c` in every unit OK, exactly one `SHA256SUMS` per unit (fit units 44–109 files, batch units 178 / 321), no `INCOMPLETE.txt`. `fit.bin` 14–23 MB and `law.bin` 45–159 MB per T unit, 1.8 GB in all. **Disk (before): `/` 70 G, 60 G used, 85 %; records on `yorick:/u/grads/fb31` NFS 4.4 T, 39 %.** The copy goes to NFS only; `/` is unchanged after (85 %); the xeval build (≈ 340 MB source + objects) is on the same NFS under `tmp/`. Neither passes 92 %.
Known flaw (not fixed, ops tool): `_batch_OV_W1_{T,V}/bin_version.json` holds a libstdc++ loader error (`CXXABI_1.3.15 not found`), not a version: `collect_nots.sh` runs `smcbvs4 version` without `env.sh`. Binary provenance is in every record's `binary` block: git_commit eefcbc4a2ab42fdf52ec1e5d318a956bdd07f463 (F), T sha b6641feb… (portable), V sha 72c9109d… (sapphirerapids); `scripts/bin/smcbvs4.sha256` in each batch unit.
Observation (not a defect for the checks): in every fit, T and V, `eval.bin.json` `params.seed` is the **data seed** (e.g. 403020001 for ARweak s1 and s2), not the engine seed (s2 islands use data seed + 100). PREREG §2 reads "`eval` seed = the fit's engine seed". Both arms use the same value, so the pairing and the x draws are the same for s1 and s2 and for T and V; the cross tool uses the same seed (self-check below).

## 2. Per T fit: tier, N_final, cost (`W1_readback/W1_escalation.csv`, `W1_cost_stages.csv`, `W1_sacct_jobs.csv`: 168 job rows; same formats as W0)
| fit | tier_final / N_final | rebuilds t0 / t1 | calibrate core-h (wall) | islands at N_final core-h (wall max) | merge + eval | total |
|---|---|---|---|---|---|---|
| IND s1 | 0 / 10,000 | 11 / – | 37.39 (2,804 s) | 13.05 (549 s) | 0.067 | **50.53** |
| **IND s2** | **1 / 40,000** | 14 / 3 | **89.56 (6,717 s)** ≈ 49.8 t0 + 39.8 t1 | **54.30 (2,201 s)** | 0.067 | **143.96** |
| NULL s1 | 0 / 10,000 | 1 / – | 0.67 (50 s) | 1.55 (64 s) | 0.051 | 2.30 |
| NULL s2 | 0 / 10,000 | 1 / – | 0.68 (51 s) | 1.53 (69 s) | 0.051 | 2.29 |
| ARweak s1 | 1 / 40,000 | 14 / 1 | 35.65 (2,674 s) ≈ 27.4 t0 + 8.3 t1 | 24.99 (1,015 s) | 0.051 | **60.72** |
| **ARweak s2** | 0 / 10,000 | 1 / – | 2.05 (154 s) | 7.14 (283 s) | 0.058 | **9.28** |
| V (6 fits) | 0 / 2,500 | 1–3 | 0.09–0.88 (21–199 s) | 0.31–1.39 (19–91 s, 16 tasks) | 0.06–0.09 | 0.49 (NULL) … 2.40 (IND s1) |
Setup is 0.027–0.036 per fit; no refused attempts in W1. tier_final / N_final from `calib.bin.json tiers[tier_final].N_final`; the tier split of the calibration and the rebuild counts come from the cost-file mtimes (rsync keeps NOTS mtimes; ±2 min) and the `cost_diag_t*_k*` files; every island json carries N = N_final and `tier` = tier_final. Escalated: **3 of 8 T fits** (W0 AR s1; W1 IND s2, ARweak s1). Peak limits: all T islands ≪ 2:00 (max 2,201 s), calibrate max 6,717 s vs 3:00 = 10,800 s.
Mean T cost by tier (W0 + W1 counted batches): **tier 0 (5 fits) 22.5** — bimodal: 49.4 when the calibration needs 11–12 rebuilds (ADJ-OPP W0 48.28, IND s1 50.53) and 4.6 when it converges at the first (ARweak s2 9.28, NULL 2.30, 2.29) — **tier 1 (3 fits) 104.9** (AR 110.12, ARweak s1 60.72, IND s2 143.96). T total 427.49 + V 13.65 (4.84 + 8.81) + W0 evidence 91.51 = 532.64.

## 3. HQ outliers
**(a) IND s2 = 143.96 core-h (IND s1 = 50.53).**
- **It is escalation (tier 1, N 40,000), by the coded rule, not a fault.** Stage split: setup 0.031 + calibrate 89.56 + islands 54.30 + merge 0.038 + eval 0.029.
- **Why the calibrate ran 6,717 s** (per-round times from the cost files): the tier-0 pilot, then 14 tier-0 rebuilds of 259 s each (≈ 3.45 core-h per rebuild; the cap ℓ = 14 was reached, so the grid never became bitwise identical; the trigger is inferred, `calib.bin` is not collected) = ≈ 3,732 s, 49.8 core-h; then the tier-1 pilot 198 s and **3 tier-1 rebuilds of 923 / 933 / 930 s** (≈ 12.4 core-h each, 3.6× a tier-0 rebuild; tier 1 has 4× H, T_e) = 2,985 s, 39.8 core-h. IND s1 converged at tier-0 rebuild 11 (≈ 250 s each, 2,804 s, 37.39) and did not escalate; ARweak s1 and the W0 AR needed 1 tier-1 rebuild, IND s2 needed 3. That is the whole difference.
- **Islands at N 40,000:** 54.30 (4 × 24 CPU, wall max 2,201 s) = 4.16 × IND s1 at N 10⁴ (13.05, 549 s). For comparison: W0 AR-T2 49.21 (2,085 s), W0 ADJ-OPP at N 10⁴ 12.29 (486 s; × 4 = 49.2). Island cost scales with N (4.0–4.2×) and with the dataset (IND slightly above AR and ADJ-OPP).
- **Cost model of an escalated IND-type fit:** fixed part ≈ 106.8 (setup, tier 0 in full 49.8, tier-1 pilot 2.6, islands 54.3, merge and eval) + 12.4 per tier-1 rebuild: k1 = 1: 119.2; 2: 131.6; **3: 144.0 (observed)**; 4: 156.4; 5: 168.8; **6: 181.2 > 172**. The calibrate TIMEOUT (3:00 = 10,800 s) would arrive in the 8th tier-1 rebuild, so the 172 per-fit stop binds first. **Headroom of IND s2: 28 core-h ≈ 2 more tier-1 rebuilds.**
- **Is 172 at risk in W2/W3?** IND is finished (both seeds). Of the 12 remaining T fits: **ADJ-OPP × 3 (W2):** tier 0 converged at 12 of 14 in W0 (a 14-rebuild miss is plausible); escalated cost ≈ 94 + 10.8 per tier-1 rebuild (tier-0 in full ≈ 42, tier-1 rebuild ≈ 10.8 are estimates from 2.99 per tier-0 rebuild and the 3.6× ratio): 105 at k1 = 1, 126 at 3, above 172 only at k1 ≥ 8. **AR-strong × 7 (r01 s2 in W2, r02–r04 in W3):** W0 AR-T2 = 110.12 at k1 = 1 (tier 0 in full 47.0, tier-1 pilot + rebuild 13.6, islands 49.2); ≈ 11–12 per further rebuild: above 172 at k1 ≥ 7 (k1 = 6 ≈ 167). **AR is the exposed type** (the most expensive islands plus a full tier 0); ARweak × 2 is far below (escalated ≈ 54 + 6.6 per rebuild).
- Model risk (§7): P(any of the 12 remaining T fits > 172) ≈ 0.09, P(a calibrate TIMEOUT) ≈ 0.04, **resting on three tier-1 observations (k1 = 1, 1, 3)**; if tier-1 convergence per rebuild is as low as 0.43 (Beta(3,4)) the numbers are 0.34 and 0.21. W0's "5 % chance a tier-1 calibration does not converge at k1" is now 1 of 3 observed.

**(b) ARweak s2 = 9.28 core-h vs s1 = 60.72: a full, valid T fit. Not a short-circuit.**
- Stages in `_batch_OV_W1_T/cost` and sacct: setup, calibrate (task 6: 154 s, COMPLETED), **islands 4 tasks COMPLETED** (223 / 268 / 278 / 278 s), merge COMPLETED (0.031), eval COMPLETED (0.027). 7.14 core-h of islands.
- `calib.bin.json`: status completed, cal_status ok, tier_final 0, N_final 10,000, 1 rebuild (`cost_diag_t0_k1` only; 117 s; calibration `seconds` 147). The flag `checks_passed_final` is set in the eval record. **Every island json: N = 10,000 = calib N_final, tier 0, mode law, status completed**, island seed 403020101; `run_manifest.calib_N` = {N_plan 10,000, N_final 10,000, differs false, source calib.bin.json}; `fit.meta` N 10,000, Rp 4, tier 0.
- **Non-stub outputs:** `fit.bin` 20,817,920 B, `law.bin` 123,985,344 B, `eval.bin` 347,456 B; `fit.bin.json` status / fit_state completed, `eval.bin.json` status and fit_status completed (the W0 refusal stub was 3.8 KB with status invalid_input); the unit passes `sha256sum -c` and the scripts' section-hash verification.
- **Law particle count:** `law.bin.json` M = **400,001**, `list_size` 400,001 (`list_full` true), dropped mass 0, `max_abs_dF` 0, R_eff = 3.9995 of R′ = 4. M = 400,001 is the store / list size (top 1,000 + 399,000 tail) in **all six T fits of W1 and in the escalated W0 AR fit alike**, so it is the expected value and does not depend on N; the N check is the island N above.
- Values are consistent with s1: HPM {1000,3000,5000,7000} in both, log Ẑ −258.8891 (s2) vs −258.8875 (s1), log Z_T lower bound −258.99320 (both), predictive h² 0.018448 vs 0.018402.
- Why so cheap: the first tier-0 rebuild already gave an identical grid (as NULL), where the same dataset with the s1 engine seed needed 14 rebuilds and escalated. Tier-0 cost is bimodal (§2): 2–9 core-h when the grid is stable at once, ≈ 48–50 when it takes 11–12 rebuilds, ≈ 60–144 after escalation. **Within a dataset the two seeds went opposite ways for IND (s1 no, s2 yes) and for ARweak (s1 yes, s2 no); NULL was 0 / 0.**
- **NULL T fits (2.30, 2.29): valid too:** calibration converged at the first rebuild (≈ 50 s), tier 0, N 10,000, 4 islands completed at N 10,000, merge and eval completed, `fit.bin` 14.3 MB / `law.bin` 45 MB (smaller store), non-stub eval, HPM = MPM = ∅, `n_null_gt_0.5` = 0.

## 4. Cross-Hellinger (criterion H)
`smcbvs4_xeval` built from **origin/exp/P1M-engine b89cba4d** (merge of #87, X/y section-hash guard; `git archive` → `tmp/20261119-w1readback/xeval_build`, nice 19, -j3; binary sha256 afef0e46…; its `git_commit` field reads "unknown" because it is built from an archive, as in W0). `cross --a <V law.bin> --b <T law.bin> --truth <V truth.json> --data <V data.bin> --data-b <T data.bin> --dataset ID --seed-id s --threads 3`. **No guard bypass and no patched build:** the guard that refused T-vs-V in W0 (whole-file `data.bin` hashes embed each arm's binary block; here too they differ, e.g. IND s1 V d5f13a1c… vs T 578a14fb…) now compares the X/y sections and accepted all 6 pairs. The self-check (B = truth, 12 fits) **reproduces the engine's `dist.T.predictive.h2` bit-exactly in 12 of 12** (`W1_readback/cross/selfchk_*.json`; values in `W1_readback/selfcheck_bitexact.txt`). `merge_cross.py` → `W1_readback/cross_vt.json` (3 datasets, 6 cells).
| pair | h² (se) | d_H(V,T) | d_H(T,f*) | ratio (limit 0.10) |
|---|---|---|---|---|
| ARweak s1 (T tier 1) | 5.60e-7 (1.3e-7) | 7.48e-4 | 0.13565 | **0.0055** |
| ARweak s2 | 5.71e-7 (1.5e-7) | 7.55e-4 | 0.13582 | **0.0056** |
| IND s1 | 6.80e-7 (6.8e-7) | 8.25e-4 | 0.06759 | **0.0122** |
| IND s2 (T tier 1) | 8.51e-7 (5.7e-7) | 9.23e-4 | 0.06759 | **0.0136** |
| NULL s1 | 7.98e-9 (2.6e-9) | 8.93e-5 | 0.02579 | **0.0035** |
| NULL s2 | 7.71e-9 (1.7e-9) | 8.78e-5 | 0.02579 | **0.0034** |
Max 0.0136 (IND s2); W0 gave 0.007 / 0.013. Escalated pairs are not worse for H (ARweak s1 0.0055 vs s2 0.0056).

## 5. Read-back table, registered vs v2 side by side (`--wave-check --cross-file W1_readback/cross_vt.json`; `W1_readback/registered/`, `W1_readback/v2/`)
Hashes verified: `compare_overlap.py` 311bbad886fc61c679ac47d1c30faf8d8897e33681baf5711f1f268472632eea (registered); `compare_overlap_v2.py` 4f402e5127efd4754cf25e4ade6ad799f697ebc28e1c657ff49f93fd2905b5c6 (ADDENDUM 1). Both run on the same records, `python3 -I`, rc 0.
**Delivery: registered 10 of 12 W1 fits (T 4/6, V 6/6); v2 12 of 12.** The registered script rejects IND-T-s2 and ARweak-T-s1 with `arm settings: N = 40000, pre-registered 10000`; for those two pairs every comparison column is empty (NA). **The other four pairs are identical in the two outputs** (no column differs; v2 only adds the tier / N columns). Including W0 (registered 3 of 4: AR-T not delivered; v2 4 of 4), registered 13 of 16, v2 16 of 16 of the fits read so far.
| pair | registered | v2 |
|---|---|---|
| ARweak s1 | T not delivered, all NA | HPM equal, F equal, Δlog Ẑ −0.0079 (1.31 isl s.e.), worst PIP ratio 0.021, d_H(T,f*) 0.1357 |
| ARweak s2, IND s1, NULL s1, NULL s2 | as v2 | as below |
| IND s2 | T not delivered, all NA | HPM equal, F equal, Δlog Ẑ −0.0114 (1.61 isl s.e.), worst PIP ratio 0.069, d_H(T,f*) 0.0676 |
Values per pair (v2; the same as the registered script where it delivers):
| pair | HPM T = V (MPM equal) | F_T − F_V | max abs ΔPIP; worst ratio | log Ẑ V (isl s.e.) / T | Δlog Ẑ (V−T); in comb. isl s.e. | log Z_T lb V / T | gap log Ẑ − lb V / T |
|---|---|---|---|---|---|---|---|
| ARweak s1 | {1000,3000,5000,7000} (yes) | 0 | 2.1e-4; 0.021 | −258.8954 (0.0057) / −258.8875 (0.0020) | −0.0079; **1.31** | −258.993200 / −258.993199 | 0.098 / 0.106 |
| ARweak s2 | {1000,3000,5000,7000} (yes) | 0 | 2.2e-4; 0.022 | −258.8948 (0.0049) / −258.8891 (0.0064) | −0.0058; **0.72** | −258.993200 / −258.993200 | 0.098 / 0.104 |
| IND s1 | {1000,3000,5000,7000,9000} (yes) | −5.7e-14 | 1.26e-3; 0.126 | −210.4449 (0.0057) / −210.4435 (0.0035) | −0.0014; **0.21** | −210.607155 / −210.607154 | 0.162 / 0.164 |
| IND s2 | same (yes) | −5.7e-14 | 6.9e-4; 0.069 | −210.4561 (0.0064) / −210.4447 (0.0031) | −0.0114; **1.61** | −210.607155 / −210.607154 | 0.151 / 0.162 |
| NULL s1 | {∅} (yes) | 0 | 1.8e-5; 0.002 | −289.8956 (0.0003) / −289.8960 (0.0003) | +0.0004; **1.10** | −289.902586 / −289.902586 | 0.007 / 0.007 |
| NULL s2 | {∅} (yes) | 0 | 1.3e-5; 0.001 | −289.8959 (0.0002) / −289.8958 (0.0002) | −0.00003; **0.10** | −289.902586 / −289.902586 | 0.007 / 0.007 |
| pair | T tier / N | d_H(T,f*) / d_H(V,f*) | plug-in h² HPM = MPM (T = V) | predictive h² T / V (oracle) | core-h T / V |
|---|---|---|---|---|---|
| ARweak s1 | 1 / 40,000 | 0.13565 / 0.13577 | 0.018145 | 0.018402 / 0.018434 (0.004082) | 60.72 / 1.62 |
| ARweak s2 | 0 / 10,000 | 0.13582 / 0.13580 | 0.018145 | 0.018448 / 0.018441 | 9.28 / 1.76 |
| IND s1 | 0 / 10,000 | 0.06759 / 0.06757 | 0.003320 | 0.004568 / 0.004566 (0.003913) | 50.53 / 2.40 |
| IND s2 | 1 / 40,000 | 0.06759 / 0.06760 | 0.003320 | 0.004569 / 0.004569 | 143.96 / 2.04 |
| NULL s1 | 0 / 10,000 | 0.02579 / 0.02579 | 0.000670 | 0.000665 / 0.000665 (0.000671) | 2.30 / 0.50 |
| NULL s2 | 0 / 10,000 | 0.02579 / 0.02579 | 0.000670 | 0.000665 / 0.000665 | 2.29 / 0.49 |
X/y sha (truth.json) equal over the four fits of each dataset and different across the three datasets. Together with W0: Δlog Ẑ (V−T) in island s.e. 2.41 (AR, T tier 1), 1.31 (ARweak s1, tier 1), 1.61 (IND s2, tier 1), 0.72, 0.21, 1.10, 0.10, 0.06: all inside 3.
**E1 sign observation (descriptive, island-only, nothing tested):** V − T is negative in 8 of the 9 pairs so far, and its size depends on T's tier. **T escalated (N 40,000): −0.0152 (AR), −0.0079 (ARweak s1), −0.0114 (IND s2)**; T at tier 0 (N 10⁴): −0.0007 (ADJ-OPP), −0.0058 (ARweak s2), −0.0014 (IND s1), +0.0004, −0.00003 (NULL). The total particle count is V 16 × 2,500 = 40,000, T tier 0 4 × 10⁴ = 40,000, T tier 1 4 × 40,000 = 160,000, so a (log Ẑ) Jensen-type bias that falls with N would give exactly this pattern; this is a hypothesis for the analysis, not a result. Indicative E1 on the three W1 datasets with the seed-pooled yardstick over 3 datasets (s_V 0.0046, s_T 0.0008; the registered one needs 10): |Δ_d| / se_comb = 1.36 (ARweak), 1.31 (IND), 0.06 (NULL). With W0's reprojection (§6 there): a sign that persists on the AR sets would be the real N / tier effect; the analysis should report s_T by tier.

## 6. Per-pair criteria status (one or two seeds, three datasets; NOT a verdict)
| crit | status at W1 (v2 script; registered in brackets where it differs) |
|---|---|
| D 40/40 | 16 of 40 fits read (W0 4 + W1 12) all delivered under v2; **registered: 13 of 16 (3 escalated T fits "not delivered")**, which alone would make D INCOMPLETE |
| PAIR | PASS (X/y sha equal within each of the 3 datasets, different across them; the monitor's check agrees) |
| S1 HPM | equal in 6/6 W1 seed pairs (IND, ARweak, NULL = ∅): 3 datasets with both seeds, all equal; W0 AR and ADJ-OPP s1 equal too |
| S2 T never higher F | PASS (ΔF ≤ 6e-14) |
| S3 MPM | PASS 6/6 |
| **S4 NULL** | **PASS: `n_null_gt_0.5` = 0 in all 4 NULL fits (T s1, s2, V s1, s2), HPM = MPM = ∅** (now evaluable) |
| P PIP | island-only: PASS (worst ratio 0.126 at IND s1, max abs ΔPIP 1.3e-3 vs floor 0.01) |
| E1 log Ẑ | **island-only: inside 3 s.e. in all 6 pairs (worst 1.61)**; as registered not evaluable (needs 10 datasets); the largest ratios (1.61 IND s2, 1.31 ARweak s1) are the two pairs whose T fit escalated (v2 only; empty in the registered output) |
| E2 lower bound | PASS in all 6 pairs (lb ≤ log Ẑ for every fit; gaps 0.007–0.164) |
| H | PASS (ratio ≤ 0.0136 vs 0.10) |
| C cost per fit | PASS: T max 143.96 ≤ 172.5, V max 2.40 ≤ 15 (IND s2 is 83 % of the T limit) |

## 7. Rung arithmetic for the re-projection (arithmetic + one Monte Carlo; the Opus child owns the projection)
**Spent: W0 254.74 (counted 163.24 + evidence 91.50) + W1 277.90 = 532.64** (monitor: cumulative 532.6). **Escalations: 3 of 8 T fits** (W0 AR s1; W1 IND s2, ARweak s1); by design: AR 1/1, ARweak 1/2, IND 1/2, NULL 0/2, ADJ-OPP 0/1. REPROJECTION_W0 expected 3.35 of these 8 (0.85 + 0.30 + 2 × 0.35 + 2 × 0.25 + 2 × 0.5), observed 3. Mean T cost: tier 0 22.5 (bimodal 4.6 / 49.4), tier 1 104.9 (§2).
**Remaining (W2 plan staged in `F_eefcbc4a/scripts/OV_W2_{T,V}`; W3 per `make_waves.py`): 12 T + 12 V fits.** W2 T: ARweak r02 s1, s2, ADJ-OPP r01 s2, ADJ-OPP r02 s1, s2, AR r01 s2 (+ the same 6 V); W3 T: AR r02, r03, r04 × s1, s2 (+ 6 V). Counts by design: AR 7, ARweak 2, ADJ-OPP 3 (IND and NULL are finished).
**Model (same structure as REPROJECTION_W0 §3, `W1_readback/w1_projection.py`, output `w1_projection_output.txt`; 2·10⁵ draws, seed fixed):** P(escalate) per design Beta (prior means 0.85 AR, 0.5 ARweak, 0.3 ADJ-OPP with equivalent sample size 4, updated by the observations above → posterior means 0.88, 0.50, 0.24); the seeds are drawn independently (W1 showed no within-dataset pairing: IND and ARweak went opposite ways); tier-1 rebuilds k1 ~ Geometric(r), r ~ Beta(6,4) (mean 0.6: three tier-1 fits converged at k1 = 1, 1, 3), capped at 14; escalated cost = 98.5 (AR) / 54.1 (ARweak) / 93.9 (ADJ-OPP) + k1 × 11.6 / 6.6 / 10.8, ± 3; non-escalated: AR 50 ± 8, ADJ-OPP 48.3 ± 4, ARweak 9.3 (half) or 28 ± 4; V = 2.46 / 1.70 / 2.38 per fit.
| basis | E | P10 | P50 | P90 | P > 1.6k | P > 2.0k | P > 2.1k | P > 2.5k |
|---|---|---|---|---|---|---|---|---|
| **W0 + evidence (532.64 spent), base** | **1,614** | 1,460 | 1,614 | 1,763 | **0.56** | 0.005 | 0.002 | 0 |
| counted only (W0 163.24; 441.14 spent) | 1,522 | 1,369 | 1,523 | 1,671 | 0.24 | | | |
| P(esc) × 0.7 / × 1.15 | 1,491 / 1,675 | | | 1,669 / 1,804 | 0.22 / 0.78 | 0.001 / 0.009 | | 0 |
| tier-1 convergence worse, r ~ Beta(3,4) (mean 0.43) | 1,701 | 1,495 | 1,675 | 1,940 | 0.71 | 0.07 | 0.04 | 0.004 |
| r ~ Beta(2,5) (mean 0.29), a stress case | 1,839 | 1,544 | 1,783 | 2,231 | 0.83 | 0.24 | 0.16 | 0.03 |
By wave (expected / P10–P90; base): **W2 400 / 309–502** (quote 480, stop > 960; P(> 960) < 10⁻⁴), **W3 681 / 563–774** (quote 640, stop > 1,280; P(> 1,280) = 10⁻⁴; P(W3 > 733) 0.23). Cumulative after W2 **933 (P90 1,034)**, after W3 1,614. Escalations in the remaining 12 T fits: E 7.9 (P10–P90 6–10), so **≈ 10.9 of 20 over the rung** (REPROJECTION_W0: ≈ 10 of the 18 remaining, ≈ 11 of 20). P(any remaining T fit > 172) 0.09, P(calibrate TIMEOUT) 0.04 (base; 0.34 / 0.21 at r ~ Beta(3,4)).
**Did the numbers move materially vs REPROJECTION_W0 (1,816; 1,613–2,021; ~10/18 escalate)? Yes on the level, no on the risk at the top.** Expected −202 (−11 %), P90 −258 (−13 %): above the 10 % threshold, **downward**; P90 stays far below 2.1k (no crossing; P(> 2.1k) 0.002 vs 0.04). The 1.6k line is now a coin flip (P 0.56 vs 0.91); at the cumulative 1.6k stop W3 still decides (W2 ends at 0.93k). The escalation rate did not move (3 of 8 observed against 3.35 expected). **Drivers:** W1 came in at 277.9 against the 447 (P90 569) planned: NULL 4.6 vs ≈ 127 assumed, ARweak 70.0 vs ≈ 158, IND 194.5 vs ≈ 140 (+55); W2 400 vs 479 (the two ARweak fits ≈ 40 each vs 79 assumed); W3 681 vs 635 (+46: AR escalation 0.88 and tier-1 rebuilds averaging 1.8; W0 assumed one plus a 5 % tail). The re-projection should check this level with an independent model: the evidence is 3 tier-1 and 5 tier-0 T fits, with tier-0 costs bimodal and the tier-1 rebuild count at {1, 1, 3}.
The monitor's own projection (1,194) is the mean cost per completed attempt times the fits left and ignores the escalation weighting; it should not be compared with the table.
**Stop rules, last probe `probe_20261119T045108Z.txt`:** `stop_rules.py … --wave W1 --plans F_eefcbc4a/scripts --quote 450 --prior monitor/cumulative.json` (output `W1_readback/stop_rules_W1_last_probe.txt`) → "wave actual 277.9 (quote 450) | cumulative overlap 532.6 | projection 1194 … datasets with X/y hash seen: 3 (all paired: True) **VERDICT: no stop rule fired**", exit 0. All 12 fits COMPLETED; per-fit max 143.96 (< 172), V max 2.40 (< 15).

## 8. Open points for the manager / HQ
- **Registered script vs v2 (H-21):** both outputs are in this read-back as ordered; the only difference is the N check (2 escalated T fits in W1, 3 over W0 + W1). v2 reports tier and N per fit.
- **IND s2 at 83 % of the per-fit T limit** and a tier-1 tail of three observations: if W3 AR escalates with k1 ≥ 7, a per-fit stop (172) is possible; the model says ≈ 9 %, ≈ 34 % under a pessimistic tier-1 convergence. The calibrate TIMEOUT (3:00) is a separate, later line (k1 ≥ 8).
- **E1 sign / tier pattern** (§5): analysis to report s_T by tier; V at 16 × 2,500 vs T tier 1 at 4 × 40,000 particles.
- **Eval seed = data seed** (§1): PREREG §2 wording; no effect on the checks.
- Tool flaws: `bin_version.json` loader error in `collect_nots.sh` (as W0); `monitor/cumulative.json` still lists only W0 (not edited here).
- NOTS clean-up of the W1 run dirs waits for the manager's OK (units are in `records/`; desktop verification is a separate step). Nothing was submitted, cancelled or deleted.

Files: `results/overlap1e4/W1_readback/` = `W1_escalation.csv`, `W1_cost_stages.csv`, `W1_sacct_jobs.csv`, `w1_readback_tables.py`, `cross_vt.json`, `cross/` (6 cross + 12 self-check records), `registered/`, `v2/` (`wave_check.csv`, `per_fit.csv`, `stdout.txt`), `w1_projection.py` + `w1_projection_output.txt`, `stop_rules_W1_last_probe.txt`. Scratch: `SMC_Engineering_Department/tmp/20261119-w1readback/` (xeval source and build, `run_cross.sh`, logs). No git state changed; nothing committed.
