# T30 (T21-X): Pilot discovery under the terminal-repair hypotheses (no loss instance containing the truth)

**Status:** conjectured, not proven. Methodology SMC-BVS v3.0 (2026-10-19), SHA-256 93043758058a6d422cca6ca4b6be8f3a9e8149b6f6de2e1bab1ce31c44b8019c. Read with `00_COMMON.md`. Lead's ruling 61: kept as an optional conjecture in the T24-conditional form; the BOCC-only form and the universal contrapositive are in DROPPED.md.

**Category / rank:** negative/limit (emptiness of a loss class under stated hypotheses); **optional**.

## Definitions used
The tier-0 pilot: H₀ particles, bridge stages, then L burn-in and 4 measured rounds at φ = 1 before the candidate grid is built; its forward filtration; 𝒮_cal; "eligible particle" = a pilot particle in 𝓡_d at the start of the pilot's φ = 1 rounds, selected from the pilot's past; a_n, η_n (T24); hidden sets 𝓜 ∋ S₀ (T28, T29).

## Assumptions
G, R, SE, BM-C (through T03), EX-A, EX-S, CAL, SR; LK_d, EXIT_d, GAIN_d for a fixed d (new); existence of an eligible particle with probability → 1; execution of the pilot's L+4 terminal rounds.

## Precise statement
(i) P(S₀ ∈ 𝒮_cal) → 1 in joint probability, with P(S₀ not scored in the pilot's terminal rounds | eligible particle) ≤ (1 − a_n)^{L+4} + (L+4)η_n → 0 (T24(ii) in the pilot's forward filtration).
(ii) Consequently, for every data-measurable 𝓜 ∋ S₀ with ∅ ∉ 𝓜, the calibration-avoidance clause of MISS-E and MISS-H fails with probability → 1: no T28 or T29 instance with S₀ ∈ 𝓜 exists under these hypotheses, and by T28(iv) no exponential evidence-loss instance exists.
(iii) Not claimed: that BOCC(d) alone implies (i) (BOCC supplies neither LK_d, EXIT_d nor GAIN_d's multi-extra deletion condition); that every loss instance violates SE, BM or bounded occupancy; that calibration discovery implies evidence or PIP accuracy (those need T26 or T25).
Open questions recorded: can G, R, SE, BM plus bounded pilot occupancy yield a pilot discovery theorem without assuming LK/EXIT/GAIN; which conditions exclude stuck multi-extra supersets; what ensures accuracy after discovery.

## Dependencies
Builds on: T03, T10, T11, T24, T28, T29. Used by: nothing (terminal).

## Numerical evidence (provisional)
provisional evidence (Sol check J12): one actual-partition instance (n = 64, p = 18, two cancelled true variables, start mass of S₀ = 1.49·10⁻⁴): S₀ first scored by a Gibbs step in bridge stage 1 round 0, later by swaps and an independence proposal; S₀ was the best scored model at the external stop; the run stopped during burn-in, so it establishes neither the hypotheses nor the asymptotic claim. provisional evidence (Sol check J4): the T24 constants.

## Proof-route hint (optional)
Apply T24(ii) inside the pilot with its forward filtration (no conditioning on the later calibration outcome); then T28(iv)'s truth/superset consequences. Hardest steps: deriving LK, EXIT and multi-extra GAIN from a primitive statistical regime (H1–H2 of the council's objections: the maximiser changes before its update and internal moves interfere; H3: pilot discovery needs a trajectory argument, not the polynomial path bound; H4: stuck supersets with ≥ 3 extras). *When proof.md is run on this file, its lead considers the statement both with and without these hints; the hints never reach the reviewers.*
