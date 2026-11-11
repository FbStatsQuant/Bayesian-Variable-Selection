# Council brief (W3-RM), round 2 — identical for both seats

You are a council reviewer (effort / reasoning effort HIGH; never use a higher setting; do not spawn subagents).
Repository: C:\Users\felip\Bayesian-Variable-Selection (branch main). Do NOT change git state. Write exactly ONE file,
named in your task; do not edit anything else. Python with numpy is `py -3.13`.

## Package under review (ticket W3-RM, Theory Wave 3 of the SMC-BVS paper: "Theorem 3", the reported model)
- Theory_work/Wave3/W3-RM/STATEMENT.md (v1.2)
- Theory_work/Wave3/W3-RM/lemmas/: L0_core.md, L1_fixed.md, L1b_rss.md, L2_NAF.md, L3_SANDR.md, L3b_rate.md,
  L4_formR.md, L5_E4.md, L7_examples.md
- Theory_work/Wave3/W3-RM/SHARPNESS.md, ASSUMPTION_MAP.md, numerics/SUMMARY_SHARPNESS.md (observations only)
- Theory_work/Wave3/W3-RM/citecheck.py, reviews/CITECHECK.txt
Binding rules: Theory_work/Wave3/PROTOCOL.md and PROGRAM.md (item 3), which extend Theory_work/Wave2/PROTOCOL.md,
Wave1C/PROTOCOL.md, Wave1/PROTOCOL.md. All results are asymptotic by decision of the owner: never treat "asymptotic
only" as a defect. Sources cited by the package may be opened freely (Theory_work/Wave1C/C-GROW, Wave1/W1-GEN,
Wave1/W1-N3, Wave1C/C-PACK, C-DLV, C-ENG, Wave2/W2-APP, W2-LOC2, W2-UNI, W2-FAC-PK; code Scripts/SMC_BVS/core/).
Do NOT read the lead's REPORT.md or LOG.md. Earlier reviewer replies exist in reviews/ (R01–R08 with dispositions); you
may consult them to see what was already raised, but form your own judgment and re-verify.

## Your job: try to break the result, then score it
Check the two main theorems (C1) RM-F and (C2) RM-R through the core (C0) RM-0, Lemma E4 (C3), the examples (C4) and
the sharpness record (C5). Read the NEW mathematics line by line: Lemma NA-F and N-loc (L2_NAF.md), Lemma τ and B2τ
(L1b_rss.md), Lemma SAND-R (L3_SANDR.md, a delta-proof — open the reused source lines of
Theory_work/Wave1C/C-GROW/lemmas/L6_random_AR1.md and Theory_work/Wave2/W2-UNI/lemmas/L2_k0.md for at least the
selection-removal, spherical-tail and ladder steps) and SAND-R′ (L3b_rate.md), Lemma D-loc and the p = 1 branch
(L4_formR.md), Lemma E4 against the code (Scripts/SMC_BVS/core/cpp/v3_start.h, v3_core.cpp:388-520,
v3_engine.h:370-420, v3_run.R:80-140), the verification that GEN (C6)'s design satisfies RM-F (SHARPNESS.md §3.2).
Look for: false steps; missing cases; hypotheses used but not stated; stated but unused; mismatch between the bridge
table / input map of STATEMENT §4 and the lemmas; constants or rates that do not track; statuses of cited results
quoted wrongly or upgraded; overclaims in STATEMENT §0/§4/§6, L7_examples.md, SHARPNESS.md; any design family inside a
theorem statement (forbidden); infidelity to the method as coded.

## Six gates (each: PASS / FAIL with a one-paragraph justification and file:line evidence)
G1 Correctness of every step.
G2 Hypotheses used = hypotheses stated.
G3 No hidden assumptions.
G4 Cited lemmas have adequate status (statuses quoted verbatim, none upgraded; each new lemma has a cross-family check
   on file).
G5 Constants and rates tracked.
G6 Fidelity to the method as coded (and to the binding program: primitive, partition-free where possible, no design
   family in a theorem statement, e4 closed, examples and sharpness record honest).

## Output (in your file)
1. Gate verdicts G1–G6.
2. An uncapped score from 0 to 10 (one decimal), with the reasons for every point deducted.
3. Numbered findings: severity (FATAL / MAJOR / MINOR / NIT), location (file:line), the precise problem, proposed fix.
   Mark which findings are REQUIRED for a pass.
4. One paragraph: is Theorem 3, as stated in v1.2, fit to be the paper's main reported-model theorem? What is the
   single most valuable strengthening still missing?
Pass rule (for your information): both seats ≥ 8.0 with all six gates PASS in the same round.
Final message: gate verdicts, score, and the REQUIRED findings (short).

## Round 2 note
This is round 2 (STATEMENT v1.2.1). Round 1 did not pass: seat A scored 8.8 with gate G6 FAIL (the sharpness record
labelled the L2 numerics as violations of the leakage assumption), seat B scored 8.9 with all gates PASS. The round-1
replies are reviews/C1_council_astra.md and reviews/C1_council_opus.md; what the lead changed in response is listed in
reviews/C1_disposition.md. You are a FRESH seat: review the whole package as it now stands by the brief above (do not
limit yourself to the round-1 findings), and in addition verify that each round-1 finding was actually fixed in the
current files. Do not run citecheck.py (it rewrites reviews/CITECHECK.txt); read it and the output instead.
