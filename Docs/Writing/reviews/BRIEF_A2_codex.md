# Brief: Codex fidelity read of the advisor-report section "Are the assumptions reasonable?" (Writing, 2026-11-16)

You are an independent reviewer. Check one short document (about 5 pages plus a table) for **fidelity** to its sources.
Findings only; do not edit any file except your report. Paths are relative to `/home/fb31/BVS-wt/WRITING`. Scratch goes in
`.rc_tmp/` only; do not set TMPDIR.

## Document
`Docs/Writing/assumptions/assumptions.pdf` (LaTeX: `assumptions.tex`). Theorem and assumption numbers in it refer to the
companion section `Docs/Writing/results/what_we_prove.pdf`.

## Sources
1. **Core:** `.rc_tmp/a2_sources/TRACK_B.md` (theory/W3-AUDIT @ 56dafbdd): dossiers B1–B12 and their summary table. Every
   verdict, citation and inside/outside call in the document must match it. Lines that TRACK_B marks "[audit calc]" or
   "[audit reading]" are unchecked and must not be used.
2. `.rc_tmp/a2_sources/AUDIT.md` §6 (mathematical-object items T1–T13, X1–X5) and §9 (reach of the printed-estimates
   theorem); `CHECKPOINT_3.md` (items 2, 6); `BRIEF.md` (the standard).
3. **Song and Liang (2015), the paper:** `.rc_tmp/a2_sources/Song_Liang_2015.pdf` (sha256 315c247c236b5f33…; journal page =
   PDF page + 946; read with `pdftotext -layout`). Check every page, equation, condition and theorem number, and every
   quotation.
4. For the theorem and assumption labels: `Docs/Writing/results/what_we_prove.pdf`.

## Known deliberate choices (report only if they misstate a source)
- Design classes (independent / locally correlated / pervasive factor) group TRACK_B's designs. One footnote covers the one
  cell that differs within a class.
- One sentence cites track C (internal), as "a numerical check of the conditions' population quantities, not yet complete". HQ allowed
  this.
- The explicit constants of the proofs are not judged (HQ ruling).

## What to check
- **A.** Each verdict (same / comparable / stronger / none) against TRACK_B.
- **B.** Each Song–Liang citation and quotation against the PDF.
- **C.** Each inside / outside / unclear call, in the table and in the text, against TRACK_B's table and dossiers.
- **D.** Each "evidence" line: does it claim more than TRACK_B or the cited result?
- **E.** The mathematical-object section against AUDIT §6: counts, groupings, and the stated status of each item
  (including the unbiasedness inputs X1, X5).
- **F.** Any sentence that frames asymptotics or proof constants as a limitation, or that overstates the reach of a
  theorem.

## Report
`Docs/Writing/reviews/A2_codex_fidelity.md`: a findings table (id, location, what the document says, what the source says
with file:line or page, and severity: C = changes a claim, S = scope, F = could mislead, E = editorial). End with one line:
`FIDELITY: FAITHFUL` or `FIDELITY: NOT-FAITHFUL`. Effort high.
