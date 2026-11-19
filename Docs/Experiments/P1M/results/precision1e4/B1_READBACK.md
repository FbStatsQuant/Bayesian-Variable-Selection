# B1_READBACK: boundary-regime V-vs-T check (ADDENDUM_1_BOUNDARY, f8513e74): AR-weak, p = 10⁴, n = 100, one dataset, V and T × 2 seeds (Sonnet worker; 2026-11-19)

**DESCRIPTIVE ONLY: no outcome class, no criterion verdict, no effect on any gate.** Records `records/precision1e4/B1/` (`4-ARweak-n100-r91-{V,T}-s{1,2}`; `sha256sum -c` re-run here: 0 non-OK in all 4 fit and 2 batch units; V build `d0c30b65…`, T build `09249230…`, both F = eefcbc4a). Outputs in `results/precision1e4/B1/` (not committed): `cross_vt.json`, `cross/`, `v2/` and `registered/` (`stdout.txt`, `wave_check.csv`, `per_fit.csv`), `b1_extras_output.txt`. Scripts: `compare_overlap_v2.py` sha `4f402e51…` and registered `compare_overlap.py` `311bbad8…` (both verified, unchanged), xeval `smcbvs4_xeval` (b89cba4d, sha `afef0e46…`).

## Answer in the overlap's terms
**V and T agree on this dataset in every per-pair quantity the overlap scored (S1 HPM equal, S2 no higher F for T, S3 MPM equal, P PIP, E1 log Ẑ, H Hellinger, C cost), but no arm recovers S₀: the HPM is the EMPTY model in all four fits.** At n = 100 (β_min √n ≈ 3.6) the posterior mode is the null model (F_hpm − F_S₀ = +24.85 nats; S₀ is not in the store; outcome class `posterior`), carrying 0.744–0.746 of the mass; the remaining ≈ 26 % is a diffuse tail over 400,001 store models (no null variable has PIP above 0.0105; the smallest PIP among the 5 true variables is 1.8 × 10⁻⁵). So this is a regime where the posterior is null-dominated with a diffuse tail, not a multi-model spread; V and T agree on it, including on the tail (cross d_H ≈ 4 × 10⁻⁴). The registered script (shown beside) calls both T fits "not delivered" for N = 40,000 ≠ 10,000, the same artefact as in the overlap, so its comparison columns are NA.

## Table (v2 `--wave-check`, `B1/v2/wave_check.csv`, `B1/b1_extras_output.txt`)
| | seed 1 | seed 2 |
|---|---|---|
| HPM (size), V / T | ∅ (0) / ∅ (0) | ∅ (0) / ∅ (0) |
| HPM = S₀ (V, T) | False, False | False, False |
| HPM equal V vs T; MPM equal | True; True | True; True |
| F_hpm (V = T to 12 digits); F_S₀; difference | −147.775522; −172.629; +24.854 | same |
| T higher F than V | False | False |
| HPM mass exp(F_hpm − log Ẑ), V / T | 0.7437 / 0.7451 | 0.7459 / 0.7438 |
| log Ẑ V, T; **V − T** (island s.e.; in s.e.) | −147.4793, −147.4813; **+0.00197** (0.00328; 0.60) | −147.4824, −147.4795; **−0.00282** (0.00309; 0.91) |
| max_j \|PIP_V − PIP_T\| (÷ bound max(0.01, 3 s.e.)) | 5.1 × 10⁻⁴ (0.051) | 1.18 × 10⁻³ (0.118) |
| max island PIP sd, V / T (target 0.005) | 0.0027 / 0.0009 | 0.0029 / 0.0009 |
| cross d_H(V, T) [h2 ± se] | 3.6 × 10⁻⁴ [1.3e-7 ± 1.0e-7] | 4.2 × 10⁻⁴ [1.7e-7 ± 1.7e-7] |
| d_H(T, f\*) / d_H(V, f\*); **d_H(V,T) / d_H(T,f\*)** (bound 0.10) | 0.3353 / 0.3350; **0.0011** | 0.3356 / 0.3348; **0.0012** |
| triangle screen > 10 % | False | False |
| tier_final / N_final, V; T | 0 / 2,500; **1 / 40,000** | 0 / 2,500; **1 / 40,000** |
| core-h V; T | 0.804; 36.63 | 0.702; 44.21 |
(oracle d_H to truth 0.107; engine predictive h2 of T 0.112 and V 0.112 against the oracle 0.013: this dataset is far from identified at n = 100, for both arms equally.)

## Notes
- **Cross-Hellinger:** `cross --a V/law.bin --b T/law.bin --truth --data V/data.bin --data-b T/data.bin` for the 2 seed pairs, same flags as the overlap, no guard bypass; both rc 0, `exact_a/b` False, dropped mass 0, tail mass 0.085 each. The cross h2 (1–2 × 10⁻⁷) is of the size of its own s.e., i.e. consistent with 0; d_H = √h2 is the (upward-biased) point value. **Self-checks (B = truth, 4): 2 bit-equal, 2 differ from the engine's `dist.T.predictive.h2` by 1.1 × 10⁻¹⁶ (1 ulp; V s1, T s1)**, while all 12 W3 self-checks were bit-equal; not material here, stated.
- **Calibration (`calib_meta.json`):** V: I_used 3 = I_max, `grid_unconverged` True (the constant "bounded-stop" at I_max 3, as in every overlap V fit). **T: both seeds escalated to tier 1 (N = 40,000) on `grid_unconverged` after 14 rebuilds at tier 0 (3/20 in the overlap); T s1 then converged (13 rebuilds), T s2 did not converge even at tier 1 (14 rebuilds, final `grid_unconverged` True): the first T fit of the study with the final flag True.** `checks_passed_final` True for all four.
- **Cost:** V 0.80 / 0.70 against the class `ARweak n100` (E 1.36; soft 3.0, hard 3.4); T 36.6 / 44.2 against the report line 172.5. B1 total **82.35 core-h** (V batch 1.51, T batch 80.84) against the quote 115 (wave stop 230): 0.72 ×. No stop or report line tripped.
- **ADDENDUM premise:** the overlap's AR-weak datasets (n = 200) did not recover S₀ either (HPM ≠ S₀ in all 8 fits, FZ_READBACK §8.7a), so "recovered S₀" in the addendum's motivation should be read as PIP/predictive recovery; at n = 100 even the HPM size is 0.

## Offset cell (bnd; N 2,500, m 1, I_max 3, k = 16; one dataset: a point, not tested; no offset-vs-p)
δ_B1 = mean over the 2 seeds of [log Ẑ_V − log Ẑ_T] = **−0.00042 = −0.13 s_T** (s_T = 0.00324). Per seed pair +0.00197 (+0.61 s_T) and −0.00282 (−0.87 s_T); seed spread (sd of the two differences) 0.00339 = 1.05 s_T; island s.e. of log Ẑ: V 0.0025 / 0.0027, T 0.0021 / 0.0014. Both T references are tier 1. The overlap's δ is −0.00394 (10 datasets) and the leg's cells about −0.006 (FZ_READBACK §2); this one point is 0.0004 from zero against a seed spread of 0.0034; nothing is inferred from it.
