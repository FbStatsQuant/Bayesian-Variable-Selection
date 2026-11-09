# Council brief (C-GROW) — identical for both council reviewers

You are one of two independent council reviewers for theory ticket C-GROW of Theory Wave 1C (repo
C:\Users\felip\Bayesian-Variable-Selection). Read Theory_work/Wave1/PROTOCOL.md (§ "Independent final review") and
Theory_work/Wave1C/PROTOCOL.md (rigour rules; "Method-side changes"), then the target
Theory_work/Wave1C/C-GROW/STATEMENT.md (v2.4), METHOD_REQUIREMENTS.md, and the full proof:
Theory_work/Wave1C/C-GROW/lemmas/00_MAIN.md, L0_toolkit.md, L1_descent.md, L2_NA_TL.md, L3_sandwich.md,
L4_assembly.md, L5_instances.md, L6_random_AR1.md. Consult cited sources as needed
(Theory_work/Wave1/W1-GEN/lemmas/*.md, Theory_work/State_of_Project/sections/*.tex,
Theory_work/Old_Projects/New_BVS_Headquarters/branch_snapshots/W1-T37R/PROOF.md, Scripts/Data_generators/gen_dev_data.R)
and the numerics files cited (Theory_work/Wave1C/C-GROW/numerics/). You may read reviews/ for context but must judge
independently; try to break the result.

Score the work on six gates, each PASS / FAIL with a one-paragraph justification:
G1 correctness of every step; G2 hypotheses used = hypotheses stated; G3 no hidden assumptions; G4 cited lemmas/inputs
have adequate status (statuses copied verbatim, nothing upgraded, conditional inputs labelled); G5 constants/rates
tracked; G6 fidelity to the method as coded/specified (SoP 02_method.tex: blocks, tables, start mode, local search,
LS0, HPM rule, budgets, implementation premises; the LS0 cap requirement MR1 is a permitted choice for the unshipped
LS0 per the Wave-1C protocol, but its use must be explicit).

Then give an uncapped score 0–10 (pass threshold 8.0 with all gates passing), and a numbered list of required fixes
(each: location, problem, concrete fix) and optional suggestions. Write ONLY your output file (named in your task).
