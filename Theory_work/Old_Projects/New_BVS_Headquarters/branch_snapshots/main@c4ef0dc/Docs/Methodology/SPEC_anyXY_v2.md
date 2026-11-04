# SMC-BVS v1: complete specification for any (X, y), version 2

Lead (Opus 5.5), 2026-10-19. Supersedes `SPEC_anyXY.md` (kept for the record). Changes come from the four-reviewer audit;
each is traced in `REVIEW_ADJUDICATION.md` (R# below). Status: proposal; nothing implemented. Items marked **[PERSON]**
change a choice Felipe made or accepted.

**Principle.** Input: X (n × p), y (n), one integer seed s. Every setting is (i) a modelling convention with a stated reason,
(ii) an explicit function of (n, p) or of X, or (iii) a declared resource budget. Nothing depends on the true support, the
signal strength, the study sizes or past results. Accuracy is not guaranteed by any setting; it is what the verification
(`VERIFY_GRID_v2.md`) measures, and claims are limited to the verified envelope. Global optimality of the HPM is never claimed.

## 1. Input checks and preprocessing

| Step | Rule |
|---|---|
| 1.1 | Non-finite entries → stop, status `invalid_input`, list them. No imputation. |
| 1.2 | Require n ≥ 3, p ≥ 1. |
| 1.3 Constant columns | Drop column j **only if all its values are exactly equal** (R5). p_eff = number kept; dropped columns listed, never selected. If p_eff = 0: return Ŝ = ∅, PIPs and evidence unavailable, status `no_predictors`. |
| 1.4 X | Stable two-pass standardisation: centre (subtract the mean computed after dividing by max \|x_ij\|), then divide by the sample SD (denominator n − 1). ‖x_j‖² = n − 1. |
| 1.5 Constant y | **Only if all values are exactly equal** (R5): return Ŝ = ∅ (the exact HPM: Q ≡ 0, D ≥ 1, w decreasing), PIPs and evidence **unavailable** (R6), status `y_constant`. |
| 1.6 y | Same stable centring and SD-scaling. |
| 1.7 Collinear columns | Kept. Report connected components of the graph \|r_jl\| ≥ 1 − 1e-10. Duplicates split PIP mass (the MPM may exclude both); documented, not changed. |
| 1.8 Resource preflight (R4) | Estimate memory for XᵀX (8p_eff² bytes) and block tables (§4) and work for the start; if above the declared budget (default: the job's memory allocation), stop with status `resource_limit` and the estimates. |

Everywhere below p means p_eff.

## 2. Target posterior (unchanged from v1; accepted by Felipe)

```text
standardised working model:  y | β_S, σ², S ~ N_n(X_S β_S, σ² I)          (no intercept; y centred and scaled)
β_S | σ², S ~ N_k(0, n σ² (G_S + I)^(-1)),   G_S = X_SᵀX_S,  z_S = X_Sᵀy     g = n, τ = 1
σ² ~ IG(0.01, 0.01)
ϖ(S) ∝ w(|S|) 1{|S| ≤ k_max},  w(k) = B(1+k, 2p−k)/B(1, p) = ½ / C(2p−1, k),  k_max = min(p, ⌊n/2⌋)
log m(S) = log C_n − ½ [log det H_S − log det(G_S + I)] − (a0 + n/2) log(2b0 + Q_S),
H_S = (n+1)G_S + I,   Q_S = yᵀy − n z_Sᵀ H_S⁻¹ z_S,   C_n = (2b0)^{a0} Γ(a0 + n/2) / (π^{n/2} Γ(a0))
```

Reasons, corrected where the audit found the v1 argument wrong:
- g = n: unit information. τ = 1: one pseudo-observation on the standardised scale. BB(1, p): depends on p only; the prior
  the project's theory covers. Its extra cost over a uniform-on-size prior is log((2p−k−1)/(p−k)) per variable, ≈ log 2
  only when k ≪ p (R21). k_max: guard against near-interpolating models; ½ is a declared restriction, not needed for
  propriety (A2).
- IG(0.01, 0.01) (R9): proper, as the proofs need. Its effect on a comparison of two models is at most
  n·b0·|1/Q₁ − 1/Q₂|: it vanishes near a decision boundary (Q₁ ≈ Q₂) and is dominated by the gap otherwise. (v1's
  "4% of Q, ≤ 0.1" argument was the wrong bound.)
- Exponent a0 + n/2 after centring is a declared choice (the integrated-intercept form would use n − 1); it favours larger
  models by at most ½ log(n + 1) nats (FC).
- "Evidence" means the evidence of this standardised working model, not a raw-data marginal likelihood (R20).

**Numerics (R7).** Log-determinants from Cholesky factors; no explicit inverses or determinants. Q_S by subtraction, and
recomputed by the non-negative form Q = ‖y − X_Sβ̂‖² + (‖X_Sβ̂‖² + ‖β̂‖²)/n, β̂ = nH⁻¹z, whenever Q < 1e-8 · yᵀy
(the subtraction has then lost most of its digits). Log-sum-exp for every sum of
weights, profile convolution and evidence. A failed Cholesky gives status `numerical_failure` for that model's score
(score −∞, counted and reported).

## 3. Decision and outputs

- HPM: argmax of log score over every model scored (exact branch: over all models). Tie (R8): models within
  1e-9·max(1, |best|) of the best form a tie set; report the set; the returned representative is the smallest |S|, then
  lexicographically smallest.
- PIPs: Rao–Blackwellised average over the 4 polish sweeps at φ = 1, over particles and islands (exact branch: exact).
  MPM = {j : PIP_j > ½}; it may exceed k_max (documented, not forced).
- Evidence: log Ẑ per island and pooled (log of the mean of Ẑ_r); full scale (with C_n) and relative to m(∅).
- Status ∈ {exact, ok, escalated_ok, escalated_unresolved, y_constant, no_predictors, invalid_input, resource_limit,
  numerical_failure}. Schema field `checks_passed` (not `converged`, R16) = status ∈ {exact, ok, escalated_ok}.
- Truth is never an input. Diagnostic (g) = truth's score vs the HPM's score, and whether the truth is **retained** in the
  stored top-40p (R18); "ever scored" is not claimed.

## 4. Algorithm

**Branch 1: exact enumeration (R1).** If E = Σ_{j=0}^{k_max} C(p, j) ≤ N_total · p, with N_total = 512 + 4 × 2,500 = 10,512
(i.e. enumerating costs no more scores than one stage of the sampler), score every model with |S| ≤ k_max, streaming:
running HPM, log-sum-exp evidence, exact PIPs. Status `exact`. This holds for p ≤ 17 whenever n ≥ 20, and for larger p when
the cap binds (p ≤ 34 at n = 10, p ≤ 251 at n = 6–7, all p tested up to 3,000 at n ≤ 5).

**Branch 2: SMC** (otherwise).

| Component | Rule | Type |
|---|---|---|
| Block size | **B = min(⌊√n⌋, ⌊√p⌋, B*)**, B* = 16 (the current engine's limit; raised only with a new implementation) (R3). n = 100: 10; n = 200: 14. | Felipe's rule + implementation limit |
| Blocks | Complete linkage on 1 − \|r\| (X only); cut top-down, splitting any node with > B members; pack clusters greedily in dendrogram order into blocks of ≤ B. Ties in merge order: lowest index first. The block count is ≥ ⌈p/B⌉ (packing leaves gaps). | rule |
| Block tables | All 2^{\|C_b\|} sub-models per block scored against the full y; r_b(U) = m(U)/m(∅); α = 1. **Not inserted in the score cache.** Every scored sub-model counts for the HPM. (B ≤ k_max for n ≥ 3, so no sub-model exceeds the cap.) | rule |
| Start | π₀ ∝ ϖ ∏_b r_b; exact size-convolution draw; Z₀ exact (needs ϖ to depend on S only through \|S\|, true here). | rule |
| Bridge | q_φ ∝ π₀ exp(φ d), d = log BF − Σ_b log r_b; weights exp{(φ_t − φ_{t−1}) d}. | rule |
| Stage | Reweight; systematic resampling; one systematic Gibbs sweep over 1..p (an addition at \|S\| = k_max is excluded); one uniform swap; R_nb neighbour swaps. | rule |
| Uniform swap | Skipped if \|S\| ∈ {0, p}. Delete j uniformly from S, add l uniformly from outside S; accept min{1, q_φ(S′)/q_φ(S)}. | rule |
| **Neighbour graph** | N(j) = the partners l with \|r_jl\| > r_n = √(2 log p / n) (beyond the typical largest of p null correlations at sample size n), always including j's single largest-\|r\| partner, keeping at most the B largest; then symmetrised (l ∈ N(j) ⇔ j ∈ N(l)). Replaces m = B (R11). | function of X, n, p |
| Neighbour swap | Skipped if S = ∅ (R2). Delete j uniformly from S; if N(j) \ S = ∅ reject; else add l uniformly from N(j) \ S; accept min{1, [q_φ(S′)/q_φ(S)]·\|N(j)\S\|/\|N(l)\S′\|}. **R_nb = B** swaps per stage (work budget: B scores, about B/p of a sweep). | rule + budget |
| Schedule | Pilot: largest φ with ESS ≥ 0.90 N (weight CV² ≤ 1/9), by 60 bisection halvings; step floor 1/T_max with T_max = 1,000 (resource limit). n_forced = floored stages, reported. Stage count logged (no 100-stage warning). | budget |
| Particles | Pilot 512, frozen schedule; 4 islands × 2,500. | budget |
| Polish | 4 rounds of the full move set at φ = 1. | budget |
| Local check | Best-improvement over all p + k(p − k) flips and swaps of the HPM (additions beyond k_max excluded); move and repeat until none improves; ties lexicographic. | rule |
| Memory | Score cache 500p, stored top 40p models; HPM tracked over every scored model, including evicted ones. | budget |
| Seeds | One user seed s; L'Ecuyer-CMRG streams: 0 pilot, 1–4 islands, 5 tier-2 pilot, 6–9 tier-2 islands. Accepted s: 1 to 2³¹ − 1. Single-threaded scoring. | rule |

## 5. Self-check and one escalation tier

Computed after islands, polish and check:

| Trigger | Rule | Principle |
|---|---|---|
| E1 | Some island's best score is more than 1 nat below the overall best (R13; benign near-ties no longer trigger) | a missed mode worth a factor e in posterior odds |
| E2 | SD of log Ẑ_r across islands > 1 nat | evidence not known within a factor e |
| E3 | The local-optimality check improved the HPM | the sampler stopped short of a local mode |

n_forced > 0 and "HPM first found in polish or check" (mode-loss warning) are reported, not triggers (R13).
If any trigger fires: rerun once with streams 5–9, 4× particles (2,048; 4 × 10,000), a new adaptive pilot schedule, polish and
check. Recompute E1–E3, stop. HPM = best over both tiers; Ẑ and PIPs from tier 2 only. Work and time are recorded; the tier
has its own schedule, so its cost is not bounded by a fixed multiple (R14).

## 6. Acceptance (details and thresholds in `VERIFY_GRID_v2.md`)

1. Independent reference scorer (separately written, naive formulas) agrees with the production scorer on random models.
2. Exact branch and SMC branch both checked against independent enumeration where enumeration is feasible.
3. Target invariance: scores of a fixed model set unchanged (to 1e-9 relative) under column permutation, y → a·y + b
   (a ≠ 0), and X-column affine maps; exact-branch HPM tie sets unchanged. SMC: agreement rates, not path identity (R8).
4. Every status branch reached by a constructed input.
5. Historical regression at p = 500 on the archived 14 Oct inputs (now at
   `/projects/ml75/fb31/BVS/archives/Oct14_paired_inputs_copy_20261019/production`), at B = 5 and B = 14: disagreements
   are scored under both targets; only a better model under the old target certifies an old search failure (R10).

## 7. Open

- Neighbour graph rule (§4) replaces m = B: **accepted by Felipe for now (2026-10-19).**
- Reviewers (Fable C, Astra 2) note that √n has no statistical role in B (blocks depend on X only); **Felipe keeps the
  rule (2026-10-19).** The cap B* = 16 is his own earlier "min(√n, √p, B*)" with B* the implementation limit.
- Verification at full size (`VERIFY_GRID_v2.md`, 10× reference runs): **accepted by Felipe (2026-10-19).**
- Outer limit: raising B* needs a C++ start (TIMING_blocksize.md: about B ≤ 20).
- Secondary prior arm: not now (Felipe).
- Implementation and verification of all of the above.
