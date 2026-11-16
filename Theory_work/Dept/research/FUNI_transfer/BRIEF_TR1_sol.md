# BRIEF — TR1: does a delivery argument transfer to a different search cap? (Theory Department, 2026-11-16)
Sol (codex gpt-6.1-sol), effort high, ONE call, fresh, read-only. You have no stake in the answer; either outcome is useful.

Do not write any file outside the worktree and set no TMPDIR. Scratch only in /home/fb31/BVS-wt/THEORY-DEPT/.rc_tmp/, deleted at the end.
Write exactly one file: `/home/fb31/BVS-wt/THEORY-DEPT/Theory_work/Dept/research/FUNI_transfer/TR1_sol.md`. Change no git state.
All paths are relative to /home/fb31/BVS-wt/THEORY-DEPT (a checkout of current main for these folders).

## Question
Does the argument of **C-DLV Prop-F** (`Theory_work/Wave1C/C-DLV/lemmas/L4_delivery.md`; claim statement :79-84; method described at :7 and :53)
and of **W2-FAC-A Prop-F-FAC Steps 1-2** (`Theory_work/Wave2/W2-FAC-A/lemmas/L7_delivery.md`, statement :22-24, Steps 1-2 around :35-38)
hold for the method whose local-search (LS0) cap is **ℓ_n + |S̃₀|** (as described in `Theory_work/Wave2/W2-UNI/lemmas/L5_delivery.md:7-9`,
the method of claim W2-UNI:F-UNI, statement :15-21), under the idealisation **IDEAL-W** as defined in those files?
Concretely: the conclusion at stake is F-UNI's "P(no output) = 0 for every admissible n ≥ 3" (delivery of an output by the shipped method).

## What to do
1. State precisely the method each proof is about (LS0 cap, other caps/ceilings it uses, IDEAL-W's content).
2. Walk the steps of Prop-F (and Prop-F-FAC Steps 1-2) with the cap ℓ_n replaced by ℓ_n + |S̃₀|. For each step say: holds verbatim / holds
   with a stated change / fails. **Give the exact step that fails, if any**, with a concrete reason (or a counterexample configuration).
3. If the code is needed to pin a cap or ceiling, read `Scripts/SMC_BVS/core/v3_run.R` and `Scripts/SMC_BVS/core/cpp/v3_core.cpp`
   (cite file:line). Note: W3-RM2-R's STATEMENT (in `/home/fb31/BVS-wt/W3-RM2-R/Theory_work/Wave3/W3-RM2-R/STATEMENT.md:219`) records a
   different route (DLV-0) under extra conditions; you may read it, but judge the Prop-F transfer on its own merits.

## Output
`TRANSFER: YES | NO | YES-WITH-CHANGES`, the step table (≤ 25 lines, file:line), and, if YES-WITH-CHANGES, the exact changes needed.

## Addendum (consultant via HQ, sent as a steer to the running TR1 session at 05:36)
Question 2: is an every-n delivery claim for cap ℓ_n + |S̃₀| possible under IDEAL-W alone, or only on a restricted domain / under IDEAL-W⁺ with the re-derived allocation (cf. W3-RM2-R DLV-0, STATEMENT:219)? Final line `EVERY-N UNDER IDEAL-W: YES | NO`.
