# Brief: scoped fidelity read of Assignment 8, the theory slides (Writing, 2026-11-24)

You are an independent reviewer. Report findings only. Edit no file except your report, and delete nothing.

Paths are relative to `/home/fb31/BVS-wt/WRITING`. Scratch goes in `.rc_tmp/` only: never `/tmp`, and do not set TMPDIR
(POLICIES §14). You report to the Writing manager only; do not message HQ or any other thread.

## The document
`Docs/Writing/manuscript/slides/theory_slides.tex` (with `\input{p5_targetN}`, file
`Docs/Writing/manuscript/slides/p5_targetN.tex`); compiled `Docs/Writing/manuscript/slides/theory_slides.pdf`. A frozen
copy is in `.rc_tmp/a8/sol_snapshot/`. The assignment is `Docs/Writing/ASSIGNMENT_8.md`.

The slides are a transcription: every assumption and every theorem statement (proved and planned) of the formal
specification, with no proofs and no commentary. Deliberate choices, not findings in themselves: beamer blocks instead of
amsthm; statements split across "(cont.)" frames; cross-references hard-coded as text; status tags shortened to the row ids
plus status string.

## Scope (only this)
1. **Spec statements, verbatim.** Every slide statement against its source in `Docs/Writing/manuscript/spec/spec.tex`
   (sections in `Docs/Writing/manuscript/spec/sections/`: `sp1_notation`, `sp2_model` for the notation slide;
   `sp5_assumptions` for every assumption/convention and Table `tab:usage`; `sp6_theorems` for Theorems 1–6 and Planned
   Theorems P1–P4 with their open-choice boxes; `sp7_supplementary` for S1–S17). Findings: any change of hypothesis,
   quantifier, constant, symbol, conclusion, number or label; any statement, assumption, open-choice box or status tag
   missing or added; a PROVED/PLANNED status that differs from the spec; a usage-table entry that differs.
2. **P5 and Target N** (`p5_targetN.tex`) against `Theory_work/Dept/assess/MIS_KL/ASSESS_fable.md` §2 (setting (P),
   Target A, Target N) and `Theory_work/Dept/assess/MIS_KL/ASSESS_astra.md` §2, §3, §5 (the open-choice block: exact
   selection with consistency fallback; literal-KL integrability; the intercept; an example outside (OVᶜ)). Findings: any
   departure from the source wording or mathematics; anything presented as decided or proved that the sources leave as a
   candidate; a lock condition misquoted or attributed to the wrong section.

Out of scope: style, layout and clarity (except text cut off or unreadable in the PDF, which is a finding), proofs,
numerical results, the correctness of the spec itself against the registry (read on 11-24 under A7).

## Report
Write `Docs/Writing/reviews/A8_sol_fidelity.md` as a table with columns: id (F01…); slide (PDF page and frame title);
what the slide says; what the source says (file:line); severity: C = changes a claim or a definition, S = missing or added
material, F = could mislead, E = editorial. End with `FIDELITY: FAITHFUL` or `FIDELITY: NOT-FAITHFUL` and the counts per
severity. Effort: high. One finding per defect, at its exact location.
