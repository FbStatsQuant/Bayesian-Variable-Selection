# Council brief — W3-SCR (certified screening), round 1

You are one of two independent council seats (you do not see the other seat's review). You score the FINISHED proof
package of theory ticket W3-SCR of the SMC-BVS paper project. Repo: C:\Users\felip\Bayesian-Variable-Selection (branch
main). Do NOT run any git command that changes state. Do NOT edit any file except your single report file (named in
the task message) and scratch files in your own scratch folder under Theory_work/Wave3/W3-SCR/reviews/. Work at
effort/reasoning effort high (never higher); do not spawn subagents. If you run Python (`py -3.13`, numpy/scipy
available) set OMP_NUM_THREADS=1 and keep runs short: the machine is busy.

## What the ticket claims
The method (SMC-BVS, production core in Scripts/SMC_BVS/core/) reports the best-scored model Ŝ of a Bayesian
variable-selection score F and prints the flag `local_certified` (Ŝ is a local optimum of F over one deletion / one
addition / one swap) and its search archives. The ticket proves, for ANY fixed standardised design and with no
condition on how the search started ("certified screening", item 5 of Theory_work/Wave3/PROGRAM.md): a sparse
certified reported model contains the true support S₀ with high probability under a signal-visibility condition on
(X, θ*); plus: a self-normalised refinement; a master "gap" theorem with a geometric noise complexity; a corollary for
uncertified runs (near-best scanned centres, capped searches); bridges from primitive design conditions; an
excess-set inequality and exact recovery under a near-orthogonality floor; a refit bound; a sharpness proposition.

## The package to score (read all of it)
- Theory_work/Wave3/W3-SCR/STATEMENT.md (v3.3) — every claimed result; §3 what is and is not claimed; §4 interface.
- Theory_work/Wave3/W3-SCR/CODE_CHECK.md — code facts CC1-CC6 (what the printed flags and archives mean).
- Theory_work/Wave3/W3-SCR/lemmas/L1_score.md, L2_noise.md, L3_screening.md, L4_bridges.md, L5_exact.md,
  L6_sharp.md, L7_master.md — all proofs.
- Theory_work/Wave3/W3-SCR/ASSUMPTION_MAP.md — where each assumption enters; sharpness record.
- The code itself (full access): Scripts/SMC_BVS/core/ (v3_fit.R, v3_run.R, v3_exact.R, v3_preprocess.R,
  cpp/v3_engine.h, cpp/v3_core.cpp, cpp/v3_ledger.h, cpp/v3_score.h).
- Target card and binding rules: Theory_work/Wave3/PROGRAM.md (item 5), Theory_work/Wave3/PROTOCOL.md (design-agnostic
  statements — no design family in a theorem statement; interface properties; results about the method as coded; all
  target results are asymptotic and "asymptotic only" is NOT to be treated as a limitation).
- Supporting material you may consult (not itself scored as proof): numerics in Theory_work/Wave3/W3-SCR/numerics/
  (n0_out.txt fidelity of the independent score implementation; n3_out.txt and n4_out.txt lemma falsification
  attempts; SUMMARY_N1_N2.md production-fit frequencies and boundary-violation numerics), the citation check
  reviews/CITECHECK.txt, and the review trail in reviews/ (R01 … R07 with dispositions). You are NOT bound by earlier
  reviewers' conclusions; form your own judgement and try to break the proofs.

## What to do
Re-derive the key steps yourself. At minimum: the one-step identity for F and the sufficient condition for an
improving addition (L1); the probabilistic events and their probabilities (L2); the screening argument and its
asymptotic form (L3); the bridges and the constants of Corollaries A1, A1° (L4, L3); the master gap theorem and the
uncertified-run corollaries M2, M5, SCR-G against the code facts CC6 (L7); the excess-set inequality and SCR-C (L5);
SCR-N and its two consequences (L6). Check the code facts against the code. Look for hidden assumptions, wrong
constants, non-uniform o(1) steps, mismatches between STATEMENT.md and the lemma files, and overclaims.

## Output format (mandatory)
Write your report to the file named in the task message, containing:
1. **Gate verdicts** — PASS or FAIL for each of the six gates, each with a short justification:
   G1 correctness of every step; G2 hypotheses used = hypotheses stated; G3 no hidden assumptions;
   G4 cited lemmas / external results have adequate status (every cited result is proved in the package, is a named
      standard theorem, or is a verified code fact); G5 constants and rates tracked;
   G6 fidelity to the method as coded.
2. **Score** — one number on an uncapped 0-10 scale (decimals allowed) for the package as a whole (10 = publishable
   proof with no reservations; 8 = correct and complete with only cosmetic issues; below 8 = at least one issue that
   must be fixed before the result can be relied on).
3. **Findings** — a numbered list of every issue, each with severity (BLOCKER / MAJOR / MINOR / NOTE), exact location
   (file + quoted text), what is wrong, your derivation or counterexample, and the fix you require.
4. **What you verified** — the list of results you checked completely and found correct.
Then reply with: the six gate verdicts, the score, and one line per finding (at most 25 lines).
