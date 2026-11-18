# Brief: scoped Codex fidelity read, Assignment 5 restructure of the manuscript (Writing, 2026-11-17)

You are an independent reviewer. This is the single Codex read of this revision. Report findings only, and edit no file
except your report. Paths are relative to `/home/fb31/BVS-wt/WRITING`. Scratch goes in `.rc_tmp/` only; do not set TMPDIR.
**Check only the three excerpt files below.** Each excerpt carries its manuscript file:line.

## Rule and decisions being implemented (context)
The owner's rule, and the HQ decisions, are in `.rc_tmp/ASSUMPTION_COMPLIANCE.md` (theory/W3-AUDIT 582af8a3) and the HQ
summary below:
1. Result 3 is presented as "the theorem for block and moderate AR correlation"; visibility = "no true predictor masked by
   ≤ 15 others"; its failures are named (pervasive mixed-sign factors, riboflavin-like data).
2. Certified screening (row 3.7) is in the main text, as "the guarantee that needs neither condition", with its weaker
   conclusion:
   - "certified" = the local-optimality flag;
   - no run is claimed to certify a small model;
   - miss counts by n are given;
   - it is not presented as "the result for strong-factor data".
3. Row 3.6 is a supplement remark; row 3.5 stays in the main text.
4. Corollary 9C is a conditional remark.
5. Row 1.4's Gaussian example is labelled as an example.
6. Disclosures: Theorem 2's Gaussian rows are Song–Liang's worked example; exact arithmetic and ideal random numbers are
   conventions that SL also presuppose.
7. Precedent notes (from `Docs/Writing/from_theory/PRECEDENTS_2026-11-17.md`) are added in §5.

## A. Statements: `.rc_tmp/a5_codex/A_statements.md`
**Source:** the earlier checked text, `.rc_tmp/a4_checked_draft/sections/*.tex` (Codex-read once already). Check that
moving theorems (certified screening into §4; row 3.6 and Corollary 9C into remarks in the supplement) changed no
hypothesis, conclusion, quantifier or scope; that the screening numerics (miss counts derived from "contained every true
predictor in 61 of 122 …") are arithmetically right; and that labels and references point to the right objects.

## B. Statuses and the summary table: `.rc_tmp/a5_codex/B_status.md`
**Sources:**
- `.rc_tmp/claims_freeze.tsv` (= the registry at tag `theory-v2026-11-freeze`; main d063cc3e has no changes);
- `.rc_tmp/card_v113.md`;
- `Docs/Writing/results_v2/STATUS_LEDGER_FREEZE.md`;
- for the new row-3.5 note, `.rc_tmp/ASSUMPTION_COMPLIANCE.md` items 6 and 47 (W1-N1:B/F "2a pending; line check running").

Scope lines are checked against `Docs/Writing/from_theory/TRACK_B_v1.4.md` (summary table).

## D. Song–Liang and precedent sentences: `.rc_tmp/a5_codex/D_SL.md`
**Sources:**
- `Docs/Writing/from_theory/PRECEDENTS_2026-11-17.md`: every "Precedents" line must match its locations and its "How
  ours compares" sentence; it must not claim more and must not drop a qualifier;
- `Docs/Writing/from_theory/TRACK_B_v1.4.md` and `WRITING_DELTA_v1.4.md`, as before;
- the two Song & Liang PDFs in `.rc_tmp/a2_sources/` (journal page = PDF page + 946);
- `.rc_tmp/ASSUMPTION_COMPLIANCE.md`, line 27 (the SL worked-example disclosure) and line 35 (the conventions).

You need not open the arXiv papers; PRECEDENTS records their verification. Check the bibliography entries for these
papers in `Docs/Writing/shared/refs.bib` (the last ten entries) against PRECEDENTS' "Versions read" table: title, venue,
year and arXiv id.

## Report
Write `Docs/Writing/reviews/A5_codex_fidelity.md`. It is one table with these columns:
- id;
- part;
- manuscript file:line;
- what it says;
- what the source says (file:line or page);
- severity: C = changes a claim, S = scope, F = could mislead, E = editorial.

End with `FIDELITY: FAITHFUL` or `FIDELITY: NOT-FAITHFUL` and the counts. Effort: high.
