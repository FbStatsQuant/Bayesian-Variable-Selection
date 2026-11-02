# LOWP_SPEC: addendum to master Part II for Regime L, p ∈ {20, 30}

Owner: LOWP thread (New Campaign). Status: draft for HQ, 2026-10-28. Authority: `CHARTER.md` §1, `DECISIONS.md` D1–D6, master Part II (§II.2–§II.13). Everything not stated here is exactly master Part II. Where master Part II says "Regime L: no benchmark", D3 overrides it: the 8 primary benchmark methods run at p ≤ 30 (adaptations in `../bench_lowp/ADAPTATIONS.md`).

## L.1 Design

| Item | p = 20 | p = 30 |
|---|---|---|
| n | 200 | 200 |
| Population blocks of 5 | 4 | 6 |
| s₀ (D2: one signal per block of 5, up to the pattern) | 4 (blocks 1–4) | 5 (blocks 1–5; block 6 has none) |
| Scenarios | S1–S6 (master §II.4, built from blocks of 5) | same |
| Scales used | c ∈ {1, 0.5} (`c100`, `c050`) | same |
| Replicates | 100 | 100 |
| Datasets / cases | 600 / 1,200 | 600 / 1,200 |

The stored `Y` keeps all five master columns (c100, c075, c050, c035, c025) so the generator, files and hashes stay uniform with master §II.9; only `c100` and `c050` are fitted (D1).

## L.2 Truth (D2)

`truth(p)` is master §II.9 with STEP = 1 and S0 = {20: 4, 30: 5}: blocks = 1 + k, active = 5(block − 1) + POS[k mod 6], β = PATTERN[k mod 6], k = 0..s₀−1.

| p | s₀ | Active indices | β | Blocks | Within-block position | S6 ρ at each signal |
|---|---|---|---|---|---|---|
| 20 | 4 | 3, 7, 14, 16 | 1.4, −1.0, 1.8, −1.2 | 1, 2, 3, 4 | 3, 2, 4, 1 | .4 .5 .6 .7 |
| 30 | 5 | 3, 7, 14, 16, 25 | 1.4, −1.0, 1.8, −1.2, 0.8 | 1, 2, 3, 4, 5 | 3, 2, 4, 1, 5 | .4 .5 .6 .7 .8 |

The p = 30 row is master §II.3 unchanged.

**Smallest eigenvalue of Σ_s** (check 1, tolerance 1e-4):

| p | S1 | S2 | S3 | S4 | S5 | S6 |
|---|---|---|---|---|---|---|
| 20 | 1.0000 | 0.3351 | 0.3000 | 0.1500 | 0.3000 | 0.3000 |
| 30 | 1.0000 | 0.3341 | 0.3000 | 0.1500 | 0.3000 | 0.1000 |

At p = 20, S6 has blocks ρ = .4, .5, .6, .7 only, so its smallest eigenvalue is 1 − 0.7 = 0.3 (block 6, ρ = .9, exists only at p = 30).

**Nominal SNR = c²·β′Σ_sβ** (σ = 1):

| p | Scenario | c = 1 | c = 0.5 |
|---|---|---|---|
| 20 | S1, S3, S4, S6 | 7.64 | 1.91 |
| 20 | S2 | 6.36 | 1.59 |
| 20 | S5 | 5.65 | 1.41 |
| 30 | S1, S3, S4, S6 | 8.28 | 2.07 |
| 30 | S2 | 7.00 | 1.75 |
| 30 | S5 | 6.77 | 1.69 |

The p = 30 rows equal master §II.5. Values are recomputed by `R/lowp_generate.R::lowp_scenario_check()` and saved in `tests/scenario_check_lowp.out`.

## L.3 Seeds

seed = base + 10000·s + r, s = 1..6, r = 1..100 (master §II.7).

| p | Data base | Dev base | CV-fold base | Dev-fold base | Method seed |
|---|---|---|---|---|---|
| 20 | **1,210,000** (new) | **2,210,000** (new) | **3,210,000** (new) | **4,210,000** (new) | data seed + 4,000,000 → 5,220,001–5,270,100 |
| 30 | 1,310,000 (master) | 2,310,000 (master) | 3,310,000 (master) | 4,310,000 (master O11) | data seed + 4,000,000 → 5,320,001–5,370,100 |

- **Choice of the p = 20 bases.** They follow master's digit convention (millions digit = role, hundred-thousands digit = p class: 2 → 20, 3 → 30, 4 → 500, 5 → 1000).
- **Collision check.** Every used range [base + 10001, base + 60100] (and the method range) was checked against every base in master §II.7 (data, dev, fold, dev-fold and method ranges for p = 30, 500, 1000) and the sealed held-out bases recorded in `F_2026-10-19…/RUNS.md` (data 7,610,000/7,710,000; folds 8,610,000/8,710,000). No overlap; the check is executable (`R/lowp_generate.R::lowp_seed_collision_check()`, output in `tests/seed_collisions.out`).
- **Method seed** = data seed + 4,000,000, identical for both scales of a dataset; passed to SMC-BVS as its `seed`, and to every benchmark wrapper as `seed` (master §II.7, §III.3.0 RNG rule).
- **Dev method seed** = dev data seed + 4,000,000 (6,220,001–6,270,100 at p = 20; 6,320,001–6,370,100 at p = 30); dev cases are excluded from all counts.
- **Repeat SMC seeds** (RUN_DESIGN.md): repeat m = 1..5 uses method seed + 1,000·m. This stays in the same 10000-slot as the dataset, with offsets 1,001–5,100 that no base + 10000·s + r (r ≤ 100) can reach, so it collides with no data, fold or method seed. Checked by the same script.
- Folds: master §II.9 rule with the fold base above; identical across scales. Only F1–F3 (CV) use them.

## L.4 Generator

`R/lowp_generate.R::generate_dataset(p, scenario, replicate, kind)` is master §II.9 with `p %in% c(20L, 30L)` and the bases above: Mersenne-Twister / Inversion / Rejection; `set.seed(seed)`; `Sigma <- scenario_covariance(scenario, p)`; `raw_X <- matrix(rnorm(n*p), nrow = n) %*% chol(Sigma)` (X first); `X <- scale(raw_X)` (sd n−1); `eps <- rnorm(n)`; β consumes no random numbers; `Y[, c] = c·Xβ + ε` for the five scales. Folds: `set.seed(fold_seed); sample(rep(1:10, length.out = 200))`. `scenario_covariance()` is copied unchanged from the bench20261019 generator (`F_2026-10-19…/code/R/gen_prod_data.R`), so it is the master construction for any p divisible by 5.

## L.5 Files and separation of truth (master §II.10)

Identifiers: `dataset_id = p{pppp}_S{s}_r{rrr}` (`p0020_S3_r007`), `case_id = dataset_id_scale_key`. Layout (same names locally and on NOTS):

```
inputs/p0020/, inputs/p0030/   X (n×p, scaled:* attributes stripped), Y (n×5), foldid, dataset_id, data_seed, fold_seed   ← fitting jobs open only this
truth/p0020/, truth/p0030/     active, beta, signal = Xβ, eps, scenario                                                     ← generator checks and scoring only
manifests/                      inputs_manifest_lowp.csv, truth_manifest_lowp.csv (file SHA-256 + float64-LE SHA-256 of X, each Y column, signal, eps, foldid)
dev/{inputs,truth,manifests}/   dev datasets (r = 1..5 per scenario and p; 60 rows; ids dev_p{pppp}_S{s}_r{rrr})
```

- One RDS per dataset, `saveRDS(compress = FALSE)`. The file SHA-256 depends on the R version that wrote it (the float64 hashes do not), so sealed files are generated once and copied to NOTS; NOTS regeneration is a check (L.6 4(b)), not a source; files `chmod a-w` after sealing; `truth/` set to mode 000 during fitting waves and restored by scoring.
- The **exact enumerator reads `inputs/` only** (it is a fitting-side computation on X, y, like SMC). Truth enters only in `scoring/`.
- Size: X = 200·p·8 bytes (32 KB at p = 20, 48 KB at p = 30); all 1,200 production datasets plus 60 dev datasets take about 72 MB (measured, 2,524 files). They live in NOTS home under `New_Campaign/inputs`, `truth`, `manifests` (charter §2).

## L.6 Verification checks (gate G2, master §II.13 adapted)

1. **Truth placement**: `truth(20)`, `truth(30)` reproduce L.2 exactly (indices, blocks, positions, S6 ρ, β); smallest eigenvalues match L.2 to 1e-4; p = 30 also matches master `scenario_check.out` rows.
2. **Standardisation**: every dataset, max|colMeans(X)| < 1e-10 and max|colSums(X²)/(n−1) − 1| < 1e-10.
3. **Response**: max|Y[, c] − (c·signal + ε)| ≤ 1e-12·max(1, max|Y|), every column.
4. **Bit-identical regeneration**: (a) regenerate S1 r1, S4 r50, S6 r100 per p in a fresh R process and compare with `identical()` and float64 hash; (b) on NOTS, regenerate the same 6 datasets plus all 1,200 X/ε hashes and compare with the local manifest (pilot bundle). Check (b) requires all 1,200 production and 60 dev rows and all six regenerated copies; anything less is INCOMPLETE, not PASS. A mismatch STOPS the run: keep both evidence sets and diagnose (possible causes include a BLAS/`chol` difference, manifest corruption, a seed or configuration change, or a code difference). The sealed local files stay canonical; changing the canonical source would be an explicit HQ decision followed by a new audited seal, manifest and transfer. (Master's p = 500 Oct-14 identity check does not apply.)
5. **Manifest closure**: 1,200 production and 60 dev rows; all hashes recompute; seeds unique and equal base + 10000·s + r.
6. **Σ sanity (descriptive)**: per scenario and per population block, the within-block mean sample correlation averaged over the 100 replicates is within ±0.02 of that block's population value (0.5^|j−k| pattern means in S2 are not checked; 0.7 in S3; 0.85 in S4; 0.7 within and 0.3 between in S5; ρ_b block by block in S6); report the maximum block deviation.
7. **Low-p extra**: the p = 30 X and ε of S1 r1 regenerated with master's p = 30 base reproduce the same bits through both code paths (`lowp` generator and a literal transcription of master §II.9), so the extension changed nothing at p = 30.

Checks 1–3 and 5–7 run in `R/lowp_verify.R`; check 4(b) runs in the NOTS pilot bundle.

## L.7 Exact reference (scoring-side reference, not the production exact branch)

Per dataset and scale: log Z (standardised working-model scale, as §I.6), all p exact PIPs, exact HPM with F and the §I.6 tie rule, the HPM certificate quantities of §I.2 (η, margin, certificate bound), exact MPM (PIP > 1/2), posterior mass by size, the top 1,000 models with F. The score is F(S) of master §I.2, computed with the SMC core's `v3_score.h` arithmetic (`enum/`); its equivalence evidence is in `enum/VALIDATION.md`. The posterior mass of the truth is computed at scoring time as exp(F(S₀) − log Z), so the enumerator never sees truth.

Both production branches of SMC-BVS select SMC at these sizes: 2²⁰ and 2³⁰ exceed (5H₀ + 4N₀)p = 12,560p (251,200 and 376,800).
