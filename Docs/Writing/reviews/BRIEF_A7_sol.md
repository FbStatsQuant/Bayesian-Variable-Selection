# Brief: scoped fidelity read of Assignment 7, the formal specification (Writing, 2026-11-24)

You are an independent reviewer. Report findings only. Edit no file except your report, and delete nothing.

Paths are relative to `/home/fb31/BVS-wt/WRITING`. Scratch goes in `.rc_tmp/` only: never `/tmp`, and do not set TMPDIR
(POLICIES §14). You report to the Writing manager only; do not message HQ or any other thread.

## The document
`Docs/Writing/manuscript/spec/spec.tex`, sections in `Docs/Writing/manuscript/spec/sections/` (`sp1_notation` …
`sp7_supplementary`, appendices `spA_crosswalk`, `spB_hq`; the algorithms are `sp4_algorithms.tex`). Compiled:
`Docs/Writing/manuscript/spec/spec.pdf`. A frozen copy is in `.rc_tmp/a7/sol_snapshot/`.

It is a reference specification: definitions, algorithms as coded, assumptions, and theorem statements with status tags.
It is built from the owner-review edition `Docs/Writing/manuscript/owner_review.tex` (sections `or3_model`,
`or4_sampler`, `or5_assumptions`, `or6_theorems`, `supplement_or`, `appendices_or`), which passed a fidelity read on
11-23. Deliberate choices, not findings in themselves: the numbering (assumptions 5.n, supplementary S1…, planned P1–P4);
display keys DIST/RM/MARG/OMIT/RMF; the screening and witness conditions numbered as Assumptions SCR and WIT; the
"OPEN CHOICE" boxes (candidates, explicitly undecided); the list in Appendix B (`spB_hq.tex`) of where the spec departs
from A6 wording (check that each departure is right, not that it exists).

Helper notes (use as maps, verify against the sources): `Docs/Writing/manuscript/spec/a7_notes/S1_pins.md` (code pins
for every algorithm line) and `a7_notes/S2_statements_registry.md` (statement → registry rows, MATCH/DIFF).

## Scope (only these three things)
- **A. Definitions and algorithms against the code.** Every definition in `sp1`–`sp4` (data, standardisation, priors and
  densities, marginal likelihood, posterior, start law, discrepancy, tempered path, pilot ESS rule, ρ and the grid rule,
  moves and acceptance probabilities, local search, stores, outputs, Ẑ and pooling, the list fields, Δ-domain), Table
  `tab:params`, and every line of the eight algorithms in `sp4_algorithms.tex`, against `Scripts/SMC_BVS/core/` in this
  worktree (identical to tag `method-v3.1.1-listpip`). §4.4 (the 1M engine) against `.rc_tmp/a6/sol_src/f2/` and
  `.rc_tmp/a6/sol_src/p1m/`. Findings: a formula, constant, order of operations, tie rule, failure condition or status
  that differs from the code, or a definition that cannot be matched to code.
- **B. Theorems and assumptions against the registry, verbatim.** Every statement in `sp6_theorems.tex` §6.1 and
  `sp7_supplementary.tex`, and every assumption and convention in `sp5_assumptions.tex`, against the registry statement
  files named in S2 (`Theory_work/...STATEMENT.md` and the reader text `Theory_work/Wave3/W3-READER/READER_VERSIONS.md`)
  and against `owner_review.tex`. Any change in hypotheses, quantifiers, constants or conclusions is a finding. Check that
  the theorem → assumption citations are complete (no hypothesis used but not cited) and that Table `tab:usage` matches
  the statements.
- **C. Status tags.** Every `\proved{…}` and `\planned{…}` tag: the row ids and the quoted status strings against
  `Theory_work/INFRA/registry/claims.tsv` on this checkout (main). Findings: a wrong id, a status string not verbatim
  (the council part — round, manifest, scores — is omitted on purpose), an overstated status, or a dropped condition. For
  the planned theorems, check that nothing is stated as decided that the project files leave open (`Theory_work/Dept/QUEUE.md`
  "Named open items", `Docs/Writing/ASSIGNMENT_6.md`, `Theory_work/Wave3/W3-D5P/ERRATA.md`).

Out of scope: clarity and style, proofs, numerical results, Song–Liang.

## Report
Write `Docs/Writing/reviews/A7_sol_fidelity.md` as a table with columns: id (A01…, B01…, C01…); spec file:line; what it
says; what the source says (file:line or TSV row id); severity: C = changes a claim or a definition, S = scope or
incompleteness, F = could mislead, E = editorial. End with `FIDELITY: FAITHFUL` or `FIDELITY: NOT-FAITHFUL` and the counts
per severity. Effort: high. One finding per defect, at its exact location.
