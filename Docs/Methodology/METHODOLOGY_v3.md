# SMC-BVS v3: composite-start SMC for Bayesian variable selection — complete method report

**Version:** v3.0, 2026-10-19. **Status:** design, agreed by the lead (Opus 5.5) and three theory consultants (Astra-T1 and
Astra-T2, gpt-6-astra xhigh; Fable-T3, Fable 5.1 high) over two meeting rounds. **Not implemented, not verified, nothing in
it is proved.** Every statement about guarantees is a target or an existing AI-proved, not-adopted project result, labelled as
such.

**Relation to v2.** The pre-theory plan (`../Spec_anyXY_20261019/SPEC_anyXY_v2.md`, frozen read-only with
`FROZEN_PRE_THEORY.md`) stays the basis of the **first deployment**. v3 is the theory-aligned version: the exact object the
theory programme (§11) is about. §12 lists every difference.

**Requirements set by Felipe.** (1) Runnable from X, y and one integer seed alone: every choice is made in advance.
(2) Scalable. (3) Aligned with as many and as relevant theoretical results as the method allows. (4) No bare tuning constants:
every setting is a modelling convention with a stated reason, an explicit function of (n, p) or of X, or a declared resource
budget. Nothing depends on the unknown support, the signal strength, study sizes or past results. (5) Felipe's own decisions
are kept: the target posterior, the size cap ⌊n/2⌋, the block-size rule, the neighbour-graph rule, the HPM decision, and no
secondary prior arm for now.

Sources: §14.

---

## 1. What the method does, in one paragraph

Given X (n × p) and y, SMC-BVS computes the posterior over subsets S of predictors under a unit-information g-prior with a
unit ridge, a vague inverse-gamma noise prior and a beta-binomial BB(1, p) model prior capped at ⌊n/2⌋ variables. It reports
the highest-posterior model found (HPM), posterior inclusion probabilities (PIPs) and the evidence Z. When the capped model
space is small it enumerates it exactly. Otherwise it starts from an exactly sampleable approximation of the posterior built
from small correlation blocks of predictors, each enumerated exactly, and tempers from that start to the posterior with a
sequential Monte Carlo (SMC) bridge, moving particles with Gibbs, swap, correlation-neighbour and independence moves. A
calibration phase builds the tempering schedule, including extra temperatures wherever competing high-scoring models found
so far would make the bridge jump; then a fresh final run, whose settings are fixed before its randomness is drawn, produces
the reported estimates.

## 2. Inputs, outputs and statuses

**Input:** numeric X ∈ ℝ^{n×p}, y ∈ ℝⁿ, an integer seed s ∈ [1, 2³¹ − 1], and the job's resource allocation (memory, wall
time; standalone default 8 GiB memory). Nothing else.

**Outputs:** the HPM with its log score and provenance (which phase first scored it); a near-tie list; PIPs (primary and
secondary pooling) and the median probability model (MPM); the evidence per final island, pooled, its 95% lower bound, on the
full working scale and relative to m(∅); calibration estimates, labelled as such; status and flags; the blocks, the neighbour
graph, the schedules, the budgets used, the random-stream map, score counts, per-stage ESS (restricted and empirical), the
candidate-set size and rebuild count, timings by phase, resource estimates; the preprocessing map (dropped columns, column
means and scales, s_y). When a simulation truth is supplied separately (never to the fit), the truth's score versus the HPM and
whether the truth is retained in the stored top models.

**Statuses** (exactly one): `exact` (enumeration completed) · `completed` (SMC completed; flags may be set) ·
`schedule_limit` (no admissible schedule within the stage ceiling at the highest tier; the best scored model is returned,
evidence and PIPs unavailable) · `numerical_failure` (scoring failed after the fallback; estimates unavailable; the best scored
model returned, labelled incomplete) · `resource_limit` (preflight predicts the memory or time allocation will be exceeded;
estimates of the inputs returned) · `y_constant` · `no_predictors` · `invalid_input`.

**Flags and certification fields:** `escalated` (tier 1 used); `checks_passed_calibration`, `checks_passed_final`;
`forced_pilot_steps` (count); `grid_unconverged`; `local_limit`; `low_empirical_ESS` (any final stage below 0.5 N);
`near_tie_truncated`; `local_certified` (the returned model is a scanned centre with no improving neighbour);
`global_certified` (only on `exact`, with numerical comparisons validated). Passing diagnostics never sets
`global_certified`.

## 3. Notation and budgets

| Symbol | Definition | n = 200, p = 500 | n = 200, p = 1,000 |
|---|---|---|---|
| p | number of retained (non-constant) predictors | 500 | 1,000 |
| K | size cap, min(p, ⌊n/2⌋) | 100 | 100 |
| B | block size, min(⌊√n⌋, ⌊√p⌋, B*), B* = 16 (implementation limit) | 14 | 14 |
| ℓ | ⌈log₂(n + p + 1)⌉ (local-search and rebuild budget) | 10 | 11 |
| L | max(4, ⌈log₂(n + 1)⌉) (burn-in rounds at φ = 1) | 8 | 8 |
| N₀ | max(2,500, n, p) final particles per island | 2,500 | 2,500 |
| H₀ | ⌈512·N₀/2,500⌉ calibration particles (pilot and each diagnostic island) | 512 | 512 |
| T₀ | max(1,000, ℓ²) stage ceiling | 1,000 | 1,000 |
| R | 4 islands (final and diagnostic) | 4 | 4 |
| tier e | e ∈ {0, 1}; (N_e, H_e, T_e) = 4^e (N₀, H₀, T₀) | | |

These are **declared resource budgets**, not accuracy guarantees. At the study sizes they equal v2's numbers. Tier 1 multiplies
particles and the stage ceiling by 4, so it permits up to about 16× the bridge work. N₀ = 2,500 unless n or p exceeds 2,500.

## 4. Preprocessing

1. Stop with `invalid_input` if any entry of X or y is not finite, or n < 3, or p < 1.
2. Drop column j only if all its entries are **exactly** equal; record it; it is never selected. p := number kept. If p = 0,
   return Ŝ = ∅, PIPs and evidence unavailable, status `no_predictors`.
3. If all entries of y are exactly equal, return Ŝ = ∅ (the exact HPM: every Q_S = 0, D_S ≥ 1 and w is decreasing), PIPs and
   evidence unavailable, status `y_constant`. (The exact PIPs are not 0; they are not computed.)
4. Standardise stably: for each column, divide by its maximum absolute value, compute the mean, centre, then divide by the
   sample SD (denominator n − 1), so ‖x_j‖² = n − 1. Same for y, recording s_y² = ‖Cy‖²/(n − 1) with C = I − 11ᵀ/n.
   Original indices, means and scales are kept for reporting and back-transformation.
5. Report connected components of {|r_jl| ≥ 1 − 10⁻¹⁰} (duplicates are kept; they split PIP mass, and the MPM may exclude
   both members).
6. Resource preflight (§8.6).

These rules make the target invariant to affine maps of y (a ≠ 0) and of each column of X, and to column permutation (up to
index-based tie-breaks in clustering and decisions, which are deterministic).

## 5. Target posterior (Felipe's model, unchanged)

On the standardised data (X, y), for S ⊆ {1, …, p} with k = |S| ≤ K, G_S = X_SᵀX_S, z_S = X_Sᵀy:

```text
y | β_S, σ², S ~ N_n(X_S β_S, σ² I_n)                   (no intercept; y is centred)
β_S | σ², S    ~ N_k(0, n σ² (G_S + I_k)⁻¹)              g = n (unit information), τ = 1 (one pseudo-observation)
σ²             ~ IG(a₀, b₀),  a₀ = b₀ = 0.01
ϖ(S)           = w(k) 1{k ≤ K} / W_K,   w(k) = B(1+k, 2p−k)/B(1, p) = ½ / C(2p−1, k),   W_K = Σ_{j≤K} C(p, j) w(j)

H_S = (n + 1) G_S + I_k,   Q_S = yᵀy − n z_Sᵀ H_S⁻¹ z_S,
log m(S) = log C_n − ½ [log det H_S − log det(G_S + I_k)] − (a₀ + n/2) log(2b₀ + Q_S),
C_n = (2b₀)^{a₀} Γ(a₀ + n/2) / (π^{n/2} Γ(a₀)),
π(S | y) = ϖ(S) m(S) / Z,   Z = Σ_{|S|≤K} ϖ(S) m(S).
```

Reasons (accepted by Felipe; defended in the audit):
- g = n: unit information. τ = 1: one pseudo-observation on the standardised scale; keeps every m(S) finite for collinear X_S.
- IG(0.01, 0.01): proper, as the project proofs require. Its effect on comparing two models is at most n·b₀·|1/Q₁ − 1/Q₂|:
  negligible near a decision boundary (Q₁ ≈ Q₂) and dominated by the gap otherwise. With y standardised, Q_S ≥ yᵀy/(n+1).
- BB(1, p): depends on p only; prior mean size p/(p+1) ≈ 1; each extra variable costs log((2p−k−1)/(k+1)) nats; the project's
  existing theory is for this prior. Its extra cost over a uniform-on-size prior is log((2p−k−1)/(p−k)) per variable, ≈ log 2
  only when k ≪ p.
- Cap K = min(p, ⌊n/2⌋): keeps near-interpolating models out of the space; the ½ is a declared restriction, not needed for
  propriety. The project's dimension result (T6) says the cap does not bind in the regimes it covers.

**Reduction statement (consensus of the three consultants; to be proved, V1).** Write raw data X^r, y^r, D_x = diag(column
SDs), X = C X^r D_x⁻¹, and U ∈ ℝ^{n×(n−1)} orthonormal with UUᵀ = C. With θ = s_y β and v = s_y² σ², the posterior above is
the posterior of the contrast regression of Uᵀy^r on UᵀX with n − 1 Gaussian errors (Uᵀε ~ N(0, σ*² I_{n−1}) exactly, before
standardisation of y), slab θ_S | v, S ~ N(0, n v (G_S + I)⁻¹) and v ~ IG(0.51, 0.01 s_y²). So the exponent a₀ + n/2 is the
integrated-intercept model with IG shape a₀ + ½, and the response scale enters only through the data-dependent IG rate.
This is not a claim that the working evidence equals a raw-data marginal likelihood; "evidence" below always means the
evidence of this working model.

## 6. Algorithm

### 6.1 Execution order

```text
preprocess, preflight
if exact-branch condition: enumerate (6.2), local certification, report
else:
  build blocks, tables, start (6.3); neighbour graph (6.4)
  CALIBRATION, tier e = 0 (streams 0 and 1–4):
     pilot (H_e particles, adaptive ESS schedule, 6.6) → polish + local search on the pilot
     candidate set V; preliminary grid (6.7)
     repeat ≤ ℓ times: 4 diagnostic islands (H_e each) on the current grid, with burn-in and measured rounds
                       → local search → update V → rebuild grid; stop when the rebuilt grid equals the previous one
     checks (6.9)
  if any trigger and e = 0: repeat CALIBRATION at tier 1 (streams 5 and 6–9), keeping the score leaders
  freeze: grid, budgets (N_e), V-independent settings
  FINAL (streams 10–13): 4 fresh islands × N_e, new iid start draws, frozen grid, burn-in L rounds, 4 measured rounds
  final local search; final checks (flags only)
  report (6.11–6.13)
```

Final observations never revise the schedule and never select replacement estimates. Calibration estimates are archived and
labelled; they are never reported as the estimate.

### 6.2 Exact branch

If E = Σ_{k≤K} C(p, k) ≤ (5H₀ + 4N₀)·p (12,560·p at baseline; counted with saturating integer arithmetic), score every model
with |S| ≤ K in a streaming pass: running best (strict order of §6.10), log-sum-exp accumulation of Z and of the PIP numerators.
No blocks are built. Status `exact`; `global_certified` when all comparisons are numerically validated. This applies for
p ≤ 17 for n ≥ 22 (p ≤ 18 at n = 20, 21), and for larger p when the cap binds (for example p ≤ 36 at n = 10; all p ≤ 3,000 at n ≤ 5). Because the
threshold grows with N₀ ≥ n, every fixed-p problem is eventually enumerated as n grows.

### 6.3 Blocks, tables and the composite start

- **Clustering:** complete linkage on the distance 1 − |r_jl| computed from X; ties between candidate merges broken
  lexicographically on the sorted original-index lists.
- **Cut:** top-down from the root; any node with more than B members is split into its two children (visited smallest index
  first) until every retained cluster has at most B members.
- **Packing:** next-fit in dendrogram leaf order, whole clusters only (a retained cluster is never split), into blocks
  C₁, …, C_J of at most B members. J ≥ ⌈p/B⌉ (packing leaves gaps).
- **Tables:** for each block, every sub-model U ⊆ C_b is scored against the full y; r_b(U) = m(U)/m(∅) (table exponent 1).
  Since B ≤ K for n ≥ 3, no sub-model exceeds the cap. Every table score counts for the HPM. Table scores are not inserted in
  the score cache.
- **Start:** γ₀(S) = ϖ(S) ∏_b r_b(S ∩ C_b), π₀ = γ₀/Z̄₀. Z̄₀ is computed exactly by convolving the block size profiles
  e_b(j) = Σ_{|U|=j} r_b(U) up to K with the size prior (valid because ϖ depends on S only through |S|). Exact iid draws:
  draw the total size, then block sizes backwards, then each block's sub-model within its size class.
- **Discrepancy:** d(S) = log BF(S) − Σ_b log r_b(S ∩ C_b), BF(S) = m(S)/m(∅); bridge γ_φ(S) = γ₀(S) e^{φ d(S)}, φ ∈ [0, 1];
  γ₁ ∝ the posterior; Z = m(∅) Σ_S γ₁(S).

### 6.4 Neighbour graph

r_n = √(2 log p / n) (about the largest correlation p unrelated columns reach by chance). For each j: the partners l ≠ j with
|r_jl| > r_n, always including j's single largest-|r| partner, keeping at most the B largest (ties by original index); then the
symmetric union N(j) (l ∈ N(j) ⇔ j ∈ N(l); degrees may exceed B). No edges when p = 1. Accepted by Felipe for now.

### 6.5 The move round at temperature φ

A round is the list of m = p + B + 2 labelled elementary steps — the p Gibbs coordinate updates, one uniform swap, B neighbour
swaps, one independence proposal — applied **in a uniformly random order drawn independently of the particle's state, afresh
for every particle and every round**.

- **Gibbs coordinate j:** draw j's inclusion from its conditional under γ_φ, with an addition at |S| = K excluded. Record the
  conditional inclusion probability o_j immediately before the draw (used for PIPs in measured rounds).
- **Uniform swap:** skipped (self-loop) if |S| ∈ {0, p}; delete j uniformly from S, add l uniformly from outside; accept with
  1 ∧ γ_φ(S′)/γ_φ(S).
- **Neighbour swap:** skipped if S = ∅; delete j uniformly from S; if N(j) \ S = ∅ reject; else add l uniformly from N(j) \ S;
  accept with 1 ∧ [γ_φ(S′)/γ_φ(S)]·|N(j)\S| / |N(l)\S′|.
- **Independence proposal:** S′ ~ π₀ (exact draw), accepted with 1 ∧ e^{φ[d(S′) − d(S)]}. Every proposal is scored, accepted or
  not.

Each step is reversible with respect to γ_φ; the composition in a random order whose law is invariant under reversal is
self-adjoint (checked by all three consultants; V5). An individual realised order is not.

### 6.6 Resampling and the pilot schedule

- **Resampling:** fresh multinomial resampling after every reweighting, including the terminal stage (O(N) per stage with a
  linear-time categorical sampler).
- **Pilot:** H_e particles from π₀; at each stage the next temperature is the largest φ′ with population ESS of the weights
  e^{(φ′−φ)d} at least 0.90·H_e (weight CV² ≤ 1/9), found by 60 bisection halvings; exploratory floor 1/T_e (forced steps
  counted as `forced_pilot_steps`); ends exactly at φ = 1; then L burn-in rounds, 4 measured rounds and a local search.

### 6.7 Candidate set and candidate grid

- **V:** the union of the top 20p scored models by log γ₀, the top 20p scored models by log γ₁ (the target), and ∅;
  deduplicated; list ties lexicographic; frozen during each construction.
- **Restricted log-normaliser:** F_V(t) = log Σ_{S∈V} γ₀(S) e^{t d(S)}.
- **Restricted ESS** between temperatures u < v: ρ_V(u, v) = exp{2F_V(v) − F_V(u) − F_V(2v − u)}, the population ESS fraction
  of the weights e^{(v−u)d} under the restricted law q_u(· | V) (evaluating F_V beyond 1 is a finite-sum moment, not a
  production temperature).
- **Construction:** start at u = 0 with the pilot temperatures as targets. For the next pilot temperature b: if
  ρ_V(u, b) ≥ 0.90 append b; otherwise bisect on (u, b] with u fixed, at most 60 halvings, and append the largest tested
  endpoint that passes; continue from the appended point. Validate strict numerical progress and the inequality at every
  appended point. Non-progress, failed validation, or more than T_e intervals → the construction fails.
- **Rebuild loop:** after each set of diagnostic islands, update V and rebuild; stop when the rebuilt grid equals the
  previous one; at most ℓ iterations (lead's ruling: convergence is judged on the grid, not on V, because with a flat
  posterior the top list keeps changing by Monte Carlo noise; Fable-T3 proposed judging it on V). If not converged: flag `grid_unconverged` (a calibration trigger); at tier 1 the last
  grid is used and the flag is reported. If a construction fails: trigger escalation at tier 0; status `schedule_limit` at
  tier 1.
- **Purpose:** the pilot cannot see a mode it has not sampled, so its schedule may jump across the point where a competing
  model takes over. The grid inserts temperatures exactly where models already scored would make the bridge jump. Fable-T3's
  two-state analysis (to be proved, V11): if the competing pair is in V and the bridge is pair-dominated, the final-run relative
  evidence error is O_P(√(cT/N)) at fixed N. Without it, the evidence can be off by n^{−1/2} (proxy deletion) or e^{−Θ(n)}
  (proxy block plus a near-cancelled true variable), while every self-check passes.
- **Limits:** the grid controls restricted one-step weight dispersion only; it does not control full-space ESS, particle
  occupancy, mixing, or modes never scored; |V| ≤ 40p + 1 may truncate when many near-equivalent models matter. Cost per
  construction ≤ 60·|V|·T_e scalar log-sum-exp evaluations (≈ 2.4·10⁹ at p = 1,000, T_e = 1,000 in the worst case; the
  consultants differ on whether this is negligible against scoring; it is measured, not assumed).

### 6.8 Calibration and final runs

- **Calibration** (tier e): the pilot (§6.6) and, per rebuild iteration, 4 diagnostic islands of H_e particles on the current
  grid, each followed by L burn-in rounds, 4 measured rounds and a local search. Streams 0 and 1–4 (tier 0), 5 and 6–9 (tier 1).
  Score leaders are kept across tiers.
- **Final:** 4 islands × N_e particles from fresh iid π₀ draws, the frozen grid, multinomial resampling, one move round per
  stage, then L burn-in rounds and 4 measured rounds at φ = 1, then a local search. Streams 10–13, independent of all
  calibration randomness. No forced steps.

### 6.9 Checks and escalation

Calibration triggers (any one ⇒ at most one escalation to tier 1, decided before any final randomness):
E1 some diagnostic island's best score is more than 1 nat below the overall best (a missed mode worth a factor e in odds);
E2 the SD of the 4 diagnostic log Ẑ exceeds 1 nat (evidence not known within a factor e); E3 a local search improved the best;
forced pilot steps; `grid_unconverged`; a failed grid construction; `local_limit`.
Forced pilot steps trigger tier 1 but do not invalidate a successfully constructed grid. After the final run, E1–E3 and the
empirical-ESS check are recomputed as flags only.

### 6.10 Local search and the decision rule

- **Local search:** from the current best scored model (the centre), scan every feasible flip and swap (additions beyond K
  excluded) with the centre frozen during the scan; move to the best strict improvement (lexicographic ties); at most ℓ moves,
  then one further scan; stop earlier when a scan finds no improvement. Every evaluated model updates the global best. If the
  last scan still improves, set `local_limit` (no restart). `local_certified` only when the returned model is a scanned centre
  with no improving neighbour. The search never alters particles.
- **HPM:** the strict maximum of log ϖ(S) + log m(S) over every model ever scored (tables, pilot, calibration, final rounds,
  rejected proposals, independence proposals, local searches), kept as a running best that survives cache eviction. Only
  exactly equal scores invoke the tie rule: smallest |S|, then lexicographically smallest index set. A near-tie list (models
  within 10⁻⁹ nat of the best, drawn from the stored top 40p + 1) is reported; it never reorders, and `near_tie_truncated` is set
  if the list may be incomplete.

### 6.11 PIPs

In the 4 measured final rounds, average the recorded conditional inclusion probabilities o_j (Rao–Blackwellisation) over
particles and rounds within each island. **Primary:** equal-weight mean over the 4 islands. **Secondary:**
Σ_r Ẑ_r PIP̂_{rj} / Σ_r Ẑ_r (consistent as the number of islands grows at fixed N, because Ẑ_r·PIP̂_{rj} is unbiased for
Z·PIP_j; to be proved, V6). Neither normalised estimate is unbiased at finite budgets. MPM = {j : primary PIP̂_j > ½}; it may
exceed K and is reported as computed.

### 6.12 Evidence

Final island r: Ẑ_r = m(∅) Z̄₀ ∏_t (1/N_e) Σ_i exp{(φ_t − φ_{t−1}) d(S_i^{(t−1)})}, with W_K inside γ₀ exactly once.
Pooled Ẑ = (1/4) Σ_r Ẑ_r via log-sum-exp; 95% lower bound 0.05·Ẑ (Markov; one-sided, not an accuracy interval). Reported on
the full working scale and relative to m(∅). Given the frozen calibration, each Ẑ_r is unbiased (existing project results P6,
P7); log Ẑ is not.

### 6.13 Numerics

Cholesky factors for log-determinants and solves; no explicit inverses or determinants. Q_S by subtraction, recomputed by the
non-negative form Q = ‖y − X_S β̂‖² + (‖X_S β̂‖² + ‖β̂‖²)/n with β̂ = n H_S⁻¹ z_S whenever Q < 10⁻⁸·yᵀy (no clipping).
Log-sum-exp for every sum of weights, profiles and evidence. On a Cholesky failure, refactor from scratch, then use an
augmented QR on X_S; if that fails, stop with `numerical_failure` (no artificial −∞, which would silently change the target).

## 7. End-to-end pseudocode

```text
SMC_BVS(X, y, s):
  checks, preprocessing (§4); preflight (§8.6) → maybe return
  K, B, ℓ, L, N₀, H₀, T₀ from (n, p)
  if Σ_{k≤K} C(p,k) ≤ (5H₀ + 4N₀)p: return ENUMERATE()
  Gram, correlations; blocks, tables, Z̄₀, sampler of π₀; neighbour graph
  for e in {0, 1}:
     grid, V, diagnostics ← CALIBRATE(e)            # pilot, V, preliminary grid, ≤ ℓ rebuilds, checks
     if no trigger or e = 1: break
  if grid construction failed at e = 1: return schedule_limit (best scored model)
  islands r = 1..4 (streams 10..13): FINAL_ISLAND(grid, N_e)    # bridge + L burn-in + 4 measured rounds
  final local search; final flags
  return HPM, near ties, PIPs (primary, secondary), MPM, Ẑ_r, Ẑ, 0.05Ẑ, status, flags, provenance
```

## 8. Cost and scalability

Let s(k) be the cost of one score at model size k: O(k³) from the Gram matrix (3–20 µs for k ≤ 20 on the lead's PC,
`../Spec_anyXY_20261019/TIMING_blocksize.md`), up to O(nk²) under the QR fallback.

1. **Preprocessing and Gram:** O(np²) time, 8p² bytes; correlations and clustering O(p² log p) time, O(p²) memory.
2. **Tables:** Σ_b 2^{|C_b|} ≤ p·2^B/B scores. Measured with the 14 Oct engine at n = 200, p = 1,000: B = 14, 2.9 s, 20 MB;
   B = 16, 15.5 s, 121 MB. Linear in p for fixed B.
3. **SMC:** per stage about N·(p + B + 2) scores per island (Gibbs dominates); stages T (22 in one local pilot at n = 200,
   p = 1,000); calibration ≈ (1 + 4·iterations)·H_e particle trajectories; final 4·N_e; plus (L + 4) rounds at φ = 1.
   With N₀ ∝ max(n, p) the per-stage cost is O(p²·s(k)) once p > 2,500: time binds before memory for p ≳ 10⁴.
4. **Grid:** ≤ 60·|V|·T_e log-sum-exp evaluations per construction, |V| ≤ 40p + 1.
5. **Local search:** ≤ (ℓ + 1)·(p + K(p − K))·s(K).
6. **Preflight:** before allocation, branch by branch (and again before escalation), estimate peak memory (standardised data,
   Gram, correlations, clustering, tables, convolution tables, model keys, populations, active factors, cache 500p, top-40p
   store, V, QR scratch) and wall time (score count × measured s(k)); if either exceeds the job allocation, return
   `resource_limit` with the estimates. Islands may run sequentially.
7. **Implementation limit:** B* = 16 binds only when n and p are both ≥ 289; raising it needs a C++ start (about B ≤ 20).

## 9. What is guaranteed now, and what is not

**By construction (given correct code):** the exact branch returns the exact HPM, PIPs and Z of the target. The start is an
exact iid sampler with exactly known normaliser. Every move is reversible for its tempered target; the random-order round is
self-adjoint. Given the frozen calibration, each final Ẑ_r is unbiased for Z (existing project results P6, P7, AI-proved, not
adopted). The HPM is the best of every model scored. Reported estimates come from a run whose settings were fixed before its
randomness was drawn, so escalation does not bias them.

**Not guaranteed:** that the HPM is the global posterior mode (no finite search certifies this without a usable upper bound
on Z); accuracy of Ẑ or PIPs at a given budget (no mixing or weight-moment bound is established); detection of modes no move
ever reaches (a constructed counterexample in the audit shows every check passing while the returned model is far below the
optimum). The checks detect disagreement; they do not certify accuracy.

## 10. Assumptions the theory will need (consultant consensus; all to be examined by the theory run)

- **Data-generating model:** Gaussian linear model with an intercept; fixed noise variance σ*²; bounded centred signal energy
  ‖μ‖²/n ≤ M; fixed number of true variables s₀ (first theorems); p ≤ n^A (polynomial).
- **Design:** sparse eigenvalues bounded below, λ_min(X_TᵀX_T/n) ≥ φ₀² for |T| ≤ m_n + s₀ with
  m_n = ⌈(s₀ log(2p) + (s₀ + 1)(log n)/2 + ω_n)/log 2⌉; for start-side results, a cluster-separation condition (CS:
  within-cluster |r| above between-cluster |r|, clusters of at most B variables, between-cluster correlation at the
  √(log n / n) scale — the same scale as the neighbour threshold) and a no-leakage condition (NL).
- **Signal:** beta-min, min_{j∈S₀} θ_j² ≥ M_n σ*² log n / (n φ₀²) with M_n → ∞ (the log n scale is sharp in orthogonal
  designs by the project's Pb1); screening results need it only for a strong subset.
- **Computation:** exact scores up to numerical error with validated comparisons; for growing-dimension computational results,
  warm-start / entrance and excursion control relative to a working set A_n = {|S| ≤ d_n}; pair dominance (PD) for evidence
  through switches; omitted-mass and weight-moment conditions for evidence accuracy.
- **Not covered by any planned result:** growing s₀ (first wave), duplicated predictors (unidentifiable), weak signals below the
  beta-min scale (only screening), heavy-tailed or non-Gaussian errors.

## 11. Theory programme: targets V1–V13 (conjectures for the theoretical-architecture run)

Labels refer to the paper draft `Proposed_project/paper_draft/paper_draft.tex` (T1–T11, P1–P11, L1–L7, F1–F4, Pb1–Pb4,
C1, C9) and `Proposed_project/proofs/` (AI-proved, AI-reviewed, **not adopted**, written for the 14 Oct target with
unstandardised y).

| # | Target | Builds on | Consultants' difficulty |
|---|---|---|---|
| V1 | **Reduction and normalisation:** the §5 reduction; parameter maps; normalised capped prior; compact-rate envelopes for s_y² under bounded signal. | eq. (m), P1 | routine |
| V2 | **Dimension, no supersets, support and PIP consistency** for the v3 target: Π(\|S\| > m_n \| y) → 0; Π(S₀ \| y) → 1 at O_P(√(log n/n) + e^{−ω_n}); max_j \|PIP_j − 1{j∈S₀}\| ≤ 1 − Π(S₀ \| y); HPM consistency; screening of strong signals without full beta-min. Requires redoing T6–T8, T10 uniformly in the empirical IG rate and with g = (n − 1) + 1. Posterior-error rates ≠ frequentist selection-error rates. | T6, T7, T8, T10 | substantial |
| V3 | **Contraction:** squared prediction rate (s₀ + 1) log²(p ∨ n)/n without beta-min, improving to (s₀ + 1) log(p ∨ n)/n under polynomial p and sparse eigenvalues; coefficient rate divided by φ₀²; variance contraction with a diverging multiplier on n^{−1/2}; raw-scale back-transformation. Centred C9 to be re-examined. | T9, T9a, C9 | substantial |
| V4 | **Sharp orthogonal threshold:** for centred orthogonal designs (G = (n − 1)I, D = n exactly), the HPM transition at λ_n = (n − 1)θ²/σ*² ≈ τ_n = log n + 2 log((2p − s₀)/s₀), limit Φ(c)^{s₀}, exceeding the minimax centre 2 log(p − s₀) by log n + O(1). | Pb1, P4 | substantial |
| V5 | **Exact start and kernels:** the convolution sampler and Z̄₀; every boundary case; Hastings ratios; the independence step's acceptance and its minorisation constant inf_S π₀(S)/q_φ(S); self-adjointness of the random-order round. | P1, P6 | routine |
| V6 | **Fixed-data Monte Carlo validity of the final run, conditional on calibration:** unbiased linear-scale Ẑ_r; O(1/N) relative mean-square error and conditional CLTs for Ẑ and RB-PIPs as N → ∞ (multinomial resampling); joint evidence–PIP identities and R-consistency of the secondary pooling; unconditional limits are Gaussian mixtures over the calibration. Not conditioned on passing diagnostics or numerical completion. | P6, P7, P11, F1 | routine |
| V7 | **All-scored HPM discovery and combined recovery:** P(S* never scored \| calibration) ≤ (1 − π₀(S*))^Q with Q = 4N_e(1 + T + L + 4) independent π₀ draws (initial and independence proposals); combined with V2: P(Ŝ ≠ S₀) → 0 under any one of (a) Q·π₀(S₀) → ∞, (b) the no-switch regime (V8), (c) burn-in correction (V9); plus numerical score-gap and completion probabilities. | P9, T5 | routine to substantial |
| V8 | **No-switch regime:** under (CS), (NL), beta-min, sparse eigenvalues: π₀(S₀) → 1 for the actual blocks (start-side concentration and a dimension bound for π₀, which cannot use T6's density identity); then HPM = S₀, PIPs → 0/1, Ẑ/Z → 1 under the actual growing budgets. | T2(i), T3, T11, L3, T8 | substantial |
| V9 | **Burn-in correction (component theorem):** for fixed p and Γ ≻ 0, w.p. → 1 the Gibbs dynamics at φ = 1 follow coordinate ascent on F(S) = −(n/2) log σ̄²(S) − (\|S\|/2) log n, whose unique fixed point is S₀, within a constant C(Γ, β*, p) of rounds; L → ∞ eventually exceeds it. (Fixed-p production problems are eventually enumerated, so this is a component of V7/V8, not a separate production guarantee; the earlier "s₀ + 1 sweeps" claim was withdrawn.) | T3, T11(iii), C1 | routine to substantial |
| V10 | **Mixing with the cap ⌊n/2⌋:** warm-start mixing of the φ = 1 round on a working set A_n = {\|S\| ≤ d_n} plus excursion bounds, e.g. P(leave A_n within L_n steps) ≤ (L_n + 1)·W_n·π(A_nᶜ); polynomial inverse absolute spectral gap under sparse eigenvalues and beta-min (canonical paths, adapting Yang–Wainwright–Jordan to BB(1, p) and g = n; unverified route). Production/theory gap stated: L is logarithmic, t_mix may be polynomial. | T6, T7, T8 | substantial / open |
| V11 | **Evidence through discovered crossings:** (positive) if the competing pair is in V after the rebuilds and the bridge is pair-dominated (PD), the final relative evidence error is O_P(√(cT/N)) at fixed N; (negative) the pilot schedule alone gives Ẑ/Z = n^{−1/2}e^{O_P(1)} for proxy deletion and e^{−Θ(n)} for a proxy block plus a near-cancelled true variable, while E1–E3 pass. | T4, T5, L4, Pb3, Pb4 | substantial |
| V12 | **Limits of the checks:** with non-crossing kernels both diagnostic and final runs share the restricted law, so no check fires; what `checks_passed` and `local_certified` do and do not certify. | T5 | routine (mostly negative) |
| V13 | **Resources:** explicit total-work and peak-memory bounds in (n, p) under the declared budgets; numerical error of scores and its effect on decisions; probabilities of `schedule_limit`, `numerical_failure` and `resource_limit`, to be controlled in any combined recovery statement. A fixed memory allocation cannot support unrestricted growing-dimension consistency. | — | substantial |

Also to state: on the exact branch, V2–V4 are theorems about the algorithm's output directly.

Consultant cautions to carry into the theory run: the transfer of T6–T10 is substantial, not a constants check; standardised
errors are not conditionally Gaussian; "agreement among consultants identifies promising routes, it does not establish them";
Song & Liang (2015) prove target results (Theorems 1–4, Supplementary Theorem S) and treat their sampler only by citing SAMC
convergence, with the whole procedure's consistency asserted by composition — the same separation (target theory, then sampler
theory) is the template here, with our bridge replacing their split-and-merge.

## 12. Differences from the frozen v2

| Component | v2 (frozen, first deployment) | v3 |
|---|---|---|
| Target statement | as v3, prior normaliser implicit | W_K explicit; reduction statement |
| Exact branch | Σ C(p,k) ≤ 10,512p | ≤ (5H₀ + 4N₀)p, grows with the budget |
| Budgets | fixed 512 + 4 × 2,500, T_max 1,000 | N₀ = max(2,500, n, p), H₀, T₀ = max(1,000, ℓ²) (equal at the study sizes) |
| Resampling | systematic | multinomial |
| Moves | systematic Gibbs order, 1 uniform swap, B neighbour swaps | random order of all steps; independence proposal from π₀ added |
| Schedule | pilot schedule frozen for islands; step floor in production | calibration with candidate grid and rebuilds; no forced steps in the final run |
| Phases | pilot + 4 islands produce the estimates; escalation re-runs and reports tier 2 | calibration decides effort; a fresh final run produces all estimates |
| Polish | 4 rounds, PIPs over polish | L = max(4, ⌈log₂(n+1)⌉) burn-in + 4 measured rounds |
| Local search | unbounded best-improvement | ≤ ℓ moves + one scan; local certification defined |
| Ties | relative tolerance 10⁻⁹·max(1, \|best\|) | exact equality only; near-tie list informational |
| PIP pooling | equal over islands | equal (primary) and Ẑ-weighted (secondary) |
| Triggers | E1–E3 | E1–E3 + forced pilot steps, grid failure or non-convergence, `local_limit`; final flags only |
| Numerical failure | status per model | QR fallback, then `numerical_failure` (no −∞) |
| Preflight | memory | memory and wall time, before each branch and before escalation |

## 13. Open items

- Implementation and verification of v3 (none done). The v2 verification grid (`../Spec_anyXY_20261019/VERIFY_GRID_v2.md`)
  would need the v3 additions: calibration rebuilds, the grid, the independence step, and Fable-T3's adversarial cell (a proxy
  block plus a near-cancelled true variable).
- Whether the candidate-grid cost is negligible in practice (consultants differ; to be measured).
- The outer limit of B (B* = 16 is an implementation limit).
- A secondary prior arm (truncated BB(1, 1)): not now (Felipe).

## 14. Sources

- Frozen v2 and its audit: `../Spec_anyXY_20261019/` (SPEC_anyXY_v2.md, VERIFY_GRID_v2.md, REVIEW_ADJUDICATION.md,
  FABLE_C_review.md, FABLE_D_review.md, ASTRA_1_review.md, ASTRA_2_review.md, TIMING_blocksize.md).
- Theory consultation and design meeting: `../Theory_consult_20261019/` (THEORY_PACKET.md, ASTRA_T1_reply.md,
  ASTRA_T2_reply.md, FABLE_T3_reply.md, THEORY_SYNTHESIS.md; `meeting/`: MEETING_ROUND1.md, r1_*.md, MERGED_DRAFT_v3.md,
  r2_*.md, logs and prompts).
- Round-1 methodology (R1) and decisions: `../Setup_20261019/`.
- Existing theory: `../../Proposed_project/paper_draft/paper_draft.tex`, `../../Proposed_project/proofs/`,
  `../../Proposed_project/literature_theory/`.
- Song, Q. and Liang, F. (2015). A split-and-merge Bayesian variable selection approach for ultrahigh dimensional regression.
  JRSSB 77(5), 947–972. https://academic.oup.com/jrsssb/article/77/5/947/7040600 ; local copy
  `03_Literature/4_References/Song and Liang (2015) A split-and-merge Bayesian variable selection.pdf`.
