# T31 (T22): What the reported checks and certificates can establish

**Status:** conjectured, not proven. Methodology SMC-BVS v3.0 (2026-10-19), SHA-256 93043758058a6d422cca6ca4b6be8f3a9e8149b6f6de2e1bab1ce31c44b8019c. Read with `00_COMMON.md`.

**Category / rank:** validity and certification limits; **core** (proposition).

## Definitions used
Reported quantities: Ẑ, the bound 0.05Ẑ, island SD of log Ẑ_r (E2), E1, E3, low_empirical_ESS, local_certified, global_certified; Z_W := Zπ(W) (distinct from the comparator mean r_WZ); Z_V := Σ_{S∈V}ϖ(S)m(S); Q_f; thresholds t fixed before final randomness; weight comparability ratio C_eq.

## Assumptions
EX-A, EX-S, CAL; MISS-E/CPL-E for (iii)–(iv); the usability, threshold-measurability or external-bound assumptions stated in the clauses.

## Precise statement
(i) Under T12: P_𝓒(Z ≥ αẐ) ≥ 1 − α and E_𝓒 log Ẑ ≤ log Z; so 0.05Ẑ has coverage at least 95% under the ideal final-run assumptions; it is not a relative-error interval; conditioning afterwards on final flags does not preserve this coverage automatically.
(ii) [estimator-class example, not a regression construction] For 0 < a, ε < 1, an unbiased nonnegative estimator equal to aZ with probability 1−ε and to Z{1 − (1−ε)a}/ε otherwise has four independent copies all equal to aZ with probability (1−ε)⁴: zero log dispersion with arbitrarily severe underestimation. Independence and agreement give no uniformly informative multiplicative-accuracy certificate over this class.
(iii) Under T28, diagnostics measurable from the evidence coupling have the comparator's law up to h_n^E; score/search diagnostics need T29's information control; passing transfers only if the comparator passes with high probability; calibration flags are fixed given 𝓒, recomputed final E2 is not.
(iv) [upper bounds] If U uses only coupled information and P_{ref,𝓒}(U^W ≤ CZ_W) ≥ 1 − α′ with CZ_W < Z, then P_𝓒(Z ≤ U) ≤ h_n^E + α′ on that loss instance; not an unconditional impossibility theorem.
(v) [discovery after selection] For a threshold t fixed before final randomness: P_𝓒{∃S : π₀(S) ≥ t, S missed by the iid draws} ≤ min{1, ⌊1/t⌋e^{−Q_ft}}; and with probability ≥ 1 − δ every model with Q_fπ₀(S) ≥ log[1/(δπ₀(S))] has been scored (usable after selection). Substituting π₀(Ŝ) into a fixed-model miss formula is invalid as a competitor certificate; neither statement shows all better-posterior models have large start mass.
(vi) local_certified has exactly T20(i)'s meaning; global_certified is restricted to completed validated enumeration; a genuine external U ≥ Z would certify the best scored model globally whenever U − Z_V < max_{S∈V}ϖ(S)m(S) (v3 supplies no such U).
(vii) Restricted ESS controls only T13's restricted moment; grid equality across rebuilds certifies neither omitted mass nor mixing; if M models have unnormalised weight ratio ≤ C_eq at a temperature, V captures at most C_eq|V|/M of their mass; "near-equivalent" without a quantitative condition supplies no bound.

## Dependencies
Builds on: T12, T13, T11, T20, T28, T29 (and T05–T07, T27 for interpretation). Used by: nothing (terminal interpretation).

## Numerical evidence (provisional)
provisional evidence (Sol check J7): exact finite law p = (0.4, 0.3, 0.2, 0.1), 3 draws: fixed-model miss 0.216, all-above-0.25 miss 0.532, selected-threshold competitor miss 0.54 vs naive 0.545 (conditional on the selected label: 1 vs 0.74); fixed-threshold union bound 0.559. provisional evidence (Sol check J8): information-transfer corrections.

## Proof-route hint (optional)
Markov and Jensen; the explicit rare-tail law; information-preserving coupling (T17); at most ⌊1/t⌋ atoms of mass ≥ t for the union bound; allocate error δπ₀(S) per atom for the simultaneous statement; T13 for (vii). Hardest step: none in the algebra; a verified production loss instance is the difficult premise. *When proof.md is run on this file, its lead considers the statement both with and without these hints; the hints never reach the reviewers.*
