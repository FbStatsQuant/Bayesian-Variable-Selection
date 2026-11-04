# T22 (T16): Aggregate start bounds and conditional concentration for the actual blocks

**Status:** conjectured, not proven. Methodology SMC-BVS v3.0 (2026-10-19), SHA-256 93043758058a6d422cca6ca4b6be8f3a9e8149b6f6de2e1bab1ce31c44b8019c. Read with `00_COMMON.md`.

**Category / rank:** deterministic start analysis (i)–(ii), (iv): **core** (lemma); statistical concentration (iii), (v): **secondary** (theorem).

## Definitions used
Tables r_b, γ₀, π₀, w(k) (00_COMMON §2); AGG's q_n, e_n for a feasible reference S° (s = |S°|, U_b* = S°∩C_b) with the stated conventions; u_n := (p−s)⁻¹Σ_{l∉S°} max_{S°∩C_{b(l)}⊆T⊆C_{b(l)}∖l} r_{b(l)}(T∪l)/r_{b(l)}(T); uncapped weight γ₀^{unc}(S) = w(|S|)∏_b r_b(S∩C_b); δ_n^{comp} = sup_{S⊉S°}γ₀^{unc}(S)/γ₀^{unc}(S∪S°); r_k (T10); R_i = 1/q_i(S₀) − 1 for i ∈ {0,1}; leakage quantities E_{T,l}, v_T; inventory codes VIS, NL_avg(κ), EXP, BO.

## Assumptions
EX-A for (i), (ii), (iv); G, R, within-block SE, VIS, NL_avg(κ) and EXP for (iii); T03's hypotheses for the full-endpoint conclusion in (iv); BO, SE, bounded signal energy and BM-∞ for (v).

## Precise statement
(i) [deterministic aggregation] If q_n < 1: π₀(S°) ≥ (1−q_n)^{s+1}/(1+e_n)^s and 1 − π₀(S°) ≤ (s+1)q_n/(1−q_n) + se_n. Moreover q_n ≤ u_n, so u_n < 1 permits its substitution. A further candidate bound is π₀(S°) ≥ (1−u_n)^{s+1}/[1 + (2^s − 1)δ_n^{comp}]. Conventions: empty maxima are 0; q = u = 0 if s = p; e = δ = 0 if s = 0.
(ii) [reference-to-truth odds] π₀(S₀) = π₀(S°)·[w(s₀)/w(s)]·∏_b r_b(S₀∩C_b)/r_b(S°∩C_b) exactly; if S° ⊆ S₀, successive feasible additions give π₀(S₀)/π₀(S°) ≥ ∏_{j=0}^{s₀−s−1}r_{s+j}. Normalised reference mass remains essential.
(iii) [statistical, with EXP] For fixed κ > 0: q_n ≤ u_n = O_{P₀}(2^B√(log n)n^{−κ}) when EXP's remainder is O_{P₀}(1) (exponent form 2^B√(log n)n^{−κ+o_{P₀}(1)} with an o_{P₀}(log n) remainder); EXP's visibility lower bound with M_n^V → ∞ and B ≤ 16 gives e_n = o_{P₀}(n^{−m}) for every fixed m; hence 1 − π₀(S₀) = O_{P₀}(2^B√(log n)n^{−κ} + e_n). Exact zero leakage permits κ = ½; NL_η supplies the admissible κ of the inventory. Neither substitutes for EXP.
(iv) [endpoint propagation] For 0 ≤ φ ≤ 1: 1/q_φ(S₀) − 1 ≤ R₀^{1−φ}R₁^φ ≤ max(R₀, R₁); hence inf_{φ∈[0,1]}q_φ(S₀) ≥ min{π₀(S₀), π(S₀)}. With T03 and (iii) this gives uniform concentration on [0,1].
(v) [BO] Under BO, completing the true variables in a block removes its signal leakage into the remaining coordinates of that block; with SE, bounded signal energy and BM-∞ the projection argument supplies VIS; the score conclusion still requires EXP. No over-tempered clause is retained. Start concentration implies neither schedule completion nor evidence accuracy, nor that every initial particle equals S₀.

## Dependencies
Builds on: T01, T03, T10. Used by: T21, T26, T27.

## Numerical evidence (provisional)
provisional evidence (Sol check J5): 468 table cases (adversarial and seeded), 376 applicable bounds, 0 failures, including empty, full and binding-cap references; actual partition at n = 64, p = 9, B = 3; observed EXP remainder range [−0.10, 0.17] on 20 additions (cannot establish its stochastic order); two-branch bound verified algebraically. Files: judge/sol1/J5_COMPOSITE_START.md, J5_tables.json.

## Proof-route hint (optional)
Dominate the completed-table generating function coefficientwise by exp{z(p−s)q_n}; prior ratio w(s+j)/w(s) ≤ (s+j)!/(s!(p−s)^j); Σ_jC(s+j, j)q_n^j = (1−q_n)^{−(s+1)}; charge incomplete configurations to their completions (≤ e_n per missing coordinate, (1+e_n)^s); the uncapped sum dominates the capped normaliser. (iii): truncate |Z| ≤ h_n uniformly over the ≤ p2^B table comparisons; a_l ≤ C(n+1)^{−1/2}exp{(δ+σ*Z)²/(2v_T)} by EXP; the two-branch bound gives E[·; |Z| ≤ h_n] ≤ (2h_n/√(2π))n^{−1/2}e^{E_{T,l}}; linearity and Markov, no independence. (iv): Hölder on the total odds Σ_{S≠S₀}[γ₀(S)/γ₀(S₀)]^{1−φ}[γ₁(S)/γ₁(S₀)]^φ ≤ R₀^{1−φ}R₁^φ. Hardest step: deriving EXP from primitive assumptions (the uniform block-score expansion over O(p2^B) entries). *When proof.md is run on this file, its lead considers the statement both with and without these hints; the hints never reach the reviewers.*
