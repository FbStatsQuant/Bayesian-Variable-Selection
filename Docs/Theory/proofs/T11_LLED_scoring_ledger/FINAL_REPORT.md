# FINAL REPORT — T11(iii): the final run's iid π₀ draws

**Result: proved (Opus 5.5 lead; independent reviews: Astra x2 + Opus xhigh; campaign review pending); not adopted.**
Adoption is Felipe's word.

- Final proof: `proof/PROOF_v5.tex` and `proof/PROOF_v5.pdf` (4 pages).
- Statement: `STATEMENT.md`.
- Review log: `CLAIMS_OF_FATAL_FLAWS.md`; every reviewer reply is in `review/`.
- Date: 2026-10-22.

## What was proved, in plain words

The final SMC run makes Q_f = 4N_e(T + L + 5) draws from the start distribution π₀:
- the 4N_e starting particles;
- one independence proposal per particle per round, over T + L + 4 rounds.

**The result.** Fix the calibration output 𝓒 (the frozen grid, T, the tier N_e, and so on). Fix any model S* chosen from the data and 𝓒 alone, before the final run starts. Then

  P(S* is never among these Q_f draws | 𝓒) = (1 − π₀(S*))^{Q_f} ≤ exp(−Q_f π₀(S*)).

This holds on the event that the final run is launched. It holds whatever the particles do: acceptances, resampling and mixing make no difference.

**Why it holds.** Each π₀ draw is made from random numbers that nothing has used before. The final run's random streams (10–13) are independent of the calibration's streams (0–9). The draw count Q_f is fixed by 𝓒 before any final randomness is used.

**What the proof does.**
1. It shows that reading "fresh" uniforms gives exactly independent uniforms, even when *which* number is read next depends on what was read before (Lemmas 1–2).
2. It shows that the backward sampler gives exact π₀ draws (Lemma 3).
3. It shows that the designated draws are therefore iid π₀ given the calibration (Proposition 5).
4. It conditions down to 𝓒 to get the formula (Theorem 6).

**The clause "the adaptive calibration draw count is never a fixed exponent"** is read as a scope note: the formula is claimed only for the final draws. Remark 7 explains why the formula cannot be used with a random, adaptive draw count. It gives a two-draw example where (1 − x)^N fails to give the miss probability, even on average.

**Extra, beyond (iii) (Corollary 9).** Under the same conditions,

  P(S* is not scored in the final run | 𝓒) ≤ (1 − π₀(S*))^{4N_e(T+L+4)}.

This uses only the independence proposals, because the method says those are always scored. If the initial draws are also scored, the exponent becomes Q_f. The method text does not say explicitly that they are.

## Statement changes

None to the claim. STATEMENT.md writes out what the original one-line wording left implicit:
- The data are fixed. The probability is over the algorithm's randomness.
- The formula holds on the event that the final run is launched.
- The stream model (EX-S), exact sampling (EX-A) and calibration-measurability (CAL) are spelled out.
- The final-run description of METHODOLOGY §6.5, §6.8 and §7 is written out. A launched run executes all its rounds; aborts by the computing environment are outside the idealised model.
- S* is "measurable w.r.t. data and 𝓒 (before final randomness)", quoting the theorem file's own preamble.

During review, definitions (w, W_K, ϖ, the tables, γ₀) and short verbatim method quotes were added so that reviewers could check them. No new hypothesis was added. EXP / EXP′ is not needed.

## Review history

**Stage A: lead with Astra #1** (GPT-6 Astra, high; session `<uuid>`).

| Round | Proof | Verdict | Fatal | Gap | Outcome |
|---|---|---|---|---|---|
| 1 | v1 | verified | 0 | 3 | All gaps were in supplementary parts, because the packet lacked definitions and method text. All three were accepted and fixed. |
| 2 | v2 | verified | 0 | 1 | The gap concerned the scoring corollary, which is outside (iii): the quoted text does not show that initial draws are scored. Accepted; the corollary was restricted to proposals. Two exposition points were also fixed. |
| 3 | v3 | verified | 0 | 0 | No findings. Astra #1 agreed with every answer. Stage A closed. |

**Stage B: two fresh independent reviews in parallel** (amendment 1).

| Round | Proof | Astra #2 (session `<uuid>`) | Opus 5.5 xhigh (native agent, Claude Personal) |
|---|---|---|---|
| 1 | v3 | verified, no findings | verified; 0 fatal; 1 gap (F8); 7 exposition |
| 2 | v4 | verified; agreed with all answers | verified; agreed with all answers; 4 exposition notes |
| 3 | v5 | verified, no findings | verified; 1 exposition note, no change required |

- **Opus F8 (round 1)** was in Corollary 9, outside (iii). The proposals form a subfamily of the draws whose position in the chronological order may depend on the run, so the iid property of all draws did not directly transfer to them. It was accepted and fixed: Proposition 5 now covers any class of "designated" calls decided when each call starts.
- **Opus exposition notes (round 2)** were applied in v5.

**Disputes:** none. No Astra judge was needed.

The full log, including every fatal or gap claim verbatim with the lead's answer and the reviewers' rulings, is in `CLAIMS_OF_FATAL_FLAWS.md`.

## Sanity check (not evidence of proof)

A toy single-seed simulation is in `helpers/numcheck/`. It used one shared uniform stream with state-dependent consumption, Metropolis moves, independence proposals and resampling, with 200,000 replications.
- **Absence frequency:** 0.75959 against the formula's 0.76023 (z = −0.67).
- **Chi-square tests** of the draws' marginal distribution and of draw pairs against π₀: not significant.
- **Negative control:** a deliberately broken variant that reused a uniform was far off (z = −67).

## Agent and call counts

| Model | Agents | Calls | Role |
|---|---|---|---|
| Astra #1 (GPT-6 Astra, high) | 1 session | 3 (1 new, 2 resumes) | Stage A reviewer |
| Astra #2 (GPT-6 Astra, high) | 1 session | 3 (1 new, 2 resumes) | Stage B reviewer |
| Opus 5.5 (xhigh) | 1 agent | 3 (1 launch, 2 follow-ups) | Stage B reviewer, Claude Personal |
| Sonnet 5.5 | 1 | 1 | Toy numerical check |
| Haiku 5.5 | 1 | 1 | LaTeX compile |
| Fable | 0 | 0 | |
| Astra judge | 0 | 0 | |

Lead: Opus 5.5 (high). There were no restarts and no counterexamples.

## Caveats

- **Reviewers' information.** Reviewers saw only STATEMENT.md (with its quoted method passages) and the proof, per the brief. All three noted that they could not check the setting items against the full method file, which was not in the packet. The lead checked those items against METHODOLOGY_v3.md (SHA-256 verified) and 00_COMMON.md.
- **Idealised model.** The result holds for the idealised algorithm: exact arithmetic (EX-A), ideal independent uniform streams (EX-S), and calibration using only streams 0–9 (CAL). It does not cover runs aborted by the computing environment, or targets S* chosen using the final run's own randomness.
- **Campaign review.** The campaign review (Stage C, by the managing lead) is pending.

## Stage C (campaign review, 2026-10-22)

- Final reviewers Fable 5.1 (high) and Astra (xhigh) both hold the proof correct (source: COLLECTED/review/FABLE_STAGE_C_phase2.md). Exposition edits applied: none (no edits; final file unchanged). 
- Result label now: proved (Opus 5.5 lead; independent reviews Astra x2 + Opus xhigh; campaign review Fable 5.1 + Astra: correct); not adopted.
