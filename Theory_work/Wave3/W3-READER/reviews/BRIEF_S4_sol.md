# BRIEF — S4: Sol statement-change check, W3-READER (pre-CP3; PROTOCOL_v4 §4.2), 2026-11-16

You are an independent reviewer (Sol, effort high, one pass). Repository root (worktree):
`/home/fb31/BVS-wt/W3-READER`, branch `theory/W3-READER` at HEAD (main merged in at a0f0a266). Ticket folder:
`Theory_work/Wave3/W3-READER/`. **Write exactly one file:** `Theory_work/Wave3/W3-READER/reviews/S4_statement_change_sol.md`.
No other writes, no git state changes, no TMPDIR and no writes outside the worktree; scratch only in
`/home/fb31/BVS-wt/W3-READER/.rc_tmp/` (git-ignored), and delete it after (D62).

## What you review
Frozen snapshot `Theory_work/Wave3/W3-READER/reviews/S4_frozen/` (verify first: `cd reviews/S4_frozen && sha256sum -c MANIFEST_S4.txt`).
The previous reviewed snapshot is `reviews/S3_frozen/` (Opus diff check `reviews/S3_diffcheck_opus.md`, disposition
`reviews/S3_disposition.md`; earlier Sol line check `reviews/S2_linecheck_sol.md`, disposition `reviews/S2_disposition.md`).
Diffs S3 → S4: `S4_frozen/DIFF_*_S3_to_S4.diff` (READER_VERSIONS, CLAIMS_CARD, NOTATION, METHOD_INTUITION, REPORT, lemmas R3, R4).
Every change since S3 is in scope. The update logs ("#### Update log (thmK)") and the card's version lines list each change
with its tag. The changes are:
1. S3's findings and their repairs (S3_disposition), and the S2 repairs re-tagged in S3.
2. H5 cards 6–7 consequences (row 1.1 PASS-with-open-items; abstract wording of rows 1.1/Thm 1′, 3.1/3.2; row 3.6 to the body).
3. D-17 wording (moderate-n mixture remarks; METHOD_INTUITION).
4. Registry status refreshes at main f526e45b and 33e1f0f5 (SL0 cleared; POST2 C/E/A1/A0/D; W2-APP:POST@1.0.6; W3-SAMP).
5. Row 1.1 Forms A / B1 (abstract) and Theorem 1′ wording.
6. Row 3.7 forms and Theorem 8′.
7. Three applied swaps: thm3 v0.4 (W3-PSHARP-R READER_DELTA v0.4), thm4 v0.5 (W3-MISR-R READER_DELTA v0.4 @93e50640),
   thm8 v0.6 (W3-SCR-R2 READER_DELTA v4 @048b6b23); sources are the deltas named in each update log.
8. Card v1.3 Song–Liang fixes (rows 1.1, 1.4, 2.2, 3.1) and the corrections of commit 98e1daf3, checked against the
   paper by `S4_frozen/inputs/SL_PDF_CHECK.md` and `SL_PDF_CHECK_card.md` (paper:
   `Papers/Core_bibliography/32_2015_Song_Liang_*.pdf`; spot-check at least the row 1.4 and row 1.1 citations).
9. FUNI-N: delivery clauses of Theorems 6–7 and card 3.1/3.2 narrowed (bounded domain 𝔇 under (S4)(i)–(iv); every n under
   A:IDEAL-W⁺, defined in `S4_frozen/inputs/A_IDEALW_PLUS.md`, a carrier copy of dept/theory fc30c749); sentence [RM2R-5]
   (source `/home/fb31/BVS-wt/W3-RM2-R/Theory_work/Wave3/W3-RM2-R/reviews/post_cp3/READER_DELTA_v-next.md` §7); lemmas R3
   (target and IDEAL-W row) and R4 (remark) take A:IDEAL-W⁺ / 𝔇 as a hypothesis; REPORT R3 block. Check that **no reader
   text claims every-n delivery under plain IDEAL-W**. F-UNI's narrowed statement is in
   `/home/fb31/BVS-wt/THEORY-DEPT/Theory_work/Dept/research/FUNI_NARROW/` (L5_delivery_F-UNI_v2.patch, DIFF_sol.md). F-UNI is
   quoted as "narrowing to 2.1.0, requote after S2"; that is expected (not a finding) until the recorder's task S2 lands.
10. **Not applied, fidelity read only:** the card-13 proposal `S4_frozen/proposal/DELTA_row21_thm9_DIST.md` (+ A/B diffs;
    master `/home/fb31/Bayesian-Variable-Selection/Theory_work/Wave3/W3-DIST/STATEMENT.md` v1.4.10 §1R; earlier reads F9,
    F9c, F9d in `/home/fb31/BVS-wt/THEORY-DEPT/Theory_work/Dept/research/DIST_thm9_fidelity/`). One FIDELITY verdict line for it.

## What to check, per changed statement
- **Statement-change tag.** Each changed reader statement (theorem text, assumptions, conclusions, card "Result" cell) carries
  a tag EQUAL / WEAKER / STRONGER relative to the S3-frozen text (or, for a swap, to the delta). Confirm or correct each tag.
  WEAKER is acceptable only when it restores or follows the master's own premise or narrowing; say which master line.
- **Fidelity to the master** (omitted premise, changed quantifier, dropped condition, wrong scope, rate or constant drift).
- **Statuses** quoted verbatim from `Theory_work/INFRA/registry/claims.tsv` at HEAD (or the stated commit), with every
  "conditional on …" carried; nothing below PROVED-CHECKED presented as checked; no internal ids in reader-facing sentences.
- **D71:** list every interpretive sentence that is new or changed since S3 and judge it (FAITHFUL / NOT, with the source).
- House rules: asymptotics are never framed as a limitation; no n₀-size or "huge constants" remarks except the HQ-mandated
  sentence [RM2R-5] (code limits); "explicit constants, not optimised".

## Output format
Integrity line; then findings `[S]` (statement/fidelity), `[F]` (faithfulness of a status or premise), `[C]`
(correctness), `[E]` (editorial), each with file:line in S4_frozen, the defect, and a proposed repair; a tag table (one row
per changed statement: location, lead's tag, your tag); the D71 list; then exactly these closing lines:
```
TAGS: CONFIRMED | CORRECTED (list)
FIDELITY (applied text): FAITHFUL | NOT-FAITHFUL
FIDELITY (card-13 proposal): FAITHFUL | NOT-FAITHFUL
OMITTED-PREMISE: NONE | <list>
VERDICT: PASS | FIXES-NEEDED | FAIL
```
