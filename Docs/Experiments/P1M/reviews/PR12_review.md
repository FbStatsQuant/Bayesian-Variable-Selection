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
