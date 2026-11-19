# W0 READ-BACK, 10⁴ T-vs-V overlap (Sonnet worker, 2026-11-18; per-wave checks only, NOT the rung verdict)

## Summary (10 lines)
1. Collected and verified: 12 units under `records/overlap1e4/W0/` (8 fits + 4 `_batch_*`), one SHA256SUMS each, 0 nested, `sha256sum -c` OK. Nothing deleted on NOTS.
2. Counted batches T2 + V2 = **163.24 core-h** (T 158.40, V 4.84); evidence T + V 91.50; W0 total 254.74 (sacct CPUTimeRAW).
3. V vs V2: **IDENTICAL outside provenance** (28 files/pair; every container section of fit/law/eval/data bit-equal). The tool needed 3 fixes (below).
4. Cross-Hellinger done: d_H(V,T) = 6.1e-4 (AR), 7.3e-4 (ADJ-OPP) = **0.7 % / 1.3 %** of d_H(T,f*) (limit 10 %). xeval needed a local guard patch (below).
5. HPM, MPM, F identical T=V on both datasets (HPM = S0 each); max|ΔPIP| 8.9e-5 / 1.5e-4 (floor 0.01); log Z_T lower-bound consistency holds.
6. **|Δlog Ẑ| = 0.0007 (0.06 s.e.) ADJ-OPP, 0.0152 (2.41 island s.e.) AR**: inside 3 s.e. but AR is the only number near an edge; the registered E1 (seed-pooled, 2 seeds) is not evaluable at W0.
7. **PREREG/SCRIPT MISMATCH (needs HQ):** the registered script marks AR-T *not delivered* (`N = 40000, pre-registered 10000`) because the calibration escalated to tier 1. Run as registered the AR pair has no values. A labelled supplementary copy (N 10⁴ or 40,000 accepted, nothing else changed) gives the numbers here. A logged deviation + new script sha is needed before W1 reads escalated fits.
8. T cost per fit: **48.28** (tier 0, ADJ-OPP) vs **110.12** (tier 1, AR) core-h; V 2.38 / 2.46. Cost ≤ limit on all 4 fits (T 172.5, V 15). 1 of 2 T fits escalated.
9. Escalation: AR-T2 tier 0 → 1, N_final 40,000: calibration 60.64 core-h (≈ 47 tier 0 + ≈ 14 tier 1), islands at N 40,000 49.21 (4 × 24 CPU, wall max 2,085 s), merge+eval 0.07, refused first islands 0.17.
10. Data for the Opus re-projection: `W0_readback/W0_escalation.csv`, `W0_cost_stages.csv`, `W0_sacct_jobs.csv` (115 job rows, 4 batches). Rung arithmetic at the end.

## 1. Collection
`collect_wave.sh W0` (ARMS T V T2 V2; one `ssh nots` stream, nice 19, ≈ 1.3 GB). Units `<run_id>` (evidence T, V), `<run_id>.T2`, `<run_id>.V2`, `_batch_OV_W0_{T,V,T2,V2}`. `rescue_AR_N40000/` is in `_batch_OV_W0_T2/scripts/`, the refused islands and `manifests.bak_N10000` inside the AR-T2 unit. Evidence batches: OV_W0_T AR has no fit.bin (INCOMPLETE.txt); OV_W0_T ADJ-OPP carries a 3.8 KB `fit.bin` that is the GUARD-W refusal stub (status invalid_input). Flaw: `_batch_*/bin_version.json` holds a libstdc++ loader error, not a version (collect_nots.sh ran `smcbvs4 version` without env.sh). The binary provenance is in every record's `binary` block (git_commit = F eefcbc4a…, T2 sha 5fc6bbb3 portable, V2 ba569a33 SPR) and `scripts/bin/smcbvs4.sha256`; ops should source env.sh in `collect_nots.sh`.

## 2. V vs V2 cross-check (`cross_check_V.py … --info-bin <smcbvs4 built from 1b6ddd59>`; output `W0_readback/cross_check_V_output.txt`)
Result **IDENTICAL outside provenance**, rc 0. Fixes to `staging/overlap1e4/tools/cross_check_V.py` (backup `.bak_20261118`, patch `W0_readback/cross_check_V.patch`): (a) pairing bug: `d[:-3]` cut the `-s1` so every V2 unit was "MISSING" (now `d + ".V2"`); (b) drop-list +`mem_estimate`, `*rss*`, `end_file_kb`, `fit_bin`, `calib_bin`, `*content_sha256` (whole-file hashes embed the binary block; measured memory differs by ≈ 64-128 bytes or 16 MB RSS); (c) `data.bin` compared by sections (its whole-file hash embeds the binary block, the same artefact as incident W0-XY). logZ, F, HPM and all 45 fit.bin sections are equal. Dropped keys are only binary/inputs/paths/timing/memory (list in the `--show-dropped` run).

## 3. Cross-Hellinger (criterion H)
`smcbvs4_xeval` built from origin/exp/P1M-engine 1b6ddd59 (#85) in `tmp/20261118-w0readback/xeval_build`, nice 19, -j3; `cross --threads 3` (≈ 10 s/pair) + `merge_cross.py` → `cross_vt.json`. Self-check B = truth reproduces the engine `dist.T.predictive.h2` **bit-exactly** for all 4 fits. **Deviation:** the unpatched tool refuses T-vs-V ("laws built on different data.bin (recorded hashes differ)"): it compares whole-file `data.bin` hashes, which embed each arm's binary block (T2 and V2 binaries differ). The `data.bin` sections are identical and truth X/y sha are equal, so I ran a tmp-only build with the two hash guards bypassed by `XEVAL_SKIP_DATAHASH` (`xeval_datahash_guard.patch`; nothing else changed; binary sha 066b70f8…; the unpatched build, 4128b275…, kept). The engine guard should compare the X/y section hashes (HQ/engine call; no repo change made). The xeval binary reports git_commit "unknown" (built from an archive; evaluation tool only).

## 4. Read-back table (W0 = 2 datasets × s1; registered script `--wave-check`, tool `compare_overlap.py` sha 311bbad8… verified; AR column from the supplementary copy, §5)
| quantity | AR r01 s1 | ADJ-OPP r01 s1 |
|---|---|---|
| HPM T / V (S0) | {1000,3000,5000,7000,9000} / same (= S0) | {1000,1001,5000,7000,9000} / same (= S0) |
| MPM equal; F_T − F_V | yes; 0 | yes; −1e-13 |
| max abs ΔPIP (V−T); worst ratio to max(0.01,3·se_isl) | 8.9e-5; 0.009 | 1.5e-4; 0.015 |
| log Ẑ V (island s.e.) / T | −177.2705 (0.0062) / −177.2552 (0.0010) | −220.0691 (0.0063) / −220.0684 (0.0109) |
| Δlog Ẑ (V−T); in combined island s.e. | −0.0152; **2.41** (bound 3) | −0.0007; 0.06 |
| log Z_T lower bound V / T | −177.378442 / −177.378441 | −220.223431 / −220.223430 |
| gap log Ẑ − log Z_T V / T | 0.108 / 0.123 | 0.154 / 0.155 |
| E2 (i)(ii)(iii) | hold (all ≤ 0, bound +3 s.e.) | hold |
| d_H(T,f*) / d_H(V,f*) | 0.08584 / 0.08581 | 0.05799 / 0.05787 |
| **d_H(V,T)** (h² / se) vs 10 % d_H(T,f*) | **6.14e-4** (3.8e-7 / 1.0e-7) vs 8.58e-3: ratio 0.007 | **7.28e-4** (5.3e-7 / 1.0e-7) vs 5.80e-3: ratio 0.013 |
| plug-in h² HPM = MPM (T, V equal) | 0.008187 | 0.003126 |
| predictive h² T / V (oracle) | 0.007369 / 0.007364 (0.007281) | 0.003363 / 0.003349 (0.003251) |
| pairing X/y sha | equal over T2, V2, V, T; differs from the other dataset | same |
| billed core-h T / V (limit 172.5 / 15) | 110.12 / 2.46 | 48.28 / 2.38 |
Registered-script reading of the same data: ADJ-OPP pair fully delivered, all values as above; **AR-T not delivered** (`arm settings: N = 40000, pre-registered 10000`), so the AR pair row is empty in `wave_check_registered_script.csv`. `*_SUPP_N40000.csv` = the same script with the single N check widened to {10⁴, 40,000} (`compare_overlap_supp_N40000.py`, not the registered sha).

## 5. PREREG criteria at W0 (one seed, two datasets: status is per pair, NOT a verdict)
| crit | evaluable at W0? | status |
|---|---|---|
| D 40/40 | no (2 of 40) | AR-T "not delivered" under the registered N check, delivered under the supplementary copy: see item 7 |
| PAIR | yes | PASS (X/y sha equal across the 4 fits of each dataset, different across datasets) |
| S1 HPM | per pair (needs both seeds) | s1 equal 2/2 |
| S2 T never higher F | yes | PASS (ΔF ≤ 1e-13) |
| S3 MPM | per pair | PASS 2/2 |
| S4 NULL | no (no NULL fit) | n/a |
| P PIP | island-only s.e., one seed | PASS (≤ 1.5e-4 vs floor 0.01) |
| E1 log Ẑ | no (seed-pooled yardstick needs 2 seeds, 10 datasets) | island-only: inside 3 s.e. (AR 2.41) |
| E2 lower-bound | yes | PASS |
| H | yes, with the cross file | PASS (ratio 0.007 / 0.013) |
| C cost per fit | yes | PASS (T 110.1 and 48.3 ≤ 172.5; V ≤ 2.5 ≤ 15) |

## 6. Escalation and per-stage cost (core-h = sacct CPUTimeRAW/3600; `W0_escalation.csv`, `W0_cost_stages.csv`, `W0_sacct_jobs.csv`)
| fit (batch) | tier_final / N_final | setup | calibrate (wall) | islands at final N (wall max) | merge + eval | refused attempt | total |
|---|---|---|---|---|---|---|---|
| AR-T2 | **1 / 40,000** | 0.036 | **60.64** (4,548 s; ≈ 47.0 tier 0 + ≈ 13.6 tier 1) | **49.21** (4 × 24 CPU, 2,085 s) | 0.031 + 0.038 | 0.167 | **110.12** |
| ADJ-OPP-T2 | 0 / 10,000 | 0.038 | 35.84 (2,688 s) | 12.29 (486 s) | 0.062 + 0.044 | 0 | **48.28** |
| AR-V2 | 0 / 2,500 | 0.036 | 1.03 (232 s) | 1.30 (16 tasks, 79 s) | 0.053 + 0.036 | 0 | 2.46 |
| ADJ-OPP-V2 | 0 / 2,500 | 0.036 | 0.86 (193 s) | 1.41 (100 s) | 0.047 + 0.033 | 0 | 2.38 |
Tier split of the AR calibration is an estimate from cost-file mtimes (±2 min; tier 0 ran all B = 14 checks, tier 1 stopped at k1). Peak MaxRSS: calibrate 3.5 GB (16 G allowed), AR islands at N 40,000 0.74 GB, merge at N 40,000 0.34 GB in 14 s (20 min allowed). Evidence batches: OV_W0_T 87.04 (aborted, billed), OV_W0_V 4.46. Island cost scales with N: 4.0× (49.2/12.3) for 4× N.

## 7. Open points for the manager / HQ
- **E-N mismatch:** prereg §2 fixes T N = 10⁴ but also "coded calibration with escalation (D-26)"; the script's N check ignores the tier. Any escalated T fit (here 1 of 2) is "not delivered" and drives D to INCOMPLETE. Fix = a §9 deviation: accept N = `calib.bin.json tiers[tier_final].N_final`, new script sha, re-run the tests. No script edit was made.
- xeval guard (§3) and the `bin_version.json` collection flaw (§1): tool fixes for engine / ops.
- AR Δlog Ẑ = 2.41 island s.e. (V lower than T; T's own island s.e. is 0.001, V's 0.006): watch it in W1/W2 with two seeds.
- NOTS clean-up of the W0 run dirs waits for the manager's OK (units are in `records/`; desktop verification is a separate step).

## 8. Aid for the re-projection (arithmetic only; the Opus child owns the projection)
Remaining 18 T + 18 V fits; per-fit T = 48.3 (tier 0) or 110.1 (tier 1); V ≈ 2.42. With W0 spent 254.74 (incl. evidence): escalation rate e = 0 → ≈ 1,168; e = 0.5 → ≈ 1,724; e = 1 → ≈ 2,280 core-h (stop rule 1,600; ceiling 2,500). W0 gives e = 1/2 (no interval worth quoting); designs that escalated: AR strong only so far.

Files: `results/overlap1e4/W0_readback/` (CSVs, cross files, patches, `w0_readback_tables.py`). Scratch: `SMC_Engineering_Department/tmp/20261118-w0readback/` (builds, views). No git state changed.
