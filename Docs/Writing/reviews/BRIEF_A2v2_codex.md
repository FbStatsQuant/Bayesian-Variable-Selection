# Brief: Codex fidelity read of "Are the assumptions reasonable?", v2 (Writing, 2026-11-16)

You are an independent reviewer. Check one short document (5 pages plus a table) for **fidelity** to its sources.
Report findings only, and edit no file except your report. Paths are relative to `/home/fb31/BVS-wt/WRITING`. Scratch
goes in `.rc_tmp/` only; do not set TMPDIR.

## Document
`Docs/Writing/assumptions/assumptions.pdf` (LaTeX: `assumptions.tex`). Its theorem and assumption numbers refer to
`Docs/Writing/results/what_we_prove.pdf`.

## Sources
1. **Core:** `.rc_tmp/a2_sources/TRACK_B_v1.4.md` (dossiers B1–B12, the summary table, §S, §T2) and
   `.rc_tmp/a2_sources/WRITING_DELTA_v1.4.md`. TRACK_B v1.4 supersedes `TRACK_B.md` in the same folder; do not use the
   old file. Lines marked "[audit calc]" or "[audit reading]" must not be used.
2. `.rc_tmp/a2_sources/AUDIT.md` §6 (items T1–T13, X1–X5) and `CHECKPOINT_3.md`.
3. **Song and Liang (2015):**
   - the paper, `.rc_tmp/a2_sources/Song_Liang_2015.pdf` (journal page = PDF page + 946);
   - the supplement, `.rc_tmp/a2_sources/Song_Liang_2015_supplement.pdf` (sha256 a584b328c859c087…; "supp. p." = its
     page). Its pp. 13–16 may need reading as images.

   Read both with `pdftotext -layout`, and render pages as images where the text is garbled.
4. `Docs/Writing/results/what_we_prove.pdf`, for the theorem and assumption labels. TRACK_B's "Thm 1, 1′, 2, 9, 6, 10, 3"
   map to D2's Theorems 3.1, 3.4, 3.9, 4.2, 5.7, 5.19, 3.13.

## Binding format (HQ)
- §1 ¶1 must be the v1.4 headline **verbatim**.
- A one-word comparison is allowed only where the delta marks it uniform:
  - the model and exact sparsity are the same;
  - visibility implies their Condition 5;
  - they have no condition of the leakage-set, local-regression or no-leakage kind.
- Every other comparison must be one conditional sentence that names the regime, with page and equation.
- Never "our conclusions are stronger"; conclusions are compared per theorem only, as in the delta.

## What to check
- **A.** Each comparison, in the table and in the §3 paragraph heads, against the v1.4 summary table and its dossier.
  Report any one-word label outside the uniform list, and any regime split that is dropped or reversed.
- **B.** Each Song–Liang citation (page, equation, condition, theorem; supplement pages) and each quotation, against
  the PDFs.
- **C.** Each inside / outside / unclear call against v1.4.
- **D.** Evidence lines that claim more than v1.4 or the cited result.
- **E.** §2 "How the conclusions compare" against the delta's items (i)–(iii) and its sampler sentence.
- **F.** §4 against AUDIT §6.
- **G.** Any sentence that frames asymptotics or proof constants as a limitation.

## Report
Write `Docs/Writing/reviews/A2v2_codex_fidelity.md`. It is a table with these columns:
- id;
- location;
- what the document says;
- what the source says (file:line or page);
- severity: C = changes a claim, S = scope, F = could mislead, E = editorial.

End with `FIDELITY: FAITHFUL` or `FIDELITY: NOT-FAITHFUL`. Effort: high.
