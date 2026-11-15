# SC4 disposition (lead, 2026-11-11) — review `reviews/SC4_diff_check_sol.md` (Codex gpt-6.1-sol high, blind)

Manifest `26e9e50976f67a4f31e94498395a339d158cf569bb4334b4485666c13cd69734` quoted; `manifest.py bind` OK.
Verdict: **ACCEPT WITH CHANGES** (1 MAJOR, 1 MINOR, 3 optional). All applied; STATEMENT v1.3.1 is LOCKED with them.

| # | class | finding | action |
|---|---|---|---|
| 1 | MAJOR | (T7) called the example families "Verified in this ticket" and cited `lemmas/L11_EXAMPLES.md`, which was not in the frozen packet | applied verbatim: the label reads "Proposed examples (verification remains a proof obligation of this ticket; `lemmas/L11_EXAMPLES.md`)". The verification is written in L11 and goes through its own line check; its status is reported in the REPORT, not in the statement |
| 2 | MINOR | the orthogonal entry attributed the exact order n^{−1/2} to orthogonality alone | applied verbatim: the entry now carries F2's conditions (s₀ ≥ 1, fixed nonzero signal strengths bounded away from zero and bounded above, p/√log n → ∞) |
| O1 | optional | give the constants of the fifteen-correlate example | applied: ρ² = 0.4, θ*₁² = 2(1 + 2A)σ² log n/(n − 1), p = min(⌊n^A⌋, n − 1), A ∈ [0.1, 1] |
| O2 | optional | account for the old stand-alone isolated-leaker entry | applied: the new entry says it replaces it |
| O3 | optional | historical numerics still cite (N2) for small supports | applied: one note at the top of `numerics/RESULTS.md` |

Reviewer's classification of the four v1.3.1 items, recorded for HQ: item 1 ((N2) scope) editorial clarification of
unchanged formal claims plus a narrowing of the informal necessity reading; item 2 ([TK]) editorial; item 3 ((B-R),
C_L = 0) **substantive narrowing of a bridge conclusion**, with (T3)(b)'s two conclusions unchanged and still following;
item 4 ((T7)) narrowing of the example families. The reviewer also confirmed that (N2) is non-vacuous for s₀ ≥ 16 (an
explicit construction), that (N3) has no similar vacuity, and that no hypothesis or conclusion of (C0), (C1), (T0),
(T1) or of the proved bridges changed.
