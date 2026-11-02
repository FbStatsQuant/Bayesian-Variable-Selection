# FINAL REPORT — T31 (T22), part (i): what the 0.05·Ẑ bound certifies

**Result: proved (Opus 5.5 lead; independent reviews: Astra x2 + Opus xhigh; campaign review pending); not adopted.**
Adoption is Felipe's word.

Final files: `STATEMENT.md`, `proof/PROOF_v3.tex` and `proof/PROOF_v3.pdf` (5 pages).

## What was proved, in plain words

Fix the data and a calibration that succeeded (grid frozen). Assume exact arithmetic and ideal random streams (EX-A,
EX-S), fresh final streams (CAL), and, **as an explicit hypothesis**, T12's unbiasedness E_c[Ẑ] = Z. T12 is a sibling
conjecture and is not proved here. Then:

- **(a) Coverage.** P_c(Z ≥ αẐ) ≥ 1 − α for every α ∈ (0,1). So the reported 0.05·Ẑ is below the true evidence Z with
  probability at least 95%. Proof: Markov's inequality.
- **(b) Log bias.** log Ẑ is a bounded random variable, and E_c log Ẑ ≤ log Z: on the log scale the estimate is biased
  downwards on average. Proof: Jensen's inequality. The proof first shows that Ẑ is positive and takes finitely many
  values; one step is Q_S ≥ yᵀy/(n+1) > 0.
- **(c) Not a relative-error interval.** The properties behind (a) and (b) say nothing about how far *below* Z the
  estimate can be. There are estimators with all those properties (positive, finitely valued, unbiased, even with four
  i.i.d. unbiased islands) that underestimate Z by any chosen factor with probability as close to 1 as you like, while
  (a) still holds. So no two-sided "Ẑ is within a factor c of Z" guarantee follows.
- **(d) Conditioning on a final flag can destroy coverage.** Take the final E2 flag ("SD of the four log Ẑ_r > 1").
  Both SD conventions are covered. There are such estimators where coverage, conditional on the flag being **raised**,
  is 0 (d1), and others where coverage, conditional on the flag **not** being raised, is below any chosen γ (d2). So
  coverage given the final flags does not follow "automatically".

(c) and (d) are **non-implication** statements: they show the premises do not give more. They do not claim that a
real data set produces those laws. For fixed data, the actual estimator does satisfy a sure bound
e^{−Δ}Z ≤ Ẑ ≤ e^{Δ}Z, where Δ = max d − min d depends on the data and is not reported. That bound was found by the Opus
reviewer and is now in the last Remark of the proof. It is why the non-implication reading is the intended one.

## Statement changes

None to hypotheses or conclusions. The step-1 decision was (a), correct as stated. The source text is quoted verbatim in
STATEMENT.md. "Under T12" became the explicit hypothesis (H-T12). The two informal cautions ("not a relative-error
interval", "conditioning on final flags does not preserve coverage automatically") were written as precise
non-implication statements (c), (d). After review, explanatory wording only was revised twice; the reviewed versions are
kept in `review/STATEMENT_as_reviewed_r1.md` and `_r2.md`. Every reviewer confirmed that no hypothesis or conclusion
changed and that the statement is a faithful formalisation of clause (i).

## Review history

| Stage | Reviewer | Version | Verdict | Findings |
|---|---|---|---|---|
| A | Astra #1 (GPT-6 Astra, high; session <uuid>) | v1 | verified | none |
| B r1 | Astra #2 (GPT-6 Astra, high; new session <uuid>) | v1 | verified | none |
| B r1 | Opus 5.5 xhigh (read-only agent) | v1 | verified | 11 exposition (incl. the sure bound) |
| B r2 | Astra #2 (resumed) | v2 + log | verified | 2 exposition ("only true one" overclaim; unverifiable "method does not report") |
| B r2 | Opus (continued) | v2 + log | verified | 5 exposition (same overclaim; small-Δ derivation; implicit steps; measurability proviso; file name) |
| B r3 | Astra #2 (resumed) | v3 + log | verified | none |
| B r3 | Opus (continued) | v3 + log | verified | 3 exposition (cosmetic; recorded, not applied so the final text is the reviewed v3) |

No reviewer, in any round, raised a fatal or gap finding. All exposition findings and the lead's answers are in
`CLAIMS_OF_FATAL_FLAWS.md`; the reviewers agreed with every answer. The Astra judge was not needed.
Replies: `review/astra_01_review_r1.log`, `review/stageB_astra2_r{1,2,3}.log`, `review/stageB_opus_r{1,2,3}.md`.

Sanity check (not evidence of proof): a Haiku assistant computed the example laws of (c), (d1) and (d2) exactly for
several α, γ, c₀, η. All 104 checks passed and the canary was exact (`helpers/numcheck/check.py`, `results.txt`).

## Limits and open points

- Conditional on (H-T12) = T12(iii), which is being proved in a sibling thread. If T12 holds only for almost every
  calibration, (a)–(b) hold for those calibrations.
- The identification of P_c with the conditional law given 𝓒 needs joint measurability of the final run in (c, streams).
  This is a standard proviso, stated in STATEMENT §1 and in Remark 4; the conclusions themselves are stated for P_c.
- Exact arithmetic (EX-A) is essential: no coverage claim is made for floating-point evidence (RULINGS 21, NUM).
- Whether real data sets realise laws like those in (c)–(d) is not addressed. For this, see the file's other parts and
  T28/V11.

## Counts

- Astra: 2 sessions, 4 calls (Astra #1: 1 call; Astra #2: 3 calls). Astra judge: not used.
- Opus 5.5 (xhigh): 1 reviewer agent, 3 calls (r1 plus 2 continuations).
- Haiku 5.5: 1 agent (exact numeric check). Sonnet: 0. Fable: 0. Sol: 0.
- Temp packet folders (`<PC_TEMP_PATH>`) deleted.

## Stage C (campaign review, 2026-10-22)

- Final reviewers Fable 5.1 (high) and Astra (xhigh) both hold the proof correct (source: COLLECTED/review/FABLE_STAGE_C_phase2.md). Exposition edits applied: none (no edits; final file unchanged). 
- Result label now: proved (Opus 5.5 lead; independent reviews Astra x2 + Opus xhigh; campaign review Fable 5.1 + Astra: correct); not adopted.
