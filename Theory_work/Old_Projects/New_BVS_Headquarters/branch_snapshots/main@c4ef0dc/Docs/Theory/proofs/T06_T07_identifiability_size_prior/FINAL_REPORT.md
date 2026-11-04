# FINAL REPORT: T06 (identifiability and exact ties) and T07 (size-only ranking ceiling and Bayes decisions)

**Result: proved (Opus 5.5 lead; reviewed by 2 independent Opus 5.5 xhigh, CP + CW); not adopted.**
- T06(ii)(b) is conditional on T03 (explicit hypothesis H-T03).
- Every other clause is unconditional.

Date: 2026-10-22. Wave 3 (WAVE3_BRIEF.md).

- Proof: `proof/PROOF_v2.tex` and `proof/PROOF_v2.pdf` (9 pages).
- Statement: `STATEMENT.md`.

## What was proved, in plain words

**T06(i): when do two models always get the same score?** Exactly when their columns have the same "outer product" X_SX_Sᵀ. That forces the same number of variables.
- Two models that span the same space but have different outer products never tie identically.
- Example: x₁, x₂ versus x₁, (x₁+x₂)/√2. These differ because the slab prior N(0, nσ²(G+I)⁻¹) is not a g-prior.
- Under Gaussian noise, an exact tie between models with different outer products happens with probability 0.
- So under NIS, the tie rule is (almost surely) never needed.

**T06(ii): the tie rule is not needed at the truth when the truth has most of the posterior.** Whenever π(S₀) > ½, S₀ is the unique best model; this needs no assumption. If T03 holds, that event has probability → 1.

**T06(iii): duplicated columns, and how far apart two truths are.**
- Two exactly duplicated columns (x_i = ±x_j) make the swapped models equally probable, so each such model has posterior < ½.
- No selection rule can tell apart two truths whose signals are closer than about the noise level. The maximal error is at least Φ(−‖μ₁−μ₂‖/(2σ*)).
- The method's near-duplicate warning (|r| ≥ 1 − 10⁻¹⁰) is neither necessary nor sufficient for exact ties.

**T07: decisions.**
- (i) No prior that depends only on model size can fix a ranking error between models of the same size.
- (ii) The HPM minimises posterior 0–1 loss, the MPM minimises posterior Hamming loss, and under the cap the best Hamming decision keeps the min(K, #{PIP > ½}) largest PIPs.
- (iii) For the reported HPM and estimated PIPs these guarantees hold exactly when:
  - the best model was actually scored (Ŝ = S† iff S† ∈ 𝒮); or
  - the PIP error is controlled: the excess Hamming risk is ≤ 2‖p̂ − PIP‖₁.

## Statement changes (approved by the statement checker, review/STATEMENT_CHECK.md and STATEMENT_CHECK_2.md)

1. **Necessary, T06(iii) two-point bound.** As literally stated ("every selector"), the bound is false: a selector can use the raw mean of y^r when the intercepts differ. It now holds in two forms:
   - for location-invariant selectors (anything computed from the standardised data, as the method's target is);
   - for every selector when the two truths have equal mean of y^r ("mean-matched"; this is not α₁ = α₂).
2. **T06(ii).** T03 is taken as an explicit hypothesis (H-T03, its conclusion (i) quoted verbatim), as the brief asked. The strict-maximiser part is proved without any hypothesis.
3. **Strengthenings:**
   - "equal spans need not tie" becomes "never tie identically", with examples that exist exactly when K ≥ 2 (every n ≥ 4) and never when K = 1;
   - "probability-zero ties" holds under G alone, for every non-structural pair;
   - "neither atom exceeds ½" is strict, and PIP_i = PIP_j is added.
4. **Readings that make informal sentences precise:**
   - the near-duplicate warning, made into a mathematical statement;
   - the action spaces and tie handling of the Bayes decisions;
   - T07(iii), formalised as exact transfer conditions;
   - the score formulas of 00_COMMON §1, quoted verbatim.

## Review history

- **Statement checker** (fresh Opus 5.5 xhigh): approved all 11 change-report items, with required edits (all applied). It was consulted once more after round 1 and approved two precisions.
- **Round 1 (PROOF_v1)**: CP and CW both returned "not verified". There were no fatal findings; both raised the same two gaps:
  - the score formulas were not quoted in the statement;
  - the "n ≥ 4" remark was not proved.

  Both gaps were accepted and fixed (CLAIMS_OF_FATAL_FLAWS.md), together with all the exposition points.
- **Round 2 (PROOF_v2)**: CP and CW both returned **verified**, with no fatal or gap findings. Each confirmed that all its round-1 findings were resolved.
- **Exposition notes left open**, all agreed to affect no result, and not applied so the reviewed text stays exact:
  - the null-event convention for π and PIP;
  - the symbol c is reused;
  - one implicit line, S† = S†_w, in Remark 6.8;
  - F is defined on Ω in the proof but on all of 2^[p] in the statement's notation line.
- **Judge**: not needed.

## Agent counts

| Role | Model | Count |
|---|---|---|
| Statement checker | Opus 5.5 xhigh | 1 agent (consulted twice) |
| Reviewer CP | Opus 5.5 xhigh | 1 agent (2 rounds, resumed) |
| Reviewer CW | Opus 5.5 xhigh | 2 delegate_task runs (rounds 1 and 2) |
| Helpers | none | 0 |
| Judge | none | 0 |
| Fable | none | 0 (the campaign review is run by the managing lead) |

## Files

- STATEMENT.md
- proof/PROOF_v1.* and PROOF_v2.* (final)
- review/:
  - CHANGE_REPORT.md
  - STATEMENT_CHECK.md and STATEMENT_CHECK_2.md
  - round1/ and round2/ (packets and replies)
  - pre-edit copies of STATEMENT
- CLAIMS_OF_FATAL_FLAWS.md
- STATUS.md
- helpers/check_T06_T07.py with its output, plus edit scripts. These are numerical sanity checks (seed 1, local, all pass), not part of the proof.
