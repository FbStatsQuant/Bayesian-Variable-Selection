# W2-PREM: Discharge the premises of Theorem B (restated T24) asymptotically

W1-T24G (branch `theory/W1-T24G`, folder `theory_campaign/W1-T24G/`) proved the deterministic Gibbs-path repair bound, Theorem B. Its asymptotic usefulness rests on named premises:
- **NL0(a):** no leakage at supersets with a extras, including a = 1 for correlated nulls;
- **UDEL(a ≥ 2);**
- **TS;**
- **TL(𝒵, A);**
- **BTP;**
- **IND:** conditional independence of terminal trajectories; this one is genuinely open in the masked regime.

In W1-T24G's own assessment, these are P(true) 0.75 and P(provable) 0.5.

**Goal:** prove as many of these as possible under G, R, SE and BM-∞ (with s₀ and d fixed), or under the weakest clean extra condition, and pin down exactly what fails.
1. Read REPORT.md §4 and PROOF.md in W1-T24G. Also read the related locked results: T22iii (EXP′), T03 (and the restated T03♯ on branch `theory/W1-T03R`), and T09/T10.
2. For each premise, give one of: PROVED (with proof), PROVED UNDER (an explicit extra condition), COUNTEREXAMPLE, or OPEN (with the obstruction).
3. **IND:** read how the implementation draws its random streams (`Scripts/SMC_BVS/core/`, `Docs/Methodology/METHODOLOGY_v3.md`, and the CAL/EX-S idealisations in `Docs/Theory/theorems/00_COMMON.md`). Decide whether terminal trajectories are conditionally independent given the stage-T population, and prove it, or show why not.
4. Where the proofs need "uniform log-BF expansions of EXP type over finite families", try to supply them, ideally from one lemma shared with EXP′.
5. **Deliverable:** `theory_campaign/W2-PREM/REPORT.md`, with a premise-by-premise table, proofs, and the confidence card.
