# BRIEF — W1-T03R (verbatim stored prompt, fired 2026-11-02 16:32 UTC)

You are a cloud research run in the SMC-BVS theory campaign (HQ-managed). TASK_ID = W1-T03R. Work as a careful research mathematical statistician; take the time it needs.

## PROTOCOL
- Branch `theory/W1-T03R` from main; write ONLY under `theory_campaign/W1-T03R/`. Never touch main, no PR, no notifications.
- First commit: save this prompt as `theory_campaign/W1-T03R/BRIEF.md`; `git push -u origin theory/W1-T03R`.
- Commit AND push after every meaningful step; the run may be stopped any time.
- Status words only: PROVED (complete, checked line by line), PROOF SKETCH, COUNTEREXAMPLE (reproducible), CONJECTURE, OPEN. Never upgrade; results are candidates pending cross-family review.
- Numerics: Python 3 (pip install numpy scipy sympy mpmath); R NOT available. Scripts in `theory_campaign/W1-T03R/scripts/`, record findings.
- Notation of `Docs/Theory/theorems/00_COMMON.md`. Stay in scope.
- Deliverable `theory_campaign/W1-T03R/REPORT.md`: Headline; refined statements in full with named hypotheses; proofs (full new proofs of changed steps in PROOF.md or PROOF.tex); evidence; what fails and why; needs escalation; outside scope; confidence card (statement, P(true), P(provable), crux).

## Context
Paper (JRSS-B target) Thm 1 = T03 selection consistency with lemmas T01 (contrast reduction) and T02 (dimension control, exclusion of strict supersets). All three are PROVED-LOCKED in wave 3 (Opus lead + 2 Opus xhigh reviewers; not adopted), files `Docs/Theory/proofs/T01_T02_contrast_dimension/` (STATEMENT.md, PROOF_v3.tex) and `Docs/Theory/proofs/T03_A2_selection_consistency/` (STATEMENT.md, PROOF_v2.tex); register `Docs/Theory/proofs/LOCKED_PROOFS.md`; theorem files `Docs/Theory/theorems/T01_*, T02_*, T03_*`; prior/score definitions in 00_COMMON.md and `Docs/Methodology/METHODOLOGY_v3.md` (g-prior marginal, Beta-Binomial BB(1,p) size prior, cap K). The frozen paper plan requires a restatement. Common setting for all targets: triangular array, s0 FIXED (14 in the study), p_n <= n^A, B <= 16; the generator's growing rule s0 = floor(sqrt(n)) is NOT covered.

## TASK
1. T02(i): replace the 2^{-m} model-size tail by the EXACT BB(1,p) tail; this should cut the size threshold m_n from ~200 to s0 + O(s0 log n / log p). Prove the sharpened tail bound with explicit constants.
2. T03 restatement: restrict SE (sparse eigenvalue condition) to the comparison unions actually used in the proof (not all subsets); replace the provisional constant M* by BM-inf or an unnamed constant; s0 fixed, p_n <= n^A, triangular array. Re-derive: posterior mass outside S0 is O_P(sqrt(log n / n)); PIPs within that of the 0/1 truth; HPM and MPM of the true posterior = S0 w.p.->1; without beta-min, large signals still get PIP -> 1.
3. Identify exactly which steps of the locked proofs change; write the new proofs of changed steps in full; cite unchanged steps by label.
4. n=200 honesty paragraph: at n=200 SE is impossible (rank <= 199 vs subsets of 215-229 columns) and beta-min fails by ~100x in squared signal. Write the precise disclosure paragraph; give any finite-n statement that survives.
5. Evaluate the new tail bound numerically at (n,p,s0) = (200,500,14), (200,1000,14) and larger n; compare with the old bound.
Read first: 00_COMMON.md, the T01/T02/T03 statements and proofs, METHODOLOGY_v3.md prior sections.
