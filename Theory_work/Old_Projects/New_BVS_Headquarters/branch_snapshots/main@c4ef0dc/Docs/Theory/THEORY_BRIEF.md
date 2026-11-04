# THEORY_BRIEF.md: dossier for the theoretical architecture of SMC-BVS v3

**Written by the lead (Fable 5.1, high), 2026-10-19, under `C:\Users\felip\.claude\protocols\theory.md`.**
**Methodology version:** `C:\Users\felip\OneDrive\Documents\Local_to_global_Bayesian\01_Methodology_and_Theory\Methodology\SMC_BVS_v3_20261019\METHODOLOGY_v3.md`, v3.0 of 2026-10-19, SHA-256 `93043758058a6d422cca6ca4b6be8f3a9e8149b6f6de2e1bab1ce31c44b8019c` (verified by the lead on 2026-10-19). Every theorem of this run is about that exact document. Where this dossier and the methodology differ, the methodology governs; report the difference.

**Status of everything here:** the method is designed, not implemented, not verified; nothing about it is proved. The "existing project theory" cited below is AI-proved and AI-reviewed but **not adopted** by Felipe, and was written for the 14 October target with unstandardised y and column norm n. It is a resource, not a foundation: every statement that reuses it must say what transfer it needs.

**Fixed by Felipe (not to be changed by any theorem):** the target (standardised X and y; β_S ~ N(0, nσ²(G_S + I)⁻¹); σ² ~ IG(0.01, 0.01); BB(1, p) capped at K = min(p, ⌊n/2⌋)); the HPM decision; block size B = min(⌊√n⌋, ⌊√p⌋, 16); neighbour threshold √(2 log p / n); no secondary prior arm. If a theorem would need a change to the method, record it as a **recommendation** with its reason; never adopt it.

---

## 0. What Felipe wants to know

Bayesian variable selection in linear regression, mainly p > n (study sizes n = 200, p ∈ {500, 1000}), by a method that must run on any (X, y) with every choice made in advance. Four areas:

1. **The target posterior:** consistency and contraction (support recovery, PIPs, prediction, coefficients, variance), and the sharp limits (what signal strength is needed, what size-only priors cannot do).
2. **Monte Carlo validity and rates of the SMC estimates** (evidence Z, PIPs, HPM discovery) for fixed data.
3. **Combined guarantees for the algorithm's actual output with polynomial compute**, under the declared budgets.
4. **The limits:** what cannot be guaranteed, and what the checks do and do not certify.

Organisational model: Song and Liang (2015), JRSSB 77(5), 947–972, https://academic.oup.com/jrsssb/article/77/5/947/7040600 (local copy `C:\Users\felip\OneDrive\Documents\Local_to_global_Bayesian\03_Literature\4_References\Song and Liang (2015) A split-and-merge Bayesian variable selection.pdf`). They prove **target** results (Theorems 1–2 Hellinger contraction via Jiang's sieve; Corollary 1 rates; Theorem 3 sure screening of PIPs; Theorem 4 and Corollary 2 concentration of a misspecified subset on its KL projection; Theorem S in the supplement, MAP consistency) and treat the **sampler** separately, by citing SAMC convergence; the consistency of the whole procedure is asserted by composition (§3.1, "Clearly, it follows…"). The same separation (target theory; sampler theory; then composition, made rigorous where possible) is the template here, with our tempering bridge in place of their split-and-merge.

---

## 1. Settings and asymptotic regimes

Notation: [p] = {1, …, p}; a model is S ⊆ [p], k = |S|; X_S the n × k submatrix; P_S the orthogonal projection on its column span.

- **R1 (main statistical regime).** n → ∞ along a sequence of fixed designs X = X_n; s₀ = |S₀| fixed; p = p_n ≤ n^A for some A ≥ 1 (polynomial). Felipe's study sizes (n = 200, p = 500, 1000) sit at A ≈ 1.2–1.3.
- **R2 (fixed p).** p, the partition, β*, σ*² fixed; n → ∞. Isolates mechanisms (start limit, switch gaps, burn-in). Caveat: for fixed p the method eventually enumerates exactly (§2.5), so R2 statements about the SMC branch are component theorems, not production guarantees.
- **R3 (fixed data, Monte Carlo).** (X, y) fixed; the budget grows. The method's budgets are fixed functions of (n, p) with a two-tier family (N_e, H_e, T_e) = 4^e(N₀, H₀, T₀), e ∈ {0, 1}. A "N → ∞" statement must therefore be about an explicitly defined family: the cleanest is **conditional on the calibration output** (the frozen grid, stage count T, L, and tier), letting the final-run particle count N → ∞ with everything else frozen; unconditional statements average over the random calibration.
- **R4 (production).** The actual algorithm with its actual budgets, as n → ∞ in R1: N_e = 4^e max(2500, n, p), H_e = 4^e⌈512N₀/2500⌉, T_e = 4^e max(1000, ℓ²), L = max(4, ⌈log₂(n + 1)⌉), ℓ = ⌈log₂(n + p + 1)⌉, 4 islands. Combined guarantees (area 3) are statements in R4.

---

## 2. The method in exact mathematical form

### 2.1 Preprocessing and the working data

Raw input X^r ∈ ℝ^{n×p}, y^r ∈ ℝⁿ, a seed, a resource allocation. Stop with `invalid_input` if any entry is non-finite or n < 3 or p < 1. Columns with all entries exactly equal are dropped (never selected); p := number kept; p = 0 gives `no_predictors`. If y^r is constant: Ŝ = ∅, status `y_constant`.

Standardisation (C = I − 11ᵀ/n): each column is centred and divided by its sample SD with denominator n − 1, so **‖x_j‖² = n − 1** and 1ᵀx_j = 0; likewise y = Cy^r/s_y with s_y² = ‖Cy^r‖²/(n − 1), so **‖y‖² = n − 1**, 1ᵀy = 0. Write D_x = diag(column SDs of CX^r). Then X = CX^rD_x⁻¹.

Consequences: the target is invariant to affine maps of y^r (a ≠ 0) and of each column, and to column permutation up to index-based tie-breaks. **G_S := X_SᵀX_S = (n − 1)R_S**, where R_S is the sample correlation matrix of the columns in S; z_S := X_Sᵀy; r_jl := x_jᵀx_l/(n − 1) is the sample correlation. Connected components of {|r_jl| ≥ 1 − 10⁻¹⁰} are reported (duplicates are kept; they are unidentifiable).

### 2.2 Target posterior (fixed by Felipe)

For S with k = |S| ≤ K, K = min(p, ⌊n/2⌋):

```
y | β_S, σ², S ~ N_n(X_S β_S, σ² I_n)                        (no intercept; y is centred)
β_S | σ², S    ~ N_k(0, n σ² (G_S + I_k)⁻¹)                   (g = n, unit ridge τ = 1)
σ²             ~ IG(a₀, b₀),  a₀ = b₀ = 0.01   (density ∝ v^{−a₀−1} e^{−b₀/v})
ϖ(S)           = w(k) 1{k ≤ K} / W_K,  w(k) = B(1+k, 2p−k)/B(1, p) = ½ / C(2p−1, k),  W_K = Σ_{j≤K} C(p, j) w(j)

H_S = (n + 1) G_S + I_k,   D_S = det H_S / det(G_S + I_k),   t_S = n z_Sᵀ H_S⁻¹ z_S,   Q_S = yᵀy − t_S,   ν = a₀ + n/2
m(S) = C_n D_S^{−1/2} (2b₀ + Q_S)^{−ν},   C_n = (2b₀)^{a₀} Γ(ν) / (π^{n/2} Γ(a₀))
π(S | y) = ϖ(S) m(S) / Z,   Z = Σ_{|S|≤K} ϖ(S) m(S),   BF(S) = m(S)/m(∅),   F(S) := log ϖ(S) + log m(S)
```

Facts (elementary, from the formulas): the eigenvalues of nX_SH_S⁻¹X_Sᵀ are nλ/((n+1)λ+1) < n/(n+1) for λ an eigenvalue of G_S, so 0 ≤ t_S ≤ (n/(n+1))‖P_Sy‖² and **Q_S ≥ yᵀy/(n+1) = (n−1)/(n+1)**; 1 ≤ D_S ≤ (n+1)^k; w(k+1)/w(k) = (k+1)/(2p−k−1) (each extra variable costs log((2p−k−1)/(k+1)) nats); W_K ≥ w(0) = ½ (so capping at most doubles retained atoms); the size-class ratio P(|S| = k+1)/P(|S| = k) = (p−k)/(2p−k−1) ≤ ½ for k ≥ 1 (geometric size tail; this is why the Castillo–Schmidt-Hieber–van der Vaart and Yang–Wainwright–Jordan prior templates do not apply, see §3).

Joint posterior (needed for contraction statements): S ~ π; σ² | S, y ~ IG(ν, (2b₀ + Q_S)/2); β_S | σ², S, y ~ N_k(nH_S⁻¹z_S, nσ²H_S⁻¹).

**Decisions and reported quantities.** PIP_j = π({S : j ∈ S}); MPM = {j : PIP_j > ½} (may exceed K; reported as computed); the **HPM** is the strict maximiser of F(S) over models **ever scored** (§2.12), ties (exact equality only) broken by smallest |S| then lexicographically smallest index set; the evidence Z of the working model (not a raw-data marginal likelihood).

### 2.3 Reduction statement (consensus of the three consultants; to be proved; V1)

Let U ∈ ℝ^{n×(n−1)} have orthonormal columns with UUᵀ = C. With θ = s_yβ and v = s_y²σ², the posterior of §2.2 is exactly the posterior of the regression of Uᵀy^r on UᵀX (n − 1 rows; if y^r = α*1 + X^rβ* + ε with ε ~ N(0, σ*²I), then Uᵀε ~ N(0, σ*²I_{n−1}) exactly and the intercept is removed exactly), with slab θ_S | v, S ~ N(0, nv(G_S + I)⁻¹) and **v ~ IG(a₀ + ½, b₀s_y²)**, since (a₀ + ½) + (n−1)/2 = a₀ + n/2. Hence the exponent ν = a₀ + n/2 is the integrated-intercept model, g = n = (n − 1) + 1, and the response scale enters only through the data-dependent IG rate b₀s_y². The old project proofs cannot be applied directly: T6's identity E₀[m(S)/f₀(y)] = 1 fails for standardised y (y lies on a sphere in a contrast subspace), and all results need uniformity over the IG rate in a compact set (s_y² ∈ [c, C] with probability → 1 under bounded signal and fixed noise) and the shift (n−1)+1 in g. **Independence of s_y and ε is false and must not be assumed.**

### 2.4 Data-generating model for statistical statements

y^r = α*1 + X^rβ* + ε, ε ~ N_n(0, σ*²I_n), design fixed; S₀ = supp(β*), s₀ = |S₀|; μ := CX^rβ* = Xθ* with θ* = D_xβ* (the signal on the standardised-column scale; μ is centred). Probabilities P₀ are over ε. The working-scale truth (θ*/s_y, σ*²/s_y²) is random; statements about S are parametrisation-free; statements about coefficients must say which scale (working, θ = D_xβ, or raw β). Expected standing assumptions (consultant consensus, **to be examined, not imposed**): fixed s₀; p ≤ n^A; bounded centred signal energy ‖μ‖²/n ≤ M; σ*² > 0 fixed; sparse eigenvalues λ_min(R_T) ≥ φ₀² for |T| ≤ m_n + s₀ with m_n = ⌈(s₀ log(2p) + (s₀+1)(log n)/2 + ω_n)/log 2⌉; beta-min min_{j∈S₀} θ*_j² ≥ M_nσ*² log n/(nφ₀²), M_n → ∞ (sharp at the log n scale in orthogonal designs by the project's Pb1); for start-side results a cluster-separation (CS) and a no-leakage (NL) condition. Not covered by any planned result: growing s₀, duplicated predictors, signals below the beta-min scale (only screening), non-Gaussian errors.

### 2.5 Exact branch

If E := Σ_{k≤K} C(p, k) ≤ (5H₀ + 4N₀)·p (12,560p at baseline; saturating integer arithmetic), every model with |S| ≤ K is scored in a streaming pass: running best (strict order of §2.12), log-sum-exp accumulation of Z and of the PIP numerators. Status `exact`, `global_certified` when all comparisons are numerically validated. Covers p ≤ 17 for n ≥ 22, more when the cap binds. Since N₀ ≥ n, every fixed-p problem is eventually enumerated as n → ∞ (at very large n for p ≥ 25). **On the exact branch, every target theorem is a theorem about the output.**

### 2.6 Blocks, tables, composite start, discrepancy, bridge

- **B = min(⌊√n⌋, ⌊√p⌋, 16)** (= 14 at the study sizes; = 16 whenever n, p ≥ 289, so B is eventually fixed in R1).
- **Clustering:** complete linkage on the distance 1 − |r_jl|; ties between candidate merges broken lexicographically on the sorted original-index lists. **Cut:** top-down from the root; any node with more than B members is split into its two children (smallest index first) until every retained cluster has ≤ B members. **Packing:** next-fit in dendrogram leaf order, whole clusters only, into blocks C₁, …, C_J with |C_b| ≤ B; J ≥ ⌈p/B⌉. The partition is a deterministic function of X alone.
- **Tables:** for each block, every U ⊆ C_b is scored against the full y: r_b(U) = m(U)/m(∅) = BF(U). Since B ≤ K for n ≥ 3, no sub-model exceeds the cap. **Every table score counts for the HPM.** Cost Σ_b 2^{|C_b|} ≤ p2^B/B scores.
- **Start:** γ₀(S) = ϖ(S) ∏_b r_b(S ∩ C_b) for |S| ≤ K, π₀ = γ₀/Z̄₀, Z̄₀ = Σ_S γ₀(S), computed **exactly** by convolving the block size profiles e_b(j) = Σ_{|U|=j} r_b(U) with the size prior (valid because ϖ depends on S only through |S|). **Exact iid draws:** draw the total size ∝ w(k)c_k, then block sizes backwards, then each block's sub-model within its size class (project P1, proved for arbitrary positive tables and any size-only prior with a cap; applies verbatim). π₀ is a size-coupled product, not a product of block posteriors.
- **Discrepancy and bridge:** d(S) = log BF(S) − Σ_b log r_b(S ∩ C_b); γ_φ(S) = γ₀(S)e^{φd(S)}, q_φ = γ_φ/Z̄_φ, φ ∈ [0, 1]; q₀ = π₀, q₁ = π, **Z = m(∅)Z̄₁**. The bridge is defined for all real φ (over-tempered range φ > 1 is used by the restricted-ESS evaluation, §2.10).

### 2.7 Neighbour graph

r_n = √(2 log p / n). For each j: partners l ≠ j with |r_jl| > r_n, always including j's single largest-|r| partner, keeping at most the B largest (ties by original index); then the symmetric union N(j) (l ∈ N(j) ⇔ j ∈ N(l); degrees may exceed B). No edges when p = 1. A deterministic function of X.

### 2.8 The move round at temperature φ (the kernel K_φ)

A round is the list of m = p + B + 2 labelled elementary steps, applied in a **uniformly random order drawn independently of the particle's state, afresh for every particle and every round**:

- **Gibbs coordinate j** (p steps): draw j's inclusion from its exact conditional under γ_φ given S \ {j}, with addition at |S| = K excluded (probability 0 of adding when |S| = K and j ∉ S). The conditional inclusion probability o_j is recorded immediately before the draw.
- **Uniform swap** (1 step): self-loop if |S| ∈ {0, p}; delete j uniformly from S, add l uniformly from [p] \ S; accept with 1 ∧ γ_φ(S′)/γ_φ(S).
- **Neighbour swap** (B steps): self-loop if S = ∅; delete j uniformly from S; if N(j) \ S = ∅ reject; else add l uniformly from N(j) \ S; accept with 1 ∧ [γ_φ(S′)/γ_φ(S)]·|N(j) \ S| / |N(l) \ S′| (read as 0 if j ∉ N(l)).
- **Independence proposal** (1 step): S′ ~ π₀ (exact iid draw, independent of S), accepted with 1 ∧ e^{φ[d(S′) − d(S)]}. **Every proposal is scored, accepted or not.**

Each step is reversible w.r.t. q_φ (project P6, verbatim; the independence step is a standard independence Metropolis–Hastings move with proposal π₀ and target q_φ ∝ π₀e^{φd}). The round kernel K_φ = (1/m!) Σ_σ K_{σ(1)}⋯K_{σ(m)} is a mixture over orders; since the adjoint of K_{σ(1)}⋯K_{σ(m)} is the reversed composition and the uniform law on orders is reversal-invariant, **K_φ is self-adjoint on L²(q_φ)** (checked by the three consultants; a realised order is not reversible). The exact Gibbs conditional and the Hastings ratios are explicit from §2.2 (V5).

**Lead's observation (a fact about the kernel; wording corrected after council round 1).** Three events must be kept apart: a model in 𝓜 being *scored* during a round, a particle *visiting* 𝓜 during a round, and a particle *occupying* 𝓜 at the end of the round. (a) Scoring: every round scores exactly one fresh iid π₀ draw per particle (the independence proposal), accepted or not; this is exact and is the basis of the discovery count in §2.13. (b) Visiting: the independence step alone moves the particle into 𝓜 with probability Σ_{S′∈𝓜} π₀(S′)(1 ∧ e^{φ[d(S′)−d(S)]}), so the elementary independence kernel satisfies the minorisation K_ind(S, ·) ≥ ε_φ q_φ(·) with ε_φ = inf_U π₀(U)/q_φ(U) > 0 (a fact about the whole round too, since the surrounding invariant steps preserve a minorisation; ε_φ may be exponentially small). (c) Occupying at the end of the round: later steps in the realised order can undo an entrance, so no end-of-round bound of the form "≥ π₀(𝓜)·acceptance" follows from (b); but the Doeblin minorisation does pass to the whole round: for any realised order with the independence step at position i, K_{σ(1)}⋯K_{σ(m)} ≥ K_{σ(1)}⋯K_{σ(i−1)}·ε_φ q_φ·K_{σ(i+1)}⋯K_{σ(m)} = ε_φ q_φ, because the later steps are q_φ-invariant and the earlier ones are stochastic; hence K_φ(S, ·) ≥ ε_φ q_φ(·) for every S (established independently by Fable-C1, Astra-C1 and Astra-C2 in council round 1), so K_φ is uniformly ergodic with constant ε_φ, which may be e^{−Θ(n)}. Consequently **v3's kernels are never non-crossing**: project T5's non-crossing hypotheses (i)–(iv) fail, and only its leaky form (v) applies, now with every scoring mechanism (initial draws, independence proposals, Gibbs and swap proposals, tables, local-search scans) counted as a hazard. T5's negative message survives only when all these hazards are small, not merely when π₀(𝓜) is exponentially small.

### 2.9 Resampling, pilot and the empirical-ESS schedule

- **Resampling:** fresh **multinomial** resampling after every reweighting, including the terminal stage (so the particles are equally weighted at every stage, and after the last stage).
- **Pilot** (calibration, tier e): H_e particles iid from π₀; at each stage the next temperature is the largest φ′ ∈ (φ, 1] with the ESS of the weights e^{(φ′−φ)d(S_i)} computed over the H_e pilot particles (METHODOLOGY §6.6 calls this the "population ESS", meaning the particle population; it is the empirical ESS, (Σw_i)²/Σw_i², not the exact population quantity 1/(1 + χ²)) at least 0.90·H_e (weight CV² ≤ 1/9), found by 60 bisection halvings; **exploratory floor** φ′ − φ ≥ 1/T_e (a forced step is counted as `forced_pilot_steps`, a trigger); ends exactly at φ = 1; then L burn-in rounds, 4 measured rounds, a local search (§2.12). The pilot schedule is a function of (y, X, pilot randomness).

### 2.10 Candidate set, restricted ESS, candidate grid, rebuild loop

- **V:** the union of the top 20p scored models by log γ₀, the top 20p scored models by log γ₁ = F (the target), and ∅; deduplicated; list ties lexicographic; frozen during each construction; |V| ≤ 40p + 1.
- **Restricted log-normaliser** F_V(t) = log Σ_{S∈V} γ₀(S)e^{td(S)}; **restricted ESS fraction** between u < v: ρ_V(u, v) = exp{2F_V(v) − F_V(u) − F_V(2v − u)} = 1/(1 + χ²(q_v(·|V) ‖ q_u(·|V))), evaluating F_V at 2v − u > 1 as a finite sum (not a production temperature).
- **Construction:** start at u = 0 with the pilot temperatures as targets. For the next pilot temperature b: if ρ_V(u, b) ≥ 0.90 append b; else bisect on (u, b] with u fixed, ≤ 60 halvings, append the largest tested endpoint that passes; continue from the appended point. Validate strict numerical progress and the inequality at every appended point. Non-progress, failed validation, or more than T_e intervals ⇒ construction fails. Note the grid refines the pilot schedule: it never removes a pilot temperature.
- **Rebuild loop:** after each set of 4 diagnostic islands (H_e particles each, run on the current grid with L burn-in and 4 measured rounds and a local search), update V and rebuild; stop when the rebuilt grid equals the previous one; at most ℓ iterations; otherwise flag `grid_unconverged` (a trigger). A failed construction triggers escalation at tier 0 and status `schedule_limit` at tier 1 (best scored model returned; Z and PIPs unavailable).
- **What the grid controls and does not:** restricted one-step weight dispersion among models already scored; not full-space ESS, occupancy, mixing, or modes never scored.

### 2.11 Calibration, triggers, escalation, the tier family

Calibration at tier e uses streams 0 and 1–4 (tier 0) or 5 and 6–9 (tier 1): pilot → candidate set and preliminary grid → ≤ ℓ rebuild iterations with 4 diagnostic islands each → checks. **Triggers** (any one ⇒ at most one escalation to tier 1, decided before any final randomness): E1 some diagnostic island's best score more than 1 nat below the overall best; E2 SD of the 4 diagnostic log Ẑ > 1 nat; E3 a local search improved the best; forced pilot steps; `grid_unconverged`; failed grid construction; `local_limit`. Score leaders are kept across tiers. After calibration, the grid, the budgets N_e and all V-independent settings are **frozen**.

### 2.12 Final run and the reported estimators

- **Final:** 4 islands (streams 10–13, independent of all calibration randomness) × N_e particles, fresh iid π₀ draws, the frozen grid (stages φ₀ = 0 < φ₁ < … < φ_T = 1), multinomial resampling after every reweighting, **one move round per stage**, then L burn-in rounds and 4 measured rounds at φ = 1, then a local search. No forced steps. Final observations never revise the schedule and never select replacement estimates; E1–E3 and the empirical-ESS check (any final stage below 0.5N ⇒ `low_empirical_ESS`) are recomputed as **flags only**.
- **Evidence:** per island Ẑ_r = m(∅)Z̄₀ ∏_{t=1}^{T} (1/N_e)Σ_i exp{(φ_t − φ_{t−1})d(S_i^{(t−1)})} (with W_K inside γ₀ exactly once); pooled Ẑ = ¼Σ_r Ẑ_r (log-sum-exp); reported 95% lower bound 0.05·Ẑ (Markov, one-sided). Given the frozen calibration, each Ẑ_r is unbiased for Z (project P6, P7); log Ẑ is not.
- **PIPs:** in the 4 measured final rounds, average the recorded o_j (Rao–Blackwellisation) over particles and rounds within each island. **Primary:** equal-weight mean over the 4 islands. **Secondary:** Σ_r Ẑ_r PIP̂_{rj} / Σ_r Ẑ_r. MPM = {j : primary PIP̂_j > ½}.
- **HPM:** strict maximum of F over **every model ever scored**: tables, pilot, calibration, final rounds, rejected and accepted proposals (swaps, independence), local searches; kept as a running best that survives cache eviction. Tie rule: exact equality only, then smallest |S|, then lexicographic. A near-tie list (within 10⁻⁹ nat of the best, from the stored top 40p + 1) is informational and never reorders. Provenance (which phase first scored the HPM) is reported.
- **Local search** (after the pilot, after each diagnostic island, after the final run): from the current best scored model (the centre), scan every feasible single flip and swap (additions beyond K excluded) with the centre frozen during the scan; move to the best strict improvement (lexicographic ties); at most ℓ moves, then one further scan; stop earlier when a scan finds no improvement. Every evaluated model updates the global best. `local_limit` if the last scan still improves; `local_certified` only when the returned model is a scanned centre with no improving neighbour. The search never alters particles. It is deterministic given the centre: a best-improvement ascent on F with cap ℓ.

### 2.13 Budgets as functions of (n, p), and the count of iid π₀ draws

| Symbol | Rule | n = 200, p = 500 | p = 1000 |
|---|---|---|---|
| K | min(p, ⌊n/2⌋) | 100 | 100 |
| B | min(⌊√n⌋, ⌊√p⌋, 16) | 14 | 14 |
| ℓ | ⌈log₂(n + p + 1)⌉ | 10 | 11 |
| L | max(4, ⌈log₂(n + 1)⌉) | 8 | 8 |
| N₀ | max(2500, n, p) | 2500 | 2500 |
| H₀ | ⌈512N₀/2500⌉ | 512 | 512 |
| T₀ | max(1000, ℓ²) | 1000 | 1000 |
| R | 4 islands | 4 | 4 |
| tier e | (N_e, H_e, T_e) = 4^e(N₀, H₀, T₀), e ∈ {0, 1} | | |

**Lead's count (a fact; corrected after council round 1).** Each particle, at every round (T bridge stages + L burn-in + 4 measured), draws one exact iid π₀ proposal, and every particle starts from an iid π₀ draw. All these draws are iid from π₀ and independent of the particle states, and every one is scored. Conditional on the calibration output 𝓒 (which fixes T, L, N_e before any final randomness), the final run scores **Q_final = 4N_e(1 + T + L + 4)** iid π₀ draws, so for any model S* fixed given 𝓒, P(S* never scored in the final run | 𝓒) ≤ (1 − π₀(S*))^{Q_final}, **regardless of acceptance, mixing or resampling**. The calibration's own draw count is adaptive (the rebuild loop and the escalation decision depend on what was scored), so it must not be inserted as a fixed exponent; an unconditional bound is E[(1 − π₀(S*))^{Q_final}], and a deterministic lower bound on Q_final uses T ≥ 1: Q_final ≥ 4N_e(L + 6) = Ω(max(n, p) log n). At the study sizes, Q_final ≈ 10⁴·(T + 13) ≥ 1.4·10⁵. Since N_e ≥ max(n, p), start masses π₀(S*) ≥ n^{−κ} with κ < 1 (or κ < A when p ≍ n^A) are "polynomially cheap" at the actual budgets; smaller inverse-polynomial masses are not discovered by the iid mechanism alone.

Cost (§8 of the methodology): tables O(p2^B/B) scores; SMC ≈ N(p + B + 2) scores per stage per island; grid ≤ 60|V|T_e log-sum-exp evaluations per construction; local search ≤ (ℓ + 1)(p + max_{k≤K} k(p − k))s(K) (the methodology writes K(p − K), which is the maximum only when K ≤ p/2; corrected after council round 1); preflight predicts memory and wall time and returns `resource_limit` if the allocation is exceeded. A fixed memory allocation cannot support unrestricted growing-dimension consistency (V13).

### 2.14 Numerics and statuses that theorems must condition on

Scores by Cholesky; Q_S recomputed in a non-negative form when Q < 10⁻⁸yᵀy; Cholesky failure ⇒ refactor, then augmented QR, then `numerical_failure` (no artificial −∞; the target is never silently changed). Statuses: `exact`, `completed`, `schedule_limit`, `numerical_failure`, `resource_limit`, `y_constant`, `no_predictors`, `invalid_input`. A combined statement about the output must either condition on `completed`/`exact` or bound the probability of the other statuses. The flags (`escalated`, `checks_passed_*`, `local_certified`, `global_certified` only on `exact`, …) certify nothing about accuracy except as stated; passing diagnostics never sets `global_certified`.

---

## 3. What is known about the components

All project results below are in `C:\Users\felip\OneDrive\Documents\Local_to_global_Bayesian\01_Methodology_and_Theory\Proposed_project\paper_draft\paper_draft.tex` (statements; the dependency map is its Appendix B) with proofs in `...\Proposed_project\proofs\<name>\PROOF.md`. They were written for: column norm n (v3: n − 1), unstandardised y, B = 5 (v3: ≤ 16), systematic Gibbs sweeps plus swaps (v3: random-order round with an independence step), systematic resampling (v3: multinomial), a single pilot schedule frozen for islands (v3: calibration with a candidate grid and rebuilds, and a fresh final run), unbounded local search (v3: ≤ ℓ moves). Status "AI-proved" means proved by AI agents and reviewed by AI agents, not adopted.

| Result | Content | Transfer to v3 (lead's reading) |
|---|---|---|
| P1 | Exact composite start: Z̄₀ by convolution, backward sampler, size-tilted marginals | **Verbatim** (arbitrary positive tables, any size-only prior with cap) |
| T1, L1, L2 | Discrepancy identity d = Δ_det + νΨ; Δ_det ≥ 0, ≤ |S|/(2nφ²(S)); off-block bound O(nκ) | **Verbatim** as algebra (identity in H_S, G_S); constants with n − 1 |
| L3, L4, L7, L5 | Bridge facts: concentration propagates (inf of q_φ(S*) at endpoints); χ² monotone, greedy schedule optimal and terminating; single-model χ² identity; stage count under local sub-Gaussianity | **Verbatim** (pure bridge facts; apply to the population schedule, not the empirical one) |
| T4, P2 | Two-state switch: greedy ESS schedule uses log₂Δ₀ + O(1) stages, path length < π; several switches | **Verbatim** for the population schedule; the empirical schedule needs the particles to see the mode |
| T5 | Mode loss under non-crossing kernels: on E (no initial particle in 𝓜) the whole run has the restricted law; E[Ẑ | E] = Z(1 − q₁(𝓜))/(1 − q₀(𝓜)); leaky bound (v); adaptive schedules (vi) | **Not verbatim:** v3's kernels cross (independence step, §2.8). Only (v) applies, with η ≥ π₀(𝓜)·acceptance; the negative message holds when π₀(𝓜) = e^{−Θ(n)} |
| T3, T11, F4, C1 | Fixed-p start limit: π₀ → point mass at S̃₀ = ∪_b supp(γ_b) (block KL projections); switch gap Δ₀/n → κ₀ ≥ 0, ½ log n per cancelled variable when κ₀ = 0; deletion-only switches without cancellation; cap can crowd out a true variable (T11(iv) remark) | Needs re-check for v3's standardisation (block tables with (n−1) norms, empirical IG rate) and v3's blocks (B ≤ 16, X-driven); statements expected to carry over |
| T2 | No-switch regime (Target, unproved): π₀(S₀) → 1 under (V), (NL); over-tempered concentration gives T = O(A) stages | Open in the old project too; the start-side dimension bound cannot use T6's density identity |
| L6 | BB(1, p) prior lemma | **Verbatim** |
| T6, T9a(i) | Posterior dimension: Π(|S| > m_n | y) → 0, any cap ≥ s₀, any p (quantitative: Π(|S| > m | y) ≤ 2^{−m}(2p)^{s₀}(n+1)^{s₀/2}√n·Θ_n) | **Needs transfer** (V2): the density identity E₀[m(S)/f₀] = 1 fails for standardised y; redo via the reduction (§2.3) uniformly in the IG rate |
| T7 | No supersets under (SE) up to m_n + s₀, p ≤ n^A: O_P(√(log n/n) + e^{−ω_n}) | Needs transfer (uniformity in (a₀, b₀); g = (n−1)+1) |
| T8 | Selection consistency and HPM under beta-min M_n → ∞: Π(S₀ | y) → 1 at O_P(√(log n/n)); P₀(HPM ≠ S₀) ≤ 2E₀[1 − Π(S₀ | y)] | Needs transfer; on the exact branch it is then a theorem about the output |
| T10 | Per-variable sure screening of strong signals without full beta-min | Needs transfer |
| T9, T9a(iii), C9 | Prediction and variance contraction at (s₀+1)ℓ_n²/n without beta-min; single-log rate (s₀+1)ℓ_n/n for p ≤ n^A under (SE); random-design Hellinger version with centred sub-Gaussian rows | Needs transfer; C9's "centred rows" becomes moot (the method centres empirically) but its empirical-centring version is unproved; raw-scale back-transformation needs column-scale bounds |
| Pb1, P4 | Orthogonal design: exact neighbour odds, top-k HPM; sharp HPM threshold τ_n = log D + 2 log((2p−s₀)/s₀), limit Φ(c)^{s₀}, gap log n + O(1) above the minimax centre 2 log(p−s₀) | For centred orthogonal columns, G = (n−1)I gives D = n exactly, p ≤ n − 1; the integrated-variance part rests on T7 and needs the transfer |
| P3, P5 | Size-only ceiling; HPM Bayes for 0–1 loss, MPM for Hamming loss, constrained MPM | **Verbatim** |
| P6 | Kernel correctness: Hastings ratios, neighbour-swap ratio, invariance of compositions with frozen scan probabilities | **Verbatim** for each step; add the independence step and the random-order self-adjointness (V5) |
| P7 | Frozen schedules: E[Ẑ] = Z; Markov lower bound; E log Ẑ ≤ log Z; resampling condition (offspring unbiased given the past; multinomial qualifies) | **Verbatim** conditionally on the calibration (grid, T, L frozen before final randomness; escalation decided before final randomness) |
| F1 | Imported: LLN/CLT as N → ∞ for a fixed schedule with multinomial resampling (Del Moral–Doucet–Jasra 2006; Chopin 2004); adaptive tempering limits (Beskos et al. 2016, Thm 3.4, multinomial, their A5–A7) | Applies to the final run conditionally on the grid; the unconditional limit is a mixture over the random calibration |
| P8, P9, P10, P11 | Certificates (universal bound numerically vacuous); truncation |PIP_j − PIP_{j,V}| ≤ f; HPM over V = global HPM iff global HPM ∈ V; visited-set estimator safeguards; RB PIPs zero conditional variance | **Verbatim** |
| Pb3, Pb4 | Open: bridge → mode model; a positive crossing result | Open; v3's grid and independence step change the question (V11) |

**Literature verdicts already established** (`...\Proposed_project\literature_theory\UNIFIED_LIST.md`, `DECISION.md`, with 97/97 identifiers resolved in `CITATION_CHECK.md`; 10 reports in `reports\`): the standard SMC menu (LLN/CLT; frozen-schedule unbiasedness; non-asymptotic error under global mixing, Marion–Mathews–Schmidler 2023, Le Fay–Chopin–Vihola 2026; local mixing plus mode-mass bounds, Mathews–Schmidler 2024, vacuous at a switch; Syed et al. path length and Λ²/T; Gerber–Chopin–Whiteley 2019 on resampling); the standard VS menu (Yang–Wainwright–Jordan 2016; Narisetty–He 2014; Castillo–Schmidt-Hieber–van der Vaart 2015; Rossell 2022 Prop. 1 HPM error bound and Prop. 6 fixed-design projection; Song–Liang 2015; Scott–Berger 2010; Zhou et al. 2022 mixing; Barbieri–Berger 2004); why the YWJ and Castillo templates fail for BB(1, p) + g = n (geometric size tail; g not polynomial in p); that T11-type polynomial complexity is "unconditionally unlikely"; that divide-and-conquer SMC (Lindsten et al. 2017) is the closest sampler precedent; that George–McCulloch 1997 anticipates the visited-set estimator. Precedents for assumptions should be taken from these verified sources or from `C:\Users\felip\OneDrive\Documents\Local_to_global_Bayesian\03_Literature\Papers\` (31 PDFs plus subfolders); anything not seen is to be marked unverified.

**The three consultants' main cautions** (recorded in METHODOLOGY_v3 §10–11): the transfer of T6–T10 is substantial, not a constants check; standardised errors are not conditionally Gaussian in the raw coordinates (use the contrast representation); agreement among consultants identifies routes, it does not establish them; Ẑ can be off by e^{Θ(n)} with every self-check passing when a crossing is not resolved by the schedule (the grid of §2.10 is the design response; whether it suffices is V11); the fixed memory allocation bounds any growing-dimension claim.

---

## 4. Facts about the exact method that the council should use

1. **Everything scored counts.** The HPM is the max of F over all scored models, including the p2^B/B table sub-models. Hence if S₀ ⊆ C_b for some block b, S₀ is always scored, and HPM = S₀ whenever S₀ is the global mode of π. More generally the discovery bound of §2.13 holds with Q = total iid π₀ draws.
2. **The kernels cross.** By §2.8, every round proposes a fresh iid π₀ draw per particle. Non-crossing mode-loss results do not apply; leaky ones do, with entrance rate ≥ π₀(𝓜)·acceptance per particle-round.
3. **The final run is a frozen-schedule SMC** (grid, T, L, N_e fixed before streams 10–13 are drawn), with iid exact start, exact Z̄₀, multinomial resampling at every stage, q_φ-invariant self-adjoint kernels, one round per stage. Unbiasedness (P7) and the standard LLN/CLT (F1) apply conditionally on calibration, for the terminal particles and for the RB-PIPs recorded in the measured rounds (P11); the measured rounds are at φ = 1 after L burn-in rounds, all with the same kernel K₁.
4. **The calibration is random and data-dependent.** Given it, each island evidence Ẑ_r is unbiased for Z, and the unnormalised products Ẑ_r·PIP̂_{rj} are candidates for the identity E[Ẑ_r PIP̂_{rj} | 𝓒] = Z·PIP_j (to be proved through the burn-in and measured rounds; it is not in P7 as stated). The normalised PIP estimators (primary and secondary) and log Ẑ are **not** unbiased at finite budgets (corrected after council round 1). The escalation decision is calibration-measurable and the final streams are fresh, so no selection bias enters Ẑ. The unconditional law of the estimators is a mixture over the calibration.
5. **The candidate grid is a refinement of the pilot schedule driven by scored models.** Its guarantee is restricted: for the pair (or set) of competing models in V, the one-step restricted χ² is ≤ 1/9 at every grid interval. Fable-T3's two-state analysis (V11) says: if the competing pair is in V and the bridge is pair-dominated (PD), the final relative evidence error is O_P(√(cT/N)); without the grid, the pilot schedule alone gives Ẑ/Z = n^{−1/2}e^{O_P(1)} (proxy deletion) or e^{−Θ(n)} (proxy block plus a near-cancelled true variable) with E1–E3 passing.
6. **The local search is a deterministic best-improvement ascent on F from the best scored model, capped at ℓ = ⌈log₂(n + p + 1)⌉ moves.** It cannot certify global optimality; `local_certified` means no improving single flip or swap from the returned centre.
7. **The size cap K = ⌊n/2⌋ is in the state space.** Mixing arguments on {|S| ≤ K} must handle models up to size n/2 (no (SE) control there), or work on a working set A_n = {|S| ≤ d_n} with excursion bounds (V10).
8. **Multinomial resampling at the terminal stage** means the measured rounds start from an equally weighted population drawn (with replacement) from the stage-T population; this costs nothing in validity but adds resampling noise.
9. **B is eventually fixed (16) in R1**, so "B fixed" is theory-friendly; the blocks are correlation clusters, so cluster-type design assumptions (CS) are the natural start-side hypotheses, and the neighbour threshold √(2 log p/n) is the same scale as the between-cluster correlation one would assume.
10. **The exact branch covers every fixed-p problem eventually**, so fixed-p SMC statements are component theorems (about pieces reused in growing p), not production guarantees.

---

## 5. The methodology thread's suggested targets V1–V13

METHODOLOGY_v3 §11 lists V1 (reduction and normalisation), V2 (dimension, no supersets, support and PIP consistency for the v3 target), V3 (contraction, coefficients, variance, raw-scale back-transformation), V4 (sharp orthogonal threshold), V5 (exact start and kernels), V6 (fixed-data Monte Carlo validity of the final run conditional on calibration; R-consistency of the secondary PIP pooling), V7 (all-scored HPM discovery and combined recovery), V8 (no-switch regime: π₀(S₀) → 1 for the actual blocks, then everything consistent at fixed budgets), V9 (burn-in correction, fixed p), V10 (mixing with the cap), V11 (evidence through discovered crossings, positive and negative), V12 (limits of the checks), V13 (resources, numerics, failure statuses). **These are starting suggestions, not the council's list.** The council proposes its own list: adopt, split, merge, sharpen, drop, or add. In particular, the lead flags as under-examined: (a) a direct theorem about the final local search as a component of HPM recovery (uniform single-flip improvement toward S₀ under (SE) and beta-min; the hard case is supersets reached by a data-dependent centre, where uniform noise bounds over p^{m_n} pairs cost m_n log p, so a naive argument fails); (b) the combined R4 theorem's dependence on Q_final = 4N_e(1 + T + L + 4) with N_e ≥ max(n, p): which start masses π₀(S₀) are "polynomially cheap" at the actual budgets; (c) the secondary PIP pooling's exact unbiasedness identity E[Ẑ_r PIP̂_{rj}] = Z·PIP_j (requires the measured-round RB average to be a terminal-stage functional: check whether burn-in rounds after the terminal resampling preserve the identity; P7(i) is stated for the terminal population only); (d) the role of exact ties and the near-tie list in HPM consistency (v3 uses exact equality, so the consultants' tolerance objection is resolved by design; say so); (e) what the pooled 0.05·Ẑ bound and the island SD certify; (f) negative results in the style of T5 and Fable-T3's counterexamples restated for v3's crossing kernels and grid.

---

## 6. Rules for every candidate theorem

Each candidate gives: category (consistency, contraction rate, asymptotic normality/BvM, algorithmic validity, algorithmic convergence or complexity, robustness, negative/limit result); an informal statement and a precise statement with every quantifier explicit (which regime of §1, which of the method's objects, conditional on what); assumptions each marked *standard* (precedent from a source you have actually seen, with locator) or *new* (why needed, why reasonable, how it could be checked on data when possible); the proof route (strategy, key lemmas, known results relied on, hardest step); confidence that it is true (high/medium/low with a reason); why it matters to Felipe's four areas; what it builds on and what uses it; and, if it would need a change to the method, the recommendation and reason, separately. Everything is a conjecture. Theorems must be about the method of §2 with its tuning rules, not an idealisation; where an idealisation is unavoidable (for example the population ESS schedule), say exactly which rule is idealised and why.

---

## 7. Files

- Methodology (authoritative): `C:\Users\felip\OneDrive\Documents\Local_to_global_Bayesian\01_Methodology_and_Theory\Methodology\SMC_BVS_v3_20261019\METHODOLOGY_v3.md`
- Existing theory statements: `C:\Users\felip\OneDrive\Documents\Local_to_global_Bayesian\01_Methodology_and_Theory\Proposed_project\paper_draft\paper_draft.tex` (§2 setup, §3–5 statements, Appendix B map); proofs under `...\Proposed_project\proofs\<name>\PROOF.md` (foundations: F4, L4, L6, P6, P7; elementary_I: P1, T1, L1, L2, L3, L5, L7; elementary_II/III: P8–P11, P3–P5; T3_T11; T4; T5; T6; T7_T8 (T7, T8, T10); T9_C9; P2; Pb1).
- Literature: `C:\Users\felip\OneDrive\Documents\Local_to_global_Bayesian\01_Methodology_and_Theory\Proposed_project\literature_theory\` (`UNIFIED_LIST.md`, `DECISION.md`, `CITATION_CHECK.md`, `VERIFY_A.md`, `VERIFY_B.md`, `reports\{O1,O2,O3,A1,A2,S1,…,S5}.md`); papers `C:\Users\felip\OneDrive\Documents\Local_to_global_Bayesian\03_Literature\Papers\`; Song & Liang (2015) at the path in §0.
- This run: `C:\Users\felip\OneDrive\Documents\Local_to_global_Bayesian\01_Methodology_and_Theory\Theory_architecture_v3\` (council\, review\, judge\, theorems\, RULINGS.md, THEORY.tex, THEOREM_MAP.md, DROPPED.md, STATUS.md).

---

## 8. Corrections log (lead)

- **2026-10-19, after council round 1 (both Astra members flagged these independently):** §2.8 observation rewritten to separate scoring, visiting and end-of-round occupancy, and to state the independence-step minorisation; §2.9 pilot ESS clarified as the empirical ESS over the pilot particles; §2.13 discovery count restricted to the frozen final run (the adaptive calibration count is not a valid fixed exponent) with the "polynomially cheap" start-mass range stated; §4 item 4 corrected (only Ẑ_r and the unnormalised products are candidates for conditional unbiasedness; normalised PIPs and log Ẑ are not); §2.13 local-search scan count corrected to max_k k(p − k).
- **2026-10-19, after council round 1 (Fable-C1 re-run, Astra-C1, Astra-C2):** §2.8 (c) now records that the independence-step minorisation passes to the whole round, K_φ ≥ ε_φ q_φ (the earlier wording said no end-of-round bound follows; that was too pessimistic).
