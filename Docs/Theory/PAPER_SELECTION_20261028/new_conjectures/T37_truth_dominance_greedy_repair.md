# T37: Finite-n truth dominance and deterministic greedy repair

**Status:** NEW conjecture, added 2026-10-28 to fill the "finite-n repair" hole. Source: `../FABLE_REVIEW.md` §2, adopted by HQ. Methodology SMC-BVS v3.0. Read with `../../theorems/00_COMMON.md`.

**Category / rank:** core. Primary repair route for the paper's repair theorem; the Gibbs-path route T24 is the alternative.

## Definitions used
- **Local search:** the production local search. It scores every feasible flip and swap of the centre, moves to the best strict improvement, takes at most ℓ moves, and ends with a final certifying scan.
- **Near-truth region:** 𝓡_d = {U ∪ P : U ⊆ S₀, P ⊆ S₀ᶜ, |P| ≤ d}, with s₀ + d ≤ K.
- **Gains:** g(S, l) = F(S+l) − F(S) and h(S, j) = F(S−j) − F(S); swap gains are defined in the same way.
- **TD(d, m), truth dominance with margin m ≥ 0:**
  - for every S ∈ 𝓡_d with S ⊉ S₀, some missing true variable j has g(S, j) ≥ m + the gain of every other feasible move at S;
  - for every S ∈ 𝓡_d with S ⊋ S₀, some extra l has h(S, l) ≥ m + the gain of every other move;
  - at S₀, every move has gain ≤ −m.

## Assumptions
EX-A; fixed design X and truth S₀. Clause (ii) adds G; clause (iii) adds R, SE and BM-∞, with s₀ and d fixed.

## Precise statement
- **(i) Deterministic.** Assume TD(d, 0) with strict inequalities. Then from any centre S ∈ 𝓡_d, the local search with ℓ ≥ |S Δ S₀| moves monotonically to S₀ in exactly |S Δ S₀| moves, scores S₀, and reports `local_certified` at S₀. The path never leaves 𝓡_d. Hence S₀ ∈ 𝒮, and Ŝ = S₀ whenever π(S₀) > ½ (T21).
- **(ii) Finite n.** Under G, for fixed X, P₀(TD(d, m) fails) is at most the sum, over the ≤ 2^{s₀} C(p, d)(p + s₀p) distinct move comparisons, of P₀(a single score difference falls below m).
  - Each term is a one- or two-dimensional non-central Gaussian event.
  - Its non-centrality is (n−1)δ²_{T,l}/σ*², and its penalty is ½ log(n+1) + log[(2p−k−1)/(k+1)].
- **(iii) Corollary indexed by n.** Assume s₀ and d are fixed, ℓ_n = ⌈log₂(n+p+1)⌉ ≥ s₀ + d eventually, and G, R, SE and BM-∞ hold.
  - Then the bound in (ii) → 0, so TD(d, 0) holds with probability → 1.
  - Clause (i) then becomes an unconditional repair route that replaces GAIN_d, LK_d and EXIT_d.

## Why it should be true
Each gain is a monotone function of one residual projection u_{T,l}ᵀy (two for swaps).
- Adding a missing true variable j gains the full non-centrality (n−1)‖(P_{T+j} − P_T)μ‖².
- Its look-alike l captures only the r² fraction of the same signal.
- Once S₀ ⊆ S, every null variable has zero leakage and pays the size penalty.

So the greedy order is "truths in, then extras out". That is T24's prescribed path without the randomness. The margin (n−1)θ²(1−r²)/(2σ²) between a true variable and its look-alike is also the proposed mechanism behind SMC-BVS's advantage in correlated designs (S3–S6 at c = 0.5).

## Proof route
- **(i):** induction on |S Δ S₀|, using TD.
- **(ii):**
  1. Write each comparison as a difference of quadratic forms in contrast coordinates (T01).
  2. Bound the log-ratio of the IG marginal by a Gaussian exponent, using bounded-Q_S Taylor control (as in T02's hint).
  3. Apply a union bound.
- **(iii):** plug in T03's beta-min margin.

## Main risks
- **Loose union bound.** The 2^{s₀} union in (ii) makes the finite-n number loose at s₀ = 14 (about 10 nats). A dependence-aware bound along the actual greedy path is the research part.
- **Move cap below the needed distance.** At n = 200, ℓ = 10 < s₀ + d = 15. The finite-n clause therefore needs either the one-extra-scan rule or a centre within 10 moves of S₀; state this.
- **Eligibility is not covered.** T37 does not deliver an eligible centre: some local-search centre must lie in 𝓡_d. That is T38's job.
