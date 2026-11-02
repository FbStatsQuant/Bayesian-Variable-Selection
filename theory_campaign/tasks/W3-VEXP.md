# W3-VEXP: Adversarial verification of W1-EXP

Run `git fetch origin theory/W1-EXP` and read `theory_campaign/W1-EXP/` on that branch: REPORT.md, PROOF.md (and any other proof or notes files), scripts/ and outputs.

You are an **independent referee**. Try to break the claims; don't just restate them. The claims to check: Thm 1 (EXP' from G, p <= n^A, ||mu||^2 <= Mn and SE-blk, with explicit remainder), Thm 2 / Thm 6 (unconditional favourable regime in the BO benchmark), Prop 2.1, Thm 3 / Thm 4 (CL(L) gives the two-sided ratio law, hence T27(i)), Thm 5 (linked-hub family LH carries masking + near-truth start mass + pi(S0) -> 1), and the claim that S1/S3/S4/S6 are block-orthogonal (favourable) at population level.

1. Check each claim line by line against the method spec `Docs/Methodology/METHODOLOGY_v3.md`, `Docs/Theory/theorems/00_COMMON.md` and the locked results it cites (`Docs/Theory/proofs/`, `COLLECTED_PROOFS_v2.tex`, `LOCKED_PROOFS.md`). For each step, record one of: VERIFIED, GAP (and whether it is fixable), or ERROR (with a counterexample).
2. Reproduce the key numerical evidence and counterexamples independently, with your own code (Python; R is not available).
3. Check that the method is modelled faithfully. Compare what the proof assumes the method does (move order, scoring, ESS/resampling rules, local search, cap K, streams) with the spec and with `Scripts/SMC_BVS/core/`.
4. **Deliverable:** `theory_campaign/W3-VEXP/REPORT.md` with a verdict table (claim | verdict | evidence), complete repairs of any GAP you can fix, and the confidence card.
