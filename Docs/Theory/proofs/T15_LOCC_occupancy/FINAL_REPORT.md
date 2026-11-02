# FINAL REPORT — T15 (L-OCC): occupancy from an evidence lower tail

**Result: proved (Opus 5.5 lead; independent reviews: Astra x2 + Opus xhigh; campaign review pending); not adopted.** Adoption is Felipe's word.

Date: 2026-10-22. Protocol: proof.md with Felipe's run overrides, Protocol Amendment 1 (Stage B), and its correction (Opus reviewer on Claude Personal).

Final files:
- statement: `STATEMENT.md` (v4, plus one post-review wording alignment in a scope remark);
- proof: `proof/PROOF_v4.tex`, `proof/PROOF_v4.pdf` (4 pages);
- review history: `review/`;
- claims log: `CLAIMS_OF_FATAL_FLAWS.md`;
- exact checks: `helpers/`.

## 1. What the theorem says, in plain words

Each of the 4 final-run islands outputs an evidence estimate Ẑ_r. Write W_r = Ẑ_r/Z for its ratio to the true evidence. Let 𝔄 be any set of models fixed before the final run, and let f_r be the fraction of island r's particles outside 𝔄 at the end of the run (or at a fixed recording point in the terminal rounds).

- **(i)** On average, f_r ≤ π(𝔄ᶜ)/c + P(W_r < c), for any c in (0,1). So a small outside fraction is guaranteed when (a) the posterior puts little mass outside 𝔄 and (b) this island rarely underestimates the evidence badly.
- **(ii)** The same bound holds in probability form: P(f_r > u) ≤ π(𝔄ᶜ)/(cu) + P(W_r < c).
- **(iii)** If the island's evidence is accurate on average, E|W_r − 1| ≤ B, then P(W_r < c) ≤ B/(1−c). That value can be substituted into (i) and (ii).
- **(iv)** The lower-tail term must refer to the same island. Replacing it by the pooled evidence's lower tail P(Ẑ/Z < c) is not justified. An explicit example shows this. Island 1 has tiny evidence and all its particles outside 𝔄, while another island has large evidence. The pooled average then looks fine, yet island 1 is entirely outside 𝔄. The example even satisfies the frozen-run identity for every test function.

The key input is the frozen-run identity of sibling conjecture T12(i): E[W_r f_r] = π(𝔄ᶜ). From it, parts (i)–(ii) are a split at W = c plus Markov's inequality. The run rules require sibling conjectures to appear as explicit hypotheses, so the identity enters as hypothesis (H-T12). **T15 is therefore proved conditionally on T12(i).** It is unconditional once T12(i) is proved.

## 2. Statement changes and why

The inequalities, constants and quantifiers of the theorem file are unchanged. The other changes:

- **T12 dependency made explicit.** The theorem file says "Builds on T12". STATEMENT.md states T12(i) as the hypothesis (H-T12), as the run rules require. No statement-checker call was needed, because this follows the run rules and is not a new assumption.
- **Pooled-tail sentence made precise.** The theorem file's sentence "a pooled-evidence lower tail does not substitute" became part (iv), a non-implication with an explicit example. It was strengthened during review:
  - v2: strictly positive evidence (Astra #1);
  - v3: every outside mass a ∈ (0, cu/4], plus (iv-b), which realises the example with particle populations satisfying the T12 identity for every test function (suggested by the Opus reviewer);
  - v4: wording only.
- **Realised-population sentence kept as a scope remark.** The theorem file's sentence on realised populations is a scope remark: the bounds concern the law of the run, not a realised population.
- **EXP / EXP′ not needed.** No decision from Decision Point 2 affects T15.

## 3. Review history

| Stage | Reviewer | Version | Verdict | Findings |
|---|---|---|---|---|
| A | Astra #1 (session <uuid>), r1 | v1 | verified | 1 exposition (example used W = 0) → fixed in v2 |
| A | Astra #1, r2 | v2 | verified | none |
| B | Astra #2 (new session <uuid>), r1 | v2 | verified | none |
| B | Opus 5.5 xhigh (Claude Personal), r1 | v2 | verified | 5 exposition → fixed in v3 |
| B | Astra #2, r2 (ruling on v3 + log) | v3 | verified | 2 exposition → fixed in v4 |
| B | Opus, r2 (ruling on v3 + log) | v3 | verified | 4 exposition (2 shared with Astra #2) → fixed in v4 |
| B | Astra #2, r3 | v4 | verified | none of any severity |
| B | Opus, r3 | v4 | verified | 1 optional wording note → aligned in STATEMENT §4 |

- **Fatal or gap findings:** none, from any reviewer, at any round. CLAIMS_OF_FATAL_FLAWS.md records this, with every exposition finding and the lead's answer.
- **Rulings on the log:** both Stage B reviewers ruled on it and agree that nothing is outstanding.
- **Astra judge:** not used.
- **Lead's judgment of the findings:** all were accepted as correct. None changed parts (i)–(iii), which are word for word the same as in v1.

## 4. Independent numerical checks (Haiku 5.5, exact rational arithmetic)

These are sanity checks of the counterexample in (iv). They are not evidence for (i)–(iii), which are short exact arguments. Each check is in `helpers/`.

- **`check_iv.py`** (v1 law), 49 (c,u) pairs: all pass. A deliberately wrong canary fails, as it should.
- **`check_iv_v2.py`** (strictly positive law), 49 pairs: all pass. Canary fails.
- **`check_iv_v3.py`** (general a and particle populations):
  - Part A, 147 (c,u,a) triples: all pass.
  - Part B: the population identity holds exactly on a 3-model space with N = 2.
  - Both canaries fail.

The lead re-ran each script; outputs are in `helpers/*_output.txt`. The theorem file's provisional numerical evidence (Sol check J6, E[W f] = π(𝔄ᶜ)) concerns the T12 input, not this proof, and was not used.

## 5. Caveats for Felipe

- **Conditional on T12(i).** If the T12 thread changes the identity (for example, to which recording positions it covers), T15 inherits that change. T15 holds at exactly the positions where T12(i) holds.
- **The theory's idealisations.** The usual theory assumptions apply: exact arithmetic (EX-A), ideal random streams (EX-S), and calibration independent of the final run (CAL). Part (iv) shows a counterexample law exists; it does not show that the actual SMC produces that law on some data set.
- **Calibration-conditional.** The bounds are about the law of the final run given the calibration. They do not bound the outside fraction of a population already observed.

## 6. Agents and calls

| Model | Role | Count |
|---|---|---|
| Opus 5.5 (high) | lead: mathematics, files, LaTeX, packets, codex calls | this session |
| GPT-6 Astra (high), session #1 | Stage A reviewer | 2 calls (1 new + 1 resume) |
| GPT-6 Astra (high), session #2 | Stage B reviewer | 3 calls (1 new + 2 resumes) |
| GPT-6 Astra (xhigh) | judge | 0 (not needed) |
| Opus 5.5 (xhigh) via T3 delegate_task | Stage B reviewer | 3 completed calls on Claude Personal, plus 1 launch on Claude Work cancelled unfinished per the correction; no output used |
| Haiku 5.5 | exact numerical checks | 1 agent, 3 tasks |
| Sonnet 5.5, Fable, Sol | — | 0 |

Totals: 5 Astra calls (2 sessions); 4 Opus reviewer launches (3 used); 1 Haiku agent (3 tasks).

Packet folders under `<PC_TEMP_PATH>` were deleted at the end. All replies are saved verbatim in `review\`.

## Stage C (campaign review, 2026-10-22)

- Final reviewers Fable 5.1 (high) and Astra (xhigh) both hold the proof correct (source: COLLECTED/review/FABLE_STAGE_C_phase2.md). Exposition edits applied: none (no edits; final file unchanged). 
- Result label now: proved (Opus 5.5 lead; independent reviews Astra x2 + Opus xhigh; campaign review Fable 5.1 + Astra: correct); not adopted.
