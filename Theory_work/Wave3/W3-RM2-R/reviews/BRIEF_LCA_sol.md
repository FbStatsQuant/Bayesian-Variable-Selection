# BRIEF LC-A — line check, W3-RM2-R lemmas Q1, Q2, Q7 (Sol, gpt-6.1-sol, reasoningEffort high; new agent, blind)

You line-check three lemma files of ticket W3-RM2-R (Tier B rider). Work read-only in `/home/fb31/BVS-wt/W3-RM2-R`
(paths relative to it); write nothing; do not change git state. Do **not** read `LOG.md`, any `CHECKPOINT_*`, or any
file under `Theory_work/Wave3/W3-RM2-R/reviews/` other than this brief (you are blind to earlier reviews).

## Files to check, line by line
1. `Theory_work/Wave3/W3-RM2-R/lemmas/Q1_sandF_c.md` — a copy of the parent lemma `Theory_work/Wave3/W3-RM2/lemmas/L1_sandF_b.md`
   with changed lines marked [R-#]. Check every [R-#] change, and that unmarked text is the parent's (diff the two files).
2. `Theory_work/Wave3/W3-RM2-R/lemmas/Q2_TL_c.md` — partial copy of `Theory_work/Wave3/W3-RM2/lemmas/L2_width.md` (§0 and §4)
   with [R-#] changes, plus a new §6 (posterior/mode input). Check every [R-#] change and §6.
3. `Theory_work/Wave3/W3-RM2-R/lemmas/Q7_proxy_d.md` — new file (example with a decaying signal). Check everything.

## Against
- The statement: `Theory_work/Wave3/W3-RM2-R/STATEMENT.md` v1.0 — §2 ((T1-F♭), (V♭), (V_b♭), (BM-W⁺), 𝓜_n, [MODE]),
  §4 bridges (Q1)–(Q3), §5 (C5⁺). Each lemma must prove exactly what the statement says it proves, under no more than
  the statement's hypotheses (statement copies vs lemma statements; quantifiers; constants).
- Inputs: `Theory_work/Wave3/W3-RM2/lemmas/L0_toolkit_b.md` (constants C_R, κ_E; (T4)(b), (E6)), `L2_width.md` §§0–1, §4,
  `L6_examples.md:330-384`, `L3_assemblyF.md:22-24`, `Theory_work/Wave3/W3-RM2/STATEMENT.md`;
  `Theory_work/State_of_Project/sections/04_theory.tex:768-790` (TH09 card), `Theory_work/Wave3/W3-POST/STATEMENT.md:14-100`.

## What to do
Try to break each changed step: wrong inequality, a constant that does not close, a hidden use of a hypothesis that was
weakened (M_n → ∞, λ_n/log n → ∞, BM-∞), an n₀ that depends on something not fixed, a wrong citation. For Q7, verify the
residual formula, the bound on d_n, and that every hypothesis of RM2-F (PARENT v1.4) and of RM2-F-plus is covered.

## Reply format
Per file: VERIFIED / VERIFIED-WITH-AMENDMENTS / GAP / ERROR, then numbered findings tagged C (correctness), S (strength),
F (faithfulness) or E (editorial), each with file:line, what fails, and a fix. End with a one-line summary per file.
