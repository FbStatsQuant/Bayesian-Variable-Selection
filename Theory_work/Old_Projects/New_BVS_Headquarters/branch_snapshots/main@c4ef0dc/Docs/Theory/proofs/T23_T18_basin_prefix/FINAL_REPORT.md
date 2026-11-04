# FINAL REPORT — T23(ii): pathwise Rao–Blackwell PIP bound

**Result: proved (Opus 5.5 lead; independent reviews: Astra x2 + Opus xhigh; campaign review pending); not adopted.** Adoption is Felipe's word.

Theorem file: `theorems/T23_T18_basin_prefix.md`, part (ii) only. Method: METHODOLOGY_v3.md, SHA-256 93043758…8019c (hash re-checked 2026-10-22). Run under proof.md with the run overrides and Protocol Amendment 1 (recorded in STATUS.md).

**Final proof:** `proof/PROOF_v4.tex` and `proof/PROOF_v4.pdf` (6 pages). v1–v3 are kept for the record.
**Other files:** STATEMENT.md; CLAIMS_OF_FATAL_FLAWS.md; review/ (every reply verbatim, full Astra logs, the three change lists); STATUS.md; helpers/make_v4.py (the script for the v3→v4 wording edits).

## What is proved (plain words)

The primary PIP estimator averages, over particles and the 4 measured rounds, the Gibbs inclusion probabilities recorded just before each Gibbs draw. Call a particle-round "bad" if the particle is anywhere other than the true model S₀ at some moment of that round, its start included. B̄_r is the fraction of bad particle-rounds on island r.

- **(ii-a) On every run (needs only exact arithmetic):** for all coordinates j at once, |PIP̂_{rj} − 1{j∈S₀}| ≤ B̄_r + max_j |o_j(S₀) − 1{j∈S₀}|.
  - In a good particle-round, every recording is taken at S₀.
  - A bad particle-round contributes at most 1.
- **(ii-b)** max_j |o_j(S₀) − 1{j∈S₀}| ≤ u_π = (1 − π(S₀))/π(S₀).
  - Each one-flip neighbour of S₀ has posterior mass at most 1 − π(S₀).
  - At the size cap |S₀| = K, additions have o_j = 0.
- **(ii-c) Under BASIN:** E_𝓒 max_j |PIP̂_j − 1{j∈S₀}| ≤ δ + (1−a)^{⌊L/r₀⌋} + (L+4)(η+ρ) + u_π = 𝓑_n.
  - The proof follows one particle. It is at S₀ when measured round h starts unless one of these happened:
    - it started outside the basin (δ);
    - it missed S₀ in all ⌊L/r₀⌋ entrance trials ((1−a)^{⌊L/r₀⌋});
    - it left the basin (≤ η per round);
    - it left S₀ after reaching it (≤ ρ per round).
  - One more ρ covers leaving S₀ during the measured round itself.
  - The proof actually gets the slightly sharper (L+3)η + (L+4)ρ.
- **(ii-d)** P_𝓒(MPM̂ ≠ S₀) ≤ 2𝓑_n, by Markov's inequality. Ties at ½ are handled.
- The proof assumes no independence between particles and uses no union bound over the p coordinates. Lemma 1 shows that each particle's next round, given the past, is a fresh K₁-round from its current state. This holds for any processing order, sub-stream layout or batching of the random numbers.

## Statement changes

None. Step-1 outcome: (a), correct as stated.
- EXP/EXP′ is not needed.
- No sibling conjecture is used as a hypothesis; the occupancy step is proved directly from BASIN, without citing part (i).
- STATEMENT.md §5 records five readings. These are precisions, not changes:
  1. ρ is the whole-round departure probability from S₀.
  2. η is the one-round first-exit probability from the basin 𝓡.
  3. There is no resampling in the L + 4 terminal rounds.
  4. δ applies to every island.
  5. "MPM error" means the event MPM̂ ≠ S₀.
- The proof states EX-S in the form it uses, (F): each random choice of the algorithm, given everything used by earlier choices, has the law the method prescribes. Both Stage B reviewers ruled (F) a faithful reading of EX-S and CAL, not an added assumption.

## Review history

**Stage A (lead + Astra #1).** Astra #1: gpt-6-astra, reasoning high, session <uuid>.
- PROOF_v1 → "No findings … VERDICT: verified".

**Stage B, round 1** (independent, started together; each reviewer had only STATEMENT.md, the proof and the report format).
- **Astra #2** (new session <uuid>, high): no findings, verified.
- **Opus 5.5 reviewer** (effort xhigh, read-only Plan agent, own account): verified, with 6 exposition findings, all accepted → PROOF_v2. The findings:
  - Lemma 1's stopping-time step was not written out.
  - The kernel being fixed given 𝓒 was not cited to the statement.
  - The case S₀ ∉ Ω needed a convention.
  - Lemma 4's range of H was not bounded.
  - Lemma 4's hypothesis list was not minimal.
  - EX-A and the island index were not stated explicitly.

**Round 2 (rulings on v2).**
- Both verified and agreed with all six changes.
- They raised 7 more exposition points, all accepted → PROOF_v3. The main ones:
  - Lemma 1 cited method details that STATEMENT.md does not contain (both reviewers).
  - Lemma 1 assumed the population is processed round by round.
- The fix rewrote Lemma 1 with per-particle σ-fields and a step-by-step conditioning proof.

**Round 3 (rulings on v3).**
- Astra #2: no findings, verified; it ruled (F) faithful.
- Opus: verified, with 2 exposition points (define the σ-fields by variates *used*, not *drawn*; a clash of path notation). Both accepted → PROOF_v4, wording only.

**Round 4 (confirmation of v4).** Both verified.
- The Opus reviewer added one cosmetic note: the path symbol Z reuses the evidence symbol Z. It said this "needs no action". It is deferred, not changed, so the final proof is exactly the text both reviewers confirmed.

**Overall.**
- No fatal or gap finding in any round, from any reviewer (CLAIMS_OF_FATAL_FLAWS.md).
- No dispute, so no Astra judge.
- The lead holds the proof correct. Astra #1 verified v1; Astra #2 and the Opus reviewer verified v2, v3 and v4. The v1→v4 changes are exposition plus a more careful proof of Lemma 1. Astra #1 was not re-consulted after Stage A.

## Skipped / not done

- No numerical sanity check and no helper agents. The result is elementary, and the theorem file's provisional Sol check J4 already covers the prefix-versus-endpoint point.
- Parts (i), (iii), (iv) and (v) of T23 were not touched. (ii-c) does not say when BASIN holds.
- The cosmetic Z-symbol note above is deferred.
- Stage C (campaign review: one Fable 5.1 plus one Astra across all proofs) belongs to the managing lead.

## Counts

| Who | Model / setting | Calls |
|---|---|---|
| Lead | Opus 5.5 (high) | this thread |
| Astra #1 | gpt-6-astra, high, session 01a16419-… | 1 call |
| Astra #2 | gpt-6-astra, high, session 01a1641c-… | 4 calls (1 new + 3 resumes) |
| Opus reviewer | Opus 5.5 xhigh, native read-only agent | 1 agent, 4 calls (1 launch + 3 continuations) |
| Astra judge | — | 0 (not needed) |
| Sonnet 5.5 / Haiku 5.5 / Fable / Sol | — | 0 |

Totals: Astra 5 calls in 2 sessions; Opus reviewer 4 calls.

## Stage C (campaign review, 2026-10-22)

- Final reviewers Fable 5.1 (high) and Astra (xhigh) both hold the proof correct (source: COLLECTED/review/FABLE_STAGE_C_phase2.md). Exposition edit applied: E23-1 (STATEMENT.md section 3, one sentence appended after the displayed inequality of conclusion (ii-a), also in Theorem (a) of the proof). New final files: proof/PROOF_v5.tex and proof/PROOF_v5.pdf (PROOF_v4 kept unchanged); STATEMENT.md updated (copy before the edit: STATEMENT_before_stageC.md). 
- Result label now: proved (Opus 5.5 lead; independent reviews Astra x2 + Opus xhigh; campaign review Fable 5.1 + Astra: correct); not adopted.
