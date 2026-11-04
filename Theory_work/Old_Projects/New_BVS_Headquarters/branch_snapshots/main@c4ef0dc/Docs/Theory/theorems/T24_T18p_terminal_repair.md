# T24 (T18′): Conservative terminal repair with a fixed extra-variable budget

**Status:** conjectured, not proven. Methodology SMC-BVS v3.0 (2026-10-19), SHA-256 93043758058a6d422cca6ca4b6be8f3a9e8149b6f6de2e1bab1ce31c44b8019c. Read with `00_COMMON.md`.

**Category / rank:** conditional positive convergence; **secondary** (theorem).

## Definitions used
𝓡_d = {U∪P : U ⊆ S₀, P ⊆ [p]∖S₀, |P| ≤ d}, fixed d ≥ 1, s₀+d ≤ K; Λ_n^all = max_{T∈𝓡_d}Σ_{l∉S₀∪T}o_l(T,1); ξ_n (EXIT_d); g_n^±, g_n = min(g_n^+, g_n^−) (GAIN_d; an empty family has minimum +∞); D = 2^{s₀+d}; c_n = 1/(s₀+d+B+2)!; ρ_* (T23); a_n := [c_n{1 − (s₀+d)e^{−g_n}} − DΛ_n^all − ρ_*]_+; η_n := min{1, (B+3)DΛ_n^all + ξ_n}.

## Assumptions
EX-A, EX-S, SR; fixed s₀, d; LK_d, EXIT_d, GAIN_d (new); T03's hypotheses for truth stability; CAL for final-run use; pilot use requires the pilot's forward filtration; statistical verification uniform before selecting a state.

## Precise statement
(i) inf_{x∈𝓡_d}K₁(x, S₀) ≥ a_n and sup_{x∈𝓡_d}P_x(first exit from 𝓡_d during one round) ≤ η_n. Under T03 and the inventory's logarithmic leakage/exit limits, (L+4)(η_n + ρ_*) → 0; since B ≤ 16, c_n has a fixed positive lower bound, and GAIN_d gives a_n ≥ c_n/2 eventually with probability → 1.
(ii) [HPM repair] For a particle in 𝓡_d selected from the available past: P(no truth score in H terminal rounds) ≤ (1−a_n)^H + Hη_n; with H = L+4 this is a discovery route needing neither HIT nor ONE. Availability of an eligible particle and operational execution are separate.
(iii) [PIP repair] T23 applies with r₀ = 1, a = a_n, η = η_n, ρ = ρ_*, plus a vanishing expected stage-T fraction outside 𝓡_d (independently or via T15).
(iv) [gain sub-conjectures] Under G, R, SE, BM-∞ a uniform projection-gain argument is proposed to derive g_n^+ → ∞ for fixed d (conversion to exact integrated log-score gains is an obligation); for d = 1, T03's global margin gives g_n^− → ∞; for d ≥ 2 a favourable single deletion from every proper truth superset remains an explicit GAIN_d assumption.
The v2 slot constants 1/(s₀!d!) and the treatment of EXIT_d as internal-change control are withdrawn (internal non-Gibbs moves can change the greedy maximiser without exiting 𝓡_d).

## Dependencies
Builds on: T03, T09, T11, T23. Used by: T21 (route e), T30.

## Numerical evidence (provisional)
provisional evidence (Sol check J4): enumerated component (n = 8, p = 4, d = 1): internal non-Gibbs changes with probability 1.0 while ξ = 0.29 (EXIT does not bound internal changes); conservative ordering constant 1/(s+d+B+2)! = 1.98·10⁻⁴ there; the segment argument for leakage supports η ≤ (B+3)DΛ + ξ. provisional evidence (Sol check J12): the two-cancellation pilot prefix (n = 64, p = 18) scored S₀ via Gibbs before any particle visit; stopped before burn-in completed. Files: judge/sol2/J4_REPAIR_BASIN.md, J12_TWO_CANCELLATIONS.md.

## Proof-route hint (optional)
Freeze the initial extra set P; prescribe greedy missing-true additions with P fixed, then greedy extra deletions, with all initially present true labels and all B+2 non-Gibbs labels afterwards (relative-order probability ≥ c_n); suppress fresh outside additions (≤ DΛ_n^all over the ≤ D subsets of S₀∪P on the path); charge failed designated Gibbs decisions by (s₀+d)e^{−g_n} and later truth departure by ρ_*. Leakage in an arbitrary round: partition the Gibbs updates into ≤ B+3 stretches between non-Gibbs labels, restart the suppressed comparison after each internal swap or independence reset, count non-Gibbs first exits by ξ_n. Hardest steps: statistical bounds for LK and EXIT; the multi-extra deletion condition. *When proof.md is run on this file, its lead considers the statement both with and without these hints; the hints never reach the reviewers.*
