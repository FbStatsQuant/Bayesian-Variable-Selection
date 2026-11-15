# SL1 disposition (lead, 2026-11-11) — review `reviews/SL1_statement_lock_sol.md`, verdict DO NOT LOCK

All eight required changes are applied in STATEMENT v1.1 (markers [SL1-#]); the four optional suggestions too.

| # | class | finding | disposition in v1.1 |
|---|---|---|---|
| 1 | CRITICAL | The mass floor is false for saturated models (|S| = K); T₁ undefined at s₀ = K; p = s₀ allowed | ACCEPTED. (FLOOR)/(T0) restricted to |S| < K; "Nothing is claimed for saturated models"; (E) now requires p > s₀ eventually; T₁ := 0 at s₀ = K; constants corrected (f_n(k) ≥ ½(n+1)^{−1/2} for k < p). §0, §6 and PLAN.md reworded. |
| 2 | CRITICAL | (S1)(b) and [ALK] need a leakage / small-gain hypothesis; the linearised step is false for gains of order n | ACCEPTED. (AL) is now a hypothesis of (T1) (all clauses) and of the uniform, transfer and corollary forms; [LEAK(Q)] is conditional on the displayed small-rate premises; (AL)'s text states the small-gain consequence via (J0); PLAN.md states the logarithmic expansion and where the linearisation is used. |
| 3 | CRITICAL | The headline rate dropped the truth-deletion and second-order terms | ACCEPTED. §0 and (T1)(b) state the full bound n^{−1/2}𝔏⁰_n + n^{−1}𝔏_n(S₀)² + o_P(n^{−κ}); IF-START gives the explicit deterministic rate r_n and keeps 1_𝒜. |
| 4 | CRITICAL | o₀/T₁ undefined when p = s₀ | ACCEPTED. p > s₀ eventually is part of (E); (T1)(c) says T₁ > 0 for that reason; §6 excludes p = s₀. |
| 5 | MAJOR | Blocks appeared in public hypotheses; theorems did not consume the interface table | ACCEPTED. §5 is split into 5.1 component lemmas (AGG, ASM, NEC-b; labelled, blocks by necessity), 5.2 bridge lemmas (one interface property each), 5.3 theorems with partition-free hypotheses only. (N2), (N3) are now partition-free (quantified over every V ⊆ S₀), derived from the component diagnostics (C2). The blanket sentence in §0 is replaced by an exact one. |
| 6 | MAJOR | C-MIS:LemR@1.0.0 is not literally PROVED-CHECKED | ACCEPTED, option (b). The reduction is re-proved locally (Lemma R′); C-MIS:LemR is no longer consumed (§7, PLAN §5). |
| 7 | MAJOR | MIS concentration needs the substituted hypotheses; random supports not covered | ACCEPTED. (T6) says each claim holds provided its hypotheses hold after substitution; random candidate designs only through (T3)(a) with deterministic β^𝒞. |
| 8 | MINOR | Complete the coded-data definitions; rename the shortened (FL-R); distinct constants | ACCEPTED. §1 "Data as scored" (C, D_x, retained p, G_S, z_S, Y, s_y, y; validity; unscaled vs scored response; pin `v3_preprocess.R:111-127`); (FL-R16); c_Σ, a_V, κ_Q distinct from the scorer's a₀ = b₀ = 0.01. |
| O1 | optional | partition-free (V*-c) recovers (V-c) | ACCEPTED: (V*-c) removed. |
| O2 | optional | κ ≥ 1 ambiguity; uniformity sentence | ACCEPTED: κ_Q named; (T1)(d) lists both visibility forms. |
| O3 | optional | display the visibility remainder; name clash C | ACCEPTED: remainders displayed in F1–F3; constants C₀, C₁, C₂. |
| O4 | optional | strong factors: "outside the proved hypotheses" | ACCEPTED: (N4), §0, §6 reworded. |

## A further change not requested by SL1 (marker [G1])
The sharpness-gate numerics (production core; `numerics/`, in progress) found v1.0's visibility hypothesis improvable:
in a fixed design where each truth has 15 close correlates (correlation 0.9), (V-c) fails over 15-sets (minimum
level 0.39 < 1 + 2A ≈ 3.2) and v1.0's functional e_n ≈ 2·10⁴, yet π₀(S₀) ≈ 0.91 with o₀ ≈ T₁. Reason: e_n charges a
truth deletion given **any** set U without the price of U itself. v1.1 therefore (i) replaces e_n in Lemma AGG by the
truth-block functional Ξ (prior-weighted table mass of every configuration of the truth's block that misses a truth),
for which o₀ ≥ c_sΞ also holds, so the functional is necessary as well as sufficient; (ii) adds the margin form (V-m)
of visibility with its bridge (B-V2); (iii) keeps (V-c) as a sufficient condition through (AGG-d) and bridge (B-V1).
No v1.0 claim is weakened by [G1]: under (V-c) the v1.0 conclusions follow from the v1.1 ones.
