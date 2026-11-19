# Criterion H for the 14 `VF` fits (I_max = 0 re-runs of the overlap V fits) vs the overlap T fits (2026-11-19/20)
**All 14 pairs pass: d_H(VF, T) ≤ 0.10 × d_H(T, f*); the maximum ratio is 0.0136** (ADJ-OPP r02 s1); the 14 self-checks (VF law vs the truth) and the 14 T self-checks agree with the engine's own d_H(T, f*) (`dist.T.predictive.h2` of the T eval record) to ≤ 1e-9 relative.
Tool: `smcbvs4_xeval` (b89cba4d, `~/SMC_Engineering_Department/tmp/20261119-w1readback/xeval_build/smcbvs4_xeval`, sha256 `afef0e463216edca…`): `cross --a <VF law.bin> --b <overlap T law.bin> --truth <VF truth.json> --data <VF data.bin> --data-b <T data.bin> --dataset ID --seed-id s --threads 3` (nice 19; its data-identity guard (X / y section hashes, n, p) passed for all 14), plus `--b-truth 1` self-checks of each VF and each T law; merged with `tools/xeval/merge_cross.py` → `cross_vf.json` (schema overlap1e4.cross_vt/1, 14 cells, 10 datasets). Pairs: the VF fit with the overlap T fit of the same dataset and seed (W0 uses the valid `.T2` T fits). Raw outputs `cross_vf_raw/`, summary `cross_vf_summary.json`, script `vf_cross.sh`, pair list `pairs.tsv`.

| VF fit | overlap T fit | d_H(VF,T) | d_H(T,f*) | d_H(VF,f*) | ratio d_H(VF,T)/d_H(T,f*) | ≤ 0.10 |
|---|---|---|---|---|---|---|
| 4-ADJOPP-n200-r01-VF-s1 | 4-ADJOPP-n200-r01-T-s1.T2 | 7.310e-04 | 5.799e-02 | 5.789e-02 | 0.0126 | yes |
| 4-ADJOPP-n200-r02-VF-s1 | 4-ADJOPP-n200-r02-T-s1 | 1.114e-03 | 8.163e-02 | 8.162e-02 | 0.0136 | yes |
| 4-AR-n200-r01-VF-s1 | 4-AR-n200-r01-T-s1.T2 | 5.936e-04 | 8.584e-02 | 8.583e-02 | 0.0069 | yes |
| 4-AR-n200-r01-VF-s2 | 4-AR-n200-r01-T-s2 | 6.302e-04 | 8.571e-02 | 8.585e-02 | 0.0074 | yes |
| 4-AR-n200-r02-VF-s1 | 4-AR-n200-r02-T-s1 | 5.806e-04 | 6.338e-02 | 6.337e-02 | 0.0092 | yes |
| 4-AR-n200-r02-VF-s2 | 4-AR-n200-r02-T-s2 | 5.858e-04 | 6.327e-02 | 6.324e-02 | 0.0093 | yes |
| 4-AR-n200-r03-VF-s1 | 4-AR-n200-r03-T-s1 | 7.506e-04 | 6.085e-02 | 6.091e-02 | 0.0123 | yes |
| 4-AR-n200-r03-VF-s2 | 4-AR-n200-r03-T-s2 | 6.719e-04 | 6.085e-02 | 6.088e-02 | 0.0110 | yes |
| 4-AR-n200-r04-VF-s1 | 4-AR-n200-r04-T-s1 | 5.214e-04 | 4.237e-02 | 4.240e-02 | 0.0123 | yes |
| 4-AR-n200-r04-VF-s2 | 4-AR-n200-r04-T-s2 | 5.334e-04 | 4.252e-02 | 4.243e-02 | 0.0125 | yes |
| 4-ARweak-n200-r01-VF-s1 | 4-ARweak-n200-r01-T-s1 | 7.559e-04 | 1.357e-01 | 1.356e-01 | 0.0056 | yes |
| 4-ARweak-n200-r02-VF-s1 | 4-ARweak-n200-r02-T-s1 | 7.155e-04 | 1.880e-01 | 1.880e-01 | 0.0038 | yes |
| 4-IND-n200-r01-VF-s1 | 4-IND-n200-r01-T-s1 | 8.903e-04 | 6.759e-02 | 6.755e-02 | 0.0132 | yes |
| 4-NULL-n200-r01-VF-s1 | 4-NULL-n200-r01-T-s1 | 8.788e-05 | 2.579e-02 | 2.579e-02 | 0.0034 | yes |

d_H = the cross predictive Hellinger distance (x rows 0…3,999, 64-node Gauss–Hermite, the engine eval's estimator); the ratio uses d_H, not h². NULL r01: d_H(T, f*) = 0.0258 (nonzero), ratio 0.0034. Criterion H in the overlap read-back was the same quantity for V vs T; this is the I_max = 0 counterpart.
