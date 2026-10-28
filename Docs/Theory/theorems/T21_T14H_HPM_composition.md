# T21 (T14-H): Composition theorem for the reported HPM

**Status:** conjectured, not proven. Methodology SMC-BVS v3.0 (2026-10-19), SHA-256 93043758058a6d422cca6ca4b6be8f3a9e8149b6f6de2e1bab1ce31c44b8019c. Read with `00_COMMON.md`.

**Category / rank:** combined statistical and algorithmic consistency; **core** (theorem).

## Definitions used
Scored set 𝒮, 𝒮_cal; Ŝ, S†; δ₁ = 1 − π(S₀); U := the event that no usable HPM output is produced; ℱ := calibration permits the prescribed final run; Q_f = 4N_e(T+L+5); r_k (T10); stopped opportunity count O (T11(iv)); exact-branch inequality Σ_{k≤K}C(p,k) ≤ (5H₀+4N₀)p (00_COMMON §2).

## Assumptions
EX-A; EX-S for random routes; CAL for fresh-final-run formulas; SR for Gibbs scoring; G, R, SE, BM-C (through T03) for truth recovery; operational availability; the chosen route's hypothesis (HIT, PX, table inclusion, a scanned neighbour centre, or T24's hypotheses with an eligible particle). OP-s is unnecessary when calibration or tables already supply the HPM score.

## Precise statement
(C1) P{U or Ŝ ≠ S₀} ≤ P(U) + 2E₀δ₁ + P{Uᶜ, S₀ ∉ 𝒮}. The middle term → 0 by T03; the discovery term → 0 under any of:
(a) [fresh iid] P(S₀ ∉ 𝒮) ≤ P(ℱᶜ, S₀ ∉ 𝒮_cal) + E[1_ℱ 1{S₀ ∉ 𝒮_cal}(1 − π₀(S₀))^{Q_f}]; Q_fπ₀(S₀) → ∞ on launched runs suffices when the nonlaunch-and-no-earlier-hit term vanishes. If S̃₀ = S₀ ∖ {i} has normalised start mass ≥ c > 0, T10 gives π₀(S₀) ≥ c·r_{s₀−1} and a guaranteed intensity of scale N_e(T+L+5)/(p√n), which diverges for p ≲ √n (including the boundary through the logarithmic round budget); a lower bound proves no failure above that range (negative conclusions need T27's two-sided law).
(b) [Gibbs execution] If before discovery an actual Gibbs execution has X_{pre-j} ∖ {j} = S₀ ∖ {j}, SR scores S₀; round-start occupancy does not imply this.
(c) [swap execution] From the appropriate size-k proxy model, a uniform swap proposes and scores S₀ with probability b = 1/[k(p−k)] per execution; if P(no hit, O < D) ≤ δ then P(no hit) ≤ δ + (1−b)^D; PX supplies a useful D, ONE alone does not; neighbour swaps use the actual edge and 1/[k|N(j)∖S|].
(d) [tables and scans] S₀ ⊆ C_b makes S₀ table-scored; a completed scan from a flip-or-swap neighbour scores it (T20(ii)).
(e) [terminal repair] Under T24, an eligible particle selected from the available past has P(no truth score in the next H rounds) ≤ (1 − a_n)^H + Hη_n; add the probability that no eligible particle is available; for final-run repair retain the nonlaunch term; pilot repair uses the pilot's forward filtration.
(f) [exact branch] If the exact-branch inequality holds and the computation completes, Ŝ = S† and the evidence and PIPs are exact; fixed p eventually enters this branch.

## Dependencies
Builds on: T03, T10, T11, T20, T22, T24, T34. Used by: T26, T27, T29, T31.

## Numerical evidence (provisional)
provisional evidence (Sol check J7): at p = n the guaranteed one-addition intensity is of order n^{−1/2} × logs (not n^{−3/2}); one cancellation iid-cheap below a = ½ with the logarithmic factor deciding at a = ½; n = 200, p = 500, tier 0: Q_min·r₄ ≈ 49.6. provisional evidence (Sol check J12): in the n = 64, p = 18 two-cancellation instance the first truth score came from a Gibbs step in bridge stage 1 (not from the initial draws). Files: judge/sol1/J7_DISCOVERY_BUDGETS.md, judge/sol2/J12_TWO_CANCELLATIONS.md.

## Proof-route hint (optional)
Decompose failure into unavailable output, failure of strict truth optimality (T03(iii)), and failure to score truth; apply the ledger (T11) route by route; T11(vii) for Ŝ = S† once scored. Hardest step: verifying exposure or repair hypotheses at the actual budgets. *When proof.md is run on this file, its lead considers the statement both with and without these hints; the hints never reach the reviewers.*
