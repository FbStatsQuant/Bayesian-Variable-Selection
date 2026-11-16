# BRIEF LC-B — line check, W3-RM2-R lemmas Q4, Q5, Q6 (Sol, gpt-6.1-sol, reasoningEffort high; new agent, blind)

You line-check three lemma files of ticket W3-RM2-R (Tier B rider). Work read-only in `/home/fb31/BVS-wt/W3-RM2-R`
(paths relative to it); write nothing; do not change git state. Do **not** read `LOG.md`, any `CHECKPOINT_*`, or any
file under `Theory_work/Wave3/W3-RM2-R/reviews/` other than this brief (you are blind to earlier reviews).

## Files to check, line by line
1. `Theory_work/Wave3/W3-RM2-R/lemmas/Q4_core_plus.md` — a copy of `Theory_work/Wave3/W3-RM/lemmas/L0_core.md` with changed
   lines marked [R-#]: new parts (a′), (b⁺), (c⁺). Check every [R-#] change; confirm unmarked text is the parent's.
2. `Theory_work/Wave3/W3-RM2-R/lemmas/Q5_dlv0.md` — new: deterministic delivery (DLV-0) by an exit walk of the code as
   pinned. **Check it against the code itself**: `Scripts/SMC_BVS/core/` (`v3_fit.R`, `v3_preprocess.R`, `v3_calib.R`,
   `v3_run.R`, `v3_setup.R`, `cpp/v3_core.cpp`, `cpp/v3_start.h`, `cpp/v3_engine.h`, `cpp/v3_calib.h`, `cpp/v3_score.h`,
   `cpp/v3_runtime.h`). Every cited file:line must say what the lemma says; every way `v3_fit` can end without
   `estimates_available = TRUE` (a `return`, `stop`, `throw`, or non-"ok"/non-"completed" status on its call graph) must be
   covered by one of (E1)–(E8), or the lemma is incomplete — list any uncovered exit with file:line.
3. `Theory_work/Wave3/W3-RM2-R/lemmas/Q6_assembly.md` — assembly of (C1⁺), (C2⁺) and the containment Cont-plus.

## Against
- The statement: `Theory_work/Wave3/W3-RM2-R/STATEMENT.md` v1.0 — §1, §2 (𝓜_n, [MODE], St_n, NA(𝓛′), TL(𝓛′), (D),
  IDEAL-W⁺, 𝔇, valid non-degenerate input), §3 ((C0⁺), (C-D)), §4 ((C1⁺), (C2⁺), bridge table), §6 ((C4⁺), dependency
  table). Each lemma must prove exactly what the statement claims, under no more than its hypotheses.
- Sources: `Theory_work/Wave3/W3-RM/STATEMENT.md` (§1 lines 32-68; RM-0 160-176; E4 219-230); `Theory_work/Wave1C/C-GROW/lemmas/L1_descent.md`;
  `Theory_work/Wave1C/C-DLV/STATEMENT.md`, `lemmas/L1_resources.md`, `lemmas/L2_degenerate.md`, `lemmas/L3_grid.md`,
  `lemmas/L4_delivery.md`; `Theory_work/Wave1C/FINAL/sections/s6_delivery.tex:1-62`; `Theory_work/Wave2/W2-UNI/lemmas/L5_delivery.md`;
  `Theory_work/Wave3/API_AUDIT/pass1/R-AUD1_sol.md`; `Theory_work/Wave3/W3-RM2/STATEMENT.md`, `lemmas/L3_assemblyF.md`,
  `lemmas/L5_formR.md`, `lemmas/L2_width.md` §1; the ticket's own `lemmas/Q1_sandF_c.md`, `Q2_TL_c.md`, `Q7_proxy_d.md`
  as stated inputs (their statements only; they are checked elsewhere).
- Registry statuses: `Theory_work/INFRA/registry/claims.tsv`.

## Sweep duties (also yours, Tier B)
Statement copies vs lemma statements; quantifiers (every seed / every run / data events); each lemma's scope against
its downstream uses (Q4 (c⁺) and Q6 rely on Q5; Q6 relies on Q1, Q2, Q4); conditionality carried (SOP:TH09,
W2-APP:POST).

## Reply format
Per file: VERIFIED / VERIFIED-WITH-AMENDMENTS / GAP / ERROR, then numbered findings tagged C (correctness), S (strength),
F (faithfulness, incl. to the code) or E (editorial), each with file:line, what fails, and a fix. End with a one-line
summary per file.
