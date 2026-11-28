# Brief: scoped fidelity read of Assignment 6, the owner-review edition (Writing, 2026-11-23)

You are an independent reviewer. Report findings only. Edit no file except your report, and delete nothing.

Paths are relative to `/home/fb31/BVS-wt/WRITING`. Scratch goes in `.rc_tmp/` only: never `/tmp`, and do not set TMPDIR
(POLICIES §14). You report to the Writing manager only.

## The document
The owner-review edition is `Docs/Writing/manuscript/owner_review.tex`. Its sections are in `Docs/Writing/manuscript/sections/`:
- `or1_reading`, `or3_model`, `or4_sampler`, `or5_assumptions`, `or6_theorems`, `or7_planned`, `or8_status`;
- `supplement_or`, `supp_index`, `appendices_or`, `appendix_sl_or` (the long Song–Liang comparisons, moved out of §5).

A frozen copy of the text you read is in `.rc_tmp/a6/sol_snapshot/`. The compiled PDF is
`Docs/Writing/manuscript/owner_review.pdf`.

It is an edition of the checked manuscript (`Docs/Writing/manuscript/sections/s3_method.tex`, `s4_results.tex`,
`s5_assumptions.tex`, `supplement.tex`). Those files passed earlier fidelity reads (A5 final). This edition copies their
statements and rewrites the prose around them. Deliberate changes in this edition, not findings in themselves: Results 1–6
use their own counter (`mainthm`/`mainprop`, so Result k is Theorem k); in Assumption 4(a)(ii) the checked text's `r_n`
is renamed `\delta_n` (it clashed with Song–Liang's `r_n`); a few "In words" and "Why it is natural" paragraphs were
rewritten for clarity (check that they still say no more than the statements).

## Scope (only these four things)
- **A. Theorem statements.** Read every formal statement in `or6_theorems.tex`: Results 1–6, the environments `theorem`,
  `proposition` and `lemma`, plus Lemma `lem:summaries` in `or3_model.tex`.
  - Check each against its counterpart in the checked files above. Any change in hypotheses, quantifiers, constants or
    conclusions is a finding.
  - Also check that each "In words" paragraph (`\inwords`) and each row of Table `tab:results` says no more and no less
    than its statement.
- **B. Statuses.** Check every `\status{...}` box in `or6_theorems.tex` and `supplement_or.tex`, the table
  `tab:status-diff` and its text in `or8_status.tex`, the verbatim table `app:status-verbatim` in `appendices_or.tex`,
  and the "What remained" list there.
  - Compare them with the registry on main (`.rc_tmp/a6/sol_src/claims_main.tsv`) and with the tag
    `theory-v2026-11-freeze` (`claims_tag.tsv`).
  - The helper note `.rc_tmp/a6/sol_src/H1_status_and_pins.md` maps manuscript results to registry rows. Use it as a map
    and verify against the TSVs.
  - Findings: an overstated status; "recorded" for something not recorded; a dropped condition the registry still lists;
    a date or count that is wrong.
- **C. Song & Liang sentences.** Check every sentence that cites \SL{} or `SongLiang2015`, in `or3_model.tex`
  (`Compared with \SL`), `or5_assumptions.tex` (all `\Asl{}` parts and Table `tab:a-summary`'s last column),
  `or6_theorems.tex` (`\vssl{}`), `supplement_or.tex` and `appendix_sl_or.tex`.
  - Compare them with the PDFs: `.rc_tmp/a2_sources/Song_Liang_2015.pdf` (journal page = PDF page + 946) and
    `Song_Liang_2015_supplement.pdf`.
  - The helper catalogue `.rc_tmp/a6/sol_src/H3_songliang.md` lists their conditions with pages and flags (F1–F9). Its
    flags were applied in this edition, so check that the fixes are right.
- **D. Parameters against the code.**
  - **Model and prior.** Check Table `tab:prior` (`or3_model.tex`) and the defaults in the text of `or3_model.tex` and
    `or4_sampler.tex` (the stage descriptions) against `Scripts/SMC_BVS/core/` in this worktree.
  - **The 1M engine.** Check Table `tab:engine` (now in `appendices_or.tex`, §"The parallel engine, change by change") and §"The parallel engine" in `or4_sampler.tex` against:
    - the frozen engine files `.rc_tmp/a6/sol_src/f2/` (`CAMPAIGN_FREEZE.md`, `calib.h`, `setup.h`, from tag
      `p1m-freeze-F2`);
    - the P1M documents `.rc_tmp/a6/sol_src/p1m/` (`DECISIONS.md`, `ENGINEERING_SPEC.md`, `GC_PREREG.md`, the
      `OVERLAP_1e4_*` files, `LEG_READBACK.md`);
    - `.rc_tmp/a6/sol_src/HQ_DECISIONS.md`.
  - The helper note `H2_planned_and_1M.md` there gives line pins to start from.
  - Also check the PLANNED section (`or7_planned.tex`) for any sentence that claims more than H2 §B or `HQ_DECISIONS.md`
    supports.

Out of scope: clarity and style (a separate reader did that), the proofs, the 1M results, and anything in the supplement
other than its status boxes and its \SL{} sentences.

## Report
Write `Docs/Writing/reviews/A6_sol_fidelity.md` as a table with these columns:
- id (A01…, B01…, C01…, D01…);
- manuscript file:line;
- what it says;
- what the source says (file:line, TSV row id, or journal page);
- severity: C = changes a claim, S = scope, F = could mislead, E = editorial.

End with `FIDELITY: FAITHFUL` or `FIDELITY: NOT-FAITHFUL` and the counts per severity. Effort: high. Be precise: one
finding per defect, with its exact location.
