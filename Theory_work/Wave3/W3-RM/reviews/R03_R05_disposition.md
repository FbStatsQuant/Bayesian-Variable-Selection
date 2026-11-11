# R03 and R05 dispositions (lemma checks, Codex gpt-6.1-sol high)

Reviewer replies verbatim: `reviews/R03_L0L1L2_check_sol.md`, `reviews/R05_E4_check_sol.md`.

## R03 (L0_core, L1_fixed, L2_NAF)
Verdicts: RM-0(a), (b) VERIFIED; B1, B2, B3, B3', B4, B6 VERIFIED; NA-F VERIFIED-WITH-AMENDMENTS; N-loc => (N-D)(i)
VERIFIED-WITH-AMENDMENTS; RM-F VERIFIED. No FATAL/MAJOR.
| # | finding | disposition |
|---|---|---|
| 1 MINOR | empty family (P = empty set, U_n empty) not handled in NA-F / N-loc | applied in `lemmas/L2_NAF.md` [R03-1] |
| note | onset n0 depends on the rate envelopes | wording added in Step 3 |
Reviewer's own numerical probe: 960 lattice pairs, no violation. Files added AFTER R03 and therefore not covered by it:
Lemma B1' (`L1_fixed.md`), `L1b_rss.md` (Lemma tau, B2tau), the entropy budget h < 1/2 in `L2_NAF.md` [P1], the archive
corollary in `L0_core.md` [P7] — all sent to the mid-point review and the sweep.

## R05 (L5_E4 against the code)
Verdict: VERIFIED-WITH-AMENDMENTS. No FATAL/MAJOR. Numerical falsification by the reviewer: production header compiled
standalone, 12,000 random instances (many exact ties, empty blocks, K > p), 84,000 calls, 0 failures; 7,301 truncated
calls per tie_dp value (all fallback calls returned a maximiser).
| # | finding | disposition |
|---|---|---|
| 1 MINOR | citations RUN:391, 411 should be RUN:392, 410 (+ ENGINE:60, 70) | applied [R05-1] |
| 2 NIT | restate \|C_b\| <= 31, vector extents, representability; say whether the domain is enlarged | applied [R05-2] |
| 3 NIT | cap condition; "every feasible flip"; guard rejection after LS0; "no completed output" | applied [R05-3] |
