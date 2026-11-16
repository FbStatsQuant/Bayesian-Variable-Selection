# PR #12 review — WP5 evaluator, `law.bin`, dry-run Slurm driver, competitor harness

Reviewer: Opus 5.5 (independent of the author), high effort; brief `briefs/REVIEW_PR_template.md` (N = 12).
Scope: `exp/P1M-wp5-eval` @ 25e268b into `exp/P1M-engine`, commits after 8ff9775 only (6c64f29, 9be2b7a, 9fbb37b,
ff007ad, 25e268b; 27 files, +3,596 / −6, all under `Scripts/SMC_BVS/engine_v4/`). Checkout: own worktree, detached at
`origin/exp/P1M-wp5-eval`; read only (no pushes, no GitHub comments). Contract INTERFACES v0.1.2; metrics
EXPERIMENT_PLAN §3.3 and W3-DIST STATEMENT §0, §2.

## Verdict: **ACCEPT-WITH-FIXES**

The mathematics is right. I derived the closed-form plug-in Hellinger myself and checked it against independent
nested quadrature, to ≤ 1e-13 relative over the whole (m, s², v, σ²) range. The conjugate posterior and the map back to
the raw scale match `core/` and STATEMENT §0. Gate T7 is a real brute-force Monte Carlo, and it reproduces bit for bit.
The Slurm driver cannot submit.

There is one **MAJOR, blocking** problem: the Π̂^𝒯 distribution metrics do not scale. The predictive cost is linear in
the number of law components, and the test-row matrices are built over the union of all law columns. I measured that
at p ≥ 10⁴ the 10⁻¹² cut keeps essentially the whole store. So eval runs out of time even on the 10⁴ pilot, and runs out
of memory at 10⁵–10⁶ (MAJOR-1). Fix this before any pilot eval is submitted. The rest is minor.

Counts: CRITICAL 0 · MAJOR 1 · MINOR 11.

## Tests I ran (Owls, `nice -n 19`, 3 threads, TMPDIR = `~/SMC_Engineering_Department/tmp/20261115-review-pr12`, removed after)
- `tests/run_tests.sh --quick --threads 3`: **42 test cases, 0 failed**. WP5 Slurm-driver tests OK (12 tests).
  Competitor harness OK, but every package is missing on Owls (glmnet, ncvreg, biglasso, L0Learn, susieR, varbvs, BAS,
  bigmemory). rc = 0.
- `v4_tests --full`: **43 test cases, 0 failed**. Gate T7: **40 / 40 pass** in 175.7 s. My `T7_result.tsv` is
  **byte-identical** to the committed `tests/wp5/T7_result_owls_20261115.tsv` (closed form, MC, SE and draws columns).
  Worst |closed − MC| / tol = 0.445.
- My own checks:
  1. **Plug-in d_H² closed form.** I transcribed `h2_plugin` (dist.cpp:40-45) into R. I compared it with nested
     adaptive quadrature E_Δ ∫√(N(y; Δ, v) N(y; 0, σ²)) dy, Δ ~ N(m, s²). This is independent of `h2_normals` and of
     the code's algebra. I used 7 cases, including large |m| (up to 3), s² up to 5, v/σ² from 0.2 to 4, and s² = 0.
     Worst relative error: **8e-14**.
  2. **Raw-scale map.** At every sample row, â + xᵀb equals ȳ + s_y Σ θ̄_j z_j, with max difference **2.7e-15**. The
     data had non-zero column means (x = 3 + 2N); b = (0.959, −0.800) and â = 1.22, against truth (1, −0.8) and 1.
  3. **Law size and cost** (bench programs linked against `libv4_bit.a`; see MAJOR-1).

## (a) Mathematics: closed form, conjugate posterior, raw scale (all verified)
- **Derivation.** Take f(y|x) = N(â + xᵀb, v) and f*(y|x) = N(α* + xᵀβ*, σ²). For two normals,
  ∫√(f f*) dy = √(2√(vσ²)/(v + σ²)) · exp(−Δ²/(4(v + σ²))), where Δ(x) = (â − α*) + xᵀ(b − β*).
  Under Gaussian ν_x with mean 0, Δ ~ N(m, s²) with m = â − α* and s² = (b − β*)ᵀΣ(b − β*).
  Completing the square gives E e^{−aΔ²} = (1 + 2as²)^{−1/2} exp(−a m²/(1 + 2as²)), with a = 1/(4(v + σ²)).
  This is exactly plan §3.3 item 1 and dist.cpp:40-45, computed stably as −expm1(log affinity). Prediction error
  E Δ² = m² + s² (eval.h:110) is also correct.
  - m = â − α* (dist.cpp:28) relies on μ_x = 0. That holds for every WP1 gen design (IND, AR stationary with unit
    variance, BLK, ADJ-OPP) and for FAC; I checked against gen.cpp.
  - `design_cov` (model.cpp:48-56) matches gen.cpp. AR is ρ^{|j−l|}, since x₁ = e and the recursion keeps unit variance.
    BLK blocks are (j−1)/b on 1-based indices, which equals gen's 0-based j/b.
- **Conjugate posterior.** In core, X is centred and scaled to sample SD 1, and G = XᵀX is unnormalised
  (v3_preprocess.R, v3_score.h:12). The likelihood ys = X_Sθ + ε, the prior θ | v ~ N(0, n v (G_S + I)⁻¹) and the
  prior v ~ IG(0.01, 0.01) give:
  - posterior precision (1/(nv))((n + 1)G_S + I) = H/(nv), so θ | v, S ~ N(n H⁻¹ z_S, n v H⁻¹);
  - v | S ~ IG(a₀ + n/2, b₀ + Q/2), with Q = yᵀy − n z_SᵀH⁻¹z_S.
  This matches eval.h:9-11 and posterior.cpp:132-165. θ̄ is golden-tested against core's own solves (1e-13), and
  logm/Q/F against `v3::Scorer` bits.
  - **Draws** (dist.cpp:182-209): g ~ Gamma(α_n), v = β_n/g, then t = L^{−T}ξ, so Cov t = H⁻¹ and
    θ = θ̄ + √(nv) t. This is correct.
  - **Student-t predictive** (dist.cpp:229-240): df 2α_n, scale² (β_n/α_n)(1 + n x̃ᵀH⁻¹x̃), times s_y². This is correct.
  - **GH centring** on the Gaussian approximation of √(f̄ f*), and the KL rule under f*: correct. They are tested
    against Simpson (5e-11).
- **Raw scale.** b_j = s_y θ_j / ŝ_j and â = ȳ − x̄ᵀb, with x̄_j = col_max·col_mean, ŝ_j = col_max·col_sd and
  v_resp = s_y² v. This also holds in v3_standardise's anchored two-pass branch, since x̄ = x₁ + dm(um + corr) and
  ŝ = dm·us reproduce z exactly. The plug-in uses posterior means E b = s_y θ̄/ŝ and E v = s_y² β_n/(α_n − 1).
  Plug-in intercept, no intercept uncertainty: as STATEMENT §0 / R1 define f_{S,θ,v}.

## (b) Is T7 an independent brute-force Monte Carlo? **Yes for the expectation it targets, with stated shared pieces.**
**Independent:**
- the RNG (mt19937_64, not the eval's Philox);
- its own Cholesky and Δ arithmetic (test_t7.cpp:68-96);
- the y-integral, done through `h2_normals` (separately checked against Simpson to 1e-12), not through `h2_plugin`'s
  algebra;
- MC size doubled until SE ≤ tol/3, with pass = |closed − MC| ≤ ½ unit of the 3rd significant digit;
- T7c, a joint (x, y) MC that avoids `h2_normals`.

**Shared with the code under test**, so not validated by T7:
1. Σ (`design_cov_matrix`, test_t7.cpp:38, 72).
2. The μ_x = 0 convention (test_t7.cpp:87).
3. The fixtures' (b, â, v), which come from `model_post` / `b_mean` / `v_mean`. T7 therefore does not test the posterior
   or the raw-scale map. The golden θ̄ test and my check 2 cover those.

**Coverage gap:** all 20 fixtures have small |m|, because the intercept is estimated, and v ≈ σ² except f16–f19. My
quadrature check covers the rest of the range. See MINOR-6.

## (c) Slurm driver: dry run only, arrays, department paths. **Yes, with small hardening items.**
- **Never submits.** p1m_driver.py has no `subprocess`, `os.system` or `ssh`; it only writes files. `submit.sh` is
  generated for the manager and refuses to run without `CONFIRM=yes` and a matching `SHA256SUMS`.
- **Arrays.** setup[1..F] → calibrate[1..F] (`aftercorr`) → per fit, islands[1..R′] (`afterok:<cal>_i`) → merge → eval.
  That is 2 + 3F sbatch calls (≤ 23 under the 150-task cap). merge and eval are single tasks per fit; this is acceptable,
  because per-task dependencies on different island arrays cannot be written as one array.
- **Paths.** Every generated path is under `$DEPT`:
  - runs, `--output`/`--error` and TMPDIR go through `scratch`;
  - build and bin go under `scripts/<batch>`;
  - `--constraint=sapphirerapids`, the 150-task cap, the 2 h task cap and the worst case are enforced.

  The guards are weaker than "never outside" (MINOR-8).

## Findings

### MAJOR-1 — Π̂^𝒯 distribution metrics are infeasible at production scale (time at 10⁴; memory at 10⁵–10⁶). Blocking for pilot eval.
**Where:**
- `src/post/law.cpp:26` keeps F ≥ F_max + log 10⁻¹², capped at `max_models` = 10⁶ (post.h:42; eval calls `build_law`
  with the default, run.cpp:151).
- `src/eval/run.cpp:58-63` makes `cols` the union of the columns of **every** law component.
- `src/eval/dist.cpp:152-179` materialises (n_x + n_test) × |cols| doubles **twice** (gen's column-major `Xt`, then the
  copies).
- `dist.cpp:263-287` evaluates the full mixture, `log_mix` over all M components, at 2 × n_gh nodes for each of the
  n_x rows.

**Evidence (measured on Owls with this PR's code):**
- **Law size.** I scored S₀ and every S₀ ∪ {j} with `model_post` (AR(0.6), strong signal, s₀ = 5). Within the 10⁻¹² cut:
  **9,995 / 9,995** at (n, p) = (200, 10⁴) and (400, 10⁴); **99,995 / 99,995** at (200, 10⁵). Together these models
  carry **1.19×, 0.52× and 1.00×** the weight of S₀. The best null addition is only 0.9–4.2 nats below S₀.
  - Pairs sit about 2 × 9 nats down, still inside the 27.6-nat window. So at 10⁴ the law is the whole store
    (40p + 1 ≈ 4·10⁵); at 10⁶ it is the `max_models` cap (10⁶). The e2e test already shows this at p = 12
    (law M = 481 = the whole store).
  - This contradicts the plan's premise (§3.3: "the weight sits on a handful"), and a mass-based cut would not shrink
    the law much: the S₀ + j singles hold about a third to a half of the mass, spread evenly.
- **Time.** The cost is **24 µs per (x row × component)**; this was flat in M from 100 to 1,000.
  - 10⁴ rung: n_x = 4,000 and M ≈ 4·10⁵ give ≈ 3.8·10⁴ CPU-s ≈ 10.7 core-h for Π̂^𝒯, i.e. ≈ 2.7 h wall on the
    planned 4-CPU, **20-min** eval task (also above the 2 h `max_task_hours`).
  - 10⁶ rung: M = 10⁶ gives ≈ 2.7·10⁴ core-h per fit.
- **Memory.** |cols| ≈ p, so the test-row matrices take 14,000 × p × 8 B × 2: ≈ 2.2 GB at 10⁴, ≈ 22 GB at 10⁵
  (eval memory 8 G) and ≈ 220 GB at 10⁶ (16 G). Eval runs out of memory on every 10⁵ and 10⁶ fit.
- `post --draws N` also writes a dense N × C `draw_b` (law.cpp:94-106). With C ≈ p that is 80 GB at N = 10⁴ and p = 10⁶.
  The driver does not pass `--draws`.

**Suggested fix.** The metric definition needs an HQ / W3-DIST decision. Options, which can be combined:
- (i) Keep `law.bin` as specified (D-8), but compute the predictive metrics of Π̂^𝒯 on a declared approximation:
  - exact top-K components (e.g. K = 1,000, or until cumulative mass 1 − ε);
  - plus an importance subsample of the tail, refreshed per x row;
  - report the residual mass and an MC SE.

  The posterior law of d_H by draws (item 2) is exact already, and its O(M) inverse-CDF scan could be a binary search
  on cumulative weights.
- (ii) Stream x / test rows in row chunks, generating only the columns of the components in use (gen_test is
  counter-based and row-addressable), instead of materialising n_rows × |union|.
- (iii) Hoist the constant `lgamma` pair out of `log_comp`: α_n is the same for every model, so the t normaliser's
  lgamma part is one constant (≈ 2–3× speedup, not enough alone).
- (iv) Store draws sparsely (per-model columns).
- (v) Add a scale test (e.g. M = 10⁵ synthetic components) that asserts eval wall and RSS against the driver's planned
  limits.

Relay to HQ: the plan's "handful" premise is false at the planned (n, p).

### MINOR-1 — Contract: eval/post do not call `pm::require_fma_variant()` and write no binary block (INTERFACES v0.1.2 §5.3/§6, lines 249, 269)
These are absent because WP1's `include/v4/provenance.h` is not in the base (8ff9775); README_WP5 Open #1 says so.
Track it as a merge condition once WP1 lands. README_WP5.md:3 still says "INTERFACES v0.1.1"; update it to v0.1.2.

### MINOR-2 — Contract: fit.bin names that eval reads are not in INTERFACES §5.2
The names are `hpm_S`, `meta.hpm_F`, `meta.logZ`, `meta.status`, `pip_r` as R′ × p (INTERFACES lists only the
per-island `pip_r` of length p), `occ_top`/`occ_top_r` and `meta.occ_total(_r)` (as hex u64), and `meta.timings`.
README Open #2 already asks WP1/WP4 for this. Get it into INTERFACES before WP4's merge writer is frozen.

### MINOR-3 — `law.bin` mode is hard-coded to V (law.cpp:83, `fmt::Writer W(fmt::K_LAW, fmt::M_V)`)
eval.bin inherits the fit's mode (run.cpp:235). A compat or law-mode fit gets a law.bin labelled V. Pass `FB.mode()`
through `post::run`.

### MINOR-4 — GUARD-W fails open (run.cpp:113)
`jstr_or(meta, "status", "completed")` treats a fit.bin **without** `meta.status` as completed. `post` has no GUARD-W at
all (law.cpp:157-170): on an incomplete fit it builds a law, or throws "empty store". Require the field (missing →
`invalid_input`) and apply the same guard in `post`.

### MINOR-5 — Raw-scale intercept and the draw covariance are untested
- test_eval.cpp:74-78 computes `a0` and discards it (`(void)a0`); the comment's check of ȳ + s_y Σ θ̄(x − x̄)/ŝ is not
  done.
- `wp5_posterior_draw_moments` (test_eval.cpp:97-108) checks only means, not Cov(b) = s_y² n E[v] D⁻¹H⁻¹D⁻¹.

I verified both by hand (above). Add the two assertions; the first is my check 2, at tolerance 1e-12.

### MINOR-6 — T7 fixtures barely exercise the m-term and v ≠ σ²; Σ is never checked against WP1 gen
- **m-term.** All fixtures plug in an estimated intercept, so |m| = O(n^{−1/2}).
  - Add 2–3 fixtures with a deliberately shifted â (|m| ~ 1) and v/σ² ∈ {0.3, 3}.
- **Σ.** T7 and T7c take Σ from `design_cov`, as the closed form does. `wp5_draw_x_covariance` tests draw_x against
  hard-coded values, not against gen.
  - Add a test of `design_cov` against the empirical covariance of `gen::generate_test` rows, including AR column gaps
    and BLK block boundaries. In production the predictive uses gen rows while the plug-in uses `design_cov`, so a
    mismatch would make the two inconsistent unnoticed.

### MINOR-7 — No `--kill-on-invalid-dep=yes` in the sbatch header (p1m_driver.py:157-182)
If a setup, calibrate or merge task fails, its dependants stay PENDING (DependencyNeverSatisfied) indefinitely. They
count against the 150-task budget and need a manual `scancel`. Add `#SBATCH --kill-on-invalid-dep=yes`, or document
the cleanup in submit.sh.

### MINOR-8 — The "inside the department" guards are partial (p1m_driver.py:411; submit.sh/build.sh `P1M_DEPT`)
- `--dept` is checked by string prefix. `/home/fb31/SMC_Engineering_Department_x` and `.../SMC_Engineering_Department/../x`
  both pass, and `P1M_DRIVER_TEST` bypasses the check.
- `--out` (the local generation directory) is not checked.
- `submit.sh` and `build.sh` accept a run-time `P1M_DEPT` override.

Use `os.path.realpath` + `os.path.commonpath` for `--dept` and `--out`. Limit the test bypass to a temp-dir root. In
submit.sh, refuse a `P1M_DEPT` outside `$HOME/SMC_Engineering_Department` unless a test flag is set.

### MINOR-9 — The driver test executes `submit.sh` with `CONFIRM=yes` relying on PATH order (test_p1m_driver.py:144-153)
This is harmless on Owls, which has no sbatch. On a host with a real `sbatch`, a failed fake install, e.g. a
non-executable file, would submit. Make submit.sh call `${SBATCH:-sbatch}` and have the test set `SBATCH` to the fake's
absolute path. The test should also assert `command -v sbatch` is the fake before running.

### MINOR-10 — eval and post run without a job manifest (p1m_driver.py:247-252)
The other stages go through `--manifest` with content-hash-verified inputs (INTERFACES §5.3). eval/post read fit.bin,
data.bin and truth.json unverified. Add `eval.json` and `post.json` templates; truth.json can be hashed with
`sha256_file`, as eval already records it.

### MINOR-11 — Competitor package paths are untested (tools/competitors/p1m_competitors.R)
No package is installed on Owls, so only the built-ins (marginal + OLS, oracle OLS, SIS) are exercised. README_WP5
reports this honestly. The NOTS package list (glmnet, ncvreg, biglasso + bigmemory, L0Learn, susieR, varbvs, BAS) goes
to the manager per the brief. Two notes:
- Penalised predictives use σ² = CV error, which is σ² + prediction error.
- SuSiE and varbvs predictives are Gaussian approximations, as labelled.

The C5 comparison should state both choices.

## Checklist items with no finding
- **Bit-identity.** WP5 claims bits only through WP1's BitScorer (logm, Q, route, log dets, F). The golden test
  compares those bit for bit against `core/cpp/v3_score.h`, including odd n, ρ = 0.9 and an exact fit, and θ̄ to 1e-13.
  The WP5 sources are built with `V4_BIT_FLAGS`.
- **Determinism.** `dist_metrics` is thread-invariant (tested with 1 vs 3 threads). Reductions are serial over stored
  per-item values, and the store mass uses fixed 65,536 chunks.
- **Discipline.**
  - Nothing is written outside `engine_v4/`; no file is over 50 MB (the T7 table is 61 lines).
  - Tests write under `$TMPDIR`.
  - The only hard-coded path is the driver's `DEPT_DEFAULT` (by design, overridable).
  - Removing the eval/post stubs from `stubs.cpp` is correct.
- **32-bit limits.** Sizes use `size_t`/`int64` (model_ptr, LH_ptr i64; X buffers size_t). `(int)comps.size()` is fine
  up to 10⁶.

---

## Re-check (2026-11-16): head f596f27, WP5 changes 25e268b..f596f27 excluding the merged base (0502009 = merge of a4ca68c)

Same reviewer, same rules: detached worktree, read only. TMPDIR `~/SMC_Engineering_Department/tmp/20261116-review-pr12b`,
removed after. Disposition: `PR12_disposition.md` (D-17).

### Verdict: **FIX FIRST**
The fixes are small and confined to Sol F9. D-17 is implemented correctly and MINORs 1–10 are fixed; the scale
blocker (MAJOR-1) is resolved. What is missing is the **Sol F9 items**, which REVIEW_disposition_sol assigns to "WP5
(PR #12 fixes)":
- π̂(𝒯) is still clipped;
- the tolerances are not absolute;
- the law truncation is neither propagated nor labelled.

Each is a few lines (list below). After that, MERGE. No full re-review is needed: I would check only the F9 diff.

### Tests run (Owls, nice 19, 3 threads)
- `run_tests.sh --quick`: **52 test cases, 0 failed**. Slurm-driver tests OK (12). Competitor harness OK, including the
  new mock run: all 9 package methods `completed` and their predictives scored.
- `v4_tests --full`: **55 test cases, 0 failed**, in 3 min 52 s; peak RSS 0.85 GB for the whole run.
  - T7: **46 / 46**. My `T7_result.tsv` is byte-identical to the committed table.
  - The M = 5,000 agreement test: exact 0.005006, approximation 0.005006, tail SE 3.6e-6.
  - T7′: M = 10⁵ in 12.1 s / 0.20 GB; M = 10⁶ in 14.2 s / 0.81 GB.
- My own checks (bench programs linked against `libv4_bit.a`):
  1. **Estimator bias and SE calibration.** Real-data laws of M = 6,000 models at p = 3,000 (IND gen), at two
     temperatures (tail mass 0.64 and 0.75). I ran 8 independent tail draws against the exact full mixture
     (`top_k = M`). Standardised errors (approx − exact)/SE_tail:
     - tail mass 0.64: mean **−0.02**, rms 1.30; KL mean +0.00;
     - tail mass 0.75: mean −0.38, rms 0.90.

     There is no detectable bias from the √ / log of the estimated density. The rms is consistent with a 4-group SE
     (t₃: expected rms √3). One |z| = 2.54 out of 16. The √τ bound held in all 16 runs.
  2. **Memory of the real law path.** `ModelPost` + `Component` copies take **≈ 1.6 kB per model**, i.e. ≈ 1.6 GB at
     M = 10⁶. That is twice T7′'s synthetic Law; see R-2.

### (1) D-17 implementation
- **Exact weighted closed forms** (dist.cpp:480-495). E_π[d_H²(f_{S,θ̄_S,v̄_S}, f*)] and E_π[prediction error] are
  per-component closed forms, O(M · (k + s₀)); this is correct.
  - `quad_form` (dist.cpp:22-47) is O(U). I re-derived it:
    - AR uses S_l = (S_{l−1} + d_{l−1}) ρ^{c_l − c_{l−1}}, giving Σ_{i<l} d_i ρ^{c_l − c_i};
    - BLK is Σ_b [ρ(Σ_b d)² + (1 − ρ)Σ_b d²];
    - FAC is ρ(Σd)² + (1 − ρ)Σd².

    `wp5_quad_form_matches_dense` checks it against the dense form, with AR gaps and BLK boundaries.
- **Draws by binary search** (dist.cpp:233-244). `u·cum.back()` with `upper_bound` selects component c with probability
  w_c; this is correct. law.bin draws are sparse (`draw_ptr`/`draw_b` over the model's own columns, law.cpp:102-116),
  and the e2e test checks `draw_ptr` dims.
- **Top-K + stratified tail** (dist.cpp:317-350, 405-446, 524-578). This is unbiased for f̄ at every node. In the
  systematic sample, each point (r + u₀)/R_g · τ is marginally uniform on [0, τ), so each draw picks tail component c
  with probability w_c/τ. Hence E[τ · mean_r f_{c_r}(y)] = Σ_tail w_c f_c(y), and the estimate f̂ = Σ_top w_c f_c + that
  is unbiased (common random numbers across rows do not affect this).
  - The G = 4 groups use independent offsets (address position g), so `sd(h2_g)/√G` is a valid between-group SE. The
    x-noise cancels because the groups share the rows.
  - **√τ bound.** f̄ = (1 − τ) f̄_K + τ f_T gives √(f̄ f̄_K) ≥ √(1 − τ) f̄_K pointwise in (x, y). Hence
    H²(f̄, f̄_K) ≤ 1 − √(1 − τ) ≤ τ, and by the triangle inequality for the metric d_H,
    |d_H(f̄, f*) − d_H(f̄_K, f*)| ≤ √τ. Here `out[G+1]` = exact part / (1 − τ) is the correctly normalised f̄_K.
  - Note: at realistic tail masses (0.53–0.75) the bound is **vacuous** (0.73–0.87, against d_H ≈ 0.07). The reported
    value rests on the tail estimate and its SE, as D-17 intends; the record should say so (R-3).
- **Streamed rows** (dist.cpp:174-230). Rows come in blocks of 500, using only the columns of the top-K and the sampled
  tail (max 2,003 columns at p = 10⁶). They are bit-equal to `gen::generate_test` (`wp5_make_rows_equal_gen_test`,
  4 designs). `design_cov` is checked against gen-sampled covariances (`wp5_design_cov_matches_gen_rows`; this also
  closes MINOR-6b).
- **Agreement at M = 5,000.** Confirmed: the value matches the exact full mixture within 3 tail SE, for both d_H² and
  KL. The exact comparator is the same `MixAt` path with every component exact, which was itself validated against
  Simpson (5e-11). The test uses one fixed seed. My 8-seed run is the stronger evidence.

### (2) Is T7′ honest about what it times? **Yes in its output and README; the headline numbers are not.**
The test times only `dist_metrics` for the store object Π̂^𝒯 on a synthetic law. It prints "dist_metrics wall", and
the law build is extrapolated and printed as an "ESTIMATE" (4.1 µs/model → ≈ 4 s at 10⁶). The README adds that reading
the fit.bin and data.bin is not measured.

Not covered:
- the `eval` command end to end (mmapped 2.3 GB fit.bin and its content hash, a 1.6 GB data.bin, store_mass, store_find
  over 4·10⁷ entries, writing eval.bin);
- the H, M and oracle objects (cheap: one component each);
- `post`.

The synthetic Law is about half the memory of the real path (R-2). My estimate of the real eval peak at 10⁶ is
≈ 1.6 GB (law) + 1.6 GB (data) + up to 2.3 GB of file-backed fit pages ≈ 5–6 GB, against 16 GB. Wall time is
dominated by the measured 14 s plus a few seconds of I/O and hashing, against 1 h. The margins are large, so this does
not block.

Wording should still change: the commit message and LOG quote "M = 10⁵ in 12.0 s / 0.20 GB, M = 10⁶ in 13.2 s / 0.81 GB"
as if for eval, and the README quotes different numbers (13.6 s / 0.09 GB, 14.9 s / 0.81 GB). (R-2)

### (3) MINORs 1–11
| # | status | evidence |
|---|---|---|
| 1 FMA guard, binary block | **fixed** | the CLI calls `require_fma_variant()` for every command except info/version (main.cpp:61); `binary_block()` goes into eval.bin meta (run.cpp:250) and law.bin meta (law.cpp:91) |
| 2 fit.bin names | **routed** | to WP1 for INTERFACES v0.1.3 per the disposition; not WP5 code |
| 3 law.bin mode | **fixed** | `write_law(..., ff.bin->mode())` (law.cpp:188); the e2e test asserts the mode |
| 4 GUARD-W | **fixed** | missing `meta.status` → `invalid_input` in eval (run.cpp:120-122) and post (law.cpp:180); post on an incomplete fit writes no law; all tested |
| 5 intercept, draw covariance | **fixed** | raw-scale identity at every row (≤ 1e-12); Cov(b) against s_y² n E[v] D⁻¹H⁻¹D⁻¹ within 5 SE |
| 6 m-term, v ≠ σ²; Σ vs gen | **fixed** | 3 fixtures (|m| = 0.8–1.2, v/σ² ∈ {0.5, 2}) → T7 46/46; `design_cov` vs gen rows |
| 7 kill-on-invalid-dep | **fixed** | in the header; asserted in the test |
| 8 department guards | **fixed** | realpath + commonpath for `--dept` and `--out`; `P1M_TEST_ROOT` must lie inside `$TMPDIR`. The prefix-trick, `..` and `--out` cases are all tested. submit.sh and build.sh resolve `P1M_DEPT` |
| 9 sbatch stub | **fixed** | `${SBATCH:-sbatch}`; the test uses an absolute stub path and a PATH of only `fbin:/usr/bin:/bin`, and asserts `which sbatch` is the stub |
| 10 eval/post manifests | **fixed** | `eval.json` and `post.json` templates with fit.bin and data.bin inputs. eval refuses on a `truth_sha256` mismatch (tested) |
| 11 competitor mock | **done (DEFER kept)** | the mocks exercise extraction and records for all 9 methods; records carry `version: "mock"`, and mocks load only via `P1M_COMPETITOR_MOCK`. Real APIs are still unverified (acknowledged) |

### Sol F9 items (now in scope): **not done (the FIX FIRST items)**
- **F9-a: Z_𝒯/Ẑ is still clipped.**
  - `run.cpp:183`: `tgt = 0.01 + (1 − min(1, exp(logZ_T − logZ)))`. This silently clips π̂(𝒯) at 1, and
    `eq_T_target_met` then acts as if the store mass were certified.
  - `store.pi_T_hat` itself is reported unclipped (correct).
  - Fix: base the target on the deterministic quantity only, or report `eq_T_target` from the unclipped ratio with a
    flag `pi_T_hat_gt_1`. Label `pi_T_hat` "noisy diagnostic, not a bound on store mass". Add a record line that the
    only deterministic bound is **log Z_𝒯 ≤ log Z**; `logZ_minus_logZ_T` exists but carries no label. `logZ_lower95`
    is a Markov lower confidence bound (`core/v3_run.R:155`); keep it, but document that it gives no upper bound on Z.
- **F9-b: the omitted mass is a sum, but it is not propagated and the law is not labelled.**
  - `store.dropped_mass` is the directly summed Σ_dropped e^F / Σ_𝒯 e^F (law.cpp:28-30). That is the SUM F9 asks for.
  - But nothing propagates it to the distance metrics, and nothing calls law.bin a truncated approximation.
  - Fix: add `dH_bound_truncation = √dropped_mass` to each Π̂^𝒯 dist block. By the same argument as the √τ bound,
    |d_H(f̄_store, f*) − d_H(f̄_law, f*)| ≤ √(1 − √(1 − δ)) ≤ √δ. Add the words "truncated approximation of the store
    BMA" to the law.bin meta and the README.
- **F9-c: tolerances are not absolute and pre-declared.**
  - T7 still passes on "½ unit of the 3rd significant digit" (test_t7.cpp:64, `tol3`). Sol notes this threshold is
    undefined near zero distance.
  - There is no doubling check on GH order or n_x against a declared absolute tolerance for the predictive.
  - Fix: declare absolute tolerances in README_WP5 before the run, e.g. |Δh2| ≤ 1e-5 and |Δpred_error| ≤ 1e-4, with MC
    SE ≤ ⅓ tol. Apply them in T7 alongside or instead of `tol3`. Add one test that doubles n_gh (64 → 128) and n_x
    (4,000 → 8,000) on a fixed law, and asserts the change is below the declared tolerance (the x-MC SE is reported
    already).
- **F9 fixture list.** Already covered: identical densities (`h2_normals` = 0), shifts and unequal scales (T7 20–22),
  finite mixtures (Simpson and M = 5,000), centring (golden data with x = 3 + 2N). Not seen: **zero signal / empty
  support** (S₀ = ∅ oracle, k = 0 component in dist_metrics), and the **near-constant (anchored) preprocessing branch**
  through the raw-scale map. Add both; small tests.

### Remaining minors (non-blocking; can go with the F9 fix)
- **R-1.** The tail SE uses G = 4 groups (3 df). With a fixed seed, the M = 5,000 gate at 3 SE is deterministic, but
  under t₃ about 6 % of seeds would fail. My 8-seed run had one |z| = 2.54. Use G = 8, or a t_{G−1} quantile, for
  gates and confidence intervals.
- **R-2.** Relabel T7′ as "dist_metrics(Π̂^𝒯) wall/RSS" in the commit and LOG, and reconcile the three sets of numbers
  (commit 12.0 / 13.2 s; README 13.6 / 14.9 s; my run 12.1 / 14.2 s). State that the real law path is ≈ 1.6 kB/model
  (≈ 1.6 GB at 10⁶), and that a full eval at 10⁶ is estimated at ≈ 5–6 GB peak, not measured. A one-off end-to-end
  eval on the 10⁴ pilot will measure it.
- **R-3.** In the `predictive` block, add a flag or note when `dH_bound` ≥ the estimate itself (vacuous), so the
  analysis cites the estimate ± SE rather than the bound.

Counts for the re-check: open items F9-a, F9-b, F9-c and the F9 fixtures (fix first; small); R-1 to R-3 (minor).

---

## Final re-check (2026-11-16): head 85530b1, diff f596f27..85530b1. Scope: Sol F9 items, R-1, R-3, the T7′ wording, and WP5's switch to `gen::generate_test_rows`

### Verdict: **MERGE**

**Tests** (Owls, nice 19, 3 threads, TMPDIR `…/tmp/20261116-review-pr12c`, removed after):
- quick: **61 test cases, 0 failed**; Slurm driver OK (12); competitor harness OK, including the mocks.
- `--full`: **64 test cases, 0 failed**.
  - T7: **46 / 46** under the new absolute criterion; my table matches the committed `T7_result_owls_20261116.tsv`.
    Worst |closed − MC| / tol = 0.54.
  - M = 5,000 agreement: 0.005008 vs exact 0.005006 (tail SE 2.3e-6, z ≈ 0.9); KL z ≈ 1.2.
  - T7′: M = 10⁵ in 12.8 s / 0.20 GB; M = 10⁶ in 13.8 s / 0.81 GB.

| item | status | evidence |
|---|---|---|
| F9-a: Z_𝒯/Ẑ unclipped and labelled | **done** | `store.pi_T_hat` is unclipped, with `pi_T_hat_gt_1`, `pi_T_hat_note` ("noisy diagnostic … never certifies P-STORE") and `deterministic_bound` ("log Z_T ≤ log Z … no deterministic upper bound") (run.cpp:169-176). The eq_T target uses the **unclipped** ratio and is labelled a diagnostic (run.cpp:190-192); the e2e test asserts the exact formula. `logZ_T_note` and `logZ_lower95_note` are in the evidence block (metrics.cpp:128, 149) |
| F9-b: law labelled a truncated approximation; δ carried | **done** | law.bin `meta.label` and `meta.truncation` (law.cpp:86-87). `store.law_label`. The Π̂^𝒯 dist block has `law_truncation{label, omitted_mass = δ, dH_bound_truncation = √δ, weighted_h2_bound_truncation = δ}` (dist.cpp:456-466); e2e asserts the labels and that the bound equals √δ |
| F9-c: absolute, pre-declared tolerances | **done** | T7 constants are declared in code and README before the run: SE ≤ 1e-5 (d_H²) / 2.5e-4 (prediction error), and |closed − MC| ≤ max(5·SE, 1e-6). MC doubles 2²⁰…2²⁸. The v1 relative criterion is printed for information only. This is well defined near zero |
| F9-c: quadrature / x-draw doubling | **done** | `wp5_predictive_numerical_error_doubling`, with tolerances declared in the test header. GH 64 → 128 changes d_H² by **1.3e-15** and KL by 1.2e-16 (declared ≤ 1e-8). x 4,000 → 8,000 changes d_H² by 5.8e-5 against x-SE 1.3e-4, and KL by 2.2e-4 against 5.2e-4 (declared ≤ 5 SE) |
| F9 fixture: empty support / zero signal | **done** | a = 0 gives S₀ = ∅. The k = 0 component's plug-in equals `h2_normals(ā, v̄, 0, σ²)` to 1e-15 with s² = 0; the weighted plug-in equals the plug-in. The predictive matches Simpson to 1e-9. Selection is "correct"; `min_true` = null |
| F9 fixture: anchored near-constant branch + unequal scales | **done** | `prep::standardise` asserted anchored on x = 1 + 1e-9 e. Scales 3e4 and 2e-3 with centre 5. Max |(x − x̄)/ŝ − z| = 2.7e-8 and raw-vs-standardised predictor 1.4e-7, against declared 1e-6 / 1e-5 (the cancellation bound eps/1e-9 is stated) |
| R-1: tail groups | **done** | default G = 8 (run.cpp:51); the note says to cite ± SE with t_{G−1} |
| R-3: vacuous-bound flag | **done** | `predictive.dH_bound_vacuous` and `note` (dist.cpp:582-584) |
| T7′ wording | **done** | README: "T7′ **times the store-law metrics only**"; "**A full `eval` at 10⁶ is NOT measured**". It gives the 1.6 kB/model real law path and the 5–6 GB estimate, and records the run-to-run spread with all three earlier timings. The commit message corrects f596f27's wording |
| `generate_test_rows` switch | **OK** | the copied gen arithmetic is replaced by WP1's `gen::generate_test_rows` (PR #17, merged). `wp5_make_rows_equal_gen_test` (4 designs, bit-equal to `generate_test`) and `wp5_design_cov_matches_gen_rows` still pass. Non-gen designs are unchanged |

**Non-blocking notes** (fix whenever convenient):
- **N-1: the √δ claim is stated too broadly.** README_WP5 lines 44-46 and the comment at dist.cpp:457-459 say "every d_H of the law object is within √δ". The derivation covers the **mixture predictive** d_H(f̄, f*), and the δ bound covers the weighted d_H². For `post_dH`, the tail probabilities and quantile levels move by at most δ (total variation), not √δ. The posterior-mean plug-in is not covered by either bound. Restrict the wording to those cases.
- **N-2: the x-doubling check is lenient.** The 8,000-row set contains the 4,000 rows, so the difference has SD ≈ SE₄₀₀₀/√2, and the 5-SE threshold is about 7 of its own SDs. The F9 requirement (reported x-MC SE, quadrature error ≪ tolerance) is met; just do not cite this check as tight.

Final review counts: CRITICAL 0 · MAJOR 0 open (MAJOR-1 resolved by D-17) · MINOR 0 open (1–10 fixed; 11 mocked and DEFER) ·
F9 done · 2 non-blocking notes.
