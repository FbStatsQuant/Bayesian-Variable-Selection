# CODE_FACTS — SMC-BVS exactly as coded (W3-READER helper)

Source of truth: `Scripts/SMC_BVS/core/` on branch `theory/W3-READER` (equal to `main` for `Scripts/`).
**Pin convention:** `core/X:n` means `Scripts/SMC_BVS/core/X`, line n (repo-relative after expanding `core/`).
Where code and docs disagree, the **code wins** (flagged "DOC≠CODE"). "UNVERIFIED" = not checked against code.
Production entry point: `v3_fit(X, y, seed, allocation, ls0 = TRUE)` (`core/v3_fit.R:73`). Default `ls0 = TRUE` = "v3.1".

---

## 1. Preprocessing (`core/v3_preprocess.R`)

- **Input checks → `invalid_input`:** X numeric matrix, y numeric vector, `length(y) == nrow(X)`, all entries finite, n ≥ 3, p ≥ 1 (`core/v3_preprocess.R:99-107`). Seed must be integer in [1, 2^31−1] (`core/v3_preprocess.R:7-11`, `core/v3_fit.R:88-89`).
- **Dropped columns:** a column is dropped iff all its entries are *exactly* equal (`core/v3_preprocess.R:111-112`). `kept`/`dropped` are recorded (`:113`). No columns left → status `no_predictors`, `hpm = ∅` (`:114`). y exactly constant → `y_constant`, `hpm = ∅` (`:115`). Precedence: invalid_input, no_predictors, y_constant (`:95`).
- **p** everywhere downstream = number of **retained** columns (`core/v3_preprocess.R:113`, `core/v3_fit.R:104`).
- **Standardisation** of every kept column and of y (`core/v3_standardise`, `core/v3_preprocess.R:37-68`): divide by max|x|, subtract the mean, divide by the sample SD with denominator n−1 (`:38-41, :66-67`). Hence each column has mean 0 and ‖x_j‖² = n−1, and yᵀy = n−1 (comment `core/cpp/v3_blocks.h:8-9`). A numerically stable "anchored two-pass" centring is used only when the centred values are ≤ √eps (`core/v3_preprocess.R:47-65`); same target, different arithmetic.
- **Intercept:** not a model parameter; handled by centring X and y. The working likelihood has no intercept term (scorer uses centred standardised y and X; `core/cpp/v3_score.h:10-13`). Docs: "no intercept; y is centred" and an equivalence to an integrated-intercept contrast model (`Docs/Methodology/METHODOLOGY_v3.md:100, :120-127`, stated "to be proved, V1" — not a code fact).
- **Exact duplicates (|r_jl| ≥ 1−1e-10)** are only *reported* as `dup_components` (union-find), never dropped (`core/v3_fit.R:119`, `core/cpp/v3_core.cpp:742-760`).
- Scales kept for back-mapping: `col_max, col_mean, col_sd, y_max, y_mean, y_sd_scaled, s_y` (`core/v3_preprocess.R:124-127`). No back-transformation of coefficients is computed (the method reports model-space outputs only).

## 2. Model and prior as coded (`core/cpp/v3_score.h`)

Notation (standardised data): n, p (retained), S ⊆ {1..p}, k = |S|, G = XᵀX (`v3_score.h:44-53`), z = Xᵀy (`:54-55`), G_S, z_S the S-submatrix/subvector.

- **Size cap:** K = min(p, ⌊n/2⌋) (`core/cpp/v3_score.h:40`; R mirror `core/v3_preprocess.R:21`). Scoring |S| > K is an error (`v3_score.h:230`); all moves forbid it (§5).
- **Model prior (truncated beta-binomial BB(1,p), per-model):**
  w(k) = ½ / C(2p−1, k) (`core/cpp/v3_score.h:64-65`; equals B(1+k, 2p−k)/B(1,p) per comment `:15`),
  W_K = Σ_{k≤K} C(p,k) w(k) (`:66-68`),
  ϖ(S) = w(|S|)/W_K for |S| ≤ K, 0 otherwise (`:69-70`, stored as `logprior[k]`).
- **Likelihood:** y | β_S, σ², S ~ N_n(X_S β_S, σ² I_n) (implied by the closed form below; docs `METHODOLOGY_v3.md:100`).
- **Coefficient prior:** β_S | σ², S ~ N_k(0, n σ² (G_S + I_k)⁻¹) — a unit-information g-prior (g = n) on a unit-ridged Gram. Not stated literally in code; it is the unique Gaussian prior that reproduces the coded matrices H_S = (n+1)G_S + I and A_S = G_S + I (`core/cpp/v3_score.h:175-183`): with V⁻¹ = (G_S+I)/n, G_S + V⁻¹ = H_S/n and det(I + V G_S) = det H_S / det A_S. Matches docs `METHODOLOGY_v3.md:101`.
- **Noise variance:** σ² ~ IG(shape a₀, rate b₀), a₀ = b₀ = 0.01 (`core/cpp/v3_score.h:14`), integrated out analytically.
- **Closed-form marginal (exactly as coded):**
  ν = a₀ + n/2 (`v3_score.h:57`)
  log C_n = a₀ log(2b₀) + lgamma(a₀ + n/2) − (n/2) log π − lgamma(a₀) (`:58-59`)
  H_S = (n+1) G_S + I_k,  A_S = G_S + I_k (`:175-183`)
  Q_S = yᵀy − n z_Sᵀ H_S⁻¹ z_S (`:217`); if Q_S < 1e-8·yᵀy it is recomputed in the non-negative form Q = ‖y − X_S b‖² + (‖X_S b‖² + ‖b‖²)/n, b = n H_S⁻¹ z_S (`:145-160, :219`)
  **log m(S) = log C_n − ½ (log det H_S − log det A_S) − ν log(2b₀ + Q_S)** (`:222-223`)
  log m(∅) = log C_n − ν log(2b₀ + yᵀy) (`:60`, `:231`).
  Numerics: Cholesky on stored Gram → Cholesky on Gram recomputed from X → augmented Householder QR → `NumericalFailure` (`:227-238`).
- **Score F (log unnormalised posterior of S):** **F(S) = log ϖ(|S|) + log m(S)** (`core/cpp/v3_engine.h:97`; `core/cpp/v3_core.cpp:117`).
- **Target:** π(S | y) ∝ exp F(S) on {|S| ≤ K}, i.e. π(S|y) = ϖ(S) m(S)/Z with **Z = Σ_{|S|≤K} ϖ(S) m(S)** — YES, proportional to exp(F(S)). Evidence: exact branch log Z = log Σ exp F (`core/cpp/v3_core.cpp:539, :557`); SMC Ẑ targets the same Z (§5).
- Heuristic score error bound η(S) = 64 eps[ν(yᵀy/Q)(1 + k cond_H) + k(cond_H + cond_A) + |log C_n| + ν|log(2b₀+Q)|] (`v3_score.h:240-246`), labelled "heuristic (not a validated interval bound)" (`core/cpp/v3_core.cpp:120`). Used only by exact-branch `global_certified`.

## 3. Block partition (`core/cpp/v3_blocks.h`)

- **Block size B = min(⌊√n⌋, ⌊√p⌋, 16)** (`core/v3_preprocess.R:22`); 16 = implementation cap `B_MAX` (`core/cpp/v3_core.cpp:145-146`). NOT 15. (DOC≠CODE minor: comment at `v3_core.cpp:144` says "1 <= B <= 20"; constant is 16.)
- **Construction:** complete-linkage hierarchical clustering on d_jl = 1 − |r_jl| (r = sample correlation from G) with deterministic tie rules (`v3_blocks.h:39-108`); top-down cut: split any node with > B members (`:121-133`); next-fit packing of the resulting clusters, in leaf order, whole clusters only, into blocks of ≤ B members (`:134-141`). Blocks C_1..C_J partition the retained columns.
- **Purpose:** each block is small (≤ 16 ⇒ ≤ 2¹⁶ sub-models), so every sub-model of every block can be scored exactly (§4), and correlated predictors tend to share a block, so the start law π₀ captures within-block competition (e.g. proxies) exactly.
- **Neighbour graph** (used by the N-swap move): r_n = √(2 log p / n); for each j keep the l ≠ j with |r_jl| > r_n, at least 1, at most B, ordered by |r| desc; symmetrise (`core/cpp/v3_blocks.h:146-172`).
- **cut_group** flag (reported only): components of the graph {|r_jl| ≥ √(2 log p / n)} that span ≥ 2 blocks (`core/cpp/v3_core.cpp:792-819`, `core/v3_fit.R:141-143`).

## 4. Start tables, start law π₀, start mode (`core/cpp/v3_start.h`)

- **Tables:** for each block b and each sub-model U ⊆ C_b with |U| ≤ K, score U against the full y: log r_b(U) = log m(U) − log m(∅), log r_b(∅) = 0 (`v3_start.h:76-98`).
- **Start (unnormalised):** **γ₀(S) = ϖ(|S|) ∏_b r_b(S ∩ C_b)** (`v3_start.h:68-69`, sum in `comp`, `:54-66`). **π₀ = γ₀ / Z̄₀**, log π₀(S) = log γ₀(S) − log Z̄₀ (`:70`). This is the posterior one would get if the Bayes factor of S factorised over blocks (no between-block interaction), with the exact size prior coupling the blocks.
- **Exact normaliser by DP (size-profile convolution):** e_b(j) = Σ_{|U|=j, U⊆C_b} r_b(U) (`:115-117`); F_b(k) = Σ_j e_b(j) F_{b−1}(k−j), truncated at K (`:121-131`); **Z̄₀ = Σ_{k≤K} ϖ(k) F_J(k)** (`:132-135`). All in log space.
- **Exact iid sampler** (`draw_pi0`, `v3_start.h:153-176`): draw total size k ∝ ϖ(k)F_J(k); then for b = J..1 draw k_b from P(k_b = j | r) = e_b(j)F_{b−1}(r−j)/F_b(r) (`:139-150`); then within each block draw U with |U| = k_b ∝ r_b(U). One uniform per categorical.
- **Discrepancy:** **d(S) = log BF(S) − Σ_b log r_b(S ∩ C_b)**, BF(S) = m(S)/m(∅) (`core/cpp/v3_engine.h:88, :97`). Then log γ₁(S) := log γ₀(S) + d(S) = log ϖ(|S|) + log BF(S) = F(S) − log m(∅), so γ₁ ∝ target.
- **Start mode S̃₀ = argmax π₀** (`start_mode`, `v3_start.h:271-305`): max-plus DP over blocks of per-block per-size maxima of log r_b (`mode_dp`, `:195-226`), maximising log ϖ(k) + M_J(k); size ties → smaller k (strict `>` at `:223`). Among all maximisers (the set E of DP-tight per-block choices) return the lexicographically smallest index set: by explicit enumeration capped at `cap` (`:278-301`); production cap = 10⁶ (`core/cpp/v3_core.cpp:469`). If enumeration hits the cap (`count >= cap`, `:290`) and `tie_dp` (default TRUE, `core/v3_run.R:99`), the tie-aware DP `mode_tie_dp` returns lex-min E without enumerating (`v3_start.h:234-270, :303`). Requires cap ≥ 2 (`:272`). Tie rule kept for reproducibility only (`:187`).
- **Why it exists:** S̃₀ is the centre of LS0 (§7) — a deterministic, data-driven second starting point for local search that does not depend on the SMC particles. π₀ itself exists as (i) the φ = 0 end of the bridge with exactly known normaliser (gives the evidence anchor) and iid initial particles, and (ii) the independence-proposal law inside the MCMC kernel.

## 5. Tempered SMC (`core/cpp/v3_engine.h`)

- **Path (geometric bridge):** **γ_φ(S) = γ₀(S) e^{φ d(S)} = γ₀(S)^{1−φ} γ₁(S)^φ**, φ ∈ [0,1] (`v3_engine.h:14`). φ = 0: π₀; φ = 1: target.
- **One island** (`run_island_s`, `v3_engine.h:274-368`):
  1. N iid draws from π₀ (`:286-292`); log Ẑ initialised to log m(∅) + log Z̄₀ (`:299`).
  2. For each stage t (φ_{t−1} → φ_t): weights w_i = exp{(φ_t − φ_{t−1}) d(S_i)} (`:316-317`); log increment = log((1/N)Σ w_i) (`:318-319`); log Ẑ += increment (`:322`); ESS = (Σw)²/Σw² recorded (`:320-321`); **multinomial resampling at every stage** (no ESS trigger) (`:324-327`; resampler `:234-259`); then **one MCMC round per particle at φ_t** (`:331`).
  3. At φ = 1: L burn-in rounds (`:343-347`), then Hm = 4 measured rounds with Rao–Blackwell recording (`:351-360`; Hm=4 at `core/v3_run.R:90`, `core/v3_calib.R:12`).
  4. Island PIP_rj = Σ o_j / (N·Hm) over particles and measured rounds (`:364`).
  - **Island evidence: log Ẑ_r = log m(∅) + log Z̄₀ + Σ_t log((1/N)Σ_i e^{(φ_t−φ_{t−1}) d(S_i^{(t−1)})})** (comment `:264`, code `:299, :322`).
- **MCMC round** (`one_round`, `v3_engine.h:201-214`): the m = p + B + 2 labelled steps {G_1..G_p, U, N_1..N_B, I} in a fresh uniformly random order (Fisher–Yates, `:195-200`). Each targets γ_φ:
  - **G_j (Gibbs coordinate):** o_j = a/(1+a), a = γ_φ(S∪j)/γ_φ(S∖j); o_j = 0 if adding j would exceed K; include j iff u < o_j (`:111-132`). o_j recorded for RB *before* the draw (`:128`).
  - **U (uniform swap):** j uniform in S, l uniform outside S, MH accept min(1, γ_φ(S′)/γ_φ(S)); self-loop if |S| ∈ {0,p} (`:145-159`).
  - **N_b (neighbour swap, B copies):** j uniform in S, l uniform in N(j)∖S, MH with Hastings ratio |N(j)∖S| / |N(l)∖S′| (`:160-180`).
  - **I (independence):** S′ ~ π₀ exactly, accept min(1, exp{φ[d(S′) − d(S)]}) (`:181-192`).
  - Swaps keep |S|, so the cap is automatic; add moves only via Gibbs, which enforces K.
- **Schedule:** final run and diagnostic islands use a **fixed grid** (`:306-308`); only the calibration pilot is adaptive (§6). ESS is not used to choose φ in the final run; it only feeds the flag `low_empirical_ESS` = any stage ESS < 0.5 N (`core/v3_run.R:201`).
- **N and islands (final):** R = 4 islands (`core/v3_run.R:91`), N = N_e particles each, N₀ = max(2500, n, p), N₁ = 4N₀ (`core/v3_preprocess.R:25, :30`). Final islands use RNG streams 10–13 with fresh π₀ draws (`core/cpp/v3_core.cpp:443-452`).
- **Pooled evidence:** **Ẑ = (1/R) Σ_r Ẑ_r**, via log-sum-exp (`core/v3_run.R:154`); `log_Z_lower95 = log 0.05 + log Ẑ` (Markov, one-sided) (`:155`); `log_Z_rel_m0 = log Ẑ − log m(∅)` (`:156`).
- Score cache: capacity 500p, cleared entirely when full (`core/v3_run.R:92`, `core/cpp/v3_score.h:249-294`); cache hits return identical bits.

## 6. Calibration (`core/v3_calib.R`, `core/cpp/v3_calib.h`) and exact branch

**Exact-branch decision first** (`core/v3_fit.R:105-106, :120-132`): exact iff Σ_{k≤K} C(p,k) ≤ (5H₀ + 4N₀)·p (saturating 128-bit count; `core/cpp/v3_core.cpp:71-85`, `core/v3_preprocess.R:18, :28`).
- **Exact branch** (`v3_enumerate`, `core/v3_exact.R:5-18`; `cpp_enumerate`, `core/cpp/v3_core.cpp:523-568`): scores every |S| ≤ K; exact log Z (streaming log-sum-exp, `:542-547, :557`), exact PIPs (`:559`), HPM under the strict order (§8), top-(40p+1) store, MPM = {j: PIP_j > 0.5} (`core/v3_exact.R:12`), `local_certified = TRUE` iff status `exact` (`:14`), `global_certified` iff F(HPM) − η(HPM) > max_{S≠HPM}[F(S) + η(S)] (`core/cpp/v3_core.cpp:560-563`). No randomness, no calibration, no local search.

**SMC branch calibration** (what is calibrated: the temperature grid and the effort tier; why: so the final run's settings are fixed before its randomness is drawn):
- **Budgets** (`core/v3_preprocess.R:19-33`): ℓ = ⌈log₂(n+p+1)⌉, L = max(4, ⌈log₂(n+1)⌉), N₀ = max(2500,n,p), H₀ = ⌈512 N₀/2500⌉, T₀ = max(1000, ℓ²), tiers e ∈ {0,1} with (N_e, H_e, T_e) = 4^e(N₀,H₀,T₀).
- **Pilot** (`cpp_cal_pilot`, `core/cpp/v3_core.cpp:620-652`): one island of H_e particles, stream 0 (e=0) or 5 (e=1), **adaptive schedule**: next φ′ = largest value with population ESS of e^{(φ′−φ)d} ≥ 0.90·H (try φ′=1 first, else 60 bisections); **floor**: if φ′ − φ < 1/T_e, take φ + 1/T_e and count a "forced step" (`core/cpp/v3_calib.h:25-46`). Then L burn-in + 4 measured rounds, then a local search from the global best (`v3_core.cpp:642`).
- **Candidate set V** (`cpp_cal_V`, `v3_core.cpp:699-724`): {∅} ∪ top-20p models by log γ₀ ∪ top-20p by log γ₁ (≡ F), from all models scored so far (leader stores, `core/cpp/v3_ledger.h:72, :78`).
- **Grid construction on V** (`build_grid`, `core/cpp/v3_calib.h:60-98`): restricted log-normaliser F_V(t) = log Σ_{S∈V} γ₀(S)e^{t d(S)} (`:48-53`); restricted ESS **ρ_V(u,v) = exp{2F_V(v) − F_V(u) − F_V(2v−u)}** (`:54-58`). From u = 0, aim at the next pilot temperature b > u; append b if ρ_V(u,b) ≥ 0.90, else bisect (60 halvings) for the largest v with ρ_V ≥ 0.90; validate; failure if non-progress or > T_e intervals. The grid inserts temperatures where models already scored would make the bridge jump.
- **Rebuild loop** (`core/v3_calib.R:84-119`): up to ℓ iterations: 4 diagnostic islands × H_e on the current grid (streams 1–4 or 6–9, continuing across iterations; `v3_core.cpp:653-698`), local search from the global best, recompute V (now enlarged) and the grid; **converged** iff rebuilt grid identical to previous (`core/v3_calib.R:115`).
- **Triggers** (`core/v3_calib.R:60-61, :101-110, :118`): E1 = some island best < overall best F − 1; E2 = sd(log Ẑ_r over islands) > 1; E3 = the global best F strictly increased in a calibration local search; forced_pilot_steps > 0; grid_failure; grid_unconverged; local_limit.
- **Escalation:** if any trigger fires at tier 0, re-run calibration at tier 1, once only, after a memory preflight recheck (blocked → `resource_limit`) (`core/v3_calib.R:150-159`). The calibration ledger, cache and streams persist across tiers (`v3_core.cpp:571-573`).
- **Grid fallback (v3.1):** if the tier-1 grid fails, freeze the last successful tier-1 construction, else the tier-1 pilot schedule (`core/v3_calib.R:122-125, :163-169`); default on with ls0 (`core/v3_fit.R:151`). Otherwise `schedule_limit` (`core/v3_calib.R:170`). `grid_failure_no_escalation` (`:170`) appears unreachable from `v3_fit` (a grid failure always fires a trigger) — my inference, UNVERIFIED by test.
- **Frozen schedule** (`v3_frozen`, `core/v3_run.R:68-76`; frozen in `core/v3_calib.R:184-190`): grid, tier e, N = N_e, L, inherited models (union of the calibration top-(40p+1) and both leader stores, plus the calibration HPM with provenance; `v3_core.cpp:725-740`), SHA-256 hash. The final run uses the same seed but disjoint streams 10–13 (`core/v3_run.R:8-11`).
- Calibration estimates (pilot/diagnostic Ẑ, PIPs) are archived, never reported (`core/v3_calib.R:52, :96`).

## 7. Local searches (`Engine::local_search`, `core/cpp/v3_engine.h:370-419`)

- **Neighbourhood** of centre C: every feasible single flip (delete any j ∈ C; add any j ∉ C if |C| < K) and every swap (j ∈ C, l ∉ C) (`:394-406`). Best neighbour = largest F, ties by lexicographic order (`:392`).
- **Move rule:** move only on a *strict* F improvement (`:408`); at most `cap` moves; if after `cap` moves a scan still finds a strict improvement → stop with `local_limit = TRUE`, `termination = "move_limit"`, returning that improving neighbour (`:409-411`). Otherwise `termination = "no_improvement"`, `local_certified = TRUE`, returned = current centre (`:413-414`).
- **Every scanned model is scored into the ledger** (can become HPM even without a move) (`:375, :391`).
- **ℓ (threshold/cap):** ℓ = ⌈log₂(n+p+1)⌉ (`core/v3_preprocess.R:23`); also the max number of calibration rebuilds.
- **Final local search:** from the global HPM after the 4 final islands, cap ℓ (`core/cpp/v3_core.cpp:453-458`).
- **LS0 (v3.1, default on):** after the final local search on a completed run, a local search from the start mode S̃₀ (`start_mode(st, 1e6, tie_dp)`), same rules, same ledger/cache, centre scored, phase `ls0`, no random numbers (`core/cpp/v3_core.cpp:460-481`). **Cap = ℓ + |S̃₀|** by default ("ell_n_plus_mode"); option `v3.ls0_cap = "ell_n"` gives cap ℓ (`v3_core.cpp:403-404, :473-475`; `core/v3_run.R:100-101`). An LS0 guard stop or numerical failure leaves the run without output (`v3_core.cpp:463-464`).
- **`local_certified` (reported):** TRUE iff the reported HPM equals the `returned` model of a search that ended with `no_improvement` — final search or LS0 (`core/v3_run.R:179, :192-195`; `local_certified_by` ∈ {final, ls0, both, none}). Meaning: the HPM is a local maximum of F over all single add/delete/swap neighbours (adds respecting K). An equal-F tie change of the HPM breaks certification (`:178`). `global_certified` is always FALSE in the SMC branch (`:180`).
- Calibration local searches (pilot and each diagnostic iteration) use the same routine with cap ℓ (`v3_core.cpp:642, :689`).

## 8. Pooling and outputs (`core/v3_run.R:119-220`, `core/v3_fit.R`)

- **pip_primary:** equal-weight mean over the 4 islands of the island RB PIPs (`core/v3_run.R:159-162`); each island PIP is the mean of the Gibbs conditional inclusion probabilities o_j over N particles × 4 measured rounds at φ = 1 (`core/cpp/v3_engine.h:128, :364`). Yes, Rao–Blackwellised; yes, equal island weights. **DOC≠CODE:** the Ẑ-weighted "secondary" PIP in `METHODOLOGY_v3.md:272-274` is not computed (removed, `core/README.md:16`).
- **MPM** = {j : pip_primary_j > 0.5} (strict) (`core/v3_run.R:163`); may exceed K (not capped).
- **HPM** = best F under strict order: larger F; exact tie → smaller |S|; then lexicographically smaller (`core/cpp/v3_util.h:120-126`), over **every model scored in the final run's ledger**: all block-table sub-models (`ingest_tables`, `core/cpp/v3_core.cpp:372-387, :408`), inherited calibration models (`:418-442`), all final-island particles and proposals (init, Gibbs flips, swaps, independence), the final local search, and LS0 (`core/cpp/v3_ledger.h:82-113`). Reported with `hpm_F` and provenance (`core/v3_run.R:142`). Near ties: stored models within 1e-9 nat of hpm_F (`:170-173`).
- **log_Z** = log Ẑ (§5), plus `log_Z_r`, `log_Z_lower95`, `log_Z_rel_m0`, `log_Z_r_rel_m0`, `pip_r` (`core/v3_run.R:150-163`).
- **Final checks (reported only, do not change outputs):** E1 any island best < hpm_F − 1; E2 sd(log Ẑ_r) > 1; E3 strict F increase during the final local search (LS0 excluded); low_empirical_ESS; `checks_passed_final` (`core/v3_run.R:181-205`).
- **When there is no output:** `estimates_available = FALSE` and all of `log_Z, log_Z_r, log_Z_lower95, log_Z_rel_m0, log_Z_r_rel_m0, pip_primary, pip_r, mpm` set to NA by exact name (`core/v3_run.R:109-114`; applied in `core/v3_fit.R:85`). Statuses: `invalid_input`, `no_predictors`, `y_constant` (hpm = ∅), `resource_limit` (memory preflight, `core/v3_fit.R:26-68, :117`; or runtime guard: elapsed + last operation > allocated hours, checked after every bridge stage, grid construction, local search, LS0; `core/cpp/v3_runtime.h:13-27`), `numerical_failure` (all three score routes failed), `schedule_limit`. On stops the best model scored so far is returned as `hpm` with `hpm_incomplete = TRUE` (`core/v3_fit.R:134-137, :154-159`; `core/v3_run.R:143-148`). Defaults: mem 8 GB, 24 h (`core/v3_fit.R:73, :92`).
- **Reported model:** the code reports both `hpm` and `mpm` with no single "selected" model field; the README lists `hpm` and `mpm` as supports (`core/README.md:11`). Which is "the reported model" in the paper is a presentation choice — UNVERIFIED in code.
- Completed status strings: `completed` (SMC; `core/cpp/v3_core.cpp:413`) and `exact` (exact branch).

## 9. Pipeline sketch

```
(X, y, seed, allocation)
  │
  ▼ PREPROCESS  [core/v3_preprocess.R:97]   drop exactly-constant columns; standardise X, y (centre, SD n-1)
  │   out: X (n×p), y, kept/dropped; statuses invalid_input/no_predictors/y_constant
  ▼ BUDGETS     [core/v3_preprocess.R:19]   K, B, ell, L, N0, H0, T0, tiers; exact-branch test
  ▼ PREFLIGHT   [core/v3_fit.R:26]          memory (and exact-branch time) → resource_limit?
  ├──── exact branch ──► ENUMERATE all |S|≤K [v3_core.cpp:524] → log Z, PIP, HPM, MPM, certificates. END
  ▼ SETUP       [core/v3_setup.R:67]        blocks C_1..C_J (≤B); tables r_b(U); π0, Z̄0 (DP); neighbour graph
  │   out: γ0, exact π0 sampler, d(S) = log BF(S) − Σ log r_b
  ▼ CALIBRATE   [core/v3_calib.R:144]       tier 0: pilot (adaptive φ, H0 particles) + LS
  │                                         → V → grid (ρ_V ≥ 0.9) → ≤ ell × {4 diag islands + LS + rebuild}
  │                                         triggers? → tier 1 once (×4 effort)
  │   out: frozen {grid, tier, N_e, L, inherited models}
  ▼ FINAL RUN   [v3_core.cpp:391]           4 islands × N_e: π0 draws → per stage reweight/resample/1 round
  │                                         → L burn-in → 4 measured rounds (RB PIP)
  │   out: Ẑ_r, PIP_r, ledger (HPM over all scored models incl. tables + inherited)
  ▼ FINAL LOCAL SEARCH from HPM, cap ell     [v3_core.cpp:456]
  ▼ LS0 from start mode S̃0 = argmax π0, cap ell+|S̃0|  [v3_core.cpp:465-481]
  ▼ ASSEMBLE    [core/v3_run.R:119]         log Ẑ = log mean Ẑ_r; pip_primary = mean PIP_r; MPM (>½);
                                            HPM, local_certified, flags E1–E3, lowESS
```

## 10. Hard-coded constants

| Constant | Value | Pin |
|---|---|---|
| a₀, b₀ (IG prior on σ²) | 0.01, 0.01 | `core/cpp/v3_score.h:14` |
| g (via H = (n+1)G+I), ridge | g = n, unit ridge I | `core/cpp/v3_score.h:175-183` |
| Model prior | BB(1,p): w(k)=½/C(2p−1,k), truncated at K | `core/cpp/v3_score.h:61-70` |
| Size cap K | min(p, ⌊n/2⌋) | `core/cpp/v3_score.h:40`; `core/v3_preprocess.R:21` |
| Block size B | min(⌊√n⌋, ⌊√p⌋, 16) | `core/v3_preprocess.R:22`; `core/cpp/v3_core.cpp:145` |
| ℓ (LS cap, max rebuilds) | ⌈log₂(n+p+1)⌉ | `core/v3_preprocess.R:23` |
| L (burn-in rounds) | max(4, ⌈log₂(n+1)⌉) | `core/v3_preprocess.R:24` |
| Measured rounds Hm | 4 | `core/v3_run.R:90`; `core/v3_calib.R:12` |
| N₀ (final particles/island) | max(2500, n, p) | `core/v3_preprocess.R:25` |
| H₀ (calibration particles) | ⌈512 N₀ / 2500⌉ | `core/v3_preprocess.R:26` |
| T₀ (stage ceiling) | max(1000, ℓ²) | `core/v3_preprocess.R:27` |
| Tier multiplier | 4^e, e ∈ {0,1}, ≤ 1 escalation | `core/v3_preprocess.R:30`; `core/v3_calib.R:158` |
| Islands R | 4 | `core/v3_run.R:91`; `core/v3_preprocess.R:29`; `core/cpp/v3_core.cpp:664` |
| Pilot ESS threshold | 0.90·H | `core/cpp/v3_calib.h:31` |
| Pilot step floor | 1/T_e | `core/cpp/v3_calib.h:38-43` |
| Grid ρ_V threshold | 0.90 | `core/cpp/v3_calib.h:79, 84, 92` |
| Bisection halvings | 60 | `core/cpp/v3_calib.h:34, 82` |
| Snap-to-1 tolerance | 1e-12 | `core/cpp/v3_calib.h:42, 89` |
| Q recompute threshold | Q < 1e-8·yᵀy | `core/cpp/v3_score.h:219` |
| Exact-branch threshold | Σ_{k≤K}C(p,k) ≤ (5H₀+4N₀)p | `core/cpp/v3_core.cpp:75-84` |
| Score cache capacity | 500p (clear when full) | `core/v3_run.R:92`; `core/v3_calib.R:147` |
| Top store / leader stores | 40p+1 by F; 20p by log γ₀; 20p by log γ₁ | `core/cpp/v3_ledger.h:78` |
| V snapshot (archive only) | all if p ≤ 25 or |V| ≤ 1e4, else top 1e4 | `core/v3_calib.R:17-21` |
| Near-tie window | 1e-9 nat | `core/v3_run.R:171`; `core/v3_exact.R:7` |
| E1 / E2 thresholds | 1 nat / sd > 1 | `core/v3_run.R:182-183`; `core/v3_calib.R:101-102` |
| low_empirical_ESS | ESS < 0.5 N | `core/v3_run.R:201` |
| MPM threshold | PIP > 0.5 | `core/v3_run.R:163`; `core/v3_exact.R:12` |
| Markov lower bound | 0.05·Ẑ | `core/v3_run.R:155`; `core/v3_fit.R:126` |
| Start-mode enumeration cap | 10⁶ | `core/cpp/v3_core.cpp:469`; `core/cpp/v3_start.h:271` |
| LS0 cap | ℓ + |S̃₀| (option: ℓ) | `core/cpp/v3_core.cpp:473`; `core/v3_run.R:101` |
| Duplicate threshold | |r| ≥ 1 − 1e-10 | `core/cpp/v3_core.cpp:754` |
| Neighbour / cut_group threshold | √(2 log p / n); neighbours ≤ B, ≥ 1 | `core/cpp/v3_blocks.h:154, 167`; `core/cpp/v3_core.cpp:802` |
| Score error bound factor | 64·eps | `core/cpp/v3_score.h:244` |
| Allocation defaults | 8 GB, 24 h | `core/v3_fit.R:73, 92` |
| RNG | xoshiro256**, seeded by SplitMix64 of (seed≪32)+stream; streams 0–13 | `core/cpp/v3_util.h:36-61`; `core/v3_run.R:8-11` |
