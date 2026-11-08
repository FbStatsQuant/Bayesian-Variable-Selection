# R07 — council round 1: disposition

Reviewers (fresh `delegate_task`s, package only, told not to read reviews/ or LOG):
Codex gpt-6.1-sol (reasoningEffort high) → `reviews/R07_council1_sol_raw.md`;
Claude Opus 5.5 (effort high, claude-personal) → `reviews/R07_council1_opus_raw.md`.

| reviewer | G1 | G2 | G3 | G4 | G5 | G6 | score |
|---|---|---|---|---|---|---|---|
| Sol | PASS | PASS | PASS | PASS | PASS | PASS | **9.3** |
| Opus | PASS | PASS | PASS | PASS | PASS | PASS | **8.6** |

**Council PASSED in round 1** (both ≥ 8.0, all gates passing in the same round). Both rebuilt the harness from the frozen
header in their own scratch folders and reproduced the saved outputs (incl. the p = 44 counterexample).

Point deductions and disposition (all applied after the round; wording only, STATEMENT → v1.3):
| point | disposition |
|---|---|
| Sol 1 (−0.4): integer exactness explanation overbroad | FIXED: README separates representability from sum exactness and states the explicit bound (values ≤ 10⁹, ≤ 23 terms ⇒ |sums| ≤ 2.3·10¹⁰ < 2⁵³). |
| Sol 2 / Opus 1 (−0.3 / −0.4): v1.1 labels, H4 missing in PROOF.md and L-FP summary | FIXED: labels → v1.3; H4 added in PROOF.md rows and L-FP header. |
| Opus 2 (−0.2): L5(B) description of the line-234 reset | FIXED: reset runs after each j's inner loop; every later call is preceded by a fresh assignment. |
| Opus 3 (−0.2): (d) "every cap and instance" ambiguous | FIXED: restricted to D_m with cap ≤ 2^m under (H4). |
| Opus 4 (−0.2): callers / O-LS0 context | FIXED: STATEMENT §0 "Callers" (prototype `v3_core.cpp:274,710`, default cap; O-LS0's `cpp_ls0_start_mode` not in repo; mode unique in 2,400 fits, `O-LS0/REPORT.md:102-103`). |
| Opus 5 (−0.1): lex-order transport proved only for equal sizes | FIXED: L1(iv) extended to all sets (entrywise strictly increasing map preserves `lexicographical_compare`, incl. the prefix rule). |
| Opus 6 (−0.1): (c) bound with K; duplicated-columns remark | FIXED: N ≤ C(p,k*) ≤ max_{k≤K} C(p,k); duplicated columns named as the known source of exact ties (citation `METHOD_v3.1_FINAL.md:182`, `CODE/v3_preprocess.R:73-93,128`). |
