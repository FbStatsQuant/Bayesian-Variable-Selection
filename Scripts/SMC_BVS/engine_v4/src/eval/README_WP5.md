# WP5 — evaluator, `law.bin`, Slurm driver, competitor harness (engine v4)

Scope: ENGINEERING_SPEC §0.3 WP5, §1 rows 6–7, §0-v2.3/§0-v2.7; EXPERIMENT_PLAN §3 (§3.3 = W3-DIST metrics), §4;
W3-DIST STATEMENT §0, §2; DECISIONS D-8, D-13, **D-17** (review PR12 MAJOR-1). Contract: INTERFACES v0.1.2.

## Commands
```
smcbvs4 eval --fit fit.bin --data data.bin --truth truth.json --out eval.bin [--law law.bin] [--cost cost.json]
             [--seed s] [--threads k] [--n-draws 10000] [--n-x 4000] [--n-gh 64] [--n-test 10000] [--rel-cut 1e-12]
smcbvs4 eval --competitor comp_<method>.json --data data.bin --truth truth.json --out ev_<method>.bin
smcbvs4 post --fit fit.bin --data data.bin --out law.bin [--rel-cut 1e-12] [--max-models M] [--draws N --seed s]
```
Mixture-predictive options (D-17): `--top-k 1000 --tail-r 1000 --tail-groups 8 --block-rows 500`. With a job manifest,
`params.truth_sha256` is checked against truth.json (`invalid_input` on a mismatch).
The record is `<out>.json` (written by WP1's `main`); `eval.bin` (kind 9) holds the 10⁴ draws of d_H per object.
GUARD-W (fail closed): a fit.bin without `meta.status` is `invalid_input`; a fit whose status is not `completed` gets a
record with `fit_status` and no metric fields (eval) or no law (post). `eval.bin` / `law.bin` take the fit's mode and
carry the binary block in `meta` (INTERFACES v0.1.2 §5.3); the FMA guard runs in `main` for every command.

## What the record holds (schema `smcbvs4.eval/1`)
- **selection**: HPM (`hpm_S`, else store entry 0) and MPM (`pip_eq > 0.5`, `core/v3_run.R:163`) vs S₀: equality,
  Hamming, TP/FP/FN; F(S₀) scored directly (BitScorer) and checked against the ledger when S₀ ∈ 𝒯; outcome class
  correct / posterior (F(HPM) > F(S₀)) / search (F(S₀) > F(HPM)) / tie; provenance fields passed through from `meta`.
- **pip** for `pip_eq`, `pip_Z`, `pip_T`: sup over nulls, min over truths, Brier, counts > 0.1 / > 0.5, 20 reliability
  bins; island spread from `pip_r` (max sd, target 0.005 of §0-v2.3); max|PIP_eq − PIP_𝒯| against 0.01 + (1 − π̂(𝒯)), computed from the unclipped ratio and labelled a
  diagnostic (`eq_T_target_note`).
- **evidence**: log Ẑ, log Ẑ_r, σ̂, robust σ̂ (1.4826 MAD), max − median, R_eff, R_eff/R′, max W_r, `log_Z_lower95`
  (`core/v3_run.R:155`), log Z_𝒯 = log Σ_𝒯 e^F, log Ẑ_occ for M ∈ {1, 10, 100, 1000} pooled and sd over islands (D-13).
- **store**: size, log Z_𝒯, π̂(𝒯) = Σ_𝒯 e^F / Ẑ, law size, dropped mass, max |F_store − F_recomputed|.
  **Sol F9:** π̂(𝒯) = Z_𝒯/Ẑ is a ratio of a deterministic sum and a noisy estimate. It is reported **unclipped** (it can
  exceed 1; `pi_T_hat_gt_1`), labelled a noisy diagnostic, and never treated as a bound on the store mass or as a
  certificate of P-STORE. The only deterministic bound is **log Z_𝒯 ≤ log Z** (`deterministic_bound`,
  `logZ_T_note`). `logZ_lower95` = log(0.05 Ẑ) is a Markov lower confidence bound and gives no upper bound on Z.
- **dist**: for Π̂^H, Π̂^M, Π̂^𝒯 and the oracle Π(·|S₀), at production scale (D-17; the store law keeps ≈ every
  S₀ ∪ {j}, so M ≈ 40p + 1 up to the 10⁶ cap):
  - `plugin`: closed form at the law's posterior mean (b̄ over the union of supports, ā, v̄) and its prediction error;
  - `weighted_plugin`: exact E_π[d_H²(f_{S,θ̄_S,v̄_S}, f*)] and E_π[prediction error], O(M) closed forms;
  - `post_dH`: 10⁴ conjugate draws (model by binary search on cumulative weights): quantiles and Π̂(d_H² > c log n/n);
  - `predictive`: d_H² and KL of the mixture predictive: exact top-K (1,000 by weight) + a stratified (systematic)
    importance sample of the tail (R = 1,000 in 8 independent groups, refreshed per block of 500 rows), an unbiased
    estimate of f̄ at every (x, y) node; reported with the x-MC SE, the tail-MC SE (between groups), the tail mass τ,
    the top-K-only value and the bound |d_H(f̄, f*) − d_H(f̄_K, f*)| ≤ √τ (flag `dH_bound_vacuous` when √τ ≥ the
    estimate: then cite the estimate ± tail SE, t with 7 df). Exact when the tail has ≤ R components;
  - `law_truncation` (Π̂^𝒯 only; Sol F9-b): the law is a **truncated approximation of the store BMA**; the summed omitted
    relative mass δ (`omitted_mass`) is carried as error terms: every d_H of the law object is within √δ of the store
    object's (`dH_bound_truncation`; H²(f̄_store, f̄_law) ≤ 1 − √(1 − δ) ≤ δ), and weighted means of d_H² within δ;
  - `test`: MSE of the predictive mean and mean log predictive density on 10⁴ rows (same estimator); ratios to the oracle.
  Rows are streamed in blocks with only the columns in use: for gen designs WP1's `gen::generate_test_rows`
  (PR #17; bit-identical to `generate_test`; rows 0 … n_x − 1 for the integrals, n_x … for the test rows), otherwise
  Markov / factor constructions on eval-seeded Philox normals. dᵀΣd is O(|cols|) for IND / AR / ADJ-OPP / BLK / FAC.
- **cost**: fit timings from `meta.timings`; the sacct summary of `tools/slurm/p1m_cost.py` (`--cost`); eval wall.

## The plug-in closed form (plan §3.3 item 1)
For a draw (or the posterior mean) with raw coefficients b, intercept â and variance v: f(y|x) = N(â + xᵀb, v),
f*(y|x) = N(α* + xᵀβ*, σ²), and both share ν_x = N(0, Σ). For two normals
∫√(f f*) dy = √(2√(vσ²)/(v+σ²)) · exp(−Δ²/(4(v+σ²))) with Δ(x) = (â − α*) + xᵀ(b − β*) ~ N(m, s²),
m = â − α*, s² = (b − β*)ᵀΣ(b − β*). For Z ~ N(m, s²), E e^{−aZ²} = (1 + 2as²)^{−1/2} exp(−a m²/(1 + 2as²))
(complete the square). Hence d_H² = 1 − √(2√(vσ²)/(v+σ²)) (1 + 2as²)^{−1/2} exp(−a m²/(1 + 2as²)), a = 1/(4(v+σ²)),
computed as −expm1(log affinity). E_x(μ̂ − μ*)² = E Δ² = m² + s².

## Gate T7 (declared before the run; `tests/wp5/test_t7.cpp`, `v4_tests --full wp5_gate`)
23 fixtures (20 + 3 after review PR12 MINOR-6) = posterior-mean plug-ins of models near S₀ (S₀, +FP, −FN, proxy, badly misspecified) on data from IND /
AR(0.6) / BLK(20, 0.5) / FAC(0.3), n ∈ {100, 200, 400}, strong and weak amplitude.
- T7a plug-in d_H², T7b prediction error: closed form vs Monte Carlo over x ~ ν_x (mt19937_64, independent of the
  eval's Philox; y integrated by the two-normal affinity, itself checked against quadrature to 1e-12).
  **Pass (PRE-DECLARED ABSOLUTE tolerances, Sol F9; constants in test_t7.cpp, fixed 2026-11-16 before the run):**
  the MC standard error is ≤ 1e-5 for d_H² and ≤ 2.5e-4 for the prediction error, AND
  |closed − MC| ≤ max(5 · SE, 1e-6). MC size doubles from 2²⁰ to at most 2²⁸ until the SE condition holds; failing
  either is a FAIL. (v1's "½ unit of the 3rd significant digit" is undefined near zero distance; it is now printed
  for information only.)
- Numerical error of the predictive integrals (`wp5_predictive_numerical_error_doubling`, declared before the run):
  doubling the GH order 64 → 128 at fixed rows changes d_H² and KL by ≤ 1e-8 (measured 1.3e-15 / 1.2e-16); doubling
  the x draws 4,000 → 8,000 changes them by ≤ 5 x-MC SE (measured 5.8e-5 vs SE 1.3e-4; KL 2.2e-4 vs 5.2e-4). The x
  error is Monte Carlo and is reported with every estimate (`h2_se_x`, `kl_se_x`).
- Fixtures added for Sol F9: empty support / zero signal (S₀ = ∅, the k = 0 model: plug-in = H²(N(ȳ, v̄), N(0, σ²))
  exactly, predictive vs Simpson ≤ 1e-9); the anchored (near-constant) preprocessing branch with unequal column scales
  (x = 1 + 1e-9 e, 3e4 e, 5 + 2e-3 e): raw-scale predictor = standardised predictor to 1.4e-7 relative, x̄ + ŝ z
  reproduces x to 2.7e-8 in z units. Already present: identical densities, mean/variance shifts, centring, finite
  mixtures (Simpson, M = 5,000).
- T7c (sanity): joint (x, y) MC within 4 s.e.

Result (MEASURED, Owls, 3 threads, 2026-11-16, absolute criterion): **46 / 46 pass**; worst |closed − MC| / tol = 0.54; max SE 9.6e-06 (d_H²), 2.4e-04 (prediction error); up to 2^28 draws — `tests/wp5/T7_result_owls_20261116.tsv`
(the v1 relative-criterion table of 2026-11-15 is superseded).
GH(64) predictive vs Simpson: worst relative error 5e-11.

## Scale test T7′ and the mixture estimator (D-17 item 7; `tests/wp5/test_scale.cpp`, `v4_tests --full wp5_`)
- Agreement: law of 5,000 conjugate components from real data (S₀, S₀ + j, S₀ + j + l; p = 2,000, IND; tempered weights,
  tail mass 0.53; 8 tail groups): top-K + tail d_H² 0.005008 vs the exact full mixture 0.005006 (tail SE 2.3e-6);
  KL 0.019415 vs 0.019404 (tail SE 9.0e-6). Within 3 SE (asserted), and |√h2_exact − dH_topK| ≤ √τ (asserted). The
  reviewer's 8-seed check (4 groups) found no detectable bias (mean z −0.02 / −0.38).
- T7′ **times the store-law metrics only**: `dist_metrics(Π̂^𝒯)` on a synthetic law (MEASURED, Owls, 3 threads,
  production sizes 10⁴ draws / 4,000 x × 64 GH / 10⁴ test rows, AR gen spec at p = 10⁶): M = 10⁵: 12.0 s, peak RSS 0.20 GB; M = 10⁶: 12.8 s, 0.81 GB
  (limits: 10⁴ rung 20 min × 4 CPUs, 8 GB; 10⁶ rung 1 h × 8 CPUs, 16 GB). Run-to-run spread on Owls (shared,
  loaded) is ≈ ±1–2 s: earlier runs 12.0 / 13.2 s and 13.6 / 14.9 s; the reviewer's 12.1 / 14.2 s.
- **A full `eval` at 10⁶ is NOT measured.** The real law path holds ≈ 1.6 kB per model (ModelPost + Component), i.e.
  ≈ 1.6 GB at M = 10⁶, twice T7′'s synthetic law; with data.bin (1.6 GB) and the file-backed fit.bin pages (≤ 2.3 GB)
  the reviewer ESTIMATES a peak of ≈ 5–6 GB (limit 16 GB). Law build (model_post per kept model, n = 200): 3.9 µs per
  model on 3 threads → ESTIMATE 4 s for 10⁶ models. A one-off end-to-end eval on the 10⁴ pilot will measure it.

## `law.bin` (kind 7; `include/v4/post.h`)
Models with F ≥ max F + log 10⁻¹² (store prefix; HPM order; at most 10⁶), weights, logm, Q, α_n, β_n, route, θ̄
(standardised), packed Cholesky factor of H = (n+1)G_S + I, the union columns with x̄ and ŝ, ȳ, s_y, dropped mass;
optional N draws (role POST), sparse: model, a, v and the coefficients on the model's own columns (`draw_ptr`/`draw_b`).
The file takes the fit's mode; `meta` carries the binary block.

## Slurm driver (`tools/slurm/`, dry run only)
`p1m_driver.py --plan plan.json --out <dir>` writes `stage_{setup,calibrate,islands,merge,eval}.sbatch`, `submit.sh`
(the manager's; `CONFIRM=yes`; verifies SHA256SUMS), `env.sh` (NOTS modules: GCC/14.3.0 CMake/3.31.8), `build.sh`,
job-manifest templates, one run manifest per fit, `ledger_row.md`. Graph: setup[1..F] → calibrate[1..F] (`aftercorr`)
→ per fit: islands[1..R′] (`afterok:<calibrate>_i`) → merge → eval(+post); 2 + 3F sbatch calls; ≤ 150 tasks; no task
above 2 h; worst case = Σ CPUs × limit. prep exit 20/21 end the fit's pipeline (OUTCOME file; later stages exit 0;
eval writes the outcome record). Every stage, eval and post included, runs with a job manifest: `p1m_manifest.py`
fills inputs (path → content hash; the producer record must be completed) and `params.truth_sha256` for eval.
`#SBATCH --kill-on-invalid-dep=yes` removes dependants of a failed task. `--dept`, `--out` and a run-time `P1M_DEPT`
must resolve (realpath) inside the department folder (tests: `P1M_TEST_ROOT` inside `$TMPDIR`). `submit.sh` calls
`${SBATCH:-sbatch}`; its test passes a stub by absolute path on a PATH holding no other sbatch. Eval resources:
10⁴ 4 CPUs / 8 GB / 20 min; 10⁵ 8 / 16 GB / 45 min; 10⁶ 8 / 16 GB / 1 h. `p1m_cost.py` turns one sacct dump per batch into per-fit cost JSON. Example: `examples/plan_A2_pilot_1e4.json`
(2 fits at 10⁴: 40 tasks, worst case 164.0 billed core-h with the planning resources).

## Competitor harness (`tools/competitors/p1m_competitors.R`)
lasso-CV (λ_min, λ_1se; glmnet), MCP / SCAD (ncvreg), lasso via biglasso, L0Learn (L0L2), SuSiE (L = 10), varbvs,
BAS (p ≤ 10⁴; model law with our kernels), SIS screen (hand-off file for the engine), built-in baselines (marginal+OLS,
oracle OLS). **On Owls none of the packages is installed** (glmnet, ncvreg, biglasso, bigmemory, L0Learn, susieR,
varbvs, BAS): those methods give `package_missing` records. Their extraction / record logic is tested against mocks
(`tools/competitors/mock_packages.R`, `P1M_COMPETITOR_MOCK`; structure only, not the real APIs — review MINOR-11,
DEFER until the packages are installed on NOTS). NOTS needs the same list. Predictive choices to state in C5:
penalised fits use σ² = CV error (σ² + prediction error); SuSiE and varbvs use a Gaussian at the posterior mean.

## Open
1. fit.bin names read by eval but not yet in INTERFACES (`hpm_S`, `meta.hpm_F/logZ/status/timings`, `pip_r` R′×p,
   `occ_top(_r)`, `meta.occ_total(_r)`): list sent to WP1 for v0.1.3 (review MINOR-2).
2. Plan §3.1 exact log π₀(S₀) and the lattice mass need setup.bin tables (WP2): not in this slice.
3. Real competitor package APIs untested until the packages exist on NOTS (MINOR-11, deferred).
4. A full eval at 10⁶ (I/O, store scan, law build, all objects) is not measured; first measurement on the 10⁴ pilot.
