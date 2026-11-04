# N9: numerical checks against the production engine

## 1. Method

**Production code, not a re-implementation.** `scripts/n9_harness.cpp` and `scripts/n9_order.cpp` `#include` the
production headers in `Scripts/SMC_BVS/core/cpp/` without changing them. The only shim is three R symbols named in
`v3_runtime.h:29-31` (`SEXP`, `Rf_isNull`, `Rcpp::XPtr`), which are never called. Compiler flags are those of
`Makevars.v3` (`-O2 -fno-math-errno -ffp-contract=off -march=x86-64-v2`). Setup follows `cpp_setup`
(`v3_core.cpp:269-300`): `data_init`, `make_blocks`, `build_tables`, `build_start`, `neighbour_graph`, with the
production B = min(⌊√n⌋, ⌊√p⌋, 16) (`v3_preprocess.R:22`).

**Exact kernels of the production step functions.** For every state S ∈ 𝒮_K, `Engine::step_gibbs / step_uswap /
step_nswap / step_indep` are called with a scripted `VariateSource`:
- each discrete choice floor(u·k) is driven with u = (a+½)/k, a = 0..k−1, so each branch has weight 1/k (the
  continuous-uniform idealisation (H-U); the grid-level deviation is measured in §4);
- the proposal is read from `Engine::tmpQ` after the call; a harness assertion checks that the uniform-swap map
  (a,b) ↦ S′ is injective, that the empty-candidate branch of the neighbour swap is a pure self-loop consuming one
  uniform, and that |S| ∈ {0,p} (uniform swap) and S = ∅ (neighbour swap) consume no uniform;
- the acceptance probability is the threshold of the accept uniform, found by bisection on the production RNG's 2⁻⁵³
  grid (`v3_util.h:60`). It is the production acceptance, not a recomputed formula;
- Gibbs: o_j is read from `rb_acc` (recorded before the draw, `v3_engine.h:128`), and cross-checked against the
  bisected threshold (agreement ≤ 1 grid unit everywhere);
- the independence proposal law is the exact law of `draw_pi0`, obtained by a depth-first interval search over the
  uniforms `draw_pi0` consumes (each categorical is monotone in u, so every index is one interval on the grid). Each
  leaf gives a uniform path, which is then replayed through `step_indep`; a harness assertion checks that the replay
  proposes the same model.

The **only mirrored line** is the count |N(j)∖S| used to enumerate the neighbour-swap branches (`v3_engine.h:169`).
The acceptance (including the Hastings factor) comes from the production call.

**Round kernel.** R = (1/m!) Σ_σ K_{σ(1)}⋯K_{σ(m)} over all m! orders of the m = p+B+2 labelled steps, computed exactly
by a dynamic programme over label subsets (V(T) = |T|⁻¹ Σ_{t∈T} mult(t)·K_t V(T∖t), with the B identical N labels
collapsed). R is then compared with Monte Carlo runs of the **production** `Engine::one_round` (production xoshiro256**
stream, production Fisher–Yates `draw_order`).

**Metrics** (π = γ_φ normalised over 𝒮_K, in long double): row-sum error; ‖πK − π‖₁ (invariance); DB abs =
max_{S≠S′} |π(S)K(S,S′) − π(S′)K(S′,S)|; DB rel = the same divided by the larger flow, over all pairs, and over pairs
with both flows > 1e-13.

**Negative controls** (power of the check; mirrored copies of `v3_engine.h:162-192` with one deliberate mutation):
(i) a neighbour swap without the factor |N(j)∖S|/|N(l)∖S′|; (ii) an independence step that accepts with
1 ∧ γ_φ(S′)/γ_φ(S), i.e. without the π₀ proposal ratio. Plus (iii) the fixed canonical order G1..Gp, U, N1..NB, I.

**Designs** (seeded; `scripts/run_all.sh`):

| tag | n | p | K | B | design | states | Hastings factor ≠ 1 on |
|---|---|---|---|---|---|---|---|
| A | 20 | 6 | 6 = p | 2 | AR(1), ρ = 0.8 | 64 | 120 / 256 neighbour proposals |
| B | 20 | 8 | 8 = p | 2 | factor groups {0,1,2} r≈0.9, {3,4} r≈0.6 | 256 | 544 / 896 |
| C | 10 | 8 | **5 < p** (cap binds) | 2 | as B, n = 10 | 219 | 244 / 798 |

The graphs have unequal degrees (A: 2,3,3,4,2,2; B: 4,2,2,1,2,1,1,1; C: 2,2,2,2,2,2,1,1). Each graph is symmetric and loop-free
(the harness checks this). Design A and B include |S| = p (K = p); design C has the size cap K = 5 < p. Each design is run at
φ ∈ {0, 0.5, 1}. (Designs A–C would go to the exact branch in production (M §6.2). The kernels are the same functions
at every (n, p), so the checks apply to the general-p code paths.)

How to reproduce: `~/.config/bvs-hq/owls/owls_run -j 1 -- bash theory_campaign/N9-KERNEL/scripts/run_all.sh`, then
`python3 theory_campaign/N9-KERNEL/scripts/summarise.py`. The run took about 2 minutes on one core.

## 2. The code's target equals the spec (M §5, §6.3)

An independent long-double implementation of log m(S) (M §5: Gaussian elimination for log det H_S, log det(G_S+I), Q_S)
agrees with the production scorer to ≤ 1.9e-14 on all states. The spec's log γ_φ = log ϖ + φ(log m − log m(∅)) +
(1−φ)Σ_b log r_b, built from that independent log m, agrees with the production `lgphi` up to a constant to ≤ 2.3e-14
(all designs, all φ). (`results/*.txt`, lines `[spec]`.)

## 3. Elementary moves and the round (`results/summary.txt`; maxima over φ ∈ {0, 0.5, 1})

| kernel | max ‖πK−π‖₁ | max DB abs | max DB rel | verdict |
|---|---|---|---|---|
| Gibbs, every j (cap rule in C) | 1.9e-16 | 6.9e-17 | 2.0e-14 | reversible to rounding |
| uniform swap (self-loop at |S| ∈ {0,p} in A, B) | 1.1e-16 | 9.1e-18 | 8.2e-14 | reversible to rounding |
| neighbour swap (unequal degrees) | 1.6e-16 | 2.4e-17 | 1.1e-13 | reversible to rounding |
| independence (π₀ proposal) | 9.9e-16 | 2.1e-17 | 2.3e-12 | reversible to rounding |
| **round, uniform random order** | 1.2e-15 | 5.6e-17 | 5.6e-14 | **self-adjoint to rounding** |
| fixed canonical order, φ > 0 | 9.0e-16 | 1.2e-2 | 0.999 | invariant, **not** self-adjoint |
| fixed canonical order, φ = 0 | 1.0e-15 | 1.7e-17 | 2.9e-13 | self-adjoint (see note) |
| control: nswap without Hastings factor | 0.18 | 1.4e-2 | 0.75 | **fails**, as it must |
| control: indep with symmetric acceptance | 0.44 | 4.3e-2 | 1.00 | **fails**, as it must |

In these designs DB rel over all pairs equals DB rel over pairs with flows > 1e-13: no acceptance probability fell below
2⁻⁵³, so the grid effect of PROOF §5.1(a) did not arise.

*Note on the fixed order at φ = 0.* There the independence step accepts every proposal, so K_I = 𝟙π₀ᵀ. Because I is
the last label of the canonical order, the product is 𝟙π₀ᵀ, which is trivially self-adjoint. At φ > 0 the fixed order is
not self-adjoint, as M §6.5 says ("an individual realised order is not").

**Production `one_round` vs computed R.** We ran 27 Monte Carlo tests: 3 designs × 3 φ × 3 start states (∅, the
largest state, a middle state), with 1e5 rounds (2e5 for A). The χ² p-values range over 0.008–0.985. The smallest,
0.008 (C, φ = 0, start state 109), is unremarkable among 27 tests (Bonferroni 0.22). The TV distance is at the
sampling-noise scale. So the production round, with its own RNG stream and its own Fisher–Yates order, has the kernel R.

## 4. Round order (`results/order.txt`)

We drove the production `draw_order` through all m! choice vectors, for p ≤ 4, B ≤ 2 (m = 4..8). Each time the m!
choice vectors gave m! distinct permutations: a bijection, so the order is uniform under (H-U), and the set of
permutations is closed under reversal. Grid level: P(floor(u·k) = a) on the 2⁻⁵³ grid differs from 1/k by a relative
≤ 6.0e-15 for k ≤ 64. So the order law, and every uniform choice in the steps, is uniform to O(k·2⁻⁵³).

## 5. Start sampler and Z̄₀ (`results/*.txt`, lines `[start]`)

| design | log Z̄₀ (build_start) − brute force Σ_{𝒮_K}γ₀ | − independent long-double spec value | max rel. error law(draw_pi0) vs γ₀/Z̄₀ | TV | χ² of production-RNG sample |
|---|---|---|---|---|---|
| A | 1.2e-16 | 2.7e-15 | 6.5e-14 | 1.7e-16 | N = 2e6: χ² = 62.0, df 63, p ≈ 0.51 |
| B | 4.5e-16 | 1.3e-14 | 2.0e-13 | 4.7e-16 | N = 1e6: χ² = 214.1, df 255, p ≈ 0.97 |
| C (cap K = 5) | 1.0e-16 | 2.2e-16 | 4.7e-14 | 9.4e-17 | N = 1e6: χ² = 226.6, df 218, p ≈ 0.33 |

The "independent" value recomputes w(k), W_K, every r_b and the sum over 𝒮_K from the independent log m in long
double. The DFS gives one leaf per state of 𝒮_K, no duplicate leaves, no state with zero mass, and total mass 1 to
7e-16. In design C the capped size prior and the truncated convolution are exercised: no set with |S| > 5 is ever drawn.

## 6. What the checks do not cover

- Rounding-level departures (PROOF §5): measured here at ≤ 2.3e-12 relative. The 2⁻⁵³-grid effect on acceptance
  probabilities below 2⁻⁵³ is not exercised by these small designs; it is bounded analytically (PROOF §5.1).
- p ≤ 8, B = 2 only (B = 3 needs p ≥ 9; the 512-state round DP would need about 30 min, and the step-level checks do
  not depend on B except through the graph, which is already irregular here). The proofs do not depend on p or B.
- The checks idealise the stream as iid (H-U). The 53-bit grid is quantified in §4. Correlations of the generator
  are out of scope.
