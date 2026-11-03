# MEET-v31 · Chair synthesis of Round 3

Inputs: `R3_A.md`, `R3_B.md` and `R3_C.md` (fresh tasks), `SYNTH_R2.md`, PC1 and PC2, and the draft `THEOREM_REVISION_INPUTS.md`. All three seats answered **R3-7 "none"**: no further method question is open in any seat's view. Item 1 is closed by applying the agreed rule to ABL-START (R3-6, all ACCEPT; see `ITEM1_ABL_START.md` once the fits finish).

## R3-1. Certificate card: CLOSED (all ACCEPT)

The card is PC2's "Recommended minimal card for v3.1" (G1, G2, L1, L2, L3 always; R optional), POST HOC, with these compatible additions:
- **A:** one declared certificate budget (scores and B&B nodes) covers L1, L2 and R; on exhaustion the item reports "unresolved". A failed certificate never changes the fit's status.
- **A:** L1 is evaluated on the finally returned Ŝ, from whichever search ended on it (final local search or LS0). An LS0 that stops on `local_limit` gives L1 = "n/a".
- **B:** G2 premise (i) reads "Lemma RO (XF VERIFIED) plus GUARD-W, the implementation fact 'any worker stop, LS0 stop or guard stop ⇒ no output' for v3.1 code: a code-audit obligation, not a mathematical gap".
- **B:** under stacking there is one card per reported record (baseline and expanded), each with its own 𝒯 and Z_𝒯.
- **C:** G2 is a probability statement joint with output, never conditional on completion. Rigorous floating-point coverage needs validated SC and VAL-FP.

The label "numerical implementation of an exact-arithmetic certificate", with η printed, stays until validated arithmetic exists. Exclusions are as PC2 lists them. C withdrew its R2 point that {Ŝ} must be isolated for C4(b) to be valid; PC2 shows that point is about sharpness only.

## R3-2. Wording for D6(i): CLOSED

A and B accepted the SYNTH_R2 text. C amended it to make "access" precise. The amendment is consistent with A's and B's R2 concessions (A: "Seat C's access/storage distinction … is right"). B's optional "(8np bytes)" is added. **Adopted text:** "A full-coordinate move round visits all p coordinates and requires scoring access to every predictor, through X or sufficient statistics (8np bytes for X). That access may be local, shared or distributed; its computation and communication costs must be counted. Neither a private copy of all X nor a private 8p² Gram matrix per worker is inherent. C7 is the declared Gram-free scoring path, law-preserving in exact arithmetic, with floating-point fidelity checked separately."

## R3-3. Estimator for E_π[h] (D7): CLOSED

All three gave the same answers to the two sub-questions:
- **(a)** The terminal frequency of the returned HPM is **dropped from the theorem-bearing list 𝓗** (all three). A and B keep it as a **descriptive diagnostic with no theorem**, printed next to e^{F(Ŝ)}/Ẑ (B). C did not ask for it; it is reporting only.
- **(b)** v3.1 ships **plain measured-round particle averages for joint h** (c_h = 0). Rao–Blackwellisation is used only for the marginal PIPs (the production estimator). No RB joint estimator ships; it is v3.2 at most (all three). B's code fact: the kernel never computes pair conditionals (`cpp/v3_engine.h:349–364`).

**Adopted spec (C's text, with A's and B's clarifications):**
- **Declaration.** 𝓗 is a finite list of bounded model-space functions. The default list is fixed from (X, y): model-size indicators, and joint inclusion on neighbour-graph edges (≤ 2pB pairs). A user may also declare h measurable in (X, y, 𝓒), i.e. fixed before stream 10. N1 is stated conditional on the frozen 𝓒, so it covers such h (A, B; status as N1).
- **Accumulation.** H_r(h) = (4N_e)⁻¹ Σ_q Σ_i h(S_rqi), taken after each complete measured round (φ = 1, equal weights after multinomial resampling; B checked the code). The run reports μ̂(h) = Σ_r Ẑ_r H_r(h)/Σ_r Ẑ_r and the equal-weight version.
- **What is not allowed.** Products of marginal RB-PIPs are not joint estimates.
- **Archive (optional).** An archive of the measured-round populations as a key → count multiset enables post hoc computation. An h chosen adaptively after the run does not inherit the fixed-h guarantee.
- **Continuous parameters.** Functionals of continuous parameters use h̄(S) = E[h | S, X, y].
- **Class and study effect.** ADDITIVE. No re-run. No joint-summary claims for the 2,400 study fits.

## R3-4. Item 9 table: CLOSED, with one classification note

All rows were accepted by all three (e1–e8, w1–w3, w5–w7, the paragraph on remaining constants, "no separate p ≪ n / p ≫ n rule", and the theory-scope paragraph). Refinements adopted:
- **w4 (C):** "the ℓ² term exceeds 1,000 exactly when n + p ≥ 2³¹" (inclusive). B re-checked: the threshold is n + p + 1 > 2³¹, which is the same thing.
- **e2 (A, B):** the exact pairwise margin is η(S) + η(Ŝ). The store keeps only (F, S), so 2η(Ŝ) is the labelled-heuristic proxy.
- **e3, n = 2 (chair-checked fact):** A said exact duplicates are "collapsed to one representative". That is wrong. Spec §4 rule 5 and `cpp/v3_core.cpp:715–728` only *report* the components {|r| ≥ 1 − 10⁻¹⁰}; duplicates are kept. B's statement is correct and goes into the spec: "At n = 2 every centred non-constant column is proportional to (1, −1), so all singleton models have exactly equal F. The exact output is ∅, or the lexicographically smallest singleton with a p-fold exact tie, reported as such." Statuses: `degenerate_n` for n = 1, the existing `no_predictors` for zero predictors, and n = 0 rejected.
- **e4 (A, B):** both sketch the same polynomial route for the tie-aware DP (greedy index-by-index choice with a feasibility max-plus DP over blocks). The invariant "DP output = the prescribed choice" stays an OPEN obligation (N3).
- **ESS 0.90 class.** A and C say (c); B says (a). B's substantive point is that the threshold defines the law of 𝓒 (pilot step and grid validation), so changing it is not a free budget change. The chair records **(c), a declared one-step dispersion budget**, for two reasons:
  - Amendment 01 defines (a) as a *modelling* convention (prior, cap). The ESS threshold is not part of the model or the target.
  - B's point holds equally for the other (c) budgets, which also enter the law of 𝓒: H₀ is the calibration population and T_e caps the grid (`v3_calib.R`, `cpp/v3_calib.h:25–92`). The adopted constants paragraph already says "changing them is not automatically law-preserving".
  B's caveat is attached to the row: "defines the law of 𝓒; carried by the theorems as a hypothesis (Theorem G needs the same threshold for pilot and grid)". This is a label; no setting changes.
- **Remaining-constants paragraph:** C's replacement text is adopted (60 halvings (d); one-nat thresholds as (c) diagnostic criteria; values are conventions, not optima).

## R3-5. Conflicts in the draft inputs: CLOSED (all three agree)

- **(i)** Split V1(a): (a1) Ẑ and the RB marginal PIP stay as locked; (a2) a general bounded h at the P-D7 accumulation point is a PROOF SKETCH (N1). A's reading, unchecked: (a2) may be a short extension of the locked terminal-round lemma.
- **(ii)** Lemma RO stays as recorded (XF VERIFIED). GUARD-W, i.e. the v3.1 worker, merge and LS0 code satisfying "any stop ⇒ no output", is a new code-audit obligation (engineering, class (iv)), not a method question.

## R3-6. Item 1 procedure: CLOSED (all ACCEPT)

Conventions stated before the results, all compatible with SYNTH_R2 §2:
- **(A)** A design where an arm did not finish is inconclusive. An arm-A stop is a delivery event.
- **(B)** A design where any of arms A–C has no complete output, or whose pooled log Ẑ disagree by > 1 nat, is inconclusive and counts toward neither Outcome 1's nor Outcome 3's 9/12.
- **(A, B)** If fewer than 9 designs are conclusive, the result is Outcome 2. If fewer than 12 designs complete, the same proportions apply to the completed designs, and both S4 and both S5 designs are still required for Outcome 3.
- No outcome reopens item 1 in this meeting. Outcome 3's follow-up goes to HQ.

## R3-7. Anything else

"None" from all three seats. Notes for the minutes (not method questions):
- A's R2 reversal criterion for D5 is recorded for HQ to read against the full rescoring.
- W-cal, the merged-LS0 replay, the GUARD-W audit and IND-T for streams 10..9+R′ are engineering actions.
