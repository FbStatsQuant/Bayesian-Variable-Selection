# case1 · gpt-6.2-sol (codex, reasoningEffort high), SCORED run

Same wrapper as the 6.1 run: read in chunks of 120 lines, read no other file. Run about 19:10 to 19:15 CT (wall ≈ 5 min, manager's clock). Full reply: T3 child thread "SOL62 A/B case1 · gpt-6.2-sol". Header line correct.

**Verdict:** LOCK-WITH-AMENDMENTS. This is the same as the stored 6.1 original.

**Findings:**
- **L1-1 MAJOR.** The row-wise KL(ii) reading fails for design-dependent α. Counterexample: α = X²_{𝒞,2,1}; given row 1, y = χ²₁ + N(0,1), which is not Gaussian. Fix: restrict to a fixed intercept and deterministic slopes/variance. **Known answer: CAUGHT.**
- **L1-2 MAJOR.** CorH-U ⇒ CorH-plus(b) fails because C̄_H ≠ C_H(s,A). This is the same new finding as 6.1's L1-2: two independent reviewers found it, so it is *likely real*. Adjudication pending.
- **L1-3 MAJOR.** The SL s̃ identification in the singular extension fails: Moore–Penrose slopes vs. other valid slopes give different supports (the kernel is spanned by 1_p). This is *new*, and was not in 6.1 (either run) or in the stored review. The manager rates it plausible; adjudication pending.
- **L1-4 MINOR.** Bundles four scope edits:
  - carry positive total variance;
  - MIS-R(ii) needs its own class-event hypotheses;
  - "conditionally" in the (d) summary (stored L1-2: **real, secondary**);
  - the conditional mean needs an integrability convention (stored L1-3: **real, secondary**).

  It also says E3 is a fixed-design specialization.
- **L1-5 MINOR.** CorGb-plus constants and dependence must be stated (c_R, M₀, A fixed; c varies with the liminf), and the design event displayed. It correctly marks G.2/A0 as not supplied.
- **L1-6 MINOR.** (RD): define Π_c, give a Borel extension at z = 0, and show measurability of the parameter-posterior masses. This is stored L1-4: **real, secondary.**
- **L1-7 MINOR.** Dependency ledger:
  - separate direct inputs from inherited ones;
  - POST2:E/A1 are missing from the plan's summary;
  - Cramér needs a citation;
  - "BASE `D_hellinger.md`" is POST2's file (PROMPT line 245 vs line 30). **Verified real** (a citation-owner error).

**Q1–Q6.** All answered in more depth than 6.1: an explicit sample-Gram route for Q2, explicit M′_n for Q3, and numerics advice in Q6. "Not supplied" is marked item by item, and missing sources are not raised as a finding.

**Score.**
- Known answer: caught.
- Secondaries: 3/3.
- New: 2 plausible (L1-2, which is shared with 6.1, and L1-3) + 1 verified real (L1-7 citation owner).
- False: 0.
- Nitpick: 0 to 1 (part of L1-4/L1-5 is scope housekeeping).
- Fidelity: better than 6.1. Its verdict matches the stored review, and it does not inflate missing inputs into a MAJOR finding.
- Speed: about 2× slower than 6.1 here.
