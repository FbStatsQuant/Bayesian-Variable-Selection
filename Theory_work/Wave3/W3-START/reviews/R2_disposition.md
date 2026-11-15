# Council round R2 — disposition (lead, 2026-11-11)

Frozen content: `reviews/MANIFEST_R2.txt`, digest `5e26bb8b58f98718959378cff18789927c6a8a1e881e3d77af06ae1ccb2e9885`
(52 files: the ticket files of STATEMENT v1.3.4 and 18 external inputs). Blind first reads (briefs
`BRIEF_R2_sol.md`, `BRIEF_R2_opus.md`); six gates G1–G6. Run on the merged tree (branch at 49df4a4).

| seat | model, provider, effort | score | gates | file |
|---|---|---|---|---|
| sol | Codex gpt-6.1-sol, codex, reasoningEffort high | 9.2 | PASS (G1–G6) | `reviews/R2_council_sol.md` |
| opus | Claude Opus 5.5, Claude Work, effort high | 8.9 | PASS (G1–G6) | `reviews/R2_council_opus.md` |

**Council PASSED in round R2**: both seats ≥ 8.0, all six gates PASS, same manifest. `manifest.py bind`: "bind: OK, 2
review(s) give a PASS verdict (>= 8.0)"; council cell:
`R2; MANIFEST 5e26bb8b58f98718959378cff18789927c6a8a1e881e3d77af06ae1ccb2e9885; sol=9.2 PASS(reviews/R2_council_sol.md); opus=8.9 PASS(reviews/R2_council_opus.md)`.
`manifest.py verify` passes on the current tree. Every id of `REPORT.md` §3 is "accepted" by both seats (opus: F1, BR,
OVL with non-blocking remarks).

**Reconciliation (rule 15, rounds ≥ 2):** `reviews/RC_R2_reconciliation_sol.md` — ALL EARLIER CRITICAL/MAJOR FINDINGS
RESOLVED: yes. R1's ten non-blocking issues: nine RESOLVED, O2 NOT APPLIED (owner's rule on asymptotic results; "no
mathematical defect or missing theorem hypothesis follows"). SC5 findings 1–2: RESOLVED. SC4 #1, BR1 #1 and #3,
SW1 #1: STILL RESOLVED. Changes of meaning introduced by v1.3.4: none. No remaining edit requested.

## Non-blocking issues of round R2 — NOT applied
Seat sol: none. Seat opus: six. The frozen content must stay unchanged after the passing round (LIFECYCLE §4.1 A4),
so none is applied; each is recorded with the lead's reading, for the next version.

| # | issue | lead's reading |
|---|---|---|
| O1 | `REPORT.md:72-92`, `:103-111`: every `STATEMENT.md:<line>` reference starts one line early; several single-line references point at the neighbouring row | correct, and the lead's error: v1.3.4 added one line at `STATEMENT.md:65-66` and the report's references were not shifted; SC5 and `citecheck.py` (existence of ranges only) did not catch it. Ids and names in the report are right. The registry blocks of `CHECKPOINT_3.md` §10 carry the corrected spans. Repair for the next version: shift the references by one; extend `citecheck.py` to compare the first words of a cited row with the claim's label |
| O2 | `STATEMENT.md:185`: the P-OVL row of the §4 interface table reads as if the general P-OVL were delivered; (T5) and the report state the production form correctly | correct; write "production form (SAMP `STATEMENT.md:104`): P-START, or Proposition OVL". The registry block of OVL already says "production form" |
| O3 | `lemmas/L9_BR.md:110`: ξ, R, E_R, E_ξ are undefined when μ̃ = 0 (which does not occur on E_cov) | correct; add "if μ̃ = 0 put E_R = E_ξ := the sure event" |
| O4 | `lemmas/L6_COROLLARIES.md:26`: "C_n, C′_n = O((log n)²)"; C_n = O(log n), as L6.1 and L6.3 use | correct; state the two orders separately |
| O5 | `STATEMENT.md:271`: the η = 0 sentence of F1 needs the premise stated just before it | correct; "With η = 0, under the premise above, …" |
| O6 | `STATEMENT.md:254` "every ε > 0" against ε ∈ (0, 1) in `lemmas/L5_ASM_STARTF.md:40` | cosmetic; align the two (the bound is trivial for ε ≥ 1) |

No finding of either seat concerns a proof step, a hypothesis or a constant of a claim.
