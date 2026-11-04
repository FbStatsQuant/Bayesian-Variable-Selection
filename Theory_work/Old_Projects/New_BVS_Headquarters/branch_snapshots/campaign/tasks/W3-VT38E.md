# W3-VT38E: Adversarial verification of W1-T38E

Run `git fetch origin theory/W1-T38E` and read `theory_campaign/W1-T38E/` on that branch: REPORT.md, PROOF.md (and any other proof or notes files), scripts/ and outputs.

You are an **independent referee**. Try to break the claims; don't just restate them. The claims to check: Theorem T38(b)-R (the composition, corrected liminf form), counterexample C1 (SMC extinction despite start and bridge mass), Thm D1 / Prop D3 (LT and SHARE), route D2 (pilot first round scores S0 when a one-flip neighbour has start mass > 1/10, via Lemma S), route E3 (LS0), Lemma E1 and CF2 (eligibility failure), and the compatible family CF(c).

1. Check each claim line by line against the method spec `Docs/Methodology/METHODOLOGY_v3.md`, `Docs/Theory/theorems/00_COMMON.md` and the locked results it cites (`Docs/Theory/proofs/`, `COLLECTED_PROOFS_v2.tex`, `LOCKED_PROOFS.md`). For each step, record one of: VERIFIED, GAP (and whether it is fixable), or ERROR (with a counterexample).
2. Reproduce the key numerical evidence and counterexamples independently, with your own code (Python; R is not available).
3. Check that the method is modelled faithfully. Compare what the proof assumes the method does (move order, scoring, ESS/resampling rules, local search, cap K, streams) with the spec and with `Scripts/SMC_BVS/core/`.
4. **Deliverable:** `theory_campaign/W3-VT38E/REPORT.md` with a verdict table (claim | verdict | evidence), complete repairs of any GAP you can fix, and the confidence card.
