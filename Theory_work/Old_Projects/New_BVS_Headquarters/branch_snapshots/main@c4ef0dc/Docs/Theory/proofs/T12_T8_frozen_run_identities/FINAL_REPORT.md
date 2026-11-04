# FINAL REPORT — T12 (T8): frozen-run evidence and recorded Rao–Blackwell identities

**Result: proved (Opus 5.5 lead; independent reviews: Astra x2 + Opus xhigh; campaign review pending); not adopted.** Adoption is Felipe's word.

- Proof: `proof/PROOF_v5.tex` / `proof/PROOF_v5.pdf` (16 pages). PROOF_v4 is the version both Stage B reviewers verified; v5 adds only their final exposition fixes.
- Statement: `STATEMENT.md` (v2.2), whose history section lists every change.
- Date: 2026-10-22. Protocol: proof.md with Felipe's overrides plus Amendment 1 (see STATUS.md).

## What the theorem says, in plain words

The final run of SMC-BVS v3 is four independent "islands" of particles. Each island moves from the easy start distribution π₀ to the posterior π along a fixed temperature grid. Fix the calibration output 𝓒 (grid, particle numbers, and so on), whose randomness is separate from the final run's. Then:

- **(i) Evidence.** Each island's evidence estimate Ẑ_r is exactly unbiased: E[Ẑ_r] = Z. More generally, the "evidence-weighted" particle average is unbiased for Z_t q_t(f) at every stage. This survives:
  - extra rounds at temperature 1 (burn-in, measured rounds);
  - resampling with equal weights;
  - looking at the particles part-way through a round, at a position chosen by the random step order (for example just before the Gibbs step for variable j).

  It does **not** survive stopping a particle at a time chosen by its own state; this fails on every input.
- **(ii) PIPs.** The Rao–Blackwell PIP estimate recorded just before each Gibbs step satisfies E[Ẑ_r·PIP̂_rj] = Z·PIP_j.
- **(iii) Pooled evidence.** For the pooled Ẑ = ¼ΣẐ_r: E Ẑ = Z, E log Ẑ ≤ log Z, and the reported bound 0.05·Ẑ is below Z with probability ≥ 95% (Markov). All of this holds given 𝓒.
- **(iv) Limits.**
  - log Ẑ is biased downward whenever the bridge discrepancy d is not identically 0.
  - The normalised PIPs (primary and secondary) are biased in general. An explicit certified example at n = 20, p = 2 shows a bias of about −0.17.
  - The islands are independent given 𝓒, but not necessarily after averaging over 𝓒.
  - Conditioning on a calibration-measurable launch event keeps unbiasedness.
  - Conditioning on a passing final diagnostic (E2) can break the identities.
  - A bound on log-score errors (NUM) alone gives no unbiasedness or Markov guarantee.

EXP and EXP′ are not used.

## Statement changes, and why

1. **Made precise (Astra #1 statement check: APPROVED WITH CHANGES).**
   - The frozen run is stated for arbitrary integer parameters. The method is the case N = N_e, M = 4, L′ = L, with no stage-0 round.
   - START, exactness of the π₀ sampler and of Z̄₀, is an imported dependency (T09(i)), not an extra restriction.
   - The negative parts of (iv) are component statements, with the scope stated: the p = 2 example would take the exact branch in the full method, and N = 1 is not the production budget.
   - "Not necessarily independent after averaging over 𝓒" is formalised as an exact characterisation: unconditional independence holds iff the island law given 𝓒 is a.s. constant. No claim is made about the actual calibration law.
   - "Favourable diagnostics" is formalised as the final E2 check passing. "NUM alone" is formalised as a perturbed-score model that NUM does not exclude.
2. **One error of mine, caught by Astra #1.** My first draft extended (iv.d) to *every* conclusion of (iii) under a launch event. That is false for intermediate stages, whose targets depend on the random grid. It was repaired: only the 𝓒-free conclusions are kept, and intermediate stages hold in averaged form. This was an over-extension beyond the conjecture, so it is not counted as a step-1 restart.
3. **Stage B round 1.** Both reviewers independently found that the statement pointed to 00_COMMON for the marginal-likelihood formula instead of writing it out. STATEMENT §0 now carries Felipe's fixed target formulas. Joint measurability of the stream map is now stated explicitly under EX-S. No conclusion changed.

## Review history

| Stage / round | Reviewer | Object | Verdict | Fatal / gap / exposition |
|---|---|---|---|---|
| A, statement check | Astra #1 (high) | STATEMENT v1 | APPROVED WITH CHANGES | 1 false clause, (iv.d), plus 3 required clarifications; all adopted |
| A, review | Astra #1 (high), resumed | PROOF_v2 | **verified** | 0 / 0 / 3 (fixed in v3) |
| B, round 1 | Astra #2 (high), new session | PROOF_v3 | not verified | 0 / 1 / 1 |
| B, round 1 | Opus 5.5 (xhigh), Claude Personal | PROOF_v3 | not verified | 0 / 2 / 6 |
| B, round 2 | Astra #2 | PROOF_v4 + claims log | **verified**; agrees with all 3 answers | 0 / 0 / 2 (fixed in v5) |
| B, round 2 | Opus 5.5 (xhigh) | PROOF_v4 + claims log | **verified**; agrees with all 3 answers | 0 / 0 / 2 (fixed in v5) |

- CLAIMS_OF_FATAL_FLAWS.md has every gap finding verbatim, with my answer and both reviewers' rulings. No fatal finding was raised at any stage.
- The Astra judge was not needed.
- The independent checks of the numerical example agree to 12+ digits:
  - a Sonnet assistant wrote its own implementation (helpers/sonnet_check/);
  - the Opus reviewer re-ran the certificate, wrote its own float implementation, and ran a single-seed Monte Carlo of the literal algorithm with 200,000 islands, getting −0.1752 ± 0.0008 against the certified −0.17397.

## The computer-assisted part

Parts (iv.b) and (iv.e) use one explicit instance: n = 20, p = 2 (data in the STATEMENT appendix), T = 1, N = 1. The exact finite-state law was computed in 60-digit interval arithmetic (mpmath 1.3.0; helpers/p2_exact.py, certify_instance.py; output helpers/certify_iv.log, reproduced in the proof's Appendix B). At the method's L′ = L, the certified values are:

- primary PIP bias −0.173974…;
- secondary PIP bias −0.159677…;
- every enclosure narrower than 2·10⁻⁵³;
- all claimed inequalities checked by exact endpoint comparisons.

Everything else is a pen-and-paper proof.

## Agent and call counts

| Model | Agents | Calls | Role |
|---|---|---|---|
| GPT-6 Astra (high), session #1 `<uuid>` | 1 | 2 | statement check; Stage A proof review |
| GPT-6 Astra (high), session #2 `<uuid>` | 1 | 2 | Stage B review; round-2 ruling |
| GPT-6 Astra (xhigh), judge | 0 | 0 | not needed |
| Opus 5.5 (xhigh), Claude Personal, read-only Plan agent | 1 | 2 | Stage B review; round-2 ruling |
| Sonnet 5.5 | 1 | 1 | independent recomputation of the instance |
| Haiku 5.5, Fable, Sol | 0 | 0 | none |

Lead: Opus 5.5 (high), the mathematics and the operator role. Totals: 4 Astra calls, 2 Opus calls, 1 Sonnet call.

## Where things are

- Project folder: `<OLD_ROOT>\01_Methodology_and_Theory\Theory_architecture_v3\proofs\T12_T8_frozen_run_identities\`
- `review\` holds every reply, full log and packet as sent.
- The temporary packet folders under `<PC_TEMP_PATH>` were deleted at the end.
- No NOTS, no multi-seed runs, and no edits outside this folder.

## Open points (not part of this theorem)

- START is imported from T09(i), which is being proved in a sibling thread.
- The negative examples are component statements. Whether the actual calibration produces non-degenerate island laws, and whether normalised-PIP bias is visible on SMC-branch inputs, are not claimed.

## Stage C (campaign review, 2026-10-22)

- Final reviewers Fable 5.1 (high) and Astra (xhigh) both hold the proof correct (source: COLLECTED/review/FABLE_STAGE_C_phase2.md). Exposition edits applied: E12-1 (proof section 8.2, the sentence on the width of every enclosure), E12-2 (Appendix B, the sentence before the log). New final file: proof/PROOF_v6.tex and proof/PROOF_v6.pdf (PROOF_v5 kept unchanged). 
- Result label now: proved (Opus 5.5 lead; independent reviews Astra x2 + Opus xhigh; campaign review Fable 5.1 + Astra: correct); not adopted.
