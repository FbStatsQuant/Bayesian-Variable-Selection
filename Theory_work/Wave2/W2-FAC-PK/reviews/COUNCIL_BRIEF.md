# W2-FAC-PK — council brief (round 2; round 1: R08 Sol 8.6 gate 3 FAIL, R09 Opus 9.1 PASS — disposition reviews/R08_R09_disposition.md)

You are one of two independent council seats (Theory Wave 2 protocol: Theory_work/Wave2/PROTOCOL.md, extending
Theory_work/Wave1C/PROTOCOL.md and Theory_work/Wave1/PROTOCOL.md). Repo C:\Users\felip\Bayesian-Variable-Selection.
Read-only except your own reply file (and an optional scratch folder reviews/<seat>_scratch/). No git state changes.

**Deliverable under review** (folder Theory_work/Wave2/W2-FAC-PK/): STATEMENT.md (v3.1, locked), lemmas/L0_imports.md,
L1_start.md, L2_neg.md, L3_static.md, L4_assembly.md, METHOD_REQUIREMENTS.md, REPORT.md. Review history (verbatim
replies + dispositions) in reviews/R01–R07; you may use it, but judge independently and try to break the result.
Sources: Theory_work/Wave2/W2-FAC-B/ (lemmas, STATEMENT), Theory_work/Wave1C/FINAL/sections/ (s3, s6, s7),
Theory_work/Wave1C/HQ_AUDIT/A1, A2, A4, Theory_work/Wave1/W1-GEN/STATEMENT.md ([OP]),
Theory_work/State_of_Project/sections/02_method.tex, Scripts/SMC_BVS/core/ (v3_fit.R, v3_run.R, cpp/v3_core.cpp).
Numerics: numerics/ (scripts + outputs; Python 3.13 with numpy/scipy at C:/Users/felip/AppData/Local/Programs/Python/Python313/python).
Citation check: reviews/CITECHECK.txt.

**Scope rule (binding):** all results are asymptotic; finite-n behaviour, astronomically large onsets and the absence of
finite-n bounds are never objections. The narrowing to the exact-Gram stage and the open items (p ≫ n, full method P6,
frontiers F2/F2′) are declared in STATEMENT §0/§5; judge whether they are honestly declared, not whether they are solved.

**Six gates** (PASS/FAIL each, with reasons):
1. Correctness of every step (L0–L4).
2. Hypotheses used = hypotheses stated (per claim P1–P5).
3. No hidden assumptions (events, uniformity over sets, ties, cap-rule evaluation, imported results outside their hypotheses).
4. Cited lemmas/results have adequate status, quoted verbatim; no status upgraded.
5. Constants and rates tracked (all o(1)/O(log log n) terms dominated; δ, ε, c₀, C_M, c_D choices consistent).
6. Fidelity to the method as coded (LS0 loop rule and prefix property, cap computation, preflight/allocation terms,
   METHOD_REQUIREMENTS' implementation instructions).

Return: the six gate verdicts, an uncapped 0–10 score, a numbered list of required fixes (if any) and optional
suggestions. Pass = both seats ≥ 8.0 with all six gates PASS in the same round.
