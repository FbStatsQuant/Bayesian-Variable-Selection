# Writing Department: Assignment 8, the theory slides (HQ, 2026-11-24; owner's request)

## Purpose (owner, binding)
The owner asked for "beamer, Madrid theme style slides with all assumptions and theorems (proven and to prove). For now
just those things, no analysis on the assumptions on the slides. Include this last misspecification result." He will
use them to set the theory goals for a presentation in about two weeks.

## Base
`manuscript/spec/spec.tex` (A7, main de67a60d) is the single source. Transcribe its statements; don't re-derive or
re-word the mathematics. Keep its notation, labels and numbering so every slide can be traced to the spec.

## Contents (in this order)
1. A title slide, then one slide of notation and setting: the model, the prior and the regime, only as much as the
   statements need.
2. **The assumptions.** Every numbered assumption of the spec, with its exact formal statement, one or two per slide.
   - No commentary, reasonableness notes or Song–Liang comparisons.
   - End the section with one slide of the assumption–theorem usage table.
3. **The proved theorems.** Theorems 1–6 in the spec's order, one per slide (split a long one over two slides).
   - Give the formal statement, and below it a single status line: PROVED.
   - Registry ids may go in a footnote-sized line.
4. **The theorems to prove.**
   - P1–P4 as in the spec, each marked PLANNED, with its boxed open choice shown as an "open choice" block.
   - **P5 (new): misspecification under a KL projection, at fixed p.** Take Target A from
     `Theory_work/Dept/assess/MIS_KL/ASSESS_fable.md` §2 (setting (P) and Target A), stated as a PLANNED candidate. Add
     an open-choice block listing Astra's lock conditions (`ASSESS_astra.md` §2, §5):
     - exact selection is the target, with consistency as the fallback;
     - a literal-KL integrability caveat;
     - a fixed intercept;
     - an example outside (OV^c).
   - Target N (the heteroscedastic boundary at growing p) goes on one slide, marked "PLANNED, conditional: kept only if a
     valid design exists".
5. **The supplementary statements:** compact, several per slide, statements only.

**Not in scope:** proofs, analysis of the assumptions, results and benchmarks, and new theory.

## Form
- `\documentclass{beamer}`, `\usetheme{Madrid}`, 16:9.
- Use `theorem`/`assumption` blocks; PLANNED items get a visibly different block colour (for example `alertblock` or
  `exampleblock`).
- Readable font size. When a statement does not fit, split it; never shrink below footnotesize.
- Source in `manuscript/slides/theory_slides.tex`. PDF named `manuscript/slides/theory_slides_<date>.pdf`.

## Staffing and checks (token-lean)
- The Opus manager decides; one Sonnet helper transcribes from spec.tex.
- One scoped gpt-6.2-sol fidelity read: every slide statement against spec.tex and against the two ASSESS files
  (verbatim). Log it in SOL62_QUALITY.md.
- No clarity read, no Fable.

## Reporting
- To HQ (thread mcp:4f1a2e12-7ac4-4619-9128-1469ea92eb2e, environment 1fde6176): one start line with an ETA, then one
  delivery line with the PDF path. Push to main when done.
