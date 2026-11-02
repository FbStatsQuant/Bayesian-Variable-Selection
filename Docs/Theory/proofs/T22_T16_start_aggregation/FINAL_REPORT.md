# FINAL REPORT — T22 (T16), parts (i), (ii), (iv)

**Result: proved (Opus 5.5 lead; independent reviews: Astra x2 + Opus xhigh; campaign review pending); not adopted.** Adoption is Felipe's decision.

- Final proof: `proof/PROOF_v3.tex` and `proof/PROOF_v3.pdf` (5 pages).
- Statement: `STATEMENT.md`.
- Date: 2026-10-22.
- Method file: METHODOLOGY_v3.md, SHA-256 93043758…8019c (checked).

## What was proved, in plain words

The SMC sampler starts from a cheap "composite start" distribution π₀. π₀ is built from small exact tables of Bayes factors, one table per block of correlated variables, combined with the size prior. The bridge q_φ then moves from π₀ (φ = 0) to the true posterior π (φ = 1). All three parts below hold for every data set; no statistical assumption is used.

- **(i) The start puts real mass on a good reference model S°.**
  - Two table numbers control this.
  - q (or the simpler upper bound u) measures how much adding extra variables to S° can gain in the tables.
  - e measures how much removing a variable of S° can gain.
  - If q < 1, then π₀(S°) ≥ (1−q)^{s+1}/(1+e)^s, and 1 − π₀(S°) ≤ (s+1)q/(1−q) + s·e.
  - Also q ≤ u, so u can replace q.
  - A second form, using a "completion ratio" δ^comp, also holds: π₀(S°) ≥ (1−u)^{s+1}/[1+(2^s−1)δ^comp].
- **(ii) From the reference to the truth.**
  - π₀(S₀)/π₀(S°) is an exact product of a prior ratio and table ratios.
  - If S° ⊆ S₀, each added variable costs at most a known factor r_k = (k+1)/((2p−k−1)√(n+1)).
  - The reason is that one added variable can lower a Bayes factor by at most √(n+1).
- **(iv) The bridge never loses the truth more than its two ends do.**
  - For every φ in [0,1], the odds against S₀ under q_φ are at most a weighted geometric mean of the odds at the two ends (Hölder's inequality).
  - So q_φ(S₀) ≥ min{π₀(S₀), π(S₀)}.
  - Consequence: if both π₀ and π concentrate on S₀, the whole bridge does, uniformly in φ.

## Changes to the statement

All changes were approved by Astra #1 as statement checker (step 1b), with the verdict "APPROVED WITH CORRECTIONS". Details are in STATEMENT.md, "Changes to the statement".

- **C1, added hypothesis:** (ii) and (iv) assume S₀ is a feasible model, |S₀| ≤ K = min(p, ⌊n/2⌋).
  - Without it, the identity in (ii) is false: π₀(S₀) = 0 while the right side is positive.
  - Astra confirmed this with a concrete instance (n = 3, p = 2, S₀ = {1,2}).
  - Asymptotically nothing is lost: the regime R already assumes "eventually s₀ ≤ K".
- **C6, generalisation:** the proof holds for any real X, y and any block partition, and (i) holds for any positive tables. The method's setting is a special case.
- **C7, scope:** (i-c) is stated under u < 1.
- **Readings:**
  - "With T03 and (iii) …" in (iv) became a conditional corollary, (iv-c). The conclusions of T03 and of part (iii) enter only as explicit hypotheses; nothing about T03 or (iii) is proved here.
  - δ^comp's supremum is taken over feasible models. This makes the bound stronger and implies the other reading.
  - "Normalised reference mass remains essential" is treated as a remark, not a claim.
- **EXP / EXP′ is not needed** for (i), (ii) or (iv). Astra confirmed this. Part (iii), which needs EXP′, was left alone as instructed, and so was part (v).
- **The proof-route hint** never entered STATEMENT.md or any packet.

## Review history

### Stage A: lead and Astra #1 (session <uuid>)
- **Statement check:** approved with corrections (`review/astra_01_statement_check.log`).
- **Review of PROOF_v1:** VERDICT verified, one exposition finding (`review/astra_02_review_A1_v1.log`).
  - The finding: "2^s − 1 such M" should read "at most 2^s − 1".
  - I accepted it and fixed it in PROOF_v2, the proof candidate.

### Stage B: two independent reviews of PROOF_v2, started together with fresh context and given only the packet

- **Astra #2** (new session <uuid>): no findings, VERDICT verified (`review/astra2_B_review_v2.log`).
- **Opus 5.5, xhigh:** five exposition findings, VERDICT verified (`review/opus_B_review_v2.md`).
  - The findings were: a display overflowing the margin, an unstated step for D_S ≥ 1, symbol clashes, an impossible case Ω = {S₀}, and the 0⁰ convention.
  - I accepted all five and fixed them in the unified PROOF_v3 (`review/CHANGES_v2_to_v3.md`, `review/REVIEW_PROCESSING.md`).
- **Round 2:** PROOF_v3 and the claims log went back to both reviewers.
  - Astra #2: agrees with the log, VERDICT verified (`review/astra2_B_round2_v3.log`).
  - Opus: agrees with the log, confirms all five fixes, VERDICT verified (`review/opus_B_round2_v3.md`).
  - Opus raised one new cosmetic point, N1: the letter x is reused as a dummy variable in one paragraph of (i-a).
  - I accepted N1 but deferred it, so that the final file is exactly the version every reviewer verified.
- **CLAIMS_OF_FATAL_FLAWS.md:** no fatal or gap finding in any review. Both Stage B reviewers agreed with the log.
- **Disputes:** none, and the Astra judge was not used.

### Numerical sanity check (not a review, not evidence of proof)
- A Sonnet assistant wrote an independent brute-force implementation from STATEMENT.md and ran it with one seed, locally (`helpers/numcheck/REPORT.md`).
- Scale: 10,000 small instances (p ≤ 9, the cap often binding, adversarial tables for (i)). In total about 1.1M checks of part (i), 3.1M of (ii-a) and 0.54M φ-points of (iv).
- 0 failures.
- All 4 planted false variants were detected.

## What this does not establish
- Nothing about part (iii) (the statistical rate, which needs EXP′) or part (v).
- Nothing about T03, which (iv-c) uses only as a hypothesis.
- (i) gives a useful bound only when the table numbers q (or u) and e are small. Showing that they are small for real data is the job of part (iii).

## Agent and call counts
| Model | Agents | Calls | Role |
|---|---|---|---|
| Opus 5.5 (high), lead | 1 (this session) | — | mathematics and operator |
| GPT-6 Astra (high), #1 | 1 session | 2 | statement checker; Stage A reviewer |
| GPT-6 Astra (high), #2 | 1 session | 2 | Stage B reviewer (review, round-2 ruling) |
| Opus 5.5 (xhigh) | 1 | 2 | Stage B reviewer (review, round-2 ruling) |
| Sonnet 5.5 | 1 | 1 | numerical sanity check |
| Haiku 5.5 | 0 | 0 | — |
| Astra judge (xhigh) | 0 | 0 | not needed |
| Fable | 0 | 0 | not used (per overrides) |

Statement restarts: 0. Counterexamples presented: 0.

## Files and cleanup
- **Project folder:**
  - STATEMENT.md, STATUS.md, CLAIMS_OF_FATAL_FLAWS.md, this report.
  - `proof/`: v1–v3, tex and pdf.
  - `review/`: every Astra log, both Opus replies, the processing notes, the change list and the report format.
  - `helpers/numcheck/`: the numerical check.
- **Packet folders** under `<PC_TEMP_PATH>` held only copies of project files plus the reviewer logs, which were copied into `review/`. They were deleted at the end of the run.
- No theorem file, THEORY.tex, method file, README or other proofs\ subfolder was edited. No NOTS use and no multi-seed runs.

## Stage C (campaign review, 2026-10-22)

- Final reviewers Fable 5.1 (high) and Astra (xhigh) both hold the proof correct (source: COLLECTED/review/FABLE_STAGE_C_phase2.md). Exposition edits applied: none (no edits; final file unchanged). 
- Result label now: proved (Opus 5.5 lead; independent reviews Astra x2 + Opus xhigh; campaign review Fable 5.1 + Astra: correct); not adopted.
