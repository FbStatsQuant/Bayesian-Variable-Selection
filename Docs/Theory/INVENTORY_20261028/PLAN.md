# PLAN: theory inventory, alignment audit, and relevance (HQ, 2026-10-28)

## Goal (Felipe)
1. An inventory of the theoretical results we have.
2. How well the method described in the proofs matches what was actually executed.
3. The relevance and intuition of the results obtained so far.

Team (Felipe): Astra (high) as consultant; Sol 6.1, Sonnet and Haiku as workers. HQ (Opus) leads, integrates and decides. Felipe gets one final answer.

## Deliverable
`THEORY_INVENTORY.md` in this folder, plain language, with four sections:
- A. **Inventory.** All 36 conjectures: which are proved (locked), which parts, under which hypotheses; which are open or dropped; the dependency picture.
- B. **Alignment.** For each of the 21 proved entries: the algorithmic objects it models, traced across L0 (METHODOLOGY_v3.0) → L1 (master Part I) → L2 (executed code v2.1). Verdict per object:
  - MATCH;
  - IDEALISATION (declared EX-A/EX-S/CAL/EXEC);
  - DIVERGENCE (what differs, and whether it changes the theorem's applicability);
  - NOT EXERCISED (the code path exists but never ran in the study, or the theorem's branch was never taken).

  Plus executed features that no proved theorem covers.
- C. **Regime check.** What the asymptotic results say at n=200, p∈{500,1000}, s0=14, c∈{1,0.5}: the size of their rates and conditions, and how they square with the observed results.
- D. **Relevance and intuition.** Per result: what it says in plain words, why it matters for the method and the paper, and what is still open.

## Pieces (L0/L1/L2 and paths in CONTEXT.md)

| # | Piece | Who | Inputs | Output (work/) | Acceptance |
|---|---|---|---|---|---|
| 0 | Plan consult | Astra high (codex, read-only) | PLAN.md, CONTEXT.md | consult/ASTRA_PLAN.md | Answers the 4 questions; HQ records what it adopts |
| 1 | Mechanical inventory + hash check | Haiku | LOCKED_PROOFS.md, theorems/, proofs/ | work/H1_inventory.md | Every theorem T01–T36 listed once; every locked hash recomputed; 2 planted canary rows reported as mismatches |
| 2 | Alignment, group A: target posterior and statistics (T01_T02, T03, T04, T06_T07) | Sol 6.1 high | STATEMENTs, L0 §target, L1 §I.1–I.2, I.8, code preprocess/setup/score | work/S_A_alignment.md | Every proved clause covered; every code claim has file:line; verdicts in the fixed vocabulary |
| 3 | Alignment, group B: start, kernels, hazards, ESS (T09, T10, T11(iii), T13, T22(i)–(iv), T27(i)) | Sol 6.1 high | same, L1 §I.3–I.5; code start/blocks/engine/calib/core | work/S_B_alignment.md | same |
| 4 | Alignment, group C: evidence, outputs, certificates (T12, T14(i), T15, T20(i)–(ii), T21, T23(ii), T25(iv), T31(i)) | Sol 6.1 high | same, L1 §I.5–I.6; code ledger/score/core/fit/run, study adapter | work/S_C_alignment.md | same |
| 5 | Regime check | Sol 6.1 high | STATEMENTs of T02, T03, T04, T06, T22(iii), T27(i); master Part II.2–II.5; EMPIRICAL_SUMMARY.md | work/S_D_regime.md | Each rate evaluated numerically, with the computation shown; each condition marked plausible / doubtful / unknown, with reasons |
| 6 | Relevance and intuition drafts | Sonnet | LOCKED_PROOFS.md, STATEMENTs, THEORY_BRIEF.md, THEOREM_MAP.md, EMPIRICAL_SUMMARY.md | work/SN_intuition.md | All 21 entries; plain language; no claim beyond the statement's wording |
| 7 | Citation verification | Sonnet (not an author) | file:line claims sampled from pieces 2–4, plus 3 planted false citations | verify/SN_citecheck.md | Each claim checked against the file; the 3 canaries caught |
| 8 | Integration | HQ | all of the above | THEORY_INVENTORY.md | Every DIVERGENCE checked by HQ in the code itself |
| 9 | Final consult | Astra high | THEORY_INVENTORY.md + the S_* files | consult/ASTRA_FINAL.md | HQ resolves or records every point |

Pieces 1–6 are independent and run in parallel. Piece 7 waits for 2–4; piece 8 for everything; piece 9 for 8.

## Budget
- Astra: 2 calls.
- Sol: 4 calls (+1 retry each if needed).
- Sonnet: 2.
- Haiku: 1.
- Fable: 0.
- Each output file is capped at about 25 KB.

## Rules for all workers
Read-only on every input. Write only your own output file. Never fabricate a file:line; quote the line. Cite statement clauses by their label. No proving, no editing of theorems, no runs on Owls or NOTS.
