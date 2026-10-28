# T26 (T17): No-switch consistency at the actual budgets

**Status:** conjectured, not proven. Methodology SMC-BVS v3.0 (2026-10-19), SHA-256 93043758058a6d422cca6ca4b6be8f3a9e8149b6f6de2e1bab1ce31c44b8019c. Read with `00_COMMON.md`.

**Category / rank:** combined consistency corollary; **secondary**.

## Definitions used
Δ_n := 1 − inf_{φ∈[0,1]}q_φ(S₀); δ₁, u_π, ρ_* (00_COMMON §2); b_n := 2(T+1)Δ_n/(1 − Δ_n); f_T(S₀ᶜ) (T15); the final run, Ẑ_r, Ẑ, PIP̂_{rj}, primary and secondary PIPs, MPM̂; T ≤ T_e = O(log²n) on a successful construction.

## Assumptions
G, R, SE, BM-C (through T03), VIS, NL_avg(κ), EXP (through T22(iii)), EX-A, EX-S, CAL; OP-a for the required initial execution; OP-s for evidence/PIP availability; the relaxed EXP remainder suffices when it preserves a fixed positive polynomial decay exponent.

## Precise statement
T22(iv) and T03 give Δ_n ≤ max{1 − π₀(S₀), δ₁} and (T+1)Δ_n → 0 in probability. Then:
(i) [evidence] By T14 with S° = S₀, for each fresh final island and for the pooled evidence, E_𝓒|Ẑ_r/Z − 1| ≤ b_n and E_𝓒|Ẑ/Z − 1| ≤ b_n; including the vanishing operational noncompletion probability, Ẑ/Z → 1 and log Ẑ − log Z → 0 in joint probability. No over-tempered condition is used.
(ii) [PIPs and MPM] By T15 with c = ½: E_𝓒f_T(S₀ᶜ) ≤ 2δ₁ + P_𝓒(Ẑ_r/Z < ½) ≤ 2δ₁ + 2b_n; counting initially incorrect particles as bad and charging departure from truth during the remaining rounds by (L+4)ρ_*, the recording-prefix argument (T23(ii)) gives E_𝓒max_j|PIP̂_{rj} − 1{j∈S₀}| ≤ 2δ₁ + 2b_n + (L+4)ρ_* + u_π, also for the primary average; the right side → 0 in probability, giving uniform PIP consistency, MPM̂ = S₀ with probability → 1, and (all four island errors vanishing jointly) consistency of the secondary PIPs.
(iii) [HPM] Start concentration makes an initial iid pilot draw equal S₀ with probability → 1 whenever that initialisation executes, so T21 yields HPM recovery without successful final scheduling; alternatively T21(a); on the exact branch T03 applies directly.
(iv) [limits] Not derived: OP-s, a bounded stage count, absence of forced steps, reliable diagnostic flags, or any uniform Monte Carlo rate (the old √(log p/N_e) rate is withdrawn).

## Dependencies
Builds on: T03, T14, T15, T21, T22, T23 (recording argument). Used by: T31. T19 and T25 are separate stronger-hypothesis alternatives.

## Numerical evidence (provisional)
provisional evidence (Sol check J6): the first-moment and occupancy inequalities used here (judge/sol2/J6_FIRST_MOMENTS.md). provisional evidence (Sol check J5): EXP remains unresolved.

## Proof-route hint (optional)
Combine T22(iv) with T14(i) for (i); per-island lower tail from (i) into T15, then the prefix-stability argument of T23 for (ii); convert conditional bounds to joint probability with bounded tail probabilities without turning an O_{P₀} statement into a frequentist mean rate. Remaining obligations: EXP and operational completion. *When proof.md is run on this file, its lead considers the statement both with and without these hints; the hints never reach the reviewers.*
