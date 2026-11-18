# Brief: Codex fidelity read of the unified manuscript, tightly scoped (Writing, Assignment 4, 2026-11-17)

You are an independent reviewer. This is the manuscript's single Codex read: findings only, no edits except your report.
Paths are relative to `/home/fb31/BVS-wt/WRITING`. Scratch goes in `.rc_tmp/` only; do not set TMPDIR. **To save usage,
check only the four excerpt files below, against the named sources. Do not read or review the rest of the prose.**
Each excerpt carries its manuscript file:line.

## A. Theorem statements: `.rc_tmp/a4_codex/A_statements.md`
Every theorem, proposition, corollary, lemma, assumption and local assumption, plus Remarks "The rate cannot be improved"
and "An alternative route". **Source:** the checked text of D2 v2.1, `Docs/Writing/results_v2/sections/*.tex` (and, for
the Lemma in §3, `Docs/Writing/results_v2/sections/s2_setting.tex`). The statements were copied, with only presentation
changes. Check that no hypothesis, conclusion, constant, quantifier or scope changed, and that labels and cross-references
point to the right objects.

## B. Status notes and the summary table: `.rc_tmp/a4_codex/B_status.md`
Every `\status{…}` box, every `\scope{…}` line, and Table `tab:results`. **Sources:**
- the frozen registry, `.rc_tmp/claims_freeze.tsv` (= `claims.tsv` at tag `theory-v2026-11-freeze`, d40c9780; key =
  ticket:local_id; column `status`);
- the frozen card, `.rc_tmp/card_v113.md` (rows 1.1–4.1);
- the map from manuscript results to masters, `Docs/Writing/results_v2/STATUS_LEDGER_FREEZE.md`;
- for the scope lines, `Docs/Writing/from_theory/TRACK_B_v1.4.md` (summary table, design columns).

Plain labels:
- "proved and independently checked" = PROVED-CHECKED with no open condition;
- "proved and checked, conditional on X" = PROVED-CHECKED, conditional on X;
- "proved but not yet independently checked" = PROVED (unchecked).

## C. Parameter tables against the code: `.rc_tmp/a4_codex/C_params.md`
The compact table (`tab:params`), the full table with code locations (`tab:params-full`) and the conventions bullets.
**Source:** the code at `Scripts/SMC_BVS/core/` (the paths in the table are relative to it). Check each value, formula
and code location. The full table and its locations come from an earlier, code-checked document (D1,
`Docs/Writing/methodology/smc_bvs_method.tex`). The only intended changes are:
- symbol renames: burn-in L → L_bi; temperature φ → ξ; step ceiling T_i → T^max_i;
- the "Theory" column re-pointed to the manuscript's labels.

## D. Song–Liang comparison sentences: `.rc_tmp/a4_codex/D_SL.md`
The introduction's "Earlier work" paragraph, §5.1, "How the conclusions compare", the §5 table, and every paragraph
head and evidence line that mentions Song and Liang. **Sources:**
- `Docs/Writing/from_theory/TRACK_B_v1.4.md` (summary table, §S, §T2);
- `Docs/Writing/from_theory/WRITING_DELTA_v1.4.md`: the §5.1 first paragraph must be the v1.4 headline verbatim, and
  one-word comparisons are allowed only for the uniform cases it lists;
- the paper `.rc_tmp/a2_sources/Song_Liang_2015.pdf` (journal page = PDF page + 946);
- the supplement `.rc_tmp/a2_sources/Song_Liang_2015_supplement.pdf`.

These sentences passed a full Codex read in an earlier document (A2 v2). Check mainly that nothing changed in the move,
and that the new introduction paragraph claims no more than TRACK_B v1.4 §S.

## Report
Write `Docs/Writing/reviews/A4_codex_fidelity.md`. It is one table with these columns:
- id;
- part (A/B/C/D);
- manuscript file:line;
- what it says;
- what the source says (file:line or page);
- severity: C = changes a claim, S = scope, F = could mislead, E = editorial.

End with `FIDELITY: FAITHFUL` or `FIDELITY: NOT-FAITHFUL` and the counts. Effort: high. Deadline: today; be efficient.
