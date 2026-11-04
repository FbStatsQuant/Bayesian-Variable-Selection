# FINAL REPORT — T14(i) (L-FM, singleton case): first-moment evidence consistency

**Result: proved (Opus 5.5 lead; independent reviews: Astra x2 + Opus xhigh; campaign review pending); not adopted.** Adoption is Felipe's word.

Date: 2026-10-22. Protocol: proof.md with Felipe's overrides for this run, plus Protocol Amendment 1 (Stage B) and its correction (the Opus reviewer runs on Claude Personal).

- Final proof: `proof/PROOF_v3.tex` and `proof/PROOF_v3.pdf` (4 pages; SHA-256 of the .tex c12954d1…97efdd4).
- Statement: `STATEMENT.md` (SHA-256 7e94d7e3…f36ffd).

## 1. What was proved, in plain words

The final SMC run estimates the evidence Z (the normalising constant of the posterior). Each island produces an estimate Ẑ_r. Fix any one model S° in advance. At each temperature t, let η_t be the posterior-path mass outside S°, that is, how far the bridge distribution q_t is from putting all its mass on S°. The theorem says the average relative error of the island estimate is small when these masses are small:

  E|Ẑ_r/Z − 1| ≤ (2/(1 − ε_*)) · (η_0 + η_1 + … + η_T),  where ε_* = max_t η_t.

There is also a sharper middle bound, written with b_t = q_0(S°)/q_t(S°):

  E|Ẑ_r/Z − 1| ≤ [Σ_t (b_{t−1}η_{t−1} + b_tη_t) + |1 − b_T|]/b_T.

Further results:
- The exact identity Ẑ_r/Z = A_T/b_T holds.
- The same bounds hold for the pooled estimate Ẑ (the average of the four islands).
- An explicit two-state example shows that the endpoint term |1 − b_T| cannot be dropped: without it, the bound fails.

These bounds hold for every particle count N ≥ 1. They need only:
- exact arithmetic;
- independent random streams, with the final run independent of calibration;
- exact iid π₀ starting draws;
- multinomial resampling;
- one move round per stage that leaves the current bridge law invariant.

They do not need EXP or EXP′, mixing, the statistical model, or any other v3 conjecture. The T12 identity they build on is re-proved inside the proof.

**Caution for use.** This is a first-moment (L¹) statement. It gives consistency of Ẑ only when Σ_t η_t is small, that is, when one model carries nearly all the mass along the whole temperature path. It says nothing about variance (Sol's J6 example has E(Ẑ/Z)² ≈ 10⁶ while the L¹ error is 0.002), and nothing about multi-model sets. Part (iii) of the theorem file covers sets; parts (ii) and (iii) were not in this run.

## 2. Proof strategy

1. Change of temperature: q_{t−1}(G_t h) = (Z̄_t/Z̄_{t−1}) q_t(h).
2. One-stage conditional mean of the empirical population.
3. Induction gives E[A_t q̂_t(f)] = b_t q_t(f).
4. Since R_t(S°) = 1, each increment A_t − A_{t−1} only sees mass off S°, so E|A_t − A_{t−1}| ≤ b_{t−1}η_{t−1} + b_tη_t.
5. Telescoping, plus the deterministic endpoint term, gives the middle bound.
6. Using b_s/b_T ≤ 1/(1 − ε_*) gives the final bound.
7. The pooled case follows from the triangle inequality.
8. The two-state example has T = N = 1: the error is 0.18, while the bound without the endpoint term is 6/55 ≈ 0.109.

## 3. Statement changes

There were no mathematical changes. The statement analysis concluded it was correct as stated (proof.md step 1(a)).

- **Notation (after Astra #1 finding 1).** "q₁ = π, Z = m(∅)Z̄₁" clashed with stage indexing. It was rewritten so that a numerical subscript is always a stage index (Z = m(∅)Z̄_T). This is logged in STATEMENT.md §4.
- **Reading of an informal sentence.** "The endpoint term |1 − b_T| is essential" is read as: in the abstract setting, dropping the term breaks the bound for some instance. This reading is stated as (i-d), and it is not claimed that such an instance comes from a real SMC-BVS data set. All three reviewers judged this reading fair.

## 4. Review history

| Stage | Reviewer | Input | Verdict | Findings |
|---|---|---|---|---|
| A | Astra #1 (gpt-6-astra, high), session <uuid> | PROOF_v1 | verified | 1 exposition (stage/temperature subscript clash): accepted, fixed in v2 |
| A | Astra #1, same session (resume) | PROOF_v2 + log | verified | agrees with the fix; no new findings |
| B | Astra #2 (gpt-6-astra, high), new session <uuid> | PROOF_v2 | verified | none |
| B | Opus 5.5 xhigh (Claude Personal, T3 delegate_task) | PROOF_v2 | verified | 3 exposition: conditioning on F_{t−1}; (i-c) wording; remark citing T12. All accepted, unified into v3 |
| B | Astra #2 (resume) | PROOF_v3 + log | verified | agrees with all answers; none |
| B | Opus 5.5 xhigh (new round task) | PROOF_v3 + log | verified | agrees with all three answers; none |

- Fatal or gap findings: none, in any round. CLAIMS_OF_FATAL_FLAWS.md records this and logs the exposition findings with the answers.
- Astra judge: not used.
- All replies are saved in `review/`. Stage B Opus scratch scripts are in `review/stageB_opus_scratch/`.
- Temp packet folders were deleted at the end; a copy of the Stage A packet is kept in `review/packet_stageA_copy/`.

## 5. Numerical sanity checks (supporting only, not evidence of proof)

- **Sonnet assistant** (`helpers/NUMCHECK_T14i.md`): exact enumeration over 108 abstract instances and 324 choices of S°, with |Ω| ≤ 4, N ≤ 3, T ≤ 3.
  - The identities hold to 1e-15 relative.
  - The bound was never violated; the largest ratio of the error to the middle bound was 0.88.
  - The bound without the endpoint term failed in 35 cases.
  - The (i-d) numbers were reproduced exactly.
- **Opus reviewer:** independently ran 84 plus 200 exact instances, including non-reversible invariant kernels, with the same outcome.

## 6. Agent and call counts

| Model | Calls | Purpose |
|---|---|---|
| Sonnet 5.5 | 1 agent | LaTeX compile of v1 + exact numerical check |
| Haiku 5.5 | 0 | |
| GPT-6 Astra (high) | 4 calls in 2 sessions | #1: review r1 + ruling r2; #2: review r1 + ruling r2 |
| Astra judge (xhigh) | 0 | |
| Opus 5.5 xhigh reviewer | 3 launches | 1 on Claude Work, cancelled within minutes per the correction, output unused; 2 on Claude Personal (r1 review, r2 ruling) |
| Fable / Sol | 0 | |

The lead (Opus 5.5 high, this thread) did the mathematics, the files, the later LaTeX compiles (v2, v3), the packets and the Astra calls.

## 7. Files

- STATEMENT.md
- proof/PROOF_v1–v3 (.tex, .pdf)
- review/
- helpers/numcheck_T14i.py and helpers/NUMCHECK_T14i.md
- CLAIMS_OF_FATAL_FLAWS.md
- STATUS.md
- this report

Next: Stage C (the managing lead's campaign review: Fable 5.1 + Astra across all proofs).

## Stage C (campaign review, 2026-10-22)

- Final reviewers Fable 5.1 (high) and Astra (xhigh) both hold the proof correct (source: COLLECTED/review/FABLE_STAGE_C_phase2.md). Exposition edits applied: none (no edits; final file unchanged). 
- Result label now: proved (Opus 5.5 lead; independent reviews Astra x2 + Opus xhigh; campaign review Fable 5.1 + Astra: correct); not adopted.
