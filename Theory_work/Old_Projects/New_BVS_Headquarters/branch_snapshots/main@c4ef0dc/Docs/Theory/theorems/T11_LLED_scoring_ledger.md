# T11 (L-LED/T14-D): Unified scoring and discovery ledger

**Status:** conjectured, not proven. Methodology SMC-BVS v3.0 (2026-10-19), SHA-256 93043758058a6d422cca6ca4b6be8f3a9e8149b6f6de2e1bab1ce31c44b8019c. Read with `00_COMMON.md`.

**Category / rank:** algorithmic validity and discovery; **core** (lemma). Merges v2's L-LED and T14-D.

## Definitions used
Scored set 𝒮, 𝒮_cal, reported HPM Ŝ, global S†; the mechanisms (Gibbs flips, uniform swap, neighbour swaps on N(·), independence proposals and initial draws from π₀, block tables, local scans); execution-time state X_{pre-j} before coordinate j's step; Q_f = 4N_e(T+L+5); "opportunity" = a (particle, round, step) at which a mechanism could score the model; first-hit time τ; conditional hazard p_e (00_COMMON §2).

## Assumptions
EX-A, EX-S, CAL; SR for Gibbs scoring. Component execution or launch conditions are explicit.

## Precise statement
Fix S* ∈ Ω measurable w.r.t. data and 𝓒 (before final randomness).
(i) [per-mechanism rules] Gibbs coordinate j: under SR, S* is evaluated iff X_{pre-j} ∖ {j} = S* ∖ {j} (this includes the current-state case; before first discovery only the flip-neighbour case gives a new score). Uniform swap from a size-k exchange neighbour: the unique exchange producing S* is proposed with probability 1/[k(p−k)]. Neighbour swap: probability 1/[k|N(j)∖S|] if the insertion is in N(j)∖S, else 0 (degrees may exceed B). Independence proposal / initial draw: proposal probability π₀(S*), regardless of acceptance. Tables: every S* ⊆ C_b is scored when the tables execute. Local scan: given its centre, every feasible flip and swap is scored; a random centre contributes a probability after averaging, not a deterministic unconditional indicator.
(ii) [expected Gibbs evaluations] Σ_{r,i,ρ,j} P(X^{r,i,ρ}_{pre-j} ∖ {j} = S* ∖ {j}); if a round starts in stationarity every state-independent ordering prefix preserves q_φ. Actual particles are not assumed stationary.
(iii) [iid draws] P(S* absent from the final iid draws | 𝓒) = (1 − π₀(S*))^{Q_f} ≤ e^{−Q_fπ₀(S*)}. The adaptive calibration draw count is never a fixed exponent.
(iv) [stopped opportunities] For chronological predictable opportunities with success probability ≥ b, with O the count up to first success or the horizon (including the successful one): P(no hit, O ≥ D) ≤ (1−b)^D; if P(no hit, O < D) ≤ δ then P(no hit) ≤ δ + (1−b)^D. An expected count alone does not supply this premise. Generally P(τ ≤ H) = Σ_e E[1{τ > e⁻}p_e], and P(hit) ≥ bEO ≥ 1 − E(1−b)^O (a weaker bound, not an independent-trials identity).
(v) [set exposure] For a fixed set 𝓜: P(𝓜 scored) ≤ 1{𝒮_cal ∩ 𝓜 ≠ ∅} + Q_fπ₀(𝓜) + EΣ_e p_e^{noniid}, with future Gibbs, swap and local-scan opportunities in the last sum; clip at one.
(vi) [launch] On the SMC branch the unconditional final-only miss bound is P(not launched, S* ∉ 𝒮_cal) + E[1{launched, S* ∉ 𝒮_cal}(1 − π₀(S*))^{Q_f}]. Enumeration scores every feasible model.
(vii) If S† is scored, then Ŝ = S† (tie rule; NIS not needed).

## Dependencies
Builds on: T09, T10, decision rule. Used by: T20, T21, T24, T27, T28, T29, T30, T31.

## Numerical evidence (provisional)
provisional evidence (Sol check J8): exact stopped Bernoulli tree (b = 0.3): exact hit 0.51 = first-failure sum; the incorrect product expression gives 0.447; P(no hit, O ≥ 2) = 0.49 = bound. Literal Gibbs "iff" without the current-state case: FAIL. provisional evidence (Sol check J7): Q_f bounds at n = 200, p = 500 tier 0: Q_min = 140,000, Q_max = 10,130,000.

## Proof-route hint (optional)
Condition on each execution prefix; fresh proposal randomness; first-hit decomposition and sequential survival bounds; the adaptive union bound with deterministic ceilings for (v). Hardest step: ensuring a claimed opportunity lower bound holds on the no-hit event. *When proof.md is run on this file, its lead considers the statement both with and without these hints; the hints never reach the reviewers.*
