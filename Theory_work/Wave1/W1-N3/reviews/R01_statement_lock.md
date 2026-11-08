# R01 — statement lock: disposition

Reviewer: Codex gpt-6.1-sol (reasoningEffort high), fresh `delegate_task`, brief = files only. Reply verbatim:
`reviews/R01_statement_lock_raw.md`. Verdict: **LOCK-AFTER-FIXES**; no counterexample to (a)–(e); reviewer independently
verified the (d) construction for every cap.

| fix | disposition |
|---|---|
| 1 scope / what stays OPEN; abstract deviation ≠ data/LH counterexample | ACCEPTED: STATEMENT §0 "Scope" paragraph |
| 2 encoding invariants; domain enlargement; exact scores vs exact tables; source pointers | ACCEPTED: (H1) rewritten; §1 paragraphs "Domain enlargement", "Exact scores vs exact tables"; `04_theory.tex:73`, `:78`; path aliases |
| 3 FP execution model, overflow | ACCEPTED: (H2-FP) with finite intermediates; (e) text notes rounding ties at prefix/prior additions; reviewer's p = 2 example to be added to `numerics/fp_example.py` |
| 4 exact vs native oracles; lossless doubles; equality-cap and FP boundary tests | ACCEPTED. Oracles: integer tables of magnitude < 2⁵³ (all sums exact in binary64, so the native run *is* an exact-arithmetic run) validate (a)–(d) natively; DATA tables are reported under the "exact tables" reading (informational) and validate (e) natively. Doubles cross the harness boundary as hex floats (`%a` / `float.hex`), integers as exact decimal. New families `cap_edge(N-1,N,N+1)` (incl. K = 0, cap = 1) and `fp_stress(e only)`. |
| 5 compute limits; seeds; n = 2 scope; review sequencing | PARTLY ACCEPTED. Seeds: 2 declared seeds (20261108, 7) ≤ 20. p ≤ 12: the ticket from HQ explicitly asks for exhaustive brute force "p <= 12" for this thread, which I read as HQ's scope exception to the p ≤ 10 default; runs take < 30 s locally. The p = 44 instance is proved analytically (L6); its run is a 1.2 s confirmation of the frozen code, not an enumeration of models. n = 2: routine-level test plus `numerics/eng10_preprocess_n2.R` asserting the public preprocessing rejects n = 2. Sequencing: PLAN updated — L1–L5 checked (falsification + Sol line-by-line) before mid-point review; L6, L-FP, L7 checked after it, before the sweep. FR05's assembly and LH replica stay HQ work (STATEMENT §0). |

Statement locked as v1.1 on 2026-11-08.
