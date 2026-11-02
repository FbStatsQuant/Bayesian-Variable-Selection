# Theory campaign 2026-11: protocol for cloud runs

This campaign pursues the frozen paper targets in `Docs/THEORY_PRIORITIES.md`. It is managed by the HQ thread, which launches one cloud run per task. If you are a cloud run, read this file and then your task file in `theory_campaign/tasks/`.

## Read first (in this order)
1. `Docs/THEORY_PRIORITIES.md`: the story, the 8 targets, the gap, the pursuit order and gates, and the preliminary data findings (§5).
2. Your task file: `theory_campaign/tasks/<TASK_ID>.md`.
3. The files your task names. Useful references:
   - definitions and hypotheses: `Docs/Theory/theorems/00_COMMON.md`;
   - the method spec: `Docs/Methodology/METHODOLOGY_v3.md`;
   - statements and proofs: `Docs/Theory/proofs/`, `Docs/Theory/proofs/LOCKED_PROOFS.md`, and `Docs/Theory/proofs/COLLECTED_PROOFS_v2.tex` (wave-1 proofs);
   - the new conjectures: `Docs/Theory/PAPER_SELECTION_20261028/` (FROZEN_LIST, both consultant reviews, and `new_conjectures/T37–T39`);
   - per-theorem summaries: `Docs/Theory/one_pagers/T01–T39.md`;
   - the engine: `Scripts/SMC_BVS/core/`.

## Rules
- **Where to work.** Work only on the branch `theory/<TASK_ID>`, and write only under `theory_campaign/<TASK_ID>/`. Do not edit any other file, and never push to `main`.
- **Commit and push early and often.** Commit after every meaningful step: a lemma, a counterexample, a script, a draft section. Push each commit. The run can be stopped at any time, and anything not pushed is lost.
- **Honest status words only.** Use exactly these: PROVED (a complete proof you checked line by line), PROOF SKETCH (the crux is identified and the steps are plausible, but not every step is verified), COUNTEREXAMPLE (with a reproducible script or explicit construction), CONJECTURE, and OPEN. Never upgrade a status. A proof here is a **candidate**: it is not reviewed and not adopted. Review happens later, by other model families.
- **Numerical checks.** Python 3 is available, but R is not. You may `pip install numpy scipy sympy mpmath`. Prefer exact enumeration at small p (p ≤ 20). Put every script under `theory_campaign/<TASK_ID>/scripts/`, with a fixed seed, and write down what it showed.
- **Notation.** Use the notation of `00_COMMON.md` and the T37–T39 files. If you introduce a new symbol, define it.
- **Scope.** Stay inside your task. If you find something important outside it, record it in the report under "Outside scope" and do not pursue it.
- **Time and effort.** Work deeply; this is research. Before you stop, write the report even if you have no result. A clean negative result, such as "this route fails, here is why", is valuable.

## Deliverable: `theory_campaign/<TASK_ID>/REPORT.md`
1. **Headline:** 3–6 lines saying what you established, with status words.
2. **Statements:** each refined statement you propose, in full, with hypotheses named.
3. **Proofs or sketches:** complete proofs if you have them, otherwise a skeleton with the crux isolated. Long proofs can go in `PROOF.md` or `PROOF.tex` next to the report.
4. **Evidence:** numerical checks, small-case enumerations, counterexamples.
5. **What fails and why:** routes tried and abandoned.
6. **Needs escalation:** steps you believe need a stronger prover or an independent check, and why.
7. **Outside scope:** anything important you found outside the task.
8. **Confidence card:** for each target your task touches, give the refined statement, your confidence (low / medium / high) that it is true, your confidence that it is provable at reasonable cost, the crux, and whether a method change would be needed.
