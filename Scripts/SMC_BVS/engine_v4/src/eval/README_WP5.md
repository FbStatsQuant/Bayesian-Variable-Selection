# WP5 — evaluator, `law.bin`, Slurm driver, competitor harness (engine v4)

Scope: ENGINEERING_SPEC §0.3 WP5, §1 rows 6–7, §0-v2.3/§0-v2.7; EXPERIMENT_PLAN §3 (§3.3 = W3-DIST metrics), §4;
W3-DIST STATEMENT §0, §2; DECISIONS D-8, D-13. Contract: INTERFACES v0.1.1 (v0.1.2 items: see "Open").

## Commands
```
smcbvs4 eval --fit fit.bin --data data.bin --truth truth.json --out eval.bin [--law law.bin] [--cost cost.json]
             [--seed s] [--threads k] [--n-draws 10000] [--n-x 4000] [--n-gh 64] [--n-test 10000] [--rel-cut 1e-12]
smcbvs4 eval --competitor comp_<method>.json --data data.bin --truth truth.json --out ev_<method>.bin
smcbvs4 post --fit fit.bin --data data.bin --out law.bin [--rel-cut 1e-12] [--max-models M] [--draws N --seed s]
```
The record is `<out>.json` (written by WP1's `main`); `eval.bin` (kind 9) holds the 10⁴ draws of d_H per object.
GUARD-W: a fit whose `meta.status` is not `completed` gets a record with `fit_status` and no metric fields.

## What the record holds (schema `smcbvs4.eval/1`)
- **selection**: HPM (`hpm_S`, else store entry 0) and MPM (`pip_eq > 0.5`, `core/v3_run.R:163`) vs S₀: equality,
  Hamming, TP/FP/FN; F(S₀) scored directly (BitScorer) and checked against the ledger when S₀ ∈ 𝒯; outcome class
  correct / posterior (F(HPM) > F(S₀)) / search (F(S₀) > F(HPM)) / tie; provenance fields passed through from `meta`.
- **pip** for `pip_eq`, `pip_Z`, `pip_T`: sup over nulls, min over truths, Brier, counts > 0.1 / > 0.5, 20 reliability
  bins; island spread from `pip_r` (max sd, target 0.005 of §0-v2.3); max|PIP_eq − PIP_𝒯| against 0.01 + (1 − π̂(𝒯)).
- **evidence**: log Ẑ, log Ẑ_r, σ̂, robust σ̂ (1.4826 MAD), max − median, R_eff, R_eff/R′, max W_r, `log_Z_lower95`
  (`core/v3_run.R:155`), log Z_𝒯 = log Σ_𝒯 e^F, log Ẑ_occ for M ∈ {1, 10, 100, 1000} pooled and sd over islands (D-13).
- **store**: size, log Z_𝒯, π̂(𝒯) = Σ_𝒯 e^F / Ẑ, law size, dropped mass, max |F_store − F_recomputed|.
- **dist**: for Π̂^H, Π̂^M, Π̂^𝒯 and the oracle Π(·|S₀): (1) plug-in d_H² closed form, prediction error m² + s²;
  (2) posterior law of d_H from 10⁴ conjugate draws (quantiles; tail Π̂(d_H² > c log n/n), c ∈ {½, 1, 2, 4, 8});
  (3) predictive d_H² and KL (Student-t mixture; 4,000 x × 64-node Gauss–Hermite, centred on the geometric mean of
  the two densities); (4) test MSE and mean log predictive density on 10⁴ rows; ratios to the oracle.
  Test rows come from WP1's `gen::generate_test` (same definition as the data) when `truth.json` carries a gen spec.
- **cost**: fit timings from `meta.timings`; the sacct summary of `tools/slurm/p1m_cost.py` (`--cost`); eval wall.

## The plug-in closed form (plan §3.3 item 1)
For a draw (or the posterior mean) with raw coefficients b, intercept â and variance v: f(y|x) = N(â + xᵀb, v),
f*(y|x) = N(α* + xᵀβ*, σ²), and both share ν_x = N(0, Σ). For two normals
∫√(f f*) dy = √(2√(vσ²)/(v+σ²)) · exp(−Δ²/(4(v+σ²))) with Δ(x) = (â − α*) + xᵀ(b − β*) ~ N(m, s²),
m = â − α*, s² = (b − β*)ᵀΣ(b − β*). For Z ~ N(m, s²), E e^{−aZ²} = (1 + 2as²)^{−1/2} exp(−a m²/(1 + 2as²))
(complete the square). Hence d_H² = 1 − √(2√(vσ²)/(v+σ²)) (1 + 2as²)^{−1/2} exp(−a m²/(1 + 2as²)), a = 1/(4(v+σ²)),
computed as −expm1(log affinity). E_x(μ̂ − μ*)² = E Δ² = m² + s².

## Gate T7 (declared before the run; `tests/wp5/test_t7.cpp`, `v4_tests --full wp5_gate`)
20 fixtures = posterior-mean plug-ins of models near S₀ (S₀, +FP, −FN, proxy, badly misspecified) on data from IND /
AR(0.6) / BLK(20, 0.5) / FAC(0.3), n ∈ {100, 200, 400}, strong and weak amplitude.
- T7a plug-in d_H², T7b prediction error: closed form vs Monte Carlo over x ~ ν_x (mt19937_64, independent of the
  eval's Philox; y integrated by the two-normal affinity, itself checked against quadrature to 1e-12).
  Pass: |closed − MC| ≤ ½ unit of the 3rd significant digit, with MC s.e. ≤ ⅓ of that (MC doubles 2²⁰ … 2²⁷).
- T7c (sanity): joint (x, y) MC within 4 s.e.

Result (MEASURED, Owls, 3 threads, 2026-11-15, 187.6 s): **40 / 40 pass** — `tests/wp5/T7_result_owls_20261115.tsv`.
GH(64) predictive vs Simpson: worst relative error 5e-11.

## `law.bin` (kind 7; `include/v4/post.h`)
Models with F ≥ max F + log 10⁻¹² (store prefix; HPM order), weights, logm, Q, α_n, β_n, route, θ̄ (standardised), packed
Cholesky factor of H = (n+1)G_S + I, the union columns with x̄ and ŝ, ȳ, s_y, dropped mass; optional N draws
(role POST) of (model, a, v, b over the union columns).

## Slurm driver (`tools/slurm/`, dry run only)
`p1m_driver.py --plan plan.json --out <dir>` writes `stage_{setup,calibrate,islands,merge,eval}.sbatch`, `submit.sh`
(the manager's; `CONFIRM=yes`; verifies SHA256SUMS), `env.sh` (NOTS modules: GCC/14.3.0 CMake/3.31.8), `build.sh`,
job-manifest templates, one run manifest per fit, `ledger_row.md`. Graph: setup[1..F] → calibrate[1..F] (`aftercorr`)
→ per fit: islands[1..R′] (`afterok:<calibrate>_i`) → merge → eval(+post); 2 + 3F sbatch calls; ≤ 150 tasks; no task
above 2 h; worst case = Σ CPUs × limit. prep exit 20/21 end the fit's pipeline (OUTCOME file; later stages exit 0;
eval writes the outcome record). `p1m_manifest.py` fills inputs (path → content hash, producer record must be
completed); `p1m_cost.py` turns one sacct dump per batch into per-fit cost JSON. Example: `examples/plan_A2_pilot_1e4.json`
(2 fits at 10⁴: 40 tasks, worst case 164.0 billed core-h with the planning resources).

## Competitor harness (`tools/competitors/p1m_competitors.R`)
lasso-CV (λ_min, λ_1se; glmnet), MCP / SCAD (ncvreg), lasso via biglasso, L0Learn (L0L2), SuSiE (L = 10), varbvs,
BAS (p ≤ 10⁴; model law with our kernels), SIS screen (hand-off file for the engine), built-in baselines (marginal+OLS,
oracle OLS). **On Owls none of the packages is installed** (glmnet, ncvreg, biglasso, bigmemory, L0Learn, susieR,
varbvs, BAS): those methods give `package_missing` records and their code paths are untested. NOTS needs the same list
(not checked: no NOTS access for builders).

## Open
1. INTERFACES v0.1.2 (WP1 code not yet pushed): call `require_fma_variant()` / `binary_block()` in eval/post and put
   the block into `eval.bin` / `law.bin` meta; the manifest filler already accepts the v0.1.2 content hash.
2. fit.bin names read by eval but not fixed in INTERFACES: `hpm_S`, `meta.hpm_F`, `meta.logZ`, `meta.status`,
   `pip_r` (R′×p), `occ_top` / `occ_top_r`, `meta.occ_total(_r)`, `meta.timings` (change request to WP1/WP4).
3. Plan §3.1 exact log π₀(S₀) and the lattice mass need setup.bin tables (WP2): not in this slice.
4. Package-backed competitor paths untested until the packages exist somewhere we may run.
