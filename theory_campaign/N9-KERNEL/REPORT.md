# N9-KERNEL report: V5 (kernel reversibility, self-adjoint round, exact start sampler) against the production code

## 1. Headline
The audit checked every sub-claim of N9 against `Scripts/SMC_BVS/core/cpp/` @ `39db138`. v3.1 does not change the step
functions, so the audit covers v3.1 too. Every sub-claim is **PROVED (candidate)**: exact arithmetic, iid U[0,1) uniforms,
and a score that is a function of the sorted model (true in the code). None is FALSE and none is a GAP. The exact
kernels of the **production** step functions, extracted by scripted uniforms and threshold bisection, satisfy detailed
balance to ≤ 2.3e-12 relative. This holds on 3 designs (n = 20, p = 6 and 8; n = 10, p = 8 with the cap K = 5) × φ ∈ {0, ½, 1}.
Two mutated controls fail at O(1): a neighbour swap without its Hastings factor, and an independence step without its
proposal ratio. So the check has power. Detailed balance holds only up to floating-point rounding and the 2⁻⁵³ RNG grid
(quantified in PROOF §5). No code change is needed.

## 2. Verdict table

| # | Sub-claim (statement in PROOF.md) | Code | Verdict | Numerical check (CHECK.md) |
|---|---|---|---|---|
| 1 | Gibbs flip j: heat bath for γ_φ on 𝒮_K; addition at |S| = K is a self-loop. Reversible. | `v3_engine.h:113-132` | **PROVED (candidate)** | DB rel ≤ 2.0e-14; cap exercised (C) |
| 2 | Uniform swap: q = 1/(k(p−k)), symmetric; acceptance 1∧γ′/γ; self-loop at |S| ∈ {0,p}; size-preserving, so it never leaves 𝒮_K. Reversible. | `:146-159` | **PROVED (candidate)** | ≤ 8.2e-14; |S| = p exercised (A, B) |
| 3 | Neighbour swap: q = 1/(k·|N(j)∖S|); acceptance 1∧(γ′/γ)·|N(j)∖S|/|N(l)∖S′| is the exact Hastings ratio for any symmetric loop-free graph, any degrees; the cap B acts before the symmetric union; reject at N(j)∖S = ∅; self-loop at ∅. Reversible. | `:162-180`; graph `v3_blocks.h:149-173` | **PROVED (candidate)** | ≤ 1.1e-13; factor ≠ 1 on 31–61 % of proposals; control without the factor fails (DB rel 0.5–0.75) |
| 4 | Independence move: S′ ~ π₀, acceptance 1∧e^{φ(d′−d)} is the exact MH ratio. Z̄₀ cancels, and the move needs only law(draw_pi0) ∝ γ₀ = exp(lg0), which holds (row 7). Reversible. | `:182-192` | **PROVED (candidate)** | ≤ 2.3e-12; control with symmetric acceptance fails (rel 1.0) |
| 5 | The order is a uniform permutation (Fisher–Yates, m−1 fresh uniforms read before any step), independent of the state; m = p+B+2 fixed. | `:193-214` | **PROVED (candidate)** | all m! choice vectors → m! distinct permutations, m ≤ 8 |
| 6 | Any reversal-invariant, state-independent random order of γ-reversible kernels is self-adjoint. Exact condition: all steps reversible at the same φ, order law invariant under reversal, order independent of the state (a random step count is fine under the same two conditions). A fixed order is not self-adjoint. | — | **PROVED (candidate)** | round DB rel ≤ 5.6e-14; fixed order 0.68–0.999 at φ > 0; production `one_round` MC matches R (27 χ² tests) |
| 7 | `draw_pi0` draws exactly from π₀ = ϖ∏r_b/Z̄₀ on 𝒮_K: size from ϖ(k)F_J(k), block sizes backwards from e_b(j)F_b(r−j)/F_{b+1}(r) (telescopes), sub-model ∝ r_b within its size class. The capped prior enters through the truncated convolution, which is exact for indices ≤ K. Ties play no role. | `v3_start.h:101-176` | **PROVED (candidate)** | DFS law vs γ₀/Z̄₀: max rel ≤ 2.0e-13, TV ≤ 5e-16; production-RNG χ² p = 0.51, 0.97, 0.33 |
| 8 | Z̄₀ = Σ_{|S|≤K} ϖ(S)∏_b r_b(S∩C_b), exact up to floating point (long-double log-sum-exp). | `:122-135` | **PROVED (candidate)** | vs brute force ≤ 4.5e-16, vs independent long-double spec value ≤ 1.3e-14 |

**Answers to the specific questions.**
- (a) Unequal degrees: handled, because the factor uses the available degrees |N(j)∖S|, |N(l)∖S′|. An asymmetric graph is
  impossible (`v3_blocks.h:170` symmetrises). Capped degrees: the cap B acts before the union and does not matter for
  the proof.
- (b) The cap K and ∅: Gibbs excludes additions at K. Swaps preserve the size. π₀ has support 𝒮_K. No move ever proposes
  a set outside 𝒮_K, so nothing needs to be rejected for leaving the support.
- (c) Uniform swap at |S| = 0 or p: a self-loop that consumes no uniform.
- (d) In the independence move, Z̄₀ cancels from the acceptance ratio. Z̄₀'s exactness matters for log Ẑ =
  log m(∅) + log Z̄₀ + Σ log inc (`v3_engine.h:299`), not for the move.
- (e) Data-dependent inputs: the blocks, tables and graph are built from (X, y) once per setup, before any island, and
  never depend on particles. State-dependent inputs: only the Gibbs feasibility, the self-loop rules and |N(j)∖S|, all
  covered by the proofs. The adaptive pilot φ depends on the population, but it is the schedule, not the kernel: each
  round is γ_φ-reversible for the φ it is given.
- The task text's "γ_φ ∝ prior·m^φ·π₀^{1−φ}" has an extra ϖ^{1−φ}. The spec and the code use γ_φ = ϖ·BF^φ·∏r_b^{1−φ}
  ∝ (ϖm)^φ π₀^{1−φ}. The code's lgphi matches this spec formula to ≤ 2.3e-14 (CHECK §2). This is a notation point only.

## 3. Consequences
Nothing is FALSE, so no method result is affected:
- **Unbiased Ẑ_r** (V1(a), T12/T31): needs exact iid π₀ initial draws (row 7), the exact Z̄₀ (row 8), and a
  γ_{φ_t}-invariant move after each reweight-resample (rows 1–6). Invariance is enough; reversibility is more than
  needed. All three hold.
- **PIP identities** (RB marginal PIP, primary estimator): need only that every step is γ₁-invariant and that the order
  is independent of the state. Then the state just before each Gibbs step j is π-distributed, and E[o_j] = π(j ∈ S).
  Both hold.
- **Self-adjointness** (row 6) is used where reversibility is required: spectral and variance arguments, and the
  rejection of C10. It holds for the round as drawn, not for a single realised order.
- **The 2,400-fit study**: not affected. It ran the same `core/` kernel code (the only commit touching `core/`). V5 can
  get a registry row: "N9/V5 PROVED (candidate), code-checked at 39db138, numerical check CHECK.md".

## 4. Departures at floating-point level (PROOF §5; no fix recommended)
1. Acceptance `u < α` with u on the 2⁻⁵³ grid: the probability is ⌈α2⁵³⌉/2⁵³, so it is 2⁻⁵³ instead of α when
   α < 2⁻⁵³. The error is at most 2⁻⁵³ per step, and it did not occur in the checks.
2. The π₀ categoricals are cumulatives of doubles: TV(π̂₀, π₀) = O(J·K·2⁻⁵³) (measured: ≤ 5e-16).
3. lg0 + φd does not cancel the composite exactly at φ = 1: the target is changed by a relative O(ε|c|), and the
   reversibility is not changed.
4. One shared stream per island: harmless under (H-U). It is relevant only to reproducibility (the v3.2 per-particle
   streams item).

## 5. Needs escalation
- An independent line-by-line review of PROOF.md §1–3 (all are candidates), especially the telescoping in Claim S and the
  adjoint argument in Claim R.
- Whether the theorem statements should carry (H-U) and "exact arithmetic" as explicit hypotheses, plus a remark
  bounding the effects in §4.

## 6. Outside scope
- METHODOLOGY_v3 §11 lists, under V5, the independence step's minorisation constant inf_S π₀(S)/q_φ(S). This is not part
  of N9 as stated and was not examined.
- The adaptive pilot schedule makes φ_t depend on the population. Unbiasedness under an adaptive schedule is a separate
  question; the pilot is calibration only, and the final islands use a frozen grid.

## 7. Confidence card
| Target | Refined statement | True | Provable cheaply | Crux | Method change |
|---|---|---|---|---|---|
| N9 / V5 | Rows 1–8 above, under (H-U), exact arithmetic, deterministic score | high | yes (done, candidate) | the Hastings factor needs graph symmetry, enforced at `v3_blocks.h:170`; the π₀ backward sampler telescopes | none |

Files: `PROOF.md` (statements, code quotes, proofs), `CHECK.md` (method and tables), `scripts/` (harness, order check,
build, runner, summariser), `results/` (raw outputs and `summary.txt`).
