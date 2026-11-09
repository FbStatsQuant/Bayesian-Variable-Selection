# v1.1 fidelity review — brief (one fresh reviewer)

You are an adversarial fidelity reviewer. Your job is to find every place where the new v1.1 text of the
State-of-Project document misstates its sources. Do not confirm; try to break it.

Repo root: `C:\Users\felip\Bayesian-Variable-Selection`. Read-only: do not edit any file except your output file,
and do not run state-changing git commands. Do NOT read `Theory_work/State_of_Project/review/` (evaluation key).

## Objects under review (v1.1 additions only)
1. `Theory_work/State_of_Project/sections/07_theory_loop.tex` — the whole file (new section "Theory loop: Waves 1 and 1C").
2. Every paragraph headed `\paragraph{Update v1.1 ...}` (each preceded by a comment line `% v1.1 update (...)`) in
   `sections/04_theory.tex`, `sections/04b_supplement.tex`, `sections/05_history.tex`, `sections/06_open_and_plan.tex`.
3. The v1.1 paragraph in `sections/00_agent_brief.tex` ("What changed in v1.1"), the v1.1 changelog item in
   `sections/E_changelog.tex`, and the rows of `registry/theory_loop.tsv` plus the TH163 row at the end of `registry/history.tsv`.
The compiled document is `Theory_work/State_of_Project/State_of_Project_v1.1.pdf` (§7 is the new section).

## Sources (ground truth)
Citation prefixes: `W1/` = `Theory_work/Wave1/`, `W1C/` = `Theory_work/Wave1C/`, `NBH/` =
`Theory_work/Old_Projects/New_BVS_Headquarters/`. `\src{path:a-b}` cites lines a–b of the current file. The authoring rules are
`Theory_work/State_of_Project/AUTHORING.md` (read §0).

## What to check
- G1 Statement fidelity: every `stmt` box must reproduce its cited span verbatim up to LaTeX formatting (every hypothesis,
  quantifier, constant, exponent, qualifier). Report any dropped/added/changed content, wrong spans, or abridgements not
  marked `[…]`.
- G2 Status fidelity: every `\status{...}` and every quoted status/score must be verbatim from the cited file; nothing
  upgraded or softened (e.g. "PROVED (by this seat, unchecked)" is not "proved"; PARTIAL stays PARTIAL; council scores and
  rounds exact; "not adopted by HQ" kept).
- G3 Claims: every claim-bearing sentence outside the boxes (status lines, "What changed versus v1.0", plain readings,
  not-proved boxes, update paragraphs, overview table, frontier list, agent brief, changelog, registry rows) must be supported
  by its cited lines; plain readings must not claim more than the statements (regime, asymptotic vs finite-n, "jointly with
  output", premises).
- G4 Completeness: anything the sources record as a limit/gap/scope restriction for these results that is missing from the
  not-proved boxes and would mislead a reader; misattributions between tickets.
- G5 Citations: wrong line numbers (cited lines do not say what the sentence says).

## Output
Write your full review to `Theory_work/State_of_Project/review_v11/R1_fidelity_sol.md`:
a verdict line (FAITHFUL / FAITHFUL-WITH-FIXES / NOT-FAITHFUL), then a numbered list of findings, each with severity
(BLOCKING / MAJOR / MINOR / NIT), location (file:line), the source evidence (path:line, quoted), and the exact fix.
Be exhaustive; spot-checking is not enough for statuses and the update paragraphs. Your final message: the verdict and the
counts per severity.
