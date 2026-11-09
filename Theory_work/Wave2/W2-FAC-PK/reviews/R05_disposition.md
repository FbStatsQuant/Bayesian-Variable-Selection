# R05 disposition (L4 check, Codex Sol high: VERIFIED-WITH-AMENDMENTS)
Reviewer reply verbatim: reviews/R05_L4_check_sol.md.
1. (MAJOR, resource scope) evaluation cost of a general cap rule: applied — L4 (iii) now requires (α) a ≤ ℓ_n + 2K
   deterministically and (β) evaluation cost absorbed in the implementation constants; the three proposed rules are O(1)
   arithmetic after the start mode. STATEMENT (P4)(iii) narrowed accordingly (v3.1, flagged post-lock narrowing; weakens
   the claim's scope only). METHOD_REQUIREMENTS records the evaluation requirement.
2. (MINOR) cost factor is an upper bound: applied in L4.4 and METHOD_REQUIREMENTS ("at most r ≤ 2 times", equality only
   for scan-proportional terms; envelope increments and total runtime excluded; "doubles" replaced).
3. (MINOR) ceiling in the table: applied (ℓ_n + ⌈(1 + δ)K⌉ + 1).
4. (MINOR) CAP transfer wording: applied (positive discovery / certified-on-event / joint HPM transfer; negative
   statements only downward; flags, metadata, cap-dependent no-output events excluded; a ≥ ℓ_n required).
5. (MINOR) deterministic lower bound for max(ℓ_n + |S̃₀|, p): applied (p ≥ (17/16)K ≥ (17/16)|S̃₀| on every input, n ≥ n₀).
6. (EDITORIAL) request increment: applied (Kq(p) vs A2; 2Kq(p) vs legacy W̄).
7. (EDITORIAL) provenance (A1 HOLDS-WITH-AMENDMENTS, d315c1e council, A4 OK-WITH-FIXES) and the explicit allocation
   display: applied.
