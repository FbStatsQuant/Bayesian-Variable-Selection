# FINAL REPORT — T01 (A0 = T1) and T02 (A1 = T2), wave 3

**Result:** proved (Opus 5.5 lead; reviewed by 2 independent Opus 5.5 xhigh, CP + CW); not adopted.

**Final proof:** `proof/PROOF_v3.tex`, `proof/PROOF_v3.pdf` (13 pp; SHA-256 tex 626137f4…3250, pdf a29a660a…5c73). The statement is in `STATEMENT.md`.

## What is proved

**T01**
- **(i)** For every valid input, the v3 posterior, rewritten in contrast coordinates (θ = s_yβ, v = s_y²σ²), is exactly the posterior of an (n−1)-dimensional Gaussian regression. Its IG prior has shape 0.51 and the data-dependent rate b₀s_y². Evidences differ by the model-free factor c_n(s_y); Bayes factors and posterior model probabilities coincide. The conditionals of v and θ are stated explicitly.
- **(ii)** An envelope: changing the IG rate within [b₁, b₂] changes every marginal and joint integral by at most κ₁₂ = (b₂/b₁)^{0.51}.
- **(iii)** s_y² concentrates at σ*² + ‖μ‖²/(n−1) at rate n^{−1/2}. The scale event 𝓑_n has probability → 1, with an explicit bound. Uᵀε is exactly N(0, σ*²I_{n−1}).
- **(iv)** The rate derivative of a log Bayes factor.
- **(T)(a)** On 𝓑_n, the v3 posterior of any event is at most κ² times the mixed quantity "numerator at the fixed rate b₋, denominator at the fixed rate b₊".
- **(T)(b)** As a worst case over inputs, a same-rate bound at b₋ or b₊ alone does not control the v3 posterior by any constant factor. (b1) gives witnesses with p = 1 at two fixed rates; (b2) gives witnesses with p = 2 inside 𝓑_n.

**T02**
- **(i)** Π(|S| > m | y) ≤ 2^{−m}(2p)^{s₀}(n+1)^{s₀/2}√n·Θ_{n,m}, with Θ tight uniformly in m. This gives Π(|S| > m_n(ω_n) | y) = O_P(e^{−ω_n}). The proof needs only ‖μ‖²/n ≤ M, λ_min(R_{S₀}) ≥ φ₀² and s₀ ≤ K, and it covers every deterministic ω_n.
- **(ii)** Under SE, Π(S ⊋ S₀ | y) = O_P(√(log n/n)).

**Proof routes.**
- T02(i) uses the mixed-rate transfer: an exact Markov identity at the fixed rate b₋, and a lower bound for the S₀ denominator at the fixed rate b₊.
- T02(ii) needs no envelope. For supersets, the v3 Bayes factor against S₀ is nonincreasing in the IG rate, so its value at the data-dependent rate is bounded by its value at rate 0. Supersets are then summed size by size, using exact chi-square laws and a truncated exponential moment.
- No step treats the errors as Gaussian conditionally on s_y.

**Earlier work reused (re-proved here, not cited):**
- Proposed_project/proofs/T7_T8 §§1–4: the smoother, determinant and prior lemmas, the good event, the dimension lemma and the superset sum.
- Adaptation to v3: noise dimension n−1, normalisation ‖x_j‖² = n−1, IG shape 0.51 at fixed rates, the cap, and self-contained chi-square tails in place of Laurent–Massart.

## Statement changes (approved by the statement checker, Opus 5.5 xhigh; review/STATEMENT_CHECK_R1.md, R1b, R2)

No hypothesis was added or removed, and no conclusion was weakened. Two informal clauses were made precise:
1. **Transfer rule (T).** (a) states the positive content. (b) states the negative content ("same-rate bounds alone do not establish it") as a worst case over inputs:
   - (b1) no data-free implication between two fixed rates;
   - (b2) witnesses inside 𝓑_n.

   (b) is explicitly *not* a statement about P₀. The checker noted that a P₀ version would be false for model events. My first p = 1 form was rejected because its witnesses lie outside 𝓑_n; the p = 2 form fixed that. My phrase "not even a growing factor" was removed because (b₊/b₋)^ν always works.
2. **U is a fixed, non-random matrix.** With a data-dependent U, the exact law in (iii) can fail.

Readings and renamings are in STATEMENT.md §4:
- S′ for the second model in (iv);
- b₁, b₂, κ₁₂ for the generic numbers in (ii);
- model events written {S = ·};
- z^c and Q^c defined from y_c;
- the discipline clause reworded.

## Review outcome

| Round | Proof | CP reviewer (Agent, Plan type) | CW reviewer (delegate_task, Claude Work) |
|---|---|---|---|
| 1 | v1 | verified; 8 exposition findings | verified; 6 exposition findings |
| 2 | v2 (unified exposition revision; review/CHANGES_v1_to_v2.md) | verified; 3 notation findings | verified; 3 notation findings |

- There were no fatal or gap findings in either round, so CLAIMS_OF_FATAL_FLAWS.md records none.
- **v3 differs from the reviewed v2 only by notation fixes** from round 2:
  - 𝖠 in three spots;
  - Lemma 2.2's parameters written 𝔞 and 𝔟;
  - V₁ and V₂ in the Loewner fact;
  - "t_n deterministic" stated in (T)(a).

  This is checked by helpers/make_v3.py, which changes 8 lines. v3 was not re-sent to the reviewers.
- **Judge:** not used.

## Agents and calls

| Role | Agents | Calls / rounds | Account |
|---|---|---|---|
| Statement checker (Opus 5.5 xhigh, Plan type) | 1 | 3 | CP |
| Proof reviewer (Opus 5.5 xhigh, Plan type) | 1 | 2 | CP |
| Proof reviewer (Opus 5.5 xhigh, delegate_task) | 1 per round | 2 | CW |
| Helpers, judge, Fable | 0 | 0 | — |

The lead also ran local single-seed sanity scripts: helpers/check_T01.py (identities to 1e-14, envelope, derivative) and helpers/check_T01_Tb.py (the (T)(b2) example, which converges very slowly).

## Notes for downstream use (T03, T04, T05, T08, T22)

- Use T01(i) to move between the standardised and contrast formulations.
- Bound any v3 posterior event on 𝓑_n by T01 (T)(a). Never transfer a bound proved at a single fixed rate.
- For comparisons between nested models where the larger one has the smaller Q, the monotonicity in the rate (Lemma 8.3 of the proof) removes the rate entirely.
- T02(i) holds for every deterministic ω_n, and it needs no eigenvalue condition beyond S₀.
