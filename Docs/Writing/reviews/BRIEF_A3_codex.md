# Brief: Codex fidelity read of "What we prove" v2 (Writing, Assignment 3, 2026-11-16)

You are an independent reviewer. Check one document for **fidelity** to its sources. Report findings only, and edit no
file except your report. Paths are relative to `/home/fb31/BVS-wt/WRITING`. Scratch goes in `.rc_tmp/` only; do not set
TMPDIR. This is the document's single Codex read; re-checks will go to another reviewer.

## Document
`Docs/Writing/results_v2/what_we_prove_v2.pdf` (LaTeX: `what_we_prove_v2.tex`, `sections/*.tex`). It is a tight
re-edit of a first version that already passed a fidelity read. The main text (§1–6) holds five core results; the
supplement (Appendix A) holds further results; Appendices B–E hold notation, conventions, constants and the status ledger.
`CUT_LIST.md` lists what was left out.

## Sources
1. **The checked base:** v1, `Docs/Writing/results/sections/*.tex` (PDF `results/what_we_prove_v1.pdf`). Every theorem,
   assumption and remark in v2 comes from v1, often condensed. **Main check:** no condensation changes a claim, a
   condition, a quantifier or a scope.
2. **Statuses:** `Docs/Writing/results/STATUS_LEDGER.md` (plain labels and HQ rulings H1–H4) and the registry
   `.rc_tmp/a3_claims_main_a7fc5093.tsv` (main a7fc5093, column `status`).
3. **Theory notes,** `Docs/Writing/from_theory/`:
   - `ANSWERS_2026-11-16.md`: C* (Appendix D); 32s₀ (§5); the moderate-n heuristic (Remark 3.3(c)); the noiseless gain;
   - `IDEALW_NOTE_2026-11-16.md`: the sentence in the Result 3 status;
   - `ROW36_NOTE_2026-11-16.md` and `AUDIT_NOTE_2026-11-16.md` item 1: the §6 scope;
   - `TRACK_B_v1.4.md`: only for the design classes and the inside/outside statements in §2.3, §5 Remark 5.4 and §6.

## What to check
- **A.** Each statement in v2 against its v1 source: hypotheses, conclusions, constants, quantifiers, scope. Pay most
  attention to the condensed places:
  - §2 (prior, run, start law, certification, conventions);
  - Theorem 3.2 (in-probability form stated first; expectation bound second);
  - Remark 3.3 (merged sharpness + heuristic);
  - Theorem A.9 and the sentence after it;
  - Theorem A.12 and its numerics;
  - Proposition 6.1 and the pooled sentence;
  - the §6 scope paragraph;
  - Remarks 4.3 and 5.4.
- **B.** Each status box and each Table 1 status against the ledger and registry (H1 wording, the conditional items,
  "not yet independently checked" for the pooled form, bridge-pending notes, revision pending for rows 3.1/3.2).
- **C.** The Theory-note items (C*, 32s₀, heuristic and numbers, IDEAL-W⁺ sentence) against the notes.
- **D.** Appendix E's freeze list against the notes (what happens at the freeze, and what after it).
- **E.** Table 1, the abstract and each "In words" or "Why it matters" line: does any claim more than its theorem?
- **F.** Any sentence that frames asymptotics or proof constants as a limitation, or that ranks our results against Song
  and Liang overall.

## Report
Write `Docs/Writing/reviews/A3_codex_fidelity.md`. It is a table with these columns:
- id;
- location;
- what the document says;
- what the source says (file:line);
- severity: C = changes a claim, S = scope, F = could mislead, E = editorial.

End with `FIDELITY: FAITHFUL` or `FIDELITY: NOT-FAITHFUL`. Effort: high.
