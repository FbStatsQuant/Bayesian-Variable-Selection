# W1-N3 — Proof of Theorem N3-code (index)

Target: `STATEMENT.md` v1.3 (locked). The proof is split into lemma files (64K-output rule); this file only maps clauses to
lemmas and records the dependency order.

| clause | proved in | uses | hypotheses |
|---|---|---|---|
| reduction argmax π₀ = argmax f; lex order on internal = original indices | `lemmas/L1_reduction.md` (i), (iv) | D0, preprocessing order | (H1) |
| union-order fact (lex on equal-size sets = min of symmetric difference) | L1 (iii) | — | — |
| per-block maxima, argmax lists | `lemmas/L2_block_maxima.md` | — | (H1), (H2); (H4) for the C++ execution |
| DP table M[b][k] = V_b(k); size selection kbest = k*, lg0 = max f | `lemmas/L3_L4_dp_and_size.md` | L2 | (H1), (H2); (H4) for the C++ execution |
| enumeration: tightness (A), call tree ↔ 𝒜* (B), DFS order (C), cap semantics (D) — key lemma | `lemmas/L5_enumeration.md` | L1(iii), L2, L3, L4 | (H1)–(H3); (H4) for the C++ execution |
| **(a)–(d)** assembly; deviation family D_m (every cap; p = 44 for cap = 10⁶) | `lemmas/L6_assembly_and_deviation.md` | L1–L5 | (H1)–(H3); (H4) for the C++ execution (not for the mathematical family) |
| **(e)** floating point | `lemmas/LFP_floating_point.md` | L2's comparison part | (H1) incl. inverse maps, (H2-FP), (H3), (H4) |
| **(f)** tie-aware DP (reference algorithm) | `lemmas/L7_tie_aware_dp.md` | L1(iii), L3 argument | exact arithmetic |

Order of checks: R01 statement lock → R02 batch 1 (L1–L5) → R03 re-check (L1, L5 attempt 2) → R04 mid-point (CONTINUE) →
R05 batch 2 (L6, L-FP, L7) → R06 exhaustive sweep → council.

Numerical companion: `numerics/README.md`.

Scope (from STATEMENT §0 and L6 "What this does and does not close"): N3 is proved for the frozen `start_mode`
conditionally on N ≤ cap; the specified truncation fallback is absent; e4 for the emitted centre of an integrated LS0 is
not discharged; the deviation is on abstract tables only.
