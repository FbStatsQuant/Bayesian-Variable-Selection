# FINAL REPORT — T13 (T10): restricted ESS and the omitted-mass identity

**Result: proved (Opus 5.5 lead; independent reviews: Astra x2 + Opus xhigh; campaign review pending); not adopted.**
Adoption is Felipe's decision.

- Proof: `proof\PROOF_v4.pdf` (source `proof\PROOF_v4.tex`, compiled with xelatex; 11 pages).
- Statement: `STATEMENT.md` (version 3, approved by Astra #1).
- Date: 2026-10-22. Protocol: proof.md with Felipe's overrides for this run, plus Protocol Amendment 1 and its correction.

## 1. What the theorem says, in plain words

The candidate grid is built so that, between consecutive temperatures, the bridge's weight spread *restricted to the scored models in V* stays small (ρ_V ≥ 0.9). T13 says how this restricted control relates to the real, full-space control.

- **(i) Identity.** The full-space one-step divergence equals the restricted one (1/ρ_V) times a correction made only of V's probability mass at three temperatures: a(v)²/(a(u)a(w)).
- **(ii) Consequence.** If V carries at least 1 − ε_C of the mass at the evaluation points φ_{t−1} and w_t = 2φ_t − φ_{t−1}, every accepted grid interval has 1 + χ² ≤ 10/(9(1 − ε_C)²).
  - (c) Coverage on [0, 1] alone is not enough. w_t lies above 1, and there is a real data set where coverage is 0.927 on [0, 1] but 0.573 at w = 2, and the full-space bound fails (1.533 > 1.372).
  - (d) The largest w_t need not be the worst point. On the same data, with another V, the worst point is φ₀ = 0.
- **(iii)** The same identity holds for any working set W inside V.
- **(iv)** If V contains no model of a set 𝓜 and ∅ ∉ 𝓜, removing 𝓜 from the bridge does not change the grid construction at all.

Nothing here says anything about particle mixing.

## 2. Changes to the statement, and why

All changes were checked by Astra #1 in three statement checks (`review\astra_01..03`). Check 1 rejected one reading, which counts as one restart of step 1 (the limit is 3). The final statement is `STATEMENT.md` §2.

1. **ε_C must be in [0, 1).** For ε_C ≥ 1 the bound is undefined or false.
2. **(iv)(a): "calibration never scores 𝓜" became an explicit hypothesis.** The hypothesis is that the scored pool V is drawn from avoids 𝓜. The method does not say whether table scores or leaders carried across tiers feed V's top lists. The source wording is kept as a sufficient condition, with that provenance proviso.
3. **(ii)(b): each grid is paired with the V of the construction that produced it.**
4. **(ii)(c)–(d): the two cautionary examples must come from real data run through the method.** That means the method's blocks, tables, γ₀ and d, on the SMC branch, with a V of the method's form and a grid the construction actually outputs. My first version used abstract weights; Astra rejected that as a weakening (restart 1). The witness also names its tier, its T_e and a deterministic implementation.
5. **(iii): the bound uses coverage at v.** COVER supplies it.
6. **(i), (iii) hold for all real u, v,** a free strengthening.
7. **Positivity is derived, not assumed.**
8. **(iv)(b) is for one fixed deterministic implementation.**
9. **(ii)(d) is strengthened:** the minimum is attained *only* at φ₀.

None of these changes the substance of the source theorem. EXP / EXP′ is not needed anywhere.

## 3. How the proof works

- **(i), (iii):** a two-line second-moment calculation. Lemma 2 gives 1 + χ²(q_v^A ‖ q_u^A) = Z̄_u(A)Z̄_w(A)/Z̄_v(A)² for any model set A. Then substitute Z̄_ψ(A) = q_ψ(A)·Z̄_ψ (Lemma 3).
- **Positivity (Lemma 1):** from the model's formulas. Q_S ≥ 0 follows from the method's non-negative form of Q.
- **(ii)(b):** every appended grid point passes ρ_V ≥ 0.9 against the previous point, by the construction rule.
- **(iv):** ρ_V depends only on the bridge weights inside V, and the construction sees the bridge only through ρ_V. Induction on the construction's steps finishes the argument.
- **(ii)(c)–(d), the witnesses:**
  - Data: n = 42, p = 40, orthogonal standardised columns. The response loads on two columns j₁, j₂ in different blocks (coefficients 0.97 and 0.10) plus one direction orthogonal to all columns.
  - Every quantity then has a closed form (Lemma 4). The discrepancy d is 0 except on models that contain both j₁ and j₂, where it equals a constant D ≈ 2.457.
  - The seven decisive inequalities are certified by interval arithmetic (outward rounding, enclosures narrower than 10⁻²⁰; Appendix A).
  - Appendix B quotes, verbatim and with checksums, every method definition used.

## 4. Review history and my judgments

| Stage | Reviewer | Version | Verdict | Findings (fatal / gap / exposition) | My answer |
|---|---|---|---|---|---|
| A | Astra #1 | v1 | not verified | 0 / 1 / 2 | Gap accepted: the witness inequalities had no certified error bound. Fixed by interval arithmetic (v2). Exposition fixed. |
| A | Astra #1 | v2 | verified | 0 / 0 / 1 | Printed endpoints were rounded to nearest; fixed with outward rounding (v3). |
| A | Astra #1 | v3 | verified | none | Stage A proof candidate. |
| B | Astra #2 (fresh) | v3 | not verified | 0 / 1 / 0 | Gap accepted: the method definitions were not in the packet. Fixed by Appendix B (v4). |
| B | Opus xhigh (fresh) | v3 | not verified | 0 / 4 / 5 | The four gaps are the same issue in detail (m(S) formula, n − 1 standardisation, block properties, budgets). All accepted and fixed in v4, with the exposition points. |
| B | Astra #2 | v4 | **verified** | none | Agrees with every logged answer. |
| B | Opus xhigh | v4 | **verified** | 0 / 0 / 3 | The provenance note is closed by my mechanical check (9/9 quoted passages match the source lines; checksums match). The other two notes need no change (the reviewer agrees). |

- No reviewer found a mathematical error at any stage. Every finding was about rigour or completeness of the record.
- Every gap finding, verbatim with my answer and the reviewers' rulings, is in `CLAIMS_OF_FATAL_FLAWS.md`.
- Raw replies are in `review\`: the Astra logs `astra_0*.log` and `stageB_astra2_0*.log`, and the Opus replies `stageB_opus_0*.md`.
- **Astra judge: not used.** There was no dispute: both Stage B reviewers verified v4 in their second round.

## 5. Checks that support the numbers

- **Certified computation:** `helpers\witness_certified.py`, with output in `helpers\witness_certified_output.txt`; it is also printed in Appendix A.
- **Independent numerical check by a Sonnet assistant** (`helpers\check_sonnet\`):
  - the general Cholesky formula against the closed forms, on 1,049 models and two block partitions;
  - brute-force enumeration on a reduced analogue;
  - all values agree to 30+ digits.

  Not used as evidence in the proof.
- **Both Stage B reviewers recomputed the witness values independently.** The Opus reviewer also simulated the quoted block rules on the data.
- **Appendix B provenance check:** `helpers\proof_build\check_appendix_B.py` (9/9 passages match).

## 6. Caveats

- **The witnesses are existence results** about the method's objects. They do not claim that a random calibration actually produces those pilot temperatures or that pool. Astra #1 ruled this the right reading of the source's cautions.
- **(iv)(a)'s link to "calibration never scores 𝓜"** carries the provenance proviso of change 2. Felipe may want to fix in the method which scored models feed V.
- **The numerical evidence in the theorem file** was not used.

## 7. Agent and call counts

| Model | Role | Count |
|---|---|---|
| GPT-6 Astra #1 (high), one session `<uuid>` | statement checker + Stage A reviewer | 7 calls: 3 statement checks, 1 review cut off by a session crash and rerun, 1 review of v1, 1 ruling on v2, 1 confirmation of v3 |
| GPT-6 Astra #2 (high), fresh session `<uuid>` | Stage B reviewer | 2 calls: review of v3, ruling on v4 |
| Opus 5.5 (xhigh), native Agent, Plan type, Claude Personal | Stage B reviewer | 1 agent, 2 calls: review of v3, ruling on v4 |
| Sonnet 5.5 | assistant (independent number check) | 1 agent, 1 call |
| Astra judge (xhigh) | — | 0 (not needed) |
| Fable, Sol, Haiku, other Opus | — | 0 |

Lead: Opus 5.5 (high), who also did the operator work.

## Stage C (campaign review, 2026-10-22)

- Final reviewers Fable 5.1 (high) and Astra (xhigh) both hold the proof correct (source: COLLECTED/review/FABLE_STAGE_C_phase2.md). Exposition edits applied: none (no edits; final file unchanged). 
- Result label now: proved (Opus 5.5 lead; independent reviews Astra x2 + Opus xhigh; campaign review Fable 5.1 + Astra: correct); not adopted.
