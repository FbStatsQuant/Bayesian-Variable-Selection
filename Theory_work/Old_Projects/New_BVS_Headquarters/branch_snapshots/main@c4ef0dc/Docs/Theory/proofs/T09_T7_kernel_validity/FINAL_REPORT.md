# FINAL REPORT — T09 (T7): exact start, invariant kernels and whole-round minorisation

**Result: proved (Opus 5.5 lead; independent reviews: Astra x2 + Opus xhigh; campaign review pending); not adopted.** Adoption is Felipe's word.

- Final proof: `proof/PROOF_v3.tex` and `proof/PROOF_v3.pdf` (7 pages; SHA-256 of the .tex bab55fdf…76ba6, of the .pdf f0d45334…12234).
- Statement: `STATEMENT.md` (source `theorems/T09_T7_kernel_validity.md`, method SHA-256 93043758…8019c, verified at the start).
- Protocol: proof.md with Felipe's run overrides, plus Protocol Amendment 1 and its correction (see STATUS.md).

## 1. What the theorem says, in plain words

SMC-BVS starts its particles from π₀, an easy approximation of the posterior built from small blocks of predictors. It then moves them toward the posterior with a "round" of small random steps: Gibbs flips, two kinds of swaps, and one "independence" step that proposes a fresh draw from π₀. T09 says this machinery is mathematically sound:

- (i) The start's normalising constant is computed exactly by convolution, and the backward sampler draws exactly from π₀.
- (ii) Every single step leaves the bridge distribution q_φ unchanged and is reversible, including the edge cases (the size cap, empty or full models, missing neighbours).
- (iii) A round in a random order is reversible on average, but a round in one fixed order need not be. We give a concrete example of such a fixed order.
- (iv) Because every round contains one independence step, every round, whatever its order, mixes at least at rate ε_φ, the smallest ratio π₀/q_φ. This gives a total-variation bound (1 − ε_φ)^h and a spectral-gap bound ≥ ε_φ.
- (v) ε_φ is only a guaranteed worst-case rate. An exponentially small ε_φ does not prove that the sampler is slow. We show a family of data sets with exponentially small ε_φ, a mode switch along the bridge and a large discrepancy range, where the round still mixes within 55 rounds for every n.

## 2. Statement changes

**No hypothesis was added or changed.** Two informal sentences of the theorem file were written as precise mathematics in STATEMENT.md. The original wording is quoted next to each.

1. (iii) "An individual realised order need not be reversible" became: a fixed-order round is reversible exactly when it equals its reversed-order round, and an explicit instance exists where it is not.
2. (v) "does not establish exponentially slow mixing …" became an existence claim. It is a family (n → ∞, p = 2) with ε₁ ≤ e^{−κn}, discrepancy range ≥ κn and a switch, yet gap ≥ 1/40 and mixing time ≤ 55.

One correction to my own reading was made after Astra #1's round-1 review. My first version said "no lower bound on mixing time that tends to 0", which is wrong; the corrected text says "tends to infinity". The correction is recorded in the STATEMENT.md change log and in CLAIMS_OF_FATAL_FLAWS.md. All three reviewers judged the final readings faithful to the original wording.

**Dependencies:** none were used. The proof is self-contained: it does not assume the project results P1 or P6 or any sibling v3 conjecture. Neither EXP nor EXP′ is needed.

## 3. Proof strategy

- (i) Write the convolution as a sum over block-wise sub-models; the backward sampler's probabilities then telescope to γ₀/Z̄₀.
- (ii) Use a general Metropolis–Hastings lemma, and check for each step that the stated acceptance ratio equals the true Hastings ratio, edge cases included. The neighbour-swap result holds for any neighbour graph under the "read as 0" rule.
- (iii) The adjoint of a product of kernels is the product in reverse order, and reversing is a one-to-one map on orders.
- (iv) The independence kernel satisfies K_ind(S,·) ≥ ε_φ q_φ(·). Steps before it are stochastic and steps after it leave q_φ invariant, so the bound passes to the whole round. A Doeblin lemma then gives the total-variation and gap bounds.
- (iii)/(v) example: an explicit two-predictor design with correlation τ and signal ρ, solved in closed form.
  - The start puts its mass on {1,2}; the posterior puts its mass on {1}.
  - The orders that end with "Gibbs 1, Gibbs 2" reach {1} from anywhere with probability ≥ 1/2. Those orders make up 1/20 of all orders, so every round lands at {1} with probability ≥ 1/40.
  - A remark shows that any prescribed exponential rate can be reached by taking τρ close to 1.

## 4. Review history

| Stage | Reviewer | Version | Verdict | Findings |
|---|---|---|---|---|
| A, round 1 | Astra #1 (gpt-6-astra high, session <uuid>) | v1 | not verified | 1 fatal (my wrong gloss in the reading of (v)); 1 exposition (0/0 notation). Both accepted and fixed in v2. |
| A, round 2 | Astra #1 (same session) | v2 | **verified** | both findings ruled resolved; no new findings |
| B, round 1 | Astra #2 (gpt-6-astra high, new session <uuid>) | v2 | **verified** | none |
| B, round 1 | Opus 5.5 xhigh (native agent, Claude Personal, read-only) | v2 | **verified** | 7 exposition (F1 graded "borderline gap": prescribed rates). All accepted; unified revision v3. |
| B, round 2 | Astra #2 | v3 | **verified** | agrees with all answers; 1 new exposition finding (argmax braces) |
| B, round 2 | Opus 5.5 xhigh | v3 | **verified** | agrees with all answers; 3 new exposition findings (notation clashes N1–N3) |

- CLAIMS_OF_FATAL_FLAWS.md holds the one fatal finding verbatim with my answer, and the borderline F1. Every reviewer who saw the log agreed with the answers and with the fixes.
- **Astra judge: not used.** No dispute remained.
- **Open exposition notes on PROOF_v3:** all notation only; no reviewer found any effect on the mathematics. They are not applied, so that the final text is exactly the one all reviewers checked.
  - The rate symbol K₀ clashes with the cap K and the kernels K_φ.
  - The vectors h₁, h₂, h₃ clash with the step count h.
  - Subscript 1 means both the state {1} and φ = 1.
  - R means both the correlation matrix and the ratios R₁, R₂.
  - "w(1) = w(1)" should say "both singletons have the same prior weight".
  - "argmax = {1,2}" should read "the unique maximiser is {1,2}".

  Fixing them is a five-minute copy-edit for the campaign document.

## 5. Numerical sanity check (not evidence of proof)

A Sonnet assistant independently implemented the objects and checked them numerically on one seed, locally (`helpers/numcheck/REPORT.md`).
- Generic instance n = 12, p = 5:
  - convolution and sampler exact to about 1e-16;
  - every step kernel reversible to about 1e-17;
  - the "read as 0" rule needed for non-symmetric graphs;
  - the averaged round self-adjoint;
  - minorisation holds for 200 random orders.
- Two-predictor family at n up to 400: the switch, exponentially small ε₁, gap near 1, and K_σ(∅,{1,2}) → 1 while the reversed order gives → 0.
- Consistent with every claim.

## 6. Agent and call counts

| Model | Agents | Calls | Role |
|---|---|---|---|
| Opus 5.5 (lead, this session) | — | — | mathematics, LaTeX, packets, Astra operation |
| GPT-6 Astra, high: Astra #1 | 1 session | 3 (call 1 failed with "model at capacity" before reviewing; one retry by resuming the same session, then round 2) | Stage A reviewer |
| GPT-6 Astra, high: Astra #2 | 1 session | 2 | Stage B reviewer |
| GPT-6 Astra, xhigh: judge | 0 | 0 | not needed |
| Opus 5.5, xhigh | 1 | 2 (review + one SendMessage for rulings) | Stage B reviewer |
| Sonnet 5.5 | 1 | 1 | numerical check |
| Haiku 5.5 | 0 | 0 | — |
| Fable | 0 | 0 | — |

Totals: 5 Astra calls (4 successful), 2 Opus reviewer calls, 1 Sonnet call.

## 7. Files and clean-up

- STATEMENT.md
- proof/PROOF_v1–v3 (.tex, .pdf)
- review/: every Astra log and reply, both Opus replies, and the v2→v3 change list
- helpers/numcheck/
- CLAIMS_OF_FATAL_FLAWS.md
- STATUS.md

The temporary packet folders under `<PC_TEMP_PATH>` were deleted at the end of the run, after every reply had been copied into review/.

## Stage C (campaign review, 2026-10-22)

- Final reviewers Fable 5.1 (high) and Astra (xhigh) both hold the proof correct (source: COLLECTED/review/FABLE_STAGE_C_phase2.md). Exposition edits applied: none (no edits; final file unchanged). 
- Result label now: proved (Opus 5.5 lead; independent reviews Astra x2 + Opus xhigh; campaign review Fable 5.1 + Astra: correct); not adopted.
